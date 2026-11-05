---
name: goal-alignment-review
description: Review Claude's own work on a content job against the job's end goal before anyone sees it, and say what to keep, change or drop so the next actions serve the goal better. Reads the job's DADDY.md (north star, verdicts, facts) and checklist, red-teams every idea or script as a skeptical viewer, the platform and the client, checks that the process itself is still pointed at the goal, and logs the result. Use it before showing ideas, scripts, plans or research to the user or a client; at the end of each phase; when the user says "review your work", "double-check", "is this aligned", "will this go viral", "what should change"; or whenever a lot of work has happened since the last check.
---

# Goal-alignment review

A second pass that asks one question of everything produced: **does this move the end goal, and is it the best way to?**
It reviews outputs (ideas, scripts, pages) and the process (what we are spending time on). It never approves its own
work by default: you are biased toward what you just made, so argue against it first.

## Inputs (read them, don't recall them)
1. `DADDY.md`: section 1 (end goal and business goal), section 4 (verdicts), section 6 (facts), section 9 (decisions).
2. `08-script-checklist.md` and, for scripts, the output of `python3 tools/script_check.py`.
3. The work under review, plus the evidence it claims to rest on (reference breakdowns, demand scan).

## Steps
1. **Restate the goal** in one line from DADDY.md section 1, both halves: the reach goal (going viral) and the business
   goal (the right buyers, trust, leads). Work that serves only one half is flagged.
2. **List what is under review** and what each piece is for (post type, cluster, purpose).
3. **Score each piece 0-2** on the rubric below and write one line of reason per score.
4. **Red-team it three ways**, one paragraph each:
   - *The scrolling viewer* (a US store owner, 2 seconds, sound off): do the title band and first words stop me? Do I
     learn something I didn't know? Would I send it to someone?
   - *The platform*: is it original (one added fact), does frame 0 carry the hook, does anything read as engagement
     bait or an ad, does the length fit the payoff?
   - *The client and the buyer*: can he say every line honestly? Does it make a $100k+/month merchant trust him more,
     or does it attract freebie-seekers? Does anything fight his agency pivot?
5. **Check the process**: is the next planned step the shortest path to a posted, measurable video? Name any loop
   (more research where a test post would teach more, polishing before the hook is proven, waiting on inputs that a
   placeholder could stand in for).
6. **Verdict per piece:** KEEP, CHANGE (say exactly what), or DROP. Then a ranked list of the 3 changes that would move
   the goal most.
7. **Log** a line per verdict in DADDY.md section 9, and turn any repeated miss into a new checklist rule or a new
   automatic check in `tools/script_check.py`, dated.

## Rubric (0-2 each; ship at 15+ of 20, nothing at 0)
| Dimension | 2 points when |
| --- | --- |
| Reach | The hook and topic sit on the widest rung that still fits the lane; frame 0 would stop a stranger |
| Buyer fit | A big-catalog merchant would care and trust him more after it |
| Evidence | Each choice traces to an outlier, a demand cluster or a VisionKit rule, named |
| Gap | A real surprise, paradox, cost gap or belief flip, not a familiar tip |
| Truth | Every number VERIFIED in DADDY.md section 6; nothing he can't say honestly |
| Checklist | `script_check.py` passes; the manual checklist items are answered |
| Shape | Counted units, a surprise every 10-12 s, one turn, a fitting CTA |
| Voice | Sounds like him (02-voice-profile.md), speakable by the avatar |
| Series | Can become Part 2, a recut or a recurring test |
| Measurable | Post type, keyword and the number to watch (likes per view, saves, comments) are set |

## Rules
- A user verdict beats the rubric. Say which verdict decided it.
- No score without a reason; no "looks good".
- Say plainly what could not be checked (Claude cannot watch or hear the final video; views are not known in advance).
- Keep the review short: a table plus the three changes. Detail goes in the files, not the chat.
