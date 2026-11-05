# 05 dhruvxr rule book

Version 2 (final, 07:52 UTC, 5 Nov 2026). Source: `research/dhruvxr/STUDY.md` (cited as §), with shot start frames from `research/dhruvxr/raw/shots_by_hand.json`. Nothing here is new measurement; every number comes from the study, except percentages and pixel sizes worked out here from its numbers.

How to read this:
- **USE** = do it as measured. **CHANGE** = keep the device, change the number, source or scope. **DROP** = do not do it.
- **[M]** = measured in the study. **[J]** = judged (by eye, or a default picked here). Claude did not watch playback or hear audio (§3).
- Frame numbers: WHP at 30 fps, ATN at 29.97 fps. We build at 30 fps, so ATN frame numbers can be used as-is (drift under 1 frame over 15 s: 14.95 s x 0.03 f/s = 0.45 f).
- Gate 1 defaults (BRIEF.md) are applied: spec piece in ATN style (text manifesto over music, no client logos), sign-off "[STUDIO]", no real third-party logos, one idea in the first 3 s, -9 to -10 LUFS and -1 dBTP, ffmpeg plus PIL/numpy only.
- WHP-only devices are marked "optional" when the spec piece is ATN style.

---

## 1. Format
- **R1 USE.** 16:9 landscape. Deliver 1920x1080 (default, §9.1) and a 1280x720 copy to match the references. Ex: WHP and ATN are both 1280x720 [M, ffprobe].
- **R2 USE.** 30 fps constant. Ex: WHP 30 fps, ATN 29.97 fps [M].
- **R3 USE.** Length 15.0 to 16.5 s. Default 15.0 s = 450 f [J default]. Ex: WHP 16.49 s (494 f), ATN 14.95 s (448 f) [M].
- **R4 USE.** Engine is ffmpeg plus PIL/numpy. No After Effects or Premiere (§5 engine note). Every effect in section 8 must have a numpy or PIL plan before it goes in the edit.

## 2. Pace
- **R5 USE.** Total shots 26 to 31 for 15 to 16.5 s. Median shot 4 to 6 f. 35 to 58% of shots are 4 frames or less. Ex: WHP 31 shots, median 6 f, 35% at 4 f or less; ATN 26 shots, median 4 f, 58% [M, hand shot list, ±1 f].
- **R6 USE.** After the opening burst, one card or one form per hold. Holds 0.9 to 2.4 s (27 to 72 f). Ex: ATN "Attention" f153 to f179 (0.9 s); ATN "Isn't enough anymore." f30 to f66 (1.2 s); WHP keyhole of dots f130 to f194 (65 f, 2.2 s) [M].
- **R7 USE.** One second, shorter burst after the middle: 4 to 7 shots of 1 to 8 f (3 f each in ATN) within 0.7 to 0.8 s, placed between 43% and 69% of the run time. Ex: ATN f192 to f215 (7 backgrounds at 3 f each, 6.4 to 7.2 s, 43 to 48% in); WHP f322 to f342 (4 shots in 0.7 s, 10.7 to 11.4 s, 65 to 69% in) [M; percentages computed here].
- **R8 USE.** Cuts stay off the beat grid. Do not snap cuts to beats. Ex: cuts on the beat grid WHP 11% vs 16% chance, ATN 0% vs 17% chance [M, medium trust]. Sound hits follow picture instead (R60).
- **R9 USE.** The last 2.5 to 5.7 s carry no new idea: only the end mark and black (section 11). Ex: ATN f279 to f447 (5.6 s); WHP wordmark f421 to f494 (2.4 s) [M].

## 3. Opening
- **R10 USE.** First 1 s (f0 to f29) = 8 to 9 shots, mostly 1 to 4 f each, hard cuts. Ex: WHP 8 shots in the first 1 s; ATN 9 shots, brand cards every 4 f at f0 to f29 [M].
- **R11 USE.** Shots in the first 3 s (f0 to f89): 11 to 15. Ex: WHP 15, ATN 11 [M].
- **R12 USE.** Every burst shot is on one idea. Ex: ATN f0 to f29 = famous products, all saying "a great product"; WHP f0 to f29 = idea objects (bulb, pen, desk, pen line) [J].
- **R13 USE.** Gate 1: one idea, readable, by 3.0 s (f90). The first word lands by f2 to f21. Ex: ATN "a" f2, "great" f6, "prduct" f12, claim done "Isn't enough anymore." by f66 (2.2 s); WHP first label f21 (0.7 s) [M].
- **R14 CHANGE.** The opening card montage uses our own designed fictional marks, never real brands. Ex: ATN f0 to f29 shows Apple, Meta, Whop, Wise, Figma, Adobe, an orange asterisk mark and ChatGPT [M]. See R69.
- **R15 CHANGE.** White flash frames (1 to 3 f) are a WHP device. ATN-style default: 0 in the opening, at most 1 in the whole piece [J default]. Ex: WHP flashes at f10, f45, f78 to f80, f195 to f196, f243 to f244, f322 (the study counts 5 events, its list shows 6 positions); ATN has 0 [M].

## 4. Type
- **R16 USE.** Clean neo-grotesk sans: Inter Regular or Medium. Ex: both videos; ATN reads close to SF Pro Text [J, no font fit run]. Do not use SF Pro (its licence was not checked here).
- **R17 USE.** Sentence case, lower case where possible. Ex: ATN "attention isn't earned" f180 to f215, "dhruv" f310; WHP "ownership" f132, "this" f287 [M].
- **R18 USE.** Ink colour grey-white #AA to #DF on black, never pure #FFFFFF. Near white #F7 only on a bright background. Ex: ATN text on black; #F7 on the bright snow in the ATN skier shots [M, medium].
- **R19 USE.** Body text ink height 2.2 to 4.6% of frame height: 16 to 33 px at 720, 24 to 50 px at 1080. Ink height runs ascender to descender, not cap height [M, ±2 px].
- **R20 USE.** At most 2 lines larger than body, at 7.8 to 10% of frame height (56 to 72 px at 720, 84 to 108 px at 1080). The largest goes on the thesis. Ex: ATN "It gets ignored." 7.8% (f122 to f152), "It's earned" about 10% (f216 to f245) [M and J; §3 says some sizes were judged by eye].
- **R21 USE.** Lines centred vertically at 50 to 54% of frame height. Either split across the width or set word by word with wide gaps. Ex: ATN f180 to f215 "attention isn't earned" left, "by features." right; ATN f2 to f29 "a     great     prduct" [M].
- **R22 CHANGE.** Corner code labels are WHP only; optional, at most 1 pair, our own words. If used: italic, slashes like code comments, x 8 to 18% or 82 to 90%, y 17% or 80 to 84%, soft glow. Ex: WHP "// Ideas //" f21, "@ Ideas //" f28, "// Audience 0" f81 to f95 [M].
- **R23 CHANGE.** Concept word plus phonetics is WHP only; optional. If used: word at x 26 to 35%, y 27%; phonetics at x 71 to 82%, y 77%. Ex: WHP "ownership" f132 and "/ˈōnərˌSHip/" f138 [M].
- **R24 DROP.** The "prduct" misspelling. A deliberate typo of our own is allowed only if the script needs it, max 1 [J]. Ex: ATN f12 to f29 [M].

## 5. Text motion
Only the moves in R25 to R31 are allowed (§9.7).
- **R25 USE.** Default: text cuts in and out hard, with its shot. Ex: most ATN cards change on the shot cut; WHP labels cut out with their shot at f74 [M].
- **R26 USE.** Word-by-word add-on, one word every 4 to 6 f, in step with the card changes. Ex: ATN "a" f2, "great" f6, "prduct" f12 [M].
- **R27 USE.** Right-to-left reveal (end of the line shows first) over 3 to 6 f, mask wipe. Ex: ATN "It gets ignored." f122 to f127 (6 f); WHP wordmark f421 to f424 (3 f) [M].
- **R28 USE.** Blur-in from soft to sharp over 2 to 3 f, 3 blur steps. Ex: WHP labels f21 to f23 [M].
- **R29 USE.** Fade up over 2 f; fade out over 8 f, after a white flash. Ex: WHP "ownership" up f132 to f133, out f197 to f204 [M].
- **R30 USE.** Dim and blink on a shot change, about 5 f. Ex: ATN f25 to f29 [M].
- **R31 USE (optional).** Two-frame big word flash, once at most. Slow drift of about 25 px over 60 f, two keys, two labels in opposite directions. Ex: WHP "Audience" f76 to f77; WHP "ownership" and phonetics drift from f138 [M].
- **R32 DROP.** Every other text move: bounces, overshoot, per-letter pops, typewriter cursor, slides, 3D flips, scale punches [J, from §9.7 "text motion from the references only"].

## 6. Copy
- **R33 USE.** 12 to 20 words on screen in total, not counting UI. ATN-style default: 16 to 20 [J default]. Ex: ATN 20 words across 8 cards; WHP about 12 [M].
- **R34 USE.** 1 to 5 words per card, median 2 to 3. Each card 0.9 to 1.2 s (27 to 36 f). About 2 to 4 words a second. Ex: ATN median 2.5 words, 0.9 to 1.2 s per card [M].
- **R35 USE.** The 4-step argument: claim, problem, turn, thesis, then sign-off. Ex: ATN claim f2 to f66, problem f122 to f152, turn f153 to f179, old belief f180 to f215, thesis f216 to f278, sign-off f310 [M].
- **R36 USE.** The turn is 1 word, alone on its card, at about 34% of run time, on a hard cut with the drop. On 450 f that is f153 (5.1 s). Ex: ATN "Attention" f153 to f179, 5.1 s of 14.95 s [M].
- **R37 USE.** The thesis is split across 2 cards. Ex: ATN "It's earned" f216 to f245, "by perception." f246 to f278 [M].
- **R38 USE.** One gap of about 2.4 s (about 72 f) with no copy, where the picture carries the word. Ex: ATN f67 to f121, picture carries "ignored" [M].
- **R39 DROP.** Their lines and their argument. No "a great product isn't enough", no "attention isn't earned by features", no "earned by perception" [J, from §9.20 "drop copying"].

## 7. Picture content
- **R40 USE.** Monochrome stock-like footage of hands, eyes, crowds and people, licensed or shot by us. Ex: WHP hand writing f16 to f23, crowd f76 to f90; ATN eye macro f30 to f66 [M frames from `raw/shots_by_hand.json`, J content].
- **R41 USE.** One screen tilted in 3D, with a 2-frame focus pull. It must be our own product UI or a UI designed from scratch. Ex: WHP checkout UI f91 to f111; ATN curved wall of websites f67 to f152 [M].
- **R42 USE.** Tech and design imagery: UI, terminal-style logs, walls of screens, design-tool selection boxes, profile cards. Ex: WHP log list f112 to f129; ATN selection box f222 to f245 [M].
- **R43 USE.** One digital glitch moment between 1.4 and 4.3 s (f42 to f129), 9 to 18 f long. Ex: WHP scan-line tear f112 to f129 (18 f); ATN rectangle-offset insert f42 to f50 (9 f) [M].
- **R44 DROP.** The MRI head as a must. Use it only if the idea needs it. Ex: WHP f8 to f9, ATN f153 to f179 [M].
- **R45 CHANGE.** Cut-out subject held over swapping backgrounds: only with a green-screen or pre-keyed clip (no Linux matting tool in the repo). Ex: ATN skier f180 to f215, 7 backgrounds at 3 f each [M].

## 8. Effects
- **R46 USE.** One or two headline effects per piece, no more. Ex: WHP dot-matrix forms plus white-flash montage; ATN eye reflection plus cut-out over backgrounds [J, §5].
- **R47 USE.** Montage composited inside an eye (iris mask), slow push, with a red and cyan character-grid layer at the left. Ex: ATN f30 to f66 [M]. Needs a licensed eye macro.
- **R48 USE.** 1 px white design-tool selection box with corner handles around the thesis line. Ex: ATN f222 to f245 (24 f) [M].
- **R49 USE.** Curved 3D wall of our own screens: screens fly in and stack, a hero screen lands, then all darkens to black. Ex: ATN f67 to f152, hero at f104 [M].
- **R50 USE (optional, max 1).** One dot-matrix form: our own mark or object as square dots with a soft Gaussian bloom, 2-frame white bloom on a hit. Ex: WHP f0 to f3, f245 to f286, bloom f243 to f244 [M].
- **R51 USE (optional).** White blowout to 1-bit threshold: exposure to white over 3 f, then hard threshold for 5 f. Ex: WHP f78 to f85 [M].
- **R52 CHANGE.** Glitch strength: pilot 3 or 4 strengths first (§9.10). The repo bans box glitch in music edits; whether this piece counts as a music edit was not checked. Ex: WHP band shifts f112 to f129; ATN boxes f42 to f50 [M].
- **R53 CHANGE.** Cylinder-wrapped word: only if the thesis word needs it; pilot first; no repo tool. Ex: ATN f216 to f221 [M].
- **R54 USE.** Texture: grain plus a soft vignette on footage and screen walls. Optional WHP line screen: 1 px vertical lines at about 5 to 8% opacity over live footage. Ex: ATN eye f30 to f66 and wall f67 to f152; WHP f11 to f111, f323 to f342 [J, seen on full-res frames].
- **R55 USE.** Camera moves are two-key drifts or pushes. No hand-keyed paths. Ex: WHP drift f130 to f194, collage push f287 to f321 [J, §5 rebuild notes].
- **R56 DROP.** Copying their effects as built: their keyhole, their Whop UI, their card designs, their particle-to-Whop-logo, their globe. Same kind of device, built from scratch [§9.20].

## 9. Colour
- **R57 USE.** Black base. Mean brightness 0.14 to 0.25. Near-black pixels at least 60% (ref 63 to 78%). Near-grey pixels at least 85% (ref 86 to 97%) [M, `skills/minidoc-reference-style/scripts/colour_stats.py` at 2 fps, medium trust].
- **R58 USE.** Monochrome footage. Colour only on our own product or brand piece. Mean saturation 0.02 to 0.06; vivid pixels 0.3 to 2.2%. Fail above saturation 0.08 or vivid 3% [M ref; J fail margin]. Ex: WHP orange checkout button f91 to f111; ATN red-orange skier f180 to f278 [M].
- **R59 USE.** Accent hues: red plus orange/yellow first (51 to 74% of vivid pixels), cyan/blue second (25 to 40%). No full-frame grade or tint; the only tint in the refs is the faint red on the WHP dot globe f343 to f410 [M].

## 10. Sound
- **R60 USE.** Sound hits land on picture changes: at least half of the 6 dB+ level jumps within 0.1 s (3 f) of a shot change. Ex: WHP 12 of 22 (55%) vs 27% chance; hits at 2.8, 3.9, 4.4, 6.4, 7.9 to 8.3, 9.7, 11.0, 14.1 s [M, medium; J that they are designed].
- **R61 USE.** The drop lands on the turn card cut. Ex: ATN bass drop at 5.0 to 5.1 s on "Attention" f153 [M].
- **R62 USE.** Music runs to the last frame. No silence, except an end fade of at most 0.5 s. Ex: WHP fade 15.96 to 16.49 s; ATN loud to the end [M].
- **R63 CHANGE.** Voice. ATN-style default: no voice-over, music only. A voice sample in the first 5 s (ATN 0.0 to 5.2 s, 13 words) only if licensed and logged in SOURCES.txt. Never reuse or recreate the ATN sample. Brand voice-over (WHP 1.4 to 15.3 s, 15 words) is for client films only [M times].
- **R64 CHANGE.** Loudness -9 to -10 LUFS integrated, true peak -1 dBTP or lower. Ex: ATN -5.4 LUFS, +2.1 dBFS peak (clipped); WHP -14.1 LUFS, +0.1 dBFS peak. Keep LRA near the refs, 3.1 to 3.8 LU [M; target from Gate 1].

## 11. Ending
- **R65 CHANGE.** The end mark is "[STUDIO]" (our studio mark placeholder), small and centred on black. Mark ink height about 5% of frame height (36 px at 720, 54 px at 1080) [M for WHP wordmark at 5%; "dhruv" size not measured].
- **R66 USE.** ATN tail: hard cut to black for 31 f, mark appears with no fade, holds 56 f, fades out over about 24 f, then black about 57 f to the end. Ex: ATN black f279 to f309, "dhruv" f310, fade f366 to f390, black to f447 [M].
- **R67 USE.** Mark on screen 2.4 to 2.7 s (72 to 81 f). Music plays through. Ex: WHP wordmark 2.4 s, ATN "dhruv" 2.7 s [M].
- **R68 DROP.** The "dhruv" sign-off, the Whop logo and wordmark, the right-to-left wordmark wipe as a copy, and any voice tagline. Ex: ATN f310; WHP f421 to f494 [§9.19].

## 12. Rights
- **R69 DROP.** Real third-party logos and brand cards (Apple, Meta, Whop, Wise, Figma, Adobe, ChatGPT, the asterisk mark), and real platform badges. Our own fictional marks only. Ex: ATN f0 to f29 [Gate 1; badge rule J].
- **R70 DROP.** Copying any frame, layout, asset or line from WHP or ATN (§9.20).
- **R71 USE.** All footage, stills, UI and sound are ours or licensed, and each is logged in SOURCES.txt (file, source, licence, frames used) [J format].
- **R72 DROP.** The reference music and voice sample. Do not try to identify or reuse them (§8).
- **R73 USE.** Fonts with an open licence only (Inter is SIL OFL). Whether Inter is installed here was not checked.

---

## Checklist for a finished render (one page)
Tick each line. Any "no" is a fail unless the rule says optional.

**Format and pace**
- [ ] 16:9, 1920x1080 (plus 1280x720 copy), 30 fps constant, 15.0 to 16.5 s. (R1 to R3; ffprobe)
- [ ] 26 to 31 shots, median 4 to 6 f, 35 to 58% at 4 f or less. (R5; every-frame strip)
- [ ] Holds after the burst 0.9 to 2.4 s. One second burst of 4 to 7 shots at 43 to 69% in. (R6, R7)
- [ ] Cuts not snapped to the beat grid. (R8)

**Opening**
- [ ] f0 to f29: 8 to 9 shots, 1 to 4 f each, one idea. f0 to f89: 11 to 15 shots. (R10 to R12)
- [ ] First word by f21; first idea readable by f90. (R13)
- [ ] No real brand in the burst. (R14, R69)

**Type, motion, copy**
- [ ] Inter, sentence case, ink #AA to #DF (#F7 only on bright ground). (R16 to R18)
- [ ] Body ink height 24 to 50 px at 1080; at most 2 big lines at 84 to 108 px. (R19, R20)
- [ ] Lines centred at 50 to 54% height. (R21)
- [ ] Only allowed moves: hard cut, word add-on every 4 to 6 f, right-to-left reveal 3 to 6 f, blur-in 2 to 3 f, fade 2 f up / 8 f out, blink. (R25 to R32)
- [ ] 12 to 20 words total, 1 to 5 per card, 27 to 36 f per card. (R33, R34)
- [ ] Claim, problem, turn, thesis, sign-off. Turn = 1 word at about 34% (f153 on 450 f). (R35, R36)
- [ ] No line taken from ATN or WHP. (R39, R70)

**Picture, effects, colour**
- [ ] One glitch, 9 to 18 f, inside f42 to f129. (R43)
- [ ] One or two headline effects only. (R46)
- [ ] Mean brightness 0.14 to 0.25; near-black at least 60%; near-grey at least 85%. (R57; `colour_stats.py`)
- [ ] Mean saturation at most 0.08; vivid pixels at most 3%; colour only on our own piece. (R58, R59)

**Sound**
- [ ] Integrated -9 to -10 LUFS; true peak -1 dBTP or lower. (R64; ffmpeg ebur128 with true peak)
- [ ] Drop on the turn card cut. Half or more of the 6 dB+ hits within 3 f of a cut. (R60, R61)
- [ ] Music to the last frame; any end fade 0.5 s or less. (R62)
- [ ] Any voice sample licensed and in SOURCES.txt. (R63)

**Ending and rights**
- [ ] Last 2.5 to 5.7 s: black, "[STUDIO]" centred at about 5% height, on 72 to 81 f, no fade in, about 24 f fade out. (R65 to R67)
- [ ] No "dhruv", no Whop, no third-party logo or badge anywhere. (R68, R69)
- [ ] Every asset logged in SOURCES.txt. (R71)

---

## Not checked for this book
- Playback and sound: Claude did not watch or hear either video. Sound rules rest on level and speech-band measures (§3).
- Fonts: no font fit was run; Inter is a judged match. Whether Inter is installed here, and the SF Pro licence, were not checked.
- Whether the repo's box-glitch ban applies to this piece (R52).
- Whether 16:9 and 15 s are the page's fixed rules or chance: 2 posts only (§8).
- The study says WHP has 5 white flash events but lists 6 positions (R15). Not re-counted.
- Defaults picked here, not measured: 15.0 s length (R3), 0 to 1 white flash (R15), 16 to 20 words (R33), saturation and vivid fail margins (R58), "[STUDIO]" mark size at 5% (R65).
