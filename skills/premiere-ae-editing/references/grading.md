# Colour: Lumetri mechanics, log footage, matching by numbers

What a good grade looks like, the targets for backlit log talking heads and the reviewers' verdicts: editing-playbook
`references/grade-taste.md`. This file is how to build, measure and check a grade with these tools. The user may be
new to grading (the editor this was built with was): give numbers, "stop when" targets and a reality test, not theory.

## Contents
1. How grades are built
2. Log footage and mixed sources
3. Measure before you touch
4. Calibrating a colour model from a reference render
5. Numbers that worked
6. A colour pass over a multi-ad project
7. Dimmers, spotlights and vignettes
8. Presenters and cut-outs in a plate
9. Graded stills from log footage
10. Bulk graded clips from log footage
11. Readability of graphics after grading
12. Music edits and grades set from After Effects scripts

## 1. How grades are built
- Lumetri on ADJUSTMENT LAYERS above the footage, one look per location, cut around B-roll (B-roll gets its own clip
  Lumetri). The reference sequence's grade was cloned into every ad with per-look slider overrides
  (`clone_component(doc, lumetri_id, {index: value})`, indexes in prproj-format.md section 7). Track stack, B-roll
  edges and what to extend when B-roll is removed: prproj-recipes R19.
- Read the project's live values, never a notes document: a grading doc said Temperature -4, Tint -3, Exposure -0.2,
  Blacks -6.9; the approved project held +5, -15, +1.0 and -25.9. `prproj_dump.py` shows them.
- A face light is a second Lumetri with a static feathered ellipse mask (Feather 138, Exposure +0.5), only where it is
  needed, built per shot and never pasted from another shot.
- Verify on REAL Premiere frames (Export Frame or an export), side by side with the reference, before calling it done.

## 2. Log footage and mixed sources
- Log camera footage (Sony, behaves like S-Log3 / S-Gamut3.Cine) can arrive labelled Rec.709 (a 6K camera re-encoded to
  H.264 8-bit 4:2:0 was): check the picture, not the tag. Copy the user's colour-space override from one clip onto
  every clip from that camera (`OverriddenColorSpace` in the VideoStream, prproj-format.md section 5). Unify variants:
  inside one ad two clips carried different Sony options and one had none. The value that behaved like S-Log3 /
  S-Gamut3.Cine there: "1012,1001,1,Narrow,YCC,8-bit,Scene-Referred".
- Re-cleaned audio versions of a clip ("VERSION 2" files) come in WITHOUT the override: put it back, and verify against
  the user's own renders made BEFORE the source swap, at the same timestamp (a face's mean RGB 155.9 / 120.1 / 107.4
  against 160.8 / 124.1 / 107.8 = within compression).
- B-roll from the same camera gets the same override plus a clip-level copy of the master Lumetri; brightness checks
  showed no per-shot tweaks were needed.
- Rec.709 stock and YouTube archive under a log house grade: no override. Clone the master Lumetri but zero its
  log-specific basics (15 Tint, 19 Exposure, 20 Contrast, 21 Highlights, 22 Shadows, 23 Whites, 24 Blacks, 41 Sharpen,
  42 Vibrance) and keep its curves, wheels and vignette for the house feel; then per clip Temperature 0 to +6,
  Saturation 85-95, Exposure -0.3 to +0.35; old SD archive also Sharpen 20 and Exposure +0.3 to +0.35. Later
  replacements used lighter presets: stock Temperature +4 (the rest neutral), archive Temperature 3 / Saturation 96 /
  Contrast 8 / Sharpen 16, modern stock Temperature 2 / Saturation 100. Why: the master grade is tuned for log and burns
  Rec.709 footage.

## 3. Measure before you touch
- Targets (face lit and shade sides, skin hue, vectorscope angle, darkest detail, neutral checks) and the fixes that go
  with them (green Tint for pink, Exposure in 0.1 steps, the eyedropper only on true white): grade-taste section 3.
- A frame meter for those targets: level percentiles, clipping, per-box luma, HSV hue and vectorscope angle per box, a
  grid to place the boxes, and a preview of white-balance / exposure / blacks moves before touching Lumetri. One was
  written with the client's grading notes and ships in the kit library (not in this skill):
  `python analyze_frame.py f.png --grid` / `--box name x0 y0 x1 y1 --exclude ...` in
  `~/VisionKit/kit/library/pipelines/ad-build-kit/` (Pillow and numpy; runs on a Mac as is). Exclude the caption band
  and graphics: captions read 100 on the waveform.
- "She looks pinkish": measure the median CIELAB of warm skin pixels (R > G + 6, G > B + 4, R - B > 28, 95 < R < 250) in
  a face box on exported frames, early against late (that job's `skin_measure.py` is in
  `~/VisionKit/kit/library/pipelines/ad-build-kit/work/`). Once the daylight had changed from 35 s on (flatter,
  pink-lavender shadows), not the grade: only the talking-head pieces after 35 s got Exposure 0.62, Temperature +6,
  Tint -18, Contrast 26, and the frame at 36 s then read L 51.5, a* 11.0, b* 17.2 against L 48.2, a* 12.45, b* 15.9
  early on. No further complaint.
- "Whitewashed" = lifted blacks and low contrast: read the darkest percentile (1st-percentile luma) before and after.
  Fixes that passed: a product shot Exposure 0.45, Contrast 32, Shadows 6, Whites -12, Blacks -42, Saturation 112; a
  packing shot Exposure 0.55, Contrast 30, Shadows 4, Whites -10, Blacks -48, Saturation 110, Vibrance 15 (p1 luma
  0.19 -> 0.09); a sofa A-roll Contrast 14, Shadows 15, Blacks -36, Saturation 105, Vibrance 15 (from 8 / 22.7 / -25.9 /
  100 / 13.2; p1 0.15 -> 0.12).
- Measure blacks and saturation on frames before and after every pass.

## 4. Calibrating a colour model from a reference render
Claude cannot watch Premiere's playback, so fit the reference look and predict every piece before touching Premiere:
1. Grab raw log frames and the reference render at the same moments.
2. Align them by normalised cross-correlation of gradient images, searching scale 1.00-1.62 (step 0.01), offsets of
   16 px and "pad vs stretch" decode geometry; exclude the caption band (y 860-1080 on 1080x1920), the face-light
   ellipse and textured blocks.
3. Sample 12 x 12 px block means into colour pairs.
4. Fit an S-Log3 decode, the S-Gamut3.Cine to Rec.709 matrix, white-balance gains, a monotone piecewise-linear tone
   curve in log2, a 3 x 3 post matrix and a saturation-versus-luma curve.
- One fit: about 50,000 pairs, held-out RMS about 4.8 / 255, white-balance gains [0.98, 1, 0.87]; one Lumetri Exposure
  unit moved the model by about 0.65 stops. It predicted two locations as fine with a straight clone and the third as
  "too bright, a bit cyan, and flat".
- Report the model's warnings even after an approval: the user said "grades are perfect", and a day later the boss
  called that third location "whitewashed". The fitted model is per job; keep it with the job, not in the skill. That
  job's fitting code ships as reference code (`model.py`, `align.py`, `run_align.py`, `sample_pairs.py`,
  `calib_grab.py`, `vgrab.py` in `~/VisionKit/kit/library/pipelines/ad-build-kit/work/`); its fitted model files are
  gone, so re-fit per job.

## 5. Numbers that worked (vertical talking-head ads on log footage; starting points, not laws)
- Reference main grade: Temp +5, Tint -15, Exposure +1.0 (later +0.7), Contrast 8, Highlights -21.9, Shadows 22.7,
  Whites -5, Blacks -25.9, Sharpen 13, Vibrance 13.2, Vignette -0.28, gentle S curve, warm highlight wheel.
- Washed-out locations (second round): river Temp 3, Exposure 0.9, Contrast 22, Shadows 14, Blacks -38, Saturation 108,
  Vibrance 16; park Temp 4, Contrast 16, Shadows 18, Blacks -32, Saturation 104, Vibrance 15.
- Final note "more contrast, shadows down, highlights up a tad, pinch of saturation" became per location:
  sofa con +16 hil +14 sha -14 blk -8 sat +3 vib +6; park con +18 hil +12 sha -14 blk -12 sat +3 vib +6 tint +6;
  river hil +4 sha -20 blk -30 sat +5 vib +6 tint +6 temp +2.
- Lessons: saturation +6 turned skin orange: use Vibrance for pop. Riverside "washed out" = a lifted black point (blacks
  17-28 % grey against 11-15 % on the good set, saturation about 30% lower): Blacks and Shadows need big moves.

## 6. A colour pass over a multi-ad project
- Inventory every Lumetri on every item with its sliders first (one project: 134 instances, 96 edited in 2 passes).
- Change only the grade adjustment layers and the camera's own B-roll; skip muted items, keyframed Lumetris (a tracked
  spotlight), face lights (exposure only), archive and stock. Guard so a Lumetri shared by two looks never gets the
  change twice.
- Build on the user's latest save as a new version; verify with Export Frame against the previous renders (that pass:
  p1 luma sofa 0.06-0.08 -> 0.04-0.05, river 0.18 -> 0.12-0.13, park 0.09-0.10 -> 0.05-0.06) and one before / after
  sheet.

## 7. Dimmers, spotlights and vignettes
- A Lumetri used as a dimmer (spotlight, vignette) is cloned from a NEUTRAL Lumetri (exposure only, no LUT, flat
  curves), never from the master grade: a clone of the grade applies the look a second time. Check the template has no
  LUT before cloning it. The spotlight build: prproj-recipes R22.
- Vignettes on vertical crops of wide sources: set Amount to -3 for a moment; if only the top and bottom darken, the
  vignette is drawn on the wide source and cropped away. Set it to 0 and put the vignette on an adjustment layer
  (normal amount -0.3). Why: a clip vignette on a 6K source never reaches the 9:16 corners.

## 8. Presenters and cut-outs in a plate
- Keyed presenter into a plate (a green-screen essay job): derive per shot from measurements, never copy the user's
  trial numbers: Temperature = 230 x (plate warmth - presenter warmth), +40 under firelight; Saturation = 90 - 0.27 |T|
  (63..100); Exposure = 0.45 x mid-tone gap in stops (clamp -2..+0.3, about -1.6 on very dark plates); Contrast -20;
  Blacks -30 on night plates. One grade per plate file. Finish: a small blur when the presenter is far, a light-spill
  copy (17-35 % opacity, masked, hot tinted Lumetri), a top adjustment layer with Noise 5 + contrast +18 for shared
  grain.
- Match one presenter still to the approved ones by numbers: stats on opaque pixels only (cut-out alpha above 250), on
  the whole figure and on a face band (12-36% of the height): linear luminance mean, L* spread (contrast), chroma, mean
  a* and b*. Target = the mean of 3 reference poses; render about 6 Lumetri candidates and keep the closest. Values that
  passed: Temp 8, Tint 10, Saturation 140, Exposure -0.05, Contrast 12, Whites -10; a later still set was already close,
  so the move was halved (Temp 4, Saturation 115, Exposure +0.08). Pitfall: PIL dropped the render's alpha, the black
  background entered the averages and every candidate read darker: always mask the stats with the cut-out's own alpha.
- A cut-out still in a warm room plate (After Effects values: Levels, Tint, lens blur, grain): motion-design
  `depth-2.5d-3d.md` section 3; the rig mechanics: after-effects.md section 8.

## 9. Graded stills from log footage (website / thumbnail photos)
Fastest way to get a full-resolution still with EXACTLY the approved video look (no rebuilding the grade): take one
frame of the same camera + location from a finished render, line it up with the log source frame it came from (the
item's src time and Motion scale / position from the project), fit a degree-4 polynomial mapping log RGB to rendered RGB
(robust refit that drops pixels under captions / graphics), apply it to the full-res source frame you want, crop, light
unsharp mask, export JPG q95 + PNG. Decode both with the BT.709 matrix (PyAV reformat src_colorspace ITU709, limited to
full range; the ffmpeg flags for the same decode and for tagging an encode are in media-toolkit.md section 7). Check:
model vs render difference image should be black except burned-in text (about 2/255 RMS).
A punchy video grade can read "too orange" on a still (feedback 7 Oct 2026). Measure skin / foliage saturation on
patches; calm it with luma-preserving saturation x0.8 overall and about x0.62 on orange-yellow hues, a slightly cooler
white balance, blacks lifted a little; protect the product with a feathered mask so brand colours stay true. Shadow
skin went from 0.65 to 0.45 saturation in that fix. That job's scripts (`grade_still.py`, `calm_v2.py`, and the frame
pickers `score.py`, `cands.py`, `faces.py`) ship as reference code in
`~/VisionKit/kit/library/pipelines/ad-build-kit/webstill/`.

## 10. Bulk graded clips from log footage (B-roll packs for social / ads)
When someone needs a set of clean graded clips (not the edit), skip Premiere: `scripts/media/slog3_grade.py` turns Sony
S-Log3 / S-Gamut3.Cine into a natural Rec.709 look (S-Log3 decode, gamut matrix, soft filmic curve, gentle saturation),
adds per-clip auto levels (black point, white stretch, mid-tone protection), and bakes it into one .cube per clip for
ffmpeg `lut3d`: 4K landscape and vertical 1080x1920 crops in minutes. "Don't burn the grade, just make it look okay" =
this natural look, not the punchy ad grade. QC with a contact sheet per folder (also handy for the person receiving the
clips) and check vertical crops at the first, middle and last frame: subjects move, a mid-frame check alone missed two
faces going out of frame. Drop the vertical version when the action crosses the frame.

## 11. Readability of graphics after grading
Mock every title / card on GRADED frames from each location (bright sky, dark sofa, white board), with the real caption
at its real place, and check contrast. Composite the mocks in linear light, the way Premiere blends graphics
(prproj-format.md section 9), or a mock looks more solid than the export.

## 12. Music edits and grades set from After Effects scripts
- The music-edit house look (Lumetri, vignette, grain, bloom, a black-and-white chapter with 12 fps Posterize Time):
  grade-taste section 7 and motion-design `cracked-edits.md`. Grade and vignette sit BELOW the transitions
  (transitions.md).
- From an After Effects script, Lumetri saturation runs 0-300 with 100 = normal (a "-8" meant as a slight
  desaturation was refused as out of range and skipped): after-effects.md trap 47.
- A soft whole-picture bloom turns broadcast pitches neon: threshold 85+, intensity 0.2 or less.
