---
name: motion-design
description: "How we design motion and which effects our reviewers approved or banned: two-key moves with named eases, the overlap rule, hand-offs, continuity; titles, kinetic type, animated captions, lower thirds, cards, counters, CTA and end cards; transitions, flashes, strobes and glitches by genre; beat-synced 'cracked' sports music edits end to end; native After Effects looks (analog finish, dither, halftone, glow); 2.5D parallax and 3D tilts; an 18-effect After Effects library with taste marks and Windows and Mac run steps. Use it whenever the user wants something animated, motion graphics, moving titles or captions, a transition, flash, whip, zoom cut, speed ramp or glitch, motion that is smoother, cleaner, more dynamic, more premium or less 'PowerPoint', an edit cut to a song or a flashy sports edit, an effect recreated from a tutorial or creator, life on a still photo, or a taste check on an effect, even if After Effects is never named."
---

# Motion design

How things should move, which effects our users and reviewers loved or rejected, and the recipes behind the approved
ones. Taste depends on the genre, so pick the genre first. The tool mechanics (After Effects scripting, the runner,
keyframe APIs, .prproj editing, frame sheets) are in **premiere-ae-editing**; storytelling, cutting, B-roll and the
general caption style are in **editing-playbook**. A new client's brief and references win over these defaults, and the
user's own hand edits in their latest save are the brief.

## 1. Pick the genre first

| Genre | Default motion | Never |
|---|---|---|
| Social ads with captions and cards (vertical paid social, often a famous face) | reference-style dynamic captions, cards with proof, counters that land and hold, eased zoom pieces on the A-roll, hard cuts | small text straight on footage, graphics over the face, stickers, a counter right after a counter |
| Premium YouTube explainers (16:9, presenter, review format) | premium type, real footage and 3D, one movement at a time, a visual change about every 3 s, gentle 2.5D drift | poster type, sticker piles, cartoon stand-ins, fake breathing on stills |
| Clean-techy brand and explainer reels | two-key moves, one continuous camera move, hand-offs, light native glow, quick white flashes | bounces, overshoot, spins, pops, pointers, paid glow |
| Cracked sports music edits | an optical transition on every cut, type behind the player, flash panels, strobes on the beat | geometric transitions, auras, colour floods, abstract holds of 10+ frames, black breath frames |
| Native social posts (faceless pages, news pages) | real footage, one native caption in the house look, hard cuts, 5-10% punch-ins | designed data cards, template motion, the TikTok white box |
| Documentary cutdowns (long footage cut into stories) | hard cuts, short white flashes on big jumps | a stray frame of another subtitle or shot at a flash (check both sides) |

If the genre is unclear, ask. Full verdicts with the users' words: `references/effect-vocabulary-and-taste.md`.

## 2. Rules for every genre
1. **A move is two keys, a look is per frame.** Camera pushes, slides, arrivals, zooms and counters are two keyframes
   shaped in the speed graph, never frame by frame (per-frame values look mechanical and nobody can adjust them). Flash
   recipes, strobes and flash panels are hold keys or 1-frame layers, one distinct look per frame (a premium transition
   is 6-12 different frames).
2. **Named eases** (out / in influence): settle 15/80 for moves that land (the default), bell 73/73 for moves that
   overlap the next one, accel 80/15 for moves that leave on a cut, gentle 45/60 for drifts, hold or linear for steps.
3. **Overlap:** start the next move when the current one is 50-80% done and land the next move's speed peak on the
   current move's last key (50% overlap: both bell 73/73; 20% overlap: the next one out 24 / in 80). Starting when the
   first ends is a stop-start; a spike at the second move's first key jolts. Why: two moves then read as one.
4. **Split compound moves** across properties so one dimension never drags another; a stagger of many items is one
   two-key slider driving an expression; a dense curve only on its own named control when one ease cannot do it.
5. **Hand off motion at every cut:** the same direction and speed across the cut, eased, motion blur on (off on hard
   3-frame panel wipes, which ghost). A whip zoom can hide a change of world; a whip pan only after a frame check shows no
   mirrored or static frame.
6. **Continuity over cuts:** one continuous move through one world beats a new layout every beat; deliver the
   "change every ~3 s" through the move. One movement at a time ("just not this many movements together lol"). Never
   re-animate an element already on screen; never cut away from a page the voice is still reading.
7. **"Dynamic" = speed contrast inside one move** (a kick, a drift, a whip, a climb slamming into a freeze), not more
   cuts or new angles. The camera follows the action from a stable view ("dont change angle like that").
8. **Time it to the word and the beat:** text on its word's first spoken frame; pose swaps 2 frames early; zooms wait for
   the word; a proof graphic lands on the payoff phrase, not the setup; overlays start with their B-roll and never spill
   into the next shot. In music edits hits land on the beat or 1 frame early, never late. Snap every event to a frame.
9. **One number, no clutter:** never the same figure twice in a frame; counters land fast and hold still to a hard cut;
   no numbered points or pointers unless the script is a numbered list; no captions while a graphic prints the spoken
   words; little text ("too much text man, try to show").
10. **Overshoot depends on the genre:** none in clean, premium or finance briefs; small approved pops in social ad cards
    (72 -> 104 -> 100%). `popIn` defaults to 110%: set it on purpose.
11. **Glow lightly and natively:** native Glow, threshold about 55%, radius about a quarter of the element, intensity 0.8
    or less, Composite Original On Top; whole-picture bloom threshold 85+, intensity 0.2 or less. No paid glow plug-ins,
    no auras, no glow that ends in a square edge.
12. **Stills live through camera moves, never fake breathing or sway** ("would look too ai"): 2.5D drift, pose swaps,
    contact shadow, light wrap, colour match, grain.
13. **Real over designed:** real footage, archive and 3D renders beat drawings, stickers and designed data cards; text
    only where it means something; a motif must come from the subject's real story.
14. **Build in Premiere, After Effects for elements only:** plates, presenters, screenshots, text and simple moves are
    Premiere layers; After Effects makes what Premiere cannot (complex animated graphics, keying, 2.5D rigs, effects
    Premiere lacks) and delivers ELEMENTS (alpha overlays, moving plates), never whole shots with recurring assets baked
    in. Why: a presenter change baked into 17 renders meant 17 re-renders.
15. **Verify motion as frames** before anyone sees it: in, middle and last frame of every shot; both sides of every
    transition; every frame wherever effects last 1-3 frames; the timing against the voice; the real Premiere timeline.

Details and reasons: `references/motion-rules.md`.

## 3. Genre rules
### Social ads with captions and cards
- Captions: kicker + one big word (Coolvetica Heavy Comp 236 px fitted to 980 px, blur-in 0.2 s, 128 -> 100% in 0.24 s,
  an RGB split sliding in, a 0 -> 24% -> 0 white flash on the cut), only over B-roll, subtitles under it disabled.
- Stacked synced list words on their spoken words ("perfect"); a partial-word roll for near-identical words; frosted
  glass cards top-left (the blur itself is a Premiere layer); headline cards that really ran, with a highlighter; a meter
  that ends on a marker and fades with its B-roll; year counters, never two back to back.
- Everything not tied to an on-set prop lives in the lower caption zone with one bottom gradient; nothing over the face.
- Small text on plates, sized for a phone; mock every title on graded frames first.
- Zoom pieces on the A-roll: two stacked Transforms (a drift and a punch), peaks 116-121%, anchored on the face.
- Recipes with every value: `references/titles-captions-type.md` section 3.

### Premium YouTube explainers
- "Premium calm" type through one text helper with a premium switch; thin accent bars; one verdict stamp at most.
- Copy the channel's earlier graphics exactly when asked (rebuild from the old project's dump, not by eye).
- Chapter maps as designed transitions (the user's 3-pillar design), animated icons instead of 1-2-3.
- Presenter stills in a 2.5D room: Truck +-10 px, Dolly 0-2% per shot; poses from one master image; one wardrobe.
- End screen: 15-20 s, presenter and background only, space left for the platform's elements (never add them).
- Recipes: `references/titles-captions-type.md` section 4, `references/depth-2.5d-3d.md`.

### Clean-techy brand and explainer reels (a second house style)
- Every move two keys with a named ease; continuity and hand-offs; transitions caused by movement.
- No bounces, overshoot, spins, pops, tilted stickers, wobbly hand-drawn marks or film-burn blobs; pop sounds become
  soft ticks; quick white flashes, straight outlines and underlines, short slides with an expo ease-out.
- One measured reference look per video; montages of one subject with face-matched framing.
- Designed scenes in After Effects (scoped method): `references/scene-building.md`.

### Cracked sports music edits
- Bar: "we are the best in the world... absolutely crazy editors go so hard"; "Anything flashy is good. Anything crazy is
  good. Anything basic is bad."
- One storytelling base per edit from the 12 in the structure library; a window from one beat before the drop through
  the song's most-replayed stretch to a section's last downbeat plus a bar; the payoff zone at 55-70%.
- Cut on the strongest kick or snare within +-0.2 s, floored to a frame; land the transition's PEAK on the hit.
- 20-35% of frames in an effect state, a transition on every cut, about 5 white frames per 10 s; vary density by
  section, densest at the payoff.
- The picture in a 1080x800 band with type in the bars; the number or word behind the player with a 1-frame white
  silhouette (the effect he loved most); the title in the top bar with his head popping out; lyric words in the bottom
  bar; flash panels lit frame by frame; strobes written in the one-letter code.
- Banned: spins, box glitches, blades, whips with mirrored frames ("PowerPoint", "looks ass"), the light crack and the
  silhouette burst (rejected 14 Oct), auras, colour floods, abstract holds of 10+ frames, black breath frames, gimmick
  motifs, literal word-on-object text, reticles.
- End on the last downbeat and hold a card for one bar; check footage audio is off. End to end:
  `references/cracked-edits.md`.
- Assembly (decided 15 Oct 2026): music edits are assembled in Premiere and After Effects only makes the effect
  elements; the earlier one-live-comp build is the old route (`references/cracked-edits.md` section 16).

### Native social posts
- Start from real moments, borrowed footage and one native caption in the house look (bold caps headline, coloured
  numbers, a tweet card over a clip, carousels); the number is the punchline or the stakes, never the product.
- Real movement only: motion from the footage, 5-10% punch-ins, hard cuts; no slide-ins, wipes, counting numbers, 3D flips,
  template chrome, whoosh packs or a new skin per format ("these are all SAME types of posts bro").
- 4-9 readable words at a time, mid-screen, at most 2 text sizes, nothing under 40 px; frame 0 is the cover and every
  number on it is final and true.
- Rules: `references/titles-captions-type.md` section 6; the post formats themselves: social-video-formats.

### Documentary cutdowns
- Hard cuts; a white flash over 0.1 s then a 0.3 s fade from white at the hook end and into the CTA; scene flashes (4
  frames out, 6 back) on 2-3 big jumps per long cut; look at both sides of every white transition. `references/transitions.md`.

## 4. How to work
1. **Genre, brief, references.** Read the user's latest save and their hand edits first; they are the brief.
2. **Look before inventing.** Check the vocabulary and the libraries (`references/effect-vocabulary-and-taste.md`,
   `references/effects-library.md`). When the user names an effect from a tutorial or creator, find it there.
3. **Asked to "learn the effects" of a page:** count the headline effects first (one or two per post), tell the user the
   count and the list, and ask before adding the creator's other devices.
4. **Mock type on real graded frames; test a new transition in a test reel** (one real cut per technique, 1.2 s each)
   and compare it frame by frame with the reference (L / S / C numbers) before it goes into an edit.
5. **Build** with the premiere-ae-editing tools: Premiere layers first, After Effects elements where needed.
6. **QA as frames** (rule 15), then deliver as a new version; never overwrite what the user already has.
7. **Record every verdict** with its date and the user's words in the taste file, and turn a systematic miss into a
   default in the generator, so the next job starts from it.

## 5. Tools
- premiere-ae-editing `scripts/ae/`: `ae_lib.jsx` (`keys`, `popIn`, `flyIn`, `slowPush`, `typeOn`, `imgCard`,
  `highlighter`, `softEllipse`, `softBand`), `motion_lib.jsx` (`k2`, `EASES`, set pieces), `scene_lib.jsx` (`chain`,
  `cap`, `camera`, `testComp`), `ae_build.py`, `ae_run.py`, `check_jsx.py`; `scripts/media/frames.py`, `fsheet.py`
  (every-frame sheets), `beats.py` (kicks, snares), `hear.py` (word times).
- This skill's `effects-library/`: 18 native effects, `ae/effects_build.py` (test one effect with a frame sheet, build the
  library, `--dry-run` without After Effects). Read `effects-library/README.md` first.
- The music-edit kit (anatomy, moments, compare, plan toolkit, build script, `fx_lib.jsx`, `edits_lib.jsx`): shipped in
  `library/pipelines/edits-kit/`; described in `references/cracked-edits.md` section 18; why these edits sell songs:
  social-video-formats.

## 6. Which reference to read

| You need | Read |
|---|---|
| Eases, overlap, hand-offs, continuity, zooms, push-in rates, timing, measured reference values | `references/motion-rules.md` |
| Whether an effect or look is approved, rejected or untested, with the users' words, by genre | `references/effect-vocabulary-and-taste.md` |
| A beat-synced sports music edit, from the song to QA | `references/cracked-edits.md` |
| Type rules, type animation, the approved caption, title, card, counter and CTA recipes, native post type | `references/titles-captions-type.md` |
| Which transition for which genre, every transition's status, flash values, the zoom cut | `references/transitions.md` |
| Analog finish, dither, halftone, glow and bloom, LED wall, globe, logos, colour working space, effect facts | `references/native-looks.md` |
| 2.5D room rig maths, presenter compositing, gentle camera values, tracking without a camera, 3D tilts and renders | `references/depth-2.5d-3d.md` |
| A fully designed motion piece built in After Effects (scene modules, plates, tests, helper agents) | `references/scene-building.md` |
| The 18-effect library and our other effect libraries, each with a taste mark | `references/effects-library.md`, `effects-library/README.md`, `effects-library/recipes/` |

## 7. Open questions (ask the user when they matter)
- Which genre defaults the reviewer's kit should lead with when a brief does not say.
- SF Pro in client videos (its licence targets Apple-platform design) or Inter as the house UI font.
- The sRGB working space for all our After Effects builds, or only plate-heavy ones (approved Windows renders used AE's
  default space; test one shot first).
- Flash-panel halves: confirm the order against the user's own edit (they described bottom half first).
- Documentary cutdowns: flashes on every scene change, big jumps only, or none (asked, not answered).
- Pending verdicts: the first full use of flash panels and the three newest music edits (impact frames, poster
  silhouettes, type flash, ghost trail, freeze clones, photo prints, numeral sandwich, hit list, stutter, loops).

Sources: real production jobs, Sept to Oct 2026.
