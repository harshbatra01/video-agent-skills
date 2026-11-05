# 14. Shake Chroma Transition

Recipe name in the study: "Shake + chroma-warp impact (finish in AE 'with shakes and blurs')". Category: transition. Source: a tutorial creator's reel (DdoSNUYvtPg). Confidence of the recipe: medium.

Native build: `../ae/effects/shake_chroma_impact.jsx` (function `build_shake_chroma_impact()`).

Partial match: shares the one-frame reel layout with the One-Frame Glitch Transition.

## What it looks like

An adjustment layer from 4 frames before the cut to 8 frames after (12f-24f with the cut at 16f) violently shakes the frame and liquid-warps it with RGB fringing. At the peak (the cut frame) the image is shifted so far that the reflect-wrapped edges mirror into view. The rings become symmetric hourglass 'pinch' shapes and vertical tubes, with cyan / orange / green chroma fringes along every edge. Inverted burst frames show as dark-green/beige mirrored shapes. The intensity ramps up exponentially into the cut (sharp spike at 16f), drops fast just after, then trails off smoothly to zero by 24f. Shake frequency is about 8.8 Hz, with heavy motion blur.

## Inputs

- the edited cut with the one_frame_glitch_burst (or any hard cut)

## Layer stack

Comp SC_PRE (1920x1080, 30 fps): the BURST comp (or the edit) as layer 2. Above it, [1] ADJ_SHAKE adjustment layer, in 12f out 24f (cut at 16f), with Slider Control 'Shake Amp', CC RepeTile (Unfold), then Transform (wiggle via expression, own shutter angle). Comp SC_OUT (1920x1080): [1] SC_R = SC_PRE with Displacement Map (weight 0.5) and Shift Channels keeping red, blend ADD; [2] SC_G = SC_PRE with Displacement Map (weight 0.75) and Shift Channels keeping green, blend ADD; [3] SC_B = SC_PRE with Displacement Map (weight 1.0) and Shift Channels keeping blue, Normal; [4] black solid. A null CTRL holds the 'Chroma Amt' slider. Layer motion blur ON for ADJ_SHAKE.

## Steps

1. In SC_PRE, add adjustment layer ADJ_SHAKE spanning cut-4f to cut+8f. Add a Slider Control named 'Shake Amp' with keys 0 at cut-4f (outgoing influence 90%), 4.0 at cut (linear in/out, sharp peak), 0 at cut+8f (incoming influence 90%).
2. On ADJ_SHAKE add CC RepeTile: Expand Right 480, Expand Left 480, Expand Down 270, Expand Up 270, Tiling Unfold (mirror, the substitute for Sapphire Wrap X/Y = Reflect), Blend Borders 0%.
3. Then add Transform with expressions on Position, Rotation and Scale (see expressions). Set Use Composition's Shutter Angle OFF and Shutter Angle 360. Enable layer motion blur on ADJ_SHAKE and comp motion blur.
4. Optional Directional Blur after Transform (Direction expression = the movement angle, Blur Length = Shake Amp*12) for extra smear.
5. In SC_OUT, add a null CTRL with a Slider Control 'Chroma Amt', keyed exactly like Shake Amp but with values 0 / 1.0 / 0.
6. Put three copies of SC_PRE in SC_OUT. On each, add Displacement Map: Displacement Map Layer = the same layer (Source), Use For Horizontal Displacement Luminance, Max Horizontal Displacement = expression thisComp.layer("CTRL").effect("Chroma Amt")("Slider") * 160 * w, Use For Vertical Displacement Lightness, Max Vertical = the same * 0.5, Displacement Map Behavior Stretch Map to Fit, Edge Behavior Wrap Pixels Around ON, Expand Output OFF. Use w = 0.5 on SC_R (Warp Red 0.5), w = 0.75 on SC_G, w = 1.0 on SC_B (Warp Blue 1.0).
7. Isolate channels with Shift Channels. SC_R: Green From Full Off, Blue From Full Off. SC_G: Red Off, Blue Off. SC_B: Red Off, Green Off. Blend SC_R and SC_G in ADD over SC_B (Normal). At Chroma Amt 0 the three recombine to the clean image.
8. Check against ref_shake_chroma_warp_24.67.png at the cut frame: mirrored hourglass tubes with RGB fringes.

## Effects used

- **S_Shake (Sapphire)** (``) on ADJ_SHAKE (reel): Amplitude keyed (1.238 at 0:00:00:18), Frequency 8.80, Seed 0.220; sub-groups X Shake, Y Shake, Z Shake, Tilt Shake, Channels collapsed; Opacity Normal; Mask Use Luma; Blur Mask 12.00; Invert Mask off; Wrap X Reflect, Wrap Y Reflect
- **S_DistortChroma (Sapphire)** (``) on ADJ_SHAKE (reel): Lens None / Source; Matte from Layer None / Source; Matte from Path None; Amount keyed (0.000 at 0:00:00:18); Blur Lens, Rotate W, Steps unreadable; Warp Red 0.500; Warp Blue 1.000; Color1 red, Color2 green, Color3 blue; White Balance off; Amount Rel X 1.000; Amount Rel Y 1.000; Wrap X Reflect; Wrap Y Reflect; Filter ON; Blur Matte 0.00; Invert Matte off; Matte Use Luma; Opacity Normal
- **Slider Control 'Shake Amp'** (`ADBE Slider Control`) on ADJ_SHAKE: keys 0 / 4.0 / 0
- **CC RepeTile** (`CC RepeTile`) on ADJ_SHAKE: Expand Right 480; Expand Left 480; Expand Down 270; Expand Up 270; Tiling Unfold; Blend Borders 0%
- **Transform** (`ADBE Geometry2`) on ADJ_SHAKE: Position/Rotation/Scale via expressions; Use Composition's Shutter Angle OFF; Shutter Angle 360
- **Displacement Map** (`ADBE Displacement Map`) on SC_R / SC_G / SC_B: Map Layer = self (Source); Horizontal Luminance, Max = ChromaAmt*160*w; Vertical Lightness, Max = ChromaAmt*80*w; Stretch Map to Fit; Wrap Pixels Around ON; w = 0.5 / 0.75 / 1.0
- **Shift Channels** (`ADBE Shift Channels`) on SC_R / SC_G / SC_B: keep one channel each (other two from Full Off)

## Keyframes

Both sliders: key 1 at cut-4f (reel 12f) value 0, Easy Ease out with 90% influence (speed 0); key 2 at the cut (16f) peak (Shake Amp 4.0, Chroma Amt 1.0), linear in and out so the speed graph spikes; key 3 at cut+8f (24f) value 0, ease in with 90% influence. In the reel's speed graph the speed rises exponentially into 16f, flips to a large negative spike, then decays to 0 at 24f. Keyframe icons show Easy Ease hourglasses at 12f/16f/24f on both Amplitude and Amount. The adjustment layer bar spans 12f to 24f.

## Expressions

ADJ_SHAKE > Transform > Position: var a = effect("Shake Amp")("Slider"); var f = 8.8; var nx = noise([time*f, 1.7]); var ny = noise([4.3, time*f]); [value[0] + nx*a*30, value[1] + ny*a*30];   Rotation: noise([time*8.8, 9.1]) * effect("Shake Amp")("Slider") * 0.75;   Scale: var s = 100 + effect("Shake Amp")("Slider")*2; [s, s];   (peak 4.0 gives about +-120 px and +-3 deg).   SC_x > Displacement Map > Max Horizontal Displacement: thisComp.layer("CTRL").effect("Chroma Amt")("Slider") * 160 * 0.5   (0.75 for G, 1.0 for B); Max Vertical Displacement: the same * 0.5.

## Third-party plug-ins and native stand-ins

Sapphire S_Shake and S_DistortChroma (not installed). Substitutes: S_Shake = CC RepeTile (Unfold, standing in for Reflect wrap) + Transform with noise() wiggle and its own 360 deg shutter. S_DistortChroma = three per-channel copies with self-luma Displacement Map (Warp Red 0.5 / Green 0.75 / Blue 1.0 weights) recombined with Shift Channels + Add.

## What the reel did not show (inferred)

S_Shake peak Amplitude: only 1.238 at 18f was readable. Peak about 4.0 is inferred from the ease shape (the value drops about 70% in the first 2 of 8 frames). S_DistortChroma Amount peak is unreadable (0.000 at 18f); about 0.1 in Sapphire units is inferred, mapped to Chroma Amt 1.0 = 160 px displacement here. Blur Lens, Rotate W and Steps values are hidden behind the caption. Only the left third of the comp viewer is visible in the reel, so the whole-frame look of the peak is partly inferred.
