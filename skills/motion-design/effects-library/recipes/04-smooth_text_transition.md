# 04. Smooth Text Transition

Recipe name in the study: "Smooth text transition (double-null parented push)". Category: transition. Source: a tutorial creator's reel (DaklnysP87i). Confidence of the recipe: medium.

Native build: `../ae/effects/smooth_text_transition.jsx` (function `build_smooth_text_transition()`).

## What it looks like

1920x1080, 30 fps, 60 f on pure black #000000. f0-f12: 'Go with the' (white #EDF2FB, ~260 px, medium neo-grotesk) reveals word by word via the tutorial brand's text preset (its native rebuild is a separate word-reveal preset, not in this library). The whole group arrives from about 240 px right with a very fast start (the motion happens while the words are still invisible or blurred) and keeps creeping left slowly (about 2-3 comp px per frame by f5-f16). From ~f19 the group accelerates left (skewed bell: 0 speed at f19, peak ~1600-1700 px/s around f31, long ease-in tail) and fades out with opacity 100 to 0 over f30-f34, so it is gone by about f29-f30 visually. In parallel the second word ('TITLE' in the builder; same size; hero styling is a cyan-centre/blue-edge gradient running #107BE4, #19BBF0, #1BE5F0 (centre), #18BAF3, #137EE9 across its letters, with a soft cyan glow halo, #03222A 10 px out fading to #011018 at 40 px) starts at f30, blurred and fading in, already moving left from about 200 px right of centre and decelerating into dead centre by f59 (long smooth settle). A few black frames follow before the loop restarts.

## Inputs

- two text strings: a first line ('Go with the' in the reel) and a second word (the builder uses 'Say hello to' and 'TITLE')

## Layer stack

Comp 'Smooth Text Transition' 1920x1080, 30 fps, 60 f, top to bottom: 1 'Null 11' (null, parent None); 2 'Null 10' (null, parent Null 11); 3 'TITLE' (text, parent Null 10, in 30 f -> out 60 f, word-reveal preset, optional gradient + glow); 4 'Go with the' (text, parent Null 10, in 0 -> out 35 f, word-reveal preset, opacity fade at the end); 5 'Black Solid' #000000. No mattes. All layers use Normal mode.

## Steps

1. New comp 1920x1080, 30 fps, 60 frames; add black solid #000000.
2. Text 'Go with the': Inter Medium (fallback SF Pro Display Medium), 260 px, tracking -20, fill #EDF2FB, centred paragraph, anchor centred, position (960,540). Layer in 0, out 35 f (the original 30 f end extended by 5 f). Apply the word-reveal preset (a separate rebuild, not in this library; or an Opacity text animator by words, `titles-captions-type.md` section 2) starting at 0 f.
3. Duplicate it, change the text to the second word ('TITLE'), move the layer so it starts at 30 f (out 60 f), and set its position to (1613,540), ie 653 px to the right. The preset keys move with the layer, so it reveals from 30 f. Hero styling, optional: Gradient Ramp (ADBE Ramp) Radial, Start of Ramp at the word centre (1613,540 before parenting) colour #1BE5F0, End of Ramp 330 px to the right colour #107BE4. Then Deep Glow 2 (PEDG2) Radius 80, Exposure 0.4, or native Glow (ADBE Glo2) Threshold 40%, Radius 60, Intensity 0.8.
4. Add 'Null 10' at (960,540). Parent both texts to it (AE keeps their world positions).
5. Null 10 Position: key at 30 f = (960,540); key at 0 f = (1203,540). Ease: 0 f out speed 3250 px/s, influence 6%; 30 f in speed 0, influence 60% (the Flow 2.0 'fast start, long settle' curve).
6. Add 'Null 11' at (960,540) and parent Null 10 to it. Null 10's values become relative: 0 f (243,0), 30 f (0,0).
7. Null 11 Position: key at 19 f = (960,540) (deliberately overlapping Null 10's tail), key at 59 f = (307,540), so the second word lands at x=960. Ease: 19 f out speed 0, influence 57%; 59 f in speed 0, influence 100% (skewed bell, peak at ~31% of the span).
8. 'Go with the' Opacity: 30 f = 100%, 34 f = 0%, Easy Ease (33.33% both).
9. Optional: enable motion blur on the texts (the reference shows blurred streaks during the fast exit/entry; shutter 180).

## Effects used

- **Gradient Ramp** (`ADBE Ramp`) on the second word (hero styling only): Ramp Shape Radial; Start Color #1BE5F0 at word centre; End Color #107BE4 at ~330 px radius (inferred from the finished colours, not shown in the tutorial)
- **Deep Glow 2** (`PEDG2`) on the second word (hero styling only): Radius ~80, Exposure ~0.4, Blend Screen (inferred; native fallback Glow ADBE Glo2 Threshold 40%, Radius 60, Intensity 0.8)

## Keyframes

Null 10 Position (before parenting): 0 f [1203,540] out 3250 px/s @6% -> 30 f [960,540] in 0 @60% (tooltip/readout: 960.0,540.0; after parenting 0.0,0.0 at 0:00:01:00). Null 11 Position: ~19 f [960,540] out 0 @57% -> 59 f [307,540] in 0 @100% (307,540 read from the Properties panel). Text 1 Opacity: 30 f 100% -> 34 f 0%, easy ease. Text layer timing: 'Go with the' 0-35 f, the second word 30-60 f.

## Expressions

none

## Third-party plug-ins and native stand-ins

Flow 2.0 (SuperFlow) is used to draw both ease curves (Null 10 readout 0.00, 0.00, 0.00, 1.00 = an extreme ease-out cubic-bezier). The native substitute is the KeyframeEase speed/influence values given. The text animation itself is the tutorial brand's paid or giveaway preset; its native rebuild is a separate word-reveal preset (not in this library).

## What the reel did not show (inferred)

(1) Null 10's frame-0 offset was not shown numerically; it was measured as ~243 px from the motion path against the safe-area guides (the speed-graph integral gives ~186 px, so the true value is 190-245). (2) Null 11's first key time: the blue key sits about 11 f before 1:00, so ~19 f. (3) The second word's gradient and glow are not in the tutorial (there the word is plain white); colours were sampled from the finished loop. (4) Font is not named; Inter/SF Pro Display Medium is the closest look. (5) The finished loop shows ~6 black frames after the 60-frame comp, which is a playback gap in the title card.
