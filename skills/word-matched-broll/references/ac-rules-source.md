# What Attention Compound shows while the voice runs (4 Nov 2026)

Read from every shot of all 3 reels with the words said over it: Altman 179 shots, Elon 196, Max 85.
Sheets: `research/ac-rules/*.jpg`, shot lists `*_shots.json`, tool `tools/ac_shot_words.py`.
By eye, from one middle frame per shot, with no playback or sound. Measured numbers are cut detection.

## Measured
| | Altman | Elon | Max | v3 |
|---|---|---|---|---|
| Shots | 178 in 86 s | 195 in 76 s | 84 in 91 s | 175 in 113 s |
| Median shot | 0.29 s | 0.20 s | 1.00 s | 0.33 s |
| 90th percentile shot | 1.06 s | 0.93 s | 1.71 s | 1.52 s |
| Longest shot | 4.13 s | 2.67 s | 5.70 s | 3.40 s |
| Caption height in frame | about 47% | about 47% | about 50% | 68% |

## The rules
1. **The picture is the word.** Nearly every cut lands on a spoken word, and the shot shows that word. Altman: "OpenAI" is the logo, "on Earth" is the Earth, "control" is statues, "Friday" is a clock face, "kill switch" is a switch.
2. **Bursts, then holds.** Idea words get 0.05 to 0.25 s flicker bursts. Proof gets 1 to 4 s holds. Altman: "control." has 8 images in 0.9 s, then "$86B" holds 3.0 s and "$852B" holds 3.25 s. v3 cut evenly on half-beats, which is why it felt like noise.
3. **A name gets many looks of that person, never one interview.** Altman has 8 different clips in the first 3 s. Elon has 12 in the first 1 s. v3 used one man in 13 shots from about 4 backgrounds.
4. **Proof is a news host or chyron that says the line.** "OPENAI VALUED AT $852B", "OUSTED CEO'S SURPRISE MOVE", "MUSK CONSIDERING COLLEGE STATION FACTORY". The chyron is on the word, and readable.
5. **An idea gets a symbol, treated hard.** Statues, Vitruvian Man, atoms, skulls, chess. Mostly high-contrast black and white on black. Never a generic tech shot. Keyboards and server rooms: 0 in all 3 reels.
6. **A number gets a print.** Big on screen, over the host or the object.
7. **Black with one glowing word is the breath.** "For context,", "their lives.", "GONE.", "into this", "sentence.". 0.5 to 1.2 s, about every 10 to 20 s, usually before a turn.
8. **Built objects carry a whole phrase.** Elon's TV holds across 6 s with cutaways. Max's TV holds 5.7 s. A polaroid on wood holds 1.9 s. The object comes back later as a callback.
9. **Captions sit in the middle of the frame,** 1 to 3 words, small, serif mixed with bold sans, right over the picture.
10. **Colour swings shot to shot.** Blue set, red set, black and white, green terminal. Much of it comes from the sources.
11. **Hard flash cuts** with giant blurred letters mark the big turns, not every cut.
12. **Real soundbites.** "Five years" and "Sam Altman is apparently back" play real audio. Not used here, because the script and voice are locked.

## Where this job cannot follow
- Rule 3 is limited: about 5 CEO interviews, most of them seated, and all of them recent.
- Rule 12 would need a script change.
- Break-in: no footage exists, so rule 8 carries it.
