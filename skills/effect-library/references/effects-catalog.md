# Effects catalog (the boss's layer)

Started 19 Oct 2026. Purpose: when a new video starts, read the script, find each moment below, and propose
"this effect, here" with a recommendation, before building anything.

What this file is NOT: a copy of the kit. Taste verdicts live in the kit (motion-design
`references/effect-vocabulary-and-taste.md`, editing-playbook, client files) and win over anything here. This file
points to them and adds what the kit does not have: what actually runs on THIS Mac (no Adobe) and the new tools.

Companion files: `kit-effects-guide.md` (every kit effect, where it was used, what runs here) and
`vibe-motion-review.md` (each vibe-motion look and the plan to rebuild the good ones in HyperFrames).

## Toolchains on this Mac

| Code | Tool | Where | Runs here? | Notes |
|---|---|---|---|---|
| V7 | Python builder from the mini-doc job (PIL + numpy + ffmpeg) | skill `minidoc-reference-style`, `scripts/build_template_v7.py`; effect specs in its `references/effects-library.md` | yes, used for v1 to v6 | every effect is code we own; slow to restyle |
| HF | HyperFrames 0.8.174 (HTML + GSAP rendered by a pinned Chrome) | CLI in `~/VisionKit/mine/jobs/minidoc-01/hf-test/`; skills `hyperframes*`, `media-use`; 447 registry items (`npx hyperframes catalog`) | yes, tested 19 Oct 2026 | renders transparent ProRes 4444 layers we place over V7 or any cut; telemetry off with `HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1` |
| FF | ffmpeg 9.0.2 filters | system | yes | grain, xfade, LUTs, overlays, loudness |
| AE | Kit After Effects library, 18 effects with taste marks | motion-design `effects-library/` | NO (no Adobe here) | read the recipes for ideas and taste only |
| VM | vibe-motion/skills | github.com/vibe-motion/skills | not installed | unmaintained, no licence file: do not copy its code into client work without the author's OK |

Status words: TESTED (built and checked on this Mac), KIT-LOVED / KIT-KEEP / KIT-OUT (the kit's verdict, see the
taste file for the exact context), REF (measured on the Altman reference), UNTESTED (exists, never built here).

## Moments and what fits them

### 1. Hook, first 0.5 to 3 s
| Option | Tool | Status | When |
|---|---|---|---|
| Pixel-block opener: mosaic resolves, ragged white block flashes, caption builds | V7 `blocks()` | REF, used in v6 | doc hooks copied from the Altman format. The kit marks the AE pixel_reveal "breaks our taste" for other genres: only use it where the reference has it |
| Giant glowing word whip into a tilted polaroid | V7 `giant()` + `polaroid()` | REF, used in v6 | the scary or key word of the hook |
| Big word slam on beat | HF `headline-slam`, `char-slam-explode`, blueprint `kinetic-type-beats` | UNTESTED | an alternative hook if a reference does not dictate one |

### 2. Naming a person or source (founder content too)
| Option | Tool | Status | When |
|---|---|---|---|
| Bold condensed name title, small gold pill, no box, below the caption line | HF `lt-kicker-name`, `lt-soft-pill`, `lt-side-rule` (restyle) | KIT liked this look in ads; HF block UNTESTED | founder reels, podcast clips, first time someone speaks |
| Sports-broadcast strap | HF `lt-bold-block`, `lt-stack-bars` | KIT liked; TESTED as a chyron (below) | |

### 3. A quote, a post, a tweet
| Option | Tool | Status | When |
|---|---|---|---|
| Real post as an X card, words lifting on their VO word starts, last key word in gold | HF `x-post` (adapted, engagement numbers removed) | TESTED 19 Oct (minidoc-01, 28.9 s) | any quoted post. Kit: "a tweet card over a clip" is approved for news pages, so put it over darkened moving footage, not a plain card |
| Serif quote card | V7 quote card | used in v6 | plain dark card breaks the mini-doc "no empty frames" rule; use only as the one breather |
| Reddit post, YouTube comment | HF `reddit-post`, `yt-comment-card` | UNTESTED | audience-reaction beats |
| Never: invented likes, views or replies on any card (house rule) | | | |

### 4. A number, money, a valuation
| Option | Tool | Status | When |
|---|---|---|---|
| Big serif number card ($56B, $1) | V7 number card | used in v6 | keep it over darkened moving footage |
| Count-up, rolling digits, slot roll | HF `count-up`, `number-wheel`, `slot-machine-roll`, `apple-money-count`, `number-pop-in` | UNTESTED | a number that changes ($56B to $1T); kit liked "year counters" in ads |
| Number on a real news chyron | real footage | REF (best option) | needs licensed or CC news footage |
| Story in numbers behind the subject | AE idea, rebuild in HF | KIT-KEEP | |
| Colour the numbers (gold in this doc; white, red for negatives, green for ticks in ads) | any | KIT | |

### 5. A date or a time jump
| Option | Tool | Status | When |
|---|---|---|---|
| Year card | V7 year card | used in v6 | |
| Split-flap board | HF `split-flap-board` | UNTESTED | "In 2018", "By January 2024" |
| Date tag on a chyron | HF (in the tested chyron) | TESTED | event dates |

### 6. A place, a move, geography
| Option | Tool | Status | When |
|---|---|---|---|
| US map, gold arc from A to B, B fills gold, labels | HF `us-map-flow` (adapted, local map data) | TESTED 19 Oct (Delaware to Texas, 0.47 s) | any "moved to", "expanded to" |
| Other maps | HF `us-map`, `us-map-bubble`, `us-map-hex`, `world-map`, `nyc-paris-flight` | UNTESTED | global stories |
| 3D globe route | VM `threejs-earth-render` | UNTESTED, licence unclear | big international moves (16:9 native, needs reframing) |

### 7. A news event, a headline
| Option | Tool | Status | When |
|---|---|---|---|
| News chyron: gold date tag + dark bar, condensed caps, wipe in, balanced 2 lines | HF `lt-bold-block` restyled | TESTED 19 Oct ("Tesla shareholders vote to move to Texas") | over the footage of the event. Generic design only, never a real network's branding |
| Scrolling ticker | HF `news-ticker` | UNTESTED | a run of headlines |
| Headline cards that really ran, word for word, with a highlighter | HF `marker-highlight`, `inline-highlight` | KIT liked; UNTESTED | real headlines only, never invented |
| Screen-photo look: fisheye, moire, push to a spot, yellow highlight slides in | VM `fisheye-motion` (Remotion) | UNTESTED, no licence | showing a court document or article "on a screen"; rebuild the idea in HF instead |

### 8. A ruling, a verdict, a legal turn
| Option | Tool | Status | When |
|---|---|---|---|
| VOIDED / REVERSED stamp | V7 stamp | used in v6 | |
| Strike a word and replace it | HF `strikethrough-replace` | UNTESTED | "voided", "reversed", rule changes |
| Hand-drawn circle or underline on a document | HF `hw-callout-circle`, `hw-underline` | UNTESTED; kit rejected "wobbly hand-drawn marks" in one ad round | only if the client's taste allows |

### 9. Abstract idea (power, time, money, risk)
| Option | Tool | Status | When |
|---|---|---|---|
| Symbol montage bursts, 2 to 4 frames a shot | V7 `BURST()` | REF, used in v6 | abstract words; prefer short video loops over stills |
| Literal object with giant serif word | V7 | REF | "kill switch", "locked out" |
| Never: a gimmick motif not from the story (kit OUT) | | | |

### 10. Comparison, before and after
| Option | Tool | Status | When |
|---|---|---|---|
| Split cards | HF `comparison-split`, blueprint `comparison-split` | UNTESTED | |
| Wipe between two states | HF `before-after-wipe`, `grade-split-reveal` | UNTESTED | |
| Black-and-white to colour reveal | VM `colorize` (Python + moderngl) | UNTESTED, no licence | old photo coming to life |
| Colour pop (B&W world, colour cut-out) | V7 cut-out (`person_mask.js`) + grade | KIT-KEEP on shots with visible background | |

### 11. Charts, stock moves, trends
| Option | Tool | Status | When |
|---|---|---|---|
| Line, bar, decline charts | HF `data-chart`, `decline-chart`, `animated-bar-chart`, `chart-story`, `bar-chart-race` | UNTESTED | real data only, source on screen |
| Candlestick stock chart | VM `remotion-candlestick` | UNTESTED; needs Remotion (licence costs for 4+ people) and Yahoo data | rebuild in HF if needed |
| Caution: a news-page reviewer rejected "designed data cards and motion-graphic data videos" | | KIT-OUT for that client | check the client file first |

### 12. Transitions and energy between shots
| Option | Tool | Status | When |
|---|---|---|---|
| 2-frame light smear flash, 1-frame exposure pop, decaying shake | V7 `flash`, `pop`, `shake` | REF, used in v6 | the default cut accents in this format |
| Zoom cut with radial blur | AE idea; HF `cinematic-zoom`, `push-in` | KIT-KEEP | |
| White flash through | HF `flash-through-white`, `editorial-flash-overlay` | UNTESTED | approved family (light and flash) |
| Invert flicker, RGB split | HF `rgb-glitch-text`, `chromatic-aberration-wipe` | KIT-KEEP in music edits | |
| Whip pans | HF `whip-pan` | KIT-OUT ("looks ass" when a frame mirrors) | avoid |
| Spins, box glitches, blades, shutters | HF `glitch`, `shutter-slam`, `transitions-mechanical` | KIT-OUT ("PowerPoint") | avoid |

### 13. Stills that must not look dead
| Option | Tool | Status | When |
|---|---|---|---|
| Flicker plus slow push | V7 `flicker()` | REF, used in v6 | every still |
| Parallax and depth on a cut-out | HF `parallax-zoom`, `camera-rig-depth-stack`, `rack-focus` | UNTESTED | the biggest gap vs After Effects; test next |
| Punch-in split of one picture on the words | V7 (v6 pace pass) | used in v6 | |

### 14. Breather, turn, soundbite
| Option | Tool | Status | When |
|---|---|---|---|
| One black breather card | V7 | REF (once per video) | the music edit client rejected black frames; it is right only in this doc format |
| Rule-break soundbite with the music out | V7 audio | REF | a real speaker, 2 to 5 s |

### 15. Captions and finish (every frame)
| Option | Tool | Status | When |
|---|---|---|---|
| 1 to 3 word captions, serif italic + heavy sans key words, black on bright frames | V7 | REF, used in v6 | doc format |
| Dynamic captions with RGB split; stacked synced list words | HF `caption-glitch-rgb`, `caption-kinetic-slam`, `per-word-rise` | KIT liked in ads; UNTESTED in HF | ads, founder reels |
| Edge blur, magenta and green fringe, pink rim, vignette, grain, applied after captions | V7 `finish()` | REF | doc format |
| Grain on HF layers so they match V7 shots | FF `noise` on the overlay only (`tools/hf_composite.py`) | TESTED | any HF layer over a V7 cut |
| Light leaks, halftone, dither, camcorder HUD | HF `light-leak`, `halftone-field`, `ordered-dither-pass`, `camcorder-hud` | UNTESTED | section looks; kit: glows never flood the frame |

### 16. Ending, logo, CTA
| Option | Tool | Status | When |
|---|---|---|---|
| Face-strip collage into a logo sting | V7 idea | REF | doc endings |
| Logo sting, CTA lockup | HF `logo-sting`, `logo-outro`, `cta-lockup`; VM `pixel2motion` (raster logo to animated SVG) | UNTESTED | page logo still a placeholder in minidoc-01 |

## Rules learned while testing HyperFrames (19 Oct 2026)
- Registry blocks are 1920x1080 starting points with sample data (fake likes, "illustrative data"). Restyle every one
  for 1080x1920 and strip invented numbers.
- Snap HF element times to the cut's real frames: v6 cuts sit on the beat grid, not on whole frames. Use the first frame
  at or after the grid time, or one frame of the old shot shows through.
- Blocks pull GSAP, fonts and map data from CDNs. Save them under `assets/` so renders work offline and repeat exactly.
- Low memory (8 GB) forces HF's slow screenshot mode: 225 frames at 1080x1920 took about 40 s with one worker.
- The mini-doc rule "no empty frames" applies to HF cards too: put them over darkened moving footage.

## How to use this at the start of a video
1. Read the script and tag each line with a moment number from this file.
2. For each tag, pick one option, checked against the client file and the kit taste file. Prefer TESTED, then KIT-KEEP.
3. Show the plan as a table (time, line, effect, tool, why), with one recommendation per spot, before building.
4. After the review, update the Status column here (dated) and the kit taste notes via feedback-for-kanishk.md.
