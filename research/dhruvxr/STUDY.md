# dhruvxr: page study (2 X videos)

Study date: 5 Nov 2026. Branch `job/dhruvxr`, made from `research/metro-media-house`. Videos in `x-videos/` (from branch `reference-reels`).
Claude read every frame, the transcripts and measurements. Claude did not watch playback or hear audio.

| Code | File | Post text | What it is (judged) |
|---|---|---|---|
| WHP | `_dhruvxr_2116246221421780992` | "Recent wrap, @whop did we cook?" | A client brand film for Whop: voice-over, Whop UI, Whop logo end card |
| ATN | `_dhruvxr_2109649042661908480` | "You can't guess how many diet cokes it took me to finish this overnight." | A self-made manifesto: text only over music, a voice sample in the first 5 s, signed "dhruv" |

So the page reads as a **motion designer's portfolio on X**: one client job, one personal piece. Judged from 2 posts only.

---

## 1. The short version
1. Both are 16:9, 1280x720, about 30 fps, 15 to 16.5 s. Both end with a small centred mark on black (Whop wordmark 2.4 s, "dhruv" 2.7 s).
2. **Mostly black and white.** 86 to 97% of pixels are near grey and 63 to 78% near black. Colour comes only from product or brand pieces (orange checkout button, brand logos, a red-orange skier).
3. **The first second is a micro-montage.** WHP has 8 shots and ATN 9 shots in the first 1 s, mostly 2 to 4 frames each. After that the pace drops to holds of 1 to 2.4 s.
4. **Very few words.** WHP shows about 12 words on screen and ATN 20. They're small, grey-white, sentence case, in a clean sans. One idea per card, about 1 s per card in ATN.
5. **Tech and design imagery:** product UI tilted in 3D, terminal logs, website walls, design-tool selection boxes, brand profile cards. Both include an MRI head clip.
6. **Dot and particle forms** carry WHP (a logo made of dots, a keyhole of dots, star particles, a dot globe). ATN instead uses compositing: cards reflected in an eye, a cut-out skier over swapping paintings.
7. **Sound:** WHP is a brand voice-over (15 words) over music, with level hits that land on picture changes (12 of 22 jumps, against 27% chance). ATN is a voice sample for the first 5 s, then a bass drop at 5.1 s on the turn card "Attention". In neither video do cuts follow the music beat (at or below chance).
8. **Loudness differs a lot:** WHP -14.1 LUFS, ATN -5.4 LUFS with a +2.1 dBFS peak (clipped).

---

## 2. Numbers per video
Shots are from the hand shot list (`raw/shots_by_hand.json`), because `cut_events.py` merged WHP's first 17 frames into one event and missed dark-to-dark cuts (ATN 5.11 s). Tool counts are shown too.

| Measure | WHP | ATN | Range |
|---|---|---|---|
| Format | 1280x720, 30 fps | 1280x720, 29.97 fps | 16:9 landscape |
| Length | 16.49 s (494 f) | 14.95 s (448 f) | 15 to 16.5 s |
| Shots, by hand | 31 | 26 | 26 to 31 |
| Cut events, tool (`cut_events.py`) | 17 (9 CUT, 6 CUT+FLASH, 2 FLASH) | 21 (20 CUT, 1 FLICKER) | |
| Median shot | 0.20 s (6 f) | 0.13 s (4 f) | 4 to 6 f |
| Shots of 4 frames or less | 11 (35%) | 15 (58%) | 35 to 58% |
| Longest shot | 2.43 s (wordmark end) | 2.87 s (black tail) | |
| Shots in first 1 s / first 3 s | 8 / 15 | 9 / 11 | 8 to 9 / 11 to 15 |
| White flash frames (1 to 3 f) | 5 events (f10, f45, f78-80, f195-196, f243-244, f322) | 0 | 0 to 5 |
| Text elements | 11 (plus UI and logs) | 9 (plus brand card UI) | |
| Words on screen (copy, not UI) | about 12 | 20 | 12 to 20 |
| Spoken words (faster-whisper) | 15 (brand VO) | 13 (voice sample, 0 to 5.2 s) | |
| Tempo, `beat_map.py` | 67 BPM, weak fit (17% onsets on grid vs 11% chance) | 73.25 BPM, weak fit (24% vs 12%) | low confidence |
| Cuts on beat grid (`beat_map.py`, ffmpeg cuts) | 11% vs 16% chance | 0% vs 17% chance | at or below chance |
| Cuts on strong onsets (top 3%, ±2 f) | 13% vs 24% chance | 10% vs 26% chance | below chance |
| Text in-times on strong onsets | 30% vs 25% (n=10) | 40% vs 26% (n=10) | slightly above, small n |
| Level jumps of 6 dB+ landing within 0.1 s of a shot change | 12 of 22 (55%) vs 27% chance | 2 of 11 vs 24% | WHP only |
| Loudness (EBU R128) | -14.1 LUFS, LRA 3.1, peak +0.1 dBFS | -5.4 LUFS, LRA 3.8, peak +2.1 dBFS | |
| Mean brightness | 0.14 | 0.25 | 0.14 to 0.25 |
| Near-black pixels | 78% | 63% | |
| Near-grey pixels | 97% | 86% | |
| Mean saturation | 0.02 | 0.06 | |
| Vivid pixels | 0.3% | 2.2% | |
| Vivid hue: red plus orange/yellow | 74% | 51% | |
| Vivid hue: cyan/blue | 25% | 40% | |

Against the metro page and the repo's references: brightness 0.37 to 0.46 there, 0.14 to 0.25 here. Median shot 0.54 to 0.80 s there, 0.13 to 0.20 s here. This page is far darker and faster, and has almost no words.

---

## 3. How far to trust each number
| Number | Trust | Why |
|---|---|---|
| Length, fps, resolution | High | ffprobe |
| Hand shot list | High, ±1 frame | Read on every-frame strips. Where a shot starts during a dissolve, it's my call |
| Tool cut events | Low here | Thresholds set on Altman. They merged the first 0.57 s of WHP and missed dark cuts |
| Text in and out frames | High, ±1 frame | Every-frame crops in `text/` |
| Text size and position | Medium | `tools/text_box.py` ink box, ±2 px. Ink height runs ascender to descender, not cap height. A3, A7b and A8 picked up background, so I judged their sizes by eye |
| Fonts | Judged | No font fit was run. Closest free match by eye |
| Tempo | Very low | Full mix, no stem, weak fits. ATN bass hits at 5.1, 7.6, 10.1 and 12.6 s are 2.5 s apart, which could be one bar at about 96 BPM. That's judged |
| Cuts vs beat | Medium | Both tests agree that cuts are not beat-synced. The onsets are dense, so the chance rates are high |
| Level jumps vs shot changes | Medium | 0.1 s windows. They suggest designed hits in WHP, but I haven't heard any of them |
| Voice vs music sections | Medium | Speech-band share plus Whisper word times. Not heard |
| LUFS, peak | High | ffmpeg ebur128 |
| Colour | Medium | `colour_stats.py` at 2 fps. Fine as a warning light |

Not checked at all: playback, sound, the identity of the voice or sample, music track IDs, which sounds are SFX and which are music, views and likes, the page's other posts.

---

## 4. Style law (rebuild spec)
Tags: **BOTH** = in both videos. **WHP** or **ATN** = in one video only.

### Frame and length
- BOTH: 16:9 1280x720, 30 fps (29.97 in ATN), 15 to 16.5 s, posted on X.
- BOTH: Black is the base. Mean brightness 0.14 to 0.25, near-black 63 to 78%.
- BOTH: Monochrome footage. Colour only on the product or brand pieces.
- WHP: Fine vertical-line screen texture over the live footage (f11 to f111, f323 to f342). Judged on full-resolution frames.
- ATN: Grain and a soft vignette on the eye and the website wall.

### Pace
- BOTH: First 1 s = 8 to 9 shots of 1 to 4 frames. That's the hook: a burst of images on one idea (ideas and objects in WHP; famous brands in ATN).
- BOTH: After the burst, holds of 0.9 to 2.4 s, one card or one form at a time.
- BOTH: A second, shorter burst later on (WHP f322 to f342: 4 shots in 0.7 s; ATN f192 to f215: 7 backgrounds at 3 frames each).
- BOTH: The last 2.5 to 5.7 s are near-empty: a small mark on black, then black or a fade.
- BOTH: Cuts don't follow the beat. In WHP the sound hits follow the picture instead (judged from level jumps).

### Type
- BOTH: Clean neo-grotesk sans, sentence case, lower case where possible. Closest free matches: Inter Regular or Medium. ATN reads close to SF Pro Text. Judged, not fitted.
- BOTH: Grey-white ink, not pure white, on black: #AA to #DF. Near white (#F7) on bright snow.
- BOTH: Small. Most body text has an ink height of 2.2 to 4.6% of frame height (16 to 33 px on 720). One bigger line per video: ATN "It gets ignored." at 7.8% and "It's earned" at about 10%; WHP's wordmark at 5%.
- WHP: Labels in italic with slashes, like code comments: "// Ideas //", "@ Ideas //", "// Audience 0", "@/ visibility //". They sit in the corners (x 8 to 18% or 82 to 90%; y 17% or 80 to 84%) with a soft glow.
- WHP: Concept word plus phonetics: "ownership" at x 26 to 35%, y 27%, and "/ˈōnərˌSHip/" at x 71 to 82%, y 77%. They drift apart by about 25 px over 60 frames.
- ATN: Lines centred vertically at 50 to 54%. They're split across the width ("attention isn't earned" on the left, "by features." on the right) or set word by word with wide gaps ("a     great     prduct").
- ATN: One deliberate misspelling, "prduct". Judged deliberate.
- ATN: The thesis word "It's earned" sits in a 1 px white design-tool selection box with handles (f222 to f245).

### Text animation (frames at 30 fps)
- WHP: Labels blur in over 2 to 3 frames (f21 to f23) and cut out with their shot (f74).
- WHP: Big word flash: "Audience" for 2 frames only (f76 to f77), italic with glow.
- WHP: "ownership" fades up over 2 frames (f132 to f133), holds, and fades out over 8 frames after a white flash (f197 to f204).
- WHP: The wordmark reveals right to left over 3 frames (f421 to f424), then fades up over 7 frames (to f431).
- ATN: Words add one at a time: "a" at f2, "great" at f6, "prduct" at f12, about every 4 to 6 frames, in step with the card changes. They dim and blink at f25 to f29 as the shot changes.
- ATN: "It gets ignored." reveals right to left over 6 frames (f122 to f127).
- ATN: Most cards change with a hard cut on the shot change.
- ATN: The end mark "dhruv" appears with no fade (f310), holds 56 frames, then fades out over about 24 frames (f366 to f390).

### Copy
- BOTH: 12 to 20 words on screen in total. 1 to 5 words per card. About 1 s per card in ATN.
- WHP: Concept nouns that the voice-over joins up: Ideas, Audience, visibility, ownership, this, then the brand.
- ATN: A 4-step argument: claim ("a great prduct / Isn't enough anymore."), problem ("It gets ignored."), turn ("Attention / attention isn't earned by features."), thesis ("It's earned / by perception."). Then the sign-off.

### Picture content
- BOTH: Stock-like monochrome footage of hands, eyes, crowds and people, plus an MRI head clip. WHP f8 to f9 and ATN f153 to f179.
- BOTH: Screens tilted in 3D. WHP's checkout UI (f91 to f111); ATN's curved wall of websites (f67 to f152).
- BOTH: A digital glitch moment between 1.4 and 4.3 s. WHP's scan-line tear with log list (f112 to f129); ATN's rectangle-offset insert (f42 to f50).
- WHP: Dot-matrix forms throughout: logo, keyhole, globe, and a logo built from photo tiles that bursts into a collage.
- ATN: Real brand profile cards (Apple, Meta, Whop, Wise, Figma, Adobe, an orange asterisk mark, ChatGPT) at 2 to 4 frames each.
- ATN: A cut-out subject (the skier) stays put while the background swaps every 3 frames.

### Sound
- BOTH: Music runs to the last frame. There's no silence except WHP's final 0.5 s fade (15.96 s on).
- WHP: Opening sub-bass hit from 0.1 to 1.6 s at about 0 dB RMS in 0.1 s windows. Then a dip (-26 dB at 2.1 to 2.6 s). Then hits on picture changes, at 2.8 (crowd), 3.9 (glitch), 4.4 (keyhole), 6.4 (white flash), 7.9 to 8.3 (logo bloom), 9.7 (tiles), 11.0 (stairs) and 14.1 (wordmark). Voice-over from 1.4 to 15.3 s, 15 words.
- ATN: A voice sample from 0.0 to 5.2 s (high speech-band share, 0.6 to 1.0). Bass drop at 5.0 to 5.1 s on the "Attention" cut. Bass hits at 6.8, 7.7, 9.2, 10.1 and 12.6 s. Loud the whole way through (-5.4 LUFS).

### Ending
- BOTH: A small centred mark on black, held 2.4 to 2.7 s. WHP shows the client's logo and wordmark; ATN the creator's lower-case name.
- ATN: Hard cut to black for 1.0 s first, and black again for 2.0 s after.

---

## 5. Effect list with frames and rebuild notes
Headline effects (one or two per post): **WHP**: dot-matrix forms, and the white-flash monochrome micro-montage. **ATN**: the brand-card montage reflected in an eye, and the held cut-out over swapping backgrounds.
Evidence: `strips/all_*.jpg` (every frame), `text/*.jpg` (every frame of text boxes), `frames/*.jpg` (full resolution), `raw/*/evsheet/`.
Engine note: After Effects and Premiere aren't in this environment. Every rebuild below is planned for ffmpeg plus PIL/numpy, unless noted.

| # | Effect | Frames | What happens | Rebuild | Repo cover |
|---|---|---|---|---|---|
| 1 | Opening micro-montage | WHP f0 to f45; ATN f0 to f29 | Shots of 1 to 4 frames, hard cuts. WHP has white flashes at f10 and f45 | Cut list in the build script | Yes, plain cuts |
| 2 | Logo or form made of dots, with a soft bloom | WHP f0 to f3, f245 to f286; white bloom f243 to f244 | Shape rendered as a grid of square dots with a soft radial glow. The glow shrinks as the camera pulls back (f245 to f286) | PIL dot grid over a mask, plus a Gaussian glow stack | `native-looks.md` §3 halftone and §4 glow; effects-library #12 (AE) |
| 3 | Vertical-line screen texture | WHP live footage | Fine vertical stripes over the picture | 1 px line overlay at about 5 to 8% | None. Trivial to add |
| 4 | Corner code labels, blurring in | WHP f21 to f23 in, f74 out | Italic grey text with glow; blur goes to sharp over 3 f | PIL text, 3 blur steps | `titles-captions-type.md` §2 smooth arrival |
| 5 | Two-frame big word | WHP f76 to f77 | "Audience", italic, glow, over the crowd | One text layer for 2 frames | Yes |
| 6 | White blowout into 1-bit threshold | WHP f78 to f85 | Exposure to white over 3 f, then hard threshold for 5 f | numpy levels plus threshold per frame | `transitions.md` light blow-out (music-edit kin) |
| 7 | Product UI tilted in 3D, focus pull | WHP f91 to f111 | 2-frame blur-in, perspective tilt, slow drift, dark surround | PIL perspective warp, two-key drift | effect-library `screen-photo-push` (partly) |
| 8 | Scan-line tear plus log list | WHP f112 to f129 | Horizontal bands shift, white bars, a log list flashes. 18 f | numpy band shifts per frame | effects-library #13 glitch burst (partly). Check against the box-glitch verdict |
| 9 | Fade from white into a dot form, with drifting labels | WHP f130 to f194 | White, grey, dark over 3 f. Dot clusters drift. Two labels drift about 25 px in opposite directions | PIL; each drift is two keys | Partly |
| 10 | Two-frame white flash, then dots become particles that converge into a logo | WHP f195 to f243 | Stars drift and gather over 46 f, then a 2-frame bloom | numpy particles with eased paths | effect-library `particle-mind` (partly) |
| 11 | Logo of photo tiles bursts into a collage, camera pushing | WHP f287 to f321 | Tiles become photos. "this" moves with the world and leaves at the edge | PIL layers with a 2-key camera scale | effect-library `video-wall` (partly) |
| 12 | Slow-shutter monochrome footage | WHP f323 to f330 | People smeared | Shoot at a slow shutter, or frame echo | effects-library #9 slow_shutter (AE) |
| 13 | Rotating dot globe, fading out | WHP f343 to f410 | Dot sphere with a faint red tint, dims over about 60 f | numpy orthographic dot sphere | `native-looks.md` §8 (AE). Easy in numpy |
| 14 | Wordmark right-to-left wipe, then fade up | WHP f421 to f431 | 3 f wipe plus 7 f fade | PIL mask wipe | Yes |
| 15 | Brand profile card montage, words adding one by one | ATN f0 to f29 | Card = logo tile, name, verified badge, bio, banner, at 4 f each. "a", "great", "prduct" add on | HTML cards in headless Chrome, or PIL | `production-automation` card pipeline |
| 16 | Montage reflected in an eye | ATN f30 to f66 | Card montage composited inside the iris. Random red and cyan character text at the left. Slow push | Mask composite plus a character-grid layer | `native-looks.md` §9 character grid (AE) |
| 17 | Rectangle glitch insert | ATN f42 to f50 | Offset rectangles of other frames, a zoomed copy of the line, colour blocks | numpy | Box-glitch family; banned in music edits only |
| 18 | Curved 3D wall of website screens | ATN f67 to f152 | Screens fly in and stack, a hero screen lands at f104, then everything darkens to black | PIL perspective per card; two-key moves | None direct |
| 19 | Right-to-left text reveal | ATN f122 to f127; WHP f421 to f424 | The end of the line shows first | Mask wipe | Yes |
| 20 | Held cut-out over swapping backgrounds | ATN f180 to f215 | The skier stays put while 7 backgrounds change every 3 f | Needs a matted subject plus a backgrounds list | Person matte: `person_mask.js` is Mac only. Here a green-screen or pre-keyed clip is needed |
| 21 | Cylinder-wrapped repeated word, inverted window, selection handles | ATN f216 to f221 | Text scrolls around a 3D cylinder; a negative window shows the subject | numpy per-column warp | None in the repo |
| 22 | Word in a design-tool selection box | ATN f222 to f245 | 1 px box with corner handles around the line | PIL | None; trivial |
| 23 | Hard cut to black, then sign-off | ATN f279 to f447 | 31 f black, name with no fade, 56 f hold, 24 f fade out, black | PIL | Yes |

---

## 6. Timeline by second
### WHP (30 fps)
| s | Picture | Text | Effect | Sound (measured level, judged role) |
|---|---|---|---|---|
| 0 to 1 | Dot logo, bulb, flare, MRI, white, pen, desk, pen line | "// Ideas //" in at f21, "@ Ideas //" at f28 | Micro-montage, white flash f10 | Sub hit from 0.1 s at about 0 dB |
| 1 to 2 | Calligraphy pen, white f45, ink drip | Labels hold | White flash | Hit continues to 1.6 s; VO "Ideas." 1.40 to 2.00 |
| 2 to 3 | Ink drip, crowd, white blowout, threshold crowd, crowd from above | "Audience" f76 to f77; "// Audience 0" f81 to f95; "@/ visibility //" f84 to f95 | Blowout, threshold | Dip to -26 dB, hit at 2.8 |
| 3 to 4 | Checkout UI tilted, scan-line tear | UI text | 3D tilt, glitch | Hit at 3.9 |
| 4 to 6 | Log list, white to keyhole of dots | "ownership" f132, phonetics f138 | Fade from white, drift | Hit at 4.4; VO "Ownership." 4.48 to 5.58 |
| 6 to 8 | White f195 to f196, star particles | Labels fade out f197 to f204 | Particles | Hit at 6.4; VO "Every business. One checkout." 6.56 to 8.88 |
| 8 to 10 | White logo bloom, glowing mark pulling back, mark of tiles | "this" f287 | Bloom | Hit at 7.9 to 8.3; VO "This is" 9.90 |
| 10 to 12 | Collage, white f322, slow-shutter crowd, stairs, fisheye, dot globe | "this" again f316 to f321; "$150M"; "[ 14:02 ]" | Second burst | Hit at 11.0; VO "where the internet gets paid." to 12.48 |
| 12 to 14 | Globe fading, black | none | | About -18 dB bed |
| 14 to 16.5 | Whop wordmark | Wordmark f421 on | Wipe plus fade | Hit at 14.1; VO "Whop.com" 14.28 to 15.30; fade to silence 15.96 to 16.49 |

Hook in the first 1 s: rapid "ideas" objects, plus the brand mark at frame 0. Turn: the product UI at 3.0 s, then "ownership". End: logo plus voice tagline.

### ATN (29.97 fps)
| s | Picture | Text | Effect | Sound |
|---|---|---|---|---|
| 0 to 1 | Brand cards every 4 f: Apple, Meta, Whop, Wise, Figma, Adobe, asterisk, ChatGPT | "a" f2, "great" f6, "prduct" f12 | Card montage | Voice sample "Yo," 0.0 to 0.46 |
| 1 to 2.2 | Eye macro with the cards in the iris | "Isn't enough anymore." f30 to f66 | Reflection composite, glitch insert f42 to f50 | Sample "if you don't shut your mouth," 1.0 to 2.6 |
| 2.2 to 5.1 | Curved wall of websites, darkening | "It gets ignored." f122 to f152 | 3D wall, right-to-left reveal | Sample "I'ma shut it for you, PUNK!" 3.06 to 5.16 |
| 5.1 to 6 | MRI head slices | "Attention" f153 to f179 | Hard cut on the drop | **Bass drop at 5.0 to 5.1** |
| 6 to 7.2 | Skier, then 7 backgrounds at 3 f each | "attention isn't earned" plus "by features." f180 to f215 | Held cut-out | Bass hit at 6.8 |
| 7.2 to 8.2 | Cylinder word wrap, then a boxed word over the skier | "It's earned" f216 to f245 | Wrap, selection box | Bass hit at 7.7 |
| 8.2 to 9.3 | Skier downhill | "by perception." f246 to f278 | | |
| 9.3 to 15 | Black, name, black | "dhruv" f310 to about f390 | Hard cut to black | Bass hits at 9.2, 10.1, 12.6; loud to the end |

Hook in the first 1 s: famous brand logos plus "a great prduct". Turn: the drop plus "Attention" at 5.1 s (34% in). End: the thesis, then a black sign-off.

---

## 7. Copy
### WHP (the voice carries the sentence; the screen shows nouns)
| Time | On screen | Spoken | Role |
|---|---|---|---|
| 0.70 to 2.47 | "// Ideas //", "@ Ideas //" | "Ideas." | Hook: the first value |
| 2.53 to 3.17 | "Audience", "// Audience 0", "@/ visibility //" | (none heard by Whisper) | Problem: nobody sees you (judged) |
| 3.03 to 3.70 | Checkout UI: "Checkout", "Pro membership", "$49.00", "Pay $49.00" | | Product |
| 4.40 to 6.80 | "ownership", "/ˈōnərˌSHip/" | "Ownership." | Value |
| 6.5 to 8.9 | none | "Every business. One checkout." | Product claim |
| 9.57 to 10.70 | "this", "$150M", "[ 14:02 ]" | "This is where the internet gets paid." | Tagline |
| 14.03 to 16.49 | Whop logo plus wordmark | "Whop.com" | Call to action: the brand |
On-screen copy words: about 12. Voice: 15 words in 4 phrases.

### ATN (the screen carries the whole argument)
| Card | Frames | Duration | Words | Role |
|---|---|---|---|---|
| "a great prduct" | f2 to f29 | 0.9 s | 3 | Hook claim |
| "Isn't enough anymore." | f30 to f66 | 1.2 s | 3 | Problem |
| "It gets ignored." | f122 to f152 | 1.0 s | 3 | Problem, made concrete |
| "Attention" | f153 to f179 | 0.9 s | 1 | Turn (on the drop) |
| "attention isn't earned" "by features." | f180 to f215 | 1.2 s | 5 | Old belief |
| "It's earned" | f216 to f245 | 1.0 s | 2 | Thesis, part 1 |
| "by perception." | f246 to f278 | 1.1 s | 2 | Thesis, part 2 |
| "dhruv" | f310 to about f390 | 2.7 s | 1 | Sign-off |
Total: 20 words across 8 cards. 1 to 5 words per card, median 2.5. 0.9 to 1.2 s per card, about 2 to 4 words a second. There's a 2.4 s gap with no text (f67 to f121), where the picture carries "ignored".

---

## 8. What 2 videos cannot tell us
- Views, likes, reposts or retention for either post (none on file).
- The page's other posts, how often it posts, and whether client wraps or personal pieces do better.
- Whether the WHP voice is a hired voice, AI or the client's own. Not heard.
- The music tracks and the source of the voice sample (not to be identified).
- Which level hits are sound effects and which are music.
- Whether ATN had permission for the brand logos. WHP's Whop assets were presumably provided by the client (the post tags @whop); that's not confirmed.
- What tools they used (After Effects, Blender, Figma), beyond what the frames suggest.
- Whether 16:9 and 15 s are fixed rules or chance.

---

## 9. Use, change or drop
Where: I = idea, S = script and copy, A = audio, E = edit plan and storyboard, M = motion, T = type, F = finish, R = rights.

1. **USE: 16:9, 15 to 16.5 s, 30 fps.** Where: intake. Default delivery 1920x1080 at 30 fps (the reference is 1280x720; we can deliver both).
2. **USE: a black, monochrome base.** Colour only on our product or brand piece. Target brightness 0.14 to 0.25, near-black at least 60%, near-grey at least 85%. Where: E colour plan, checked with `colour_stats.py`.
3. **USE: the first-second micro-montage.** 8 to 9 shots of 1 to 4 frames, all on one idea. Where: E. This breaks the repo's opening limits (they were set for narrated mini-docs), so the budget needs your call (question 7).
4. **USE: one form or card per hold after the burst,** 0.9 to 2.4 s each, plus one second burst after the middle. Where: E.
5. **USE: small grey-white sans type,** Inter Regular or Medium. Ink height 2.2 to 4.6% of frame height, colour #AA to #DF on black. One larger line (8 to 10%) for the thesis. Where: T.
6. **USE: 12 to 20 words on screen,** 1 to 5 words per card, about 1 s per card. Where: S.
7. **USE: text motion from the references only:** 3-frame blur-in, word-by-word add-on every 4 to 6 f, right-to-left reveal over 3 to 6 f, hard cuts, and a final mark that appears with no fade and fades out over about 24 f. Where: M.
8. **USE: one dot-matrix form** (our own mark or object as square dots with a soft bloom), with a 2-frame white bloom on a hit. Where: M #2, #10.
9. **USE: one tilted 3D product screen** with a 2-frame focus pull. It must be our own product UI, or a UI designed from scratch. Where: M #7, R.
10. **USE: one digital glitch moment between 1.4 and 4.3 s,** 9 to 18 frames, band shifts. Where: M #8. I'll show 3 or 4 strengths first.
11. **USE: the drop on the turn card.** Picture cuts stay off the beat grid; sound hits land on picture changes instead (WHP: 12 of 22 hits). Where: A, E.
12. **USE: a small centred mark on black as the ending,** held 2.4 to 2.7 s, with the music playing through. Where: F.
13. **USE: monochrome stock-like footage of hands, eyes and crowds,** licensed or shot by us. Where: E asset map, R.
14. **CHANGE: the voice.** WHP has a brand voice-over; ATN has a voice sample. Pick by format (question 2). Any sample must be licensed and logged in SOURCES.txt. Where: A.
15. **CHANGE: the brand-logo montage (ATN f0 to f29).** Real logos of Apple, Meta, Whop, Wise, Figma, Adobe and ChatGPT are other companies' trademarks. Default: our own designed fictional marks, or products we have rights to show. Where: R, E.
16. **CHANGE: loudness.** ATN sits at -5.4 LUFS with a +2.1 dBFS peak, which is clipped. Default target: -9 to -10 LUFS, true peak -1 dBTP. That's loud like the page, but not clipping (judged). Where: A, F.
17. **CHANGE: the cut-out over swapping backgrounds (ATN #20).** Only if we have a subject on green screen or a clean matte; there's no matting tool for Linux in the repo. Where: E, M.
18. **CHANGE: the cylinder text wrap (ATN #21).** No repo tool covers it. Build it only if the script's thesis word needs it, and pilot it first. Where: M.
19. **DROP: the "dhruv" sign-off and the Whop logo and wordmark.** Ours ends on our own name or mark. Where: F.
20. **DROP: copying any frame, layout or asset:** their keyhole, their Whop UI, their exact card designs and their "prduct" typo. We use the same kind of devices, built from scratch. Where: all stages.
21. **DROP: the MRI head as a must.** It's in both videos, but copying it would read as a copy. Keep it only if the idea needs it. Where: E.
22. **OPEN (Gate 1 questions):** see HANDOFF.md and the Gate 1 report.
