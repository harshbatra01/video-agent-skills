# B-roll v4 plan, line by line (4 Nov 2026)
Script v5 and voice unchanged. Times from `vo/v2/words.json`. Frames: `research/broll_v4/pairs/`, tool `tools/broll_v4_frames.py`, source scan sheets `research/broll_v4/scan/`.
Source seconds below come from the scan sheets. Planned, not built.

| Time | Words | Picture | Source | Kind |
|---|---|---|---|---|
| 0.0 to 6.0 | document for investors, resist shutdown | Reporter holding the pages, real filing stack, filing card | ABC M8j_Py_TQ9k 37, S-1 pages, ABC 57 | Real, built object |
| 6.8 to 8.5 | not even the scariest part | Black, glowing word | Built | Built |
| 9.1 to 14.7 | IPO, by law, what could go wrong | NBC "going public" 0, Capitol 60 Min 776, Bloomberg chyron 96 | On disk | Real |
| 15.2 to 21.5 | testing, broke into real systems | 60 Min team 364, filing page with highlight | On disk | Real |
| 22.2 to 24.3 | fake company | Polaroid on wood | Built, illustration | Built |
| 24.9 to 26.6 | hack it | Real old-TV photo, "> hack it" on its screen | `research/props_v4/tv_vintage.jpg`, illustration | Built |
| 26.9 to 30.3 | no internet, internet was on | NASA Earth at night, lights removed, lights on at "internet was on" | `earth_night.jpg`, illustration | Built |
| 30.8 to 33.7 | 1,800 moves, got nowhere | 1,800 dots, then the locked gate | `door_locked.jpg`, illustration | Built |
| 34.1 to 38.1 | same name | Two name cards, names hidden | Built, illustration | Built |
| 38.6 to 43.7 | 433 real users | Endless mailboxes | `mailboxes.jpg`, illustration | Built |
| 44.1 to 49.7 | emails, account, chats | Mailboxes, shredder on "deleted", switchboard on "chats" | Commons photos, illustration | Built |
| 50.3 to 57.2 | had no idea, biggest question | CEO close, 60 Min | On disk | Real |
| 57.8 to 62.3 | most infamous moment | OpenAI logo CBS 6 to 12, news wall of on-topic clips only | On disk | Real |
| 63.0 to 70.2 | OpenAI, Hugging Face | Bloomberg rN_7QlYg_b8 18 chyron and 42 card, CNBC Y7XVEZZZ0bA 64 Hugging Face CEO | On disk | Real |
| 70.7 to 75.3 | 141,006 test runs | 60 Min dual screens 672 with the number | On disk | Real |
| 75.8 to 78.5 | three break-ins | CNBC card at 18: "Anthropic says its models hacked 3 companies in testing" | On disk | Real |
| 79.1 to 81.9 | Researchers asked | Old TV holding 60 Min 560 | Built plus real | Real in object |
| 82.5 to 89.8 | yes, wasn't allowed | Typed answers, cut with 60 Min researcher 544 to 600 | Built plus real | Half |
| 90.3 to 97.9 | it stopped, built to be careful | Senate, nameplate, ZC58H12VOHk 90, table 190 | On disk | Real |
| 98.4 to 101.1 | IPO before end of November | NBC 18 to 42, Bloomberg | On disk | Real |
| 101.7 to 106.8 | could get sued | Real filing text, highlighted, then gavel | On disk | Real, built |
| 107.5 to 111.5 | will Anthropic still stop | CEO close 60 Min 768 | On disk | Real |

Planned share by time: about 70% real people, news and filing pages, about 30% objects (32.7 of 111.5 s). AC Elon is about 61% real by eye. A plan count, not a measurement.

## Out for good
Keyboards, server rooms, cables, stock laptop, silhouette, Fifth Third, CNBC logo, SpaceX board, Altman Senate chyrons on the OpenAI lines, WSJ reporter on "same name". Stock files V35nBNzfS88 and B-QYMpjnsWo stay out.

## To check before a render
- 60 Min logs at 560 to 672 are from a different Anthropic test. Keep them unreadable and off the break-in story.
- The filing says these tests were built by a third-party partner. Anthropic's office on "during testing" is an illustration of people at work.
- Page a.png says "Four of our models" while the script says three break-ins. These may not conflict, but it was not rechecked. Do not show that sentence large until checked.

## Sourced 4 Nov 2026, with the user's OK
Clips: `Y7XVEZZZ0bA` (CNBC, Hugging Face CEO), `rN_7QlYg_b8` (Bloomberg). Photos and licences: `research/props_v4/CREDITS.tsv`. CC BY and CC BY-SA photos need credit when posted.

## Test
`research/broll_v4/test/Anthropic_IPO_breakin_test_v1.mp4`, 22.1 to 30.5 s, 8.4 s, tool `tools/broll_v4_test.py`. Audio is the v3 mix, with stand-in music and v3 sound cues.
