# Media toolkit: getting, reading and measuring media

Methods from the Mac port (verified there between late September and 14 Oct 2026). The commands are plain yt-dlp,
ffmpeg and Python, so most run on Windows too (bash syntax: use Git Bash, or set the variables by hand); the Mac-only
pieces (mlx-whisper, Apple Vision, the Apple GPU for Demucs) are marked. Only download when the user asks.

## Contents
1. Downloading video (yt-dlp)
2. One moment of a long video, frame-accurately
3. Stock footage and stills
4. Clean copies of watermarked video memes
5. Transcription
6. Splitting voice and music, identifying songs
7. Cuts, OCR, colour and motion measurement
8. Stills of every meme in a compilation video
9. House rules for media jobs
10. Encoding renders with ffmpeg
11. Keying and alpha with ffmpeg
12. Subject mattes with SAM 2
13. Tracking without Mocha
14. Reading documents (PDF highlights and notes)

## 1. Downloading video (yt-dlp)
- Read the rights note in youtube-downloads.md first: these lines (other player clients, format fallbacks) work around
  YouTube's checks the same way the PO-token route does, so the same rule applies: only footage the user or client has
  the rights to use, only when the user asks, one download at a time, and the reviewer decides whether the route stays.
- YouTube on the Windows PC: `scripts/media/ytdl.py` with its PO-token setup (youtube-downloads.md) is the main route.
  The plain yt-dlp lines below are the Mac port's route (and the fallback where ytdl.py is not set up).
- When the user pastes links plus a folder, download edit-ready MP4 (H.264 + AAC) without asking about format:
  `yt-dlp -f "bv*[vcodec^=avc1]+ba[acodec^=mp4a]/b[ext=mp4]/bv*+ba/b" --merge-output-format mp4 --no-playlist -N 4 -o "<dest>/%(title)s.%(ext)s" <URL>`.
  VP9/AV1 files scrub badly in Premiere, which is why H.264 wins even though it usually caps at 1080p. `--no-playlist`
  is deliberate (links often carry a `&list=` the user does not mean). Report the file path and size when done.
- If extraction fails, update yt-dlp first (a pip copy in a venv is often newer than Homebrew's or winget's).
- YouTube "Sign in to confirm you're not a bot" / 429 without the PO-token setup: update yt-dlp, then add
  `--extractor-args "youtube:player_client=web_embedded"`, which still returned 137 (1080p H.264) + 140-16 (original-
  language AAC; plain 140 may be missing when a video has dubbed audio tracks). The format list flickers between runs,
  so use fallbacks (`137+140-16/137+140/96-17/...`) and retry up to 3 times. Avoid `-drc` audio variants. Heavy use
  triggers the bot check for a while (it cleared in about 20 minutes once). One download at a time
  (youtube-downloads.md). Never use the user's browser cookies.
- Instagram reels of public accounts and X videos download with yt-dlp without a login (X "http-*" formats include
  audio). X-hosted clips vanish: the originals behind official-looking posts were deleted (404) the next day, so fetch
  the same day and prefer broadcasters' own posts or your own recordings. Reading X through unofficial mirrors may break
  X's terms: research-and-sourcing.
- Exact sections in H.264 at 1080p (imports cleanly in Premiere, no whole-video download):
  `yt-dlp -f "bv*[height<=1080][vcodec^=avc1]+ba[ext=m4a]/bv*[height<=1080]+ba/b[height<=1080]/b" --download-sections
  "*S-E" --force-keyframes-at-cuts --merge-output-format mp4 URL`. Its trailing `/b` can quietly give 360p
  (youtube-downloads.md): check the height after download. Vertical sources: filter on the shorter side, not on height.
- Search without downloading: `yt-dlp "ytsearch10:<terms>" --skip-download --print "%(id)s %(title)s %(channel)s
  %(duration)s %(view_count)s %(live_status)s"` (live_status shows scheduled premieres). Thumbnails:
  `https://i.ytimg.com/vi/<id>/maxresdefault.jpg` (1280x720), else `hqdefault.jpg`.
- A Vimeo video that answers 401 is embed-restricted by its owner, and a TikTok blocked on one network may be blocked
  for a reason: ask the client for the file or a download link instead of working around the restriction. (The Mac port
  noted workarounds for both; they were left out of this kit on purpose.)

## 2. One moment of a long video, frame-accurately
Do not download a whole 4K file for a 20 s moment. Get the stream URLs and let ffmpeg seek on them:
```
VURL=$(yt-dlp --no-playlist -f "bv*[height<=2160][vcodec^=vp9]/bv*[height<=2160]" -g "URL" | head -1)
AURL=$(yt-dlp --no-playlist -f "ba[ext=m4a]/ba" -g "URL" | head -1)
ffmpeg -ss START -i "$VURL" -ss START -i "$AURL" -t DUR -map 0:v:0 -map 1:a:0 \
  -c:v libx264 -crf 18 -preset medium -g 30 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart out.mp4
```
- `-ss` before `-i` with a re-encode is frame-exact (verified with SSIM 1.000000 against ground truth), gives true 4K
  from VP9 and lands as H.264 that scrubs in Premiere. `yt-dlp --download-sections "*A-B" --force-keyframes-at-cuts` is
  also exact but slow on 4K VP9.
- Verify a cut: extract the clip frame and the source frame at the same time and compare with
  `ffmpeg -i a.png -i b.png -lavfi ssim -f null -` (a true match scores about 0.99, the neighbouring frame about
  0.65-0.75; do not pass `-v error` or the report is hidden).
- YouTube reports `fps=30` for 29.97 videos: always ffprobe `r_frame_rate` before frame math or NLE XML.

## 3. Stock footage and stills
- **Pexels** (free licence, no attribution): www.pexels.com blocks curl, so search in a browser pane:
  `https://www.pexels.com/search/videos/<query>/?orientation=landscape`. Every search page carries `__NEXT_DATA__` JSON
  (`props.pageProps.initialData.data[].attributes`: id, slug, title, size, duration, user, `video.thumbnail.medium`,
  `video.video_files`); from the page you can `fetch()` several queries in one script and parse them. Download with the
  site's own download link from the shell: `curl -L -A "<browser UA>" -o out.mp4 "https://www.pexels.com/download/video/<id>/"`
  (redirects to the largest file, often 4K); `/download/video/<id>/?h=1080&w=1920` gives 1080p. Some files labelled
  1080 are really 720 and some "uhd" are 1440p: ffprobe after download. Skip AI-generated ("aigc") results. Opening a
  single video page triggers an interactive Cloudflare check: never solve it, use search pages (older ids also resolve
  at the `videos.pexels.com` pattern in stills-and-sources.md).
- Pexels photos: the same `__NEXT_DATA__` has image URLs, alt text, slug, user and licence; `?cs=srgb&fm=jpg` with no
  width gives the original.
- **Mixkit**: plain-HTML search pages (`https://mixkit.co/free-stock-video/<query>/`); free files at
  `https://assets.mixkit.co/videos/<id>/<id>-720.mp4` (720p only). A good backup.
- **Pixabay** blocks curl; Unsplash's search API needs auth; Wikimedia Commons is fine for logos and public-domain art
  (check the licence, credit "Photo: Name, CC BY 4.0"); Prelinger and other public-domain archives for old film; NASA
  imagery (Black Marble night Earth) is free.
- Pexels and Pixabay answered scripts with a Cloudflare 403 unless they used the sites' free API keys (the user creates
  his own). Mixkit marks some clips "Restricted" (personal use only), which ruled out most of its Bitcoin, chart, neon
  and named-city clips; it answered 429 once. Coverr's tag pages work without a key (its API needs one; skip its AI
  clips).
- Frame-check every stock clip for faces in focus, logos, sponsor boards, shoe and kit brands, other apps' screens and
  landmarks whose lighting is protected (the Eiffel Tower at night): one pull kept 34 clips (1.25 GB) and rejected 11 of
  45 for exactly these.
- Always look at a contact sheet of thumbnails before downloading or delivering: slugs hide things that are wrong for the
  client (holiday hats, religious symbols, brand names on props). Keep a manifest (file, source URL, licence, where used).
- Check free disk space before big pulls (`df -h /` on a Mac); one contact-sheet loop once filled 48 GB of scratch
  space. Write thumbnails with `-frames:v 1 -update 1` from a Python loop.
- Render SVGs for a contact sheet with headless Chrome (`--headless=new --screenshot` with its own `--user-data-dir`).

## 4. Clean copies of watermarked video memes
When memes arrive as Instagram downloads with a moving "@handle" watermark and a 3 to 4 s outro card:
- Detect the watermark with a Canny-edge template match of the logo on 1 fps frames (watermarked > 0.55, clean < 0.45);
  OCR reads the handle (the "@" comes out as G/C/6/E/B/S), which names the original poster.
- Search the on-screen caption in quotes plus "meme"; the same video is usually on TikTok, Instagram or Facebook.
  Instagram reels download clean with yt-dlp; a clean copy runs 3 to 4 s shorter than the watermarked one.
- Save clean copies under the ORIGINAL file name in a `Clean/` folder (so Premiere can relink), mark the originals
  (Finder tags on a Mac: green = clean copy found, red = not found) and keep a results list.

## 5. Transcription
- Mac: `mlx-whisper` with `mlx-community/whisper-large-v3-turbo` in its own venv
  (`python3 -m venv ~/.venvs/mlx-whisper && ~/.venvs/mlx-whisper/bin/pip install mlx-whisper`); a 45 minute episode
  takes a few minutes on Apple Silicon. The Mac `hear.py` wraps it for word timings in windows. Windows: faster-whisper
  (`hear.py`, timing.md); the lessons below are about Whisper itself and hold for both.
- **Never ask for word timestamps on a full episode**: on a 56 min file they dropped about two thirds of the speech.
  Word timings: re-run only the short window you need. On clips of about a minute (reels) word timestamps are fine.
- **Decode loops**: long or multi-track recordings can fall into a loop ("Yeah." x300) and return garbage for the rest.
  Turn off conditioning on previous text from the start on multi-track recordings (`--condition-on-previous-text False`
  in the CLI), and check words per 5 minutes across the file (a healthy conversation runs about 900-1100); a sudden drop
  means a loop.
- A track that starts with long digital silence makes Whisper emit "Thank you." every 30 s and then nothing: extract the
  audible region and transcribe that alone. Over a closing music tail Whisper invents "Thank you." / "you" / "Amen.":
  strip trailing low-probability words before counting words or pace.
- The mlx_whisper CLI with several input files overwrites its outputs: one file per call.
- Names: Whisper mangles proper nouns and two big models agreeing means nothing. Confirm every name against a source
  outside the audio; re-transcribing a hard 20 s segment at `atempo=0.75` sometimes shakes a better reading loose.
- Multicam or multi-track offsets: band-pass 300-3000 Hz, rectified envelope in 1 ms bins, cross-correlate 40 s windows
  at several points; convert the peak back with the SAME bin size (a bin mismatch once gave a confident wrong offset);
  confirm by transcribing a 20 s clip from each file at the claimed offset. A reconnect file from a call recorder can be
  padded to the session length yet run late: measure it.

## 6. Splitting voice and music, identifying songs
- Demucs two-stem split: `python -m demucs -n htdemucs --two-stems=vocals -d mps -o <out> a.wav` (`-d mps` = the Apple
  GPU: three one-minute tracks in about 18 s; on Windows leave the device to Demucs, not tested here). Install it in a
  throwaway venv with `opencv-python-headless librosa scikit-learn scipy demucs soundfile` (ask first).
- Loudness per stem: `ffmpeg -i stem.wav -af ebur128=peak=true -f null -` or `atools.py`. Beat tracking: run librosa (or
  `beats.py`) on the music stem, not the full mix. Demucs stems of an MP3 run about 23 ms late against an ffmpeg decode
  (encoder delay).
- Song IDs for "Original audio" reels: Shazam on 10 to 12 s windows of the music stem with `shazamio` under Python 3.12
  (`uv run --python 3.12 --with shazamio`; it crashed on 3.14); `matches[0].offset` gives the position in the song.
  Shazam is an outside service: the snippets leave the machine, so ask before sending a client's audio.

## 7. Cuts, OCR, colour and motion measurement
- Cut detection: `ffmpeg -vf "scale=640:-2,scdet=threshold=8,metadata=print:file=x.txt"` scores every frame; hard cuts
  at 10 or more matched contact sheets. For edited reels add a shift-compensated difference (phase correlation, then the
  residual) so page scrolls are not counted and cuts inside insets are found. OpenCV's `phaseCorrelate` modifies its
  inputs in place: pass copies.
- Exact frames: ffmpeg `select='between(n,a,b)'`; OpenCV `CAP_PROP_POS_FRAMES` seeks on H.264 can land one frame off;
  `-ss` returns the first frame at or after the time, so seeking mid-frame silently gives the next frame.
- OCR: Apple Vision on the Mac (`scripts/media/ocr`, accurate mode, word boxes), Windows OCR (`ocr.ps1`); both feed
  `ocrfind.py` (timing.md). A batch Swift OCR tool read 6-7 frames a second per process at 720x1280, so run several
  processes; word-level boxes (for highlights that follow the voice) come from Vision's `boundingBox(for:)` per word.
- Colour sampling from H.264 / ProRes: decode with `scale=in_color_matrix=bt709:in_range=tv`; encode RGB to H.264 with
  `scale=out_color_matrix=bt709:out_range=tv` plus `-colorspace bt709 -color_primaries bt709 -color_trc bt709` (browsers
  otherwise show it slightly green and dark). Add `-map_metadata -1 -write_tmcd 0` to drop a stray timecode track.
  PyAV 19 honours the stream's BT.709 tag (grading.md has the PyAV route).
- Per-shot zoom and pan: ORB features plus `estimateAffinePartial2D` between the third and third-last frame, central 90%.
- Text on screen, measured: OCR frames at 2 fps for the first 8 s, then 1 fps up to 40 s, at 720 px wide; count readable
  words against tiny ones (under 1.8% of the frame height) and where the text sits; cuts per 10 s from ffmpeg scene
  detection at 0.3. It turned "looks designed" into a list of fixes when our posts were compared with references.
- Baked-in letterbox bars: `cropdetect=24:2:0` over 4 s starting 0.5 s after the in-point; apply the crop only when it
  keeps under 92% of the width or height and over 40% (otherwise it is noise or a dark shot); allow forcing a crop
  (`w:h:x:y`) or switching it off per clip. Why: baked bars waste the vertical frame and read as a lazy re-upload. The real picture area inside pillar or letter bars comes from the MEDIAN
  frame of the clip, not from one frame.
- System Python may lack modules; the Mac's Homebrew ffmpeg has no drawtext, so draw labels on contact sheets with PIL.

## 8. Stills of every meme in a compilation video
Compilations reveal each meme by un-blurring it, so a clean still exists only at the END of each meme's time on screen.
Decode once to grey 320x180, compute per-frame mean absolute difference and Laplacian sharpness; real cuts measure 12+
and reveal steps stay under about 2, so segment on a difference over 10; take the sharpest frame in each segment's tail.
Extract by frame number (`select='eq(n\,N)'`, about 20 terms per call), never by timestamp. To crop memes off a white
canvas, use the gradient (the meme border is a sharp step, the drop shadow a smooth ramp), then inset to clear the
shadow. Check the crops on a magenta background before delivering.

## 9. House rules for media jobs
- Download only when the user asks, one download at a time, into the job folder.
- Say what is not cleared (film clips, news footage, commercial songs) and for what use.
- Images the user pastes into the chat mid-task may not be saved to disk; when exact pixels or colours matter, ask for the
  file instead of matching by eye, or say clearly that values were matched by eye.
- Keep every downloaded source with a manifest in the job folder, not in a scratch folder that gets wiped.
- One heavy job at a time (renders, transcription preps, mattes, downloads). A gate that waits for other heavy processes
  must treat a FAILED or EMPTY process query as "busy": a query that came back empty under load let a render start on
  top of a prep. Poll every 20 s and wait for 2 quiet polls in a row. One GPU job at a time too: two matte jobs at once
  competed for a 12 GB card.
- Keep a laptop awake for a long unattended job without changing any setting: on Windows the job's own process calls
  `SetThreadExecutionState(0x80000001)` (ES_CONTINUOUS | ES_SYSTEM_REQUIRED), which blocks idle sleep only while it
  runs (closing the lid still sleeps it); on a Mac run the command under `caffeinate -i`. Mains power: SKILL.md rule 4.
- Key every cache on every parameter that changes the output: a crop-preview cache keyed without its crop centre, scale
  and y offset showed stale crops.
- Any automatic change a tool applies (an auto-crop, an auto-zoom, a "tighten the margins" rule) defaults to doing
  nothing and needs a measured trigger. Why: a meme job's first auto-crop pass changed 74 of 171 memes and drew "an
  overuse of crops"; with named triggers only (UI bars, metadata rows, watermarks, margins of 10% or more) it changed
  19 (meme-compilation-edit house rules).
- Prefix helper outputs (sheets, temp files) with `_` and skip `_` files in globs: an old contact sheet got pulled into
  the next one.
- Footage hygiene before cataloguing: rename files to ASCII (emoji names broke the tools), find the real picture area
  inside pillar or letter bars (section 7), and look for watermarks and burned-in names, scores or "Round 2" bugs;
  crop them out by zoom (about 1.35-1.6x) or frame below them.
- On Windows run any Python that reads downloaded files as `python -I -X utf8`: `-I` ignores PYTHONIOENCODING, and
  `-X utf8` keeps emoji and accented names from crashing print. Tools that live in the user site-packages (torch,
  sam2, faster-whisper, yt-dlp on that PC) cannot run under `-I`: run those without it and keep them away from untrusted
  folders.

## 10. Encoding renders with ffmpeg
- Choose the encoder by a VMAF test against the source on 30 s of real footage (VMAF 95 or more is visually lossless;
  needs an ffmpeg built with libvmaf). One Windows laptop (RTX, 1080p 29.97):

| Encoder | One job | Size | VMAF | Parallel throughput |
|---|---|---|---|---|
| x264 CRF 16, preset fast | 6.6 s | 46 MB | 99.84 | 5.8x real time (4 jobs) |
| NVENC H.264 | 6.0 s | 85.5 MB | 99.87 | 8 to 9.8x (4 to 8 jobs) |
| AMF | 6.7 s | 65.5 MB | 99.83 | not tested |

- NVENC at cq 21 was chosen (cq 19 = 68 MB / 99.867, cq 21 = 54.7 MB / 99.854, cq 23 = 44 MB / 99.75):
  `-c:v h264_nvenc -preset p6 -tune hq -rc vbr -cq 21 -b:v 0 -maxrate 60M -bufsize 120M -profile:v high -spatial-aq 1
  -temporal-aq 1 -rc-lookahead 32 -g 120`. It needs NVIDIA driver 610+ (596 failed): ask the user to update. GPU
  decoding gave no gain.
- Encode parts 3-4 at a time and cache each part under a hash of its exact ffmpeg command plus the input's size and
  modification time, so a fix re-encodes only the clips that changed: a 13:06 cut rendered in 2:08 (about 6x real
  time) and a cached fix took 49 s; CPU renders had taken 10-13 min, about 4x longer on battery.
- Frame exactness: parts as MPEG-TS, not MKV (timing.md); trim each part from (in - 0.5 / fps) with `-frames:v N` so no
  first frame drops; a frame-exact grab seeks a quarter frame in (ffmpeg keeps the frame whose interval contains the
  seek point); pad an insert at another frame rate with `tpad=stop_mode=clone`, then cut it with `-frames:v`.
- On a Mac (untested): no NVENC. Run the same VMAF test with `h264_videotoolbox` against libx264 (check
  `ffmpeg -hide_banner -encoders | grep videotoolbox` and `ffmpeg -hide_banner -filters | grep vmaf` first).
- The batch pipeline built on this (plans, gates, QC, XML): production-automation `render-pipeline.md`.

## 11. Keying and alpha with ffmpeg
- Green screen: `chromakey=0x00FF00:0.16:0.08,despill=type=green`, an optional crop of the figure, scaled to about
  860-900 px tall and overlaid bottom centre with x / y offsets. Key the full width; when a template's figure has a
  straight crop edge, push the figure so that edge sits on the frame edge (one key clipped a shirt, the next showed the
  template's own straight edge).
- Alpha for Premiere from ffmpeg: QuickTime Animation, `-c:v qtrle -pix_fmt argb` (.mov; about 220 MB for a short
  clip), on its own track.
- A screen recording under a card goes on a black background, not on a blurred copy of itself (the blurred fill
  smeared the app's logos).
- Keying in After Effects (Keylight values for 3D renders on green): after-effects.md section 7.

## 12. Subject mattes with SAM 2 (the music-edit kit's route)
- The code: `roto.py CLIP OUT.mp4 [--box | --point]` (with `automatte.py` and `reframe.py` for framing and re-ID) in
  `library/pipelines/edits-kit/tools/`.
- SAM 2.1 large tracks the subject both ways from one prompt frame (a box, a point, or a re-identified person); refine
  the edge with a guided filter (radius = width / 240, eps 2e-3), firm up the core ((a - 0.15) / 0.7), blend over time
  (0.75 / 0.25), write a grey H.264 matte. About 8.5 fps at 1080p on an RTX laptop GPU; hair curls kept. Cache mattes
  keyed by file + range + prompt, so a new hand box really re-runs. Framing and type placement from the matte:
  timing.md music section.
- Install next to an existing PyTorch (ask first: PyTorch + SAM 2 are about 3-4 GB, the model about 900 MB, each user's
  own download): install setuptools, wheel, hydra-core and iopath first, then sam2 with `--no-build-isolation
  --no-deps` and `SAM2_BUILD_CUDA=0`. Plain pip started re-downloading torch (2.7 GB) into an isolated build env. SAM 2
  then skips its fill-holes post-processing with a harmless warning.
- Mac (untested): the kit's tools call `.cuda()` and CUDA autocast: use a device variable ("mps" if available, else
  "cpu"; float16 autocast on MPS, or none). SAM 2 runs on MPS with a "preliminary support" warning and slower: test a
  2 s clip first. The kit encoded mattes with `h264_nvenc` and no fallback: use `h264_videotoolbox` or libx264 (CRF
  12-14).
- Try the apps' own one-click mattes first (After Effects Object Matte, Premiere Object Mask: after-effects.md
  section 7).

## 13. Tracking without Mocha
- Mocha AE ships with After Effects 2026 (after-effects.md section 7): check it first, and the user may prefer to do a
  planar track himself.
- A numpy + PIL tracker that scored 0.92-0.99 on a handheld whiteboard: inverse-compositional affine Lucas-Kanade on a
  3-level pyramid, textured pixels only (gradient above the 35th percentile), Tukey-weighted residuals, hands masked out
  of the template. At the start of each jump-cut piece, a global search over rotation (-24 to +24 deg in 2 deg steps)
  x scale (0.88-1.12) by FFT normalised cross-correlation at 1/4 resolution, then refine. A QA sheet with the tracked
  boxes warped in.
- Into sequence space: multiply by the analysis scale and the clip's Motion scale (K = 4 x 0.57 for a quarter-size
  analysis of a clip at 57% scale) and smooth in 2 passes. Frames from ffmpeg, or from After Effects as a fallback
  (after-effects.md section 3). Writing it into Premiere masks: prproj-recipes R21; overlays that follow it:
  after-effects.md section 7.

## 14. Reading documents (PDF highlights and notes)
- An annotated script often arrives as a PDF. A small dependency-free reader can walk the PDF objects and return each
  highlight with the text under it, the sticky notes and the page text in reading order; that works on
  uncompressed-xref PDFs (Chrome / Skia exports). One read 24 highlights and 1 sticky note on a machine with no PDF
  renderer installed. Write it as plain Python (no libraries needed). For compressed PDFs use a PDF skill if
  one is installed.
- Notes inside a script addressed to Claude are tasks: own them and confirm them. A link Claude cannot open (a Drive link
  in a sticky note): say so and ask for the file in the job folder.
