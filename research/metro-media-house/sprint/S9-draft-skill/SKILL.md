---
name: reference-page-match
description: Make a video that fits as the next upload on a reference page (an Instagram or YouTube account the user names). Study every frame of the page's recent reels, split paid from organic posts, pick an idea the page would pick, write the script in locked stages, lock the sound first, storyboard, render a 3 s pilot, then build and review against the measured page spec. Use when the user says "make the next video for this page", "fit this page", "match this account", "what would this page post next", or shares several reels from one page. Worked example in references/metro-media-house.md. Pair with reference-study, word-matched-broll, minidoc-reference-style and idea-finder.
---

# Reference page match

**Status:** draft, written from one study (Metro Media House, 4 reels, 5 Nov 2026). Not yet used to make a posted video. Treat the method as tested once and the numbers as one page's numbers.

Claude reads frames, transcripts and measurements. It cannot watch motion or hear. Say so in every deliverable.

## Why this exists
`reference-study` measures one video. A page is a habit across many posts: how it picks ideas, when it says the name, how it ends, what changes when a post is paid. One reel misleads. In the Metro study, 1 of the 4 reels was the sponsor's own ad on another account, and the paid reel on the page swapped its ending for a 10 s ad tail. Fitting a page needs every reel read, paid and organic kept apart, and numbers compared only from one tool.

## Order of work (stop at every gate)
| # | Step | Do | Deliver at the gate | Gate |
|---|---|---|---|---|
| 1 | Study every frame | Run the study commands below on every reel. Read short reels frame by frame. Read text from full-resolution crops. | `STUDY.md`: numbers table, trust table, paid vs organic, style law tagged SAME / PAGE / VARIES / ONCE, effect list with timecodes, script formula, use / change / drop list | User confirms the spec |
| 2 | Page and idea selection | Work out what the page picks and why (topic, known name, comparison, network vs person). Run `skills/idea-finder` or, if its radar cannot run, the same steps by hand with web search | `IDEAS.md`: 3 to 5 ideas, each with hook line, comparison, name-drop point, paradox, kicker, sources, paid or organic | User picks one |
| 3 | Script in locked stages | Hook, then beat list, then full draft, then kicker. Lock each before the next. Check against the page formula and word count | Each stage on its own, with the formula slot it fills | User locks each stage |
| 4 | Sound first | Voice (or TTS draft), music bed level, word timings. Picture is cut to these, not the reverse | Audio file, word timings JSON, gap level against the page range | User approves the sound |
| 5 | Storyboard | Word-anchored shot list (see `skills/word-matched-broll/SKILL.md`), effects placed by timecode from the effect list | Shot list with word, time, source, effect, rights note | User approves |
| 6 | 3 s pilot | Render only the opener. Read every frame against the page's opener frames | Pilot file plus a frame strip beside the reference opener | User approves the look |
| 7 | Build | Full edit to the locked sound | Draft render | |
| 8 | Review | Run the same study commands on the build. Put build and page numbers side by side from the same tool | Side-by-side table, every frame read, list of misses | User verdict |

## Study commands (run from the page's research folder)
Every reel gets the same tools and the same thresholds. These are the lines from `research/metro-media-house/tools/run_all.sh`, with `$S` = `skills`, `$v` = the reel, `$t` = its transcript JSON, `$O` = its output folder:
```
python3 -I $S/minidoc-reference-style/scripts/frame_scores.py $v $O/scores.json
python3 -I $S/minidoc-reference-style/scripts/cut_events.py $O/scores.json $v $O/events.json
python3 -I $S/minidoc-reference-style/scripts/event_sheets.py $O/events.json $v $O/evsheet/ev 25
python3 -I $S/minidoc-reference-style/scripts/ref_stats.py $O $v $t > $O/ref_stats.txt
python3 -I $S/minidoc-reference-style/scripts/motion_class.py $v $O/shots_ref.json $O/motion.json
python3 -I $S/word-matched-broll/scripts/ac_shot_words.py $v $t $O/shotwords/sw
python3 -I $S/word-matched-broll/scripts/colour_stats.py <id> $v > $O/colour.json
```
Page-level helpers written in the Metro study (`research/metro-media-house/tools/`):
- `gap_level.py <video> <transcript.json>`: music bed level under the voice in gaps, without the hard-wired paths of `skills/reference-study/scripts/gap_sfx.py`.
- `invert_frames.py <video>`: counts single colour-inverted frames. A lower bound; it misses partial inversions.
- `flash_sheet.py <events.json> <video> <out.jpg>`: one sheet of every non-plain cut event, 2 frames before to 4 after.
- `summary.py`: collects per-reel numbers into `numbers.json`.

Other tools to read frames and timing (check each script's header for arguments before use): `skills/minidoc-reference-style/scripts/frame_strip.py`, `skills/minidoc-reference-style/scripts/sheet.py`, `skills/reference-study/scripts/time_sheet.py`, `skills/reference-study/scripts/beat_map.py`, `skills/word-matched-broll/scripts/scan_sheet.py`.

## Rules learned
1. **Read every frame of a short video.** Contact sheets hide motion and 1-frame devices (the Metro inverted-frame cut is 1 frame).
2. **No OCR here.** Read caption text, sizes and positions from full-resolution crops, not from contact sheets.
3. **Only compare numbers from the same tool.** ffmpeg scene detection and `cut_events.py` gave 73 vs 85 shots on the same reel.
4. **Split paid from organic before averaging.** Check the post caption for a disclosure and check which account posted it.
5. **The page has a story machine, not only a look.** Measure where the name is first said, the comparison slot, the turn point and the ending shape.
6. **Instagram and news sites are blocked from the shell.** Use the files the user provides and the WebSearch tool. Never invent views, likes or dates.
7. **Fix font paths small and say so.** In the Metro study some repo scripts failed on Linux fonts. The fix changed the font path only, with a fallback so they still work on a Mac, and is listed in `research/metro-media-house/README.md`.
8. **Do not copy marks that are the page's own** (logo sting, sponsor cards). Design our own.

## Trust rules
- Every number carries a trust level (High, Medium, Low, Judged) and the reason.
- Say what was not checked: playback, sound, voice identity, music IDs, views, retention.
- Say "judged by eye" for anything read from frames rather than measured.
- Likes and comments are not views. Do not rank reels on them across paid and organic.
- A page formula from a handful of reels is a hypothesis. Say how many reels it rests on.

## Files
- `references/metro-media-house.md`: the worked example, the measured spec of one page.
- Full study: `research/metro-media-house/STUDY.md`, `README.md`, `IDEAS.md`.

<!-- Status: draft done -->
