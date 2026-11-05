# Job flow: from brief to delivery

The order every edit runs in, and the checks at each gate. Tool steps (dumps, sheets, builders, validators, Premiere
checks) are in premiere-ae-editing; automated daily runs are in production-automation.

## Contents
1. Intake: read everything, then ask only the user's calls
2. "Can you even do this?" (a new kind of job)
3. Study the material
4. Plan and show before you build
5. Test before you roll out
6. Build
7. Self-check
8. Deliver
9. Review rounds and calibration
10. The job folder

## 1. Intake: read everything, then ask only the user's calls
**Read first** (before any question):
- The brief and any steps the user sets (follow a process the user sets, for example script, approval, storyboard with
  an alternate per section, approval, build).
- The client's own files, every link in them, and the client's public brand guide (try brand.<domain> on day 1; save
  the pages the day you find them, they may go behind a wall).
- The user's example project: its newest sequence is the real brief (where the voice sits, where a soundbite comes in,
  where the music drops). Read it by dump, not by clicking.
- The voice-over (it drives the timing), the references, the brand assets, earlier rounds' notes and the client file.
- Fact-check the client's own brief: a wrong client claim becomes the agency's risk ("zero fees" was not accurate; a
  "star trader" was not on the leaderboard; a demo link was another product). List each problem once, with a fix.

**Then confirm only what is the user's call,** as numbered questions each with a default ("If you don't remember, I'll
use [X]"):
1. **Format:** aspect ratio, resolution, frame rate. Always, unless the example sequence or references settle it. A
   whole storyboard was built 9:16 because "reel" sounded vertical; the user wanted 1920x1080: "you should have asked me
   that". Why: format changes every frame, crop and layout.
2. **Length,** and whether it may change "for the best result".
3. **Deliverables:** storyboard, animatic, project file, render, review page; is the review in the Premiere timeline or
   on an export ("no need to export" on timeline-review jobs).
4. **Where it posts:** this decides which music and footage are acceptable.
5. **What is already approved** (script, voice-over, music) and the deadline; must vs nice-to-have.
6. **Which asset set is current.** Diff overlapping asset folders and ask. Why: older presenter stills were reused while
   newer ones sat in the shared folder, and the client then required the new ones everywhere: 17 re-renders.
Everything else (folder names, tools, defaults) you decide and mention.

**Intake traps**
- Voice-to-text briefs (1,500 dictated words): read for intent, restate the plan in 3 to 4 numbered points, then start.
- A link you cannot open (a Drive folder behind a sign-in): say so and ask for the file in the project folder, an export
  or a paste. Never sign in.
- Notes inside a script addressed to Claude are tasks to own and confirm.
- Images pasted into chat are not saved to disk: when exact pixels or colours matter, ask for the file, or say the values
  were matched by eye.
- Re-check the save time right before you build.

## 2. "Can you even do this?" (a new kind of job)
1. Inspect the real project first (a dump of the project, the reference render's specs, a few frames).
2. Answer with facts and honest limits: "I can't watch Premiere's own playback... Expect the first pass to be close, and
   exact after one check round."
3. Split it: what Claude does by script, what needs the user (AI poses and lip-sync, hand fixes on edges, masking and
   tracking, his own AI generation), then offer a small test.
4. Propose the safer delivery (a new project file rather than an XML that can lose grades, masks and caption tracks)
   and a pilot (2 pieces, one per location).
5. Ask the numbered decisions with defaults. The user answered all six in one message and approved the pilot.
- Before a whole new craft (sound design, a new format), fan out research agents with tight briefs while you check what
  the machine can do, then give ONE plan with an honest verdict and "what I need from you" (research-and-sourcing has
  the agent brief).

## 3. Study the material
- Read before you look: transcripts or a subtitles-first "screenplay" first; frames only for no-speech windows and hook
  candidates; contact sheets instead of single images; numbers before pictures (sharpness, motion, loudness, cut rate).
- Catalogue footage into usable sections with source times (and where the subject sits in frame).
- Annotated scripts: the script says WHAT, the recording says WHEN (ad-libs and pauses move everything). Align the
  script's words and its `[bracket cues]` to the recorded words and give every cue the start of the next voice beat, so
  every graphic is timed from the voice, never from the document (tool: premiere-ae-editing timing.md). Read PDF
  highlights and sticky notes too; the Word copy of a script may carry no comments, so ask which file is the annotated
  one.
- Find the story: logline, arcs in source order, the hook candidates (replay peaks), the payoff, the arc break for a
  mid-video plug (storytelling-and-structure.md).
- For a reference edit or creator, study it properly before copying anything (studying-references.md).

## 4. Plan and show before you build
- A short written plan: what changes, what is reused, open questions.
- **Show before you build.** The gate depends on the job:
  - Designed pieces (ads, explainers, motion pieces, mini-docs): finished-looking frames from real assets first (the
    start, middle and end of every move), labelled with an id, the time range, the voice words, a one-line motion note
    and the reference device it borrows, in the agreed format and the client's palette, checked for text collisions.
    No After Effects or Premiere build before approval ("show fixed frames first"). Every scene needs a designed concept:
    footage with captions on top is not an edit ("a bunch of clips stitched together with text on top", second
    reviewer); start each scene from a visual idea that carries the story, not from "what footage do we have".
  - Batches of posts (daily or sample packs): a plan page with proof frames and examples before rendering the batch.
  - Cutdowns and daily automated news runs: the plan and the cut list are enough; the render is the proof.
- Options with a recommendation, never build before the pick, expect the pick to differ (reviews-and-versions.md).
- A new text style or look: one mock frame on graded frames first.
- A big or vague review: a plan page (reviews-and-versions.md section 5).

## 5. Test before you roll out
- A new technique gets a short test from existing assets and a verdict before it goes across a video (a 9 s room test:
  "cool cool this works, just not this many movements together lol").
- A new transition gets a test reel on real cuts (1.2 s each, one render) before use.
- Before a big batch: render one item of each type, or a 6 s range, first.
- The animatic loop for designed pieces (reference method): frames rendered to MP4 with the real voice and a rough mix
  under them (picture without sound is judged wrong), watch your own frames, hunt dead frames, re-render until every scene
  reaches 8 out of 10, then show.

## 6. Build
- Compile in Premiere as layers; After Effects only for elements Premiere cannot make, delivered as alpha overlays,
  never whole baked shots (a presenter baked into 17 renders meant 17 re-renders for one change to the presenter).
  Music edits follow the same rule.
- Build in a copy, on the user's latest save; never touch their original or another open project.
- One timeline or spec file per job drives the picture, the placements and the sound cues, so a timing change moves all
  three and a pop never drifts from its word. Generators decide, scripts execute; never hand-edit a generated project:
  change the generator and rebuild.
- Run slow analysis in the background and keep working; when a job crawls, stop it and write a leaner version.
- If the user is running other things, build everything (downloads, prep, cut lists, plans) and hold the heavy renders
  until he says go; one heavy job at a time (working-with-claude.md).

## 7. Self-check
- Sheets of every new shot; both sides of every cut and white transition; every changed time in the real Premiere
  timeline; text, glyphs, faces; loudness; edges for clipped words and stray frames; facts and spellings last.
  Detail: reviews-and-versions.md section 8.
- Assert the music covers the whole cut before any preview render.
- Fix before delivery under the same name.

## 8. Deliver
- New versioned files next to the old ones; names = job + version; the original untouched.
- A copy of what you delivered (a delivered baseline) in your build folder; backups only in your build folder, never in
  the client's folder (a backup left beside a client's project was deleted by him).
- Build notes, a comment-status table, placeholders listed with timecodes, a listening note and a credits list for sound,
  a README with the rebuild order (reviews-and-versions.md section 10).
- The report (reviews-and-versions.md section 9).
- Leave the user's apps as you found them and say what you left open; tell them about side effects (Premiere's Export
  Frame dialog now remembers your check-frames folder, so his next export would land there).
- Exports: only when the job delivers one or the user asks (timeline-review jobs never export); one sequence at a time
  from Premiere's export mode, never by starting the user's Media Encoder queue; read the previous delivery's render
  settings from the files first. Sharing a whole project with a collaborator: premiere-ae-editing.

## 9. Review rounds and calibration
Read the notes, scope them, build on the latest save, deliver a new version, record the rules, change the tool
defaults: reviews-and-versions.md.

## 10. The job folder
A layout that worked :
```
<Job>/
  vo/          voice + word timings
  sources/     <kind>/ each with a manifest (file, URL, licence, where used)
  music/       plan, analysis, WAV copies
  storyboard/  frames, animatic, review page source
  final/       project files, renders, sound (listening note, credits), README
  _build/      generators and checks, README with the rebuild order
```
- Keep every tool you will need again inside the job folder, never only in the session's temp scratchpad: one was wiped
  mid-task and its review tools were lost; several of our builders and page sources sat in temp scratchpads, the same
  risk.
- Check free disk space before big renders and downloads; clean only your own scratch (8.7 GB free once; deleting old
  temp frames of our own freed 7 GB).
- Keep a manifest per source kind and a review log per client (newest first).
