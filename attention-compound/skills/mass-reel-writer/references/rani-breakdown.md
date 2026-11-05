# The Rani breakdown: 11 reels, measured and read line by line

Reference: an Indian D2C founder's personal brand (artificial jewellery), studio talking head with a podcast mic,
Hinglish, run by an agency. 11 reels with views, given by the user on 19 Oct 2026. Median 36k. The scripts word for
word: `reels.json` (also in the job folder at `research/reference-rani/scripts-verbatim.md`).

**Limits:** 11 reels is a small sample. Views also depend on things a script can't show (cover, edit, posting time,
the account's momentum, whether a reel was a collab). Ages run from 1 to 14 days, so young reels may still grow. K is
a recut of I posted to an audience that had partly seen it. Read every number below as a signal.

---

## 1. Each reel in one table

| Reel | Views | Hook (gist) | Hook type | Shape | Subject | What it asks you to do | Emotion | Ending |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **H** 4 cities | 2.6M | In these Indian cities you'll get China-like products cheaper than China | Secret reveal + rival | List of 4 places, "aur last" | Places and prices | Nothing: just know them | Pride, greed for a deal | Comment LIST |
| **F** cheap shoes | 853k (2 days) | Buying Rs 500 shoes, you think you saved thousands | Contrarian, "you" call-out | You vs your friend, escalation (phone, laptop, labour), moral | A habit everyone has | Buy the right thing next time | Guilt, amusement, argument | Follow |
| **I** Gujarat markets | 314k | In these Gujarat markets you get products cheaper than China, and I found out while sourcing for my brand | Secret reveal + personal line | List of 5 markets, resale path | Places and products | Nothing: just know them | Pride, opportunity | Comment Gujarat |
| **A** brand test | 94k | Do you know Mamaearth, Lenskart and boAt run a simple test before launch? | Secret reveal about famous brands | Suppose (jewellery), test steps, warning | Brands, then your business | Run Rs 4-5k of ads | Insider aspiration | Comment test |
| **K** Gujarat recut | 84k | Same as I, no personal line, 4 markets | Secret reveal | List of 4 | Places | Nothing | Pride | Comment Gujarat |
| **B** repeat clients | 36k | The biggest achievement in business is a repeat client | Plain claim | Claim, my 40%, warning, questions | Your business | Find out why customers don't return | Mild worry | None |
| **J** Rs 50K jewellery brand | 34k | You can start a jewellery brand with just Rs 50,000 | Low-capital promise | Budget split, test, scale | Your future business | Months of work | Aspiration | Comment Yes |
| **G** management | 24k (1 day) | I've seen many founders complain their employees don't deliver | Observation + flip ("the problem is you") | 3 lessons | Your team | Change how you manage | Mild ego sting | None |
| **D** test an idea | 21k | We all have business ideas but can't test them | Common belief + contrarian | Steps: domain, AI site, ads, data | Your idea | 2 weeks, Rs 2,000-2,500 | Hope | None |
| **E** isabgol | 20k | This Indian product is cheaper than Chinese but makes 10x profit | Rival + money | Facts, injustice line, product ideas | One niche product | Build a wellness brand | Outrage, pride | Comment yes |
| **C** WhatsApp | 6.6k | Just Rs 10,000 of WhatsApp makes Rs 8-10 lakh a month | Big money promise | A six-step maths chain | Your marketing | Run campaigns, do the maths | Greed, then doubt | Comment guide |

## 2. The measurements (`scripts/reel_metrics.py`)

| Reel | Views | Words | Words/s | Numbers per 100 words | Named anchors | Ordinals | "But" words | Formal "aap" | Informal "tum" | Instructions per 100 words |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| H | 2.6M | 191 | 3.4 | 5.8 | 9 | 4 | 0 | 1 | 0 | 0 |
| F | 853k | 115 | 2.9 | 3.5 | 0 (everyday objects) | 0 | 0 | 0 | 8 | 3.5 |
| I | 314k | 154 | 3.4 | 0 | 13 | 3 | 0 | 5 | 0 | 0 |
| A | 94k | 166 | 4.2 | 1.2 | 4 | 1 | 0 | 3 | 2 | 5.4 |
| K | 84k | 116 | 3.3 | 0 | 11 | 3 | 0 | 3 | 0 | 0 |
| B | 36k | 97 | 3.2 | 1.0 | 0 | 1 | 0 | 4 | 0 | 3.1 |
| J | 34k | 197 | 3.5 | 7.6 | 3 | 0 | 1 | 8 | 0 | 0.5 |
| G | 24k | 215 | 3.6 | 1.4 | 0 | 3 | 3 | 7 | 2 | 3.7 |
| D | 21k | 167 | 3.7 | 3.6 | 3 | 3 | 2 | 6 | 0 | 4.2 |
| E | 20k | 147 | 3.3 | 2.7 | 7 | 0 | 5 | 3 | 2 | 4.1 |
| C | 6.6k | 152 | 3.4 | 9.9 | 1 | 0 | 0 | 11 | 0 | 2.6 |

**Rank correlation with views (Spearman, n=11):**

| Signal | r | Reading |
| --- | --- | --- |
| Formal "aap" count | -0.70 | The more she addresses and instructs the viewer, the fewer the views |
| "But / lekin" words | -0.62 | The winners never say "but"; the turn is in the facts, not in an argument |
| Ordinals (first, second, last) | +0.41 | A counted shape helps |
| Average sentence length | +0.40 | Winners flow in long spoken chains ("...aur...aur..."), one picture per clause |
| Hook contains a number | -0.40 | In this profile the number isn't what wins the hook; the gap and the rival are |
| Instructions per 100 words | -0.25 to -0.39 (depends on how instructions are counted) | Homework loses; the top 3 have none |
| Numbers (count) | -0.35 | Past about 6 per 100 words it reads like a spreadsheet (J 7.6, C 9.9) |
| Named anchors | +0.29 | Places and brands people know help |
| Length in words | -0.08 | Length (97-215 words) doesn't decide anything |

## 3. What the data adds to what we already knew

1. **Reveal beats homework.** H, I and K give zero instructions: they tell you something about the world (places,
   prices). The lowest reels lecture ("do this, then this"). This is the strongest new finding.
2. **Talk like a friend, not a teacher.** F uses informal "tum" all the way through, like a friend teasing you. The
   low reels pile up formal "aap... kar sakte ho" instructions. In English this is tone: "you think you saved money"
   (a friend) vs "you should set up" (a teacher).
3. **The subject is something you can picture:** a city, a market, a shoe, a brand. Not "your business".
4. **Ask almost nothing.** Winners ask you to know, save or buy smarter. Losers ask for weeks of work (D, J) or maths
   (C).
5. **One simple number per unit, no more.** H has a price per city; C and J chain budgets and percentages and lose.
6. **No "but" needed.** The turn sits in the payoff itself (Rs 50 T-shirt sold for Rs 1,000-2,000). Arguing ("but
   actually...") reads as a lecture.
7. **The number isn't the hook here; the gap is.** "Cheaper than China" beats "Just Rs 10,000".
8. **Long spoken chains, short ideas.** Winners average 17-19 words a sentence, but every clause carries one image.
9. **Fast delivery.** About 3.4 words a second in Hinglish. In English, aim for about 2.7-3.
10. **The CTA doesn't decide reach.** "Comment X" appears on both winners and losers; it decides leads.
11. **The series engine.** H (2.6M) was followed within days by I (Gujarat) and K (recut): the same formula, a new
    place. About one post a day across the 11.
12. **A strong engine on a niche subject still loses.** E has the best outrage engine (25x markup, "our crop, their
    brand"), but on isabgol, a product most viewers never think about.

## 4. Calibration of the scorecard

The 10-dimension scorecard in `scorecard.md`, scored on these 11 reels (in hindsight, so biased toward fitting):

| Reel | Views | Score /20 |
| --- | --- | --- |
| H | 2.6M | 20 |
| F | 853k | 18 |
| I | 314k | 17 |
| K | 84k | 17 (recut to an audience that had seen I) |
| A | 94k | 13 |
| E | 20k | 13 (niche subject) |
| D | 21k | 8 |
| G | 24k | 7 (1 day old) |
| B | 36k | 5 |
| J | 34k | 4 |
| C | 6.6k | 1 |

Rank correlation of the total with views: **0.79**. Strongest single dimensions: "a list worth saving or a line
worth quoting" (0.84), "low-effort ask" (0.81), "reveal, not homework" (0.76), "counted shape" (0.70).
