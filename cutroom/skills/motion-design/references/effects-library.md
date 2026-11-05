# Effects library: what each effect is, how to run it, and its taste mark

Four places hold ready-made effects:
1. `effects-library/` in this skill: 18 effects rebuilt natively from creator tutorial reels, one builder each, with a
   harness, recipes and a stock list (section 2). Run instructions: `effects-library/README.md`.
2. The music-edit kit's After Effects libraries (`fx_lib.jsx`, `edits_lib.jsx`), built and tuned on our own music edits
   (section 4). They ship in `library/pipelines/edits-kit/tools/ae/`.
3. Set pieces in premiere-ae-editing `scripts/ae/motion_lib.jsx` and `scene_lib.jsx` (section 5).
4. Helpers in premiere-ae-editing `scripts/ae/ae_lib.jsx` (section 6).

## Contents
1. Taste marks
2. The 18 library effects
3. Running them (short)
4. Our music-edit libraries
5. motion_lib.jsx and scene_lib.jsx set pieces
6. ae_lib.jsx helpers that move things
7. Techniques worth lifting from the demos
8. When the user names an effect, or asks to learn a page's effects

## 1. Taste marks
- **safe:** fits our verdicts. Still look at the rendered frames once.
- **check frames first:** part of it was rejected before (the reason is named). Render a test and check every frame
  against that verdict before using it.
- **breaks our taste, do not use unless asked:** it goes against a verdict. Only when the user or a client brief asks for
  that look, and say so.

## 2. The 18 library effects
Run status: **ready** = composes, passes our syntax check and uses native effects only (some need free stock clips or a
matte first); **needs work** = a missing plug-in, SFX or font stops the build. Nothing has been rendered on Windows yet; the
builds ran on a Mac.

| # | Key | What it does | Reach for it when | Needs | Taste mark | Status |
|---|---|---|---|---|---|---|
| 1 | pixel_reveal | a still appears as hard blocks switching on along a ragged diagonal in about 1 s | a still arriving on a clean page in a tech explainer | skater.mov | breaks our taste, do not use unless asked: a block grid is the box-glitch family the music-edit user called "PowerPoint"; in a clean tech explainer that asks for it, refit its 39-key layout pan to two eased keys | ready (stock) |
| 2 | luma_dissolve | darks appear first and highlights last, over white (the clip is its own Gradient Wipe) | a soft, organic in or out on bright footage | field_runner.mov | safe: optical, the picture's own light | ready (stock) |
| 3 | wave_blur_text_reveal | a big word resolves from hexagon bokeh along a wavy diagonal front while scaling 176 -> 100 -> 81% | title words with weight | nothing | safe (Camera Lens Blur is a heavy render) | ready |
| 4 | smooth_text_transition | words arrive with a fast start and a long creep, blur and opacity settling; two nulls overlap their eases | caption or title words in a clean style | nothing | safe: keep the hero word's glow light (threshold 75, intensity 0.5) | ready |
| 5 | glowing_gradient_stroke | a line draws on under a prompt box with a tapered glowing core and a racing colour palette | UI moments, "thinking" states, prompt boxes | Deep Glow 2 | check frames first: the radius-1000 haze is a colour wash; keep the glow small and native | needs work (paid plug-in) |
| 6 | cursor_light_trail_text_reveal | a white cursor sweeps right revealing text, with a blue light trail | typing on screens, intro cards | Deep Glow 2 | safe once the glow is native and light | needs work (paid plug-in) |
| 7 | gradient_depth_reveal | pastel colour bands flow along a depth map, then the clip reveals nearest first | dreamy openings when a depth map exists | field_runner.mov + matte | breaks our taste, do not use unless asked: about 1 s of pure colour bands is a colour flood and a long abstract hold; only with the colour phase under 10 frames | ready (stock + matte) |
| 8 | hail_mary_highlight_streak | highlights smear into long one-axis streaks with bloom (49 shifted tap layers) | hero shots with chrome, lights, reflections | rain_street.mov | check frames first: optical light (the approved family), but long one-axis smears and a lens streak that hid the moment were rejected; keep the subject readable and the comb stretch short | ready (stock) |
| 9 | slow_shutter_echo_trail | a sharp leading frame with 4-5 smeared ghosts behind (CC Force Motion Blur + Echo) | a hero move, a last shot | wall_dancer.mov + matte | safe: the ghost-trail family (our own ghost trail is not judged yet) | ready (stock + matte) |
| 10 | whip_pan_wipe | every hard cut hidden by a 10-13 frame horizontal whip, a whoosh on the cut | a run of shots of one subject (clean style) | 4 clips + 2 SFX | breaks our taste, do not use unless asked: whips with mirrored or static frames were rejected ("looks ass"); use the zoom cut | needs work (the 2 SFX files are missing) |
| 11 | mixed_media_cutout | a photocopy background at 12 fps steps, a colour cut-out subject with a white sticker rim | editorial collage moments | field_runner.mov + matte | check frames first: a white matted rim was rejected once as "a pale white wash" | ready (stock + matte) |
| 12 | pixel_dither_background | footage as a 1-bit two-colour print with 4 px dots and 12 px dither cells, a blocky wordmark | backgrounds, tech texture, a section look | clouds_a.mov + tile (included) | safe as a texture or section look; keep holds short in music edits | ready (stock) |
| 13 | one_frame_glitch_burst | a 6-frame burst at a cut: inverted smear, 2 white frames, zoom-blurred incoming frame, 2 frames of an inverted half-frame, then a scale settle | a hard drop on the music | nothing | safe: a recipe of distinct frames like our flash recipes; in music edits check the split frames against the box-glitch verdict | ready |
| 14 | shake_chroma_impact | a 12-frame shake and RGB chroma warp around a cut | an impact on a headline or a hit | nothing (2 clips when built alone) | check frames first: mirror-wrapped edges show on the peak frame; lower Shake Amp | ready |
| 15 | overlap_keyframes_20_50_graph_peak | a live diagram of the overlap rule and the speed-graph peak | teaching or checking an overlap | nothing | safe (a teaching demo; the rule is in `motion-rules.md`) | ready |
| 16 | copy_with_property_links_glow_shapes | 10 shapes whose effect stacks follow one master by expression links | one look on many layers | Deep Glow 2 | safe as a technique (use the technique, not the neon comp) | needs work (paid plug-in) |
| 17 | eg_notification_template_variations | one notification card in Essential Graphics, nested 6 times with different properties | reusable UI cards with many variations | nothing | safe as a technique: neutral icons only, never a real app's UI | ready |
| 18 | ui_accounts_card_typography | a dark finance card showing tracking, a 1.25 size ratio and weight, with focus-dim | any UI mock-up that has to look real; teaching type hierarchy | Inter fonts | safe (the rules are in `titles-captions-type.md`) | needs work (Inter not installed on the build PC) |

Totals: taste marks 11 safe (2, 3, 4, 6, 9, 12, 13, 15, 16, 17, 18), 4 check frames first (5, 8, 11, 14), 3 breaks our
taste (1, 7, 10). Run status: 13 ready (7 of them need free stock clips or mattes first), 5 need work (5, 6, 16: Deep Glow;
10: SFX; 18: Inter).

## 3. Running them (short)
- Copy the `effects-library` folder to a work folder first (the builds write the .aep, renders and test folders inside it).
- `python ae/effects_build.py test <key> --dry-run` writes and syntax-checks the build script without After Effects;
  without `--dry-run` it builds, renders `ae/_test/<key>/<key>.mp4` and a frame sheet.
- `python ae/effects_build.py master --showreel` builds all 18 into "FX Library v1.aep" with a showreel comp.
- It runs through our premiere-ae-editing runner on Windows and on a Mac, refuses while the user's After Effects has a
  project open, and always sets the sRGB working space the builds were tuned in.
- Inside a job: include `effects_lib.jsx` and the effect file in the generator's libs, or rebuild the look from its
  recipe on the job's own layers. Bring it into Premiere as an ELEMENT, never as a finished shot with presenters or logos
  baked in.
- Full steps, stock downloads, fonts, the three fixes and Mac notes: `effects-library/README.md`. Each effect's measured
  recipe: `effects-library/recipes/NN-<key>.md`.

## 4. Our music-edit libraries
Built 13-14 Oct 2026 in the music-edit kit (ES3, need ae_lib.jsx first). Taste from the reviews:

| Function | What | Taste mark |
|---|---|---|
| `frameRecipe` | the one-letter-per-frame strobe language (`cracked-edits.md` 7.6) | safe; X (black) only inside a strobe, short colour runs only |
| `lightBlowout` | hot orange, flat white 1-3 frames, golden haze | safe (kept) |
| `zoomRush` | radial streaks, over-zoomed rolled arrival | safe (kept) |
| `radialSplit` | rainbow tunnel inside the zoom rush | safe |
| `smear` | streak hold | safe only short and vertical; long sideways was rejected |
| `lightPaint` | highlights tinted on black, smeared | check frames first: only short ("TOO long") |
| `defocus` | melt into haze, arrive as colour blobs | safe ("okay") |
| `lightBurst` | ray burst | check frames first (not judged) |
| `vortex` | spin + zoom blur tunnel | check frames first (not judged; must not read as a rigid spin) |
| `colorFlood` | full colour frames in sequence | breaks our taste, do not use unless asked (floods rejected twice) |
| `aura` | energy glow around the player | breaks our taste, do not use unless asked ("do not do auras of this type") |
| `silStack` | silhouette strobe stack (F / I / K / W / P) | safe ("WFIK" kept); P frames not judged |
| `sliceOut` | light crack into flying strips | breaks our taste, do not use unless asked (rejected 14 Oct) |
| `silIris` | silhouette burst | breaks our taste, do not use unless asked (rejected 14 Oct) |
| `flashGrid` | flash panels lit frame by frame | safe (his ask; confirm the halves order) |
| `typeFlash`, `freezeClone`, `ghostTrail`, `popFreeze`, `photoPrint`, `outlineText` (numeral sandwich), `strikeWord` (hit list) | the newer devices (`cracked-edits.md` section 8) | check frames first (not judged yet) |
| `holdAt`, `delayBy`, `cutoutCopy` | freeze, delay and cut-out helpers | helpers |
| edits_lib: footage with remap, focus, band and mirror extension (audio off); punch, shake, flash, expo pop; slam word, hero text, caption; mattes, cut-outs, silhouette strobe, outlines | the proven base | safe (one thin rim at most) |
| edits_lib: `colorPop` | B&W world, colour cut-out | safe on shots with visible background |
| edits_lib: `zoomCut`, `invertFlicker`, `colorFlash`, `rgbSplit`, `posterizeSpan` | kept transitions and looks | safe |
| edits_lib: `whip`, `spinCut`, `shutterCut`, `glitchCut`, `battery`, `reticle` | rejected devices kept for the record | breaks our taste, do not use unless asked |
| edits_lib: `breath` (a black solid between two times), `popIn` (the cut-out pop: white rim plus a dimmed background) | the black breath frame and the pop that read as a pale white wash | breaks our taste, do not use unless asked. edits_lib's `popIn` also replaces ae_lib's `popIn` (same name, a different device) in any build that loads edits_lib |

## 5. motion_lib.jsx and scene_lib.jsx set pieces
Written for short documentary reels and a storyboard build in the clean style; in premiere-ae-editing `scripts/ae/`.

| Helper | What | Taste mark |
|---|---|---|
| `k2`, `chain`, `EASES`, `setEase`, `holdAt` | two-key moves with named eases | safe (the core) |
| `clipL`, `stillL`, `focusPos` | footage and stills with eased push-ins around a focus point | safe |
| `lumaDissolveIn` | library #2 as a helper | safe |
| `slowShutter` | library #9 as a helper | safe |
| `printShot` | a photo print over a huge glowing word | safe |
| `splitShot` | two clips side by side, each the middle half of its frame | safe |
| `wallShot` | a 3 x 3 video wall, one tile blows out, slow push | safe (clean and doc looks) |
| `highlightRects` | highlighter rects parented to a moving still, staggered | safe |
| `tvOff` | CRT switch-off as three two-key moves | safe |
| `faceMontage` | face-matched montage pushed by one null | safe |
| `counterRow`, `capRow` | clean-style counters and caption rows | safe (check the fonts exist on Windows) |
| `acGrade`, `acFinish` | the analog night finish (`native-looks.md` section 1) | safe for documentary looks |
| `glitchBurst` | library #13 as a helper | safe; check split frames in music edits |
| `shakeChroma` | a three-channel snap with a decaying shake | check frames first |
| `smearOut` | the last frames of a shot streak sideways and burn | check frames first (keep it short) |
| `pixelReveal` | library #1 as a helper | breaks our taste in music edits, do not use unless asked |
| `whipOut`, `whipIn` | library #10 as helpers | breaks our taste, do not use unless asked (unless a frame check shows no mirrored or static frame) |
| scene_lib `cap` | smooth text captions (blur 10 -> 0, rise 12 px, 5 frames) | safe; it uses SF Pro: swap to Inter for client work |
| scene_lib `flash`, `fadeIn`, `fadeOut`, `box`, `typed`, `rgbHit` | small motion pieces | safe |
| scene_lib `hud` | corner brackets closing onto a box with a tag | check frames first: a HUD over a film scene passed in clean reels, but a reticle was rejected in music edits |
| scene_lib `nightGrade`, `paperGrade`, `finish`, `camera`, `dofBands`, `ditherZone`, `testComp`, `plate`, `seqL` | grades, finish, camera, depth bands, dither, test and plate helpers | safe |

## 6. ae_lib.jsx helpers that move things
- `keys(prop, [[t, v, easeIn, easeOut], ...])`: influence 33 = gentle, 75-90 = strong. Safe.
- `popIn(l, t, over)`: scales past the target, then settles; default `over` 1.1. Check frames first: pass 1.04-1.06 for
  cards in ads, never overshoot in clean or premium briefs (`motion-rules.md` section 5).
- `flyIn`, `slowPush` (4% over a shot), `typeOn` (Source Text substring, about 18 characters a second), `drawPath` (Trim
  Paths draw-on), `outlineBox`, `imgCard` + `highlighter` (OCR rects map straight onto the card), `stillBg` (blurred dim
  background with a slow push), `softEllipse` and `softBand` (glows and shadows with no box edge). Safe.

## 7. Techniques worth lifting from the demos
- **Property links by script (#16):** one master effect stack; every settable property on the copies is an expression link
  to the master (exactly what Copy With Property Links writes). One edit restyles every layer: useful for flash-panel
  styles or any repeated look.
- **Essential Graphics by script (#17):** expose Source Text and a Dropdown Menu Control (which time-remaps an icon comp),
  nest the template, and set each copy through its Essential Properties with hold keys, instead of duplicating comps.
- **Typography (#18):** the 1.25 size ratio, tracking by size, lighter weights for small text, focus-dim to 38% over
  10-frame Easy Ease pairs.
- **The 20-50 diagram (#15):** a live check that a second layer's speed peak sits on the first layer's last key.

## 8. When the user names an effect, or asks to learn a page's effects
- A named effect from a tutorial or creator ("use the effects you learned"): look for it here and in its recipe before
  inventing one.
- "Learn the effects" from a page: count the headline effects first (one or two per post), tell the user the count and the
  list, and ask before adding the creator's other editing devices. Why: 108 "effects" counted on a page of about 30
  tutorials was over-scoped.
- A creator's look: take the measured spec (editing-playbook's reference looks and study method) plus its native build
  (`native-looks.md`).
