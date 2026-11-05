# 16. Linked Effects (Ctrl+Alt+C)

Recipe name in the study: "Copy With Property Links (Ctrl+Alt+C) glow shapes". Category: technique_demo. Source: a tutorial creator's reel (DcBTMVShtWj). Confidence of the recipe: high.

Native build: `../ae/effects/copy_with_property_links_glow_shapes.jsx` (function `build_copy_with_property_links_glow_shapes()`).

## What it looks like

Black comp with 10 flat blue shapes (#1E82E9: diamonds, a circle, squares, a rectangle, hexagons, ~150-190 px, scattered, a few rotated ~15-20 deg). Shape Layer 1 carries an effect stack that makes it look printed/neon: slightly chewed edges (Roughen Edges), fine grain texture, a soft blue halo (Deep Glow) and a faint offset shadow; the styled blue reads #1F8CF4-#27A0F7 with a dark navy halo (#020613) just outside the edges. After Copy With Property Links (Ctrl+Alt+C) and paste on layers 2-10, every shape shows the same look, and dragging the master's Deep Glow Exposure (0.08 -> 0.20) or Add Grain Intensity/Size updates all ten in real time.

## Inputs

- no footage; 10 simple shape layers

## Layer stack

Shape Layer 10 ... Shape Layer 2 (each with linked copies of the stack), Shape Layer 1 = master with Roughen Edges > Deep Glow 2 > Drop Shadow > Add Grain, black background (comp bg or solid #010101). Comp named 'Tut' in the reel.

## Steps

1. Comp 'Tut' 1920x1080 (reel comp is landscape), 30 fps, 10 s, bg #000000.
2. Create 10 shape layers (polystar hexagon, rect, ellipse, rotated squares) filled #1E82E9, sizes 150-190 px, scattered; name Shape Layer 1-10 (layer 10 on top).
3. On Shape Layer 1 add in order: Roughen Edges, Deep Glow 2, Drop Shadow, Add Grain with the values below.
4. Script equivalent of Ctrl+Alt+C / Ctrl+V: on layers 2-10 add the same four effects and set an expression on every settable property: comp("Tut").layer("Shape Layer 1").effect("<Effect Name>")("<Property Name>") (that is exactly what Copy With Property Links writes).
5. Demo animation on the master: Deep Glow Exposure 0.08 (0f) -> 0.20 (30f) -> 0.08 (60f); Add Grain Intensity 0.3 -> 0.7 -> 0.3 to show all layers following.

## Effects used

- **Roughen Edges** (`ADBE Roughen Edges`) on Shape Layer 1 (master): Edge Type Roughen; Edge Color (inactive for Roughen) peach #E0A080; Border 8.00; Edge Sharpness 1.00; Fractal Influence 1.00; Scale 100.0; Stretch Width or Height 0.00; Offset (Turbulence) 0.0,0.0; Complexity 2; Evolution 0x+0.0; Evolution Options default.
- **Deep Glow 2** (`PEDG2`) on Shape Layer 1 (master): Radius 500.00; Exposure 0.17 (seen 0.08, 0.09, 0.10, 0.17, 0.20 while tweaking); Threshold 55.00 %; Threshold Smooth 55.00 %; Blend Mode Screen; View Final Render; Source Opacity 100.00 %; Unmult checked. Read from Deep Glow v1 panel.
- **Drop Shadow** (`ADBE Drop Shadow`) on Shape Layer 1 (master): Shadow Color assumed #000000 (swatch hidden); Opacity 50 %; Direction 0x+135.0; Distance 5.0; Softness 19.0; Shadow Only off.
- **Add Grain** (`VISINF Grain Implant`) on Shape Layer 1 (master): Viewing Mode Final Output; Preset [None]; Tweaking > Intensity 0.700; Size 0.300; Softness, Aspect Ratio, Channel Intensities, Channel Size, Color, Application, Animation, Blend with Original default.

## Keyframes

None in the reel (values dragged live). Demo: master Deep Glow Exposure 0.08 @0f, 0.20 @30f, 0.08 @60f, Easy Ease.

## Expressions

On every effect property of Shape Layer 2-10: comp("Tut").layer("Shape Layer 1").effect("Roughen Edges")("Border") etc. (one per property, same effect/property names). Ctrl+Alt+C = Edit > Copy With Property Links; Ctrl+V pastes the effects with these expressions.

## Third-party plug-ins and native stand-ins

Deep Glow v1 in the reel -> Deep Glow 2 (PEDG2). Native fallback: Glow (ADBE Glo2) Threshold 55 %, Radius 120, Intensity 1.2, Screen. Motion Tools / Fast Layers panels are UI only.

## What the reel did not show (inferred)

Drop Shadow colour swatch hidden by the face cam (assumed black); Add Grain values beyond Intensity/Size not expanded (defaults assumed); exact shape sizes/positions estimated from the viewer; comp size assumed 1920x1080 from the viewer aspect.
