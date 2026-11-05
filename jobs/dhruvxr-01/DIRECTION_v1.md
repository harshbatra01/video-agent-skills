# DIRECTION v1: spec brand film in the WHP style (draft for approval)
5 Nov 2026. Nothing here is approved yet. UNCHECKED = a fact not verified this session.

## 0. What the repo can do for this job
| Step | Useful in the repo | Notes |
|---|---|---|
| Measuring our render against WHP | `skills/minidoc-reference-style/scripts/` (frame_scores, cut_events, event_sheets, frame_strip), `skills/word-matched-broll/scripts/colour_stats.py`, `skills/reference-study/scripts/beat_map.py`, `research/dhruvxr/tools/` (crop_strip, text_box, sync_test, envelope) | All ran here already. Best use: the same numbers table, ours against WHP |
| Sound | `skills/premiere-ae-editing/scripts/media/beats.py` (numpy, beat grid), `atools.py` (LUFS, true peak), `kit/library/pipelines/ad-build-kit/audio/` (analyze_sfx.py measures each SFX, bake_kit.py trims and peak-aligns a kit, music_edit.py cuts a track to length), `skills/research-and-sourcing/references/music-and-sfx-sourcing.md` and `licensing-and-rights.md` | ad-build-kit has Windows paths hard-coded, so adapt. `synth.py` needs scipy, which is not installed |
| Visual effects in Python | `skills/effect-library/blocks/` (particle-mind, screen-photo-push, colorize-reveal, video-wall) | Particles and the tilted screen are direct helps. Not run yet |
| Effect values | `skills/motion-design/effects-library/recipes/` (pixel dither, one-frame glitch, slow shutter, luma dissolve), `skills/motion-design/references/native-looks.md` (halftone, glow, globe maths), `transitions.md` (flash values) | AE recipes, but the numbers carry over to Python |
| Type | `skills/motion-design/references/titles-captions-type.md`; Inter is installed here | |
| After Effects route | `skills/premiere-ae-editing/scripts/ae/` (ae_build, ae_run, motion_lib, scene_lib) plus the 18-effect AE library | Only if After Effects runs on your Mac. Raises the quality ceiling a lot |
| HTML cards | `skills/production-automation` (headless Chrome templates); headless Chrome works here | For UI cards and labels |
| Gates and QA | `skills/video-agent`, `skills/edit-loop-guard` (+ guard_check.py), `skills/goal-alignment-review`, `kit/library/pipelines/edits-kit/tools/` (cuts.py snaps cuts to hits, compare.py, qasheet.py) | guard_check thresholds were set for the Altman job; adjust them. edits-kit tools not run yet |
| Not useful here | idea-finder radar (news), word-matched-broll (narrated B-roll), mass-reel-writer, meme and podcast skills | |

## 1. Company for the spec
WHP is a brand film for Whop. We make a spec (unsolicited) brand film for another company in the same form.

| Option | Why it fits | Risk |
|---|---|---|
| **Linear (recommended)** | Dark, monochrome brand that suits the black-and-grey look; a product UI that suits the tilted 3D screen; its audience (builders, designers) is the audience of motion pages on X | Linear spec reels are common, so ours must be sharp |
| Vercel | Black-and-white brand, fits the look exactly | The UI is mostly code and dashboards, so it's less visual |
| Raycast | Dark brand, keyboard and command UI | The product is narrow, so it's harder to say in 14 words |

Facts about these companies are UNCHECKED here (names, domains, colours, fonts). Before any build we read the company's own brand page.

**Rights for a spec:** use the logo only as the brand guidelines allow (no altering the mark), record the real app ourselves with dummy data, label the post "spec, not affiliated", and imply no endorsement. Your call.

## 2. Script (Linear), on WHP's measured frame grid (30 fps, 495 frames, 16.5 s)
Voice-over: 14 words in 5 phrases (WHP has 15 in 5). Placed on WHP's word times.

| # | Time (s) | Frames | Voice | On screen | Picture | Effect | Sound |
|---|---|---|---|---|---|---|---|
| 1 | 0.00 to 0.27 | f0 to f7 | | | A dotted ring (our own shape, like an empty status circle) | Dot form | Sub impact starts 0.1 s |
| 2 | 0.27 to 1.50 | f8 to f44 | | "// noise //" top left from f21; "@ noise //" bottom right from f28 | Burst of "noise": notification stack, sticky-note wall, tangled cables, crossed-out whiteboard, alarm clock, a crowded office | Shots of 1 to 12 f, white flash f10, mono, vertical-line texture | Sub impact to 1.6 s |
| 3 | 1.40 to 2.00 | f42 to f60 | "Noise." | labels hold | White flash f45, then a slow macro (a cursor blinking on an empty page) | | |
| 4 | 2.53 to 3.00 | f76 to f90 | | "Backlog" big italic, 2 f (f76 to f77); "// backlog 999+" top right, "@/ priority //" left (f81 to f95) | Crowded open-plan office, white blowout, then 1-bit threshold | Blowout, threshold | Dip to about -26 dB, hit at 2.8 |
| 5 | 3.03 to 3.70 | f91 to f111 | | App UI text | Real Linear issue list, tilted in 3D, one issue moves to Done | 2 f focus pull, drift | |
| 6 | 3.73 to 4.30 | f112 to f129 | | Commit-log text (our own, made up, no real names) | Scan-line tear | Glitch 18 f | Hit at 3.9 |
| 7 | 4.33 to 6.47 | f130 to f194 | "Focus." (4.48) | "focus" upper left, "/ˈfōkəs/" lower right, drifting apart | Fade from white into a dot-matrix crosshair | Dot form, drift | Hit at 4.4 |
| 8 | 6.50 to 8.07 | f195 to f242 | "Every team. One system." (6.56 to 8.88) | | White 2 f, then dots become particles that gather | Particles | Hit at 6.4 |
| 9 | 8.10 to 9.53 | f243 to f286 | | | White bloom, then the Linear mark clean, glowing behind it, camera pulling back | Bloom behind the logo, not on it | Hit at 7.9 to 8.3 |
| 10 | 9.57 to 10.70 | f287 to f321 | "This is how great software ships." (9.90 to 12.48) | "this" top left, moving with the camera | The mark built from small tiles of team and product shots, bursting into a collage; "[ 09:41 ]" chip | Tiles, camera push | Hit at 9.7 |
| 11 | 10.73 to 11.40 | f322 to f342 | | | White 1 f, then a second burst: slow-shutter crowd, stairwell, fisheye | Burst | Hit at 11.0 |
| 12 | 11.43 to 13.70 | f343 to f410 | | | Dot globe turning and fading out | Globe | Bed about -18 dB |
| 13 | 13.70 to 14.00 | f411 to f420 | | | Black | | |
| 14 | 14.03 to 16.50 | f421 to f494 | "linear.app" (14.28, domain UNCHECKED) | Wordmark: wipe right to left over 3 f, fade up stepped every 3 f to f431 | Black | | Hit at 14.1; fade to silence 15.96 to 16.49 |

Copy risk: the shape mirrors WHP closely ("Every team. One system." against "Every business. One checkout."). That is the brief ("very similar"), but it is the most copy-like line. Alternative: "Every idea. One place."

## 3. Creative direction
- **Frame:** 16:9, 1920x1080 master plus a 1280x720 copy, 30 fps, 16.5 s.
- **Colour:** black base. Footage graded mono, near-black at least 70%, mean brightness 0.14 to 0.20. Colour appears only in the Linear UI and the mark (their own colours, from the brand page).
- **Texture:** fine vertical lines over footage (about 5% strength), grain sigma 3 to 5, soft vignette.
- **Type:** Inter (installed). Labels italic, 2.2 to 2.5% of frame height, grey #B4 to #CA, soft glow. Concept word upright, 3.9%. Our text never covers the mark.
- **Motion:** blur-ins of 3 f; text drifts are two-key moves; end animations stepped every 3 f (10 fps), as measured on WHP.
- **Footage:** monochrome stock (hands, offices, crowds, stairs), licensed (Pexels licence or paid Artgrid/Storyblocks), plus our own app recording. No faces without a licence that covers them.
- **Sound:** sub impact on frame 0, quiet dip at 2 s, hits only on picture changes (8 hits, WHP times), voice on top, -14 LUFS, true peak -1 dBTP, fade on the last 0.5 s.
- **Voice:** calm, low, unhurried (WHP not heard, so this is judged). Options: your own voice, a hired voice, or ElevenLabs (needs your key and a commercial plan).
- **Music:** a licensed dark minimal track with a hit at the start (Epidemic Sound or Artlist), cut to 16.5 s. I propose 3 and you pick by ear.

## 4. Execution plan (each step ends at a gate)
| # | Step | Who | Time (estimate) | Gate |
|---|---|---|---|---|
| 1 | Approve company, script, direction | You | | GATE A |
| 2 | Brand check: brand page, logo files, guidelines, the real domain and colours | Me, if the site loads here; else you | 20 min | |
| 3 | Sound first: 3 tracks for you to hear, the voice read, beat map and hit list measured on the real files | Both | 1 to 2 h | GATE B |
| 4 | Assets: app recording (your Mac), stock picks with licences in SOURCES.txt | You record; I pick and log | 1 to 2 h | |
| 5 | Engine: After Effects on your Mac (better 3D, glow, particles) or Python here | You decide | | GATE C |
| 6 | Pilot: first 3 s, beside WHP, every-frame strips and numbers; 3 to 4 strengths for glow and glitch | Me | 1 to 2 h | GATE D |
| 7 | Full build, then the same numbers table ours against WHP before you see it | Me | 3 to 5 h | GATE E |
| 8 | Notes rounds with a ledger, final checks (size, fps, loudness, spelling, rights) | Both | per round | GATE F |

## 5. Questions (each with a default)
1. Company: Linear? Default: Linear.
2. Rights: spec label and guideline-safe logo use? Default: yes, "spec, not affiliated" in the post.
3. Voice: yours, hired, or ElevenLabs? Default: ElevenLabs if you have a key, else yours.
4. Music: licensed library (which account do you have)? Default: Epidemic Sound.
5. Engine: is After Effects on your Mac? Default: Python here, and a 3 s pilot decides.
6. "Every team. One system." or "Every idea. One place."? Default: the first.
