# Words, timing and cut points

## Getting word timings (best first)
1. Premiere's own transcript inside the project: `python scripts/prproj/prtranscript.py X.prproj words.json` (words
   with start / duration / confidence per transcript, owning media title). Use these over exported CSVs.
2. Local Whisper, nothing leaves the machine. Both versions write the same JSON: {"file", "duration", "segments":
   [{"s","e","text"}], "words": [{"s","e","w","p"}]}.
   - Windows: `python scripts/media/hear.py media.wav out.json [vocab.txt] [model]` (faster-whisper large-v3-turbo,
     CPU int8, about 2.5 min per 12 min of audio). vocab.txt = names it must spell (used as hotwords on every window).
     `large-v3` = slower, tighter word times. A 16 kHz mono 16-bit WAV loads directly; everything else, including
     32-bit float WAVs straight from a DAW, is decoded through PyAV (float WAVs crashed with `wave.Error: unknown
     format: 3` before 14 Oct 2026).
   - Mac (from the Mac port): `~/.venvs/mlx-whisper/bin/python scripts/media/hear.py media.wav out.json [--vocab
     names.txt] [--model turbo|large-v3] [--from S --to S]` (mlx-whisper on the Apple GPU; a 4 s test took 2 s).
     Times stay in the full file's seconds even for a window. mlx-whisper has no hotwords, so `--vocab` goes in as the
     initial prompt, which once hallucinated names into the first seconds: check the opening words. After each run it
     prints words per 5 minutes (a healthy talking track runs about 900-1100; a sudden drop is a decode loop, not
     silence) and flags a short segment repeated 8+ times in a row. The first run downloads the model (about 1.6 GB);
     without mlx-whisper (an Intel Mac, or the venv missing) it falls back to faster-whisper with the Windows
     positional form only. Plain transcripts of whole episodes: the mlx_whisper CLI without word timestamps
     (media-toolkit.md section 5).
3. Offline Windows speech: `powershell -File scripts/media/sapi_words.ps1 in.wav out.tsv` (word-level absolute times,
   rougher; fine for a script-aligned voice-over). No Mac equivalent: use a `hear.py` window.
- Captions or transcripts: Premiere's transcripts are made on the SOURCE and can be older than the current cut. When
  they are, use the caption track as the timed script, and the transcript only where a piece has no captions.
- A new voice file in a project (a CTA read): Premiere's Text panel > Transcribe on that clip, save, then decode its
  TranscriptData blob (`prtranscript.py`; find the blob that holds a word you know). Premiere heard a brand name as
  another word ("fix"): type brand names correctly on screen whatever the transcript says.

## Script to voice: timing cues from an annotated script
- Extract the script text; tokenise its words and `[bracket cues]` per section; align the script words to the
  recognised voice words with `difflib.SequenceMatcher(autojunk=False)`; fill unmatched words from the previous match;
  give each cue the start of the next voice beat; print a beat sheet (file, start, end, text). Why: the script says
  WHAT, the recording says WHEN (ad-libs and pauses move everything). Every block of one 10-minute video was timed this
  way (11 voice files of 80-211 words).
- Read the PDF highlights and sticky notes of an annotated script as well (media-toolkit.md section 14); the Word copy
  may carry no comments, so ask which file is the annotated one.

## Lessons
- Whisper word STARTS land 0.1-1.0 s early or late (often inside the pause before the word). Cuts placed on raw times
  looked "not cut properly and not synced". Take every edge from the audio with `scripts/media/speech_cuts.py`
  ("Cut edges from the audio" below), and spot-check a few by ear or by drawing the envelope + words + cut line.
- turbo dropped whole lines once; a names list as initial prompt hallucinated the names into the first seconds. Settle
  disputed bits by re-transcribing just that window with large-v3. Keep a hand-checked fix list ("heard => right") and
  regenerate the transcript from it.
- Long files: get word timings window by window (`--from/--to` on the Mac `hear.py`): word timestamps on a whole long
  episode dropped about two thirds of the speech once. Names: confirm them against a source outside the audio (two
  models agreeing means nothing).
- Take phrase edges from the audio, never from Whisper word times (11 Oct 2026, meme edits on the Mac): a cap on long
  last words dropped the "-to" of "incognito", and Whisper squeezed a whole clause into one stretched word. Inside the
  last word a bump after a short silence is the final consonant release ("stan-d"); only a soft bump (under -55 dB)
  after the words is a breath. Before building, scan every cut for an edge where the audio is louder than -55 dB on
  both sides; there should be none (`speech_cuts.py --scan`).
- The user wants the presenter's REAL words (ad-libs included), never the script document's wording.
- Map review timecodes from a review tool to the edit with the offset you measured once (Frame.io time = A-roll + 8:08.5
  on one job); find a picture-in-picture source offset by audio cross-correlation.

## Cut edges from the audio (speech_cuts.py, 14 Oct 2026)
Levels are dBFS RMS in 10 ms windows of the LOUDEST channel of the RAW file, before any clip gain (a voice recorded on
one side reads 6 dB low in a mono mix). How tight to cut and why: editing-playbook `cutting-and-pacing.md` sections 4-5.
- Default = ABSOLUTE levels, the clean voice-over rules measured on a reviewer's own fixes of a quiet narrator
  recording: a word's soft tail and onset run down to -70 dB (room noise at about -72 to -80 dB is dead air); the in
  point sits 1-2 frames before the first frame at -70 dB or louder (a soft "s" rising out of the floor stays); the out
  point about 3 frames after the last one (at most 5), stopping short of any new sound; a bump after a short silence
  INSIDE the last word is its final consonant ("stan-d") and stays; a separate soft bump (peak under -55 dB) after a
  50 ms dip OUTSIDE the words is a breath and is cut at both ends, even at -58 to -70 dB (with no transcript it is kept
  and flagged, since it may be a consonant). Loud sounds are never cut by rule; a short loud one outside the words is
  flagged as a possible click. A sound joined to a breath or the next word by a dip that never reaches -70 dB is cut
  at the dip's quietest point.
- Edge scan: no cut edge may have audio over -55 dB on BOTH sides (that edge chops a sound). It measures the 80 ms
  that a cut drops and the 50 ms it keeps on each side of an edge; a seamless join (out == next in) is not an edge.
  `--scan`, `--keep` and `--phrases` exit with code 1 when it finds one.
- Restart flags: a phrase that begins like the one before ("Gen Z won't- Gen Z won't"), a word or run of up to 4 words
  said twice back to back, cut-off words (a trailing dash, or a 4+ letter word that starts the next one), words
  stretched over 0.8 s, speech with no transcript words, and transcript words with no sound under them. A whole-file
  transcript merges restarts: on narrator recordings transcribe each piece on its own (`--wav-dir`); per-piece
  transcripts are mandatory there.
- A per-piece transcript can invent words on a breath (Whisper heard a breath-only piece as "Thank you."): the tool
  flags a piece that never reaches -55 dB as "soft sound only: breath or noise, cut" whatever its transcript says.
- Why these rules: on three raw voice takes (room floors -72 to -78 dB) every edge the tool gave was clean, while the
  raw Whisper sentence edges used directly as cuts chopped 1, 5 and 8 edges. The -70 / -55 levels came from another
  editor's tool whose meter was not shipped, so the scale here (RMS per 10 ms) is an assumption that fit those takes:
  tune with `--edge` / `--loud` and check a few edges by ear on a new microphone or room (tentative).
- `--rel` = the older RELATIVE rule, for noisy field audio (street, events, handheld recordings) whose floor sits far above -70 dB:
  the snap modes then give exactly the old output (a pause = 80 ms quieter than the local floor + 10 dB, cut 50 ms
  before speech resumes), and the voice-over modes measure from the recording's own floor (edge = floor + 10 dB, the
  other levels keep their spacing). Warnings (on stderr): the room floor above -65 dB ("use --rel"); the floor within
  2 dB of the edge level (many cuts will land in dips; `--rel` may suit better); speech under about -45 dB (very
  quiet: check flagged breaths by ear).
- Commands:
  - `python scripts/media/speech_cuts.py MEDIA WORDS.json "phrase@after" ...`: the cut where the sentence starting with
    that phrase begins, searched from `after` seconds on (absolute: the next speech after a real pause, breaths
    skipped, 1.5 frames before its first sound). `MEDIA --at 12.4 15.9`: snap raw times.
  - `MEDIA --keep 12.0-15.5 20.1-24.0 [--words WORDS.json]`: clean in / out (seconds and frames) for the phrases you
    keep. With the words file (also accepted before `--keep`) each range is read through its own words: the sound
    pieces holding them are kept whole, even past the range when Whisper ends a phrase early; edge pieces holding only
    another phrase's words, a breath or a click are left out (and named in the notes); with no pause between two
    phrases it cuts at the quietest point between their boundary words. Without words the range is used as given,
    with a note when loud sound sits within 0.3 s outside it.
  - `MEDIA --scan 12.03-15.63 ...` or `--scan CUTS.json`: the edge scan of a cut list in source seconds (CUTS.json =
    `[[in, out], ...]`, `[{"in": s, "out": s}, ...]`, or the `--json` output of `--keep` / `--phrases`).
  - `MEDIA [WORDS.json] --phrases [--wav-dir DIR]`: the whole recording as phrase pieces (split where nothing reaches
    -60 dB for over 0.20 s or it stays under -62 dB for 0.18 s; pieces under 0.08 s, clicks, are dropped), each with
    clean in / out, its words, flags and the scan of its own edges. With `--wav-dir` it writes each piece as a 16 kHz
    mono WAV (0.5 s of silence each side) and prints a `for f in DIR/*.wav; do python hear.py "$f" "${f%.wav}.json";
    done` loop (on a Mac run it with the mlx-whisper venv's python); run `--phrases` again with the same DIR and the
    restart checks use each piece's own transcript.
  - Options: `--fps 30` (the frame grid for in / out), `--edge -70`, `--loud -55` (override the levels), `--json
    OUT.json` (`--keep`, `--phrases`). No arguments or `--help` prints the usage.
- WORDS.json = `hear.py` output (`{"words": [{"s", "e", "w", "p"}]}`); times are seconds in the media file.

## Timing rules for edits
- Picture changes on the word they illustrate; pose swaps 2 frames before the word; titles out before the next cut.
- SFX transient on the frame (or 1 frame late), never early.
- Time maps: keep a per-block offset (voice file time -> sequence time) in the generator, e.g. `V3 = lambda f: f + 42.68`,
  so every graphic time is "word time in file + offset".

## OCR (where to put highlights and zooms)
1. Windows: `powershell -File scripts/media/ocr.ps1 ocr.json shot1.png shot2.png ...` (Windows built-in OCR, word
   boxes in px; needs absolute image paths). Mac: `scripts/media/ocr ocr.json shot1.png shot2.png ...` (Apple Vision,
   accurate mode, word boxes in px with a top-left origin, the same JSON; build it once with swiftc, SKILL.md). Symbols
   read badly on the Mac (a check mark came back as "J").
2. `python scripts/media/ocrfind.py ocr.json shot1.png "exact phrase"` -> one rect per text line (+ score / of). The
   phrase must be contiguous words as OCR read them; check score == of before trusting the rects.
3. Feed rects to `highlighter` / `outlineBox` / zoom targets in the AE generator (imgCard ox / oy maps them).

## Seeing footage without watching it
- `python scripts/media/frames.py info FILE` (codec, size, fps, frames, audio), `sheet` (frames at exact times with
  labels), `even` (N evenly spaced frames per file, a quick catalog of renders or B-roll), `grab`, `dupes`.
- Score frames numerically first when choosing B-roll (sharpness, motion, colour stats) and only sheet the shortlist.
- ffmpeg: on the Windows PC 9.0.2 since Oct 2026 (winget Gyan.FFmpeg, on PATH), on the Mac 8 from Homebrew (no
  drawtext, no soxr). Use it for audio extraction, piped low-res frames (motion maps) and contact sheets. PyAV
  (`import av`) still works for exact seeks. For exact frame N use ffmpeg `select='between(n,a,b)'` (OpenCV seeks can
  land one frame off); cut detection: ffmpeg `scdet` (media-toolkit.md section 7).
- VLC is only a last resort: its seeking is unreliable (`--start-time` returned wrong frames, `--stop-time` can hang),
  hardware decoding must be off for its scene filter (`--avcodec-hw=none`), and its frame dumps come out padded
  (1080x1920 as 1088x1922, 6048x3408 as 6048x3426). WAV out (Windows, before ffmpeg was installed): `--no-video
  --sout=#transcode{acodec=s16l,channels=2,samplerate=48000}:std{access=file,mux=wav,dst=...}`; its sout parser eats
  backslashes (give dst relative or with forward slashes); frame grabs returned 0 frames with mixed slashes or a
  relative scene path (use absolute paths); VLC grabs drop alpha (overlays showed black backgrounds).
- Keep a combined contact sheet readable: a 1400 x 3400 stack was "too tall to read in one go"; split it by question
  (the 6 formats that mattered went into 2 images).
- A reference edit's cut points, cheaply: the mean absolute difference of 54x96 grey frames per frame, with a
  timestamped sheet around each cut; ffmpeg `scdet` scores (media-toolkit.md section 7) are the finer route.

## Long raw footage (field recordings), learned 11 Oct 2026
The steps behind this section (prep, subtitle reading and alignment, the snap audit, seam checks, the renderer) are
laid out as one pipeline in production-automation `cutdown-batch-pipeline.md`; those tools are not part of the kit.
The two edge checks are this skill's own (`edge_shots.py`, `edge_words.py`).
- GPU Whisper on a Windows PC with an NVIDIA card: `pip install nvidia-cublas-cu12 "nvidia-cudnn-cu12==9.*"`, then `os.add_dll_directory()` + PATH
  for `site-packages/nvidia/{cublas,cudnn}/bin` before importing faster_whisper (else "cublas64_12.dll not found").
  PyAV 19 breaks faster-whisper's own file decoder (`metadata_errors`): pass a float32 16 kHz numpy array instead.
  `BatchedInferencePipeline` (float16, batch 16, word_timestamps) ran 25-40x real time; the sequential decoder 3-5x
  when the CPU was busy. INT8 is unsupported on RTX 50 (sm_120): use float16.
- Read before you look: a one-line-per-utterance "screenplay" (time, words, flags for loud transients, motion, shot
  changes, "no speech" gaps) tells the story of 13 min in ~200 lines; then ONE labelled sheet of only the no-speech
  windows answers what speech cannot (travel, loud moments, map inserts, approaches).
- Snapping cuts: a point further than ~0.35 s from any word is in a no-speech stretch and must stay where the editor
  put it (only step off a loud hit onto the quietest 10 ms). Dragging it to the nearest word silently deleted 60 s of
  action once. Clamp envelope windows to the file: a negative end index slices almost the whole array in numpy.
  Overlapping speakers (narrator over dialogue) have no clean cut point: keep the stretch whole instead.
- The user's measured cut padding (11 cutdowns of long footage): out point a median 0.29 s after the last kept word (middle
  half 0.19-0.56 s), lead-in a median 0.5 s before the next word. Plain Whisper word edges are only about +-150 ms, so
  "inside a word" audits are noisy; WhisperX alignment (~35 ms) is the upgrade.
- Grade an automatic cut against the editor's real one (kept-time precision / recall per source second) and read
  the biggest disagreements with their words: the fastest way to learn their taste and to catch tool bugs.
- YouTube "Most replayed": `yt-dlp -J --skip-download URL` returns `heatmap` (100 slices, value 0-1), about 45 s per
  video, nothing downloaded. A channel's own hook picks sat at the 95th percentile of it: use the peaks as hook candidates.
- Channel outliers: score = views / median views of the ~15 videos either side in upload order (yt-dlp --flat-playlist
  -J gives views + durations fast); 3x+ is a clear outlier; aggregate by title word and length band.
- Burned-in captions: a pixel is caption if bright AND unchanged across neighbouring frames; OCR each caption once from
  the per-pixel minimum of 3 frames. Windows OCR (ocr.ps1) needs absolute image paths; if PowerShell refuses the script,
  call it as `powershell -ExecutionPolicy Bypass -File scripts/media/ocr.ps1 ...`, which applies to that one process
  and changes no system setting. Read rate was about 1/3 of spans, so treat captions as a supplement (their
  [sound-effect]-style tags still mark action).
- Probe every video's frame rate; never assume one (two tools assumed 60 fps on 29.97 sources).
- Audit thresholds that held on noisy field audio: a censor mute = 5 or more consecutive 10 ms frames under -90 dBFS
  inside speech (FAIL any cut inside or just before it); no cut within +-0.12 s of a loud transient (a bang); no clip
  under 0.5 s; no edge inside a caption.
- Keep a backup of every word file before a re-alignment pass: one pairing step lost 1,552 of 1,711 words and wrote
  over the file.
- QC false alarms to expect (each long cut gave 5-12 flash flags, nearly all false): the flash detector fires on white
  dips, narrator fade-outs, rain and flashing lights (1-2 frame "switches"), the source's own subtitle blinks in fast
  motion, an insert's own animation and coloured subtitles; the stray-shot check also fires on flashing lights changing
  colour. A seam check should skip white-dip seams (both sides' mean over 200) and soft seams (change under 8). Judge
  every flag on frame-exact sheets.
- Transcript choice (11 Oct, noisy field audio with crackly sources): faster-whisper's BatchedInferencePipeline made 63 s segments and
  drifted 5-14 s on quiet crackly lines, and aligning words inside a wrong segment window cannot fix that. The full
  WhisperX pipeline (VAD-cut chunks of 30 s max + wav2vec2 alignment, own venv with torch cu128) matched the burned-in
  captions. Do not use its suppress_numerals (it looped "." tokens over a number followed by a unit); fill untimed numerals from neighbours.
  WhisperX can still stretch one word across speech it missed (a 3.7 s "with"): captions and shot changes win.
- Burned-in captions also recover lines both ASRs miss (shouted lines, crackly audio): treat every caption span as speech
  that a cut must not split (a subtitle cut mid-display looks broken), and never let an out point run into the next
  caption.
- Write cut points as anchors, not seconds: words ("end after 'I heard two'"), a caption's start or end, or an explicit
  hold time where words are unreliable. Times written against one transcript slipped onto neighbouring words ("I was",
  "I'm") as soon as a better transcript replaced it.
- A cut that touches a word keeps the whole word. Dropping half-touched words clipped the last word of two lines. When the next speaker overlaps, cut exactly on the word end.
- The seam report (last words before and first words after every cut) doubles as the review cut list and catches every
  clipped sentence. Audit flags inside noisy audio are often ASR mis-timing: confirm each one against captions/frames.
- Rendering (Windows, NVIDIA): ffmpeg 9.0.2's h264_nvenc needs NVIDIA driver 610+ (596 failed): ask the user to update, use libx264 meanwhile.
- Subtitle OCR, round 2 (same day): threshold WHITE pixels (all three channels > 185), not bright ones (max channel):
  on a bold outlined font the bright mask fattens letters into blobs and Windows OCR returns nothing (white-only read
  13 of 14 such lines; over whole sources the read rate went from 48% to 91%). Find subtitle switches frame-exactly and
  count a span only when it lasts 3 frames or more. Keep a bright-mask reading too for red/coloured highlight words and take the more word-like
  text. Coloured speaker subtitles (red speaker, pink speaker) still fail: crop the subtitle band of every unread span
  into one labelled strip and read it by eye (40 lines in one image).
- Subtitle edges are not always speech or picture edges: (1) voices run a few frames past their subtitle, so an out on
  a subtitle end may stretch to the word end, but only while the subtitle band stays unchanged; (2) narrator lines
  CROSS-FADE into the next over 7-12 frames with per-frame changes too small for a switch detector, so the detector
  marks the next camera cut instead and 2 frames of the next line show: cut at the first frame of the fade; (3) a
  subtitle edge can sit 1-3 frames after a camera switch, leaving a stray shot: check for a camera switch within 5
  frames of every cut and move the cut onto it. Narrator lines that blur in show one faint frame before any
  mask-based detector reacts: end one frame before the detected fade start, and confirm on frame-exact grabs. Camera switches: consecutive-frame correlation under 0.5 AND mean
  difference over 20 levels (64x36 grey); fast camera motion stays at 0.7-0.9, and 30 fps footage doubled to 60 fps
  makes every other difference 0, which breaks median-based spike tests.
- WhisperX junk: on crackly audio and shouting it smears single "words" over 2-8 s and can drift ~10-14 s in chaotic stretches
  (a speaker's line placed 14 s before its subtitle). Ignore words longer than 1.2 s and trust the subtitles there.
- Joining rendered parts: use MPEG-TS (90 kHz clock = exactly 1500 ticks a frame at 60 fps), not MKV (1 ms clock):
  MKV parts gave the joined MP4 timestamps 1-8 ms off the frame grid, and a frame-exact QC grab (seek a quarter frame
  in) then landed on the neighbouring frame and faked flashes. QC grabs: -copyts and select the frame whose timestamp
  is within half a frame of the target.
- Subtitle-guided word timings (12 Oct): force-align each burned-in subtitle's exact text (wav2vec2) inside its own
  window (0.3 s before to 0.8 s after the subtitle) and use those words wherever a subtitle exists; ASR words only fill
  the gaps. ASR had put a narrator's last words 7 s early, so a cut on the subtitle's end clipped "nearby" and no check
  could see it. Two traps: the early window lets a line's first word land on the previous line's tail (clamp: a new
  line never starts before the previous line's last word ends), and OCR junk text aligns to junk (skip those lines).
- Split edits (L-cuts) solve "the picture must stop here but the word isn't finished" (next subtitle fading in, a
  camera switch): end the picture where it must and let the sound run on under the next shot until the word ends
  (cap ~0.35 s). Carry only words of the line being cut, never the start of the next line (a tail once carried "Com-").
- Stray shots: a camera switch within HALF A SECOND of a clip edge leaves a flash of another angle (9 frames read as
  "a random frame" to the client). Move the cut onto the switch unless words would be lost; at an out, words that end
  within the split-edit cap go into the sound tail.
- Dead beats: list stretches inside each kept clip with no words and no subtitle, with picture motion; low motion =
  cut it, high motion = usually action (a sudden move), keep it.
- Subtitle-edge in-points that reach back for an early first word must check the pixels (12 Oct): OCR span ends run
  early in heavy motion, so the old line flashed for 5 frames. Burned-in subtitles are white text with a dark outline:
  a share of white-next-to-dark pixels in the subtitle band above about 1.3% means a line is still on screen.
- On-screen graphics with state (an item counter, a score, a list) must stay in order across cuts: scan that corner of
  the frame over the whole source with a cheap crop strip before locking the cut, and add back short beats if needed.
- Verify a render by decoding it front to back (frame index = position). Seek-based grabs landed one frame off on a
  GPU encode with B-frames, and a container's average frame rate (frames / duration) read 29.974 for a 29.970 file,
  which drifted planned frames by 3 over 13 minutes: use the stream's nominal rate.
- An insert at another frame rate (25 fps into 29.97) can come up one frame short of its slot: pad it with its last
  frame (tpad clone) and cut to the slot length, or every later clip slips against the sound.
- Censored footage (13 Oct): broadcasters bleep swears by muting about 0.2 s INSIDE the word (digital silence,
  -120 dBFS). A short run of digital silence during a line is part of a word, never a pause: no cut inside or just
  before it, or the word ends mid-way ("motherf-").
- Subtitle end edges linger 0.5-1 s after the speech. For tight cuts (shorts, hooks) end about 0.2 s after the last
  word and start on the first word; keep subtitle edges for relaxed long-form cuts. Yelled lines get their subtitle
  late: check the loudness before trusting the subtitle's in-edge.
- Several mics or devices carry the same line 2-3 times (live, then rebroadcast), each subtitled. Keep the first copy and
  cut the repeats; a repeat later on can finish a sentence across a time jump.
- Never let a camera-switch rule move a cut into speech: finishing the line beats a clean switch.
- Two-line subtitles (13 Oct): OCR often reads one line, so subtitle-aligned words cover only part of the time the
  subtitle is on screen and the rest looks like a pause. A word-tight cut there chopped a narrator mid-sentence. Before
  cutting inside a subtitle, compare its screen time with its words; a long wordless stretch means unread speech.
- Overlapping speakers: a subtitle's end edge can land inside the next speaker's first word ("STOP! Ge-").
  End tight beats on the last word's end checked against the loudness, not on the subtitle edge.
- An in-point a few frames before a subtitle switch flashes the previous line: start at or after the switch.
- Forced alignment skips digits ("over 80 items"): the words after a number get placed early, so a word-tight out
  cuts the last word. On lines with numbers, end on the subtitle's end edge or on the loudness (13 Oct).
- A phrase repeated by the same voice within about a second ("wait, wait... wait!") is one
  sentence, not an echo; cutting between the repeats sounds mid-sentence. A subtitle ending in a comma means the
  sentence goes on.

## Music edits: beats, sync and frame-level review (13 Oct 2026)
The music-edit kit that does this end to end (anatomy, hit snapping and the sync report, mattes, framing previews, the
layered AE build) ships in `library/pipelines/edits-kit/tools/`; what each tool does: motion-design
`cracked-edits.md` section 18 and production-automation `music-edit-builds.md`.
- Hits: `ffmpeg -i edit.mp4 -ac 1 -ar 22050 a.wav`, then `beats.py a.wav hits.json 30`: band-split spectral flux gives
  kicks (30-150 Hz), snares (1.5-6 kHz), hats (6-11 kHz) and onsets, plus tempo, a beat grid and loudness per video
  frame (the drop shows as a jump of 10+ dB). Half-time tracks read as double tempo; check by ear.
- Beat arithmetic: frames per beat = 60 / BPM x fps (150 BPM at 30 fps = 12 frames, a 16th note = 3 frames; a slowed
  70 BPM = 25.7 frames). Tempo detectors read half or double time (one song measured 138, 94 and 70 BPM in different
  runs; its map said 69.5 half-time): trust the kick / snare list over the BPM.
- Two snaps, two purposes: cuts go on the strongest hit near the plan (below); titles and lyric words go on their
  sung word's time floored to a frame (Whisper words of the song). Put a transition's PEAK on the hit
  (transitions.md, method step 5).
- Sync audit: count cuts within 1.5 frames of a kick, snare or onset (about 65% on a good hand-cut edit). Put visual
  hits on the beat or 1 frame early, never late: viewers notice sound arriving early at about 45 ms but tolerate
  picture arriving early up to about 125 ms (ITU-R BT.1359).
- Edits hide 1-frame events (strobes, flash frames, inserts): review EVERY frame with `fsheet.py` (60 frames per
  sheet at 108 px wide), not one frame per second, and crop 100% patches to see texture passes (wave warp, grain).
- Many versions of one render: diff small per-frame thumbnails against v1 and list the frame ranges that differ; often
  all versions match except one short window, so only that window needs a side-by-side look.
- Read the effect stack from the .prproj dump too: nests named "Nested Sequence N" hide the strobes and transition
  presets (e.g. 1-frame copies with a mask + glow + blend mode, Transform + 4x Mirror + Transform zoom stacks).
- A cut or mid-video insert placed on a scene change can still split a narrator sentence that runs ACROSS the change
  (13 Oct: "Now that it's confirmed that the man | was telling the truth"). Read the ASR segment text at every
  insert point and move the insert into a real pause before the sentence.
- Where OCR misses coloured speaker boxes, the ASR-only lines can be hallucinated: a later line showed up 6 s
  early over a different speaker. Grab frames before trusting ASR-only stretches at a cut.
- Pre-render stray-frame check: `scripts/media/edge_shots.py VIDEO EDL.json --fps N` finds the exact camera-cut frames
  within 0.4 s of every clip edge and flags edges that leave 1-4 frames of another shot (decodes only 0.8 s per edge).

### Cutting and framing a music edit by script (learned on the first scripted edit, 13 Oct 2026)
- Cut on the strongest hit near each planned cut, not on a fixed beat grid: a real performance drifts (snares here
  swung up to 0.15 s off the median grid) and the loudest hits are uneven. Score every kick/snare within +-0.2 s as
  strength x (1 - 0.5 x distance / 0.2), take the best, then FLOOR to a frame so the cut lands 0-1 frame early. A
  fixed grid got 31% of cuts on strong hits (chance was 27%); this got 25 of 26.
- Report sync before rendering (it costs nothing): for each cut, the strongest hit 0-1.5 frames after it. A weak
  "nearest hit" in a plain nearest search hides a strong one 1 frame later.
- Frame 9:16 crops from a matte of the subject, not from a person-detector box. Box trackers jump to whoever is
  largest (a defender, a sliding keeper); a SAM 2 matte of the right player gives a steady point (centre of the top
  45% of the shape = head and shoulders) and doubles as the shape for type-behind, outlines, strobes, colour pops.
- Prompt the matte where the subject is clearest (mid-range by default) and track both ways. Clamp every matte or
  tracking range to the shot's own start/end: padding that reaches into the next shot prompted SAM 2 on a different
  picture twice (subject "found" in 3 of 125 frames). A sanity line per matte ("found in N of M frames, mean area")
  catches it.
- Auto prompts still pick the wrong person sometimes (a keeper sliding in front is the largest body): check, then
  give a hand box at a named time; make the hand prompt part of the cache key so a new box really re-runs.
- Score footage for subject presence before choosing shots: detect people on 4 frames per shot and re-ID them
  against a gallery of the subject. About a third of a fan pack's "action" shots had him hidden or tiny.
- Preview framing without rendering: crop each clip at start/middle/end exactly as the comp will (cover scale x zoom,
  anchor = focus, clamped), tint the matte, draw type boxes and the 10%/76% safe lines. One sheet caught type over
  the eyes, a slow-mo shot losing its ball halfway and a clip framed on the keeper, all before a render.
- 1080p broadcast wide shots: the player is about 10% of the frame height. Past about 1.8x zoom it turns soft; zoom
  moderately and MARK him instead (a lock-on ring at the moment that matters).
- Look at the frames on both sides of every WHITE transition seam (dip, scene flash, insert in/out): the automatic
  flash check cannot see through the fade, and 4 of 4 real misses in one round hid there or at hook edges (the next
  line's subtitle for 2 frames before a dip, an old "Okay." for 5 frames at a hook in-point). Find the true switch
  frame with a per-frame difference scan of the subtitle band; animated subtitles start blurring in 4-5 frames
  before the OCR start time.
- Compilation channels splice in footage from ANOTHER of their videos when the narrator says "featured in a
  different video of ours": a different on-screen source ID and date stamp, a channel label, a thumbnail inset. Cut the
  narrator line AND the borrowed clip; a matching line ("you saved my life") made the borrowed clip look like ours.
- Endings: end on the section's last downbeat (the bar line) and hold an end card for one more bar while the music
  plays on, fading the last 0.6 s. Stopping 0.1 s after the next section's first downbeat felt "cut off" to the user.
- Lay type out with REAL font metrics (PIL ImageFont on the same font file AE uses, found by PostScript name): a
  condensed face (Coolvetica Heavy Compressed) is about 0.4 em per letter, a wide black face (Galano Grotesque Black)
  about 0.6; a guessed width put words on top of each other. Capitals rise about 0.67 x size above the baseline.
- Place type from the subject, not from a guess: map his matte's head point through the clip's scale, anchor and clamp
  to comp pixels. "Number behind his head" reads best with the glyphs' centre near the top of his head, so the tops of
  all digits show and his head covers only the lower middle.
- Measuring letterboxed edits: find the bars from the MEDIAN frame (type in a bar for 10-15% of the time made a 95th
  percentile test call the bar picture), and measure brightness inside the picture only, or every dark shot reads as
  a black frame.
- Check every clip edge against the RAW speech-recogniser words, not only the subtitle-aligned ones (14 Oct, four real
  clipped endings in one batch). Where the OCR
  read only part of a subtitle, or garbled it, the aligned words are squeezed into the wrong span and an edge that
  looks clean in them cuts a live word. `scripts/media/edge_words.py CUT.txt PREPDIR` lists the subtitle, words and
  pauses at every edge and flags "CUT INSIDE A WORD (raw ASR)"; ignore raw words over 1 s (smeared shouting).
- Subtitles can LEAD the voice by 0.2-0.4 s (the next line appears as the current word ends), so no frame-exact out
  shows the right subtitle. End the clip on an earlier sentence that has a real pause after it, or keep going to the
  next such pause; a split edit only works when the next clip starts on silence.
- Plain (snapped) edge times on narration whose subtitles were half-read can snap into the middle of the sentence
  (an out moved 2.6 s early). Pin narrator edges with exact times taken from the raw words.
- In slow comedy sequences the quiet stretch IS the content: keep shots where the subject is visible, cut only empty
  stretches. Cutting all "dead air" left a 56% cut with no joke.
- Compilations (best-knockouts reels, scene packs) hide cuts inside long "shots": replays, angle changes and
  pillarboxed 4:3 footage defeat the shot detector. Run a cut check on every source range you use, and look at a
  frame sheet around each key moment (a knockdown can be a cut to a different angle 2 frames after the punch).
- Burned-in captions in compilations (fighter names, scores) sit in the corners of the 4:3 picture: about 1.25x zoom
  on a 1080x800 band crops them out.
- Drum-hit strength is relative to the loudest hit in the whole song: in quiet sections (an intro beat before a
  switch) every hit reads "weak", so judge sync there by distance to the nearest detected hit, not by strength. A sync
  report that counts only hits of strength 0.5 or more then fails a song with a big level jump: one plan showed 5 of 19
  cuts "on a strong hit", all just after the beat-switch drop (strength 0.68-1.00), while most other cuts sat within
  1 frame of hits of strength 0.13-0.35. Fix (not built yet): normalise strength per loudness section, or per 4 bars,
  before snapping and reporting.
