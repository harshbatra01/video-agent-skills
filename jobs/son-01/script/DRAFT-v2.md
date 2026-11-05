# Son script, draft v2, with hook options and comparison variants (6 Nov 2026)

**Status: draft, not locked.** It applies the fixes from AUDIT-v1:
- numbers cut from 14 to 11;
- famous names in the first sentence;
- "dot-com crash" replaced by "the internet bubble burst";
- sentences lengthened to the page's average;
- "a few years later" corrected to "years later" (Alibaba 2000 to Nvidia 2017).

## Part 1: hook options
Every hook below is followed by the same body. The table checks each against the house hook rules (script-lab K1 to K3) and the Metro shape (a long first sentence of 19 to 24 words, "This is / This might be the most...", with the name held back).

| ID | Hook (first sentence) | Words | Famous name or number in sentence 1 (K2) | Name in first 4 words (K3) | Metro shape | Needs | Facts |
|---|---|---|---|---|---|---|---|
| **H1** | This might be the most expensive photo in AI, because the man next to Jensen Huang sold Nvidia. Twice. | 18 + 1 | Yes | No | Yes | A real photo of Son beside Jensen Huang | B, plus framing |
| H2 | This is the man who sold Nvidia before the AI boom, and then did it again. | 16 | Yes | No | Yes ("This is the man") | Any photo of Son | B |
| H3 | This man sold Nvidia twice, and the second time, he cried doing it. | 13 | Yes | Yes | Partly | Any photo of Son; it absorbs the open loop, so line 2 becomes the comparison | B |
| H4 | This man missed out on 150 billion dollars by selling Nvidia, and then he sold it again. | 17 | Yes, number and name | No | Partly | Any photo of Son | B (his own estimate) |
| H5 | Every time you ask ChatGPT something, you're using this man's biggest bet, and he sold Nvidia to make it. | 19 | Yes | No | Yes in length | A ChatGPT screen, then Son | B |
| H6 | This might be the most expensive photo in AI: the man next to Jensen Huang sold Nvidia to bet on ChatGPT. | 21 | Yes | No | Yes | The Son and Huang photo | B, plus framing |
| H7 | This is the biggest gambler in AI, and he's basically Adam Sandler in Uncut Gems. | 15 | Yes (Adam Sandler) | No | Yes, like the Ackman reel's hook | Any photo of Son | Framing |
| H8 | This man once lost 70 billion dollars, and now he's betting 64.6 billion on ChatGPT. | 15 | Yes, numbers | No | Partly | Any photo of Son | B; this is the classic angle, already covered on YouTube |

**My ranking:**
1. **H1** if the photo exists. It's the exact Metro form and passes K2.
2. **H3** if there's no photo. It's the strongest on the house rules, with Nvidia as word 4.
3. **H4** to lead with a number.

H7 copies the Ackman reel's shape most closely, but it puts the comparison where the gap should be.

## Part 2: comparison line (swap one in; the rest of the script is unchanged)
| ID | Line | Fit | Rights | Note |
|---|---|---|---|---|
| A | He's basically the opposite of Warren Buffett, who holds his winners for decades. | Real-world contrast. The holding-versus-selling idea runs through the whole script | Buffett news footage needs a licensed source | Safest. "Holds for decades" is a characterisation (Coca-Cola, Apple) |
| B | He's basically Adam Sandler in Uncut Gems, betting everything on the next big win. | Movie hero, like the two top Metro reels. A gambler who can't stop | No film clip on screen (user default): printed text over Son footage | Strongest emotion; a younger audience knows it |
| C | He's basically James Bond at the poker table, always going all in. | Movie hero, widely known | Same as B | Bond wins at poker, so the comparison flatters him more than B |

## Part 3: v2 script (hook H1, comparison A)
This might be the most expensive photo in AI, because the man next to Jensen Huang sold Nvidia. Twice. And the second time, he cried doing it. He's basically the opposite of Warren Buffett, who holds his winners for decades. His name's Masayoshi Son, and the habit that made him a fortune is the same habit that keeps losing him one. In 2000, he was briefly the richest man on Earth, until the internet bubble burst and wiped out about 70 billion dollars. Around then, he gave a young founder named Jack Ma 20 million dollars after a six-minute meeting. That bet made him rich again, so he went looking for the next one. Years later, his fund put about 4 billion dollars into a gaming chip company called Nvidia. Then the stock dipped, and he sold every share. But Nvidia kept climbing, and the shares he sold would later be worth about 150 billion dollars. *[Son: "The fish that got away was big."]* So you'd think he'd never let go again. Last year, he bought back in, then sold every last share, 5.8 billion dollars' worth, to fund OpenAI. *[Son: "I was crying to sell Nvidia shares."]* Today he has 64.6 billion dollars in OpenAI, about an eighth of the company, and part of it is borrowed. So every time you ask ChatGPT something, you're using his biggest bet. The first time he sold Nvidia, it was the fish that got away. This time, he's betting OpenAI is the bigger fish.

## Measured (same tools as AUDIT-v1; files `draft-v2A/B/C_tagged.txt` and `_score.txt`)
| Measure | v2 A | v2 B | v2 C | v1 | Metro PAL / ACK / YC |
|---|---|---|---|---|---|
| Words | 252 | 253 | 251 | 248 | 234 / 250 / 229 |
| Narration at 175 wpm (plus about 5 s of clips) | 81 s | 81 s | 81 s | 80 s | 78 / 95 / 80 s total |
| Average sentence | 14.0 | 14.1 | 13.9 | 11.8 | 13.8 / 13.9 / 12.1 |
| Event words | 44% | 44% | 45% | 47% | 29% / 60% / 55% |
| Explaining words | 18% | 18% | 18% | 21% | 32% / 12% / 25% |
| Longest explaining run | 2 | 2 | 2 | 2 | 2 / 1 / 4 |
| Reading ease | 74 | 74 | 75 | 76 | 69 / 74 / 69 |
| Hard words | 6.9% | 6.5% | 6.1% | 6.7% | refs 7.3 to 10.4% |
| Numbers (per 100 words) | 11 (4.4) | 11 (4.4) | 11 (4.4) | 14 (5.7) | 6 (2.6) / 7 (2.8) / 9 (3.9) |
| First sentence (words) | 18 | 18 | 18 | 9 | 19 / 20 / 24 |

**Still slightly number-heavy.** Cutting "about an eighth of the company" would give 10 numbers (4.0 per 100 words), level with YC.

## Fact notes (unchanged from v1 unless stated)
- "Years later" replaces "a few years later". Alibaba was 1999 or 2000; Nvidia was 2017.
- "That bet made him rich again": the Alibaba IPO made him Japan's richest man in 2014 (B, Fortune 2014).
- "Last year, he bought back in": one source only (C). Cut it if no second source turns up.
- Every on-screen number still needs a check at its source before locking.
