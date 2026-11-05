# Bulk cutdowns

The tool code for this pipeline stays on Kanishk's PC; this file keeps the method so it can be rebuilt.

Long source videos (already-edited documentary uploads) cut into long cuts, 5 to 6 minute standalones and one-shot
shorts, with the editor's house recipe (hook, dip to white, story, mid-video insert, end plug, very low dynamic music).
Built 11 to 14 Oct 2026: 11 sources, about 40 distinct cuts. A round went from most of a day to about 40 minutes for
two long cuts, and 15 files were made unattended in about 2 h 25 min. How to cut (hooks, story shape, how much to keep,
tight edges, music by role) is in editing-playbook; this file is the machine: the tools, the spec, the guards, the round
script and the render. The tools themselves are not part of the kit: read it as the method, the guards and the numbers.

Layout: `cuts/roundN.py` (batch plan and render scripts; `round8.py` is the newest template) and `training/tools/`
(the tools). `ytdl.py`, `edge_shots.py` and `edge_words.py` live in premiere-ae-editing's `scripts/media/`.

## 1. The chain, per source video
| Step | Tool | Notes |
|---|---|---|
| 1 Pick | `pick_next.py`, `yt_meta.py`, `yt_outliers.py`, `hook_vs_replay.py` | score title action words, topic multipliers, the YouTube outlier band (2 to 4x did best), length (18 to 45 min feeds a long cut, a standalone and shorts) and freshness (never posted, or 180+ days since); then check by hand that the editor has not already cut it and the page has not posted it (length +-5% and title) |
| 2 Download | `ytdl.py ID --out DIR` (skill) | 1080p H.264, at least 720p with no lower fallback (a 360p file once slipped through), one at a time across sessions, about 1 min |
| 3 Prep | `prep_source.py VIDEO PREPDIR [--chunk 300] [--jobs 5] [--no-align]` | audio, loudness, transients, motion, shots, WhisperX words, frame-exact subtitle spans with OCR in 300 s chunks, merged captions, subtitle-guided words, `screenplay.txt`; 3.3 to 16.8 min per 12 to 36 min source; a GPU lock (two large Whisper models do not fit in 12 GB) |
| 4 Unread subtitles | `sub_strip.py` then `--apply fixes.json`; re-run caps_merge, sub_align, screenplay | coloured speaker boxes fail OCR: read them by eye from one strip |
| 5 Understand | read `screenplay.txt` and the heatmap peaks; small labelled frame grids only for no-speech windows and hook candidates; `crop_strip.py` for on-screen counters | subtitles first, `~` = ASR-only speech, `~~` = no-speech stretch with loud-hit, motion and shot flags; watch for cross-promo clips from other videos (cut them whole); stateful counters ("Items: 01-07", "SCORE: n") must stay in order in long cuts |
| 6 Logline + arc map | by hand | one sentence per cut (the stranger test); arcs in source order; the arc break for the mid insert (about 45 to 55%) |
| 7 Cut list | `cuts/<key>/_working/cut_long_v1.txt` | the spec (section 2) |
| 8 Snap + audit | `edl_text.py` -> `snap_audit.py EDL.json PREPDIR --snap SNAPPED.json --report SEAMS.txt` | fix or justify every FAIL; then `edge_shots.py`, `edge_words.py`, and `words_at.py` for word-tight shorts |
| 9 Plan | the round script (`--plans`) | beds per scene, scene flashes, SFX, inserts, end plug; dry-check the audio layout |
| 10 Hold or render | `roundN.py --render [keys]` | one video at a time behind `heavy_gate`; about 6x real time on the GPU |
| 11 QC | `seam_verify.py`, `qc_seams.py --sheet`, `tp_fix.py` | look at every flagged seam and both sides of every white transition; fix the cut list and re-render from the cache, same name if not yet delivered |
| 12 XML | `make_xml.py TIMELINE.json PLAN.json REASONS.json OUT.xml "Name"` + `fcpxml.py --check` | markers carry the reasons |
| 13 Notes (optional) | `cut_notes.py`, `derive_reasons.py --from-long`, `shorts_notes.py` (warns when a short has no logline), `summary_edl.py` | pages per cut; skipped when speed matters (the XML markers carry the reasons) |
| 14 Deliver | MP4 + XML side by side | `<Title> - long cut vN.mp4`, `<Title> - standalone vN.mp4`, `shorts/<Title> - short A vN (<logline gist>).mp4`; report (references/review-pages-and-qa.md) |
| 15 Review | `review_diff.py` | the editor's hand re-cut of the imported XML, diffed clip by clip; rules into the review log, memory and tool defaults |

## 2. The text cut list (the spec)
- Header lines `key: value` (source, format, logline); sections `[hook]` and `[story]`; one clip per line:
  `IN > OUT | note`.
- Anchors instead of bare seconds: `e:<sec>` (a subtitle edge by time), `h:<sec>` (an exact hold, never shifted),
  `c:<subtitle text>` or `w:<words>` (with `@lo-hi` to pick the occurrence), or a plain number that snaps to a pause.
  Why: times written against one transcript slipped onto neighbouring words once a better transcript replaced it.
- Inserts: `!insert FILE gain=+4.5 [nofx]` after the story clip at the arc break (long cuts only).
- `edl_text.py` turns it into JSON; split edits are clips of `[in, out, sound_tail]`.

## 3. Snap and audit (`snap_audit.py`)
- Snapping puts cuts in real pauses on whole frames: `PAD_OUT 0.25`, `PAD_IN 0.20`, `MIN_CLIP 0.5` (from the editor's
  measured habits: out 0.29 s after the last word, lead-in 0.5 s). A point more than 0.35 s from any word holds still
  (a snapper once dragged no-speech points to the nearest word and silently dropped 60 s of action).
- Guards: `c_refine` (words longer than 1.2 s are ignored: ASR smears them); `shot_guard` (a camera switch within 30
  frames, correlation under 0.5 and difference over 20, moves the cut onto the switch, never into speech); a split-edit
  sound tail of up to 0.35 s; a subtitle-pixel guard (0.013: white next to dark outline means a line is still on
  screen); a censor-mute FAIL (5 or more consecutive 10 ms frames under -90 dBFS inside speech is a bleep, part of the
  word).
- The audit runs independently: a cut inside a word, a bang within +-0.12 s, a cut inside a caption, a clip under
  0.5 s. "Inside caption" is expected on word-tight shorts.
- Edge checks before rendering: `edge_shots.py` (stray frames: a cut = a change over 4x the window median and over 12)
  and `edge_words.py` (the words at every edge, with COMMA, DIGITS and CENSOR flags), run against the raw ASR words too.
- Envelope windows are clamped (a negative index once sliced the whole array).

## 4. The round script (`cuts/roundN.py`)
- Holds each video's source, fps, bed plan and flash points. `--plans` is the cheap step; `--render [keys]` renders
  one video at a time behind `heavy_gate`; the chain per video is render -> seam verify -> make XML (with check) ->
  QC sheet -> true-peak fix, printing one line per finished step so a Monitor can stream it; QC fixes go into a
  re-render pass after the batch (fast from the cache). Why: on a shared machine the user says "go" once, and one line
  per step shows any failure without reading logs. Make its paths configurable before reuse.
- **Plan defaults the tools apply** (the taste and the reasons are in editing-playbook):
  - Beds by role, as target loudness: calm -35, tension -33, running (fast movement) -31, action -28, hook -27 LUFS;
    gain = target minus the track's own loudness. Why: beds at -38 to -40 were "toooooo low raise it just a bit".
  - One bed per scene, 6 to 10 segments per long cut, switched on story beats; each reuse starts at a different offset
    into the track (0, 20, 30, 40, 60, 100, 120 s) so loops never restart at the same spot; fades in 1.0 to 1.5 s (0.2 to
    0.6 s into action), out 1 to 2 s; the hook bed is the riser at -27 LUFS, in 0.2 s, out 0.4 s; beds pause under the
    mid insert (out 0.25 s, back over 0.6 s) and resume where they stopped; music drops before a key loud moment.
  - Hook to story: a dip to white (the render flashes white over 0.1 s, then the story fades in from white over 0.3 s;
    the editor's own Premiere preset runs 0.33 to 0.47 s centred on the cut, and 0.20 to 0.27 s into the end plug, so a
    finished XML matches the render) plus a whoosh starting 1.3 s before the cut and a camera shutter on the cut, both at
    -4 dB; into the end plug the same pair with the shutter 0.1 s early; scene flashes (4 frames out to white, 6 back,
    on 2 to 3 big jumps per long cut) and the insert's in and out with the same pair at -10 dB, shutter 0.05 s early; a
    whoosh that would start before 0 s plays only its tail.
  - Inserts: the mid insert whole (it measures -20.7 LUFS, so +4.5 dB); the end plug (its first 3.62 s, +4.5 dB) on
    every cut since 13 Oct. Render plan keys: `cta`, `cta_from`, `cta_to`, `cta_gain_db`.
  - A 4-frame equal-power crossfade on every audio edit, centred on the cut.
- Dry-check the audio layout before rendering: no bed edge inside a removed stretch, story positions mapped
  explicitly (a scene flash landed one clip early after an insert shifted the indices), 0.5 s nearest-edge tolerance.
- A bed that started 0.4 ms after an insert's first frame was not paused by the test; the fix is in the layout
  (`if ga - 1e-3 <= cur < gb: cur = gb`).

## 5. The renderer (`render_cut.py`)
- `python3 render_cut.py SNAPPED.json PLAN.json OUT.mp4 [--resume] [--keep] [--no-cta]`; writes `.timeline.json`.
- MPEG-TS parts with `-video_track_timescale 15360`, a part cache keyed on the exact command plus the input's size and
  modification time, `plan['jobs']` parts encoded at once (default 4), the encoder from `plan['encoder']` or
  `CUT_ENCODER` (default NVENC cq 21; when NVENC is missing it falls back to libx264 CRF 16 by itself, so a Mac renders
  on the CPU until a VideoToolbox branch is added and benchmarked with `render_bench.py`), inserts padded to their
  slot, the master chain (two-pass loudnorm, limiter 0.70, `-aac_pns 0`). All numbers: references/render-pipeline.md
  sections 4 to 6.
- The render and the XML share `audio_layout`, so the XML check also tests the render.

## 6. The Premiere XML (`make_xml.py`)
- V1 picture linked to dialogue on A1-A2; A3-A4 music (a bed that overlaps the one before moves to the next pair);
  A5-A6 shutters; A7-A8 whooshes. Levels are set; fades and crossfades are not (the editor adds the dip-to-white preset
  when finishing).
- Markers: each removed stretch with its reason in the comment, DIP TO WHITE, WHITE FLASH, the insert.
- Loop beds as back-to-back clips 0.05 s clear of the file's end; every `<file>` declares every stream its clips use;
  `fcpxml.py --check` every XML. Premiere refused every XML ("File Import Failure") until both were fixed; the tell
  was a `.ims` file named after the XML with a blank format. The fix came from copying a file that already imported on
  that machine and listing every element ours used that it did not.

## 7. Review loop
- The editor teaches by re-cutting our imported XML in their own manual project ("dont remake or anything just
  understand"). `review_diff.py USER.prproj PREPDIR OUT.txt "SEQ NAME=CUT.timeline.json"` (read-only; needs the skill's
  prproj_lib) lists every change with words, subtitles and loudness. Untouched parts count as approvals.
- Measured hand trims from one review: long-cut hook 18.0 to 14.5 s (-19%), standalone hook 14.7 to 12.5 s (-15%),
  shorts -9%, -31% and -4%; stories, the insert spot and a 5:30 closing section untouched.
- Every review becomes dated rules in the review log (newest first) plus a memory gist and a tool default; "Don't fix
  the reviews on these" means apply from the next video.

## 8. Picking and analytics (optional)
- YouTube: `yt_meta.py` (heatmap, replay peaks, chapters; `yt-dlp -J`, about 45 s per video, nothing downloaded),
  `yt_outliers.py` (outlier = views / median of the 15 uploads either side, from `--flat-playlist -J`), `pick_next.py`,
  `hook_vs_replay.py` (the editor's own hook clips sat at a median 95th percentile of the heatmap).
- Calibration: `analyze_edits.py` (a project dump to per-edit stats), `habits.py`, `pair_report.py`, `score_cut.py`
  (blind-test precision and recall against the editor's own cut: 84% / 69%), `render_bench.py` (encoder speed, size,
  VMAF), `crop_strip.py` (a 480x120 crop costs about 1/20 of a frame), `quiet_beats.py` (dead beats inside kept clips).

## 9. Research reports behind the defaults (not in the kit)
- A long-cut editing report (26 sourced rules: gaps between kept sentences at 30 fps of 3 to 6 frames tight, 9 to 12
  normal; J-cuts of 6 to 15 frames; compress waiting, never cause and effect; the dated outcome as the last 10 to 20 s;
  QC 12 frames either side of every cut) and a dynamic-music report (bed levels, switching on bar lines, cue counts,
  Epidemic stems and recut limits). Both tag each claim as primary, vendor or synthesis. The reports themselves are not
  in the kit; the cutting taste they feed is in editing-playbook.

## 10. Do not ship or run
- Superseded: `captions.py` (by `caption_timeline.py`), `digest.py` (by `screenplay.py`), `asr_all.py` and `prep_all.py`
  (first-day batches), `wx_align.py` (by `wx_transcribe.py` + `sub_align.py`), `patch_render_inserts.py` (one-off).
- Check every docstring and default is neutral before sharing outside the team. Some original tools named the client;
  the kit copies were scrubbed on 14 Oct 2026 (client name out of the docstrings and the CTA line, private names out of
  the bed labels and the review log; the library README lists every change). Re-check after any new copy from
  Kanishk's PC.

## 11. Backlog (promised, not built)
OCR for coloured subtitles; an automatic first-pass cut; automatic music beds from loud moments and motion; a one-command
shortlist that prefetches the next two picks; 10 s hook previews before full renders; an echo finder; in-point
reach-back only where the loudness shows voice; regenerated XMLs for the first two sources (still the old refused
kind).

## 11b. Extending
- **A new round:** copy the newest round script, list the new sources and their plans, run `--plans`, then render
  when the user says go. Make paths settings, not constants.
- **A new rule from a review:** put it in the review log (dated, newest first), then into the tool that enforces it
  (a snap guard, an audit FAIL, a plan default), and test it against the reviewed cut it came from.
- **A new format or client:** fork the folder; the house recipe lives in the plan defaults (beds, flashes, SFX,
  inserts, end plug) and the renderer, so a new client means new plan defaults and insert files, not new code paths.
- **Vertical versions** (offered, never asked for): a new crop and layout step in the renderer plus a 9:16 XML layout.

## 12. Risks the boss decides
- The YouTube route uses PO tokens to get past YouTube's bot check: it may breach YouTube's terms even for a client's
  own uploads. Masters from the client are cleaner and better quality. Use only with rights to the footage.
- Sensitive footage: keep the warning-screen-safe cutting rules (editing-playbook) and get the user's call before
  posting sensitive cuts.
- The music plan must cover client work with the page safelisted; it was never confirmed in writing.

## 13. On the Mac (untested)
| Windows piece | Mac replacement |
|---|---|
| Windows OCR (`ocr.ps1` through PowerShell) in the subtitle tools | Apple Vision (the skill's `ocr.swift`, or the `ocrmac` package) or Tesseract, writing the same JSON |
| CUDA WhisperX and faster-whisper | CPU, or whisper.cpp / mlx-whisper for ASR with WhisperX alignment on CPU or MPS; expect several times slower than the 12 GB RTX laptop |
| `prep.py`'s CUDA DLL setup (`os.add_dll_directory`) | always pass `--skip-asr` |
| WhisperX venv `Scripts\python.exe` in `prep_source.py` | `<venv>/bin/python` |
| NVENC in `render_cut.py` | `h264_videotoolbox` or libx264, chosen by `render_bench.py` |
| PowerShell process queries in `heavy_gate.py`, ctypes PID checks, Win32 battery calls | `ps -axo command` (the kit copy of `heavy_gate.py` already switches to it on a Mac) or psutil, `os.kill(pid, 0)`, `pmset -g batt` |
| `%USERPROFILE%`, `%TEMP%` | `~`, `tempfile` |
| `fcpxml.py` URLs | fixed in the kit's copy of the skill (14 Oct 2026): each `<pathurl>` follows its own path's form, so a Mac path no longer gets a doubled slash after `file://localhost`, and `--check` reads both forms. Still untested: importing such an XML in Premiere on a Mac, so test one first |
