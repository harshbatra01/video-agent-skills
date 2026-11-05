# 02 Look, colour and type (dhruvxr: WHP + ATN)
Version: final, 07:52 UTC. Tags: **MEASURED** = numpy on decoded frames in this sprint. **STUDY** = taken from research/dhruvxr/STUDY.md section 4, not re-measured. **JUDGED** = my reading of numbers; Claude cannot watch the videos.

## Outputs
- `sheets/WHP_shots_sheet.jpg`, `sheets/ATN_shots_sheet.jpg`: one frame per shot (the middle frame of each hand-cut shot in research/dhruvxr/raw/shots_by_hand.json), 256x144 thumbs, labelled with shot, frames, length and mean luma.
- `sheets/WHP_placement_map.jpg`, `sheets/ATN_placement_map.jpg`: every text element with a known position, on a 10% grid.
- Method: ffmpeg `select` decodes the mid frame of every shot at 1280x720; numpy measures. Luma Y = Rec.709 weights on RGB 0 to 1. Saturation = HSV S on pixels with Y > 0.05. Vivid = S > 0.35 and max channel > 0.25. Texture = std of (Y minus a 1.5 px Gaussian blur), in 8-bit levels; dark grain = the same, only on pixels with Y < 0.12. dx/dy = mean absolute column-to-column difference over row-to-row difference (1.0 = no direction; above 1 = vertical-line structure; below 1 = horizontal structure).

## 1. Colour and grade: the rules
- MEASURED: Black is the base. Time-weighted mean luma (mid frame of each shot, weighted by shot length) WHP 0.157, ATN 0.239; near-black (Y < 0.10) WHP 76%, ATN 60%. This agrees with STUDY (0.14 to 0.25, 63 to 78%). Black shots and end cards read Y 0.000 to 0.002, true #000000. The footage black point (p1) is 0 to 4 levels on almost every dark shot: blacks are crushed to 0, not lifted.
- MEASURED: White points (p99) are 200 to 255 on live footage. White flashes are full #FFFFFF (WHP f195 to f196, Y 1.000) or near it (#FCFCFC at f10, #E5E5E5 at f322).
- MEASURED: Live footage is monochrome. WHP sat is 0.000 to 0.006 on 24 of 31 shots; colour shows only on the checkout UI (vivid 2.6%, #DE3C0F, hue 13 deg), the photo collage (5.7%) and the dot globe (0.65%, #793B43, hue 352 deg, a faint red).
- MEASURED: ATN has more colour, all from third-party pieces: brand cards (Whop #AB271C, Wise #67A45B, Figma #79A550, Adobe #910E16, Meta #3C50A4), the eye macro (warm skin #8D5749, 11% vivid), sky behind the skier (#6B8FB0, hue 209 deg) and the old paintings (#6B5139, #80644A, #295352, #624339). The MRI head and two statues are near grey (sat 0.03 to 0.10); the angel statue reads 0.197.
- MEASURED: Contrast is high. Luma std 45 to 98 levels on WHP live footage, p95 minus p5 up to 252 (WHP threshold crowd). ATN snow shots are softer (std 19 to 33). Dot-form shots are low std (16 to 20) because they are 94 to 98% black.
- MEASURED: Brightness swings shot to shot: WHP goes 0.018, 0.275, 0.037, 0.075, 0.988 across its first 5 shots (f0 to f10). The hook is a flicker of dark and bright, not a steady grade.
- JUDGED: Grade recipe for our spec: desaturate footage fully (sat 0), crush blacks to 0, keep whites at 235 to 255, let contrast run high, and allow colour only on one object per shot.

## 2. Grain and texture
- MEASURED: Dark-area grain (hp std in Y < 0.12) runs 1.0 to 5.6 levels in WHP (14.87 on the scan-line glitch shot, which is glitch, not grain) and 0.8 to 5.9 in ATN. Highest: ATN eye macro 5.89, WHP keyhole 5.59, WHP pen macro 5.15. Clean graphics read 0.0 to 0.1 (WHP star field 0.11, black cards 0.00).
- MEASURED: Vertical-line texture in WHP: dx/dy 7.56 (terminal crowd), 8.18 (spiral stairs), 5.10 (fisheye), 4.43 (white flash f322), 2.78 (pen line), 2.49 (calligraphy). This backs STUDY's fine vertical-line screen. On other WHP footage dx/dy is 0.48 to 1.65, so the texture is either weak there or masked by content. Content can also push dx/dy; not checked by eye.
- MEASURED, new: ATN's background-swap shots (f192 to f215) read dx/dy 0.09 to 0.32 on all 7 frames: strong horizontal structure, like scan lines or interlace. JUDGED: likely a horizontal line overlay on those backgrounds. Not confirmed by eye; check a full-res frame before copying.
- JUDGED rebuild: grain = Gaussian noise, sigma about 3 to 5 levels, on footage only, never on type or black cards. Line screen = 1 px lines every 2 to 3 px at 5 to 8% opacity (STUDY suggestion), vertical for WHP-style, horizontal for ATN background swaps.

## 3. Palette (hex)
| Role | Hex | Source |
|---|---|---|
| Base black, cards, end | #000000 | MEASURED, black shots Y 0.000 |
| Dark footage mean | #040404 to #131313 | MEASURED, mean hex of dot forms and dark shots |
| Mid footage greys | #777777, #7C7C7C, #818181, #8B8B8B | MEASURED, WHP hand, pen and ink shots |
| Light footage grey | #AAAAAA to #B7B7B7 | MEASURED, WHP pen line, crowd |
| Body ink, core | #C8C8CA to #F3F5F7 | MEASURED, brightest 1% of ATN text crops on black |
| Body ink, mean with edges | #AA to #DF grey | STUDY |
| End mark peak | #FCFCFC (dhruv, 252), #F2F2F2 (WHP wordmark at f440, 242) | MEASURED |
| Flash white | #FFFFFF | MEASURED, WHP f195 |
| Snow light (ATN skier) | #DDDFDE mean, #C6D2D7 | MEASURED |
| Accent seen (do not copy, third-party brand colours) | #DE3C0F, #AB271C, #910E16, #67A45B, #3C50A4 | MEASURED |
| Faint red tint (WHP globe) | #793B43 | MEASURED |
- JUDGED: For our ATN-style spec use #000000 ground, ink #E6E6E6 (core) with anti-aliased edges, footage greys from the table, and no accent unless the [STUDIO] mark has its own colour. The accent list above is brand colour from Whop and the ATN cards, so keep it out.

## 4. Type: style, size and placement
- STUDY: Neo-grotesk sans, sentence case or lower case. Closest free match Inter Regular or Medium. ATN close to SF Pro Text. Judged, not fitted.
- MEASURED: Ink core is grey-white, not pure white: ATN "It gets ignored." #C8C8CA; "a great prduct" #ECECEE; "Isn't enough anymore." #F2F1F3; "Attention" #F3F5F7; sign-off "dhruv" #EDECEC in the crop, 252 peak in the video.
- Not measured: ink colour on bright snow (A7 to A9 crops read #FEFFFF but the brightest 1% there is the snow, not the ink). STUDY gives #F7 there.
- STUDY: Body ink height 2.2 to 4.6% of frame height (16 to 33 px on 720). Big lines: ATN "It gets ignored." 7.8%, "It's earned" about 10%.
- MEASURED: WHP wordmark ink box x 43.8 to 56.2%, y 47.5 to 52.4%, height 5.0% (36 px) at f440. ATN "dhruv" x 46.4 to 53.4%, y 48.2 to 51.7%, height 3.6% (26 px) at f340. Both dead centre.

### Placement map (x and y in % of frame; see sheets/*_placement_map.jpg)
| Reel | Element | Frames | x % | y % | Size (ink height) | Source |
|---|---|---|---|---|---|---|
| WHP | "// Ideas //" corner label, top left | f21 to f74 | 8 to 18 | 17 | 2.2 to 4.6% range | STUDY |
| WHP | "@ Ideas //", "// Audience 0", "@/ visibility //" corner labels | f21 to f111 | 82 to 90 (or 8 to 18) | 80 to 84 (or 17) | 2.2 to 4.6% range | STUDY |
| WHP | "Audience" big word | f76 to f77 | not measured | not measured | bigger than labels | STUDY |
| WHP | "ownership" | f132 to f204 | 26 to 35 | 27 | not measured | STUDY |
| WHP | "/ˈōnərˌSHip/" | f132 to f204 | 71 to 82 | 77 | not measured | STUDY |
| WHP | "this" | f287 to f300 | moves with world | moves | not measured | STUDY |
| WHP | Whop wordmark | f421 to f493 | 43.8 to 56.2 | 47.5 to 52.4 | 5.0% (36 px) | MEASURED |
| ATN | "a great prduct", word by word, wide gaps | f2 to f29 | spread across width | 50 to 54 | 2.2 to 4.6% range | STUDY |
| ATN | "Isn't enough anymore." | f30 to f66 | not measured | 50 to 54 | 2.2 to 4.6% range | STUDY |
| ATN | "It gets ignored." | f122 to f152 | not measured | not measured | 7.8% | STUDY |
| ATN | "Attention" | f153 to f179 | not measured | 50 to 54 | not measured | STUDY |
| ATN | "attention isn't earned" left, "by features." right | f180 to f215 | left half, right half | 50 to 54 | 2.2 to 4.6% range | STUDY |
| ATN | "It's earned" in 1 px selection box | f222 to f245 | not measured | 50 to 54 | about 10% | STUDY |
| ATN | "by perception." | f246 to f278 | not measured | 50 to 54 | not measured | STUDY |
| ATN | "dhruv" | f310 to f390 | 46.4 to 53.4 | 48.2 to 51.7 | 3.6% (26 px) | MEASURED |
- JUDGED rule for our spec: one line per card on the 50 to 54% band, ink 2.2 to 4.6% high, one thesis line at 8 to 10%, sign-off centred at about 3.6%.

## 5. Motion graphics (what moves, frames, eases)
| What | Frames | Measurement | Ease (JUDGED from the curve) |
|---|---|---|---|
| ATN "dhruv" sign-off | on f310, hold f310 to f347 (38 f), fade f348 to f390 (43 f) | peak 0 to 252 in 1 frame; then 246, 241, 236 ... 12, 6, 0, about 5.9 levels a frame | Hard on, linear fade out |
| WHP wordmark | reveal f421 to f424, fade f421 to f440+ | right band (x 50 to 62%) lights at f421 to f422, left band (x 37 to 50%) at f424; peak 12, 80, 146, 191, 220, 234, 240, 242 | Right-to-left wipe; ease-out fade (steps 68, 66, 45, 29, 14, 6) |
| WHP dot globe fading | f343 to f397 | mean luma 5.8 to 1.0; slow 5.8 to 3.7 over f345 to f375, then 3.7 to 1.1 over f376 to f391 | Ease-in (speeds up at the end) |
| WHP flash into keyhole | f129 to f133 | mean 183, 249, 130, 31, 2.4 | White to dark in 3 f, near linear |
| WHP "ownership" exit after flash | f197 to f205 | peak 65, 58, 50, 42, 35, 29, 25, 21, 20 | Linear, easing out over the last 2 f |
| ATN word blink at card change | f25 to f30 | text band peak 171, 93, 5, 99, 177, 237 | V-shaped dip, linear down and up, 5 f |
| ATN MRI head hold | f153 to f179 | mean luma 10.0 to 8.4 | Slow linear darken |
| ATN skier hold, "by perception." | f246 to f278 | mean luma 221.8 to 225.1, then black at f279 | Slow linear brighten, hard cut out |
| ATN cut into skier | f179 to f181 | mean 8.4, 146.9, 194.7 | One in-between frame (not checked by eye) |
- MEASURED, new: WHP's wordmark fade (f421 to f435) and dot globe (f343 to f396) change value only every 3 frames. JUDGED: those graphics were animated at 10 updates a second inside the 30 fps edit ("on threes"). Rebuild: render those graphics at 10 fps and hold each frame for 3.
- STUDY, not re-measured: WHP labels blur in over 2 to 3 f (f21 to f23) and cut out with the shot (f74). "Audience" shows for 2 f. "ownership" fades up over 2 f (f132 to f133). The labels drift apart about 25 px over 60 f. ATN words add at f2, f6, f12. "It gets ignored." reveals right to left over 6 f (f122 to f127). The website wall flies in from f67, hero lands at f104, all darkens to black by f152. Particles converge over 46 f (f197 to f242). The glow shrinks as the camera pulls back (f245 to f286).
- Disagreement: STUDY says "dhruv" holds 56 f and fades over about 24 f (f366 to f390). My per-frame peak (99.95th percentile) starts falling at f348. STUDY may have judged visibility by eye on strips. Use my numbers for the curve; the end frame agrees (f390).

## 6. Per-shot numbers (MEASURED)

### WHP per shot (mid-shot frame, full 1280x720)

Time-weighted mean luma 0.157; time-weighted near-black (Y<0.10) 76%; shots with vivid pixels >1%: 2 of 31.

| # | frames | len f | label | mean Y | near-black % | sat | vivid % | vivid hue deg | vivid hex | black p1 | white p99 | contrast std | texture hp std | dark grain | dx/dy | mean hex |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0-3 | 4 | Whop mark of dots | 0.018 | 97.4 | 0.046 | 0.00 | - | - | 1 | 122 | 19.6 | 6.62 | 3.15 | 1.00 | #040404 |
| 2 | 4-5 | 2 | light bulb | 0.275 | 49.8 | 0.002 | 0.00 | - | - | 17 | 234 | 78.5 | 2.54 | 1.14 | 1.17 | #464646 |
| 3 | 6-7 | 2 | flare threshold | 0.037 | 93.8 | 0.006 | 0.00 | - | - | 0 | 207 | 39.2 | 5.98 | 3.55 | 1.16 | #090909 |
| 4 | 8-9 | 2 | MRI head front | 0.075 | 82.4 | 0.005 | 0.00 | - | - | 0 | 176 | 45.0 | 8.09 | 4.7 | 1.04 | #131313 |
| 5 | 10-10 | 1 | white flash | 0.988 | 0.3 | 0.000 | 0.00 | - | - | 150 | 255 | 20.7 | 3.11 | - | 1.85 | #FCFCFC |
| 6 | 11-15 | 5 | pen macro | 0.509 | 4.5 | 0.000 | 0.00 | - | - | 2 | 239 | 56.9 | 3.14 | 5.15 | 1.65 | #818181 |
| 7 | 16-23 | 8 | hand writing desk | 0.468 | 15.1 | 0.000 | 0.00 | - | - | 1 | 246 | 76.0 | 2.72 | 2.48 | 0.48 | #777777 |
| 8 | 24-32 | 9 | pen line | 0.670 | 0.0 | 0.000 | 0.00 | - | - | 43 | 248 | 60.6 | 2.32 | - | 2.78 | #AAAAAA |
| 9 | 33-44 | 12 | calligraphy pen low | 0.490 | 21.9 | 0.000 | 0.00 | - | - | 0 | 234 | 79.7 | 2.93 | 0.96 | 2.49 | #7C7C7C |
| 10 | 45-45 | 1 | white flash | 0.870 | 9.4 | 0.000 | 0.00 | - | - | 0 | 255 | 79.7 | 2.75 | 2.96 | 1.10 | #DDDDDD |
| 11 | 46-75 | 30 | ink drip macro | 0.549 | 8.0 | 0.000 | 0.00 | - | - | 4 | 220 | 61.6 | 4.32 | 3.96 | 1.55 | #8B8B8B |
| 12 | 76-77 | 2 | crowd + Audience | 0.720 | 2.8 | 0.000 | 0.00 | - | - | 17 | 245 | 66.6 | 6.12 | - | 1.00 | #B7B7B7 |
| 13 | 78-80 | 3 | white blowout | 0.902 | 0.0 | 0.000 | 0.00 | - | - | 43 | 255 | 51.9 | 2.07 | - | 1.47 | #E6E6E6 |
| 14 | 81-85 | 5 | threshold crowd | 0.302 | 55.9 | 0.037 | 0.00 | - | - | 1 | 255 | 97.6 | 7.03 | 4.27 | 1.22 | #4D4C4E |
| 15 | 86-90 | 5 | crowd top-down | 0.124 | 67.1 | 0.030 | 0.00 | - | - | 0 | 200 | 45.9 | 6.10 | 3.6 | 1.19 | #1F1F20 |
| 16 | 91-111 | 21 | checkout UI tilted | 0.035 | 90.0 | 0.241 | 2.57 | 13 | #DE3C0F | 0 | 102 | 20.2 | 5.29 | 2.79 | 0.96 | #0C0806 |
| 17 | 112-129 | 18 | scan-line glitch + log list | 0.801 | 12.8 | 0.000 | 0.00 | - | - | 0 | 255 | 91.3 | 9.11 | 14.87 | 0.22 | #CCCCCC |
| 18 | 130-194 | 65 | keyhole of dots, ownership | 0.017 | 97.5 | 0.000 | 0.00 | - | - | 0 | 115 | 20.0 | 10.64 | 5.59 | 1.03 | #040404 |
| 19 | 195-196 | 2 | white flash | 1.000 | 0.0 | 0.000 | 0.00 | - | - | 255 | 255 | 0.0 | 0.00 | - | 0.00 | #FFFFFF |
| 20 | 197-242 | 46 | star particles | 0.012 | 99.7 | 0.000 | 0.00 | - | - | 0 | 12 | 4.5 | 0.90 | 0.11 | 0.93 | #030303 |
| 21 | 243-244 | 2 | white logo bloom | 0.839 | 0.0 | 0.000 | 0.00 | - | - | 131 | 255 | 38.7 | 4.53 | - | 1.20 | #D5D5D5 |
| 22 | 245-286 | 42 | glowing mark | 0.037 | 94.3 | 0.000 | 0.00 | - | - | 1 | 88 | 17.4 | 1.61 | 1.03 | 1.00 | #090909 |
| 23 | 287-300 | 14 | mark of photo tiles, this | 0.008 | 98.3 | 0.182 | 0.16 | - | - | 0 | 86 | 16.3 | 5.18 | 3.01 | 0.99 | #020202 |
| 24 | 301-321 | 21 | photo collage | 0.073 | 83.2 | 0.319 | 5.68 | 223 | #5F615E | 0 | 197 | 45.6 | 5.50 | 3.16 | 1.10 | #121213 |
| 25 | 322-322 | 1 | white flash | 0.900 | 0.3 | 0.000 | 0.00 | - | - | 34 | 255 | 57.5 | 6.87 | - | 4.43 | #E5E5E5 |
| 26 | 323-330 | 8 | terminal crowd slow shutter | 0.564 | 13.6 | 0.000 | 0.00 | - | - | 2 | 243 | 76.3 | 14.22 | 3.18 | 7.56 | #8F8F8F |
| 27 | 331-336 | 6 | spiral stairs | 0.279 | 38.6 | 0.000 | 0.00 | - | - | 0 | 215 | 68.5 | 10.18 | 1.58 | 8.18 | #474747 |
| 28 | 337-342 | 6 | fisheye climber | 0.362 | 32.8 | 0.000 | 0.00 | - | - | 1 | 236 | 81.9 | 10.79 | 2.51 | 5.10 | #5C5C5C |
| 29 | 343-410 | 68 | dot globe fading | 0.009 | 98.0 | 0.346 | 0.65 | 352 | #793B43 | 0 | 91 | 17.0 | 8.52 | 3.99 | 1.01 | #030202 |
| 30 | 411-420 | 10 | black | 0.000 | 100.0 | 0.000 | 0.00 | - | - | 0 | 0 | 0.0 | 0.01 | 0.01 | 0.60 | #000000 |
| 31 | 421-493 | 73 | Whop wordmark | 0.002 | 99.8 | 0.000 | 0.00 | - | - | 0 | 0 | 10.4 | 3.07 | 1.99 | 1.27 | #000000 |

### ATN per shot (mid-shot frame, full 1280x720)

Time-weighted mean luma 0.239; time-weighted near-black (Y<0.10) 60%; shots with vivid pixels >1%: 15 of 26.

| # | frames | len f | label | mean Y | near-black % | sat | vivid % | vivid hue deg | vivid hex | black p1 | white p99 | contrast std | texture hp std | dark grain | dx/dy | mean hex |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0-3 | 4 | Apple card | 0.092 | 85.0 | 0.170 | 1.86 | 14 | #6F3322 | 0 | 204 | 53.9 | 3.64 | 2.35 | 0.97 | #181717 |
| 2 | 4-7 | 4 | Meta card | 0.226 | 60.3 | 0.118 | 2.61 | 246 | #3C50A4 | 0 | 204 | 75.9 | 4.76 | 3.26 | 0.94 | #39393D |
| 3 | 8-11 | 4 | Whop card | 0.054 | 87.3 | 0.559 | 8.93 | 4 | #AB271C | 0 | 192 | 31.0 | 3.64 | 2.14 | 1.04 | #160B0A |
| 4 | 12-15 | 4 | Wise card | 0.156 | 67.4 | 0.548 | 23.02 | 108 | #67A45B | 0 | 191 | 60.8 | 4.17 | 2.77 | 0.81 | #1E2C1A |
| 5 | 16-18 | 3 | Figma card | 0.231 | 60.7 | 0.318 | 16.97 | 89 | #79A550 | 0 | 204 | 76.3 | 4.77 | 3.53 | 0.84 | #383C33 |
| 6 | 19-22 | 4 | Adobe card | 0.078 | 73.7 | 0.688 | 21.32 | 346 | #910E16 | 0 | 190 | 35.8 | 3.73 | 2.04 | 0.95 | #270E12 |
| 7 | 23-26 | 4 | orange asterisk card | 0.036 | 91.1 | 0.292 | 3.67 | 11 | #894437 | 0 | 143 | 26.3 | 2.90 | 1.65 | 0.76 | #0B0807 |
| 8 | 27-27 | 1 | near black | 0.002 | 100.0 | 0.000 | 0.00 | - | - | 0 | 3 | 0.8 | 0.09 | 0.09 | 0.55 | #000000 |
| 9 | 28-29 | 2 | ChatGPT card | 0.008 | 98.8 | 0.174 | 0.01 | - | - | 0 | 33 | 7.5 | 1.25 | 0.78 | 0.80 | #020102 |
| 10 | 30-66 | 37 | eye macro, cards in iris | 0.385 | 9.8 | 0.116 | 11.21 | 23 | #8D5749 | 15 | 238 | 64.6 | 5.27 | 5.89 | 0.91 | #666160 |
| 11 | 67-152 | 86 | 3D wall of websites | 0.230 | 48.9 | 0.134 | 3.45 | 212 | #333F51 | 0 | 209 | 63.4 | 3.86 | 2.6 | 0.41 | #383A3F |
| 12 | 153-179 | 27 | MRI head side, Attention | 0.033 | 90.2 | 0.027 | 0.02 | - | - | 0 | 82 | 16.5 | 2.38 | 1.42 | 1.00 | #080808 |
| 13 | 180-191 | 12 | skier ridge | 0.761 | 0.0 | 0.152 | 11.45 | 209 | #6B8FB0 | 115 | 241 | 33.0 | 1.80 | - | 0.63 | #B3C4D0 |
| 14 | 192-194 | 3 | painting | 0.231 | 31.8 | 0.396 | 28.73 | 31 | #6B5139 | 0 | 195 | 49.9 | 8.42 | 1.99 | 0.19 | #45392B |
| 15 | 195-197 | 3 | statue fountain | 0.172 | 36.1 | 0.101 | 0.11 | - | - | 0 | 138 | 34.3 | 7.25 | 3.18 | 0.32 | #2D2B2A |
| 16 | 198-200 | 3 | statue Venus | 0.373 | 19.0 | 0.071 | 0.11 | - | - | 0 | 215 | 65.0 | 10.65 | 2.22 | 0.09 | #615E60 |
| 17 | 201-203 | 3 | ceiling fresco | 0.312 | 21.7 | 0.212 | 8.00 | 31 | #80644A | 0 | 195 | 54.4 | 10.19 | 2.16 | 0.17 | #564E46 |
| 18 | 204-206 | 3 | wave painting | 0.147 | 51.7 | 0.380 | 8.08 | 179 | #295352 | 0 | 158 | 37.1 | 7.47 | 4.14 | 0.28 | #1E2727 |
| 19 | 207-209 | 3 | angel statue | 0.302 | 20.5 | 0.197 | 0.16 | - | - | 0 | 165 | 47.6 | 10.13 | 4.03 | 0.10 | #454E56 |
| 20 | 210-215 | 6 | painting boat | 0.301 | 21.8 | 0.243 | 9.59 | 15 | #624339 | 0 | 201 | 55.3 | 9.99 | 3.17 | 0.20 | #564A46 |
| 21 | 216-221 | 6 | It's earned wrap + inverted window | 0.769 | 1.0 | 0.136 | 1.73 | 12 | #A64437 | 21 | 255 | 35.3 | 4.30 | - | 0.61 | #BEC4C8 |
| 22 | 222-245 | 24 | skier, It's earned box | 0.816 | 0.0 | 0.089 | 0.48 | 279 | #757967 | 151 | 250 | 21.0 | 2.08 | - | 0.76 | #C6D2D7 |
| 23 | 246-278 | 33 | skier, by perception | 0.876 | 0.0 | 0.023 | 0.31 | 237 | #54485F | 118 | 242 | 19.1 | 1.94 | - | 0.78 | #DDDFDE |
| 24 | 279-309 | 31 | black | 0.000 | 100.0 | 0.000 | 0.00 | - | - | 0 | 0 | 0.0 | 0.00 | 0.0 | 0.05 | #000000 |
| 25 | 310-389 | 80 | dhruv | 0.001 | 99.9 | 0.000 | 0.00 | - | - | 0 | 0 | 6.5 | 2.70 | 1.54 | 2.04 | #000000 |
| 26 | 390-447 | 58 | black | 0.000 | 100.0 | 0.000 | 0.00 | - | - | 0 | 0 | 0.0 | 0.00 | 0.0 | 0.00 | #000000 |

## 7. Not checked
- Ink colour and size for most WHP labels, "Audience", "this", and ATN lines on snow: not re-measured here (STUDY numbers kept).
- Hue numbers use the mid frame of each shot only; colour can change inside long shots (ATN website wall f67 to f152, WHP collage).
- dx/dy texture readings are content-sensitive; the ATN horizontal-line finding is not confirmed by eye.
- Eases are judged from luma curves, not from position tracking. Position eases (drifts, fly-ins, camera push) were not measured.
- WHP text crop ink colours were not read (script failed on one WHP crop; ATN crops only).
