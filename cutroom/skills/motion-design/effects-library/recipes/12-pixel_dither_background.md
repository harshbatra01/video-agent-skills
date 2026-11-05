# 12. Pixel Dither Background

Recipe name in the study: "Pixel Dither background". Category: stylize. Source: a tutorial creator's reel (DdtmTkIAf12, Ddtm_TUgYiZ). Confidence of the recipe: medium.

Native build: `../ae/effects/pixel_dither_background.jsx` (function `build_pixel_dither_background()`).

## What it looks like

A blue-sky cumulus time-lapse rendered as a 1-bit two-colour print with no grey levels other than compression softening. Bright cloud is paper #f3fbfd (brightest #f4fafd), and every 4 px cell (1920-wide comp; measured 3.85 px at 1904) carries a small fixed ink dot, so white areas show a fine 4 px dot lattice. Open sky is flat ink #65bad2 (darkest #5eb4cc) with a faint lighter dot lattice. Mid-tones break into a 12 px super-cell (3x3 cells) ordered-dither texture of rounded-square rings and plus-shaped 2x2 clusters, which makes cloud edges stair-step in 4 px blocks. The clouds billow UPWARD slowly (the cloud top climbs about 150 px over 60 frames because the source is slowed about 50%), while the dot grid stays locked to the screen. Everything in the plate scales together when the camera punches in 3.75x (cells become about 15 px), so the dither is baked before any camera move. On top of the dither sits a wordmark ('TITLE' in the builder) made of 24 px square blocks: solid opaque #7ecadd (lighter than the sky), not dithered, an eroded serif pixel font with notches and missing blocks. In 16:9 it spans about 75% of frame width x 32.5% of height (x 175-1600, y 365-715 of 1904x1078), centred at 47% x / 50% y, and the glass search bar covers its middle. In 9:16 the same plate fills the portrait frame and the wordmark is about 150% of frame width, cropped on both sides, at y 42-59%.

## Inputs

- a cumulus cloud time-lapse with clean blue sky and bright white billowing clouds rising from the bottom third, static camera, 1080p or larger (16:9 for the landscape version; it can be cropped for 9:16)
- a heavy serif font for the wordmark text (e.g. Georgia Bold or Times New Roman Bold); the builder's placeholder word is 'TITLE'
- a Python/PIL-generated threshold map PNG (1920x1080 and 1080x1920 8-bit grey) as described in the steps

## Layer stack

Comp PD_Source (1920x1080, 30 fps): cloud clip with Time Stretch 200% and Frame Blending = Pixel Motion. Comp PD_Wordmark (1920x1080): text layer 'TITLE' with Roughen Edges, then Mosaic, then Levels (Individual Controls) on alpha, then Fill. Comp PD_Plate (1920x1080, 30 fps, 16 bpc), top to bottom: [1] PD_Wordmark precomp, Normal, 100%; [2] ADJ_Dither adjustment layer, Normal: Threshold then Tint; [3] PD_Map = pd_threshold_1920x1080.png, blend mode SUBTRACT, Quality Draft, Position exactly 960,540, Scale 100%; [4] PD_Lum = PD_Source precomp, Normal: Shift Channels, Levels, Mosaic. PD_Plate is then placed in the hero comp under the glass bar and moved by the CAM null (see glass_search_bar_typing). There are no track mattes in the plate. For 9:16, build the same stack at 1080x1920 with the 1080x1920 map and a wordmark scaled about 2x.

## Steps

1. Generate the threshold map in Python (PIL), 8-bit grey, sized 1920x1080 (and 1080x1920). For each pixel: cx = x % 4, cy = y % 4, k = M[(y//4)%3][(x//4)%3] with the clustered centre-first 3x3 matrix M = [[7,3,6],[2,0,1],[8,4,5]], base = 0.05 + 0.9*(k+0.5)/9. If (cx,cy) == (1,1), T = 1.0 (always-ink dot); if (cx,cy) == (3,3), T = 0.0 (always-paper dot); otherwise T = base. Save T*255 as pd_threshold_1920x1080.png. If the mid-tone texture looks too blobby against ref_pixel_dither_background_texture_2.00.png, regenerate with the dispersed matrix M = [[0,7,3],[6,5,2],[4,1,8]].
2. Create PD_Source and import the cloud clip. Set Time Stretch to 200% and enable frame blending (Pixel Motion), because the reel says 'slow down your clip'.
3. Create PD_Plate (1920x1080, 30 fps, 16 bpc). Add PD_Source as layer PD_Lum.
4. On PD_Lum add Shift Channels: Take Alpha From Alpha, Take Red From Red, Take Green From Red, Take Blue From Red. This is grey from the red channel, which best separates blue sky from white cloud (the shader used Channel = Red).
5. On PD_Lum add Levels: Channel RGB, Input Black about 95, Input White 235, Gamma 1.10. Tune Input Black until the open sky is at least 95% ink and the cloud highlights keep only the fixed dot lattice.
6. On PD_Lum add Mosaic: Horizontal Blocks 480, Vertical Blocks 270 (4 px cells), Sharp Colors ON.
7. Import pd_threshold_1920x1080.png. Place it above PD_Lum at Position 960,540, Scale 100%, layer Quality Draft (nearest neighbour), Blend Mode SUBTRACT. The result is L - T: positive where the cell is brighter than its threshold.
8. Add an adjustment layer ADJ_Dither above both, with Threshold (Level 1), then Tint (Map Black To #5FB6CF, Map White To #F3FBFD, Amount to Tint 100%). Check: sky = flat cyan with faint paper dots, clouds = white with a 4 px ink-dot grid, mid-tones = 12 px ring clusters.
9. Optional softening to match the reel's compression: add Gaussian Blur 0.6 px on ADJ_Dither after Tint (Repeat Edge Pixels on).
10. Build PD_Wordmark: text layer 'TITLE', Georgia Bold (or any heavy serif), about 430 px, fill white, centred at (905, 540), with letter width adjusted so the word spans about 1440 px. Add Roughen Edges (Edge Type Roughen, Border 14, Edge Sharpness 1.0, Fractal Influence 1.0, Scale 60, Complexity 2). Add Mosaic (Horizontal Blocks 80, Vertical Blocks 45 = 24 px blocks, Sharp Colors ON). Add Levels (Individual Controls), Alpha: Input Black 120, Input White 136, to binarise the blocks. Add Fill (Color #7ECADD).
11. Put PD_Wordmark on top of PD_Plate, Normal, 100%. It must NOT be under the dither.
12. For the 9:16 build, repeat at 1080x1920 (Mosaic 270x480 cells, wordmark Mosaic 45x80 blocks, wordmark about 1600 px wide centred at y 920 so it is cropped both sides).

## Effects used

- **Shift Channels** (`ADBE Shift Channels`) on PD_Lum: Take Alpha From = Alpha; Take Red From = Red; Take Green From = Red; Take Blue From = Red
- **Levels** (`ADBE Easy Levels2`) on PD_Lum: Channel RGB; Input Black 95 (tune); Input White 235; Gamma 1.10 (the gamma value is from the shader panel); Output Black 0; Output White 255
- **Mosaic** (`ADBE Mosaic`) on PD_Lum: Horizontal Blocks 480; Vertical Blocks 270; Sharp Colors ON
- **Threshold** (`ADBE Threshold2`) on ADJ_Dither: Level 1
- **Tint** (`ADBE Tint`) on ADJ_Dither: Map Black To #5FB6CF (ink, sampled sky #65bad2 / darkest #5eb4cc); Map White To #F3FBFD (paper, sampled #f4fafd); Amount to Tint 100%
- **Roughen Edges** (`ADBE Roughen Edges`) on PD_Wordmark/text: Edge Type Roughen; Border 14; Edge Sharpness 1.0; Fractal Influence 1.0; Scale 60; Complexity 2
- **Mosaic** (`ADBE Mosaic`) on PD_Wordmark/text: Horizontal Blocks 80; Vertical Blocks 45 (24 px); Sharp Colors ON
- **Levels (Individual Controls)** (`ADBE Pro Levels2`) on PD_Wordmark/text: Alpha Input Black 120; Alpha Input White 136
- **Fill** (`ADBE Fill`) on PD_Wordmark/text: Color #7ECADD; Opacity 100%
- **Pixel Dither (Halftone)** (``) on invideo shader (reference only, not buildable): Grid Size 8.03; Shape Square (options Circle/Square/Line/Diamond/Cross); Channel Red; Color Mode Duotone; Sampling Bilinear; Angle -6.15; Dot Size Scale 10.54, dragged to 7.34; Aspect 1.01, dragged to 1.65; Random Seed 0.00; Center X 0.50; Center Y 0.50; Offset X 960.00; Offset Y 540.00; Contrast 1.00; Gamma 1.10; Brightness 0.00; Ink Color #1c749e; Paper Color #f0ece2; Alpha Paper off; Invert off

## Keyframes

None on the dither. PD_Source runs at Time Stretch 200% so the clouds rise about 2.5 px/frame at the cloud top. The camera keys are in glass_search_bar_typing (whole PD_Plate scaled 90-100%, then 375%).

## Third-party plug-ins and native stand-ins

The reel's look comes from an invideo agent-generated GLSL shader 'Pixel Dither (Halftone)', which is not available in AE. Native substitute: Shift Channels (red to grey), Levels, Mosaic 4 px, a pre-rendered 12 px threshold map in Subtract mode, Threshold, Tint (duotone). If writing a PNG is impossible, replace PD_Map with a white solid carrying Cell Pattern (Cell Pattern Bubbles, Disperse 0, Size 12, Contrast 100, Invert on) for the 12 px clustered screen. You lose the fixed 4 px dot lattice, which can be faked with Grid (Size From Width & Height Sliders 4x4, Border 1, Color #5FB6CF, Opacity 35%, Blending Mode Normal) on ADJ_Dither.

## What the reel did not show (inferred)

The hero's own shader settings were never shown. The panel values on screen (ink #1c749e / paper #f0ece2, dot size 10.54 then 7.34) belong to a demo state with a different palette, so the hero ink/paper were sampled from the render instead. The exact dither algorithm can't be read. From the pixels: 4 px cells plus a 12 px (3x3) ordered structure, a fixed dot inside every cell, and ink on dark/red-channel-dark areas. The clustered 3x3 matrix and the always-ink/always-paper dot pixels are inferred from that. Levels Input Black about 95 is a starting point; tune it so the sky reads near-solid ink. The wordmark font is unknown (an eroded serif pixel font); it is rebuilt as serif text, Roughen Edges, 24 px Mosaic.
