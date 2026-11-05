---
name: word-matched-broll
description: Decide what is on screen for every spoken word in a narrated mini-doc, using rules read from 460 Attention Compound shots. Covers bursts and holds, real chyrons as proof, symbols for ideas, built objects when no footage exists, captions, colour, and how to build and check a word-anchored shot list. Use when planning or fixing B-roll, when visuals feel random or mismatched, when asked to match a reference's visuals, or before building a storyboard or shot list for a voice-over.
---

# Word-matched B-roll

Why this exists: v3 of the Anthropic video cut evenly on a beat and treated the picture as filler. The user rejected it. Scored after that: 35% of screen time missed the words and 24% was generic stock.
The rules come from all 460 shots of 3 reels, read against the words spoken over them (Altman 179, Elon 196, Max 85), using one middle frame per shot, with no playback or sound.

**Status:** v4, built on these rules, has not had the user's verdict or any posted result. They are closer to the reference by measurement, not proven to perform.

## The rules
1. **The picture is the word.** Nearly every cut lands on a spoken word, and the shot shows that word. "OpenAI" is the logo. "Friday" is a clock face.
2. **Bursts, then holds.** Idea words get 0.05 to 0.25 s flicker bursts. Proof gets 1 to 4 s holds. Altman's "control." has 8 images in 0.9 s, then "$86B" holds 3.0 s.
3. **A name gets many looks of that person.** Altman has 8 different clips in the first 3 s. Elon has 12 in the first 1 s. Never one interview repeated.
4. **Proof is a news host or chyron saying the line.** On the word, and readable.
5. **An idea gets a symbol, treated hard.** Statues, atoms, skulls, chess. Mostly high-contrast black and white. Keyboards and server rooms: 0 in all 3 reels.
6. **A number gets a print.** Big on screen, over the host or object.
7. **Black with one glowing word is the breath.** 0.5 to 1.2 s, about every 10 to 20 s, usually before a turn.
8. **Built objects carry a phrase.** A TV, a polaroid on wood. They hold across cutaways and come back later.
9. **Captions sit mid-frame,** about 47% height, 1 to 3 words, small, serif mixed with bold sans. Move them off logos and chyrons.
10. **Colour swings shot to shot.** Much of it comes from the sources.
11. **Hard flash cuts** with giant blurred letters mark big turns, not every cut.
12. **Real soundbites** where the script allows.

## Measured targets
| | Altman | Elon | Max |
|---|---|---|---|
| Shots | 178 in 86 s | 195 in 76 s | 84 in 91 s |
| Median shot | 0.29 s | 0.20 s | 1.00 s |
| 90th percentile | 1.06 s | 0.93 s | 1.71 s |
| Longest | 4.13 s | 2.67 s | 5.70 s |
| Caption height | about 47% | about 47% | about 50% |

Altman colour: brightness 0.36, near-black 36%, saturation 0.31, vivid 13.8%. Colour numbers are a warning light. The user's eye decides.

## The method
1. **Study the reference.** `scripts/ac_shot_words.py <video> <words.json> <prefix>` writes one frame per shot with its words, plus a shot list. Word files need `w` with `s`/`e` or `t0`/`t1`.
2. **Scan your sources.** `scripts/scan_sheet.py <clip> <every_s> <out.jpg>` makes timecoded sheets. Pick shots by the sheet, then look at the exact frame.
3. **Plan by word.** Anchor every shot to a word time from the real voice, never to a beat or a timer.
4. **Fill in this order:** real footage of the thing, news chyron that says it, filing or document, hard symbol, built object from a real photo.
5. **Test a short clip first,** beside the reference, and get a verdict before a full render.
6. **Check every shot.** Run step 1 on your own render and read each frame against its words.
7. **Report the real share.** Measure time per type on the final cut. A plan count is not a measurement.

## Check every shot for
Our shot check caught all of these:
- A headline or chyron on a different topic.
- Readable emails or logs from a different event.
- Hosts or interviewers in frame instead of the subject.
- Burned-in timestamps, stray people, an object blocking the frame.
- Captions over logos or chyrons.
- A prop on the wrong scale. A stadium for 433 people was still in v4.
- The same person repeating across a long stretch.

## When no footage exists
- Say so before building, with options. Never quietly fill with stills.
- Build objects from real photos, not flat drawings. The user approved the look only after this change.
- Label illustrations on screen. Do not let real footage imply it shows the event.
- Watch long runs with no people. Our 28 s run is longer than any we saw in AC, and it is a known weak spot.

## Honest result on v4
113 s, 1.5 cuts a second, median 0.40 s, against Altman's 2.1 and Elon's 2.6. Real clips were 49% of screen time, not the 70% we estimated from the plan. AC Elon is about 61% by eye.

## Tools
`scripts/ac_shot_words.py`, `scripts/scan_sheet.py`, `scripts/colour_stats.py`. Needs Python with Pillow and numpy, plus ffmpeg.
`examples/anthropic-ipo/BROLL-V4-PLAN.md` shows a finished word-by-word shot plan.

Source note with job details: `references/ac-rules-source.md`. To score B-roll, use skill `broll-scoring`.
