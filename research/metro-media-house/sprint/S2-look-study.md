# S2 Look study: Metro Media House reels (grade, captions, graphics)

Status: stopped at deadline, missing: strips/ review, exact graphic counts for ACK, EIN, YC (only skimmed), grain check, more full-res frames

Reels: PAL=DclpjyxhKF6, ACK=DdHKc5GBqT-, EIN=Dee-mp9BJqG (USVC, paid), YC=DfFsUfUx0dZ (paid).

Tools: `S2-tools/look.py` (one ffmpeg decode pass per reel at 240x136, picks each shot middle frame from `raw/<id>/shots_ref.json`, builds sheets, computes grade numbers, grabs 8 full-res caption frames per reel). Raw output: `S2-tools/look_stats.json`.

## 1. Frame sheets (shot middle frames, 240 px tiles, 10 per row, label = shot # and mid-time)

- `S2-sheets/PAL_DclpjyxhKF6_shotmids.jpg` (85 shots, 24 fps)
- `S2-sheets/ACK_DdHKc5GBqT-_shotmids.jpg` (125 shots, 25 fps)
- `S2-sheets/EIN_Dee-mp9BJqG_shotmids.jpg` (118 shots, 25 fps)
- `S2-sheets/YC_DfFsUfUx0dZ_shotmids.jpg` (124 shots, 24 fps)

## 2. Grade numbers (MEASURED, numpy on the shot middle frames, values are medians across shots)

Luma = Rec.709 on 0 to 255. Warm = mean R minus mean B above +8, cool = below -8. Near-mono = mean HSV saturation under 0.10. Clip frame = over 1% of pixels at luma 250+. Crush frame = over 5% of pixels at luma 5 or less.

| Reel | p2 (black pt) | p50 (mid) | p98 (white pt) | contrast p98-p2 | mean sat | warm % | cool % | near-mono % | clip frames % | crush frames % |
|---|---|---|---|---|---|---|---|---|---|---|
| PAL | 6.4 | 72.8 | 211.0 | 189.9 | 0.305 | 34 | 24 | 13 | 5.9 | 27 |
| ACK | 8.6 | 81.6 | 172.7 | 161.5 | 0.297 | 32 | 26 | 11 | 4.8 | 32 |
| EIN (USVC) | 5.5 | 66.0 | 192.4 | 160.4 | 0.074 | 19 | 10 | 59 | 0.0 | 33 |
| YC | 8.9 | 80.2 | 185.9 | 169.5 | 0.288 | 40 | 13 | 19 | 8.1 | 27 |

Measured readings:
- Black point sits just above true black (p2 = 5.5 to 8.9), mids are low (p50 = 66 to 82 of 255, about 26 to 32%), white point is well below clip (p98 = 173 to 211). Median clipped-pixel share is about 0 to 0.006%. So: dark, mid-low key, highlights held back, nothing blown.
- About 27 to 33% of shots have a large block of near-pure black (over 5% of pixels at luma 5 or less). That matches letterbox/black-card or dark-background shots; which one it is was not separated by the numbers.
- The three Metro Media House reels (PAL, ACK, YC) share one profile: sat about 0.29 to 0.31, slight warm lean (32 to 40% warm shots vs 13 to 26% cool), 11 to 19% near-mono shots.
- EIN (USVC cousin) is a different grade: sat 0.074 median and 59% of shots near-monochrome. It is a mostly black-and-white piece.
- Cross-check with `raw/<id>/colour.json` (earlier study, all frames, 0 to 1 scale): mean_saturation PAL 0.294 / ACK 0.359 / EIN 0.173 / YC 0.249; near_grey_pct PAL 31.9 / ACK 29.9 / EIN 67.5 / YC 45.8; near_black_pct 21 to 25 for all. Same ordering and same EIN outlier; my shot-median sat is lower for ACK because colour.json averages all frames (long colourful shots weigh more) while mine counts each shot once.

## 4. Caption placement (MEASURED where the detector worked)

Method: 8 words spread evenly through each transcript, frame grabbed at word mid-time at full res (1916x1078), near-white text pixels (min channel 225+, channel spread 25 or less) below 30% of height. Where the frame itself is bright (white paper, sky) the detector catches the background and the reading is useless; those are marked unreliable.

Clean single-line readings (y top to bottom % of height, x span %):
- PAL 32.96s "the": y 48.4 to 51.9 (centre 50.3), x 15.8 to 30.2. PAL 64.36s "quietly": y 48.2 to 52.6 (50.5), x 45.6 to 54.5.
- ACK 24.42s "the": y 48.8 to 51.6 (50.1), x 46.9 to 53.1. ACK 35.64s "him": y 49.0 to 51.8 (50.3), x 45.7 to 54.1. ACK 48.27s "walked": y 48.8 to 51.6 (50.2), x 29.6 to 38.0.
- EIN 35.79s: y 46.6 to 50.0 (48.2). EIN 67.74s: y 46.5 to 51.2 (49.2), x 30.9 to 68.6. EIN 86.02s: y 47.1 to 53.1 (50.0). EIN 102.2s: y 47.0 to 51.6 (49.4).
- YC 11.19s: y 47.9 to 51.3 (49.8), x 43.8 to 53.9. YC 23.52s: y 47.4 to 51.2 (49.7). YC 44.0s: y 48.1 to 52.0 (50.4), x 38.9 to 60.7. YC 67.68s: y 47.0 to 50.8 (49.2).
- Off-centre hits: PAL 53.92s y 70.7 to 75.1 and YC 55.49s y 73.7 to 77.1 (lower third white text; could be a caption or an on-screen label, not confirmed).
- Unreliable (bright frame, band 30 to 99.9%): PAL 11.19, 42.66, 75.91; ACK 0.79, 12.37, 75.59; ACK 87.79 found no white text; YC 0.6, 78.57.

Measured result: the caption is white text centred on the frame's horizontal midline, y centre 48 to 50.5% of height, single line, glyph height (white row extent) 2.8 to 4.7% of frame height (about 30 to 50 px on 1078). x span on single short words is 6 to 10% of width; some spans start at 15 to 30% x, which means the caption line is not always centred horizontally or that other white text was in the frame (not resolved by measurement).

## 3. Grade by eye (JUDGED from the PAL sheet and the full-res YC 44.0s frame; other sheets not reviewed in time)

- Soft, slightly hazy image; footage looks like upscaled archival/interview video, not crisp. Mild glow on white caption text (judged, not measured).
- Visible edge darkening (vignette) on the YC 44.0s frame, left and right edges darker than centre (judged).
- Blacks near but not fully crushed (fits p2 of 5 to 9). No strong colour cast overall; mixed warm interiors and cool blue/teal stage and HUD shots.
- Grain: could not judge at sheet scale.
- White paper card colour, MEASURED with numpy (median of top-left background region, x 3 to 18%, y 8 to 30%): PAL 8.4s: #d6d6d9 (RGB 214,214,217); PAL 69.9s: #ebe8ec (RGB 235,232,236); PAL 74.4s: #f5f2f6 (RGB 245,242,246). Measured: neutral off-white with blue a hair above red and green (about +2 to +3), so not warm; brightest card reads #f5f2f6, not pure #ffffff. The 8.4s value (#d6d6d9) is darker, likely shading or a different card (check before copying).

## 4b. Caption look (JUDGED from the PAL sheet and YC 44.0s full-res frame)

- Default caption: small white clean sans (Helvetica or SF-like, medium weight), no box, soft shadow/glow, centred on the frame midline, builds word by word ("So he auctioned" at 44.0s). Full-res glyph height about 3.5% of frame height (matches measured 2.8 to 4.7%).
- Hero words: same sans, much bigger and bold (about 2 to 3 times), white, sometimes red for a name ("Tony Stark" in PAL 5.1s) or yellow highlight on a number ("$10,000.00" in the PayPal mock). Examples in PAL: Silicon Valley, Billionaire, apologizing, weapons, autonomous drones, real wars, they didn't like.
- Words are sometimes scattered across the midline at set x positions ("Throwing him out", "One builds the weapons"), which explains the measured x spans starting at 15 to 30%.

## 5. Motion graphics inventory (JUDGED, PAL sheet only, 85 shots; other reels not counted in time)

- Off-white paper card with cut-out photo or framed picture: about 9 shots (#8, #12, #33, #34, #40, #41, #59, #79 to #81, #83, #84).
- Fake UI mock-up (PayPal payment screen with tick, amount highlighted yellow): 3 shots (#13, #14, #15).
- Photo collage or multi-panel split (several photos tiled, white panels): about 6 (#1, #4, #11, #33, #34, #50).
- Logo card on black (Palantir logo, sometimes with radial web graphic): 3 (#48, #49, #60).
- HUD / tinted thermal or drone footage overlays (teal, cockpit HUD): about 6 (#35 to #37, #62 to #64).
- Tilted 3D screen stacks / magazine pages: about 3 (#51 to #53).
- Chess piece metaphor shots: 2 (#43, #44).

## 5b. EIN and YC sheets, quick look (JUDGED, not counted)

- EIN: mostly black-and-white archival photos (fits the measured 59% near-mono), with colour only on a few inserts (planet, red dice card, chip, amber meter). Graphics: big bold condensed white headline words ("17", "OF ALL TIME", "EINSTEIN", "CERTAINTY", "FELL", "SEMI CONDUCTOR"), photo cut-outs and polaroid frames on off-white paper, serif name labels over portraits (Einstein, Bohr, Schrodinger, Heisenberg), quote-mark cards ("GOD DOESN'T PLAY DICE"), book-page close-ups.
- YC: colour interview and event footage; small white midline captions on almost every shot; off-white and black plain text cards (e.g. 16 8.9s, 43 25.2s, 76 45.5s, 77 46.4s, 90 57.0s); a few big bold words ("customers", "$43 Million", "$6 thousand", "OpenAI"); logo inserts (twitch, doordash, Airbnb, Stripe, reddit, TED); end card "USVC" in blue on white (121 74.2s), showing YC is a paid USVC piece.

- ACK (quick look, JUDGED): colour footage with small white midline captions on nearly every shot; drawn-on graphics (red devil horns 6 to 7, 3.7 to 4.7s), cut-outs on off-white paper (12, 16 to 18, 24 to 26), logo/bank-front montage (34 to 42), meme and collage inserts, stock-chart and news-ticker footage, flat illustration pyramid scheme (102 to 105), Pac-Man insert (108), big bold hero words ("1.4 billion", "Carl, Fuck you", "getting.").

## Look spec (numbers to copy)

- Luma: black point p2 about 6 to 9 (of 255), mid p50 about 72 to 82, white point p98 about 175 to 210, almost no clipping (under 0.01% pixels at 250+).
- Saturation (HSV mean, shot median): about 0.29 to 0.31 for Metro Media House; keep 10 to 20% of shots near-monochrome. EIN-style (USVC) is a mostly black-and-white grade (sat 0.07, 59% mono).
- Slight warm lean: about 35% warm shots vs 20% cool.
- Captions: white sans, no box, single line, y centre 48 to 51% of height, glyph height 3 to 4.5% of height, word-by-word build; hero words 2 to 3 times larger, bold, white, key names red, key numbers yellow highlight.
- Paper card: neutral off-white, about #ebe8ec to #f5f2f6 (never pure white).
