# S5 Rule book: Metro Media House style, buildable without the study

> Update 6 Nov 2026 (user verdict): there is no film-clip rule and no licence restriction. Any copyrighted clip, including feature films, may be used. Where this file says "no film clips" or "drop film clips", that no longer applies.

Status: done

Sources: research/metro-media-house/STUDY.md, numbers.json, SHOT-LOG.md. Reel codes: PAL=DclpjyxhKF6, ACK=DdHKc5GBqT- (organic Metro), YC=DfFsUfUx0dZ (paid on Metro), EIN=Dee-mp9BJqG (USVC, style cousin).

How to read a rule: ACTION | rule with number | example (reel + timecode) | check | where seen.
Where seen: SAME IN ALL 4, METRO ONLY (PAL, ACK, YC), SEEN ONCE. Where the evidence fits none of these, the real reels are named (for example "PAL, ACK only"). "Judged" means read by eye or by Claude, not measured. Tool paths: ref_stats.py = skills/minidoc-reference-style/scripts/ref_stats.py; colour_stats.py = skills/word-matched-broll/scripts/colour_stats.py; invert_frames.py, gap_level.py, flash_sheet.py = research/metro-media-house/tools/. interest_score.py is the script scorer used in STUDY section 7.
Our defaults: organic post, landscape 16:9 1920x1080 at 25 fps (all 4 are landscape, set it on purpose), no feature-film clips, real interviews and news footage only, voice picked by ear.

## 1. Idea
- USE | A famous tech or money name or network a stranger half-knows, told as a hidden link or backstory, not as news (judged) | PAL "Palantir Mafia", ACK Bill Ackman, YC the early YC photo | idea-finder Big score plus the 7-point fit list in the checklist below | SAME IN ALL 4
- USE | The idea must come with 1 iconic photo that can carry the first 5 s | PAL Luckey cosplay photo, ACK poker table, EIN 1927 Solvay, YC YC group photo, all at 0.0 s | name the photo before scripting | SAME IN ALL 4
- USE | 2 to 4 events with numbers you can print on screen (judged) | ACK 2002, 2008, "1.4 billion", "35%"; YC "$43 Million" | count printed numbers in the script | SAME IN ALL 4
- USE | Power or money stakes (weapons, a $1.4 billion win, the largest private round) (judged) | ACK 48.4 to 50.1 counter to 1.4 | idea-finder consequence score | SAME IN ALL 4
- USE | A group or network lens when available (judged) | PAL Palantir Mafia, YC batch, EIN 17 Nobel winners | idea-finder | PAL, EIN, YC only (not ACK)
- CHANGE | The idea must have real interview or news footage of the subject, because film clips are off for us | ACK news anchor 38.7 to 41 s | list 3+ real clips before scripting | METRO ONLY (film clips were Metro's crutch)
- DROP | Sponsor-fit topic choice (startups, investing) as a filter; we post organic | YC, EIN both match a venture product | none needed | paid reels only (EIN, YC)

## 2. Hook (first 3 s)
- USE | Line shape "This is / This might be [one of] the most [X] [person or photo] in [world]" | PAL "This is the most powerful man in Silicon Valley right now"; YC "This might be the most important photo in startup history" | read the first Whisper sentence | SAME IN ALL 4
- USE | One subject only: the hook photo, 13 to 16 words in the first 5 s (14 to 16 on Metro) | PAL 16 words, EIN 13 | ref_stats.py words in first 5 s | SAME IN ALL 4
- USE | The place or category word gets a big word or a background swap | PAL "Silicon Valley" big word 2.0 to 3.5 s and Golden Gate swap 1.88 to 2.25 s | frame strip of 0 to 3 s, by eye | METRO ONLY (seen PAL, ACK)
- USE | Do not say the person's name in the first 3 s; hold it to 8 to 17 s | PAL name at 8.0 s, ACK 10.0 s, YC 16.9 s | Whisper word timings | METRO ONLY (EIN names at 3.7 s)

## 3. Script
- USE | 230 to 250 words for 78 to 95 s, 171 to 184 words a minute, average sentence 12 to 14 words | PAL 235 words, 184 wpm, 13.8 | ref_stats.py words; interest_score.py sentence length | wpm SAME IN ALL 4; length METRO ONLY
- USE | Comparison slot at 4 to 8 s: "basically [character] in real life" or a famous rival group | ACK "basically the real Wolf of Wall Street"; YC "the PayPal mafia might finally be getting some competition" | read 4 to 8 s of transcript | METRO ONLY
- USE | Paradox line by 17 s: "the same thing that made him X nearly Y" | ACK "the same thing that made him ... nearly blew up his career" | judged | PAL, ACK only
- USE | Dated run of events, short active sentences, event words 29 to 60% | ACK 60%, PAL 29% | interest_score.py | SAME IN ALL 4
- USE | One turn at 35 to 75% of runtime | PAL "But Palmer's only the side piece" (35%); ACK Herbalife "and lost everything" (75%) | interest_score.py tags, judged | SAME IN ALL 4
- USE | Zoom out to now at 75 to 90%, "you" only near the end | PAL "Now look at what that crew runs"; ACK "And right now, some CEO just found out" | judged | SAME IN ALL 4 ("you": PAL, EIN only)
- CHANGE | Explaining words ran 12 to 47%; cap ours at 2 explaining sentences in a row and follow each with a picture or soundbite | PAL 32%, EIN 47% | interest_score.py longest explaining run | SAME IN ALL 4
- USE | Pass mark 18 of 24 with Interesting at 9 or more (they scored 20 to 22, judged) | ACK 22, PAL 20 | interest_score.py plus the 12 checks | SAME IN ALL 4

## 4. Pace
- USE | Median shot 0.54 to 0.75 s, 90th percentile 1.2 to 1.6 s | YC 0.54, PAL 0.75 | ref_stats.py | METRO ONLY (EIN 0.80, 1.93)
- USE | 7 to 9 shots in the first 5 s | PAL 7, ACK 9 | ref_stats.py | SAME IN ALL 4
- USE | 1.08 to 1.55 shots a second overall; fastest quarter is Q1 or Q2 | ACK Q2 1.81 | ref_stats.py by quarter | rate METRO ONLY; Q1/Q2 SAME IN ALL 4
- USE | Longest hold 4.1 to 6.6 s, only on a soundbite, built object or last shot | PAL Karp 51.9 to 56.2 s | ref_stats.py longest shot | METRO ONLY
- USE | 59 to 67% of cuts within 0.12 s of a word start; do not cut to the beat (beat hits at chance) | PAL 67%, beat 12% vs 14% chance | ref_stats.py | SAME IN ALL 4 (55 to 67% incl. EIN)
- USE | 5 to 8% of shots are 4 frames or less | YC 8.1% | ref_stats.py | SAME IN ALL 4
- Note: compare only within one tool; ffmpeg scene detection gives different shot counts (STUDY section 3).

## 5. Opener
- USE | 3x3 grid of white blocks reveals the hook photo in 0.5 to 1.3 s, a few cells at a time, faint grid lines stay | PAL 0.12 to 0.62, ACK 0.08 to 0.52, EIN 0.48 to 1.28, YC 0.00 to 1.25 | frame strip 0 to 3 s, by eye | SAME IN ALL 4
- USE | By 1.5 s the background darkens and the subject is cut out with a light rim | PAL 0.83 to 1.0, ACK 0.96 | by eye | METRO ONLY (seen PAL, ACK)
- USE | Background swaps cell by cell to the place word at 1.9 to 3.0 s | PAL Golden Gate 1.88 to 2.25; ACK Apple Park 2.76 to 2.96 | by eye | PAL, ACK only
- CHANGE | At most 1 extra hit in the first 3 s (each reel did a different one) | YC solarise to a print 1.29 to 1.50; EIN zoom blur 1.56 to 1.64 | flash_sheet.py | SEEN ONCE each
- DROP | Thermal 2-frame flash and red neon outline as defaults | ACK 0.80 to 0.88 and 1.36 to 1.52 | flash_sheet.py, invert_frames.py | SEEN ONCE
- CHANGE | Comparison beat at 4 to 8 s shows real footage of the subject plus the printed comparison line, not a film clip | PAL Iron Man 4.4 to 8.0 is what we replace | footage map review | METRO ONLY

## 6. Captions
- USE | Every spoken word on screen, each on its word start, 1 to 6 words a line, clear at phrase end | all reels, whole runtime | captions/*.jpg crops, by eye | SAME IN ALL 4
- USE | Clean grotesk sans, medium weight, sentence case; Inter Medium is the closest free match (judged) | ACK 26.0 s | side-by-side crop | SAME IN ALL 4
- USE | Cap height 37 to 40 px on 1078 (3.4 to 3.7% of height), centre at 44 to 52% height, words spread across the width beside the face | ACK 26.0 s 50%, ACK 12.9 s 44%, EIN 102.9 s 49% | crop measure, about ±3 px | SAME IN ALL 4
- USE | White on dark frames, black on white or cream paper, no box, no stroke | PAL white "valley" card 23.4 s | by eye | SAME IN ALL 4
- USE | 8 to 15 big words a reel (judged count), 3 to 4x size, bold, stacked or split around the subject, colour taken from the source | PAL "Tony Stark" red 4.5 to 5.9; ACK "THE REAL WOLF OF WALL STREET" yellow 5.3 to 6.9 | by eye | SAME IN ALL 4
- CHANGE | Build a per-word placer; style_captions.py sets only font, size and vertical offset | n/a | show one side-by-side crop before the full build | tool gap
- DROP | Condensed capitals in quotes, serif labels over faces, typing-cursor block | EIN 102 to 103, 4 to 6, 116.9 to 118.4 | by eye | SEEN ONCE (EIN)

## 7. Picture content
- USE | Real people first; each named person gets several different clips, not one repeated | YC 26.9 to 30.9 s | SHOT-LOG.md read | SAME IN ALL 4
- USE | One real soundbite where someone else owns the key line, hold 1.8 to 4.3 s, captioned | PAL Karp 51.9 to 56.2; ACK Forbes 72.9 to 79.4 | ref_stats.py longest shots | PAL, ACK only
- USE | News proof with chyron for dated events | ACK "2008 MARKET MELTDOWN" 38.7 to 41 | SHOT-LOG.md | METRO ONLY
- USE | Every figure printed as big type over the object | ACK 48.4 to 50.1 counter "1" to "1.4" | by eye | SAME IN ALL 4
- USE | Logo bursts on lists, 0.16 to 0.24 s per logo | ACK 23.3 to 25.4 (8 banks) | flash_sheet.py, ref_stats.py | SAME IN ALL 4
- USE | White paper cards and prints as breath beats every 10 to 20 s; bright frames (luma over 200) 11 to 14% | PAL 11.5%, YC 13.5% | colour_stats.py | cards SAME IN ALL 4; share PAL, EIN, YC (ACK 1.1%)
- USE | Colour symbols (chess, dice, explosion, banknotes) | PAL chess pieces; EIN dice | by eye | SAME IN ALL 4
- DROP | Feature-film clips (Iron Man, Wolf of Wall Street, likely The Godfather) | PAL 4.4 to 8.0; ACK 5.3 to 10.0 and 87.5 to 92 | footage map review | METRO ONLY
- CHANGE | Photo walk-through (B&W except the named person, 2-frame white silhouette, push, cut to footage) only for group-photo ideas | YC 26.9 to 30.9 | by eye | SEEN ONCE (YC; PAL in part)
- Note: moving footage share by tool is 35 to 51% (low trust, motion_class.py); by eye more than half of PAL, ACK, YC moves (judged).

## 8. Transitions
- USE | Inverted-frame cut: 1 frame negative of shot A, optional 1 white or black frame, then shot B; about 1 every 3 to 5 s on sentence turns (11.4 to 13.5 a minute) | ACK 18 events, YC 18 | invert_frames.py (lower bound), flash_sheet.py | METRO ONLY (PAL 2+, EIN 0)
- USE | Hard white single frames between shots | ACK 7.0, 10.0, 17.2 s; PAL 23.4 s | flash_sheet.py (CUT+FLASH 3 to 24 a reel) | SAME IN ALL 4
- CHANGE | Pixel mosaic, grey-block dissolve, light leak: 1 a reel at most | ACK 31.0, 29.8, 44.0 to 44.6 | flash_sheet.py | SEEN ONCE each

## 9. Colour and grade
- USE | Full colour: mean saturation 0.25 to 0.36, vivid pixels 15 to 22%, near-monochrome shots 20 to 24% | ACK 0.36, 21.6% | colour_stats.py at 2 fps | METRO ONLY (EIN 0.17, 71% mono)
- USE | Mean brightness 0.37 to 0.46, near-black pixels 21 to 25% | PAL 0.46, 21.4% | colour_stats.py | SAME IN ALL 4
- USE | Vivid hues warm-led: red plus orange/yellow 48 to 66%, cyan/blue 28 to 48% | YC 66% / 28% | colour_stats.py | SAME IN ALL 4
- USE | Soft edge glow or halation, slight vignette on paper #EDECEA to #F2F1EF (judged) | PAL 69.3 s framed photo | by eye on crops | SAME IN ALL 4
- DROP | EIN's archival black and white look as the template | EIN 71% near-monochrome | colour_stats.py | SEEN ONCE

## 10. Sound
- USE | Voice nearly non-stop: 3.5 to 6.6 s total pause (gaps over 0.12 s) per reel | PAL 3.5 s | Whisper word gaps, as in numbers.json | METRO ONLY (EIN 10.2)
- USE | Loud music bed 0.8 to 3.7 dB under the voice in gaps (low trust) | YC 0.8, ACK 3.7 | gap_level.py | SAME IN ALL 4
- USE | Cut on words, not beats (beat hits at chance in all 4) | ACK 20% vs 20% chance | ref_stats.py | SAME IN ALL 4
- CHANGE | Risers or hits on story turns, likely, not heard | YC loudness peaks 8 to 10, 42, 58 s | 2 s RMS | SEEN ONCE
- CHANGE | Voice: theirs was not heard; pick ours by ear against the reels | n/a | listen | default

## 11. Ending
- USE | Mirrored two-line kicker, the second line flips the first, no lesson, last 2 sentences; write it before the body | PAL "The PayPal Mafia built the internet you scroll all day. The Palantir Mafia built the thing quietly watching you do it." | read the last 2 sentences | SAME IN ALL 4
- USE | Callback picture under the kicker (the hook photo or its group) | PAL 69.3 to 76.7 | by eye | METRO ONLY (organic PAL, ACK)
- CHANGE | Hold after the last word 0.3 to 6.2 s on file; ours ends on the kicker plus callback, no sting | PAL 1.8 s | ref_stats.py, Whisper end time | varies
- DROP | 9 to 11 s ad tail and "Comment GUIDE" for our default organic post | YC 69.8 to 80.2 | n/a | paid only (EIN, YC)

## 12. What not to copy
- DROP | The M logo sting and any Metro or USVC mark | PAL 76.7 to 78.4; ACK 92.4 to 95.0 | by eye | PAL, ACK only
- DROP | Their exact captions, layouts or built objects frame for frame; same rhythm, our own footage and designs | PAL receipt 13.0 to 16.5 | side-by-side review | all
- DROP | Feature-film clips, the EIN look, thermal flash and neon outline as defaults (see above) | see sections 5, 7, 9 | footage map review | per rule

## Checklist for a finished cut (run in this order)
1. Format: 1920x1080, 25 fps, landscape. Length 78 to 95 s organic.
2. ref_stats.py: median shot 0.54 to 0.75 s; 90th pct 1.2 to 1.6 s; 7 to 9 shots and 13 to 16 words in first 5 s; 1.08 to 1.55 shots a second; fastest quarter Q1 or Q2; 59 to 67% cuts on word starts; beat hits near chance; 5 to 8% shots of 4 frames or less; longest shot 4.1 to 6.6 s on proof only.
3. Words: 230 to 250, 171 to 184 a minute, total pause 3.5 to 6.6 s.
4. Script read: superlative hook line; name at 8 to 17 s; comparison at 4 to 8 s; one turn at 35 to 75%; zoom out at 75 to 90%; mirrored kicker; no more than 2 explaining sentences in a row; interest_score pass 18/24 with Interesting 9+.
5. Frames 0 to 3 s: one photo, 3x3 grid reveal done by 1.3 s, at most 1 extra hit.
6. invert_frames.py: about 11 to 14 inverted cuts a minute, on sentence turns. flash_sheet.py: white single frames present.
7. Captions crop: every word, Inter Medium, cap 37 to 40 px, centre 44 to 52%, black on white cards, 8 to 15 big words.
8. colour_stats.py: brightness 0.37 to 0.46, saturation 0.25 to 0.36, vivid 15 to 22%, near-black 21 to 25%.
9. gap_level.py: bed 0.8 to 3.7 dB under voice.
10. Picture: real people, one soundbite, printed numbers, logo bursts, white card every 10 to 20 s, no film clips, no M sting, no ad tail.
