# The meme-compilation pipeline

How the reference jobs were built by script, from the client's raw files to a timeline the user reviews. The scripts
are in `../reference-pipeline/` (the real job code, renamed neutral; read its README for the constants to change and
what each script needs). Ours stays the main way to write Premiere projects: on Windows / Premiere 2026 use the
premiere-ae-editing skill (fcpxml.py for the first assembly, prproj_lib.py for effects and masks); the Premiere 2025
bridge route below is the Mac path the jobs used.

## Two kinds of job
- **Full edit**: the client sends a screen recording of the narrator reading memes plus the meme files. You cut the
  voice, sync the memes, crop, blur. (Reference sizes: 146 memes, 442 cuts, 240 masks, 20:07; 171 memes, 503 cuts, 187
  masks, 20:51.)
- **Blur and crop pass**: a human editor already cut the voice and placed the memes; you add sizing, crops and blurs to
  their timeline without touching their cuts (reference: 190 slots, 31 crops, 239 masks).

## Full edit, stage by stage
| # | Stage | Script(s) | Mac | Windows |
|---|---|---|---|---|
| 1 | Unpack and look: codecs (VP9 in MP4 becomes H.264), voice channel (often right only), loudness floor | ffprobe by hand | yes | yes |
| 2 | OCR every meme (WebP to PNG first) and the recording's Drive title bar at 2 fps | prep_ocr.sh, ocr_batch.swift, screen_runs.py | yes | OCR step needs a replacement (our ocr.ps1 + a converter to the same JSON) |
| 3 | Speech regions and pieces from the loudness envelope | regions_full.py | yes | yes |
| 4 | Transcribe every piece on its own (catches restarts a whole-file transcript merges); re-transcribe repetition garbage; list restarts | pieces_asr.py, fix_loops.py, restart_check.py | yes (mlx-whisper) | swap to faster-whisper |
| 5 | Assign phrases to memes: the title bar first, then text matching against every meme's OCR (off-screen reads); flags restarts, noise, stray fragments | assign.py | yes | yes |
| 6 | Your review: decisions.json (cuts, reassignments, trims inside phrases, per-meme overrides: crops, reveals, black boxes). Read the review file line by line | by hand | | |
| 7 | Blur plan from the house rules (opening wipe, snaps, long blocks wiped while read, curse words); curse boxes sized from the real letters | plan_blurs.py, tightbox.py | yes | yes (set WORDS_FILE) |
| 8 | Edit list: voice cut edges from the audio (-70 dB handles, breaths, -55 dB scan), crops (minimal, watermarks, site bar, unread panels, carousel dots, balance, tighten), sizes, blurs with times | build_full_edl.py, crop_util.py | yes | yes |
| 9 | QA before building: no cut edge inside speech; every meme as it will appear with its blur boxes coloured by type; what the tighten rule changes | cut_qc.py, sheet.py, preview_tighten.py | yes | yes |
| 10 | Import: a new project with the recording and background, then the memes 20 per bridge call, saving after each (one call with about 170 imports stalled Premiere 2025) | gen_import_full_jsx.py + pp.py | yes (bridge) | ours: fcpxml.py assembly instead |
| 11 | Build: voice cuts on V1/A1 and memes on V3 by setInPoint/setOutPoint + overwriteClip, each placement read back and retried (it silently fails now and then); ends forced to the planned frame; gap audit. Refuses an existing or open target project | gen_build_full_jsx.py + pp.py | yes (bridge) | ours: fcpxml.py (V1/A1 cuts, V2 background, V3 memes) |
| 12 | Patch the saved project: masks (static boxes, keyframed wipes, feather per rule), instance names, +15 dB clip gain capped at -0.5 dBFS peaks, video meme speeds; gap audit on the result | patch_full.py, prproj_masks.py, xml_gap_audit.py | yes (Premiere 2025 masks) | Premiere 2026 masks: our prproj_lib (AEMask2) |
| 13 | Verify: reopen, audit, export check frames at wipe starts, mid-wipes and curse close-ups; every A1 clip matches the plan. Leave it open for review; no export | gen_verify_full.py, check_a1.py | yes (bridge) | ours: Premiere UI check / Export Frame |

## Blur and crop pass on an editor's cut
`editor_timeline.py` reads the editor's tracks to JSON; `pieces_asr.py` transcribes each of their voice clips;
`plan_pass.py` plans crops and blurs per meme slot (it carries the 13 Oct feather and edge rules); `gen_build_pass_jsx.py`
adds sizes and effects to their existing V3 items in a COPY of their project; `patch_pass.py` adds the masks;
`gen_verify_pass.py` exports check frames. A Windows editor's project opened on a Mac needs its media paths rewritten
first.

## Diffing the user's fixes (how the rules were learned)
`../reference-pipeline/review_tools/` (see its README): unzip both projects to XML, `extract_fx.py` per project, then
`cut_diff.py` and `cut_detail.py` (voice frames removed or added, with words and levels), `meme_diff.py` (per meme:
span, crop, scale/position, every blur with key times measured against what he says, not clip in-points), `rects.py`
(visible rectangles), `crop_sheet.py` and `blur_sheet.py` (yours red, his green). Turn every pattern into a rule in
`house-rules.md` and a default in the code.

## Inputs no script makes (make them by hand per job)
- `db10ms.npy`: the raw voice channel's level every 10 ms in dBFS (100 values per second), read by six scripts. The
  source does not say RMS or peak: calibrate on a known pause (room noise should read -72 to -80 dB) before trusting
  the -70 / -60 / -55 dB thresholds. premiere-ae-editing's `speech_cuts.py` measures the same scale its own -70 / -55
  rules use (dBFS RMS per 10 ms of the loudest channel of the raw file, so a voice on one side counts at full level),
  and can write the file: `python -c "import sys, numpy as np; sys.path.insert(0, '<skill>/scripts/media');
  import speech_cuts as s; np.save('db10ms.npy', s.levels('raw.wav'))"` with `<skill>` =
  `~/.claude/skills/premiere-ae-editing`. Its `--scan` and `--phrases --wav-dir` modes are the same edge scan and
  per-piece transcription this pipeline does (premiere-ae-editing `references/timing.md`).
- `raw_a0.wav` (16 kHz mono voice, for transcription) and `raw_st48.wav` (48 kHz stereo, for the gain caps): ffmpeg
  extracts of the recording.
- `video_ocr.jsonl` (text from video memes, read by build_full_edl.py) and `verify_picks.json` (check-frame picks, read
  by gen_verify_full.py).
- `decisions.json` / `decisions_pass.json`: your review (stage 6).

## Failure modes the reviews exposed (guard against them)
- Side trims of 3% or less on tight screenshots clipped first letters: trim a side only where the band is uniform and
  has no OCR text.
- A white card behind a caption and photo made the phone crop drop the photo: extend over any run that overlaps the
  text.
- Metadata crops cut a caption he reads, or the bottom reaction row when another showed higher up.
- Lines sorted by y across columns split 2-line labels in two-column grids: group lines per column.
- "Line 1 stays visible" must mean the meme's first text line, not the first line after a title.
- Repeated label text aligned to its first occurrence; a wipe's reading end matched a word in the next label.
- Snap ramps clamped to 4 to 12 frames instead of a per-line ramp; wipes ending on the transcript's word end instead of
  +0.25 s or chained to the next reveal.
- A relative loudness threshold (floor + 12 dB) treated room noise as speech: use -70 dB absolute; detect breaths.
- A cap on long last words dropped word endings; transcript mistiming cut into words: take every edge from the audio.
- Regex escapes inside raw strings (`\\.`) silently broke watermark patterns.
- The unread-panel rule cut whole pictures until it required a flat panel down to the unread text; the carousel rule
  fired on movie posters until it was limited to phone screenshots.
- Meme overwrites need the same read-back-and-retry loop as voice cuts; stills can land a frame short and leave a hole
  (audit gaps on every used track before saving).

Source: adapted from a friend's Mac skill set (Oct 2026)
