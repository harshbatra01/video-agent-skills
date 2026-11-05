# 06 Scripts: 3 full scripts for one new 15 to 16.5 s video (dhruvxr style)

Status: final (07:52 UTC). Script 1 written first, then 2 and 3. Written by a subagent from `research/dhruvxr/STUDY.md` only. Claude cannot watch or hear; all timings are planned, not measured on a render.

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

## Script 2: "[PRODUCT]" (WHP-type brand film, fictional or our own product)

Length 16.5 s = 495 f (f0 to f494). Drop and turn at **f168 = 5.60 s = 33.9%**. Voice carries the sentence; screen shows nouns (WHP pattern).

### Core message
Ideas get buried in threads; [PRODUCT] puts every draft side by side so work gets finished. [PRODUCT] is a placeholder; no product facts are claimed.

### Voice-over (our own recorded voice; 16 words)
"Ideas." (f42 to f60) / "Buried in threads." (f80 to f105) / "Clarity." (f170 to f195) / "All your drafts, side by side." (f200 to f266) / "Finished work starts here." (f297 to f354) / "[PRODUCT]." (f383 to f414)

### Cards (on-screen words, frames at 30 fps)
| # | Words (exact) | In | Out | Dur | Words | Role | Text motion |
|---|---|---|---|---|---|---|---|
| 1 | "// Ideas //" | f21 | f74 | 1.80 s | 1 | Hook | 3 f blur-in f21 to f23; cuts out with shot f74 |
| 2 | "Threads" | f76 | f77 | 2 f | 1 | Problem flash | 2-frame big word, italic, glow (WHP f76 pattern) |
| 3 | "@/ noise //" | f81 | f95 | 0.50 s | 1 | Problem label | 3 f blur-in |
| 4 | "clarity" | f168 | f230 | 2.10 s | 1 | TURN, on the drop | 3 f blur-in f168 to f170; x 26 to 35%, y 27% |
| 5 | "/ˈklerədē/" | f174 | f230 | 1.90 s | 1 | Phonetics | 3 f blur-in; x 71 to 82%, y 77%; drifts 25 px from card 4 over 60 f; 8 f fade out after white f231 |
| 6 | "side by side" | f241 | f285 | 1.50 s | 3 | Product label | 3 f blur-in |
| 7 | "finished work" | f287 | f321 | 1.17 s | 2 | THESIS, part 1 | Moves with the world, leaves at frame edge |
| 8 | "starts here." | f322 | f342 | 0.70 s | 2 | THESIS, part 2 | Hard cut in on white flash f322 |
| 9 | "[PRODUCT]" | f380 | f424 | 1.50 s | 1 | Product wordmark | Right-to-left wipe 3 f (f380 to f382), fade up 7 f (to f389) |
| 10 | "[STUDIO]" | f435 | f494 | 2.00 s | 1 | Our end mark on black | No fade in; hold f435 to f470 (36 f); fade out f471 to f494 (24 f) |
On-screen words: **14**. Voice words: 16 (WHP: 15).

### Shot-by-shot plan (30 fps, 495 f)
| Shot | Frames | Len | Picture | Text | Effect | Sound hit |
|---|---|---|---|---|---|---|
| 1 | f0 to f3 | 4 f | [PRODUCT] mark built of dots | none | Hard cut | Sub hit starts f3 |
| 2 | f4 to f6 | 3 f | Sticky note macro | none | Vertical-line screen texture on | Sub continues |
| 3 | f7 to f9 | 3 f | Pencil line drawn | none | Texture | Sub |
| 4 | f10 | 1 f | White | none | White flash | Sub |
| 5 | f11 to f14 | 4 f | Fictional voice-memo waveform UI | none | Texture | Sub |
| 6 | f15 to f17 | 3 f | Marker cap pops off | none | Hard cut | Sub |
| 7 | f18 to f21 | 4 f | Napkin sketch | "// Ideas //" from f21 | Blur-in | Sub |
| 8 | f22 to f25 | 4 f | Fictional phone notes list | same | Hard cut | Sub |
| 9 | f26 to f29 | 4 f | Index cards fanned | same | Hard cut | Sub |
| 10 | f30 to f44 | 15 f | Ink spreads from the sketch | same | Slow push | Sub to f48 (1.6 s); VO "Ideas." f42 |
| 11 | f45 | 1 f | White | same | White flash | none |
| 12 | f46 to f75 | 30 f | Fictional chat thread scrolling faster and faster | same to f74 | Motion blur | Dip to -26 dB f63 to f78 |
| 13 | f76 to f77 | 2 f | Same scroll, blown out | "Threads" | Big word flash | Hit f76; VO "Buried in threads." f80 |
| 14 | f78 to f95 | 18 f | Threshold black and white of the scroll, from above | "@/ noise //" f81 to f95 | Threshold | Hit f84 |
| 15 | f96 to f111 | 16 f | [PRODUCT] board UI (our own design) tilted in 3D | UI labels only | 2 f focus pull f96 to f97 | Hit f96 |
| 16 | f112 to f129 | 18 f | Scan-line tear over the UI, a fictional log list flashes | none | Band shifts, white bars (glitch 3.73 to 4.30 s) | Glitch hit f112 |
| 17 | f130 to f167 | 38 f | White, fading to dots that gather into one point | none | Fade from white | Riser f130 to f167 |
| 18 | f168 to f230 | 63 f | Dot grid snaps into a sharp square (keyhole idea, our own form) | "clarity", phonetics | Drift | **DROP f168 (5.60 s)**; VO "Clarity." f170 |
| 19 | f231 to f232 | 2 f | White | labels fade out f231 to f238 | White flash | Hit f231 |
| 20 | f233 to f286 | 54 f | Star particles become draft cards that land side by side on the board | "side by side" f241 to f285 | Particles | VO "All your drafts, side by side." f200 to f266; hit f241 |
| 21 | f287 to f321 | 35 f | [PRODUCT] mark made of photo tiles of our own team work, camera push, tiles burst into a collage | "finished work" | 2-key camera scale | Hit f287; VO "Finished work starts here." f297 |
| 22 | f322 | 1 f | White | "starts here." in | White flash | Hit f322 |
| 23 | f323 to f342 | 20 f | Second burst: 4 shots of 5 f (slow-shutter studio, stairs, fisheye desk, hands on keyboard) | "starts here." | Hard cuts, texture back on | Ticks f323, f328, f333, f338 |
| 24 | f343 to f379 | 37 f | Rotating dot globe, dims | none | Dot sphere, fade | Bed about -18 dB |
| 25 | f380 to f424 | 45 f | Black | "[PRODUCT]" wordmark | Wipe plus fade up | Hit f380; VO "[PRODUCT]." f383 |
| 26 | f425 to f434 | 10 f | Black | none | Hard cut | Tail |
| 27 | f435 to f494 | 60 f | Black | "[STUDIO]" | No fade in, 24 f fade out | Soft hit f435; fade to silence by f494 |
Shot count 30 (27 rows; row 23 holds 4 shots; WHP: 31). Shots of 4 f or less: 13 (43%). Card lengths run 2 f to 2.1 s here, as in WHP, not 1 s each as in ATN.

### Assets needed (script 2)
1. [PRODUCT] name, dot mark, photo-tile mark and wordmark (placeholders until supplied).
2. [PRODUCT] board UI designed by us (shots 15, 20), plus a fictional log list.
3. 8 macro inserts for the burst (sticky note, pencil, marker, napkin, index cards): our own shoot or our own renders.
4. Fictional chat UI and fictional phone-notes UI (no real app look).
5. Own team photos with releases for shot 21; own studio clips for shot 23.
6. Dot form, particle and dot globe renders (numpy).
7. Voice-over: our own voice, 16 words. No voice clone of a real person.
8. Music with drop at 5.60 s; sub hit, 12 picture-change hits, riser, ticks. Licence UNCHECKED until chosen.
9. Phonetic spelling "/ˈklerədē/" for "clarity": UNCHECKED against a dictionary.

### Facts and numbers in script 2
- None. WHP showed "$150M"; we show no figure. If a number is wanted later, it stays "[NUMBER] UNCHECKED" until sourced.
- "[ 14:02 ]" style timecode dropped; not needed.

---

## Script 3: "Frame one" (ATN-type manifesto)

Length 15.5 s = 465 f (f0 to f464). Drop and turn at **f158 = 5.27 s = 34.0%**.

### Core message
You get about one second before a swipe; a logo reveal does not stop anyone; a feeling does, and it must land in frame one. "One second" is a rhetorical frame, UNCHECKED as a fact.

### Cards (exact words, frames at 30 fps)
| # | Words (exact) | In | Out | Dur | Words | Role | Text motion | Size |
|---|---|---|---|---|---|---|---|---|
| 1 | "you" / "get" / "one" / "second." | f2, f6, f12, f18 | f29 | 0.93 s | 4 | Claim | Word-by-word add every 4 to 6 f; dim and blink f25 to f29 | 3.5%, wide gaps |
| 2 | "Don't waste it." | f30 | f66 | 1.23 s | 3 | Warning | 3 f blur-in | 3.5% |
| (gap) | none | f67 | f126 | 2.00 s | 0 | Picture carries the swipe | none | |
| 3 | "Swiped." | f127 | f157 | 1.03 s | 1 | Problem | Right-to-left reveal over 4 f (f127 to f130) | 7.8% |
| 4 | "Feeling" | f158 | f184 | 0.90 s | 1 | TURN, on the drop | Hard cut | 3.5% |
| 5 | "logos don't" / "stop thumbs." | f185 | f220 | 1.20 s | 4 | Old belief | Hard cut; split across width | 3.0% |
| 6 | "Feeling does" | f221 | f250 | 1.00 s | 2 | THESIS, part 1 | Hard cut; 1 px selection box with handles | 10% |
| 7 | "in frame one." | f251 | f283 | 1.10 s | 3 | THESIS, part 2 | 3 f blur-in | 4.6% |
| (black) | none | f284 | f314 | 1.03 s | 0 | Breath | Hard cut to black | |
| 8 | "[STUDIO]" | f315 | f394 | 2.67 s | 1 | End mark | No fade in; hold f315 to f370 (56 f); fade out f371 to f394 (24 f) | 3.0% |
| (tail) | none | f395 | f464 | 2.33 s | 0 | Black tail | | |
On-screen words: 4 + 3 + 1 + 1 + 4 + 2 + 3 + 1 = **19**.

### Shot-by-shot plan (30 fps, 465 f)
| Shot | Frames | Len | Picture | Text | Effect | Sound hit |
|---|---|---|---|---|---|---|
| 1 to 9 | f0 to f29 | 4,3,3,3,4,3,3,3,4 f | Burst: 9 fictional logo stings (our own made-up marks), each caught mid-reveal (flare, spin, shine, 3D extrude) | card 1 adds | Hard cuts on f0, f4, f7, f10, f13, f17, f20, f23, f26 | Tick per cut |
| 10 | f30 to f66 | 37 f | One fictional logo sting playing slowly, a loading ring beside it | "Don't waste it." | Glitch insert f44 to f52 (9 f, 1.47 to 1.73 s), band shifts | Crunch f44 |
| 11 | f67 to f126 | 60 f | Fictional phone feed scrolls up; at f110 a thumb (our own hand shot) swipes the logo post away; posts blur past | none | Vertical motion blur | Whoosh f67; swipe hit f110 |
| 12 | f127 to f157 | 31 f | Feed darkens to black | "Swiped." | Right-to-left reveal | Riser f127 to f157 |
| 13 | f158 to f184 | 27 f | Macro of an eye's pupil widening (our own shoot, released talent) | "Feeling" | Hard cut | **DROP f158 (5.27 s)** |
| 14 | f185 to f196 | 12 f | Cut-out thumb, frozen above a screen | "logos don't" / "stop thumbs." | Hard cut | Bass hit f185 |
| 15 | f197 to f217 | 21 f | Second burst: thumb cut-out stays put; 7 backgrounds swap every 3 f | same | Swap f197, f200, f203, f206, f209, f212, f215 | Ticks; bass hit f209 |
| 16 | f218 to f220 | 3 f | Thumb alone on dark grey | same | Hard cut | none |
| 17 | f221 to f250 | 30 f | Single frame of warm light on skin, out of focus | "Feeling does" in box | Selection box | Bass hit f221 |
| 18 | f251 to f283 | 33 f | Fictional timeline, playhead parked on frame 1, a timecode reading 00:00:00:01 | "in frame one." | Playhead blink every 6 f | Hit f251 |
| 19 | f284 to f314 | 31 f | Black | none | Hard cut | Music cuts f284 |
| 20 | f315 to f394 | 80 f | Black | "[STUDIO]" | No fade in, 24 f fade out | Soft hit f315 |
| 21 | f395 to f464 | 70 f | Black | none | none | Silence by f464 |
Shot count 21. Shots of 4 f or less: 10 (48%).

### Assets needed (script 3)
1. 9 fictional logo stings, our own marks (burst, shot 10). Nothing that resembles a real brand.
2. Fictional phone feed UI and posts (shot 11); own hand footage for the swipe and thumb cut-out (alpha).
3. Eye macro (shot 13): own shoot with a signed release, or licensed stock. Licence UNCHECKED.
4. 7 background textures (shot 15); warm light plate (shot 17).
5. Fictional editing timeline UI (shot 18).
6. "[STUDIO]" mark; Inter font.
7. Music with drop at 5.27 s; ticks, crunch, whoosh, swipe hit, riser, 4 bass hits. Licence UNCHECKED.

### Facts and numbers in script 3
- "you get one second": rhetorical, UNCHECKED. Do not back it with any attention-span statistic.
- No other facts.

---

## Which to make first (judged, not tested)
Script 1 is the closest copy of the ATN grid and the safest pilot. Script 3 uses the burst as the argument itself (logo stings that waste the first second). Script 2 needs the most assets (product UI, VO, team photos).

## Must not say or show (all scripts)
1. No real third-party logos, names, UI or app looks: not Apple, Meta, Whop, Wise, Figma, Adobe, ChatGPT or any other, not even as parody or blurred.
2. No ATN lines, verbatim or near: "a great prduct", "Isn't enough anymore.", "It gets ignored.", "attention isn't earned by features.", "It's earned by perception."
3. No WHP lines: "This is where the internet gets paid.", "Every business. One checkout.", "Whop.com", "ownership" with phonetics in the same layout as a direct copy.
4. No "dhruv", no "@_dhruvxr", nothing that implies the creator made, endorsed or approved this.
5. No invented numbers: no "$150M", "10x", "users", "teams trust us", percentages, or ranking claims ("first", "only", "best", "#1").
6. No attention-span statistics (for example the "goldfish" figure); they are disputed and UNCHECKED.
7. No quotes attributed to real people.
8. No sampled voice lines from films, songs or creators (ATN's opening sample source is unknown); own voice only.
9. No real MRI or medical scans (both references use one) unless licensed with a source note.
10. No real faces without a signed release; no voice clones of real people.
11. No claims about AI products or companies by name ("[X] can't make taste"); scripts 1 and 3 stay opinion.
12. No em dashes in on-screen copy; sentence case only, as in the references.

## Not checked
- No timing was rendered or played; all frame numbers are planned from STUDY.md.
- Licences for music, font, stock and the phonetic spelling are UNCHECKED.
- Readability of 3% type at 1080p on a phone in X is judged, not tested.
