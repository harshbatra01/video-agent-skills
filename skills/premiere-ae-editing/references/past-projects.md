# Past jobs: what they taught (reuse before rebuilding)

Lessons from the kinds of job this skill was built on (Sept to Oct 2026), without names or paths. Per-client facts
(folders, versions, the client's rules) live in the kit's client files or in Claude's memory on that machine: read the
matching one when a job continues an earlier one.

## Keep a shared-resources list per machine
Write down once, per machine, where these live and check they still exist before relying on one:
- A Premiere template project with graphics that already have keyed audio Level, text and shapes (CTA cards were the
  best structural templates on one job; prproj-format.md section 9).
- Adobe's own mogrts (paths per machine: prproj-format.md section 9).
- One or two real finished projects to copy structures from, opened read-only (a music-page project was the template
  for track layouts and graphics).
- The SFX kit: one baked kit of 48 kHz 24-bit WAVs (pops, glass, ticks, counters, booms, swishes; audio.md section 6)
  plus the user's own licensed library.
- The licensed music folders, with the licence noted next to them (Epidemic's Creator plan does not cover client work).

## What each kind of job needed (to plan the next one)
- Vertical paid-social ads on log footage: the log override on every clip of that camera, grades on adjustment layers
  per location cut around B-roll, zoom pieces, B-roll by measured framing, titles by text, After Effects overlays as
  ProRes 4444 on top tracks, tracked masks, a sound pass from a baked kit, CTA end segments. Every version was built on
  the user's latest save, never on the previous build, and renders went into versioned folders so an earlier delivery
  stayed valid.
- 16:9 explainers with an AI presenter: about one generator per minute of video, a first assembly by FCP7 XML, previews
  as After Effects renders with audio, client rounds by relinking new renders into the user's own edit. Lesson: compile
  in Premiere and keep the presenter as Premiere layers (a wardrobe change cost 17 re-renders). A shared folder with
  numbered parts (script, voice, screenshots, a build folder with assets, audio, ae, renders, premiere) kept a
  two-person job findable.
- Cutdowns of long raw footage: transcripts plus subtitle reading, anchored cut lists, edge checks before rendering,
  ffmpeg renders with one fixed recipe, and an XML for the user to finish (timing.md; production-automation).
- Music edits: measure the reference frame by frame, cut on the strongest hit, review every frame around every cut
  (transitions.md, timing.md music section, after-effects.md section 12).
- Faceless and news posts: built by code (HTML + ffmpeg) with Premiere layers as the editable escape hatch
  (prproj-recipes R15; production-automation).
- Green-screen essays with a presenter over plates: keep the job's own tools in the job's folder with its own notes
  file, touch that job only in sessions about it, grade per plate from measurements (grading.md section 8).

## Planning numbers (so estimates are honest)
- A 10:38 explainer rough cut (91 shots, 533 SFX, voice, temp bed): about 4.5 hours from the intake of the shared
  folder, about 7 hours on day one with the sample study, research and a short rig test. A review round of 45 comments
  plus 9 new 3D renders, everything re-rendered: about 2 h 20 min. Later client rounds: 30-60 min of work plus renders.
- Cutdowns: at the start one round took most of a day; with the pipeline, 2 long cuts took about 40 min and 15 files
  about 2 h 25 min unattended, one heavy job at a time.
- Three music edits took about 1.5 hours once the kit existed; a daily batch of 4 news posts about 8-10 min of Claude's
  time (about 35 min on a heavy fact-checking day).
- Render costs: after-effects.md section 10, media-toolkit.md section 10.

## How the tools were tested (repeat this after changing them)
The libraries were consolidated from job code and tested on real files before being documented: (1) a delivered
project rebuilt from the user's file came out identical; (2) every prproj_lib operation on a Premiere-saved project,
with `import_mp4` matching Premiere's own fields; (3) After Effects end to end (an opaque card shot and a keyed alpha
shot, a highlighter on OCR'd words, soft glows, time remap); (4) operations on a copy of a real project, opened in
Premiere. Test (4) found what the others could not: clips on a new track did not draw, because clones kept HeadTransition
refs and duplicate Node IDs. When prproj_lib, the AE runner or a builder changes, re-run the same four kinds of test.

## Memory
Per-project facts and the user's decisions live in Claude's memory folder for the working directory (and in the client
dossiers when the kit includes them). When something general is learned on a job, add it to the matching reference here
as a method plus its reason, not as a story about that job.
