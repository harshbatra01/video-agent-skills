# 02. Luma Dissolve

Recipe name in the study: "The Luma Dissolve". Category: transition. Source: a tutorial creator's reel (DeURRG7vITo). Confidence of the recipe: high.

Native build: `../ae/effects/luma_dissolve.jsx` (function `build_luma_dissolve()`).

## What it looks like

Per-pixel threshold dissolve driven by the clip's own luminance, composited over pure white #FFFFFF. Measured on the tutorial viewer at d=66.86% with softness 0.09, 0.29 and 0.49: alpha = clamp(((1+s)(1-d) - L)/s, 0, 1). Here L is the source pixel's Rec.709 luma (display-referred, 0-1), d = Dissolve%/100 and s = Softness (0.1 in the preset). Observed alpha matches within 0.01 for L 0.01-0.21. Dark pixels appear first and stay longest; bright pixels arrive last and vanish first. At s=0.1 it looks posterised, like ink: solid blacks with hard white cut-outs and a semi-transparent band 10% of the luma range wide. REVEAL, reel intro f0-f30 at 30 fps (measured d: f4 95, f7 87, f10 76, f12 68, f14 54, f15 49). f0-f3 pure white. f4 first black specks (hoodie, hair, shadows). f6-f8 runner and dark pillars as black shapes with white holes. f10-f12 midtones. f13-f15 the road. Brightest highlights finish f20-f30. EXIT f49-f60 (d: f50 5, f51 15, f52 53, f53 76, f54 85, f55 89.5, f56 92, f57 94, f58 95, f59 96, about 100 by f61). Road and sky drop to white in one frame (f52). f53 keeps only L below 0.25, with hard edges. f54-f59 the darkest pixels thin into a grey ghost (hoodie around #555 by f54), gone by f61. Larger softness (about 0.5) gives a washed-out, dreamy fade where only the darks stay solid.

## Inputs

- a high-contrast live-action clip with a dark subject against brighter surroundings, e.g. a runner in black clothes on a sunlit street, side tracking shot with motion-blurred buildings, graded punchy (crushed blacks, warm highlights)
- a pure white #FFFFFF background solid, or a second clip underneath for a clip-to-clip transition

## Layer stack

Comp 1920x1080 (the tutorial comp is 24 fps; the reel is 30 fps), comp BG white. Top: CLIP footage layer, Normal, no track matte, effect Gradient Wipe with Gradient Layer = itself. Bottom: white solid #FFFFFF 1920x1080, or the incoming or outgoing clip. In the reel the clip is masked or cropped to a 3:2 box 836x564 px; the dissolve applies only to the clip, and the text layers fade with opacity.

## Steps

1. Import the clip and put it in a 1920x1080 comp at 30 fps (24 fps to copy the tutorial timing). Add a white solid #FFFFFF under it.
2. On the clip add Effect > Transition > Gradient Wipe (ADBE Gradient Wipe). Gradient Layer = the clip itself (setValue(layer.index)). Gradient Placement = Stretch Gradient to Fit. Invert Gradient = On (bright pixels disappear first, as Sapphire's Invert Pattern). Transition Softness = 10%.
3. Reveal: key Transition Completion 100% at the clip in-point and 0% at +1.0 s. Tutorial easing: both keys speed 0; key 1 outgoing influence 33.33%, key 2 incoming influence 100% (fast start, long tail; peak speed about -410 %/s at 0.196 s). Reel intro measurement fits Easy Ease 33.33/33.33 over 30 frames slightly better; use that for the intro reference.
4. Dissolve out: key Completion 0% then 100% 10-11 frames later at 30 fps (about 8 frames at 24 fps). Key 1 outgoing influence 33.33%, key 2 incoming influence 100%, speeds 0.
5. Check: render one frame at Completion 66.86% with Softness 10% and with 49%. Then alpha must equal clamp(((1+s)(1-d)-L)/s): at s=0.49, L 0.01 -> 0.98, L 0.11 -> 0.78, L 0.21 -> 0.58. Compare with ref_luma_dissolve_layercrop_*.png.
6. If Gradient Wipe's softness ramp does not match, use the fallback: delete it and add Keying > Extract (ADBE Extract). Channel Luminance, Black Point 0, Black Softness 0. Add Slider Control 'Dissolve %' (keyed like above) and put the expressions below on White Point and White Softness.
7. For a clip-to-clip transition, replace the white solid with clip B (same timing). For a smoother look raise softness (Gradient Wipe softness 30-50%).

## Effects used

- **S_DissolveLuma (Sapphire, NOT installed)** (`S_DissolveLuma`) on Runner (tutorial, comp Footage 2): Background None | Source; Transition Dir Dissolve Off to Bg; Auto Trans No: use Dissolve%; Dissolve Percent KEYED 100.00% at 0f, 0.00% at 01:00f (24 fps), demo frame 66.86%; Softness 0.1000 (demo scrub 0.09-0.68, settles 0.49); Use Luma Of Difference; Invert Pattern ON (default off); Smooth Pattern 0.00; Opacity Normal
- **Gradient Wipe** (`ADBE Gradient Wipe`) on CLIP: Transition Completion KEYED (100 -> 0 reveal, 0 -> 100 out); Transition Softness 10%; Gradient Layer = this layer (Source); Gradient Placement = Stretch Gradient to Fit; Invert Gradient = On
- **Extract** (`ADBE Extract`) on CLIP (fallback only): Channel Luminance; Black Point 0; Black Softness 0; White Point = min(255, 255*(1+s)*(1-d)); White Softness = 255*s while White Point < 255, else 280.5 - White Point; Invert off
- **Solid** (`solid`) on BG: #FFFFFF, comp size

## Keyframes

Tutorial (24 fps): Dissolve Percent 0f = 100%, 24f = 0%. Key 1 out speed 0, influence 33.33%; key 2 in speed 0, influence 100% (OCR of the drag tooltips: -13.52 %/s 79.50% -> -4.36 %/s 100% -> 0.00 %/s 100%). Value per 24-fps frame: 100, 99.4, 97.1, 91.8, 81.0, 64.7, 50.0, 39.3, 31.4, 25.3, 20.5, 16.5, 13.2, 10.5, 8.3, 6.4, 4.8, 3.6, 2.5, 1.7, 1.0, 0.6, 0.2, 0.1, 0. Reel intro (30 fps): 100% at f0 -> 0% at f30, Easy Ease 33.33/33.33 (rms 1.2 vs measured). Reel exit (30 fps): 0% at f49 -> 100% at f59-60, out 33.33% / in 100% (rms 2.9).

## Expressions

Fallback Extract with Slider 'Dissolve %' on the same layer. White Point: s=0.1; d=effect("Dissolve %")("Slider")/100; Math.min(255, 255*(1+s)*(1-d)). White Softness: s=0.1; d=effect("Dissolve %")("Slider")/100; wp=255*(1+s)*(1-d); wp<=255 ? 255*s : Math.max(0, 255*(1+s) - wp). Primary Gradient Wipe build needs no expressions.

## Third-party plug-ins and native stand-ins

Reel uses Sapphire S_DissolveLuma (Boris FX), not installed. Native substitute: Gradient Wipe (ADBE Gradient Wipe) with the clip as its own gradient layer, Invert Gradient on, Transition Softness 10%, Completion keyed like Dissolve Percent. Fallback: Extract (ADBE Extract) on luminance with expression-driven White Point and White Softness.

## What the reel did not show (inferred)

Gradient Wipe's internal softness formula was not tested in AE (analysis only); verify it with the 66.86% test, or use the Extract fallback. The reel's own intro and exit keys were never shown on screen. Their timing was measured from pixels: the intro tail after f15 is unreliable because only the brightest 5% of pixels remain, and the exit tail after f59 is polluted by the next caption. The Sapphire match name was not shown (assumed S_DissolveLuma). Background/Use Luma Of semantics: with Background None, 'Difference' was confirmed to behave as the source's own luma.
