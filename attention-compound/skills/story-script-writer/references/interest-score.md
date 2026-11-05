# The interest score, v1 (3 Nov 2026)

Catches a script or plan that is an information exchange before anyone writes more of it.
Built from 4 scripts: Sam Altman, Elon Musk and Max Verstappen (Attention Compound), and a birthday photo reel (insightsasymmetric).
Tags and the 0 to 2 marks are judgement, with no view data behind them. Calibrate on your own results.

**There is no separate simplicity score.** Simplicity is the Simple group below, 8 of the 24 points, plus the measured reading numbers.

## The 12 checks, 0 to 2 each
| Group | Check | 2 means |
|---|---|---|
| Interesting | Picture | A stranger can see one moment |
| Interesting | Action | 40% or more of the words are events |
| Interesting | Want | Someone wants something, and we know what |
| Interesting | Hook paid | The payoff is bigger than the hook's promise |
| Interesting | Turn | Something you did not see coming |
| Interesting | Return | A detail from the first quarter comes back changed |
| Simple | One thread | Retold in one sentence by a stranger |
| Simple | Info run | No more than 2 explaining sentences in a row (1 point for up to 5) |
| Simple | Terms | Every hard term explained in a clause or removed |
| Simple | Sentences | Average 15 words or fewer |
| Massy | Known name | A stranger knows a name in it |
| Massy | Daily picture | An everyday thing or comparison anyone gets |

## Pass mark (proposed)
18 of 24, with Interesting at 9 or more. Below that, change the story, not the words.
Run it on the plan, then on each finished part. A plan has no sentences, so score it out of 22 (no Sentences check). A plan scored by its writer runs high, so trust the script score.

## Scores so far
| | Sam | Elon | Max | Birthday | Our first script |
|---|---|---|---|---|---|
| Interesting (12) | 11 | 11 | 12 | 12 | 2 |
| Simple (8) | 7 | 8 | 7 | 7 | 3 |
| Massy (4) | 4 | 4 | 3 | 2 | 1 |
| **Total** | **22** | **23** | **22** | **21** | **6** |

Our rewritten story scored 21 of 24, self-scored: 52% event words, 22% explaining, longest explaining run 3, reading ease 81.

## Measured
| | Sam | Elon | Max | Birthday | Our first script |
|---|---|---|---|---|---|
| Words where something happens | 47% | 40% | 79% | 71% | 6% |
| Words that explain or describe | 29% | 31% | 4% | 12% | 76% |
| Words that build tension | 24% | 29% | 17% | 17% | 18% |
| Most explaining sentences in a row | 5 | 2 | 1 | 1 | 9 |
| Words before the first event | 36% | 13% | 0% | 14% | 51% |
| Average sentence, words | 10.7 | 12.4 | 14.3 | 15.6 | 11.5 |
| Hard words (3+ syllables) | 8.3% | 7.3% | 10.4% | 7.6% | 9.1% |
| Reading ease (higher is easier) | 76 | 80 | 68 | 71 | 80 |

## What made them interesting and simple
1. Things happen. Even the explaining parts are short and lead to an action.
2. Explain in one clause, then move. Each unknown name gets a few words.
3. One picture carries the idea.
4. One thread, retold in a sentence.
5. The hook gets paid.
6. No system is explained for its own sake.

## How to tag
One sentence per line in a text file:
```
T| The hook line that makes a promise.
I| A line that explains something.
E| A line where someone does something.
```
Then run:
```bash
python3 interest_score.py script_tagged.txt
```

## Not covered
Delivery, visuals, music, real clips and audience data.
