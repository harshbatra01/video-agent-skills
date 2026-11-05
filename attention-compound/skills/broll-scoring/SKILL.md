---
name: broll-scoring
description: Label, score and fix the B-roll of any narrated edit (mini-doc, reel, explainer, ad), shot by shot, and compare it against a reference video. Measures every shot (time, length, words said over it, video or still, sharpness), labels what each shot shows, scores match to the words, quality and framing, totals them weighted by screen time, and writes a fix list with replacement sources. Use it whenever the user asks to review, rate, score, audit, label or compare B-roll, asks "is this B-roll good", "why does my edit feel weaker than the reference", "which shots are weak", "replace the bad B-roll", says shots "add nothing", are "cut off", "too small", "random", "pointless", or wants B-roll chosen for a script, even if the word B-roll is never used.
---

# B-roll scoring (the reviewer's own skill, 19 Oct 2026)

Built from the Musk vs Delaware mini-doc job, where it was used to compare the job against the Sam Altman reference.
- Before: ours scored 7.5 out of 10, the reference 8.3.
- Fix: the swaps listed in the report.
- Example report: `references/example-report.md`.

## The rules the reference follows (apply them when choosing B-roll, not only when scoring)
1. **A name gets that person:** real clips or photos of the named person, on the word.
   - Never a stand-in face: a bust, a pundit or a random man reads as "who is this?".
2. **A number gets a print:** a news chyron that prints the number, or a big number card over darkened moving footage.
3. **An idea gets a symbol burst:** "control", "humanity", "money", "justice" get 2 to 4 frames each of statues, art or objects.
4. **A metaphor gets the literal object.**
   - From the reference: kill switch = a light switch, biggest mistake = fire.
   - From our job: referee = a referee showing a card.
5. **A place gets the real place, wide.** The court is the courthouse exterior. Never a narrow interior (a staircase, an
   arched window, an empty room) as filler.
6. **Proof comes from real news footage.** The reference spends 29% of its time on broadcasts with chyrons. Under 10% means
   the story is unproven on screen.
7. **The subject fills at least 50% of the frame and is never cut by the frame edge.** Rejected by the user: a gold bar
   at 15% of the frame, cut off at the bottom.
8. **Video first.** A still gets a push and flicker. Stills are fine when they are the literal thing (the real judge's photo).
9. **Every shot changes with the caption words.** The reference averages 0.38 s per shot. A wrong picture held for 0.3 s is
   still wrong.

## Scoring (per shot, out of 10)
- **M, match to the words, 0 to 5:**
  - 5 = the named person or the literal thing;
  - 4 = a clear symbol or metaphor;
  - 3 = on topic but generic;
  - 2 = loose;
  - 1 = wrong or misleading (wrong person, wrong company);
  - 0 = a placeholder.
- **Q, quality, 0 to 5:** sharp, clean, well lit, no compression mush, not upscaled.
- **F, framing, 0 to 5:** the subject is big, not cut off, well placed for 9:16, and the shot moves.
- **Shot score = (2 x M + Q + F) / 2.** Match counts double because it is what separates a great B-roll edit from a pretty one.
- **Video score** = the average of the shot scores, weighted by screen time.
- Report alongside:
  - weak shots (score under 5): their count and seconds;
  - time on shots that miss the words (M of 2 or less);
  - picture time with the subject under 20% of the frame;
  - screen time by type: clip, still, news, grid, gfx, card.

Benchmarks from the reference:
- 8.3 out of 10 overall;
- 3% of the time misses the words;
- 3% of picture time has small subjects;
- 29% of the time is news.

Ship a cut only at 8 or above with under 5% misses.

## Workflow
1. **Shot list.**
   - For your own edit: the edit plan (`edit_vX.json`: t0, t1, source).
   - For a reference: cut detection (`minidoc-reference-style` analysis tools: frame_scores, cut_events, ref_stats).
2. **Words.** Get a word-timed transcript of the final audio (`asr_words.py`, faster-whisper small.en). Use the final mix,
   not the script: timings shift.
3. **Sheets and metrics.** Run:
   `python3 -I scripts/broll_sheets.py <video> <shots.json> <words.json> <out_dir> <prefix>`
   It writes:
   - `<prefix>_sheet_NN.jpg`: one middle frame per shot, with number, time, length, video or still, and the words;
   - `<prefix>_metrics.json`.
4. **Label by eye.** Look at every sheet: all of them, no sampling. Write `labels.py` with one line per shot:
   `n|what it shows|type|subject % of frame|Q|F|M|note`.
   - Use shot ranges for repeats.
   - Add the user's own notes as notes ("USER NOTE: ...").
   - Template: `references/labels-template.py`.
5. **Totals.** `python3 -I scripts/broll_report.py <dir>` prints the comparison table and every shot's row (markdown).
   - It expects the prefixes `ref` and `ours` (sheets step), and `REF` and `OURS` in `labels.py`.
   - To score one video alone, label it as both.
6. **Write the report.** In this order:
   1. how it was scored;
   2. the totals table;
   3. what the numbers say (3 to 5 points);
   4. the fix table: our shots, the problem, the replacement and the rule it follows;
   5. what needs the user (licensing);
   6. a projected score, labelled as a projection;
   7. every shot labelled.

   Check every duration you quote against the metrics file before sending.
7. **Feed it back.** Add the user's verdicts as dated rules: the job's DADDY.md verdicts and this skill's rules list.

## Fixing the weak shots (sourcing order)
1. **What the job already has.** Make a portrait contact sheet of the pool first: a centre 9:16 crop of every file. Many
   fixes are already on disk.
2. **Wikimedia Commons** (`scripts/commons_search.py "<query>" 8 bitmap|video`, then `scripts/commons_get.py <dir> <list.tsv>`).
   - Only Public domain, CC0, CC BY or CC BY-SA. Log the author and licence in CREDITS.tsv; the post description needs the
     credit lines.
   - The download tool backs off on HTTP 429. Keep requests few and slow.
   - It found the real Delaware Chancellor's portrait, the courthouse, the Delaware Supreme Court building, Tesla shareholder
     meetings and a referee with a red card.
3. **Search the action, not the noun.**
   - "referee showing red card" beat "football referee", which only returned portraits.
   - Search for the moment the word describes.
4. **Reject:**
   - stand-ins that could be read as the real person;
   - another company's branding (a FIAT stock certificate for a Tesla line);
   - wrong numbers on screen (a certificate for 25 shares on "nine shares");
   - SpaceX pictures on Tesla lines.
5. **Needs the user (never fake these):**
   - broadcast news clips and chyrons;
   - agency photos of private people (the shareholder);
   - paid stock footage.

   List exactly which shots they would replace, and leave the shot as the best open option until then.
6. **Frame each replacement.** For each replacement still, set the crop: a focus point, or an exact source box when the subject
   is off-centre (the referee needed a box to show the raised red card).
   - Snapshot every changed frame before the full render.
   - Re-score the changed shots after the render.

## Limits to state in every report
- Claude scores one middle frame per shot, not playback.
- Subject size is an eye estimate.
- The marks are one reviewer's judgement; the user's and the reviewer's taste outrank them.
