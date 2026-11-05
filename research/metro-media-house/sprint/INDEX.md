# Sprint index (5 Nov 2026, 13:17 to 13:28 IST)

10 agents started at about 13:19 IST, plus 1 late start at 13:24 for the unfinished EIN shot labels. Each wrote only its own new files. Nothing was rendered, installed or posted. All work is from frames, transcripts, measurements and web search: no playback, no audio heard.

| File | Status | One-line finding |
|---|---|---|
| `S1a-shot-labels-PAL-ACK.md` | Done (PAL 73/73, ACK 162/162) | Mid-size subjects (20 to 50% of frame height) get the most screen time (PAL 41%, ACK 44%). PAL is mostly built composites (28% of time); ACK is mostly real footage (archive, interview, film: 58%). |
| `S1b-shot-labels-YC-EIN.md` | Stopped at deadline (YC 123/123, EIN 0/97) | YC is mostly archive footage (52 of 123 shots), held together by the group photo, which flashes in colour and then turns desaturated with each new person picked out (shots 1-5, 12, 41-42, 54-55, 82-83). |
| `S1c-shot-labels-EIN.md` | Stopped at deadline (EIN 52/97, not checked against tiles) | EIN shots 1 to 52 (0 to 59.8 s) labelled by splitting SHOT-LOG.md's grouped reading by word timing. The tile sheet was not opened, so shot-level type and size are inferred. Shots 53 to 97 unlabelled. |
| `S2-look-study.md` + `S2-sheets/` + `S2-tools/` | Stopped at deadline (ACK, EIN, YC graphics only skimmed; no grain check) | PAL, ACK and YC share one dark, low-key grade: black point p2 6 to 9, mid p50 66 to 82, white point p98 173 to 211, almost no clipping, saturation about 0.29 to 0.31, slight warm lean. Captions are white, centred at 48 to 51% height, 3 to 4.5% tall. Paper cards are off-white, about #ebe8ec to #f5f2f6. |
| `S3-page-study.md` | Done | The two most-liked reels (PAL 51,224, ACK 41,062) are organic, each about one famous living man with a "basically [movie hero]" hook and a short lowercase caption. The two weakest are USVC-paid, with "most important photo" hooks and long captions. A hypothesis, since 4 reels change together. Nothing found on who runs the page. |
| `S4-web-research.md` | Done | Nothing found on who runs Metro Media House or who makes the USVC reels. The technique sources are real (Card Wipe grid reveal, Invert effect, paper cut-out tutorials). All comment-to-DM numbers are vendor claims. 31 URLs, weak ones marked. |
| `S5-rule-book.md` | Done | Most of the style is shared by all 4 reels and can be checked with numbers. Only three things are Metro-only: the inverted-frame cut, the name held back to 8 to 17 s, and the comparison line, which must now be shown without film clips. Ends with a 10-step checklist for a finished cut. Note: `interest_score.py` is at `skills/story-script-writer/scripts/interest_score.py`. |
| `S6-scripts.md` + `S6-tagged/1.txt` | Stopped at deadline (script 1 of 3) | The Masayoshi Son script (242 words, about 83 s) scores inside every reference range: 55% event words, average sentence 12.1, reading ease 72. Its hook is 25 words, though, and the "$60B+" figure and four framing lines are unchecked. Huang and Traitorous Eight have notes only. |
| `S7-build-plan.md` | Done | The biggest gap is a per-word caption placer, needed on every frame. Inter fonts, PIL and ffmpeg are all here, so a new script here is the fastest fix. The second gap is the person matte, which only runs on the Mac. About 17 to 24 working hours across 13 stages. |
| `S8-red-team.md` | Done (scripts not red-teamed: S6 was empty at 13:22) | A stranger would scroll past our draft hooks: 21 to 26 words, against the page's 10 to 11, with no known word on screen while the name is held back. Fixed hooks and kickers are in the file, plus 10 rule changes (hook cap of 14 words, no C-grade facts in the hook or kicker). |
| `S9-draft-skill/SKILL.md` + `references/metro-media-house.md` | Draft done | A reusable "reference-page-match" skill. The 8 steps with user gates, exact study commands and trust rules. The Metro spec is included as the worked example. Not installed in `skills/`. |

## Corrections found for the earlier study (not yet applied; existing files were not edited during the sprint)
1. STUDY.md effect 13: the yellow highlighter is built with `skills/effect-library/blocks/screen-photo-push/screen_push.py`, not `hail_mary_highlight_streak` (S7).
2. STUDY.md effect 1: the effects-library README marks `pixel_reveal` as "breaks our taste". Settle it at the 3-second pilot (S7).
3. IDEAS.md idea 4: "They started Fairchild, then Intel" overstates it. Only Noyce and Moore co-founded Intel (S8).
4. IDEAS.md idea 1: the Son kicker "This time, he borrowed it first" rests on an unchecked claim. Use S8's rewrite or check it first (S8).

## Open after the sprint
- EIN shot labels 53 to 97, and a tile check of 1 to 52 (S1c), Huang and Traitorous Eight scripts, red team of the Son script, grain check, graphic counts for ACK, EIN and YC.
- The hook length rule from S8 (10 to 14 words) conflicts with the S6 Son hook (25 words). Settle it before scripting.

## Round 2 (13:26 to 13:29 IST, 6 agents, 2-minute time box)
| File | Status | One-line finding |
|---|---|---|
| `R2-ein-labels-53-97.md` | Stopped, 0 of 45 labelled | Row skeleton only (times and words for shots 53 to 97); the tiles were not opened in time. |
| `R2-tools/grid_reveal.py` + `R2-grid-reveal.md` + `R2-tools/test/` | Test ran | The opener effect now exists as a script: blurred photo, 9 white #F2F1EF blocks popping into a 3x3 grid in groups of 2 to 3, each fading to sharp over 3 to 4 frames, faint grid lines. Tested at 960x540 on a PIL placeholder (38 frames). The lead checked the contact sheet: the effect is visible. Not yet compared frame by frame with the reference strips; no subject cut-out or background swap. |
| `R2-tools/caption_words.py` + `R2-caption-tool.md` | See the file's own status at commit time | Prototype of the missing per-word caption placer (Inter Medium, centred at 50%, words spread, black on bright frames). |
| `R2-script-huang.md` | Started late, see file | Huang script for idea 3; may be a stub at the stop. |
| `R2-script-traitorous-eight.md` | Started late, see file | Traitorous Eight script for idea 4; may be a stub at the stop. |
| `R2-son-script-redteam-and-v2.md` | Started late, see file | Red team and v2 of the Son script; may be a stub at the stop. |
