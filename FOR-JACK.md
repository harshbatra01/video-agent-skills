# For Jack: the 2-minute version

This repo teaches Claude Code to work like a video editor and producer. I pick the reference and make the calls; the agents do the research, scripting, footage matching, building and checking.

## What it does today
- **Reverse-engineers a video style.** Give it a reference reel and it measures the reel: shot lengths, cuts per second, words per minute, where the sound hits, colour, caption size. Then it writes the rules for a new video in that style.
- **Writes the script in locked stages.** Hook, turn and ending, each scored for interest and red-teamed before you see it.
- **Matches footage to every spoken word.** It plans what is on screen for each word, based on 460 measured reference shots, then scores every B-roll shot against the line it sits on.
- **Edits in Premiere and After Effects by script.** It writes project files, builds comps, places captions and sound, measures loudness and makes frame sheets.
- **Turns long episodes into trailers and cold opens.** It transcribes a podcast, picks the moments and writes a word-for-word cut list an editor can assemble in Premiere.
- **Stops wasted rounds.** It keeps a log of every decision and checks for the loops that burned versions on past jobs before each new version is shown.

## Built on real jobs
Two narrated mini-docs in the Attention Compound style: Musk vs Delaware (18 versions) and the Anthropic IPO filing. The Anthropic one's script, story library, shot plan and full decision log are in `attention-compound/examples/anthropic-ipo/`.

## Try it in 5 minutes
```bash
git clone <this repo> && cd video-agent-skills && ./install.sh --apply
```
Open a new Claude Code session and say one of these:
- "Make a 60 second story video about X. Start with the video-agent skill."
- "Study this reel and tell me what makes it work: <link>"
- "Turn this episode into a 60 second cold open: <file>"

## Where things are
| Folder | What |
|---|---|
| `attention-compound/` | Story videos: idea, script, reference study, word-matched B-roll, review loop (13 skills) |
| `cutroom/` | Editing craft: Premiere and After Effects, motion, sourcing and rights, social formats, podcast trailers, batch pipelines (9 skills), plus 4 real client files |

## Honest limits
It isn't fully automatic. Taste and direction still decide, and some renders get sent back and rebuilt. Claude can't watch or hear the result, so a person checks every cut. The tools were tested on macOS. Footage rights aren't cleared by anything here.

Take whatever is useful.
