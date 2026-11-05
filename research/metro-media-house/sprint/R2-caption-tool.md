# R2 caption tool (caption_words.py)

Usage: `python3 sprint/R2-tools/caption_words.py <bg video|image> <transcript.json> <out.mp4> [--w 1920 --h 1080 --fps 25 --t0 0 --t1 3 --png 1.5]`
Transcript: `{"words":[{"w","s","e"}]}`. `--png T` also saves the frame at T s next to out.mp4.

Matches spec: one word at a time at its start time; Inter Medium (found via fixed path, glob, then fc-match); cap height sized to 3.6% of frame height; vertical centre 50%; words spread across width in equal slots with wide gaps (8% side margins); line clears at sentence end or after 4 words; black text when mean luma under the word box is over 180, else white. PIL frames piped to ffmpeg (libx264, yuv420p).

Not yet: big bold emphasis words, fades in/out, per-word kerning to the reference, safe-area tuning for 9:16.

Test: NOT run (sprint time ran out). Reel path reference-reels/DfFsUfUx0dZ/reel.mp4 was not found; reel files live under raw/DfFsUfUx0dZ/, transcript location unconfirmed.
