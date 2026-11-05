# Metro Media House study folder

Start with `STUDY.md` (findings, numbers, style law, effects, script formula, use/change/drop list).
`SHOT-LOG.md` has what is on screen for each word run in all 4 reels.

## Contents
| Path | What |
|---|---|
| `STUDY.md` | The study |
| `SHOT-LOG.md` | Shot-by-word reading of every reel |
| `numbers.json` | Every number in the main table, per reel, from `tools/summary.py` |
| `raw/<id>/scores.json`, `events.json` | `frame_scores.py` and `cut_events.py` output |
| `raw/<id>/evsheet/` | `event_sheets.py` strips of every cut event |
| `raw/<id>/ref_stats.txt`, `shots_ref.json` | `ref_stats.py` output. Its section rows (hook 0-5, context 5-20 ...) are hard-coded from the Altman reel, so ignore them; use the quarters in `numbers.json` |
| `raw/<id>/motion.json` | `motion_class.py`, moving vs still per shot |
| `raw/<id>/shotwords/` | `ac_shot_words.py` sheets (one frame per shot with its words) and shot list |
| `raw/<id>/colour.json` | `colour_stats.py` |
| `raw/<id>/gap_level.json` | `tools/gap_level.py`: music level in voice gaps |
| `raw/<id>/beat_map.json` | `beat_map.py` on the full mix |
| `raw/<id>/inverted.json` | `tools/invert_frames.py`: single colour-inverted frames |
| `raw/<id>/timesheet_1s.jpg` | `time_sheet.py`, one frame a second |
| `strips/` | Every frame of: the first 3 s of each reel, all flash and flicker events, the PAL receipt, both organic endings, both ad tails, the EIN cursor, the YC photo walk |
| `captions/` | Full-resolution frames used to measure the captions (JPEG quality 92) |
| `script/` | Tagged scripts (E, T, I per sentence) and `interest_score.py` output |
| `tools/` | Scripts written for this study (below) |

Re-run everything: `cd research/metro-media-house && tools/run_all.sh`, then the extra tools listed below.

## Tools
Repo tools run as they are: `frame_scores.py`, `cut_events.py`, `event_sheets.py`, `ref_stats.py`, `motion_class.py`, `frame_strip.py` (minidoc-reference-style); `ac_shot_words.py`, `colour_stats.py` (word-matched-broll); `beat_map.py`, `time_sheet.py` (reference-study); `interest_score.py` (story-script-writer).

Repo scripts changed for Linux (font path only, with a fallback so they still work on a Mac):
- `skills/minidoc-reference-style/scripts/event_sheets.py`
- `skills/minidoc-reference-style/scripts/frame_strip.py`
- `skills/word-matched-broll/scripts/ac_shot_words.py` (already fell back to PIL's tiny default font; now tries DejaVu Sans first)

Not changed: `skills/reference-study/scripts/gap_sfx.py` has paths hard-wired to old jobs. `tools/gap_level.py` repeats its level measurement (voice RMS over word spans against RMS in gaps over 0.12 s, trimmed 0.04 s) and leaves out the sound-hit count, which the repo itself marks unreliable.

New here: `tools/run_all.sh`, `tools/gap_level.py`, `tools/invert_frames.py` (a frame is an inverted frame when its correlation with a neighbour is below -0.5 or -0.6 on 96x54 grey), `tools/flash_sheet.py`, `tools/summary.py`.

## Installs
None for this study. Earlier in this session, before the no-install rule, these were installed from PyPI: yt-dlp 2026.10.26, opencv-python-headless 5.0.0.93, faster-whisper and scipy. None of them was used for these results: the scripts that ran need only numpy, Pillow and ffmpeg, which came with the environment. The faster-whisper model never downloaded (Hugging Face is blocked), so the supplied transcripts were used. OCR (tesseract) is not installed, so captions were measured by eye.

## Trust
See `STUDY.md` section 3. In short: lengths, words, words a minute and cut timing are solid. Shot counts depend on the tool. Moving share, tempo and music level are weak on this page. Every soundbite, font match and score mark is judged, not measured. Nothing was heard or watched in motion.

## Transcript corrections made from frames
- PAL: "Palmer Lucky" is Palmer Luckey (on-screen "Palmer Luckey"); "Teal" is Thiel.
- YC: "Graham funded eBay" is "Graham funded him again" (on-screen caption at 47.0 s).
- Not corrected, as nothing on screen confirms them: other names and numbers were spot-checked against printed numbers on screen ($10,000.00, 1.4 billion, 35%, 17, $43 Million, $6 thousand, hundred and twenty-two, Five thousand, 13) and matched.

Rights: the reels belong to their owners and are for private study only (see `reference-reels/README.md`). Frames here are low-resolution study crops.
