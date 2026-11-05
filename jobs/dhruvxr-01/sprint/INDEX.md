# Sprint INDEX: dhruvxr-01 (5 Nov 2026, 13:16 to 13:27 IST)
Every file in this folder and its one-line finding. Gate 1 defaults applied (BRIEF.md). Nothing was posted, sent, installed or fully rendered.
Base study: `research/dhruvxr/STUDY.md`. Corrections to it: `10_LEAD_CHECKS.md`.

| File | One-line finding |
|---|---|
| `BRIEF.md` | Shared brief and the Gate 1 defaults every agent worked from (ATN-style spec piece, "[STUDIO]" mark, no real logos, ffmpeg plus PIL, -9 to -10 LUFS). |
| `01_SHOT_LABELS.md` | All 57 shots labelled (WHP 31, ATN 26). No live-shot footage in either: footage reads as stock or archive (WHP 21%, ATN 35% of runtime), designed graphics carry WHP (67%), and subjects are small (marks 1 to 8% of frame). |
| `02_LOOK_COLOUR_TYPE.md` + `sheets/` | Measured: blacks at 0 to 4 levels, 24 of 31 WHP shots have saturation 0.006 or less, every colour seen belongs to a brand. Palette for us: #000000 base, ink about #E6E6E6, no accent. New: the WHP wordmark and globe animate in steps of 3 frames (10 updates a second). Shot sheets and text placement maps in `sheets/`. |
| `03_PAGE_STUDY.md` | x.com is blocked by network policy, so the live page was not read. From post IDs: ATN posted 13 Oct 2026 05:05 UTC, WHP 30 Oct 2026 19:09 UTC, 17.6 days apart. Captions are short, first person and about making the piece. No counts seen, so no top vs weak ranking. |
| `04_WEB_RESEARCH.md` | No studio "owns" this look. It is made by in-house SaaS brand teams, freelance launch-video studios ($600 to $25,000 starting prices, snippets only) and template sellers, mostly in After Effects, Cinema 4D and Figma, plus Jitter, Rotato and Cavalry. No source ranks top films. Source pages were not opened (snippets only, 2 hosts blocked). |
| `05_RULE_BOOK.md` | 73 numbered rules (R1 to R73: 54 USE, 10 CHANGE, 9 DROP) with study numbers, example frames and a one-page render checklist. Flags the study's white-flash count error (6, not 5). |
| `06_SCRIPTS.md` | 3 scripts with frame-level shot plans: 1 "Taste" (ATN manifesto, 450 f, turn card at f153), 2 "[PRODUCT]" (WHP-type brand film with our own voice, 495 f), 3 "Frame one" (ATN manifesto, 465 f). Script 1 follows ATN's frame grid most closely; the red team says that is exactly the problem (see 08). No facts on screen; UNCHECKED items marked. |
| `07_BUILD_PLAN.md` + `proof/` | Buildable here with ffmpeg 6.1.1, numpy, Pillow, headless Chrome and Inter (installed). Gaps: no scipy (synth.py will not run), no Linux person matte, no After Effects, no TTS key. About 5.5 to 6.5 hours to a full cut (estimate). Dot-matrix proof ran in 0.42 s but is darker than the style (mean 0.055). |
| `08_RED_TEAM.md` | Stranger test. Biggest risk: script 1 is a near word-for-word swap of ATN on ATN's exact frames (f2, f30, f122, f153, f180, f216, f246, f310), so it reads as a copy; script 2 is a product ad outside Gate 1 (park it). Other severity-3 risks are a black frame 0 in the feed preview, message text too small on a phone (2.2 to 4.6% is about 4 to 9 pt on a phone, judged), and reading as a copy of ATN. Fixes: hook readable on f0, message lines at 6 to 8% height, at most 1 ATN device and one device of our own, no text in the bottom 15% or the corners, a mute test, a separate 4:5 Instagram layout, WCAG flash limit. Rewrote script 1 lines; scripts 2 and 3 skimmed only. |
| `09_FACT_CHECK.md` | Cross-check of every sprint file against the study: no invented counts and no real logos proposed anywhere. Severity 2 items: the rule book's 2.4 s gap (really 1.83 s), script 1 reusing ATN's frames and sentence frame, the build plan's 1280x720 master against the study's 1920x1080 default, and two different "dhruv" fade curves (use the measured one in 10_LEAD_CHECKS.md). Pass marks for near-black differ between files (at least 60% vs 63 to 78%). |
| `10_LEAD_CHECKS.md` | Lead corrections to STUDY.md: ATN tempo is unmeasured (no tempo fits clearly; the 96 BPM idea is not supported), WHP has 6 white-flash events, WHP decodes 493 frames, "dhruv" holds about 40 frames then fades evenly over about 41 (not 56 + 24), the WHP wordmark steps every 3 frames, ATN's no-text gap is 1.83 s, not 2.4 s, and the post URLs and ID-derived post times in 03 check out. |
| `11_DOT_PROOF_CHECK.md` | Dot size already matches WHP (grid 0.94% of frame width, measured), but the proof form is far too big (81% of width vs WHP's 19%) and the glow falls off too fast. WHP has two dot phases (fine glowing dots, then coarse dots with no glow) and random dropout. Seven numbered parameter changes given for the next proof run. |
| `12_RED_TEAM_SCRIPTS_2_3.md` | Scripts 2 and 3 red-teamed: script 2 reads as an ad for an app that doesn't exist and copies WHP's word-plus-phonetics layout; script 3 copies ATN's sentence shape. Fixed lines given for both. Recommends piloting script 3 first (with fixes): its first second is the thing being wasted, so hook and message are one, and it works on mute. This differs from the scripts agent, which preferred script 1. |
| `skill-draft/dark-launch-reel/SKILL.md` | Draft reusable skill (about 4,070 words): measured style law, opening budget, type spec, 18 ffmpeg/PIL effect recipes, sound and rights rules, checklist, tool usage, what rests on 2 videos only, and 4 conflicts with repo rules for the user to rule on. Not copied into `skills/`. |

## Conflicts for the user (from the sprint)
1. Body text size: the references use 2.2 to 4.6% of frame height; effect-library says 5% for readable text; the red team asks for 6% or more.
2. White flashes: WHP has 6; the repo caps whole-frame hits at 3; the rule book defaults to 0 to 1.
3. Opening density: 8 to 9 shots in the first second breaks the mini-doc opening limits (approved for this job only).
4. 16:9 only, or also a separate 4:5 layout for Instagram (red team).
5. Which script to pilot: the scripts agent prefers script 1 ("Taste"); both red teams say script 1 reads as an ATN copy, and 12 recommends script 3 ("Frame one") with its fixes.
6. Script 3 has two sets of fixed lines: 08 section F and 12 (12 defers to 08 where they differ). Pick one.
7. Master size: 1920x1080 (study default, 05, 06) or 1280x720 (07's build master).

## Folders
- `sheets/`: one frame per shot for each reel, and text placement maps (02).
- `proof/`: dot-matrix proof script, 12 PNG frames and a small mp4 (07), judged in 11.
- `skill-draft/dark-launch-reel/`: the draft skill.

## State at the stop (13:27 IST)
- Stage 1 approved (Gate 1 defaults). Stage 2 (idea pick) not started; the scripts in 06 are early drafts ahead of it, not locked.
- HANDOFF.md was not updated during the sprint (no-overwrite rule). This INDEX is the current handoff.
- Not checked by anyone: playback, sound, any live X page (blocked), source web pages (snippets only), licences for music, stock and fonts, phone readability on a real device.
- Recommended next step: rule on conflicts 1 to 7 above, then run Stage 2 with the red-team fixes folded into the scripts.
