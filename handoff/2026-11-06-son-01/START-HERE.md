# START HERE: full context from the previous cloud session (6 Nov 2026)

You are continuing a job another Claude session started. Read this file fully, then the files it points to. Don't redo finished work.

## 1. The goal
Make ONE new video that could be posted as the next upload on the Instagram page **Metro Media House** (metromedia.house): same kind of idea, story, script, editing, effects and sound, so nobody could tell it wasn't theirs. It's our own work: our own build and type, and no copying of their logo or exact frames.

## 2. Where everything is (repo `harshbatra01/video-agent-skills`, branch `research/metro-media-house`)
All work is on the branch `research/metro-media-house`, not on `main`. Check it out first.

| Path | What |
|---|---|
| `reference-reels/<id>/` | The 4 reference reels: `reel.mp4`, `reel.transcript.json` (Whisper words, not checked by hand), `reel.info.json` |
| `research/metro-media-house/STUDY.md` | The full study: numbers, trust, paid vs organic, style law, 20 effects with timecodes, script formula, idea selection, use/change/drop list |
| `research/metro-media-house/SHOT-LOG.md` | What is on screen for each spoken line |
| `research/metro-media-house/HANDOFF.md` | Study handoff, with the known errors list |
| `research/metro-media-house/sprint/INDEX.md` | A rushed 10-minute parallel sprint (draft quality): rule book, look study, page study, web research, build plan, red team, draft skill, plus 2 tool prototypes |
| `research/metro-media-house/sprint/R2-tools/` | `grid_reveal.py` (opener effect, tested) and `caption_words.py` (per-word captions, tested on the wrong plate; re-test on a clean background) |
| **`jobs/son-01/`** | **The video job.** Start with `HANDOFF.md`, then `DADDY.md` (verdicts and decision log) |
| `jobs/son-01/research/STORY-LIBRARY.md` | 25 dated scenes about Masayoshi Son, graded facts, soundbite leads, photo options, angles |
| **`jobs/son-01/script/DRAFT-v3.md`** | **The current script.** Text approved by the user, pending fact and asset checks |
| `jobs/son-01/script/AUDIT-v1.md` | Every repo script check, run against the script |
| `jobs/son-01/SOURCES.txt` | Sources and clip leads |
| `skills/` | The repo's skill pack. The ones this job uses are in section 6 |

Reel codes: PAL = DclpjyxhKF6 (Palmer Luckey, organic), ACK = DdHKc5GBqT- (Bill Ackman, organic), YC = DfFsUfUx0dZ (YC photo, paid by USVC), EIN = Dee-mp9BJqG (Einstein, posted by USVC itself; a style cousin, not a page sample).

## 3. What the page does (short version; the detail is in STUDY.md)
- **Format:** landscape 16:9 at 1920x1080, 24 or 25 fps, 78 to 95 s, about 175 words a minute, loud music bed only 1 to 4 dB under the voice.
- **Opening:** one famous photo, revealed through a 3x3 grid of white blocks in the first second, with the line "This is / This might be the most...".
- **Pace:** median shot 0.54 to 0.80 s, 7 to 9 shots in the first 5 s, cuts on word starts (not on the beat).
- **Captions:** small white word-by-word captions in a clean sans (closest match Inter Medium), about 3.6% of frame height, centred at 50% height, words spread across the frame; black text on white frames; 8 to 15 big bold key words per reel.
- **Metro-only devices:**
  - a single colour-inverted frame as a cut, about every 3 to 5 s;
  - the name held back until 8 to 17 s;
  - a "basically [movie hero]" comparison shown with film clips;
  - the M logo sting at the end (we don't copy it).
- **Script:** superlative photo hook, comparison, name with a paradox ("the same thing that made him..."), dated events with printable numbers, a real soundbite, a turn, a zoom-out to now with "you", and a mirrored two-line kicker. No lesson.

## 4. Current state of the video job (son-01)
- **Topic:** Masayoshi Son. **Angle:** "he sold Nvidia twice". In 2019 he sold early ("the fish that got away was big"). In Oct 2025 he sold every share to fund OpenAI ("I was crying to sell Nvidia shares"). He now has $64.6B in OpenAI.
- **Script v3** (`jobs/son-01/script/DRAFT-v3.md`): 251 words, about 81 s plus 2 short clips of Son. It's level with Metro on length, sentence rhythm and opening length.
  - **Hook:** H1, "This might be the most expensive photo in AI, because the man next to Jensen Huang sold Nvidia. Twice." This applies if a real photo of Son beside Jensen Huang exists.
  - **Fallback hook (the user's wording):** "This man missed out on 150 billion dollars by selling Nvidia, and then made the exact same mistake again."
  - **Comparison:** "He's basically James Bond at the poker table, always going all in." Use real Casino Royale footage of the final all-in hand.
- **Nothing has been built yet.** No voice, music or picture.

## 5. The user's decisions and working style (follow these)
- **Work sequentially, with approval at each step.** Show one step, wait for the go. The next phase is building the reel **a few seconds at a time**, each part approved before the next.
- **Footage:** no restrictions. Any copyrighted or licensed clip may be used, including feature films, on this and future jobs. Still log every clip in `SOURCES.txt`.
- **Format:** organic post (no ad tail), landscape 1920x1080, 25 fps, 80 to 85 s.
- **Voice:** picked by the user by ear from 3 options.
- **Writing style for every reply and file:** plain English, short points, exact numbers, no em dashes. Make reports readable in the chat, not only as file links.
- **Honesty:**
  - Never fabricate facts, numbers, quotes or measurements.
  - Separate what was measured from what was judged.
  - Say what you couldn't check.
  - Claude can't watch video or hear audio.
- **Installs:** install nothing without first telling the user the name, source and size.
- **Git:**
  - Commit and push to `research/metro-media-house`. Never push to `main` without the user's explicit permission.
  - End commit messages with the attribution lines the session asks for.
- **Batching:** batch open questions, each with a default. Don't stall.
- **Choices:** the user likes several options (they asked for multiple hooks) and then picks.

## 6. Skills this job follows (in `skills/`)
- `video-agent`: the order of work and the gates. We are at stage 3 to 5: script done, then sound plan, then storyboard.
- `story-script-writer` (with `scripts/interest_score.py`), `reel-scripts`, `mass-reel-writer` (with `scripts/reel_metrics.py`), `script-lab` (hook rules K1 to K13) and `goal-alignment-review`: the script checks. All have been run; see AUDIT-v1.md.
- `edit-loop-guard`: run it before building, on every note, and before showing any version.
- `word-matched-broll`: footage matched word by word.
- `minidoc-reference-style`: analysis tools, music first, the Daddy file.
- `motion-design`, `effect-library`, `premiere-ae-editing`: the build.
- `reference-study`: the measurement tools.

## 7. Open questions to ask the user first (each has a default)
1. **"The exact same mistake" in the fallback hook:** keep it, soften to "move", or check Nvidia's price since Oct 2025 first? Default: check the price first.
2. **How assets arrive:** the Son and Jensen Huang photo, Son's two clips, the Casino Royale all-in scene, and the source pages to check facts. Either allow hosts in the cloud environment settings (YouTube, CNBC, Bloomberg), or the user sends links and files. Default: ask the user.
3. **Voice:** 3 options to pick by ear. Music first, per video-agent and edit-loop-guard.
4. **First build part:** the hook (0 to about 6 s): photo, 3x3 grid reveal, captions. Default: start there once the photo is in.

## 8. Known problems and limits
- **Facts are grade B.** The previous environment couldn't open full web pages, so every on-screen number must be checked at its source before the script locks. "Last year he bought back into Nvidia" has only one source.
- **Blocked in the previous environment:** Instagram, Reddit (even in search), Hugging Face, YouTube downloads, and WebFetch on most news sites. WebSearch worked. A new environment may differ: test first.
- **No OCR installed.** Read on-screen text from full-resolution crops, not contact sheets.
- **Known errors in the study** are listed in `research/metro-media-house/HANDOFF.md` (for example, the effect 13 tool and the Traitorous Eight overstatement).
- **Draft quality:** the sprint files are drafts; trust STUDY.md and the job files first.
- **Fonts:** three repo scripts were patched for Linux fonts (`event_sheets.py`, `frame_strip.py`, `ac_shot_words.py`), with a fallback so they still run on a Mac.
