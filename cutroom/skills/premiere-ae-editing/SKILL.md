---
name: premiere-ae-editing
description: Operate Adobe Premiere Pro and After Effects by script on Windows or Mac. Change .prproj projects safely (relink, retime, place B-roll, overlays and SFX, disable, Lumetri grades, log overrides, masks, zooms, volume keys, tracks, bins, captions and their styles, transcripts), write XML assemblies for Premiere's import, drive a running Premiere to check builds and export, build After Effects elements with ExtendScript and render them unattended, key green screens, read footage through frame sheets, word timings and OCR, measure loudness and master mixes, bake an SFX kit and place SFX and music beds, download and cut sources, and work through timecoded review notes. Use it whenever the user mentions Premiere, After Effects, a .prproj, .aep, .jsx, .mogrt or .epr file, XML or FCPXML, a sequence or timeline, B-roll placement, captions or subtitles, Lumetri or a grade, masks, renders or exports, keying, SFX, music beds, loudness or LUFS, yt-dlp, or review notes with timestamps, even if the apps are never named.
---

# Premiere + After Effects: operating the tools

Edit by script, never by long click sessions, and look at real frames before saying anything is done. Paths are
relative to this skill's folder, `~/.claude/skills/premiere-ae-editing` (on Windows `~` is `C:\Users\<name>`).

## Which machine am I on (check first)
The session's environment line says `win32` (Windows) or `darwin` (Mac). Use that column below. In every reference,
`python` means the tools' Python: plain `python` on Windows, `~/.venvs/premiere-ae/bin/python` on a Mac.

| | Windows | Mac |
|---|---|---|
| Tools' Python | `python` 3.13 (av, numpy, pillow, esprima, faster-whisper) | `~/.venvs/premiere-ae/bin/python` (av, numpy, pillow, esprima) |
| Run an After Effects script | `ae_run.py`: `AfterFX.com -r`, refuses while AE runs | `ae_run.py` Mac route: osascript DoScript, refuses if AE holds a project |
| Look inside a running Premiere | its window, by computer use | the CEP bridge `scripts/premiere/pp.py` (optional, the user installs it) |
| Word timings | `hear.py` (faster-whisper on the CPU; a GPU route for long footage: timing.md) | `hear.py` in the mlx-whisper venv |
| OCR | `scripts/media/ocr.ps1` | `scripts/media/ocr` (built from `ocr.swift`) |
| Fonts and glyphs | `env_check.py` font list | `scripts/media/fontcheck` |
| Encoder for big renders | NVENC (driver 610+) or libx264 | VideoToolbox or libx264 (media-toolkit.md section 10) |
| Shortcuts | Ctrl | Cmd |
| Machine facts | after-effects.md section 11, timing.md, youtube-downloads.md | `references/mac-notes.md` |

If a script in your copy only knows the other machine (for example it looks for AfterFX.com or PowerShell on a Mac, or
starts a helper with Windows-only process flags, as `ytdl.py` still does when its token server is not running), stop and tell the user which tool still
needs its port (mac-notes.md has the porting table). Never improvise a runner that sends scripts into an After Effects
or Premiere that holds the user's project.

### First time on a Windows PC (ask before installing anything)
1. Python 3.13 with `pip install av numpy pillow esprima faster-whisper`.
2. ffmpeg on PATH (`winget install Gyan.FFmpeg`; 9.0.2 in Oct 2026); PyAV covers decoding where ffmpeg is missing.
3. After Effects: the USER turns on Edit > Preferences > Scripting & Expressions > "Allow Scripts to Write Files and
   Access Network" (a security preference; without it scripts silently do nothing, after-effects.md section 11).
4. Optional: GPU Whisper on an NVIDIA card (timing.md "Long raw footage"), YouTube downloads (youtube-downloads.md,
   read its rights note first).
5. `python scripts/env_check.py`: app versions, what is running, Python modules, fonts.

### First time on a Mac (ask before installing anything)
1. Tools venv: `python3 -m venv ~/.venvs/premiere-ae && ~/.venvs/premiere-ae/bin/pip install av numpy pillow esprima`
   (Homebrew's Python refuses global installs, PEP 668).
2. Transcription venv (Apple Silicon): `python3 -m venv ~/.venvs/mlx-whisper && ~/.venvs/mlx-whisper/bin/pip install
   mlx-whisper` (the first transcription downloads the model, about 1.6 GB).
3. Build the two Swift helpers from the skill folder (Xcode Command Line Tools): `swiftc -O scripts/media/ocr.swift -o
   scripts/media/ocr` and `swiftc -O scripts/media/fontcheck.swift -o scripts/media/fontcheck`.
4. ffmpeg from Homebrew if missing (check that it has the filters you need, mac-notes.md). yt-dlp only if the user wants
   YouTube downloads (read youtube-downloads.md first): into the tools venv (`pip install "yt-dlp[default]"`), because
   `ytdl.py` runs it as `python -m yt_dlp`.
5. Premiere bridge, only if a job needs a running Premiere: the USER runs `zsh bridge/install_bridge.sh` after reading
   it. It copies a hidden panel into the CEP extensions folder, writes a private token to `~/.editbridge_token` and
   sets Adobe's PlayerDebugMode so unsigned panels load (a security setting: never run it yourself or with `--yes`).
   Then the user restarts Premiere once, after saving. Details and undo steps: mac-notes.md.
6. `python scripts/env_check.py` to confirm apps, bridge ports, modules, tools, disk and fonts.

## What this skill is
The tools: learned on real client jobs (vertical ads on log footage, YouTube explainers with an AI presenter,
green-screen essays, music edits, cutdowns of long raw footage, code-built news and faceless posts) on a Windows PC,
re-tested on 7 Oct 2026 (Premiere 26.5, After Effects 26.5, Python 3.13 + PyAV), then ported to a Mac between 11 and
14 Oct 2026 (Premiere 25.6.6 and 26.5.1, After Effects 26.2.1, Python 3.14), which added a Premiere bridge, Premiere
2025 masks, caption styling, motion libraries and Mac runners. In Python this finds the folder on both machines:
`os.path.expanduser('~/.claude/skills/premiere-ae-editing')`.
Not here: taste, story, cutting and review judgement (editing-playbook); motion rules, effects and their verdicts
(motion-design); sourcing and rights (research-and-sourcing); batch pipelines (production-automation); platform
formats (social-video-formats).
Job code that is not one of this skill's tools yet (the zoom and title builders, the SFX kit and cue generators, the
music-edit kit, the board tracker, the colour-model fit, the frame meter, the PDF notes reader, the 2.5D rig) ships in
the library, `library/pipelines/<folder>/`  (its README maps each folder to
the editor's originals). The references name the files where they describe the method. It is reference code: port the
function you need into these tools and test it on a copy before relying on it.

## House rules (the user's standing instructions)
1. **Never touch the user's originals.** Read their LATEST save (also check the Auto-Save folder, `Adobe Premiere Pro
   Auto-Save` next to the project), write a new versioned file next to it ("Show v7.prproj"), new renders into a new
   folder. Their hand edits in that save are the brief: keep them and say what you kept. You may replace your own
   just-built file only while Premiere has never opened or saved it. Name new things the way the user names theirs (job
   name + version). Never put "Claude" in a name a client sees (renders, sequences, delivered files, client-visible
   projects); internal tools and work files may use it.
2. **Disable, never delete** their clips, captions, music or B-roll (`disable_item`). They delete things themselves; you
   delete only what you placed.
3. **Only the project this session is about.** The user often has another project open (on a Mac maybe in Premiere
   2025 AND 2026): never quit Premiere (Ctrl+Q / Cmd+Q prompts to save every open project), never Save / Don't Save a
   project you were not asked to touch, close yours with Ctrl+Shift+W (Cmd+Shift+W) while its title bar is active or
   by the bridge. Ask before restarting any Adobe app. Find sequences by name, never "the active sequence". Never start
   the Adobe Media Encoder queue.
4. **Do not blast the machine.** One After Effects and one aerender at a time (a second aerender killed the first), one
   render-queue item at a time, one heavy job (render, prep, matte, download) at a time, a 2 s test before a big batch,
   no killing AE while a render file still grows, free disk space checked before big renders or downloads. A gate that
   waits for other heavy jobs must treat an empty process list as busy. On a laptop, check mains power before a long
   render: Windows `(Get-CimInstance Win32_Battery).BatteryStatus` (1 = on battery; on battery that PC capped the CPU at
   2.4 GHz and libx264 ran about 4x slower, 12 Oct), Mac `pmset -g batt` (not tested here). Ask the user to plug in
   rather than drain the battery. Premiere and AE may run together when the machine has the RAM (31 GB was fine).
5. **Secrets and rights.** Never view, print or store API keys or the bridge token. Never change Adobe security prefs
   (AE scripting preferences, PlayerDebugMode): the user does. Download from YouTube and other sites only when the user
   asks; the YouTube route works around YouTube's bot check and may break its terms, so use it only for footage the
   client has rights to, and the reviewer decides whether to keep it (youtube-downloads.md). Say when material is not
   cleared (archive footage is editorial; music lifted from someone's reel is unlicensed; Epidemic's Creator plan does
   not cover client work).
6. **No AI generation, lip-sync, voice changes or fake breathing / sway on stills** unless asked: the user does AI with
   their own tools.
7. **Hand back what an editor does faster by hand** (masking, roto, tracking fixes, AI gen) and build on their result.
8. **Talk plainly:** short pointers, plain English, NO em dashes, numbers instead of adjectives, say what you verified
   and what you did not. Define a grading term once when it matters. Claude cannot hear: say so, and let the user's ears
   judge sound.
9. **Token-light working:** scripts over clicking, compact printed summaries, one labelled contact sheet instead of many
   image reads (split one that is too tall to read), screenshots at 0.4-0.5 scale, long outputs to files. Stay off the
   screen while the user works on the PC.
10. **Compile in Premiere, After Effects only where needed.** Plates, presenter stills, screenshots, simple moves, text and
   cuts are separate Premiere clips and graphics, so a review change is one relink or one clip swap. After Effects is for
   what Premiere cannot do well (complex animated graphics, keying, camera rigs), brought in as elements (alpha overlays,
   moving plates), never as finished shots with everything baked in. Music edits follow the same rule: Premiere
   assembles them and After Effects only makes the effect elements. A presenter baked into 17 renders once meant 17
   re-renders for a single change to the presenter. (Dynamic Link comps are the exception when the user asks for them,
   after-effects.md section 14.)

## Start of a job (10 minutes, saves hours)
1. `python scripts/env_check.py`: app versions, what is running, Python modules, tools, fonts (bridge ports on a Mac).
2. On a Mac with Premiere open: `python scripts/premiere/pp.py --v 2026 --status` (and `--v 2025`): which projects are
   open. On Windows: look at the title bar before touching anything.
3. Find the project and its newest save; `python scripts/prproj/prproj_dump.py X.prproj > dump.txt` and grep the dump
   (sequences, tracks, every item with times, effects, captions, media list; on Windows set `PYTHONIOENCODING=utf-8`
   first, or emoji in names crash the redirected dump). Note disabled layers before copying any recipe from a
   reference sequence.
4. See the material: `python scripts/media/frames.py even sheet.png 6 a.mp4 b.mov ...` (one row per file + metadata),
   `frames.py sheet` for exact times. Hear it: transcripts (`timing.md`).
5. If the job continues an earlier one, read that client's notes (dossier or memory file) and
   `references/past-projects.md`. If two asset folders overlap, ask which set is current.
6. Write a short plan (what changes, what is reused, open questions). Ask only decisions that are really the user's.

## Pick the route

| The task | Do it with | Read |
|---|---|---|
| Change an existing timeline (relink renders, extend, retime, swap media, add B-roll / overlays / SFX, disable, volume keys, effect values, new tracks, bins) | text surgery on a COPY of the .prproj: `scripts/prproj/prproj_lib.py` | `references/prproj-recipes.md`, then `references/prproj-format.md` |
| Zoom pieces, B-roll over a log grade, glass blur under a card, tracked masks, spotlights | Premiere adjustment layers by script | prproj-recipes R18-R22 |
| Blur boxes, wipes and black boxes in a Premiere 2025 project | `scripts/prproj/prproj_masks.py` | prproj-format.md section 8 |
| Captions: SRT from words, Premiere caption tracks, styling, disabling under graphics, burn-in | `scripts/captions/style_captions.py`, ffmpeg + ASS | `references/captions.md`, `references/captions-style-patch.md` |
| First assembly from rendered shots + audio (no project yet) | FCP7 XML (the XML Premiere imports), File > Import: `scripts/prproj/fcpxml.py` | prproj-recipes R15 |
| Build a scene from stills, screenshots, presenter cutouts, simple moves and text | Premiere layers: import the assets, place them on their own tracks with Motion keyframes, titles as graphics | `references/motion-design.md`, `references/prproj-recipes.md` |
| Complex animated graphics, keying, camera rigs, effects Premiere lacks | After Effects ExtendScript, rendered headless as ELEMENTS (alpha) for Premiere: `scripts/ae/` (+ `motion_lib.jsx`, `scene_lib.jsx`) | `references/after-effects.md`, `references/motion-design.md` |
| Music-edit transitions and flashes (blow-outs, zoom rush, line-art strobes, flash panels, silhouette strobes) | per-frame recipes, compared with the reference frame by frame | `references/transitions.md` |
| Things only a running Premiere can do (import ProRes / WAV / stills, caption tracks from SRT, frame grabs, exports with a preset, Dynamic Link import, sharing a project) | Windows: the window by computer use; Mac: the bridge `scripts/premiere/pp.py` | `references/premiere-ui.md` |
| A watchable preview with sound without touching Premiere | `scripts/ae/ae_assemble.py` | after-effects.md |
| Learn how an existing .aep was built | `scripts/ae/ae_dump.py` (opens a copy) | after-effects.md section 9 |
| Check pictures | `scripts/media/frames.py` on renders; Export Frame (Windows) or bridge `exportFramePNG` (Mac) for the real timeline | `references/premiere-ui.md` |
| Loudness, mastering, voice, SFX kit and cue sheets, beds, bar-grid music edits, -14 LUFS exports | `scripts/media/atools.py` + prproj_lib audio functions, `assets/presets/H264 match source, -14 LUFS.epr` | `references/audio.md` |
| Colour | Lumetri on adjustment layers by script, log overrides, measuring frames | `references/grading.md` |
| Word timings, cut points, script-to-voice cues, OCR rects for highlights | `prtranscript.py`, `hear.py`, `speech_cuts.py`, OCR (`ocr.ps1` / `ocr`) + `ocrfind.py` | `references/timing.md` |
| Download footage, cut one moment of a long video, stock, transcription, stems, encoding, ffmpeg keying, subject mattes, tracking | `ytdl.py` / yt-dlp, ffmpeg, Whisper, Demucs, SAM 2 | `references/youtube-downloads.md`, `references/media-toolkit.md` |
| Cutouts, PSDs, web screenshots, HTML overlays, licences | Photoshop by script (COM on Windows, osascript on a Mac) or numpy, headless Chrome | `references/stills-and-sources.md` |
| A client / reviewer review with timecodes | the review loop | `references/review-rounds.md` |

## The loop (every change)
1. Generator script decides (times from words, rects from OCR, crops from sheets) and writes the edit.
2. Static checks: `check_jsx.py` for After Effects scripts, `validate_struct.py original new` plus the semantic checks
   (prproj-format.md section 17) for projects.
3. Run (After Effects only through `ae_run.py`, never by hand-launching AE or running a build script from File > Scripts
   in the user's AE).
4. Look: one labelled sheet per batch; fix and re-render only what failed.
5. Open the new project in Premiere (Windows: by window; Mac: as a second project through the bridge, with the user's
   OK) and check every changed time (a valid file once drew a clip at the wrong time).
6. Report briefly; record new lessons (below).

**Done means:** files written as new versions, validators clean, frames looked at, checked in Premiere at the changed
times (or the report says plainly that this step is still open), and the report says exactly which file to open and
what is still open.

## Scripts
Platform tags: (Win) = Windows only, (Mac) = Mac only; no tag = both.

| Script | Use |
|---|---|
| `scripts/env_check.py` | what is installed / running on this machine: apps, Python modules, tools, fonts (Mac: bridge ports, disk) |
| `scripts/prproj/prproj_lib.py` | the project library: `Doc.open/save`, `sequences`, `find_sequence`, `tracks`, `clip_item_ids`, `item_info`, `relink`, `set_item_end`, `retime_item`, `clone_item`, `place_video_item`, `place_audio_item`, `import_mp4`, `new_bin`, `add_video_track`, `add_audio_track`, `disable_item`, `set_value`, `set_keys`, `set_level_keys`, `set_clip_gain`, `delete_item`, `normalize_blobs`; RelativePaths follow the project's own Windows / Mac form (`path_style`, `style=`, `PATH_STYLE`), and tracks are added in either `<ID>` / `<Index>` order. `python prproj_lib.py X.prproj` lists sequences and tracks; `unpack` writes the XML |
| `scripts/prproj/prproj_masks.py` (+ `mask_template_pp2025.xml`) | Premiere 2025 Gaussian Blur masks: static or keyframed boxes, four-corner outlines, black boxes over words |
| `scripts/prproj/prproj_dump.py` | readable dump of any project (read this, not the XML) |
| `scripts/prproj/validate_struct.py` | structural check of a built project against its source |
| `scripts/prproj/prtranscript.py` | Premiere's own transcripts out of a project, word by word |
| `scripts/prproj/fcpxml.py` | edit list JSON to FCP7 XML for File > Import (linked picture + sound, stereo pairs, markers with comments; each `<pathurl>` follows its own path's form, Windows or Mac); `--check X.xml` finds what makes Premiere refuse an XML |
| `scripts/captions/style_captions.py` (+ `fbtool.py`, `exp_patch.py`, `variants_example.py`) | caption track styling by FlatBuffers patch on a saved, closed project; safe field discovery on a scratch project (verified on the Mac) |
| `scripts/premiere/pp.py` (Mac) | run ExtendScript in a running Premiere through the bridge (`--v 2026` port 47915, `--v 2025` port 47916), `--status`, `-e expr` |
| `bridge/install_bridge.sh` (Mac) | installs the bridge panel + token; the USER runs it (it sets PlayerDebugMode) |
| `scripts/ae/ae_lib.jsx` | ExtendScript helpers that dodge the known traps (keys, text with glyph fallback, plates, paths, soft glows, keying, time remap, cards, highlighter, grain) |
| `scripts/ae/motion_lib.jsx`, `scripts/ae/scene_lib.jsx` | two-key eased moves (`k2`, `chain`), transition set pieces, captions, plates, finishes (after-effects.md section 13; run on the Mac so far) |
| `scripts/ae/ae_build.py` | wraps specs + libraries into one build-and-render .jsx (one item at a time, logs, DONE flag) |
| `scripts/ae/ae_run.py` | runs a .jsx safely and waits for renders to finish growing, then reports (Windows and Mac routes: after-effects.md section 2) |
| `scripts/ae/check_jsx.py` | syntax + ES3 check of a .jsx and every spec before spending an AE launch |
| `scripts/ae/ae_assemble.py` | edit list JSON to a preview .mp4 with audio, rendered in AE |
| `scripts/ae/ae_dump.py` | read-only dump of .aep projects (on copies) |
| `scripts/media/frames.py` | `info`, `sheet` (labelled frames at times), `even`, `grab`, `dupes` (PyAV) |
| `scripts/media/atools.py` | LUFS, true peak, loudest window of any audio/video file |
| `scripts/media/beats.py` | music hits from a wav (numpy only): onsets, kicks, snares, hats, tempo, beat grid, per-frame loudness; for beat-synced cuts and sync audits of edits |
| `scripts/media/fsheet.py` | every-frame contact sheets (frame number, time, kick/snare marks, red border on big jumps) for edits where effects last 1-3 frames |
| `scripts/media/edge_shots.py`, `scripts/media/edge_words.py` | pre-render checks of every clip edge: stray frames of another shot, cuts inside a word (timing.md) |
| `scripts/media/slog3_grade.py` | natural grade for Sony S-Log3 footage without a vendor LUT + per-clip levels, baked to a .cube for ffmpeg `lut3d` (graded clip exports in bulk) |
| `scripts/media/hear.py` | local Whisper word timings (Windows: faster-whisper, float WAVs decoded through PyAV; Mac: mlx-whisper venv, `--from/--to` windows) |
| `scripts/media/speech_cuts.py` | cut edges from the audio, absolute voice-over rules by default (-70 dB edges, breaths cut, final consonants kept): snap predicted times (`phrase@after`, `--at`), `--keep` clean in / out for kept phrases, `--scan` edge check (no edge with sound over -55 dB on both sides), `--phrases` with restart flags and `--wav-dir` per-piece transcripts; `--rel` for noisy field audio (timing.md) |
| `scripts/media/ocr.ps1` (Win), `scripts/media/ocr.swift` (Mac) + `ocrfind.py` | OCR of screenshots (Windows OCR / Apple Vision, same JSON), phrase to highlight rects |
| `scripts/media/fontcheck.swift` (Mac) | is a PostScript font installed and does it have the glyphs a string needs |
| `scripts/media/sapi_words.ps1` (Win) | offline Windows speech recognition word times (fallback) |
| `scripts/media/ytdl.py` (Win; on a Mac start its token server by hand first) | YouTube downloads through a PO-token provider, one at a time; read the rights note first (youtube-downloads.md); `--help` only prints the note |
| `scripts/stills/ps_cutout.jsx`, `decon.py`, `psd_composite.py` | Photoshop Select Subject cutouts, hair-edge cleanup, PSD reading without Photoshop |
| `assets/presets/H264 match source, -14 LUFS.epr` | export preset with loudness normalisation (-14 LUFS, -1 dBTP) for scripted exports |
| `assets/ae/` | tube vignettes and Bayer threshold maps used by the finish and dither helpers |

## Traps that bite first (full lists in the references)
- Ticks: 254016000000 per second; item Start/End are sequence time, in/out and keyframes are MEDIA time; Start 0 is omitted.
- Premiere renumbers ObjectIDs on save: find things by name / MatchName, never by an old id (a hard-coded mask
  template id made one build refuse to open).
- A track's transitions live in a second TrackItems list: touch only the clip list.
- Copied clips must drop Head/TailTransition refs and get a new Node ID (prproj_lib does it), or they draw at the
  template's time. Copied Motion brings its crops along (place_video_item resets Motion). `clone_item` keeps sync by
  default: for B-roll at a new time pass `src_in=`.
- Clips at default Motion have NO Motion component: use a template item the user moved or scaled.
- `<CurrentValue>` is a stale cache; `StartKeyframe` holds the value. Audio Level = 10^((dB-15)/20).
- Caption tracks draw above every video track; stacked Transforms multiply (punch x drift: cap zoom peaks near
  116-121%).
- Windows and Mac saves differ in the RelativePath form (`.\file` vs `./sub/file`, `&` double-escaped on the Mac):
  prproj_lib follows the PROJECT (its own media paths), whichever machine edits it (`style=` / `PATH_STYLE` to force).
  A track's `<ID>` and `<Index>` come in either order on both machines (134 of 221 Windows project files put `<ID>`
  first); `add_video_track` / `add_audio_track` handle both. A sequence renamed by script keeps its old bin name.
- Through the bridge (Mac): Premiere snaps stills to a 29.97 grid when you set their out point (1-frame holes), floors
  audio in/out to whole frames (pad short SFX first), and `overwriteClip` silently fails now and then: read back and retry.
- After Effects: scripts go into the AE that is already open (`-r` on Windows, DoScript on a Mac); ES3 only; re-fetch
  handles after adding effects; shape-layer blurs are clipped to a box (use feathered solids); never remove ALL
  time-remap keys; missing glyphs render blank; script scales differ from the UI (Lumetri saturation 0-300, Threshold
  0-1); a comment starting `//@` blocks AE with a dialog; "Apple ProRes 422 HQ" is not a template ("High Quality" is
  ProRes 422, "High Quality with Alpha" is ProRes 4444); on the Mac new projects need the sRGB working space and
  written files need `lineFeed = "Unix"`.
- Whisper word starts are 0.1-1 s off: snap cuts to the audio. Word timestamps on whole long files dropped speech: work
  in windows. Premiere Export Frame can repeat the previous frame, and double-clicking an already-open sequence does not
  switch the Program monitor (use the timeline tabs).
- Heredocs mangle backslashes (even a quoted `<<'EOF'`; a regex `\b` once became a backspace) and the Write tool turns
  `\uXXXX` escapes into real characters: write generators with the Write/Edit tools, use `json.dumps` for JS strings,
  make one edit per call and grep that it landed. (Windows) Git
  Bash converts `/c/...` paths only when they are separate arguments, not inside `python -c` code, and rewrites any
  argument that looks like a POSIX path (`/markets/x`): pass full URLs or set `MSYS_NO_PATHCONV=1`. `python -I` ignores
  PYTHONIOENCODING: add `-X utf8`.
- FCP7 XML: one unresolvable clip makes Premiere refuse the whole file. Every `<file>` must declare all the streams its
  clips use, and no clip may run past its file's end: `fcpxml.py --check` every XML before handing it over.

## Reference map
- `after-effects.md`: running AE safely on both machines, the self-reporting build pipeline, render templates, 49
  ExtendScript traps, effects and matchNames, text, keying, time remap and tracking, the 2.5D rig maths, reading .aep
  files, render costs, Dynamic Link.
- `audio.md`: measuring, targets, voice mastering, the full-mix chain, Premiere level maths and crossfades, the SFX kit,
  cue maths and lanes, beds, bar-grid music edits, offline mixes, the Epidemic connector.
- `captions.md`: caption mechanics: phrases from word timings, ASS burn-in, Premiere caption tracks, disabling under
  graphics, burn-in on export, reading burned-in captions.
- `captions-style-patch.md`: styling Premiere caption tracks by patching the saved project (blob format, field map,
  traps, safe field discovery).
- `grading.md`: Lumetri on adjustment layers, log overrides, mixed sources, measuring skin and blacks, a colour model
  fitted from a reference render, colour passes, graded stills and clip packs.
- `mac-notes.md`: what was verified on the Mac: projects and XML that travel between the machines, the Premiere bridge,
  AE by DoScript, aerender, fonts, Mac media tools, porting Windows tools.
- `media-toolkit.md`: downloads, frame-exact segments, stock, transcription, stems, measurements, ffmpeg encoding,
  keying with ffmpeg, SAM 2 mattes, tracking, PDF notes, house rules for media jobs.
- `motion-design.md`: where each kind of graphic gets built, the helper for each pattern, the checks before delivery.
- `past-projects.md`: what each kind of job needed, planning numbers, how the tools were tested.
- `premiere-ui.md`: a running Premiere (window on Windows, bridge on the Mac): safety, checks, imports, captions,
  exports, sharing a project, Dynamic Link builds.
- `prproj-format.md`: .prproj internals: objects, ticks, items, media, effects, Lumetri, masks, graphics, captions,
  audio, tracks, blobs, what Premiere changes, validation.
- `prproj-recipes.md`: prproj_lib recipes R1-R26 (relink, retime, clone, place, tracks, import, overlays, SFX, masks,
  XML, zooms, B-roll over log grades, glass blur, tracked masks, spotlights, resizing, appended segments, titles).
- `review-rounds.md`: turning timecoded notes into a new version: intake, the latest save, fixes, verification, build
  notes, calibration.
- `stills-and-sources.md`: Photoshop by script, cut-outs, repainting brand names, web screenshots and HTML overlays by
  headless Chrome, stock, archive and Commons rules, platform flags.
- `timing.md`: word timings, script-to-voice cues, cut points, OCR, seeing footage, long raw footage, music-edit sync.
- `transitions.md`: music-edit transitions: the measure-rebuild-compare method, frame recipes, one-letter strobes,
  flash panels, the user's Premiere recipes, rejected builds.
- `youtube-downloads.md`: the PO-token YouTube route, its rights note, the 720p floor, one download at a time, the Mac
  status.

## Keep this skill sharp
When something new is learned (a trap, a verified structure, a reviewer's taste rule), add one dated line to the right
reference file (taste goes to editing-playbook or motion-design) and, if it is a tool bug, fix the script and re-run its
test (the four kinds of test in past-projects.md). When a review shows a systematic miss, change the default in the
generator or helper, not just the one shot. Mark machine-specific facts "(Windows)" or "(Mac)".

Sources: real production jobs, Sept to Oct 2026.
