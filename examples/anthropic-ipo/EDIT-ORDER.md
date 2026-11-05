# Edit order for the Anthropic IPO video (proposal, 4 Nov 2026)

Status: waiting on the user's OK. No render happens before step 11.

Updated 4 Nov: format is landscape, like the Altman video. The opening must be easy to grasp, because the Elon video's busy first seconds were the user's main reason it did not work. Step 1 starts from that. Step 5 and every graphic use landscape. Step 6 has a working read in `vo/v1/`.

## A. Learn before making
1. **Elon lessons.** Written as the skill `edit-loop-guard` (4 Nov): 13 loops, the note routine and the pre-show checklist. Applies from here to the end. Scriptable checks done: `tools/guard_check.py` (G1 to G10), tested on Elon v18. `daddy.py` stays hard-wired to the Elon job's files, so it needs pointing at this job at build time.
2. **Directory of what we have.** Done 4 Nov: `ASSET-MAP.md`, every animation, effect, transition, music track and sound effect by source, with status and rights, plus the gaps to work on. Add the Attention Compound findings after step 4.
3. **Repo scan.** Done 4 Nov, `ASSET-MAP.md` section 8 and `mine/library/EFFECT-LIBRARY.md`. Open-source repos not yet explored. Name, source, size, licence and what each adds. Nothing installed without OK. It comes here because it changes what the storyboard can promise.
4. **Reference study.** Done 4 Nov: `REFERENCE-STUDY.md`. Measure the Attention Compound reels the way the Altman video was measured: pace, moving footage share, captions, music, colour (`tools/colour_stats.py`). Files are in `research/ac-refs/`. Altman's colour, pacing and vibe come first (user, 4 Nov).
5. **Taste session (user). Page built 4 Nov, then replaced by the storyboard at the user's request.** Reel `taste/taste_reel_v1.mp4`, beats `taste/beats.json`. Side-by-side frames and options sheets. Mark each Elon effect keep, change or drop, and note what you like in the references. Output: taste notes and style law v2, "how this differs from Elon".

## B. Sound
6. **Voice (user). Full v5 read made 4 Nov:** `vo/v2/`, 1:52, transcript matches. Timings valid for this take only. Pick by ear. Full read of `script/STORY-SCRIPT_v5.txt` (locked 4 Nov, replaces v4), transcript check on every number, word timings, pace target. This locks the length. The read in `vo/v1/` is v4, so use it to judge the voice only, not for timings.
7. **Music (user). The user will send their own track (4 Nov). Claude's candidates are out.** Retime the storyboard to its beats on arrival. 3 to 5 candidates tried against the real voice. Settle rights, including embedded or Instagram in-app music. Build the beat map.

## C. Picture on paper
8. **Footage map.** For each line, what real footage exists, source and rights. Target: about 67% moving footage, Altman's share. Gaps get flagged here, not during the edit.
9. **Storyboard (user).** Line, time, visual, colour, effect, sound, the asset each one comes from in `ASSET-MAP.md` with status and rights, reason, and how it differs from Elon. One frame sheet beside Altman's for the colour verdict. Every element through the Daddy gate. Predicted B-roll score against the reference. Check against the first-prompt notes and the kit.
10. **Review and proof.** Skeptical viewer review, then the first 3 s pilot beside the reference, then a 10 s test. Any look gets an options sheet on real frames first. User signs off.

## D. Build
11. **Full build.** Sheets and low-cost checks first. Log everything in `DADDY.md`. Render only after the checklist passes. One batched render per round of notes.
12. **Review rounds (user).** Timecoded notes. Before each render, check that no earlier verdict was undone.
13. **Finish.** Loudness, facts, licences, credits, recheck the IPO date line, caption and cover. Final approval is the user's.
14. **Feed back.** Notes go into skills, the effects catalog and taste notes. Log results once posted.
