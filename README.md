# Video agent skills

Claude Code skills that make Claude work like a video editor: it studies a reference, writes the script, matches footage to every word, builds the edit in Premiere and After Effects, and checks the result before anyone sees it. Built and refined on real client and story-video jobs.

Two-minute tour: [`FOR-JACK.md`](FOR-JACK.md).

| Pack | For |
|---|---|
| [`attention-compound/`](attention-compound/) | Narrated mini-docs and story reels in the Attention Compound style: idea, locked script, reference study, word-matched B-roll, review loop |
| [`cutroom/`](cutroom/) | Editing craft: Premiere Pro and After Effects by script, motion design, sourcing and rights, social formats, batch pipelines, podcast trailers, meme compilations |

Each pack stands alone, with its own README, skills and installer. Use one or both.

## Install
```bash
./install.sh            # dry run: shows what would be copied to ~/.claude/skills
./install.sh --apply    # install both packs
```
Or install one pack from inside its folder: `cd cutroom && ./install.sh --apply`.
Existing skills with the same name are never overwritten. Start a new Claude Code session afterwards.

## Needs
Claude Code, Python 3 (Pillow, numpy), ffmpeg and ffprobe. yt-dlp for downloads. Premiere Pro and After Effects for the editing tools.

## Limits
A person still directs and approves: Claude cannot watch or hear video, so every cut gets checked by eye and ear. Footage and music rights are not cleared by anything here.
