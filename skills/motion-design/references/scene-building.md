# Building a designed motion piece in After Effects (scoped)

**Scope:** only for shots that are entirely designed motion (a brand reel, a designed explainer scene, an animated
storyboard). Our house rule still stands: compile the video in Premiere and use After Effects for elements; presenters,
logos and any asset that may change in review stay Premiere layers (a presenter baked into 17 renders meant 17
re-renders). The runner, the traps and the render templates are in premiere-ae-editing `references/after-effects.md`;
pipelines that build many posts or videos are production-automation's.

## Contents
1. Shape of the build
2. One timeline file
3. Plates from an approved storyboard
4. Testing a scene against its frames
5. Assembling and rendering
6. Into Premiere
7. Fixing after review without breaking links
8. Self-reporting builds
9. Helper agents building scenes in parallel

## 1. Shape of the build
- One module per scene that returns its After Effects code, any helper code and its sample times; a master build
  concatenates every scene into one project.
- Per scene, one content comp and one finish comp (grade, bloom, fringe, vignette); for a short reel, one content comp
  holding every shot on one timeline plus one render comp with the finish.
- Captions in ONE separate comp for the whole film, never inside scene comps, so they can change without touching the
  animation. Designed text that is part of a frame (a typed line, a label, a counter) belongs to its scene.
- Folders inside the project: main comps at the top, `_precomps`, `_footage`, `_assets`. Names are the job's. Never
  put "Claude" in a name a client sees (renders, sequences, delivered files, client-visible projects); internal tools
  and work files may use it (premiere-ae-editing house rule 1).
- `audioEnabled = false` on every footage layer, or its sound comes along into Premiere.
- Every move is two keys with a named ease (`k2`, `chain`); see `motion-rules.md`.
- Our own builds work the same way at the block level: a Python generator per about one minute of video decides
  everything (times from word timings, rects from OCR, crops, scores, asset paths) and writes short JS specs; builder
  libraries draw.

## 2. One timeline file
All times come from one file: scene bounds that never change once approved, word timings (start of word i), a frame snap
F(t), and comp names. The storyboard renderer, the After Effects generator and the sound cue list all read it. Why: it
makes three checks possible (AE frames against storyboard frames, sound cues against animation keys, Premiere placements
against the plan) and one timing change updates all three. Our version of the same idea on ads: one spec list per overlay
in sequence seconds drove the AE build, the Premiere placement and the SFX cue sheet, so no pop ever drifted from its word.

## 3. Plates from an approved storyboard
When a frame was designed in a storyboard kit (HTML or canvas), render its static parts as plates from the SAME kit so
After Effects shows exactly what was approved (named plates per scene, an alpha option for cut-outs, captions hidden in
plates). Animate the plates with two-key moves. Use a rendered image sequence (driven by two eased time-remap keys) only for
what keyframes cannot do, such as a particle field. Prefix every plate id with the scene id. Helpers: `plate`, `seqL` in
scene_lib.jsx.

## 4. Testing a scene against its frames
- Build one scene alone, render sample frames, and put each next to its storyboard frame on one sheet. Look at the sheet with
  your own eyes, fix, repeat; budget about six test runs per scene; stop at "looks like the storyboard and moves well".
- Sample frames: a TEST comp that time-remaps the main comp with HOLD keys onto the chosen times, in a save-as copy,
  rendered with aerender (about 1.5 s a frame). Turn motion blur off for these samples: time-remapped samples otherwise show
  fake motion blur (`testComp` in scene_lib.jsx).
- Compare whole renders numerically too: decode at low resolution with the BT.709 matrix, diff against the preview after a
  small blur, rank by the worst areas; kerning differences score low, missing elements stand out.
- Check the frames on both sides of every transition and chunk join.

## 5. Assembling and rendering
- Master build: all scenes into one project, then render each scene comp as ProRes 422 ("High Quality" template; there is
  no "ProRes 422 HQ" template) and captions as ProRes 4444 with alpha.
- A quick full preview with sound comes from an edit list rendered in After Effects or joined with ffmpeg; check its
  loudness.
- Long films: render in frame ranges, one aerender at a time, join with ffmpeg's concat demuxer, render the audio
  separately. aerender has died near the end of a long render and left an unreadable file.

## 6. Into Premiere
- Ours (default): rendered elements (alpha overlays, moving plates) on their own Premiere tracks.
- Alternative: Dynamic Link (import the comps live). It skips the render and keeps comps live, but every fix must be made in
  those exact comps; footage audio comes along unless disabled; Premiere 26.5 colour-manages linked comps as sRGB and lifts
  the shadows unless each linked item gets a Rec.709 colour override (or the AE project's working space is None). Use it
  only when the user asks or will finish the shots in After Effects.

## 7. Fixing after review without breaking links
- Dynamic Link points at comp IDs: fix comps in place (clear and rebuild the contents of a named comp, keeping the comp),
  never delete and recreate them; otherwise re-import and re-place in Premiere.
- Save every version as a new .aep (save-as of the previous one) so earlier versions stay valid and the working space
  setting carries over.
- When the user edited the After Effects project himself, compare his save with a clean rebuild before regenerating and keep
  his changes.

## 8. Self-reporting builds
Nobody watches After Effects run, so builds report on themselves:
- Wrap each build in try/catch; on failure save `<name>_ERROR.aep` with the error message in a comp name.
- Add comp markers at the SFX beats, so sound placement is one step.
- Build a preview comp at the delivery size over a real frame of the edit next to the alpha element.
- Render the element as ProRes 4444 with alpha plus an H.264 preview; save the .aep next to the renders so the user can edit
  any word, timing or colour by hand.
- When composing a new script from pieces of earlier generators, copy the constants header too (W, H, FPS, colours, fonts,
  layout lines): two renders failed with "W is undefined".

## 9. Helper agents building scenes in parallel
For a film with many scenes, scene builders can work in parallel if they share After Effects through a lock. The brief that
worked, condensed (fill in the brackets):
```
You are building scenes [S08, S09] of a [100 s, 16:9] edit in After Effects by script. The storyboard is approved;
turn its frames into animated comps that look like the frames. Scenes [S03-S05] are built and are the reference for
quality and conventions.

Done means: one content comp + one finish comp per scene from your module; every storyboard frame reproduced in
composition and look; the motion described in each frame's note happens (pushes, landings, typing, highlights,
flashes, transitions); the test sheet puts your render next to each storyboard frame.

House rules: every move is TWO keys with a named ease (settle, bell, accel, gentle, linear, hold), never frame by
frame; clean motion with no bounces, overshoot, spins or cartoony pops [when the brief asks for clean]; where the
board says "continues" build one continuous move; no captions in scene comps; real footage where the board has it,
audioEnabled = false on every footage layer; no "Claude" in any name a client sees (internal tools and work files may use it); keep depictions of
sensitive activity abstract.

Files: the approved frame list with times, voice-over and motion notes; frame images; the plate tool; shared AE
libraries (read, do not edit). Prefix every function and global variable with your scene id, because all modules are
concatenated into one project and a shared name breaks other scenes. Test: the scene test command (queues for the AE
lock). Never open, close, save or quit After Effects or any project yourself, never run aerender, never touch Premiere.

Traps: ES3 only (build JS strings with json.dumps); toComp() on a 3D layer returns [x, y, depth]; effects on shape
layers are clipped to the shape's box; a precomp added to a comp starts at 0 s (set startTime first); straight alpha
for PNG cut-outs; a missing glyph renders blank.

Budget: at most 6 test runs per scene, look at each sheet once, no reviewer agents. Reply with what you built per
frame, what you could not match, sheet paths and plate ids.
```
What went wrong in shared builds, so the brief covers it: a builder's `var tr` replaced the library's `tr()` and broke
every later scene; a helper name clashed with another builder's; one modal error dialog blocks After Effects for every
builder (a harness may dismiss only dialogs it recognises, and must stop on anything else). A comment that starts with
`//@` is an ExtendScript directive and shows a syntax-error dialog that blocks After Effects: never start a comment that way.
