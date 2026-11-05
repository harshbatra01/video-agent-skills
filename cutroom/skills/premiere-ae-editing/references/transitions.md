# Transitions and flash effects for music edits: how to build them (learned 13-14 Oct 2026)

How premium "cracked" sports / AMV edits build their transitions, measured frame by frame on about 30 top edits, and
how to rebuild them in After Effects (and in Premiere, the user's own way) without plugins. The method matters as much
as the recipes: measure the reference, rebuild, compare frame by frame with numbers, repeat. Which effect is approved,
rejected or untested, and the user's words: motion-design skill (`references/effect-vocabulary-and-taste.md`,
`references/transitions.md`, `references/cracked-edits.md`). This file keeps the method, the recipes and the AE facts.

## Status before you build (14 Oct 2026)
Which transition is approved, rejected or untested, with the user's words, lives in one place: motion-design
`references/transitions.md` section 2 (and `effect-vocabulary-and-taste.md` section 3). Check it before you build
anything from this file. The guard that matters here, because some recipes below are kept only for their mechanics:
- REJECTED on 14 Oct 2026: the light crack into flying strips and the silhouette burst ("I don't like the light crack
  or the silhouette burst", "look bad"). An earlier version of this file called them "accepted as fresh": that was
  wrong. Their build notes stay at the end only for the AE mechanics they taught; never use them unless the user asks.
- Also rejected or banned (never build unless asked): auras, colour floods, plain geometry (spins, box or checkered
  glitches, closing shutters or blades), whips that show a mirrored or static frame, black breath frames, abstract
  frames that hide the picture for 10+ frames, a full white frame on the payoff moment.
- The code for these recipes is the music-edit kit's `fx_lib.jsx` and `edits_lib.jsx` in
  `library/pipelines/edits-kit/tools/ae/`, not this skill's scripts.

## The method (do this for any new effect)
1. Find the intense moments of a reference automatically instead of watching: per frame, compute on a 96 px copy
   the mean luma change (cuts, flashes), the luma correlation with the previous frame (below -0.25 = an inverted
   frame), the drop in gradient energy against the local median (blur / smear / zoom-blur frames) and the chroma
   change (colour bursts). Sum them over 12-frame windows and keep the top windows at least 1 s apart. Lay every
   frame of each window out in a row. Crop letterbox bars first (find them from the median frame), or every white
   frame inside the band is hidden by the bars' black.
2. Rebuild the effect on a real cut of your own footage, 1.2 s per test, many tests in one test reel (one render,
   about 45 s).
3. Compare ours and the reference side by side at the same height, frame by frame, AND print three numbers per
   frame: L = mean luma, S = luma spread (structure; a flat white or black frame has S under 8), C = colourfulness
   (mean max-min of RGB). The numbers find what the eye glosses over (four "white" frames that were really vignetted
   picture, a "dark" frame that was a rainbow).
4. Tune per frame and re-render until the L/S/C rows follow the reference's shape. Then look at it once more.
5. Put the transition's PEAK on the hit, not only the cut frame: blow-out white frames at -1 / 0 / +1, the fullest
   flash-panel frame at 0, strobe recipes starting on the hit. Why: the strongest references do this, while their raw
   cut frames sat anywhere from 7% to 83% of a beat away from the hit.

## What the measurements say (build parameters)
- Premium transitions are optical: light, blur, streaks, colour, line art, or flat panels lit frame by frame.
- Flat white lasts 1-3 frames; the body of a transition keeps structure and colour (streaks, blobs, tints).
- A transition is a RECIPE of 6-12 distinct frames, not one effect with an ease curve.
- Density targets per 10 s and by section: motion-design `cracked-edits.md`.

## Frame recipes (0 = first frame of the next shot)

| Transition | Frames |
|---|---|
| Light blow-out | -2 hot orange (L 149, C 158), -1/0/+1 flat white (L 249, S 6), +2/+3 golden light (L 223, S 16, C 115), +4 the shot |
| Zoom rush | 3 frames of pure radial streaks around the cut (radial blur "Brightest" mode, scale x1.5 into the cut), the next shot arrives over-zoomed and slightly rolled, settles over 7 frames; a radial chromatic split (red copy scaled up, blue down, Add) makes it a rainbow tunnel |
| Streak smear | bright vertical bars of the picture's own colours: directional blur ~320 px + scale-Y x1.9 + exposure and contrast (L ~180, S ~70); the references hold it 8+ frames, ours stays short (a long sideways smear was rejected) |
| Light painting | 1 white frame, then only the highlights (Levels input black ~0.4) tinted cyan on near-black, smeared sideways ~300 px, darkening from L 126 to 55 over 10 frames, then fade; only short (a 6-7 s use was "TOO long") |
| Line-art strobe | E K E K: Find Edges line drawing on white (L 237) / thin lines on black (L 20), then bright and black streak frames S D S D, then 2 saturated colour streak frames |
| Defocus space | out-going melts into a grey haze (L 110, S 20), in-coming starts as glowing colour blobs (L 90, C 140) and focuses over ~12 frames |
| Ray burst | 2 frames of bright, desaturated rays WITH structure (L 175, S 65-80, C 13), then the shot |
| Vortex | spin blur + zoom blur held ~8 frames, bright and contrasty, little colour (L 184, S 73, C 37); a Twirl distortion read as a rigid rotation |
| Colour flood (rejected) | orange x2 (picture visible), yellow x4, red x6 with the next shot slowly ghosting through (S rises 3 -> 14) |
| Aura (banned) | the player's matte grown, broken by animated Turbulent Displace, blurred, filled with a saturated colour in ADD mode behind the cut-out; a wider faint copy for bloom (Glow alone made a thin white halo) |

A thin gold rim on the cut-out is not an aura: matte grown with Minimax (grow 7) + Glow 45, gold [1, 0.78, 0.15], on one
moment only.

## One letter per frame (strobe recipes, `frameRecipe` in the music-edit kit's `fx_lib.jsx`)
Every look is band-size and lasts one frame; a string plans, varies and syncs a strobe ("EKEK" = 4 frames).

| Letter | Look (After Effects settings) |
|---|---|
| E | line art on white: Exposure +1.2, contrast 45, Find Edges, Black & White, Levels input black 0.2 / white 0.78 |
| K | glowing lines on black: E + Invert, Levels 0.3 / 0.9, optional Tint, Glow 30 / 18 / 0.6 |
| I / N | colour negative / mono negative |
| B | hard black and white (contrast 70) |
| W / X | white / black (X only inside a strobe: black breath frames are banned) |
| S / H | bright vertical / horizontal streak: Motion Blur 300 px, Transform scale 180 on one axis, Exposure +3.5 with Offset 0.22, Black & White |
| D | dark streak (Exposure -6.5) |
| C | colour streak: Exposure +2.3, Lumetri saturation 220, contrast 55 (script scale 0-300, after-effects.md trap 47) |
| Z | zoom-blur burst: scale 130, CC Radial Fast Blur 90, Exposure +0.5 |
| T / V | impact frame: Threshold 0.43 (= level 110 of 255, script values are 0-1) / the same inverted |
| R Y U G P O | colour solids at 86% with the picture ghosting through |
| . | the frame untouched |

- In use: "EKEK" (gold lines [1, 0.85, 0.3]), "EKEKSD" into a black-and-white chapter, "SDSDCC", "EKE" on a strike,
  "VT" on contact frames, "I" and "I.I" flickers, "N" inside a black-and-white section. Line-art strobes were kept.
- Type flash (not reviewed yet): W = black word on a white band, B = white word on a black band, pattern "WB", the
  word 290-420 px fitted to the band.

## Silhouette strobe stack (kept) and the poster frame
- One look per frame on the cut, built from the next shot's player: F = flat field colour with the player as a white
  silhouette; I = white field with the player in the field colour; K = black with a white player; W = white;
  P = white field with a BLACK player (the poster frame, not reviewed yet). Field colour used: maroon [0.62, 0.05, 0.18].
- "WFIK" was kept (not flagged); "PK" and "PPK" are untested.
- Build: band-size solids plus solids track-matted (luma) by the clip's subject matte (SAM 2, media-toolkit.md
  section 12). A flash on the same frame hides the silhouette: use one or the other.

## Flash panels ("flashGrid", the user's kind of geometry; first full use not reviewed yet)
- Split the picture band into n panels (columns or rows). Each frame lights a set of panels at 100% with HOLD keys and
  crisp edges; the FULLEST frame is frame 0 = the beat; panels still lit at the end fade over 4 frames into the next
  shot. Why: his own reference lights flat white or cream panels frame by frame, which reads as designed light, while
  moving geometry read as "PowerPoint".
- Patterns: `fill` (one more panel per frame, starting n-1 frames before the beat, 4-frame fade), `fill_rev`, `fill2`
  (two per frame), `centre` (middle outwards), `alt` (odd, even, all), `pass` (a lit block passes over the cut; halves
  = `pass` with n = 2 rows, no fade), `unfill` (full on the beat, then panels switch off one by one to reveal the shot).
- Used: 7 vertical white bars `fill` n = 7; cream halves `pass` n = 2 rows in [0.94, 0.94, 0.88]; 5 horizontal white
  bands `fill` n = 5 into a chapter; `unfill` n = 7 two frames after a type flash; `centre` n = 7 in cream.
- Open: the halves order. He described his own as "bottom half of the screen first, then bottom and top half, and then
  just top half, and then nothing"; `pass` lights the top first, and his edit has a down and an up light bar. Check
  against his frames and flip if needed.

## After Effects facts that decided whether a recipe worked
- Exposure works in gamma-encoded space: +1.8 stops takes a 0.4 grey only to 0.67, and -4.5 stops still leaves
  highlights at about 23%. Dark night footage cannot be lifted to white or golden with Exposure alone: white, golden
  and orange frames are band-size colour SOLIDS at 50-97% opacity with the picture ghosting through (or Exposure's
  Offset param, which lifts blacks).
- Never stack Exposure + Glow + Screen on the same frames: it turns everything into blank white.
- A low-threshold Glow after a big negative Exposure lights the remaining highlights up as a rainbow.
- Put the grade and vignette BELOW the transitions and flashes: a vignette over a flash turns flat white into a grey
  gradient (after-effects.md section 12 gives the full layer order).
- Adding an effect to a layer invalidates script references to that layer's earlier effects ("Object is invalid"):
  set an effect's values before adding the next one, or fetch it again.
- Levels' Input/Output values cannot be keyframed by script; key Brightness & Contrast, Exposure or the adjustment
  layer's opacity instead.
- Letterbox layouts: distortions pull black from outside the picture band. Put Motion Tile on each FOOTAGE layer
  (output height ~170%, mirror edges). Motion Tile on an ADJUSTMENT layer scales the whole comp into the tile
  (squashed picture), and a Transform stretch of the edge rows (scale 9000%) ran the GPU out of memory. Renders got
  slower once every clip carried Motion Tile.
- Key per frame with linear keys exactly on frame times; a value per frame is how the references change look.
  `prop.setValuesAtTimes(times, values)` writes a whole row of them in one call (after-effects.md trap 42). This is the
  exception to the two-keys-per-move rule for ordinary motion (after-effects.md section 13): a flash recipe is a
  sequence of distinct frames, not a move.
- When a clip is pre-rolled for a transition, clamp its matte's time remap to the matte file's length (AE refuses
  negative or out-of-range remap values and the whole build fails).
- Layers that sit ABOVE the letterbox bars (a pop-out of the player over the title) must not carry the mirrored band
  extension, or a mirrored copy of the head shows above the band.

## The same effects in Premiere (the user's own hand recipes, read from their reference edit's .prproj, 13 Oct 2026)
The reviewer edits in Premiere, so these are the proven routes there. Nests named "Nested Sequence N" hide the stacks:
read them from `prproj_dump.py`, not from the timeline.
- White silhouette strobe: a 1-frame copy of the clip on the track above, a mask around the player, VR Glow and an
  Opacity blend mode; 2-3 of them with 1-frame gaps.
- Inverse strobe: the same with the mask inverted (the background flashes white, the player stays).
- Impact Dip To White (a third-party Impact transition, 4 frames) on the big cuts, plus 1-frame white frames on kicks.
- Light-bar wipe: a 3-frame graphic of Noise + a Shape with Crop keyframes.
- Mirror-edge zoom or spin: Transform + 4 x Mirror + Transform inside a nest.
- Texture pass: a Black Video layer with VR Digital Glitch + Wave Warp + Lumetri + Noise over a long stretch; it only
  shows at 100%, so check crops at full size.
- Speed tweaks of 0.86-1.27x so moves land on beats; a 1-frame "portal" frame; an end card shaken by a shake preset
  (about 600 keyframes) that settles in 4 frames.
- In his documentary cutdowns (measured in his own project): AE_Impact_Dip_To_White of 0.33-0.47 s centred on the
  hook-to-story cut and 0.20-0.27 s into the end CTA, and a 4-frame Constant Power crossfade on every dialogue cut.
  A render that copies these numbers matches the XML he finishes by hand (the XML carries markers where they go).

## Rejected builds, kept for the mechanics (do not use unless asked)
- Light crack + flying strips: a hot white line glows along every strip boundary for 2 frames, then the out-going frame
  breaks into 5-6 strips (masked duplicates of the clip layer) that fly off in alternating directions with motion blur
  over the next shot already playing (start it 4 frames early); white frame on the beat. Mechanic worth keeping: draw
  the mask rectangles in comp space and convert them to layer space with the layer's anchor / position / scale.
- Silhouette burst: a duplicate of the next clip, track-matted by a duplicate of its matte that scales about the player
  per frame (25, 40, 70, 130, 260, 520%...), over the out-going shot, with a white rim from a further matte copy grown
  with Minimax under the window; exposure +0.6 at most (at +1.8 with glow it read as a plain white frame).
