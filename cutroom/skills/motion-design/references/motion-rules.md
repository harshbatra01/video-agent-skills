# Motion rules: moves, eases, overlap, hand-offs, continuity

How things move, for every genre. Which look is right for which job: `effect-vocabulary-and-taste.md`. The scripting
side (k2, chain, keys, KeyframeEase, setValuesAtTimes, parenting traps) lives in premiere-ae-editing
`references/after-effects.md` sections 4, 5 and 13; this file says what to build and why.

## Contents
1. Moves and looks: two kinds of animation
2. Named eases
3. Overlap: the 20-50 rule (corrected wording)
4. Compound moves, staggers, dense curves
5. Overshoot, bounce and pops (depends on the genre)
6. Hand-offs at every cut
7. Continuity: one world, one move
8. "Dynamic" means speed contrast
9. Camera moves on footage: zooms and push-ins
10. Timing to the voice and the beat
11. Holds, numbers and clutter
12. Montages
13. Stills
14. Verify motion as frames
15. Measured reference values

## 1. Moves and looks: two kinds of animation
- **A move** (a push-in, a card sliding in, a word arriving, a counter, a zoom) is TWO keyframes, start and end, on its
  own property, shaped in the speed graph with a named ease (section 2). Why: per-frame values look mechanical and
  nobody can adjust them by hand later. A clean-motion reviewer's words: "when creating animations never animate frame
  by frame always use keyframes at start and end of motion and use graphs."
- **A look that changes every frame** (a flash recipe, a strobe, an impact frame, flash panels) is hold keys or trimmed
  1-frame layers, one distinct look per frame. Why: a premium transition is a sequence of 6-12 different frames, not one
  effect on an ease curve (frame study of about 30 top edits, 14 Oct 2026). The same reviewer's own glitch burst is
  built this way, so both rules hold.
- Quick test: if a thing travels or scales from A to B, it is a move; if each frame is a different picture, it is a look.
- An item that must hold still gets its leftover entrance keys stripped (Position, Rotation, Opacity) and opacity set to
  100%. Why: a 3-frame opacity fade left over from a fly-in dimmed a product right at the cut.
- An element already on screen never animates in again. Reviewer: "you transitioned the comb in again".

## 2. Named eases
Out influence of key 1 / in influence of key 2; speeds 0 at both keys; the outer side of each key keeps 33.3%.

| Ease | Out / in | Speed peak at | Use for |
|---|---|---|---|
| settle | 15 / 80 | 13.2% of the move | fast start, long settle: moves that land (the default) |
| bell | 73 / 73 | 50% | moves that overlap the next one |
| accel | 80 / 15 | 86.8% | slow start, fast end: whips and squashes that leave on a cut, fade-outs |
| gentle | 45 / 60 | 41.8% | soft drifts |
| hold / linear | | | steps, constant drifts, per-frame looks |

The peak positions were checked with After Effects' ease maths. Other eases that worked on approved or measured work:
- Premiere graphics in approved social ads: 0.15 out / 0.85 in for arrivals (snappy start, long settle), 0.70 / 0.25
  for exits; layers staggered 0.10-0.26 s; each item rises 8-70 px while it fades in.
- "Fast start, long creep" (the smooth text transition): key 1 out at high speed (3150-3250 px/s) with 4-6% influence,
  key 2 in at speed 0 with 60%. The move happens while the words are still blurred or transparent.
- A cursor sweep: out 20 / in 95 (about cubic-bezier 0.20, 0, 0.05, 1) over 26 frames; the tutorial used 36 / 100.
- Short slides in the clean-techy style: an expo-style ease-out.
- Fades in scene builds: fade in = settle, fade out = accel, 6 frames.
- Our older `keys()` helper in ae_lib.jsx: influence 33 = gentle, 75-90 = strong.
Position takes one KeyframeEase per side; Scale and other non-spatial 2D/3D properties one per dimension (mechanics:
after-effects.md trap 31).

## 3. Overlap: the 20-50 rule (corrected wording)
When move B follows move A, start B when A is **50 to 80% done** (so the two overlap by 20 to 50% of A's span) and shape
B so that **B's speed peak lands exactly on A's last keyframe**. Why: the two then read as one continuous motion with no
dip in speed at the hand-over. (The source text says B starts "when A is 20 to 50% done"; its own numbers and its own
builder mean 50-80% done. Verified with the ease maths.)

| Case | Keys (A is 0f to 24f) | Ease of B | Result |
|---|---|---|---|
| Wrong | B 24f to 48f | any | stop-start: a visible halt |
| Sloppy | B 12f to 36f | out 1 / in 91 | speed spike at B's first key (0.5% into B): the hand-off jolts |
| Right, 50% overlap | B 12f to 36f | both 73 / 73 (bell) | B peaks at 24f, A's last key |
| Right, 20% overlap | B 19f to 43f | out 24 / in 80 | B peaks at 19.9% of its span (23.8f), A's last key is at 20.8% |

A live diagram of this rule is effects-library #15 (`overlap_keyframes_20_50_graph_peak`).

## 4. Compound moves, staggers, dense curves
- Split a compound move across separate properties so one dimension never drags the other. Example, a CRT switch-off:
  the layer's Scale Y settles (the picture collapses to a bright line), then a Transform effect's Scale Width settles
  (the line shrinks to a dot), then the dot fades: three two-key moves (`tvOff` in motion_lib.jsx).
- A stagger of many items is ONE two-key eased slider driving an expression on all of them. Why: the timing stays one
  move the user can adjust. Our stepped counters follow the same idea: a Source Text expression reads one [time, value]
  array, so the number and its shape always agree.
- A dense curve (many keys) only when one ease cannot describe the path, for example a camera path; put it on its own
  clearly named control and say so. Why: anything the user might adjust gets two keys.
- Ease-driven reveals: a posterized matte only changes over a few stops of an Exposure sweep, so key only that range; an
  accel curve evens out an exponential front.
- When Premiere and After Effects must match a curve exactly (a glass card's blur window in Premiere following an AE
  card), sample the curve per frame with linear keys and export the same numbers as geometry for the Premiere side.

## 5. Overshoot, bounce and pops (depends on the genre)
- **Clean-techy, premium explainer and finance briefs: no overshoot.** No bounces, no easeOutBack, no spins, no cartoony
  pops, no tilted stickers, no wobbly hand-drawn marks, no film-burn blobs. Use fades, short eased slides with an
  expo-style ease-out, straight outlines and underlines, quick white flashes; pop sounds become soft ticks. Why: the
  clean-motion reviewer asked for motion that feels "clean and techy, never cartoony"; our premium explainer reviewer
  wanted "premium [calm]", and pins that fade instead of pop.
- **Social ad captions and cards: small pops are approved.** A question card 72 -> 104 -> 100% with a -5 deg settle in
  0.3 s; a gold star 0 -> 118 -> 100% at 0.46 s (the one hero element); a dynamic caption word 128 -> 100% in 0.24 s,
  then a slow drift to 103.5%. Keep overshoot to about 4-6% except one hero element per graphic.
- `popIn` in ae_lib.jsx overshoots to 110% by default: pass `over` on purpose (1.04-1.06 for cards), or use `k2(...,
  "settle")` for clean briefs. When unsure, settle with no overshoot.
- Browser or code animatics: critically damped springs (no overshoot) plus a small constant drift so nothing goes dead.

## 6. Hand-offs at every cut
- Plan a hand-off at every cut: the same direction and speed on both sides, eased keys, motion blur on. Why: "smooth
  motion where one move brings in the next" is what makes clean reference reels feel clean.
- An After Effects move that hands off to a Premiere move (a graphic comp into the presenter clip): compute both sides
  from the same ease so the speed is continuous at the cut.
- A whip ZOOM can hide a change of world: matched scale, speed and brightness on both sides, a 3-frame crossfade at the
  peak and a zoom blur, both sides built from one shared layout so nothing jumps.
- Whip PANS hide hard cuts between shots of one subject in the clean style, but our music-edit user rejected whips that
  show a mirrored or static frame ("looks ass"). Default to the zoom cut; use a whip only after a frame check shows no
  mirrored or held frame (`transitions.md`).
- Motion blur OFF on hard 3-frame panel wipes, or they render as two ghosted copies.
- Match cuts between similar cards: same roll angle (4 deg), same card size, pins fade rather than pop. Reviewer on the
  first try: "make it a biiit more smooth".

## 7. Continuity: one world, one move
- Prefer one continuous camera move through one world over a new layout every beat. Reviewer notes on a narrated
  mini-doc: "keep the last scene going, no need to hard cut", "continue from last scene instead of bringing back the
  message board", "transition should be seamless/smooth". Another: "make all AE motion one continuous move".
- Every transition is caused by movement (the camera rises, things swim or fly in), no morphing, when a brief asks for
  continuity. Design transitions: match cuts, an object carried into the next scene, an element that becomes the next
  scene's element.
- Our explainers still want a hard visual change about every 3 s (a sample hook changed every ~3.4 s, while only ~32%
  of its frames moved). Not a conflict: deliver the change through the move (a new element, a push into the next item).
- One movement at a time; the rest holds. User on a 2.5D test: "cool cool this works, just not this many movements
  together lol".
- Never cut away from a page the voice is still reading (keep the shop page open, no cut to the presenter).
- Fill a long voice hold with something that moves slowly, not with more text.
- A recurring device can carry a story (a sheet that opens the film and becomes an inbox at the end; real start lights
  returning as a metronome). It must come from the subject's real world: a made-up charging battery was rejected
  ("i dont like the charging concept at all").

## 8. "Dynamic" means speed contrast
- "More dynamic ramps, the motion is kinda boring" was fixed with strong speed contrast inside one continuous camera
  move: a kick, a drift, a whip, a climb that slams into a freeze (299,996 to 299,999) just before the hit. Not more
  cuts and not new angles.
- The camera follows the action; it does not swing to new angles. A 3D chase angle was rejected ("dont change angle like
  that"); the fix kept the head of a rising line at a fixed point while the world scrolled (a crash-game graph).
- Tracking without a 3D camera and the parenting traps: `depth-2.5d-3d.md` section 6. A 60 degree comp shutter keeps a
  fast tracking shot readable.
- In music edits "dynamic" is ramps, punches and flashes inside held shots, not more cuts (`cracked-edits.md`).

## 9. Camera moves on footage: zooms and push-ins
**Approved zoom recipe for talking-head ads** (copied from the user's own reference edit, kept by the user):
- Each zoom piece is an adjustment layer above the A-roll carrying TWO Transform effects: a slow drift and a quick punch.
  Keys on Scale Height, Sampling bicubic.
- Intro: punch 115 -> 100% over 0.867 s (ease out) times drift 108 -> 100% over the piece (the user's reference used
  120 x 110).
- Push: punch 100 -> 110% over 1.133 s times a linear drift from 100% at 1.3-2.0% per second.
- Pull: punch 110 -> 100% over 1.117 s times a linear drift from where the push ended back to 100%.
- Alternate push and pull, keep the level continuous across piece boundaries.
- Board or whiteboard shot: anchor (0.40, 0.35), punch 104, intro 104 x 103, drift 0.25-0.4% per second.
- The maths: stacked Transforms multiply, so the peak = punch x drift (115 x 108 = 124%). Check that product against the
  frame: the reference reached 132% and cropped her hair. Cap peaks around 116-121%.
- Anchor the zoom on the face: Transform Anchor Point and Position both at the face point (0.5, 0.33).
- Start a move every time the picture returns from B-roll, so it is seen; push into a B-roll cut and land the pull after.
- Zooms wait for the word they illustrate ("wait a bit before zooming").
- When B-roll is removed to show A-roll again, extend the zoom layers (and the grade pieces) over the new A-roll, or the
  picture jumps to unzoomed, ungraded footage.

**Push-in rates** (per second, linear unless noted):

| Where | Rate |
|---|---|
| presenter in a news-style reel | 2-4% (up to 6-11%) |
| every still in a mini-doc (reference genre) | 4-10% (measured 5-8%) |
| a photo on a desk-style doc | 3.5%, elsewhere 5-13% |
| our client explainers: blurred background still (`stillBg`) | 4% over the whole shot |
| our 2.5D room drift | Dolly 0-2% over a shot (`depth-2.5d-3d.md`) |

- 1080p broadcast wide shots go soft past about 1.8x zoom: zoom moderately and mark the subject instead.
- A product hero shot lands and holds still before the cut ("move then cut"); hold product shots 2-3 s.

## 10. Timing to the voice and the beat
- Text appears on its word's first spoken frame. A word that starts within about 0.2 s before a cut appears on the cut;
  the phrase after a text beat waits for the next shot (measured on mini-docs).
- Pose swaps 2 frames before the stressed word, with a 2-frame dissolve.
- Under a voice, an SFX peak lands on the frame or 1 frame late. In music edits a visual hit lands on the beat or 1 frame
  early, never late: early sound is noticed at about 45 ms, late picture is tolerated up to about 125 ms (ITU-R BT.1359).
- Snap every event to a frame before writing a script: round(t x fps) / fps minus 0.1 ms. Why: times rounded to 4
  decimals land after the real frame time and put about a third of all cuts and hits one frame late.
- A proof graphic lands on the payoff phrase, not the setup. Reviewer: "have some subs rolling for 2-3 seconds and then
  pop the headline in... currently its on screen for too long even as she is building up". Hard cut out.
- Overlays and titles start WITH their B-roll shot and never spill into the next shot. If an overlay needs more time,
  start the B-roll earlier (a meter's B-roll moved 0.4 s earlier so the meter starts with it and lands on "100 times").
- When a year and a value roll together, roll them only after the voice says the value, so no year sits next to a wrong
  value.
- Counters land fast, then hold still to a hard cut ("freeze it before and just hard cut").
- On native posts the number reacts within 1-2 frames of the event it shows.

## 11. Holds, numbers and clutter (information graphics)
- One number on screen. Never the same figure twice in one frame: a counter plus a dotted "300K" behind it "looked odd";
  two numbers in one counter frame read as clutter.
- A graphic that sits about 1 s behind a wipe and a pop reads "harsh": hold it longer, or change it inside a frame that is
  already there with a short crossfade. Scope: information graphics. The 1-3 frame flashes of music edits are a
  different device and stay.
- No numbered points (01/02/03 cards, numbered dials, marker dots on lines, side numbers on arcs) unless the script
  itself is a numbered list. Ours: 1-2-3 badges "looks ass"; a board with 1-2-3 numbering was "bland". The clean-motion
  reviewer: "The script does not have any points, this is pointless".
- No callout tags with leader lines ("dont do pointers"). Values sit inside or above the element, labels under it,
  ranges as shaded bands.
- No captions while a designed graphic prints the spoken words ("captions on top of text doesn't make sense"); details
  in `titles-captions-type.md`.
- Counters are a device to spread around ("i like the year counters and stuff see if we can fit in other places"), but
  never two back to back ("i dont like the counter over there since we already did that just before").
- Little text: "too much text man, try to show". One verdict stamp at most.

## 12. Montages
- A montage belongs together: one subject, face-matched framing (the same eye position and size on every cut), one
  grade, one null pushing the whole run with two settle keys (`faceMontage` in motion_lib.jsx). Every third frame in
  black and white worked. No logos, slides or unrelated images: a flash montage with a logo and slides was "all over
  the place and not cohesive".
- Social ads: one clip per spoken item, matched to the word, 1.0-1.2 s each. No 5-frame shots: "no super small clips
  small is fine but not super small"; a shot that flashes for a few frames is an error.
- Mini-doc look (reference only, when a client asks for it): a quarter of shots are 2-4 frames and face montages cut every
  2 frames, always one subject and matched framing.
- Photo montage idea (research, untested): hold each photo 3-6 frames with a slow push, a 1-2 frame white flash on the
  beat, grain and a light leak; or 3D polaroids with a camera push and depth of field.

## 13. Stills
- A still feels alive through a camera move (push-in, 2.5D depth planes, drift), never through fake breathing or body sway
  on a cut-out. User: "breathing maybe would also look bad right now as its an image would look too ai".
- Pose swaps, contact shadow, light wrap, colour match and grain add life too. Details: `depth-2.5d-3d.md`.

## 14. Verify motion as frames
- Before anyone sees it: a sheet of the in, middle and last frame of every shot at about 480 px; read it once, fix,
  re-render. Next to the storyboard frames when a board exists.
- Look at both sides of every transition, and at every frame (not one per second) wherever effects last 1-3 frames.
- Check glyphs (blank symbols), clipped glows, half-cut icons, text over faces, text that leaves too early, and timing
  against the voice (the word a graphic illustrates is under it).
- Check it in the Premiere timeline at its real time; the user may have moved things.
- Test a new technique on a short test from existing assets first (a 9 s room test got the verdict before a whole video
  used it). A new transition gets a test reel: one real cut per technique, 1.2 s each, about 45 s of render.

## 15. Measured reference values
Measured frame by frame on public reference work (references, not our house style):

| Look | Numbers |
|---|---|
| Tech-news explainer at 25 fps | a dark panel wipe covers 16%, 90%, 100% of the frame over three frames while carrying its content; a 2-frame dip to black before a reveal; italic setup words fade over 3 frames while rising about 18 px over 4; a reveal box appears one frame early and its letters rise out of it one frame apart, 6 frames each; bar charts build the baseline over 8 frames and the bars over 9, staggered; document focus lightens the rest of the page to about 40% while a multiply-yellow sweep follows the voice; no bounce, overshoot or glow anywhere |
| Presenter news reels | push-ins 2-4% per second (up to 6-11%); display type built word by word on the syllable; a hand-drawn arrow writes on over about 0.45 s |
| Mini-doc | push-ins 5-8% per second; 1-2 frame white flashes, black flicker frames, the odd inverted frame; per reel 12-17 one- or two-frame white flashes (rebuild spec: 5-15 white flash frames, 2-6 zoom or whip blurs, 1-3 glitch slices, one 6-10 image flash montage, one strobe); end-card logo hard-cuts in at about 10x, eases down over about 27 frames, keeps shrinking for 2 s and fades over 0.8 s with the music playing through |
| Desk-style doc | push-ins 3.5% per second through a photo, 5-13% elsewhere; drifting 3D moves across desk sets with focus pulls; footage shrinks into a print on a page; end: two thin white diagonals slide in from the corners over the darkening last shot (about 10 frames), meet in an X and collapse into the logo, held on black 1.5 s |
| VC cold opens | words bloom and settle over 3-6 frames; transitions of 2-6 frames between montage shots; the last line cuts to black, about 2 s of silence, the logo fades up |
| Our premium explainer sample | a hard visual change every ~3.4 s, about 32% of frames moving |
| Top music edits | about 20-40% of frames in a blur, transition or effect state (the top three measured 108-116 such frames and 6.3-10.8 white frames per 10 s); the target for ours is 20-35% (`cracked-edits.md` section 5) |
