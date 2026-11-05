# Effect library (measured frame by frame on the Altman reference, 960x720 at 23.976 fps)

Times are reference timestamps. "Ours" says how build_template_v7.py makes it (1080x1920, 30 fps).

## 1. Pixel-block opener (0.00 to 0.54 s)
- A candid photo in a warm, bloomed grade starts as a coarse mosaic. Blocks resolve to sharp one by one (faces last); about
  half the frame is sharp from frame 0. On frames 1, 2, 5, 6 and 8, ragged clusters of 3 to 5 blocks flash near white.
- Caption builds "The", then "The SCARIEST". Sound: a sub hit plus digital crackle on each flash frame.
- Ours: `blocks()` with 60 px cells, per-cell reveal times, ragged white clusters, `glitch` SFX on the same frames.
- Note for frame 0: it is also the grid cover. Keep the face readable on frame 0, or start the mosaic on frame 2.

## 2. Giant-word whip into a polaroid (0.54 to 0.63 s)
- One frame: the photo shrinks with motion blur while a giant glowing serif "SCARIEST" smears across. Next frame: the
  same photo as a tilted polaroid on black, with the word's ghost trailing.
- Polaroid holds about one beat (0.58 to 1.21 s), floating slightly (rotation -2.4 to -1.2 degrees, scale 0.97 to 1.01);
  "thing" appears to its left, "about" to its right, each at its spoken time.
- Ours: `giant()` 2-frame pre-roll before the cut, `polaroid()`; crop the photo with an explicit box so the head fits.

## 3. Interview cuts with a per-shot grade (1.21 to 2.38 s)
- Cuts at 1.21, 1.50, 1.84 and 2.38 s to three interviews, each in a different grade: warm-green, teal, washed-bright,
  deep blue. The caption builds "Sam", "Sam Altman", "Sam Altman isn't".

## 4. 9-grid with a cut-out (4.60 to 6.40 s)
- 4.60: a 3x3 grid (thin dark lines) over a purple duotone collage of faces, with floating moon spheres.
- 4.73 to 4.89: cells flash white one after another, then the whole frame blows out with a silhouette in it.
- 4.93 to 4.98: the subject enters from the right, black and white, motion blurred.
- 5.02: one negative (inverted) frame with a green tint.
- 5.06: the subject lands centre as a black-and-white cut-out, the grid collage behind.
- 5.10 to 5.39: cells behind flash white one by one and fill with playing clips (YouTube screens, a podcaster, news).
- 5.43: 2-frame white blocky smear. 5.52 to 5.89: slow push in. 5.93 to 6.39: dark blocky frame, overexposed subject,
  the cells go white and refill with colour news footage (named chyrons) behind the black-and-white cut-out.
- Ours: `grid9()` with per-frame cut-out masks from `person_mask.js` (78 frames of a WEF clip), purple duotone cells
  before they fill, ragged flash order, a negative frame, a slow push of 8%.

## 5. Symbol montages (12.9 to 14 s, 17 to 18 s, 73 to 76 s)
- Abstract words get bursts of 2 to 4 frame shots: statues, Renaissance art, atom, Vitruvian man, moon, clock, black hole.
- Ours: `BURST()` at 3 frames per image. Prefer short video loops over stills where possible.

## 6. Literal objects with type (18 to 19.5 s)
- "kill switch": a light-switch photo with a giant serif "Switch" over it, then "fire" in smoke.
- Sound: a sub swell rising about 18 dB from 16.6 s, holding to 19.5 s, with sharp clicks at 18.5 and 19.8 s.
- Ours: `swell` and `click` in the v7 score.

## 7. Black breather card (7.2 to 8.4 s), the deliberate rule break
- "For context," on black with a soft glow. The only empty frame in the video, and it resets attention.
- Ours: one black card on "But". Every other graphic sits over darkened moving footage.

## 8. Rule-break soundbite (33.1 to 35.2 s; 45.1 to 51.1 s)
- The voice-over stops. A news anchor speaks with their own sound, one held shot for 2 to 4 s, chyron visible. The music
  drops out. Captions continue in the same style for the anchor's words.
- Ours: Larry Fink (WEF 2026, CC BY 4.0) "...so congratulations." after "one trillion dollars", music ducked to 18%.

## 8b. Stamp frames (ours, approved direction 19 Oct)
- Never lay a stamp over the number. The word or number sits alone on top; a red line strikes through it over 4 frames; the
  stamp (VOIDED, REVERSED) punches in below at 1.35x to 1.0x; captions step aside because the stamp prints the word.

## 9. Number reveal on a real chyron (56 to 63 s)
- A Bloomberg anchor with an "OpenAI valued at $852B" chyron, then a big serif "$852B" caption. Real headlines carry the numbers.
- Ours (no licensed chyrons): number cards over darkened moving footage. A real chyron would be better.

## 10. Face-strip collage (77.2 to 79 s)
- 4 to 5 faces sliced into vertical strips, with a strobe between, then the logo sting with a glow.

## 11. Light smears and flashes (22 of 141 cuts)
- 1 to 3 motion-blurred near-white frames between shots. Also exposure pops on cuts, and camera shake on impacts.
- Ours: `flash` (2 frames: 92% then 45% white), `pop` (1 frame, 35%), `shake` (5 frames, decaying 36 px).

## 12. Frame-edge look (every frame, captions included)
- Measured in the corners: edge blur rising toward the corners, magenta and green fringe of 6 to 8 px against 960 px of width
  (left vs right edge), a thin pink-magenta rim along the frame edge, vignette, bloom on highlights.
- What it is: lens-emulation stacking: radial chromatic aberration plus an edge-weighted defocus (or a lens-distortion
  pass), a glow and a vignette, often a "VHS/camcorder" or "dreamy lens" preset in CapCut or After Effects (chromatic
  aberration plus camera-lens blur through a radial mask).
- User verdict (19 Oct): it is **chromatic aberration near the borders only**. A rim or edge glow read as "a border glow,
  not like the reference". Shrinking a channel left empty edge bands (yellow stripes): scale channels outward only.
- Ours (v8): `ca_out()` scales red +2.2% and green +1.1% (blue fixed), mixed in by a mask that is 0 inside 55% of the radius
  and full at the corners; vignette and grain; no rim, no edge blur. Applied after the captions.

## 13. Micro-motion on stills
- Stills breathe: exposure flicker every 2 to 3 frames, slow push or pull, or sit inside a collage.
- Ours: `flicker()` (plus or minus 6% gain, every 2 frames) on every photo and burst frame.

## 14. Captions
- 1 to 3 words, built word by word, centred near the middle; serif italic with a tight heavy sans for key words; numbers in
  the serif, larger; soft glow; colour flips to black over bright frames (25.8 to 26.4 s, "ever built." on a white page).
- Ours: Didot Italic plus Helvetica Neue Bold at tracking -5; black text when over 45% of the caption band is bright.
