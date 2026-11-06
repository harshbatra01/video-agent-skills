# Context handoff: dhruvxr-01 (Linear spec film in the @_dhruvxr style)
Written 6 Nov 2026 at the end of the first cloud chat. Read this whole file before doing anything.
Repo: harshbatra01/video-agent-skills. Work branch: `job/dhruvxr`. Never push to main.

## 1. Who the user is and how they want to work (their rules, in force)
- Work sequentially, with the user's approval at each step (said after a rushed sprint). One step at a time, then wait.
- Between approved steps, keep working without asking. Batch open questions, each with a default.
- Plain English, short points, exact numbers, no em dashes.
- Never fabricate facts, numbers, quotes or measurements. Always say what was measured, what was judged by eye, and what was not checked. Claude cannot watch playback or hear audio: say so.
- Show every report in the chat, not only as a file link.
- Install nothing without first giving the name, source and size.
- Commit and push after each step on `job/dhruvxr`. Never push to main.
- Follow `skills/video-agent/SKILL.md` (order of work, job files) and run `skills/edit-loop-guard/SKILL.md` on every note and before showing any version.
- Licensing: the user said "don't worry about licences, I'll handle that later". Still log every source in `build/assets/sources.txt` / `SOURCES.txt`.
- The user is called "the boss" in the asset upload commit; they record anything that needs a login (the Linear app).

## 2. The goal
Make one new video that could pass as the next upload of the X page @_dhruvxr: same kind of idea, script, on-screen copy, effects, pacing, music and sound, but our own work. The user chose: a spec brand film for **Linear**, built in the form of the reference **WHP** (dhruvxr's Whop film).

## 3. What was done, in order
1. **Transcripts** of the 2 reference videos checked against frames (`x-videos/`). WHP: "Ideas. Ownership. Every business. One checkout. This is where the internet gets paid. Whop[.com?]". ATN: a voice sample, message is on-screen text only.
2. **Stage 1 study** (`research/dhruvxr/STUDY.md`): every frame read, text logged to the frame, sound, colour, effects, style law, use/change/drop list. Corrections to it: `jobs/dhruvxr-01/sprint/10_LEAD_CHECKS.md` (8 items, e.g. ATN tempo unmeasured, WHP has 6 white flashes, "dhruv" fade is 40 f hold + 41 f fade).
3. **Gate 1**: user said "defaults are fine".
4. **Sprint** (`jobs/dhruvxr-01/sprint/`, see `INDEX.md`): 12 subagent drafts (shot labels, look, page study, web research, rule book, 3 scripts, build plan, red teams, fact check, skill draft). Rough drafts, NOT approved, not reviewed line by line. A rushed video attempt there failed (pilot/ folder).
5. **Direction** (`jobs/dhruvxr-01/DIRECTION_v1.md`): company Linear (approved), script on WHP's frame grid, creative direction, execution plan. User decisions: Linear yes; **no After Effects** (build in Python here); licences later; sound design after the picture.
6. **Build v0 to v2** (`jobs/dhruvxr-01/build/`): one picture script `build.py`, one sound script `sound.py`. The user uploaded footage, photos and Linear brand files into `build/assets/` (with `sources.txt`, `brand_notes.txt`). Latest: **`build/out/cut_v2.mp4`** (16.5 s, 495 frames, 1280x720, 30 fps, picture + sound). Comparison sheet: `build/out/compare_v2.jpg`.

## 4. Latest numbers (cut v2 against WHP, measured)
| | WHP | Ours v2 |
|---|---|---|
| Mean brightness | 0.138 | 0.136 |
| Near-black pixels | 78.0% | 76.8% |
| Near-grey pixels | 96.7% | 96.8% |
| Cut events (cut_events.py) | 17 | 19 |
| Sound level-curve correlation (0.1 s) | | 0.92 |
| Sound hits on picture changes | 12 of 22 | 11 of 15 |
| Loudness | -14.1 LUFS (with VO) | -13.2 LUFS (no VO), true peak -0.9 dBTP |
Sound sections (WHP vs ours, dB): sub intro -1.0 / -0.1, dip -25.8 / -25.6, bed -17.3 / -17.2, fade -38.5 / -38.2. Details: `build/out/sound_v1_vs_WHP.txt`, WHP anatomy `research/dhruvxr/sound/WHP_anatomy.json`.

## 5. Script and voice-over (from DIRECTION_v1.md)
VO, 14 words on WHP's word times: "Noise." (1.4 s) "Focus." (4.5 s) "Every team. One system." (6.6 s) "This is how great software ships." (9.9 s) "linear.app" (14.3 s).
On screen: "// noise //" and "@ noise //" labels, "Backlog" (2 frames), "// backlog 999+", "@/ priority //", "focus" + "/ˈfōkəs/", "this", "[ 09:41 ]", Linear logo, Linear wordmark.
Open choice: "Every team. One system." (closest to WHP, most copy-like) vs "Every idea. One place." Default: the first.

## 6. Linear brand rules (from build/assets/brand_notes.txt, applied)
- Logo and wordmark are Linear's own files, only scaled, composited AFTER grain and vignette; no glow, grain or distortion on them; not combined with other graphics.
- So: the photo tiles (f287 to f300) form our own ring, not the Linear mark; the wordmark appears with a stepped fade only (no wipe).
- Say "Linear", never "Linear app". Domain: linear.app. Label the post "spec, not affiliated".
- OPEN for the user: the soft background light behind the logo (judged as separate scene light).

## 7. Open items (next steps, in order)
1. User reviews cut v2 and gives timecoded notes (ledger them per edit-loop-guard).
2. **App recording**: `build/assets/ui.mp4` and `ui.png` (dark theme, dummy workspace, issue list, one issue moved to Done). Until then f91 to f129 show a placeholder card. `build.py` reads `ui.png` if present (wire ui.mp4 frames in the same way as the other clips).
3. **Voice-over**: no TTS here, ElevenLabs was blocked. Options: the user records it, gives an ElevenLabs key, or approves an offline TTS install (name, source, size first). Then place on WHP's word times and re-level to -14 LUFS, -1 dBTP.
4. Fisheye slot (11.2 s) is a weak match (rock climber + our barrel warp). A better clip would help.
5. Sound is synthesized by our own code (numpy). Matches WHP's levels, pitches (A minor to F major 7) and hit timing. Needs the user's ears.
6. Not acted on yet, from the sprint red team (user to rule): body text 2.2 to 4.6% of frame height may be too small on phones; a 4:5 Instagram version; white-flash count.
7. After approval: 1920x1080 master (`build.py --scale 1.5`), final checks (size, fps, loudness, spelling, rights), then update skills with what the job taught (video-agent step 13).

## 8. How to run
- Needs: Python 3 with numpy and Pillow, ffmpeg/ffprobe, the Inter font. `build.py` reads Inter from `/usr/share/fonts/opentype/inter/` (variable `FD` at the top). On a Mac change `FD` to where Inter is installed (for example `~/Library/Fonts/`), and the DejaVu mono path (`MONO`).
- Picture: `cd jobs/dhruvxr-01/build && python3 build.py out/picture_v3.mp4` (about 70 s at 1280x720). `--only 91-129` renders a range. `--scale 1.5` gives 1920x1080.
- Sound: `python3 sound.py out/sound_v2.wav` (about 2 s). It levels itself against `research/dhruvxr/raw/WHP/envelope_100ms.json`.
- Mux: `ffmpeg -i out/picture_v3.mp4 -i out/sound_v2.wav -c:v copy -c:a aac -b:a 256k -shortest out/cut_v3.mp4`.
- Measure against WHP: `skills/word-matched-broll/scripts/colour_stats.py`, `skills/minidoc-reference-style/scripts/frame_scores.py` + `cut_events.py`, `research/dhruvxr/tools/envelope.py`, `sync_test.py`, `crop_strip.py`, `text_box.py`.
- The cloud environment's network blocked linear.app, YouTube and stock sites; PyPI and GitHub worked.

## 9. File map
| Path | What |
|---|---|
| `x-videos/` | The 2 reference videos + transcripts (WHP = _dhruvxr_2116246221421780992, ATN = _dhruvxr_2109649042661908480) |
| `research/dhruvxr/STUDY.md` | The measured study (style law, effects, timeline, use/change/drop) |
| `research/dhruvxr/raw/`, `strips/`, `text/`, `frames/`, `sound/`, `tools/` | Measurements and evidence |
| `jobs/dhruvxr-01/DIRECTION_v1.md` | Company, script, creative direction, plan, decision log |
| `jobs/dhruvxr-01/HANDOFF.md` | Running status notes |
| `jobs/dhruvxr-01/build/` | `build.py`, `sound.py`, `assets/`, `out/` (latest `cut_v2.mp4`) |
| `jobs/dhruvxr-01/sprint/` | Unapproved sprint drafts and `10_LEAD_CHECKS.md` corrections |
| `jobs/dhruvxr-01/DADDY.md`, `SOURCES.txt` | Job files (DADDY is still thin: fill it as decisions are locked) |
