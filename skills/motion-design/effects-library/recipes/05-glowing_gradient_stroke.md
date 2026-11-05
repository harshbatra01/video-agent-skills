# 05. Glowing Stroke

Recipe name in the study: "Glowing gradient stroke (tapered line, Colorama colour cycle, track matte, Deep Glow)". Category: stylize. Source: a tutorial creator's reel (DbGCgZrP-GU). Confidence of the recipe: high.

Native build: `../ae/effects/glowing_gradient_stroke.jsx` (function `build_glowing_gradient_stroke()`).

## What it looks like

1920x1080, 30 fps, 30-frame loop on black. A dark rounded 'prompt box' (about 1084x185 px, centred) has a 2 px line along its bottom edge at y=633 from x~471 to x~1449. f0-f8: a thin blue line draws on left to right (trim end 0 to 100, easy ease). f0-f4: a tapered glowing core fades in on top of it (thick in the middle, tapering to points over the outer 40% at each end). Its colour comes from a palette scrolled left to right across the line: white #F7F7FA -> red #E1000A -> orange-red #E83004 -> white -> cyan #19FBF5 -> blue #0A5FD4 -> white, about 1.7 palette cycles per loop, very fast at the start and slowing to a stop at f30. At a fixed point the colour goes teal -> red -> white hotspot -> blue -> teal. A huge soft haze in the current colours (Deep Glow radius 1000) fills the area around the line, so the black card picks up red/teal/blue light. Values measured on the downscaled reference line: teal #31B4A5, red #86020D to #A0261E, hotspot #A66D6D/#9398A2, blue #2748A2.

## Inputs

- a short line of UI text ('Go with the flow.' in the builder) and an up-arrow icon (can be a shape layer)
- no footage

## Layer stack

Comp 'Glowing Stroke' 1920x1080, 30 fps, 30 f, top to bottom: 1 'Black Solid 2' (1920x1080 solid, Gradient Ramp + Colorama, Track Matte = layer 2 'Shape Layer 2', Alpha Matte, Normal mode); 2 'Shape Layer 2' (tapered duplicate line + Deep Glow 2 + opacity keys; acts as matte, auto-hidden); 3 'Shape Layer 1' (2 px line + Trim Paths, visible); 4 'Arrow' (send icon, white); 5 'Go with... flow. 2' (scribble text, see prompt_scribble_typeon); 6 'Go with the flow.' (white text); 7 'Fill' (rounded-rect shape, the prompt box). No parenting.

## Steps

1. New comp 1920x1080, 30 fps, 30 frames, background black.
2. 'Fill': rectangle shape 1084x185, Roundness 60, position (960,540), fill #0A0A0B (optional 1 px stroke #1C1C1E).
3. 'Shape Layer 1': pen path from (471,633) to (1449,633) (layer at 960,540, anchor 0,0, so vertices (-489,93) and (489,93)). Stroke 2 px #2F5BFF, no fill, Line Cap Round. Add Trim Paths: Start 0, Offset 0, Trim Multiple Shapes Simultaneously. End key 0 f = 0%, 8 f = 100%, Easy Ease.
4. Duplicate it as 'Shape Layer 2' (anchor (-1.5,93), position (960,633)). Delete its Trim Paths. On Stroke 1 > Taper: Length Units Percent, Start Length 40%, End Length 40%, Start Width 0, End Width 0, Start Ease 0, End Ease 0. Stroke stays 2 px.
5. On Shape Layer 2 add Deep Glow 2: Glow Mode Exponential, Blend Mode Screen, Radius 1000, Exposure 0.15, View Final Result, Source Opacity 100%, Unmult ON. Opacity key 0 f = 0%, 4 f = 100%, Easy Ease.
6. Add 'Black Solid 2' 1920x1080 at (960,540) above. Gradient Ramp: Start of Ramp (-6,544) colour #000000, End of Ramp (1944,536) colour #FFFFFF, Linear Ramp, Scatter 0, Blend 0%.
7. Colorama on the solid: Input Phase > Get Phase From Intensity; Add Phase None / Source, Add Phase From Intensity, Add Mode Wrap. Output Cycle custom stops (angle clockwise from top): 0 deg #F7F7FA, 48 deg #E1000A, 120 deg #E83004, 180 deg #F2F9F7, 240 deg #19FBF5, 307 deg #0A5FD4. Cycle Repetitions 1, Interpolate Palette on, Composite Over Layer on, Blend With Original 0%.
8. Phase Shift key 0 f = 0x+0.0 deg, 30 f = -1x-261.0 deg (-621 deg). Ease: 0 f out speed -10000 deg/s, influence 4%; 30 f in speed 0, influence 40%.
9. SCRIPT SUBSTITUTE for steps 6-8, because Colorama's Output Cycle cannot be set from ExtendScript. Generate a 1920x1080 PNG where column x has the palette colour at angle 360*(x+6)/1950, linear RGB interpolation between the stops above, wrapping 360 back to white. Import it and add Offset (ADBE Offset): Shift Center To key 0 f (960,540) -> 30 f (4272,540) (= +1.725 widths, so the colours scroll right), Blend With Original 0, same ease (out influence 4% with speed ~10000/360*1920 = 53300 px/s, in 0 @40%). Use this layer in place of Black Solid 2.
10. Set the track matte of Black Solid 2 (or the palette layer) to Shape Layer 2, Alpha (layer.setTrackMatte(shapeLayer2, TrackMatteType.ALPHA)). The matte includes Deep Glow's alpha, so the haze takes on the palette colours.
11. Add the text 'Go with the flow.' (Inter Regular 76 px, #F2F2F2, left at x~520, baseline ~565) and a white up-arrow icon at (~1400,540) (3 px stroke, ~40 px tall) above Fill.

## Effects used

- **Gradient Ramp** (`ADBE Ramp`) on Black Solid 2: Start of Ramp -6.0,544.0; Start Color black; End of Ramp 1944.0,536.0; End Color white; Ramp Shape Linear Ramp; Ramp Scatter 0.0; Blend With Original 0.0%
- **Colorama** (`APC Colorama`) on Black Solid 2: Input Phase: Get Phase From Intensity; Add Phase None / Source; Add Phase From Intensity; Add Mode Wrap; Phase Shift KEYED 0x+0.0 (0 f) -> -1x-261.0 (1:00). Output Cycle: Use Preset Palette [none], custom triangles at 0 deg white #F7F7FA, 48 deg red #E1000A, 120 deg orange-red #E83004, 180 deg white #F2F9F7, 240 deg cyan #19FBF5, 307 deg blue #0A5FD4 (hex sampled from the wheel); Cycle Repetitions 1.00; Interpolate Palette on; Composite Over Layer on; Blend With Original 0%
- **Deep Glow 2** (`PEDG2`) on Shape Layer 2: Glow Mode Exponential; Blend Mode Screen; Radius 1000.00; Exposure 0.15; View Final Result; Source Opacity 100%; Unmult on (Required for Alpha); preset label INTRO-HD
- **Trim Paths (shape operator)** (`ADBE Vector Filter - Trim`) on Shape Layer 1: Start 0.0%; End KEYED 0% (0 f) -> 100% (8 f) Easy Ease; Offset 0x+0.0; Trim Multiple Shapes Simultaneously
- **Stroke Taper (shape stroke sub-group)** (`ADBE Vector Stroke Taper`) on Shape Layer 2: Length Units Percent; Start Length 40.0%; End Length 40.0%; Start Width 0.0%; End Width 0.0%; Start Ease 0.0%; End Ease 0.0%
- **Offset** (`ADBE Offset`) on Palette layer (script substitute for Gradient Ramp + Colorama): Shift Center To KEYED (960,540) at 0 f -> (4272,540) at 30 f, out influence 4% / in 0 @40%; Blend With Original 0

## Keyframes

Shape Layer 1 Trim End: 0 f 0% -> 8 f 100%, easy ease. Shape Layer 2 Opacity: 0 f 0% -> 4 f 100%, easy ease. Colorama Phase Shift: 0 f 0 deg -> 30 f -621 deg (-1x-261.0); value at 29 f reads -1x-260.8; speed graph spike then long decay, in-handle at mid-span; fit out -10000 deg/s @3.6%, in 0 @40%.

## Expressions

none

## Third-party plug-ins and native stand-ins

Deep Glow 2 (installed, PEDG2), used as is. Native fallback if needed: two Glow (ADBE Glo2) on Shape Layer 2 (Glow Radius 60 / Intensity 2, and Glow Radius 600 / Intensity 1, Glow Operation Screen, Glow based on Alpha Channel). Colorama is native, but its custom Output Cycle cannot be scripted, so use the palette-PNG + Offset substitute above (same look, 1:1 phase mapping). The tutorial also shows the Vaultex, Fast Layers, EaseCopy and BOUNCr panels, which are UI helpers only.

## What the reel did not show (inferred)

(1) Shape Layer 1's stroke colour is only seen as a blue swatch; #2F5BFF is inferred from the faint blue line at the ends in the reference. (2) Palette stop angles and colours were sampled from the wheel UI (bt709), so they are about +/-3 deg and slightly UI-shaded. (3) The phase-shift speed graph's area matched ~261 deg rather than 621 deg, so its y labels may be misread; the ease shape fit was scaled to -621 deg (the value read twice from the panel). (4) Prompt box size/roundness, text font and arrow are inferred from the viewer at 100% zoom (rulers ~0.95 screen px per comp px). (5) Whether the Fill box has a gradient or border could not be read (it is nearly black on black).
