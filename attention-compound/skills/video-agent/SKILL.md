---
name: video-agent
description: The start point for making a narrated mini-doc or story video from idea to final render. Sets the order of work, the gates where the user decides, the job files to keep, and which skill to use at each stage. Use at the start of any new video job, when asked "make a video about X", when resuming a job, or when unsure which step comes next.
---

# Video agent

Built from 2 jobs: the Elon video (18 versions, under 500 views) and the Anthropic IPO video (v4, no verdict or posted result yet). So this is what we learned, not a proven hit formula.

**The test for every decision: does a first-time viewer understand this and want the next second?** Copying a reference is the method, not the goal.

## The order
| # | Stage | Skill | User gate |
|---|---|---|---|
| 1 | Find the idea and story | `idea-finder` | Pick the topic |
| 2 | Study the references | `reference-study`, `minidoc-reference-style` | See the use, change or drop list |
| 3 | Write the script in locked stages | `story-script-writer`, `goal-alignment-review` | Lock each stage |
| 4 | Confirm the format | This file | Answer the intake |
| 5 | Voice, full read, word timings | `references/sound-and-voice.md` | Pick by ear |
| 6 | Music and sound plan | `references/sound-and-voice.md` | Pick by ear |
| 7 | Footage map, line by line | `word-matched-broll` | Hear the gaps early |
| 8 | Word-anchored storyboard | `word-matched-broll`, `video-taste`, `effect-library` | Approve |
| 9 | Short test beside the reference | `edit-loop-guard` | Approve the look |
| 10 | Full build and render | `word-matched-broll` | Say go |
| 11 | Review notes | `edit-loop-guard`, `broll-scoring` | Timecoded notes |
| 12 | Finish | `references/house-rules.md` | Final approval |
| 13 | Feed back | Update the skills | Log results |

Between gates, keep working without asking. Put open questions in one batch, each with a default.

## Intake, before building
Ask as numbered questions, each with a default: aspect ratio, resolution, frame rate, length, deliverables, where it posts, which asset folder is current, what footage rights the user accepts, and the deadline.

## Job files
- `DADDY.md` at the job root: intent, style law, verdicts, script, facts, every edit and sound, decision log. Template: `minidoc-reference-style/references/DADDY_TEMPLATE.md`.
- **The Daddy gate:** before adding anything, ask if it fits the theme, makes sense, is worth adding, takes away more than it adds, or should change to fit. Log the verdict. The user's call wins.
- `HANDOFF.md`: where things stand and the next step, updated every turn, so work can continue in another chat.
- `SOURCES.txt` for every clip and photo, with licence and credit.
- Keep reusable tools in the job folder, one build script edited forward.

## Before showing any version
Run the checklist in `edit-loop-guard`. State:
- what changed and the numbers against the reference
- real footage share, measured on the cut
- what was not checked (always playback and sound)
- whether the next step needs a render, and about how long

## Rules and detail
- `references/house-rules.md`: how to work with the user.
- `references/sound-and-voice.md`: voice, music, sound and mix.
- `examples/anthropic-ipo/`: a real job's script, story library, B-roll plan and decision file.

## Needs outside this pack
Python with Pillow and numpy, ffmpeg, yt-dlp. For Premiere and After Effects work, HyperFrames and other tools, see the pack's `README.md`.
