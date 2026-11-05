# Attention Compound style

Claude Code skills for faceless narrated mini-docs and story reels in the Attention Compound style: a number in the hook, one idea per beat, real footage matched to each spoken word, a callback ending.

## Install
```bash
./install.sh --apply
```
Then, in a new Claude Code session: "Make a video about X. Start with the video-agent skill."

## Skills
| Skill | What it does |
|---|---|
| `video-agent` | Start here. Order of work, user gates, job files, house rules, sound and voice |
| `idea-finder` | News radar, Big score against Story score, kill checks |
| `story-script-writer` | Script in locked stages, interest score, plain language, the story formula |
| `goal-alignment-review` | Red-teams ideas and scripts before anyone sees them |
| `reference-study` | Measures a reference reel and sets opening limits |
| `minidoc-reference-style` | Rebuilds a reference's style frame by frame |
| `word-matched-broll` | What to show on each word, from 460 measured reference shots |
| `broll-scoring` | Scores B-roll shot by shot against the words |
| `video-taste` | Taste for shots, colour, captions and sound |
| `effect-library` | Effect verdicts and 6 small Python effect blocks |
| `edit-loop-guard` | 13 loops that waste versions, and the rule that stops each |
| `script-lab` | Talking-head reel scripts: discovery, hooks, review |
| `mass-reel-writer` | Talking-head reel formula from 11 measured reels |

`examples/anthropic-ipo/` is one real job: script versions, story library, B-roll plan and decision file (`DADDY.md`).

## Needs
Python 3 with Pillow and numpy, ffmpeg, ffprobe, yt-dlp. `idea-finder`'s radar also needs Horizon and last30days (see its `scripts/README.md`). HyperFrames, GSAP skills and `sound` are third-party: install them from their own repos. Some skills point to the companion `cutroom/` skills for Premiere and After Effects work.

## Limits
Built from two real jobs, not a proven hit formula. Tools were tested on macOS only. Claude cannot watch or hear the result.
