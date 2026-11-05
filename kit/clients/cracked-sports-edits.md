# Cracked sports music edits (for Vision Clipping's music promo pages)

Client file for the boss's Claude. This is Vision Clipping's own product line: beat-synced sports edits where a client's
song is the audio. Sources: Kanishk's chat of 13 to 14 Oct 2026, his memory notes and the files on his PC (checked 14 Oct
2026). Times UTC unless marked IST. "The user" = Kanishk.

## Start here

- **Status (14 Oct 2026):** the pilot (Lamine Yamal x Tkandz "Now or Never") is at **v8** (flash panels), not yet
  reviewed. **Wave 1** of three new edits was delivered on 14 Oct at 03:53 UTC (09:23 IST), no verdicts yet: 01 Mike
  Tyson x Central Cee ft. Lil Baby "BAND4BAND" (v1 to v3), 02 Anthony Edwards x Travis Scott "SICKO MODE" (v1 to v2),
  03 Lamine Yamal x Don Miguelo "Y Que Fue?" (v1).
- **Last verdicts:** v7 "Almost there"; "Not a big fan of all the transitions yet, but a good starting point"; build new
  edits on new storytelling bases.
- **How they are built (old route):** one live After Effects comp per edit (every clip, word, hit and transition a live
  layer, nothing baked). **Decided 15 Oct 2026:** music edits are now assembled in Premiere, with After Effects only
  making the effect elements.
- **Very next step:** get Kanishk's verdicts on v8 and wave 1 (he will say what he "really, really, really" likes); carry
  the winners into wave 2 on new bases (velocity edit, end payoff, then vs now, a 13 s duo loop). Confirm the
  flash-panel halves order. Double-check every on-screen fact before anything is posted.

## What the client is and wants

- **The goal (Kanishk, 13 Oct):** "CRACKED GOOD LOOKING FULL OF DIFF EFFECTS edits like crazy creativity... sync them to
  music beats and just juice them up". Football, basketball and more, for Vision Clipping's music promo pages, where the
  client's song is the audio and must feel like the star.
- **Phases:** WHAT (a huge inspiration bank, 13 Oct), then HOW (a free in-house kit: "build them yourself... make it re
  usable", no paid tools), then training ("train yourself to be better and better with everything"; at 22:14 UTC on
  13 Oct: "The focus is training you"). Long-term aim: automate these edits like vc-news.
- **The bar:** "we are the best in the world... absolutely crazy editors go so hard, we need to match their quality".
  Effects must LOOK good, not just exist. His own GASS x Mbappe edit is the starting point, not the bar: first "THAT is
  the amount of quality we want", then "mbappe was one that i did, im not that experienced. it nEEDS TO BE MUCH BETTER".
  The real bar is the consensus top of the bank (edits picked by 2 to 4 researchers independently).
- "Anything flashy is good. Anything crazy is good. Anything basic is bad." "good wont cut we need GREAT". Flashy and
  crazy wanted "at every given point".
- **Who does what:** Kanishk sets the bar and the taste, approves downloads and installs (name, source, size), ticks the
  AE scripting pref ("Allow Scripts to Write Files and Access Network"), frees disk, supplies 4K packs when YouTube
  blocks, reviews renders with timestamps and screenshots, and fact-checks on-screen numbers before posting. Claude does
  research, measurement, tools, plans, builds, renders and QA, and records every verdict in memory and the skill.

## Formats and specs

### Frame and timing
- 1080x1920, 30 fps. The picture sits in a **1080x800 band (y 560 to 1360) with black bars** above and below (like
  GASS x Mbappe): we see more, the virtual camera moves less, and type gets room in the bars. Title baseline y 540 (just
  above the band's top edge), captions in the bottom bar at y 1402 (34 px; optional second line +48 px, 26 px, tracking
  300), lyric words at y 1446. Type safe zone 10% to 76% of the frame height.
- Lengths: the pilot 31.97 s; wave 1 21.6 to 29.7 s. Benchmarks for YouTube edits (75 edits with 150k+ views): median
  length 39 s (middle half 27 to 56 s), like rate median 2.8% (top 10% above 4.2%), comments per 1k views median 0.49.
- Beat arithmetic: frames per beat = 60 / BPM x fps; 150 BPM at 30 fps = 12 frames (16th note = 3 frames); a slowed
  70 BPM = 25.7 frames. Tempo detectors read half or double time (the pilot song measured 138, 94 and 70 BPM in
  different runs; the song map said 69.5 half-time): trust the kick/snare list over the BPM.
- Every event snapped to a whole frame: round(t x fps) / fps minus 0.1 ms (4-decimal times had put a third of v1 to v3
  events one frame late). Cuts on the strongest kick or snare within +/-0.2 s (strength x (1 - 0.5 x distance / 0.2)),
  floored to a frame, so cuts land 0 to 1 frame early; report sync against chance before rendering.

### Pilot and wave 1 settings
- **Pilot:** "Now or Never" (UK rap; Yamal and PSG had used it), song window 12.80 to 44.77 s (one beat before the drop,
  around the song's own most-replayed stretch on YouTube, 9 to 17 s with the peak at 14 s), band [560, 800], 30 fps.
  Plan `pilot\plan_v8.py`; render `pilot\renders\yamal_now_or_never_v8.mp4`.
- **Wave 1:**

| Edit | Song window | Base | New on top |
|---|---|---|---|
| 01 Mike Tyson x Central Cee ft. Lil Baby "BAND4BAND" | 44.42 to 66.0 s (21.58 s) | fight cold open | impact frames, poster silhouettes, stutter strike, pop-up freeze, hit list, "20" (youngest heavyweight champion) |
| 02 Anthony Edwards x Travis Scott "SICKO MODE" | 50.25 to 73.86 s (23.61 s) | bar build + beat-switch reset | ghost trail, freeze clones, type flash on the drop, numeral sandwich (1st overall pick 2020), frozen last dunk |
| 03 Lamine Yamal x Don Miguelo "Y Que Fue?" | 8.0 to 37.7 s (29.7 s) | theme compilation (celebrations) + loop | flash-on-word, type flash on the hook, photo prints, giant YAMAL behind him |

### The pilot's house look (grade)
- Lumetri contrast 18, saturation 92 (from a script Lumetri saturation is 0 to 300 with 100 = normal), temperature -4,
  highlights -12, shadows -6, blacks -8; vignette 28; grain 3; bloom threshold 86, radius 60, intensity 0.16 (a softer
  bloom had turned the pitch neon). B&W chapter: saturation 0, contrast 40, exposure -0.4, with 12 fps Posterize Time;
  colour returns through a light blow-out. Grade and vignette sit BELOW the transitions.
- Research rule for colour as structure: one colour or overlay family per edit; B&W or a tint for a quiet bar, colour
  back on the drop; change the flash colour per hit; end on a B&W card; then-vs-now grade (B&W past, colour present).

### Type
- Coolvetica Heavy Comp (titles, lyric words, type flash), Galano Grotesque Black (numbers, outline numerals), Proxima
  Nova Semibold / Extrabold (captions, labels, the hit list). Real font widths from `typeset.py`; text y is the baseline
  (capitals rise about 0.72 x size above it).
- Research type rules: one typeface family plus one accent colour per edit; premium faces = ultra-condensed heavy
  grotesque (Druk / Anton class), wide heavy italic, high-contrast serif, script signatures; a giant surname 2 to 3x the
  frame width cropped by the frame edge; fill on the kick, outline on the snare. Avoid default caption templates
  (Montserrat + yellow keyword + emoji), type on the face or body, a new font every shot.

### Sound
- The song is the product; SFX only add weight to cuts. One procedural SFX family per edit, mixed 11 to 25 dB under the
  song: whoosh_up 0.36 s before the drop at -15 dB, impact 5 ms before the drop at -13; whoosh_short 0.15 s before each
  optical transition at -20; glitch 0.03 s before strobe recipes at -25; whoosh_short 0.2 s before flash panels at -20;
  impact 5 ms before each number slam at -21; riser 1.2 s before the strike at -21; impact on the ball in the net at -11.
  No audio complaints after v5.
- Every footage layer (and every duplicate) carries its own audio in AE: set `audioEnabled = false`, and verify by
  subtracting the song after cross-correlating for the AAC delay (v4 had clip audio as loud as the song: "A MAJOR BUG is
  audio").
- Research ideas, untested: built silence (-5 dB with treble cut for 4 or 8 beats before a big hit; audio off for 2
  frames at a beat switch; on fight endings music out a beat early over room tone: "the silence is what people replay");
  "kick = cut, snare = flash, 808 = shake" has no source (folklore: test by ear).

### Cutting rhythm and density
- Premium football edits cut 0.6 to 1.3 times per second; 40 to 75% of shots last 3/4 to 3 beats (Messi SHOCK and Boom
  Shaka cut only 0.6/s with 2 to 4 beat shots); mograph strobe edits are the exception (3.8 cuts/s, 84% of shots under
  3/8 of a beat). "Flashy" does not mean more cuts: the flashiest edits hold shots and fill them with effects.
- Effect density, measured on the picture band (crop the bars first or every white frame is hidden): aim 20 to 35% of
  frames in a transition or effect state, a transition on every cut, about 5 white frames per 10 s, 25+ colour bursts per
  10 s. v5 was about 1% (it read as basic); top three references 108 to 116 blur/transition frames and 6.3 to 10.8 white
  frames per 10 s; v6 27.8 and 10.6. Vary density by section: the densest stretch is the payoff zone.
- Sync the transition's PEAK to the hit (white frame, streak peak, fullest panel on the beat): blow-out white frames at
  -1 / 0 / +1; flash panels fullest on frame 0; strobe recipes start on the hit.
- Lyric moments beat drum hits when the words matter (edit 01: 13 of 24 cuts on strong drum hits, the rest on lyric
  words). Title and lyric words use Whisper word times floored to a frame; cuts use the strongest hit.
- Opening: frame 1 already moving on the downbeat, one beat before the move (starting at the start of a play is "the most
  common amateur tell"); a quiet open beats a shouted one; a famous face in frame 1; the song's hook is the first visual
  hit (41% of 69 YouTube edits have their most-replayed moment in the first 10%).
- The payoff is a dense 2 to 10 s zone at 55 to 70% of the runtime (replay data shows two peaks: the first second and
  55 to 70%; our Mbappe drop sits at 20%).
- Endings resolve on a section's last downbeat plus one held bar, with a 0.6 s fade.
- Loop ending (research): a 13 s loop found at 8.5M; edit 03 opens and ends inside the same smirk shot. Make a 13 s loop
  version of every edit (not tested yet).
- For a song promo the song is audible from frame 0: run its intro under any quote or use a wordless stare.

### The effect vocabulary, with status
| Effect | Status |
|---|---|
| Number or word behind the player + 1-frame white silhouette (+ a thin gold rim) | KEEP, loved (v3: "at 22 the effect i REALLY like") |
| Picture in the 1080x800 band, type in the bars | KEEP, his ask (v3) |
| Title in the top bar word by word, his head popping out over it | KEEP (v4: "this is good") |
| Story-in-numbers motif with captions | KEEP (built from his favourite) |
| White silhouette strobes, inverse strobe | KEEP |
| Flash panels (flashGrid: bars, halves, bands) | KEEP: his definition of geometry; v8 unreviewed |
| Silhouette strobe stack "WFIK" | KEEP (not flagged in v7) |
| Light blow-out, zoom rush, line-art strobe recipes, invert flickers, RGB split, defocus, short vertical smear | KEEP (in v8, not flagged; defocus "okay") |
| Negative strobe into B&W + 12 fps posterize inside | KEEP (v5 on) |
| Speed ramps, punch, shake, payoff lyric words | KEEP |
| Light painting | ONLY short (the 6 to 7 s one was "TOO long"; the one at 25.7 s stayed, cut under half its length) |
| Zoom cut with radial blur as the main transition | DROPPED as main ("better than zoom"); still used inside zoom rush |
| Whips / swipes showing mirrored or static frames | DROPPED ("looks ass") |
| Charging battery motif, the GIFT word, the lock-on ring, a black breath frame | DROPPED (v3) |
| Spin / rotate, checkered or box glitch, closing shutter | DROPPED ("PowerPoint") |
| Colour floods, long sideways smear, red lens streak | DROPPED (v6) |
| Aura (glow outline / energy around the player) | BANNED ("do not do auras of this type", "REMOVE the aura ik its popular but its ass") |
| Light crack + flying strips, silhouette burst iris | DROPPED (v7: "look bad") |
| Full white frame on the payoff moment | DROPPED (it hid the ball going in) |
| Cut-out "pop" (white rim + dim) | dropped in testing (pale wash) |
| Impact frames, poster silhouette, type flash, freeze clone, ghost trail, pop freeze, photo print, numeral sandwich, hit list, stutter, flash-on-word, loop ending | UNREVIEWED (wave 1) |
| Glass shatter, depth-map strobe, material strobe, 3D word, world swap, rays shake | NOT BUILT |

### Recipes (exact values)
- **Number or word behind the player (`plankit.number`):** GalanoGrotesque-Black (or Coolvetica-HeavyComp for names) at
  400 to 560 px (760 for a name); x from his head in comp pixels (`automatte.comp_point`), the glyph centre near the top
  of his head (lift 0 to 0.3 x glyph height), kept 12 px inside the band and 30 px from the frame edge, centred when wider
  than 1000 px; slams in from 128%; a coloured depth copy (garnet, grey or red); on its first frame a white silhouette
  (frame 0, glow 45) plus Exposure +0.5 for 0.18 s; a caption in the bottom bar; impact SFX 5 ms early at -21 dB. The
  thin gold rim allowed: matte grown with Minimax (grow 7) plus glow 45, gold [1, 0.78, 0.15], on the celebration only.
- **Title in the top bar:** Coolvetica-HeavyComp sized by `typeset.fit` to 990 px wide, words gap 0.22 em, baseline
  y 540, depth copy red [0.78, 0.06, 0.12], slam from 135%, each word on its sung time (floored to a frame); the clip's
  cut-out is re-laid ABOVE the bars for the title's span (pop-outs) with no mirrored band extension.
- **Lyric words in the bottom bar:** Coolvetica-HeavyComp 96 px, shade 0.6, slam from 140%, y 1446, word times from
  Whisper. Use the one lyric that matches the picture literally, on the real event (v5 "I TOOK ONE SHOT / AND I HIT MY
  TARGET" on the real Euro 2024 goal; wave 1 "I'M REALLY A THREAT", "NO HICISTE NA'").
- **Story in numbers (pilot):** 2007 "BORN 13 JULY 2007" on "gift since birth", 304 "ROCAFONDA · MATARÓ" on "I came
  from dirt", 16 "16 YEARS 362 DAYS / YOUNGEST SCORER IN EUROS HISTORY" after the goal, 10 on "in the end". One number
  per strong hit on a lyric that earns it; every fact double-checked before posting.
- **The real goal in real time (pilot v4 on):** the wide build-up at zoom 1.55 to 1.6, then the close reverse-angle
  replay time-remapped so contact lands on the kick at 20.17 s and the ball in the net on the biggest kick of the line at
  21.02 s; remap keys [[19.96, 18.48], [20.17, 18.71], [21.02, 20.25], [21.78, 20.45]] (edit time, source time; each
  edit time then snapped to its strongest hit). 1080p broadcast wide shots go soft past about 1.8x zoom.
- **Type flash:** per frame W = a black word on a white band, B = a white word on a black band; pattern "WB";
  Coolvetica-HeavyComp 290 to 420 px fitted to the band (from the Charli xcx "Von dutch" lyric video, 8.5M).
- **Numeral sandwich (edit 02):** an outline numeral 760 px, stroke 8, gold [1, 0.82, 0.3] behind, placed with `side_x`
  on the side with more room (a centred narrow "1" behind a centred player vanished); the front word Coolvetica 220 with
  a navy depth copy ("EDWARDS"); a small tracked label in the bottom bar ("1ST OVERALL PICK · 2020 NBA DRAFT").
- **Hit list (edit 01):** names struck one per hit (TUBBS, BIGGS, BERBICK, ETIENNE, SELDON from the compilation's own
  captions): ProximaNova-Extrabld 46 px, tracking 260, a red bar [0.9, 0.06, 0.1] 16% of the type size thick wipes across
  in 2 frames on the strike time, the name dims to 55% over 3 frames.
- **Ghost trail (edit 02):** 6 cut-out copies, copy i delayed by i x 0.05 s (`valueAtTime(time - dt)` on remap), opacity
  70 x 0.78^i, Tint 70%, Exposure +0.8, a live cut-out on top; all snap off at the end time.
- **Pop-up cut-out freeze (edits 01, 02):** freeze 8 to 14 frames; frozen background Gaussian Blur 0 to 26 and Exposure
  0 to -1.1 over 3 frames; cut-out scale 100 to 114 to 110% about his head over 4 frames with a soft drop shadow; white
  frames at 90% then 35% on frames 0 to 1.
- **Freeze to photo print (edit 03):** cream paper [0.93, 0.92, 0.88] band solid; the held frame masked with 8% side and
  9% top margins; rotation 0 to -2.5 deg and scale 108 to 100% over 3 frames; drop shadow; label ProximaNova-Semibold
  30 px tracking 340; one white frame at 95%; about 12 to 13 frames long.
- **Stutter strike (edit 01):** `plankit.stutter_rk` plays rep frames, jumps back and repeats, keys on exact frame times,
  no frame blending; once per edit.
- **Velocity ramps:** `ramp_rk` = a Gaussian speed dip around the anchor (v_far 1.1 to 1.4, v_near 0.35 to 0.4, width
  0.10 to 0.14 s, keys every 1/15 s, source time pinned to the anchor so the skill frame lands exactly on the hit).
  Research: base 30 to 40% speed, ramp 20 to 30 frames into and out of each hit, slow on the wind-up, real time on
  contact.
- **Colour pop:** only on a shot with visible background (on a tight close-up it is invisible): adjustment layer Lumetri
  saturation 0, contrast 25, the colour cut-out re-laid above it.
- **Flash panels (flashGrid, his "geometry"):** the band split into n panels (columns or rows); each frame lights a set of
  panels at 100% with HOLD keys and crisp edges; the fullest frame is frame 0 = the beat; panels still lit at the end fade
  over 4 frames into the next shot. Patterns (`build_edit.grid_seq`): `fill` (one more panel per frame, start n-1 frames
  before the beat), `fill_rev`, `fill2` (two per frame), `centre` (middle outwards), `alt` (odd, even, all), `pass` (a lit
  block passes over the cut; his Mbappe halves = `pass` with n = 2 rows, no fade), `unfill` (full on the beat, panels
  switch off one by one to reveal the shot). Used in v8: 7 vertical white bars `fill` n = 7 (7.7 s); cream halves `pass`
  n = 2 rows, colour [0.94, 0.94, 0.88] (13.7 s); 5 horizontal white bands `fill` n = 5 into the goal (18.6 s); `unfill`
  n = 7 two frames after a type flash; `centre` n = 7 cream.
- **Frame-recipe language (one character per frame, all band-size, 1 frame each):** E line art on white (Exposure +1.2,
  contrast 45, Find Edges, B&W, Levels in-black 0.2 / in-white 0.78); K glowing lines on black (E + Invert, Levels 0.3 /
  0.9, optional Tint, glow 30 / 18 / 0.6); I colour negative; N mono negative; B hard B&W (contrast 70); W white; X black;
  S / H bright vertical / horizontal streak (Motion Blur 300 px, Transform scale 180 on one axis, Exposure +3.5 offset
  0.22, B&W); D dark streak (Exposure -6.5); C colour streak (Exposure +2.3, Lumetri sat 220 con 55); Z zoom-blur burst
  (scale 130, CC Radial Fast Blur 90, Exposure +0.5); T impact frame (Threshold 0.43 = 110/255); V inverted impact frame;
  R Y U G P O colour solids at 86% with the picture ghosting through; "." untouched. In use: "EKEK" (gold lines
  [1, 0.85, 0.3]), "EKEKSD" into a B&W chapter, "SDSDCC", "EKE" on the strike, "VT" on contact frames, "I" and "I.I"
  flickers, "N" inside B&W.
- **Silhouette strobe stack codes:** per frame F = a flat field colour + the next shot's player as a white silhouette;
  I = white field + the player in the field colour; K = black + white player; W = white; P = white field + BLACK player
  (poster); field maroon [0.62, 0.05, 0.18]. Built as band solids plus solids LUMA-matted by the clip's SAM 2 matte. v7/v8
  at 6.43 s "WFIK"; wave 1 uses "PK" and "PPK".
- **AE layer order for the band layout (bottom to top):** footage; type behind + cut-out; silhouette strobes; section
  looks; the grade and vignette; hit layers (punch, shake, zoom cut); bars; bar type; pop-outs; front type; flashes and
  transition frames on top. The grade sits BELOW the flashes: a grade or vignette over a flash turns flat white into a
  grey gradient (the training round moved it down; an earlier version of this list had the grade on top). Motion Tile (output height 170%, mirror) on each footage layer, never on an
  adjustment layer; pop-outs above the bars never carry the mirrored band extension; flashes are band-size solids;
  Exposure works in gamma space (white and golden frames are colour solids; never stack Exposure + Glow + Screen).
- **Next techniques queued (from research pass 2, with taste risk):** depth-map strobe or fog (1 to 2 frames of a grey
  depth map on the snare; needs a free depth model and his OK to install), material strobe (only the cut-out turns
  halftone or hatch for 2 to 3 frames), a 3D extruded word behind him (Blender 5.1 is installed), a world swap behind the
  cut-out for 0.5 to 1 s per drop, rays shake (CC Light Rays on the head 0 to 250 to 60 plus a +/-40 px, +/-2 deg jolt
  over 8 frames), an anamorphic streak (8 px white solid, Fast Box Blur 250 horizontal, Add, swept in 4 to 6 frames), a
  pose-match flash cut (1 white frame + Camera Lens Blur 50 to 0 and scale 108 to 100 over 6 frames), glass / hex
  refraction (CC HexTile, 6 to 10 frames), time slice (under 12 frames, it can read as "blades"), a masked soft twitch
  (only the player jolts 2 to 8 frames), halftone ripple. Glass shatter was studied but not built.

### Structure library (`edits-kit\STRUCTURES.md`, 12 bases; pick one base per edit)
1 progress motif, 2 quote-first tribute, 3 two-act graphic to real, 4 single reveal, 5 steady pulse with type, 6 sequence
callback, 7 mograph strobe, 8 hook burst + slow section, 9 lyric story / mirror, 10 fight cold open, 11 bar build +
beat-switch reset, 12 theme compilation + loop. A "how to choose" table keys on song hook, quote, iconic visual, era
story, repeating drop, loop length and literal lyrics. He asked to "REALLY try to understand structures of edits... mix
and match andsee what fits best ACCORDING to the edit".
- **Progress motif rules ("DNA lights", Bela Films Verstappen x Kendrick):** start lights 2 / 4 / 5 at 13.97, 17.31,
  20.69 s, each 0.7 to 0.8 s, 3.3 to 3.4 s apart, a 0.3 s loudness breath at 13.85 s before the first: 3 to 4 inserts of
  0.6 to 0.9 s spaced 3 to 4 s, released within one beat of the last state. The prop must come from the subject's real
  world (the battery was rejected).
- **Translate the hook and match a real gesture to it:** "¿Y qué fue?" ("so what happened?", a taunt) lands on his
  arms-wide shrug, the repeat on his hand to the ear (Whisper times "¿Y" 14.92, "QUÉ" 15.60, "FUE?" 15.82).
- **An athlete really using the song is the strongest seed** (Yamal walking out to "Y Que Fue?" coincided with Shazam #2
  worldwide): check whether the subject has used the song before choosing the pairing.
- **More bases to try next:** a 13 s duo loop (Malik Messi & Yamal, 8.5M in under 3 months), idol x famous fan, a
  velocity edit (every clip 30 to 40% speed), an end payoff (strongest image on the loudest hit in the last 2 s; only 3 of
  69 edits peak at the end), a manager / legend persona on UK rap (Mourinho x "Pressure", 4.3M), then vs now (B&W past,
  colour on the drop), a ranked countdown (real data only), a meme template (a 1 s copyable action on the hook), a
  two-song switch, a skit or question hook, a world-swap metaphor.

### The starting point: GASS x Mbappe v1 (Kanishk's own edit)
- Nemzzz ft. Travis Scott "GASS", 20.6 s, 1080x1920, 30 fps, 618 frames, made in Premiere; 13 renders in
  `C:\VISION\MUSIC\FOOTBALL\Renders`, project `Football edits.prproj` (sequences "gass mbappe" = v1, "GASS MBAPPE
  FINAL"). All 12 full renders are frame-identical except 2.4 to 4.6 s; only v1 (and the 21 Sep "final") has the
  music-video whip build, the "MBAPPE 10" back photo and the GASS logo slam ("v1 was the most").
- Measured: 26 shots, median 0.62 s; after the drop 19 shots averaging 0.7 s; 65% of big frame changes within 1.5 frames
  of a kick, snare or onset (52% of cuts on strong hits vs 24.7% chance); about 1.2 flash / strobe / wipe events per
  second; the 1080x800 band leaves 58% of the screen black; drop at 3.3 to 4.1 s (20%); the last 3.2 s a static Spotify
  card.
- Signature: 1-frame white silhouette strobes (0.03, 0.93, 1.73, 9.43 s), an inverse strobe (9.9 s), white frames on
  kicks (4.07, 10.30 s), 3-frame light-bar wipes, dip-to-white on 5 cuts, a wave-warp + glitch + grain texture pass.
- Gaps: no ramps, no zoom punches after the drop, no captions or type, one grade, roto stops at flat silhouettes, a weak
  first second, a static end card.
- **How he built his effects in Premiere (read from the .prproj):** white silhouette strobe = a 1-frame copy of the clip
  on the track above, a mask around the player, VR Glow, Opacity blend mode, on 2 to 3 frames with 1-frame gaps; inverse
  strobe = the same with the mask inverted (the background flashes white, the player stays); Impact Dip To White
  (4 frames) on 5 cuts plus 1-frame white frames on kicks; light-bar wipe = a 3-frame graphic of Noise + Shape with Crop
  keyframes; mirror-edge zoom / spin = Transform + 4x Mirror + Transform inside nests; texture pass = Black Video with VR
  Digital Glitch + Wave Warp + Lumetri + Noise over 3.2 to 17 s (visible only at 100%); speed tweaks 0.86 to 1.27x so
  moves land on beats; a 1-frame "portal" frame; the end card shaken by a 600-keyframe shake preset that settles in 4
  frames.
- His other edits (Messi "Confidence", Knucks "Home", basketball v2 "4 Raws", Military v3 "Time Flies") share the house
  style: letterbox, light-bar wipes, B&W switches, a Spotify card.

### What the bank says (273 edits, 303 creators, 73 techniques, 59 tools; 13 Oct)
- Kinetic type is the most-used technique (98 edits), then colour grade 72, glow 60, beat cuts 57, lyric text 54. Our
  1-frame strobe density already matched the best verifiable edits. What beats us: concept, designed type, compositing,
  hook + payoff, ramps, a loop or live song-card ending; flashes and shakes are table stakes. The August 2026 "freshest
  wave": depth style (depth-map fog), rays shake, time slice, black smoke; typography and text-behind-subject are "the
  premium tell".
- Hooks beat craft for reach (inventive mograph edits often have under 3K views while hook-led Shorts get 2 to 28M); a
  band layout is fine on Reels (top Instagram edits post widescreen inside the vertical feed).

### Social and business rules
- Post titles carry the song: "Player - SONG (Artist) - Skills & Goals" (181.8M), "SONG - ARTIST (version) x SUBJECT"
  (12.6M), "[subject] x [artist]" (4.3M); link the exact audio version in the description.
- Ask clients for edit-ready versions of their song: slowed + reverb, sped up, instrumental, no-beat-switch, a clean 20 to
  30 s cut with a clear drop (38% of TikTok songs were speed or pitch modified in 2023).
- Run honest edit pages that credit the song: label-run fake fan accounts draw "industry plant" backlash.
- The business model already runs at scale elsewhere (an artist's album released as one anime-edit mix credited to dozens
  of editors, with per-track campaigns paying editors per 1,000 views; rates in research file 04, left out here).

## House look and taste rules (with the verdicts)

- **A rejection is about that placement unless he says "never":** "if u used it elsewhere and i didnt point it out there
  its fine there but here no". Blanket bans so far, his words: auras ("do not do auras of this type"), "PowerPoint"
  geometry (spins, checkered or box glitch, closing shutters), whips that show mirrored frames ("looks ass"), black
  frames, colour floods (disliked twice).
- **Loved:** the big number behind his head with the cut-out in front + the 1-frame white silhouette strobe + a gold rim
  ("at 22 the effect i REALLY like"). Build on it.
- **Band framing** like GASS x Mbappe: "its not NECESSARY that we HAVE to use full frame... like mbappe one so we can see
  more". Keep tracking calm (the v3 first frame looked janky). Everything in frame ("NOTHING is properly in frame" at the
  v3 goal).
- **No gimmick motif:** "i dont like the charging concept at all". A motif must come from the subject's real story.
- **No forced literal words:** "this gift one is there for no reason at all". Text only where it means something.
- **Type designed and textured** (depth copy, grain, sheen), a big word + a small caption, not spaced out over the face,
  not bland.
- **No black breath frames** ("black frame near 20" rejected: a breath is a quiet shot, a freeze or an audio dip), no
  reticle gimmicks ("the shot effect it just doesnt look nice").
- **Endings resolve:** "end cuts off sooner than it should".
- **Geometry done well is OK** ("even geometry ones can be done if done well... mixed with flashes"), and what he means
  by geometry is flat white or cream flash PANELS lit frame by frame: "bottom half of the screen first, then bottom and top
  half, and then just top half, and then nothing", seven vertical bars one by one, horizontal versions.
- **Too long is bad:** abstract frames hiding the picture for 10+ frames (cyan light painting, a long sideways streak); a
  red streak that "doesnt even show anything".
- **Keep the payoff visible:** no full white frame on the ball going in.
- Kanishk on the transitions so far: "Not a big fan of all the transitions yet, but a good starting point": keep the
  flashes, find "cooler shit", experiment with storytelling bases.
- **Filter research through his taste before building:** research said "use the whole vertical frame" (overturned by the
  band rule) and measured a 0.3 to 0.6 s "dip or black" breath (he bans black frames). Glows, auras and floods are
  everywhere in top edits: take their type and timing, skip the glow.
- **Never fake stats:** numbers on screen are checked facts; ask him to double-check before posting.

## Every deliverable and version, with status

### Pilot: Lamine Yamal x Tkandz "Now or Never" (renders in `edits-kit\pilot\renders\`, every version kept)
| Version | Date (UTC) | What changed | Verdict |
|---|---|---|---|
| v1 | 13 Oct 12:26 | full 9:16 reframe (detector + re-ID), battery motif 25 / 50 / 75 / 99%, NOW behind his head, 16 behind him with a gold outline, B&W "dirt" stretch, colour pop, ramps, own overlays and SFX; 28.6 s, 29 clips | self-QA only: 31% of cuts on strong hits (chance 27%), framing on defenders, a hidden cut, an invisible colour pop |
| v2 | 13 Oct 13:15 | cuts on the strongest hits, SAM 2 matte on all 33 clips, framing from the matte, whips, lock-on ring, battery over dimmed footage | self-QA: sync 54% |
| v3 | 13 Oct 13:26 | better shots, NOW / OR / NEVER word by word, ring on the strike, battery 97-98-99 on a snare roll, pop on a crowd, arms-wide end card; sync 58% | 14 notes (see review history); "do better bro do better" |
| v4 | 13 Oct 14:17 | 1080x800 band, calm framing, zoom cut with radial blur instead of swipes, title in the top bar with head pop-out, story in numbers 2007 / 304 / 16, real goal angles in real time, ends on the last downbeat + a bar (31.97 s); 1-frame-late rounding fixed; sync 62% | "this is good. but good wont cut we need GREAT"; "A MAJOR BUG is audio" |
| v5 | 13 Oct 14:43 | audio fixed; shutter, negative strobe into B&W + 12 fps, invert flickers, gradient colour flashes, true RGB split, glitch slices, spin; 3 more ramps; the payoff lyric word by word; bloom | rotate (~3 s, ~13 s), checkered box (6 to 7 s), box close (18 s) = "PowerPoint"; asked for a training round |
| v6 | 14 Oct 00:09 | an optical transition library on almost every cut (blow-out, zoom rush + chroma tunnel, smear, light painting, line-art strobes, flood, defocus, ray burst), a gold aura on the end card; white frames 0.6 to 10.6 per 10 s | mirrored head over the title (~4 s); 6 to 7 s "TOO long"; red frame at 8 s out; 9 s "okay"; stretched frame at 13 s out; 18 to 19 s "ass"; red flash on "hit my target" out; aura out for good |
| v7 | 14 Oct 02:00 | fixes; silhouette strobe stack (6.4 s), light crack into flying strips (7.7, 18.6 s), silhouette burst (13.7 s); the net moment without white | light crack and silhouette burst "look bad"; geometry = flash panels; "Almost there" |
| v8 | 14 Oct 02:12 | 7 white bars one per frame (7.7 s), cream halves (13.7 s), 5 horizontal bands into the goal (18.6 s); the silhouette stack kept | PENDING |
- Also in `pilot\renders\`: test reels `fx_test.mp4`, `fx_test2.mp4`, `fx_test3.mp4` and a range test
  `yamal_now_or_never_v8_r7.3-8.1.mp4`.

### Wave 1 (`edits-kit\edits\`)
- `01_tyson_band4band` (renders v1 to v3), `02_ant_sickomode` (v1 to v2), `03_yamal_yquefue` (v1): PENDING.

### Research and training deliverables
- **Cracked Edits Bank page** (Artifact in Kanishk's account, shared "anyone with the link"; outside viewers can read but
  not mark): https://claude.ai/artifact/SumRpyqLV6Fr5rNxEgVyj6 (db collections "marks" and "finds", both empty on
  14 Oct). Local copy `edits-bank\cracked-edits-bank.html` (858 KB).
- `edits-bank\00-our-mbappe-breakdown.md` (the bar breakdown), `edits-kit\STRUCTURES.md` (12 bases),
  `edits-kit\STUDY.md` (training round: 30 references measured at frame level, 10 optical transitions rebuilt over 8
  compare rounds, a side-by-side proof sheet, a test reel, a density table v5 vs v6), `edits-kit\RESEARCH_V2.md`
  (research pass 2: bases, ranked techniques, rules, wave 1).

## Review history, round by round

- **13 Oct, WHAT phase:** frame-by-frame study of GASS x Mbappe (all 618 frames + the .prproj); 9 parallel research lanes
  (football, basketball / US, combat / F1 / other, AMV / edit scene, captions / type, effects catalogue, roto /
  compositing, sync / structure / virality, tools / packs) plus a reader of two older edit-research Artifacts, merged
  into the bank page. Kanishk asked for frame-level inspection ("things happen for 1 frame").
- **13 Oct, HOW phase:** no paid tools ("build them yourself... make it re usable"); really understand structures. Free
  installs approved with name, source and size (refs about 250 MB, PyTorch + SAM 2 3 to 4 GB; RIFE + Real-ESRGAN about
  100 MB planned, not installed). Disk was 28 GB free; he freed it to 105 GB.
- **v3 review (13 Oct, 14 notes):** full frame not needed ("like mbappe one"); a janky first frame; swipes "look ass";
  text spaced out and bland; "i dont like the charging concept at all"; GIFT forced; a black frame near 20 s; the strike
  effect bad; nothing in frame at the goal; "at 22 the effect i REALLY like"; the end cuts off. "do better bro do better".
  Done: v4 (each note mapped to a change in the report).
- **v4 review (13 Oct):** "this is good. but good wont cut we need GREAT"; better transitions than the zoom; "A MAJOR BUG
  is audio" (clip audio mixing into the song); cooler transitions into the B&W at about 8 s. Done: v5.
- **v5 review (14 Oct):** rotations, checkered box, box close = "PowerPoint"; "Anything flashy is good. Anything crazy is
  good. Anything basic is bad."; asked for a training round (the edit not the focus). Done: the training round
  (`STUDY.md`, 8 more refs, `moments.py`, `compare.py`, `fx_lib.jsx` with 10 optical transitions tuned until they
  matched the reference frames), then v6.
- **v6 review (14 Oct):** see the table; "REMOVE the aura ik its popular but its ass"; "even geometry ones can be done if
  done well... mixed with flashes"; "if u used it elsewhere and i didnt point it out there its fine there but here no".
  Done: v7.
- **v7 review (14 Oct):** "I don't like the light crack or the silhouette burst"; his geometry = flash panels; "Almost
  there"; "build new edits after this". Done: v8, then "go through the research once again properly. You didn't research
  all of them": 5 readers re-read all ten lane files (about 665 KB) end to end, filtered by his taste, into
  `RESEARCH_V2.md`; 8 new techniques built and tested; wave 1.
- **v8 and wave 1:** pending.

## What went wrong and the fix

| What broke | Cause | Fix | Rule now |
|---|---|---|---|
| AE scripts silently did nothing; then the runner called a good render a crash | the scripting pref was reset by an update; AE 26.5's Home screen ignores `AfterFX.exe -r`; the console launcher runs as AfterFX.com | the user ticked the pref; `AfterFX.com -r`; the runner checks both process names | a file-writing ping first (poll every 30 s until it writes; read the prefs file from disk while he uses the PC); scripts log START; stop after 150 s with no START |
| A runner patch did not apply | the file was edited without reading it first | stopped the render, patched again | grep that a patch landed before relaunching |
| Wrong or ignored effect values | script scales differ from the UI (Lumetri saturation 0 to 300, Threshold 0 to 1, Shift Channels menu 1 to 10 with 10 = Full Off); Exposure works in gamma space | 92; 0.43; 10; colour solids or the Offset param | probe doubtful params with a Ramp solid + `saveFrameToPng`; keep `effects_params.txt` per install |
| Clip audio mixed into the song (v1 to v4) | every footage layer and duplicate has audio on | `audioEnabled = false` in `clip()` | subtract the song from each render after cross-correlating for the AAC delay |
| A third of cuts and hits one frame late (v1 to v3) | 4-decimal times land after the frame time | `snap_plan` | snap every event to the frame minus 0.1 ms |
| Cuts only at chance on strong hits (v1 31% vs 27%); edit 02 report "5/19 cuts on a strong hit" | a fixed beat grid vs a swinging performance; strengths scaled to the loudest hit (the beat-switch drop) | strongest-hit snap (54 to 62%); per-section scaling still open | report sync before rendering; normalise strength per loudness section |
| Framing or matte on the wrong person (defenders, a sliding keeper, a team-mate's arm, other kits) | the detector picks the largest body; an auto box merged two people; the re-ID gallery learned the Barça kit | CLIP re-ID, then framing from the SAM 2 matte; a hand `--box` at a named time | check `planview` before rendering; the prompt is part of the matte cache key |
| A hidden cut inside a catalogue "shot" (pilot, edit 03) | the shot split misses some cuts in packs | `cutcheck.py`, use the clean half | check every chosen source range |
| Type problems (front words hidden by the cut-out, NOW behind his hair, overlapping words, NOW at the top edge, a caption off both edges, a hollow "1" invisible) | layer order; no headroom; guessed widths; y treated as centre; tracking 380; a centred narrow glyph behind a centred player | front words after cut-outs; the title in the top bar; `typeset.py`; baselines; `fit_caption`; `side_x` | real font metrics and type boxes in `planview` |
| Colour pop invisible | a close-up with no background | a crowd shot | pick pop shots with visible background |
| Junk on screen (one frame of another shot, a fan-pack watermark, fighter names, a "Round 2" bug, 4:3 side bars) | source footage | an edge checker; frame low at zoom 1.2; `keep_above` zoom 1.35 to 1.6; active-area crop | inspect packs frame by frame around every use |
| Transitions came out as blank white frames (training rounds 1 to 2) | Exposure + Glow + Screen stacked on the same frames | per-frame recipes, colour solids, grade below the transitions | measure L / S / C per frame against the reference |
| GPU out of memory; a squashed picture; a mirrored head over the title (v6) | a 9000% Transform stretch of edge rows; Motion Tile on an adjustment layer; band extension on pop-outs | Motion Tile (170%, mirror) per footage layer; `BAND_EXTEND` off for pop-outs | toolkit defaults in `clip()` |
| Clones hidden under a paper solid | `duplicate()` lands directly above its source | `moveBefore` | re-stack after every duplicate |
| A round-5 build crashed; shell patches broke | a Python name clash; apostrophes in shell appends, backslashes in heredocs | renamed; patches as script files | never patch through shell strings |
| The SAM 2 install started re-downloading PyTorch (2.7 GB) | pip build isolation | deps first (setuptools, wheel, hydra-core, iopath), then sam2 with `--no-build-isolation --no-deps` and `SAM2_BUILD_CUDA=0` | install deps first |
| Downloads failed (five vertical refs, 4K re-downloads, tools tripping on file names) | a size filter that assumed landscape; YouTube's bot check after about 40 downloads; emoji and special characters | an orientation-neutral limit; waited and asked for 4K packs; ASCII rename (`fNN_name.mp4`) | one download at a time, rename on download |
| The catalogue sheet showed the wrong shots | an ID list read as a CLIP text search | explicit `ids:` / `q:` / `from:` selectors | explicit selectors |
| The bank parser dropped entries | lane files drifted from the format | parser fixed, duplicates merged | the parser prints a per-file report; the brief fixes the format |
| Two lanes shared a scratchpad and one overwrote the other's helper | no own folder per agent | separate subfolders | give each agent its own subfolder |
| The shared WebSearch budget (about 200 per turn) ran out in every lane | one budget for all agents | split searches over turns or use yt-dlp YouTube search | plan search-heavy work across turns |

## Open items and next steps

1. **Reviews pending:** v8 (flash panels) and wave 1 (01 Tyson v3, 02 Ant v2, 03 Yamal YQF v1). Carry the winners into
   the next wave.
2. **Check the halves order:** he described his Mbappe flash as "bottom half of the screen first, then bottom and top
   half, and then just top half, and then nothing"; v8 uses `pass`, which lights the top first. The Mbappe edit has both a
   down (5.57 s) and an up (12.30 s) light bar. Confirm against his frames; flip if needed.
3. **Sync report normalisation** per section for songs with a beat switch (edit 02).
4. **Next wave bases:** velocity edit, end payoff, then vs now, a 13 s duo loop; a 13 s loop cut of every edit.
5. **Not built yet:** glass shatter, depth-map strobe / fog (needs a free depth model and his OK to install), material
   strobe, a 3D extruded word (Blender), world swap, rays shake, RIFE slow-mo and Real-ESRGAN upscaling (planned 13 Oct,
   not installed).
6. **4K footage:** YouTube blocked 4K re-downloads; `pilot\footage4k\` is empty. Ask for 4K packs (heavy effects on
   720p footage look cheap; top packs are 4K / 60 to 120 fps).
7. **Premiere and After Effects (decided 15 Oct 2026):** assemble music edits in Premiere; After Effects only makes the
   effect elements. The single live AE comp per edit was the old route. Kanishk's own Premiere recipes are above.
8. **Mac port** of the GPU tools, font paths and the AE runner (see the last section).
9. **Bank page:** no marks yet (do not wait on them: read the files yourself). An Instagram pass through his logged-in
   Chrome was offered and needs his explicit OK. Someone outside India (the boss) can open the TikTok leads (TikTok does
   not open from India; Instagram reel pages and `/popular/<tag>/` grids open in the browser pane without login).
10. **Footage tools:** per-sport CLIP prompts (they say "footballer", "barca", "spain" and were reused for boxing and NBA)
    and per-kit re-ID; a better shot-cut detector (dissolves, replays). Known limits: the `f2_celebrations` pack has a
    blurred watermark top left (rows 15 to 160: zoom 1.2, frame low).
11. **Facts on screen to double-check before posting:** the 2007 birth date, 304 / Rocafonda postcode, 16 years 362 days
    record, Barça 10, Tyson champion at 20, Edwards first pick 2020.
12. **Business:** ask clients for edit-ready versions of their songs.
13. **Doc fixes:** done in the kit on 14 Oct: premiere-ae-editing `transitions.md` now marks the light crack and the
    silhouette burst REJECTED, `after-effects.md` marks the lock-on ring REJECTED, and the kit copy of `STRUCTURES.md`
    says a breath is a quiet shot, a freeze or an audio dip, never a black frame. Still as written: Kanishk's own
    `edits-kit\STRUCTURES.md` on his PC, and aim 8 of the bank page ("use the whole vertical frame", in
    `bank-page/aims.json`), which his band rule overturns.
14. **Rights:** copyrighted songs and broadcast footage were downloaded from YouTube for study and for the edits
    (approved by Kanishk); scene packs (often Topaz-upscaled, from YouTube, Drive or Telegram) carry only "fair use"
    boilerplate; named-star match footage has no clean free source; labels can claim edits that use major-label songs.
    Do not redistribute the reference renders, footage, song files or lyric transcripts. Clean SFX sources: Sonniss,
    Freesound CC0 / CC-BY, Pixabay.

## Where the files live on Kanishk's PC

- **His originals (read-only):** `C:\VISION\MUSIC\FOOTBALL\` (GASS x Mbappe renders, `Football edits.prproj`, his other
  edits).
- **The bank:** `C:\VISION\VISION CLAUDE\edits-bank\`: `README.md` (index + rebuild command),
  `00-our-mbappe-breakdown.md`, `research\_brief.md` (the shared agent brief and technique tags) + `01` to `10` lane files
  (665 KB), `our-edits\sheets\` (every-frame PNG sheets), `page-src\` (`build_page.py`, `template.html`, `aims.json`,
  `our_summary.json`, `page_assets.py`, `framestats.py`, `timeline.py`, `picks.py`), `cracked-edits-bank.html`.
- **The kit:** `C:\VISION\VISION CLAUDE\edits-kit\`: `README.md` (pipeline), `STRUCTURES.md`, `STUDY.md`,
  `RESEARCH_V2.md`; `tools\` (anatomy, study, moments, compare, cmp_fxtest, catalog, reframe, reframe_check, roto,
  automatte, cuts, cutcheck, typeset, planview, qasheet, overlays, sfx, plankit, setup_edit, build_edit, yt) +
  `tools\ae\edits_lib.jsx` and `fx_lib.jsx` (ES3, need the skill's `ae_lib.jsx` first) + `tools\ae\probe\` (effect probes,
  `effects_list.txt`, `effects_params.txt` = the AE 26.5 effect and param dump); `pilot\` (song, footage, catalog, mattes,
  plans v2 to v8, test-reel plans `plan_fxtest*.py`, `plan_ttest.py`, `ae\` jsx + aep, `renders\` v1 to v8 and test reels,
  `qa\`); `edits\01_tyson_band4band`, `02_ant_sickomode`, `03_yamal_yquefue` (plan_NN.py, plan JSONs, catalog, mattes, ae,
  renders, qa); `refs\` (23 study refs, 361 MB) and `refs2\` (8 more, 208 MB); `anatomy\` (measurements of refs and
  ours); `assets\overlays\`, `assets\sfx\` (generated: regenerate with the scripts); `models\sam2.1_hiera_large.pt`
  (898 MB); `cache\`; `logs\`.
- **Memory notes (Kanishk's Claude):** cracked-edits-project, feedback-cracked-edits-taste, feedback-build-own-tools.
- **Skill updates made during this job (Kanishk's skill):** `references\transitions.md` (new), `after-effects.md`
  sections 11 to 12, `timing.md` "Music edits", `youtube-downloads.md`, `scripts\media\beats.py` and `fsheet.py` (new),
  `scripts\ae\ae_run.py` (AfterFX.com) and `ae_build.py` (START log line).
- **Do not ship or share:** all media (refs, footage, renders, mattes, overlays and SFX files, song WAVs, sheets, QA
  PNGs), lyric transcripts and song maps (`song\words.json`, `nn_words.json`, `anatomy\*_words.json`: transcribed lyrics
  of copyrighted songs), model weights and caches, generated build output (`ae\*.jsx` per version, `.aep`, logs, plan
  JSONs), one-offs (`tools\_patch_anat.py`, `tools\_rename_footage.py`, `edits\_setup_wave1*.sh`, `pilot\ae\_ping*.jsx`,
  `page-src\ouredit.json`). The research files hold per-edit fees and plugin prices (not copied here).

## Which kit skills and pipeline to use for this client

- **Pipeline:** `~/VisionKit/kit/library/pipelines/edits-kit/` (the tools, AE libraries, structure library and worked
  plans). If it is missing or older than Kanishk's `edits-kit\`, ask him.
- **motion-design:** the effect vocabulary, beat-synced "cracked" edits, the effects library and how to run it, type
  animation.
- **editing-playbook:** the taste verdict library, structure and story bases, review rounds.
- **premiere-ae-editing:** the AE runner (`ae_run.py`, `ae_build.py`, `ae_lib.jsx`, `check_jsx.py`), beats and words
  (`beats.py`, `hear.py`), `fsheet.py`, `ytdl.py` (it works around YouTube's bot check and may break YouTube's terms: use
  only with rights to the footage, the boss decides).
- **research-and-sourcing:** research lanes from one shared brief, footage and song rights, the bank.
- **social-video-formats:** edit titles, benchmarks, edit-ready song versions, honest edit pages.
- **production-automation:** the script-first, cached edit pipeline; fixing systematic misses in the toolkit, not the plan.

### How a cracked edit is made
1. **Study the reference at frame level:** every-frame sheets (60 per sheet), diff all versions to find the changed window,
   read the effect stack from the .prproj dump, run `anatomy.py` (cuts, kicks / snares, drop, motifs, sync vs chance);
   write a breakdown (timeline table, effect inventory, numbers, gaps).
2. **Build the inspiration bank:** parallel research lanes from one shared brief (who we are, the bar to beat, WHAT not
   HOW, real URLs only, "(unverified)" when unsure, metadata-only yt-dlp, an own temp folder, a reply under 150 words,
   30+ entries and 15+ creators per lane), then `build_page.py` into a filterable page with consensus picks first.
3. **Read all research and filter it through the taste list** into one list of bases and ranked techniques; note where
   research contradicts his verdicts.
4. **Choose subject and song** (best if the athlete really used it); get the audio, kicks / snares (`beats.py`), word times
   (`hear.py`) and the song's most-replayed curve (`yt.py heat`).
5. **Choose the base and the window:** one base from STRUCTURES.md / RESEARCH_V2.md; the window one beat before the drop,
   around the most-replayed stretch, ending on a section's last downbeat plus one bar; plan the hook (frame 1 moving on the
   downbeat) and the payoff zone (55 to 70%).
6. **Get and catalogue footage:** `python setup_edit.py EDIT_DIR SUBJECT --song ID --footage ID,ID` (one download at a
   time, ASCII names, catalogue, CLIP tags, subject scores, sheets, all cached). Pick moments with `catalog.py strips`
   (8 frames per shot labelled with source seconds); check hidden cuts, burned-in captions, watermarks and pillar bars
   (`active_area`, `keep_above`). About a third of fan-pack "action" shots hide the subject (pilot 110 of 167 clear,
   Tyson 35 of 67, Edwards 49 of 103).
7. **Write the plan:** `plan_NN.py` with `plankit.Edit` (about 100 lines): clips on the strongest hit, auto mattes and
   framing, the proven base set (band, number behind + white silhouette, title in the top bar with pop-out, lyric words,
   flashes, flash panels), the base's devices, 2 to 3 new techniques, hits (punch / shake / expo / silhouette),
   transitions, looks, overlays, SFX. `save()` prints the sync report.
8. **Preview framing without rendering:** `python planview.py PLAN.json OUT.png` (crops, mattes tinted red, type boxes
   yellow, the 10% / 76% safe lines cyan); fix wrong-person mattes with a box at a named time.
9. **Test any new effect first:** a test reel with one real cut per technique (1.2 s each, about 45 s render); compare
   with the reference frames (`compare.py --stats`) and tune per frame until the L / S / C rows follow the reference.
10. **Build and render:** `python build_edit.py PLAN.json [--only-test S] [--range A-B] [--final]` writes the .jsx and a
    layered .aep, rendered through the skill's `ae_run.py`; test one moment with `--range`, then the full H.264 preview;
    ProRes 422 with `--final`. Render cost for a 30 s 1080x1920 layered edit: about 82 to 120 s (slower once every clip
    carries Motion Tile).
11. **QA before showing:** anatomy on the render (sync on strong hits vs chance), moments density vs refs, qasheet windows
    at every changed moment at full size (`--crop` for ball contact or a face, `--grid` to read coordinates), a pass over
    the whole render every 1/3 s, the audio subtraction test.
12. **Deliver and review:** a report answering his numbered notes one by one, the render path, facts to double-check,
    open asks; turn each verdict into a standing rule (memory taste file, skill reference) and a toolkit default; keep
    every version under a new file name.
- House habits: one GPU job at a time (SAM 2 mattes for two edits compete for the 12 GB card), one AE, one download; stay
  off the screen when Kanishk is on the PC (check state from logs and the prefs file); close AE gracefully (`taskkill`
  without /F; never while a render file grows); GPU tools run without `python -I` on his PC (torch, sam2, open_clip,
  faster-whisper and yt-dlp live in the user site-packages; set PYTHONIOENCODING=utf-8). Wave 1 (three edits) took about
  1.5 hours to build.

### Mac notes (the boss runs Premiere and AE on a Mac; all untested)
- **CUDA is hard-coded** in `roto.py`, `reframe.py` and `automatte.py` (`.cuda()`, `device="cuda"`, bfloat16 autocast,
  `torch.cuda.empty_cache()`): use "mps" if available, else "cpu"; float16 autocast on MPS or none. SAM 2 runs on MPS with
  a "preliminary support" warning and is slower: test on a 2 s clip. `catalog.py` already falls back to CPU.
- **NVENC is hard-coded** in `roto.py` (no fallback): use `h264_videotoolbox` or libx264 (`-crf 12-14`). `overlays.py`
  already falls back to libx264.
- **Windows paths (Kanishk's originals; fixed in the kit copy on 14 Oct):** sheet labels loaded
  `C:/Windows/Fonts/arialbd.ttf` (the kit copy uses `/System/Library/Fonts/Supplemental/Arial Bold.ttf` on a Mac);
  `typeset.py` searched only Windows font folders (the kit copy adds `/Library/Fonts`, `~/Library/Fonts`,
  `/System/Library/Fonts` and `FONT_DIRS`; Adobe Fonts activated through Creative Cloud are not in these folders, so
  install the font files); `build_edit.py`, `setup_edit.py` and `study.py` hard-coded Kanishk's skill path (the kit copy
  reads `PAE_SCRIPTS`, default `~/.claude/skills/premiere-ae-editing/scripts/`); the plan scripts hard-coded the
  edits-kit path (the kit copies are kit-relative). CUDA and NVENC above were NOT changed.
- **Running AE:** the skill's `ae_run.py` takes its Mac route by itself (AppleScript `DoScript` into a running AE; it
  refuses to replace a project the user has open; premiere-ae-editing mac-notes.md). By hand: `osascript -e 'tell
  application id "com.adobe.AfterEffects" to DoScriptFile "/path/x.jsx"'` (AE open, scripting pref ticked) or render the
  saved .aep with `aerender`. These builds have not been run on a Mac yet. The libraries are plain ES3 using built-in effects (CC Radial Fast Blur,
  Motion Tile, Threshold, Find Edges, Minimax, Shift Channels, Posterize Time, Exposure, Lumetri, Glow): re-run the effects
  probe on his AE to confirm matchNames and render template names.
- **Python:** a venv with PyAV, numpy, Pillow, torch + torchvision (Mac wheels), sam2 from Meta's repo with
  `SAM2_BUILD_CUDA=0`, open_clip_torch (downloads ViT-L-14 weights on first run), faster-whisper (CPU int8 is fine),
  yt-dlp[default] + the PO-token server (Deno), ffmpeg (Homebrew).
- **Needs his own:** the YouTube download setup (yt-dlp + PO-token server, no account), the SAM 2 and CLIP model
  downloads, Adobe licences, font licences (Coolvetica, Galano Grotesque, Proxima Nova).
