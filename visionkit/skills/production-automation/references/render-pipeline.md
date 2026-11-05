# Render pipelines

How each engine renders, the settings we use, how we made renders faster without losing quality, and the gating that
keeps the machine usable. Frame and loudness mechanics that are not pipeline-specific are in premiere-ae-editing
(timing.md, audio.md, after-effects.md).

## 1. Stills from HTML (headless Chrome)
- Command (one PNG per card): `chrome --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1
  --window-size=W,H --default-background-color=00000000 --virtual-time-budget=6000 --user-data-dir=<own profile>
  --screenshot=out.png file:///page.html`. The transparent background colour makes overlay PNGs keep their alpha.
- Fonts are injected as `@font-face` rules pointing at font files; the page calls `document.fonts.load('40px X')` for
  every family and fits text only after `document.fonts.ready`. The fit loop shrinks the size 2 px at a time until
  nothing overflows (`fit(el, max, min, maxH)`). Why: exact fonts and text that always fits, with no clicking.
- If the PNG comes back a different size, crop to the target when it is larger, else resize.
- Give Chrome its own `--user-data-dir`. Never ship that profile folder: it holds a Cookies database.
- Speed: 12 test posts in 51 s; a day's 8 posts in about a minute.
- Headless Edge wrote nothing (it hands off to a running Edge), and headless Chrome crashed on a very tall shop page:
  use Chrome, a normal window height, and keep a fallback (the user's screenshot, or a typeset quote card).

## 2. Video from HTML (frame by frame)
- One headless Chrome per batch driven over the DevTools protocol (Python `websockets` sync client), each instance on
  a free port with its own profile (a shared profile made the second Chrome fail).
- Templates expose `window.show(spec)` (build the scene) and `window.renderAt(t)` (pose it at time t). GSAP 3.12.5
  timelines are seeked per frame. Each frame is a `Page.captureScreenshot` JPEG at quality 93 piped into ffmpeg:
  `-f image2pipe -framerate 30 -c:v mjpeg -i -` then `libx264 -crf 17 -preset medium -pix_fmt yuv420p -movflags
  +faststart`.
- Footage enters as a JPG frame layer (the clip cut into frames with a cover crop around a focus point), or a photo
  with an eased camera pan and push. Real camera moves only: no fake breathing or sway on people.
- Fonts: search the asset fonts folder recursively and skip Italic files (an Italic fallback once got picked);
  variable fonts get `font-weight: 100 900`.
- Pure-function test: render frame 45, then 20, then 45 again; the two 45s must match. Why: any state carried between
  frames breaks seeking.
- Motion renders start 0.5 s into the timeline so frame 0 (the cover) already shows the hook; every number on frame 0
  is final and true, never mid-count.
- Speed: a 7 s video in 11 s; 9 posts (50 images, 8 videos) in 78 s; 18 posts (104 images, 14 videos) in about 4 min.
- Alternative (reference set): a PIL frame engine driven by a timeline file across parallel processes (59 s of video in
  about 10 s with 12 processes). Every multiprocessing script needs `if __name__ == "__main__":` (workers are spawned on
  macOS and Windows); fork pools hung with OpenCV, so separate `--range` processes were used.

## 3. ffmpeg compositing (the news-post recipe)
One ffmpeg run per video makes the final, the editable layers and the audio.
- **Inputs:** the clip (`-ss in -t dur`), the overlay PNG looped at the frame rate, and optionally the song
  (`-ss song_in` at the beat drop).
- **Letterbox bars:** `cropdetect=24:2:0` over 4 s starting 0.5 s after the in-point; apply only when the crop is under
  92% of the width or height and over 40% (so a real edge is never mistaken for bars). Spec `crop: false` turns it
  off; `"w:h:x:y"` forces one. Why: baked-in bars waste the vertical frame and look like a lazy re-upload.
- **Pre-filter:** an optional filter before the crop, for example `delogo=x=20:y=258:w=536:h=160` over another page's
  burned-in caption on the only copy of a clip (keeps the native LIVE badge and comments). Flag it: removing someone
  else's caption from their clip is a rights and taste call for the reviewer.
- **Layouts:** full-bleed cover crop with focus `fx`/`fy` 0 to 1; blurred fill (background = the clip scaled to cover,
  `boxblur=30:2,eq=brightness=-0.22`, foreground on top); split (black canvas, clip from y 560 under two photos);
  tweet (clip starts under the card, card bottom read from the overlay's alpha bounding box + 30 px); headline box at
  least 760 px tall centred at y 650 for wide clips; black background for app screen recordings (a blurred copy only
  shows smeared logos).
- **Subtitles:** ASS file through the `subtitles` filter with a fonts folder (needs ffmpeg built with libass).
- **Audio:** `afade=t=out:st=<dur-1>:d=1,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000`; modes `clip` (the clip's own
  sound), `song` (the client song from its drop), `mix` (song bed under the clip at `bed_db`, default -14 dB, `amix ...
  normalize=0`).
- **Outputs in the same run:** final MP4 (libx264 preset medium CRF 19, yuv420p, AAC 192k, `+faststart`), the base
  layer MP4 without overlay (veryfast CRF 20, no audio), the WAV (pcm_s16le), and a keyed reaction layer when present
  (`-c:v qtrle -pix_fmt argb`). Then the two XMLs are written (references/principles-and-build-engines.md section 3).
- A re-render of one post takes about 20 s.

## 4. The long-cut renderer (house recipe in ffmpeg)
- Renders each clip as an MPEG-TS part with `-video_track_timescale 15360`, then joins them. Why: MKV parts (1 ms
  clock) left the joined file 1 to 8 ms off the frame grid and faked flashes in frame-exact QC.
- Frame-exact trims: start from `pre - 0.5/fps` and cut with `-frames:v N`; seek a quarter frame into the target frame
  (ffmpeg keeps the frame whose interval contains the seek point). An insert at another frame rate (25 fps into 29.97)
  came up one frame short: pad it with `tpad=stop_mode=clone`, then `-frames:v`.
- Probe the frame rate of every source; read the stream's nominal rate (a container average read 29.974 for 29.970 and
  drifted 3 frames over 13 minutes).
- Split edits: the picture stops where it must and the sound tail runs on up to 0.35 s.
- Inserts, dips to white, scene flashes and music beds come from the plan; the render and the XML share one audio
  layout.
- **Parallel parts plus a part cache:** encode 3 to 4 parts at a time; cache each part under a hash of its exact
  ffmpeg command plus the input's size and modification time, so a QC fix re-encodes only the clips that changed.
- **Numbers (Windows laptop, RTX 12 GB, NVENC):** a 13:06 cut rendered in 2:08 (about 6x real time); a cached fix took
  49 s; CPU renders had taken 10 to 13 minutes, and about 4x longer on battery.
- **The chain per video** (one line printed per finished step, so a Monitor can stream it): render -> seam verify ->
  make XML (with `--check`) -> QC seam sheet -> true-peak fix.

## 5. Choosing the encoder by a VMAF test
Why: the editor asked "why does it take SOOO much time... speeding things up without losing any quality", and a
number settles "without losing quality".
- Method: encode the same 30 s of real 1080p source with each candidate; measure VMAF against the source (95 or more is
  visually lossless), the time as one job, the file size, and the throughput with 4 and 8 parallel jobs. Write a small
  benchmark script for it (VMAF needs ffmpeg built with libvmaf).
- Windows result (30 s of 1080p 29.97):

| Encoder | One job | Size | VMAF | Parallel throughput |
|---|---|---|---|---|
| libx264 CRF 16 fast | 6.6 s | 46 MB | 99.84 | 5.8x real time (4 jobs) |
| NVENC H.264 | 6.0 s | 85.5 MB | 99.87 | 8 to 9.8x (4 to 8 jobs) |
| AMF | 6.7 s | 65.5 MB | 99.83 | not tested |

- NVENC quality steps: cq 19 = 68 MB / VMAF 99.867; **cq 21 = 54.7 MB / 99.854 (chosen)**; cq 23 = 44 MB / 99.75. GPU
  decoding gave no gain. Flags used: `-c:v h264_nvenc -preset p6 -tune hq -rc vbr -cq 21 -b:v 0 -maxrate 60M
  -bufsize 120M -profile:v high -spatial-aq 1 -temporal-aq 1 -rc-lookahead 32 -g 120`. NVENC needed NVIDIA driver 610
  or newer (596 failed).
- **On the Mac (untested on his machine):** there is no NVENC. Run the same bench with `h264_videotoolbox` and
  `hevc_videotoolbox` against libx264. VideoToolbox takes `-b:v` (a bitrate) or, on Apple Silicon, `-q:v` (1 to 100);
  pick the value by VMAF the same way. Apple chips have a fixed number of hardware encode engines (more on Max and Ultra
  chips), so 3 to 4 parallel hardware jobs may queue instead of adding speed: let the bench choose the job count.
  Check first: `ffmpeg -hide_banner -encoders | grep videotoolbox` and `ffmpeg -hide_banner -filters | grep vmaf`.
- The long-cut renderer reads the encoder from the plan (`plan['encoder']`) or the `CUT_ENCODER` environment
  variable (default `nvenc`). If a 0.2 s test encode with `h264_nvenc` fails, it falls back to `x264` (libx264 preset
  fast, CRF 16, `-g 120`), which is what a Mac gets today. `plan['jobs']` (default 4) sets how many parts encode at
  once. Adding VideoToolbox means a new branch in `video_encoder()` and a new name for the bench:
  `python3 render_bench.py SOURCE.mp4 START SECONDS [--jobs 1] [--encoders x264,amf,nvenc]`.

## 6. Loudness and audio finishing
- Targets: deliver about -14 LUFS, true peak at or below -1 dBTP, 48 kHz. Platforms publish no upload target; -14 to
  -16 LUFS is the safe band.
- **Long mixes:** two-pass `loudnorm` on the full mix (I -14, TP -1, LRA 20, `linear=true`), then `alimiter` (limit
  0.70, attack 3 ms, release 60 ms, `level=false`), AAC 256k with `-aac_pns 0`; `tp_fix.py` re-limits at 0.70, then
  0.63, then 0.56, only if true peak is still over -1 dBTP. Results on about 40 renders: -13.9 to -14.9 LUFS, true peak
  -1.3 to -2.8 dBTP. Interview-heavy mixes measure about -18.7 LUFS raw; one short at -15.1 LUFS was accepted.
- Why each piece: louder beds after a review pushed true peak to -0.24 dBTP; an AAC noise-substitution burst made a
  +3 dB spike (hence `-aac_pns 0`); a 192 kHz oversampled limiter made it worse (+1.2 dBTP: the resampler rings).
- **Short posts:** one-pass loudnorm (I -14, TP -1.5, LRA 11) after a 1 s fade-out is enough for 15 to 30 s clips.
- **Every audio edit gets a 4-frame equal-power crossfade** centred on the cut with handles from both sides (cutdowns;
  "apply 4 frame cross fade between ALL the audio clips to prevent peaking").
- **Never bake a gain boost into a WAV.** A bed baked +8 dB hit peak 1.0; use level keyframes in Premiere instead.
- **Measure every render and preview.** Premiere exports with no loudness normalisation measured -13 to -15 LUFS with
  true peak +0.1 dBTP: offer a normalised version (premiere-ae-editing has a -14 LUFS export preset). A preview hit
  0.0 dBTP at its biggest booms.

## 7. After Effects renders inside a pipeline
- One After Effects at a time, one render-queue item at a time (20 queued items crashed AE), a 2 s test comp or a
  `--range A-B` render of one moment before a big batch, H.264 for previews and ProRes 422 ("High Quality") for finals,
  ProRes 4444 ("High Quality with Alpha") for elements.
- Never kill AE while a render file is still growing (three 1 MB stubs once); close it gracefully. Wait for a security
  preference with a file-writing ping script, not by watching the screen (references/scheduling-and-unattended-runs.md).
- **Render cost decides the re-render scope.** Graphic and card shots render in seconds; shots with lens blur on a big
  2.5D room plate are slow: 3 such shots about 6.5 min, a 26.8 s end shot 518 s (447 MB ProRes), 17 shots about
  45 min, a 10:38 H.264 preview about 20 min. A 30 s 1080x1920 layered music edit took 82 to 111 s (slower once every
  clip carried Motion Tile).
- Long films (reference set): render in frame ranges, one aerender at a time, join with the concat demuxer and lay the
  audio separately (an aerender once died near the end).
- Scripted builds leave auto-save copies (107 files of 2 to 8.6 MB in one job): save build projects to scratch or clean
  them up after delivery, with the user's OK.
- On the Mac the skill's `ae_run.py` takes its Mac route by itself: the script goes in through AppleScript `DoScript`
  into a running AE (it refuses to replace a project the user has open), or a saved project renders with `aerender`
  (premiere-ae-editing mac-notes.md). The Windows command (`AfterFX.com -r`) does not apply there.

## 8. Premiere exports inside a pipeline
- Before rendering a new version, read the previous delivery's settings from the files: duration, size, fps and
  frame count from the MP4 atoms plus integrated LUFS and true peak per file, one line each (ffprobe plus the skill's
  `atools.py`).
- Export from Premiere's Export mode one sequence at a time into a NEW folder; never start the Media Encoder queue
  (it held the user's old jobs). Save first; check power and load. The PC once crashed after 4 of 8 exports (no half
  files were left; the user rendered the rest).
- Check in and out marks: with none, exporting the whole sequence picks up newly appended endings.

## 9. Gating heavy work
- **One heavy job at a time.** `heavy_gate.py` (cutdowns): call `wait_turn()` before any heavy step; "heavy" = a python
  process whose command line contains the render, prep, transcription or caption tools; poll every 20 s and wait for
  2 quiet polls in a row. A failed or empty process query counts as busy: once an empty answer under load let a render
  start on top of a prep.
- **GPU lock file** for transcription preps (two large Whisper models do not fit in 12 GB), stale after 40 min; several
  preps can queue on it and each download hands off to its prep the moment it lands. Remove a stale lock only after
  confirming its process is dead.
- **One GPU job at a time** for mattes (two edits' SAM 2 jobs compete for a 12 GB card); one After Effects; one
  download.
- **One YouTube call at a time across all processes:** a lock file (stale after 20 min), a 6 s gap and
  `--sleep-requests 0.75`. About 15 parallel calls got a 15 minute "not a bot" block; two downloads at once gave 403,
  "format not available" and 0-byte files.
- **Power:** on battery the laptop CPU was capped at 2.4 GHz and libx264 ran about 4x slower; wait for mains power.
  Mac check: `pmset -g batt` (untested).
- **Disk:** check free space before render-heavy steps (`df -h /` on a Mac). Once only 8.7 GB was free and Claude's own
  scratch held 8.3 GB; clean only your own scratch.
- **RAM:** one Adobe app at a time until the machine had 31 GB; after that Premiere and AE could run together.
- **Hold renders when the user is busy:** build everything light, then wait for "go" (references/scheduling-and-unattended-runs.md).

## 10. Planning numbers
| Job | Time |
|---|---|
| A day's 4 to 8 news posts, build only | about 1 minute (12 test posts in 51 s) |
| One news video re-render | about 20 s |
| 18 HTML posts (104 images, 14 videos) | about 4 min |
| Transcription prep of one 12 to 36 min source | 3.3 to 16.8 min (GPU) |
| One long cut render (13 min) | 2:08 on NVENC; 10 to 13 min on CPU |
| Three long cuts rendered, checked, fixed, re-rendered | about 25 min |
| 15 cutdown files unattended (one heavy job at a time) | about 2 h 25 min |
| Three music edits from setup to render | about 1.5 h |
| SAM 2 matte at 1080p | about 8.5 fps (RTX 12 GB; slower on MPS) |
| 10:38 explainer rough cut from intake | about 4.5 h |
