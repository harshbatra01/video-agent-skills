# 11. Mixed Media

Recipe name in the study: "Mixed Media Effect". Category: stylize. Source: a tutorial creator's reel (DdL719cApOS). Confidence of the recipe: medium.

Native build: `../ae/effects/mixed_media_cutout.jsx` (function `build_mixed_media_cutout()`).

## What it looks like

12 fps stepped (3/2 cadence in 30 fps). Background: monochrome photocopy look, high contrast with heavy grain and speckle, blacks lifted to ~#1E2327 (never pure black), mids #5A585D, sky and whites flattened to warm paper #DBD8D3 with tiny black dust specks; occasional thin white film scratches; luminance p1/p50/p99 = 23/101/216. Subject: keeps colour but ~20% desaturated (lavender hoodie #7F6D81, pants #292A2F), cut out with a white-grey sticker outline ~3 px at 1076 width (~5 px at 1920), colour #C8CDCE-#E8E8E8, slightly soft, no shadow. Grain/scratch overlay animates every frame (30 fps) on top of the 12 fps image. Transition from the original colour clip: at f13 the subject switches to the stylised cut-out first; then the background wipes right-to-left with a soft vertical edge (~40-60 px feather): edge at ~95% width f14, 55% f15, 50% f16, 42% f20, 20% f22, 2% f24, done f25 (expo ease-out, advancing in 12 fps steps). Presented in a 1076x1076 window at y 418-1494 of a 9:16 frame, above and below filled with the same footage at ~200%, heavily blurred and darkened.

## Inputs

- a 4-5 s action clip with one clear subject (reel: skateboarder in a purple hoodie, fisheye low angle, concrete architecture and overcast sky)
- a subject alpha matte for that clip (green-screen stock, or ~50 mattes generated outside AE at 12 fps); Roto Brush is not scriptable
- optional paper/dust/scratch texture overlay (can be generated with Fractal Noise)

## Layer stack

Comp MM_Square 1080x1080 at 24 fps (12 fps look), top to bottom: (1) MM_Grain adjustment layer: Noise (animates every frame). (2) MM_Original = colour footage with Linear Wipe for the reveal (only during the transition). (3) MM_Subject = footage, Alpha Matte from MM_Matte (matte layer hidden above it), Hue/Saturation + Unsharp Mask; Posterize Time 12. (4) MM_Outline = footage with the same matte, Fill white, Minimax Maximum 5 px on alpha, Gaussian Blur 0.8; Posterize Time 12. (5) MM_Paper = solid with Fractal Noise speckle, blend Multiply 35%, plus a large soft Fractal Noise in Overlay 15%. (6) MM_BG = footage: Posterize Time 12 -> Black & White -> Levels -> Unsharp Mask -> Noise -> Tint (black #1E2327, white #DBD8D3). For the vertical deliverable: Comp MM_Vertical 1080x1920: MM_Square centred at y 960 (square at y 420-1500); below it MM_Fill = MM_Square scaled 200%, Gaussian Blur 60, Exposure -1.6.

## Steps

1. Create MM_Square 1080x1080 24 fps; bring in footage and its matte.
2. MM_BG: Posterize Time 12; Black & White (defaults); Levels Input Black 25, Input White 205, Gamma 0.9, Output Black 30, Output White 222; Unsharp Mask Amount 200, Radius 2.5, Threshold 0; Noise Amount 35%, Use Color Noise off, Clipping on; Tint Map Black To #1E2327, Map White To #DBD8D3, Amount 100%.
3. MM_Paper: solid with Fractal Noise (Contrast 400, Brightness -70, Scale 4, Complexity 1, Evolution expression time*400) in Multiply at 35% so only dark specks appear on light areas; second solid Fractal Noise Scale 600, Contrast 60 in Overlay 15% for paper unevenness.
4. MM_Outline: footage + matte; Fill #E6E8E8; Minimax Operation Maximum, Radius 5, Channel Alpha, Direction Horizontal & Vertical; Gaussian Blur 0.8; Posterize Time 12.
5. MM_Subject: footage + matte; Posterize Time 12; Hue/Saturation Master Saturation -20; Curves slight S; Unsharp Mask Amount 60, Radius 1.5.
6. MM_Grain: adjustment layer with Noise 10% (monochrome) so grain flickers at the full frame rate; optional thin white scratch layer (Fractal Noise stretched vertically) in Screen 20% blinking on random frames.
7. Transition: MM_Original (colour footage) on top with Linear Wipe, Wipe Angle 270 deg (clears from the right), Feather 50; Transition Completion keyed per frame (see keyframes). Set MM_Subject and MM_Outline in-point 1 frame before the wipe starts so the sticker appears first.
8. For 9:16: nest MM_Square into MM_Vertical 1080x1920 at y 960; add MM_Fill below (scale 200%, Gaussian Blur 60, Exposure -1.6).

## Effects used

- **Posterize Time** (`ADBE Posterize Time`) on MM_BG, MM_Subject, MM_Outline: Frame Rate 12
- **Black & White** (`ADBE Black&White`) on MM_BG: defaults (Reds 40, Yellows 60, Greens 40, Cyans 60, Blues 20, Magentas 80); Tint off
- **Levels** (`ADBE Easy Levels2`) on MM_BG: Input Black 25; Input White 205; Gamma 0.9; Output Black 30; Output White 222
- **Unsharp Mask** (`ADBE Unsharp Mask2`) on MM_BG: Amount 200; Radius 2.5; Threshold 0
- **Noise** (`ADBE Noise2`) on MM_BG: Amount of Noise 35%; Noise Type Uniform; Use Color Noise off; Clipping on
- **Tint** (`ADBE Tint`) on MM_BG: Map Black To #1E2327; Map White To #DBD8D3; Amount to Tint 100%
- **Fractal Noise** (`ADBE Fractal Noise`) on MM_Paper: Fractal Type Basic; Noise Type Block; Contrast 400; Brightness -70; Scale 4; Complexity 1; Evolution time*400; layer blend Multiply 35%
- **Fill** (`ADBE Fill`) on MM_Outline: Color #E6E8E8; Opacity 100%
- **Minimax** (`ADBE Minimax`) on MM_Outline: Operation Maximum; Radius 5; Channel Alpha; Direction Horizontal & Vertical
- **Gaussian Blur** (`ADBE Gaussian Blur 2`) on MM_Outline: Blurriness 0.8
- **Hue/Saturation** (`ADBE HUE SATURATION`) on MM_Subject: Master Saturation -20
- **Noise** (`ADBE Noise2`) on MM_Grain (adjustment): Amount of Noise 10%; Use Color Noise off
- **Linear Wipe** (`ADBE Linear Wipe`) on MM_Original: Wipe Angle 270 deg; Feather 50; Transition Completion keyed
- **Gaussian Blur** (`ADBE Gaussian Blur 2`) on MM_Fill (vertical only): Blurriness 60; Repeat Edge Pixels on
- **Exposure** (`ADBE Exposure2`) on MM_Fill (vertical only): Exposure -1.6

## Keyframes

Reveal (30 fps, relative to wipe start s): MM_Subject + MM_Outline in at s-1. Linear Wipe Transition Completion on MM_Original: s: 5%, s+1: 45%, s+2: 50%, s+6: 58%, s+8: 80%, s+10: 98%, s+11: 100% (hold keyframes so it steps). Reel timings: subject f13, wipe f14-f25; the same wipe repeats at 20.4-20.7 s (f612-f621).

## Expressions

Fractal Noise Evolution: time*400. Optional scratch flicker opacity: (Math.random()<0.15)?25:0 with seedRandom(Math.floor(time*30),true).

## Third-party plug-ins and native stand-ins

invideo extracted 12 fps stills and restyled each with an image model from an .md 'style profile' and a reference video. Native substitute: Posterize Time 12 + Black & White/Levels/Unsharp/Noise/Tint photocopy background + Fractal Noise paper specks + colour subject from a matte + Minimax white outline + Linear Wipe reveal.

## What the reel did not show (inferred)

The .md rulebook and reference video content are never shown, and the image model output varies per frame (texture boils between stills), so all parameter values are inferred from sampled colours. Outline width is ~3 px at 1076 wide. Whether the subject was colour-graded beyond desaturation is unclear.
