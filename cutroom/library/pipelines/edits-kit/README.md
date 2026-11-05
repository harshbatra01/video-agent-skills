# Edits kit (free, built in-house, 13 Oct 2026)

Make cracked sports music edits by script: measure the song, pick a structure, find the shots, reframe to 9:16,
cut the player out, then build ONE layered After Effects comp (every clip, hit, word and motif stays a live layer)
and render it. Nothing here is paid: Premiere/After Effects we already have, plus free models on the GPU.

**The single After Effects comp build is the old route.** Since 15 Oct 2026 the house rule is assembly in Premiere (every
clip, word, hit and transition a layer), with After Effects only making the effect elements. Steps 1 to 8 and 10 still
apply; step 9 below is the old build, kept for reference (skills: motion-design `cracked-edits.md`, production-automation
`music-edit-builds.md`).

## Pipeline (run in this order)
| Step | Tool | What it gives |
|---|---|---|
| 1. Song | `ytdl.py` (skill) for the audio, `beats.py` (skill) for kicks/snares/tempo/loudness, `hear.py` (skill) for word times, `tools/yt.py heat URL` for the most-replayed seconds | where the drop, the hook and every strong hit are |
| 2. Structure | `STRUCTURES.md` | which story shape fits (progress motif, quote-first, single reveal...) |
| 3. Footage | `tools/catalog.py build/tag/idscore/strips/sheet/search` | every shot split, scored (motion, sharpness), tagged by CLIP (scale, action, kit), `idscore` = how clearly HE is in it (re-ID), `strips` = 8 frames per shot with source seconds to pick ranges |
| 4. Cut times | `tools/cuts.py` | `on(t)` = strongest kick/snare near a planned cut, floored to a frame; `report` = sync check before rendering |
| 5. Matte + framing | `tools/automatte.py` (uses `roto.py`) | SAM 2 matte of the subject on EVERY clip (prompt from the re-ID person, or a box at the clearest moment, tracked both ways) and the 9:16 framing from it (head + shoulders centre, smoothed); auto zoom on wide shots |
| 6. Overlays | `tools/overlays.py` | our own light leaks, light-bar sweeps, film burns, flare streaks in any palette |
| 7. Plan | a `plan_*.py` per edit (latest: `pilot/plan_v4.py`) | the edit as JSON: band (letterbox), clips, ramps, hits, zoom cuts, words (hero / caption, behind him or in the bars), pop-outs, looks, end fade |
| 7b. Type | `tools/typeset.py` + `automatte.comp_point` | real font widths for layout; where his head lands on screen, to put a number right behind him |
| 8. Preview | `tools/planview.py plan.json out.png` | every clip's crop (band or 9:16) at start / middle / end with its matte and real-size type boxes: framing QA with no render |
| 9. Build (old route: the house rule is now assembly in Premiere) | `tools/build_edit.py plan.json [--range A-B] [--final]` + `ae_run.py` (skill) | layered .aep + rendered preview; every event snapped to its exact frame; --range renders one moment |
| 10. Check | `tools/anatomy.py render.mp4` + `tools/qasheet.py` (`--crop` for small details) | cuts, flashes, sync to kicks/snares, frame sheets |
Transitions: `tools/ae/edits_lib.jsx` "transitions v2" (shutter, invert / negative flicker, gradient colour flash, true RGB
split, glitch, spin, posterize) via the plan's `transitions` list; `pilot/plan_ttest.py` renders a test reel of them on
real cuts. `tools/ae/probe/effects_list.txt` = every effect this After Effects has (dumped from app.effects).
`tools/reframe.py` (person detector + CLIP re-ID tracker) still gives the re-ID person for the matte prompt and works alone
when no matte is wanted. `tools/cutcheck.py plan.json` finds hidden cuts inside chosen source ranges.

## Making a new edit (wave 1, 14 Oct)
1. `python tools/setup_edit.py edits/NN_name SUBJECT --song YT_ID --footage YT_ID,YT_ID` (run without -I): song wav,
   kicks / snares, word timings, footage download, catalog + CLIP tags + subject scores + contact sheets.
2. Read the song (heatmap: `tools/yt.py heat`, words, loudness), pick a base from `STRUCTURES.md` / `RESEARCH_V2.md`,
   pick shots with `catalog.py strips` and frame sheets, check hidden cuts with `cutcheck.cuts_in`.
3. Write `edits/NN_name/plan_NN.py` with `tools/plankit.py` (Edit: add / hit / tr / number / title / lyric_line /
   strike_name / caption / keep_above / side_x / save). Clips from pillarboxed or letterboxed sources get their real
   picture area detected automatically ("active") and are framed inside it.
4. `tools/planview.py plan_vN.json out.png` (framing, no render), then `build_edit.py` + `ae_run.py`, then frame sheets.

## Research tools
- `tools/anatomy.py VIDEO OUT --name N`: shots, cuts, flashes, breaths, drop, recurring motifs, sync vs chance, strip image.
- `tools/study.py REFS OUT [--words]`: anatomy (+ Whisper) for a folder of reference edits.

## Needs
Python 3.13 with PyAV, numpy, Pillow (system) and, in the user site-packages, torch 2.11 (CUDA 12.8), torchvision,
SAM 2 (`models/sam2.1_hiera_large.pt`), open_clip (ViT-L-14), faster-whisper, yt-dlp. Run GPU tools WITHOUT `python -I`.
After Effects needs Preferences > Scripting & Expressions > "Allow Scripts to Write Files and Access Network" ticked.

## Folders
`refs/` downloaded reference edits (study only) · `anatomy/` their measurements · `pilot/` the first edit (song, footage,
catalog, mattes, plan, ae, renders) · `assets/overlays/` our overlay pack · `models/` SAM 2 weights · `cache/` reframe paths.
