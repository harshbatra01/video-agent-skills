# 07. Gradient Depth Reveal

Recipe name in the study: "Gradient Depth Reveal". Category: reveal. Source: a tutorial creator's reel (DdwPfZJTGiP). Confidence of the recipe: high.

Native build: `../ae/effects/gradient_depth_reveal.jsx` (function `build_gradient_depth_reveal()`).

Partial match: built with a hand-made depth map from a person matte, because there was no real depth pass.

## What it looks like

A landscape (rolling green meadow, low hills, cumulus sky) first appears as pure pastel colour bands that follow depth: Colorama on the depth map. The bands cycle continuously through a looping palette of peach #ecc6a8, violet #c376e6, magenta-pink #d971d2, light pink #e8aeda and lavender #b195e0, at 200 deg of phase per second (one full loop every 1.8 s). The colours flow from far to near, so the sky (black in the depth map) changes colour as one flat field: violet #c973e2, then #d472d6, #de72c8, #e188cf, one step every 4 frames. The hills carry the next bands (light pink / lilac) and the foreground grass the bands after that (yellow-peach / purple), keeping the grass texture from the depth map. Then the real clip reveals by depth, nearest first. Over about 16-20 frames (30 fps) the foreground grass becomes real (purple-tinted at first), then the hills, and the sky last, with very soft transitions (Softness 100%) so it reads as a fog of colour receding into the distance. After the reveal the image is the clean clip.

## Inputs

- a landscape video with clear depth layering (foreground grass/flowers, mid hills, sky with clouds), 16:9, static or slow push-in
- the matching depth map video of that clip, white = near, black = far (e.g. Depth Anything; in the reel the invideo agent made it). Fallback when no depth map exists: build one in AE from a vertical Gradient Ramp plus the clip's blurred luminance (see steps)

## Layer stack

Comp 'Depth Reveal' (1920x1080; the reel's comp is 24 fps, so 30 fps is fine for the build; duration 5 s). Top to bottom: [1] 'Clip' = main landscape footage, Normal, with Gradient Wipe (Gradient Layer = layer 2, Source); [2] 'Depth Map' = depth video, Normal, with Colorama. The main clip must be ABOVE the depth map. No mattes or precomps needed. Optional fallback: [2] 'Depth Map' precomp DM_Fake made of a Gradient Ramp solid plus the clip in Overlay, then Gaussian Blur.

## Steps

1. Import the landscape clip and its depth map. Put both in comp 'Depth Reveal', with the depth map as layer 2 and the clip as layer 1 above it.
2. On 'Depth Map' add Colorama. Input Phase: Get Phase From Intensity; Add Phase None (Source); Add Phase From Intensity; Add Mode as default. Phase Shift: Alt-click the stopwatch and type the expression time*200.
3. Colorama Output Cycle: Use Preset Palette [none], custom wheel with 5 triangles at 0 deg peach #ECC6A8, 72 deg violet #C376E6, 135 deg magenta-pink #D971D2, 215 deg light pink #E8AEDA, 280 deg lavender #B195E0, all at 100% opacity. Cycle Repetitions 1.00, Interpolate Palette ON. Modify / Pixel Selection / Masking at defaults. Composite Over Layer ON, Blend With Original 0%.
4. Scripting note: the Colorama Output Cycle is custom arbitrary data and ExtendScript cannot set it. Either set it by hand once and save an .ffx preset that the script applies, or use the CC Toner fallback: delete Colorama and add CC Toner (Tones Pentone) on 'Depth Map', with colour expressions on Highlights / Brights / Midtones / Darktones / Shadows sampling the looping palette at offsets L = 1.0 / 0.75 / 0.5 / 0.25 / 0.0 plus time*200/360 (see expressions).
5. On 'Clip' add Gradient Wipe: Transition Softness 100%, Gradient Layer = 'Depth Map' with Source, Gradient Placement = Stretch Gradient to Fit, Invert Gradient OFF.
6. Keyframe Transition Completion: 100% at 0:00:01:00, then 0% at 0:00:01:15 (30 fps), both Easy Ease. Before 1 s the shot is pure colour bands; the reveal runs nearest-first because white (near) pixels become opaque first as completion drops.
7. Fallback depth map (no depth video): precomp DM_Fake, 1920x1080. Solid with Gradient Ramp (Linear, Start of Ramp (960,300) black, End of Ramp (960,1080) white). Above it, the landscape clip with Black & White (default), Blend Mode Overlay, 40%. Then an adjustment layer with Gaussian Blur 6 and Curves to push the sky to pure black and the foreground grass to bright white with texture. Use DM_Fake as layer 2.

## Effects used

- **Colorama** (`APC Colorama`) on Depth Map: Input Phase: Get Phase From Intensity; Add Phase None / Source; Add Phase From Intensity; Add Mode shown as 'Average'; Phase Shift 0x+0.0 with expression time*200. Output Cycle: Use Preset Palette [none]; 5 triangles about 0/72/135/215/280 deg, colours peach / violet / magenta-pink / light pink / lavender; selected triangle opacity 100%; Cycle Repetitions 1.00; Interpolate Palette ON. Composite Over Layer ON; Blend With Original 0%
- **Gradient Wipe** (`ADBE Gradient Wipe`) on Clip: Transition Completion keyed 100% to 0%; Transition Softness 100%; Gradient Layer '1. 1.4-invideo-depth_anything_video.mp4' (the depth map) / Source; Gradient Placement Stretch Gradient to Fit; Invert Gradient OFF
- **CC Toner** (`CC Toner`) on Depth Map (fallback): Tones Pentone; Highlights/Brights/Midtones/Darktones/Shadows driven by expressions; Blend w. Original 0%
- **Gradient Ramp** (`ADBE Ramp`) on DM_Fake (fallback): Start of Ramp (960,300) black; End of Ramp (960,1080) white; Ramp Shape Linear Ramp
- **Black & White** (`ADBE Black&White`) on DM_Fake clip (fallback): defaults
- **Gaussian Blur** (`ADBE Gaussian Blur 2`) on DM_Fake adjustment (fallback): Blurriness 6; Repeat Edge Pixels on

## Keyframes

Clip > Gradient Wipe > Transition Completion: 100% at 1:00 s, then 0% at 1:15 (30 fps), Easy Ease on both. The reel's 24 fps comp had the CTI at about 0:00:01:02 when 100% was set and about 0:00:01:09-01:10 when 0% was set (about 8 frames). The visible reveal in the rendered result lasts about 16-20 frames at 30 fps because Softness 100% spreads it, so 0.5 s with Easy Ease reproduces the render. Colorama Phase Shift is driven by the expression, not keys.

## Expressions

Colorama Phase Shift: time*200   (read on screen). CC Toner fallback, one expression per tone colour with L = 0 (Shadows), 0.25 (Darktones), 0.5 (Midtones), 0.75 (Brights), 1.0 (Highlights): var L = 0.0; var P = [[0,[236,198,168]],[0.20,[195,118,230]],[0.375,[217,113,210]],[0.60,[232,174,218]],[0.78,[177,149,224]],[1.0,[236,198,168]]]; var ph = ((L + time*200/360) % 1 + 1) % 1; var c = P[0][1]; for (var i = 0; i < P.length-1; i++) { if (ph >= P[i][0] && ph <= P[i+1][0]) { c = linear(ph, P[i][0], P[i+1][0], P[i][1], P[i+1][1]); break; } } [c[0]/255, c[1]/255, c[2]/255, 1];

## Third-party plug-ins and native stand-ins

none for the effect: Colorama and Gradient Wipe are native. Only the depth map came from an AI (invideo agent / Depth Anything). Native fallback for the depth map is in the steps.

## What the reel did not show (inferred)

The Colorama triangle colours come from the dimmed UI wheel and were cross-checked against rendered sky colours (e.g. #c973e2), so they are within about 10 RGB levels. Triangle angles are measured to about 5 deg. The exact Transition Completion keyframe times were only partly visible (the CTI was scrubbed), so the 0.5 s span is inferred from the rendered reveal duration. A faint peach 'Gradient Depth Reveal' title fades in inside the thumbnail; it is not part of the effect and its font and timing are unknown.
