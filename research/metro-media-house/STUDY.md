# Metro Media House: page study (4 reels)

Study date: 5 Nov 2026. Branch: `research/metro-media-house`, made from `reference-reels`.
Method: the repo's own tools (see README.md for what ran and how far each number can be trusted).
Claude read frames, transcripts and measurements. Claude did not watch playback or hear audio.

| Code | Reel | Account | Posted | Paid? |
|---|---|---|---|---|
| PAL | DclpjyxhKF6, Palmer Luckey and the "Palantir Mafia" | Metro Media House | 28 Aug 2026 | No disclosure in caption |
| ACK | DdHKc5GBqT-, Bill Ackman | Metro Media House | 10 Sep 2026 | No disclosure in caption |
| EIN | Dee-mp9BJqG, Einstein vs Bohr, then AI | **USVC (usvchq)** | 14 Oct 2026 | Yes: "Paid for by USVC's adviser AngelList Asset Management" |
| YC | DfFsUfUx0dZ, the early YC photo | Metro Media House | 29 Oct 2026 | Yes: same disclosure, "Presented by @usvchq" |

---

## 1. The short version

1. **Three of the reels are one page's organic house style (PAL, ACK) plus one paid placement on that page (YC).** EIN is USVC's own ad, posted on USVC's account. It shares the hook template, opener device, caption font and white paper cards with the Metro reels, so it was very likely made by the same studio. That is judged by eye, not proven. It drops two Metro signatures (inverted-frame cuts, the M logo sting) and is mostly black and white. Treat it as a style cousin, not as a page sample.
2. **Every reel opens on one famous photo** and the line "This is / This might be ... the most ...". The photo is revealed cell by cell through a 3x3 grid of white blocks in the first second. All 4.
3. **Every reel ends on a mirrored two-line kicker** that flips the hook: "The PayPal Mafia built the internet you scroll all day. The Palantir Mafia built the thing quietly watching you do it." All 4.
4. **The pace is calmer than the AC references in this repo.** Median shot 0.54 to 0.80 s against Altman's 0.38 s. Only 7 to 9 shots in the first 5 s, against Altman's 12. Cuts follow word starts, not the music beat.
5. **The Metro signature cut is a single colour-inverted frame,** often followed by one white or dark frame, then the new shot. ACK has 18 and YC 18, PAL 2 by the detector (an undercount, see section 3), EIN 0.
6. **Captions are small white words in a clean grotesk sans, placed one by one across the middle of the frame,** with gaps between them. On big beats one or two words go large and bold. On white frames the words turn black.
7. **The story:** a famous name or network, a "basically [movie character] in real life" comparison, the name held back until 8 to 17 s, one paradox ("the same thing that made him ... nearly blew up his career"), a run of dated events with printed numbers, a turn, a zoom out to now, then the mirrored kicker.
8. **Paid reels add a 9 to 11 s ad tail** on white or cream cards ("Comment GUIDE" / "Comment book") and drop the M logo sting. Comments per like are 4 to 21 times higher on the paid reels.

---

## 2. Numbers per reel

Same tool and threshold for every reel. Shots come from `cut_events.py` via `ref_stats.py`. Colour comes from `colour_stats.py` at 2 frames a second.

| Measure | PAL | ACK | EIN | YC | Range, all 4 | Metro only (PAL, ACK, YC) |
|---|---|---|---|---|---|---|
| Format | 1916x1078, 24 fps | 1916x1078, 25 fps | 1920x1080, 25 fps | 1916x1078, 24 fps | landscape 16:9 | landscape 16:9 |
| Length | 78.4 s | 95.0 s | 119.4 s | 80.2 s | 78 to 119 s | 78 to 95 s |
| Words (Whisper) | 235 | 252 | 349 | 231 | 231 to 349 | 231 to 252 |
| Words a minute | 184 | 171 | 177 | 174 | 171 to 184 | 171 to 184 |
| Shots (cut events) | 85 | 125 | 118 | 124 | 85 to 125 | 85 to 125 |
| Micro-shots inside events | 26 | 85 | 10 | 76 | 10 to 85 | 26 to 85 |
| Median shot | 0.75 s | 0.60 s | 0.80 s | 0.54 s | 0.54 to 0.80 s | 0.54 to 0.75 s |
| 90th percentile shot | 1.62 s | 1.42 s | 1.93 s | 1.20 s | 1.20 to 1.93 s | 1.20 to 1.62 s |
| Longest shot | 4.42 s | 6.56 s | 8.80 s | 4.12 s | 4.1 to 8.8 s | 4.1 to 6.6 s |
| Shots a second | 1.08 | 1.32 | 0.99 | 1.55 | 0.99 to 1.55 | 1.08 to 1.55 |
| Cuts a second by quarter | 1.28, 1.28, 0.87, 0.92 | 1.56, 1.81, 1.22, 0.67 | 1.27, 0.94, 1.24, 0.50 | 1.75, 1.55, 1.40, 1.50 | fastest in Q1 or Q2 in all 4 | |
| Shots in first 5 s | 7 | 9 | 9 | 7 | 7 to 9 | 7 to 9 |
| Words in first 5 s | 16 | 14 | 13 | 15 | 13 to 16 | 14 to 16 |
| Shots of 4 frames or less | 4.7% | 4.8% | 6.8% | 8.1% | 5 to 8% | 5 to 8% |
| Cuts within 0.12 s of a word start | 67% | 65% | 55% | 59% | 55 to 67% | 59 to 67% |
| Cuts on the beat vs chance | 12% vs 14% | 20% vs 20% | 17% vs 16% | 24% vs 24% | at chance in all 4 | |
| Inverted-frame events | 2 | 18 | 0 | 18 | 0 to 18 | 2 to 18 |
| CUT+FLASH events | 5 | 24 | 3 | 11 | 3 to 24 | 5 to 24 |
| Moving footage, tool | 48% | 35% | 49% | 51% | 35 to 51% | 35 to 51% |
| Near-monochrome shots | 20% | 20% | 71% | 24% | 20 to 71% | 20 to 24% |
| Frames brighter than luma 200 | 11.5% | 1.1% | 11.1% | 13.5% | 1 to 14% | 1 to 14% |
| Mean brightness | 0.46 | 0.37 | 0.43 | 0.44 | 0.37 to 0.46 | 0.37 to 0.46 |
| Mean saturation | 0.29 | 0.36 | 0.17 | 0.25 | 0.17 to 0.36 | 0.25 to 0.36 |
| Vivid pixels | 17.7% | 21.6% | 6.8% | 14.5% | 7 to 22% | 15 to 22% |
| Near-black pixels | 21.4% | 24.5% | 23.9% | 22.1% | 21 to 25% | 21 to 25% |
| Vivid hue: red plus orange/yellow | 57% | 48% | 61% | 66% | 48 to 66% | 48 to 66% |
| Vivid hue: cyan/blue | 39% | 48% | 37% | 28% | 28 to 48% | 28 to 48% |
| Music under voice, in gaps | 2.3 dB | 3.7 dB | 3.0 dB | 0.8 dB | 0.8 to 3.7 dB | 0.8 to 3.7 dB |
| Total pause time (gaps over 0.12 s) | 3.5 s | 6.6 s | 10.2 s | 6.2 s | 3.5 to 10.2 s | 3.5 to 6.6 s |
| Picture after the last word | 1.8 s | 6.2 s | 0.7 s | 0.3 s | 0.3 to 6.2 s | |
| Likes (no views on file) | 51,224 | 41,062 | 7,919 | 18,304 | | |
| Comments | 176 | 108 | 495 | 213 | | |
| Comments per 100 likes | 0.3 | 0.3 | 6.3 | 1.2 | | |

**Against this repo's references, same tools** (from `reference-study`): Altman median 0.38 s, 12 shots in the first 5 s, 16 words, brightness 0.36, moving share 39% by tool. AC Max median 0.80 s, 7 shots. So this page sits between Altman and Max in pace, and is brighter than all of them.

---

## 3. How far to trust each number

| Number | Trust | Why |
|---|---|---|
| Length, words, words a minute | High | Direct. Word count is Whisper's; a few words may be wrong. |
| Shots, median, quarters | Medium | `cut_events.py` thresholds were set on Altman. The page uses many composites, where a new layer pops in without a full cut. ffmpeg scene detection at 0.25 gave 73, 162, 97 and 123 shots, against 85, 125, 118 and 124 from cut events. Compare only within one tool. |
| Micro-shots | Low | Counts big jumps inside long events. Includes block reveals and flashes, not only real 2-frame shots. |
| Inverted-frame events | Medium, lower bound | Checked on the flash-event sheets: the hits are real. It misses partial inversions (PAL 4.38 s is inverted by eye and was not caught). PAL's real count is above 2. Pairs 0.12 s apart were merged into one event. |
| Moving footage share | Low | `motion_class.py` (threshold 2.2 in the code; the analysis notes say 0.9). This page pushes and moves stills inside composites, and puts moving clips inside still frames, so the tool mixes them up. By eye, more than half of PAL, ACK and YC is real moving footage (interviews, film, archive). That is not measured. |
| Colour | Medium | Fine as a warning light. EIN's monochrome is real (archival black and white). |
| Music under voice | Low | Pauses total only 3.5 to 10.2 s, and Whisper word ends spill into gaps. It does show the bed is loud (under 4 dB below the voice), matching the repo's 2.5 to 4.7 dB finding. |
| Tempo | Very low | Run on the full mix; no music stem. Only YC shows a steady grid above chance (102 BPM, 33% of onsets vs 17% chance). The cut-on-beat result (at chance in all 4) is solid either way. |
| Soundbites | Judged | Found from frames plus first-person wording. Not heard. |
| Interest score marks | Judged | Tags and 0 to 2 marks are Claude's reading. |
| Captions | Measured by eye | Full-resolution crops, roughly ±3 px. No OCR is installed. |
| Paid status | Medium | From the posts' own captions. The Instagram "Paid partnership" label is not in the metadata. |

Not checked at all: playback, sound, voice identity (same narrator or not), music track IDs, sound effects, views, retention, and whether the page posts other formats.

---

## 4. Paid vs organic, and the USVC question

**What the captions say.** EIN and YC both end with "Presented by @usvchq ... Paid for by USVC's adviser AngelList Asset Management, which creates incentives to promote." PAL and ACK carry no disclosure and no comment-to-get call to action.

**What changes on the paid reels.**
| | Organic (PAL, ACK) | Paid on Metro (YC) | USVC's own (EIN) |
|---|---|---|---|
| Ending | Mirrored kicker, then a callback picture, then the M logo sting | Kicker, then a 10.4 s ad tail (69.8 to 80.2 s) | Kicker, then a bridge line, then an 8.8 s ad tail on cream |
| Ad tail look | none | White and black cards, blue USVC wordmark, "comment" small over a big "GUIDE" in quotes, orange folder icon | Cream paper, sponsor company logos (Mercury, Stripe, Airbnb, SpaceX, Fairchild), typing-cursor block |
| M logo sting | Yes (PAL 76.7 s, ACK 92.4 s) | No | No |
| Story topic | Free choice | Startups and the investors behind them (fits a venture product) | Science, then AI (a "13 company stories" book) |
| Bridge into the ad | none | "But to date, the public has had limited access..." | "And he wasn't the only genius who bet against the idea that won." |
| Comments per 100 likes | 0.3 | 1.2 | 6.3 |

**Reading (judged).** The paid reels keep the same story machine and swap the ending. YC, a paid post on Metro's own page, still looks like a Metro reel: inverted cuts, grid opener, small captions. So "fits the page" covers both types, and the ending decides which type it is.

**What we cannot tell:** whether the next post will be paid, who edits EIN, or whether USVC is a recurring sponsor.

---

## 5. Style law (rebuild spec)

Tags: **SAME** = in all 4. **METRO** = in PAL, ACK and YC, not EIN. **VARIES** = differs. **ONCE** = seen in one reel.

### Frame
- **SAME** Landscape 16:9, 1920x1080 (1916x1078 as delivered), 24 or 25 fps, posted as a reel. No vertical reframing, no letterbox.
- **SAME** Soft edge glow or halation on many frames, with a slight vignette on white paper cards. Judged by eye on full-resolution crops.

### Pace
- **SAME** Median shot 0.54 to 0.80 s. 90th percentile 1.2 to 1.9 s. Longest hold 4 to 9 s, used for a soundbite, a built object or the last shot.
- **SAME** First 5 s: 7 to 9 shots, 13 to 16 words, one subject (one photo).
- **SAME** Cuts follow words: 55 to 67% land within 0.12 s of a word start. Beat sync is at chance.
- **VARIES** Where the pace drops: PAL and EIN slow in the second half, ACK in the last quarter. YC stays fast to the end (1.40 to 1.75 cuts a second in every quarter).

### Opener (first 3 s, every frame checked)
- **SAME** One famous photo is the hook object. PAL: Palmer Luckey cosplay photo. ACK: Ackman at a poker table. EIN: the 1927 Solvay photo. YC: an early YC group photo.
- **SAME** A 3x3 grid reveal: white or overexposed blocks pop into grid cells over about 1 s, a few cells at a time, and the sharp photo fills in behind them. PAL 0.12 to 0.62 s, ACK 0.08 to 0.52 s, EIN 0.48 to 1.28 s, YC 0.00 to 1.25 s. Thin grid lines stay faintly visible.
- **METRO** In the first 1.5 s the background darkens and the subject is cut out with a light rim (PAL 0.83 to 1.0 s, ACK 0.96 s). The background then swaps cell by cell to the place word ("Silicon Valley" becomes the Golden Gate at 1.9 to 2.3 s; "America" becomes Apple Park at 2.8 to 3.0 s).
- **VARIES** Extra hit in the first second: ACK has a 2-frame thermal colour flash plus a 1-frame negative at 0.80 to 0.88 s and a red neon outline tracing Ackman at 1.36 to 1.52 s. YC solarises the photo out of white and shrinks it to a print on white paper (1.29 to 1.50 s), then flickers black and white on "in startup history" (2.25 to 2.42 s). EIN uses zoom blur with RGB fringe (1.56 to 1.64 s and 2.84 to 2.96 s).

### Transitions
- **METRO** Inverted-frame cut: the last frame of shot A is shown colour-inverted for 1 frame, sometimes followed by a 1-frame white or near-black frame, then shot B. ACK and YC use it about every 3 to 5 s (11.4 and 13.5 a minute).
- **SAME** Hard white single frames between shots (ACK 7.0, 10.0, 17.2, 28.2, 33.6 and 37.8 s; PAL 23.4 s).
- **VARIES** Others seen: pixel-mosaic dissolve (ACK 31.0 s), grey-block dissolve (ACK 29.8 s, "bury"), light-leak or fire burn (ACK 44.0 to 44.6 s), zoom-blur push into the next layer (EIN, YC 77.8 s).

### Captions
- **SAME** Every spoken word is on screen, built one word at a time on its word start. 1 to 6 words per line. The line clears at phrase ends.
- **SAME** Font: a clean neo-grotesk sans, medium weight, slightly tight tracking, sentence case as spoken. Closest free matches: Inter Medium or Inter Display Medium (judged, not fitted). It also reads close to SF Pro Display Medium and Helvetica Now Display Medium.
- **SAME** Size: cap height about 37 to 40 px on 1078 (3.4 to 3.7% of frame height). Small on purpose.
- **SAME** Position: vertical centre at 44 to 52% of frame height (ACK 26.0 s: 50%; ACK 12.9 s: 44%; EIN 102.9 s: 49%). Words are spread across the width with wide gaps ("and   told   Wall"), often placed beside the subject's face.
- **SAME** Colour: white on dark or busy frames, black on white or cream paper. No box, no stroke. A soft glow at most.
- **SAME** Big words: on 1 to 3 key words per beat the type jumps to 3 to 4 times the size, bold, tight, stacked or split around the subject ("Silicon Valley", "Tony Stark" in red, "on occasion kill them", "THE REAL WOLF OF WALL STREET" in yellow, "OF ALL TIME", "$43 Million", "USVC"). About 8 to 15 per reel by eye.
- **ONCE** Condensed bold capitals in quote marks for a famous line (EIN "GOD DOESN'T PLAY DICE", 102 to 103 s).
- **ONCE** Serif labels over faces in a group photo (EIN Bohr, Schrödinger, Heisenberg at 4 to 6 s).

### Picture content
- **SAME** Real people first. A named person gets many different clips (interviews, talks, archive), not one clip repeated.
- **SAME** White paper cards: a cut-out photo, a print or a polaroid on off-white paper with small black words. 11 to 14% of frames are bright in PAL, EIN and YC.
- **METRO** Film and pop-culture comparisons cut in as proof of the comparison line: PAL Iron Man (4.4 to 8.0 s) and a film clip on "godfather" (43 s, likely The Godfather, not confirmed); ACK The Wolf of Wall Street (5.3 to 10.0 s, 50.1 s, 62.6 s, 87.5 to 92 s) and Pac-Man (71 s).
- **SAME** Logo bursts on lists: banks at 0.16 to 0.24 s each (ACK 23.3 to 25.4 s), startups (YC 52.7 s), sponsor companies (EIN 112 s).
- **SAME** Printed numbers as big type over the object: "$10,000.00" receipt, "1.4 billion dollars", "35%", "2008", "17", "$43 Million", "$6 thousand".
- **SAME** Real soundbites where the line belongs to someone else, with the speaker on screen and the words captioned. PAL Karp, "Palantir is here to scare enemies and on occasion kill them" (51.9 to 56.2 s). ACK news anchor on 2008 (38.7 to 41 s) and Ackman's own Forbes clip (72.9 to 79.4 s). EIN and YC: none found in frames.
- **SAME** Composites: a cut-out person over a themed background, photo tiles popping in, screen walls at a tilted 3D angle (PAL 42 to 45 s).
- **SAME** Symbols, mostly in colour: chess pieces (PAL), dice (EIN), pyramid illustration (ACK), explosion (PAL, ACK), banknote portraits (ACK).
- **VARIES** Colour mix: PAL, ACK and YC are full colour with red and blue sources. EIN is 71% near-monochrome archival.

### Built objects
- **ONCE** each, but the type recurs: PAL PayPal receipt UI with a spinner, a check, then a yellow highlighter sweep on "$10,000" (13.0 to 14.3 s), then a zoom-blur out to a photo of Trump holding the printed receipt (14.3 to 16.5 s). PAL framed PayPal Mafia photo pinned on a white wall (69.3 s). PAL illustrated room that pulls back into a gold frame being watched (74.0 to 76.7 s). EIN polaroid board "Einstein vs Bohr" (58 to 72 s). YC camcorder screen (48 s). YC orange folder icon (78 to 80 s).

### Photo walk-through (YC, also PAL in part)
- **VARIES** The hook photo is the spine. Each time a person is named, the photo turns black and white except that person, a 2-frame white silhouette flashes over them, it pushes in, then it cuts to real footage of them (YC 26.9 to 30.9 s, 36.3 s, 50.2 s). PAL comes back to its photo device at the end (69 to 73 s).

### Sound (measured where possible, not heard)
- **SAME** Voice nearly non-stop: 3.5 to 10.2 s of total pause per reel. 171 to 184 words a minute.
- **SAME** The music bed is loud: 0.8 to 3.7 dB under the voice in the gaps.
- **VARIES** YC's loudness peaks at 8 to 10 s, 42 s and 58 s (2-second RMS -7.4, -7.5 and -6.2 dB, against about -13 typical). These sit on story turns ("It all starts", "and killed him", "The PayPal Mafia built"). Likely risers or hits. Not heard.
- **ONCE** ACK drops to about -24 to -30 dB after 88 s (the film tail plus logo).

### Ending
- **SAME** Mirrored two-line kicker that flips the hook (section 7).
- **METRO organic** Callback picture under the kicker, then the M logo sting: white or black diagonal strokes sweep in from the corners and collapse into the "M" mark over about 0.5 s, then hold about 1.3 s on light grey (PAL) or black (ACK).
- **Paid** Ad tail instead of the sting (section 4).

---

## 6. Effect list with timecodes and how to rebuild

Frame evidence: `strips/` (every frame) and `raw/<id>/evsheet/`, `raw/<id>/shotwords/`.

| # | Effect | Where (s) | Evidence | Rebuild with our tools |
|---|---|---|---|---|
| 1 | 3x3 grid block reveal of the hook photo | PAL 0.12 to 0.62; ACK 0.08 to 0.52; EIN 0.48 to 1.28; YC 0.00 to 1.25 | `strips/*_000-003.jpg` | AE: `effects-library` 01 pixel_reveal as a base, with a 3x3 grid of white solids, staggered 2 to 3 frames, each fading to the image over 3 to 4 frames. Or ffmpeg/PIL in `build_template_v8.py` style: compose per frame. |
| 2 | Subject cut-out, background dims, light rim | PAL 0.83 to 1.9; ACK 0.96 to 1.6 | same strips | `premiere-ae-editing/scripts/stills/ps_cutout.jsx` or `person_mask.js` for the matte; background exposure -1.5 stops; inner glow 4 px. |
| 3 | Background swap cell by cell to the place word | PAL 1.88 to 2.25 (Golden Gate); ACK 2.76 to 2.96 (Apple Park) | same strips | Same grid as #1, revealing a new plate behind the matte. |
| 4 | Red neon outline tracing the subject | ACK 1.36 to 1.52 | `strips/DdHKc5GBqT-_000-003.jpg` | AE: matte edge, Stroke/Glow, red #FF2A2A, write-on over 4 frames, hold 2. `effects-library` 05 glowing_gradient_stroke. |
| 5 | Inverted-frame cut, 1 frame negative plus optional 1 white or black frame | ACK 18 events, YC 18, PAL 2+ | `strips/*_flash_events.jpg`, `raw/*/inverted.json` | Premiere: Invert on the last frame of A, then a 1-frame white matte. AE: `effects-library` 13 one_frame_glitch_burst, cut down to the invert step. Budget: about 1 every 3 to 5 s, on sentence turns. |
| 6 | Thermal/false-colour flash, 2 frames | ACK 0.80 to 0.84 | flash sheet row 2 | Colorama or Gradient Map with a rainbow LUT for 2 frames before the negative. |
| 7 | Zoom blur with RGB fringe into big type | EIN 1.56 to 1.64, 2.84 to 2.96; YC 77.8 to 77.9 | EIN flash sheet | `effects-library` 14 shake_chroma_impact without the shake, plus CC Radial Fast Blur. |
| 8 | Word-by-word small captions spread across the frame | all, whole runtime | `captions/*.jpg` | **No repo tool does this yet.** `style_captions.py` sets only font, size and vertical offset, and was measured on 1080x1920. Needs a small new script: one AE text layer per word from the word timings (`premiere-ae-editing/scripts/ae/`), or a HyperFrames overlay (`minidoc-reference-style/references/hyperframes-overlays.md`). Spec: Inter Medium, cap 38 px on 1080, centre y 50%, free x per word, each word on at its start, black on white frames. |
| 9 | Big word split or stacked around the subject | PAL 2.0 to 3.5, 4.5 to 5.9, 51.9 to 56.2; ACK 5.3 to 6.9; EIN 2.9 to 3.5; YC 15.5 to 16.8 | timesheets, `captions/DclpjyxhKF6_55.4.jpg` | Same new caption script, 3 to 4x size, Inter Bold, tracking -20. Last word fades in from 40% white. Colour picked from the source (red for Stark, yellow for Wolf). |
| 10 | Film and pop-culture callback clip | PAL 4.4 to 8.0 (Iron Man), 43 (likely The Godfather); ACK 5.3 to 10 and 87.5 to 92 (Wolf of Wall Street) | shot sheets | Footage choice, not an effect. Rights are a user decision (section 10). |
| 11 | Logo burst | ACK 23.3 to 25.4 (8 banks, 0.16 to 0.24 s each) | `raw/DdHKc5GBqT-/shotwords/sw_01.jpg` row 4 | `effect-library/blocks/video-wall` or plain cuts of logo plates, 4 to 6 frames each. |
| 12 | Banknote portrait burst into a counting number | ACK 48.4 to 50.1 (6 portraits at 2 frames, then "1" to "1.4" over cash) | `sw_02.jpg` rows 1 to 2 | Cut 2-frame stills, then a counter over a cash plate: `counterRow` in `premiere-ae-editing/scripts/ae/motion_lib.jsx`, restyled from Didot to Inter Bold. |
| 13 | Built UI receipt with spinner, check and highlighter | PAL 13.0 to 14.3, then zoom out to a photo holding it, 14.3 to 16.5 | `strips/DclpjyxhKF6_012-016_receipt.jpg` | HTML or HyperFrames card (`minidoc-reference-style/references/hyperframes-overlays.md`), then AE corner-pin onto a held-paper photo. `effects-library` 08 hail_mary_highlight_streak for the marker. |
| 14 | Photo walk-through: B&W except the named person, white silhouette flash, push in, cut to their footage | YC 26.9 to 30.9, 36.3 to 37.4, 50.2 to 51.9 | `strips/DfFsUfUx0dZ_027-031_photo_walk.jpg` | Partly covered: `effect-library/blocks/colorize-reveal` does a whole-frame black-and-white-to-colour sweep. Selective colour needs a person matte added (`person_mask.js` is macOS only; `ps_cutout.jsx` in Photoshop). Then a 2-frame white silhouette and a 3% push. |
| 15 | Polaroids and prints on off-white paper | YC 1.3 to 2.2; EIN 58 to 72; PAL 8.0, 69.3 | timesheets | `effect-library/blocks/screen-photo-push` and the polaroid recipe in `minidoc-reference-style/references/effects-library.md`. Paper #EDECEA to #F2F1EF with a vignette. |
| 16 | Typing-cursor block in front of words | EIN 24 to 26, 66, 100, 116.9 to 118.4 | `strips/Dee-mp9BJqG_105-119_ad_tail.jpg` | Black rectangle the height of the caption, moving one word ahead. EIN only. |
| 17 | Tilted 3D screen wall | PAL 42 to 45 | flash sheet row 6 | AE 3D layers with camera dolly, `effects-library` 18 ui_accounts_card_typography for the tilt. |
| 18 | Callback zoom-out reveal | PAL 69.3 to 76.7 (framed photo, then a feed UI, then a room that becomes a framed painting watched by a man) | `strips/DclpjyxhKF6_069-078_ending.jpg` | AE nested comps with scale keys, then a cut-out figure. Needs an illustration or a real staged photo. |
| 19 | M logo sting | PAL 76.7 to 78.4 on grey; ACK 92.4 to 95.0 on black | ending strips | Not ours to copy. If the user wants a sting, design our own mark (section 10). |
| 20 | Ad tail cards | YC 69.8 to 80.2; EIN 110.5 to 119.4 | ad-tail strips | Plain white or cream cards plus the caption tool. Only for a paid post. |

---

## 7. Script formula for this page

### Measured (`interest_score.py`, tags in `script/`)
| | PAL | ACK | EIN full / story only | YC full / story only | AC refs in repo |
|---|---|---|---|---|---|
| Words | 234 | 250 | 348 / 321 | 230 / 186 | 250 to 280 |
| Sentences | 17 | 18 | 27 / 25 | 19 / 15 | |
| Average sentence | 13.8 | 13.9 | 12.9 / 12.8 | 12.1 / 12.4 | 10.7 to 15.6 |
| Event words | 29% | 60% | 33% / 36% | 55% / 68% | 40 to 79% |
| Explaining words | 32% | 12% | 47% / 43% | 25% / 8% | 4 to 31% |
| Tension words | 38% | 28% | 20% / 21% | 20% / 25% | 17 to 29% |
| Longest explaining run | 2 | 1 | 3 / 3 | 4 / 1 | 1 to 5 |
| Words before first event | 10% | 23% | 6% / 7% | 15% / 18% | 0 to 36% |
| Reading ease | 69 | 74 | 71 / 71 | 69 / 68 | 68 to 80 |

### The 12 checks, out of 24 (judged)
| Check | PAL | ACK | EIN | YC |
|---|---|---|---|---|
| Picture | 2 (drones, receipt) | 2 ("Carl, fuck you") | 2 (a new trap every morning) | 2 (company sold on eBay) |
| Action | 1 (29%) | 2 | 1 (36%) | 2 |
| Want | 1 | 2 (to be proven right) | 2 (Einstein wants to win) | 1 |
| Hook paid | 2 | 1 ("was all this legal?" is never answered) | 2 | 2 |
| Turn | 2 ("Palmer's only the side piece") | 2 (Herbalife, lost everything) | 2 (Einstein loses) | 1 |
| Return | 1 (the mafia detail arrives at 45%, not the first quarter) | 2 ("every CEO" returns as "some CEO") | 2 ("God doesn't play dice" returns changed) | 2 (the photo and the PayPal Mafia return) |
| **Interesting /12** | **9** | **11** | **11** | **10** |
| One thread | 1 (Palmer, then Palantir) | 2 | 2 | 1 (a list of people from one photo) |
| Info run | 2 | 2 | 1 | 1 full, 2 story only |
| Terms | 2 | 2 | 1 | 2 |
| Sentences | 2 | 2 | 2 | 2 |
| **Simple /8** | **7** | **8** | **6** | **6 full, 7 story** |
| Known name | 2 | 2 | 2 | 2 |
| Daily picture | 2 ("the internet you scroll") | 1 | 2 (dice, odds) | 2 |
| **Massy /4** | **4** | **3** | **4** | **4** |
| **Total /24** | **20** | **22** | **21** | **20 full, 21 story** |

All four clear the proposed pass mark (18 with Interesting at 9 or more), PAL only just.

### Coded features
| | PAL | ACK | EIN | YC |
|---|---|---|---|---|
| Hook line | "This is the most powerful man in Silicon Valley right now" | "This is the investor every CEO in America is afraid of" | "This is one of the most iconic photos of all time" | "This might be the most important photo in startup history" |
| Comparison | "basically Tony Stark in real life" | "basically the real Wolf of Wall Street" | none | "the PayPal mafia might finally be getting some competition" |
| Name first said | 8.0 s ("His name's Palmer Luckey") | 10.0 s ("His name's Bill Ackman") | 3.7 s (names in the photo) | 16.9 s ("Sam") |
| Story type | Origin of a power network | Rise, fall, repeat | Duel of ideas, then why it matters now | One photo, many origin stories |
| Drive | Palmer: does what the valley won't. Thiel: aims the fraud system at terrorists | Being "completely convinced" | Einstein must win | Graham bets on founders, not ideas |
| Planted detail | "the same company that made him a billionaire" | "the same thing that made him ... nearly blew up his career" | "God does not play dice" | the photo and the PayPal Mafia |
| Turn | "But Palmer's only the side piece" (35%) | Herbalife: "and lost everything" (75%) | "One by one, Einstein's traps fell" (55%) | eBay auction then Twitch (55%) |
| Zoom out to now | "Now look at what that crew runs" | "And right now, some CEO just found out" | "When ChatGPT writes you a sentence" | "5,000 more came after" |
| Ending | mirrored couplet | mirrored couplet | mirrored couplet, then ad | mirrored couplet, then ad |
| Dates said | 0 | 2 (2002, 2008) | 0 ("A hundred years later") | 0 |
| "you" | 2 (in the kicker) | 0 | 2 | 0 in story, 1 in ad |
| Words a minute | 184 | 171 | 177 | 174 |

### The page formula (from 4 reels, a hypothesis)
| # | Beat | Where | What it does | Example |
|---|---|---|---|---|
| 1 | Superlative photo hook | 0 to 4 s | "This is / This might be the most [X] [person or photo] in [world]" over one famous photo | "the most important photo in startup history" |
| 2 | Pop-culture or rival comparison | 4 to 8 s | Makes a stranger care: a film character or a famous rival group | "basically Tony Stark in real life", "the PayPal mafia might finally be getting some competition" |
| 3 | Name drop plus the paradox | 8 to 17 s | "His name's X, and the same thing that made him Y nearly destroyed him" | ACK, PAL |
| 4 | Dated run of events with printed numbers | 15 to 55% | Short active sentences, each with a picture and a number | MBIA 2002, $1.4 billion, $43 million, $6,000 check |
| 5 | Rule-break soundbite | about 40 to 80% | The real person or a film says the key line | Karp "on occasion kill them", Ackman at Forbes |
| 6 | Turn | 35 to 75% | Reframes what we thought the story was | "Palmer's only the side piece", "and lost everything" |
| 7 | Zoom out to now | 75 to 90% | Ties it to the viewer's world or today | "the internet you scroll", "some CEO just found out" |
| 8 | Mirrored kicker | last 2 sentences | Two parallel lines, the second flips the first. No lesson | "Neither does Ackman." |
| 9 | Paid only: bridge plus "Comment WORD" | last 9 to 11 s | One line links the story to the sponsor, then the offer | "Comment GUIDE and we'll share..." |

### Where this page differs from the AC formula (`story-script-writer/references/ac-formula.md`)
1. **The name is held back.** AC names a famous person at once. This page shows the photo and a comparison first and names the person at 8 to 17 s.
2. **A comparison line is a fixed slot** ("basically X in real life"). Not in AC.
3. **The ending is a mirrored couplet, every time.** AC returns to a planted detail. Here the return is shaped as two parallel sentences.
4. **"You" appears near the end** (PAL kicker, EIN zoom-out). AC almost never uses "you".
5. **Networks, not only one person:** PayPal Mafia, Palantir Mafia, YC. Step 3 of AC (one person's drive) is weaker in PAL and YC, and both still scored 20.
6. **Explaining runs higher in PAL and EIN** (32 to 47% explaining words), above AC's 4 to 31%. The story still lands because each explainer is followed by a picture or a soundbite.
7. **The paid version adds a commercial tail and a bridge line.** AC has none.
8. **Same as AC:** about 230 to 250 words for organic reels, 170 to 185 words a minute, average sentence 12 to 14 words, no business lesson, one turn.

---

## 8. Idea selection: what this page picks and why

Read with `skills/idea-finder` (Big score: who, mass appeal, consequence, freshness; then the Story score).

**What the 4 have in common**
- **Who:** famous tech or money names a stranger half-knows (Thiel, Palantir, Ackman, Icahn, Sam Altman, Reddit, Twitch, Einstein, ChatGPT). Hashtags: #founder #startups #investor #palantir.
- **The angle is a hidden link or backstory, not news:** "it all traces back to", "the same thing that made him", "it all starts with the kid next to Paul Graham". The viewer learns who is behind something they already know.
- **A network or group lens** appears in 3 of 4 (Palantir Mafia, PayPal Mafia twice, the YC batch, 17 Nobel winners in one frame).
- **An evergreen story with a present-day hook:** "right now", "$122 billion, the largest private round in history", "the reason we even have AI today". No reel is pegged to one news event that we can see.
- **One iconic photo exists for the hook.** All 4 start on one.
- **Power and money stakes:** weapons and surveillance, a $1.4 billion win and a billion lost, the largest private round.
- **Sponsor fit for paid posts:** startups and investing (YC) and "what top companies almost got wrong" (EIN), both matching a venture product.

**The Story-score pattern** (from `idea-finder`'s skeleton): a person or group, real stakes, a turn, 2 to 3 dated beats, a planted detail, an ending that flips the hook, visual proof (film, real clips, receipts), and an angle other pages miss (Palmer as "only the side piece").

**What a next idea needs to fit (judged checklist)**
1. A famous photo or a famous group in one frame.
2. A name a stranger half-knows, plus a film or pop-culture comparison.
3. A paradox or hidden link in one sentence.
4. 2 to 4 events with numbers you can print.
5. A real clip where the subject says the key line.
6. A present-day zoom-out that touches the viewer ("you").
7. A mirrored kicker that writes itself.

**What 4 reels cannot tell us**
- Views, reach, retention or saves. Only likes and comments, and only for these 4 posts.
- Which ideas this page tried and dropped, or what flopped.
- How often it posts, and what share is paid.
- Whether the voice is one narrator, a hired voice or AI. Not heard.
- The music tracks, and whether sound effects are used.
- Whether the topics follow news timing (for example, an Ackman news spike before 10 Sep).
- Whether the M sting and the inverted cut are fixed rules or a 2026 phase (EIN has neither, and it is the odd one out).

---

## 9. Shot-to-word reading (summary)

Full per-shot log: `SHOT-LOG.md`. Device counts below are from reading every shot-word sheet, judged by eye.

| Device (word-matched-broll terms) | PAL | ACK | EIN | YC |
|---|---|---|---|---|
| Burst (several 2 to 6 frame images on one idea) | squeamish valley (3 founders), PayPal mafia grid | 8 banks, 6 banknotes, "lost everything" | Nobel names, "the chip" | YC startups (Airbnb, DoorDash, Coinbase) |
| Hold of 2 s or more on proof | Karp soundbite 4.3 s, receipt 2.1 s | news anchor 2.4 s, Forbes clip 1.8 s, film tail 6.6 s | Bohr explainer 7.3 s (particles), cream ad tail 8.8 s | "$43 Million" 1.3 s, ad tail 10 s |
| News proof (chyron or anchor) | 60 Minutes Thiel | "2008 MARKET MELTDOWN", "WORST NOT OVER?", "MBIA Q2 RESULTS", "ON THE PHONE" Icahn | none | TED stage, Reddit slide |
| Symbol | chess rook and king, explosion, network map | blow-up explosion, pyramid, Pac-Man, eye on a dollar | dice, atoms, planet, semiconductor | money stack, camcorder |
| Printed number | $10,000.00 | 2002, 2008, 1.4 billion, 35% | 17, 100 years, 13 | $43 Million, $6 thousand, 122 billion, Five thousand |
| White or black breath card | white "valley" card (23.4 s) | white frames as cuts only | white and black word cards (18.6, 24.1, 55.0, 66.2 s) | black and white word cards (2.2 to 3.6, 24.5 to 26.8, 45.1 to 45.8, 56.0 s) |
| Built object | receipt UI, framed photo, illustrated room | polaroid board (17.2 s) | polaroid board, chat UI, report page | camcorder, folder icon |
| Callback | PayPal photo and mafia grid at the end | Wolf of Wall Street at the end | the Solvay photo, "God doesn't play dice" | the YC photo, again and again |
| Film or pop culture | Iron Man, likely The Godfather | The Wolf of Wall Street, Pac-Man | none | 1980s trading floor (source not identified) |

Breath cards are more common here than in AC: white or black cards carrying small words appear every 10 to 20 s in EIN and YC.

---

## 10. Use, change or drop

Where it goes: S = script stage (`story-script-writer`), I = idea pick (`idea-finder`), E = edit plan (`word-matched-broll` storyboard), M = motion layer (`effects-library`, AE), C = captions, A = audio, F = finish.

1. **USE: landscape 16:9, 1920x1080, 25 fps.** Where: intake (`video-agent` step 4). Every reel is landscape. Our default is vertical, so this must be set on purpose.
2. **USE: the superlative photo hook**, "This is / This might be the most [X] ... ", over one famous photo. Where: S hook, I (the idea must come with an iconic photo).
3. **USE: the 3x3 grid block reveal** of that photo in the first 1 to 1.3 s. Where: M, effect #1. Pilot it first, per the repo's 3-second pilot rule.
4. **USE: name held back to 8 to 17 s,** with a film or rival comparison first. Where: S. This changes the AC habit of naming first.
5. **USE: the paradox line** "the same thing that made him X nearly Y". Where: S beat 3.
6. **USE: the mirrored two-line kicker.** Where: S outro. Write it before the body so the body plants it.
7. **USE: pace targets:** median 0.55 to 0.75 s, 7 to 9 shots in the first 5 s, about 1.1 to 1.5 cuts a second, cuts on word starts and not on the beat. Where: E. Check the build with `ref_stats.py` against section 2.
8. **USE: small word-by-word captions,** Inter Medium (closest free match), cap height about 38 px on 1080, centred at about 50% height, words spread across the frame, black on white frames. Plus 8 to 15 big bold words a reel. Where: C. Needs a new per-word caption script (effect #8): `style_captions.py` cannot place words across the frame. Show a side-by-side crop before the full build.
9. **USE: the inverted-frame cut,** about 1 every 3 to 5 s on sentence turns, not on every cut. Where: M, effect #5. PAL shows the page can run with far fewer, so start near ACK and YC's rate and let the user pick.
10. **USE: white paper cards and prints** (11 to 14% bright frames) as breath beats every 10 to 20 s. Where: E, M #15.
11. **USE: one real soundbite** where someone else owns the key line. Where: S beat 5, E. Rights: see 14.
12. **USE: printed numbers and logo bursts** for every figure and every list. Where: E, M #11 and #12.
13. **USE: a loud music bed,** 1 to 4 dB under the voice in gaps, with the voice nearly non-stop at 170 to 185 words a minute. Where: A (`gap_level.py` to check the mix).
14. **CHANGE: film and pop-culture clips** (Iron Man, The Wolf of Wall Street, likely The Godfather). They are central to the organic style, but their rights are unclear. Where: E footage map. The user must decide the rights rule before the footage map (`edit-loop-guard` loop 4). Fallback: real news and interview footage of the subject, plus a printed comparison line.
15. **CHANGE: the M logo sting.** It is Metro's brand mark. Ending on the kicker plus a callback shot keeps the rhythm without copying the mark. Where: F. If the user wants a sting, we design our own.
16. **CHANGE: the photo walk-through** (B&W except the named person, white silhouette flash). Use it only when the idea is a group photo, as in YC. Where: M #14, I.
17. **CHANGE: the ending type.** Build the organic ending by default. Add the 9 to 11 s ad tail only if the user says the post is a paid placement. Where: S, F.
18. **CHANGE: explaining runs.** PAL (32%) and EIN (47%) explain more than AC's ceiling. Keep the page's habit of following each explainer with a picture or soundbite, but hold our script to 2 explaining sentences in a row. Where: S language pass.
19. **DROP: the EIN look as a page template** (71% monochrome, typing-cursor block, no inverted cuts). It is USVC's account. Where: style law, marked as a cousin.
20. **DROP: thermal flash and red neon outline as defaults.** Each was seen once (ACK). Keep them in the effect list for one big moment at most. Where: M, opening budget (`edit-loop-guard` loop 5).
21. **DROP: anything that copies the page's exact assets:** its M mark, its exact captions or its exact layouts frame for frame. Same look and rhythm, our own footage, type set from scratch and our own designs. Where: all stages.
22. **OPEN for the user, before scripting:**
    a. Is our video organic or a paid placement? Default: organic.
    b. Rights rule for film clips and news footage. Default: real interviews and news only, no feature films.
    c. Topic: should the next idea come from the gaps in section 8 (a famous network photo plus a paradox)? Default: yes, run `idea-finder` with the section 8 checklist and bring back 3 to 5 candidates.
    d. Voice: we could not hear theirs. Default: pick by ear against the reels.
