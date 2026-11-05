# Study notes: what top edits do, frame by frame (14 Oct 2026)

Training round after the user's v5 review ("rotate / checkered box / box close transitions = PowerPoint; anything
flashy and crazy is good, anything basic is bad"). 30 reference edits (refs/ and refs2/: Hero Edit, sanchezae, Jissoho,
P3DITS, Shadey, Bela Films and more, plus a 12-minute TikTok/Reels football compilation) were measured and their most
intense moments laid out frame by frame. Then every transition was rebuilt and compared against the reference frames
until the numbers matched.

## Tools made for this (all in tools/)
| Tool | What it does |
|---|---|
| `moments.py VIDEO OUT` | finds an edit's 8 most intense 12-frame windows (cuts, flashes, inverts, blur, colour bursts) and lays out every frame; JSON with per-edit counts |
| `compare.py OUT PAIR... --stats` | ours vs the reference moment, frame by frame, same height, plus per-frame L/S/C (mean luma / structure / colourfulness) |
| `cmp_fxtest.py TAG` | compare sheets + numbers for the whole fx test reel (pilot/plan_fxtest.py) against the reference moments |
| `ae/fx_lib.jsx` | the optical transition + hero effect library (below) |
| `ae/probe/effects_probe.jsx` | dumps every effect this After Effects has + param matchNames |

## 1. Flash density: the biggest gap
Per 10 seconds (moments.py): frames in a blurred / transition state, white frames, big frame changes, colour bursts.

| Edit | blur frames | white | big changes | colour bursts |
|---|---|---|---|---|
| Messi "will SHOCK you" (Hero Edit) | 108 | 8.5 | 25 | 28 |
| Messi x Boom Shaka (Shadey) | 114 | 6.3 | 11 | 27 |
| LeBron "Highest in the Room" | 116 | 10.8 | 6 | 9 |
| Ronaldo "+5 hours" (Hero Edit) | 31 | 3.9 | 30 | 43 |
| Speed x Ronaldo (sanchezae, 2.5M) | 15 | 1.3 | 46 | 69 |
| Greatest Football Edit (Blue Lock) | 20 | 1.9 | 35 | 55 |
| our v5 | 3.4 | 0.6 | 36 | 40 |
| **our v6 (library on every cut)** | **27.8** | **10.6** | 42 | 42 |
| our GASS x Mbappe | 10 | 0 | 18 | 2 |
(Ours measured on the picture band only: moments.py now crops letterbox bars, which had hidden every white frame.)

The flashiest edits keep 20-40% of ALL frames in a transition or effect state. They do not cut more often (Messi SHOCK
and Boom Shaka cut only 0.6 times a second, with long 2-4 beat shots); they put an effect on almost every frame:
every cut is a 6-12 frame optical transition and the shots in between carry ramps, glows, auras and flicker.
Our v5 was hard cuts with short adjustment hits: about 1% of frames active. That is the "PowerPoint" feeling.

## 2. Cutting rhythm (shot length in beats, 22 edits)
- Premium football edits: 0.6-1.3 cuts per second; 40-75% of shots last 3/4 to 3 beats.
- Flashy does NOT mean more cuts: the flashiest ones hold 2-4 beat shots and fill them with effects.
- Mograph edits (Hamilton x Norris 4x4) are the exception: 3.8 cuts/s, 84% of "shots" under 3/8 of a beat.
- Sync of cuts to drum hits ranges 7-83%: the strongest edits sync their TRANSITION PEAKS (the white frame, the streak
  peak) to the hit rather than the cut frame itself.

## 3. Transition vocabulary that reads as premium (with the frames it was copied from)
Every one is light, blur, colour or line art: no rigid geometry. White is 1-3 frames, the rest has structure + colour.
| Transition | Frame recipe (0 = first frame of the next shot) | Reference |
|---|---|---|
| Light blow-out | -2 hot orange, -1/0/+1 flat white, +2/+3 golden haze, +4 shot | TikTok compilation 106.57 |
| Zoom rush | 3 frames of pure radial streaks around the cut, over-zoomed + rolled arrival, settles in 7 | Speed x Ronaldo 12.53 |
| Streak smear | 8+ frames of bright vertical bars of the picture's colours (L about 180, high contrast) | LeBron 16.87 |
| Light painting | 1 white frame, then only the highlights in cyan on dark, smeared sideways, darkening | Messi SHOCK 13.37 |
| Line-art strobe | E K E K (line drawing on white / lines on black), then bright / black streak frames, then colour streaks | LeBron 41.87 |
| Colour flood | orange x2, yellow x4, red x7 with the next shot ghosting through | Mbappe Nightcrawler 20.78 |
| Defocus space | out-going melts into bright haze, in-coming starts as colour blobs on black, focuses over 12 frames | Hero Edit +5h 14.35 |
| Ray burst | 2 frames of bright desaturated rays with structure, then the shot glowing | Speed x Ronaldo 26.37 |
| Vortex | spin + zoom blur tunnel, bright and contrasty (not a twirl distortion) | LeBron 29.38 |
| Glass shatter | the frame shatters into shards at the camera (not built yet) | Greatest Football Edit 59.70 |

## 4. In-shot effects seen again and again
- Energy aura around the player (purple, pink, red, blue rims): Messi SHOCK 17.90 / 27.20, Ronaldo +3h 12.07 / 16.33.
- Big word BEHIND the player, often blurred or glowing: "GOAT" (Hero +5h 19.90), "BETTER" (Homelander 12.40),
  "NO REF" double exposure (Mbappe Nightcrawler 17.83), "16" (ours, the one effect the user loved).
- Lyric words per beat, small, ON the subject: Hamilton x Kendrick ("GAZIN", "LIFE", "LOOKIN", "FOR THA").
- White silhouette / line-art strobes on single frames; inverted frames; B&W flickers; posterized 12 fps sections.
- Heavy motion blur on every fast move (Homelander: whole shots are smeared action).

## 5. Rules for our builds (from the rounds of comparing)
1. Never stack exposure + glow + screen on the same frames: it makes blank white (rounds 1-2 failed this way).
2. Key transitions PER FRAME (the references change look every frame), and check them with compare.py --stats:
   flat white frames (S under 8) at most 3 per transition.
3. In a letterbox layout give every footage layer mirrored picture beyond the band (Motion Tile on the layer), or
   distortions pull black in. Do not put Motion Tile on an adjustment layer (it scales the whole comp into the tile).
4. Target for a flashy edit: 20-35% of frames in a transition / effect state; a transition on every cut; white frames
   about 5 per 10 s; colour bursts 25+ per 10 s.

## 6. The training loop, round by round (pilot/plan_fxtest.py, tools/cmp_fxtest.py)
| Round | What was wrong (per-frame numbers vs the reference) | Fix |
|---|---|---|
| 1 | blow-out, smear, vortex, rays = 3-4 frames of blank white; defocus muddy; shatter rendered nothing | stop stacking exposure + glow + screen; key per frame |
| 2 | still white; a twirl pulled black in from outside the band | per-frame keys, a strobe "recipe" language |
| 3 | an adjustment-layer Motion Tile squashed the picture; a 9000% Transform stretch ran the GPU out of memory | Motion Tile on each footage layer (output height 170%, mirror) |
| 4-5 | white frames vignetted (grade above the transitions); dark night footage cannot be lifted by Exposure in gamma space | grade + vignette below the transitions; white / golden / orange frames as colour solids; Exposure Offset for blacks |
| 6-8 | line-art paper too grey (Input Black was the wrong knob), streak frames too dark, light painting too bright | Input White down for clean paper, exposure + offset on streak frames, softer cyan |
After round 8 every transition follows its reference's L/S/C shape within about 10-15%: blow-out (orange, 3 flat white,
2 golden), zoom rush, streak smear, light painting, line-art strobe (EKEK SDSD CC), colour flood, defocus, ray burst,
vortex, aura. Glass shatter is not built yet (the AE Shatter set-up needs its own study).
