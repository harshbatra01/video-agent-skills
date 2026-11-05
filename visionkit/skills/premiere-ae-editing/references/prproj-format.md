# Premiere .prproj internals (Premiere Pro 2026, v26.5; Premiere 2025, v25.6, where marked)

Read this before changing a project by text. Code for common jobs: `prproj-recipes.md`. Library: `scripts/prproj/prproj_lib.py`.
Everything here was seen in real projects; "verified" means a built file was opened in Premiere and checked. The format
is the same on Windows and Mac except where a line says "Mac" (seen in Premiere 25.6 and 26.5 projects on the Mac port).

## Contents
1. File and objects
2. Time
3. Where things live (object graph)
4. Track items
5. Media objects
6. Effects, params, keyframes
7. Lumetri
8. Masks
9. Graphics and text (Essential Graphics)
10. Captions and transcripts
11. Audio
12. Tracks and sequences
13. Bins and labels
14. Binary blobs
15. Deleting safely
16. What Premiere changes on load and save
17. Validation checklist

## 1. File and objects
- `.prproj` = gzip of UTF-8 XML with LF line endings. `python prproj_lib.py unpack X.prproj X.xml` gives readable text.
- Top-level children of `<PremiereData>` are objects with `ObjectID="123"` (referenced by `ObjectRef="123"`) or
  `ObjectUID="guid"` (referenced by `ObjectURef="guid"`). Each object is one block starting `\n\t<Tag ObjectID=...>` and
  ending `\n\t</Tag>`. Edit whole objects as text (`Doc.raw`, `Doc.replace_obj`) so everything else stays byte-identical.
- New objects: next free ObjectID (`Doc.new_id`), new GUIDs for UIDs, ClipIDs and FileKeys, appended before
  `</PremiereData>` (`Doc.append`). Order of objects in the file does not matter, except for blob data (section 14).
- Premiere RENUMBERS ObjectIDs on every save. Find templates by content (MatchName, names, file paths), never by an id
  remembered from an earlier save. The Project object's nested `ObjectID="2"` shows as "unresolved" in a top-level-only
  check: harmless.
- The parse tree goes stale the moment you edit text. `prproj_lib` reads live text for every lookup; if you write your
  own code, re-read lists (track items, tracks) from `doc.raw(...)`, not from an old parse.

## 2. Time
- 254016000000 ticks per second (`TPS`). Frame ticks: 23.976 = 10594584000, 24 = 10584000000, 25 = 10160640000,
  29.97 = 8475667200, 30 = 8467200000, 50 = 5080320000, 59.94 = 4237833600, 60 = 4233600000. One 48 kHz sample = 5292000.
- Track item `<Start>`/`<End>` = sequence time. Clip `<InPoint>`/`<OutPoint>` = media time. Every keyframe = the clip's
  MEDIA time (seq time - item start + in point, times speed).
- Premiere omits `<Start>` when it is 0, and omits `<InPoint>` 0 in some objects. Code must treat "missing" as 0.
- `StartKeyframe` time `-91445760000000000` means "static value".
- Adjustment layers and synthetic graphics media start at 1 hour of media time (914457600000000 = `ADJ_IN`).
- Snap Start/End to the SEQUENCE frame grid (`on_frame(sec, fps)`); audio positions rounded to 48 kHz samples load fine.
- ClipLoggingInfo TimecodeFormat: 23.976 = 110, 24 = 100, 25 = 101, 29.97 = 103, 30 = 104, 60 = 108.

## 3. Where things live (object graph)
```
Project > RootProjectItem > Items (bins, clips, sequences as ProjectItems)
BinProjectItem > ProjectItemContainer > Items > ClipProjectItem (the bin entry, has the bin Name + label)
ClipProjectItem > MasterClip (UID) > Clips: VideoClip / AudioClip (master instances), LoggingInfo, AudioComponentChains
VideoClip > Clip > Source > VideoMediaSource > Media (UID: FilePath, Title...) > VideoStream / AudioStream
Sequence (UID, <Name>) > TrackGroups > TrackGroup > Second > VideoTrackGroup / AudioTrackGroup / DataTrackGroup (captions)
VideoTrackGroup > Tracks > Track (UID) = VideoClipTrack > ClipItems > TrackItems > TrackItem refs
                                                       > TransitionItems > TrackItems > transition refs (separate list!)
VideoClipTrackItem > ClipTrackItem > ComponentOwner > Components (VideoComponentChain) > Component refs (effects)
                                   > TrackItem (Node ID, Start, End) > SubClip > Clip (instance: InPoint, OutPoint,
                                     PlaybackSpeed, ClipID) > Source > ... Media
```
- A sequence used inside another sequence is a nested clip: its Clip's Source is a `VideoSequenceSource` pointing at the
  Sequence UID.
- `python prproj_dump.py X.prproj > dump.txt` prints every sequence, track, item (time, media, in/out, speed, effects with
  keyframe counts, masks, graphic text), audio gains, transitions, captions and the media list. Read the dump, not the XML.
  (Windows) Set `PYTHONIOENCODING=utf-8` before redirecting it: names with emoji crash a redirected dump (cp1252).
  `--own-names` (the default on a Mac) heads each sequence with its own `<Name>` and adds the bin item's name when the
  two differ.

## 4. Track items
- Child order Premiere writes: Node/ID, Start, End. Keep it when retiming (`set_times`).
- `<IsMuted>true</IsMuted>` right after the item's `<SubClip .../>` = clip DISABLED (the "disable, never delete" rule).
  Works on caption items too. Track-level mute is a separate flag on the track.
- A track lists clips in `<ClipItems><TrackItems>` and transitions in `<TransitionItems><TrackItems>`. Read and write ONLY
  the clip list (`clip_item_ids`, `set_track_items`), or a transition gets pulled into the clip list.
- Empty track: insert `<TrackItems Version="1">...</TrackItems>` before `<MediaType>` inside that track's `<ClipItems>`.
- Clip lists are in time order (`set_track_items` sorts by start).
- CLONING an item (verified 7 Oct 2026): the copy must lose `<HeadTransition>`/`<TailTransition>` refs and get a unique
  `<Node><ID>` number. A clone that kept the template's HeadTransition was drawn at the TEMPLATE's time and never at its
  own. `prproj_lib._fresh_item` does both.
- An item whose in/out runs past the end of its media shows diagonal hatching in the timeline (no picture there).
- Speed: `<PlaybackSpeed>` in the clip instance (0.5 = half speed); media length = sequence length x speed.

## 5. Media objects
- Media (UID): `FilePath`, `ActualMediaFilePath`, `RelativePath` (from the project folder: `.\...` in a Windows save,
  `./...` or `../...` in a Mac save; can appear twice),
  `Title`, `FileKey` (GUID), `ImplementationID` (1fa18bfa-255c-44b1-ad73-56bcd99fceaf for normal files), `CCFileModTime`
  (file mtime in MICROseconds), optional `ModificationState` / `ContentAndMetadataState` (drop them when relinking).
- Streams: `VideoStream` (FrameRate = frame ticks, Duration ticks, FrameRect "0,0,w,h", CodecType 1635148593 = avc1,
  OriginalColorSpace JSON), `AudioStream` (FrameRate = sample ticks, Duration, AudioChannelLayout, maybe
  ConformedAudioPath / PeakFilePath: drop those when the file changes so Premiere rebuilds peaks).
- RELINK (verified on a delivered client round): change the Media paths + Title + FileKey + mod time, update stream
  Duration when the new file's length differs, rename clip names that equal the old file name. Every in/out, effect and
  keyframe on the timeline survives. `relink()`.
- IMPORT an H.264 .mp4 by text (`import_mp4`, output matches what Premiere writes field for field): ClipProjectItem >
  MasterClip (LoggingInfo, Clips, AudioClipChannelGroups; + AudioComponentChains and DefMappingID only with audio) >
  VideoClip (+ AudioClip with SecondaryContents per channel) > MediaSources > Media > streams. 44.1 kHz audio needs
  `<FrameRate>5760000</FrameRate>` in the AudioComponentChain (48 kHz = 5292000 is the default). Video-only files: one
  Clip and an empty ClipChannelGroupVectorSerializer.
- ProRes / alpha .mov (After Effects renders) or any non-H.264 file: import it in Premiere (window: Ctrl+I, type the
  full path; bridge: `importFiles` into a copy, premiere-ui.md), save, close, then work on that save and find the clip
  with `master_by_name`. Alpha works on the top track.
- `RelativePath` differs by the machine that SAVED the project. Windows: `.\file.mp4` from the project folder. Mac:
  `./sub/file.mp4` at or below the project folder and `../x/file.mp4` above it, and Premiere double-escapes `&` there
  (`&amp;amp;`); `FilePath` / `ActualMediaFilePath` are absolute POSIX paths. Projects travel between the Windows PC and
  the Mac, so prproj_lib follows the PROJECT, not the machine it runs on: `path_style(doc)` reads the project's
  own media `<FilePath>`s in the text as it was OPENED (so a batch of relinks never flips it halfway): `C:\...`,
  `C:/...`, `\\server\...` and `\\?\C:\...` count as Windows, paths starting with `/` (`/Users/...`, `/Volumes/...`)
  as Mac; the majority wins and synthetic numeric paths (adjustment layers, bars) do not count. `relink()` /
  `import_mp4()` then write that `<RelativePath>` form (`rel_path()` for Mac-style projects, with `/` even when the edit
  runs on Windows; `.\` for Windows ones). Force it per call with `style='win'` / `'mac'` or for a whole run with
  `prproj_lib.PATH_STYLE = 'win'` / `'mac'` (any other value is refused); a project with no media paths (or a tie)
  falls back to the machine. `FilePath` is always the real path on the machine doing the edit (the file must exist
  there), and Premiere looks there first. Still per machine, not per project: `STRICT_CLONE` (on by default on a Mac,
  prproj-recipes R6) and `import_mp4` making its path absolute on a Mac.
- A project from another machine (a Windows editor's project with media on E:\ opened on the Mac) opens with every clip
  offline. In a copy, rewrite ActualMediaFilePath, FilePath, ConformedAudioPath and PeakFilePath to the new folder
  (those projects had no RelativePath). Right after opening, `isOffline()` reads true for most items until Premiere has
  checked the files: check again a moment later before relinking.
- Colour space override (log footage): `<OverriddenColorSpace>` + `<InputLUTSpecified>true` + `<IsColorSpacOverridden>true`
  inside the media's VideoStream. Copy the exact value from a clip the user already overrode.

## 6. Effects, params, keyframes
- A track item's chain lists components (effects) in order. MatchNames seen: `AE.ADBE Motion` (intrinsic Motion: Position,
  Scale, Scale Width, Uniform Scale, Rotation, Anchor Point, Anti-flicker Filter, Crop Left/Top/Right/Bottom),
  `AE.ADBE Opacity`, `AE.ADBE Lumetri`, `AE.ADBE Geometry2` (Transform: zooms), `AE.ADBE AEMask2` (mask sub-component),
  `AE.ADBE Gaussian Blur 2`, `AE.ADBE Tint`, `AE.ADBE Ultra Key`, `AE.Impact_Blur_FX` (third-party), `AE.ADBE Text`,
  `AE.ADBE Shape`, `AE.ADBE Graphic Group`.
- Premiere DROPS an all-default Motion (and Opacity) component on save: many clips have none. To place a clip with
  your own Position/Scale, use as template an item that HAS a Motion component (one the user moved or scaled).
- Param value = `<StartKeyframe>time,value,...</StartKeyframe>`. `<CurrentValue>` is a stale UI cache: ignore and drop it.
- Motion Position / Anchor are frame-normalized "x:y" (0.75:0.25 shows as 1440, 270 in a 1080p Effect Controls).
- Keyframes: `<Keyframes>` list after StartKeyframe. Scalar "t,v,interp,0,inSpeed,inInfl,outSpeed,outInfl;"
  (interp 0 linear, 5 bezier). Point "t,x:y,interp,0,inSpeed,inInfl,outSpeed,outInfl,5,4,inTx,inTy,outTx,outTy;".
  Video params also carry `<IsTimeVarying>true</IsTimeVarying>`; AUDIO params never do (Premiere writes keyed audio
  Level params without it). `kf_scalar`, `kf_point`, `kf_audio`, `set_keys`.
- Effects copied from other projects or presets carry their keyframes (a blur fading 10 to 0, a Tint flash): strip
  Keyframes + set IsTimeVarying false on every param you do not animate yourself (`clone_component(strip_keys=True)`).
- Cloning a template's Motion copies ALL its values, including crops (seen: a clone inherited Crop Right 51 %).
  `place_video_item` resets Motion to defaults before your overrides.
- Colour params: effect colours (Tint) are 64-bit `A<<56 | R<<40 | G<<24 | B<<8` (`color64`); graphics JSON colours are
  0xRRGGBB ints; `asl.clip.label.color` ints look BGR.

## 7. Lumetri
- `AE.ADBE Lumetri`, about 130 params. Sliders are plain numbers; curves and wheels are ArbVideoComponentParam blobs of
  little-endian doubles (clone them, do not write them).
- Param indexes used: 14 Temperature, 15 Tint, 16 Saturation, 19 Exposure, 20 Contrast, 21 Highlights, 22 Shadows,
  23 Whites, 24 Blacks, 40 Faded Film, 41 Sharpen, 42 Vibrance, 43 Creative Saturation, 110 Vignette Amount.
- Grades lived on adjustment layers (one per look, cut around B-roll), cloned from the reference grade with per-shot slider
  overrides: `clone_component(doc, lumetri_id, {19: 0.7, 16: 105})`. See `grading.md`.

## 8. Masks (effect masks, verified 26.5)
- A mask is a SubComponent of the effect: VideoFilterComponent MatchName `AE.ADBE AEMask2`, DisplayName "Mask2",
  InstanceName "01".."NN", listed in the effect's `<SubComponents>` + `BE.VideoFilterComponent.NextComponentNumber`.
  Clone a mask that already exists in the project (find it by MatchName).
- Params: Path blob (`mask_path_blob`: u32 2, u32 1, u32 31062, u8 0, u32 2, u32 n, n x (u32 1, 6 float32 x, y, inX,
  inY, outX, outY absolute, normalized to the layer frame), u8 closed), Position / Anchor normalized "x:y", Scale Width /
  Height %, Rotation, Feather, Opacity, Expansion, ParameterID 17 = Inverted, Type 1 = "Ellipse Mask" (ONLY works with
  4 vertices; 8 vertices made the effect hit the whole frame).
- Point keyframes on mask Position work, so tracked masks can be written directly (numbers from your own tracker).

### Premiere 2025 masks (Mac port, meme compilation edits, verified in 25.6.6)
- Premiere 2025 projects (and Windows editors' 25.0 projects opened on a Mac) store a Gaussian Blur mask as a
  `VideoFilterComponent` with MatchName `AE.ADBE AEMask` (DisplayName "Mask") and 24 params, not the 2026 `AEMask2`.
  The Mask Path is a base64 "2cin" blob: header `2cin`, u32 2, u32 0, u32 n, then per vertex u32 0 + three xy float32
  pairs (point and both tangents, equal for straight edges) + u32 1, in TL, TR, BR, BL order, normalised to the source
  image.
- An animated path = `<Keyframes>ticks,base64;...` plus `IsTimeVarying` true. `StartKeyframeValue` needs a BinaryHash
  attribute: without it Premiere silently drops the path; a random unique 12-byte hash with the length suffix (`%08x` of
  bytes + 12) loads fine and Premiere rewrites it on save (section 14).
- Mask feather is in the image's own pixels (it scales with the clip), Expansion 0, and the blur's Repeat Edge Pixels on
  matched the human editor's masks.
- `scripts/prproj/prproj_masks.py` writes these: `Project(path).add_mask(gaussian_blur_component_id, box=[x0, y0, x1, y1]
  or a four-corner outline [[x, y] TL, TR, BR, BL], keys=[(media_seconds, box), ...], feather=10)`, then
  `save(new_path)`. Its template (`mask_template_pp2025.xml`) is one mask exactly as Premiere 2025 saved it; set
  `PRPROJ_MASK_TEMPLATE` to another project to clone from that instead. Its output was byte-identical to the version
  used on the real jobs. The four-corner outline lets a box follow slanted text (a shop sign in a photo).
- Solid black boxes over words: a Tint effect (Map Black To and Map White To = black, Amount 100) with a patched mask,
  feather 0.

## 9. Graphics and text (Essential Graphics)
- A timeline graphic = VideoClipTrackItem > SubClip > VideoClip (`<AdjustmentLayer>true`) > VideoMediaSource > synthetic
  Media (FilePath 1196574294, ImplementationID 42008e7a-..., own hidden MasterClip, no ClipProjectItem). Layers are
  components in the clip chain: `AE.ADBE Text` (22 params), `AE.ADBE Shape` (18 params).
- The FIRST component draws ON TOP: put background shapes last.
- Text p0 Source Text blob = uint64 LE byte length + UTF-16LE JSON {"mTextParam":{..."mStyleSheet":{"mFontName",
  "mFontSize","mFillColor","mTracking","mText"...}}} (legacy format; Premiere 26 still reads it, writes binary itself).
  Text p2 Position / p8 Anchor frame-normalized; with Anchor 0:0 Position is the baseline-left point of left text.
- Shape p0 Path blob = u32 2, u32 n, n x 7 float32 [0,x,y,inx,iny,outx,outy], u8 closed; p1 Appearance JSON
  {"mStyle":{mFillColor,mStrokeColor,...}}; p4 height scale, p5 width (when p6 uniform = false); Anchor p9 = point/size.
- A normal title's VideoClip must NOT carry `<AdjustmentLayer>true` in the track instance (Mister Horse templates do;
  with it the text never draws). Graphics blend in linear light: 86 % opacity looks see-through, use about 97 % for a
  solid card.
- When the user moves or scales a graphic with Motion, Premiere stores an explicit `AE.ADBE Motion` component inside the
  graphic's chain: a graphic the user positioned is a good Motion template.
- Real templates: Adobe's own mogrts (Windows `C:\Program Files\Adobe\Adobe Premiere Pro 2026\Essential Graphics\*.mogrt`,
  Mac `/Applications/Adobe Premiere Pro 2026/Adobe Premiere Pro 2026.app/Contents/Essential Graphics/*.mogrt`; zip of
  definition.json + project.prgraphic, itself a zip holding a .prproj), and the user's own template project if they
  keep one (ask: CTA cards with text, shapes and a keyed audio Level were the best source on one job).
- When animation or design matters, render the graphic in After Effects instead (alpha .mov on a top track). Premiere
  graphics by text are for simple titles, plates, code cards.
- prproj_lib has no text setter yet: to change a title's words, clone a graphic the user made and write its Source Text
  blob in the legacy JSON form above with `set_blob` (Premiere 26.5 read it: font, size, tracking and shadow all
  loaded), or render the title in After Effects.

## 10. Captions and transcripts
- Captions: `CaptionDataClipTrackItem` on a DataTrackGroup track > Block > FormattedTextData (FlatBuffers; the text is a
  length-prefixed string after the font name). Disable instead of deleting (IsMuted). Styling them (font, size, box,
  height) by patching those blobs: `captions-style-patch.md` (one wrong field type crashed Premiere on open). All other
  caption mechanics: `captions.md`.
- Caption tracks always draw ABOVE every video track. So grades and zooms on adjustment layers never touch captions
  (safe to add), but any graphic on a video track sits UNDER the captions: disable the caption words that collide.
- Deleting captions you made: unlink from the track list, then reference-count garbage-collect its chain (DataComponentChain,
  Block, SubClip, TranscriptClip, DataMediaSource, the caption's own MasterClip / ClipLoggingInfo / Media / DataStream)
  with counts taken BEFORE deleting, then move FormattedTextData blob data to the first remaining use.
- Transcripts: `TranscriptData` FlatBuffers. Word table [soffset vtable][uoffset to string][float32 conf][int64 start]
  [int64 dur](optional 4-byte pad)[u32 len][utf8]; follow the uoffset (assuming the string follows dur loses half the
  words). `prtranscript.py`. Sequence markers: `<Marker>` First/Second pairs + `<DVAMarker>` JSON {mMarkerID,
  mStartTime.ticks, mType "Comment"}.

## 11. Audio
- AudioClipTrackItem > AudioComponentChain + SubClip > AudioClip instance (In/Out, SecondaryContents per channel).
  Essential Sound tag "dialog" sits in TrackItem Properties.
- Volume "Level" param stores `10 ** ((dB - 15) / 20)`: 0 dB = 0.1778, -10 dB = 0.05623, -24 dB = 0.011221.
  Keyframes "ticks,value,0,0,0,0.1666...,0,0.1666...;" in media time, no IsTimeVarying (`set_level_keys`).
- Clip level without a Volume component: `<Gain>linear</Gain>` after `<AudioChannelLayout>` in the AudioClip instance
  (Audio Gain; 2.5119 = +8 dB; shows as "Gain" in the clip tooltip) (`set_clip_gain`).
- A new clip needs a DefaultVol chain (`<DefaultVol>true</DefaultVol>`, no components). Projects that came in through
  FCP XML have none (every clip got a Volume component), so `place_audio_item` falls back to the exact chain Premiere
  writes. Never clone a chain that holds components: they would be shared between clips.

## 12. Tracks and sequences
- Insert a video track: new VideoClipTrack (Index appears 3 times inside it, ID = the group's NextTrackID), bump Index
  of tracks above, rewrite the VideoTrackGroup `<Tracks>` list + NextTrackID, append `{"mNumber":-1,"mState":0}` to the
  sequence's `HSL.TimelinePatchingAndTargeting.VideoPatches`. Audio: same, plus deep-clone the track's own Components and
  Panner objects, and AudioPatches. `add_video_track`, `add_audio_track` (verified).
- Sequence frame size and rate: VideoTrackGroup `<FrameRect>` and `<FrameRate>`.
- Adding several tracks in one run: read the live track list again before each add and use an ORIGINAL empty track as
  the template (a stale parsed tree gave two new audio tracks the same index).
- In `re.sub` replacements that put an id right after a group, write `\g<1>`, never `\1`: `r'\1%s' % uuid` becomes
  group 13 when the uuid starts with "3", and the regex breaks.
- The order of a track's own `<ID>` and `<Index>` varies, and it is not a Mac difference: inside a track's
  `<Track Version=..>` block Mac projects and most Windows ones write `<ID>`, `<MediaType>`, `<Index>` (134 of the 221
  project files on the Windows PC, 14 Oct 2026); 86 write `<MediaType>`, `<Index>`, `<ID>`; 1 had no tracks. Code
  that sets a track ID must match either order: `_set_track_id` finds the one numeric `<ID>` in the Track block, and
  prproj_lib uses it on every machine (since 14 Oct 2026). Before that, `add_video_track` stopped with "track template
  not understood" on `<ID>`-first projects and `add_audio_track` silently gave the new track the template's ID (two
  tracks, one ID).
- An audio track also has its own UUID `<ID>` in `<AudioTrack>`, right after its Panner or after a `<FrameRate>` there
  (1,916 of 8,233 audio tracks on the Windows PC had the second layout, all in `<ID>`-first projects: 99 of the 134).
  The old pattern missed that layout and the new track kept the template's UUID; `add_audio_track` now handles both
  and stops loudly if it finds neither.
- Tested on copies of 10 real projects (3 `<Index>`-first, 7 `<ID>`-first): on `<Index>`-first projects the track edits
  are byte-identical to the old code, every other edit (clone, relink, import_mp4, bins) is byte-identical everywhere,
  and the 7 `<ID>`-first projects now get unique track IDs and UUIDs (validate_struct clean). Not yet opened in
  Premiere after the fix: open one track-edited copy before relying on it.
- A sequence cloned and renamed by script (`seq.clone()`, `seq.name = ...` through the bridge) changes the Sequence's
  own `<Name>` but not its bin ClipProjectItem name (seen on the Mac; Windows auto-saves show the same split: 1,524 of
  2,513 sequences had a bin name that differs from their own name). Find sequences by the Sequence `<Name>`
  (`find_sequence` does); `prproj_dump.py --own-names` shows both ("[bin item ...]").

## 13. Bins and labels
- A bin is a BinProjectItem whose ProjectItemContainer lists Item refs; the root lists top-level items. A clip sits in
  exactly one container (`new_bin`, `add_to_bin`). Import into a new bin by UI: Ctrl+Shift+A (Cmd+Shift+A) first
  (deselect) or the import lands inside the selected bin.
- Label pairs seen: LabelColors.1 = 6769408 (default video), .3 = 8851829, .5 = 19005, .6 Rose = 10776567 (used to make
  external clips stand out).

## 14. Binary blobs
- Blobs (`StartKeyframeValue Encoding="base64" BinaryHash="..."`, `PremiereFilterPrivateData`) are stored inline only at
  the FIRST element carrying a given BinaryHash; later ones are empty references. Clones must reference (`strip_inline`),
  and after deleting objects each hash's data must sit at its first remaining occurrence (`normalize_blobs`).
- BinaryHash = 24 hex + 8 hex (blob length + 12). The hash is no known algorithm, but Premiere 26.5 accepts invented
  random hashes (`new_hash`, `set_blob`).
- A reader must index EVERY element that carries a BinaryHash, not only StartKeyframeValue: one that did not returned
  blank caption text.

## 15. Deleting safely
- Delete only what YOU placed (the user's things get IsMuted). Remove the item from its track list, then the item,
  SubClip, clip instance, chain, components, params, sub-components and audio SecondaryContents (`delete_item`). Never the
  shared MasterClip, MediaSource or Markers. Then `normalize_blobs` and `validate_struct.py`.

## 16. What Premiere changes on load and save
- Renumbers ObjectIDs; drops all-default Motion/Opacity components; re-numbers duplicate Node IDs; rewrites Position with
  long decimals (0.40325:0.68759300000000001, not a loss); may upgrade captions to Graphics (items without SubClip or
  Components); marks a freshly opened externally-built project "Edited". None of this is damage.
- Opening a project you built: if it loads with no dialog, the structure is accepted. Then check pictures (premiere-ui.md).
- Project files built from one another share internal IDs and sequence GUIDs: tell the user to close one before opening
  the other, because Premiere can confuse identical sequence IDs across open projects.

## 17. Validation checklist (run every time)
1. `python validate_struct.py original.prproj new.prproj`: no duplicate ids, no NEW unresolved refs, no blob used before
   its data, no new orphans, new media files exist.
2. `python prproj_dump.py new.prproj` and compare the changed sequence against the original dump (diff the two dumps).
3. Semantic checks, one PASS / FAIL line each (write them per job; validate_struct.py checks that references resolve,
   not what they point at): every SubComponent ref points at a VideoFilterComponent with MatchName `AE.ADBE AEMask2`,
   Component refs at a *Component, Param refs at a *Param, TrackItem refs at a *TrackItem, SubClip refs at a SubClip;
   fingerprints of every caption and audio track unchanged unless you changed them; V1 and the zoom tracks unchanged;
   B-roll as planned; grade pieces plus B-roll tiling the timeline exactly; zoom % per segment within the plan; graphic
   texts as intended. Why: a build passed the structure check and Premiere still said "could not be loaded, may be
   damaged or contain outdated elements": a mask template id hard-coded from an earlier save had been renumbered, so the
   masks pointed at the wrong object. Check that every ref points at the right kind of object.
4. When Premiere refuses a project and gives no log: build variants that each leave ONE new feature out, open each, and
   diff a generated object against one Premiere wrote itself.
5. Open in Premiere and look at every changed time (premiere-ui.md). A structurally valid file can still draw wrong (the
   HeadTransition clone case looked perfect in the timeline and drew at the wrong time).
