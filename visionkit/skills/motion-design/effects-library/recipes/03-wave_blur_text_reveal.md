# 03. Wave Blur Text

Recipe name in the study: "Wave blur (Camera Lens Blur driven by a wave-warped moving blur map)". Category: reveal. Source: a tutorial creator's reel (Daacg6ktthE). Confidence of the recipe: medium.

Native build: `../ae/effects/wave_blur_text_reveal.jsx` (function `build_wave_blur_text_reveal()`).

## What it looks like

1920x1080, 30 fps, about 72 f. White background #FDFDFD with soft blue clouds: top-left corner #7BB9F4, bottom-centre and bottom-right #7DBAF3 to #94C6F6, centre pure white. A black-navy wordmark ('TITLE' in the builder; #000B17 darkest, neo-grotesk medium/semibold, tight tracking) sits centred. f0: the word is about 170% scale and almost entirely bokeh-blurred, with hexagon iris, edges 45-70 px wide and the blurred letters taking on the light-blue background. The sharp region then spreads from the top-left along a wavy diagonal edge (sine wavelength ~421 px, amplitude ~26 px, soft by ~60 px) that runs from lower-left to upper-right and travels down/right. f6-f12: the first two letters sharp (edge 5-7 px) while the third is at 9-21 px and the last two at 40-70 px. f30: left half sharp, the last two letters still at 30-52 px. The front slows, then picks up again near the end, and by about f64 everything is sharp (edges under 17 px). Meanwhile the word scales from ~170% to 100% by f26 with a strong ease-out, holds near 100%, then pulls back to ~81% by f72 with an accelerating ease-in (camera pull-back). The text stays centred the whole time.

## Inputs

- a short word of text (a wordmark; the builder uses 'TITLE')
- no footage; the background is a white solid plus 3-4 blurred blue ellipse shapes (can be generated)

## Layer stack

Comp 'Wave Blur' 1920x1080, 30 fps, 72 f, top to bottom: 1 'Adjustment layer' (adjustment, Camera Lens Blur); 2 'Map' (precomp 1920x1080 of the shape layer, visibility OFF, used only as the blur map; it must be a precomp because Blur Map uses 'Source', which ignores effects on the layer itself); 3 'TITLE' (text); 4 'Shapes' (precomp of blue blobs + Gaussian Blur); 5 'BG' (white solid #FDFDFD). Inside 'Map': 'Shape Layer 1' (white fill, no stroke) carrying Wave Warp then Fast Box Blur, with position keyframes. No parenting, no track mattes.

## Steps

1. Create comp 'Wave Blur' 1920x1080, 30 fps, 72 frames. Add solid 'BG' #FDFDFD.
2. Create precomp 'Shapes' (1920x1080, 72 f) with 3 ellipse shape layers, fill #4FA3F2, no stroke: A at (130,80) size 1000x650; B at (1750,1060) size 1100x620; C at (980,1180) size 1200x520. Add Gaussian Blur (ADBE Gaussian Blur 2) Blurriness 220, Repeat Edge Pixels off, on the precomp layer. Optionally drift each blob 30-40 px linearly over the comp. Place it above BG.
3. Add text 'TITLE': font Inter Display SemiBold (fallback SF Pro Display Medium / Helvetica Neue Medium), 300 px, tracking -20, fill #050B14, paragraph centre. Centre the anchor on the text and place it at (960,540).
4. Scale keys on 'TITLE': f0 170% (out: speed high, influence 5%) -> f26 100% (in: speed 0, influence 60%; out: speed 0, influence 70%) -> f72 81% (in: influence 10%, ie close to linear arrival). This gives a fast settle, a long hold, then an accelerating pull-back.
5. Create precomp 'Map' (1920x1080, 72 f). Inside, add a shape layer at position (960,540), anchor (0,0), with one path in layer space (comp coords minus 960,540): vertices (-1260,317), (1260,-221), (1260,1160), (-1260,1160). The top edge then runs from comp (-300,857) to (2220,319), ie through (0,793) and (1920,383), about 12 deg. Fill white #FFFFFF, no stroke.
6. On that shape layer add Wave Warp: Wave Type Sine, Wave Height 26, Wave Width 421, Direction 90, Wave Speed 1.0, Pinning All Edges, Phase 0, Antialiasing Low. Then Fast Box Blur: Blur Radius 22, Iterations 3, Blur Dimensions Horizontal and Vertical, Repeat Edge Pixels ON.
7. Position keys on the shape layer: f0 (960,320) (moved up so the white covers the whole word), f34 (960,540) (the edge cuts the word diagonally, its first letters sharp and its last ones blurred), f65 (960,770) (moved down below the word). Ease f0 -> f34: f0 out speed 3150 px/s, influence 4%; f34 in speed 0, influence 50%. Ease f34 -> f65: f34 out speed 0, influence 85%; f65 in influence 16.7% (near-linear arrival, so the front accelerates into the end).
8. Back in 'Wave Blur', put the 'Map' precomp above 'TITLE' and turn its video switch OFF.
9. Add an adjustment layer at the top with Camera Lens Blur: Blur Radius 9.0 (as read in the tutorial; use 28 to match the reference stills, see unreadable), Iris Shape Hexagon, Roundness 0, Aspect Ratio 1, Rotation 0, Diffraction Fringe 100, Blur Map Layer = 'Map' (layer index 2) with Source, Channel Luminance, Placement Center Map, Blur Focal Distance 0, Invert Blur Map off, Highlight Gain 0, Threshold 204 (8-bpc), Saturation 0, Repeat Edge Pixels on, Use Linear Working Space on.
10. Render: luminance white (the shape) = blurred, transparent/black = sharp, so the sharp area grows as the shape slides down.

## Effects used

- **Wave Warp** (`ADBE Wave Warp`) on Map > Shape Layer 1: Wave Type Sine; Wave Height 26; Wave Width 421; Direction 0x+90.0; Wave Speed 1.0; Pinning All Edges; Phase 0x+0.0; Antialiasing (Best Quality) Low
- **Fast Box Blur** (`ADBE Box Blur2`) on Map > Shape Layer 1: Blur Radius 22.0; Iterations 3; Blur Dimensions Horizontal and Vertical; Repeat Edge Pixels on
- **Camera Lens Blur** (`ADBE Camera Lens Blur`) on Adjustment layer: Blur Radius 9.0 (scrubbed up from 5.0); Iris Shape Hexagon; Roundness 0%; Aspect Ratio 1.0; Rotation 0x+0.0; Diffraction Fringe 100.0; Blur Map Layer '2. Map' / Source; Channel Luminance; Placement Center Map; Blur Focal Distance 0; Invert Blur Map off; Highlight Gain 0; Threshold 26214 (16-bpc display, about 204/255); Saturation 0; Edge Behavior Repeat Edge Pixels on; Use Linear Working Space on
- **Gaussian Blur** (`ADBE Gaussian Blur 2`) on Shapes (precomp of blue blobs): Blurriness ~220 (inferred; the tutorial shows only an fx badge on [Shapes])

## Keyframes

Map shape Position: f0 [960,320] -> f34 [960,540] -> f65 [960,770] (tutorial: middle key at 0:00:01:04, first frame 'moved up', last frame 0:00:02:05 'moved down'). Speed graph read: ~3150 px/s at f0 decaying to 0 at f34, then a slow rising segment. Fit: f0 out 3150 px/s / 4%, f34 in 0 / 50%, f34 out 0 / 85%, f65 in ~16.7%. TITLE Scale: f0 170% -> f26 100% -> f72 81% (measured from the finished render: ~170, 125 at f4, 105 at f14, 100 at f34, 94 at f54, 88 at f64, 81 at f70).

## Expressions

none

## Third-party plug-ins and native stand-ins

The tutorial uses the Flow 2.0 (SuperFlow) panel to set the ease curve, plus the Fast Layers / EaseCopy helper panels. These are workflow helpers only, with no render plugin. The native route is to set KeyframeEase values directly as given. Everything else is native.

## What the reel did not show (inferred)

(1) Camera Lens Blur radius: the tutorial copy shows 9.0, but the finished reference blurs letters with 10-90% edges of 45-70 comp px and fades the last letter to #8BBBF0. That needs about 25-35 px, so use 28 to match the reference (the hero comp was probably a different or bigger version). (2) Exact path vertices and key positions were not shown numerically. The edge line was measured from the viewer (through comp (0,793) and (1920,383) at the middle key), and the up/down offsets (-220 / +230) come from the speed-graph integral (~220 px for segment 1) and from when the reference becomes fully sharp. (3) The second segment's graph was partly hidden; its ease is inferred as an accelerating ease-in. (4) The text's scale/camera keys were not shown ('add some text animations and camera movements'); values are measured from the finished render. (5) Font name is not shown; Inter Display SemiBold is the closest look. (6) Blue blob layout is inferred from the colour samples.
