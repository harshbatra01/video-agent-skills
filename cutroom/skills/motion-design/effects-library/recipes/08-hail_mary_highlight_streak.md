# 08. Hail Mary

Recipe name in the study: "Hail Mary Effect". Category: stylize. Source: a tutorial creator's reel (Dd1Zj4KAUax). Confidence of the recipe: medium.

Native build: `../ae/effects/hail_mary_highlight_streak.jsx` (function `build_hail_mary_highlight_streak()`).

Partial match: built on a night street clip instead of the reel's goggled subject.

## What it looks like

Grade is left untouched (sky #2087B3, hood shadows #072536, warm rim #E8DCCB). Every pixel above ~54% luma (goggle rim, chrome, badge) is smeared along ONE axis, symmetrically both ways, with an exponential falloff: a bright core of 20-40 px, a tail visible ~250 px each side at 1920 width (Streak Length 549), fading to nothing, plus a soft bloom on the rim. Hero version (1.0-1.9 s) is pure horizontal; the panel version is tilted 20.3 deg, rising to the right (shader Angle 200.30). At very long length (1920) the streak breaks into evenly spaced thin copies about 23 px apart (comb / slit-scan ribbing, visible ~220 px right and ~290 px left of the rim). The hero frame also has 2-3 thin horizontal pixel-stretch bands (rows smeared sideways, 20-60 px tall at 1080, ~55% opacity) across the lower hood/zipper, and a faint translucent vertical slice (offset copy ~+30 px, hard vertical edge, ~15-20% brighter) over the right third whose edge sweeps right during f32-f40 then holds. The streak itself is static (no animation needed).

## Inputs

- a 3-6 s shot with a few small, very bright highlights against mid/dark tones (reflective goggle rim, chrome, car badge, rim light, sun flare), e.g. a hooded person in ski goggles against blue sky, locked or slow camera

## Layer stack

Comp HM_Main 1920x1080 30 fps, top to bottom: (1) HM_Slice [optional] = footage duplicate, blend Screen, opacity 20%, rectangular mask x 1150-1920 (hard edge, feather 0), Transform offset +30 px x. (2) HM_PixelStretch [optional] = precomp HM_Stretch, Normal, opacity 55%, Alpha Matte from HM_Bands (shape layer above it: 2-3 horizontal rectangles, e.g. y 640-700 and 735-760 at hero scale, feather 4 px, only left of x0). (3) HM_Streak = precomp HM_StreakComp, blend Add, opacity 100% (= Mix 1.0), with Exposure then Deep Glow 2 (or Glow). (4) Footage, Normal, grade untouched. HM_StreakComp 1920x1080: black solid at the bottom, then three copies of precomp HM_Highlights in Add mode carrying Directional Blur at lengths 40 / 160 / 550 with opacities 100 / 70 / 45. HM_Highlights 1920x1080: footage + Extract (luma key) + Gaussian Blur 1.5 (colour of the highlights is kept). HM_Stretch: footage with a 2 px wide vertical mask at x0 (just right of the highlight) and Transform anchored at x0 scaling width ~6000% so each row's colour is stretched sideways. Optional control null HM_CTRL with sliders mirroring the shader: Angle, Streak Length, Threshold, Knee, Intensity, Falloff, Glow Amount, Mix.

## Steps

1. Create comp HM_Main 1920x1080 30 fps; import the footage; keep its grade untouched (bottom layer).
2. Precompose a copy of the footage as HM_Highlights; add Extract: Channel Luminance, Black Point 138 (Threshold 0.54 x 255), White Point 255, Black Softness 117 (Knee 1.0; use 82 for Knee 0.70), White Softness 0; add Gaussian Blur 1.5.
3. Make HM_StreakComp: black solid, then HM_Highlights three times in Add mode with Directional Blur Direction 90 deg (horizontal) and Blur Length 40 / 160 / 550, opacities 100 / 70 / 45. For the tilted panel variant set Direction 69.7 deg (shader 200.3 deg = 20.3 deg above horizontal, rising right).
4. Put HM_StreakComp in HM_Main above the footage, blend Add, opacity 100; add Exposure +1.0 stop, then Deep Glow 2 (Radius 120, Exposure 0.97) or native Glow (Color Channels, Threshold 45%, Radius 60, Intensity 0.97, Composite Original On Top, Glow Operation Add).
5. Optional comb look for very long streaks: instead of the 550 px blur use 12 duplicates of HM_Highlights in Add, offset i*45 px both directions along the streak axis (i=1..6 each side), opacity 30*exp(-0.7*i)%.
6. Optional pixel-stretch bands: HM_Stretch (2 px column mask at x0, Transform anchor/position at x0, Scale Width 6000, Height 100), matte it with 2-3 thin horizontal rectangles over the lower subject, opacity 55%.
7. Optional slice: footage duplicate, Screen 20%, offset +30 px, rectangular mask on the right third; animate the mask's left edge from 0.43W to 0.85W over 8 frames, then hold.
8. Wire sliders on HM_CTRL by expression so it is 'fully customisable' like the shader (see expressions).

## Effects used

- **Hail Mary (custom)** (`n/a (invideo custom shader)`) on invideo clip (reference only, read from the agent-built shader): Angle 200.30; Streak Length 549.39 (dragged to 1920.00 at 14.8 s); Threshold 0.54; Knee 1.00 (dragged to 0.70 at 16.0 s); Streak Intensity 5.00; Falloff 4.24; Glow Amount 0.97; Mix 1.00. Clip Speed 100%, Duration 00:00:05:01.
- **Extract** (`ADBE Extract`) on HM_Highlights (inside precomp): Channel Luminance; Black Point 138; White Point 255; Black Softness 117; White Softness 0; Invert off
- **Gaussian Blur** (`ADBE Gaussian Blur 2`) on HM_Highlights (inside precomp): Blurriness 1.5; Blur Dimensions Horizontal and Vertical; Repeat Edge Pixels off
- **Directional Blur** (`ADBE Motion Blur`) on HM_Highlights copy A / B / C (inside HM_StreakComp): Direction 90 deg (hero, horizontal) or 69.7 deg (tilted variant); Blur Length 40 (A, opacity 100) / 160 (B, opacity 70) / 550 (C, opacity 45); all copies blend Add
- **Exposure** (`ADBE Exposure2`) on HM_Streak: Channels Master; Exposure +1.0; Offset 0; Gamma 1.0
- **Deep Glow 2** (`PEDG2`) on HM_Streak: Radius 120; Exposure 0.97; Threshold 0; (if available) Aspect Ratio ~0.5 along the streak angle to elongate the bloom
- **Glow** (`ADBE Glo2`) on HM_Streak (native alternative to Deep Glow 2): Glow Based On Color Channels; Glow Threshold 45%; Glow Radius 60; Glow Intensity 0.97; Composite Original On Top; Glow Operation Add
- **Transform** (`ADBE Geometry2`) on HM_Stretch (optional pixel-stretch band): Anchor Point (x0,540); Position (x0,540); Uniform Scale off; Scale Height 100; Scale Width 6000; on a layer with a 2 px wide vertical mask at x0

## Keyframes

The look needs no keyframes. Optional entrance: HM_Streak opacity 0 -> 100 over frames 0-6 (ease out). Optional slice: mask left edge 0.43W at f2 -> 0.85W at f10 (linear), hold. In the reel the hero card itself rotates -3 deg -> 0 and scales 95% -> 100% over f30-f38 (ease out); that is the title device, not the effect.

## Expressions

On HM_CTRL sliders: Angle 200.3, Streak Length 549.39, Threshold 0.54, Knee 1.0, Intensity 5, Falloff 4.24, Glow 0.97, Mix 1.0. Directional Blur Direction: a = c('Angle') % 180; 90 - a (gives 69.7 for 200.3, 90 for 180). Blur Length A/B/C: L*0.073, L*0.29, L*1.0 where L = c('Streak Length'). Extract Black Point: c('Threshold')*255; Black Softness: c('Knee')*117. HM_Streak opacity: c('Mix')*100. Glow Intensity / Deep Glow Exposure: c('Glow'). Exposure: Math.log(c('Intensity'))/Math.log(2) - 1.3.

## Third-party plug-ins and native stand-ins

Built in invideo as an AI-written custom shader (single symmetric directional streak keyed by threshold/knee with exponential falloff, intensity, glow, mix). Native substitute: Extract luma key + three additive Directional Blurs (exp falloff approximation) + Exposure + Deep Glow 2 (installed) or native Glow.

## What the reel did not show (inferred)

The shader's exact kernel (tap count, whether one- or two-sided) is not visible; the length-1920 frame shows copies on both sides of the rim, so a symmetric blur is assumed. Tap spacing ~23 px at 1920 implies ~40 taps per side; the native recipe approximates this with three blurs. The source clip without the effect is never shown, so the grade is assumed to be the clip's own. Units of Streak Length are assumed to be pixels at 1920 width.
