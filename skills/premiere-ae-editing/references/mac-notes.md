# macOS notes: what was verified on a Mac

Facts from the Mac port of this skill (Apple Silicon, M3 Max), verified between late September and 14 Oct 2026; dates
say when. Check versions on a new machine with `scripts/env_check.py`; most of this carries over to any Apple Silicon
Mac with the same app versions. Facts that hold on both machines live in the main references; Windows-only facts are in
after-effects.md section 11, timing.md and youtube-downloads.md.

## Machine and apps
- Verified versions: Premiere Pro 2025 (25.6.6) and 2026 (26.5.1), After Effects 2026 (26.2.1), Media Encoder 2025 and
  2026, Photoshop 2026, ffmpeg 8 from Homebrew (built without drawtext and without soxr), swiftc (Xcode Command Line
  Tools), Google Chrome, yt-dlp.
- The user may have BOTH Premiere versions open with their own projects. Look first (`pp.py --v 2026 --status` and
  `--v 2025 --status`), ask before any restart, never save over or close their projects.
- A project saved by Premiere 2026 cannot be opened by Premiere 2025: keep a 2025 job in 2025.
- Homebrew's Python is "externally managed" (PEP 668): the tools run from venvs (`~/.venvs/premiere-ae` for the tools,
  `~/.venvs/mlx-whisper` for transcription). Setup steps: SKILL.md "First time on a Mac"; the boss's first-run test
  list: `~/VisionKit/kit/MAC-TASKS.md`.

## Projects and XML that travel between the Windows PC and the Mac (14 Oct 2026)
- prproj_lib follows the PROJECT, not the machine: `path_style(doc)` reads the project's own media paths, so a
  Windows-saved project edited on the Mac keeps `.\file` RelativePaths and a Mac-saved one edited on Windows keeps
  `./sub/file` (prproj-format.md section 5). FilePath is always the real path on the machine doing the edit.
- The order of a track's `<ID>` and `<Index>` is NOT a Mac difference: most Windows projects put `<ID>` first too, and
  `add_video_track` / `add_audio_track` handle both orders on both machines (prproj-format.md section 12). The old
  advice "edit a project on the kind of machine that saved it" no longer applies. Opening a track-edited copy in
  Premiere on the Mac is still a first-run test (MAC-TASKS step 12).
- fcpxml.py writes each `<pathurl>` in its own path's form: `/Users/x/a b.mov` becomes
  `file://localhost/Users/x/a%20b.mov` (one slash after localhost; an older copy doubled it), and `--check` reads Mac
  and Windows URLs back on either machine. Built and checked by script only: importing such an XML in Premiere on a
  Mac is the remaining test (MAC-TASKS step 13).

## Premiere through the CEP bridge (scripts/premiere/pp.py)
- What it is: a hidden panel (CEP extension `com.local.editbridge`) installed from `bridge/` with
  `zsh bridge/install_bridge.sh`. The USER runs the installer after reading it, because it changes a security setting:
  it copies the panel into `~/Library/Application Support/Adobe/CEP/extensions/`, writes a random private token to
  `~/.editbridge_token` (chmod 600) and sets Adobe's PlayerDebugMode = 1 for CSXS 10, 11 and 12, the preference that
  lets unsigned panels load (ANY unsigned panel in that folder, not only this one). Never run it yourself or with
  `--yes`. The installer's header lists how to undo each step.
- Host range PPRO [25.0, 26.99]. The panel runs a Node HTTP server on 127.0.0.1 only: port 47915 in Premiere 2026,
  47916 in Premiere 2025, so both can run at once. Every request carries the token in the header `x-bridge-token`
  (never print it); requests with an Origin header (browsers) are refused, so only local tools can call it. Anything
  that gets in can run any ExtendScript inside Premiere as the user, so the token file stays private.
- Two bridges on the same ports cannot run at once: the installer warns when another panel uses them; the user removes
  one.
- Windows: the same panel should load from `%APPDATA%\Adobe\CEP\extensions` with PlayerDebugMode in the registry
  (HKEY_CURRENT_USER\Software\Adobe\CSXS.<n>), but there is no Windows installer and it has not been tried there; the
  Windows route stays the window (premiere-ui.md).
- CEP finds panels only at launch: after installing or changing the manifest, Premiere needs one restart (ask; the user
  saves first). "Heartbeat call failed" in the CEP log: one restart fixes it (ask).
- CEP has an end date (research, Oct 2026, re-check): Adobe plans CEP off by default from Dec 2028 and removed in Dec
  2029; ExtendScript itself is unaffected. The bridge is a CEP panel, so it needs a UXP route before then.
- AppleScript `quit` / `activate` on Premiere time out (-1712). `open -a "Adobe Premiere Pro 2026" file.xml` imports
  nothing. System Events cannot see Premiere's windows; a Swift CGWindowList script can (`screencapture -l <id>`).
- Proven calls: `app.openDocument(path, true, true, true, true)` (opens a SECOND project, so build in a copy while
  theirs stays open), `app.project.closeDocument(0, 0)`, `app.newProject`, `seq.clone()` + `seq.name = ...`,
  `proj.deleteSequence`, `projectItem.setInPoint/OutPoint(ticks, 4)` + `track.overwriteClip(item, ticks)` (frame exact,
  but it silently fails now and then: check the clip landed and retry), QE
  `addVideoEffect(qe.project.getVideoEffectByName("Lumetri Color"))`, `getParamForDisplayName("Level"/"Scale"/"Position")`,
  `exportFramePNG`, `seq.exportAsMediaDirect(out, preset.epr, 0)`,
  `seq.createCaptionTrack(srtItem, 0, Sequence.CAPTION_FORMAT_SUBTITLE)`, `proj.importAEComps(aep, [names], bin)`.
- Imports: one `importFiles` call with about 20 paths per bridge call, save, next call (150 in one call stalled
  Premiere 2025 with stacked progress windows and never returned).
- Stills snap to a 29.97 grid when their out point is set, which leaves 1-frame holes: force `trackItem.end` to the
  planned frame and audit for "Empty" QE items on every used track. Audio in/out points are floored to whole video
  frames: pad short SFX with silence to whole frames + 2 ms (ffmpeg `apad=whole_len`) before importing.
- VP9 video inside an MP4 never lands in Premiere 2025: convert to H.264 first (check `ffprobe` codec_name).
- QE `addVideoEffect` inserts each new effect ABOVE the previous ones (right under Motion): add them in reverse order.
- QE `setSpeed(x, "", false, false, false)` takes a MULTIPLIER (0.26 = 26%). Reliable alternative: patch the saved
  project's `<PlaybackSpeed>` = media ticks / slot ticks; effect keyframes on speed-changed clips are in media time.
- Clip Volume Level internal value = 10^((dB-15)/20) (0 dB = 0.17782794, +15 dB max), as in the saved file. In JSX
  `if (c.auto)` is true for an empty array: guard with `.length`.
- Loudness-normalised export by script: `assets/presets/H264 match source, -14 LUFS.epr` (a copy of the Frame.io
  "h.264 Match Source" preset with loudness normalisation on at -14 LUFS / -1 dBTP; a test export measured -14.2 LUFS and
  -1.0 dBTP). Captions in exports: ExporterParam `ADBECaptionExportOption` 0 none, 1 sidecar, 2 burn in (copy the .epr
  and change it).
- Caption styling has no API: patch the saved project (`captions-style-patch.md`). One wrong field type crashed Premiere
  on open, taking every open project down: only write fields seen in real blobs.
- Masks have no API either: clone an existing mask into the saved project (`scripts/prproj/prproj_masks.py` for
  Premiere 2025, prproj_lib for 2026, prproj-format.md section 8). `StartKeyframeValue` needs a BinaryHash attribute or
  Premiere silently drops the path.
- A Windows editor's project (media at E:\...) opens on the Mac with every clip offline. In a copy, rewrite
  ActualMediaFilePath, FilePath, ConformedAudioPath and PeakFilePath to the Mac folder (those projects had no
  RelativePath). Right after `openDocument`, `isOffline()` reads true for most items until Premiere has checked the
  files: check again a moment later before relinking.
- `.rar` (RAR5) archives open with the built-in `bsdtar -xf`.

## After Effects (the Mac route of ae_run.py)
- Scripts go in with osascript `tell application "Adobe After Effects 2026" to DoScript "..."`. DoScript always returns
  0, and a modal dialog makes it return without running anything: the script's own log + DONE flag are the only truth.
- DoScript goes into the AE that is ALREADY open. Every script generated on a Mac checks `app.project.file` / `dirty` /
  `numItems` and refuses to replace a project it did not create (a user once had an unsaved project with Dynamic Link
  comps open; a test once added a comp to a real project). The runner probes first and quits only an AE it launched
  itself; those scripts never call `app.quit()`, so a .jsx run by hand never closes the user's AE.
- Launch hidden with `open -g "/Applications/Adobe After Effects 2026/Adobe After Effects 2026.app"` (`open -a` did not
  start it), then ping it with a tiny probe script until it answers (5-6 s). Foreground `sleep` may be blocked in the
  agent harness: wait with a polling loop.
- An uncaught error in a DoScript job opens a modal alert in AE and the AppleEvent times out: probes wrap everything in
  try/catch and log to a file. `app.purge(PurgeTarget.ALL_CACHES)` from a script can leave such a dialog open. After a
  force-quit, AE 2026 opens with "Crash Repair Options" (Continue is the default) and the runner's probe shows
  "Scripting Plugin is not installed". Recovery when AE will not quit: only after confirming no user project is open,
  terminate it and relaunch with `open -g`.
- New projects default to working space Rec.709 Gamma 2.4, which shifts sRGB PNG colours (#1A6317 became #266B23): set
  "sRGB IEC61966-2.1" after `app.newProject()` (ae_build.py does on a Mac). `workingSpace = "None"` pops a blocking
  "Profile None is missing" dialog but gives exact colours through Dynamic Link: set it once by hand, then save-as that
  project for later versions.
- ExtendScript `File` writes `\r` line endings on macOS unless `f.lineFeed = "Unix"`.
- aerender: absolute `-output` path only (a relative one silently writes nowhere); one aerender at a time (a second one
  killed the first); long renders can die near the end and leave an unreadable MOV, so render in `-s/-e` frame ranges
  and join with ffmpeg concat. With the AE GUI open, aerender can render from cached footage after plate files changed:
  reload footage and purge first, then check one pixel of the render against the plate.
- Output templates (26.2 prefs): "High Quality" (ProRes 422, includes comp audio as PCM), "High Quality with Alpha"
  (ProRes 4444 + alpha), "Lossless" (QuickTime Animation, huge), "H.264 - Match Render Settings - 5/15/40 Mbps".
- Dynamic Link comps: footage layers carry audio into Premiere (`audioEnabled = false`); fixes must edit comps in place
  (rebuilding with new comps orphans the links). Premiere 26.5 colour-manages DL comps; set a Rec. 709 override per item
  (premiere-ui.md, after-effects.md section 14).
- Fonts copied into ~/Library/Fonts show up in a running AE after about 10 s; Premiere only sees fonts installed before
  it launched.
- 11 Oct 2026: right after ae_dump opened and closed a COPY of a project that an open Premiere linked by Dynamic Link, an
  AE instance with an empty project appeared (launched by launchd, not by the runner). Cause not confirmed. If it happens
  again, mention it; do not quit an AE you did not launch.

## Media tools on the Mac
- Transcription: mlx-whisper large-v3-turbo in `~/.venvs/mlx-whisper` (Apple Silicon only); the Mac `hear.py` runs in
  that venv (timing.md, media-toolkit.md section 5).
- OCR: Apple Vision through Swift (`scripts/media/ocr`, built with `swiftc -O scripts/media/ocr.swift -o
  scripts/media/ocr`); same JSON as the Windows `ocr.ps1`, so `ocrfind.py` works unchanged (timing.md).
- Fonts: `scripts/media/fontcheck [--text "<string>"] Name ...` says whether a PostScript name is installed and which
  glyphs are missing. Core Text and Adobe names can differ for variable fonts (Premiere needs `LoraItalic-Italic`, Core
  Text calls it `Lora-Italic`). Adobe Fonts files are hidden in CoreSync: mock type in headless Chrome with Google Fonts.
- This ffmpeg has no drawtext (draw contact-sheet labels with PIL) and no soxr (resample with
  `aresample=48000:filter_size=128:phase_shift=10:cutoff=0.97:linear_interp=1`).
- Python multiprocessing spawns workers on macOS: every Pool script needs `if __name__ == "__main__":`.
- zsh has no `timeout` (use `gtimeout` or none) and does not word-split `$var` in for-loops: batch from Python instead.
- Previewing a local HTML page in a browser pane: serve its folder with `python3 -m http.server <port> --bind 127.0.0.1`
  on a free port (check with `lsof -iTCP:<port>`), add a charset meta, stop the server afterwards.
- Headless Chrome lives at `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"` (stills-and-sources.md).
- Free disk space: `df -h /` before big pulls (one contact-sheet loop once filled 48 GB of scratch space).
- Long unattended jobs: run them under `caffeinate -i` so the Mac does not idle-sleep (no setting changes).

## Porting a Windows-built tool to the Mac
Most job tools were written on the Windows PC. These are the lines that break, and what replaces them (each untested
on the boss's Mac until run once; the kit's first-run task list tracks the shipped ones, ytdl.py among them):

| Windows piece | Mac replacement |
|---|---|
| Windows OCR (`ocr.ps1` through PowerShell) | `scripts/media/ocr` (Apple Vision, the same JSON) |
| CUDA (WhisperX, faster-whisper on the GPU, SAM 2) | mlx-whisper for speech; MPS or CPU for torch tools (media-toolkit.md section 12); expect several times slower than a 12 GB RTX laptop |
| NVENC | `h264_videotoolbox` or libx264, chosen by a VMAF test (media-toolkit.md section 10) |
| PowerShell process queries, ctypes PID checks, Win32 battery and sleep calls | `ps -axo command` or psutil, `os.kill(pid, 0)`, `pmset -g batt`, `caffeinate -i` |
| `%USERPROFILE%`, `%TEMP%`, `C:/Windows/Fonts/arialbd.ttf` | `~`, `tempfile`, `/System/Library/Fonts/Supplemental/Arial Bold.ttf` (font folders: `/Library/Fonts`, `~/Library/Fonts`, `/System/Library/Fonts`) |
| Chrome under `C:\Program Files\...` | `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome` |
| WinGet fallbacks for ffmpeg and Deno | Homebrew (`brew install ffmpeg deno`); `shutil.which` finds them |
| `'file:///' + path`, `'file://localhost/' + path` | a URL helper (both double the slash on `/Users/...`; FCP7 XML wants `file://localhost/Users/...`) |
| `.bat` launchers | a zsh script or launchd, under `caffeinate -i` |
| `subprocess.Popen(..., creationflags=DETACHED_PROCESS ...)` (a helper that must outlive the script) | `start_new_session=True` off Windows (`ytdl.py`'s token server still needs this one-call port: youtube-downloads.md "On a Mac") |

- `scripts/media/fsheet.py` still loads a Windows font path for its labels, so on a Mac the labels come out in PIL's tiny
  default font.
