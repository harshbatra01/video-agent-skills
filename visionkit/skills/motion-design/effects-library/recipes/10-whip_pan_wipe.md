# 10. Whip Pan Transition

Recipe name in the study: "Wipe transition without any camera (whip-pan bridge)". Category: transition. Source: a tutorial creator's reel (Dd9E5Q9AtyT). Confidence of the recipe: high.

Native build: `../ae/effects/whip_pan_wipe.jsx` (function `build_whip_pan_wipe()`).

## What it looks like

Each hard cut is hidden by a 10-13 frame horizontal whip that always travels left-to-right. Outgoing shot: frame c-5 shifts slightly right with light smear; c-4 to c-2 heavy horizontal streaks where only strong horizontal lines survive (barriers, kerbs); peak 3-6 frames around the cut are a featureless horizontal smear in the shots' dominant colour (sand ~#C89A6A, kerb red ~#C8584A, sky ~#BFC8D0); incoming shot snaps in still blurred and resolves within 2 frames. Blur length at peak is ~60-100% of frame width. Measured whips: f27-f37 (11 frames), f45-f57 (13), f73-f82 (10). Whoosh SFX peaks on the cut frame; a heavier sub whoosh on the key cut.

## Inputs

- 3-6 shots of one subject with hard cuts (reel: F1 car front, cockpit, rear on kerb, cockpit-front), each with at least 6 frames of handle either side of every cut
- whoosh SFX (gritty air whoosh x N, one sub/bass whoosh)

## Layer stack

Comp WP_Main 1920x1080 30 fps. Shots end-to-end on the timeline (hard cuts), each extended by 6 frames of handle so it overlaps the neighbour. For every cut c: the outgoing layer (bottom) gets Motion Tile -> Transform -> Directional Blur keyed over c-6..c; the incoming layer (top) starts at c-1 with opacity 0 -> 100 over 2 frames and gets the same stack keyed c..c+6. Layer motion blur on for both. Audio: whoosh layer per cut with its peak aligned to c.

## Steps

1. Lay the shots in order; extend each so the outgoing one runs to c+1 and the incoming one starts at c-1.
2. On both layers add Motion Tile (Output Width 300, Output Height 100, Mirror Edges on) so sliding never shows edges.
3. Add Transform: outgoing Position x 960 at c-6 -> 2360 at c (ease-in, influence 85%); incoming 0... i.e. -440 at c -> 960 at c+6 (ease-out, influence 85%). Untick Use Composition's Shutter Angle, Shutter Angle 360.
4. Add Directional Blur, Direction 90: outgoing Blur Length 0 at c-6, 40 at c-4, 160 at c-2, 300 at c; incoming 300 at c, 220 at c+1, 70 at c+3, 10 at c+5, 0 at c+6.
5. Incoming opacity 0 at c-1 -> 100 at c+1 (2-frame dissolve inside the peak).
6. Place a whoosh with its loudest point on c; use a heavier sub whoosh on the most important cut.

## Effects used

- **Motion Tile** (`ADBE Tile`) on outgoing and incoming shot: Tile Center (960,540); Tile Width 100; Tile Height 100; Output Width 300; Output Height 100; Mirror Edges on; Phase 0
- **Transform** (`ADBE Geometry2`) on outgoing and incoming shot: Position keyed (see keyframes); Use Composition's Shutter Angle off; Shutter Angle 360
- **Directional Blur** (`ADBE Motion Blur`) on outgoing and incoming shot: Direction 90; Blur Length keyed 0 -> 300 -> 0 around the cut

## Keyframes

Cut at frame c (30 fps). Outgoing: Transform Position x c-6: 960 (ease in 85%), c: 2360 (linear). Directional Blur Length c-6: 0, c-4: 40, c-2: 160, c: 300. Incoming: Position x c: -440 (linear), c+6: 960 (ease out 85%). Blur Length c: 300, c+1: 220, c+3: 70, c+5: 10, c+6: 0. Incoming Opacity c-1: 0, c+1: 100. Total visible whip ~10-12 frames, matching the measured 10/11/13.

## Expressions

Optional: drive both layers from one slider 'Whip' (0..1..0) with Position x = linear(whip,0,1,960,2360) and Blur Length = whip*300.

## Third-party plug-ins and native stand-ins

invideo generated AI bridge clips (start frame of shot A whipping into shot B). Native substitute: Motion Tile + Transform with 360 shutter + Directional Blur ramp and a 2-frame dissolve at the peak.

## What the reel did not show (inferred)

After panel is only 640 px wide, so exact blur lengths are estimated (peak ~60-100% of width). The bridges contain AI-invented in-between content (sand, sky), which native sliding of the two real shots will not reproduce exactly; the overall smear colour will come from the shots instead.
