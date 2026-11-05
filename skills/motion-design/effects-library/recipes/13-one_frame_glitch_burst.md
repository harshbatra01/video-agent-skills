# 13. One-Frame Glitch Transition

Recipe name in the study: "One-frame transitions (6-frame glitch burst at a cut)". Category: transition. Source: a tutorial creator's reel (DdoSNUYvtPg). Confidence of the recipe: high.

Native build: `../ae/effects/one_frame_glitch_burst.jsx` (function `build_one_frame_glitch_burst()`).

## What it looks like

A 6-frame burst around a hard cut from a dark scene A (near-black navy, mean RGB 10,9,21) to a bright scene B (white with blue concentric rings). M = the first frame of B (timeline marker, frame 16 in the agent's edit). Frame M-3: scene A luminance-inverted and fully desaturated, so the bg becomes #f1f1f1 with pale grey icons, smeared horizontally (directional blur about 25 px) and nudged right about 20 px. Frames M-2 and M-1: flat white #fbfbfb (2-frame white flash). Frame M: scene B blown up to about 280% around the centre with zoom blur, so it reads as white with the blue floor gradient, plus a black/cyan inverted fringe at the left edge. Frames M+1 and M+2: hard vertical split. The left 48.5% (M+1) then 47.5% (M+2) of the frame is scene B fully RGB-inverted (black bg, gold #856e0d rings, yellow text), and the right side is scene B normal. The split edge is straight in the top 70% and bows 15-20 px to the right near the bottom. B is at about 180% scale on these frames. Frame M+3 onward: clean scene B, which keeps settling its scale from 161% to 100% over the next 27 frames with an exponential ease-out (148% at M+4, 131% at M+6, 119% at M+10, 112% at M+15, 108% at M+20, 102% at M+25, 100% at M+30).

## Inputs

- two clips meeting at a hard cut: an outgoing dark clip and an incoming bright clip (the reel uses a dark UI-icons motion-graphic and the white concentric_rings_title scene)

## Layer stack

Comp BURST (1920x1080, 30 fps), top to bottom: [1] FLASH solid #FBFBFB, visible M-2 to M-1 only; [2] B_INV = copy of clip B with Invert (RGB) and a rectangle mask on the left, visible M+1 to M+2; [3] B = clip B from M on, with Transform scale keys and CC Radial Fast Blur on frame M; [4] A_INV = copy of clip A with Invert (Luminance), Hue/Saturation, Directional Blur, visible on M-3 only; [5] A = clip A, ending at M-1. All burst layers are 1-frame or 2-frame layers trimmed exactly. Clip B is precomposed (B_PRE) so the inverted copy and the normal copy share the same scale animation.

## Steps

1. Pick the cut frame M (first frame of B). Precompose clip B as B_PRE (full length) so scale keys can live on the B layers in BURST.
2. A: clip A ends at M-1 (out point M).
3. A_INV: duplicate A and trim to frame M-3 only (1 frame). Add Invert (Channel Luminance, Blend 0%), Hue/Saturation (Master Saturation -100), Directional Blur (Direction 90 deg, Blur Length 25), Transform (Position 980,540).
4. FLASH: a white solid #FBFBFB, trimmed to frames M-2 and M-1 (2 frames).
5. B: B_PRE from frame M on. Transform Scale keys: M 280%, M+1 180%, M+2 178%, M+3 161%, then M+30 100% (key M+3 with outgoing speed fast; key M+30 incoming influence 75%, so the ease-out decays like the measured 148/131/119/112/108/102/100%). On frame M only, CC Radial Fast Blur (Center 960,540, Amount 70, Zoom Standard) keyed 70 at M and 0 at M+1 (hold keys).
6. B_INV: a second copy of B_PRE above B with the same Scale keys (or parent its scale to B with an expression), trimmed to M+1 and M+2. Add Invert (Channel RGB). Add a rectangle mask from x 0 to x 931 (48.5% of 1920) at M+1 and 0 to 912 at M+2 (hold keys), Mask Feather 2 px. Add Wave Warp (Wave Type Sine, Wave Height 8, Wave Width 600, Direction 0 deg, Wave Speed 0, Pinning All Edges off) applied after the mask, with Mask property 'Effects and Masks' order, so the edge bows near the bottom; or offset the bottom mask vertices by +18 px.
7. Clean B continues from M+3. No effects needed except the ongoing scale settle.
8. Optional per the agent's wording: re-randomise the order of the invert / flash / split frames and the burst length (5-6 frames) for each additional cut marker.
9. Stack shake_chroma_impact on top for the finished look.

## Effects used

- **Invert** (`ADBE Invert`) on A_INV: Channel Luminance (agent: 'luminance-only invert, hue stays put'); Blend With Original 0%
- **Hue/Saturation** (`ADBE HUE SATURATION`) on A_INV: Master Saturation -100 (render was fully grey, sat mean 0.1)
- **Directional Blur** (`ADBE Motion Blur`) on A_INV: Direction 90 deg; Blur Length 25
- **Transform** (`ADBE Geometry2`) on A_INV: Position 980,540 (about +20 px nudge)
- **CC Radial Fast Blur** (`CC Radial Fast Blur`) on B: Center 960,540; Amount 70 on frame M only; Zoom Standard
- **Invert** (`ADBE Invert`) on B_INV: Channel RGB; Blend 0%
- **Wave Warp** (`ADBE Wave Warp`) on B_INV: Wave Type Sine; Wave Height 8; Wave Width 600; Direction 0 deg; Wave Speed 0; Pinning none

## Keyframes

Relative to M = the first frame of the incoming clip, at 30 fps. M-3: A inverted+desat+blur (1 frame). M-2 and M-1: white flash (2 frames). M: B at 280% + zoom blur (1 frame). M+1: split at x 48.5%, B 180% (1 frame). M+2: split at x 47.5%, B 178% (1 frame). M+3: clean B at 161%, then ease-out to 100% at M+30. All burst switches use hold keyframes or trimmed 1-frame layers. Agent log: 'marker at frame 16, 6 frames 13 to 19, white flash on 14, hard vertical split on 18, invert and blur across the rest, incoming clip plays clean from 19'. The preview recording doubled frames, so the flash and split each read as 2 frames.

## Third-party plug-ins and native stand-ins

The burst was generated by the invideo agent (its own renderer). Every frame of it is reproducible with native Invert / Hue-Sat / Directional Blur / CC Radial Fast Blur / masks / Wave Warp, as above.

## What the reel did not show (inferred)

The agent's exact per-frame effect values (blur lengths, wave amount) are not shown, so they were estimated from pixels. Whether frame M-1 is a second flash or a luminance-inverted, heavily blurred A cannot be told: it renders as flat #fbfbfb, identical to M-2. The 2-frame flash and split may be preview frame duplication of single-frame events, since the agent describes single frames; build them as 2 frames to match the render.
