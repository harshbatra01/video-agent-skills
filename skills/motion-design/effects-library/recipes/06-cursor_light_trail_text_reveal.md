# 06. Cursor Reveal

Recipe name in the study: "Cursor reveal". Category: reveal. Source: a tutorial creator's reel (DaVUZK3ywAw). Confidence of the recipe: high.

Native build: `../ae/effects/cursor_light_trail_text_reveal.jsx` (function `build_cursor_light_trail_text_reveal()`).

## What it looks like

Black 1920x1080 comp. White text 'Go with the flow.' (the builder's line; SF Pro Display Regular ~155 px, tracking about -15, centred at x960, baseline y595; glyphs span x365-1553, glyph top y481) is revealed left to right by a thin white vertical cursor line (5 px wide, ~150 px tall, y462-612). Cursor starts at x340 (25 px left of the 'G') and stops at x1572 (19 px right of the period). In the finished version (intro card) the move takes 26 frames with a violent start and a long settle: comp-x progress per frame 0, .05, .13, .26, .39, .51, .60, .67, .72, .77, .80, .84, .86, .89, .91, .92, .94, .96, .97, .97, .98, .99, 1.0 (peak speed ~5000 px/s at frames 3-4). Text exists only to the left of the cursor. A light-trail bar the height of the text (120 px, roundness 9, y~478-598) sits ON TOP of the text, its right edge locked to the cursor; its alpha ramps from 0 at the tail to ~90 % at the cursor and its colour runs #1E52A1 (tail) -> #0F71F8 (middle) -> #09B1F7 (cursor), so letters inside the trail read tinted (white -> #2AB5F2 next to the cursor) and the empty part of the bar reads #081629 -> #10376C -> #1169AD -> #109AD4. Trail length is 0 at frame 0, grows to ~855 px around frame 12 (cursor at its fastest) and shrinks back to 0 by the last frame, so the end state is plain white text and a white cursor. Deep Glow on trail and cursor adds a cyan bloom (#22C8F0 core) spreading ~150 px around the leading edge and a soft blue haze under the trail. The intro card loops it every ~35 frames.

## Inputs

- one line of text (default 'Go with the flow.')
- no footage: black solid background

## Layer stack

Top to bottom: 1 'Cursor' shape layer (pen path, white stroke 5 px) + Deep Glow 2; 2 'Reveal Matte' shape layer = duplicate of the trail rectangle with Solid white fill, parented to Cursor, video off (used as matte); 3 'Light Trail' shape layer (rectangle + Gradient Fill) parented to Cursor + Deep Glow 2, Normal mode; 4 text 'Go with the flow.' with Track Matte = layer 2 'Reveal Matte', Alpha Matte; 5 'Black Solid 2' 1920x1080 #000000. No precomps. Project 16 bpc.

## Steps

1. Project to 16 bpc. New comp 'Cursor Reveal' 1920x1080, 30 fps, duration 35 frames (1:05) so it loops like the intro card (tutorial comp 'Tut2' had its work area end at 1:04).
2. Add solid 'Black Solid 2' 1920x1080, #000000.
3. Add point text 'Go with the flow.': font SFProDisplay-Regular (installed; Medium is the close alternative), 155 px, tracking -15, fill #FFFFFF, no stroke, centre-justified, position (960, 595).
4. Add shape layer 'Cursor': one path with vertices (0,-75) and (0,75), Stroke #FFFFFF width 5, butt or round cap, no fill. Layer anchor (0,0), Position (340, 540). (Tutorial values: anchor -620,-1.8 / position 340,540 because the line was drawn off-centre; keep anchor on the line instead.)
5. Keyframe Cursor Position: 0f (340,540) -> 26f (1572.2,540). Temporal ease: key 1 outgoing speed 0 influence 20 %, key 2 incoming speed 0 influence 95 % (equivalent cubic-bezier 0.20,0,0.05,1). Spatial interpolation linear.
6. Add shape layer 'Light Trail': Rectangle path Size (1365.4, 119.7), Position (0,0), Roundness 9; no stroke (width 0). Set the layer Anchor Point to (682.7, 0) so its right edge is the anchor, parent it to 'Cursor' and set its Position to (0, -2) (cursor-layer space) so the right edge rides on the cursor and the bar is centred on y538.
7. Give 'Light Trail' a Gradient Fill (Linear): colour stops 0 % #1E52A1, 50.2 % #0F71F8, 100 % #09B1F7; opacity stops 0 % = 0, 100 % = 100. If the gradient colour property cannot be set by script, use the native fallback in the third_party field.
8. Keyframe the Gradient Fill Start Point / End Point (rectangle group space, rect spans x -682.7..+682.7): 0f start (735.0,-11.8) end (894.0,-13.5); 12f start (-171.9,-15.2) end (679.9,8.4); 34f (last frame) start (735.0,-11.8) end (894.0,-13.5). Easy Ease (F9, 33.33 %) on the 12f keys; first/last keys linear. At 0f and 34f both points lie right of the bar so the whole bar is transparent.
9. Duplicate 'Light Trail' -> rename 'Reveal Matte', change its fill to a Solid Fill #FFFFFF (delete the gradient keys on it), keep the same parent and transform, place it above 'Light Trail', and turn its video off.
10. Set the text layer's Track Matte to 'Reveal Matte', Alpha Matte (AE 2023+ track-matte layer picker). Layer order as in layer_stack.
11. Apply Deep Glow 2 (PEDG2) to 'Light Trail' and to 'Cursor' with Radius 500, Exposure 0.03, Threshold 50 %, Threshold Smooth 50 %, Blend Mode Screen, Source Opacity 100 %, Unmult on. Compare against ref_cursor_light_trail_reveal_glow_58.67.png and retune Exposure if Deep Glow 2 renders brighter than the v1 shown.
12. Optional: for the reel-intro look, nest this comp into a 1080x1920 card (see howto_title_card_intro) and loop it with loopOut('cycle') on time remap.

## Effects used

- **Deep Glow 2** (`PEDG2`) on Light Trail: Radius 500.00; Exposure 0.03; Input > Threshold 50.00 %; Threshold Smooth 50.00 %; Mask none; Style > Blend Mode Screen; Gamma Correction/Aspect Ratio/Chromatic Aberration/Tint default; Quality default; View Final Render; Source Opacity 100.00 %; Unmult checked (Required for Alpha). Read from the Deep Glow v1 panel (unregistered) at 60.5 s.
- **Deep Glow 2** (`PEDG2`) on Cursor: Same as Light Trail: Radius 500, Exposure 0.03, Threshold 50 %, Threshold Smooth 50 %, Blend Screen, Unmult on. VO says 'add deep glow on the reveal shape and cursor with these settings', only one panel shown.
- **Gradient Fill (shape contents)** (`ADBE Vector Graphic - G-Fill`) on Light Trail: Type Linear; Colors: 0 % #1E52A1 (H216 S82 B63), 50.2 % #0F71F8 (H215 S94 B97), 100 % #09B1F7 (H198 S96 B97); Opacity stops 0 % -> 0, 100 % -> 100; Start/End Point keyed (see keyframes); Blend Mode Normal; Composite Below Previous in Same Group.
- **Rectangle Path (shape contents)** (`ADBE Vector Shape - Rect`) on Light Trail / Reveal Matte: Size 1365.4 x 119.7; Position 0,0; Roundness 9. Stroke Width 0. Tutorial layer transform: Anchor -70,-1.4, Position -1302.2,-1.7 in parent space (replaced here by anchor 682.7,0 so the right edge sits on the cursor).
- **Stroke (shape contents)** (`ADBE Vector Graphic - Stroke`) on Cursor: Color #FFFFFF; Stroke Width 5; Line Cap butt (first icon highlighted); Line Join miter. Fill Color white was also set but a 2-point path has no fill area.

## Keyframes

Cursor Position: 0f (340,540) -> 26f (1572.2,540); key1 out speed 0 infl 20 %, key2 in speed 0 infl 95 % (fit to the finished card, error 0.001). Tutorial project instead: 0f -> 1:03 (33f) with Flow preset cubic-bezier(0.36,0.01,0.00,0.97) = out infl 36 %, in infl 100 %; check value 1259.5 at 0:00:00:13 matches. Light Trail Gradient Fill Start Point / End Point: 0f (735.0,-11.8)/(894.0,-13.5) linear; 12f (-171.9,-15.2)/(679.9,8.4) Easy Ease 33.33 %; 34f (735.0,-11.8)/(894.0,-13.5) linear (tutorial: last frame 1:03, middle 0:00:00:12, first frame = pasted last keys).

## Expressions

None in the reel. For looping in a parent comp: enable Time Remap on the nested layer and use loopOut('cycle'). If using the effect-based fallback for the gradient, drive Gradient Ramp/Linear Wipe points from the same Start/End keys via Point Controls with layer.toComp().

## Third-party plug-ins and native stand-ins

Reel uses Deep Glow v1 (unregistered) -> installed Deep Glow 2, match name PEDG2, same values. Native-only fallback: Glow (ADBE Glo2) twice on each layer: pass 1 Glow Threshold 50 %, Glow Radius 40, Glow Intensity 1.0, Glow Operation Screen, Composite Original On Top; pass 2 Threshold 50 %, Radius 250, Intensity 0.6. The curve tool 'Flow 2.0', 'Fast Layers' and 'EaseCopy' panels are UI helpers only; native keyframe influence values replace Flow. If the shape Gradient Fill colours cannot be set from ExtendScript, build the trail colour with Gradient Ramp (ADBE Ramp, Linear, Start Color #1E52A1 at the trail tail, End Color #09B1F7 at the cursor, plus a Curves boost of the middle blue toward #0F71F8) and the alpha ramp with Linear Wipe (ADBE Linear Wipe, Wipe Angle 270 deg, Feather = trail length) on a solid-filled rectangle.

## What the reel did not show (inferred)

Font of the reel's line never shown: SF Pro Display Regular inferred by rendering SF Pro and Inter over the reference (SF Pro matched glyph shapes; width matched with tracking -15; Medium is possible). Cursor line length/position in its own layer space not readable (anchor -620,-1.8 suggests the line was drawn off the anchor): length ~150 px measured from the card. The finished intro card moves faster than the tutorial keys (26 vs 33 frames), so the ease was fitted from per-frame card measurements (out 20 / in 95). Deep Glow 2's parameter names/response may differ from v1; Exposure 0.03 may need retuning. Exact text size measured in card space (0.42 scale) so +/-3 px.
