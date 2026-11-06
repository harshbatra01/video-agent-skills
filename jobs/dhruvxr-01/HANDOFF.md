# HANDOFF: dhruvxr-01
Updated 5 Nov 2026, about 19:30 UTC.

- Job: Linear spec brand film in the WHP style (approved by the user: Linear, no After Effects, licences handled later by the user, sound now).
- Branch: job/dhruvxr. Never main.
- Direction: DIRECTION_v1.md. Build: build/build.py (picture), build/sound.py (sound). Latest: build/out/animatic_v1.mp4 (16.5 s, 495 f, 1280x720, 30 fps, sound v1).
- Blocked: network policy blocks linear.app, YouTube and stock sites. The user is uploading assets into build/assets/ (list: build/assets/ASSETS_NEEDED.md). Three repo checks are scheduled (about 19:52, 20:22, 20:52 UTC).
- Next: when assets land, wire them into build.py (footage slots, ui, logo, wordmark, collage), render v2, compare against WHP with the same tools, update the sound hits if any cut moves.
- Sound v1 against WHP (build/out/sound_v1_vs_WHP.txt): level-curve correlation 0.92; sub intro -0.1 vs -1.0 dB; dip -25.6 vs -25.8; bed -17.2 vs -17.3; fade -38.2 vs -38.5; hits on picture changes 11 of 15 vs WHP 12 of 22. Integrated -13.2 LUFS, true peak -0.9 dBTP.
- Missing: the voice-over (14 words, WHP word times). No TTS engine here and ElevenLabs is blocked; needs the user's recording or an API key.
- Not checked: playback and listening (Claude cannot watch or hear).

## Update about 20:05 UTC
- Assets arrived (commit 2676f30): 13 clips, 9 photos, Linear logo and wordmark, brand_notes.txt, sources.txt. ui.mp4 and ui.png still to be recorded by the user.
- Latest cut: build/out/cut_v2.mp4 (picture v2 plus sound v1), 16.5 s, 495 f. Comparison: build/out/compare_v2.jpg.
- Brand rules applied: logo and wordmark are Linear's files, only scaled, laid on after grain and vignette; the photo tiles form our own ring, not the mark; the wordmark reveal is a stepped fade with no wipe mask. Open for the user: the soft background light behind the logo (judged as separate scene light, not on the mark).
- Colour v2 against WHP: brightness 0.136 vs 0.138, near-black 76.8% vs 78.0%, near-grey 96.8% vs 96.7%. Cut events 19 vs 17.
- Still open: the app recording (placeholder card at f91 to f129), the voice-over, the fisheye slot is a weak match (rock climber, barrel warp added).

## Update 6 Nov 2026 (new chat, same Mac)
- Installed Inter (Homebrew cask `font-inter`, 33.7 MB) so `build.py` can render here. Fixed `MONO` and `FD` paths in `build.py` for this Mac (DejaVu via matplotlib, Inter via `~/Library/Fonts/`).
- Rebuilt `cut_v2.mp4` locally from the already-approved `build.py`/`sound.py` (no creative changes). Re-measured against WHP with `colour_stats.py`, `cut_events.py`, ffmpeg `ebur128`: brightness 0.136 vs 0.138, near-black 76.8% vs 78.0%, near-grey 96.7% vs 96.7%, cut events 19 vs 17, loudness -13.2 LUFS true peak -0.9 dBTP. All match the numbers this file was reported with in the last chat, confirms the render is reproducible, not a new version.
- `cut_v2.mp4` is not committed (`.mp4`/`.wav` gitignored by design), it's local-only at `jobs/dhruvxr-01/build/out/cut_v2.mp4`.
- Flagged for the user, not yet resolved: `office_crowd.mp4` has a recognisable face (`sources.txt` says so itself); `notification_stack.mp4` is also a weak match (thumb scrolling an inbox, not a notification flood) and wasn't on the open-items list before; DIRECTION_v1 proposed a licensed music track, what's built is numpy-synthesized sound only; the logo-tile-burst (f295) and photo collage (f334) look structurally thinner than WHP's by eye on the comparison sheet.
- Nobody has watched or listened to this file yet, not the user, not Claude (Claude cannot). That's the real next step before any "is this good" verdict.
