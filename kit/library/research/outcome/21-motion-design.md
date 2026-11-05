# 21 Motion design playbook: faceless data and sports shorts (13 Oct 2026)

Goal: every 1080x1920 video (8 to 30 s) is understood by a stranger in 2 seconds, and no two formats look alike. Written for the Outcome studio (`C:\VISION\VISION CLAUDE\outcome\studio`: `window.renderAt(t)`, GSAP timelines in `templates/motion.html`, headless Chrome screenshots piped into ffmpeg). Frame numbers assume 30 fps (1 frame = 33 ms).

Evidence tags: **VERIFIED** = read this session (sources in section 9). **VENDOR** = a tool maker's claim with no method. **DERIVED** = my reasoning from the sources, not a measured result. **UNVERIFIED** = could not confirm; treat as a guess.

**If you only change three things:** (1) frame 0 shows the subject and the number, not a title on black; (2) every format gets its own signature move and look, so two posts never match; (3) sound is generated from the same timeline (whoosh, riser, hit, tick) instead of shipping silent files.

## 0. What is wrong with the current videos (from reading the code, not from watching the renders)

Read from `templates/motion.html` (saved 13 Oct 17:25), `studio.html` and `render.py`:
1. **One skin.** Every motion format uses the same near-black background with two soft glows, one lime accent, one display font (Anton), the same pill plus headline top-left, the same source line at the bottom.
2. **One set of verbs.** Every headline is "words rise 50 to 60 px, 0.07 to 0.09 s apart, power3.out". Every reveal is "quick white flash, rows slide in 0.1 s apart, bars fill with power2.out". One verb repeated reads as one video.
3. **Frame 0 is words, not the subject.** The `timed` format shows only a pill and the question for the first 1.4 s; the first real number lands at 4.5 s. `wheel` shows its first number at 7.3 s. (`clipbanner` is the good one: banner and number are up by 0.3 s.)
4. **Chips are weak identifiers.** Colour chips with 3-letter codes (CITY, PSG) are slower to recognise than crests or faces. Rights decide what is allowed (see 4.1 risk note); chips stay as the safe fallback.
5. **Source line sits 300 px from the bottom edge**, which is inside the app's caption and music-bar zone on many layouts (estimates run 250 to 420 px, section 1.9). Raise it.
6. **Videos are silent.** `video()` muxes no audio unless a file is passed, so every sound rule below needs the cue sheet in 5.4.

The fix is: the rules in section 0.1, a signature move per format (4.6), a rotating "look kit" (4.7), and sound generated from the same timeline (5.4).

## 0.1 The rules (print this page)

**Clarity**
1. **2-second test.** Freeze frame 0 and frame 60. A stranger must be able to name the subject, the number or question, and why it matters. If not, redo the opening. (TikTok: hook within 6 s, proposition within 3 s.)
2. **Frame 0 shows the subject:** crests or faces, the hero number, or a chart already half drawn. Never a blank or text-only frame. Frame 0 is also the cover image.
3. **One idea per scene,** 2 to 4 s (60 to 120 frames) each, at most 4 things on screen (working memory holds about four chunks).
4. **Label on the data.** Team name and crest at the end of the line or bar, no legends, a unit on every number ("%", "chance", "in 8 days").
5. **Hero number:** the biggest thing on screen, font size at least 150 px (about 8% of the 1920 height), tabular figures, held still for at least 15 frames (0.5 s) after the last digit lands.
6. **Cause, then effect, back to back.** The number reacts within 1 to 2 frames of the event, never later than 3. (Lab work on perceived causation falls off after roughly 50 to 70 ms; DERIVED.)
7. **Before and after in the same spot.** The old value sits where the new value lands. Show the change as its own chip ("+17 pts").
8. **Text hold:** seconds = max(1.0, 0.4 + 0.33 x words). Headline at most 7 words, at most 42 characters per line, at most 2 lines. Text is still for 0.5 s after it stops moving.
9. **Safe area:** everything that matters inside x 60 to 960, y 210 to 1480. Top 210 px, bottom 440 px and right 120 px belong to the app (third-party estimates; check on a phone).
10. **Muted test.** The video must make sense with sound off; the on-screen text is the caption.
11. **Contrast:** text over footage always gets a dark plate or gradient (WCAG 4.5 to 1 for small text). Small titles over bright sky need the plate and a bigger size.

**Motion**
12. **Time grid (frames):** tiny 4 to 6, normal 8 to 12, big 15 to 20, reveal 24 to 36. Ease-out for things arriving, ease-in for things leaving, ease-in-out for A-to-B moves. Overshoot only on badges, stamps and numbers.
13. **One signature move plus two support moves per video.** Rotate entrance verbs by format; never the same entrance on two scenes in a row.
14. **Impact = flash 2 to 3 frames + shake 8 to 12 frames (decaying) + punch scale 105 to 112% in 4 to 6 frames + sound hit, all on the same frame.** At most 2 per video, and never more than 3 flashes in any one second.
15. **Counters** take 24 to 36 frames (power2.out or expo.out), integers only, with ticks. **Chart lines** draw at constant speed with a moving head and a live value label; slow time around the event.
16. **Camera:** every static scene gets a slow push-in (100 to 106% over the scene) or a parallax drift. Transitions are 10-frame whip pans (5 + 5) or hard cuts on the beat. No fades except into the end card.
17. **Never ask people to read something that is still moving:** in 8 to 12 frames, hold, out in 6 to 8.

**Sound**
18. **Every hard visual beat has a sound on the same frame or 1 frame late, never early:** whoosh peak on the cut, hit on the first readable frame of the number, tick on each count or countdown second, riser that stops dead 2 to 4 frames before the hit.
19. **Master near -14 LUFS integrated, true peak -1 dBTP or lower** (a convention, no platform publishes a number). SFX hits peak near -3 dBFS; music bed 6 to 10 dB under the hits (starting point; DERIVED).
20. **Pick music whose beat is a whole number of frames** (90, 100, 120, 150 BPM = 20, 18, 15, 12 frames) and land reveals on bar lines.

**Pipeline**
21. **Every frame is a pure function of t** (`renderAt`). Test: render frame 45, then 20, then 45 again; the two frame-45 images must be identical.
22. **The timeline emits the cue sheet** (sound name + time), so picture and sound cannot drift.
23. **Release check on a phone:** 2-second test, muted test, squint test (blur 6 px: is the hero number still first?), and 3 strangers who have not seen the post.

## 1. What makes a data or sports short instantly understandable

### 1.1 The 2-second budget
- **TikTok's own ad guidance** (read 13 Oct 2026): hook "in the first 6 seconds", content proposition "in the first 3 seconds", use sound or music, 9:16, at least 720p, stay inside the UI safe zone, and text overlays at "5-10 words per second". That last figure is a density ceiling; adults read silent non-fiction at about 4 words per second (see 1.7), so do not use it as a reading time. **VERIFIED**
- **TikTok and CreatorIQ report** (Adweek, 6 Dec 2023): showing a person in the first 2 seconds raised hooking power 50% and ad recognition 32%; 90% of ad-recall impact and 80% of awareness impact come in the first 6 seconds. Creator-ad data, sample size not on the page. **VERIFIED (article), applied by analogy: DERIVED**
- **Hook benchmarks are VENDOR numbers:** average video-ad hook rate 25 to 30%, top 40 to 50% (Nestscale quoting Motion); "about 90% of weak TikToks fail in the first 3 seconds" (OpusClip's 34,635-video sample, quoted by Lemonlight). Use as direction only.
- **YouTube Shorts:** "Stayed to watch" (viewed versus swiped away) is the gate before the retention curve. The claim that people decide in under a second is blog opinion, not a YouTube figure. **VENDOR**
- **What we do with it:** subject and number visible by frame 0, headline finished by frame 30 (1 s), proposition (the claim plus why it matters) by frame 90 (3 s).

### 1.2 One idea per scene
- Working memory holds about four chunks, not seven (Cowan 2001; later work argues 3 to 5). So a scene may show at most 4 things: subject, number, label, one chip. **VERIFIED (abstract level)**
- Mayer's multimedia principles agree: remove extras (coherence), highlight what matters with colour, arrows or size (signaling), and cut long material into short segments (segmenting). Tested on lessons, not on short video. **VERIFIED, applied: DERIVED**
- Scene budget: 8 s = 3 scenes, 15 s = 5, 30 s = 8 to 9. Something new moves at least every 15 frames, something new appears every 2 to 4 s. **DERIVED**
- A scene is "one subject + one number + one verb" ("City 62%, up 9 points").

### 1.3 Labels on the data
- Eye-tracking and timing studies find labelled lines read faster than lines with a legend (Shah and colleagues, experiment 1). A follow-up memory test favoured legends (23% accuracy edge, conference abstract only). So: direct labels for the 2 to 4 series we show; a legend only for dense charts. **VERIFIED (thin evidence)**
- Practitioner guidance matches (Flourish: direct labels for 3 to 7 series; EU Data Visualisation Guide; Evergreen; Wilke).
- Our rule: label sits at the head of the line or end of the bar and moves with it; units always; no axis ticks unless the axis is the story.

### 1.4 Big numbers
- No published test of count-ups versus static numbers exists (searched; our file 14 says the same). Nearest evidence is the general "clear text plus motion in the first 2 seconds" lift quoted by vendors (up to 50% in 3-second retention, **VENDOR**). Test it (section 7).
- Size on a 1080x1920 canvas: hero number font size 150 to 260 px; support numbers 70 to 100 px; labels 44 to 60 px; nothing readable under 36 px. Use tabular figures (`font-variant-numeric: tabular-nums`, already in `.num`) so digits do not jiggle while counting.
- The number must be the first thing the eye lands on after the subject: biggest, highest contrast, one colour accent.

### 1.5 Cause then effect, before then after
- Sequence is meaning: viewers read "this, then that" as cause and effect. The classic lab result (Michotte's launching effect) says the impression of one thing causing another needs the second movement to follow within about 40 to 70 ms; by about 1 second it is gone. 1 to 2 frames at 30 fps is 33 to 67 ms. Apply to goal -> chance jump, news -> price jump. **VERIFIED (course notes and review), applied to screens: DERIVED**
- Before/after: keep both numbers in one place (old dims to 50% and slides left 30 px, new lands centre with the delta chip). The eye stays still and the only thing that moves is the change.
- Cause first: show the event for at least 12 frames before the number moves, otherwise the viewer cannot tell what the number is reacting to.

### 1.6 Faces and teams first
- TikTok/CreatorIQ (1.1): a person in the first 2 s lifts hooking power. For faceless pages the equivalents are a player portrait or a club crest in the first 6 frames, then the question. **DERIVED**
- Rights note: crests and portraits are trademarks and likenesses. The studio ships colour + code chips (146 clubs) and 'players.json'. Clear what you use; fall back to chips.
- Put the two subjects of a comparison at equal size in equal slots (left/right or top/bottom) so the number is the only difference.

### 1.7 Reading speed and how long text stays
- Adults read silent non-fiction at 238 words per minute (fiction 260); most adults fall in 175 to 300; readers with English as a second language are slower. That is about 4 words per second at best (Brysbaert 2019, 190 studies, 18,573 readers). **VERIFIED**
- Subtitles: Netflix's English style guide caps adult programmes at 20 characters per second and 42 characters per line (read 13 Oct 2026). Its minimum on-screen time is about 5/6 s (20 frames at 24 fps) and maximum 7 s (from memory of the timing article, not re-read: UNVERIFIED). Caption guidance quotes 130 to 180 words per minute.
- Our formula (DERIVED): **hold = max(1.0 s, 0.4 s + 0.33 s x words)**, counted from the frame the text stops moving. It is about 180 words per minute plus 0.4 s for the eye to find the text.

| Words on screen | Hold (s) | Frames at 30 fps | Example |
|---|---|---|---|
| 1 to 2 | 1.0 | 30 | "81%" or "CITY 62%" |
| 3 | 1.4 | 42 | "Chance to win" |
| 5 | 2.1 | 63 | "Man City or PSG: who?" |
| 7 | 2.7 | 81 | headline maximum |
| 10 | 3.7 | 111 | avoid; split into two scenes |

- A changing number needs 0.8 to 1.0 s of stillness after it lands (24 to 30 frames) plus the 0.5 s rule in rule 8 if a word is attached.
- Never leave the viewer with two things to read at once: stagger them by at least 12 frames, or merge them.

### 1.8 Captions and subtitles
- Captions raise completion: 80% of 5,616 US adults said they were more likely to watch a video to the end with captions (Verizon Media / Publicis Media, 2019, via a secondary page); Facebook reported about 12% more view time (2016, secondary). **VERIFIED as secondary**
- Animated word-by-word captions: vendors claim 18 to 28% retention lifts; no independent study isolates them. **VENDOR.** Sources agree on the format: 1 to 4 words at a time, active word in the accent colour, only the key word enlarged. Run the A/B test in section 7.
- For faceless data videos the on-screen text already is the caption. Burn separate captions only when there is a voiceover (shot list 4.4).
- Keep captions in y 1180 to 1420 (above the app's caption block), 70 to 90 px bold with a dark stroke or plate.

### 1.9 Safe areas and legibility
- No platform publishes an official safe-zone; every guide differs. The consensus box for 1080x1920: central 900x1400, top 100 to 210 px blocked (search/profile bar), bottom 250 to 420 px blocked (caption, music, buttons), right 84 to 120 px blocked (like/comment/share rail). Remotion's safe-zone tool measured TikTok's rail starting at x=949 and Instagram's at x=927. **VERIFIED as third-party; check on a phone**
- Instagram's profile grid shows a centre 3:4 crop (our file 14); one guide says feed previews crop to 4:5 (UNVERIFIED). Frame 0, the cover, must survive a centre crop.
- Our box: x 60 to 960, y 210 to 1480. Decorative things may bleed; anything read must be inside.

### 1.10 Gaps (honest list)
No controlled test found for: count-ups, progress bars, countdown overlays, animated versus static captions, or hold times in finance and sports shorts. No official TikTok or Instagram loudness number or safe-zone spec exists. Section 7 has the tests that fill these gaps with our own posts.

## 2. Motion techniques that hold viewers (30 fps)

### 2.1 Timing and easing cheat sheet
Frames to seconds: 4 = 0.13 s, 6 = 0.2 s, 8 = 0.27 s, 10 = 0.33 s, 12 = 0.4 s, 15 = 0.5 s, 18 = 0.6 s, 24 = 0.8 s, 30 = 1.0 s, 36 = 1.2 s.

Interface-animation guides put the useful range at about 200 to 500 ms (under 100 ms is invisible), arrivals ease-out, exits ease-in, bigger or longer moves need more time (secondary UX guides; the Nielsen Norman article itself would not load: **VENDOR**). A video viewer cannot pause, so we use 8 to 12 frames (270 to 400 ms) for normal moves and 4 to 6 for small feedback.

| GSAP ease | Looks like | Approx CSS cubic-bezier | Use |
|---|---|---|---|
| power2.out | easeOutCubic | 0.33, 1, 0.68, 1 | default arrival |
| power3.out | easeOutQuart | 0.25, 1, 0.5, 1 | headlines, panels |
| power4.out | easeOutQuint | 0.22, 1, 0.36, 1 | wheel spin, long deceleration |
| expo.out | easeOutExpo | 0.16, 1, 0.3, 1 | counters, big settles |
| power2.in | easeInCubic | 0.32, 0, 0.67, 0 | exits |
| power2.inOut | easeInOutCubic | 0.65, 0, 0.35, 1 | A-to-B moves |
| expo.inOut | easeInOutExpo | 0.87, 0, 0.13, 1 | whip pans, map flights |
| sine.inOut | easeInOutSine | 0.37, 0, 0.63, 1 | slow camera drifts |
| back.out(1.7) | easeOutBack | 0.34, 1.56, 0.64, 1 | badges, stamps (about 10% overshoot) |
| none | linear | n/a | chart heads, progress, rings |

The CSS values are approximate and from memory of easings.net (UNVERIFIED this session); GSAP's names are the source of truth. In After Effects, Easy Ease is 33% influence on both sides; for an ease-out set the last key's incoming influence to 70 to 85% with speed 0, for an ease-in set the first key's outgoing influence to 70 to 85% (rule of thumb, DERIVED). To port an AE curve into GSAP use `CustomEase.create("name", "M0,0 C0.2,0 0,1 1,1")`.

### 2.2 The techniques at a glance

| # | Technique | Use when | Frames | Easing |
|---|---|---|---|---|
| 1 | Kinetic type | the claim or question, 3 to 7 words, one per scene | word in 9, stagger 2 to 3, key-word pop 6, out 6 | power3.out; back.out(1.7) on the key word |
| 2 | Number counter | the hero % or $ | count 24 to 36, delta chip 12, hold 15+ | power2.out or expo.out |
| 3 | Line reveal with moving head | any chance or price history | 90 to 360 (3 to 12 s), slow-mo into the event 12 | none; power2.out on the slow-mo |
| 4 | Punch-in | key word, number landing, impact | in 4 to 6, settle 6 to 10, 105 to 112% | power2.out then power2.inOut |
| 5 | Push-in and parallax | every static scene | 60 to 120, 100 to 106% | none or sine.inOut |
| 6 | Whip pan | scene change inside one format | 10 (5 before the cut, 5 after) | expo.inOut |
| 7 | Match cut | carry a shape between scenes | 0 to 2 frame tolerance | n/a |
| 8 | Speed ramp (footage) | the second before an event | down 8, slow hold 12 to 24, up 12 | sine.inOut or bezier |
| 9 | Flash and shake | the reveal, the goal | flash 2 to 3, shake 8 to 12 | linear flash; CustomWiggle easeOut |
| 10 | Split screen | A vs B, before vs after | divider 8 to 10, halves count 24 to 36, winner pop 8 | power3.out; back.out(2) on "VS" |
| 11 | Progress bar | videos over 10 s (test first) | whole length | none |
| 12 | Timer and countdown | guess-the-% and settle-time hooks | 3 s = 90, digit slam 8 | power3.out digits; ring linear |
| 13 | "3D" type and bars | the winner moment, once per video | bars rise 18 to 24, stagger 3; orbit plus or minus 8 degrees over 60 to 90 | power3.out; back.out(1.4) |
| 14 | Map zoom | geography stories | world to region 24 to 36, markers pop 6 | expoScale with power2.inOut |
| 15 | Glitch and scanlines | breaking, upset, crypto, Fed only | 4 to 8 per burst | steps or none |
| 16 | Word-by-word captions | voiceover videos | group of 2 to 4 words, 8 to 15 per group, pop 4 | power2.out; back.out(1.4) |
| 17 | Bar chart race | title or ranking history | 8 to 12 per day step, rank swap 10 | power2.inOut |
| 18 | Wheel spin | picks, giveaways | 3.5 to 4.5 s (105 to 135), 5 to 6 turns | power4.out |

### 2.3 Build notes and proof, technique by technique
Numbers in "Proof" come from our earlier reports (files 11, 12, 16, 18, read 13 Oct 2026) or from the live TikTok page reads of 13 Oct 2026. "None found" means I searched and found no public numbers.

**1. Kinetic type.** SplitText (free since GSAP 3.13) with `type:'words', mask:'words'`, then `from(words, {yPercent:110, duration:9/30, stagger:2/30, ease:'power3.out'})`. Change the verb per format: mask-rise, scale-slam (1.8 -> 1 in 7 frames), TextPlugin typewriter, ScrambleText decode for BREAKING, slide from the side. Colour one word, two at most. Proof: none found; TikTok recommends text overlays (1.1).

**2. Counters.** Tween an object `{v}` and write `textContent` in the per-frame draw function (the `counter()` + `TICKS` pattern in motion.html is right). Integers; "<1%" under 0.5 (`pct()` does this). For a change, count from the old value ("54 -> 71"), not from zero. Tick sound on each tens-digit change. Proof: none found (file 14 s3.5); run test T1.

**3. Line reveal with a moving head.** Clip rect (as `#rv` in `clipbanner`) or DrawSVG. Head dot r = 12 px, pulse 1 -> 1.6 scale and 60% -> 0 opacity every 20 frames; the value label rides the head. Use the real clock on the x axis so the goal lands where it happened. Event pin: vertical hairline plus a 6-frame label pop. Slow time: map video time to data time with a curve that drops to 40% speed for 12 frames before the event, holds 6 frames on it, then resumes. Proof: clips with a live odds-line banner: DoomScroll Rankings Short 8.48M views (26.8K subs), Polymarketupdates Short 8.33M views (15.3K subs).

**4. Punch-in.** Scale the content wrapper around the subject (set `transformOrigin` on the number or face, not the centre): 100 -> 108% in 5 frames (power2.out), back to 103% over 8. Pair with a hit on the same frame. No more than one punch per 2 s or it reads as shaking. Proof: none found.

**5. Push-in and parallax.** Three layers (background, subject, foreground texture) travel 0.25x, 0.6x and 1.0x of the camera move (plus or minus 40 px over 90 frames), scale ratios 1.00 / 1.04 / 1.08, background blur 3 to 4 px, ease sine.inOut. House rule from the editor: no breathing or sway on photo cutouts (reads as AI); use parallax, pose swaps and cuts. The linear 1.0 -> 1.08 push in `pnl_edit` is correct. Proof: none found.

**6. Whip pan and match cut.** Whip pan = 10 frames, keyframes 5 before the cut and 5 after, eased, blur peaking at the cut (Creative Cow and Photofocus tutorials; a Premiere version runs 5 before to 10 after with a 90 degree directional blur, length 250: tutvid). In HTML: outgoing scene slides to -100% width, incoming from +100%, with an SVG filter `<feGaussianBlur stdDeviation="40 0">` ramped up and down. True motion blur: render these 10 frames at 4 sub-frames each and blend with ffmpeg `tmix=frames=4` (4x cost, only 10 frames). Match cut: match position, size and shape within 2 frames and 10 px (ring -> wheel rim, bar end -> line head). Proof: none found.

**7. Speed ramp.** In the clip-sequence player, replace `src = offset + t*speed` with the running integral of a speed curve (precompute one value per output frame). Goal ramp at 30 fps: 100% -> 25 to 35% over 8 frames, hold 12 to 24 frames, back to 100% over 12. One unofficial skill page gives the same shape (ease to 25% over frames 20 to 28, impact at 28, back up by 40). Use Bezier easing, not linear (Motion Array). Source frames must be 60 fps or interpolated (`minterpolate`) or slow-mo will stutter. Proof: none found.

**8. Flash and shake.** Flash 2 to 3 frames at 70 to 90% white (motion.html rises in 0.05 s and fades over 0.3 s, about 9 frames: fine for a soft reveal; for a hard hit use 1 frame at full white, then fade over 2 to 3 frames). Shake 8 to 12 frames, amplitude 14 to 24 px, decaying, mostly vertical for hits; scale the wrapper to 103 to 106% during the shake so the edges never show. Game-feel craft: Nijman's "art of screenshake" (camera kick 6 px, shake +4 decaying quickly) and Jonasson and Purho's "Juice it or lose it" (2012). No retention numbers exist. Safety: at most 3 flashes in any second (WCAG 2.3.1, known standard, not re-read); one 3-frame flash per impact is safe.

**9. Split screens.** Stack top/bottom (each half 960 px tall) or left/right. Divider wipes from the centre in 8 to 10 frames; "VS" badge scale-slams (back.out(2)) at frame 6; both halves count at once (stagger 4 frames). At the reveal the winner scales 104% in full colour, the loser dims to 60%. Proof: pick-a-side polls 3.8M to 7.5M plays with 2.3% to 8.2% shares (file 18, L2); "YAMAL > RONALDO" 2.81M views, 192.8K shares on a 78K page (file 12).

**10. Progress bar.** 6 to 8 px bar at y 190 (just under the top block), linear over the full length, accent colour. Vendors sell fake "dummy" bars; a real one is honest. YouTube's own progress bar is only a resume marker. No test exists: run T5.

**11. Timer and countdown.** Digit slam 1.5 -> 1 in 8 frames (power3.out), ring `stroke-dashoffset` linear over 90 frames, tick on the first frame of each second, double-time ticks in the last second, riser under the last 1.5 s, flash and reveal at zero. Three seconds maximum. Proof: @spot.the.differan (3,629 followers) 4.5M plays on a 12 s timed clip; @guess.the.flag08 (17.4K) 2.2M plays.

**12. "3D" type and bars.** Three cheap, deterministic options. (a) Extruded text: 12 to 24 stacked `text-shadow` layers stepping 1 px down-right in a darker shade. (b) Isometric bars: CSS `rotateX(55deg) rotateZ(-35deg)` on a three-face box (top light, side dark), animate `scaleY` from the base. (c) Real 3D: Three.js `TextGeometry` with a bevel inside the same page, camera orbit driven by `renderAt(t)`. Winner only; everything else stays flat. Proof: none found.

**13. Map zoom.** d3-geo + TopoJSON in SVG (d3 7.9.0, ISC) with the scale animated through `expoScale`; or MapLibre GL JS (6.14.0 on 11 Oct 2026, BSD-3) with `map.jumpTo` per frame and a wait for the `idle` event before each screenshot (slower, needs tiles, UNVERIFIED in our pipeline). Zoom in log space. Proof: @geo.all.day (244.9K followers) 10.5M plays and 4.0% shares; @geotok (58.1K) 8.3M plays.

**14. Glitch and scanlines.** RGB split = three copies with `mix-blend-mode:screen` offset 4 to 8 px for 2 to 4 frames; slice shifts = 3 to 6 horizontal strips moved plus or minus 20 to 60 px from a seeded random per frame; scanlines = `repeating-linear-gradient(0deg, rgba(0,0,0,.18) 0 2px, transparent 2px 4px)` at 25% opacity. ffmpeg alternatives: `rgbashift=rh=-6:bh=6`, `noise=alls=20:allf=t`. A 4 to 8 frame burst as a transition for BREAKING, upsets, crypto and the Fed; constantly on it looks cheap. Seeded random only. Proof: none found.

**15. Word-by-word captions.** SplitText on the caption line; groups follow word timestamps (Whisper gives word times); each group 8 to 15 frames; active word in the accent colour and scale 1.0 -> 1.12 in 4 frames; place the group 2 frames before the spoken word; y 1180 to 1420. Proof: general caption data in 1.8; animated lifts are vendor claims.

**16. Bar chart race.** One div per bar at `y = rank * rowHeight`; interpolate rank between day steps (power2.inOut) so swaps glide; 8 to 12 frames per day (30 days = 8 to 12 s); crest and live % at the bar end; open on the final ranking for 1 s, end on a 1.5 s hold (file 16 advice). Proof: @hai02a (112.6K followers) 18.8M plays; @zain02a (4.4K) 2.2M; @hai08a "Most valuable players 2004 to 2026" 307K views on 13.6K followers. Strong as a longer TikTok, weak as a Short (file 16).

**17. Wheel spin.** SVG wheel, rotation = 5 to 6 turns + landing angle over 4.2 s with power4.out (as `F.wheel` does). Pointer flick and a tick each time `floor(angle / segmentAngle)` changes; the gap grows from 2 to about 12 frames; the last two pegs creep. Landing: stamp scale 2.2 -> 1 in 10 frames, rotate -8 -> 0, hit and an 8-frame shake. Keep it honest: pick the landing segment with a seeded random draw logged in the batch JSON; otherwise the spin is staged. Wording "the wheel says", never "pick" or "tip". Proof: client's UGC format; no verified numbers in our files.

## 3. Sound design for faceless data videos

### 3.1 Why bother
Sound is on for most viewing. TikTok-sourced figures: 88% of viewing with sound on and 93% of top videos using audio (secondhand and older: **UNVERIFIED**); Reels audio is on for over 80% of plays (our file 10); TikTok lists "sound/music" among its basics (**VERIFIED**). Silent text video is the weak option. Our current files are silent, so this is the largest gap.

### 3.2 Cue map: what plays when

| Visual beat | Sound | Length | Placement | Level vs the hit |
|---|---|---|---|---|
| Whip pan, scene change | whoosh | same as the move (6 to 12 frames) | loudest point on the cut frame, so start the file 3 to 6 frames earlier | -4 dB |
| Build to a reveal | riser (noise sweep or pitched) | 24 to 60 frames (1 to 2 s) | ends 2 to 4 frames before the hit; the silence is part of the effect | -6 dB, rising |
| Number lands, goal, reveal | hit (short tail) plus optional sub drop | hit 10 to 30 frames, tail 0.5 to 1.2 s | first readable frame (the flash frame), never early | 0 dB (peak -3 dBFS) |
| Counter running | ticks | 2 to 4 frames each | every tens-digit change or every 3 frames; pitch up 2 to 3 semitones across the count | -14 dB |
| Countdown 3-2-1 | clock tick, double-time in the last second | 5 frames | first frame of each second | -10 dB |
| Label or badge pops | soft pop | 3 to 6 frames | frame the scale-up starts | -12 dB |
| Stamp, VS slam | thud plus short metallic | 8 to 12 frames | landing frame | -2 dB |
| Wheel | peg ticks, final bass hit | 2 frames | each peg crossing, spacing grows | -12 dB; last tick -6 |
| Glitch | digital burst | 4 to 8 frames | with the visual burst | -8 dB |
| UI tap (app demo) | soft click | 3 frames | frame the ring appears | -14 dB |
| Loop point | cut the music tail dead | n/a | last frame | n/a |

- **Sync rule (DERIVED):** sound early looks wrong sooner than sound late. The broadcast standard (ITU-R BT.1359-1, from memory, **UNVERIFIED this session**) puts the noticeable limit at roughly 45 ms for sound ahead of picture and 125 ms for sound behind. So a hit goes on the frame or 1 frame (33 ms) late, never 1 frame early. Whoosh pre-roll is deliberate because its peak, not its start, meets the cut.
- **Craft rules** (vendor sound-design guides, no frame offsets published): match whoosh length to the move instead of stretching a stock file; a whoosh can resolve into a dull hit so the transition "arrives"; a reverse riser that stops dead leaves a silence that sells the hit; work frame by frame; fewer, well-placed sounds beat many. The 3 to 6 frame pre-roll is DERIVED: store each file's main-transient offset and place `cue time = visual time - offset`.

### 3.3 Levels and loudness
- **No official TikTok or Instagram loudness number exists.** Fora Soft's article of 5 Jun 2026 says none of TikTok, Instagram, Facebook, X or Twitch publishes a target; behaviour clusters near -14 LUFS and is "loose and inconsistent". YouTube's reference is -14 LUFS and it turns loud files down, never up (Wikipedia; Ian Shepherd 2019). One vendor says Instagram and TikTok favour -12 to -10 LUFS (outlier, UNVERIFIED). Another says anything under -16 LUFS is too quiet on phone speakers.
- **Our target: -14 LUFS integrated (accept -16 to -12), true peak -1 dBTP (use -1.5 for AAC headroom), loudness range 6 to 10.** Measure every export with `ebur128`.
- **Relative levels** (DERIVED from vendor guides that put music 15 to 20 dB under speech and about 12 to 14 dB below full scale when there is no voice):
  - No voice: music bed about -20 LUFS short-term on its own (6 dB under the master); hits peak -3 dBFS and read 6 to 10 dB over the bed; whooshes 3 to 5 dB under hits; ticks and pops 10 to 14 dB under hits. If the master lands at -17, raise the bed 2 dB, not the hits.
  - With a voiceover: voice -16 to -14 LUFS, peaks near -6 dBFS; music 15 to 20 dB under the voice while it speaks (sidechain duck, 150 ms attack, 300 to 500 ms release) and back up in gaps; hits 3 to 6 dB under voice peaks; ticks 12 dB under.
- **Silent exports today:** the team adds music in-app. Bake the SFX into the file (they are ours) and keep the music slider low enough that SFX stay clear (start near 25% and check on a phone speaker; slider behaviour UNVERIFIED).
- **Music rights:** TikTok business accounts get only the Commercial Music Library in-app and the general library is personal non-commercial use (file 14, secondhand, 2026 rules UNVERIFIED). Confirm that the Epidemic Sound licence covers paid or per-view promo posts (flagged in file 14).

### 3.4 Cutting on the beat
- Beat length in frames at 30 fps = 1800 / BPM. Whole-frame tempos: 75 BPM = 24, 90 = 20, 100 = 18, 120 = 15, 150 = 12, 180 = 10 frames. 128 BPM = 14.06 frames (drifts a frame every 16 beats): stretch the track to 120, or snap each cut to the nearest beat.
- Hard cuts on beats 1 and 3 (every 1.0 s at 120 BPM); scene changes on bar lines (every 2.0 s at 120 BPM); the big reveal on the downbeat after a riser (4.0 s, 8.0 s at 120 BPM).
- Land the picture 0 to 2 frames after the transient, not before.
- Design lengths in whole bars: 12 s = 6 bars at 120 BPM, 16 s = 8 bars, 24 s = 12 bars.
- If the music is added in-app you do not control where the beat falls: design cut points with SFX only, or bake a licensed loop.

### 3.5 Free sound-effect sources and their licences (read 13 Oct 2026)

| Source | Licence as read | Notes |
|---|---|---|
| Sonniss GDC Game Audio Bundle (2026) | free, 17 vendors, no attribution, unlimited projects, no AI training (2024 note) | best bulk pack; read the live licence before shipping (news post, not the licence text) |
| Pixabay sound effects | Pixabay Content License: free, no attribution, modification allowed, no selling or redistributing the file standalone | the summary does not spell out commercial or ad use: UNVERIFIED, read the full terms |
| Freesound | licence set per sound: CC0, CC-BY (credit), CC-BY-NC (not allowed for us) | filter to CC0 only |
| Kenney audio packs | CC0 | UI clicks, impacts |
| ZapSplat | free tier requires a credit, paid tier removes it | one guide only: UNVERIFIED |
| Mixkit | has a "Sound Effects Free License" but the terms did not load | UNVERIFIED |
| BBC Sound Effects archive | RemArc licence: personal, educational, research | do NOT use for commercial or per-view posts |
| Epidemic Sound (in the workspace) | paid subscription | confirm scope for client and per-view posts |

Build a house pack of about 40 files named by function (whoosh_short, whoosh_long, riser_1s, riser_2s, hit_deep, hit_light, tick_a, tick_b, pop_a, stamp, glitch, wheel_peg, ui_tap ...), trimmed to a stored "hit offset", peak-matched at -3 dBFS, with a licence log (source, URL, date, licence).

## 4. Shot lists for the five video types

How to read: frames at 30 fps (1 s = 30 frames). "f" = frame. Every list obeys section 0.1: subject and number on frame 0, hold times from the formula in 1.7, nothing important outside x 60 to 960 and y 210 to 1480. Sound cues use the names in the cue map (3.2). All numbers on screen come from the market at build time; sample figures below are placeholders, not facts. Risk line, source line and time stamp stay on every video (PLAYBOOK s4 and s5).

### 4.1 (a) Goal clip with a live chance banner: 15 s (450 frames)
- Signature move: freeze, flash and number flip with a delta chip.
- Rights note: a banner over broadcast footage is on the "do not build" list in file 18 (rights and undisclosed-ad risk). Use footage we own or have licensed, or replace the footage layer with an animated pitch (2D pitch, ball along a MotionPath, crest chips). The motion below works for both.
- T = the event time (`event.at` in `clipbanner`). Below T is 3.5 s (f105). All cue times are offsets from T.

| Time (frames) | Picture and text | Motion | Sound |
|---|---|---|---|
| 0.0 to 0.3 s (f0 to 9) | Footage already playing. Banner already up: crest chip, "ARSENAL 54%", flat chart, head dot. Title top: "54% to win. Then a goal." (6 words, hold 2.4 s) | Banner rises 40 px and fades in over 8 f (power3.out); title words mask-rise from f2, stagger 2 f; push-in 100 to 104% runs 0 to 3.5 s | soft UI pop at f3 |
| 0.3 to 3.2 s (f9 to 96) | Build-up. Head moves along the real series at constant speed, value label follows. Minute chip ticks. Title holds f21 to f93 and exits f93 to f99 | head pulse every 20 f; nothing else moves | tension bed fades up from -26 to -20 dB; riser from f60 |
| 3.2 to 3.5 s (f96 to 105) | Ball arrives. | video time slows 100 to 60% from f96 | riser ends f101; silence f101 to f104 |
| 3.5 s (f105) GOAL | Banner number flips 54 -> 71 over 20 f (f105 to 125); delta chip "+17" pops at f109; line steps up over 6 f then runs on; crest pulses 1 -> 1.12 -> 1 over 8 f | flash 3 f; shake 12 f (22 px / 14 px); punch 100 -> 112% in 5 f then settle 105%; footage ramps to 35% over 8 f | HIT at f105 (peak -3 dBFS) plus sub drop 24 f; rising ticks f105 to f125 every 2 f |
| 4.2 to 5.7 s (f125 to 172) | Slow replay of the finish at 35% with a "REPLAY" tag (1 word). Number stays at 71% | ramp back to 100% over f160 to f172 | whoosh peak at f152 (start f146) |
| 5.8 to 9.5 s (f175 to 285) | Result frame: "54% -> 71%" in one spot (old value dims to 50% and slides 30 px left, new value centred at 200 px). Under it "Too high?" (2 words, from f187) | morph 12 f (power3.out); hold 3.7 s | pop f178 |
| 9.5 to 12.5 s (f285 to 375) | Context rows: "Draw 17%", "Spurs 12%" (80 px), time stamp and source line (above y 1480) | rows stagger 3 f, 8 f each; counters 24 f | ticks, pops |
| 12.5 to 14.5 s (f375 to 435) | CTA pill and risk line from brand.json | pill pop 9 f (back.out 1.7) | pop |
| 14.5 to 15.0 s (f435 to 450) | Calm version of frame 0 (54% banner, no title); hard cut f450 -> f0 so it loops | none | music tail cut |
- Proof: clips with a live odds-line banner: 8.48M views (26.8K subs) and 8.33M views (15.3K subs) (file 11).

### 4.2 (b) Countdown reveal "Guess the %": 12 s (360 frames)
- Signature move: ring countdown, riser, flash reveal. The `timed` format already exists; the changes are frame 0 (crests and "?" bars visible, not just a pill) and a shorter question.
- Reveal falls at 5.2 s so about half the video is payoff.

| Time (frames) | Picture and text | Motion | Sound |
|---|---|---|---|
| 0.0 to 0.3 s (f0 to 9) | Frame 0: both crests (300 px) left and right, "?" in empty bars, pill "GUESS THE %" | crests scale 0.6 -> 1 in 8 f (back.out 1.7), already 60% visible at f0; pill pop 8 f | pop f2 |
| 0.3 to 2.1 s (f9 to 64) | Question, 3 words: "City or PSG?" (hold 1.4 s) | words mask-rise, stagger 2 f | none (music from the app) |
| 1.8 to 5.2 s (f54 to 156) | Ring appears (scale 0 -> 1 in 12 f). Digits 3, 2, 1 at f66, f96, f126. Question dims to 35% | digit slam 8 f each (1.5 -> 1, power3.out); ring stroke linear 90 f from f66 | tick at f66, f96, f126; double-time ticks f141 to f156; riser f111 to f152, silence f152 to f155 |
| 5.2 s (f156) REVEAL | Bars fill, counters run to the market's real values (placeholder 44.6 / 23.2 / 32.0); winner in the accent, others at 60% | flash 3 f; ring shrinks to 0.2 and fades in 8 f; bars 30 f, stagger 4 f; small shake 8 f (10 px) | HIT f156; ticks f156 to f186 |
| 5.7 to 6.6 s (f171 to 198) | "THE MONEY SAYS" and delta chips ("24h +6") | slide in 12 f (power3.out); winner pulse 1 -> 1.04 -> 1 over 8 f | pop |
| 6.6 to 9.2 s (f198 to 276) | Hold: numbers still for 2.6 s | none | none |
| 9.0 to 11.1 s (f268 to 332) | Comment bait, asked not ordered: "Did you get it right?" (hold 2.1 s). Source and time stamp | box pop 9 f (back.out 2) | pop |
| 11.1 to 12.0 s (f332 to 360) | Hold; hard cut to frame 0 (crests identical, bars empty) | none | music tail |
- Proof: a 12 s timed-reveal clip got 4.5M plays on a 3,629-follower page; a flag version 2.2M on 17.4K (file 16).

### 4.3 (c) Wheel spin pick: 13 s (390 frames)
- Signature move: peg ticks, a creeping stop, a stamp.
- Integrity: choose the landing segment with a seeded random draw and log the seed in the batch JSON; say "the wheel says", never "pick" or "tip".

| Time (frames) | Picture and text | Motion | Sound |
|---|---|---|---|
| 0.0 to 0.4 s (f0 to 12) | Wheel (8 to 12 segments, crest chips, labels 56 px or more) already visible. Title "Who does the wheel back?" (5 words, hold 2.1 s). Pill "DAY 3" | wheel 85 -> 100% in 12 f (power3.out); title mask-rise f2 to f16 | pop f2 |
| 0.4 to 1.2 s (f12 to 36) | Hold so the segments can be read (24 f) | pointer idle wobble 2 px | none |
| 1.2 to 5.4 s (f36 to 162) | SPIN | rotation = 5 to 6 turns + landing angle over 126 f (power4.out); pointer flick -18 -> 0 in 4 to 6 f on every peg; background push 100 -> 104% | whoosh start f32 (peak f36); peg ticks, gap grows from 2 f to 12 f, level -12 dB rising to -6; soft riser under the last 40 f |
| 5.4 to 5.5 s (f162 to 165) | The last two pegs creep (gaps stretched to 20 f and 30 f) | tail of power4.out; enforce the minimum gap | last tick -6 dB |
| 5.5 s (f165) STAMP | White plate "THE WHEEL SAYS: ARSENAL" | scale 2.2 -> 1 in 10 f (back.out 2), rotate -8 -> 0; shake 8 f (14 px); flash 2 f | HIT f165 plus stamp thud |
| 5.5 to 7.0 s (f165 to 210) | Hold 1.5 s | none | none |
| 7.0 to 7.4 s (f210 to 222) | Wheel and title dim to 15%; money panel slides up | 12 f, power3.out | whoosh start f206 |
| 7.4 to 9.8 s (f222 to 294) | "BUT THE MONEY SAYS": crest, label, % per row. Source and time stamp | counters 30 f, stagger 4 f (power2.out); leader row in the accent | ticks |
| 9.8 to 12.0 s (f294 to 360) | Series hook: "Wheel or money? Results tomorrow." (hold 2.1 s) plus risk line | box pop 9 f | pop |
| 12.0 to 13.0 s (f360 to 390) | Hold; hard cut to frame 0 | none | music tail |

### 4.4 (d) 20-second explainer with voiceover and motion graphics: 20 s (600 frames)
- Signature move: whip pans between five beats plus word-by-word captions.
- Voice: about 150 words per minute (2.5 words per second), 46 words in total: 6 + 10 + 14 + 12 + 4. Start the voice at f6. Captions come from word timestamps (Whisper); groups of 2 to 4 words, 8 to 15 frames each, active word in the accent colour, y 1180 to 1420, placed 2 frames before the spoken word.
- Sample copy below uses placeholder numbers (SAMPLE, not real). Price = chance is Outcome's own mechanic (file 00-status).
- AI-voice labels: file 14 s18 says plain narration is not addressed by TikTok, Meta or YouTube rules, but realistic AI people and sounds are labelled. Re-check before posting.

| Beat and time (frames) | Voice (budget) and picture | Motion | Sound |
|---|---|---|---|
| 1 Hook, 0 to 2.5 s (f0 to 75) | "Fed holds? The money says 81%." (6 words). Frame 0 already shows the event icon and the hero number "81%" at 220 px; headline 4 words | hero counter 0 -> 81 over 30 f from f0; key word pop at f12 on the beat; punch-in 100 -> 108% | soft hit at f0 (-8 dB); music in |
| 2 Context, 2.5 to 7 s (f75 to 210) | "That is the price of a Yes share: 81 cents." (10 words). Left: share card "81c". Right: "= 81% chance". Icons draw on | whip pan into the beat, 10 f (f70 to f80); labels pop 6 f; DrawSVG 18 f | whoosh peak f75; pops on labels |
| 3 Data, 7 to 13 s (f210 to 390) | "A week ago: 62%. Hot inflation data pushed it up nineteen points." (12 words). Line with moving head across 4.5 s; event pin at the cause; delta chip "+19" | line linear; slow time 12 f before the event; small flash 2 f and shake 8 f (10 px); counter 62 -> 81 over 24 f | sparse ticks under the line; riser before the event; hit on it |
| 4 Meaning, 13 to 18 s (f390 to 540) | "If the Fed holds, Yes pays one dollar. If not, nothing." (11 words). Split cards "HOLDS 81%" vs "HIKES 19%" | whip pan 10 f; divider 8 f; counters 24 f; winner card 104% | whoosh, pop, ticks |
| 5 Close, 18 to 20 s (f540 to 600) | "Chance, not certainty." (3 words). End card: source, time stamp, risk line ("Not financial advice"), CTA pill. At f585 return to the frame-0 layout so it loops | pill pop 9 f | music tail; no SFX |

- Mix: voice -16 to -14 LUFS, music ducked 15 to 20 dB while speaking, hits 3 to 6 dB under voice peaks (3.3).

### 4.5 (e) Screen-recording style app demo: 18 s (540 frames)
- Signature move: tap rings and a zoom to the number. This is the `demo` format over real outcome.xyz screens in a phone frame.
- Keep it calm: no flash, no shake, no riser. Never cover prices or the logo. No profit promise. Step captions are copied from the real screens by the capture script (each at most 6 words); nothing invented about the product.

| Time (frames) | Picture and text | Motion | Sound |
|---|---|---|---|
| 0.0 to 1.0 s (f0 to 30) | Phone frame slides up with a real market page already on screen. Step box "1. Open a market" (hold 1.7 s) | phone y +200 -> 0 in 18 f (power3.out); box pop 9 f at f6 (back.out 2) | whoosh start f0 (peak f10); pop f6 |
| 1.0 to 4.0 s (f30 to 120) | Tap ring on the market card, then the screen scrolls to the market | ring 0.4 -> 1.4, opacity 1 -> 0 in 15 f; scroll 40 f (power2.inOut) | soft tap on the ring frame; scroll swish |
| 4.0 to 8.0 s (f120 to 240) | Step box "2. The price is the chance" (hold 2.1 s). Highlight ring around the price; zoom on it | ring back.out(2) in 10 f; zoom 100 -> 130% in 20 f (expoScale), hold 45 f | whoosh start f116; ping on the ring |
| 8.0 to 12.0 s (f240 to 360) | Step box 3 from the real screen. Zoom back out in 18 f; second ring | ring pop 10 f | tap, ping |
| 12.0 to 15.0 s (f360 to 450) | The real payout line only if it is on the screen. Hold for reading (at least 2 s) | none | pop |
| 15.0 to 18.0 s (f450 to 540) | End card: "Not financial advice", source and time stamp, CTA pill | pill pop 9 f | music tail |

### 4.6 Signature move per format (stops the sameness)
Each video gets one signature move and two support moves; the signature is not reused by another format.

| Format | Signature move | Support moves |
|---|---|---|
| Goal clip with banner | freeze, flash, number flip with delta chip | speed ramp, punch-in |
| Guess the % | ring countdown, riser, flash reveal | digit slam, bars fill |
| Wheel | peg ticks, creeping stop, stamp | pointer flick, dim to panel |
| Explainer | whip pans between beats, word-by-word captions | line with moving head, split cards |
| App demo | tap rings, zoom to the number | phone slide-up, scroll |
| Matchday card | rows slam in on the beat with team-colour wipes | counters, hero chip |
| Chance race | bars glide, final-ranking hold | rank-swap glide |
| Map of chances | zoom to country, fill | markers pop |
| Breaking | glitch burst, BREAKING stamp | scanlines, ticker |
| Upset retro | flash, shake, "6%" counter | slow-mo into the whistle |

### 4.7 Look kit (rotation, so two posts in a row never match)
Fixed on every video: logo placement, risk line, source line, safe area, hero-number size, hold times. Rotated: palette, background, display font, transition, sound set. Pick by format family, then rotate by a date seed (never the same look twice in a row for the same format). Fonts already in `assets/fonts`: Anton, Archivo Black, Bebas Neue, Inter, JetBrains Mono. These looks are proposals (DERIVED), not tested.

| Look | Palette and background | Display font | Transition | Sound set |
|---|---|---|---|---|
| Night pitch (today's look) | near-black, lime, soft glow | Anton | 10-frame whip pan | clean hits |
| Broadcast | navy, cyan, scoreboard bar, thin rules | Bebas Neue | slide wipes | ticks, stadium-style swells |
| Tabloid | yellow and black, hard edges, stamps | Archivo Black | hard cuts and stamps | thuds |
| Paper chart | off-white, ink line, one red accent | Inter (black weight) | line-draw wipes | soft pops, no hits |
| Terminal | black, green mono text, scanlines | JetBrains Mono | typewriter and short glitch | clicks, static |
| Neon grid | purple, pink, cyan, grid floor | Anton | glitch burst | synth hits |

## 5. Tooling

### 5.1 GSAP: frame-accurate timelines in our renderer
- **Status (13 Oct 2026):** GSAP 3.15.0 (13 Apr 2026). Since 3.13 (29 Apr 2025) the whole toolset, including the old Club plugins (SplitText, MorphSVG and the rest), is free for commercial use under the standard "no charge" licence. One forum comment says the licence blocks using GSAP inside a competing visual animation builder: UNVERIFIED, read gsap.com/standard-license once.
- `assets/js/gsap.min.js` (72 KB) is the core only. Plugins live in the `gsap` npm package (`dist/SplitText.min.js` and so on) or on jsDelivr; copy the ones we use into `assets/js` so renders stay offline and repeatable.
- **Rules that keep seeking safe** (our pipeline calls `TL.seek(t, false)` then every `TICKS` function per frame):
  1. Draw state in `TICKS` functions (pure functions of t), not in `tl.call()`. A call only fires when the playhead crosses it, so a random-access still can skip it.
  2. No `repeat:-1`, `Math.random()`, `Date.now()`, CSS transitions or CSS keyframes. Use a seeded generator.
  3. Write times in frames: `const f = n => n/30`.
  4. If two tweens touch one property, use `fromTo` (or `immediateRender:false`) so a `from()` does not fight the tween before it.
  5. Fonts and images must be loaded before frame 0 (`show()` already waits).
  6. `tl.addLabel('hit', 3.5)`; `tl.labels` gives the cue times.
  7. Determinism test (rule 21): render frames 0, 45, 20, 45 in that order and compare the two frame-45 images. Add it to `videotest.py`.
  8. For design work open a dev page with `GSDevTools.create({animation: tl})` and scrub.
- **Free plugins and what they do for us:** SplitText (word masks, captions); DrawSVG (line and ring draws); MorphSVG (bar to line, icon morphs); MotionPath (ball along a pitch path); Flip (bar-race reorders, layout jumps); CustomEase (port After Effects curves); CustomWiggle (shake); CustomBounce (stamp bounce); EasePack (ExpoScaleEase for zooms, RoughEase); ScrambleText (BREAKING decode); TextPlugin (typewriter); Inertia (wheel flings); Physics2D and PhysicsProps (confetti, rarely); GSDevTools (scrub). Draggable, Observer, ScrollTrigger, ScrollSmoother and ScrollTo are for interactive pages; skip.

Sketch (signatures checked against the GSAP docs; not run in our pipeline):
```js
const f = n => n / 30;                                    // write times in frames
const CUES = [];                                          // reset with CUES.length = 0 inside show()
const cue = (atF, sfx, gain = 0) => CUES.push({ t: atF / 30, sfx, gain });
window.getCues = () => CUES;                              // Python: st.js('window.getCues()')

gsap.registerPlugin(SplitText, ExpoScaleEase);
// mask-rise headline
const s = new SplitText('#q', { type: 'words', mask: 'words' });
tl.from(s.words, { yPercent: 110, duration: f(9), stagger: f(2), ease: 'power3.out' }, f(4));

// count-up drawn after every seek (same idea as counter() in motion.html)
function countUp(tl, el, from, to, atF, durF, fmt = v => Math.round(v) + '%') {
  const o = { v: from };
  tl.to(o, { v: to, duration: f(durF), ease: 'power2.out' }, f(atF));
  TICKS.push(() => { el.textContent = fmt(o.v); });
}

// impact: 3-frame flash + punch + decaying shake, all pure functions of time
function impact(tl, atF, el = '#scene') {
  const t0 = f(atF);
  tl.set('#flash', { opacity: .8 }, t0).to('#flash', { opacity: 0, duration: f(3), ease: 'none' }, t0);
  tl.fromTo(el, { scale: 1 }, { scale: 1.12, duration: f(5), ease: 'power2.out' }, t0)
    .to(el, { scale: 1.05, duration: f(8), ease: 'power2.inOut' }, t0 + f(5));   // settle at 105% so shake edges stay hidden
  TICKS.push(t => {                                       // shake: amplitude falls 20% per frame, 12 frames
    const i = (t - t0) * 30, k = (i >= 0 && i < 12) ? Math.pow(.8, i) : 0;
    gsap.set(el, { x: k * 22 * Math.sin(i * 2.1), y: k * 14 * Math.cos(i * 2.7) });
  });
  cue(atF, 'hit_deep');
}

// smooth zoom: ExpoScaleEase keeps the perceived speed constant
tl.fromTo('#world', { scale: 1 }, { scale: 4, duration: f(30), ease: 'expoScale(1, 4, power2.inOut)', transformOrigin: '62% 40%' }, f(60));
```
Alternatives: `CustomWiggle.create('hit', {wiggles: 7, type: 'easeOut'})` gives a ready-made decaying ease (docs confirm the call; check that it swings both sides before relying on it for shake).

### 5.2 Capture and encode
- **Today:** `Page.captureScreenshot` JPEG q93 per frame -> mjpeg pipe -> libx264 CRF 17. Sensible. Remotion's own release notes found JPEG capture much faster than PNG with no visible difference (one old example: 14 s down to 6.5 s); PNG only for alpha. For thin coloured text raise JPEG quality to 95 or more and check a frame at 300% zoom.
- **Speed:** (1) Render in parallel ranges: split the frames into 2 to 4 chunks, each in its own Chrome (the `Studio` class already gives every instance its own profile and port), encode each chunk, then join with `ffmpeg -f concat -c copy`. (2) `HeadlessExperimental.beginFrame` gives exact frame control but needs special launch flags and a patched clock (puppeteer-capture overrides timers, rAF and Date.now); not worth it for a renderer that is already a pure function of t. (3) Remotion, since v4.0.534 (release date not checked), shares the bitmap with its ffmpeg through a special Chromium; the speed idea is to skip encode and decode of images, which a pipe of raw frames could copy later.
- **Colour (test first):** Chrome's JPEG frames are full-range BT.601; phone H.264 expects BT.709 limited range. Colour tags only label, they do not convert (ffmpeg trac and forum threads). Test: encode one frame, read the lime `#D4FF3A` pixel back with Pillow, compare to the design value. If it is off by more than 3 levels try:
```
-vf "scale=in_range=full:in_color_matrix=bt601:out_range=tv:out_color_matrix=bt709:flags=accurate_rnd+full_chroma_int,format=yuv420p"
-colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv
```
UNVERIFIED on our machine; Instagram and TikTok re-encode anyway.
- **Final file:** H.264 High, yuv420p, 30 fps, CRF 16 to 18 for text-heavy frames, `-movflags +faststart`, AAC 192 kbps at 48 kHz, 1080x1920.

### 5.3 Remotion, HyperFrames or our setup

| | Ours (Python + CDP + GSAP) | Remotion 4.0.535 (12 Oct 2026) | HyperFrames 0.8.152 (13 Oct 2026) |
|---|---|---|---|
| Method | page exposes `renderAt(t)`; screenshot per frame | React components are pure functions of the frame number; Puppeteer screenshots; fast shared-memory path since 4.0.534 | HTML + CSS + GSAP/Lottie/Three/WAAPI adapters; seeks each frame in headless Chrome; ffmpeg |
| Licence | none | free for individuals and companies up to 3 people; 4 or more: Company License (Automators $0.01 per render with a $100 monthly minimum; Creators $25 per seat per month; prices from file 14, read 13 Oct 2026) | Apache-2.0 |
| Audio | none today | `<Audio>` tracks with volume curves | clips with data attributes; mixing in the producer package |
| Preview | render and look | Remotion Studio scrubber | `preview` command (Studio "evolving") |
| Cost to adopt | 0 | rewrite templates in React; Node toolchain | rewrite timing as data attributes; Node 22+; 70 open issues |

Recommendation: keep ours. Borrow three things: a scrubber page (GSDevTools), chunked parallel rendering, and the cue-sheet audio mix. Revisit Remotion if the team passes 3 people or needs many frame-accurate `<video>` layers.

### 5.4 From the timeline to the soundtrack (the missing piece)
Flow: timeline -> `CUES` -> mixer -> WAV -> mux. Store each SFX's "hit" offset (seconds from file start to its main transient) so the cue time is the time of the transient.
```python
# cues.py: build the soundtrack from the cue sheet (numpy + wave only)
import wave, numpy as np
SR = 48000

def load(path):            # 48 kHz mono 16-bit wav, made once with: ffmpeg -i in.wav -ar 48000 -ac 1 -sample_fmt s16 out.wav
    with wave.open(path) as w:
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768

def mix(cues, dur, lib, out):   # lib = {"hit_deep": {"file": "...wav", "hit": 0.012}, ...}
    buf = np.zeros(int(dur * SR) + SR, np.float32)
    for c in cues:
        s = load(lib[c['sfx']]['file']) * 10 ** (c.get('gain', 0) / 20)
        i = max(0, int(round((c['t'] - lib[c['sfx']]['hit']) * SR)))
        n = min(len(s), len(buf) - i)
        buf[i:i + n] += s[:n]
    peak = float(np.abs(buf).max())
    if peak > 0.89: buf *= 0.89 / peak                    # about -1 dBFS ceiling
    with wave.open(out, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((buf[:int(dur * SR)] * 32767).astype(np.int16).tobytes())
```
```
ffmpeg -hide_banner -i cues.wav -af ebur128=peak=true -f null -
ffmpeg -y -i video.mp4 -i cues.wav -c:v copy -c:a aac -b:a 192k -ar 48000 -ac 2 -shortest out.mp4
```
- If the music is added in-app, set levels by peaks (hits at -3 dBFS), not by LUFS: a sparse SFX track measures far below -14 LUFS and normalising it up would clip the hits. The -14 LUFS target applies only when music is baked in.
- `loudnorm` squashes dynamics; for punchy SFX prefer measure-then-static-gain plus a limiter.

### 5.5 Lottie
- lottie-web 5.13.0 (21 May 2025, MIT) and dotLottie web 0.81.0 (6 Oct 2026, MIT). Seek with `anim.goToAndStop(frame, true)` (true = frames, false = milliseconds), autoplay off; HyperFrames' adapter does the same. Avoid After Effects expressions inside Lottie files: Remotion's docs warn frames can flicker and say it cannot be fixed without an upstream change.
- Use it for small hero loops designed in AE (confetti, checkmark, flame, whistle, ball) exported with the free Bodymovin plugin. Data scenes stay in GSAP/SVG because they are data-driven.
- LottieFiles' Lottie Simple License allows commercial use, modification and no attribution for free animations; each animation's page can add limits; do not rebuild a competing library.

### 5.6 After Effects and Premiere
- Use AE for what HTML does badly: particle bursts, liquid and shape morphs, heavy glow, 3D hero titles, glitch packs. Deliver as Lottie, as a PNG sequence with alpha (loads like the JPEG clip sequence in motion.html, deterministic), or as WebM VP9 with alpha in a `<video>` (needs one seek per frame; a PNG sequence is safer). This matches the house rule: compile in Premiere, AE only for elements.
- AE as a feel lab: tune a move in the graph editor, read the influence and speed, port it as a CustomEase.
- Data-driven AE: **nexrender** (MIT; `@nexrender/core` 1.63.3, 25 Feb 2026) renders AE templates from JSON jobs through `aerender` (project path, composition, asset and text overrides) without opening the GUI; AE must be installed on the render machine and the licence terms for headless render nodes should be checked. Adobe's data-driven MOGRTs (spreadsheet-fed bar charts and line graphs) work in Premiere. Community note: expression-only charts get slow with big data; scripts ran about 7 times faster. I found no clearly free, ready-made data-driven chart template; the ones listed (Videohive, Monsterone) are paid.
- For batch output the HTML renderer is faster and cheaper than AE; keep AE and Premiere for hero edits and client changes.

### 5.7 Small libraries worth knowing
d3 7.9.0 (ISC, maps and scales), MapLibre GL JS 6.14.0 (BSD-3, tiled maps), Three.js 0.186.1 (MIT, real 3D text), Rive (MIT runtime, interactive states). Flourish and Datawrapper are good for prototyping a chart idea before building it; not for final output.

## 6. Ten reference accounts

Counts were read on 13 Oct 2026: TikTok profiles through a text reader, YouTube channel pages from their markup, earlier numbers from files 11 to 16. "Look" notes marked UNVERIFIED are from memory and the earlier research, not from re-watching this session (I cannot see video here).

| # | Account | Platform and size | Type | What to study |
|---|---|---|---|---|
| 1 | Kurzgesagt | YouTube, 25.7M subscribers | motion-heavy faceless explainer | flat vector scenes, tight palette, every move eased and scored, one visual metaphor per idea (UNVERIFIED) |
| 2 | Vox | YouTube, 12.7M | explainer with maps and charts | annotated charts, labels on the data, zoom to detail (UNVERIFIED) |
| 3 | PolyMatter | YouTube, 1.93M | faceless finance and geopolitics | map and chart callouts, steady pacing (UNVERIFIED) |
| 4 | Economics Explained | YouTube, 2.89M | faceless finance explainer | number callouts over simple graphics (UNVERIFIED) |
| 5 | @hai02a | TikTok, 112.6K followers, 4.2M likes | bar chart race | rank glide, final-ranking hold; top post 18.8M plays |
| 6 | @geo.all.day | TikTok, 244.9K, 9.9M likes | map pages | map zoom and reveal; 10.5M plays, 4.0% shares |
| 7 | @spot.the.differan | TikTok, 3,629, 159.7K likes | 12 s timed reveal | countdown clip, 4.5M plays on a tiny page |
| 8 | @statmuse | TikTok, 47.7K, 3.6M likes | sports stats | question-then-answer stat cards (Instagram and X counts not found) |
| 9 | @skysportsfootball | TikTok, 3.3M, 182.7M likes | football | Opta supercomputer reveal, 2.67M views (20 Apr 2026): big-number graphic plus a famous voice |
| 10 | @theeconomist | TikTok, 1.7M, 21.8M likes | data journalism | house chart style on vertical video (UNVERIFIED) |

**Peers to look at but not copy:** @polymarketsports 754.4K, @kalshi 689.6K, @unusual_whales 449.1K, @squawkafootball 174.2K, @polymarket 171.4K, @watcherguru 88.1K, @optaanalyst 35.3K. They post plain data cards and their reach per follower is weak: Opta Analyst supercomputer post 19,996 views on 35.3K followers (9 Jul 2026); Squawka quiz 13,512 views on 174K (Nov 2024); Unusual Whales 8-slide post 6,269 plays on 449K (8 Oct 2026); Kalshi averages 11.5K views (files 12, 13, 11). Visual Capitalist: Instagram count not found; the @visualcapitalist TikTok handle has only 253 followers, so it is not the brand's main channel (UNVERIFIED).

## 7. What to change first, and how to test it

### 7.1 Change first (each fits the current code)
1. **Frame 0 poster** in every `F.*`: subject and number (or "?") on f0, cover image exported from t=0.
2. **Verb library:** six entrance verbs (mask-rise, scale-slam, slide, typewriter, scramble, wipe) chosen per look; drop the universal white flash; call `impact()` only at the reveal.
3. **Linter in `selftest.py`:** read every text element's appear/stop time and check hold >= formula (1.7), position inside x 60 to 960 / y 210 to 1480, font size >= 36 px, hero number >= 150 px. Move the source line from 300 px to about 440 px from the bottom.
4. **Cue sheet, SFX pack and mixer** (5.4), baked into the mp4.
5. **Look kit** rotation (4.7) with a date seed.
6. **Determinism test** (rule 21) in `videotest.py`.
7. **A/B tests** below.

### 7.2 Tests
Same topic, same hour, two pages (or alternate days). Judge on 3-second hold (views past 3 s divided by views), average percent viewed, shares per view, plays per follower. Ten pairs only shows big effects; file 18 s8 says judge a format after 30 to 50 posts.

| Test | A versus B | Pairs |
|---|---|---|
| T1 | count-up hero number vs static number | 10 |
| T2 | crests/subject on frame 0 vs text-only open | 10 |
| T3 | baked SFX vs silent (music in-app for both) | 10 |
| T4 | word-by-word captions vs static captions (explainer) | 10 |
| T5 | progress bar vs none | 10 |
| T6 | hold formula vs 20% shorter holds | 10 |
| T7 | 3 s countdown vs 2 s | 10 |
| T8 | look-kit rotation vs one fixed look | 4 weeks |

## 8. UNVERIFIED list (collected)
- Any TikTok or Instagram loudness number (-14 LUFS is a convention; one vendor says -12 to -10).
- Safe-zone pixel numbers (all third-party; our 440 px bottom and 120 px right are cautious picks); the claim that a source line at 300 px is covered.
- ITU-R BT.1359-1 sound-sync thresholds, WCAG 2.3.1 three-flash rule, Netflix 5/6 s minimum and 7 s maximum subtitle times (all from memory, not re-read).
- CSS cubic-bezier equivalents of GSAP eases (from memory of easings.net).
- Sound-on shares of 88% and 93% (secondhand); animated-caption lifts of 18 to 28%; hook-rate benchmarks; the "90% fail in 3 seconds" claim (all vendor).
- Whoosh pre-roll of 3 to 6 frames, relative mix levels, and the hold-time formula (my derivations).
- Licences: Mixkit, ZapSplat, Pixabay for paid-ad use, Sonniss current text, Epidemic scope for per-view posts, TikTok Commercial Music Library rules in 2026.
- MapLibre per-frame capture, the `tmix` motion-blur trick, the BT.601 to BT.709 recipe on our machine, `optimizeForSpeed` on `Page.captureScreenshot`, the music slider behaviour in the TikTok app.
- The GSAP licence clause about competing builders; CustomWiggle swing direction.
- Instagram and X follower counts for StatMuse and Visual Capitalist; the look of YouTube channels 1 to 4 and The Economist.
- After Effects 2026 features and whether the AE licence allows headless render nodes.
- No verified view numbers exist for the wheel format.

## 9. Sources (all read 13 Oct 2026 unless a date is given)
**Platform guidance and studies**
- TikTok Ads Help, Creative best practices for performance ads (page undated; read through a text reader): https://ads.tiktok.com/help/article/creative-best-practices?lang=en
- Adweek, TikTok and CreatorIQ report, 6 Dec 2023: https://www.adweek.com/adweek-wire/tiktok-creatoriq-release-special-report-with-data-backed-keys-to-success-for-advertisers-2/
- Netflix Partner Help Center, English Timed Text Style Guide: https://partnerhelp.netflixstudios.com/hc/en-us/articles/217350977-English-Timed-Text-Style-Guide
- Brysbaert (2019), How many words do we read per minute, Journal of Memory and Language 109, 104047: https://www.Gwern.net/doc/psychology/linguistics/2019-brysbaert.pdf and https://www.bps.org.uk/research-digest/most-comprehensive-review-date-finds-average-persons-reading-speed-slower
- WSDOT video text duration (238 wpm): https://engage.wsdot.wa.gov/video-text-duration ; SSW rule: https://www.ssw.com.au/rules/post-production-do-you-give-enough-time-to-read-texts-in-your-videos
- Cowan (2001), The magical number 4 in short-term memory: https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/magical-number-4-in-shortterm-memory-a-reconsideration-of-mental-storage-capacity/44023F1147D4A1D44BDC0AD226838496
- Mayer's principles (summaries): https://services.dartmouth.edu/TDClient/1806/Portal/KB/PrintArticle?ID=171655 and https://lucidea.com/blog/mayers-12-principles-of-multimedia-learning
- Michotte launching effect (course notes, review): https://origins-of-mind-milan.butterfill.com/units/unit_251.html and https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2017.00314/pdf
- Direct labels: https://link.springer.com/article/10.3758/s13414-011-0155-1 ; conference abstract https://convention2.allacademic.com/one/aera/aera12/online_program_direct_link/view_paper/541281/ ; https://flourish.studio/learn/text/ ; https://data.europa.eu/apps/data-visualisation-guide/direct-labelling ; https://stephanieevergreen.com/directly-label/
- Captions (secondary and vendor): https://clipspeed.ai/blog/ai-captions-increase-views.html ; https://blitzcutai.com/blog/animated-captions-vs-static-captions ; https://openclip.app/guides/caption-animation-guide
- Hook claims (vendor): https://www.lemonlight.com/blog/the-top-10-hooks-businesses-can-use-to-make-tiktok-marketing-work/ ; https://nestscale.com/blog/increase-tiktok-hook-rate.html (via file 14)
- YouTube Shorts "stayed to watch": https://contentstudio.io/blog/youtube-shorts-analytics-guide ; https://www.shortimize.com/blog/youtube-shorts-retention-rate
- Safe zones (third-party): https://www.remotion.dev/elements/overlays/social-safe-zones/ ; https://adaptlypost.com/en/blog/social-media-safe-zones-2026-complete-guide ; https://www.trymypost.com/blog/instagram-reels-safe-zones-2026

**Motion craft**
- UI animation durations (secondary): https://uxdesign.cc/the-ultimate-guide-to-proper-use-of-animation-in-ux-10bd98614fa9 ; https://fluent2.microsoft.design/motion ; Nielsen Norman Group listing (article would not load): https://nngroup.com/videos/ux-animations
- Whip pans and speed ramps: https://creativecow.net/?p=2451776 ; https://photofocus.com/software/tutorials-software/easy-whip-swish-pan-in-after-effects/ ; https://tutvid.com/premiere-pro/whip-pan-blurring-transition-effect-premiere-pro/ ; https://motionarray.com/premiere-pro/premiere-pro-speed-ramping-tutorial/ ; unofficial beat-sync page: https://www.claudemarket.ai/skills/iart-ai/motion-design-skills/beat-sync-editing
- Screen shake and juice: https://infovore.org/?p=5275 (summary of Nijman's "art of screenshake"); Jonasson and Purho, "Juice it or lose it", Nordic Game 2012 (talk, no page read)

**Sound**
- Sound-design guides (vendor): https://sonilo.com/ai-music/whoosh-sound-effect-guide ; https://morphic.com/resources/sounds/whoosh-sound-effect
- Loudness and mixing: https://www.forasoft.com/learn/audio-for-video/articles-audio/lufs-targets-per-platform-2026 (5 Jun 2026) ; https://en.wikipedia.org/wiki/Audio_normalization ; https://meterplugs.com/blog/2019/09/18/youtube-changes-loudness-reference-to-14-lufs.html (2019) ; https://openclip.app/learn/audio-normalization ; https://opus.pro/blog/best-loudness-normalizers (outlier) ; https://sounddesign.irpr.agency/guides/how-to-mix-audio-for-youtube/ ; https://vidpros.com/fix-background-music-too-loud-video/
- SFX licences: https://pixabay.com/service/license-summary/ ; https://mixkit.co/license/ (terms did not load) ; https://rekkerd.org/sonniss-releases-gdc-2026-game-audio-bundle/ ; https://app.cinevva.com/guides/free-sound-effects-music ; https://musictech.com/news/music/the-bbc-sound-effects-archive-over-33000-free-samples ; https://www.production-expert.com/production-expert-1/free-sound-effects-2022

**Tooling**
- GSAP: https://gsap.com/blog/3-13/ (29 Apr 2025) ; https://webflow.com/blog/gsap-becomes-free ; https://gsap.com/docs/v3/Plugins/ ; https://gsap.com/docs/v3/Eases/CustomWiggle/ ; https://gsap.com/docs/v3/Eases/ExpoScaleEase/
- Remotion: https://www.remotion.dev/docs/license ; https://www.remotion.dev/docs/shared-memory-capture ; https://remotion.dev/docs/renderer/render-frames ; https://www.remotion.dev/blog/1-2 ; https://www.remotion.dev/docs/lottie ; prices via file 14 (https://www.remotion.pro/license)
- HyperFrames: https://github.com/heygen-com/hyperframes
- Frame-by-frame renderers and CDP: https://github.com/andreybo/html5-animation-video-renderer ; https://github.com/alexey-pelykh/puppeteer-capture ; https://cdpstatus.reactnative.dev/devtools-protocol/tot/HeadlessExperimental
- Lottie: https://help.lottiefiles.com/animation-licensing-basics-
- nexrender and Adobe data-driven templates: https://www.npmjs.com/package/nexrender ; https://helpx.adobe.com/ro/premiere/desktop/add-text-images/use-motion-graphics-templates/use-data-driven-motion-graphics-templates.html
- ffmpeg colour handling: https://trac.ffmpeg.org/ticket/979 ; https://ffmpeg.org/pipermail/ffmpeg-cvslog/2013-July/066579.html
- Package versions from the npm registry, 13 Oct 2026: gsap 3.15.0 (13 Apr 2026); lottie-web 5.13.0 (21 May 2025); @lottiefiles/dotlottie-web 0.81.0 (6 Oct 2026); remotion 4.0.535 (12 Oct 2026); maplibre-gl 6.14.0 (11 Oct 2026); d3 7.9.0; three 0.186.1; hyperframes 0.8.152 (13 Oct 2026); @nexrender/core 1.63.3 (25 Feb 2026).

**Our own files and live reads**
- `C:\VISION\VISION CLAUDE\outcome\research\` files 00-status, 11, 12, 13, 14, 16, 18 (all 13 Oct 2026); `outcome\studio\templates\motion.html`, `render.py`, `PLAYBOOK.md` (13 Oct 2026).
- Live reads, 13 Oct 2026: TikTok profile pages (followers and likes) through a text reader; YouTube channel pages (subscribers) from page markup.
