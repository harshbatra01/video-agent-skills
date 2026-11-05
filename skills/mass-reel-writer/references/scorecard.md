# The scorecard

Score every script 0-2 on each line, with a one-line reason. Calibrated on Rani's 11 reels (rank correlation 0.79
with views; scored in hindsight). Ship at 15+ of 20 with no zero on dimensions 1, 6 or 7.

| # | Dimension | 2 points | 1 point | 0 points | Rani r |
| --- | --- | --- | --- | --- | --- |
| 1 | Reveal, not homework | Tells a fact about the world; at most one instruction, at the end | Half reveal, half steps | A to-do list or lecture | +0.76 |
| 2 | Breadth | Anyone can care | Would-be sellers or founders | Existing founders or a niche | +0.66 |
| 3 | Gap | One big, simple gap in the first breath | A gap, but small or late | No gap | +0.54 |
| 4 | Known anchors | Names or objects everyone can picture, one per unit | Some names | Abstract ("your business") | +0.52 |
| 5 | Counted shape | First, second, and last; biggest gap last | Some order | No shape | +0.70 |
| 6 | Low-effort ask | Know it, save it, send it | A small action | Weeks of work or maths | +0.81 |
| 7 | Promise kept | Band, hook, body and caption match exactly | A small stretch | The body doesn't prove the hook | +0.47 |
| 8 | Emotion and identity | Pride, guilt, outrage, delight, "us vs them" | Mild interest | None | +0.52 |
| 9 | Number discipline | One simple number per unit, 3-6 per 100 words | Too few or slightly heavy | Chained maths, 7+ per 100 words | +0.51 |
| 10 | Kept or quoted | A list worth saving or a line worth quoting | Some value | Nothing to keep | +0.84 |

## Red flags (each one has sunk a Rani reel)
- The hook promises a number the body never reaches (C).
- Six numbers in one breath (C).
- "You can do X" followed by months of steps (J, D).
- A great engine on a subject nobody thinks about (E).
- A plain claim with no gap (B).
- Stacked "you should / aap kar sakte ho" lines (C, J, G).

## Measured checks (run `scripts/reel_metrics.py`)
| Metric | Target | Why |
| --- | --- | --- |
| Instructions per 100 words | 0-2 (one CTA allowed) | Homework loses (r -0.25 to -0.39; the top 3 reels have none) |
| "You should / you can / you need" lines | 0-2 | The lecture penalty (formal "aap" r -0.70) |
| Numbers per 100 words | 3-6 | Spreadsheet flops at 7.6 and 9.9 |
| Named anchors | 4+ | Things people can picture |
| Ordinals | 3+ in a list format | Counted shape |
| "But" words | 0-1 | Winners never argue |
| Words | 100-170 (English) | Length isn't the lever; pace is |
