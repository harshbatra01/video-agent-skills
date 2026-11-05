# Audit of DRAFT-v1 against every script check in the repo (6 Nov 2026)

> Update 6 Nov 2026 (user verdict): there is no film-clip rule and no licence restriction. Any copyrighted clip, including feature films, may be used. Mentions of "no film clips" below are out of date.

Tools run: `story-script-writer/scripts/interest_score.py`, and `mass-reel-writer/scripts/reel_metrics.py` on v1 and on the 3 Metro transcripts (PAL, ACK, YC), so they are compared with the same tool. Checklists scored by hand: the interest score's 12 checks, the mass-reel-writer scorecard, the script-lab review (Callaway, house hook rules K1 to K13, house voice), first-three-seconds, the Metro formula (STUDY.md s7) and the sprint findings (S3, S5, S8).

**Note on fit:** `mass-reel-writer` and `script-lab` were built on 35 to 60 s talking-head founder reels. Their word targets (100 to 170) and list-shape rules do not apply to an 80 s narrated mini-doc. Where they conflict with measured Metro data, Metro wins (they rank measured data above practitioner advice).

## 1. Same-tool metrics: v1 against Metro (`reel_metrics.py`)
| Metric | v1 | PAL | ACK | YC | Verdict |
|---|---|---|---|---|---|
| Words | 246 | 234 | 250 | 229 | OK |
| Average sentence | 11.2 | 13.8 | 13.9 | 12.1 | A little choppier than the page |
| **Numbers per 100 words** | **5.7** | 2.6 | 2.8 | 3.9 | **Miss: 1.5 to 2 times the page.** In range for mass-reel-writer (3 to 6), but the page itself is sparser |
| Numbers in total | 14 | 6 | 7 | 9 | Miss |
| "You" | 3 | 2 | 1 | 1 | Slightly more than the page; fine (K11) |
| Questions | 0 | 0 | 1 | 0 | OK |
| "But"/contrast words | 1 | 4 | 0 | 2 | OK |
| Instructions | 0 | 0 | 0 | 1 (ad) | OK |
| First sentence (words) | 9 | 19 | 20 | 24 | **Different.** Metro first sentences are long ("This is X, and he's basically Y"). See section 4 |

Tool caveat: its brand list is India and US-commerce specific and matches substrings (it counted "bing" inside "climbing"), so "named anchors" is unreliable here. By hand, v1 has 8 known names: Nvidia, Jensen Huang, Warren Buffett, Masayoshi Son, Jack Ma, Alibaba, OpenAI, ChatGPT.

## 2. Interest and simplicity (`story-script-writer`)
- Interest score: Interesting 12 of 12, Simple 7 of 8, Massy 4 of 4: **23 of 24** (self-scored, so it runs high).
- Simple group: one thread 1 (2000 and Alibaba are side steps), info run 2, terms 2, sentences 2.
- Reading ease 76 (refs 68 to 80). Hard words 6.7%, simpler than all 4 references (7.3 to 10.4%).
- Simplicity risk (house voice V1, a 14-year-old understands every line): "the dot-com crash" may mean nothing to a young viewer. It needs a 3-word gloss or a picture that explains it.

## 3. mass-reel-writer scorecard (0 to 2; ship at 15+)
| # | Dimension | Mark | Reason |
|---|---|---|---|
| 1 | Reveal, not homework | 2 | A story about the world, no instructions |
| 2 | Breadth | 2 | Nvidia and ChatGPT are household words |
| 3 | Gap in the first breath | 1 | The gap ("sold Nvidia twice") lands in sentence 2, not 1 |
| 4 | Known anchors | 2 | 8 known names |
| 5 | Counted shape | 2 | Two acts: first sale, second sale |
| 6 | Low-effort ask | 2 | No ask (organic) |
| 7 | Promise kept | 2 | "Twice" and "cried" are both paid |
| 8 | Emotion | 2 | Disbelief and irony |
| 9 | Number discipline | 1 | 14 numbers; "150 billion" twice in 3 sentences, plus $4B, $5.8B, $64.6B and 3 years |
| 10 | Kept or quoted | 2 | "The fish that got away" line |
| | **Total** | **18 of 20** | Passes |

## 4. House hook rules (script-lab K1 to K13) and first-three-seconds
| Rule | v1 | Note |
|---|---|---|
| K1: about 12 words, done by 3.5 s; first sentence at most 16 | Pass | 9 words |
| K2: a famous name or number in the first breath | **Fail** | Sentence 1 has neither; Jensen Huang and Nvidia come in sentence 2, at about 4 s |
| K3: a famous name in the first 4 words | **Fail** | Metro's own hooks fail this too: they hold the name |
| K4: 2-second test (a stranger names the subject, number and why it matters) | **Partial** | It depends on the photo showing Jensen Huang clearly, plus a big word on screen |
| K5: says what the video is | Partial | |
| K6: a gap | Pass | |
| K8: line two is an open loop | Pass | "And the second time, he cried doing it." |
| K9: body pays it off | Pass | |
| K10, K13: no greeting, no fake number | Pass | |
| K11: "you" | Pass | |
| K12: curiosity tease paid by about 6 s | Mixed | "Most expensive photo" is paid at 4 s. "Cried" is paid at 78%, a deliberate open loop as in AC and Metro |
| First 3 s: a real clip moves in the first second | Open | A storyboard question: grid reveal on a photo |

**The rules conflict here.** The house rules (K2, K3) want the famous name first. Metro holds the name back and leans on a famous face in the photo. The red-team cap (14 words) also conflicts with Metro's measured first sentences (19 to 24 words). The sprint red team said Metro hooks are 10 to 11 words, but the same-tool count says 19 to 24. That red-team claim was wrong.

## 5. Metro formula and sprint analytics
| Item | v1 | Note |
|---|---|---|
| Photo hook, comparison, name at 8 to 17 s, paradox, dated events, real voice, turn, "you" zoom-out, mirrored kicker | All present | |
| Dates said | 3 (2000, 2017, 2019) plus "last year" | **More than the page:** PAL 0, ACK 2 |
| Comparison type | A real person (Buffett) | **S3:** the two top organic reels both used a "basically [movie hero]" line (Tony Stark, Wolf of Wall Street). A movie reference in the voice needs no film clip on screen. Unproven with 4 reels |
| Subject | One famous living man | Matches the top performers (S3) |
| Organic, no CTA | Yes | Matches the top performers (S3) |

## 6. Truth gate (goal-alignment-review, Truth)
Not passed yet. No fact is VERIFIED at its source, 1 fact has one source (the 2025 rebuy), and neither clip is found. This blocks locking, not drafting.

## Fixes proposed for v2
1. **Cut numbers from 14 to about 9:**
   - Drop "2017" (say "years later").
   - Drop the Alibaba value line or the second "150 billion".
   - Keep $70B, $20M, six minutes, $150B (once), $5.8B and $64.6B.
2. **Put a famous name in sentence 1 (K2):**
   - Keeps the Metro superlative: "This might be the most expensive photo in AI. The man next to Jensen Huang sold Nvidia. Twice." (current, fails K2).
   - Or Metro-length with the name inside: "This might be the most expensive photo in AI, because the man next to Jensen Huang sold Nvidia. Twice." (one 19-word sentence, Metro-shaped, passes K2).
   - Or the house rule: "This man sold Nvidia before the AI boom. Twice."
3. **Comparison:** keep Buffett, or test a movie-hero line in the voice only (needs a fitting hero; no film on screen).
4. **Gloss "dot-com crash"** in 3 words, e.g. "when the first internet bubble burst".
5. **Lengthen 2 or 3 short sentences** toward the page's 12 to 14 average.
