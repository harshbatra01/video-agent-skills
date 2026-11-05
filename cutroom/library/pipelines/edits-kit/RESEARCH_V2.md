# Research pass 2 (14 Oct 2026): every lane of the bank, re-read in full

All ten lane files (about 665 KB) were read end to end by five parallel readers; this is the merged result, filtered
through the user's reviews (what they loved, what they rejected). Use it to plan new edits: one storytelling base per
edit, the proven base set in every edit, and two or three new techniques on top of it.

## A. Proven base set (in every new edit)
- Picture in the 1080 x 800 band (his GASS x Mbappe look), black bars for type.
- Cuts on the strongest kick / snare, 0-1 frame early (tools/cuts.py).
- The big number / word BEHIND the player with a 1-frame white silhouette strobe (the effect he loved most).
- White flashes and his flash panels (bars / halves lit frame by frame, fx_lib flashGrid).
- Invert flickers, zoom rush, line-art strobe (E K E K), title in the top bar with his head popping out, lyric words
  in the bottom bar on the sung syllables.
- Never: auras / glow outlines, colour floods, long abstract holds (10+ frames), rigid geometry (spins, slides, box
  glitches, blades), gimmick metaphors, black breath frames, fake stats.

## B. Storytelling bases to experiment with (new ones marked *)
| Base | Shape over time | Reference | Fits |
|---|---|---|---|
| * Fight cold open / silent stare-down | 0-3 s quiet line or wordless face-off; hard cut on the beat into the walkout; exchanges get shorter; white flash on the connecting punch at ~70%; freeze on the reaction, music out a beat early | Twoc_ "AURA IN UFC" (3.2M) | boxing, UFC (under-served) |
| * Bar build + beat-switch reset | 0-2 s face; one play per bar, escalating; reset at ~50% (flash / freeze, 2 frames of audio drop, new grade); clips half as long; biggest play, freeze, hold a beat past the music | Itai Rosen Ja Morant (2.6M) | NBA on Travis / Carti |
| * Theme compilation | one kind of moment (celebrations) across the edit, song title in the post title, peak in the first second | Yamal x "Y Que Fue?" (181.8M) | Latin / slowed funk |
| * 13 s duo loop | all hook, built to loop | Malik Messi & Yamal (8.5M) | mentor / heir pairs |
| * Idol x famous fan | the second famous face in the first second | sanchezae Speed x Ronaldo (2.5M) | streamer + athlete |
| * Velocity edit | every clip 30-40% speed, ramps up 20-30 frames before each hit | Mr.Nobody "One Dance" (1.4M) | skills on smooth tracks |
| * End payoff | the strongest image on the loudest hit in the last 2 s | Panthox Ronaldo | verses that end on a hit |
| * Manager / legend persona | touchline and press-conference persona on UK rap | phaseaix Mourinho x Pressure (4.3M) | managers |
| * Then vs now (grade as story) | B&W past, colour present, colour released on the drop | NBA on ESPN | legacy players |
| * Ranked countdown | a counter / badge per hit over highlights (real data only) | Messi MEMORY REBOOT | record-holders |
| * Song-hook loop / meme template | a 1 s copyable action lands on the hook | Lamar Jackson "Rolex" (7M+) | chant hooks |
| Quote-first tribute | soundbite with keyword captions, then the montage | Jordan "SDP Interlude" | quotable players |
| Progress motif | a real prop returns and advances (start lights) | Bela Films "DNA" | sports props |
| Single reveal | slow push to one iconic image | Gojo "Eyes" (4.4M) | slowed tracks |
| Mograph strobe | designed poster frames every 2-3 frames | lanzdoesvisual "4 x 4" | 8-12 s hype loops |

## C. New techniques, ranked for his taste (build order)
1. Impact frames: on the contact frame, 1 frame hard B&W threshold inverted (black player on white), then 1 frame
   normal threshold, then colour (anime impact frames; "Mob's Tea Party", Anime Expo 2025 winner).
2. Inverse silhouette poster: 2-3 frames of white with the player as a solid black silhouette (yunsuv "BLACK OUT").
3. Type flash: one giant ultra-condensed word on flat white for 2-3 frames, inverted on the next beat (Charli xcx
   "Von dutch", 8.5M): the flash carries the lyric.
4. Numeral sandwich: a hollow / translucent numeral behind him, a heavy word IN FRONT, a small tracked label (EK
   "That ONE LeBron James Edit"): his number trick with three depth layers.
5. Freeze clone: across one bar a frozen copy of the cut-out stays on each beat; all vanish on the white strobe at the
   downbeat (Gatorade "FOREVER").
6. Ghost trail: 6-8 fading copies trail one move, snapping off on the beat (Peter Sarellas NBA promo look; rare in
   short edits).
7. Stutter strike: the contact frame repeated in 1-3 frame bursts over a snare roll, once per edit.
8. Pop-up cut-out freeze: freeze, the player pops forward 100 -> 114 -> 110% while the background blurs and darkens,
   a white frame, a jolt, release (FicTic trend).
9. Freeze to photo print: freeze, 1 white frame, a white-bordered print of the moment with a small label (AZgoat
   "Coldest moments x Photos", 5.1M).
10. Giant surname behind (2-3x frame width, cropped by the frame edges, F1 opening titles) and a type wall (rows of the
    name sliding opposite ways behind him, yunsuv).
11. Flash-on-word: 1-2 frame exposure pops on the sung syllables (the "Espresso" edit): the song becomes the hero.
12. Rays shake: light rays from the player's head on the kick plus a sharp jolt (Aug 2026 trend).
Later (need more set-up): depth-map strobe / depth fog (needs a free depth model), material strobe (only the
cut-out turns halftone for 2-3 frames), 3D extruded word (Blender), world swap behind the cut-out.

## D. Rules from the structure research
- Two replay peaks: the first second and 55-70% in; the payoff is a dense 2-10 s stretch, not one hit.
- Frame 1 already moving on the downbeat, one beat before the move (starting at the start of a play is the amateur
  tell). Quiet openers work; shouted ones have nowhere to go.
- Flash at the beat switch and the contact frame; one sound effect family per edit.
- Endings: biggest play last, freeze on the reaction, hold a beat past the music (or music out a beat early over room
  tone); make a 13 s loop version of every edit.
- For a song promo the song stays audible from the start (no long spoken cold opens over silence) and the song title
  goes in the post title.

## E. Wave 1 (first three new edits)
| Edit | Base | Subject x song | New techniques on top of the base set |
|---|---|---|---|
| 01 | Fight cold open | Mike Tyson x Central Cee + Lil Baby "BAND4BAND" | impact frames, inverse silhouette poster, stutter strike, pop-up freeze |
| 02 | Bar build + beat-switch reset | Anthony Edwards x Travis Scott "SICKO MODE" | freeze clone, ghost trail, type flash, numeral sandwich |
| 03 | Theme compilation (celebrations) | Lamine Yamal x Don Miguelo "Y Que Fue?" | flash-on-word, freeze to photo print, giant surname behind, 13 s loop |
