# Premiere recipes (prproj_lib)

Every recipe: open the user's LATEST save read-only, edit in memory, save a NEW versioned file next to it, validate,
then check it in Premiere. Format details and the reasons behind each step: `prproj-format.md`.
Tested: on Windows a scratch project with new tracks, placed clips, SFX, an imported mp4 and a new bin opened and drew
correctly in Premiere 26.5 (7 Oct 2026); on the Mac R1-R3 and R5-R9 ran on a copy of a real project (11 Oct 2026,
validator clean, dump diff as intended; that build was not opened in Premiere because the user's projects were open).

```python
import sys, os
SKILL = os.path.expanduser('~/.claude/skills/premiere-ae-editing')
sys.path.insert(0, os.path.join(SKILL, 'scripts', 'prproj'))
from prproj_lib import *
SRC = '/job/Show.prproj'                    # the user's latest save (check the Auto-Save folder for newer ones first)
OUT = '/job/Show v2.prproj'                 # new version; Doc.save refuses to overwrite SRC (C:/job/... on Windows)
doc = Doc.open(SRC)
seq = find_sequence(doc, 'Main edit')       # exact name, or a unique part of it
V, A = tracks(doc, seq, 'video'), tracks(doc, seq, 'audio')   # index 0 = V1 / A1
...
doc.save(OUT)
# python validate_struct.py SRC OUT   and   python prproj_dump.py OUT > after.txt
```
Look around first: `for ti in clip_item_ids(doc, V[0]): print(item_info(doc, ti))` gives start/end ticks, in/out,
speed, clip name, media title and path, muted state. `components(doc, ti)` lists its effects.
- Before copying a recipe from a reference sequence, check which of its layers are DISABLED (`<IsMuted>`): a
  reference's zoom layers on V2 were disabled, so only V3 rendered, and the measured zooms matched no keyframes until
  this was found. Copying the disabled layers too would have doubled the zoom.
- Small inspectors are worth writing per job when the dump is not enough: clip gain dB, Volume dB and muted state per
  audio item; a title's component params; the colour-override fields per media; every Lumetri on every item with its
  sliders; a timeline JSON per save to diff the user's edits (R16). One job's versions ship in the kit library:
  `~/VisionKit/kit/library/pipelines/ad-build-kit/prproj/` (`audio_dump.py`, `title_dump.py`, `media_cs.py`,
  `lum_inventory.py`, `tl_dump.py`) and `ad-build-kit/work/skin_measure.py` (median Lab of warm skin pixels in a box).
  They use that job's older Doc class: port what you need onto prproj_lib and test it on a copy first.
Building several projects in one Python run: keep every `Doc` you open alive until the run ends (or use one process per
project). The clone Node-ID counter is keyed by the Doc object's id, which Python can hand to a new Doc once an old one
is freed, and a stale counter can repeat Node IDs.

## R1. Swap shots for new renders (keep every edit)
The user re-cut your shots, added effects, trimmed: relink instead of rebuilding.
```python
for old, new in {'B1_01_S01.mov': '/job/renders/v7/B1_01_S01_v7.mov'}.items():
    relink(doc, old, new, project_dir=os.path.dirname(OUT))
```
New render longer than the old one? Extend the item too (R2). Same length: nothing else to do. A re-rendered overlay
under a NEW file name: swap it in place instead (R25). The `<RelativePath>` it writes follows the project's own path
form, so a Mac-saved project relinked on Windows stays Mac-style: `path_style(doc)` says which form a project uses,
`style='win'` / `'mac'` forces it for one call and `prproj_lib.PATH_STYLE = 'win'` / `'mac'` for the whole run
(prproj-format.md section 5).

## R2. Extend or trim an item (and its media out point)
```python
ti = items_for_media(doc, find_media(doc, 'B11_08_END_v7.mov')[0])[0]
set_item_end(doc, ti, s2t(645.0))            # tail moves, media in point stays
retime_item(doc, ti, s2t(600.0), s2t(645.0))  # move/trim both ends (media under the first frame shifts with start)
```
Check the media is long enough (`media_duration_ticks(path)`), or the tail shows hatching (no picture).

## R3. Volume automation and clip gain
```python
set_level_keys(doc, music_ti, [(625.3, -24.0), (626.8, -16.0)])   # (sequence seconds, dB); clip needs a Volume param
set_clip_gain(doc, sfx_ti, -6.0)                                   # Audio Gain on the clip instance
```
`level_param` raises if the clip never had a volume set (DefaultVol): use clip gain, or ask the user to set a level once.

## R4. Change one effect value (find it by MatchName, never by id)
```python
for kind, cid, _, body in doc.objects('VideoFilterComponent', 'AE.Impact_Blur_FX'):
    set_value(doc, param_id(doc, cid, 'Amount'), '0.')            # numbers or raw strings ('0.5:0.5' for points)
c = find_component(doc, ti, 'AE.ADBE Motion'); set_value(doc, param_id(doc, c, 'Scale'), 110)
```
Keep the effect (value 0) instead of removing it: the user may want it back.

## R5. Disable instead of delete
```python
disable_item(doc, ti)        # IsMuted true; works for captions; enable_item() undoes it
```
Use it whenever new material replaces the user's clip, caption or music.

## R6. Copy an existing clip somewhere else
```python
nid, objs = clone_item(doc, ti, s2t(20.0), s2t(23.0))               # same sync (adjustment layers, same take in sync)
nid, objs = clone_item(doc, ti, s2t(20.0), s2t(23.0), src_in=0)     # same shot from its media start
doc.append(objs); add_to_track(doc, V[1], [nid])
```
Clones keep effects, masks and keyframes (overrides: `overrides_by_comp={0: {'Scale': 120}}`, by chain position).
`clone_item` keeps sync by default: for B-roll at a new time pass `src_in=`. A keep-sync clone moved earlier than its
media allows would start before the media begins: pass `src_in=` there too. On a Mac prproj_lib refuses such a clone
with a clear error (`STRICT_CLONE`); set `prproj_lib.STRICT_CLONE = True` to get the same check on Windows.

## R7. Place a new clip (B-roll, overlay, picture in picture)
```python
m = master_by_name(doc, 'C129.mp4')                  # a clip already in the project (bin name)
tmpl = [t for tr in V for t in clip_item_ids(doc, tr) if find_component(doc, t, 'AE.ADBE Motion')][0]
nid, objs = place_video_item(doc, tmpl, m, s2t(12.0), s2t(14.5), src_in=s2t(30.0),
                             overrides={'AE.ADBE Motion': {'Position': '0.5:0.45', 'Scale': 120.0}})
doc.append(objs); add_to_track(doc, V[1], [nid])
```
- The template only lends structure: its Motion values (crops too) are reset first, its keyframes stripped.
- `keep=('AE.ADBE Motion', 'AE.ADBE Lumetri')` also copies the template's grade (B-roll matched to the A-roll look).
- Vertical crop of a landscape clip (1080x1920 sequence): Scale = 1920 / source height x 100 (6048x3408 camera: 56.3),
  Position x = 0.5 - (cx - 0.5) x source width x Scale / 100 / 1080, where cx = subject centre as a fraction of the
  source width (measure it on a full-resolution grid of the frame, never on thumbnails: framing read from thumbnails
  was wrong once). Check the face stays inside the frame for the whole shot.
- Clamp Position x to [(1080 - W/2) / 1080, (W/2) / 1080], W = the scaled clip width in px, so the clip always covers
  the frame. Landscape archive into 9:16: Scale = 1920 / source height x 100 x zoom (720p: 266.67 at zoom 1).
- Check every crop on one sheet at the first, middle and last frame: one round fixed 7 of its archive crops there
  (faces at the edge, two soft shots, a "countless athletes" line over a shot with one runner).
- More placement mechanics: hard cuts on phrase breaks and frame-grid edges when the grade is cut around B-roll (R19).

## R8. New tracks
```python
nv = add_video_track(doc, seq)            # on top (at=0 inserts as V1 and pushes the rest up)
na = add_audio_track(doc, seq)            # on top of the audio tracks
```
Put overlays, graphics and new B-roll on new tracks above the user's tracks, never mixed into their tracks. Both work
on either track-ID order (Mac and most Windows projects put `<ID>` first; prproj-format.md section 12); adding several
tracks in one run: one add at a time, each from the live track list.

## R9. Import media
```python
mm, objs = import_mp4(doc, '/job/stock/pexels_123.mp4', project_dir=os.path.dirname(OUT)); doc.append(objs)
new_bin(doc, 'External B roll', [mm['cpi_uid']])      # or add_to_bin(doc, 'Existing bin', [...])
```
H.264 only, and clean: downloads are often variable frame rate or carry odd audio layouts, so normalise them first
(constant frame rate H.264 + stereo AAC 48 kHz) before `import_mp4`. Like `relink`, it writes the project's own
`<RelativePath>` form (`style=` to force). ProRes / alpha .mov / WAV kits: import in Premiere
by hand or by UI (premiere-ui.md), save, rebuild from that save with `master_by_name`. Many files: Ctrl+I, type the
folder path, Enter, then names in batches of 12. On the Mac import them into a COPY through the bridge
(`app.project.importFiles`, about 20 per call), save, then continue by text from that save.

## R10. After Effects overlays (alpha) on top of the edit
1. Render ProRes 4444 with alpha ("High Quality with Alpha", ae_build template 'alpha').
2. Import the .movs in Premiere (UI), save.
3. `place_video_item(doc, tmpl, master_by_name(doc, 'TITLE_01.mov'), start, end)` on a NEW top track.
4. Captions under a graphic: disable them (R5), do not delete.
Overlays must start with their B-roll shot (not over the A-roll before it) and end on its cut.

## R11. Sound effects and music clips
```python
sm = master_by_name(doc, 'POP1.wav')
a1_item = clip_item_ids(doc, A[0])[0]                       # any audio clip as structural template
aid, objs = place_audio_item(doc, a1_item, sm, s2t(5.0), s2t(5.8), gain_db=-10.0)
doc.append(objs); add_to_track(doc, na, [aid])
```
Peak on the frame (place the file so its transient lands on the visual hit, `atools.peak_time`). Lanes: new tracks A3+,
one clip at a time per lane. See `audio.md` for levels.

## R12. Delete something you placed
```python
delete_item(doc, nid, track_uid=nv); normalize_blobs(doc)
```
Only your own additions. Then validate.

## R13. A grade or effect on an adjustment layer
Clone an existing adjustment-layer item (`clone_item` with `src_in=ADJ_IN`) and its Lumetri with overrides, or cut an
existing grade layer around B-roll by cloning pieces (`retime_item` the first, `clone_item` the rest). Lumetri indexes in
`prproj-format.md` section 7, values in `grading.md`.

## R14. Effect masks (blur a logo, spotlight a board)
Clone the project's own Mask2 sub-component, write the path with `mask_path_blob(poly_pts([(x0, y0), ...]))` + `set_blob`,
add it to the effect's SubComponents. Ellipse masks need exactly 4 vertices. Tracked masks: Position keyframes
(`kf_point`) from your tracker. Simplest robust route: ask the user to draw one mask by hand, then clone and retime it.
Premiere 2025 projects use a different mask component: `scripts/prproj/prproj_masks.py` (blur boxes, four-corner
outlines, keyframed boxes, black boxes over words; prproj-format.md section 8).

## R15. Brand-new sequence from an edit list (no project yet)
`python scripts/prproj/fcpxml.py edit.json out.xml`, then File > Import in Premiere. It makes a new sequence and bins;
it cannot change an existing one. For review previews without Premiere: `scripts/ae/ae_assemble.py`.
- 12 Oct 2026: Premiere refuses the WHOLE XML ("File Import Failure") over one clip it cannot resolve. Two faults did
  it: sound clips pointing at a `<file>` that declared only video (the clip's picture and sound came from the same MP4),
  and music clips running past the end of their file (a looping bed laid as one long clip). fcpxml.py now writes the
  layout of XMLs Premiere is known to import here and checks every file it writes; run
  `python fcpxml.py --check X.xml` on any XML before handing it over (it also passes Premiere-proven ones, so a FAIL
  is real). A refused XML leaves a media-cache .ims named after it with format "    " (unknown): that is the tell that
  the XML importer turned it down, as opposed to missing media (which imports and asks to relink).
- Loop music by laying several clips back to back, each inside the file; keep ~0.05 s clear of an MP3's end (Premiere
  can measure it a little shorter than ffprobe).
- When an XML is refused, copy a file that already imports: compare it with an XML that imports on that machine (an
  older job's XML the user confirmed), copy its structure, then list every element yours uses that it does not: those
  are the only unproven parts. Why: Claude cannot run Premiere's importer, and a known-good file plus a checker that
  passes it and fails the bad ones is the closest thing to a test. After that fix the user imported all five XMLs ("The
  XML import worked this time").
- Validate the edit list before writing XML or a preview: no picture gaps, no voice overlaps, every file exists.
- Layouts that imported and served the user:
  - a cutdown: V1 picture linked to the dialogue on A1-A2; music on A3-A4 (a bed that overlaps the one before moves to
    the next pair); shutters A5-A6; whooshes A7-A8; levels set, fades and crossfades NOT written (audio.md section 5);
    markers for every removed stretch (the reason in the comment) and for each transition the user finishes by hand;
  - an explainer first assembly: V1 shots, A1 voice, A2 music, A3-A7 SFX, markers;
  - a code-built news post: V1 the base clip MP4, V2 the overlay PNG, A1 the audio WAV; a faceless post adds the keyed
    reaction as an alpha .mov (QuickTime Animation, ARGB) on its own track with the headline PNG above it;
  - plus a `<id>_source.xml` beside each post: the WHOLE source video on V1, scaled like the render, its in / out on
    the window used, linked audio on A1, so the editor can slip (Y) to any part; a 15 s cut layer has nothing to slip
    to. The fastest re-cut is still "tell me the timestamp" and a 20 s re-render: the source XML carries the raw song
    without the house loudness and fade.
- `<pathurl>` form: `file://localhost/C:/...` for a Windows path, `file://localhost/Users/...` for a Mac path (one
  slash after localhost, spaces as %20). fcpxml.py builds each one from the PATH's own form (`path_url`), whichever
  machine writes the XML, so a Mac path never gets the doubled slash an earlier version gave it, and `--check` reads
  both forms back on either machine (`url_path`). Media paths must be absolute: the builder notes any relative path,
  because Premiere's import fails on it. Importing these XMLs in Premiere on a Mac is still untested (a first-run task
  on the boss's Mac). In your own tools build file URLs with one tested helper, never by joining strings:
  `'file://localhost/' + '/Users/...'` doubles the slash, and so does `'file:///' + path` in an HTML template.
- Mac: `open -a "Adobe Premiere Pro 2026" edit.xml` imports nothing. The scripted route is the bridge,
  `app.project.importFiles([xml])` (not yet tested on the Mac port); otherwise the user does File > Import.

## R16. Diff the user's save against your last delivery (before every new round)
```bash
python prproj_dump.py "Show v6.prproj" > a.txt
python prproj_dump.py "Show v6 (user edit).prproj" > b.txt
git diff --no-index --word-diff a.txt b.txt
```
Their changes are the brief: keep them, build on them, mention them in the report. (Windows) Set
`PYTHONIOENCODING=utf-8` first, or a project with emoji in its names crashes the redirected dump.

## R17. Caption track styling (font, size, box, height)
Premiere's scripting cannot style captions. Build the track (bridge `createCaptionTrack`, or the user does), save and
close the project, then `python scripts/captions/style_captions.py IN.prproj OUT.prproj --font ... --size ...` writes a
new styled copy. Field map, traps and the safe way to discover new fields: `captions-style-patch.md`; every other
caption mechanic: `captions.md`.

## R18. Zoom pieces on the A-roll (two stacked Transforms)
- Each zoom piece is an adjustment layer above the A-roll, on its own track, carrying TWO Transform effects
  (`AE.ADBE Geometry2`), best cloned from the user's own preset items: a slow drift and a quick punch. Keys on Scale
  Height (uniform), Sampling bicubic. Only the A-roll is zoomed: B-roll sits on a track above the zoom layers (R19).
- Values copied from the user's reference edit (kept by the user): intro punch 115 -> 100% over 0.867 s (ease out) times
  a drift 108 -> 100% over the piece (his reference used 120 x 110); push: punch 100 -> 110% over 1.133 s times a linear
  drift from 100% at 1.3-2.0% per second; pull: punch 110 -> 100% over 1.117 s times a linear drift back to 100%.
  Alternate push and pull and keep the level continuous across piece boundaries. Whiteboard shot: anchor (0.40, 0.35),
  punch 104, intro 104 x 103, drift 0.25-0.4% per second.
- The maths: stacked Transforms MULTIPLY, so the peak = punch x drift (115 x 108 = 124%): check that product against
  the frame (the reference reached 132% and cropped the presenter's hair). Cap peaks at about 116-121%. Anchor on the
  face: set the Transform's Anchor Point and Position to the same face point (0.5, 0.33).
- Start a move each time the picture returns from B-roll so it is seen; push into a B-roll cut and land the pull after
  it. When to zoom (and to wait for the word): motion-design `motion-rules.md` section 9.
- prproj_lib has no zoom builder yet: clone a zoom piece the user made (or any adjustment-layer item, R13), set the keys
  with `set_keys` and `kf_scalar` influences, and check the % per segment against your plan before delivering. The
  job's own builder, its plan format and its check ship as reference code in
  `~/VisionKit/kit/library/pipelines/ad-build-kit/` (`prproj/build_zoom_gfx.py`, `work/zoom_plan.py`,
  `prproj/validate_zoom_gfx.py`; written on that job's older Doc class: port, do not run as is).

## R19. B-roll over a log A-roll graded on adjustment layers
- Track stack: V1 A-roll; V2 zoom layers (R18); V3 B-roll with its own clip Lumetri (grading.md section 2); V4 the grade
  adjustment layer, CUT so that grade pieces plus B-roll tile the timeline exactly; V5 and up graphics and overlays.
  Why: B-roll must never be punched by the zooms or graded twice. In a project that already has zoom tracks, shift up
  by one.
- Edges: hard cuts only, on phrase breaks: a dissolve shows a moment of ungraded log footage where the grade piece ends.
  Snap a planned edge to an existing A-roll cut when it is within 0.021 s, otherwise round it to the SEQUENCE frame
  (60 fps = 4233600000 ticks); round source in-points to the SOURCE frame grid (25 fps = 10160640000 ticks), or
  off-grid edges leave 1-frame slivers.
- When B-roll is removed to show the A-roll again, extend the zoom pieces and the grade pieces over the freed A-roll
  (clone grade pieces into the gap), or the picture jumps to unzoomed, ungraded log footage.
- Tell the user how to move B-roll later by hand: stretch the neighbouring grade piece into the gap it leaves and trim
  the grade where it lands.
- Validate that grade pieces plus B-roll fill each timeline with no gaps or overlaps (prproj-format.md section 17).

## R20. Live frosted glass under an After Effects card
- An alpha overlay cannot blur the footage below it, and baking the footage into AE breaks the compile-in-Premiere rule.
  So the AE card (tint, sheen, edge, text) renders as alpha, and under it sits a Premiere adjustment layer with
  Gaussian Blur 42 inside a 4-vertex rectangle mask (feather 2) whose Scale Width / Height are keyed EVERY frame
  (60 fps) inside the reveal, grow and exit windows, from the geometry the AE build wrote (`glass_geom.json`: x0, y0,
  w, h1, h2, r, tIn, tOut, tG, dur). The AE side writes its eases as per-frame keys from the same function
  (after-effects.md section 5), so the blur window follows the card exactly. No glass notes came back after this.
- The card's design: motion-design `titles-captions-type.md`.

## R21. Tracked masks from your own tracker (a whiteboard, a sign)
- One adjustment layer on a PRE-ZOOM track (between the footage and the zoom layers, so the zooms scale it with the
  picture), Gaussian Blur 26, one Mask2 per item (one per board line); each mask's Position, Rotation and Scale follow
  the tracker; a reveal animates Scale Width 100 -> 0% (smoothstep) anchored on the line's right edge.
- Key once per SOURCE frame and add a hold copy 1/240 s before the next sample (a 25 fps source in a 60 fps timeline),
  finer inside wipe windows. Why: keys that interpolate between source frames slide against the step-wise picture.
- The tracker: media-toolkit.md section 13 (or a planar track by the user). Overlays that follow the same track:
  after-effects.md section 7. "Everything follows the board's movement automatically, so there's no masking for you to
  do" (the user had offered to mask it by hand).

## R22. Spotlight instead of a tint highlight
- An adjustment layer over the moment (about 1 s) with Lumetri (Exposure 0 -> -1, Saturation 100 -> 76 over 0.2 s) and
  Gaussian Blur 0 -> 6, each under an INVERTED tracked mask (feather 60); the lit box can grow (2 lines to 4 on the
  second "here", smoothstep over 0.2 s). Outside luminance went 0.44 -> 0.30. Clone the Lumetri from a NEUTRAL one
  (grading.md section 7). Why: a green tint highlight "feels cheap".

## R23. Resize an animated graphic
- Edit the static value AND every keyframe value with one function, so the timing is untouched (the job's helper was
  `edit_param(doc, pid, fn)` in `~/VisionKit/kit/library/pipelines/ad-build-kit/prproj/build_v9.py`; prproj_lib has
  none yet: read the param's StartKeyframe and Keyframes, map every value, write them back with `set_value` /
  `set_keys`).
  A credential tag at +20%: text Scale 100 -> 120 shifted down by (k - 1) x cap height / 2 (cap 20.4 px); pill height
  scale x1.2; the pill's width keys (open / close) x1.2; if the bigger pill would cross the left margin
  (cx - k x half < 0.02), shift text and pill right by (k - 1) x half (42.8 px in one ad).

## R24. An appended segment from shots already graded elsewhere (a CTA end)
- Find an item of the same camera clip near the wanted in-point (in any sequence of the project), clone it with its
  whole effect chain at the new time (`clone_item(..., src_in=...)`, R6: grade, log override and framing come for free
  and match), and snap the new in-point to the SOURCE frame grid: round(sec x TPS / fr) x fr ticks. Three shots of 1.6-1.7 s made a 5 s end. Pick static, clean
  shots behind a kicker (a lowering shot was blurry and busy).
- The music ending for it: audio.md section 9. Check the sequence has no in / out marks before exporting, or the export
  misses the new ending (premiere-ui.md "Export").

## R25. Swap an overlay's render in place
- The job's helper (`swap_media` in `~/VisionKit/kit/library/pipelines/ad-build-kit/prproj/build_v9.py`, not in
  prproj_lib yet) made a new clip instance from the new master with the same
  in / out and times and deleted only the old instance, so the track item and its Motion stayed. With prproj_lib
  today: `relink` (R1) swaps every use of a file (right when the old render should go everywhere); for one use, place
  the new master with the old item as template at the same times (`place_video_item(..., reset_motion=False)` keeps
  the template's Motion values; the default resets them) and delete the old item (it is yours, R12).

## R26. Titles and plates by text (Essential Graphics)
- Clone a graphic the user made (prproj-format.md section 9) and size plates and pills from real font metrics: PIL
  `getlength` per glyph plus tracking / 1000 x size per gap; cap height from `getbbox('H')`. This matched Premiere's
  own layout.
- Eases are influences in Premiere's keyframe string (`kf_scalar` infl): out 0.15 / in 0.85 for a snappy start and a
  long settle, 0.70 / 0.25 for exits; stagger layers 0.10-0.26 s; rise 8-70 px while fading in.
- A title the user moved or scaled by hand carries its own Motion component: replace that Motion when you resize, or
  the new size is applied twice (three titles once carried it).
- Find titles by their graphic name across ALL tracks, never by track position: the user's own code-card track once
  pushed a title down a track.
- Graphics on video tracks sit UNDER caption tracks (captions always draw on top): disable the caption words that
  collide (R5). Grades and zooms on adjustment layers never touch captions.
- No text setter in prproj_lib yet: write the Source Text blob (prproj-format.md section 9) or render the title in AE.
  One job's graphics builders ship as reference code in `~/VisionKit/kit/library/pipelines/ad-build-kit/prproj/`:
  `build_zoom_gfx.py` writes a track of Essential Graphics text and shape clips with per-layer keys, `build_title_v2.py`
  swaps the layers inside existing title graphics, the templates are `gfx_templates.json`, `text_doc_template.json` and
  `appearance_template.json`, and `validate_zoom_gfx.py` / `validate_title_v2.py` are their checks. They use that job's
  older Doc class: port, do not run as is.
