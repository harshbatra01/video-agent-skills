---
name: mass-reel-writer
description: Write, judge and fix talking-head reel scripts built for mass reach, the way a professional scriptwriter would, using a formula reverse-engineered from a founder profile's 11 reels with views (the "Rani" reels: 2.6M place list, 853k "cheap shoes" flip, the 6.6k flop) and measured against them. Covers the ten laws (reveal not homework, widest rung, one big gap, things people can picture, counted shape, one number per unit, friend voice, low-effort ask, promise kept, something to keep), six topic-free formats with templates, unit grammar, hook patterns, a 10-point scorecard calibrated on the reels, a metrics script, and ten line-editing passes. Use when writing a reel or short-form script, choosing a format, judging whether a script will go viral, comparing scripts, or fixing one that feels like a lecture, too technical, too niche or too long.
---

# Mass reel writer

A professional scriptwriter's method for founder and expert reels that need to reach everyone. Built 21 Oct 2026 from
Rani's 11 reels (word for word, with views), Cutroom's reel research and the Callaway scripting method, and tested
against our own review rounds.

## How sources rank
1. The user's and the client's verdicts.
2. Rani's measured reels (`references/rani-breakdown.md`).
3. Cutroom's measured pages (skills `reel-scripts`, `social-video-formats`).
4. Practitioner advice (skill `script-lab`, the Callaway transcripts).

## The workflow
1. **Brief.** Who's it for (the rung), what the viewer gets, the one emotion, reach or lead post.
2. **Pick the format** (`references/formula.md` section 2). Default to the place list (Format 1) or the "you" flip
   (Format 2); advice and blueprints (Format 6) only for lead posts.
3. **Gather facts.** 5-10 true facts, each checked at the source today, ranked by how few people know them. Keep the
   ones you can say with a named thing and one number.
4. **Write the hook:** the gap in one breath, with the rival or the famous name. Then the units, in the unit grammar.
   Biggest gap last.
5. **Line-edit** with the ten passes (`references/line-edit.md`).
6. **Measure:** `python3 -I scripts/reel_metrics.py --md <file>` and compare with the targets in
   `references/scorecard.md`.
7. **Score** the 10 dimensions with reasons. Fix every 0, then every 1 you can.
8. **Red-team** it as the scrolling viewer, the platform and the client. Say plainly what you can't check: you can't
   watch or hear the final video, and views can't be known in advance.
9. **Deliver** the script, its score, the weak spots, and what must happen before posting.

## Never
- Homework scripts dressed up as reach posts.
- A hook that promises more than the body proves.
- Chained maths or stacked numbers.
- Jargon in the voice.
- Fake numbers, quotes, screenshots or "I tried it" lines.
- Two spoken CTAs.

## Files
| File | What it holds |
| --- | --- |
| `references/rani-breakdown.md` | Every reel in one table, the measurements, the correlations, what's new, the calibration |
| `references/formula.md` | The ten laws, six formats, unit grammar, hook patterns, language, endings, series, truth rules |
| `references/scorecard.md` | The 10-dimension scorecard, red flags, measured targets |
| `references/line-edit.md` | Ten editing passes |
| `references/reels.json` | The 11 scripts word for word with views, ages and lengths |
| `scripts/reel_metrics.py` | Measures any script (Hindi, Hinglish or English) and correlates a set with views |
