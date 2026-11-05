---
name: reference-study
description: Measure a reference video before copying it, and turn the study into a use, change or drop list. Holds what we measured on the Altman, Attention Compound and Asymmetric Insights reels, how far each number can be trusted, the devices seen and the approved opening limits. Use when the user shares a reference, asks why a video retains, asks to compare an edit with a reference, or before planning a new style. Pair with minidoc-reference-style for frame-level method.
---

# Reference study

Claude reads frames and numbers. It cannot watch motion or hear. These are 4 references and 1 flop, so they show patterns, not proof.

## Main finding
**Cut speed did not separate our flop from the references. How much the viewer had to take in did.**
- Our Elon video had 17 shots in its first 5 s, inside the references' 7 to 19.
- Altman's first 5 s stays on one subject. Elon's moved through about 5.
- The user's rule: keep changing the visuals, not the context.
- Our Elon video got under 500 views. No watch data is on file, so this is a likely cause, not a proven one.

## Numbers
| | Altman | AC Elon | AC Max | Asym birthday | Our Elon v18 |
|---|---|---|---|---|---|
| Format | 960x720 | 1276x718 | 720x1280 | 720x1280 | 1080x1920 |
| Length | 86 s | 76 s | 91 s | 145 s | 40 s |
| Likes | Not on file | 45,689 | 315,111 | 318,475 | Not on file |
| Median shot | 0.38 s | 0.33 s | 0.80 s | 1.60 s | 0.33 s |
| Shots in first 5 s | 12 | 19 | 7 | 10 | 17 |
| Words in first 5 s | 16 | 17 | 19 | 19 | 18 |
| Moving share, tool | 39% | 35% | 64% | 6% | 10% |
| Brightness | 0.36 | 0.42 | 0.39 | 0.26 | 0.24 |
| Near-black pixels | 36% | 23% | 19% | 51% | 44% |
| Vivid pixels, warm | 56% | 50% | 81% | 84% | 86% |
| Vivid pixels, blue | 34% | 46% | 15% | 12% | 11% |

A later, finer detector found 178 shots at 0.29 s median for Altman (`word-matched-broll`). Only compare numbers from the same tool and threshold.

## How far to trust these
- **Rough sound hits:** unreliable. A bare voice with no effects scored 415 a minute. Do not use the count on references. Use cue lists for your own videos.
- **Moving share:** the tool undercounts calm talking clips. Altman reads 39% by tool and 67% by hand. Compare tool to tool only.
- **Likes:** not views, and pages differ in size.
- **Median alone misleads.** Measuring only the median made our first cut 4 times too slow. Contact sheets also hid motion, so check every frame of key moments.

## Opening limits (approved by the user, 4 Nov 2026)
| First 5 s | Limit |
|---|---|
| Subjects or ideas | 1, or 2 at most |
| Rough sound hits | 20 or fewer, a weak signal |
| Shots | 12 to 19 is fine |
| Graphics that must be read | 0, captions only |
| Real moving clips | Most of the screen time |

## Sound mix finding
Music and effects sit 2.5 to 4.7 dB under the voice in the voice gaps of the references. Elon sat at -0.5 dB. Our first tests at about 10 dB under were too quiet. `scripts/gap_sfx.py` measures this.
Sounds in references cluster, with quiet stretches of 21 to 56 s. Our 35 evenly spaced cues looked overstimulated, so we cut to 13 on real turns.

## Devices seen, by frame
- **AC Elon:** negative portrait as a single frame, person cut out over a themed object, talking head in an old TV, white line drawing on black, mirror image, icon on cream, news wall, bright white frames.
- **AC Max:** one word in a white box in mono type, pair of CRT monitors, polaroid on wood, small coloured label tag, stacked headline clippings, bold place word over footage.
- **Asym birthday:** pixelated photo that resolves and grows, running total with logos, parchment cards, tweet cards with yellow highlight, simple red bar chart, movie clip with title and year tag, rounded news clips on blur.

## End every study with
A numbered list. Each item is marked use, change or drop, with where it goes. The user sees it before the first build. A study that never reaches the edit was the user's first complaint.

## Tools
`scripts/gap_sfx.py` (levels in voice gaps), `scripts/beat_map.py` (tempo and beat grid), `scripts/time_sheet.py` (frame sheets by time). Also `word-matched-broll/scripts/` and the scripts in `minidoc-reference-style`.
