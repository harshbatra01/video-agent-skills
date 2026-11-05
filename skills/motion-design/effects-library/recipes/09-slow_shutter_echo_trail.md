# 09. Slow Shutter

Recipe name in the study: "Slow Shutter Effect". Category: motion_graphics. Source: a tutorial creator's reel (Dd6h1XjRau7). Confidence of the recipe: medium.

Native build: `../ae/effects/slow_shutter_echo_trail.jsx` (function `build_slow_shutter_echo_trail()`).

## What it looks like

The leading frame stays sharp and opaque; behind the moving subject 4-5 discrete ghost copies trail opposite the motion, spaced ~5% of frame width (about 100 px at 1920) for a total trail of ~25% width. Each ghost is itself smeared along the motion arc, opacity decays ~0.75 per ghost, and they blend like a long exposure: dark hood ghosts darken the blue sky by ~30%, warm goggle reflections (~#FF8A3D) glow through. Snow particles read as white dots with 10-30 px streaks. Delivered cadence is 24 fps (every 5th frame duplicated in the 30 fps file) even though the prompt asked for 12 fps. In the reel the clean clip hard-cuts to the effected clip at f530 (17.67 s).

## Inputs

- a 3-5 s clip with strong, fast motion (head turn, hood in wind, runner's legs, dancer, handheld whip) against a clean bright background; the reel's input was a skier in a hood and goggles against blue sky (AI-regenerated with extra motion and a ~10 deg Dutch tilt)
- optional: a subject alpha matte for a fully sharp leading frame
- optional: the same shot without effect for a before/after hard cut

## Layer stack

Comp SS_Main 1920x1080 24 fps (or 30), top to bottom: (1) SS_Snow [optional] = black solid with CC Snowfall, blend Add (or Screen), CC Force Motion Blur. (2) SS_Sharp = footage, Normal, opacity 55% (or 100% with Alpha Matte from an SS_SubjectMatte layer if a matte exists). (3) SS_Trail = footage with [Posterize Time 12, optional and off by default] -> CC Force Motion Blur -> Echo. Grade untouched.

## Steps

1. Create SS_Main 1920x1080 at 24 fps; place the footage as SS_Trail.
2. On SS_Trail add CC Force Motion Blur (Motion Blur Samples 8, Override Shutter Angle on, Shutter Angle 720, Native Motion Blur Off) to smear each instant along its motion.
3. Add Echo after it: Echo Time -0.083 s (2 frames at 24 fps), Number Of Echoes 5, Starting Intensity 1.0, Decay 0.75, Echo Operator Blend. Tune Echo Time so neighbouring ghosts sit ~5% of frame width apart.
4. Duplicate the footage above as SS_Sharp at 55% opacity (Normal) so the leading frame reads crisp; with a subject matte, use 100% and the matte instead.
5. Optional: Posterize Time 12 as the first effect on SS_Trail for the stepped 12 fps look the prompt asked for (the delivered result reads 24 fps, so leave it off for a match).
6. Optional snow: solid with CC Snowfall (values below) in Add, plus CC Force Motion Blur Shutter 360.
7. Cut: show 0.3 s of the clean clip, hard cut to the effected version.

## Effects used

- **CC Force Motion Blur** (`CC Force Motion Blur`) on SS_Trail: Motion Blur Samples 8; Override Shutter Angle on; Shutter Angle 720; Native Motion Blur Off
- **Pixel Motion Blur** (`ADBE OFMotionBlur`) on SS_Trail (alternative to CC Force Motion Blur): Shutter Control Manual; Shutter Angle 720; Shutter Samples 16; Vector Detail 20
- **Echo** (`ADBE Echo`) on SS_Trail: Echo Time (seconds) -0.083; Number Of Echoes 5; Starting Intensity 1.0; Decay 0.75; Echo Operator Blend
- **Posterize Time** (`ADBE Posterize Time`) on SS_Trail (optional, first in stack): Frame Rate 12 (off by default; delivered result measured 24 fps)
- **CC Snowfall** (`CSSnowfall`) on SS_Snow (optional): Flakes 6000; Size 4; Variation % (Size) 60; Scene Depth 4000; Speed 300; Variation % (Speed) 50; Wind 500; Variation % (Wind) 30; Spread 20; Opacity 80; Composite With Original off

## Keyframes

No keyframes for the look. Reel edit: clean clip in card until f529, hard cut to effected clip f530-f590 (static card at x 381-1522, y 218-860 on white).

## Expressions

Optional on Echo Time: -thisComp.frameDuration*2. Optional on SS_Sharp opacity with a slider 'Sharpness' (default 55).

## Third-party plug-ins and native stand-ins

invideo's agent regenerated the clip with an AI video model (more motion, snow, Dutch tilt) and then built the trail. Native substitute: CC Force Motion Blur (or Pixel Motion Blur) + Echo (Blend) under a 55% sharp copy; snow via CC Snowfall.

## What the reel did not show (inferred)

No effect panel is shown; all values are inferred from the result. Echo time depends on the subject's speed, so 2 frames is a starting point calibrated to ghost spacing (~5% width). Whether the ghosts used Blend or a screen-like operator is inferred from dark ghosts darkening the sky. The 12 fps stepping requested in the prompt is not present in the delivered frames (frame-difference test: 24 fps cadence).
