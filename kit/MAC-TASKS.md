# Mac first run: premiere-ae-editing (instructions for Claude on the boss's Mac)

## In short
- **Who and what:** you are Claude Code on the boss's Mac (Premiere Pro and After Effects 2025 or 2026, most likely
  Apple Silicon). This is a one-time test of every tool in the premiere-ae-editing skill on this Mac. The scripts were
  built and tested on Kanishk's Windows PC; the Mac branches came from a Mac editor's port and have never run in this
  merged form on a Mac.
- **Your job:** get every tool working, or log exactly why it does not, and hand Kanishk a precise fix list. Nothing
  here is urgent: when in doubt, stop and ask the boss.
- **Where things are after the install:** the skill in `~/.claude/skills/premiere-ae-editing/` (scripts in
  `scripts/`), the kit in `~/VisionKit/kit/` (this file, the client files, the code library in `library/`), the boss's
  own layer in `~/VisionKit/mine/` (your test files, fixes and results go there, nowhere else).
- **What needs the boss:** a yes for every install, one at a time; the security switches, which he flips himself (After
  Effects scripting access, macOS Automation prompts, the optional Premiere bridge); a short clip, a short voice-over
  and a project he lets you copy; two imports in Premiere that he does by hand.
- **Time:** most of it is waiting for installs, the model download, one transcription and two tiny renders. Steps can
  be split over several sessions: the log says where you stopped.
- **The library pipelines are separate:** this list tests the skill's tools. Before the first run of any pipeline in
  `~/VisionKit/kit/library/pipelines/` (newsdesk, outcome-studio, edits-kit and the rest), follow the
  library README's "Start here" and its "Paths to set" table (some code still points at Kanishk's PC), set the
  variables from that pipeline's `.env.example`, and log the result in `~/VisionKit/mine/mac-test-results.md`.

| Step | What it tests | Needs from the boss |
|---|---|---|
| 0 | what is installed (read only) | nothing |
| 1-5 | Homebrew, ffmpeg, the tools venv, yt-dlp (only if he wants YouTube downloads), Xcode Command Line Tools | a yes per install |
| 6 | the Swift OCR and font helpers (built from source, nothing installed) | step 5 done |
| 7-8 | env_check; a compile and `--help` sweep of every script | nothing |
| 9, 9b | frames, loudness, beats; the VideoToolbox and x264 encoders | a 10-60 s clip |
| 10-11 | transcription (mlx-whisper) and the voice-over cut rules | a yes (1.6 GB model), a 20-60 s voice-over |
| 12 | editing a COPY of a project (path style, new tracks); he opens the result in Premiere | a project he names |
| 13, 13b | an FCP7 XML with Mac paths that he imports; a news-post XML (optional) | his File > Import |
| 14 | the After Effects runner on a tiny comp (and the effects library, optional) | his OK to launch AE; his scripting switch |
| 15 | Mac OCR (Apple Vision) | step 6 done |
| 16 | YouTube downloads with a one-line port (only if he said yes in step 4) | a yes per install |
| 17 | the remaining scripts (captions, LUT, Photoshop cutout) | his OK to launch Photoshop |
| 18 | the optional Premiere bridge | his decision; he runs the installer himself |
| 19 | the report | |

## Rules (they apply to every step)
1. **Ask before installing anything:** Homebrew, brew packages, Python packages, venvs, models, Xcode tools, fonts,
   Deno, a git clone.
   - Say what it is, why the kit needs it, roughly how big, and where it comes from. Wait for a clear yes.
   - One yes covers that one install, not the next.
2. **Never change a macOS or Adobe security setting yourself.** Explain what the setting does and why the kit needs it,
   then let him switch it himself:
   - Adobe's PlayerDebugMode (step 18: he runs the bridge installer himself, which sets it)
   - After Effects "Allow Scripts to Write Files and Access Network" (step 14)
   - System Settings > Privacy & Security (Automation, Accessibility, Full Disk Access), and Gatekeeper; the macOS
     prompts that ask whether Terminal or Claude may control After Effects or Photoshop are his clicks
   - Never type his password or any secret; installers that ask for a password, he runs himself in Terminal.
3. **Never edit kit files** (the kit's skill folders such as `~/.claude/skills/premiere-ae-editing/` and
   `~/.claude/skills/motion-design/`, and `~/VisionKit/kit/`). If a script needs a fix:
   - Copy it to `~/VisionKit/mine/fixes/<same relative path>` and fix and test the copy.
   - Write it up in `~/VisionKit/mine/feedback-for-kanishk.md`: file, the exact error, your change as a diff, how you
     tested it. Kanishk then fixes it upstream.
   - Exception: building the two Swift helpers next to their sources (step 6). That only creates new files the kit
     never ships, and kit updates leave them alone.
4. **In `~/VisionKit/mine/` create only your own files:** `mac-tests/`, `fixes/`, `mac-test-results.md`,
   `feedback-for-kanishk.md`. Never change or delete the boss's own files there.
5. **Log every step in `~/VisionKit/mine/mac-test-results.md`** (format below), including skips and failures.
   - Never write secrets into it: the bridge token, keys, or the PO tokens the YouTube token server writes to its own
     log.
6. **Work on copies only.**
   - Projects, media and AE projects are copied into `~/VisionKit/mine/mac-tests/` first.
   - Never save over, close or quit anything the boss has open.
   - Ask before launching or quitting Premiere, After Effects or Photoshop.
7. **One heavy job at a time** (render, transcription, download). Check free disk space before big ones.
8. **If a step fails twice the same way,** log it, skip it, and carry on. List it in the final report.
9. **Talk to the boss in plain English:** short, no jargon dumps.

Log format for `mac-test-results.md` (one block per step):
```
## 2026-MM-DD  step 9: frames and loudness
- command: <what you ran>
- result: PASS | FAIL | SKIPPED (why)
- output: <the one or two lines that prove it>
- next: <what you did about it>
```

**Shell variables do not survive between your Bash calls,** so start every command with this line:
```
SK=~/.claude/skills/premiere-ae-editing; M=~/VisionKit/mine; T=$M/mac-tests; PY=~/.venvs/premiere-ae/bin/python; MW=~/.venvs/mlx-whisper/bin/python; export PYTHONPYCACHEPREFIX=$T/pycache
```
`PYTHONPYCACHEPREFIX` keeps Python's bytecode out of the kit folders. zsh has no `timeout` command: use the scripts'
own `--timeout`, or Python. The small test scripts in steps 12 to 14 are shown as quoted heredocs (`<<'EOF'`); if your
shell tool changes backslashes in them (a trap the skill lists), write the same text with your file-writing tool
instead and grep that it landed.

## Step 0: look first (read only, no asking needed)
```
mkdir -p "$T"/{ae,renders,prproj,xml,audio,frames,ocr,help,yt} "$M/fixes"
sw_vers; uname -m; df -h ~ | tail -1
ls /Applications | grep -i adobe
for t in python3 brew ffmpeg ffprobe swiftc yt-dlp deno git; do printf '%-8s ' $t; command -v $t || echo missing; done
python3 --version; xcode-select -p
ls "$SK/scripts"
```
- **Success:**
  - You know the chip (`arm64` = Apple Silicon, `x86_64` = Intel), the macOS version, the free space, and the Adobe
    apps and versions.
  - You know which tools are missing.
  - Start `mac-test-results.md` with a header holding these facts.
- **If `$SK/scripts` is missing:** the kit is not installed. Use the kit-updater skill first
  (`python3 ~/VisionKit/kit/tools/kit_install.py status`).

## Step 1: Homebrew (ask)
- **Only if `brew` is missing.** The official installer at brew.sh asks for his Mac password, so he runs the
  one-line command from brew.sh in Terminal himself.
- **Success:** `brew --version` prints a version.
- **If it fails:** log the last lines of his Terminal output. Without Homebrew, steps 2 and 16 and the brew
  fallbacks in step 3 cannot run. Step 5 comes from Apple and still works.

## Step 2: ffmpeg and ffprobe (ask)
```
brew install ffmpeg
ffmpeg -version | head -1; ffprobe -version | head -1
```
- **Why:** `atools.py` extracts audio with ffmpeg on the Mac; mlx-whisper decodes with it; loudness cross-checks use
  its `ebur128` filter.
- **Success:** both print a version.
- **Note:** Homebrew's build may lack drawtext and soxr; the kit does not need them.
- **If brew fails:** log the error and try once more after `brew update` (ask: it updates Homebrew itself).

## Step 3: the tools venv (ask)
```
python3 -m venv ~/.venvs/premiere-ae
~/.venvs/premiere-ae/bin/pip install -U pip
~/.venvs/premiere-ae/bin/pip install av numpy pillow esprima
$PY -c "import av, numpy, PIL, esprima; print('av', av.__version__, 'numpy', numpy.__version__, 'PIL', PIL.__version__)"
```
- **Why a venv:** Homebrew's Python is "externally managed" and refuses plain pip installs.
- **What uses it:** PyAV reads video and audio for most tools; esprima checks ExtendScript.
- **Success:** the versions print. PyAV 19 was the tested version; a newer one should work.
- **If `python3` is missing:** ask to `brew install python`. If PyAV fails to install, log the error, then ask about
  `brew install pkg-config` and retry once.
- **Optional (ask):** `~/.venvs/premiere-ae/bin/pip install faster-whisper`.
  - Needed only on an Intel Mac, or for name-heavy audio, where its hotwords beat mlx-whisper's prompt.
  - Its model (about 1.6 GB) downloads on first use.

## Step 4: yt-dlp (ask; only if the boss wants YouTube downloads at all)
- **First tell him:** downloading from YouTube with these tools works around YouTube's bot check. It may break
  YouTube's Terms of Service, even for a client's own uploads. It is only for footage he has the rights to use, and
  the client's original files are better quality. It is his decision.
- **If he says no:** log "SKIPPED by choice" here and in step 16.
- **If yes:**
  ```
  ~/.venvs/premiere-ae/bin/pip install -U "yt-dlp[default]"
  $PY -m yt_dlp --version
  ```
  - **Success:** a version prints. No download in this step.

## Step 5: Xcode Command Line Tools (ask)
```
xcode-select --install
xcode-select -p; swiftc --version
```
- **How:** the first command opens an Apple dialog; he clicks Install. It is a large Apple download.
- **Why:** `swiftc` builds the Mac OCR and font checker (step 6).
- **Success:** a path and a Swift version print.
- **If it fails:** log the dialog's message. Skip steps 6 and 15, and list them.

## Step 6: build the Swift helpers (no install; they go next to their sources, see rule 3)
```
swiftc -O "$SK/scripts/media/ocr.swift" -o "$SK/scripts/media/ocr"
swiftc -O "$SK/scripts/media/fontcheck.swift" -o "$SK/scripts/media/fontcheck"
"$SK/scripts/media/fontcheck" ArialMT ProximaNova-Semibold ProximaNova-Regular Montserrat-Black ArialUnicodeMS DMSerifDisplay-Italic JetBrainsMono-Regular Inter-SemiBold SFProDisplay-Bold Didot-Bold
```
- **Success:** two binaries exist, and fontcheck prints one line per font name.
  - A line where "resolves to" names a different font means that font is NOT installed.
  - `env_check.py` looks for the binaries at exactly these paths.
- **Fonts the AE libraries use:**
  - Proxima Nova and Montserrat: Adobe Fonts, which he activates in his Adobe account.
  - DM Serif Display, JetBrains Mono, Inter: free; ask before installing, then copy into `~/Library/Fonts`.
  - SF Pro and Didot: come with macOS. Apple's SF Pro licence is aimed at Apple UI work, so ask before using it in
    client renders.
  - A running AE sees a new font after about 10 s; Premiere sees it only after a restart.
- **If swiftc errors:** log the first error line. Usual cause: Command Line Tools missing or half installed
  (step 5). Do not edit the .swift files; a needed change goes to rule 3.

## Step 7: env_check (read only)
```
$PY "$SK/scripts/env_check.py"
```
- **Success, line by line:**
  - Adobe apps with versions.
  - "running now" lists what is open (leave it alone).
  - CEP bridge: token MISSING and ports closed is expected until step 18.
  - Python modules av, numpy, PIL, esprima ok; faster_whisper is optional.
  - mlx-whisper venv: MISSING until step 10.
  - ffmpeg, ffprobe and swiftc found. yt-dlp reads "missing" unless a copy is on PATH: the venv copy from step 4 is
    not on PATH, so check it with `$PY -m yt_dlp --version` instead.
  - ocr and fontcheck "built".
  - Free disk and the font list.
- **If something is MISSING:** go back to the step that installs it, and ask first.

## Step 8: syntax and command-line sweep (no Adobe app)
```
for f in $(find "$SK/scripts" -name '*.py'); do $PY -m py_compile "$f" || echo "COMPILE FAIL $f"; done
$PY "$SK/scripts/ae/check_jsx.py" "$SK"/scripts/ae/*.jsx "$SK/scripts/stills/ps_cutout.jsx"
cd "$T/help" && for f in $(find "$SK/scripts" -name '*.py'); do echo "== $f"; PYTHONDONTWRITEBYTECODE=1 $PY "$f" --help 2>&1 | tail -2; done; ls -A "$T/help"
```
- **Success:**
  - No "COMPILE FAIL" line.
  - check_jsx prints "ok" for all 5 .jsx files.
  - Every script prints its usage, an argparse help, nothing (library files), or a short error before doing any
    work: a missing file named `--help`, or (hear.py under this venv) the missing optional faster-whisper module.
    `env_check.py` prints its normal report.
  - `ls -A` shows `$T/help` still empty.
  - No app launches and no server starts. `ytdl.py --help` only prints its note and usage.
- **If a script does anything else** (writes a file, launches something, hangs): stop the sweep, log it, put it in
  the feedback file.
- **Never run `bridge/install_bridge.sh` in this step.**

## Step 9: frames and loudness
- **Input:** ask the boss for a short clip with sound (10 to 60 s) you may copy. Use its real frame rate (from
  `frames.py info`) wherever an fps is asked later.
```
cp "<the clip he names>" "$T/frames/clip.mp4"
$PY "$SK/scripts/media/frames.py" info "$T/frames/clip.mp4"
$PY "$SK/scripts/media/frames.py" grab "$T/frames/clip.mp4" 1.0 "$T/frames/clip_1s.png"
$PY "$SK/scripts/media/frames.py" sheet "$T/frames/sheet.png" "$T/frames/clip.mp4" "a@0.5" "b@1.5" "c@2.5"
$PY "$SK/scripts/media/atools.py" "$T/frames/clip.mp4"
ffmpeg -hide_banner -nostats -i "$T/frames/clip.mp4" -af ebur128=peak=true -f null - 2>&1 | tail -12
$PY -c "import sys; sys.path.insert(0, '$SK/scripts/media'); from atools import extract_wav; print(extract_wav('$T/frames/clip.mp4', '$T/audio/clip.wav', 0, 5))"
$PY "$SK/scripts/media/beats.py" "$T/audio/clip.wav" "$T/audio/beats.json" 30
$PY "$SK/scripts/media/fsheet.py" "$T/frames/clip.mp4" "$T/frames/fs" 0 59
```
- **Success:**
  - `info` prints codec, size, fps, frames, duration and audio.
  - Read the PNGs: the right picture, and readable labels on the sheet (Mac fonts are used).
  - atools' integrated LUFS is within 0.1 LU of ffmpeg's "I:", and its true peak within about 0.3 dB.
  - `extract_wav` writes a 5 s WAV (the Mac branch, through ffmpeg).
  - beats.py writes JSON; fsheet.py writes sheets.
- **Known:** fsheet labels are tiny on a Mac (a hard-coded Windows font). Log it, no fix needed now.
- **If PyAV cannot open the clip:** try another file and log the codec. If the LUFS figures disagree by more than
  0.5 LU, log both numbers.

## Step 9b: encoders, VideoToolbox and x264 (no install)
```
ffmpeg -hide_banner -encoders | grep -E "h264_videotoolbox|libx264"; ffmpeg -hide_banner -filters | grep -E "libvmaf|subtitles"
time ffmpeg -hide_banner -loglevel error -f lavfi -i testsrc2=size=1920x1080:rate=30 -f lavfi -i sine=frequency=440:sample_rate=48000 -t 5 -c:v h264_videotoolbox -b:v 12M -c:a aac -shortest "$T/frames/vt_test.mp4"
time ffmpeg -hide_banner -loglevel error -f lavfi -i testsrc2=size=1920x1080:rate=30 -f lavfi -i sine=frequency=440:sample_rate=48000 -t 5 -c:v libx264 -crf 16 -preset fast -c:a aac -shortest "$T/frames/x264_test.mp4"
$PY "$SK/scripts/media/frames.py" info "$T/frames/vt_test.mp4" "$T/frames/x264_test.mp4"
```
- **Why:** the Windows renders use NVIDIA's NVENC; on a Mac the hardware encoder is h264_videotoolbox, with
  libx264 as the safe fallback.
- **Success:** both encoders are listed; both files are 1920x1080, 30 fps, 5 s, with audio. Log both encode times.
- **Also log whether `libvmaf` and `subtitles` are present:** a VMAF encoder test needs libvmaf, the caption builders
  need subtitles.

## Step 10: transcription with mlx-whisper (ask: venv plus a model download of about 1.6 GB)
- **Apple Silicon only.** On Intel use the faster-whisper option from step 3.
- **Input:** ask the boss for a short raw voice-over (20 to 60 s) you may copy.
```
python3 -m venv ~/.venvs/mlx-whisper && ~/.venvs/mlx-whisper/bin/pip install mlx-whisper
cp "<the voice file he names>" "$T/audio/voice.wav"
$MW "$SK/scripts/media/hear.py" "$T/audio/voice.wav" "$T/audio/voice_words.json"
```
- **Success:**
  - It prints `done: N segments, M words, ... s audio in ... s`, and the JSON has `words` with `s`, `e`, `w`, `p`.
  - Read the first lines of the transcript to him and check names by ear. mlx-whisper has no hotwords: a vocab file
    only primes the first 30 s window, and once it invented names in the opening seconds.
- **If it fails:**
  - "ffmpeg not found": step 2.
  - A Hugging Face download error: log it, and do not look for workarounds.
  - Python crash: log the last 5 lines.

## Step 11: speech cuts, the new voice-over rules (no install)
```
$PY "$SK/scripts/media/speech_cuts.py" "$T/audio/voice.wav" "$T/audio/voice_words.json" --phrases --json "$T/audio/phrases.json"; echo "exit $?"
$PY "$SK/scripts/media/speech_cuts.py" "$T/audio/voice.wav" --scan "$T/audio/phrases.json"; echo "exit $?"
$PY "$SK/scripts/media/speech_cuts.py" "$T/audio/voice.wav" "$T/audio/voice_words.json" --phrases --wav-dir "$T/audio/pieces"
```
- **Then:** run the `for f in ...` loop it prints, with `$MW` in place of `python`, and run the third command again.
- **Success:**
  - The header reads `levels: floor ... | absolute: edge -70 dB, loud -55 dB`.
  - The first two print "edge scan: clean" with exit 0.
  - The last run says "restart checks: ... from their own transcripts".
  - Ask the boss to listen to two or three in/out points (QuickTime or Premiere).
- **If a WARNING says the room floor is above -65 dB:** the recording is not clean voice-over. Run the same
  commands with `--rel` and log both results.
- **If the edge scan finds problems on the tool's own in/out:** log the lines. That is a real finding for Kanishk.

## Step 12: Premiere project tools on a COPY (Premiere stays closed for now)
- **Input:** ask the boss which project you may copy, one he is not working in right now.
```
cp "<the project he names>.prproj" "$T/prproj/copy.prproj"
$PY "$SK/scripts/prproj/prproj_lib.py" "$T/prproj/copy.prproj" | head -30
$PY "$SK/scripts/prproj/prproj_dump.py" "$T/prproj/copy.prproj" > "$T/prproj/dump.txt"; head -40 "$T/prproj/dump.txt"
$PY "$SK/scripts/prproj/prtranscript.py" "$T/prproj/copy.prproj"
cat > "$T/prproj/edit_test.py" <<'EOF'
import sys, os, re, collections
sys.path.insert(0, os.path.expanduser('~/.claude/skills/premiere-ae-editing/scripts/prproj'))
from prproj_lib import *
src = sys.argv[1]; out = src.replace('.prproj', ' v2.prproj')
doc = Doc.open(src)
print('path style:', path_style(doc))
name, seq = next((n, u) for n, u in sequences(doc) if tracks(doc, u, 'video') and tracks(doc, u, 'audio'))
before = (len(tracks(doc, seq, 'video')), len(tracks(doc, seq, 'audio')))
add_video_track(doc, seq); add_audio_track(doc, seq)
after = (len(tracks(doc, seq, 'video')), len(tracks(doc, seq, 'audio')))
print('sequence %r: tracks V%d A%d -> V%d A%d' % ((name,) + before + after))
for kind in ('video', 'audio'):
    ids = [re.search(r'<ID>(\d+)</ID>', re.search(r'<Track Version="\d+">.*?</Track>', doc.raw(t, uid=True), re.S).group(0)).group(1)
           for t in tracks(doc, seq, kind)]
    print(kind, 'track IDs', ids, 'duplicates:', [i for i, n in collections.Counter(ids).items() if n > 1])
doc.save(out); print('saved', out)
EOF
$PY "$T/prproj/edit_test.py" "$T/prproj/copy.prproj"
$PY "$SK/scripts/prproj/validate_struct.py" "$T/prproj/copy.prproj" "$T/prproj/copy v2.prproj"
$PY "$SK/scripts/prproj/prproj_dump.py" "$T/prproj/copy v2.prproj" > "$T/prproj/dump_v2.txt"; diff "$T/prproj/dump.txt" "$T/prproj/dump_v2.txt" | head -20
```
- **Success:**
  - path style is `mac` for a project saved on his Mac (`win` for one made on Kanishk's PC).
  - Tracks go up by one video and one audio, and each kind lists no duplicate track IDs.
  - validate_struct prints `duplicate ids: []`, `unresolved refs new: []`, `blob hashes used before their data: 0`,
    new orphans equal to the source's.
  - The dump diff shows only the new empty tracks.
  - On the Mac each sequence header in the dump shows the sequence's own name, plus `[bin item "..."]` when the bin
    name differs.
- **Then (ask):** the boss opens `copy v2.prproj` in Premiere as its own project, never over his work. It should
  open with no repair prompt and show the two new empty tracks; he closes it without saving.
- **If an edit raises** ("track template not understood", an assert): log the full message and the project's
  Premiere version. This is exactly what the latest fix targets, so Kanishk needs it.
- **Premiere 2025 projects:** masks come from `prproj_masks.py` (2025 `AEMask`). Test only if a job needs it, on a
  copy.

## Step 13: FCP7 XML with Mac paths (Premiere import needs the boss)
```
cat > "$T/xml/make_edit.py" <<'EOF'
import json, os, sys
T = os.path.expanduser('~/VisionKit/mine/mac-tests'); clip = os.path.join(T, 'frames', 'clip.mp4')
fps = float(sys.argv[1])
json.dump({"name": "Mac XML test", "fps": fps, "total": 3.0,
           "video": [[{"path": clip, "a": 0.0, "b": 3.0, "link": "c1"}]],
           "audio": [[{"path": clip, "a": 0.0, "b": 3.0, "link": "c1"}]]}, open(os.path.join(T, 'xml', 'edit.json'), 'w'))
EOF
$PY "$T/xml/make_edit.py" <clip fps from step 9>
$PY "$SK/scripts/prproj/fcpxml.py" "$T/xml/edit.json" "$T/xml/test.xml"
grep -o '<pathurl>[^<]*' "$T/xml/test.xml"
$PY "$SK/scripts/prproj/fcpxml.py" --check "$T/xml/test.xml"
```
- **Success:**
  - "check: clean"; every pathurl reads `file://localhost/Users/...` (one slash after localhost); `--check` prints
    `OK`.
  - Then the boss imports `test.xml` (File > Import) into a NEW empty project. The sequence appears and the clip is
    online, not offline.
  - This is the first real Mac test of the XML route: log it either way.
- **If Premiere refuses the file or the clip is offline:** log Premiere's message, the pathurl line and the clip's
  real path. Do not edit fcpxml.py; feedback file.

## Step 13b: a generated news-post XML (optional: only if the boss runs the music news pages on this Mac)
- **Where it lives:** `~/VisionKit/kit/library/pipelines/newsdesk/` (read its README). It writes
  `out/<date>/premiere/<id>.xml` with its own Mac-aware path writer.
- **Keep the kit clean:** copy the folder to `$T/newsdesk-test/` and run it there. Its outputs land next to the
  script.
- **Installs (ask for each):** Chrome, ffmpeg, Deno, yt-dlp, gallery-dl, plus the venv packages its README lists (the
  library README suggests its own venv for the pipelines, `~/venvs/kit`; ask before creating it).
- **Build one post** whose media is already on this Mac: `python -X utf8 vcn.py build batches/<date>.json` from that
  venv. Never download for this test without his yes; step 4's note applies to X and YouTube media too.
```
$PY "$SK/scripts/prproj/fcpxml.py" --check "$T/newsdesk-test/out/<date>/premiere/"*.xml
grep -o '<pathurl>[^<]*' "$T/newsdesk-test/out/<date>/premiere/"*.xml | head
```
- **Success:**
  - Every file is `OK`, and pathurls read `file://localhost/Users/...`.
  - The boss imports one XML (File > Import) into a new project: V1 clip, V2 template overlay, A1 audio, all online.
- **If it fails:** log Premiere's message and the pathurl lines. The pipeline is library code; write the problem in
  the feedback file.

## Step 14: After Effects runner, a tiny comp rendered (needs his OKs)
- **Before, ask his OK to launch After Effects for a test.** `ae_run.py` starts it hidden when it is closed, and
  quits only the copy it started.
- **Then he does two things:**
  - In After Effects > Settings > Scripting & Expressions he turns on "Allow Scripts to Write Files and Access
    Network". Every kit script writes its log and DONE flag, and it was found off once. This is an Adobe security
    setting: his yes, his click.
  - The first run makes macOS ask whether Terminal (or the Claude app) may control After Effects. He clicks OK.
    Later: System Settings > Privacy & Security > Automation.
- **AE must be closed, or open with an empty untitled project.**
```
cat > "$T/ae/make_t01.py" <<'EOF'
import sys, os
sys.path.insert(0, os.path.expanduser('~/.claude/skills/premiere-ae-editing/scripts/ae'))
from ae_build import write_jsx
T = os.path.expanduser('~/VisionKit/mine/mac-tests')
specs = ['SHOTS["T01_TEST"] = (function(){ var c = newComp("T01_TEST", 2.0); solidL(c, "bg", [0.1, 0.4, 0.1]); '
         'txt(c, "Mac test", "ArialMT", 90, [1, 1, 1], null, 0, W / 2, H / 2); return c; })();']
print(write_jsx(os.path.join(T, 'ae', 't01.jsx'), [dict(name='T01_TEST', template='h264')], specs,
                out_dir=os.path.join(T, 'renders'), w=640, h=360, fps=30, aep_path=os.path.join(T, 'ae', 't01.aep')))
EOF
$PY "$T/ae/make_t01.py"
$PY "$SK/scripts/ae/check_jsx.py" "$T/ae/t01.jsx"
$PY "$SK/scripts/ae/ae_run.py" "$T/ae/t01.jsx" --ae 2026 --timeout 600
cat "$T/ae/t01_log.txt"
$PY "$SK/scripts/media/frames.py" info "$T/renders/T01_TEST.mp4"
$PY "$SK/scripts/media/frames.py" grab "$T/renders/T01_TEST.mp4" 1.0 "$T/renders/t01_1s.png"
$PY -c "from PIL import Image; print(Image.open('$T/renders/t01_1s.png').convert('RGB').getpixel((20, 20)))"
```
- **Use `--ae 2025`** if he only has After Effects 2025.
- **Success:**
  - The runner says it launched AE hidden (or found an empty untitled project) and waits for the DONE flag.
  - The log shows `START`, `render T01_TEST status DONE` and `ALL DONE`.
  - The render is a 2 s 640x360 H.264; the grab shows a dark green frame with white "Mac test" (read the PNG).
  - The runner quits only an AE it launched itself.
  - The corner pixel is close to RGB (26, 102, 26), within about 6 per channel after H.264. On the Mac the script
    sets the sRGB working space; without it, AE 2026's default (Rec.709 Gamma 2.4) shifted colours by about 12 units
    on the porter's Mac. A bigger shift is a finding: log the pixel value.
- **If it fails:**
  - "DoScript returned without the DONE flag": the scripting setting or the Automation permission is off. Ask him
    to check both.
  - "After Effects has a project open" (from the runner) or "refusing to run: AE already has a project open" (in the
    log): ask him to save and close it.
  - "template fail" in the log: note the AE version.
  - Nothing at all after 300 s: log the runner output, check "running now" in env_check, ask him to look at AE.
- **Then, AE closed or empty:**
  ```
  $PY "$SK/scripts/ae/ae_dump.py" "$T/ae/t01_dump.txt" "$T/ae/t01.aep"; head -30 "$T/ae/t01_dump.txt"
  ```
  - **Success:** the dump lists comp T01_TEST with its solid and text layer (font ArialMT, size 90). On the Mac the
    dump script never quits AE itself; the runner quits AE only if it launched it.
  - `ae_dump.py` always asks for After Effects 2026 (it passes no `--ae`). With only AE 2025 installed it stops with
    "After Effects 2026 not found": run `$PY "$SK/scripts/ae/ae_run.py" "$T/ae/t01_dump_aedump.jsx" --ae 2025 --timeout
    900` instead (the script is already written), and log the gap for Kanishk.
- **Optional, with AE again:** a review preview with sound through `ae_assemble.py` (it uses the voice file from step
  10; without one, drop that item from the JSON).
  ```
  $PY -c "import json, os; T = os.path.expanduser('~/VisionKit/mine/mac-tests'); json.dump({'w': 640, 'h': 360, 'fps': 30, 'total': 2.0, 'items': [{'kind': 'video', 'path': T + '/renders/T01_TEST.mp4', 'a': 0.0, 'b': 2.0}, {'kind': 'vo', 'path': T + '/audio/voice.wav', 'a': 0.0, 'b': 2.0}]}, open(T + '/ae/assemble.json', 'w'))"
  $PY "$SK/scripts/ae/ae_assemble.py" "$T/ae/assemble.json" "$T/renders/assemble.mp4"
  ```
  - Run the `_assemble.jsx` it names with ae_run.py (as above).
  - **Success:** `assemble.mp4` is 2 s with picture and sound; check it with frames.py info and atools.py.
- **Optional:** the AE libraries in a real build.
  - In `make_t01.py` add `libs=[os.path.expanduser('~/.claude/skills/premiere-ae-editing/scripts/ae/motion_lib.jsx')]`
    to the `write_jsx(...)` call and run step 14 again.
  - **Success:** the log has no `BUILD FAIL` and the render is the same.
  - motion_lib needs DM Serif Display for some pieces; scene_lib loads after motion_lib and needs JetBrains Mono.
- **Optional, no After Effects needed:** the motion-design skill's effects library harness, as a dry run on a copy (it
  writes its test folders inside the folder it runs from, so never run it inside the skill):
  ```
  mkdir -p "$T/fx" && cp -R ~/.claude/skills/motion-design/effects-library "$T/fx/" && cd "$T/fx/effects-library" && $PY ae/effects_build.py test one_frame_glitch_burst --dry-run
  ```
  - **Success:** `..._test.jsx ok 1 specs` and "After Effects not started" (the same command passed on Windows on
    14 Oct 2026). A real build of this effect needs no stock clips: the same command without `--dry-run`, with the
    same OKs as t01 above (its Mac branch has never run).

## Step 15: Mac OCR (Apple Vision)
```
"$SK/scripts/media/ocr" "$T/ocr/ocr.json" "$T/renders/t01_1s.png"
$PY "$SK/scripts/media/ocrfind.py" "$T/ocr/ocr.json" "$T/renders/t01_1s.png" "Mac test"
```
- **Success:** ocr.json holds a line "Mac test", and ocrfind prints rects with `score` equal to `of`.
- **If ocr finds no text:** pass absolute paths (Windows OCR needed them; Vision may too) and log the result.

## Step 16: YouTube downloads with ytdl.py (only if he said yes in step 4)
- **Remind him:** the note at the top of `ytdl.py` (bot-check workaround, may break YouTube's terms, only footage he
  has rights to, his decision).
- **Why ytdl.py on a Mac fails as shipped:** its paths now resolve, but `ensure_server()` starts the PO-token server
  with Windows-only process flags. That raises "creationflags is only supported on Windows" when the server is not
  already running.
1. **Installs (ask for each):**
   - `brew install deno`
   - `~/.venvs/premiere-ae/bin/pip install -U "yt-dlp[default]" bgutil-ytdlp-pot-provider`
   - `~/.venvs/premiere-ae/bin/pip show bgutil-ytdlp-pot-provider | grep Version` (note the version)
   - Clone the plugin's server repository (github.com/Brainicism/bgutil-ytdlp-pot-provider) into
     `~/bgutil-ytdlp-pot-provider`, checked out at the release that matches that version (see its tags), then
     `cd ~/bgutil-ytdlp-pot-provider/server && deno install --allow-scripts=npm:canvas --frozen` (the command that worked
     on Windows, premiere-ae-editing `references/youtube-downloads.md`).
   - The server version must match the plugin version (2.0.2 on Kanishk's PC on 14 Oct 2026). Follow the
     repository's own README if its steps differ, and note that.
2. **Port the copy (rule 3):** `mkdir -p "$M/fixes/scripts/media" && cp "$SK/scripts/media/ytdl.py" "$M/fixes/scripts/media/"`.
   In the copy's `ensure_server()`, replace the `Popen(...)` call so Windows keeps its flags and the Mac starts a new
   session:
   ```
   kw = dict(creationflags=flags) if os.name == 'nt' else dict(start_new_session=True)
   subprocess.Popen([...same list...], cwd=os.path.join(HOME, 'node_modules'), stdout=log, stderr=log, **kw)
   ```
   - On Windows the Deno server runs from `server/node_modules` with `../src/main.ts`. Check that layout exists in the
     clone. If the server's own README gives a different start command, follow it and note that in the feedback.
3. **Metadata test:** `$PY "$M/fixes/scripts/media/ytdl.py" <ID of a video he has rights to> --out "$T/yt" --meta-only`.
   - **Success:** `token server 2.0.x` then `metadata ok (... bytes)`.
4. **One real download** of a short video he has rights to: the same command without `--meta-only`. Then
   `$PY "$SK/scripts/media/frames.py" info "$T/yt/"*.mp4`.
   - **Success:** H.264, at least 720p, plays in QuickTime.
   - The cross-session lock lives in `$TMPDIR` on the Mac. One download at a time.
5. **Stop the server you started:** `pgrep -fl "src/main.ts"`, then `kill <that pid>`. Never kill anything else.
6. **Write it up:** feedback file, with the diff and both results.
- **If YouTube asks to sign in, or every client fails:** stop and log it. Never add cookies or a sign-in, and never
  look for other workarounds. The kit's media-toolkit reference describes a plain yt-dlp fallback; use it only with
  his yes.

## Step 17: the remaining scripts (smoke tests, all on copies)
- `$PY "$SK/scripts/captions/style_captions.py" "$T/prproj/copy.prproj" --list`: counts caption blobs per font if the
  project has captions (read only).
  - **Styling test:** only on a copy with captions, written to a new file. Open the result in Premiere only with his
    yes.
  - `exp_patch.py` runs a Python variants file with `exec()`: only ever pass a file you wrote.
- `media/slog3_grade.py`:
  ```
  $PY -c "import sys; sys.path.insert(0, '$SK/scripts/media'); import slog3_grade as g; g.write_cube('$T/frames/test.cube'); print(open('$T/frames/test.cube').read()[:90])"
  ```
  - **Success:** a .cube header and LUT lines. The title reads "immufix natural", a known leftover; log it, no fix.
- `stills/ps_cutout.jsx` with Photoshop 2026 (ask before launching Photoshop):
  - Copy the jsx into `$T/frames/`, set its `HERE` and `OUT` (absolute, trailing `/`), and write
    `ps_cutout_jobs.txt` with one line `<image path>|test` (a photo with a person).
  - Run `osascript -e 'tell application "Adobe Photoshop 2026" to do javascript file (POSIX file "<the copy>")'`. The
    first time, macOS asks to allow control of Photoshop: he clicks.
  - **Success:** `test.psd` and `test.png` (with alpha) in OUT, and a log.
  - Then `stills/psd_composite.py` reads it: `$PY -c "import sys; sys.path.insert(0, '$SK/scripts/stills'); from psd_composite import read_psd; im, L = read_psd('<OUT>/test.psd'); print(im.size, [l['name'] for l in L])"`.
  - And `$PY "$SK/scripts/stills/decon.py" <image> <OUT>/test.png "$T/frames/decon.png"` writes a cleaned cutout.
- `media/edge_shots.py`, `media/edge_words.py`: pure Python and PyAV, but they need cut lists from a long-form
  cutdown job. Test them the first time such a job comes up, and log it then.

## Step 18: OPTIONAL Premiere bridge (only the boss decides, and he runs the installer himself)
- **What it is:** a hidden Premiere panel that runs ExtendScript sent by `scripts/premiere/pp.py`.
  - It listens on 127.0.0.1 only (port 47915 for Premiere 2026, 47916 for 2025).
  - Every request must carry a private token from `~/.editbridge_token`.
  - Requests from browsers are refused.
  - It lets you open, check and export from a running Premiere. Without it you work on saved files only (steps 12
    and 13), which covers most jobs.
- **What the installer changes** (`zsh "$SK/bridge/install_bridge.sh"`):
  - It copies the panel into `~/Library/Application Support/Adobe/CEP/extensions/`.
  - It creates the token file (chmod 600).
  - It sets Adobe's **PlayerDebugMode = 1** for CSXS 10, 11 and 12. That is the setting that lets Adobe apps load
    panels Adobe has not signed. It is global: it lets ANY unsigned panel in that folder load, not only this one.
    That is why only he decides.
- **Explain all of that to him in plain words, then let him choose.** If he wants it, he runs the command himself in
  his own Terminal after reading the script (`zsh ~/.claude/skills/premiere-ae-editing/bridge/install_bridge.sh`); it
  asks y/N before changing anything. You never run it, with or without `--yes`: it changes an Adobe security setting
  (rule 2, and the skill's own rule). If he says no, log "SKIPPED by choice".
- **After install:** Premiere must restart to find the panel. He saves his work and restarts it himself, or you ask
  first. Then test:
  ```
  $PY "$SK/scripts/premiere/pp.py" --v 2026 --status
  ```
  - **Success:** `Premiere 26.x`, his open projects and the active sequence. Read-only: look before acting, every
    time.
  - Never print or log the token.
- **If it fails:**
  - "did not answer": the panel did not load. Check that the folder exists and that he restarted Premiere.
  - The CEP log says "Heartbeat call failed": one more Premiere restart (ask).
  - Two bridges on one port: the installer warns. He removes one (explain which folder).
- **Undo** (he runs these himself if he wants the bridge gone; they are in the installer's header):
  - delete the panel folder
  - delete `~/.editbridge_token`
  - `defaults delete com.adobe.CSXS.12 PlayerDebugMode`, and the same for .10 and .11 unless other unsigned panels
    need it

## Step 19: report
1. **Finish `mac-test-results.md`:** one line per step (PASS / FAIL / SKIPPED), then the coverage table below filled
   in.
2. **Check `feedback-for-kanishk.md`:** one block per problem (file, exact error, your diff in `mine/fixes/`, how you
   tested).
3. **Tell the boss in five lines:** what works, what does not, what is waiting for his decision (bridge, YouTube),
   and what Kanishk will fix.

## Coverage: every script on the Mac (fill in the result column)
| Script | Mac status before this run | Step | Result |
|---|---|---|---|
| env_check.py | Mac branch never run | 7 | |
| ae/ae_run.py (DoScript runner) | never run on a Mac in this form | 14 | |
| ae/ae_build.py, ae_assemble.py | Mac template simulated only | 14 | |
| ae/ae_dump.py + ae_dump.jsx | Mac branch simulated only | 14 | |
| ae/ae_lib.jsx (glyph fallback ArialUnicodeMS) | not run | 14 | |
| ae/motion_lib.jsx, scene_lib.jsx | ran on the porter's Mac before the merge | 14 (optional) | |
| ae/check_jsx.py | works | 8 | |
| media/atools.py (ffmpeg extract) | not run | 9 | |
| media/frames.py (Mac fonts) | not run | 9 | |
| media/beats.py, fsheet.py | not run (fsheet: tiny labels known) | 9 | |
| media/hear.py (mlx-whisper) | ran on the porter's Mac before the merge | 10 | |
| media/speech_cuts.py (new rules) | Windows only | 11 | |
| media/ocr.swift, ocrfind.py | not built | 6, 15 | |
| media/fontcheck.swift | not built | 6 | |
| media/slog3_grade.py | not run | 17 | |
| media/edge_shots.py, edge_words.py | not run | first cutdown job | |
| media/ytdl.py | paths resolve on a Mac; starting the token server is Windows-only (one-call port in step 16) | 16 | |
| media/ocr.ps1, sapi_words.ps1 | Windows only (not for the Mac) | none | n/a |
| prproj/prproj_lib.py (path style, track IDs) | simulated only | 12 | |
| prproj/prproj_dump.py (--own-names default) | not run | 12 | |
| prproj/validate_struct.py, prtranscript.py | not run | 12 | |
| prproj/fcpxml.py (Mac pathurl) | simulated only; Premiere import untested | 13 | |
| ffmpeg h264_videotoolbox / libx264 | not run | 9b | |
| library newsdesk XML (its own writer) | not run on a Mac | 13b (optional) | |
| prproj/prproj_masks.py | Premiere 2025 projects only | 12 (if needed) | |
| captions/*.py | pure Python, not run | 17 | |
| stills/ps_cutout.jsx, psd_composite.py, decon.py | not run | 17 | |
| premiere/pp.py + bridge/ | not installed | 18 (optional) | |
| motion-design `effects-library/ae/effects_build.py` | Mac branch read, never run | 14 (optional) | |
| meme-compilation-edit `reference-pipeline/` Swift tools (`ocr_batch.swift`, `wins.swift`) | ran on the porter's Mac | the first meme job | |
