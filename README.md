# Video agent skills

Claude Code skills that turn Claude into a video editor and producer. Two independent packs:

| Pack | For |
|---|---|
| [`attention-compound/`](attention-compound/) | Narrated mini-docs and story reels in the Attention Compound style: idea, locked script, reference study, word-matched B-roll, review loop |
| [`visionkit/`](visionkit/) | General editing: Premiere Pro and After Effects by script, motion design, sourcing and rights, social formats, batch pipelines, podcast trailers, meme compilations |

Each folder stands alone: its own README, skills and installer. Use one or both.

## Install
```bash
./install.sh            # dry run: shows what would be copied to ~/.claude/skills
./install.sh --apply    # install both packs
```
Or install one pack from inside its folder: `cd visionkit && ./install.sh --apply`.
Existing skills with the same name are never overwritten. Start a new Claude Code session afterwards.

## Needs
Claude Code, Python 3 (Pillow, numpy), ffmpeg and ffprobe. yt-dlp for downloads. Premiere Pro and After Effects for the editing tools.

## Limits
Claude cannot watch or hear video: check every result by eye and ear. Footage and music rights are not cleared by anything here.
