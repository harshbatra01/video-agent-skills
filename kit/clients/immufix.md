# Immufix: Paula Radcliffe paid-social ads

Client file for the boss's Claude. Sources: Kanishk's chats of 29 Sep to 12 Oct 2026, his memory notes and the files on
his PC (checked 14 Oct 2026). Times are India time (IST) unless marked UTC. "The user" = Kanishk.

## Start here

- **Status (14 Oct 2026):** all 8 ads are finished through `v10` (the final colour pass, 4 Oct). The newest renders are
  in `Renders\V4s` (8 files, written 4 Oct 23:56 to 5 Oct 00:01, minutes after v10 was built, so almost certainly the
  v10 export by Kanishk). Claude has not checked V4s. `V3s` (from v9) were checked for 3 of 8 ads only.
- **After v10:** a graded website still of Paula with the pouch (7 Oct) and a graded clip pack for the person who runs
  Immufix's social account (11 to 12 Oct). No newer notes from Jaden are on record.
- **Blocking paid use (business, not editing):** licences for the Paula archive and the headline screenshots, an
  Epidemic plan that covers paid ads, the parked compliance questions (Secret weapon story, co-owner disclosure,
  "I'm 52" stops being true on 17 Dec 2026), and consent for the cloned CTA voice.
- **Very next step:** ask Kanishk whether V4s went to the client and what came back. Then measure V4s (length, loudness,
  true peak: earlier renders sat at -13 to -15 LUFS and +0.1 dBTP) and offer loudness-normalised copies at -14 LUFS /
  -1 dBTP as new files, and give Jaden the licence and compliance list from "Open items".

## What the client is and wants

### The client
- **Immufix:** a UK daily nutrition powder. Company: Be Well Health & Nutrition Ltd. The product was called
  "Breakthrough" in 1998.
- **Front:** Paula Radcliffe OBE, marathon world record 2:15:25 (London 2003), held 13 Oct 2002 to 13 Oct 2019. She
  bought into the business in 2026 and is a co-owner.
- **The job:** 8 vertical testimonial ads for paid Meta and TikTok, shot by the client: Paula talking to camera at three
  locations (sofa, park, riverside) plus camera B-roll of her and the product. Vision Clipping edits; Kanishk is the
  editor; Jaden reviews.

### What they want (client brief docx in `C:\VISION\IMMUFIX\`)
- "Nutrition, not supplements". Master line: "IMMUFIX: Nutrition for a life in motion".
- Build search demand for IMMUFIX, not for "Be Well".
- Paula is proof of routine and longevity, "not simply celebrity endorsement": lead with preparation and consistency
  ("the race is one day, the routine is every day"); the product is part of her day, never the cause of a result.
- The micronutrient "form matters" story (biologically cultivated, food-like matrix), but no blanket absorption or
  superiority claims. Never call competitors synthetic. No prevent, treat or recovery claims. No GLP-1 treatment claims.
  Child wording only after label checks.
- Audience test matrix: active 40 to 65, busy professionals, reduced appetite, event preparation, exercise recovery,
  existing supplement users. The grading notes doc says "30+".
- Jaden's reference brand: AG1, "clean, premium, natural and healthy", not corporate.

### The boss's standing script bar (Jaden's script review PDF, 30 Aug)
- "every single ad fundamentally needs like a call to action" with a real offer.
- "don't need to shit on people to make your thing looks good": never trash other brands.
- Tell a story with emotion, not website copy ("it's no story", "you could get an ai to say this").
- Authority lines only the star can say ("the three most important vitamins I used when I was a marathon runner").
- Hooks are specific direct address (his example: "if you signed up for a marathon this year"). He liked the Instagram
  reply-card idea.
- "I don't want this product to seem too much like an athletic sports product."

### People and roles
- **Jaden (boss):** reviews by screenshots plus short notes, sets the bar, asked for the clip pack and the website still.
- **Kanishk:** decisions and taste, downloads YouTube clips himself, hand edits (B-roll moves, pans, title placement,
  caption deletions, turning subtitles into graphics), masking and tracking when asked, all AI generation, his own music
  picks and mix, some final exports, the CTA voice (ElevenLabs).
- **Claude:** research, plans, every .prproj change by script, After Effects builds by script (headless), mockups,
  tracking by script, audio analysis and SFX placement, checks. Background research agents only, never a second editor.

## Formats and specs

### The 8 ads (bin "For claude", 1080x1920, 60 fps)
Key = first 8 characters of the sequence UID; every script and plan file uses it.

| Key | Ad (sequence name) | Look, camera clip | Length 29 Sep | Captions | Title credential | CTA | Render name (V3s) |
|---|---|---|---|---|---|---|---|
| 348e0ba6 | I'm 52 ("I'm 52 now reframed Copy 01" = "Sequence 04", the REFERENCE) | sofa, C108 | 30.17 s | yes | World Marathon Champion | code card 26.80 s | I'm 52 now v3.mp4 |
| 404c5cb2 | I held the record / ready to recover ("i held the record/ immune system after training A") | park, ddaaaaaaaa.mp4 | 29.28 s (34.3 s with the CTA end) | yes | Four-time Olympian | CTA end segment (v9) | immune system after training A v3.mp4 |
| 664b35b2 | People are always surprised | sofa, C105 + 2x C108 | 26.52 s | yes | World Marathon Champion | the user's own card track | People are always surprised v3.mp4 |
| 0991faf2 | Ran professionally ("ran professionally, didnt need all of that A") | riverside, C112 | 29.20 s | yes | Four-time Olympian | code card 26.10 s | didnt need all of that v3.mp4 |
| cd03e189 | 1 star reviews | sofa, C109 | 20.73 s (V3 render 23.08 s) | yes | World Marathon Champion | none on record (check) | 1 star reviews A v3.mp4 |
| 974102f7 | 3 questions | riverside, C117 | 45.28 s (V3 45.31 s) | yes | Four-time Olympian | code card 42.70 s | 3 questions A v3.mp4 |
| f233433f | 3 things to check (whiteboard) | park, C118 | 50.75 s (48.3 s by v8, 53.3 s with the CTA end) | NO caption track: its words are graphics | World Marathon Champion | code card 48.25 s (29 Sep), CTA end added v9 | 3 things to check A v3.mp4 |
| 593f11c4 | Secret weapon | riverside, C116 | 24.83 s | yes | Four-time Olympian | code card 22.28 s | Secret weapon v3.mp4 |

- The user trimmed 4 code cards in his v8 pass. Render names differ from ad names (held the record renders as
  "immune system after training"): always read names from the render folder, never guess.

### What each ad says (key lines; full word-timed text in `work\scripts.json`, kit copy `~/VisionKit/kit/library/pipelines/ad-build-kit/work/scripts.json`)
- **I'm 52:** harder to bounce back than at 30, didn't need random powders, pills and green shakes, daily since 24, one
  25 g scoop with water, two scoops when under the weather, code.
- **I held the record:** held the record 17 years; immune system "vulnerable for 20 minutes, half an hour" after
  training; refuel straight after; one scoop.
- **People are always surprised:** a dress, not running gear; travel; meeting people; "drains on my immune system";
  go-to since 24.
- **Ran professionally:** 20+ years; 2003 record stood 16 years; athletes with shelves of pills; "I didn't need all of
  that"; whole family; code.
- **1 star reviews:** reads a joke one-star review (a shelf of containers is now one pouch).
- **3 questions:** why not just a balanced diet, how it works, how long until benefits, almost 30 years, code.
- **3 things to check:** no mega doses (100x vitamin C), bioavailability, cellular uptake ("almost 100%"), "here and
  here" (she points at the board), code.
- **Secret weapon:** 1998 illness, double dose, training two weeks later, European Cross Country three months later,
  code.
- Fact checks: "17 years" and "16 years" are both correct. "I'm 52" expires 17 Dec 2026. See "Open items" for the
  Secret weapon wording.

### Camera and source media
- A-roll and camera B-roll: 6K files re-encoded to H.264 8-bit 4:2:0, 6048x3408, 25 fps, keyframe every 1 s. Tagged
  Rec.709 but really log.
- Colour-space override copied from C108 to every camera clip: `1012,1001,1,Narrow,YCC,8-bit,Scene-Referred`
  (behaves as Sony S-Log3 / S-Gamut3.Cine). C105 had none and C116 used a different option at the start: unified.
- Cleaned voice files carry Adobe Podcast names (`-esv2-50p-bg-10p-music-10p`). Whether music is baked into them was
  never answered.
- The user re-cleaned C105 and C108 audio on 3 to 4 Oct ("VERSION 2" files, identical picture). Swapping them in dropped
  the log override; v9 restored it. Any new re-cleaned source needs the override again.
- Caption track font: PowerGrotesk-Regular, centred near y 960.

### Track layout
- 7 ads: V1 talking head (A-roll), V2 zoom adjustment layers (only the A-roll is zoomed), V3 B-roll (each clip with its
  own Lumetri), V4 grade adjustment layer cut so grade pieces plus B-roll tile the timeline exactly, V5 and up graphics
  and AE overlays.
- Reference ad (I'm 52): V1, V2 zooms (DISABLED, IsMuted), V3 zooms (active, the user's own), V4 B-roll, V5 grade pieces
  (face light kept), V6 graphics.
- 3 things: an extra PRE-ZOOM adjustment track between footage and zooms for the tracked board blur and the "?".
- Audio: A1 voice, A2 music, A3 to A5 SFX lanes plus a crowd lane, extra tracks up to A6 where needed.
- Caption tracks always draw above video tracks: grades and zooms never touch captions, but any graphic sits under them.
  From v5 on, captions under graphics are DISABLED, never deleted.
- To move B-roll by hand: stretch the neighbouring grade piece into the gap and trim the grade where the clip lands,
  and extend the zoom layers too, or ungraded log shows.
- Projects built from one another share internal IDs and sequence GUIDs: close one before opening another.

### Grade
- **Reference grade (Sequence 04 main Lumetri, the live project values):** Temp +5, Tint -15, Exposure +1.0 (+0.7 after
  17.05 s), Contrast 8, Highlights -21.9, Shadows 22.7, Whites -5, Blacks -25.9, Sharpen 13, Vibrance 13.2, Vignette
  -0.28, gentle S curve, warm highlight wheel.
- The grading notes doc (`Downloads\IMMUFIX_GRADING_CONTEXT.md`) is OLDER (Temp -4, Tint -3, Exp -0.2, Blk -6.9):
  trust the project.
- **Face light:** a second Lumetri with a static feathered ellipse mask (Feather 138, Exposure +0.5), per shot, only
  where required.
- **v0 (29 Sep):** override on all 8 ads + an exact clone of the reference Lumetri on a V3 adjustment layer in 7 ads.
  Verdict: "grades are perfect".
- **v3 colour v2 (river: ran pro, 3 questions, Secret weapon):** Temp 3, Exp 0.9, Con 22, Sha 14, Blk -38, Sat 108,
  Vib 16. **Park (held the record, 3 things):** Temp 4, Con 16, Sha 18, Blk -32, Sat 104, Vib 15.
- **v4, 3 questions from 35 s (daylight changes, "pinkish"):** Exp 0.62, Temp +6, Tint -18, Con 26. Measured: skin at
  36 s L 51.5, a* 11.0, b* 17.2 vs early L 48.2, a* 12.45, b* 15.9.
- **Whitewashed fixes:** 1 star pouch C137: Exp 0.45, Con 32, Sha 6, Whi -12, Blk -42, Sat 112. Packing C131: Exp 0.55,
  Con 30, Sha 4, Whi -10, Blk -48, Sat 110, Vib 15 (1st-percentile luma 0.19 to 0.09). Sofa A-roll in People surprised:
  Con 14, Sha 15, Blk -36, Sat 105, Vib 15 (was 8 / 22.7 / -25.9 / 100 / 13.2).
- **v10 final pass (pass 2 deltas):** sofa ads (I'm 52, 1 star, People surprised) Con +16, Hil +14, Sha -14, Blk -8,
  Sat +3, Vib +6. Park (held, 3 things) Con +18, Hil +12, Sha -14, Blk -12, Sat +3, Vib +6, Tint +6 (mint shirt cast).
  River (ran pro, 3 questions, Secret weapon) Hil +4, Sha -20, Blk -30, Sat +5, Vib +6, Tint +6, Temp +2, and Con +26 on
  3 questions only (the user had already set Con 65 on ran pro and Secret weapon: kept). Camera B-roll gets its look's
  pass; archive, stock, face lights and the board spotlight are untouched. 96 of 134 Lumetris edited. Result (darkest
  1% luma): sofa 0.06-0.08 to 0.04-0.05, river 0.18 to 0.12-0.13, park 0.09-0.10 to 0.05-0.06. Pass 1 (smaller, Sat +6)
  turned skin orange, so pop comes from Vibrance.
- **External clips (Rec.709, no override):** clone of the master Lumetri with the log-specific basics zeroed (Tint,
  Exposure, Contrast, Highlights, Shadows, Whites, Blacks, Sharpen, Vibrance), curves, wheels and vignette kept; per
  clip Temp 0 to +6, Sat 85 to 95, Exp -0.3 to +0.35; SD archive also Sharpen 20 and Exp +0.3 to +0.35. From v5: stock
  base Temp +4 (rest 0, Sat 100); archive Temp 3, Sat 96, Con 8, Sharpen 16; modern stock Temp 2, Sat 100.
- **Grading targets (the user's own doc, backlit log talking heads):** face lit side 55 to 62 luma, shade side 45 to 50;
  skin hue 15 to 20 (under 10 reads pink); vectorscope angle about 123 (under 112 pink, over 130 orange); darkest detail
  2 to 5; red channel under about 95. Fix pink with more green Tint plus slight warmth ("Cooling made the pink worse");
  Exposure in 0.1 steps; WB eyedropper only on something truly white (a white T-shirt, never the cream sofa).
- **Vignette test on vertical crops:** set Amount to -3 briefly; if only top and bottom darken, the vignette is drawn on
  the wide source, so set it to 0 and put it on an adjustment layer.

### Zooms (from the user's "Malice" Transform presets)
- Each zoom piece = an adjustment layer with two stacked Transforms: a slow drift ("Malice Constant Zoom In Slow") and a
  quick punch. They multiply: peak = punch x drift.
- Intro: punch 115 to 100% over 0.867 s (ease out) x drift 108 to 100% over the piece (the reference used 120 x 110 and
  reached 132%, cropping her hair).
- Push: punch 100 to 110% over 1.133 s x a linear drift from 100% at 1.3 to 2.0 %/s. Pull: punch 110 to 100% over
  1.117 s x a drift back to 100%. Alternate push and pull, level continuous across boundaries, Sampling bicubic, keys on
  Scale Height.
- Anchor on the face: Anchor Point and Position both at (0.5, 0.33). Cap peaks around 116 to 121%.
- Start a move each time the picture returns from B-roll; push into a B-roll cut (into the London archive), land the
  pull after it.
- Whiteboard ad (3 things): anchor (0.40, 0.35), punch 104, intro 104 x 103, drift 0.25 to 0.4 %/s, at most 107%.

### Titles and the code card
- **Final title = option B (v3, kept since):** "PAULA RADCLIFFE" Coolvetica Heavy Comp 118 px, tracking 10, white,
  shadow (80, 22, 2), baseline y 1128 (just under the caption line; 3 things at y 360 above the board). Credential
  ("World Marathon Champion" or "Four-time Olympian") in Proxima Nova Extrabold 30 px, tracking 60, ink 0x141008,
  inside a gold pill 0xCFAE63 (height = cap + 22, width = text + 44, fully rounded). Credential tags x1.2 since v9
  (text Scale 120, the 3 things pill shifted right 42.8 px to keep its left margin).
- Title animation: name fades in 0 to 0.28 s, rises 40 px and settles from 106% by 0.5 s; pill opens from the centre
  0.20 to 0.55 s; credential fades in 0.42 to 0.62 s and lifts 8 px; everything reverses in the last 0.5 s.
- Title timings (v4 and v5, so no title spills into the next B-roll): People surprised 0.3-2.0 s, I'm 52 0.3-2.18,
  ran pro 0.4-3.3, Secret weapon 1.3-2.7, 1 star 3.8-6.43 (after the stars), 3 things 0.4-2.8, 3 questions 0.4-3.4.
- Earlier titles (superseded): v1 (30 Sep) top-left "PAULA RADCLIFFE / hairline / credential" in Proxima Nova, 0.4 to
  4.9 s: white on bright sky was unreadable. v2 (30 Sep) dark rounded plate 0x0C0C0C at 90%, 1.5 px grey edge, soft
  shadow, at x 30, y 64 (367x105 px), name Proxima Nova Semibold 35 px, 44x3 px gold line, subtitle Proxima Nova
  Regular 26 px 0xE2E2E2: the version Jaden reviewed.
- **Code card (TRYIMMUFIX):** dark card 640x206, radius 30, fill 0x0D0D0D, 2 px stroke 0x5A5A5A, 97% opacity; rises
  70 px and scales 92 to 100% over 0.55 s; "USE CODE" Proxima Nova Semibold 25, tracking 350, grey 0xAFAFAF;
  "TRYIMMUFIX" PowerGrotesk 88, tracking 30; starts on the word "code" and holds to the end. In the Premiere graphic the
  texts come first and the card last (the first component draws on top).

### After Effects graphics system (v4 to v9, all rendered as ProRes 4444 alpha overlays)
- **Layout zones (1080x1920):** kicker baseline y 1370, main caption baseline y 1590, a dark bottom gradient from y 980
  to below frame (feather 420, 74%); glass cards top-left (x 40, y 110, w 520); board graphics only in 3 things; nothing
  over her face. Everything not tied to the board lives in the lower caption zone with the same gradient.
- **Dynamic captions (loved):** only on B-roll, subtitles under them disabled. Main word Coolvetica Heavy Comp 236 px
  fitted to 980 px, gradient white to grey [0.77, 0.79, 0.82], Glow (threshold 60, radius 22, intensity 0.35), shadow
  (0.55, distance 5, softness 26), blur-in 26 over 0.2 s, scale 128 to 100% in 0.24 s (ease 80/20) then drift to
  103.5%, motion blur on. RGB split: red [1, 0.05, 0.25] and cyan [0, 0.85, 1] copies in Add, +/-22 px over 0.24 s,
  opacity 0 to 75 to 0 over 0.3 s. Kicker Proxima Nova Extrabold 54 px, tracking 60, word gap 20, one red word for the
  negative, rises 26 px in 0.2 s. White flash 0 to 24 to 0% over 0.15 s on the cut. Red strike for rejected options.
- **Stacked synced words (VITAMINS / MINERALS / NUTRIENTS, "perfect"):** one 230 px word per band at y 560 / 960 /
  1360, each on its spoken word; frame dims to 34% in 0.12 s; a WHITE rule 62% of the word width x 6 px draws out from
  the centre 0.12 to 0.42 s after the word. Used in 4 ads wherever she says the list.
- **Partial-word roll EFF[ICIENT to ECTIVE]LY (3 things 25.27-27.60 s, after CAN ABSORB IT):** fixed prefix and suffix,
  the middle rolls through two track-matte windows, 0.24 s ease-in-out, RGB ghosts, 101.5 to 106 to 101.5% punch.
- **Frosted glass info cards (3 things):** w 520 at x 40, y 110, radius 28, near-black tint 22%, white sheen over the top
  160 px at 9%, 1.5 px white edge at 34%, soft shadow (20%, blur 34), green tick circle 44 px with a Trim Paths tick;
  kicker Proxima Nova Extrabold 30 px tracking 130 with words fading up on her words ("ENHANCED", "NUTRIENT"); main
  lines Coolvetica 112 px auto-fit; width reveal ease-out 0.38 s, exit ease-in 0.25 s. The definition card grows the
  card in 0.30 s: white Proxima Semibold 36 px on a 42% black inset panel, word + meaning only. The real blur behind
  the glass is a Premiere adjustment layer (Gaussian Blur 42 inside a 4-vertex rectangle mask, feather 2, keyed every
  frame from `glass_geom.json`).
- **100x meter (3 things, with the vitamin C B-roll 10.30-13.18 s):** label and number on top, 900 px track at y 620,
  eased count 1 to 100x, colour green to yellow (at 55%) to red, stops at the track end on a red 5x76 px marker labelled
  "MEGA DOSE", number glow pulses on landing, fades out exactly on the B-roll's last frame, lands on "100 times".
- **"Ask Paula" question card (3 questions; own design because showing Instagram's UI in an ad needs Meta's
  permission):** white 900 px card centred at y 1520, radius 42, round avatar crop with a red ring, "ASK PAULA" red
  30 px tracking 160, grey "Your question", the question in 54 px typed word by word while she reads it; pops 72 to 104
  to 100% with -5 deg settling in 0.3 s; exits by hard cut or a snap to 0 in the last 0.12 s.
- **Headline cards (only headlines that really ran, word for word):** the real screenshot on a white rounded "paper"
  card, 3D tilt in (Y -30 to -7 to -2 deg, X 9 to 2 to 0, scale 90 to 100 to 104%), frame dimmed to 42%, highlighter
  yellow [1, 0.81, 0.23] rounded rects in Multiply at 88% growing left to right over the exact words, hard cut out.
  Used: BBC 4 Sep 1998 "Virus wrecks Radcliffe medal bid" (Secret weapon) and National Geographic "Fruits and
  vegetables are less nutritious than they used to be" (3 questions, 10.95-13.50 s, highlight "less" 12.27-12.47,
  line 2 12.78-13.40).
- **Counters:** IN 1998 (rolling back from 2026), TAKING IT SINCE 1998, WORLD RECORD FOR 17 YEARS, and 1998 / 17 / 20 /
  16 counters in Secret weapon, held the record and ran pro. They land fast, hold still, hard cut. Never two counters
  back to back.
- **1-of-5 stars (1 star reviews, 0.55-3.80 s, y 1150, so the gold star lands on the word "star" at 1.0 s):** no
  background box; five outline stars draw on (Trim Paths, white stroke 4, 0.06 s stagger); star 1 fills gold
  (gradient ramp light to dark gold + animated CC Light Sweep through a star alpha matte) and pops 0 to 118 to 100% at
  0.46 s with an additive blurred glow (Gaussian 34, Repeat Edge Pixels OFF since v5, it caused the box); stars 2 to 5
  flicker gold, fail, dim to 52% and sag 5 px; exit at 3.0 s. Comp 1080x400, 60 fps, 3.6 s, star radius 52, inner
  24.4, gap 128, corner round 7. Never light all five: that implies a rating nobody can back up.
- **3 things board reveal:** the three board items are blurred under a "?" from 0 to 30.62 s and unblurred line by line
  on her words: L1 4.00-4.90 s, L2a 15.05-16.25, L2b 16.25-17.15, L3a 28.15-29.45, L3b 29.50-30.35; "?" in at 0.55 s,
  out at 3.45 s. Built as one pre-zoom adjustment layer with Gaussian Blur 26 and one tracked Mask2 per line (keys once
  per source frame plus a hold copy 1/240 s before the next sample). The "?" = Coolvetica 360 px over a 300 px halo
  ellipse blurred 70 at 26% (Repeat Edge Pixels off, round glow since v6), tiny bob (sin 7.5 rad/s x 7 px, rotation
  sin 5.2 x 3 deg), parented to a tracked null.
- **"Here and here" spotlight (3 things 41.08-42.13 s):** adjustment layer with Lumetri (Exposure 0 to -1, Saturation
  100 to 76 over 0.2 s) and Gaussian Blur 0 to 6, under inverted tracked masks (feather 60); the lit box grows from 2
  lines to 4 on the second "here" (smoothstep 0.2 s); outside luminance 0.44 to 0.30. Cloned from the user's
  exposure-only Lumetri in I'm 52 (Contrast 0, Exposure 0.49), never from the master grade.
- **Held the record window graphic (v9):** "VULNERABLE FOR 20-30 MINUTES" moved into the caption zone: kicker 52 px red
  at y 1370, number 270 px at y 1580, MINUTES 52 px at y 1698.
- **CTA end segment (v9, held the record and 3 things):** 5 s after the last line. B-roll cloned from already graded
  items: C132 pouch on the post (in 72.00 s, 1.70 s), C141 scoop macro (in 4.00 s, 1.60 s), C121 Paula holding the pouch
  (in 8.00 s, 1.70 s). Overlay `cta_end.mov` at Position 0.5:0.5625 (120 px lower than centre so its backdrop starts
  where the caption backdrop starts): kicker A "HEAD OVER TO IMMUFIX" 0.12-1.42 s, kicker B "USE THIS DISCOUNT CODE"
  from 1.55 s (both 54 px at y 1060), code pill 920x230 at y 1215 (glass 72%, 3 px gold edge [0.81, 0.68, 0.39], scales
  86 to 100% from its centre), code word 190 px at 2.62 s with a white flash, shine sweep at 2.98 s, then the discount
  ("... OFF", 210 px) counting up 3.12-3.82 s in a gold gradient. The offer wording is in the CTA voice file and
  `cta_spec.json`.

### Colours and fonts
- Colours: white type; red [1, 0.231, 0.188] for negatives and strikes; green [0.204, 0.82, 0.482] for ticks;
  highlighter yellow [1, 0.81, 0.23]; code-pill gold [0.81, 0.68, 0.39]; pouch gold 0xCFAE63; ink 0x141008; card
  0x0D0D0D; edge 0x5A5A5A. Brand colours: navy and gold. Kanishk's verdict on the accents: "the colours u used are fine
  good infact" (gold not required).
- Fonts: Coolvetica Heavy Comp (big words, the name), Proxima Nova Semibold / Extrabold / Regular / Light (kickers,
  credential, body), PowerGrotesk (captions, code word), Georgia Bold / Italic (the old dictionary card, no longer
  used). Also on the PC: SF Pro Display, Galano Grotesque, Bodoni. **Needs his own:** Proxima Nova (Adobe Fonts) and a
  checked Coolvetica licence for client work.

### Audio
- **Voice:** staged to about -17.5 LUFS in every ad (I'm 52 -1.8 dB because it clipped at +10, held the record +8.1,
  3 questions +1.9, Secret weapon +2.5, 3 things +8). The user's own clip gains (+5 to +11 dB) sit on other ads.
- **Music on the timeline = the user's own Epidemic picks** (`C:\Users\Kanishk\Desktop\Audio\Paula ads`): Paradigm
  Shift (Gavin Luke, 138 BPM) on held the record, ran pro, 3 things and Secret weapon; Concrete Jungle (DonVayei) on
  People surprised, 1 star and 3 questions; Home Again (Park Lane, instrumental) on I'm 52. Clip gains about -16 to
  -24 dB. Respect his mix: only add, never rebalance it.
- **Claude's per-ad music edits stay on extra tracks, DISABLED** (bin "Ad edits", A on the timeline, B and C as
  backups): 3 things The Key (Dream Cave) / Unknown Phenomenon / Organic Foundation; 3 questions From Tree to Paper /
  Gravel Road Mystery; 1 star What Happens in the Park / Gossip Talk; I'm 52 Don't Waste My Time (instr.) /
  Eventually; People surprised Say It (instr.) / Making Me Feel Alright; held the record The Legend Begins / Colossus;
  ran pro Boost / Among the Clouds; Secret weapon The Hour of Truth (subdued intro, forced cut into the climax at
  14.30 s "Three months later I won", boom + whoosh there) / I'll Fly Far Away. Each edit ends its final chord on the
  code card or the last line and sits 11.5 to 14.8 LU under the voice. Claude cut these on its own bar grid because
  Epidemic's EditRecording with a forced duration time-stretches the track.
- **Epidemic on this job:** the official Epidemic MCP connector runs on Kanishk's PC with an API key held as a Windows
  user environment variable (value never viewed). Kanishk builds on the Creator plan, which covers neither client work
  nor paid ads; his decision is to move to Business "asap", before any ad runs. (Research: Epidemic's Pro tier covers
  client work and online ads for a freelancer or agency, and Business covers a brand's own channels and ads, so confirm
  with Epidemic which plan fits whoever will hold the licence.)
- **SFX kit:** 36 files `IMX_*.wav` (48 kHz, 24-bit) in `ENCODED RUSHES\Audio\SFX kit`, baked from 49 Epidemic
  downloads. Roles: POP1-5 (+ POP1_up2 / up4 for rising stacks), TICK1-3, GLASS1-3, QPOP1, LOCK1-2, LIGHT1-2, FLIP1-2
  (FLIP2 is ultrasonic and never used), BOOM1-2, SWISH1-3, WHOOSH1-3, SHIM1, HUD1, COUNT_10 / 09 / 05, MARK1-2,
  CROWD1. Pitched sounds are tuned to G major (the first music pick) and were NOT retuned to the user's tracks.
- **SFX levels (LU relative to the voice):** the pilot used main-word pops -6 to -10, ticks -15 / -16, card swish -12,
  glass -15 / -16, counts -17, locks -11, hero booms -10 / -14 (on 17, 16 and 1998), transition whooshes -9 to -13,
  title shimmer -14, crowd bed -19; then +2 dB on pops, ticks and glass, +4 on counts and +1 on swish, lock and whoosh
  after a check against the voice's local peaks. The user then turned pops down 3 to 4 dB: future pops about -10 LU.
  Brand sting on every code card: SWISH1 +0.08 s + LOCK2 +0.30 s. The user added camera shutter SFX himself.
- **CTA end audio (v9):** VO on A1 (4.41 s, -14.6 LUFS, -3 dB gain), the user's ElevenLabs file. His Paradigm Shift clip
  runs to the first downbeat after the CTA starts, then `IMX_MUSIC_ParadigmShift_CTA_ending.wav` (bars 67-68 + final
  chord + 1.2 s tail) so the chord lands on the discount in 3 things and about 0.2 s before it in held the record. SFX:
  WHOOSH2 0.02 s, TICK2 0.12, TICK1 1.55, SWISH1 2.62, LOCK2 2.85, COUNT_09 3.12, POP2 3.82.
- **Delivery target:** about -14 LUFS, true peak at most -1 dBTP, 48 kHz. Current renders measure -13 to -15 LUFS and
  +0.1 dBTP (immune system 34.33 s -13.3; 1 star 23.08 s -14.7; 3 questions 45.31 s -14.4). Neither platform publishes
  an upload target.

### Export settings (Premiere Export mode, Ctrl+M, one sequence at a time)
- H.264 preset "Match Source - Adaptive High Bitrate" (about 38 Mbps VBR, NVIDIA), 1080x1920 60 fps, AAC 320 kbps
  48 kHz stereo, no loudness normalisation, Effects all unchecked.
- Captions: "Burn Captions Into Video", C1 Subtitle, EXCEPT 3 things (no caption track; leave captions off).
- Export mode remembers settings per sequence: change Location every time (it pointed at the old folder). 1 star once
  remembered an MP3 preset saving to Downloads.
- Never start the AME queue: it holds 7 of the user's old v2 jobs marked Ready.
- No sequence has in/out marks, so exporting the whole sequence picks up the CTA endings.

### Safe zones
- Keep text clear of the top ~14% and bottom ~35% on Reels (about 220 px top and 420 px bottom on 1080x1920). A top-left
  title can sit under the Reels/Stories header and 4:5 feed crops cut it: about 250 px from the top for feeds.

### Camera B-roll catalogue (source seconds; x = subject centre as a fraction of width)
Folder `ENCODED RUSHES\B roll\A003_0918xxxx_C1nn.mp4`. Vertical crop at Scale 57 shows 0.313 of the width:
Position x = (540 - (cx x 6048 - 3024) x 0.57) / 1080; measure cx on a full-resolution grid, not on thumbnails.
- C120 park, holding pouch to camera: 4-10, 14-16, 20-22 (one pouch), 28-32 (two), 40-46 wide. Crew arm at 12, 18,
  24-26, 34-38. Best still: 21.56 s (website still); also 19.9-22.5, 31.1 (two pouches, bigger smile).
- C121 pouch held + checking watch 4-22 (x 0.5); scooping low angle 48-78; pouring/shaking 84-96; kneeling shake
  100-124; drinking 126-130; crew after 134. Never shows her face.
- C122 wide kneeling shake 2-10, drinking 12-24 (x 0.45). C123 medium drinking 0-18 (x 0.45; a moderate sip from
  3.4 s), smile 22-24.
- C124 pink-shoe lacing close 2-20 (x 0.48); wide lacing 24-30. C125 wide lacing 2-44; catching breath close 72-124
  (face x 0.55).
- C126 riverside railing calf stretch 2-24 / 28-38, lunges 42-58 (x 0.44; "Fishing prohibited" sign at x above 0.9).
- C127 low-angle portrait vs sky 0-18. C128 park run, small; best 26-33.
- C129 HERO run at camera (x 0.5): 30-41 (sharp 28-31.4), 42-45 close, 62-66, 88-100.
- C130 riverside tracking run: sharp 72-73.2 and 74.5-76.2 (soft 73.5-74), walking cooldown 86-94 (x 0.53-0.57).
- C131 pouches beside open suitcase 0-12 (x 0.56), packing pouch 14-20 (x 0.36).
- C132 pouch on post: 2-46 slide (use from 12.6, the pouch is cut off at 20.0), 70-86 static (x 0.45-0.5).
  C133 / C134 pouch on fence rail (C134 at 20 x 0.30).
- C135 hotel exterior 4-6. C136 suitcase at hotel 4-12 (hotel sign: crop Scale 70, Position y 0.39), car loading
  16-26; number plate readable from 28 (avoid).
- C137 pouch on round table 0-44 (at 20 x 0.44); pouch lowered into frame 51.8-52.6 (lands 52.7 at x 0.56, still from
  52.9, fingers 53.0-53.4) and 85.0-86.3 (lands x 0.58).
- C138 macros: shield logo 0-20 (x 0.62), "be well" 24-72, nutrition panel 86-116 (x 0.70-0.72).
- C139 = a different man from another shoot: NEVER used in Paula ads.
- C140 shaker on table 6-26; scoop pour 38-41 (powder falls 39.8-40.6, x 0.52); pouch + shaker 66-72 (too big for the
  vertical crop).
- C141 scoop macro 0-28 (slides: x 0.21 at 4, 0.385 at 12, 0.49 at 20). C142 powder inside shaker 0-32. C143 powder +
  pouch edge 12-54. C144 powder texture 0-40.

## House look and taste rules (with the verdicts)

### Liked and approved
- The v0 grade: "grades are perfect". The zoom style. Title B direction ("do bold name plus gold pill but below the
  caption"); a sports-broadcast strap was also liked ("i really like broadcast one").
- Dynamic reference-style captions: "the animated text which is dynamic looks nice keep it up"; "i really apprecieate
  how you figured out how to do nice dynamic captions, try bringing more of that creativity in".
- The VITAMINS / MINERALS / NUTRIENTS stack: "perfect" (only its middle rule changed to white).
- Frosted glass reveals ("frost glass ish which we reveal"), the dictionary card with "text on top", year counters ("i
  like the year counters and stuff see if we can fit in other places").
- White / red / green accents; headline cards wherever they fit ("if you think headline cards fit please of course go
  and do it").
- Dropping subtitles for graphics: "if we wanna remove subs and add graphics i am ALL FOR IT" (but disable, never
  delete: "do not do destructive stuff do not delete captions just disable them if we want them later").
- The SFX pass: "ok sfx is perfect". Motion design signed off 3 Oct: "all the motion design and everything is good now
  we just need everything to sound nice".

### Rejected
- White title on bright sky (unreadable). Title E (dark glass plate at chest): "why would u even reccomend E bro it is
  so off putting"; "the background takes away sm. and its wierdly placed sort of overing her mouth".
- "Punch" colour mock: "she looks BURNT too orange like a chicken nugget". Website still v1: "tooooo orange / breaking
  bad ish".
- 1-2-3 numbering on the board: "that just looks ass". All board-reveal concepts (marker reveal, mosaic + glow,
  lift-off type): "i do not at all like any of the reveals you showed".
- A smile instead of a drink: "her SMILING will not pass we need of her drinking specifically" (the drink that looked
  like choking was also out).
- Stars with a box ("why do they have to have a background"), boxed glows in general, the green tint highlight ("this
  green mask is just bad... it feels cheap"), opaque glass, a static ring that "stopped half the time"
  ("uninteresting"), a bar overflowing off screen ("it going offscreen looks bad"), clutter ("tooooo cluttered"),
  plain B-roll with nothing on it ("boring find ways to make it nice"), pronunciation and "noun" in the dictionary
  card, text that does not match the words (WE FORMULATED became REFORMULATED), a green rule inside a white stack, a
  second counter right after a counter ("i dont like the counter over there since we already did that just before"),
  graphics or gradients over her face.
- The first music pick (Bring Them Home, hopeful orchestral, 90 BPM): "i just dont like this music". Music must follow
  each ad's vibe (3 things = curious, slightly mysterious).
- Strangers' faces in stock or archive (a "Tokyo talk" shot was another woman); hospital-looking pills stock; a 5-frame
  flash shot ("its jarring and an error").
- Heavy B-roll in round 1: "we dont want whole add or even70 percent of ad or even 50 percent of ad to be B roll".

### Standing rules (why in brackets)
- B-roll sits above her clips, never cuts the A-roll; the grade is cut where B-roll sits; reuse across ads is fine
  (keeps the talking head intact and graded once).
- Never remove B-roll already placed: "i will delete old one myself", "just dont remove previous b roll".
- From 2 Oct: lots of Paula archive everywhere it fits ("a lot of footage of her here and there... ride off her fame";
  "even if they need license its okay"); round 1 had asked for about 40% coverage. Boss: "she has had A CAREER she is
  FAMOUS and yet we are not utilising on it".
- B-roll shows the literal thing the line names (boss: "show not tell"). Hands and objects in stock are fine ("video of
  hand full of pills and stuff i still can keep"); faces of strangers are not.
- Product shots: the pouch fully visible and centred most of the shot, landed and still before the cut (boss: "move
  then cut").
- Let her talk 1 to 2 s before a slow B-roll ("maybe just have paula talk for a sec or two and then go into the
  broll"); drop filler B-roll right before another B-roll and start the next one on the product word.
- Hard cuts, no fade that leaves 1 frame of her before a cut ("its 1 frame of normal paula before the next broll so
  don't fade it out"); montage clips 1.0 to 1.2 s ("no super small clips small is fine but not super small"); overlays
  start with their B-roll; counters land fast, hold, hard cut ("freeze it before and just hard cut").
- Titles never spill into the next B-roll or clash with other graphics.
- Land a proof graphic on the payoff phrase, not the setup ("have some subs rolling for 2-3 seconds and then pop the
  headline in").
- Hide the list, reveal each item as it is said ("we wanna keep em hooked right so we cant tell everything in start").
- Time-jump lines get real footage of the event, or the nearest real race, said so in the report ("use actual
  footage... if not of exact same race then any race that would fit").
- Small text needs size ("make it a biit more visible... not a lot just a bit").
- Headlines: only ones that really ran, word for word; never fabricate (the user parked compliance, not honesty).
- No ratings or results you cannot back: light one star, not five; never present stock people as her family.
- The user's quality reference (`ENCODED RUSHES\High quality reference 1.mp4`: 0.8 s hook, about 14 s of cinematic
  B-roll under big 2 to 3 word type, then calm talking) sets the QUALITY bar, not the style: "THAT IS NOT THE STYLE WE
  WANNA DO EXACTLY, its just to show you how high quality stuff looks".
- Grade: no "punch" that burns skin; washed out = lifted blacks, fix with Blacks / Shadows and Vibrance, not Saturation.

## Every deliverable and version, with status

All projects are in `C:\VISION\IMMUFIX\`. The original `ads immufix.prproj` was never modified. Each version was built
on the user's latest save of the one before (v5 deliberately on his v3 save).

| File | Date | Built on | What it added | Status |
|---|---|---|---|---|
| ads immufix.prproj | before 29 Sep | | the user's original (bin "For claude") | untouched |
| ads immufix - Claude grade.prproj (v0) | 29 Sep | original | C108 override on all ad clips; master grade on V3 in 7 ads | APPROVED ("grades are perfect") |
| ... Claude grade + broll.prproj | 30 Sep | v0 save | 43 camera B-roll shots in 8 ads (23 to 39% coverage), grade cut around them, hard cuts on phrase breaks, gaps left for archive | approved after the user's small moves ("everything is according to my liking now") |
| ... Claude grade + broll + external.prproj | 30 Sep | user's 07:14 save | 9 external shots (2 Paula archive, 7 stock) + bin "External B roll" (14 files, 5 spare), Rose label | kept; the user re-arranged it and keyframed pans (09:44, 09:57 saves) |
| ... Claude zooms + titles.prproj | 30 Sep 10:36 | user's 09:57 save | zooms on 7 ads, title v1 on 8, code card on 5; verified in Premiere | title v1 REJECTED (sky); the user moved 3 titles and deleted the "use this code" captions in 3 questions (12:48 save) |
| ... zooms + titles v2.prproj | 30 Sep 13:17 | user's 12:48 save | title v2 dark plate | the file Jaden reviewed on 1 Oct (user save 14:13); superseded |
| ... v3.prproj | 1 to 2 Oct | user's v2 save | title B, colour v2, real drink (C123 at 42.13 s, src 3.4), focus fix (C129 at 4.17 s, src 29.4), pouch hold (C137 6.217-7.967 s, src 52.6), vitamin C tablet and supplement-bottle stock replacing the "hospital" pills, AE stars on 1 star; 32 frames checked | superseded |
| ... v4.prproj | 2 Oct | user's 14:42 v3 save | 24 AE overlays (gfx_v1): dynamic captions in I'm 52 and 1 star; Ask Paula cards, NatGeo headline and 1998 counter in 3 questions; glass cards, 100x meter, dictionary, ring, counters in 3 things; counters in Secret weapon, held the record, ran pro; pouch-slide swaps (C132: I'm 52 src 12.6, ran pro src 30 shifted left 0.208 of frame width); pills-into-hand stock in 1 star; the vegetable shot removed (Jaden wanted it gone); 3 questions late-light fix | superseded; it DELETED captions under graphics (reversed in v5) |
| ... v5.prproj | 2 Oct night | user's v3 save + the gfx_v2 renders | 39 overlays + fixed stars; tracked board blur + "?"; live glass blur; 27 Paula archive shots (bin "Paula archive (v5)": 13 in People surprised, 7 in held the record); titles retimed; 1 star pouch colour; about 60 frames checked | superseded |
| ... v6.prproj | 3 Oct | user's v5 save (kept his caption-turned-graphic on V7 and 2 Cross Dissolves) | 11 re-renders (gfx_v3): round "?" glow, meter from 10.30 s, readable definition, REFORMULATED, EFF roll, white stack rules; tracked spotlight; People surprised re-cut (montage Boston stage 9.25, Westin Tokyo 10.45, gala 11.62, Joan Benoit Samuelson 12.62; Tower Bridge 2.75-3.83; A-roll with cloned grade pieces at 3.83-5.93, 7.52-9.25, 13.57-15.48) + colour; held the record pool shot replaced by C126 calf stretch (src 31.0) under FOR THE RECOVERY; I'm 52 archive at 12.68 removed, C132 at 13.52-14.32 on "Immufix"; ran pro mass-start in-point 32.24 | motion design APPROVED |
| ... v7.prproj | 3 Oct | v6 save (new bins "SFX kit", "Music") | 3 things sound pilot: music on A2 (Bring Them Home, 3 clips), 36 SFX on A3/A4, voice +8 dB | SFX approved, music rejected |
| ... v8.prproj | 3 Oct | user's v7 save | music per ad (bin "Ad edits"), SFX on all 8 ads, voice gains evened, audio tracks up to A6 | the user then replaced the music with his own, turned pops down, added shutters, re-cleaned two sources, made the CTA voice |
| ... v9.prproj | 4 Oct | user's v8 save | log override restored on the "VERSION 2" media (I'm 52, People surprised, last 3 shots of 1 star); credential tags x1.2; window graphic moved to the caption zone (gfx_v4); 5 s CTA end on held the record and 3 things | delivered; rendered as V3s |
| ... v10.prproj | 4 Oct night | user's v9 09:13 save | final colour pass (see Grade); before/after sheet `Renders\Grade v3 vs v10.png`; checked by Premiere frame exports vs V3s | delivered (V4 exports were offered by Claude); V4s exist |

### Renders (`C:\VISION\IMMUFIX\repair\Renders\`)
- Loose files dated 30 Sep 13:45 to 13:53 (8 ads, first round): very likely what Jaden reviewed on 1 Oct (not
  confirmed).
- `V2s\` (3 Oct, 8 files, rendered by the user).
- `V3s\` (4 Oct, 8 files from v9): Claude exported 4 through Export mode, then the PC crashed and the user rendered the
  other 4. Only immune system, 1 star and 3 questions were measured.
- `V4s\` (4 Oct 23:56 to 5 Oct 00:01, 8 files, e.g. "immune system after training v4.mp4"): made right after v10;
  not checked by Claude.

### Other deliverables
- **Website still (7 Oct):** `Renders\Website stills\Paula holding Immufix - website still.png` (v1, ad look, rejected as
  too orange) and `... website still v2.png` (calmer: saturation x0.8, oranges x0.62, slightly cooler, softer contrast,
  pouch protected); JPG copies `paula.jpg` and `paula (2).jpg`. 2400x3000 (4:5), C120 at 21.56 s (pouch at shoulder,
  looking at camera), graded by fitting the log-to-render mapping from C121 in "Secret weapon v4" (park look, RMS
  2.2/255). The pouch sits above the website's text band. Jaden wanted a better "Paula holding the product" photo.
- **Graded clip pack (11 to 12 Oct):** Jaden asked for "clips of Paula using Immufix" for the person who runs Immufix's
  social account; the user: "dont burn the colour grade please just make it look okay". 23 clips (19 of Paula: holding
  the pouch, two pouches, scooping, pouring/shaking, kneeling shake, drinking, smiling, lacing, catching breath, calf
  stretch, portrait, running x3, walking cooldown, packing; 4 product) as 4K landscape plus 19 vertical 1080x1920 (left
  out where the action crosses the frame), 25 fps, no audio, a natural S-Log3 grade (skill script `slog3_grade.py`)
  through ffmpeg, contact sheets and an "About these clips" note. In Kanishk's Google Drive
  `G:\My Drive\Immufix Paula clips (graded)` (47 files, 1.1 GB; he shares it) and locally in
  `Renders\Paula clips for <recipient>\` (the folder name carries the recipient's first name).
- **After Effects graphics:** `ENCODED RUSHES\Motion graphics\` = `gfx_v1` (24 .mov + immufix_gfx_v1.aep), `gfx_v2`
  (39 + aep + glass_geom.json), `gfx_v3` (11 + aep + glass_geom.json), `gfx_v4` (hr_window.mov, cta_end.mov + aep),
  `stars_1of5.aep` / `stars_1of5_v2.aep` + `_alpha.mov` + `_preview.mp4`. Every .aep sits next to its renders so any
  word, timing or colour can be edited by hand.
- **Pages (private claude.ai artifacts in Kanishk's account; he must share them):** pull list
  https://claude.ai/artifact/E9FATqYTv1p7qKC5TLJyQs ; round-1 plan page (50 tasks, 7 decisions, mockups, footage map,
  22 effects with tutorials, 25 headlines) https://claude.ai/artifact/AA9BEtcCs2s55euiiPhTxx . Plan task codes: D1-D7
  decisions, G1-G10 all ads, S Secret weapon, T 3 things, O 1 star, Q 3 questions, P People surprised, H held the record,
  R ran pro, F I'm 52.

## Review history, round by round

### Script stage (30 Aug, Jaden's script review PDF)
- Asked: a real CTA in every ad, no trashing competitors, emotion not website copy, star-only authority lines, specific
  hooks, not "too athletic". Done: the shot ads came after this review (the earlier drafts are in "Immufix_Ad_Creatives
  for claude.pdf").

### Kickoff (29 Sep)
- Asked: a Lumetri grade on adjustment layers, captions untouched, delivery as XML; and whether Claude could grade
  precisely, see and "hear" footage, do B-roll and zooms.
- Done: read the project by script, gave facts and limits ("I can't watch Premiere's own playback... Expect the first
  pass to be close, and exact after one check round"), proposed a new .prproj instead of XML (XML can lose Lumetri
  curves, masks and caption tracks) and 6 numbered questions with defaults. The user answered all six: new .prproj
  ("premiere project instead of fcp xml is ok"), C108's override on all clips, face light only if required, river ads
  should match the warm reference look, leave Sequence 04 untouched, screen access is fine.
- Verdict on v0: "grades are perfect".

### Kanishk's passes on 30 Sep
- B-roll: "have a good flow of b roll and speech going but only place it where it seems fit". External B-roll: cut the
  pull list back ("be a bit chill"), then wanted hand shots back, asked for YouTube links and downloaded two Paula clips
  himself. "it shouldnt be just like a 2 second blurry shot... look for good stuff to use". Mid-build: "just dont
  remove previous b roll" (the plan was rebuilt with nothing removed).
- Zooms and titles: "make sure framing of everything is still correct". Then the white title clashed with the sky:
  v2 plate. He moved and scaled 3 titles to the top-left (Claude used that spot for all 8).

### Round 1: Jaden on v2 (1 Oct; 20 screenshots plus 14 points from the user)
- Asked: ads feel slow and "corporate asf"; music "goofy corporate"; the title "in FOCUS" and centred ("middle chest")
  without clashing with captions; far more of her career (archive photos and video, headlines, collage, camera-click
  SFX); riverside ads "whitewashed" ("imbsr" = I'm being so real); Secret weapon pouch "move then cut"; Secret weapon
  code card sits where she isn't pointing (she points down and out about 23 to 24.3 s); People surprised run out of
  focus (C129 at 32 s); "show not tell" for meeting interesting people and her racing days; interesting B-roll at
  about 17 to 21 s in I held the record; 3 things: hide the three board items for tension and reveal on cue; the drink
  looks like choking; IG-style question pop-ups in 3 questions; a 1/5 star animation in 1 star; AI B-roll of "a shelf
  full of containers, then one pouch" in 1 star (the user generates); the "counting pills" stock looks like hospital
  pills; trim the fat; would I scrub or skip?
- Done: six research agents (archive licensing, music, ad style, effects, headlines, claims); a study of the user's
  quality reference; mockups of 5 titles, the Ask Paula card, board reveals, a Secret weapon time card, stars and
  colour; the washed-out colour measured (riverside blacks 17 to 28% grey vs 11 to 15% on the sofa, saturation about
  30% lower); the plan page.
- Decisions (2 Oct): title B below the caption, animated (E rejected); colour lower than the mock; Secret weapon = the
  full story ("don't worry about ASA"), compliance parked, no co-owner disclosure for now; no line cuts; music is his
  job later; stars must animate; real drinking; no 1-2-3 numbering; more effects; lots of archive in every ad (a footage
  map with links and timestamps); headlines rebuilt in AE or screenshots with a yellow/orange highlighter.
- Built: v3. Later rounds covered the rest (archive v5, board reveal v5, Ask Paula v4, headlines v4). The Secret weapon
  code-card position note has no recorded fix.

### Round 2: the user on v3 and v4 (2 Oct, about 30 notes, into v5)
- Asked: star glow box gone; titles leave before the next B-roll; whitewashed shots; headline lands on the payoff, not
  during the build-up; hard cuts; counters land fast then hold; 3 things: blur + "?" reveal line by line, smaller and
  less opaque glass, dictionary = word + noun + meaning, a meter that stops on screen with an end marker and finishes
  with its B-roll, "here and here" highlighted green; the VMN stack wherever she says it; real archive under TWO WEEKS
  LATER / THREE MONTHS LATER; let her talk before the 3 questions powder shot; Paula archive instead of generic B-roll.
  Also: "the clip that is supposed to be her running... gets scut in just like 10 frames. thats an error" (his own v4
  save had cut 1.35 s; v5 restored it and said so).
- Done: v5, rebuilt from his v3 save because v4 had deleted captions (all subtitles back, covered ones disabled). 2001
  training footage under TWO WEEKS LATER (12.35-14.30 s) and her 2001 World Cross Country win under THREE MONTHS LATER /
  EUROPEAN CHAMPION (14.30-16.48 s), because no 1998 European Cross Country video exists online. 3 questions powder shot
  from 21.33 s (was 20.03) with YOUR BODY / RECOGNISES. Vitamin C B-roll from 10.30 s so the meter starts with it.
- Verdict: only the "?" glow box was flagged on the board; accents approved; dynamic captions loved.

### Round 3: the user on v5 (3 Oct, into v6)
- Asked: round "?" glow; meter timing; readable definition without "noun"; REFORMULATED; white rules in the stack;
  "efficently and effectively should have some interesting dynaming captions"; replace the green tint ("feels cheap");
  People surprised needs more A-roll with zooms ("keep in mind the zooms and stuff should be there when A roll comes
  in"), no B-roll under "this is actually my life now" or "lots of drains", no strangers; whitewashed packing shot and
  sofa A-roll; "for the recovery, i do not like the b roll at all" (pool); filler B-roll before another B-roll in
  I'm 52 ("this b roll while shes saying has always stuck is out of place"); the 5-frame mass-start shot in ran pro.
  Answered "no" to restoring OVER 20 YEARS and to swapping Chicago 2002 for London 2003 in ran pro.
- Done: v6. Verdict: "all the motion design and everything is good now we just need everything to sound nice".

### Sound round (3 Oct, v7 then v8)
- Asked: whooshes, pops, clicks, counter ticks, transition and caption-pop SFX with variety, plus music; "grind our
  axes before cutting the tree" (research first). Claude said upfront it cannot hear: it does timing, levels, variety
  and loudness; the user's ears judge taste.
- Done: three research agents, the Epidemic connector, the SFX kit, the 3 things pilot (v7). Verdict: "ok sfx is
  perfect, i just dont like this music". Then music shortlisted per ad by vibe and SFX for the other 7 ads (v8).
  Music direction was delegated ("you're a better judge so please go ahead and choose"), then replaced by his own picks.

### Round 4: the user on v8 (4 Oct, into v9)
- Asked: "replaced 2 source footages with better audio versions which fucked up the colour grade... make it look as it
  was"; one CTA end ("only create one for now and re use it on ads which dont have a cta"); "this graphic and gradient
  is over her face, do it in centre or down maybe, keep it coherent with other graphics as to not clash"; credential
  tags "a biit more visible". Then: "render these via premiere on my behalf... in a new folder named v3s".
- Done: v9 (checked against his own renders made before the source swap, same timestamps: I'm 52 face mean RGB 155.9 /
  120.1 / 107.4 vs 160.8 / 124.1 / 107.8, within compression); V3s.

### Round 5: final colour (4 Oct night, into v10)
- Asked: "more contrast get the shadows down and highlight up a tad more then a pinch of saturation ... all ads maybe can
  benefit". Done: v10. No later verdict on record.

### Website still (7 Oct) and clip pack (11 to 12 Oct)
- See "Other deliverables". Website still v1 "tooooo orange / breaking bad ish", v2 delivered. Clip pack delivered to
  Drive; no feedback on record.

## What went wrong and the fix

- **Wrong colour on new sources:** re-cleaned "VERSION 2" audio files dropped the log override. Fix: restore the
  override and compare with renders made before the swap.
- **Zoom recipe mismatch:** the reference's V2 zoom layers were disabled, so copying both would double the zoom. Fix:
  read IsMuted before copying any recipe.
- **v4 deleted captions under graphics** (43 unresolved references, 4 blobs used before their data). Fix: v5 rebuilt from
  the save before it; from then on captions are disabled, never deleted.
- **v5 refused by Premiere** ("could not be loaded, may be damaged"): a mask template ID hardcoded from an earlier save
  had been renumbered by the user's save. Fix: find templates by MatchName and content; a semantic validator
  (`validate_sem5.py`); found by building variants that each drop one feature.
- **v6 builder tripped on the user's save** (overlays without Motion, items without Components, a caption-turned-graphic
  without SubClip, a transition in the clip list). Fix: guards, a Motion template from a 1080x1920 B-roll item, both
  Cross Dissolves kept.
- **Titles did not render:** `<AdjustmentLayer>true` came from a Mister Horse template. Fix: removed on titles.
- **Code card covered its own text:** the first component draws on top. Fix: texts first, card last, 97% opacity.
- **Title v2 check failed:** three titles carried the user's own Motion. Fix: replace it so the size is not applied
  twice.
- **v3:** the title was not on the top track in one ad (the user's code-card track pushed it down); a hand-placed stock
  clip had no Motion component. Fix: find graphics by name across all tracks; template from another B-roll item.
- **Glass and glow problems:** v4 glass cards covered her face (moved top-left, w 520); the star and "?" had boxed glows
  (Gaussian Blur Repeat Edge Pixels on); definition text under the glass tint was unreadable (text on top + dark panel);
  an 8-vertex rounded glass mask blurred the whole frame (4-vertex rectangles only); cloned Blur and Tint carried
  template keys and animated to 0 (strip keys you do not set).
- **The meter stayed pale yellow** (v4). Fix: fill colour by expression from the same eased progress as the number.
- **Pouch cut off** in the I'm 52 pouch-slide at source 20.0. Fix: source 12.6, checked in a Premiere frame.
- **v9 first CTA shot** (C137 lowering) was blurry and busy behind the kicker; the 3 things tag clipped at the left
  edge. Fix: static C132 shot, card 120 px lower, tag shifted right 42.8 px.
- **gfx_v4 renders failed** ("ReferenceError: W is undefined"): a generator built from pieces lacked the constants
  header. Fix: copy the header into every composed .jsx.
- **After Effects:** froze ("not responding") while Claude worked in Premiere, its window and crash reporter covered
  Premiere and screenshots timed out (the user closed AE; all 24 renders were done); crashed with 20 render items
  queued (one item at a time now); three 1 MB stub renders (killed at the DONE flag: wait for sizes to settle);
  `-noui` stopped the script; AE never quits by itself (watch outputs, then kill).
- **Premiere UI:** Export Frame refused a sequence name with "/"; duplicate frames from short waits; a double-click on an
  already-open sequence did not switch the Program monitor and the wrong ad was exported (use timeline tabs and
  confirm the monitor); an Adobe licensing window (not granted to computer use) covered Premiere during import (the
  user dismissed it; type paths instead of clicking under grey patches); 39 typed import names gave "File not found"
  (batches of 11 to 14).
- **Unsafe moments, all harmless:** Claude quit Premiere with Ctrl+Q once, and later the same shortcut raised the save
  prompt of the user's other open project (cancelled: use Ctrl+Shift+W); one job went to Media Encoder where his old
  jobs waited (only Claude's job removed, queue never started); the user clicked Save on Claude's inspection ("nooo sorry
  i saved"), checked by a diff.
- **Disk nearly full** (8.7 GB free on C:). Fix: Claude deleted only its own old temp frames (7 GB).
- **PC crashed** after 4 of 8 V3 renders; no half files; the user rendered the rest.
- **Audio:** most impact and boom SFX were inaudible on phones (89 to 99% of energy under 150 Hz), so pops are layered and
  booms only add weight; one click file was ultrasonic; the first SFX lane guard dropped hits (the 17-year landing among
  them), fixed with 3 lanes plus a crowd lane and tail trimming; adding two audio tracks at once gave duplicate indices
  (use the live track list and an original empty track as template; `\g<1>` not `\1` before a uuid).
- **Research:** VLC frame grabs dropped frames and failed with GPU decoding (use PyAV or ffmpeg now); Pexels search pages
  return a Cloudflare page to curl and clip pages sit behind Turnstile (browser for search pages, never click, HEAD-probe
  file URLs); a research agent's browser tab was navigated away (use your own tab); the headline agent ran about 50 min
  with an empty output file (message it to wrap up).
- **Removed old B-roll by plan** (the external build's first plan replaced some camera B-roll): the user objected ("just
  dont remove previous b roll"). Fix: nothing removed (REMOVE = []), rebuilt in minutes, and a standing rule.
- **The Epidemic connector would not register** from the user's terminal ("claude is not recognized": the Claude desktop
  app does not put its CLI on PATH). Fix: the app's bundled `claude.exe`, the API key set by the user as a Windows user
  environment variable (the config holds only the variable name; Claude checked it exists without reading it), a full
  app restart from the tray, then a test search.
- **More AE traps met:** "Object is invalid" after `addProperty` (re-fetch shape handles); the ring's Trim Paths in the
  wrong order (path, trim, stroke); invisible glass shadows and boxed glows (Gaussian Blur Repeat Edge Pixels on).
- **Tool-level failures, fixed in the skill's scripts:** blank caption text (the blob index covered only one keyframe
  field: index every BinaryHash), missing transcript words (a pad-aware decoder), an MP4 reader that lost the video track
  (a second `hdlr` overwrote the first), a builder that ran the reference ad first and lost its empty-track template,
  stale crop previews (cache keys must hold every parameter), framing misread from thumbnails (measure on full-resolution
  grids), a track-ID regex that hit the wrong pair, YouTube search failing on `ytInitialData` (regex + retries) and
  storyboard sheets coming out 3200 px wide (rebuilt at 192x108 tiles), `validate_struct` needing two arguments, and
  patches broken by heredocs and quoting (write files with the Write tool).
- **Taste misses** (white title on sky, title E, orange colour, smile for drink, numbered badges, board reveals, green
  tint): each became a rule above.
- **Unresolved in the record:** after the v5 star fix, stars 4 and 5 show a faint gold fill at 1.5 s; old and new renders
  were compared and nothing was changed (likely part of the original animation, not confirmed).

## Open items and next steps

### Editing
1. Find out what happened with V4s (delivered? approved?) and check them: duration, loudness, true peak. Also check the 5
   V3 renders never measured (3 things, I'm 52, People surprised, ran pro, Secret weapon) if V3s are still in use.
2. Offer a -14 LUFS / -1 dBTP loudness-normalised render set (current renders peak at +0.1 dBTP), as new files.
3. 1 star reviews has neither a code card nor the CTA end on record, while Jaden's rule is a CTA in every ad: confirm.
4. Secret weapon code-card position (Jaden: it sits where she isn't pointing, about 23 to 24.3 s): no recorded fix.
5. Offers never answered: run the I'm 52 pouch shot to the end of "as a part" (1.3 s instead of 0.8 s); give I'm 52 and
   1 star the same small deepening as People surprised. The Joan Benoit Samuelson photo crop leaves Joan out of frame.
6. The user's own layers (flagged, not fixed): a stray "New Caption" placeholder subtitle at about 2.3 to 2.5 s in
   3 questions; a duplicate "for 20" caption at 0:15.08 in I held the record (one copy zero-length).
7. The SFX kit's pitched sounds are tuned to G major, not to the user's final tracks (retune if pitched SFX are reused).
8. AI B-roll for the 1 star "shelf of containers, then one pouch" was the user's job: no record that it was made.
9. Unanswered from round 1: is music baked into the cleaned voice files ("music-10p")? Can Paula's team share her own
   photos and footage (the cleanest archive route)?

### Business decisions for Jaden before any ad runs
1. **Archive licences:** every Paula clip from YouTube (BBC, documentaries, IAAF, London Marathon Events, Abbott WMM
   material) is editorial and uncleared for paid ads; the Getty comp is a watermarked placeholder only. Fastest clean
   route: ask Paula's team first (she co-owns the brand), then Getty commercial quotes.
2. **Headline screenshots** (BBC, National Geographic) in a paid ad may need publisher permission; UK case law (NLA v
   Meltwater) treats headlines as possibly copyright. Recreate wording without mastheads, or get permission.
3. **Music:** Epidemic Creator covers neither paid ads nor client work. Kanishk's plan: upgrade to Business "asap"
   before ads run (Pro also covers client work and online ads for an agency; Business covers a brand's own channels:
   confirm which fits who holds the licence), safelist the Instagram, Facebook and TikTok channels, and ask Epidemic
   support about ads that run only in Ads Manager. TikTok needs a Business Account, music added in the editor and the licence box ticked (a known bug mutes
   audio after product links).
4. **Compliance (parked by the user: "for secret weapon do not worry about asa compliance, just get it done its fine
   you have my word"; "no need to disclose co owner disclosure etc for now"):** CAP 15.1.1 (authorised health claims
   only), 15.6.2 (nothing implying it prevents or treats illness), 15.8 (nothing implying a normal diet is not enough); a
   genuine testimonial is not a separate route for claims (ASA ruling Real Health Supplements, 24 Dec 2025); the ASA
   reportedly banned a Huel ad on 30 Sep 2026 for tying an athlete's race win to the product (City AM). Secret weapon
   follows exactly that "illness, then product, then recovery" pattern. Disclose Paula's stake. A realistic AI
   celebrity endorsement likely breaches the Code: AI imagery must never depict Paula.
5. **Script facts to raise when compliance is unparked:** Secret weapon says "write-off" (she won races up to 30 Aug
   1998), "two weeks" (the brand site tells the 1998 story without it) and the product was "Breakthrough" then; the
   caption EUROPEAN CHAMPION sits over 2001 World Cross Country footage, not the named race (European Cross Country,
   Ferrara, 13 Dec 1998, confirmed, no footage exists); "I'm 52" expires 17 Dec 2026.
6. **CTA voice:** an ElevenLabs file whose name suggests an instant voice clone. Confirm the talent's consent and rights
   before paid use.
7. **Fonts:** Proxima Nova and Coolvetica licences for client work.

### Housekeeping
- The originals of the builders, generators and audio tools sit in Temp scratchpads on Kanishk's PC (see "Where the
  files live"), which can be cleaned at any time; some files were already lost around 12 Oct. Copies of the code (not
  media) are now in the kit library: `pipelines/ad-build-kit/`, `pipelines/review-pages/`,
  `pipelines/youtube-research/`, `research/immufix/` and `handoffs/immufix-grading-context.md`.

## Where the files live on Kanishk's PC

### Projects and docs
- Projects: `C:\VISION\IMMUFIX\ads immufix*.prproj` (original, v0, + broll, + external, zooms + titles, v2 to v10).
- Client docs in `C:\VISION\IMMUFIX\`: the advertising brief docx, the ASA reference docx (Real Health Supplements
  ruling), the approved-testimonials docx (private customers' names: do not reuse), "Immufix_Ad_Creatives for
  claude.pdf" (earlier script drafts), "Jaden review.pdf" (the boss's script review). Text copies of the three docx files
  were made in the kit-build session's Temp scratchpad on Kanishk's PC (temporary: ask Kanishk for the docx files).
- Grading notes: `C:\Users\Kanishk\Downloads\IMMUFIX_GRADING_CONTEXT.md` (22.8 KB; holds the measurement targets and
  `analyze_frame.py` in section 11; its Lumetri values are older than the project).
- Memory notes (Kanishk's Claude): immufix-premiere-project, immufix-review-round1, immufix-broll-catalog,
  immufix-external-broll, immufix-audio-phase.

### Footage and media (`C:\VISION\IMMUFIX\repair\ENCODED RUSHES\`)
- `Cleaned` (A-roll, incl. the "VERSION 2" re-cleaned files), `Uncleaned`, `B roll` (C120 to C144).
- `External B roll\Stock (Pexels, free)` (6 object-only clips: 7033622 vitamin C tablet, 8676954 fizz, 5697643 pills
  spill, 7525915 supplement bottles, 7615430 capsule bowl, 7889571 veg close-up; plus hands clips 6297755, 4661333,
  6801319, 7615545, 10047234, 7930758) and `\Paula archive (watermarked comps - licence before use)` (Getty 141096625
  Chicago 2002 comp, 576x432, 28 s).
- `YT FOOTAGE` (Chicago 2002 WMM vertical 1080x1920 23.976; London 2003 #TBT 1280x720) and `YT FOOTAGE\YT FOOTAGE MORE`
  (Chasing Stars documentary, Thank you Paula, Trans World Sport 2001, a motivation compilation, 1998 IAAF World Cross
  Country Marrakesh). All downloaded by the user.
- `Motion graphics\` (see versions), `Audio\SFX` (49 raw Epidemic WAVs), `Audio\SFX kit` (36 IMX files), `Audio\Music`
  (18 ES_*.wav), `Audio\Music\Ad edits` (18 IMX_MUSIC_*.wav incl. the CTA ending), `_claude_check_frames` (Premiere
  check exports; Premiere's Export Frame dialog now remembers this folder), `Reference for zooms and colour.mp4` (the
  reference render), `High quality reference 1.mp4` (the user's quality reel).
- CTA voice: the user's ElevenLabs MP3 in his Downloads (project item "CTA audio"). The user's music: `Desktop\Audio\
  Paula ads`.
- A CTA project of the user's from another job in `C:\VISION\IMMUFIX\` supplied the text and shape templates for the
  Premiere graphics.

### Renders
- `C:\VISION\IMMUFIX\repair\Renders\`: first-round loose files (30 Sep), `V2s`, `V3s`, `V4s`, `Website stills`,
  `Paula clips for <recipient>`, `Grade v3 vs v10.png`.

### Scripts (originals in Temp scratchpads on Kanishk's PC; code copies in `~/VisionKit/kit/library/pipelines/ad-build-kit/`)
- Main session: `C:\Users\Kanishk\AppData\Local\Temp\claude\C--VISION-IMMUFIX-repair-ENCODED-RUSHES\b6d96195-2992-4138-a685-9dc3b5c5abcd\scratchpad\`:
  - `prproj\`: build_zoom_gfx.py, build_title_v2.py, build_v3.py, build_v3_stars.py, build_broll.py, build_ext.py,
    build_v5.py, v5lib.py (Mask2 / Gaussian Blur / Tint components, adjustment items), build_v6.py, build_v7.py
    (audio clips with `<Gain>`), build_v8.py, build_v9.py (edit_param, bigger_tags, clone_at, swap_media, CTA assembly),
    build_v10.py, validators (validate*.py, validate_sem5.py), inspectors (audio_dump, title_dump, media_cs,
    lum_inventory, tl_dump, cta_words), templates gfx_templates.json, text_doc_template.json, appearance_template.json.
    Most import the old session `build_project.py` Doc class; the skill's `prproj_lib.py` replaces it.
  - `work\`: scripts.json (word-timed scripts per ad), ads_all.json, broll_bin.json, plans (broll_plan, ext_plan,
    zoom_plan, gfx_plan), colour calibration (model.py, align.py, sample_pairs.py, calib_grab.py; the fitted model file
    is gone), mockups (mock_title_options.py, mock_ideas.py, mock_stars.py, mock_3things.py), check_sheet.py,
    refstudy.py, shotcheck.py, skin_measure.py, qa_gfx2.py.
  - `ae\`: stars.jsx, stars_v2.jsx, gfx_helpers_v1.jsx, gfx_v2_body.jsx, effroll.jsx, patch_v3.py, make_gfx_v2.py /
    v3 / v4, cta_spec.json (a ready caption kit; not in the skill yet).
  - `audio\`: analyze_sfx.py, bake_kit.py, bake_kit2.py, cues_tt.py, dialog_tt.py, ads_audio.py, cues_all.py,
    music_scan.py, track_an.py, music_edit.py, edit_map.py, verify_renders.py. Do NOT ship `dl_batch1-5.py` or
    `dl_music1-2.py` (they hold signed download links).
  - `track\`: tracker.py, board_def.py, run_track.py, masks_tt.py, spot_tt.py, make_frames_jsx.py, seqframe.py.
  - `v5\plan_broll.py` (archive placements + clamped crop formula), `webstill\` (still grading, clips.py for the pack),
    `review_page\template.html` (plan page source).
  - Already gone (scratch cleaned about 12 Oct): yt_search.py, sb_batch.py, v6\fine2.py.
- Recovered from a session transcript during the kit build (`...\ec5f7644-dcbf-495b-8860-ae4920add013\scratchpad\recovered\`
  on Kanishk's PC): storyboard.py, yt_search.py, ytinfo.py, sb_batch.py, crops.py, sharp.py, make_page.py,
  pull_data.py, probe.py, update_page.py, add_headlines.py, footage_map.json, queries.txt. Kit copies:
  `pipelines/youtube-research/` and `pipelines/review-pages/`, all untested since recovery. `update_page.py` is not in
  the kit (damaged in recovery, no intact original).

### Outside sources (archive map)
- **YouTube footage map (Kanishk downloads; uncleared for paid ads):** Chicago 2002 record: WMM vertical short
  9Q89DUovOko (0:13-0:16 close-up, 0:40-0:43 run-in, 0:46-0:49 tape break), NBC5 F4wnGFEZ808 (7:37). London 2003:
  British Athletics bqBBPXaMREI (0:04-0:10 crowd tracking, 1:43-1:46 line under the 2:15:25 clock; has a logo and clock
  graphic), DLLSKmpMKe4 (0:00-0:20, 1:36), UDEMZTB5I54 (clock 3:12, press 1:00, fans 2:04), full broadcast fan upload
  i8u0Mp_-fa4. 1998 World Cross q4sEUftpSko (2:45, 5:30, 9:00). BBC documentary y5XnD2-rjXU (6:30 Budapest, 3:30 snow,
  13:00, 24:00, 30:30). Montage n6IkUp1CJis (0:52 Budapest, 1:12-1:36 Ostend 2001 stand-in). Athens 2004 7DqgBD26d-E
  (not 1998, mood only). Training 2001 pz_dP408IEE (1:10-2:10). Chasing Stars ozIeKjwadRI (4:00 family, 10:30-14:00
  travel, 13:00 Tokyo, 14:30 refuel, 16:30 pool, 23:30-25:30 panels); trailer K6ZLs8IrY6o. Munich 2002 9qUUAIHqRVE
  (3:10). Helsinki 2005 wRw754RYPDM (1:02). Commonwealth 2002 lq3XOzWhD2w (3:40-4:50). NYC 2007 qPJYc-_3aXk (2:24).
  Beijing Dp7hVf8OeQ8 (2:56). London 2015 _RcBoqatAVw (0:20, 0:56). Boston 2025 mS3XNTv59zc. English Schools XC
  7uIolf6ZZOE. NYC 2004 f5FQx6-uMuM (9:30-10:30 sprint, 14:30 flag, low res). Also 2001 World XC g9zsKEukhCg, European
  Athletics 2002 10,000 m GN0CB1BpYtA. Avoid W6I2-YP42rs (2005 roadside stop) and 9_REX5GWubw (wrong "still stands"
  claim). Placements used: Chicago tape break from source 46.0 s; London finish from 101.97 s (720p: Scale 266.67, crop
  centre x 0.55, so the clock sits at the top).
- **Licensable archive (Getty, editorial unless cleared):** about 151 Paula clips. London 2002 BBC 1B22539_0004 to _0007,
  1B23687_0007 / _0017; Chicago 2002 141096625; Commonwealth 2002 2042574631, 2042601759, 2042647458, 2042625285,
  2042879023, 2042887661 (also 2042664859, 2042916666); NYC 2007 140867412; 2015 interviews 687994420, 687993812; ITN
  training 1994 2272378915; TWS 2003 rushes from 1732306935; 1995 Fifth Avenue Mile 140828685; 2003 training feature
  1732319547. 1998 stills: 1736151 (Marrakech), 1638400 (leading Budapest), 650534132 / 650534180 / 650529576 (collapse
  and stretcher, after a race, NOT the illness). No 1998 video exists anywhere. BBC Motion Gallery needs prior approval
  and will likely refuse a supplement brand; London Marathon Events needs prior written approval and its race TV is
  BBC-made; ITN and Trans World Sport rushes are "not released"; PA/EMPICS frames on Getty are "UK OUT, IRELAND OUT";
  Olympic footage needs the IOC; Abbott World Marathon Majors is a likely category conflict (Abbott sells nutrition);
  fan uploads cannot be licensed from the uploader. Screen frames for royals, other celebrities, rivals, sponsor logos
  and rival drinks (three Getty refuel stills show a sports-drink brand).
- **Verified headlines (25 on the plan page):** strongest: BBC 4 Sep 1998 (virus ends her medal bid), BBC 13 Apr 2003
  "Radcliffe smashes record", the BBC Athens 2004 and NYC 2004 comeback pair; National Geographic on less nutritious
  vegetables.

## Which kit skills to use for this client

- **premiere-ae-editing:** every .prproj change (relink, clone, Lumetri values, masks, Level and gain, disable instead of
  delete, new versions), the semantic validator, AE builds and renders by script, Premiere UI checks (Export Frame,
  Export mode), frame sheets, loudness checks, the S-Log3 grade script for clip packs.
- **editing-playbook:** B-roll judgement for talking-head ads, hooks and story for testimonial ads, review intake and
  version discipline, grading taste (washed out vs burnt), the verdict library above.
- **motion-design:** titles, dynamic captions, stacks, glass cards, counters, the CTA end card, the stars element.
- **research-and-sourcing:** archive licensing for a famous athlete, YouTube research without downloading (storyboards),
  headline verification, claims checks, Epidemic and music licensing.
- **social-video-formats:** paid Meta and TikTok specs, safe zones, sound for paid social, platform UI permissions.
- **production-automation:** the "one spec list drives picture, placement and sound" build for AE overlays, Premiere
  placement and SFX cues.
- **Pipelines:** none of the three main library pipelines (newsdesk, outcome-studio, edits-kit) is for this client. Its tool set is in
  `~/VisionKit/kit/library/pipelines/ad-build-kit/` (with `review-pages/`, `youtube-research/`, `research/immufix/` and
  `handoffs/immufix-grading-context.md`): reference code built on the old Doc class, so port what you need into the
  skill's libraries and test on a copy of a project before reuse.
- **Needs his own:** an Epidemic account on a plan that covers client work and paid ads (Business per Kanishk's plan, or
  Pro: see Audio) and its API key for the connector, the fonts, archive licences, access
  to the two private pages (Kanishk shares), an ElevenLabs account only if the CTA voice is redone with consent.

### How a round runs (the workflow that worked)
1. **Intake:** one long review per round (screenshots + plain notes per ad). Restate it as a numbered fix list; map each
   screenshot to its ad and time; check whether the user saved after the last build and diff that save (timeline JSON
   dumps); pull exact word times from the caption track (3 things: from the transcript). Ask which file version was
   reviewed and to say "that's all" when done. (editing-playbook)
2. **Decide before building:** for vague notes, mock 2 to 3 concrete options on real graded frames (with the real
   caption in place) and give a recommendation with a reason; expect the pick to differ. Big reviews become a plan page
   with task codes, owners and tick boxes. (editing-playbook)
3. **Sourcing:** numbered links with timestamps in chat, in priority groups; the user downloads; Claude catalogues new
   footage with frame sheets every 2 s and writes a placement plan (ad, start, end, file, source in, subject x, zoom,
   label); crops checked on one sheet. (research-and-sourcing)
4. **Graphics:** one Python spec per overlay in sequence seconds; the AE generator converts to comp time, builds,
   renders one queue item at a time with a log and DONE flag, writes meta and geometry; test-render one overlay per
   type first, then the batch, a QA sheet, re-render only failures. (motion-design, premiere-ae-editing)
5. **Import:** Claude imports renders in Premiere by UI (Ctrl+I, folder path typed, names in batches of 12), saves,
   closes. (premiere-ae-editing)
6. **Build:** copy the user's latest save, write `build_vN.py` on its XML (new objects appended, untouched objects
   byte-identical), validate structure and semantics, install as "ads immufix - Claude zooms + titles vN.prproj", open
   in Premiere, export 30 to 60 check frames at the changed times, one sheet, fix, report. (premiere-ae-editing)
7. **Sound:** cue sheet from the same overlay specs; offline mix to check loudness before touching Premiere; SFX on
   A3 to A5, music on A2. (premiere-ae-editing audio, editing-playbook sound taste)
8. **Report:** per ad: what changed, what was kept from the user's edits, what could not be checked ("I haven't heard
   any of the new audio"), 2 to 3 closed questions with a default. Update memory every round. (editing-playbook)
9. **House habits on this PC:** read the title bar before closing Premiere (save the user's unsaved changes, they are
   his); never Ctrl+Q with another project open; one Adobe app at a time was the rule until the RAM upgrade (31 GB,
   "it should be safe to run softwares together now"); check disk space before renders; on "pause" or "stop", stop at
   once and write a pause note.
