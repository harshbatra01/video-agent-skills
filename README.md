# Video agent skills

Claude Code skills for making narrated mini-docs and story videos: finding the idea, writing the script, studying references, choosing B-roll, cutting and reviewing. Built from 2 real jobs in Oct and Nov 2026.

**How proven is this?** The rules come from 4 reference reels, our own measurements and the user's notes. The Elon video got under 500 views. The Anthropic v4 has no verdict or posted result yet. Treat the rules as tested working practice, not a guaranteed formula.

## Install
```bash
git clone <this repo>
cd video-agent-skills
./install.sh
./install.sh --apply
```
Then start a new Claude Code session and say: "Make a video about X. Start with the video-agent skill."

## The skills
| Skill | What it does |
|---|---|
| `video-agent` | Start here. The order of work, gates, job files, house rules, sound and voice |
| `idea-finder` | News radar, Big score against Story score, kill checks |
| `story-script-writer` | Locked script stages, interest score, simple language, AC formula |
| `reference-study` | Measures from the references, how far to trust them, opening limits |
| `word-matched-broll` | What to show on each word, from 460 reference shots |
| `edit-loop-guard` | 13 loops that wasted versions, and the rule that stops each |
| `video-taste` | Working taste for shots, colour, captions and sound |
| `effect-library` | Effect verdicts and 6 small Python blocks |
| `broll-scoring` | Scores B-roll shot by shot against the words |
| `goal-alignment-review` | Red-teams ideas and scripts before anyone sees them |
| `minidoc-reference-style` | Rebuilds a reference's style frame by frame, with effects and scripts |
| `script-lab` | Talking-head reel scripts: discovery, hooks, review |
| `mass-reel-writer` | Talking-head reel formula from 11 measured reels |

## Vision kit (version 2026.10.15), by Kanishk
These 10 skills and the `kit/` folder come from Kanishk's Vision kit. `kit/` holds client files, research, pipelines and tools. It is a snapshot, so copy newer kit updates by hand. Client details are in here, so never make this repo public or share it without checking with Kanishk.

| Skill | What it does |
|---|---|
| `editing-playbook` | How to plan, cut, tell the story and handle notes |
| `premiere-ae-editing` | Runs Premiere and After Effects by script |
| `motion-design` | Motion rules and the After Effects effect library |
| `reel-scripts` | Story reel scripts and AI voice blocks |
| `research-and-sourcing` | Fact checks, sourcing and news research |
| `production-automation` | Batch and daily production pipelines |
| `social-video-formats` | Format rules for social posts |
| `podcast-trailers` | Podcast intros, trailers and cold opens |
| `meme-compilation-edit` | Narrated meme compilations in Premiere |
| `kit-updater` | Applies kit zips. Expects the `~/VisionKit` layout, so set that up first on a new account |

To use the kit's client files and tools on a new account, copy the folder: `mkdir -p ~/VisionKit && cp -R kit ~/VisionKit/kit`. `kit/START-HERE.md` has the rest of the setup.

## Examples
- `examples/anthropic-ipo/`: script, story library, decision log, B-roll plan, and the v4 build code.
- `examples/elon-job/PROMPT-MAP.md`: every prompt on the Elon job, and what each was about.

Example code has paths hard-wired to the original Mac. Read it as a pattern. It will not run as is.

## What you need
- Claude Code.
- Python 3 with Pillow and numpy, ffmpeg and ffprobe, for most tools.
- yt-dlp for the context scan and source downloads.
- `idea-finder`'s radar also needs Horizon and last30days, per its README. Its paths need editing.

## Left out on purpose
| Left out | Why | What it affects |
|---|---|---|
| Full reference scripts and transcripts | Other creators' text | `mass-reel-writer/scripts/reel_metrics.py` needs a `reels.json` you make yourself. Only measures and short phrases are here |
| Videos, audio, photos, frame sheets | Size and rights | Bring your own references |
| Chat logs and handoff history | Long and personal. Rules were taken out of them | Nothing needed for new videos |
| Personal coach notes, keys, logins | Private | Set keys as environment variables |
| HyperFrames, GSAP, `sound`, Eden | Third-party. Install from their own sources | `github.com/heygen-com/hyperframes`, `github.com/greensock/gsap-skills`, `github.com/vibe-motion/sound` |

## Keep this repo private
The kit holds client files. Decision logs name real footage sources, private page links and unreleased plans. Footage rights are not cleared by anything here.

## Limits
- Claude cannot watch playback or hear. Check every result by eye and ear.
- Tools were tested on macOS only. The effect blocks and radar were only syntax-checked in this pack.
- A few reference notes still mention original job folders such as `minidoc-01` or `~/VisionKit`. Read those as history.
