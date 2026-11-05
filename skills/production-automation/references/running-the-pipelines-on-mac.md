# Running the pipelines on the boss's Mac

The pipelines were built and run on a Windows laptop (RTX GPU with 12 GB, NVENC, Windows OCR, Git Bash). Most of the
code is plain Python, ffmpeg and Chrome and ports directly; the parts below do not. Anything marked "untested" has not
been run on a Mac yet. App-level Mac facts (After Effects by AppleScript, aerender, the Premiere bridge, Apple Vision
OCR, mlx-whisper, fonts) are in premiere-ae-editing's mac notes.

## 1. Before the first run
1. **Copy the pipeline out of the kit.** The library lives at `~/VisionKit/kit/library/pipelines/<name>/`, and kit
   updates replace everything under `~/VisionKit/kit/`. Copy the folder to a working place (for example
   `~/VisionKit/mine/work/<name>/` or a job folder) and run it there, so batches, finals, caches and downloads are never
   overwritten by an update and never block one. Keep media out of the kit.
2. **Read the folder's README** (and `00-status.md`, `PLAYBOOK.md` where they exist).
3. **Point the scripts at this Mac.** The kit's copies were patched while packaging (14 Oct 2026) to read their paths
   from environment variables, falling back to Mac defaults. Check the top of each script; the list may have grown:

| Variable | Used by | Set it to |
|---|---|---|
| `PAE_SCRIPTS` | most tools (hear.py, frames.py, fcpxml.py, prproj_lib, ae_build) | the premiere-ae-editing `scripts/` folder (default `~/.claude/skills/premiere-ae-editing/scripts`) |
| `CHROME_PATH` | newsdesk, studio | `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome` (also found automatically) |
| `VC_FONT_DIRS` | newsdesk builders | extra font folders, `:`-separated (the Mac folders are searched by default) |
| `VC_DRIVE_DIR` | newsdesk `vcn.py drive` | `~/Library/CloudStorage/GoogleDrive-<account>/My Drive/<news posting folder>` |
| `OUTCOME_DRIVE_DIR` | the studio's newsdesk fork | that client's own posting folder (never the news pages' folder) |
| `VC_RESEARCH_DIR` | `scan.py --full` | the folder holding `03-news-feeds.json`: the library's `research/music-pages/`. It is found by itself inside the kit layout; set it once the newsdesk is copied to a working folder |
| `FONT_DIRS` | edits-kit `typeset.py` | extra font folders, `:`-separated (Adobe Fonts activations have no file path) |
| `TEXTMETRICS_ROOT` | studio `research-tools/textmetrics.py` | the folder holding `data/refs.jsonl` (the default is a path on Kanishk's PC) |
| `VLC_PATH` | ad-build-kit audio and frame tools | the VLC binary (`/Applications/VLC.app/Contents/MacOS/VLC` is found by itself); or swap in the skill's PyAV `atools.py` |
| `WHISPERX_PY` | `prep_source.py` | the WhisperX venv's `bin/python` |
| `CUT_ENCODER` | `render_cut.py` | `x264` until a VideoToolbox option exists (it falls back to x264 by itself) |
| `ONLY`, `GFXDIR` | `ONLY`: the skill's `ae_build.py` (comma-separated block or shot names to build); `GFXDIR`: ad-build-kit `work/qa_gfx2.py` (the AE graphics output folder) | filters and folders for one run |
4. **Check the machine:** `python3 --version`, `ffmpeg -version`, Chrome, free disk (`df -h /`), power for long jobs
   (`pmset -g batt`, untested), and the logins the pipeline reads through.
5. **Run one test item** (one post, one plan, one short), look at its sheet, and import one XML in Premiere before a
   real batch.

## 2. Common setup on a Mac
- **Python:** Homebrew's Python is "externally managed", so use a venv per pipeline (or one shared venv) and run tools as
  `python3 -X utf8 <tool>.py`. Windows-only quirks (`python -I` hiding user site-packages, cp1252 consoles, Git Bash
  path rewriting) do not apply.
- **Packages by pipeline:** newsdesk: Pillow, `av` (PyAV); studio: Pillow, numpy, websockets (sync client), `av`,
  optionally esprima; edits kit: PyAV, numpy, Pillow, torch + torchvision, SAM 2, open_clip_torch, faster-whisper or
  mlx-whisper; cutdowns: numpy, PyAV, Pillow, WhisperX in its own venv. Every install needs the boss's OK (name,
  source, size).
- **Tools:** `brew install ffmpeg deno`; `pip install yt-dlp gallery-dl` in the venv. ffmpeg is found on PATH; the
  scripts' WinGet fallbacks are Windows-only and harmless.
- **Check the ffmpeg build** before trusting a recipe: `ffmpeg -hide_banner -filters | grep -E "subtitles|vmaf|drawtext"`
  and `ffmpeg -hide_banner -encoders | grep videotoolbox`. The friend's Homebrew ffmpeg 8 had no `drawtext` and no
  `soxr` (draw sheet labels with PIL; resample with `aresample=48000:filter_size=128:phase_shift=10:cutoff=0.97:linear_interp=1`).
  The newsdesk's subtitles need libass (`subtitles` filter) and the encoder bench needs libvmaf; if either is missing,
  install a fuller ffmpeg build (for example Homebrew's `ffmpeg-full` formula, untested here).
- **Encoders:** no NVENC on a Mac. Use `h264_videotoolbox` / `hevc_videotoolbox` or libx264, chosen by the VMAF bench
  (references/render-pipeline.md section 5). Untested.
- **GPU code:** replace CUDA with a device switch ("mps" if `torch.backends.mps.is_available()`, else "cpu"); autocast
  with float16 on MPS or none; expect slower runs.
- **OCR:** Windows OCR (`ocr.ps1`) becomes Apple Vision (the skill's `ocr.swift` built with `swiftc`, or the `ocrmac`
  package) or Tesseract, writing the same JSON.
- **Speech:** faster-whisper on CUDA becomes mlx-whisper (Apple Silicon) or faster-whisper on CPU (int8).
- **Fonts:** add `~/Library/Fonts`, `/Library/Fonts`, `/System/Library/Fonts/Supplemental` (the packaged builders
  already search them). Licensed fonts (Proxima Nova and others) need his own font files: Adobe Fonts activation gives
  no file path. macOS ships Helvetica as a `.ttc` that Chrome may not load through `@font-face` (install `.ttf` files or
  swap the tweet font); Impact ships with macOS; Bahnschrift is Windows-only (substitute a numbers face).
- **Drive for desktop:** `~/Library/CloudStorage/GoogleDrive-<account>/My Drive/...`.
- **Keep-awake:** `caffeinate -i <command>` instead of Windows' SetThreadExecutionState; always-on jobs via launchd
  (references/scheduling-and-unattended-runs.md section 7).
- **Process checks:** `ps -axo command`, `pgrep`, or psutil instead of PowerShell queries and `tasklist`;
  `os.kill(pid, 0)` is a valid "is it alive" test on a Mac (not on Windows).
- **Shell:** zsh has no `timeout` (use `gtimeout` or none) and does not word-split `$var` in for-loops: batch from
  Python instead. Save shipped scripts with LF line endings (CRLF breaks a `#!/usr/bin/env python3` line).
- **Multiprocessing:** macOS spawns pool workers, so every pool script needs `if __name__ == "__main__":`.
- **After Effects:** the skill's `ae_run.py` takes its Mac route by itself: scripts go in through AppleScript
  `DoScript` into a running AE (the user ticks the scripting preference; the runner refuses to replace a project the
  user has open and quits only an AE it launched), or saved projects render with `aerender`. The Windows command
  (`AfterFX.com -r`) does not apply. The pipelines' own .jsx builds have not been run through the Mac route yet.
- **Settings only the boss changes:** Adobe security preferences (the AE scripting preference; the optional Premiere
  bridge in premiere-ae-editing needs Adobe's PlayerDebugMode, which lets any unsigned panel load), macOS sleep and
  wake schedules, and whether Claude Code may "always allow" python and ffmpeg commands. Claude explains and asks; it
  never changes them.

## 3. Per pipeline
### `newsdesk/`
- Platform lines: Chrome path, font folders, the premiere-ae-editing scripts path, the Drive path, and the XML file URLs
  (the old `'file://localhost/' + path` doubled the slash on Mac paths; the packaged copy builds URLs for both). Test
  one `<id>.xml` and one `<id>_source.xml` import in Premiere first.
- Fonts: Coolvetica Hv Comp (free from Typodermic; check the licence for client work), Proxima Nova Extrabold,
  Semibold and Regular (licensed), Helvetica (see above), Impact, a numbers face.
- `scan.py` runs as is (standard library only). From a UK machine the geo-blocked sources work, so the workarounds for
  the editor's country fall away.
- Subtitles: the skill's `hear.py` runs on Apple Silicon on the CPU (slower) or through mlx-whisper.
- Do not copy the Chrome profile folder (`_chrome_profile/`): it holds a Cookies database.
### `outcome-studio/`
- `studio/render.py` and the fork's `vcn.py` find Mac Chrome and fonts; `start_archive.sh` runs the archive under
  `caffeinate -i` (leave the Terminal open; Ctrl+C stops it) or wrap it in a launchd agent.
- `goalcam.py`: the original called the Windows keep-awake function unguarded (around line 238); the kit copy wraps it
  in a try. Run it as `caffeinate -i python3 goalcam.py run <keys...>`. `archive.py` guards it too.
- Research tools: `ocr.ps1` is Windows OCR (use Apple Vision or Tesseract); `textmetrics.py` has a hard-coded root to
  change; `asr.py` uses CUDA (CPU faster-whisper or mlx-whisper); `mocks.py` uses a Windows emoji font.
- Check that the client's site and API load from the boss's location before relying on capture and filming (the
  client's terms block some countries; unverified).
- GSAP 3.12.5 (`assets/js/gsap.min.js`, GreenSock standard licence): re-download if it did not ship.
### `edits-kit/`
- CUDA in `roto.py`, `reframe.py`, `automatte.py`; NVENC in `roto.py` (no fallback): references/music-edit-builds.md
  section 11 has every change, the SAM 2 install order and the font list.
- Re-run the After Effects effects probe on his AE before the first build.
### Long cutdowns
- The Mac table in references/cutdown-batch-pipeline.md section 13 (OCR, WhisperX on CPU or MPS, `--skip-asr` for
  `prep.py`, process checks, the encoder fallback, `fcpxml.py` URLs).
- `ytdl.py` (premiere-ae-editing): its folders resolve on a Mac, but it starts its token server with Windows-only
  process flags: start the server by hand first, or apply the one-call port in MAC-TASKS step 16 (premiere-ae-editing
  `references/youtube-downloads.md`, "On a Mac"); otherwise use the plain yt-dlp route.

## 4. Accounts and keys (types only; he needs his own)
| Need | For | Notes |
|---|---|---|
| Adobe Premiere Pro and After Effects (Photoshop for cutouts) | every Premiere and AE step | his own licence and seat |
| Google Drive for desktop | newsdesk and studio delivery | signed in to the account that owns the posting folders |
| Logins to the pages themselves | posting (manual, in the app, with the client's sound) | his own; never typed by Claude |
| Throwaway X and Instagram monitoring logins | reading feeds and studying formats in the browser | never a page's or anyone's personal account; Claude never types passwords; check they are still logged in |
| Throwaway YouTube account cookies | only if YouTube blocks downloads | exported to the pipeline's `secrets/` file; never personal or the boss's own (accounts used by download tools can be flagged) |
| Music licence covering client work | any client post with library music | a Pro or Business type plan with channels safelisted before posting; the Creator type does not cover client work |
| Epidemic API key | the music connector, if used | the account holder creates it (valid 1 year); store it only as an environment variable; never print it |
| Pexels and Pixabay free API keys, a Freesound login | stock and CC0 sound steps | the sites block scripts without them |
| Meta Business Suite access | Facebook exports for cutdown analytics | the browser pane cannot read facebook.com |
| Hugging Face token | speaker labels (optional) | accept the model's terms; environment variable only |
| ElevenLabs key | narrator VO (on hold) | environment variable only |
| Optional paid readers | if the free X reader dies | a paid X data API, an Apify token or a Meta Graph token in a local `.env` |
| Font licences, model downloads | builders, mattes, tags | Proxima Nova and others; SAM 2.1 (898 MB), CLIP ViT-L-14 on first run |
| AI B-roll credits (optional) | generated clips | paid per use: ask first |
| Access to the shared Artifacts | review pages, dashboards, the edits bank page | private pages in Kanishk's account: he shares them |
- Never ship: browser profile folders (cookies), `secrets/` folders, download scripts with signed links, client
  revenue datasets.

## 5. Versions on record (the Windows build machine, 11 to 14 Oct 2026)
- ffmpeg 9.0.2 (winget Gyan.FFmpeg), Deno 2.9.7 (winget DenoLand.Deno), gallery-dl 1.32.15 and yt-dlp 2026.08.19 (pip;
  run as `python -m yt_dlp` because pip gave no exe), the bgutil PO-token provider 2.0.2, NVIDIA driver 617.42 (NVENC
  needed 610 or newer), WhisperX in its own venv (torch 2.8 with CUDA 12.8), Premiere and After Effects 26.5, Python
  3.13. Why: versions on record make breakages traceable.

## 6. Untested on the Mac (say so when using them)
VideoToolbox encodes and their VMAF values; parallel hardware encode throughput; SAM 2 and CLIP on MPS; WhisperX
alignment on CPU or MPS; Apple Vision OCR on the subtitle tools; the newsdesk XML imports in Premiere on a Mac; the
After Effects builders through DoScript or aerender; launchd agents for the archive; `pmset -g batt` as the power check;
whether the client's site loads from his location; a fuller ffmpeg build for libass and libvmaf.
