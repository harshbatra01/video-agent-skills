# B-roll fix plan, from the v3 review (4 Nov 2026)

User verdict on v3: visuals far off, mismatched with the references. "The main issue right now is the B-roll. Fix the B-roll. Make it as closely similar as possible to the reference. Fix it, or tell me it cannot be fixed."

## How this was scored
- v3: all 156 shots, one middle frame each. Labels: `research/broll_v3/labels_v3.py`. Sheets: `research/broll_v3/ours_sheet_*.jpg`.
- Attention Compound: Elon and Max read at 1 frame a second. Altman read from the 24-frame sheet only. Those are the 3 AC reels on disk.
- Marks by category, one reviewer's judgement. No playback, no sound. Subject size is an eye estimate. The user's taste outranks all of it.

## Totals for v3 (108.8 s scored)
| Measure | v3 | Bar |
|---|---|---|
| B-roll score | 6.8 | 8 to ship, skill rule. Altman was 8.3 on an earlier scoring |
| Time that misses the words (M 2 or less) | 38.5 s, 35% | Under 5%. Altman 3% |
| Generic stock: keyboards, server rooms, cables, stock laptop and silhouette | 25.9 s, 24% | None seen in AC Elon or Max |
| Stock in the break-in story, 23 to 50 s | 15.0 of 27.3 s | |
| Named people and news | 38.4 s, 35% | AC Elon about 61% of seconds, by eye |
| Moving video, tool | 62.0 s, 57% | About 67% |

Moving share is close. It is not the main problem. What is on screen is.

## What AC does that v3 does not
1. Almost every second is the real person or the real event. Elon: his own clips and news. Max: the driver, the father, the actual race.
2. When it leaves real footage, the picture is a built, specific object tied to one word: old TV with the "five years" clip, a line-drawn pistol on cream, a white 3D slab for the factory, Central Park for "three central parks".
3. Abstract AI in Altman is heavily treated: code particles, green-tinted crowd, glowing rings. Never a plain keyboard.

## Can it be fixed
**Mostly yes, but not all the way to AC.**
- **Cannot match:** AC stars one famous person with years of footage. This story's lead is an AI, and the break-in happened inside a test, so no footage of it exists. 23 to 50 s must be built, not filmed. That section will differ from AC.
- **Can fix:** the rest. Projection, not a measurement: about 7.9, close to the 8 bar, if the 38.5 s of misses become on-word shots.

## Fix table
| Time | Words | Now | Problem | Replace with | Source |
|---|---|---|---|---|---|
| 0.0 to 4.8 | document for investors | Same man, 13 shots | No document shown | Filing pages, Claude and Anthropic stills, then the CEO | On disk: Forbes, ABC |
| 4.8 to 6.9 | resist shutdown | Server, keyboard | Generic | ABC filing card, filing text highlight | On disk |
| 10.8 to 11.5, 98.4 to 100.8 | IPO, opening bell | Fifth Third Bank, CNBC logo, SpaceX day board | Another company's branding | NBC and Bloomberg Anthropic chyrons | On disk |
| 17.3 to 22.2 | testing, real computer systems | Server rooms | Generic | Filing text, then one built element | Built |
| 23 to 50 | the break-in | Keyboards, servers, silhouette, WSJ reporter on "same name" and "real users" | Unrelated people, repeated hands | One built look: fake company page, terminal, the 433 users, the email and chat pull, in AC's object style | Built. Labelled as illustration |
| 58.8 to 70.1 | OpenAI, Hugging Face | Altman at the Senate, chyron on Anthropic's valuation | Chyrons say something else | CBS Hugging Face segment, Hugging Face logo and site, OpenAI | Partly on disk, Hugging Face to source |
| 70.8 to 79.1 | 141,006 test runs | Server rooms | Generic | Test run counter already built, held longer | Built |
| 90.3 to 92.8 | saw the signs, it stopped | Server rooms | Generic | CEO from the 60 Minutes and Bloomberg clips | On disk |
| 105.1 to 105.7 | and Anthropic | Senator at a hearing | Off the words | CEO or filing text | On disk |

## Checks before showing
- Who each named lower third shows was not verified by Claude from faces. Check "Dario Amodei, CEO" against the source title or captions before the next render.
- `V35nBNzfS88` and `B-QYMpjnsWo` carry stock watermarks. Unused in v3. Keep them out.
- Run the checklist in `edit-loop-guard`, including `tools/guard_check.py`.

## Order
1. Frame sheet of the replaced shots beside AC, no render. User verdict.
2. Build the 23 to 50 s look as a 5 s test first.
3. Full render as v4 only after both pass. v3 stays untouched.
