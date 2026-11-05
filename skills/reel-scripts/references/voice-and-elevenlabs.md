# Voice-overs: ElevenLabs reads and consented voice clones

## House rules first (ours)
- API keys live only in environment variables the user sets. Never view, print, paste or store a key.
- Check the client's file before generating any voice: some clients want no AI voice at all, or none in certain formats.
- One heavy model process at a time. If the user says other heavy apps are running, prepare everything and wait for
  their go before generating.

## ElevenLabs v3 paste blocks
- **One or two audio tags per read, at most.** A block with a tag on almost every line ([slowly], [pause], [long pause],
  [exhales], [quietly], [whispers]) was rejected with "dont use this many tags"; the accepted version used only
  [long pause] before the turn and [whispers] on the last clause. Heavy tagging sounds over-directed and is hard for the
  user to scan and tweak.
- Pace with punctuation instead: ellipses slow a phrase, line breaks and blank lines make the pauses.
- Tags that behave reliably when you do use one: `[long pause]` (the weight before a turn), `[whispers]` (the last
  clause only), `[exhales]` (before something hard; easy to overuse), `[quietly]` / `[softly]`, `[slowly]`, and a
  register tag such as `[somber]` once at the top. If a voice over-acts, remove `[exhales]` first.
- Stability around 60 to 70 for emotional reads (lower wanders between takes, higher goes flat). Generate four or five
  takes and comp the best pieces.
- **Names**: the AI voice mispronounces proper names often enough that trailer voice-overs carry none (the on-screen
  card carries them). If a name must be read, respell it phonetically, flag it, and get the user's sign-off on the
  pronunciation.
- Write numbers the way they should be said ("twenty thirty", "three hundred thousand"), and read the block in your
  head as the voice before delivering.

## Voice clones: consent first
Only clone a real person's voice when that person (or the client who has their permission) has said yes. Keep the
written consent on file, get the person's sign-off on the outputs before anything posts, and label AI content where the
platform or audience expects it. Founders and investors are common targets of scam deepfake ads, which is one more
reason the consent and the labels are not optional. Never clone a voice to imitate someone who has not agreed.

## Local voice models (tested on an Apple Silicon Mac only)
What was learned building a consented clone for a finance creator's own reels (Oct 2026):
- **Licences decide.** The best open voice cloners at the time were licensed non-commercial, so not usable for paid
  client work. Commercially usable ones that were tested: VoxCPM2 (Apache, 48 kHz, about 1.2x real time on the Mac
  GPU), Qwen3-TTS (Apache), Chatterbox (MIT, adds an inaudible watermark, much slower). GPT-SoVITS was rejected by ear
  ("a lot of weird noise", "quite robotic"): its vocoder put buzzy energy at 8 to 16 kHz that spectrograms showed and
  automatic quality scores missed. A real fine-tune needs a paid cloud GPU: ask first.
- **Windows**: none of these were tried on Windows. They are PyTorch models, so an NVIDIA PC would need a CUDA build of
  PyTorch; treat every speed number above as Mac-only. Any install is the user's call (name, source, size first).
- **The approved recipe**: VoxCPM2 in continuation mode with a clean clip of the person's own speech as both the prompt
  and the reference (cfg 2.0, 10 steps, normalisation on), one paragraph per call, up to six takes per paragraph,
  keeping takes with no fillers, key words heard clearly and a word difference against the script of 0.06 or less;
  0.5 s gaps between paragraphs; two-pass loudness normalisation to -16 LUFS (ffmpeg `loudnorm` in two passes, then
  confirm with `premiere-ae-editing` `scripts/media/atools.py`); 48 kHz 24-bit.
- **What broke the likeness**: a bracketed style hint ("calm, clear and confident delivery") acts as voice design and
  pulls toward a generic narrator. The user said it "doesn't resemble anymore at all", although the speaker-similarity
  score only fell from 0.981 to 0.974. Treat the score as a guard rail (below about 0.98 against real clips was
  failing) and let the user's ear decide. Re-cutting pauses afterwards and speed nudges were dropped too.
- **The prompt clip sets the delivery**: a chatty podcast clip teaches fillers and thinking pauses; a scripted ad read
  gives clean pauses but too fast a pace (slowing the prompt with Rubber Band helped). The user picked between three
  short versions of ONE passage by ear before any full script was rendered: do that every time.

## Checks on every take
- Transcribe the take and compare it with the script: `premiere-ae-editing` `scripts/media/hear.py take.wav take.json`
  gives word timings on Windows and on a Mac (mlx-whisper there when installed); the `podcast-trailers`
  `scripts/transcribe.py` gives a segment transcript on either.
- Forced alignment catches swallowed short words (a missing "and" scored near 0 where spoken words score 0.8 to 0.96)
  and the mumble a model adds before the first word (trim at the last quiet frame before it). WhisperX does this; see
  `premiere-ae-editing` `references/timing.md`.
- Normalise numbers in the checker (years said as words, "ARK" written so it is said as a word). The rejected model's
  front end also read "S&P" as letters, "1960s" as "nineteen sixty seconds" and hyphenated numbers wrongly, and an
  Oxford comma stopped a list ending from blurring: test such words in any model.
- Run one voice model at a time: with Premiere open the machine ran out of memory and takes slowed from about 15 s to 25
  to 75 s each.
