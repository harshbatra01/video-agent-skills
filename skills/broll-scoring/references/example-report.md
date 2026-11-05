# B-roll report: reference (Sam Altman) vs ours (v9c). 19 Oct 2026

## How it was scored
- Every shot from both videos was cut at the measured shot changes and placed on contact sheets: `report/broll/ref_sheet_01-06.jpg`
  and `ours_sheet_01-06.jpg` (one middle frame per shot, with its time, length and the words said over it).
- Measured by script (`tools/broll_sheets.py`):
  - shot times and lengths;
  - the words said over each shot (whisper on the final audio);
  - video vs still (whether the picture moves after allowing for a push);
  - sharpness (Laplacian variance, comparable only within one video).
- Judged by eye from the sheets (`report/broll/labels.py`), each shot gets:
  - what it shows and its type: clip, still, news (broadcast with a chyron), grid, gfx (built graphic) or card (text on black);
  - subject size: the share of the frame the subject fills;
  - three marks out of 5:
    - **Q** quality: sharp, clean, well lit, not mush;
    - **F** framing: the subject fills the frame and is not cut off, and the shot moves;
    - **M** match: how directly the picture supports the words said over it. 5 = the named person or the literal thing,
      4 = a clear symbol, 3 = on topic but generic, 2 = loose, 1 = wrong or misleading, 0 = placeholder.
- **Shot score out of 10 = (2 x M + Q + F) / 2.** Match counts double because it is what the reference does best. Totals are
  weighted by screen time.
- Limits: Claude judged one middle frame per shot, not playback, so a shot that changes inside itself is scored on its middle.
  Subject size is an eye estimate. The marks are one reviewer's judgement: your notes outrank them.

## Totals
| Measure | Reference (Altman) | Ours (v9c) |
|---|---|---|
| Shots | 142 | 124 |
| Length (s) | 86.4 | 81.5 |
| B-roll score /10 (time-weighted) | 8.3 | 7.5 |
| Match to words /5 | 4.24 | 3.91 |
| Quality /5 | 3.94 | 3.55 |
| Framing /5 | 4.10 | 3.55 |
| Weak shots (score under 5) | 1 shots, 0.2 s | 20 shots, 9.8 s |
| Time on shots that miss the words (match 2 or less) | 2.4 s (3%) | 13.8 s (17%) |
| Picture time where the subject fills under 20% of frame | 3% | 16% |
| Screen time: clip | 41% | 36% |
| Screen time: still | 12% | 15% |
| Screen time: news | 29% | 8% |
| Screen time: grid | 7% | 5% |
| Screen time: gfx | 5% | 8% |
| Screen time: card | 6% | 27% |


## What the numbers say
1. **The reference almost never shows a picture that misses the words: 3% of its time vs 17% of ours (13.8 s).** Its rule:
   - a name gets that person;
   - a number gets a news chyron that prints it;
   - an idea gets a fast burst of symbols at 2 to 4 frames each.

   Ours fills gaps with generic interiors and the wrong faces.
2. **News footage is 29% of the reference and 8% of ours.** The reference proves its story with real broadcasts: the event,
   the people and the number are printed on the chyron. Ours has one news clip (Fink), and the rest of the proof sits on our own
   cards. This is the biggest single gap.
3. **Small or cut-off subjects: 16% of our picture time vs 3%.** Your two notes are exactly these:
   - the gold bars, #7-8 and #109-112: the bar fills about 15% of the frame and is cut off at the bottom;
   - the court interiors (staircases, arched windows, empty rooms): 16 shots, 7.0 s.
4. **Wrong-person shots:**
   - the Greek bust (Herodotus) stands in for the shareholder twice, #31 and #70;
   - Jim Cramer stands in for "the referee of corporate America" and "$30 billion", #13-17 and #68.

   Viewers will read both as "who is this?".
5. **What already works (score 9 to 10):**
   - Musk clips on his name (#3-6);
   - the Texas flag and Capitol;
   - the law books;
   - the combination lock on "locked out";
   - the dollar bill on "$1";
   - the Giga Texas aerial;
   - the gavels;
   - the Fink soundbite.

   These follow the reference rule: literal, full frame, moving.

## How to improve (by shot, in order of payoff)
| Our shots | Problem | Replace with (reference rule) |
|---|---|---|
| #7-8, #109-112 gold bar (2.5 s) | subject about 15% of frame, cut off, dark | **Number on a chyron:** a news clip or screenshot printing Musk's net worth, then the full-frame gold stack we already use at #91 (90% fill). Fill rule: the subject fills at least 50% of the frame and is never cut by the frame edge. |
| #10-12, #18-21, #41-43, #64, #79-80, #100-102 court interiors (16 shots, 7.0 s) | narrow interiors, dark, nothing happens | 1. **The real place:** a wide exterior of the Court of Chancery (Leonard L. Williams Justice Center, Wilmington). 2. **The real person on "just a judge":** Chancellor Kathaleen McCormick, from a news clip or a licensed photo. 3. **News of the ruling:** a broadcast chyron of "judge voids Musk pay". 4. **A symbol burst on "No jury, just a judge":** gavel, scales, Lady Justice (#81, now only 0.16 s), at 2 to 4 frames each, like the reference's "control" burst. |
| #13-17, #68 Jim Cramer (2.3 s) | wrong person for "referee" and "$30B" | **A literal metaphor on "referee":** a sports referee blowing a whistle or showing a card (the reference does "kill switch" = a light switch). On "$30 billion": the $30B card over a stock chart, not over a face. |
| #31, #70 Greek bust (0.9 s) | wrong person | The shareholder is a real man (Richard Tornetta). Options: a news photo or clip of him, if we can license it; or keep him faceless on purpose (a silhouette and a share certificate showing "9 shares"). Never a random face that could be read as him. |
| #47-48 red building on "he posts" | no post shown | **The post itself:** the X post card already built in the HyperFrames test, over darkened moving footage (date checked: 30 Jan 2024). |
| #92-93 rocket launch on the Tesla pay deal | SpaceX picture on a Tesla line | Tesla's Nov 2025 shareholder vote: a news chyron of the approval, or Tesla factory or Optimus footage. |
| #86, #113-114 WEF wide, Fink tiny | subject about 10% of frame | A close crop of the same clip, or the Fink chyron frame from #95. |
| #87-89 Musk on "shareholders have already voted" | no shareholders | Tesla annual meeting crowd footage, or a vote-result chyron. |
| #9 the 9-grid (4.1 s) | muddy tiles, wrong focus for "the man with nine shares" | Being rebuilt as the 2x2 grid with a clean still of Musk (request 2). |
| #124 page logo placeholder | placeholder | Singularity logo outro (request 5). The reference's outro is #141-142: two glowing shapes push in, then settle small, 4.3 s. |

**Sourcing these needs your help:** news broadcast clips and photos of real people (the judge, the shareholder) are owned by the
networks and agencies. Our openly licensed pool (Commons, CC0) cannot cover them. Tell me which clips you have or can license,
and I will place them. The symbols (referee, scales, Lady Justice, the court exterior) I can try to find under open licences first.

**Expected result** if we swap the 20 weak shots and the wrong-person shots, scoring the replacements at the level of our
current good shots: about 8.3 out of 10. That is a rough projection, not a measurement.

## Every shot, labelled and scored

### Reference: every shot

| # | in s | len s | said | shows | type | subject % | Q | F | M | score | sharp | note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.00 | 0.54 | The scariest | Altman two-shot photo, face pixel-blocked, giant SCARIEST whip | still | 45 | 4 | 5 | 5 | **9.5** | 239 | hook: the subject is on screen on word 1 |
| 2 | 0.54 | 0.67 | scariest thing about Sam | polaroid of the same photo on black, pushes in | still | 30 | 4 | 4 | 5 | **9.0** | 489 | bookend device, small but deliberate |
| 3 | 1.21 | 0.29 | Sam Altman | Altman interview, Bloomberg set, medium close | clip | 40 | 5 | 5 | 5 | **10.0** | 196 | named man on his name |
| 4 | 1.50 | 0.34 | Altman isn't | Altman at hearing table, mid shot | clip | 25 | 4 | 4 | 5 | **9.0** | 372 |  |
| 5 | 1.84 | 0.54 | isn't how | Altman at a mic in a vest | clip | 35 | 4 | 4 | 5 | **9.0** | 137 |  |
| 6 | 2.38 | 0.29 | how powerful | Altman on blue-lit stage, side angle | clip | 30 | 4 | 4 | 5 | **9.0** | 86 |  |
| 7 | 2.67 | 0.33 | powerful he | Altman in a red chair on stage | still | 25 | 4 | 4 | 5 | **9.0** | 160 | "powerful" on a throne-like chair |
| 8 | 3.00 | 0.29 | he is. | Altman seated on stage, US flag | clip | 15 | 4 | 3 | 4 | **7.5** | 310 | wide, small subject, but power cue (flag) |
| 9 | 3.29 | 0.30 | is. | Altman close, flag behind | still | 35 | 4 | 4 | 5 | **9.0** | 121 |  |
| 10 | 3.59 | 0.66 | It's what happens | TV in studio showing Altman, 'BAD THINGS'? headline | news | 30 | 4 | 4 | 4 | **8.0** | 526 | news frame sells "what happens" |
| 11 | 4.25 | 0.38 | happens to anyone | Altman interview, chyron about 'bad things' | news | 30 | 4 | 4 | 4 | **8.0** | 819 |  |
| 12 | 4.63 | 1.00 | anyone who tries to | Altman B&W cut-out over a grid of screens and faces | grid | 45 | 4 | 5 | 5 | **9.5** | 641 | "anyone who tries": many faces vs one man |
| 13 | 5.63 | 0.29 | to take his | same grid, new tiles | grid | 45 | 4 | 5 | 5 | **9.5** | 935 |  |
| 14 | 5.92 | 0.59 | his power away. | grid with board women's faces | grid | 45 | 4 | 5 | 5 | **9.5** | 776 | the actual people who tried |
| 15 | 6.51 | 0.66 | away. For | Altman at Senate hearing, 'Mr. Samuel Altman' nameplate | still | 30 | 4 | 5 | 5 | **9.5** | 291 | nameplate = authority |
| 16 | 7.17 | 1.21 | For context, Sam | black card 'For context,' | card | 0 | 5 | 4 | 4 | **8.5** | 175 | turn beat, deliberate breather |
| 17 | 8.38 | 0.55 | Sam designed OpenAI | young Altman with early OpenAI team | still | 25 | 3 | 4 | 5 | **8.5** | 159 | origin photo on 'designed OpenAI' |
| 18 | 8.93 | 0.75 | OpenAI to be | OpenAI logo on a screen, close | clip | 60 | 5 | 5 | 5 | **10.0** | 154 | literal |
| 19 | 9.68 | 0.62 | be the one company | Altman hearing nameplate again | still | 30 | 4 | 4 | 3 | **7.0** | 298 | reused, generic |
| 20 | 10.30 | 1.42 | company on Earth that no single | Earth from space at sunrise | clip | 80 | 5 | 5 | 5 | **10.0** | 635 | literal 'on Earth', full frame |
| 21 | 11.72 | 1.17 | single person could ever | pixelated faces, one man at a mic | clip | 50 | 3 | 4 | 4 | **7.5** | 582 | 'single person' = anonymous faces |
| 22 | 12.89 | 0.37 | ever control. | dark winged statue | clip | 60 | 4 | 4 | 4 | **8.0** | 327 | abstract 'control' burst |
| 23 | 13.26 | 0.30 | control. | B&W statue, raised arm | clip | 60 | 4 | 4 | 4 | **8.0** | 509 |  |
| 24 | 13.56 | 0.20 | control. | statue hands, high contrast | clip | 60 | 4 | 4 | 4 | **8.0** | 440 |  |
| 25 | 13.76 | 0.71 | A non -profit | woman board member interview | clip | 35 | 4 | 4 | 4 | **8.0** | 74 | a real board face on 'non-profit' |
| 26 | 14.47 | 0.29 | -profit | Altman on a panel sofa | clip | 20 | 4 | 4 | 3 | **7.0** | 170 |  |
| 27 | 14.76 | 0.30 | -profit whose | same panel, wider | clip | 20 | 4 | 4 | 3 | **7.0** | 293 |  |
| 28 | 15.06 | 0.62 | board didn't answer | Musk on a stage sofa (co-founder) | clip | 20 | 4 | 4 | 4 | **8.0** | 282 | right people, OpenAI board history |
| 29 | 15.68 | 1.05 | answer to money, | early OpenAI founders group photo | still | 50 | 3 | 4 | 4 | **7.5** | 114 |  |
| 30 | 16.73 | 0.12 | but | same group | still | 50 | 3 | 4 | 4 | **7.5** | 223 |  |
| 31 | 16.85 | 0.38 | but to humanity. | light streaks and network lines | clip | 40 | 4 | 4 | 3 | **7.0** | 393 | 'humanity' burst start |
| 32 | 17.23 | 0.16 | humanity. | glowing atom | clip | 40 | 4 | 4 | 4 | **8.0** | 336 | symbol burst |
| 33 | 17.39 | 0.13 | humanity. | Vitruvian man | clip | 70 | 4 | 5 | 5 | **9.5** | 1699 | literal 'humanity' |
| 34 | 17.52 | 0.29 | humanity. | golden-ratio circles | still | 50 | 4 | 4 | 3 | **7.0** | 292 |  |
| 35 | 17.81 | 0.21 | A | clock face | clip | 60 | 4 | 4 | 3 | **7.0** | 746 | micro-shot in the burst |
| 36 | 18.02 | 1.04 | A kill switch to fire | light switch on a wall | clip | 25 | 4 | 4 | 5 | **9.0** | 177 | literal 'kill switch' |
| 37 | 19.06 | 0.79 | fire even the | black card, words 'fire even the' animate | card | 0 | 5 | 4 | 4 | **8.5** | 107 |  |
| 38 | 19.85 | 0.25 | the CEO. | halftone Altman over OpenAI logo pattern | still | 55 | 4 | 5 | 5 | **9.5** | 1352 | stylised portrait on 'the CEO' |
| 39 | 20.10 | 1.17 | CEO. There was even | same, zoom | clip | 55 | 4 | 5 | 5 | **9.5** | 2005 |  |
| 40 | 21.27 | 0.38 | even a cap on | Altman walking outdoors, revenue chyron | news | 20 | 4 | 4 | 3 | **7.0** | 667 |  |
| 41 | 21.65 | 0.33 | on profit, | reporter, chyron 'OpenAI expects $70B in revenue' | news | 30 | 4 | 4 | 4 | **8.0** | 549 |  |
| 42 | 21.98 | 0.13 | profit, | stock ticker board | clip | 80 | 4 | 4 | 4 | **8.0** | 458 | 'profit' = market |
| 43 | 22.11 | 0.75 | profit, so past | CNBC anchors, chyron 'When will OpenAI turn a profit' | news | 35 | 4 | 4 | 5 | **9.0** | 837 | chyron prints the word |
| 44 | 22.86 | 0.45 | past a point, | red and green candle chart | clip | 80 | 4 | 4 | 4 | **8.0** | 333 |  |
| 45 | 23.31 | 0.26 | point, | TV on trading floor, unrelated headline | news | 30 | 3 | 3 | 2 | **5.0** | 503 |  |
| 46 | 23.57 | 0.29 | the | NYSE traders crowd | clip | 70 | 4 | 4 | 3 | **7.0** | 517 |  |
| 47 | 23.86 | 0.21 | the profit | Altman on stage with a quote card | clip | 20 | 4 | 3 | 2 | **5.5** | 104 |  |
| 48 | 24.07 | 0.33 | profit went | Fox presenters by a Meta logo | news | 25 | 4 | 3 | 2 | **5.5** | 664 |  |
| 49 | 24.40 | 0.37 | back to | CBS anchor, AI energy bills chyron | news | 35 | 4 | 4 | 2 | **6.0** | 1034 |  |
| 50 | 24.77 | 0.34 | to the world. | anchor live | news | 40 | 4 | 4 | 2 | **6.0** | 254 |  |
| 51 | 25.11 | 0.25 | world. | CNBC 'Q2 net income' graphic | news | 60 | 4 | 3 | 3 | **6.5** | 2145 |  |
| 52 | 25.36 | 0.21 |  | bar chart | still | 60 | 3 | 3 | 3 | **6.0** | 587 |  |
| 53 | 25.57 | 0.12 | It was | Altman on stage, '06 higher rate limits' slide | clip | 25 | 4 | 4 | 3 | **7.0** | 360 |  |
| 54 | 25.69 | 0.34 | was the safest | same | clip | 25 | 4 | 4 | 3 | **7.0** | 491 |  |
| 55 | 26.03 | 0.75 | safest structure | Altman on dark stage | clip | 20 | 4 | 4 | 4 | **8.0** | 211 |  |
| 56 | 26.78 | 1.46 | structure anyone ever built. And | news article 'OpenAI wraps $7B share sale', word highlighted | still | 80 | 4 | 4 | 3 | **7.0** | 736 | highlighted word = caption trick |
| 57 | 28.24 | 0.66 | And then, | Altman interview, warm | clip | 40 | 4 | 4 | 3 | **7.0** | 205 |  |
| 58 | 28.90 | 0.13 | then, | motion-blurred smear | clip | 0 | 3 | 3 | 3 | **6.0** | 105 | transition frame |
| 59 | 29.03 | 0.21 | on | black with loading spinner | clip | 5 | 4 | 3 | 3 | **6.5** | 19 |  |
| 60 | 29.24 | 0.75 | on a Friday, | radio dial turning | clip | 80 | 4 | 5 | 4 | **8.5** | 1002 | 'on a Friday' = tuning in, full frame |
| 61 | 29.99 | 0.54 |  | dark screen with code text | clip | 50 | 3 | 3 | 3 | **6.0** | 247 |  |
| 62 | 30.53 | 0.92 | four board members actually | collage of the four board members | grid | 80 | 4 | 5 | 5 | **9.5** | 1499 | literal 'four board members' |
| 63 | 31.45 | 0.42 | actually | Fox Business anchor | news | 40 | 4 | 4 | 3 | **7.0** | 419 |  |
| 64 | 31.87 | 1.25 | actually pressed the button. | anchor with Helen Toner box, 'Ex-OpenAI board member speaks' | news | 40 | 4 | 4 | 5 | **9.0** | 934 |  |
| 65 | 33.12 | 2.04 | When the company that gave us chat GPT fired | talk host, chyron 'OpenAI fires CEO Sam Altman' | news | 35 | 4 | 4 | 5 | **9.0** | 980 | chyron prints the event |
| 66 | 35.16 | 0.92 | fired its CEO. | same host, close | news | 45 | 4 | 4 | 5 | **9.0** | 114 |  |
| 67 | 36.08 | 0.21 | CEO. | Altman at hearing, B&W | clip | 35 | 4 | 4 | 5 | **9.0** | 222 |  |
| 68 | 36.29 | 0.83 | CEO. They just made | man on stage, wide | clip | 10 | 4 | 3 | 3 | **6.5** | 256 | small subject |
| 69 | 37.12 | 0.54 | made the biggest | woman on dark stage | clip | 10 | 4 | 3 | 3 | **6.5** | 127 | small subject |
| 70 | 37.66 | 0.21 | biggest mistake | burning field | clip | 90 | 4 | 5 | 5 | **9.5** | 552 | 'biggest mistake' = fire |
| 71 | 37.87 | 0.13 | mistake | same, closer | clip | 90 | 4 | 5 | 5 | **9.5** | 313 |  |
| 72 | 38.00 | 0.25 | mistake of | explosion clouds | clip | 90 | 4 | 5 | 5 | **9.5** | 208 |  |
| 73 | 38.25 | 0.66 | of their lives. | black, word 'their' | card | 0 | 4 | 4 | 3 | **7.0** | 99 |  |
| 74 | 38.91 | 0.21 |  | fire field | clip | 90 | 4 | 5 | 4 | **8.5** | 190 |  |
| 75 | 39.12 | 0.42 | Within hours, | black, word 'Within' | card | 0 | 4 | 4 | 3 | **7.0** | 146 |  |
| 76 | 39.54 | 0.75 | hours, 700 | orange particle burst | clip | 50 | 4 | 4 | 3 | **7.0** | 233 |  |
| 77 | 40.29 | 2.17 | 700 of his people threatened to walk out the door | collage of news screens and faces | grid | 90 | 4 | 5 | 5 | **9.5** | 1807 | '700 people' = many faces, 2.2 s |
| 78 | 42.46 | 0.25 | door with | Altman in a room, hoodie | still | 35 | 3 | 4 | 4 | **7.5** | 450 |  |
| 79 | 42.71 | 0.37 | with him. | same | still | 35 | 3 | 4 | 4 | **7.5** | 290 |  |
| 80 | 43.08 | 0.63 | And within four | Altman at a desk, laptop | clip | 30 | 3 | 3 | 3 | **6.0** | 646 |  |
| 81 | 43.71 | 0.54 | four days, | green tunnel / eye | clip | 80 | 4 | 4 | 4 | **8.0** | 279 | 'four days' = time warp |
| 82 | 44.25 | 0.88 | he was back. | same tunnel | clip | 80 | 4 | 4 | 4 | **8.0** | 284 |  |
| 83 | 45.13 | 1.83 | back. Sam Altman is apparently back | Fox anchor soundbite 'Sam Altman is apparently back' | news | 40 | 4 | 4 | 5 | **9.0** | 425 | rule-break soundbite |
| 84 | 46.96 | 4.13 | back as OpenAI's CEO. That's just days after getting fired. | same, 4.1 s | news | 40 | 4 | 4 | 5 | **9.0** | 178 |  |
| 85 | 51.09 | 0.67 | The two who challenged | split: the two board women | news | 40 | 4 | 4 | 5 | **9.0** | 357 | literal 'the two' |
| 86 | 51.76 | 0.75 | challenged him? Gone. | Altman seated on dark stage | clip | 20 | 4 | 4 | 4 | **8.0** | 150 |  |
| 87 | 52.51 | 0.67 | Gone. The humanity | black card 'GONE.' | card | 0 | 5 | 5 | 5 | **10.0** | 102 |  |
| 88 | 53.18 | 0.58 | humanity cap on | figure falling in light | clip | 40 | 4 | 4 | 4 | **8.0** | 239 |  |
| 89 | 53.76 | 0.34 | on profits? | stock chart with price | clip | 70 | 4 | 4 | 4 | **8.0** | 246 |  |
| 90 | 54.10 | 0.12 | profits? | dollar bills, close | clip | 90 | 5 | 5 | 5 | **10.0** | 312 |  |
| 91 | 54.22 | 1.09 | Gone. As | black card 'GONE.' | card | 0 | 5 | 5 | 5 | **10.0** | 102 |  |
| 92 | 55.31 | 0.70 | As a result, | Altman, blue stage | clip | 30 | 4 | 4 | 3 | **7.0** | 138 |  |
| 93 | 56.01 | 0.25 | the | young Altman, red wall | still | 35 | 4 | 4 | 3 | **7.0** | 120 |  |
| 94 | 56.26 | 0.71 | the company worth 86 | Altman presenting to office crowd | clip | 15 | 4 | 3 | 4 | **7.5** | 679 |  |
| 95 | 56.97 | 1.71 | 86 billion dollars the | anchor, big '$86B', 'Ousted CEO's surprise move' | news | 40 | 4 | 4 | 5 | **9.0** | 1043 | number printed on screen |
| 96 | 58.68 | 1.30 | day they fired him is now | same | news | 40 | 4 | 4 | 5 | **9.0** | 836 |  |
| 97 | 59.98 | 3.25 | now worth 852 billion dollars. | Bloomberg reporter, 'OpenAI valued at $852B', big '$852B' | news | 40 | 4 | 4 | 5 | **9.0** | 854 | 3.3 s hold on the number |
| 98 | 63.23 | 0.63 | And last week, | George W. Bush, B&W | clip | 35 | 3 | 4 | 2 | **5.5** | 163 | loose 'powerful people' tease |
| 99 | 63.86 | 0.12 |  | red-black flag | clip | 60 | 3 | 3 | 3 | **6.0** | 219 |  |
| 100 | 63.98 | 0.33 | it happened | Trump at Oval Office desk, B&W | clip | 25 | 4 | 4 | 3 | **7.0** | 366 |  |
| 101 | 64.31 | 0.25 | happened again. | black, 'it happened' | card | 0 | 4 | 4 | 3 | **7.0** | 223 |  |
| 102 | 64.56 | 0.88 | again. The most powerful | Bush with sign, B&W | clip | 35 | 3 | 4 | 3 | **6.5** | 70 |  |
| 103 | 65.44 | 0.21 | powerful | B&W hands and statue | clip | 50 | 3 | 3 | 3 | **6.0** | 202 |  |
| 104 | 65.65 | 0.25 | powerful people | same | still | 50 | 3 | 3 | 3 | **6.0** | 172 |  |
| 105 | 65.90 | 0.29 | people in | AI executive close | still | 40 | 3 | 4 | 3 | **6.5** | 147 |  |
| 106 | 66.19 | 0.33 | in AI | AI executive | still | 35 | 3 | 4 | 4 | **7.5** | 364 |  |
| 107 | 66.52 | 0.46 | AI walked | AI executive interview | clip | 35 | 4 | 4 | 4 | **8.0** | 151 |  |
| 108 | 66.98 | 0.50 | walked into the White | executive walking, chyron 'takes center stage in Washington' | news | 30 | 4 | 4 | 5 | **9.0** | 525 |  |
| 109 | 67.48 | 0.96 | White House and signed | executives walking, same chyron | news | 30 | 4 | 4 | 5 | **9.0** | 2593 |  |
| 110 | 68.44 | 1.63 | signed a promise to keep this technology | 'President Trump meets with tech leaders' table | news | 50 | 4 | 4 | 5 | **9.0** | 1426 | literal 'signed a promise' |
| 111 | 70.07 | 0.25 | technology | OpenAI knot logo spinning on black | clip | 30 | 4 | 5 | 4 | **8.5** | 361 |  |
| 112 | 70.32 | 0.17 | technology safe. | same | clip | 50 | 4 | 5 | 4 | **8.5** | 330 |  |
| 113 | 70.49 | 0.12 | safe. | same, large | clip | 70 | 4 | 5 | 4 | **8.5** | 211 |  |
| 114 | 70.61 | 0.25 | safe. | same | clip | 50 | 4 | 5 | 4 | **8.5** | 402 |  |
| 115 | 70.86 | 0.21 |  | same | clip | 50 | 4 | 5 | 4 | **8.5** | 349 |  |
| 116 | 71.07 | 0.25 | But who | logo in red | clip | 50 | 4 | 4 | 4 | **8.0** | 6 |  |
| 117 | 71.32 | 0.29 | who is | silhouettes walking, blue | clip | 80 | 4 | 4 | 4 | **8.0** | 105 | 'who is watching' |
| 118 | 71.61 | 0.21 | is watching | same | clip | 80 | 4 | 4 | 4 | **8.0** | 263 |  |
| 119 | 71.82 | 0.25 | watching them? | red silhouettes | clip | 80 | 4 | 4 | 4 | **8.0** | 111 |  |
| 120 | 72.07 | 0.42 | them? | B&W man and hand | clip | 40 | 3 | 3 | 3 | **6.0** | 50 |  |
| 121 | 72.49 | 0.37 | The most | same | clip | 40 | 3 | 3 | 3 | **6.0** | 233 |  |
| 122 | 72.86 | 0.25 | most powerful | dark red frame | still | 20 | 2 | 2 | 2 | **4.0** | 71 |  |
| 123 | 73.11 | 0.38 | powerful | code text | clip | 80 | 3 | 3 | 3 | **6.0** | 2332 |  |
| 124 | 73.49 | 0.50 | powerful technology | code and element card | still | 60 | 3 | 3 | 4 | **7.0** | 295 |  |
| 125 | 73.99 | 0.50 | technology in human | carbon element card, red | still | 50 | 3 | 3 | 3 | **6.0** | 843 |  |
| 126 | 74.49 | 0.21 | human | code | clip | 80 | 3 | 3 | 3 | **6.0** | 865 |  |
| 127 | 74.70 | 0.29 | human history. | red sacred-geometry triangle | still | 60 | 3 | 3 | 3 | **6.0** | 202 |  |
| 128 | 74.99 | 0.46 | history. | same | clip | 60 | 3 | 3 | 3 | **6.0** | 193 |  |
| 129 | 75.45 | 0.17 | And | glowing white sculpture | clip | 60 | 3 | 4 | 3 | **6.5** | 590 |  |
| 130 | 75.62 | 0.50 | And it all comes | same | clip | 60 | 3 | 4 | 3 | **6.5** | 249 |  |
| 131 | 76.12 | 0.21 | comes down | black, 'comes' | card | 0 | 4 | 4 | 3 | **7.0** | 109 |  |
| 132 | 76.33 | 0.29 | down to | green tracking boxes over hands | clip | 60 | 3 | 3 | 4 | **7.0** | 247 | surveillance look |
| 133 | 76.62 | 0.17 | to the mood | green crowded station with tracking | clip | 80 | 3 | 4 | 4 | **7.5** | 571 |  |
| 134 | 76.79 | 0.16 | mood | same | clip | 80 | 3 | 4 | 4 | **7.5** | 582 |  |
| 135 | 76.95 | 0.29 | mood of about | same | clip | 80 | 3 | 4 | 4 | **7.5** | 675 |  |
| 136 | 77.24 | 0.34 | about five | same with Trump cut-out | clip | 80 | 3 | 4 | 4 | **7.5** | 835 |  |
| 137 | 77.58 | 1.42 | five people. That's not a | split-face collage of five people | grid | 90 | 4 | 5 | 5 | **9.5** | 592 | literal 'five people' |
| 138 | 79.00 | 1.29 | a plan. That's | scientist in a dark lab | clip | 30 | 3 | 3 | 3 | **6.0** | 137 |  |
| 139 | 80.29 | 1.08 | That's just hoping the king stays | candle, dark hands | clip | 30 | 3 | 3 | 4 | **7.0** | 182 | 'hoping the king stays kind' |
| 140 | 81.37 | 0.71 | stays kind. | Altman close, blue | clip | 40 | 4 | 4 | 5 | **9.0** | 127 |  |
| 141 | 82.08 | 1.13 |  | logo sting: two glowing white diamonds | gfx | 50 | 5 | 5 | 5 | **10.0** | 3 | outro, glow push-in |
| 142 | 83.21 | 3.17 |  | same, settles small | gfx | 30 | 5 | 5 | 5 | **10.0** | 82 | outro hold 3.2 s |

### Ours (v9c): every shot

| # | in s | len s | said | shows | type | subject % | Q | F | M | score | sharp | note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.00 | 0.78 | The scariest thing | Musk seated photo, pixel blocks clearing | still | 35 | 4 | 4 | 5 | **9.0** | 375 | hook on the named man |
| 2 | 0.78 | 0.47 | thing about Elon | polaroid of the same photo on black | still | 25 | 4 | 4 | 5 | **9.0** | 388 |  |
| 3 | 1.25 | 0.31 | Elon Musk | Musk at WEF, blue backdrop | clip | 40 | 4 | 5 | 5 | **9.5** | 309 |  |
| 4 | 1.56 | 0.31 | Musk | Musk at a presidential podium | clip | 35 | 4 | 5 | 5 | **9.5** | 451 |  |
| 5 | 1.88 | 0.47 | Musk isn't | Musk at WEF | clip | 40 | 4 | 5 | 5 | **9.5** | 366 |  |
| 6 | 2.34 | 0.31 | isn't his | Musk at the podium | clip | 35 | 4 | 5 | 5 | **9.5** | 289 |  |
| 7 | 2.66 | 0.47 | his money. | gold bar, dark, bar cut off at the bottom | clip | 15 | 2 | 1 | 4 | **5.5** | 264 | USER NOTE: weak. Bar is under 20% of frame and cropped; reads as a dark smudge |
| 8 | 3.12 | 0.47 | It's | same, punch-in | still | 15 | 2 | 1 | 3 | **4.5** | 267 | same problem |
| 9 | 3.59 | 4.06 | It's what happens to the man with nine shares who tried to take it away. Delaware's | 9-grid of clips with a Musk cut-out (4.1 s) | grid | 45 | 3 | 3 | 3 | **6.0** | 412 | shows Musk, but the words are about the shareholder; muddy low-res tiles |
| 10 | 7.66 | 0.31 | Delaware's business | court interior, dark staircase, Court of Chancery tag | clip | 20 | 2 | 2 | 3 | **5.0** | 432 | USER NOTE: narrow building shot, says nothing |
| 11 | 7.97 | 0.47 | business court is | same, tag | clip | 20 | 2 | 2 | 3 | **5.0** | 532 |  |
| 12 | 8.44 | 0.31 | is the referee | arched window | clip | 20 | 2 | 2 | 2 | **4.0** | 475 |  |
| 13 | 8.75 | 0.31 | referee | Jim Cramer on the NYSE floor, B&W | clip | 40 | 4 | 4 | 2 | **6.0** | 476 | reads as 'random man'; not a referee, not Delaware |
| 14 | 9.06 | 0.62 | referee of corporate | Cramer close | clip | 50 | 4 | 4 | 2 | **6.0** | 409 |  |
| 15 | 9.69 | 0.31 | corporate America. | Cramer close, colour | clip | 50 | 4 | 4 | 2 | **6.0** | 288 |  |
| 16 | 10.00 | 0.47 | America. | Cramer | clip | 55 | 4 | 4 | 2 | **6.0** | 309 |  |
| 17 | 10.47 | 0.31 |  | Cramer | clip | 50 | 4 | 4 | 2 | **6.0** | 309 |  |
| 18 | 10.78 | 0.47 | No jury, | empty jury box, dark | clip | 20 | 2 | 2 | 4 | **6.0** | 210 | literal but dark and narrow |
| 19 | 11.25 | 0.47 | jury, | same | clip | 20 | 2 | 2 | 4 | **6.0** | 193 |  |
| 20 | 11.72 | 0.31 | just a judge. | arched window | clip | 15 | 2 | 2 | 1 | **3.0** | 184 | 'judge' with no judge in it |
| 21 | 12.03 | 0.62 | judge. | same | clip | 15 | 2 | 2 | 1 | **3.0** | 172 |  |
| 22 | 12.66 | 1.25 | 2018, | '2018' card over darkened parking lot | card | 0 | 4 | 4 | 4 | **8.0** | 274 |  |
| 23 | 13.91 | 0.62 | Tesla's board gives | man in a crowd at a meeting | clip | 25 | 3 | 4 | 3 | **6.5** | 385 |  |
| 24 | 14.53 | 0.47 | gives Elon | Musk at WEF | clip | 40 | 4 | 4 | 5 | **9.0** | 154 |  |
| 25 | 15.00 | 0.31 | Elon a pay | Musk close | still | 45 | 4 | 4 | 5 | **9.0** | 151 |  |
| 26 | 15.31 | 0.62 | pay deal worth $56 | bank vault door with curtain | still | 40 | 3 | 3 | 3 | **6.0** | 961 | money metaphor, a bit random |
| 27 | 15.94 | 2.19 | $56 billion. One | '$56B' card over dark footage (2.2 s) | card | 0 | 4 | 4 | 5 | **9.0** | 460 |  |
| 28 | 18.12 | 0.62 | One shareholder | dot grid with circled 'him' | gfx | 10 | 4 | 4 | 4 | **8.0** | 524 |  |
| 29 | 18.75 | 0.47 | shareholder sues, | red gavel close | clip | 60 | 4 | 4 | 4 | **8.0** | 286 |  |
| 30 | 19.22 | 0.47 | sues, he | same | still | 60 | 4 | 4 | 4 | **8.0** | 283 |  |
| 31 | 19.69 | 0.47 | he owns nine | Greek bust (Herodotus) | clip | 55 | 4 | 4 | 1 | **5.0** | 369 | wrong person: the shareholder is a drummer, not a philosopher |
| 32 | 20.16 | 1.72 | nine shares. January, | nine-shares grid graphic (1.7 s) | gfx | 30 | 4 | 4 | 5 | **9.0** | 346 |  |
| 33 | 21.88 | 1.25 | January, 2024, | 'Jan 2024' card over dark building | card | 0 | 4 | 3 | 4 | **7.5** | 333 |  |
| 34 | 23.12 | 0.47 | the judge agrees. | old judge caricature drawing | clip | 50 | 3 | 4 | 4 | **7.5** | 2793 |  |
| 35 | 23.59 | 0.47 | agrees. | gavel on white | clip | 60 | 4 | 5 | 4 | **8.5** | 443 |  |
| 36 | 24.06 | 0.31 |  | same | still | 60 | 4 | 5 | 4 | **8.5** | 411 |  |
| 37 | 24.38 | 0.78 | The deal, voided. | '$56B the pay deal' card | card | 0 | 4 | 3 | 5 | **8.5** | 367 |  |
| 38 | 25.16 | 0.78 | voided. But | $56B struck, VOIDED stamp | card | 0 | 4 | 4 | 5 | **9.0** | 326 |  |
| 39 | 25.94 | 0.16 | But Musk | black, 'But Musk' | card | 0 | 4 | 4 | 3 | **7.0** | 130 |  |
| 40 | 26.09 | 0.31 | Musk doesn't | Musk at WEF | still | 40 | 4 | 4 | 5 | **9.0** | 176 |  |
| 41 | 26.41 | 0.47 | doesn't just | courtroom with portraits | clip | 25 | 3 | 3 | 3 | **6.0** | 258 |  |
| 42 | 26.88 | 0.47 | just appeal, | empty room, doors | clip | 10 | 2 | 2 | 2 | **4.0** | 191 | USER NOTE type: building interior with nothing in it |
| 43 | 27.34 | 0.47 | appeal, he | same | clip | 10 | 2 | 2 | 2 | **4.0** | 256 |  |
| 44 | 27.81 | 0.62 | he moves the whole | Giga Texas aerial, Austin tag | clip | 80 | 4 | 5 | 5 | **9.5** | 291 |  |
| 45 | 28.44 | 0.47 | whole company. Never | same | still | 80 | 4 | 5 | 5 | **9.5** | 379 |  |
| 46 | 28.91 | 3.28 | Never incorporate your company in the state of Delaware, | quote card over dark footage (3.3 s) | card | 0 | 4 | 3 | 5 | **8.5** | 625 |  |
| 47 | 32.19 | 0.47 | he posts. | red-tinted building facade | still | 50 | 3 | 4 | 2 | **5.5** | 208 | 'he posts' with no post or phone |
| 48 | 32.66 | 0.47 | posts. | same | clip | 50 | 3 | 4 | 2 | **5.5** | 195 |  |
| 49 | 33.12 | 0.62 | Within five months, | Delaware-to-Texas map, arc draws | gfx | 50 | 4 | 4 | 5 | **9.0** | 327 | plain dark card (empty frame rule) |
| 50 | 33.75 | 0.47 | months, | same | gfx | 50 | 4 | 4 | 5 | **9.0** | 429 |  |
| 51 | 34.22 | 0.31 | Tesla votes | same | gfx | 50 | 4 | 4 | 5 | **9.0** | 433 |  |
| 52 | 34.53 | 0.47 | votes to leave | same | gfx | 50 | 4 | 4 | 5 | **9.0** | 458 |  |
| 53 | 35.00 | 0.31 | leave for Texas. | WEF stage wide with map overlay | clip | 10 | 3 | 3 | 2 | **5.0** | 138 |  |
| 54 | 35.31 | 0.62 | Texas. | Texas flag over a night city | clip | 70 | 5 | 5 | 5 | **10.0** | 631 |  |
| 55 | 35.94 | 0.47 | Then Texas | Texas Capitol at night | clip | 70 | 5 | 5 | 5 | **10.0** | 507 |  |
| 56 | 36.41 | 0.47 | Texas changes | same | clip | 70 | 5 | 5 | 5 | **10.0** | 420 |  |
| 57 | 36.88 | 0.31 | changes its law | law books on shelves | clip | 90 | 4 | 5 | 5 | **9.5** | 787 |  |
| 58 | 37.19 | 0.31 | law and | same | clip | 90 | 4 | 5 | 5 | **9.5** | 525 |  |
| 59 | 37.50 | 0.62 | and Tesla | same | clip | 90 | 4 | 5 | 5 | **9.5** | 839 |  |
| 60 | 38.12 | 0.47 | Tesla rewrites | Tesla car interior | clip | 50 | 3 | 3 | 4 | **7.0** | 176 |  |
| 61 | 38.59 | 0.62 | rewrites | factory aerial, blurred | clip | 50 | 2 | 3 | 3 | **5.5** | 254 |  |
| 62 | 39.22 | 0.47 | rewrites the rules. | red law books | clip | 90 | 4 | 5 | 4 | **8.5** | 216 |  |
| 63 | 39.69 | 0.31 |  | same | clip | 90 | 4 | 5 | 4 | **8.5** | 186 |  |
| 64 | 40.00 | 0.47 | To sue the board | courthouse corner, ceiling | clip | 15 | 2 | 2 | 2 | **4.0** | 212 |  |
| 65 | 40.47 | 0.47 | board now, | man at shareholder meeting, B&W | clip | 30 | 3 | 4 | 3 | **6.5** | 307 |  |
| 66 | 40.94 | 0.47 | now, you need | same | still | 30 | 3 | 4 | 3 | **6.5** | 242 |  |
| 67 | 41.41 | 1.56 | need 3 % of the company. That's | 3% grid graphic (1.6 s) | gfx | 30 | 4 | 4 | 5 | **9.0** | 509 |  |
| 68 | 42.97 | 0.31 | That's over $30 | Cramer | clip | 50 | 4 | 4 | 1 | **5.0** | 349 |  |
| 69 | 43.28 | 1.88 | $30 billion of stock. The | '$30B+' card over Cramer (1.9 s) | card | 0 | 4 | 4 | 4 | **8.0** | 467 |  |
| 70 | 45.16 | 0.47 | The man with nine | Greek bust again | clip | 55 | 4 | 4 | 1 | **5.0** | 477 | wrong person again |
| 71 | 45.62 | 0.94 | nine shares, locked | nine-shares grid | gfx | 30 | 4 | 4 | 5 | **9.0** | 284 |  |
| 72 | 46.56 | 0.31 | locked out. | red hand on a combination lock | clip | 60 | 4 | 5 | 5 | **9.5** | 146 |  |
| 73 | 46.88 | 0.62 | out. The | same | clip | 60 | 4 | 5 | 5 | **9.5** | 149 |  |
| 74 | 47.50 | 0.31 | The judge's | judge caricature | clip | 50 | 3 | 4 | 4 | **7.5** | 2571 |  |
| 75 | 47.81 | 0.47 | judge's ruling, | same | clip | 50 | 3 | 4 | 4 | **7.5** | 2112 |  |
| 76 | 48.28 | 0.31 | reversed. | same | clip | 50 | 3 | 4 | 4 | **7.5** | 2546 |  |
| 77 | 48.59 | 1.09 | reversed. December, | 'Ruling' struck, REVERSED stamp | card | 0 | 4 | 4 | 5 | **9.0** | 314 |  |
| 78 | 49.69 | 1.56 | 2025, | 'Dec 2025' card over dark arches | card | 0 | 4 | 3 | 4 | **7.5** | 377 |  |
| 79 | 51.25 | 0.47 | Delaware's top | court interior, narrow | clip | 10 | 2 | 2 | 2 | **4.0** | 298 | USER NOTE type |
| 80 | 51.72 | 0.31 | top court | arched window | clip | 15 | 2 | 2 | 2 | **4.0** | 307 |  |
| 81 | 52.03 | 0.16 | court | Lady Justice statue | clip | 60 | 4 | 4 | 4 | **8.0** | 514 | good, but on screen 0.16 s |
| 82 | 52.19 | 1.41 | court gives the deal back and awards | '$56B given back' card | card | 0 | 4 | 3 | 5 | **8.5** | 315 |  |
| 83 | 53.59 | 0.31 | awards the | dollar bill close | clip | 80 | 4 | 5 | 5 | **9.5** | 600 |  |
| 84 | 53.91 | 0.47 | the shareholder | same | clip | 80 | 4 | 5 | 5 | **9.5** | 475 |  |
| 85 | 54.38 | 1.09 | shareholder $1. By | '$1' card | card | 0 | 4 | 3 | 5 | **8.5** | 476 |  |
| 86 | 55.47 | 0.62 | By then, | WEF stage wide, Fink tiny | still | 10 | 3 | 2 | 2 | **4.5** | 327 |  |
| 87 | 56.09 | 0.31 | shareholders have | Musk at WEF | still | 45 | 4 | 4 | 3 | **7.0** | 360 |  |
| 88 | 56.41 | 0.31 | have | same | still | 45 | 4 | 4 | 3 | **7.0** | 345 |  |
| 89 | 56.72 | 0.47 | have already voted | Musk at WEF | still | 40 | 4 | 4 | 3 | **7.0** | 335 | 'shareholders voted' shows no shareholders |
| 90 | 57.19 | 0.62 | voted him a new | NYSE floor, CNBC mic | clip | 40 | 3 | 3 | 2 | **5.0** | 229 |  |
| 91 | 57.81 | 0.31 | new deal | gold bars, full frame | clip | 90 | 4 | 5 | 3 | **7.5** | 444 | good shot of the gold; the right fix for #7 |
| 92 | 58.12 | 0.47 | deal worth | rocket launch | still | 30 | 4 | 4 | 2 | **6.0** | 253 | SpaceX on a Tesla pay line |
| 93 | 58.59 | 0.47 | worth up to $1 | same | clip | 30 | 4 | 4 | 2 | **6.0** | 125 |  |
| 94 | 59.06 | 1.56 | $1 trillion. I | '$1 trillion' card | card | 0 | 4 | 3 | 5 | **8.5** | 406 |  |
| 95 | 60.62 | 6.41 | I don't think there's any other company as large as Tesla today that has that compounded return, so congratulations. On | Larry Fink soundbite (6.4 s) | news | 45 | 4 | 4 | 5 | **9.0** | 494 | rule-break soundbite with chyron |
| 96 | 67.03 | 0.78 | On Wednesday, | 'Wed 21 Oct' card over parking lot | card | 0 | 4 | 3 | 4 | **7.5** | 639 |  |
| 97 | 67.81 | 0.47 | Tesla reports | Tesla cars in a lot | still | 40 | 3 | 3 | 4 | **7.0** | 494 |  |
| 98 | 68.28 | 0.31 | reports to | same | clip | 40 | 3 | 3 | 4 | **7.0** | 422 |  |
| 99 | 68.59 | 0.31 | to a board | man at shareholder meeting, B&W | clip | 30 | 3 | 4 | 3 | **6.5** | 483 |  |
| 100 | 68.91 | 0.47 | board almost | empty room, door | clip | 10 | 2 | 2 | 2 | **4.0** | 505 |  |
| 101 | 69.38 | 0.47 | almost nobody | same | clip | 10 | 2 | 2 | 2 | **4.0** | 378 |  |
| 102 | 69.84 | 0.47 | nobody can sue. | same | clip | 10 | 2 | 2 | 2 | **4.0** | 462 |  |
| 103 | 70.31 | 0.47 | sue. | gavel, B&W | clip | 60 | 4 | 5 | 4 | **8.5** | 695 |  |
| 104 | 70.78 | 0.31 | So | same | clip | 60 | 4 | 5 | 4 | **8.5** | 564 |  |
| 105 | 71.09 | 0.47 | So the scariest | polaroid callback | still | 20 | 4 | 4 | 5 | **9.0** | 463 |  |
| 106 | 71.56 | 0.62 | scariest thing about Elon | same, closer | clip | 35 | 4 | 4 | 5 | **9.0** | 403 |  |
| 107 | 72.19 | 0.31 | Elon Musk | Musk at WEF | still | 40 | 4 | 4 | 5 | **9.0** | 376 |  |
| 108 | 72.50 | 0.62 | Musk isn't | same | still | 40 | 4 | 4 | 5 | **9.0** | 153 |  |
| 109 | 73.12 | 0.31 | isn't his | gold bar, red, cut off | still | 15 | 2 | 1 | 3 | **4.5** | 197 | same problem as #7 |
| 110 | 73.44 | 0.47 | his money. | same | still | 15 | 2 | 1 | 3 | **4.5** | 137 |  |
| 111 | 73.91 | 0.47 | money. | same | still | 15 | 2 | 1 | 3 | **4.5** | 170 |  |
| 112 | 74.38 | 0.31 |  | same | still | 15 | 2 | 1 | 3 | **4.5** | 193 |  |
| 113 | 74.69 | 0.31 | It's that | WEF stage wide, Fink tiny, B&W | still | 10 | 3 | 2 | 2 | **4.5** | 316 |  |
| 114 | 75.00 | 0.47 | that the next person | same | clip | 15 | 3 | 2 | 2 | **4.5** | 254 |  |
| 115 | 75.47 | 0.31 | person who | Musk B&W | still | 40 | 4 | 4 | 3 | **7.0** | 321 |  |
| 116 | 75.78 | 0.31 | who tries | red hand on lock | still | 60 | 4 | 5 | 4 | **8.5** | 286 |  |
| 117 | 76.09 | 0.47 | tries to take | same | still | 60 | 4 | 5 | 4 | **8.5** | 161 |  |
| 118 | 76.56 | 0.47 | take it away needs | same | still | 60 | 4 | 5 | 4 | **8.5** | 174 |  |
| 119 | 77.03 | 1.09 | needs $30 billion just | '$30B+' card over Cramer | card | 0 | 4 | 4 | 4 | **8.0** | 373 |  |
| 120 | 78.12 | 0.47 | just | courtroom double doors | clip | 50 | 3 | 4 | 5 | **8.5** | 467 | literal 'the door' |
| 121 | 78.59 | 0.47 | just to | same | clip | 50 | 3 | 4 | 5 | **8.5** | 413 |  |
| 122 | 79.06 | 0.47 | to get in the door. | same | clip | 50 | 3 | 4 | 5 | **8.5** | 348 |  |
| 123 | 79.53 | 0.62 | door. | black, 'the door.' | card | 0 | 4 | 4 | 4 | **8.0** | 117 |  |
| 124 | 80.16 | 1.50 |  | [PAGE LOGO] placeholder | card | 0 | 1 | 1 | 0 | **1.0** | 177 | placeholder, to be replaced by the Singularity outro |
