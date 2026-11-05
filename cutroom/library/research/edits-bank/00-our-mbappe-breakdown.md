# Our GASS x Mbappe edit, frame by frame (the bar to beat)

Source: 13 renders and the Premiere project (sequences "gass mbappe" and
"GASS MBAPPE FINAL"). Read on 13 Oct 2026 from every frame (618 frames, 1080x1920, 30 fps, 20.6 s) plus the project file.
Song: GASS (Nemzzz ft. Travis Scott), first 20.6 s of the track. Measured: 138 BPM (half-time feel), quiet intro
(-30 to -18 dB), drop at about 3.5 to 4.1 s (-6 dB from there).

## Versions (what changed)
All 12 full-length renders are frame-identical except **2.4 to 4.6 s** (the build into the drop).
| Render | Build into the drop (2.4-4.6 s) |
|---|---|
| `gass mbappe.mp4` = v1 (18 Sep), same as v3 | music video whip-blur shots, white flash, "MBAPPE 10" back photo with push-in, GASS logo slams in with vertical motion blur, white flash, drop |
| v2 | v1 with a tiny change at 4.13-4.27 s |
| v4 | keeps the music video whip shots, swaps photo + logo for a wide goal shot and a light-bar wipe into the drop |
| v5, "v 5", v2_1 | no music video: France dribble, dip to white, slow zoom on a wide shot, light-bar wipe, tighter zoom on the drop clip |
| FINAL_1, FINAL_2, "v5 gass mbappe" | v5 plus a 1-frame glitch insert of another clip on the kick at 3.80 s |
| `gass mbappe final` (21 Sep) | back to the v1 build (feathered flash edge, steadier logo, light-bar wipe into the drop) |
| draft (17.4 s), hook (4.1 s) | early tests, no end card |
So v1 "did the most" in exactly one place: the music-video build with the photo and the logo slam.

## Second by second (v1). K = kick, S = snare (measured)
| Time | Frames | What you see | Effect | Hit |
|---|---|---|---|---|
| 0.00-2.53 | 0-75 | Mbappe dribble (PSG), 16:9 picture in the middle of the vertical frame | white player silhouette on 2 frames with a 1-frame gap: f1+f3, f28+f30 (defenders), f52+f54 | K+S 0.01, S 0.96, K+S 1.73 |
| 2.53-2.97 | 76-88 | music video: buildings, car | blur flash in, whip / directional blur, cool desaturated look | K 2.57, K 2.98 |
| 2.97-3.20 | 89-95 | music video: the artist walking | radial zoom blur, flash | K+S 3.00 |
| 3.20-3.50 | 96-105 | white frame, then "MBAPPE 10" back photo | white flash, slow push-in, tilt at the end | K+S 3.42 |
| 3.53-4.03 | 106-121 | GASS logo (from the music video) | slams in with heavy vertical motion blur, small shake | S 3.76, K 3.81 |
| 4.07 | 122 | full white frame | flash | K 4.08 |
| **4.10** | 123 | **DROP**: Mbappe dribble vs Nantes | hard cut | K 4.08 |
| 4.10-5.57 | 123-166 | dribble, wide attack | speed tweak 1.27x | |
| 5.57-5.67 | 167-169 | cream light bar slides down over the cut | 3-frame light-bar wipe | K+S 5.57 |
| 5.67-7.30 | 170-218 | PSG dribble, wide goal | cuts | S 6.21, K 6.86 |
| 7.30-9.17 | 219-275 | celebrations, dribble | dip-to-white (4 frames) on every cut: 7.30, 7.70, 8.23, 9.10; whip move on the close-up | S 7.17, S 7.71, S 8.15 |
| 9.20-9.90 | 276-296 | close-up walking, pink LED light streak | white silhouette strobe f283, f285, f287 | K+S 9.43 |
| 9.90-10.07 | 297-301 | Mbappe from behind | inverse strobe: background turns white, player stays (alternate frames) | K+S 9.86 |
| 10.30 | 309 | white frame | 1-frame flash | K+S 10.29 |
| 10.33-12.30 | 310-368 | feet close-up, two dribbles (Reims) | cuts + zoom | K 10.92, S 11.13 |
| 12.30-12.40 | 369-371 | light bar slides up over the cut | light-bar wipe | S 12.23, K 12.46 |
| 12.40-13.67 | 372-409 | France dribble, goal, arms-out celebration | celebration slowed to 0.86x | K+S 13.31 |
| 13.67-13.80 | 410-412 | | dip to white | K+S 13.73 |
| 13.77-16.30 | 413-488 | aerial dribble (1.27 s), Real Madrid run and volley | longest shots of the edit | S 15.00 |
| 16.30-16.97 | 489-508 | ball hits the net, floodlights | mirror-edge spin/zoom on the net | K+S 16.31 |
| 16.97 | 509 | music video frame: black hole on white | "portal" frame | K+S 16.95 |
| 17.00-17.37 | 510-520 | music video: car in a tunnel | heavy motion blur whip | K 17.16 |
| 17.37-20.60 | 521-617 | Spotify logo + "Gass" + "Nemzz ft. Travis Scott", small, on black | settles in 4 frames, then static for 3.2 s | S 17.38 |

## Effect inventory (how each was built in Premiere, from the project file)
1. **White silhouette strobe**: 1-frame copy of the clip on the track above, mask around the player, VR Glow, Opacity blend
   mode; placed on 2-3 frames with 1-frame gaps. The single most "premium" thing in the edit.
2. **Inverse strobe**: same trick with the mask inverted, so the background flashes white and the player stays.
3. **Dip-to-white** (built-in Impact Dip To White, 4 frames) on 5 cuts, plus 1-frame white frames at 4.07 and 10.30 s.
4. **Light-bar wipe**: 3-frame graphic (Noise + Shape, Crop keyframes) sliding across the cut.
5. **Mirror-edge zoom / spin**: Transform + 4x Mirror + Transform stacks inside nests (net shot, end).
6. **Whip / zoom blur** on music video shots (2.6-3.2 s, 17.0 s).
7. **Logo slam**: the music video's GASS logo dropping in with vertical motion blur.
8. **Still photo hit**: "MBAPPE 10" back photo, tint flash + push-in, 0.33 s.
9. **Texture pass** (3.2-17 s): Black Video with VR Digital Glitch + Wave Warp + Lumetri + Noise: fine wavy ripple on every
   edge, grain, cool crushed-black grade. Only visible at 100%.
10. **Speed tweaks** (0.86x to 1.27x) so moves land on beats.
11. **Portal frame**: a music video "black hole" frame as a 1-frame bridge into the tunnel shot.
12. **End card**: Spotify-style, shaken by a 600-keyframe shake preset that settles within 4 frames.

## Numbers
- Main section (4.1-17.4 s): 18-19 shots, average 0.7 s, longest 1.3 s, shortest 0.37 s, plus 1-3 frame flashes.
- 43 big frame changes; 28 of them (65%) land within 1.5 frames of a measured kick, snare or onset.
- About 1.2 flash / strobe / wipe events per second in the main section.
- Picture area: 16:9 band 1080x800 in a 1080x1920 frame, so about 58% of the screen is black bars.
- End card: 3.2 s of 20.6 s (16%) is a near-static black frame.

## What it does well
- Frame-level strobes (1 frame on, 1 off) on the player: rare in average edits, reads as high effort.
- The music video as the build ties the edit to the song (good for a promo).
- Every flash sits on a kick or snare; small speed changes land moves on beats.
- One consistent texture and grade gives it a "look".

## Gaps vs cracked edits (hypotheses to test against the bank)
- No velocity (speed ramps) or smooth slow-mo, no freeze frames, no stutters.
- No zoom punches or shakes on hits in the main section.
- No captions, lyric text or player-name type (only the music video's own logo).
- Letterbox wastes most of the vertical screen; nothing uses the black bars.
- One colour look all the way; no colour pop, B&W switch or grade change on the drop.
- Roto stops at flat silhouettes: no outlines, text behind the player, clones or trails.
- No overlays (light leaks, sparks, lightning), no RGB split / chromatic hits, no glow on highlights.
- First second is an ordinary dribble, small in frame: weak hook.
- Ending is 3.2 s of static black; a loop ending or an animated card over footage would hold viewers better.

## Our other edits (measured, lighter pass)
| Edit | Format | Length | Shots | Avg shot | Cuts on a beat | Style |
|---|---|---|---|---|---|---|
| messi edit (Confidence) | 1080x1350, 60 fps | 34.1 s | 17 cuts | 2.0 s | 2 of 17 | clean gameplay cuts, slow-mo close-up push with a white flash at 12.5 s, no effects pass, no end card |
| home knucks (Home, acoustic) | 1920x1080, 25 fps | 55.2 s | 21 cuts | 2.6 s | 16 of 21 | opens on the music video with a small lyric subtitle, then PSG Mbappe clips, Spotify end card (larger, cleaner than GASS) |
| basketball v2 (4 Raws, EsDeeKid) | 1080x1920 letterbox, 30 fps | 33.2 s | 27 cuts | 1.2 s | 17 of 27 | LeBron clips, light-bar wipes as 4-frame clusters (3.1, 4.9, 15.6, 23.9 s), B&W section, white flashes, tiny Spotify card |
| Military v3 (Time Flies, Unknown T) | 1080x1920 letterbox, 24 fps | 18.8 s | 22 cuts | 0.85 s | 17 of 22 | jets, half the frames B&W, grey dips, music-video text frame, explosion flash, Spotify card |
House style today: 16:9 picture letterboxed in a vertical frame, dip-to-white, light-bar wipes, B&W switches, Spotify-style
end card. The GASS x Mbappe edit is the only one with frame-level strobes, roto silhouettes and a texture pass.

Frame sheets: `our-edits\sheets\` (every frame of v1, the changed window of v4, v5, FINAL_1 and final, key-frame crops,
`others_overview.png` for the four other edits).
