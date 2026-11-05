# Cutroom

Claude Code skills for professional video editing: plan and cut edits, drive Premiere Pro and After Effects by script, design motion, source and clear footage, and run batch production.

## Install
```bash
./install.sh --apply
```
Optional: add the house rules in `CLAUDE.md` to your `~/.claude/CLAUDE.md`. Then start a new Claude Code session and try: "Plan this edit with the editing-playbook skill."

## Skills
| Skill | What it does |
|---|---|
| `editing-playbook` | Start here. How to plan, cut, tell the story, judge B-roll, sound and grade, and handle review notes |
| `premiere-ae-editing` | Edits Premiere projects and builds After Effects comps by script; frames, loudness, transcripts, OCR, downloads |
| `motion-design` | Motion rules, transitions, type, 2.5D, and an After Effects effects library with 18 recipes |
| `research-and-sourcing` | Fact checks, news research, footage, music and SFX sourcing, licences and rights |
| `social-video-formats` | What performs on each platform: hooks, the first three seconds, CTAs, posting windows |
| `reel-scripts` | Story reel and founder reel scripts, AI voice blocks |
| `production-automation` | Spec-driven batch pipelines, render pipelines, QA gates, scheduled runs |
| `podcast-trailers` | Podcast intros, trailers and cold opens from long recordings |
| `meme-compilation-edit` | Narrated meme and tweet compilations in Premiere |

## Client files
`clients/` holds four real projects (paid-social ads, daily news pages, faceless automated posts, sports music edits), each with status, taste rules, review history and workflow, so Claude can pick any job up cold.

## Library
- `library/pipelines/edits-kit/`: script-first beat-synced sports music edits (song map, footage catalog, mattes, plan, build).
- `library/pipelines/youtube-research/`: YouTube search, storyboard and crop sheets without downloading.
- `library/research/edits-bank/`: 273 top music edits studied frame by frame, with a 73-technique effects catalogue.

## Needs
Python 3 with Pillow and numpy, ffmpeg, ffprobe, yt-dlp. Premiere Pro and After Effects 2025 or 2026 for the editing tools. `premiere-ae-editing/scripts/env_check.py` lists anything missing. Works on macOS and Windows.

## Limits
Claude cannot watch or hear video: check every result by eye and ear. Footage and music rights are not cleared by anything here.
