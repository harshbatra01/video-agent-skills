# After Effects by script (AE 2026: v26.5 on the Windows PC, v26.2.1 on the Mac)

Use After Effects only for what Premiere cannot do well: complex animated graphics, keying, 2.5D camera rigs, effects
Premiere lacks. Build it by ExtendScript, render it unattended, and bring it into Premiere as ELEMENTS (alpha overlays,
moving plates) that sit on their own tracks. Assets that recur or may change in review (a presenter's poses, logos,
screenshots) stay as Premiere clips, not baked into renders: a wardrobe change on a presenter baked into 17 renders
meant 17 re-renders. The user never has to open AE. Where each kind of graphic is built and how to check it:
`motion-design.md`; flash transitions for music edits: `transitions.md`; which devices are approved, with every value:
the motion-design skill.
- Alternative (Mac port): comps placed in Premiere by Dynamic Link instead of renders (section 14). It skips the render
  step and keeps the comps live, but every fix must then be made inside those exact comps. Renders as elements stay the
  default; use Dynamic Link when the user asks for it or will finish the shots in AE.

## Contents
1. The pipeline (generator > .jsx > run > check)
2. Running AE safely (Windows and Mac)
3. Render templates and outputs
4. ExtendScript traps (the list that cost renders)
5. Layers, shapes, effects
6. Text and fonts
7. Keying, time remap, 3D renders from collaborators
8. 2.5D stills (presenter + room)
9. Reading an existing .aep
10. Performance
11. When scripts silently do nothing (Windows)
12. Music-edit devices: how they were built (whip, counters, end card, layer order, RGB split, footage audio)
13. Motion helpers: motion_lib.jsx and scene_lib.jsx (from the Mac port)
14. Dynamic Link comps (from the Mac port)

## 1. The pipeline
```python
import sys, os, json
SKILL = os.path.expanduser('~/.claude/skills/premiere-ae-editing')    # same line on Windows and Mac
sys.path.insert(0, os.path.join(SKILL, 'scripts', 'ae'))
from ae_build import write_jsx
shots = [dict(name='B1_01_HOOK'), dict(name='B1_02_TITLE', template='alpha')]
specs = ['SHOTS["B1_01_HOOK"] = (function(){ var c = newComp("B1_01_HOOK", 5.15); stillBg(c, %s, 30, 0.45); ... return c; })();' % json.dumps(bg)]
write_jsx('/job/ae/b1.jsx', shots, specs, out_dir='/job/renders/b1', libs=['/job/ae/my_builders.jsx'])   # C:/job/... on Windows
```
```bash
python scripts/ae/check_jsx.py /job/ae/b1.jsx        # esprima parse of the file and every spec (seconds, no AE)
python scripts/ae/ae_run.py /job/ae/b1.jsx            # waits for a clean AE, runs, waits for renders, reports
python scripts/media/frames.py sheet check.png /job/renders/b1/B1_01_HOOK.mov "a@0.5" "b@2.6" "c@5.0"
```
- A Python generator owns the decisions (times from word timings, rects from OCR, crops, scores); specs are short JS
  calls into builder functions. One batch per ~1 minute of video keeps renders and fixes small.
- `ae_lib.jsx` (always included) holds the safe helpers; put project builders (cards, scales, boards) in your own
  library file and pass it in `libs`. Libraries are copied INTO the .jsx: regenerate after editing a library.
- Each spec runs in its own try/catch: a failure logs "BUILD FAIL i: message line N" and the rest still render.
- Re-render a subset: the shot filter is baked in when the .jsx is written, so regenerate with it:
  `ONLY=B1_02_TITLE,B1_05_CARD python my_generator.py` (or `write_jsx(..., only=[...])`), then run ae_run.py.
- New version of a shot = new name or new folder (renders/v7/...); never overwrite a render the user already has in
  their edit. Relink in Premiere afterwards (prproj-recipes R1).
- Make every build self-reporting, because nobody watches AE run: each generator writes a log, a DONE flag and a meta /
  geometry JSON (start, end, card boxes) and saves the .aep next to the renders, so the user can change any word,
  timing or colour by hand and the Premiere builder can place the renders and match blur windows to the geometry
  (prproj-recipes R20). On a failure save `<name>_ERROR.aep` with the error message in a comp name. For an alpha
  element, add comp markers at the SFX beats and a preview comp (the element over a real frame of the edit, at the
  edit's size), and render ProRes 4444 with alpha ("High Quality with Alpha") plus an H.264 preview ("H.264 - Match
  Render Settings - 15 Mbps").
- One spec list drives picture, placement and sound: word timings -> one spec per overlay in absolute sequence seconds
  (kind, start, end, words with times, count windows, highlight rects) -> (a) the AE generator converts to comp time,
  builds, renders alpha and writes meta + geometry; (b) the Premiere builder places the overlays from the meta,
  disables captions whose midpoint falls inside an overlay and builds glass blurs from the geometry; (c) the SFX cue
  generator reads the same specs (audio.md section 7). Why: one timing change updates all three, with no drift between a
  pop and its word. One edit list can likewise feed both the Premiere XML and the AE preview (prproj-recipes R15,
  `ae_assemble.py`) so they never disagree. Pipelines built on this: production-automation `spec-driven-builds.md`.
- Test one element per type before a full batch (9 types once), then the batch, a QA sheet, and re-renders of only
  the failures.
- After editing a generator or a library, grep the new value in the generated .jsx before rendering: a quoting error
  once left a script unchanged and the "fixed" re-render repeated the old shots.
- Composing a new .jsx from pieces of earlier generators: copy their constants header too (trap 49).
- Swap an asset in old blocks without regenerating them (a presenter's new stills): parse `var BUILDERS = [...]` from a
  COPY of each generated .jsx with `json.JSONDecoder().raw_decode`, replace the asset path in each spec, rewrite the
  ONLY filter, log, DONE and output paths with regexes, assert no old render path is left, write a new .jsx + jobs.json
  per block, and render only the shots that use the asset into a new folder. Why: the old generator state does not need
  rebuilding and earlier renders and scripts stay valid (17 shots re-rendered this way in one round).

## 2. Running AE safely (ae_run.py does all of this)
The risk is the same on both machines: a script sent to AE goes into the AE that is ALREADY running, so a build's
`app.newProject()` can replace the user's open project, and a busy or half-quit AE can swallow the job silently.

### Windows (AfterFX.com -r)
- `AfterFX.exe -r script.jsx` hands the script to an ALREADY RUNNING AE. If one is open (maybe the user's) or still
  quitting, the script runs there or `render()` silently does nothing (status stays QUEUED). So: never launch while
  AE runs; ask the user to close AE. Since 13 Oct 2026 the runner uses the console launcher `AfterFX.com` (section 11).
- AE does not always quit after `app.quit()` (it can sit on the Home screen; File > Exit / Ctrl+Q also failed once).
  Kill it only after every output has stopped growing: killing right after the DONE flag left 1 MB stub .movs.
- After a kill the next launch may show "Crash Repair Options": click Continue.
- When AE will not quit, end it gracefully first: `taskkill /PID <pid>` WITHOUT `/F` (a forced kill can lose AE's
  preferences, including a security preference the user has just ticked), and never `/F` while a render file still
  grows. From Git Bash write `taskkill //PID <pid>`: Git Bash rewrites a lone `/PID` as a path.
- Never pass `-noui`: with it the script did not run.
- Scripts generated on Windows end with `app.quit()`: never run one by hand from File > Scripts inside the user's AE.
- Claude's watchers and background jobs die when the user closes the chat, a capture window or a frozen app (four
  times in one week), but AE keeps rendering. On resume, check the DONE flags, the logs and the file sizes before
  re-running anything, and kill leftover frame-grab processes of your own that could collide. A Monitor-style watch on
  the render log expires after about 30 minutes: re-arm it for long chains.

### Mac (osascript DoScript, from the Mac port, tested 11 Oct 2026)
- osascript `DoScript` hands the script to the AE that is ALREADY running. The runner probes AE first (file, unsaved
  changes, item count) and refuses when a project is open; scripts generated on a Mac (ae_build, ae_assemble, ae_dump)
  also refuse on their own (`refusing to run` in the log). An AE that is open with an empty untitled project is reused
  and left open.
- AE not running: launched hidden with `open -g <app>` and pinged until it answers (5-6 s). Only that instance is quit
  afterwards (DoScript `app.quit()`, then TERM to its own PID if it hangs). The scripts never call `app.quit()`, so a
  .jsx run by hand never closes the user's AE.
- DoScript returns 0 even on failure, and a modal dialog makes it return without running anything: the log + DONE flag
  are the only truth. Outputs must stop growing before AE is quit. More Mac runner facts: mac-notes.md.

### Both
- Never change AE's scripting security preferences. Close projects with `CloseOptions.DO_NOT_SAVE_CHANGES`.
- `app.beginSuppressDialogs()` at the top (`endSuppressDialogs(false)` at the end); write a log file with every step
  (the runner's `log()`), check it after.
- Check `app.project.file` inside EVERY script, not once per session (trap 27), and run tests on a COPY of a deliverable
  .aep (trap 28).
- Building inside one of the user's projects (rare, only when asked, e.g. adding comps to a Dynamic Link project): check
  `app.project.file` is the expected file inside every script, build in a clearly named folder, and leave saving to the
  user.

## 3. Render templates and outputs (names checked 7 Oct 2026 on Windows, 11 Oct 2026 on the Mac)

| ae_build key | AE template name | output |
|---|---|---|
| prores | "High Quality" | ProRes 422 10-bit .mov, opaque shots for Premiere (carries comp audio as PCM) |
| alpha | "High Quality with Alpha" | ProRes 4444 + alpha .mov, overlays on a top track |
| h264 | "H.264 - Match Render Settings - 15 Mbps" | .mp4 WITH audio, previews (5 and 40 Mbps versions exist too) |
| tiff | "TIFF Sequence with Alpha" | frames for analysis / tracking |

- There is NO "Apple ProRes 422 HQ" template on either machine (asking for it logs "template fail" and falls back).
  "Lossless" is QuickTime Animation (huge).
- `om.setSettings` Format is read-only: pick a template. Queue ONE item at a time (`rq.render()` per item, then
  `rq.remove()`): queueing 20 items at once crashed AE.
- Read each item's `status` after `render()` and log it: 3019 = DONE; 3015 = QUEUED, meaning it never rendered (the
  script went to an AE that was still quitting, or render silently did nothing); 3018 = ERR_STOPPED (catch the reason
  with `app.onError`, trap 29).
- Comp frame rate 29.97 for Premiere 29.97 timelines; make comps exactly the shot length the edit needs (from word times).
- AE as a frame extractor when a machine has no ffmpeg (fallback only): a quarter-size comp of the source (scale 25%),
  one render-queue item per job rendering only the frames that are visible in the edit (the cut pieces minus the
  B-roll windows), "TIFF Sequence with Alpha", one item at a time, re-run only incomplete batches. Queueing all 20 jobs
  at once crashed AE.

## 4. ExtendScript traps
1. ES3: no let/const, arrow functions, template strings, Array indexOf/map/forEach/filter, JSON (pass data as JS
   literals written by `json.dumps`). `check_jsx.py` warns about these.
2. Adding an effect or a shape property INVALIDATES earlier handles on that layer: re-fetch by matchName afterwards
   (`fx()`, `groupOf()`, `trimOf()` do).
3. New shape layers sit at the comp centre: set Position [0,0] when path vertices are comp coordinates.
4. Mask path expressions are in layer space: wrap comp points with `fromComp()`.
5. Reading `comp.bgColor` throws "invalid numeric result" in AE 2026 (setting it is fine).
6. Levels "Output White" cannot be keyframed (`canVaryOverTime` false): animate darkening with Exposure
   (`ADBE Exposure2`); Brightness & Contrast barely dims whites. `keys()` logs a property that cannot be keyed and
   sets its last value instead, so one such param never aborts a whole block.
7. Nested params (Fractal Noise > Transform > Scale, Noise Type, Keylight groups) need the recursive `findProp`.
8. Layers made earlier sit UNDER later ones: text made before its plate ends up under it (washed out). Use
   `moveBefore` / `moveToBeginning`.
9. Time remap: AE adds its own first/last keys. Remove ONLY those after adding yours. Removing ALL keys switches remapping
   off and the next `setValueAtTime` throws "property ... is hidden" (`remapL`).
10. Effects on SHAPE layers are clipped to the shape's bounding box: a blurred ellipse glow shows square edges (the
    "glow cuts off as a square" review note). Glows / soft shadows = comp-size SOLID + feathered mask
    (`softEllipse`, `softBand`). Gaussian Blur "Repeat Edge Pixels" (`ADBE Gaussian Blur 2-0003`) also clips: set 0.
11. Shape stack order matters: path, then Trim Paths, then Stroke. An operator only changes what is ABOVE it.
12. Simple Choker "Choke Matte" negative = a sticker outline (Minimax default channel did nothing).
13. Track matte (AE 2023+): `layer.setTrackMatte(matteLayer, TrackMatteType.LUMA)` and hide the matte layer.
14. Corner Pin points accept per-corner expressions (planes driven by a camera null, section 8).
15. `layer instanceof ShapeLayer` was unreliable: use `layer.matchName` ("ADBE Vector Layer", "ADBE Text Layer").
16. Strings with backslashes or "\n" written from Python through a bash heredoc get mangled (`\\` collapses): write
    generators with the Write/Edit tools, and build JS strings with `json.dumps`.
17. (Windows) Python prints with cp1252: set `PYTHONIOENCODING=utf-8` before printing glyphs like the not-equal sign.
18. (Mac) ExtendScript `File` writes `\r` line endings on macOS unless `f.lineFeed = "Unix"`: set it on every file a
    script writes (logs, DONE flags, dumps). ae_build.py and ae_assemble.py add it when they run on a Mac.
19. New projects defaulted to working space Rec.709 Gamma 2.4 on the Mac (26.2.1), which shifted sRGB PNG colours
    (#1A6317 became #266B23): set `app.project.workingSpace = "sRGB IEC61966-2.1"` right after `app.newProject()`.
    ae_build.py does it on a Mac (`working_space='auto'`), and so does the script ae_assemble.py writes there; on
    Windows ae_build keeps AE's default unless you pass `working_space='sRGB IEC61966-2.1'`, which changes render
    colours, so test one shot against a PNG first.
20. `"text" + someAEArray` and `"text" + new Date()` throw in this ExtendScript: format element by element, use
    `new Date().toString()`.
21. Build scripts run in one big function scope: a `var el = ...` replaced the `el()` helper and broke every later call
    with "Unable to call property". In multi-module builds prefix every helper and global with the module id (a scene's
    `var tr` killed ae_lib's `tr()`); never give two expression variables the same name in a generated template.
22. Masks are applied BEFORE effects: a Transform effect shifts an already-masked layer (a split screen built that way
    showed two thin strips and a black middle), and a shrinking mask on a CC Sphere layer cut the texture first. Shift
    the layer by position and mask with `fromComp`, or use a track matte, which applies after effects.
23. A precomp added with `comp.layers.add(pre)` starts at 0 s: set `startTime = t0` before in/out, or a 2 s precomp
    placed at 23 s is simply not there (no error).
24. A comp with nothing at the back renders TRANSPARENT there; a Multiply layer (a baked vignette PNG) over transparency
    shows its own colour (white). Put an opaque black solid at the bottom of any finishing comp.
25. Glow (Add) over bright footage blew 40% of a frame to white. For a reference-matched bloom use an adjustment layer:
    Levels2 input black = threshold, Gaussian Blur, blend SCREEN, opacity = amount (exactly `1-(1-x)(1-amt*blur(hi))`).
    Gaussian Blur sigma = 0.466 px per Blurriness unit (measured). On broadcast footage keep any bloom light
    (section 12: threshold 85+, intensity 0.2 or less).
26. Easy Levels2 and Hue/Saturation values set by script RENDER correctly but read back as defaults after the project
    is reopened (the probe is wrong, not the render). Pro Levels2 (Individual Controls) reads back fine. Many effect
    values are 0-1 from a script (section 12).
27. Check `app.project.file` inside EVERY script, not once per session: the user may reopen their project between your
    runs. A guarded build also has to recognise its own untitled leftovers (by a known item name), or the next run
    refuses.
28. Test scripts open a COPY of a deliverable .aep, never the deliverable: AE auto-saved an interrupted test into its
    Auto-Save folder and reopened the deliverable dirty after a relaunch.
29. `app.onError = function (msg, severity) {...}` captures render errors that `renderQueue.render()` hides (items just
    show ERR_STOPPED); it also receives PROGRESS lines. Restore the old handler afterwards.
30. aerender with the AE GUI open can render from cached footage after plate files changed on disk: reload each footage
    item (`item.mainSource.reload()`) and purge before rendering, then check one pixel of the render against the plate.
    The first aerender right after a script reopened a project can fail: retry. One aerender at a time.
31. `setTemporalEaseAtKey` takes ONE KeyframeEase per side for spatial properties (Position) and one per dimension for
    non-spatial 2D/3D properties (Scale).
32. Parenting compensates for the parent's transform at the current time: parent children to a null BEFORE keyframing
    the null, and if the parent's scale is not 100% at t = 0, reset the child's scale and position after setting
    `.parent`. Parenting passes transforms, not opacity (`thisLayer.parent.transform.opacity` in the child).
33. Adding anything inside a shape group invalidates old references to that group ("Object is invalid"): keep name
    paths and look groups up fresh from the root. The FIRST group in Contents draws on top: create top items first or
    `moveTo(1)` each new group.
34. `toComp()` on a 3D layer returns [x, y, depth]: pass only x, y to `createPath` (it silently ignores 3-number points).
35. Image sequences: enable time remapping BEFORE setting in/out points, or AE clamps them to the source and the layer
    ends before its shot begins.
36. Sample frames rendered through a time-remapped TEST comp show fake motion blur: turn motion blur off for samples
    (scene_lib `testComp`, section 13).
37. A 3-frame panel wipe with layer motion blur on renders as two ghosted copies: no motion blur on hard wipes.
38. Fill (`ADBE Fill`) opacity 0 makes the layer invisible; crossfade to a flat colour with Tint's "Amount to Tint".
39. Text animator "Tracking Amount" is in pixels per character (150 blew a 28 px line up to 2,370 px wide). TextDocument
    has no lining/old-style figure control: pick a font with lining numerals for numbers.
40. Wave Warp on a comp-sized solid samples outside the layer at the edges: use an oversized solid.
41. In a red/cyan fringe made of channel copies, keep every channel's scale at 100% or more, or bright frames get a
    coloured edge.
42. `prop.setValuesAtTimes(times, values)` sets hundreds of keys in one call: the fast way to write the per-frame keys
    of a flash recipe (transitions.md).
43. Ease-driven reveals: a posterized matte only changes over a few stops of an Exposure sweep, so key just that range;
    an "accel" curve evens out an exponential front. Two-key moves on DIFFERENT properties (layer Scale Y, then a
    Transform effect's Scale Width) stop one dimension dragging the other (CRT switch-off).
44. A comment that starts with `//@` is an ExtendScript preprocessor directive: AE shows a syntax-error dialog that
    blocks it for every later job. Never start a comment that way, generated code included.
45. Leftover entrance keys: a 3-frame opacity fade left over from a fly-in dimmed a product right at the cut. For items
    that must hold, strip their Position / Rotation / Opacity keys and set Opacity 100%.
46. Shapes that SCALE need their anchor at the shape's centre, or they grow from a corner (a code pill did). Shapes that
    reveal from the top-left keep the anchor at [0, 0] with the Rect Position at [w/2, h/2].
47. Script scales differ from the UI, and out-of-range values fail quietly: Lumetri saturation is 0-300 with 100 =
    normal (92 = a slight desaturation, 0 = black and white; "-8" threw "Value -8 out of range 0 to 300" and that param
    was skipped); Threshold is 0-1 (0.43 = level 110); Shift Channels menus run 1-10; Easy Levels values are 0-1.
    Probe a doubtful param before a batch (section 5).
48. A layer whose time remap repeats or holds frames (a stutter on a contact frame, a freeze) needs frame blending OFF,
    or the repeats smear; key the remap exactly on frame times.
49. Composing a new .jsx from pieces of earlier generators: copy their constants header too (W, H, FPS, colour
    arrays, fonts, layout y values): two renders failed with "ReferenceError: W is undefined" without it.

## 5. Layers, shapes, effects (ae_lib.jsx)
- Transform: `P(l) S(l) O(l) R(l) A(l)`; keys: `keys(prop, [[t, v, easeIn?, easeOut?], ...])` (33 gentle, 75-90 strong).
- Footage: `imp(path)` (cached; PNG cutouts imported with STRAIGHT alpha or the edges go dark), `cover(layer, crop)`.
- Shapes: `rrect`, `ellipseL`, `drawPath` (Trim Paths draw-on, smooth option), `strokeLine`, `checkL`, `outlineBox`.
- Cards: `imgCard(comp, name, file, crop, w, x, y, rot, dur)` returns {layer, comp, ox, oy, s}: a source pixel (sx, sy)
  sits at card pixel (sx + ox, sy + oy), so OCR rects map straight onto the card for `highlighter`.
- Light / finish: `softEllipse`, `softBand`, `vignette`, `grain`, `stillBg` (blurred dim background with slow push),
  `shadow`, `glow`, `gaussBlur` (edges off), `boxBlur`, `levels`, `exposure`, `tint`, `lumetri(l, {temp, sat, exp, con, ...})`.
- Motion: `popIn` (scales past the target to 1.1x, then settles), `flyIn`, `slowPush`, `typeOn`. Two-key eased moves
  with no overshoot: `k2` / `chain` (section 13).
- Effect matchNames in use: ADBE Drop Shadow (-0002 opacity 0-255, -0003 direction, -0004 distance, -0005 softness),
  ADBE Glo2, ADBE Camera Lens Blur, ADBE Box Blur2, ADBE Gaussian Blur 2, ADBE Easy Levels2, ADBE Exposure2, ADBE Tint,
  ADBE Lumetri (-0007 temp, -0008 tint, -0011 exposure, -0012 contrast, -0013 highlights, -0014 shadows, -0015 whites,
  -0016 blacks, -0020 saturation on a 0-300 scale, trap 47), ADBE Noise, ADBE Roughen Edges, Keylight 906, ADBE Simple
  Choker, ADBE Corner Pin.
- Transform (`ADBE Geometry2`, verified 13 Oct 2026): -0001 Anchor, -0002 Position, -0003 Scale Height, -0004 Scale
  Width, -0007 Rotation, -0009 Use Comp Shutter, -0010 Shutter Angle, -0011 Uniform Scale. Exposure (`ADBE Exposure2`):
  -0003 Exposure (stops), -0004 Offset (lifts blacks), -0022 "Bypass Linear Light Conversion" (untested; it may change
  the gamma-space behaviour described in transitions.md).
- Probe the install once per machine: dump `app.effects` (category, name, matchName) and each effect's params to text
  files, and look params up by matchName with a display-name fallback. Why: names and menu counts differ between
  versions, and a silently wrong value costs a render. Probe a doubtful param with a Ramp solid through the effect and
  `comp.saveFrameToPng` (section 12).
- Custom easing as per-frame linear keys: evaluate any curve per frame and write it with `setValuesAtTimes` plus LINEAR
  interpolation (a `frameKeys`-style helper). Export the same function as geometry (JSON) so a Premiere blur window or
  mask follows it exactly (prproj-recipes R20).

## 6. Text and fonts
- Fonts by PostScript name. Names that worked on the Windows PC: "ProximaNova-Semibold", "ProximaNova-Regular",
  "ProximaNova-Extrabld", "Montserrat-Black", "SegoeUI-Semibold", "Magneto-Bold", "KindSansThin", "Coolvetica Heavy
  Comp", PowerGrotesk. On the Mac (11 Oct 2026): ProximaNova-Semibold, Montserrat-Black, Inter (variable:
  Inter-SemiBold resolves), JetBrainsMono-Regular, DMSerifDisplay-Italic, HostGrotesk-Medium, ArialUnicodeMS,
  PPEditorialNew-Regular, Gotham-Bold/Medium. What a machine has: `python env_check.py` (Windows font folders),
  `scripts/media/fontcheck Name ...` (Mac). Adobe Fonts may be active only inside AE (check there with
  `app.fonts.getFontsByPostScriptName`).
- A missing glyph renders BLANK with no error. Proxima Nova has no check mark, arrows, approx, star or not-equal;
  Montserrat-Black has no check mark (has not-equal; the Mac check also found no star); Inter lacks the heavy check
  mark. Check a string first on the Mac with `fontcheck --text "<string>" Font-Name`. `txt()` switches strings with
  those glyphs to the `GLYPH_FALLBACK` font, which ae_lib picks per machine: Segoe UI Semibold on Windows, Arial Unicode
  MS on a Mac (it has all of them; verified in a render 11 Oct 2026). Or draw the symbol (`checkL`).
- Mock type in headless Chrome with Google Fonts when the Adobe Fonts files are hidden (CoreSync on the Mac).
- Lay plates out from the measured text: `sourceRectAtTime` (`rect`, `centreAnchor`, `pill`).
- `txt(..., x, y)` puts the BASELINE at y (point text), and `centreAnchor` keeps the text where it is. So capitals sit
  about 0.72 x size ABOVE the y you asked for: a plan that thinks y is the centre puts big words a third of their size
  too high (seen 13 Oct: "NOW" at 300 px landed at the very top edge). Plan in baselines, or convert first.
- `\n` inside a text string = a new line; the Python side must emit it as the two characters backslash-n inside a JS
  string (json.dumps does).
- Route ALL text through one helper with a font map and a premium switch (a `txt()` with `FONT_MAP` and
  `PREMIUM_TYPE`): restyling about 93 shots then cost one switch plus re-renders. The switch that passed: Montserrat-Black
  -> ProximaNova-Semibold at 0.92x the size, tracking +30 on all-caps and +10 otherwise; strings with not-equal, arrows,
  approx, star, tick or "x" signs go to the glyph-fallback font. The design side: motion-design `titles-captions-type.md`.
- Type-on by words: a Text Animator with Opacity 0 and a Range Selector "Based On" = Words (value 3), Start keyed
  0 -> 100 over the read time.
- Count-ups: a Source Text expression `Math.round(ease(time, a, b, from, to)) + suffix`, switching to a final string
  after a time (for a range like "20-30"); put it on every copy (RGB-split copies too) so they agree. Colour that follows
  progress: a Fill Color expression `linear()` on the SAME eased progress (green -> yellow at 0.55 -> red) and a bar's
  Rect Size from it too, so number, length and colour never disagree (a meter stayed pale yellow until this).
- Partial-word roll (two near-identical words, only the middle changes): a fixed prefix and suffix, the middle rolling
  through two track-matte windows, spacing from each full word's real width (`sourceRectAtTime`). The recipe and its
  timing: motion-design `titles-captions-type.md`.

## 7. Keying, time remap, 3D renders from collaborators
- Green screens from Blender keyed cleanly with Keylight 906: Screen Colour = the screen's RGB (sample a corner pixel
  of a frame grab), Clip Black 12, Clip White 88, Screen Shrink/Grow -0.5 (`keyL(comp, file, [r, g, b], remap)`).
- Fit a render to a beat with time remap keys `[[comp t, source t], ...]` (`remapL`); 2x speed = [[0, 0], [2, 4]].
- Renders arrive at 24 fps and odd sizes (1080x1080): put them in a 29.97 comp, `cover()` or scale to taste.
- Check every render first: `frames.py even sheet.png 6 render1.mp4 render2.mp4 ...` (one row per file, metadata in
  the label) to decide where each fits before building.
- Ask collaborators for transparency (or green screen with a clean screen colour), 30 fps (or 29.97) instead of 24, and
  4K if possible: it saves a key and a frame-rate conversion per render.
- Velocity ramps on the beat: a Gaussian speed dip around an anchor (far speed 1.1-1.4, near 0.35-0.4, width 0.10-0.14 s),
  remap keys every 1/15 s, and the source time pinned to the anchor so the key frame of the move lands exactly on the
  hit (a `ramp_rk`-style helper). A stutter repeats the contact frame over a snare roll with remap keys on exact frame
  times and frame blending off (trap 48).
- Tracked overlays from your own tracker: a null keyed with [t, x, y, rotation, scale] samples, the element parented to
  it (parent BEFORE keying the null, trap 32), rendered as alpha and placed on the Premiere track under the zoom layers
  so the zooms move it with the picture (prproj-recipes R21). The tracker: media-toolkit.md section 13.
- Mocha AE ships with After Effects 2026 (Effect > Boris FX Mocha; on Windows in Plug-ins\Effects\mochaAE): check
  before telling the user a tracker is missing. The user may prefer to do planar tracks himself.
- One-click subject mattes inside the apps (research, not tried here): AE 26.2 Object Matte (Apr 2026), Premiere 26
  Object Mask (Jan 2026). Test one on a hard shot before running SAM 2 (media-toolkit.md section 12).

## 8. 2.5D stills (presenter cut-outs in a room)
No fake breathing or sway on stills (the user says it looks AI). Life comes from a camera rig, word-timed pose swaps
2 frames early (2-frame dissolve), a contact shadow, light wrap, a colour match and grain. This section is the rig's
mechanics; the presenter stack and warm-room values that passed, the camera values and the taste are in motion-design
`depth-2.5d-3d.md` sections 2-5 (one place, so they cannot drift apart).
- Planes: cut one room image along its measured floor lines (back wall, side wall, floor, window) with 3 px overlap and
  4x-supersampled masks; extend the window view past the glass with classic Content-Aware Fill so the frame can slide
  over it.
- Depth: every layer has an inverse depth w (z = 1 / w); per plane w = A*X + B*Y + C. Example room: floor
  w = (Y - 550) / 672 with the horizon at y 550; the walls from the floor-line slopes (+0.188 and -0.231 through the
  corner at 757, 1222); the window plane w = 0.1.
- Camera: for a truck T, V and a dolly D, a point maps to x' = cx + ((x - cx) * z - T) / (z - D), and the same for y
  with V. Room planes get Corner Pin expressions computing that on all 4 corners (trap 14); the presenter and her
  shadow get position + scale 100 * z / (z - D) at their own depth (presenter w 1.9, her shadow on the wall w 1.05). One
  CAM null with 3 sliders (Truck X, Truck Y, Dolly %) drives everything. Check the last frame for gaps at the plane
  seams (none at the values used).
- Presenter stack, built as precomps: a POSES comp (the word-timed swaps), an EDGE matte made from white-filled poses
  minus a blurred black-filled copy, a LIGHT WRAP (the room blurred and luma-matted by the edge, in Screen) and a
  SHADOW (the poses filled dark, blurred, in Multiply, offset onto the wall). Values: depth-2.5d-3d.md section 3.
- Sitting the cut-out into a warm room uses Levels and Tint on the presenter, Camera Lens Blur on the room plate, Box
  Blur on the window plane and Noise on a top adjustment layer (values: depth-2.5d-3d.md section 3). Matching a new
  still's colour to the approved ones: grading.md section 8.
- Pose alignment: per pose measure w, h, top (first opaque row), torso centre x and head centre x; anchor each pose at
  its torso centre bottom and scale by one common height over h (1455 / h on one job) so heads line up across swaps.
  New stills that are pixel-aligned with the old ones only need the cut-out folder changed: no timing or position edits.
- Deliver the rig as a moving plate and keep the presenter as Premiere layers where possible (SKILL.md rule 10): a
  wardrobe change baked into 17 rig renders meant 17 re-renders. Rig shots render slowly (section 10).

## 9. Reading an existing .aep
`python scripts/ae/ae_dump.py out.txt reference.aep` copies the project and dumps comps, layers (type, in/out, parent,
matte, blend), effects with matchNames, keyframes (first 6 per property) and expressions. Use it to copy a reference look
exactly (a score graphic was rebuilt from its path keyframes this way). AE must be closed first (on
the Mac it may also be open with an empty untitled project). The dump script writes its `START` log line first (since
14 Oct 2026): before that, a dump running longer than about 3 min 50 s on Windows tripped `ae_run.py`'s 150 s
"NO START" check and AE was killed mid-dump. On a Mac `ae_dump.py` always runs After Effects 2026 (it passes no
`--ae`); with only AE 2025 installed, run `ae_run.py <the _aedump.jsx> --ae 2025` yourself.
- "Copy exactly what we used before" means numbers from the source, never a redraw by eye: the art from the old
  project's PSD with alpha (`psd_composite.read_psd`, stills-and-sources.md), the motion from the old .aep's keyframes
  (its path keys and their times), and the layout maths written down (how a value maps to size, and how long each
  step takes).

## 10. Performance
- Fast Box Blur is far lighter than Camera Lens Blur on big precomps; precompose static parts.
- Render tests at 2 s comps before a 100-shot batch (on the Mac, two 2 s 1080x1920 ProRes shots took 11 s including the
  AE launch). Heavy batches: one AE at a time, sequential (a shell loop calling ae_run.py per batch), never two AE
  instances or two aerenders.
- Long films: aerender in `-s/-e` frame ranges joined with ffmpeg concat (mac-notes.md): long renders can die near the
  end and leave an unreadable file.
- Photoshop can be scripted too (see `stills-and-sources.md`), but it can fail to launch by COM on Windows: numpy is
  often faster for simple cutouts.
- Render cost by shot type (Windows laptop, Oct 2026): graphic and card shots render in seconds; 2.5D rig shots with
  lens blur on a 2528 x 1684 room are slow: 3 presenter shots about 6.5 min, a 26.8 s end shot 518 s (447 MB ProRes),
  all 17 presenter shots about 45 min, a 10:38 H.264 preview about 20 min. Decide the re-render scope by shot type.
- A 30 s 1080x1920 layered music edit (every clip, word, hit and transition a live layer): a full H.264 render took
  82-111 s (about 2 min on an early version) and got slower once every clip carried Motion Tile. Render one moment
  first by setting the comp's work area, then a 6 s test, then the full preview; ProRes only for the final.
- Scripted builds leave AE auto-saves behind (107 auto-save .aep copies of 2-8.6 MB each in one build folder): keep
  build projects in a scratch folder, or offer to clean up after delivery (ask first, recycle bin only).

## 11. When scripts silently do nothing (Windows, 13 Oct 2026)
- `AfterFX.exe -r x.jsx` gives NO error when scripting is blocked: AE just sits on the Home screen. The cause on 13 Oct:
  Edit > Preferences > Scripting & Expressions > "Allow Scripts to Write Files and Access Network" was OFF (likely
  reset by an update). Only the user turns it on (security pref). To see the real error, run a 2-line ping script via
  File > Scripts > Run Script File: AE then shows "Permission denied (is ... enabled?)".
- Generated scripts now log `START <version>` first; `ae_run.py` stops after 150 s with a NO START message instead of
  waiting for the full timeout.
- Waiting for the user to tick the preference: do not watch the screen (the user may be working on the PC). Run a
  2-line ping .jsx that writes a text file every 30 s and start the real job once the file appears; AE's preferences
  file can be read from disk to see the setting without touching the UI.
- Same day, AE 26.5 with the new Home screen: `AfterFX.exe -r` ran NOTHING even with the pref on, while the console launcher
  `AfterFX.com -r x.jsx` ran scripts, rendered and returned. `ae_run.py` now prefers AfterFX.com. That process runs as
  "AfterFX.com" in tasklist (not AfterFX.exe), so `ae_running()` checks both names.
- The Mac version of "nothing happened" is DoScript returning without the DONE flag (a modal dialog in AE):
  mac-notes.md.

## 12. Music-edit devices: how they were built (13 Oct 2026)
The code is not in this skill: it is the music-edit kit's After Effects libraries, `edits_lib.jsx` and `fx_lib.jsx` in
`~/VisionKit/kit/library/pipelines/edits-kit/tools/ae/` (built by that kit's `build_edit.py`). Rendering right is not
the same as approved: the status of every device is in the motion-design skill
(`references/effect-vocabulary-and-taste.md`). Mechanics below.
- REJECTED by the user (13 Oct review: "looks ass"): the whip below shows a crisp mirrored frame on the hold frame
  (no motion there, so no blur). Use the zoom cut instead. Kept for the record:
- Whip transition with no plugin: ONE adjustment layer spanning the cut (about 4 frames each side) with Motion Tile
  (Output Width/Height 300, Mirror Edges on) then Transform. Position keys: centre, then offset -0.55 x width ONE FRAME
  before the cut with a HOLD out-key, then +0.55 x width ON the cut, then centre. The hold stops motion blur from
  smearing across the cut; the Transform effect's own shutter (Use Comp Shutter off, 200) blurs the slide. The mirror
  tiles show for a frame like a kaleidoscope, which reads as a style, not an error.
- Stepped counters (a % that ticks 97, 98, 99 on a snare roll): the first segment eased, every later key HOLD
  (set key 2 to BEZIER in / HOLD out, later keys HOLD both ways). Drive the number with a Source Text expression
  holding an array of [time, value] steps, so the text and the shape always agree. (The charging-battery motif it was
  built for was rejected as a concept: a motif must come from the subject's real story.)
- End card for a wide gesture that a 9:16 crop would cut: the clip at "contain" scale in the middle, over a cover copy
  of itself with Fast Box Blur 40 and Exposure -1.6, slow push 100 -> 105%; title in the dark band above, credit below.
- Lock-on ring (REJECTED in the v3 review, "the shot effect it just doesnt look nice"; reticle gimmicks are banned;
  mechanics only): one shape layer with several groups (ring stroke, centre dot, four ticks); use each group right
  after `addProperty` (later adds invalidate older references). Scale 280 -> 100% and rotation -90 -> 0 over 0.2 s,
  landing exactly on the beat, then a 112% pulse. Place anything on the subject in COMP space: when the clip is framed
  from a matte, the subject sits at the comp centre unless the anchor was clamped at a frame edge, so check the clamp.
- Zoom cut (replaced whips, approved look): adjustment layer from 2 frames before the cut to 3 after; Transform scale
  100 -> 120% into the cut (eased), held across it, back to 100% over 3 frames; CC Radial Fast Blur Amount 0 -> 55 -> 0
  centred on the picture; Transform's own shutter for blur. No mirrored or static frames.
- Letterbox layouts (picture in a band, black bars), bottom to top: footage; type behind the player + the cut-out;
  silhouette strobes; section looks; the GRADE AND VIGNETTE; hit adjustment layers (punch / shake / zoom cut); the bar
  solids; type that sits in the bars; pop-out cut-outs (the player breaking over the bar edge); front type; flashes and
  transition frames on top. Why: a grade or vignette over a flash turns flat white into a grey gradient (the training
  round moved them below the transitions; an earlier version of this list had the grade on top). Flashes must be
  band-size solids: a part-opacity full-frame white turns the black bars grey and looks cheap. A flash also hides a
  white silhouette strobe on the same frame: use one or the other.
- Colour pop: an adjustment layer at Lumetri saturation 0 and contrast 25 over the clip, with the subject's colour
  cut-out laid again above it. Only on a shot with visible background: on a tight close-up there is nothing to turn
  grey, so the effect is invisible.
- Textured type with no plugin: Gradient Ramp on a text layer fills only the letters (start / end points are in LAYER
  space: take them from sourceRectAtTime), then Noise about 14% for grain inside the letters, a soft Glow, and an offset
  copy of the text in a colour BEHIND it that slides out 3% of the size on the slam = printed depth.
  Alternative (Mac port): when a ramp on a text layer seems to ignore its points (most likely comp coordinates were
  passed instead of layer ones), put the ramp on a comp-sized solid in comp coordinates and track-matte it by the text.
- Event timing: a layer's in point must be at or a hair before its frame. Times rounded to 4 decimals (20.1667) land
  AFTER the real frame time (20.16666...) whenever the frame is 1/3 or 2/3 through a hundredth, and the layer appears one
  frame late; in v1-v3 of the first music edit that hit about a third of all cuts and hits. Snap every in/out point
  and hit to round(t x fps) / fps minus 0.1 ms before writing the script.
- FOOTAGE AUDIO: every video layer added by script brings its own sound, ON by default, and every duplicate or cutout
  copy brings it again. Set `layer.audioEnabled = false` on all footage layers (keep only the music and SFX). Missed in
  four renders of the first music edit; caught by the user. Check: subtract the song from the render's audio after
  cross-correlating for the encoder delay (AAC adds about 21 ms): correlation with the song went 0.62 -> 0.99 and the
  leftover dropped from -9 dB (as loud as the song) to -36 dB. Same inside Dynamic Link comps (section 14).
- Shift Channels menu values: 1 Alpha, 2 Red, 3 Green, 4 Blue, ... 9 Full On, 10 Full Off (11 throws "out of range").
- True RGB split without plugins: on the clip layer itself, Shift Channels keyed to keep GREEN only for the few frames;
  two `layer.duplicate()` copies (they keep time remap, framing, effects: strip the copied Shift Channels first) set to
  red only and blue only, blending ADD, offset sideways by about 30 px and sliding back into register.
- Posterize Time on an adjustment layer holds frames of EVERYTHING below it: keep 1-frame flickers / flashes ABOVE it,
  or they smear across 2-3 frames.
- Transitions that read well on real cuts (13 Oct test reel, 1080x1920 letterbox): shutter (bars close / open with a
  hot line), invert flicker ("I.I"), B&W negative strobe into a B&W section ("IN.NB"), diagonal gradient colour flash
  in Add mode (orange -> pink), true RGB split, Wave Warp square-wave glitch with per-frame random height / phase plus
  CC Color Offset hue jumps, rotational spin with Transform shutter 300. Rejected: a cut-out "pop" built from a white
  matted rim + background dim (reads as a pale white wash). Later verdicts: the shutter, the spin and the box glitch
  were rejected as "PowerPoint"; the invert flicker, the negative strobe into B&W, the gradient colour flash and the true
  RGB split were kept (the full status list: motion-design `references/transitions.md` section 2).
- Before using a new transition in an edit, render a test reel (one real cut per transition, 1.2 s each) and review
  every frame around each cut; it costs about 45 s of render.
- A soft whole-picture bloom (Glow on an adjustment layer) turns broadcast pitches neon: threshold 85+, intensity 0.2 or
  less. A full list of this machine's effects (category, name, matchName) can be dumped from `app.effects`.
- SCRIPT VALUES CAN BE NORMALIZED 0-1, and out-of-range values are accepted silently. Threshold's Level (UI 0-255) is
  0-1 from a script: setValue(110) gave all-black frames with no error, 0.43 = level 110. Easy Levels input/output
  values are 0-1 too. When an effect looks blank or saturated, probe it: a horizontal Ramp solid through the effect,
  `comp.saveFrameToPng(0, file)`, then read where the edge falls in the PNG.
- `layer.duplicate()` puts the copy directly ABOVE ITS SOURCE, not at the top of the comp: anything created earlier
  (a paper solid, a blurred background copy) stays above it and hides it. After duplicating, `copy.moveBefore(layer)`
  to the place it must sit. Track mattes (AE 2023+ `setTrackMatte`) reference a layer by identity, so moving the
  matted layer does not break the matte.
- Freeze a layer (and its animated framing) on one moment with expressions: time remap `valueAtTime(t)`, and the same
  on Anchor / Position / Scale when they are keyed; delay a layer with `valueAtTime(time - dt)` on the remap.
  (motion_lib `freeze` holds a layer on one source frame with exactly two remap keys, section 13.)
- Frozen clones of a player only read when the camera is static (rim / baseline cameras): broadcast cameras follow the
  player, so a frozen copy lands on top of him.

## 13. Motion helpers: motion_lib.jsx and scene_lib.jsx (from the Mac port, 13 Oct 2026)
Two ES3 libraries on top of `ae_lib.jsx`, written for short documentary reels and a storyboard-to-AE build. Pass them in
`libs`, motion_lib first (scene_lib uses its `k2`, `EASES`, `setEase`, `eff`, `setE`, `impF`, `filed`, `chanOnly`):
```python
LIB = os.path.join(SKILL, 'scripts', 'ae')
write_jsx(jsx, shots, specs, out_dir=..., libs=[os.path.join(LIB, 'motion_lib.jsx'), os.path.join(LIB, 'scene_lib.jsx'), my_globals_jsx])
```
- Their motion rule: every move is TWO keys (start and end of the move) shaped in the speed graph, with named eases
  (`EASES`, out / in influence): settle 15/80 (fast start, long settle: moves that land), bell 73/73 (moves that overlap
  the next one), accel 80/15 (whips and squashes that leave on a cut), gentle 45/60. `k2(prop, t0, v0, t1, v1, style)`
  makes one move (styles also `hold` and `linear`); scene_lib's `chain(prop, [[t, v], [t, v, style], ...])` strings
  moves together, each starting and landing at zero speed on a straight path.
- How it fits our defaults: two eased keys are a clean way to build ordinary moves (push-ins, slides, type arrivals).
  Flash transitions in music edits stay per-frame recipes (transitions.md), and `popIn`'s small overshoot stays where
  our reviewers approved it; for a client who wants clean, techy motion with no bounce, build moves with `k2` "settle".
- motion_lib.jsx: `holdAt`, `eff` / `eparam` / `setE` (effects and params by name), footage with eased push-ins
  (`clipL`, `stillL`, `focusPos`), `grade`, transition set pieces (`whipOut` / `whipIn`, `lumaDissolveIn`,
  `slowShutter`, `smearOut`, `pixelReveal`, `shakeChroma`, `glitchBurst`), `printShot`, `splitShot`, a 3 x 3
  `wallShot`, `highlightRects`, a CRT switch-off (`tvOff`), `counterRow`, `capRow` captions, `freeze`, `chanOnly`,
  `rectMatte`, `faceMontage` (face-matched montage), and a documentary finish: `acGrade` (black 0.05, gamma 1.08,
  contrast 1.18, saturation -18, bloom above 0.66 with Blurriness 60 in Screen at 55%) and `acFinish` (opaque black
  base, red/cyan channel fringe, a tube vignette PNG multiplied, light soften, mono grain; set the global `VIGNETTE` to
  `assets/ae/vignette_ac.png`).
- scene_lib.jsx: SF Pro Display captions that arrive with a smooth text transition (`cap`: blur 10 -> 0, opacity
  0 -> 100, rise 12 px -> 0, two settle keys over 5 frames), `plate` and `seqL` for stills and image sequences rendered
  from a storyboard, `flash`, `fadeIn` / `fadeOut`, `hud` brackets, `box`, `typed` text, `rgbHit`, `nightGrade`,
  `paperGrade`, a `finish` comp, `camera` on a world layer, `dofBands`, `testComp` for sample renders and `ditherZone`
  (ordered dither from Bayer maps). Set the globals `PLATES` (folder of rendered plates), `VIG` (`{ac, mm, mmdark}`
  vignette PNGs from `assets/ae/`) and `BAYER` (the `assets/ae/` folder, trailing slash).
- Both ran in real builds on the Mac; `check_jsx.py` passes on a test script that loads both. Not yet run on Windows.
  Their fonts: SFProDisplay-Bold / -Medium and Didot-Bold (ship with macOS), DMSerifDisplay-Italic, JetBrainsMono-Regular.
  On Windows check those exist first: AE swaps a missing font silently.

## 14. Dynamic Link comps (from the Mac port, 13 Oct 2026)
- Premiere imports AE comps live with `proj.importAEComps(aep, [names], bin)` (through the bridge, premiere-ui.md).
  Items are named "Comp name/Project.aep": match bin items by that prefix, not the bare comp name.
- Premiere points at comp IDs, so fix comps IN PLACE: rebuilding with new comps orphans the links.
- Footage layers inside linked comps carry their audio into Premiere: `layer.audioEnabled = false` on every one.
- Premiere 26.5 colour-manages linked comps as sRGB and converts them to its Rec. 709 working space, which lifts the
  shadows: set a Rec. 709 override per item (premiere-ui.md "Dynamic Link builds"). A project with working space "None"
  gives exact colours too (mac-notes.md).
- Speed: an export with about 21 linked comps took about 100 s for 59 s of timeline.
