# Working with a running Premiere (window or bridge) and exporting

Use a running Premiere only for what scripts on the saved file cannot do: opening a build to check it, importing
non-H.264 media, caption tracks, frame grabs, exports. Everything else is faster and safer by script on a copy of the
.prproj. Two ways in:
- **The window, by computer use** (the Windows route): screenshots at scale 0.4-0.5, zoom only on details.
- **The CEP bridge** `scripts/premiere/pp.py` (the Mac route, optional): ExtendScript sent to a hidden panel inside the
  running Premiere. The user installs it (mac-notes.md). It is not installed or tested on Windows; use the window there.

## Safety first (both)
- The user often has ANOTHER project open (with unsaved changes), on a Mac maybe in Premiere 2025 AND 2026. Look before
  any action: the title bar (window), or `python scripts/premiere/pp.py --v 2026 --status` and `--v 2025 --status`
  (bridge: open projects and the active sequence).
- Never quit Premiere (Ctrl+Q / Cmd+Q prompts to save every open project), never press Save / Don't Save on a project you
  were not asked to touch. Close only your own project: Ctrl+Shift+W (Cmd+Shift+W) while its title bar is active, or
  by bridge (below). Never restart Premiere without asking (the bridge sometimes needs one: ask).
- Never start the Adobe Media Encoder queue (it holds the user's old jobs). Export only when the user asks, otherwise
  tell them the new version is ready to export.
- Ask before opening Premiere if the user may be working in it. With enough RAM (31 GB was fine) Premiere and After
  Effects can run together; one After Effects at a time.
- A malformed project can crash Premiere on open and take every open project down with it (a bad caption blob did,
  9 Oct 2026). Validate first (`validate_struct.py`), and ask before opening a hand-built project in the Premiere the
  user is working in.
- The user may duplicate a sequence and keep editing the copy while scripts run. Find sequences by NAME, never
  `app.project.activeSequence` (a solo-mute test export hit the user's copy and reset its track mutes). QE only sees the
  active sequence: check its name before any QE call.
- A frozen After Effects or its crash reporter can sit on top of Premiere as a masked grey block in screenshots.
- Two project files built from one another share internal IDs and sequence GUIDs: have only one of them open at a time.
- Before closing YOUR project, read its title bar: if it shows unsaved changes the user made while it was open, save
  them (they are theirs) and diff the save; your own inspection clicks are not edits (Ctrl+Shift+W, Don't Save). Once
  the user clicked Save on an inspection: harmless after a diff.
- Stay off the screen while the user works on the PC (computer use would fight them for the mouse): check state from
  logs, preference files or the saved project instead.
- Computer use on Windows: windows of apps that are not granted (the Adobe licensing helper, a crash reporter, the
  Claude window itself) show as blank grey blocks that cannot be clicked. Ask the user to dismiss or move them, and
  type paths into dialogs instead of clicking lists hidden under them. Premiere sometimes opens to Home without the
  project: open it from Recent.
- Tell the user about side effects on their apps: Export Frame remembers its last folder, so their next export would
  land in your check folder unless you say so.

## Open and check a build by window (Windows)
1. `request_access(["Adobe Premiere Pro 2026"])`, then PowerShell `Start-Process "C:\path\Show v2.prproj"`.
   Wait about 40 s (big projects longer), screenshot at 0.4.
2. No dialog = structure accepted. A "locate media" or "could not be opened" dialog = a broken build: cancel, close,
   fix the file (do not "fix" it in the UI).
3. Go to a time: click the timeline's playhead timecode (top-left of the timeline panel), Ctrl+A, type the full
   timecode "00:00:03:15", Enter. Typing bare digits after a double-click went to the wrong time. Panel layouts change
   between sessions: find the timecode field again in every session before clicking (the clicks missed it once).
4. Look at the Program monitor with a zoom on its picture area (cheap), or Export Frame for a full-resolution PNG.
5. Click a clip to see its Effect Controls (Motion values in pixels, effects, keyframes) when a placement looks wrong.
6. Check every changed time, not one sample: a structurally valid project once drew a clip at the wrong time.
7. Leave your build open for the user only if they asked; otherwise Ctrl+Shift+W and "Don't Save" (it shows "Edited"
   right after loading an externally built file; that is not a change of yours).

## Open and check a build by bridge (Mac)
1. Ask, then open it as a SECOND project:
   `pp.py --v 2026 -e 'app.openDocument("/abs/Show v8.prproj", true, true, true, true)'`. Their project stays open.
   A project saved by 2026 cannot be opened by 2025.
2. Opened with no error = structure accepted. A "locate media" or "could not be opened" result = a broken build: close
   it, fix the file, do not "fix" it in the UI.
3. Make it active and grab frames at every changed time (sequence time as a timecode string):
   `qe.project.getActiveSequence().exportFramePNG("00;00;05;00", "/abs/check/f_0500")`. Right after opening, the
   first export can show "Media pending": export again once media has loaded. Sheet them with `frames.py`.
   Two traps found later (Dynamic Link builds, below): it appends ".png" itself (a name ending in .png becomes
   "name.png.png"), and it reads the timecode as plain 30-per-second frame counting, so drop-frame strings landed 2
   frames late after 1:00. Check a grab against a known frame before trusting a batch.
4. Check every changed time, not one sample: a structurally valid project once drew a clip at the wrong time.
5. Close only your own project: find its index in `app.projects` by path, then `app.projects[i].closeDocument(0, 0)`
   (no save). Leave it open only if the user asked.
- 11 Oct 2026 (25.6.6): with the user's project open, `app.newProject(path)` from the bridge opened the new project as a
  SECOND project (both in `app.projects`, theirs untouched), and `app.project.closeDocument(0, 0)` at the end of the
  build closed only the new one. Ask first (the user approved it once for a build).
- Full list of proven bridge calls and their traps (overwriteClip, stills on a 29.97 grid, QE effect order, setSpeed):
  mac-notes.md.

## Export Frame by window (full-resolution still of the real timeline, Windows)
- Ctrl+Shift+E, format PNG, untick "Import into project", choose a folder reachable from Quick Access (the dialog only
  lets you click folders), type a file name when the sequence name contains "/".
- If the previous export is still writing, the next playhead move is swallowed and you get a DUPLICATE frame. Wait about
  6 s per export on heavy sources (4K, ProRes, downloaded clips), then check: `python frames.py dupes a.png b.png ...`.

## Import (non-H.264 media, folders of SFX, AE renders)
- By window: Ctrl+Shift+A first (deselect) or the import lands inside the selected bin. Ctrl+I, type the full path in
  the File name box, Enter. Many files: type the folder path, Enter, then quoted names in batches of about 12 (more gives
  "File not found"). "Import Folder" makes a bin named after the folder. Ctrl+S, close, rebuild your script on that save.
- By bridge: `app.project.importFiles([paths...], true, app.project.rootItem, false)` with about 20 paths per call, save,
  next call (150 files in one script stalled Premiere 2025 with stacked progress windows). Import into the working COPY,
  save, then rebuild with prproj_lib from that save (`master_by_name`). By hand on a Mac: Cmd+Shift+A, then Cmd+I.
- VP9-in-MP4 never lands in Premiere 2025: convert to H.264 first (check `ffprobe` codec_name).

## Captions (bridge)
- `seq.createCaptionTrack(srtProjectItem, 0, Sequence.CAPTION_FORMAT_SUBTITLE)` builds the track; a re-made SRT must be
  imported under a NEW file name (Premiere keeps the old item's captions). Styling: patch the saved file
  (captions-style-patch.md).
- Caption width at Lora Italic 58 in 1080x1920 is about 780 px; split longer lines.

## Timeline quirks (window)
- Double-click a panel tab to maximize / restore it; "\" fits the whole sequence.
- Mouse wheel and Ctrl+wheel both scroll HORIZONTALLY in this timeline (Windows).
- The video / audio divider sits just under V1: dragging a few px too high grabs a V1 clip and makes a new track (undo).
- Sequences open from a bin by double-click. But double-clicking a sequence that is ALREADY open (found through the
  Project panel search) did NOT switch the Program monitor, and Export Frame then exported the wrong ad. Switch by the
  timeline tabs (and the ">>" overflow list), and confirm the monitor shows the right sequence before every export.

## Export (only when asked)
- By window: Ctrl+M (Cmd+M). It remembers settings per sequence: CHANGE the Location every time (it pointed at the
  previous version's folder once). Preset used for deliveries on the Windows PC: H.264 "Match Source - Adaptive High
  Bitrate" (about 38 Mbps VBR, NVIDIA, AAC 320k). Captions: "Burn Captions Into Video" on the subtitle track when the
  edit has a caption track (leave off when the subtitles are graphics). Effects (watermarks etc.): all unchecked.
- By bridge: `seq.exportAsMediaDirect("/abs/out.mp4", "/abs/preset.epr", 0)` renders synchronously (about 2 min of
  timeline in 24 s; with about 21 Dynamic Link comps, 59 s took about 100 s). Captions: copy the .epr and set
  `ADBECaptionExportOption` (0 none, 1 sidecar .srt, 2 burn in).
- Loudness: renders came out around -13 to -15 LUFS with peaks about +0.1 dBTP without normalization. For -14 LUFS /
  -1 dBTP tick Loudness Normalization in the export settings, or export with
  `assets/presets/H264 match source, -14 LUFS.epr` (a copy of the Frame.io "h.264 Match Source" preset with loudness on;
  a test export measured -14.2 LUFS and -1.0 dBTP).
- An SFX tail past the last video frame stretches the export: trim audio to the sequence end.
- "Match Source - High bitrate" MP4s carry no AAC priming edit: the audio decodes 1024 samples (21 ms) late, which
  matters only for null tests.
- One sequence at a time, save before exporting (a PC crashed once during a long export run).
- After "Send to Media Encoder", Premiere drops back to the Edit view and the next "Export" click hit a monitor menu:
  press Escape, then Ctrl+M again. A sequence can also remember an old custom preset (one saved MP3s to Downloads):
  check the preset as well as the location every time.
- Before exporting a sequence with a new ending, check it has no in / out marks, or the export stops at the old out
  point. Read the previous delivery's settings from its files first (`frames.py info`: size, fps, frames, codec;
  `atools.py`: loudness) so the new version matches.
- "Which ones should I export?": answer with the one file to open, a per-piece table of what changed and the new
  lengths, and the result of the in / out check.

## Sharing a whole project with a collaborator
1. If the edit lives in an XML, import it into a new project, scrub for red "Media Offline" frames, save.
2. File > Project Manager > "Collect Files and Copy to New Location" (NOT "Consolidate and Transcode", which re-encodes
   the shots). Tick "Exclude Unused Clips"; leave "Rename media files" and "Include Audio Conform Files" off; pick an
   empty destination; Calculate (a 10-minute explainer came to 161 files, about 10.4 GB), then OK. Premiere writes a
   "Copied_<project>" folder.
3. Zip it and send it by Drive or USB (free WeTransfer stops at 3 GB). The other editor needs Premiere 2026 or newer for
   a 2026 project; otherwise send the XML plus the media to relink.
4. Graphics baked into renders cannot be edited in Premiere: send the After Effects projects and the fonts too.

## When a step needs Premiere's window
Offer the choice: "you do File > Import on the XML, or I take your screen for about 2 minutes", and leave the user's
other open project alone. Users often prefer to import themselves and keep editing.

## Built-in tools worth testing (research, not tried here)
- Premiere 26 Object Mask (Jan 2026): one-click subject masks, maybe instead of a SAM 2 matte (media-toolkit.md
  section 12).
- Film Impact transitions became free in Premiere in 2025; Mister Horse Animation Composer may already be installed
  (its title templates carry `<AdjustmentLayer>true`, prproj-format.md section 9).
- Third-party Premiere MCP servers exist (one sends telemetry by default, another cannot read Essential Sound ducking):
  not used; this skill's own routes are the saved file and the bridge.

## When you need the window on a Mac (rare)
- System Events cannot see Premiere's windows; a Swift CGWindowList script finds them and `screencapture -l <windowID>`
  grabs one even behind other apps. AppleScript `activate` / `quit` on Premiere time out.
- The timeline quirks above are the same app (except the mouse wheel note, which was seen on Windows).

## Layered renders with alpha (13 Oct 2026, Premiere 26.5.1 on the Mac)
- Sequences from the user's projects had "Composite in Linear Color" ON. A glow/shadow caption layer (ProRes 4444
  alpha) then blends in linear light and shows as a bright grey box around the text. Turn it off for that sequence:
  `var st = seq.getSettings(); st.compositeLinearColor = false; seq.setSettings(st);` After that, Premiere frames matched
  the Python reference composite at 49-56 dB PSNR. On Windows the same switch is in Sequence Settings (not tried there).
  Linear-light blending is also why a graphic at 86 % opacity looks see-through (prproj-format.md section 9).
- `FootageInterpretation.alphaUsage`: 1 = straight, 2 = premultiplied (2 on a straight file turns transparent pixels
  white), 0 = what a fresh import reports. Set it with `item.setFootageInterpretation(fi)`; `item.changeMediaPath(path,
  true)` relinks every placed segment at once.
- Extending an audio clip: `trackItem.end = time` moves the end, but `outPoint` still reads the old value until you also
  set `trackItem.outPoint` (media time). Confirm in the saved file with prproj_dump.

## Dynamic Link builds (13 Oct 2026, on the Mac)
- `importAEComps` names the items "Comp name/Project.aep": match bin items by that prefix, not the bare comp name.
- Premiere 26.5 colour-manages Dynamic Link comps as sRGB (the AE working space) and converts them to its Rec. 709
  working space, which lifts the shadows (code 4 became about 16, 81 became 90). Fix per item:
  `it.setOverrideColorSpace(rec)` with `rec` = the entry named "Rec. 709" in `seq.getSettings().workingColorSpaceList`
  (a name string is refused). After it, 30 Export Frame checks matched the AE renders within 1 to 4 levels.
- QE `exportFramePNG(tc, path)` reads `tc` as plain 30-per-second frame counting (drop-frame strings landed 2 frames late
  after 1:00) and appends ".png" itself.
- Fast audio check without rendering picture: `seq.exportAsMediaDirect(out.wav, PRESET, 0)` took 6 s for 100 s;
  null-test it against the reference mix. PRESET = the Media Encoder bundle's
  `Contents/MediaIO/systempresets/3F3F3F3F_57415645/Waveform Audio 48kHz 16-bit.epr` (on the Mac).
- AE-side rules for linked comps: after-effects.md section 14.
