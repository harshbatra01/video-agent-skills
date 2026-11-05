# Handoff: Metro Media House study

For a Claude session that did not take part in this work. Start here.

## Goal
Make one new video that could be posted as the next upload on the Instagram page Metro Media House: same kind of idea, script, edit and sound. Work in stages, with the user's approval at each stage.

## Where things are (branch `research/metro-media-house`)
| Path | What |
|---|---|
| `reference-reels/<id>/` | The 4 reels: `reel.mp4`, `reel.transcript.json` (Whisper words, not checked by hand), `reel.info.json` (likes, comments, caption) |
| `research/metro-media-house/STUDY.md` | **Read first.** Numbers, trust, paid vs organic, style law, 20 effects with timecodes, script formula, idea selection, use/change/drop list |
| `research/metro-media-house/SHOT-LOG.md` | What is on screen for each spoken line, all 4 reels |
| `research/metro-media-house/IDEAS.md` | 4 ranked topic ideas plus 1 killed, with sources and fact grades |
| `research/metro-media-house/README.md` | Which tools ran, what was changed, how far to trust each number |
| `research/metro-media-house/numbers.json` | Every number in the main table |
| `research/metro-media-house/raw/<id>/` | Tool outputs: frame scores, cut events, shot sheets, colour, sound levels, 1-per-second time sheets |
| `research/metro-media-house/strips/` | Every-frame strips: first 3 s of each reel, flash events, endings, ad tails |
| `research/metro-media-house/captions/` | Full-resolution frames used to measure captions |
| `research/metro-media-house/sprint/` | A rushed 10-minute parallel sprint. Read `sprint/INDEX.md` for what each file is. Treat it as draft material |

Reel codes: PAL = DclpjyxhKF6 (Palmer Luckey, organic), ACK = DdHKc5GBqT- (Bill Ackman, organic), YC = DfFsUfUx0dZ (YC photo, paid by USVC), EIN = Dee-mp9BJqG (Einstein vs Bohr, posted by USVC itself; a style cousin, not a page sample).

## Known errors and gaps (fix before relying on them)
1. STUDY.md effect 13: the yellow highlighter is built with `skills/effect-library/blocks/screen-photo-push/screen_push.py`, not `hail_mary_highlight_streak`.
2. STUDY.md effect 1: the effects-library README marks `pixel_reveal` as "breaks our taste". Settle it at the 3-second test.
3. IDEAS.md idea 4: only Noyce and Moore co-founded Intel, not all eight.
4. IDEAS.md idea 1: the Son kicker "This time, he borrowed it first" is unchecked.
5. EIN shot labels: 1 to 52 are guesses (`sprint/S1c`), 53 to 97 are empty.
6. The caption tool test (`sprint/R2-tools/test/caption_test.*`) was run over a reel that already has captions, so it shows double text. Re-test on a clean background.
7. `sprint/R2-son-script-redteam-and-v2.md` was never finished.
8. Nothing was heard or watched in motion. The voice, music and sound effects are unchecked.

## Decisions already made by the user
- Organic post (no ad tail), voice picked by ear. Footage: no restrictions (user verdict 6 Nov 2026: any copyrighted or licensed clips may be used, including feature films; no restrictions).
- Work sequentially with approval at each step.

## Where the work stopped
The video job is in `jobs/son-01/` (Masayoshi Son, "he sold Nvidia twice"). Script v3 is locked as text, pending fact and asset checks: `jobs/son-01/script/DRAFT-v3.md`. See `jobs/son-01/HANDOFF.md` and `DADDY.md`.
