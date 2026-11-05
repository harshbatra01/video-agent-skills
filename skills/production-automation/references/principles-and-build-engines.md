# Principles and build engines

The design rules behind every pipeline in the kit, with the reason and the job that taught each one. SKILL.md has the
short list; this file has the detail. Verdict quotes are the editor's or the boss's own words.

## 1. What automation is for
- **Volume of good posts, not a clever system.** The boss judged posts on "retention, CTR, AVD", "not because the
  system is cool or impressive", and new pages are "time and topic based, need to hit right". The pipeline only builds
  what passes the content bar (social-video-formats: interest test, build at 7/10 or more). Why: weak posts teach the
  platform the page is boring, and a fast engine just makes more of them.
- **Posts are approved or rejected, not hand-finished.** That is why code renders them: a person reviews one contact
  sheet and says yes, no or "change X", instead of opening each post in an app.
- **A news track needs steps a format track does not:** find fast, verify, add a fact, write the caption, pick the
  window. The value is created before the edit. The operator approves a daily slate in one go instead of starting
  each job by hand.
- **The engine is the cheap part.** A prediction-market studio rendered 18 posts in about 4 minutes and every one was
  rejected ("these are all SAME types of posts bro", then "the UI is bad", "I can't watch them"). The fix was the
  content and the look (real moments, the house text style), not the renderer. Spend the effort on the first frames
  and the story, and keep the engine boring.
- **Variety means different kinds of posts, not different skins.** A look kit of six skins (weather, broadcast,
  tabloid, paper, terminal, neon) read as a motion-template pack. Keep one text treatment per page; vary the format,
  the footage and the moment.

## 2. Pick the engine per format
| Format | Engine | Why |
|---|---|---|
| Cards, carousels, Story stills, quote and tweet cards | HTML/CSS template filled with the post JSON, screenshotted by headless Chrome (transparent PNG for overlays) | exact fonts, text that fits by measuring, no clicking, no Adobe seat: 12 test posts in 51 s, a day's 8 posts in about a minute |
| 9:16 headline, tweet and split videos | ffmpeg composites clip + overlay PNG + audio; the same run writes the Premiere layers and XML | one command per post, about 20 s per re-render, editable later |
| Motion graphics driven by data (charts, counters, timelines) | HTML + GSAP timeline rendered frame by frame through Chrome's DevTools protocol, piped into ffmpeg | one design system for stills and video; a 7 s chart video renders in 11 s |
| Animated templates with real motion design (a tier-list board) | After Effects rendered headless (the boss's concept doc proposes Nexrender) | a position, untested; our own AE work crashed on low RAM before an upgrade, so budget 32 GB or more per render machine (tentative) |
| Ads and explainers (talking head, B-roll, graphics, captions) | Premiere: first assembly as FCP7 XML, every later change as .prproj text edits; After Effects only renders alpha elements | the editor can open, check and change anything; a review change is one relink |
| Beat-synced music edits | a plan JSON built into one layered After Effects comp (every clip, word, hit and transition a live layer; the old route: since 15 Oct 2026 Premiere assembles and After Effects only makes the effect elements) | effects Premiere cannot do; one layer edit and one render per change |
| Long cutdowns of long sources | an ffmpeg renderer with the house recipe, plus a Premiere XML of the same timeline | parallel, cached, frame exact, about 6x real time; the editor can finish from the XML |
- Project files only on demand. A Premiere project for every daily post was judged too complex for now.
- When the editor first said "most videos would be done in premiere its simple stuff", the news pipeline became
  code-rendered with Premiere layers as the escape hatch, and nobody objected once they saw it work.

## 3. Code renders, Premiere stays editable
- **Every code-built video ships its layers:** V1 base clip MP4 (the picture without the overlay), V2 overlay PNG with
  alpha, A1 WAV, and `<id>.xml` (FCP7 xmeml v4) that rebuilds the finished cut in Premiere with File > Import.
- **Plus `<id>_source.xml`:** V1 holds the WHOLE source video, scaled exactly like the render, with its in/out on our
  window and its own audio linked on A1, and the headline on V2. In Premiere the editor slips V1 (Slip tool, Y) to any
  other part. Why: the editor asked "how can i access directly in premiere" to move a section, and a 15 s cut layer had
  nothing to slip to.
- **Middle layers go on their own tracks.** A keyed reaction clip becomes `<id>_react.mov` (QuickTime Animation, ARGB,
  about 220 MB for one short post) between the clip and the headline: V1 clip, V2 reaction, V3 headline, A1 audio. Why: an
  editor can swap the clip or move the reaction in seconds.
- **The fast path for a re-cut is still "tell me the timestamp":** a re-render takes about 20 s and keeps the house
  loudness and fade, which the source XML (raw audio) does not.
- **Long cuts: the render and the XML share one audio layout.** The XML checker then also tests the render (it found a
  bed that played under an insert 0.4 ms too early). Markers carry the reason for every removed stretch.
- Status to know: both XML kinds pass `fcpxml.py --check`; the cutdown XMLs were imported by the editor ("The XML
  import worked this time"); the news-post XMLs have not been imported by the team yet (test one before relying on it).

## 4. Compile in Premiere; After Effects makes elements
- The rule (editor, 9 Oct): "we need to be using after effects only for neccesary stuff and do the compiling in premiere".
  A presenter baked into 17 After Effects renders meant 17 re-renders for one change to the presenter.
- In a pipeline: the generator renders each AE graphic as an alpha element (ProRes 4444) plus a meta JSON (start, end,
  geometry); the Premiere builder places it and builds anything that must blur or dim the footage below it (an alpha
  overlay cannot do that). Recurring assets (presenter poses, logos) are single bin items used many times.
- Music edits follow the rule too (decided 15 Oct 2026): Premiere assembles the edit and After Effects only makes the
  effect elements. The earlier build, one live AE comp (a change = one layer edit and one render), is the old route.
- Alternative (from the friend's set): Dynamic Link comps for wholly designed motion pieces. Ours wins; use Dynamic
  Link only when the user asks or will finish in After Effects (premiere-ae-editing has the traps).

## 5. The generator contract (every engine)
- **Python decides, libraries draw.** The generator computes every time, rect, crop, score and path; specs go into the
  template or the .jsx as JSON strings built with `json.dumps` (a stray `%` in %-formatting once stopped AE from
  starting a build).
- **Every run writes:** a log that starts with a START line, a DONE flag file, a meta or geometry JSON for the next
  stage, and (for After Effects) the saved .aep next to the renders, so a person can change any word, timing or colour
  by hand.
- **Self-reporting After Effects builds:** wrap the build in try/catch; on failure save `<name>_ERROR.aep` with the
  error message in a comp name; add comp markers at the SFX beats; build a 1080x1920 preview comp over a real frame
  next to the alpha element; render the element with "High Quality with Alpha" (ProRes 4444) plus an H.264 preview
  ("H.264 - Match Render Settings - 15 Mbps"). Why: nobody watches AE run; the preview and markers make QA and sound
  placement one step.
- **When you compose a new .jsx from pieces of older generators, copy the constants header too** (W, H, FPS, colour
  arrays, fonts, layout y values): two renders failed with "ReferenceError: W is undefined".
- **Placeholders fail fast.** Shipped job scripts use `/CHANGE/ME/...` paths and `CHANGE_ME` names so a copied
  script stops until it points at the new job.
- **Never paste file names into code strings.** A shell script that built `python3 -c "...open('$f')..."` would run code
  from a crafted file name in a downloaded client folder; pass names as arguments. Never `exec()` slices of another
  script's text; import it (with a `__main__` guard).
- **Patch saved projects defensively:** back up first, check the XML is well formed before writing, escape names (an
  `&` or `<` in an unescaped name breaks the file), and build into a copy.
- **Name things the way the user does.** Never put "Claude" in a name a client sees (renders, sequences, delivered
  files, client-visible projects); internal tools and work files may use it.

## 6. Caches
- Key every cache on every input that changes the output. A crop-preview cache keyed without the crop centre, scale
  and y offset showed stale crops. The render part cache keys on a hash of the exact ffmpeg command plus the input's
  size and modification time. The matte cache keys on file + range + prompt.
- Cache the slow analyses once per source: footage catalogs, CLIP embeddings, re-ID galleries, reframe paths,
  mattes, transcripts, beat maps, YouTube heatmaps, emoji and logo files. Setup steps skip what exists.
- A fix then costs little: a cached re-render of one long cut took 49 s against 2:08 for the full 13 minute render.
- Caches get big (render parts about 2.7 GB per long source, 12 GB after a few rounds). Delete only with the user's OK,
  to the Recycle Bin or Trash, after the round is approved.

## 7. Fix the generator, not the output
- A systematic miss becomes a default or a guard in the toolkit: frame snapping of every event, footage audio off by
  default, no mirrored band extension on pop-outs, side placement for narrow glyphs, active picture area inside
  letterbox bars, caption cropping, fitted captions, word order after cut-outs (music edits); censor-mute, camera-
  switch and speech guards (cutdowns); number colouring and accent rules in the template (news posts).
- Review notes in "apply next" mode ("dont fix but keep in mind", "Don't fix the reviews on these"): log the rule,
  change the default, apply from the next item; do not re-render reviewed files. When the user does ask for fixes,
  deliver new versions.
- Keep one rule in one place. Two scripts carried the same mask-feather rule and only one got the new value; port a
  rule change to every script that uses it, or move it into a shared helper.

## 8. Versioning inside pipelines
- **Delivered files are never overwritten.** The builder versions automatically (`_v2`, `_v3`); the captions file
  lists every version on disk and marks the latest; the spec keeps the old settings in a `history` field.
- **Undelivered drafts are fixed in place under the same name.** QC fixes before handover keep the name; after
  handover every change is a new version. Why: QC found real misses every round (one round: 6, all fixed before the
  report).
- **Move drafts aside before a rebuild.** A versioning helper versions anything that exists, so a rebuild of an
  undelivered draft would make a `_v2`; move drafts to `_superseded` (old versions to `_old_versions`), never delete.
- **A just-built project may be replaced only if nobody opened or saved it.** Once Premiere has opened or saved it, the
  next change is a new version.
- **If your own last build did something destructive, rebuild the next version from the save before it** (after
  checking the newer save for hand edits worth carrying over), rather than patching on top.
- **Build into a NEW project file or a copy, never into a project the user has open.**

## 9. Forks per client
- Copy an approved pipeline for a new client: its own brand file (handles, avatar, accents, fonts, CTA line), batches,
  finals and delivery folder. The faceless fork differed from the news builder in one file only (a reaction layer, a
  black background option, its own Drive folder) and the original was never touched.
- A format becomes a new client's format by swapping the brand kit (the boss's concept doc calls this forking a format).
- Keep the client's call-to-action in one config line so it changes in one place the day the client approves wording.

## 10. Human gates and "default is no change"
- Gates we keep: the shortlist and the facts (a person approves the slate); one contact sheet per batch; the review
  page; posting in the app with the client's official sound (API posting may upload as "original sound" that does not
  count for the client's sound page: unverified, so posting stays manual).
- A planning pipeline can carry a decisions file the human fills in (the meme pipeline's `decisions.json`: cuts,
  reassignments, trims, per-item overrides) between the automatic stages and the build.
- Automatic edits default to doing nothing and need a measured trigger: crop only named UI chrome, metadata,
  watermarks and unread panels; tighten only margins of 10% or more. v1 of that rule cropped 74 of 171 items ("overall
  pattern im noticing is just an overuse of crops", a reviewer); v2 cropped 19.
- After a rejection, build nothing new until the user has answered a plan page with proof frames ("Nothing new gets
  built until you've decided"), then build the sample pack.

## 11. State and tools live in the job folder
- Keep `00-status.md` ("read first"), a README with the run order and a PLAYBOOK with the rules, and update them at
  every phase. Write a resume file with each research agent's brief before a long run.
- Keep every generator, page builder and helper you will need again inside the job folder. The only copies of an
  explainer's generators and of three review pages' sources once sat in a session's temporary scratchpad; a friend's
  scratchpad was wiped mid-task and his review tools were lost.
- A job folder layout that worked (friend's set): `vo/` (voice + words.json), `sources/<kind>/` each with a manifest
  (file, URL, licence, where used), `music/`, `storyboard/`, `final/` (ae, premiere, renders, sound, README), and
  `_build/` (generators and QA with a README of the rebuild order).
- `ls` a spec path before writing it and give batch files unique names. An overwritten batch file was rebuilt
  exactly from the session transcript (the original Write plus each Edit), but only by luck.
- Copy a pipeline folder into the job's own working folder and run it from there; job data files are read and written
  by relative name.

## 12. A data model worth growing into (from the boss's concept doc, reviewed)
- Adopt: project, page, format, job, output, revision, with each job pinned to a format version; timecoded review
  comments turned into a change list you preview, then run; automated QA gates (loudness, black frames, safe zones,
  captions in sync, faces not cropped); forking a format per client by swapping the brand kit; measuring editor
  minutes per video from job one; rights and contract clauses (the doc names Adobe's "no service bureau" clause:
  check the licence before rendering client work as a service on a seat, not checked by us); configuration sessions
  in Claude Code run by trained editors.
- Too complex for now: a 15-model intelligence layer; a 4-model reframe stack (try Premiere's Auto Reframe first); a
  project file for every daily post.
- The review verdict was "approve the direction, but not as written": news pages need their own rights rule (a "no
  third-party pixels or audio" rule would rule out every news post), a news track (find, verify, add a fact, caption,
  window), the code renderer as the main news engine rather than a fallback, and the trending loop kept running while
  the Adobe engine is proved.

## 13. Free tools first, packaged for reuse
- "we dont wanna buy tools right now... build them yourself... figure out how to make it re usable" (the editor). For
  each need: find the free route (app built-ins, Blender, ffmpeg, open models such as SAM 2, RIFE, Real-ESRGAN,
  procedural assets made in code), prove it on a short test, then package it as a script + JSON preset + a note in the
  matching skill so the next job costs few tokens.
- Free installs still need the user's OK first: say the name, the source and the size (examples asked: reference
  edits about 250 MB, PyTorch + SAM 2 about 3 to 4 GB).
- Name the upgrade the user can do instead of quietly working around it (a GPU driver that enabled NVENC, freeing
  disk space, a throwaway cookies file, free API keys).

## 14. Measure throughput from job one
- Record how long each step takes (Claude time and machine time). Numbers we have: a 4-post news batch 8 to 10 minutes
  of Claude time (about 35 on a heavy verification day); three music edits in about 1.5 hours; a 10:38 explainer rough
  cut in about 4.5 hours; cutdown rounds from most of a day down to about 40 minutes for two long cuts.
- When a step crawls, stop it and write a leaner version (frame grabs went from slowed playback to single-frame grabs:
  42 frames in about a minute). Run slow analysis in the background while you work on the next thing.
