# 06 Scripts: 3 full scripts for one new 15 to 16.5 s video (dhruvxr style)

Status: script 1 written first; scripts 2 and 3 follow. Written by a subagent from `research/dhruvxr/STUDY.md` only. Claude cannot watch or hear; all timings are planned, not measured on a render.

## Shared spec (all 3 scripts)
| Item | Value | Source |
|---|---|---|
| Frame | 16:9, 1920x1080 delivery (1280x720 also), 30 fps | STUDY 9.1 (measured refs: 1280x720, 30 and 29.97 fps) |
| Length | 15.0 s = 450 frames (f0 to f449) unless stated | Refs 15 to 16.5 s |
| Burst | f0 to f29: 9 shots of 2 to 4 frames, one idea | Refs: 8 to 9 shots in first 1 s |
| Turn | f153 (5.10 s = 34.0% of 450 f), hard cut on the music drop | ATN drop 5.0 to 5.1 s, 34% in |
| Words | 12 to 20 on screen incl. end mark; 1 to 5 per card; about 1 s per card | STUDY 4 Copy |
| Type | Inter Regular/Medium, sentence case, grey-white #AAAAAA to #DFDFDF on black, ink height 2.2 to 4.6% of frame (24 to 50 px on 1080); one bigger line 8 to 10% (86 to 108 px) | STUDY 9.5 |
| Text motion | Only: 3 f blur-in, word-by-word add every 4 to 6 f, right-to-left reveal 3 to 6 f, hard cuts, end mark no fade in / 24 f fade out | STUDY 9.7 |
| End | Hard cut to black 31 f, "[STUDIO]" small centred on black, no fade in, hold 56 f, fade out 24 f, black tail | ATN f279 to f447 pattern |
| Sound | Music with one drop at f153; hits land on picture changes, not on a beat grid; -9 to -10 LUFS integrated, -1 dBTP | Gate 1 defaults, STUDY 9.11, 9.16 |
| Rights | No real third-party logos, UI, voices or footage. All marks, apps and screens are designed by us and fictional | Gate 1, STUDY 9.15 |

Frame maths used everywhere: seconds = frame / 30. f153 = 5.10 s. f450 = 15.00 s.

---

## Script 1: "Taste" (ATN-type manifesto) [WRITTEN FIRST]

### Core message
Anyone can make anything now, so nothing stands out. Taste is the filter, and taste is chosen frame by frame. (Opinion, not a fact claim.)

### Cards (exact words, frames at 30 fps)
| # | Words (exact) | In | Out | Dur | Words | Role | Text motion | Size, place |
|---|---|---|---|---|---|---|---|---|
| 1 | "anyone" / "can" / "make" | f2 ("anyone"), f8 ("can"), f14 ("make") | f29 | 0.93 s | 3 | Claim, part 1 | Word-by-word add every 6 f; dim and blink f25 to f29 | 3.5% ink, centred y 52%, wide gaps |
| 2 | "anything now." | f30 | f66 | 1.23 s | 2 | Claim, part 2 | 3 f blur-in f30 to f32, hard cut out | 3.5%, centred y 52% |
| (gap) | none | f67 | f121 | 1.83 s | 0 | Picture carries "the flood" | none | none |
| 3 | "Nothing stands out." | f122 | f152 | 1.03 s | 3 | Problem | Right-to-left reveal over 6 f (f122 to f127) | Bigger: 7.8% ink, centred |
| 4 | "Taste" | f153 | f179 | 0.90 s | 1 | TURN, on the drop | Hard cut in on f153 | 3.5%, centred |
| 5 | "taste isn't" / "a prompt." | f180 | f215 | 1.20 s | 4 | Turn, part 2 | Hard cut in; split across width | 3.0%; "taste isn't" x 18 to 38%, "a prompt." x 62 to 80%, y 52% |
| 6 | "It's chosen" | f216 | f245 | 1.00 s | 2 | THESIS, part 1 | Hard cut in; 1 px white selection box with 4 corner handles drawn f216 | Biggest: 10% ink, centred |
| 7 | "frame by frame." | f246 | f278 | 1.10 s | 3 | THESIS, part 2 | 3 f blur-in f246 to f248 | 4.6%, centred |
| (black) | none | f279 | f309 | 1.03 s | 0 | Breath | Hard cut to black | none |
| 8 | "[STUDIO]" | f310 | f389 | 2.67 s | 1 | End mark | No fade in; hold f310 to f365 (56 f); fade out f366 to f389 (24 f) | 3.0%, centred, lower case if the mark is a word |
| (tail) | none | f390 | f449 | 2.00 s | 0 | Black tail | none | none |

On-screen words: 3 + 2 + 3 + 1 + 4 + 2 + 3 + 1 = **19** (inside 12 to 20). Cards: 8. Words per card: 1 to 4.
Read-out line: "anyone can make anything now. Nothing stands out. Taste. taste isn't a prompt. It's chosen frame by frame. [STUDIO]"

### Shot-by-shot plan (30 fps, 450 f)
| Shot | Frames | Len | Picture | Text | Effect | Sound hit |
|---|---|---|---|---|---|---|
| 1 | f0 to f3 | 4 f | Fictional make-tool #1: a big "Generate" button, flat UI, our own mark (a filled circle) | "anyone" from f2 | Hard cut | Tick + music start f0 |
| 2 | f4 to f6 | 3 f | Fictional tool #2: prompt field, cursor clicks "Make" | "anyone" | Hard cut | Tick f4 |
| 3 | f7 to f9 | 3 f | Tool #3: progress bar at 100% | "anyone can" from f8 | Hard cut | Tick f7 |
| 4 | f10 to f11 | 2 f | Tool #4: a grid of 12 identical thumbnails pops in | "anyone can" | Hard cut | Tick f10 |
| 5 | f12 to f15 | 4 f | Tool #5: "Create" button pressed state | "anyone can make" from f14 | Hard cut | Tick f12 |
| 6 | f16 to f18 | 3 f | Tool #6: export dialog "Done" | same | Hard cut | Tick f16 |
| 7 | f19 to f21 | 3 f | Tool #7: an image appears in a chat bubble (fictional chat UI, no real app) | same | Hard cut | Tick f19 |
| 8 | f22 to f25 | 4 f | Tool #8: a website builder, page done | same, dims from f25 | Hard cut | Tick f22 |
| 9 | f26 to f29 | 4 f | Tool #9: a "Publish" toast | blinks off/on f26 to f29 | Hard cut | Tick f26 |
| 10 | f30 to f66 | 37 f | Cursor clicks "Generate" again and again; outputs tile out from the centre, slow push in (scale 1.00 to 1.06) | "anything now." | Glitch insert f42 to f50 (9 f): horizontal band shifts, 2 offset rectangles of shot 4 | Glitch crunch f42; swell under |
| 11 | f67 to f152 | 86 f | Curved 3D wall of near-identical generated images (same pastel sunset, same 3D blob, same smiling avatar) flies in and stacks; a "hero" tile lands at f104 and looks like all the others; everything darkens to black f130 to f152 | "Nothing stands out." f122 to f152 | PIL perspective per tile, 2-key camera move; darken via linear gain ramp | Whoosh f67; soft hit f104 (hero lands); riser f122 to f152; music filter closes |
| 12 | f153 to f179 | 27 f | Macro on black: one bezier curve, a single handle being dragged 4 px; thin white line, grey handles | "Taste" | Hard cut on f153 | **DROP f153 (5.10 s)**, bass hit |
| 13 | f180 to f191 | 12 f | Empty fictional prompt field, caret blinking, no text typed | "taste isn't" / "a prompt." | Hard cut | Bass hit f180 |
| 14 | f192 to f212 | 21 f | Second burst: one cut-out hand-drawn letter "a" (our own drawing) stays put while 7 generated-look backgrounds swap every 3 f | same | Background swap every 3 f (f192, f195, f198, f201, f204, f207, f210) | Ticks on each swap; bass hit f204 |
| 15 | f213 to f215 | 3 f | The cut-out "a" alone on dark grey | same | Hard cut | none |
| 16 | f216 to f245 | 30 f | The same "a" small at bottom right, out of focus, on near black | "It's chosen" in selection box | 1 px white box, 4 corner handles 8x8 px | Bass hit f216 |
| 17 | f246 to f278 | 33 f | Horizontal timeline of 9 frames of the "a" being refined, playhead steps one frame every 3 f | "frame by frame." | Playhead step every 3 f; 3 f blur-in on text | Small tick per playhead step; hit f246 |
| 18 | f279 to f309 | 31 f | Black | none | Hard cut to black | Music cuts to silence or a low tail f279 |
| 19 | f310 to f389 | 80 f | Black | "[STUDIO]" | No fade in, 24 f fade out from f366 | Soft single hit f310; tail decays |
| 20 | f390 to f449 | 60 f | Black | none | none | Silence by f449 |

Shot count: 20. Shots of 4 frames or less: 10 (50%). Ref range 35 to 58%.

### Assets needed (script 1)
1. 9 fictional "make tool" UI screens (shots 1 to 9): our own designed UI, fictional names and marks (abstract shapes). No real app names. Build in PIL or HTML.
2. Cursor sprite and a tiling output grid (shot 10).
3. About 30 "samey generated" image tiles (shot 11). Must be made by us or licensed; mark the source. Do not use real people's faces unless licensed.
4. Bezier curve and handle render (shot 12), PIL.
5. Fictional empty prompt field UI (shot 13).
6. Hand-drawn letter "a" cut-out, PNG with alpha (shots 14 to 17); 7 background textures.
7. Timeline strip of 9 refinement frames (shot 17).
8. "[STUDIO]" mark file (placeholder until the real mark is supplied).
9. Music track with a clear drop placed at 5.10 s; 9 ticks, 1 glitch crunch, 1 whoosh, 1 riser, 5 bass hits. All licensed or made by us. Source UNCHECKED until chosen.
10. Optional opening voice sample f0 to f150: our own recorded voice only. Default: none.
11. Font: Inter (SIL Open Font License; licence terms UNCHECKED for this job).

### Facts and numbers in script 1
- No facts or statistics on screen. The copy is opinion. "Taste isn't a prompt" is a stance, not a claim to verify.

---

## Script 2: (in progress)

## Script 3: (in progress)

## Must not say (all scripts)
(in progress)
