# Transitions: taste, status and approval history

Which transitions are approved, rejected or untested, in which genre, and why. The frame-by-frame recipes (light blow-out,
zoom rush, streak smear and the rest, with their L / S / C numbers) and the After Effects facts that decide whether a
recipe renders (gamma-space Exposure, Motion Tile per footage layer, per-frame keys) stay in premiere-ae-editing
`references/transitions.md` and `references/after-effects.md` section 12.

## Contents
1. Transitions by genre
2. Status of every transition we built or studied
3. Corrections to older notes
4. White flashes and dips: values by genre
5. Hand-off transitions (clean style)
6. The zoom cut, and why whips went
7. The 18 library effects as transitions: optical or geometric
8. How a new transition earns its place

## 1. Transitions by genre
- **Social ads and premium explainers:** hard cuts between shots. No fade-out that leaves one frame of the talking head
  before a cut ("its 1 frame of normal [presenter] before the next broll so don't fade it out"). When the grade lives on
  adjustment layers cut around B-roll, B-roll edges are hard cuts on phrase breaks: a dissolve exposes a moment of
  ungraded log footage. Cards match-cut (same roll, same size, pins fade). A white flash 0 -> 24% -> 0 over 0.15 s marks a
  caption cut. Graphics leave by a hard cut.
- **Documentary cutdowns (long footage cut into stories):** short white flashes on 2-3 big jumps per long cut, a
  whoosh and a camera shutter under them (section 4). Look at both sides of every white transition: 4 of 4 real misses in
  one round hid there (the next subtitle for 2 frames before a dip, an old line for 5 frames at a hook in-point).
- **Cracked music edits:** every cut is a transition, and the transition is OPTICAL (light, blur, streaks, colour, line
  art), never rigid geometry. A transition is a recipe of 6-12 distinct frames, not one effect on an ease. Flat white lasts
  1-3 frames; the body of a transition keeps structure and colour. The peak (white frame, streak peak, fullest panel)
  lands on the hit. About 20-35% of frames sit in a transition or effect state (`cracked-edits.md`).
- **Clean-techy reels:** motion carries the cut: hand-offs, one continuous move, a whip zoom for a change of world, hard
  3-frame panel wipes, 2-frame dips to black before reveals (references), match cuts, transitions caused by movement.
- **Native social posts:** hard cuts only. Slide-ins, wipes and designed transitions are ad tells.
- **Narrated mini-docs (reference genre, only when a client asks for that look):** turn lines as one word or a short line
  alone on black or white for 0.5-1.2 s, two black frames before the next cut, 5-15 per film. Never in music edits, where
  black frames were rejected.

## 2. Status of every transition we built or studied
Music-edit verdicts are from the reviews of 13-14 Oct 2026.

| Transition | Where | Status | Why / words |
|---|---|---|---|
| Zoom cut (scale 100 -> 120% into the cut, radial blur 0 -> 55 -> 0) | music edits | APPROVED as the whip replacement, then no longer the main transition | "this is good. but good wont cut we need GREAT"; still used inside the zoom rush |
| Whip (Motion Tile + Transform slide with a hold frame) | music edits | REJECTED | "looks ass": the hold frame shows a crisp mirrored frame |
| Shutter (bars close and open with a hot line) | music edits | REJECTED | box close at 18 s = "PowerPoint" |
| Rotational spin (Transform shutter 300) | music edits | REJECTED | rotate at ~3 s and ~13 s = "PowerPoint" |
| Wave Warp square-wave glitch slices with hue jumps | music edits | REJECTED | the checkered or box glitch family = "PowerPoint" |
| Invert flicker ("I", "I.I") | music edits | KEPT | |
| Negative strobe into a B&W section (12 fps inside) | music edits | KEPT | |
| Diagonal gradient colour flash in Add (orange -> pink) | music edits | KEPT, not flagged | keep short so it never becomes a flood |
| True RGB split | music edits | KEPT | |
| Light blow-out | music edits | KEPT | |
| Zoom rush with a radial chromatic split | music edits | KEPT | |
| Short vertical streak smear | music edits | KEPT | |
| Long sideways smear | music edits | REJECTED | abstract frames hiding the picture for 10+ frames |
| Light painting | music edits | ONLY SHORT | the 6-7 s one was "TOO long"; a shortened one stayed |
| Line-art strobes (E K E K, S D S D, C C) | music edits | KEPT | |
| Colour flood (orange, yellow, red frames) | music edits | REJECTED | disliked twice ("red frame at 8 s out") |
| Defocus space | music edits | KEPT | "okay" |
| Ray burst | music edits | UNREVIEWED | used once, not flagged |
| Red lens-streak flash on a lyric | music edits | REJECTED | it "doesnt even show anything" |
| Vortex (spin + zoom blur tunnel) | test reel only | UNREVIEWED | |
| Silhouette strobe stack ("WFIK") | music edits | KEPT, not flagged | |
| Light crack into flying strips | music edits | REJECTED 14 Oct | "look bad" |
| Silhouette burst (a window scaling about the player) | music edits | REJECTED 14 Oct | "look bad" |
| Flash panels (7 vertical bars, cream halves, 5 horizontal bands) | music edits | HIS ASK, not judged as built yet | his definition of geometry |
| Full white frame on the payoff moment | music edits | REJECTED | hid the ball going in |
| Cut-out pop (white rim + dimmed background) | test reel | REJECTED | read as a pale white wash |
| Glass shatter | study | NOT BUILT | the AE Shatter set-up needs its own study |
| White flash, then fade in from white (hook end, CTA) | documentary cutdowns | IN USE | no complaint; "flashes on every scene change, big jumps only, or none?" still unanswered |
| White caption flash 0 -> 24% -> 0 over 0.15 s | social ads | APPROVED with the dynamic captions | |
| Whip zoom changing world at its peak | clean reels | APPROVED (reference reviewer) | |

The user's own first edit used Impact Dip To White (4 frames) on cuts, 1-frame white frames on kicks, 3-frame light-bar
wipes, a mirror-edge zoom or spin inside nests and a 1-frame "portal" frame. It is his starting point, not the bar: copy
the flashes and wipes, not the spin.

## 3. Corrections to older notes
- The light crack with flying strips and the silhouette burst were REJECTED on 14 Oct 2026 ("I don't like the light
  crack or the silhouette burst"). An earlier note said geometry mixed with flashes made them "accepted as fresh". Only the
  silhouette strobe stack survived, and what he means by geometry is flash PANELS lit frame by frame.
- The lock-on ring rendered correctly but was rejected as a look ("the shot effect it just doesnt look nice"); the
  battery counter was rejected as a concept.
- The breath before a big moment is never a black frame: a quiet shot, a freeze or an audio dip.
- Whips are not banned everywhere: the rejected thing is a mirrored or static frame showing. In any genre, a whip passes
  only after a frame check shows none.

## 4. White flashes and dips: values by genre

| Genre | Values |
|---|---|
| Social ads | a white flash 0 -> 24% -> 0 over 0.15 s on a caption cut; a whoosh 0.11 s after the flash starts. Research: a white flash = a reverse swell into an impact, in speech gaps only, at most 3 per ad |
| Documentary cutdowns | hook end: white over 0.1 s, then the story fades in from white over 0.3 s (the same into the CTA); scene flashes: 4 frames out to white, 6 back in, on 2-3 big jumps per long cut; a mid-video insert: 6-frame white fade in, 4-frame fade out, the clips either side flash too. Sound: a whoosh starting 1.3 s before the cut plus a camera shutter on the cut at -4 dB; quieter copies (-10 dB, shutter 0.05 s early) on scene flashes and the insert so extra flashes do not feel like a new chapter |
| Music edits | flat white 1-3 frames, as band-size solids; about 5 white frames per 10 s; the blow-out shape: -2 hot orange, -1/0/+1 flat white, +2/+3 golden haze, +4 the shot |
| Mini-doc reference | 1-2 frame white flashes, black flicker frames, the odd inverted frame; 12-17 white flashes per reel |
| Analog night look | white flash frames = a white solid for 1-2 frames; text beats on black get two black frames before the next cut |
| Native posts | an impact = a 2-3 frame flash + a decaying 8-12 frame shake + a 105-112% punch, at most 2 per video |

## 5. Hand-off transitions (clean style)
- **Whip zoom into a new world:** matched scale, speed and brightness on both sides, a 3-frame crossfade at the peak and
  a zoom blur, both sides built from one shared layout so nothing jumps. Approved by the reference reviewer.
- **Across apps:** an After Effects move handing off to a Premiere move uses the same ease on both sides so the speed is
  continuous at the cut.
- **Panel wipe:** a dark panel wipes up covering 16%, 90%, 100% of the frame on three frames while carrying its content
  (25 fps reference). Motion blur OFF on it, or it renders as two ghosted copies.
- **Dip:** a 2-frame dip to black before a reveal (reference).
- **Short accents between montage shots (reference VC opens):** 2-6 frame zoom blurs and flash frames agree with our
  taste; whips and glitch tears only where no mirrored or static frame shows (ours wins on that conflict).
- **One-frame glitch burst** (library #13): a 6-frame recipe around a hard cut (M = the first frame of the new shot): M-3
  the old shot luminance-inverted and desaturated, smeared 25 px and nudged right; M-2 and M-1 flat white; M the new shot
  at about 280% with a zoom blur; M+1 and M+2 a hard vertical split with the left 48.5% then 47.5% RGB-inverted; from M+3
  the clean shot settles 161 -> 100% over 27 frames with an exponential ease-out. In music edits, check the split frames
  against the box-glitch verdict.
- **Luma dissolve** (library #2): darks appear first and highlights last over white (reveal 30 frames, dissolve out 11).

## 6. The zoom cut, and why whips went
- **The whip that was rejected:** one adjustment layer across the cut with Motion Tile (mirror edges) and a Transform
  slide whose key one frame before the cut is a HOLD. On that hold frame there is no motion, so no blur, and the mirror
  tiles show crisply: "looks ass".
- **The zoom cut that replaced it:** an adjustment layer from 2 frames before the cut to 3 after; Transform scale 100 ->
  120% into the cut (eased), held across it, back to 100% over 3 frames; CC Radial Fast Blur 0 -> 55 -> 0 centred on the
  picture; Transform's own shutter for the blur. No mirrored or static frames. Approved, then judged only "good": it is now
  one ingredient of the zoom rush, not the main transition.

## 7. The 18 library effects as transitions: optical or geometric

| # | Effect | Kind | Our mark |
|---|---|---|---|
| 1 | Pixel Reveal | geometric (a block grid) | breaks our taste in music edits |
| 2 | Luma Dissolve | optical (the picture's own light) | safe |
| 3 | Wave Blur Text | optical (bokeh) | safe |
| 7 | Gradient Depth Reveal | colour flood, then a reveal | breaks our taste (a long colour phase) |
| 8 | Hail Mary | optical light streaks | check frames first |
| 9 | Slow Shutter | optical (echoes) | safe |
| 10 | Whip Pan | geometric slide with mirrored tiles | breaks our taste |
| 13 | One-Frame Glitch | a frame recipe (light, blur, invert, split) | safe |
| 14 | Shake Chroma | distortion with colour fringes | check frames first (mirrored edges on the peak frame) |

Full marks and run notes: `effects-library.md`.

## 8. How a new transition earns its place
1. Find the intense moments of a reference by numbers, not by watching (per-frame luma change, inversion, blur, colour
   bursts over 12-frame windows).
2. Rebuild it on a real cut of your own footage, 1.2 s per test, many tests in one test reel.
3. Compare ours and the reference side by side at the same height, frame by frame, with L / S / C per frame; tune until
   the rows follow the reference's shape. Flat white (S under 8) at most 3 frames per transition.
4. Check it against the verdicts above (geometry, floods, long abstract holds, auras, mirrored frames).
5. Only then put it in an edit, and record the user's verdict here with the date and his words.
Tools and the AE facts behind each step: premiere-ae-editing `references/transitions.md`.
