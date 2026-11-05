# Job-specific notes cut from edit-loop-guard

## Anthropic IPO job, as of 4 Nov 2026
Recheck these against `DADDY.md`, since they will go stale.
- **Loop 3 is live:** v5 runs about 1:52 at Adam's pace, against 72 to 87 s references. The user declined five small trims. Settle the target before music.
- **Loop 2 is live:** `vo/v1/` is v4 and Adam is a working pick. Do not time anything to it.
- **Loop 5:** opening limit approved 4 Nov: 1 or 2 ideas, 20 or fewer rough sound hits, no graphics to read. Correction same day: a bare voice alone scores 40 rough hits in 5 s, so count planned cues, not rough hits. Run `tools/guard_check.py` on every storyboard and render.
- **Study finding:** Elon's cut speed matched the references. Its first 5 s had about 5 ideas against Altman's 1. Measure ideas, not only cuts.
- **Loop 4:** no footage map yet, and AI hacking is hard to film. This may be the biggest gap, so raise it early. Real clips are allowed: the user accepted the risk on 4 Nov and will settle rights later. Keep a source list.
- **Loop 13:** no colour plan yet. It belongs in the storyboard.
- **Assets:** the storyboard picks from `ASSET-MAP.md` in the job folder. Section 10 lists the gaps to work on from the start.
- **Loop 6:** if the border look returns, start the ladder at 9% (Elon's final, called weak) and include 12.5% and above.
- **Loop 8:** landscape reopens the 9-box grid. Ask, do not assume.

## Added 4 Nov 2026, from the first Anthropic render
- Tie each graphic to its spoken word, then check it against the word timings. Filling a beat in order put graphics up to 2 s early.
- Before a full render, sheet every shot once and look for stock watermarks, interviewers in place of the subject, other companies' logos and blank frames. Round one found all four.
- A cached segment keyed only on its name hides a changed source. Put the source settings in the key.

## Rule from the v3 rejection (4 Nov 2026)
- Before any picture build, read every reference shot against the words said over it (`minidoc-02-anthropic-ipo/tools/ac_shot_words.py`). The rules it produced are in `research/ac-rules/AC-RULES.md`.
- Cut on spoken words, bursts for ideas, holds for proof. Do not cut evenly on a beat grid.
- Check every shot against its words on a labelled sheet (`tools/pic_sheets.py`) before the full finish. That check caught readable text from a different test, wrong chyrons and hosts in frame.

