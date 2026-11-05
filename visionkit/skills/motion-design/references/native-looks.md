# Native looks: built with After Effects' own effects

"Native" here means no plug-ins: every look below uses effects that ship with After Effects, so the project stays
editable on any machine. (For the native SOCIAL look, posts that look like real posts, see
`effect-vocabulary-and-taste.md` section 7.) Recipes proven on real builds of documentary and brand reels; effect match
names and parameter indexes are the ones that worked in After Effects 26.2. General scripting traps: premiere-ae-editing
`references/after-effects.md`. Many of these exist as helpers in premiere-ae-editing `scripts/ae/motion_lib.jsx` and
`scene_lib.jsx` (named below).

## Contents
1. Analog night finish (a documentary look)
2. Ordered dither (1-bit and stepped)
3. Halftone dots
4. A smooth Gaussian glow
5. Glow and bloom rules
6. Wave and crest-line fields
7. LED panel wall with per-tile switching
8. Globe from a flat texture (CC Sphere)
9. Character grids, typing and text tricks
10. Logos, pixel art and colour accuracy
11. Paper, photocopy and print looks
12. Small effect facts
13. Where each look fits (taste)

## 1. Analog night finish (a documentary look)
Built to match a mini-doc creator's measured look (`acGrade` / `acFinish` in motion_lib.jsx, `nightGrade` / `finish` in
scene_lib.jsx).
- **Grade** (an adjustment layer over all content, captions included): Levels (Individual Controls) input black 0.05 and
  gamma 1/1.08; a second Levels for contrast 1.18 (input black 0.5 - 0.5/1.18, input white 0.5 + 0.5/1.18); Hue/
  Saturation master saturation -18.
- **Bloom** (an adjustment layer): Levels input black 0.66 so only highlights pass, Gaussian Blur 60 (Gaussian Blur gives
  a sigma of about 0.466 px per unit of Blurriness), blend mode Screen at 55%.
- **Render comp:** an opaque black solid at the bottom (a multiplied vignette over transparency shows white); three
  copies of the content comp, each keeping one colour channel (Levels Individual Controls with the other two outputs at
  0), added together and scaled 100.4 / 100 / 99.6% for a red/cyan fringe that grows toward the edges (keep every
  channel's scale at 100% or more, or bright frames get a coloured edge); a baked rounded tube vignette PNG in Multiply
  (corners at about 45-60% of the centre); an adjustment layer with a 1.3 Gaussian soften; mono noise 5 as grain.
- Text beats on black get two black frames before the next cut; white flash frames are a white solid for 1-2 frames.
- The kit ships the vignette PNGs (`assets/ae/vignette_ac.png`, `vignette_mm.png`, `vignette_mmdark.png` in
  premiere-ae-editing).

## 2. Ordered dither (1-bit and stepped)
- **Stepped colours:** a smooth field layer, Mosaic to the cell size (3 px blocks), plus a tiled 24x24 Bayer threshold
  comp in Add at 1/5.2 opacity. Four colour solids, each luma-matted by a copy of that sum with Threshold at
  (k + 0.4)/5.2, give the dithered steps.
- **Shaped glyphs on a grid** (exact and native): Mosaic the field to the cell size (Sharp Colors on, so each cell takes its
  centre sample), add the tiled Bayer comp in Add; per-pixel coverage = (q Subtract a tiled "glyph screen" whose pixels hold
  the q each pixel needs) thresholded at 0.002; per-cell opacity steps come from a grey solid plus Threshold copies of q in
  Add at the step opacities, multiplied by the coverage. Tile 64x64 comps with Motion Tile at 3200% x 1800% with the layer
  at (992, 544) to keep 8 px cells on the frame grid.
- **Two-colour print of footage** (library #12, Pixel Dither Background): grey from the red channel (Shift Channels: it
  separates blue sky from white cloud best), Levels (input black about 95, input white 235, gamma 1.10), Mosaic into 4 px
  cells (480 x 270 blocks, Sharp Colors on), minus a 12 px threshold tile repeated across the frame (Subtract), then
  Threshold (level 1) and Tint (ink #5FB6CF, paper #F3FBFD). The dither is baked before any camera move, so the cells
  scale with a punch-in. The tile's greys are thresholds, so build in the sRGB working space.
- `ditherZone` in scene_lib.jsx does ordered dither from the shipped Bayer maps (`assets/ae/bayer_2px..5px.png`).
- Threshold's Level runs 0 to 1 from a script (0.43 = UI level 110).
- A reviewer asked for "more stylization and dither elements here and there", including dither on objects. A quick route
  for stills: dither them before animating and render that as a plate.

## 3. Halftone dots
A field layer sets the dot size; a tiled 16x28 cell of radial-gradient dots (Gradient Ramp radial, white to black) in Add at
97%, then Threshold 0.98 and a 0.6 px blur, gives antialiased variable dots. Colour them with a Levels-mapped copy of the
field for grey plus an orange solid matted by a "hot" map, all under a luma track matte of the dots.

## 4. A smooth Gaussian glow
After Effects' Gaussian Blur is cut off at about 2 sigma, so one huge blur leaves a hard edge. For a smooth glow, stack 24
ellipses in Add with radii `r * sqrt(-ln((i - 0.5) / 24))` for i = 1..24, plus a small blur. Blurring a shape on its own
layer blurs its alpha, which Levels cannot brighten: blur on an adjustment layer over an opaque background instead.
Effects on shape layers are clipped to the shape's box (a glow that "cuts off as a square", a reviewer note on our work
too): use comp-size solids with feathered masks (`softEllipse`, `softBand` in ae_lib.jsx), or put the shape in a small
precomp and the effect on the precomp layer. Gaussian Blur's Repeat Edge Pixels also boxes a glow: turn it off.

## 5. Glow and bloom rules
- No paid glow plug-in: Deep Glow washed pastel colours to white on a client reel, and it is not installed on our build
  PC anyway. Some reference looks use no glow at all.
- **Element glow:** native Glow (`ADBE Glo2`) lightly: Composite Original On Top, threshold about 55%, radius about a
  quarter of the element's size, intensity 0.8 or less, so colours hold and only edges glow. One glow on a precomp beats
  one per layer. Keep white article pages clean.
- **Reference-matched bloom:** an adjustment layer with Levels (input black at the threshold, 0.66), Gaussian Blur 60,
  blend mode Screen at 55% (exactly 1 - (1 - x)(1 - amount x blur(highlights))). Glow in Add over bright footage blew 40%
  of a frame to white.
- **Whole-picture bloom on broadcast footage:** threshold 85+, intensity 0.2 or less (it turns pitches neon otherwise).
- **Soft caption glow:** a blurred duplicate of the captions precomp (Gaussian 28, 55% opacity) under the original.
- Never stack Exposure + Glow + Screen on the same frames: it makes blank white. A low-threshold Glow after a big negative
  Exposure lights the remaining highlights up as a rainbow.
- No auras around people (our music-edit user: "do not do auras of this type").

## 6. Wave and crest-line fields
Without per-pixel code: a narrow solid with Gradient Ramp, Motion Tile with Mirror Edges (which makes a triangle wave),
Levels input black plus gamma to sharpen the crests, rotated to the wave direction. An expression on Tile Center moves the
waves; a position expression `(world offset . k) mod period` locks the pattern to a moving world. Wave Warp on a comp-size
solid samples outside the layer at the edges (transparent rows): use an oversized solid (for example 2100x1300) with the
Gradient Ramp points in layer coordinates. Wave Warp Pinning 1 = none.

## 7. LED panel wall with per-tile switching
A 64x32 grid as one shape-layer comp (tiles about 27 px on a 33.45 px pitch, black gaps, about 9% of tiles black and the rest
greys 12 to 31 in the reference), shown through a luma-matte reveal comp: a disc sweeping out from a point (a send button),
and noise plus Mosaic plus Threshold so whole tiles switch on and off. The wall can also be the chart: tiles under a
rising line light up as a bar graph.

## 8. Globe from a flat texture (CC Sphere)
- CC Sphere over a 2:1 precomp texture at the comp centre; Offset = [W/2 + cx - 960, H/2 + cy - 540].
- Parameters by index: -0002 Rotation X, -0003 Rotation Y, -0006 Radius (0 to 10000), -0007 Offset (layer coordinates),
  -0008 Render (2 = outside), -0010 light intensity, -0012 light height, -0016 ambient, -0017 diffuse, -0018 specular. Its
  projection fits a perspective distance D = 11.7; the silhouette is 0.9963 R.
- Ambient 100 with diffuse 0 renders the texture at flat brightness, so the sphere can match an unlit 2D plane within
  0.3/255 across a hand-off.
- A mask on the sphere layer is applied BEFORE its effects (the mask cut the texture and the sphere stretched what was
  left): use a track matte instead (mattes apply after effects).
- Dots on a globe: land polygons (Natural Earth) turned into a dot grid in Python (unwrap the date line), drawn as a
  shape-layer texture; keep it illustrative when the brief says no location claims.

## 9. Character grids, typing and text tricks
- A full-frame grid of characters as ONE text layer: Courier New Bold (`CourierNewPS-BoldMT`) with the text's leading set;
  a per-character Opacity animator with a time-stepped hash expression makes it shimmer.
- A whole row of prompts can be one text layer with spaces between them, because advances add up across spaces.
- Measure text in After Effects (a throwaway layer and `sourceRectAtTime`) when exact widths matter.
- Never give two expression variables in a generated template the same name: a later `X.caretPos = ...` silently replaced
  an earlier one, an expression referenced missing layers, After Effects disabled it, and a stray cursor sat at its default
  position.
- Typing, word reveals, letter rises and gradient text: `titles-captions-type.md` section 2.

## 10. Logos, pixel art and colour accuracy
- Split a logo SVG into parts on the same viewBox: each part imports at the SVG's size and the layers stack into the exact
  logo, ready to animate separately (a mark darts in on a dot trail, the wordmark wipes on). Follow the brand guide: no
  effects on the logo, the right logo version for the background.
- Pixel art: export sprites at their exact on-screen size and use them at 100%; set layers to Draft (nearest neighbour), and
  after applying "Best Settings" set the render quality back to "Current Settings", or edges blend.
- **Working space:** new After Effects 2026 projects default to Rec.709 Gamma 2.4, which shifts sRGB PNG colours (dark values
  brighten; #1A6317 became #266B23). Set the working space to sRGB IEC61966-2.1 before importing anything for plate-heavy and
  designed builds (the effects library harness always does). For Dynamic Link builds a project working space of None gave
  exact colours (setting it pops a blocking dialog once; then reuse that project by save-as). On Windows our approved
  renders were made in AE's default space: test one shot against its PNG before switching a job (open question).
- Lossless QuickTime Animation renders blow up on painterly footage (4.3 GB for 24 s): use ProRes 422 ("High Quality")
  unless pixel-exactness matters.

## 11. Paper, photocopy and print looks
- **Mixed media** (library #11): a photocopy background stepping at 12 fps (Posterize Time 12; Black & White; Levels input
  black 25 / white 205, gamma 0.9, output 30 / 222; Unsharp Mask 200 / 2.5; Noise 35%; Tint black #1E2327 to paper
  #DBD8D3), paper specks (Fractal Noise, contrast 400, brightness -70, scale 4, in Multiply 35%), the subject cut out in
  colour (saturation -20) over a white Minimax rim of about 5 px at 1920. A white matted rim was rejected once in a music
  edit as "a pale white wash": check frames first.
- **Paper or cork grade** (`paperGrade` in scene_lib.jsx): light contrast, a small bloom.
- **Photo print:** a frozen frame in a white border over a huge glowing word with an eased drift (`printShot` in
  motion_lib.jsx); the music-edit version is in `cracked-edits.md` section 8.
- **Footage shrinking into a print on a page** (a desk-style reference).

## 12. Small effect facts
- Fractal Noise: -0002 noise type, -0004 contrast, -0010 scale, -0013 offset turbulence, -0015 complexity, -0023 evolution.
  Noise: -0001 amount, -0002 colour noise. Nested Fractal Noise params need a recursive property search.
- Mosaic: -0001 horizontal, -0002 vertical, -0003 sharp colours. Motion Tile: -0004 / -0005 output width / height in %.
- Radial Blur: -0001 amount, -0003 type (2 = zoom). A zoom Radial Blur above an amount of about 3 ghosts big crisp text
  into visible copies; 15-20 is fine on small textures.
- Drop Shadow opacity runs 0-255 from a script (use maxValue x 0.33); -0003 direction, -0004 distance, -0005 softness.
- Fill (`ADBE Fill`) is colorize plus output opacity: opacity 0 makes the layer invisible. To crossfade footage into a flat
  colour, key Tint's "Amount to Tint" with Map Black / White To set to the colour.
- Levels (`ADBE Easy Levels2`) takes no keyframes or expressions from a script: animate brightness another way (Exposure,
  a shape fill colour, layer opacity). Easy Levels and Hue/Saturation values set by script render correctly but read back
  as defaults after reopening; Pro Levels (Individual Controls) reads back fine.
- Speed lines parented to moving objects still have to sit below the whole group in the layer stack.
- In a shape layer the FIRST group in Contents draws on top: create top items first or move each new group to index 1
  (`moveTo(1)`, which keeps comp IDs, so Dynamic Link stays safe).
- Colorama's custom Output Cycle cannot be set by script: rebuild the palette from Gradient Ramps in a precomp and scroll it
  with Offset (library #5), or drive CC Toner's five tones by expression (library #7), or save an .ffx preset by hand once.

## 13. Where each look fits (taste)

| Look | Fits | Careful with |
|---|---|---|
| Analog night finish | documentary and mini-doc reels, narrated stories | client ads that want a clean premium look |
| Ordered dither, halftone | texture "here and there", section looks, backgrounds, objects | music edits: keep holds short; never hide the subject for 10+ frames |
| Smooth glow, element glow | UI moments, soft highlights | auras around people (banned), square edges, washed colours |
| Wave fields, LED wall, CC Sphere globe | designed explainer and brand scenes | native posts (designed motion is an ad tell there) |
| Character grids, typing | tech and AI reels | |
| Paper, photocopy, prints | editorial collage moments, desk-style docs | white rims (pale wash) |

Native social posts use none of these: real footage, one caption, the house look.
