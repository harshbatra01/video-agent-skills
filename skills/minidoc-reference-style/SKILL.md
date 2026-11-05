---
name: minidoc-reference-style
description: Reverse-engineer a reference edit (a viral faceless mini-doc, reel or story video) and rebuild its exact style for a new topic, music first. Frame-by-frame analysis (cuts, flashes, micro-shots, video vs stills, caption style, frame-edge look, sound design), a beat-grid music plan, word-matched B-roll that is mostly moving footage, and the effect library learned from a Sam Altman mini-doc (pixel-block opener, polaroid, giant-word whips, 9-grid with cut-out, rule-break soundbite, edge blur and fringe, colour-flipping captions). Use whenever the user shares a reference video and wants "the same style", "a replica", "copy this edit", "break this down", "why does this retain", or a mini-doc built like a reference, even if they only say "make one like this".
---

# Reference-style mini-docs

Learned on job minidoc-01 (Oct 2026, Musk vs Delaware built on a Sam Altman reference). The user is precise about order
and about style. Every rule here came from a correction. Work in this order, show each step, and do not skip ahead.

## The Daddy file (first thing in every job, user's rule 19 Oct 2026)
Create `DADDY.md` from `references/DADDY_TEMPLATE.md` at the start, keep it current, and run every proposed addition
through its gate (`scripts/daddy.py check`, plus the six questions) before building it; `daddy.py audit` before every
render. Details: `references/daddy-file.md`.

## The order (the user's, non-negotiable)
1. **Study the reference frame by frame** before building anything (`references/analysis-method.md`). Report numbers,
   not impressions: cuts per second per section, median shot, micro-shots, share of moving footage vs stills, flash frames,
   black frames, caption style, frame-edge look, where the music drops and where the voice stops.
2. **Music first.** Pick the tempo and design the beat grid, sections and drops on the voice cues. Every cut and
   transition then snaps to the grid (`references/music-first.md`). The user's words: "the main mistake you made was not
   syncing music first".
3. **Pilot the first 2 to 3 seconds** shot for shot, next to the reference, and get a verdict before the rest.
4. **Script review against the kit frameworks** (reel-scripts `story-reel-formula.md`, editing-playbook `hooks.md` and
   `storytelling-and-structure.md`, social-video-formats `content-bar.md`). Log first, change only when asked.
5. **Source moving footage** for the B-roll (`references/sourcing.md`). Stills are the exception.
6. **Build**, measure the build with the same tools as the reference, compare in a table, then show.
7. **Motion-graphics layer (HyperFrames)** on top of the edit: chyrons, location tags, hand-drawn arrows and circles, route
   maps, tickers, rendered transparent and composited (`references/hyperframes-overlays.md`). Show a side-by-side with and without it.

## Style rules that the reference taught (measured on the Altman mini-doc, 86.5 s)
- Pace: 142 shots plus 97 micro-shots (2 to 4 frames) inside montage bursts; median shot 0.38 s; nothing holds over
  about 1 s except deliberate rule breaks. Section rates 1.0 to 2.4 cuts a second; it slows at the soundbite and the last line.
- Footage: about 67% of the runtime is moving footage (interviews, news anchors, archive), 23% stills, 10% flash-length
  frames. Stills are never dead: they flicker, push, or sit inside a collage.
- **No empty frames.** Never a plain coloured card with a little text. Graphics sit over moving, darkened footage.
  Exception, on purpose: one black "breather" card ("For context," at 8 s) that breaks the pattern. Breaking the rule
  once is a skill, not a mistake.
- **Rule-break soundbite**: the voice-over stops and a real news anchor or speaker plays with their own sound, one held
  shot for 2 to 5 s (reference 33 s and 45 s to 51 s). The music drops out under it.
- Captions: 1 to 3 words, built word by word, centred; a high-contrast serif italic (Didot Italic on a Mac) with tight
  heavy sans (Helvetica Neue Bold, tracking about -5) on the key words; white on dark, **black on bright frames**; the
  edge look is applied over the captions too.
- B-roll is literal to the word on screen (jury box on "No jury", padlock on "Locked out"). Image collages on a timer
  were called "meaningless".
- (19 Oct 2026, user review) The subject fills at least 50% of the frame and is never cut by the frame edge (gold bars at
  15% were rejected). No narrow building interiors as filler for courts or judges: show the real place wide, the real person,
  a news chyron of the event, or a 2 to 4 frame symbol burst. A name gets that person, never a stand-in face (a bust, a pundit).
  Score B-roll before review with `scripts/broll_sheets.py` (sheets + metrics), eye labels in a `labels.py`, then
  `scripts/broll_report.py` (shot score = (2 x match + quality + framing) / 2, out of 10).
- (20 Oct 2026, user review) **No instant punch-in zooms on stills.** Never split a still into wide and punch-in crops of
  the same picture: it reads as jumpy and not smooth. To keep the pace, cut to a separate image of the same subject. A subject
  with one photo holds still. Do not slow-push stills either; the motion comes from real footage.
- (20 Oct 2026) **Cutting a voice-over:** whisper word edges can sit 0.2 to 0.5 s off.
  - Put every cut point in measured silence (under about -50 dB), or set it by hand at an energy dip.
  - Then transcribe the whole track AND a short window (about 2.5 s) around each join with two models.
  - Context hides clipped words: "company" lost its end and still read correctly in the full transcript.
- (4 Nov 2026, colour and footage) The user called the Elon build's colour theme and design boring, with mostly photos as B-roll. Plan colour scene by scene and aim for the reference's moving footage share. Elon was as saturated as Altman but darker and nearly all warm. See `edit-loop-guard` loops 4 and 13.
- (4 Nov 2026, posted result) The Elon build of this style did not work when posted. The user's main reason: too many effects and sounds in the first seconds, hard to grasp. Keep the opening easy to grasp; do not copy the reference's density by default.
- Full effect library with frame timings: `references/effects-library.md`.

## Tools (`scripts/`, copy into the job's tools folder)
| Step | Script |
|---|---|
| Frame scores, cut events, verification strips, stats | `frame_scores.py`, `cut_events.py`, `event_sheets.py`, `ref_stats.py` |
| Every frame of a moment as a sheet | `frame_strip.py <video> <t0> <t1> <out.jpg>` |
| Moving footage vs stills per shot | `motion_class.py` (talking heads score about 1 to 2, stills 0 to 0.6: threshold 0.9; our own grain fools it) |
| Music analysis under a voice | `beats.py` (inconclusive under a loud voice; separation needs Demucs, ask first) |
| Word timings, onset fix, pause tightening | `asr_words.py`, `fix_words.py`, `tighten2.py` (cuts silence only; never cut on word timings) |
| Person cut-out with no installs | `osascript -l JavaScript person_mask.js in.jpg mask.png` (Apple Vision; swiftc was broken on this Mac) |
| Synth score and SFX stand-ins | `synth.py` |
| Commons search and download (images, video at 720p) | `commons_search.py`, `commons_pool.py`, `commons_get.py`, `commons_video_get.py` |
| ElevenLabs voice | `tts.py` (key from the environment only; free tier is 128 kbps and not licensed for commercial use) |
| Whole build | `build_template_v8.py` (music plan, edit plan, music, SFX layer, picture, mix; `TEST=1` sheet, `FRAMES=t0,t1` frame sheet, `SNAP=t` one full frame) |

## Sound effects (user verdict, 19 Oct 2026)
- Real, different sounds, only where the story shifts: a section change, a drop, a whip, a photo appearing (camera
  shutter), a literal object (gavel, lock, door slam). Never one sound on every cut, never on a timer, never the same sound
  back to back. The synth hit repeated on every cut was "distracting and makes the video worse than without it".
- Openly licensed SFX: the Openverse API (api.openverse.org, no account, Freesound CC0 and CC BY); align each file's
  measured transient (`sfx_info.json`: onset, peak) to the frame.

## Hard-won warnings
- Measure the build with the reference's own tools and show a table. Our first cut was 4x slower than the reference while
  the median shot of the reference had already been measured.
- Contact sheets of stills hide motion. Check per-shot motion (moving vs still) and look at every frame of key moments.
- Check every video in-point by eye: a 2-second shift landed on a political rally twice. Keep political imagery out
  unless the story is political.
- Watermarks: drop photos with photographer watermarks (they were found on Commons uploads).
- Disk: renders with grain compress badly (500+ MB clean passes). Check free space before a render; a full disk broke a mix.
- Audio offsets: put `adelay` in the mix stage, never in the extraction with `-t` (the delay pushed the soundbite past the
  cut-off and it came out silent).
- Never use the YouTube bot-check workaround. Footage rights: any clip may be used, copyrighted or not, including
  feature films and news (user verdict 6 Nov 2026: any copyrighted or licensed clips may be used, including feature films; no restrictions); keep SOURCES.txt.
