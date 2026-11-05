# Reference pipeline (the real scripts from the reference jobs, renamed neutral)

These built one full edit and one blur and crop pass (11 and 13 Oct 2026). They are job code, not a packaged tool: read
a script before running it and change its constants for the new job. Stage order and purpose: `../references/pipeline.md`.

## Run rules
- Copy this folder into the job's own `_pipeline` folder and run from there, in stage order: scripts read and write job
  data by relative name (`regions_full.json`, `pieces_asr.json`, `assign.json`, `decisions.json`, `edl_full.json`,
  `data/...`). `check_a1.py` imports `tl.py` from `review_tools/`.
- Paths and names are `/CHANGE/ME/...` and `CHANGE_ME ...` placeholders, so a script fails fast until it points at
  the new job.
- Never build into a project the user has open; the generated Premiere scripts make a NEW project or open a COPY.
- Downloading the client's folder, or clean copies of watermarked memes, only when the user asks (rights stay with the
  posters; the client decides fair use).

## Constants to change per job
| File | Constant |
|---|---|
| `assign.py`, `build_full_edl.py`, `screen_runs.py`, `crop_util.py` | `CLIENT` = the client folder (recording + memes) |
| `build_full_edl.py` | `RAW` = the recording's file name |
| `prep_ocr.sh` | `C` (client folder), `REC` (recording file name), `PY` (python3 on a Mac, python on Windows), the title-bar crop |
| `gen_build_full_jsx.py` | `OUT` (where the project is written), `"seq"`, the project name (or argv 1) |
| `patch_full.py`, `gen_verify_full.py` | `PROJ`, `SEQ`, `OUT` (check frames) |
| `editor_timeline.py`, `plan_pass.py` | `SEQ` = the editor's sequence name |
| `gen_build_pass_jsx.py`, `patch_pass.py`, `gen_verify_pass.py` | the editor's project COPY and output folders |
| `patch_full.py`, `patch_pass.py` | `NAMES`, `CROP_NAME` = the client's own preset names |
| `xml_gap_audit.py`, `check_a1.py` | the sequence name is an argument |
| `review_tools/*` | `MEME_SEQ` environment variable = the sequence name |

## Every script, by platform
Mac = the friend's Mac with Premiere 2025, as the jobs ran. Windows = this PC (Premiere 2026, Python 3.13, ffmpeg).

| Script | What it does | Mac | Windows |
|---|---|---|---|
| prep_ocr.sh | WebP to PNG, a middle frame of each video meme, OCR of every meme and of the title bar at 2 fps | yes | Git Bash with PY=python; the OCR step needs our ocr.ps1 plus a converter to the same JSON (normalised boxes, lines, words); no slanted-text quads |
| ocr_batch.swift | Apple Vision OCR: lines, words, boxes and four-corner quads that follow slanted text | yes (swiftc) | no |
| wins.swift | lists Premiere's windows (System Events cannot see them) to spot a stuck instance | yes (swiftc) | no; use tasklist / the Premiere UI notes |
| screen_runs.py | which file the Drive preview shows when, from the title-bar OCR | yes | yes |
| regions_full.py | speech regions and pieces from db10ms.npy | yes | yes |
| pieces_asr.py, fix_loops.py, restart_check.py | per-piece transcription, re-transcribe loops, list restarts | yes (mlx-whisper, Apple Silicon) | swap `mlx_whisper.transcribe` for faster-whisper (our hear.py setup; same word fields: word, start, end) |
| assign.py | phrase to meme by screen then text; flags restarts, false starts, duplicate words at joins | yes | yes |
| plan_blurs.py | the house blur plan from OCR lines and timed words | yes | yes; set WORDS_FILE to a word list or every 4+ letter "name:" counts as a username |
| tightbox.py | curse box from the real letter pixels, feather max(10, 14 / scale) | yes | yes |
| crop_util.py | all crop rules (auto, phone, metadata, site bar, balance, tighten, unread panel, under-photo, carousel) | yes | yes (path fix done) |
| build_full_edl.py | the full edit's EDL: cuts from the audio, crops, sizes, blur times | yes | yes; its mask feather is still the Oct 4 rule, port `plan_pass.feather_for` |
| cut_qc.py | flags cut edges louder than -55 dB on both sides | yes | yes |
| sheet.py, preview_tighten.py | review sheets of every meme as it will appear / what tightening changes | yes | yes (font fallback done) |
| dbg_plan.py | prints the blur plan of named memes | yes | yes |
| gen_import_full_jsx.py, gen_build_full_jsx.py, gen_verify_full.py | Premiere 2025 ExtendScript run through the bridge (pp.py --v 2025) | yes | the bridge needs Adobe's PlayerDebugMode in the registry (a security setting: the user's call); ours: fcpxml.py assembly + prproj_lib |
| patch_full.py, patch_pass.py, prproj_masks.py, mask_template_pp2025.xml | masks, names, gain and speeds written into the saved .prproj | yes (Premiere 2025 mask format AE.ADBE AEMask) | Premiere 2026 projects: our prproj_lib (AEMask2, mask_path_blob) |
| xml_gap_audit.py | every used track continuous from 0 to the end, clips on frame boundaries | yes | yes |
| check_a1.py | every A1 clip matches the cut plan | yes | yes |
| editor_timeline.py, plan_pass.py, gen_build_pass_jsx.py, gen_verify_pass.py | the blur and crop pass on an editor's cut | yes | planning yes; Premiere steps as above |
| extract_fx.py, diff_fx.py, blur_diff.py, blur_stats.py | effect and mask dumps and diffs between two saves | yes | yes |
| review_tools/ | diff the user's fixed project against the delivered baseline | yes | yes (font fallback done) |

## What changed from the source
- Neutral names: client channel, job and sequence names, people's names and meme file names are gone. Scripts that
  carried job names are renamed by job type: full-edit scripts end in `_full`, blur and crop pass scripts in `_pass`
  (`plan_pass.py`), the editor's timeline reader is `editor_timeline.py` (data files follow: `data/edl_pass.json`,
  `data/editor_timeline.json`, `data/editor_cut.xml`, `decisions_pass.json`). Effect instance names are neutral
  constants.
- Safety: `prep_ocr.sh` used to paste file names into Python code (`python3 -c "...open('$f')..."`), so a crafted file
  name in a downloaded client folder could run code; names are now passed as arguments. Three scripts ran another
  script's text with `exec()`; they now import it (`gen_build_full_jsx.py`, `review_tools/cut_diff.py` and
  `meme_diff.py` got a `__main__` guard so importing them only loads data and helpers).
- Portability: `crop_util.py` finds its folder with os.path (the old `/` split broke on Windows paths); the PIL sheets
  fall back from the Mac Arial path to Windows Arial; `plan_blurs.py` takes `WORDS_FILE`; stale names fixed
  (`check_a1.py` read `rev/` and `edl_v2.json`, `restart_check.py` read `edl.json`; `xml_gap_audit.py` and `tl.py` had
  a job's sequence name as the default).
- Dropped `balance.py`: an older copy of `crop_util.balance_margins` with no imports of its own (it cannot run alone).
- Not changed: every rule, threshold and number in the logic.
- Checked here (14 Oct 2026): all 37 Python files compile; `prep_ocr.sh` passes `bash -n`; prproj_masks' path encoder
  round-trips exactly through extract_fx's decoder (rectangle and slanted quad); the 24-param mask template loads.
  Nothing was run against a real project.

Source: adapted from a friend's Mac skill set (Oct 2026)
