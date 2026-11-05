# Effects library (18 native After Effects effects)

18 effects rebuilt from creator tutorial reels with native After Effects effects only (plus three that called a paid
glow), one builder per effect. Each builder makes its own comps and returns a main comp, so it can be built alone, all
together into one library project, or lifted into a job. Every effect carries a taste mark from our users' verdicts:
read it before using the effect. Why each mark: `../references/effects-library.md`.

Taste marks: **safe** = fits our verdicts (still look at the frames once); **check frames first** = part of it was
rejected before, test and check every frame against that verdict; **breaks our taste, do not use unless asked** = goes
against a verdict, only when the user or a client brief asks for that look.

## Folder
- `ae/effects/<key>.jsx`: one `build_<key>()` per effect (ES3 ExtendScript).
- `ae/lib/effects_lib.jsx`: shared helpers on top of the premiere-ae-editing `ae_lib.jsx` (folders, stock import,
  source comps, sliders, `fxp` effect setter, frame keys `kf`, `hex`, comp notes) and the `FONTS` table.
- `ae/lib/master_tail.jsx`, `ae/lib/showreel.jsx`: tidy-up and the "00 Showreel" comp for the full library build.
- `ae/effects_build.py`: the harness (test one effect with a frame sheet, build the whole library, an After Effects lock
  so several callers queue instead of colliding).
- `ae/_tools/wins.swift`: macOS only, optional; used only with the friend-style Mac runner to spot After Effects dialogs.
- `recipes/NN-<key>.md`: the measured recipe behind each builder (what it looks like, layer stack, every value, what the
  reel did not show).
- `stock/README.md`: the clips, mattes and SFX the builders expect; `stock/pixel_dither_tile_12px.png` (included).

## Before you build (both machines)
1. **Copy this folder to a work folder** outside the skills folder (for example `D:\work\fx-library` or
   `~/Work/fx-library`). The harness writes `ae/_test/`, `ae/_master/`, `ae/_lock`, `ae/_queue`, `renders/` and
   `FX Library vN.aep` inside it, and the renders are large.
2. **The premiere-ae-editing skill** must be installed: the harness imports its `ae_build.py`, `ae_run.py` and
   `check_jsx.py`, and every build includes its `ae_lib.jsx`. Default folder `~/.claude/skills/premiere-ae-editing/
   scripts/ae`. If the skill lives elsewhere, set `AE_SCRIPTS` to its `scripts/ae` folder, or set `PAE_SCRIPTS` to its
   `scripts` folder (the variable the kit library's pipelines read; the harness then uses `<PAE_SCRIPTS>/ae`).
3. **Python 3** with `esprima` (syntax checks; `master` needs it), `av` (PyAV) and `Pillow` (the frame sheet). Ask the
   user before installing anything.
4. **Stock:** the clips in `stock/README.md` (free Pexels licence, ids given) go into `stock/` under the listed names, after
   the user's go-ahead (say file, source and size). Two person mattes come from any roto or segmentation tool. Effect #10
   also needs two SFX files from the user's licensed library.
5. **Fonts:** the builders default to SF Pro Display Regular / Medium / Bold and Georgia Bold; #18 uses Inter. SF Pro's
   licence is written for designing Apple-platform interfaces, so for client work switch the roles to Inter (free, SIL
   Open Font Licence) with `FX_FONTS` (below). A missing font renders in a substitute; a missing glyph renders blank.
6. **After Effects 2026:** closed on Windows; on a Mac either closed or open with only an empty untitled project. Never
   build into a project of the user's, never kill the user's After Effects. Scripting must be allowed (Scripting &
   Expressions > "Allow Scripts to Write Files and Access Network"): the user ticks it himself, it is a security setting.

## Commands
Windows (PowerShell; in cmd use `set NAME=value`):
```
$env:AE_SCRIPTS = "$HOME\.claude\skills\premiere-ae-editing\scripts\ae"     # only if not the default (or set PAE_SCRIPTS)
$env:FX_FONTS = '{"regular": "Inter-Regular", "medium": "Inter-Medium", "bold": "Inter-Bold"}'   # client work
python ae\effects_build.py status                          # which runner, who holds the AE lock
python ae\effects_build.py test luma_dissolve --dry-run    # writes + syntax-checks the .jsx, no After Effects
python ae\effects_build.py test luma_dissolve              # builds, renders, writes the frame sheet
python ae\effects_build.py test luma_dissolve --times 0.5,1,2.5
python ae\effects_build.py master --showreel               # all 18 into "FX Library v1.aep" + renders\v1\
python ae\effects_build.py master --keys luma_dissolve,smooth_text_transition --version v2
```
Mac (zsh, from a venv with esprima, av and Pillow):
```
export AE_SCRIPTS=~/.claude/skills/premiere-ae-editing/scripts/ae     # only if not the default (or set PAE_SCRIPTS)
export FX_FONTS='{"regular": "Inter-Regular", "medium": "Inter-Medium", "bold": "Inter-Bold"}'
python3 ae/effects_build.py status
python3 ae/effects_build.py test luma_dissolve --dry-run
python3 ae/effects_build.py test luma_dissolve
python3 ae/effects_build.py master --showreel
```
What the runner does:
- **Windows (our ae_run.py):** refuses while any After Effects runs (ask the user to save and close it), launches it with
  `AfterFX.com -r`, waits for the build's DONE flag and for every output to stop growing, then After Effects quits. A
  dialog stops the run: ask the user to look at After Effects.
- **Mac (our ae_run.py, its mac_main branch):** probes After Effects first and refuses when a project is open (saved,
  unsaved or with any items); reuses an After Effects that has only an empty untitled project (it stays open); otherwise
  launches it hidden (`open -g`), runs the script by osascript DoScript and quits only the instance it launched. A modal
  dialog makes DoScript return without the DONE flag: the run stops with a message.
- **Mac (the friend-style runner, optional):** an `ae_run.py` with `ae_app`, `ae_pids`, `probe` and `do_script` keeps After
  Effects open between tests and can dismiss known build dialogs: compile `swiftc -O ae/_tools/wins.swift -o
  ae/_tools/wins`, set `FX_OCR` to a Vision OCR helper, and the user grants System Events Accessibility (never a script).
- Every build sets the sRGB IEC61966-2.1 working space the effects were tuned in (After Effects 2026 starts new projects
  in Rec.709 Gamma 2.4, which shifts sRGB PNG colours and the dither tile's thresholds).
- Real runs take minutes (from Claude's Bash tool use a 600000 ms timeout). Outputs: `ae/_test/<key>/<key>.mp4` (H.264
  preview), `ae/_test/<key>/sheet.png` (its top row says MISSING: the reels' reference frames are not shipped) and
  `ae/_test/<key>/<key>_test.aep` (open a COPY if you need to inspect it).

## The 18 effects: taste mark and what each needs
Run any of them with `test <key>` as above (Windows `python ae\effects_build.py test <key>`, Mac `python3
ae/effects_build.py test <key>`). Status: ready = composes and passes the syntax check; needs work = a missing
plug-in, SFX or font stops the build.

| # | key | What it does | Taste mark | Needs before it builds | Status |
|---|---|---|---|---|---|
| 1 | pixel_reveal | a still appears as hard blocks switching on along a ragged diagonal in ~1 s | breaks our taste, do not use unless asked (box-glitch family, "PowerPoint" in music edits; a clean tech explainer that asks for it: refit its 39-key pan to two eased keys) | skater.mov | ready (stock) |
| 2 | luma_dissolve | darks appear first, highlights last, over white | safe | field_runner.mov | ready (stock) |
| 3 | wave_blur_text_reveal | a big word resolves from hexagon bokeh along a wavy front while scaling 176 -> 100 -> 81% | safe (Camera Lens Blur: slow render) | nothing | ready |
| 4 | smooth_text_transition | words arrive fast and creep, blur and opacity settle; two nulls overlap their eases | safe (keep the hero glow light: threshold 75, intensity 0.5) | nothing | ready |
| 5 | glowing_gradient_stroke | a line draws on under a prompt box with a tapered glowing core and a racing palette | check frames first (the radius-1000 haze is a colour wash) | Deep Glow 2, or the native swap below | needs work |
| 6 | cursor_light_trail_text_reveal | a white cursor sweeps right revealing text, a blue light trail | safe once the glow is native and light | Deep Glow 2, or the native swap below | needs work |
| 7 | gradient_depth_reveal | pastel colour bands flow along a depth map, then the clip reveals nearest first | breaks our taste, do not use unless asked (about 1 s of colour bands = a flood and a long abstract hold; only with the colour phase under 10 frames) | field_runner.mov + field_runner_matte.mov | ready (stock + matte) |
| 8 | hail_mary_highlight_streak | highlights smear into long one-axis streaks with bloom (49 tap layers) | check frames first (long smears and a lens streak that hid the moment were rejected; keep the subject readable) | rain_street.mov | ready (stock); slow render |
| 9 | slow_shutter_echo_trail | a sharp leading frame with 4-5 smeared ghosts behind | safe | wall_dancer.mov + wall_dancer_matte.mov | ready (stock + matte) |
| 10 | whip_pan_wipe | every hard cut hidden by a 10-13 frame horizontal whip, a whoosh on the cut | breaks our taste, do not use unless asked (whips with mirrored or static frames: "looks ass"; use the zoom cut) | jogger.mov, taxi_interior.mov, skater.mov, rain_street.mov + 2 SFX | needs work (SFX) |
| 11 | mixed_media_cutout | photocopy background at 12 fps steps, a colour cut-out subject with a white rim | check frames first (a white matted rim read as "a pale white wash") | field_runner.mov + matte | ready (stock + matte) |
| 12 | pixel_dither_background | footage as a 1-bit two-colour print, 4 px dots, 12 px dither cells | safe as a texture or section look (short holds in music edits) | clouds_a.mov + the tile (included) | ready (stock) |
| 13 | one_frame_glitch_burst | a 6-frame burst at a cut: inverted smear, 2 white frames, zoom blur, inverted half-frame | safe (in music edits check the split frames against the box-glitch verdict) | nothing | ready |
| 14 | shake_chroma_impact | a 12-frame shake and RGB chroma warp around a cut | check frames first (mirror-wrapped edges on the peak frame; lower Shake Amp) | nothing in the master build; rain_street.mov + clouds_a.mov when built alone | ready |
| 15 | overlap_keyframes_20_50_graph_peak | a live diagram of the overlap rule and the speed-graph peak | safe (teaching demo) | nothing | ready |
| 16 | copy_with_property_links_glow_shapes | 10 shapes whose effect stacks are expression links to one master | safe as a technique | Deep Glow 2, or the native swap below | needs work |
| 17 | eg_notification_template_variations | one notification card in Essential Graphics, nested 6 times | safe as a technique (neutral icons only, never a real app's UI) | nothing | ready |
| 18 | ui_accounts_card_typography | a finance card showing tracking, a 1.25 size ratio and weight, with focus-dim | safe (teaching demo) | Inter Regular / Medium / SemiBold / Light / Bold installed, or `FX_FONTS` for the ui roles | needs work (font) |

Totals: 11 safe, 4 check frames first, 3 break our taste. 13 ready (7 of them need free stock clips or mattes first, #14
too when built alone), 5 need work. On a Mac with SF Pro and Inter installed, #18 is ready; the Deep Glow three need the
paid plug-in or the swap on both machines.

## Fixes for the five that need work
- **Deep Glow 2 (#5, #6, #16):** a paid plug-in, not installed on the Windows build PC, and the source's own reviewer banned
  it on client reels ("washed pastel colours to white"). Swap the `fxp(..., "PEDG2", ...)` calls for native Glow
  (`ADBE Glo2`) with the recipe's fallback values, then `effects_build.py test <key>`:
  - #5: two Glows on Shape Layer 2, radius 60 / intensity 2 and radius 600 / intensity 1, Screen, based on alpha.
  - #6: two Glows on the trail and on the cursor, threshold 50%, radius 40 / intensity 1.0 and radius 250 / intensity
    0.6, Screen, composite original on top.
  - #16: one Glow, threshold 55%, radius 120, intensity 1.2, Screen; point the read-out expression and the demo keys at
    Glow Intensity instead of Deep Glow Exposure.
- **#10:** add the two SFX files (`stock/README.md`: a mid whoosh peaking about 0.2 s in, a low boom peaking about
  0.233 s in) or delete the `sfx(...)` lines. It breaks our taste anyway.
- **#18:** install Inter (free), or set `FX_FONTS` for the ui roles.

## Using an effect inside a job
Include `effects_lib.jsx` and the effect file in `libs` of the premiere-ae-editing `write_jsx`, add
`var STOCK = "<folder>/"; var ROOTF = null; var EFFECT_FOLDER = null; var FONT_OVERRIDES = {};` as a first library, and
call `build_<key>()` from a spec; or rebuild the look from its recipe on the job's own layers. Each effect's SOURCE comp
holds one stock clip: swap the footage inside it (Alt-drag replace) to reuse the effect on your own shot. Bring the result
into Premiere as an ELEMENT (an alpha overlay or a moving plate), never as a finished shot with presenters or logos baked
in.

Fonts on a machine without SF Pro (or for client work):
```
FX_FONTS={"regular": "Inter-Regular", "medium": "Inter-Medium", "bold": "Inter-Bold"}
```
Roles: regular, medium, bold, serifBold (Georgia Bold), uiRegular, uiMedium, uiSemiBold, uiLight, uiBold (Inter).

## What changed from the source
- Neutral names: the harness is `effects_build.py`, the shared library `effects_lib.jsx`, the project root folder
  "FX Library (scripted build)", placeholder words "TITLE".
- Fonts come from one table (`FONTS` in effects_lib.jsx) instead of 33 literal font names, overridable with `FX_FONTS`.
- Placeholder app icons that copied real brands' colours now use neutral colours (same shapes); recipes 17 and 18 now
  describe the reels' real app and brand names with neutral ones.
- The harness runs through our runner on Windows and on a Mac (its mac_main branch), keeps the friend-style Mac runner as
  an option, has `--dry-run`, fixes a Windows bug (the old process check sent Ctrl+C instead of testing the process),
  uses the Python that runs it, and always passes the sRGB working space to `write_jsx` (with our current `ae_build.py` the
  default 'auto' would have left Windows builds in Rec.709 Gamma 2.4).
- Builders, values and timings are otherwise unchanged.

## Checked (14 Oct 2026, no After Effects run)
- Our `check_jsx.py` on all 21 shipped .jsx files (18 builders, effects_lib, master_tail, showreel): 21 ok, no syntax
  errors, no ES3 warnings.
- `effects_build.py test <key> --dry-run` for all 18 effects and `master --showreel --dry-run`, composed with the staged
  premiere-ae-editing scripts on copies: every script ok (18 test scripts, master 20 specs); the sRGB working space lands in
  each generated script.
- `python -m py_compile ae/effects_build.py`: ok.
- QA pass: with `AE_SCRIPTS` unset and only `PAE_SCRIPTS` set, `test one_frame_glitch_burst --dry-run` on a scratch copy
  wrote and checked its script (ok, sRGB working space in it, After Effects not started).
- Not checked: anything at render time, and the Mac branch of the harness (only its logic was read).

## Other notes
- Colour: the dither tile's greys are thresholds, so a colour-managed shift would change the pattern: keep the sRGB
  working space.
- Pixel Reveal pans its layout with 39 per-frame keys, against the two-keys-per-move rule: refit it to two eased keys if
  it gets used.
- Hail Mary is 49 tap layers and Wave Blur uses Camera Lens Blur: slow renders; test with a short work area first.
- Effect file comments must never start with `//@` (ExtendScript reads it as a directive and a syntax dialog blocks After
  Effects); the harness refuses such files. Effect file headers use `// meta key:` lines.
- Recipes keep the tutorial reel ids so the source can be found again; the tutorial brand's own word and slogan in
  those reels are replaced by the builders' placeholders ("TITLE", "Go with the flow.").

Source: adapted from a friend's Mac skill set (Oct 2026)
