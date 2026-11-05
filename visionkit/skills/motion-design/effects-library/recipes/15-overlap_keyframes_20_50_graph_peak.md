# 15. 20-50 Easing Rule

Recipe name in the study: "Overlapping keyframes: 20/50 rule + Graph Peak". Category: technique_demo. Source: a tutorial creator's reel (DaNZsi6PGWx). Confidence of the recipe: high.

Native build: `../ae/effects/overlap_keyframes_20_50_graph_peak.jsx` (function `build_overlap_keyframes_20_50_graph_peak()`).

## What it looks like

Demo comp showing why overlap needs the right ease. Two (or more) elements animate in sequence, e.g. two teal bars or two words sliding in 300 px. WRONG: B starts only when A ends (no overlap) - visible stop-start. SLOPPY: B overlaps A but uses a 'speed at the start' ease (out influence ~1 %, in ~91 %) so its peak speed hits at its first keyframe and the hand-off jolts. RIGHT: B's first keyframe sits where A is 50 % done (overlap = 50 % of A's keyframe span; the reel allows 20-50 %) and B's speed graph peaks exactly on A's last keyframe, giving one continuous motion. In the reel the diagram measures overlap 49.9 % (keys 759 vs 386-1131) and 20.5 % at the dragged position; the correct graph is a symmetric bell peaking under A's last key; the wrong one is a vertical spike at B's first key with a long concave decay.

## Inputs

- two or three simple elements (shape bars, words or cards) - no footage needed

## Layer stack

Three side-by-side or sequential sub-comps 'WRONG', 'SLOPPY', 'RIGHT' (or one comp with three rows): each row has layer A and layer B (shape rects 787x32, teal) moving on Position X; label text per row; background #F9F9F9. Optional overlay: speed graph drawn as a shape path (see keyframe_bars_explainer).

## Steps

1. Comp 1920x1080, 30 fps, 2.5 s, bg #F9F9F9.
2. Row RIGHT: A Position X keys 0f -> 24f (move 300 px), both keys Easy Ease with influence 73 % (speed 0). B keys 12f -> 36f (50 % overlap), same 73/73 ease, so B's peak speed lands on 24f = A's last key.
3. Row RIGHT-20: B keys at 19f -> 43f (20 % overlap); to keep the peak on A's last key (20 % into B) use B out influence 24 % / in influence 80 % (speed 0).
4. Row SLOPPY: B keys 12f -> 36f with out influence 1 % (or Linear out) and in influence 91 % (speed 0): peak speed at 12f.
5. Row WRONG: B keys 24f -> 48f (no overlap), 73/73 ease.
6. Label each row; optionally draw each layer's speed curve under it (sample valueAtTime velocity with an expression into a path, or draw the bell/spike paths from keyframe_bars_explainer).

## Keyframes

A: 0f -> 24f, influence 73/73. B (50 %): 12f -> 36f, 73/73. B (20 %): 19f -> 43f, out 24 / in 80. B (sloppy): 12f -> 36f, out 1 / in 91. B (no overlap): 24f -> 48f. All speeds 0 at keys. Fitted from the reel's drawn curves: bell = 73/73 (error 0.0024), spike = 1/91 (error 0.0044).

## Expressions

Optional speed readout: a text layer with sourceText = Math.round(length(thisComp.layer('B').transform.position.velocity)) to show the peak landing on A's last keyframe; or a guide line at A.key(2).time.

## Third-party plug-ins and native stand-ins

None; native keyframe velocity (KeyframeEase(speed, influence)).

## What the reel did not show (inferred)

The reel never shows AE values; influence numbers are curve fits of the drawn graphs and overlap percentages come from keyframe-icon positions. Exact move distances/durations of the demo are free choices (the reel's diagram is schematic).
