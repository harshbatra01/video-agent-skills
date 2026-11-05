# Grade taste

What a good grade looks like for our clients, the verdicts behind it, and how to judge colour when you cannot watch the
playback. Lumetri mechanics, log overrides, slider indexes, graded stills and bulk clip grading live in
premiere-ae-editing references/grading.md.

## Contents
1. Verdicts on colour
2. Measure before you touch
3. What good looks like, in numbers (backlit log talking heads)
4. Mixed sources under one look
5. Scope of a colour pass
6. Presenters, stills and composites
7. Music edits: a light house look and colour as structure
8. Reference looks and brand colours

## 1. Verdicts on colour
- Approved: the reference sequence's grade cloned exactly onto every ad of that location ("grades are perfect"); the
  final pass "more contrast get the shadows down and highlight up a tad more then a pinch of saturation", applied per
  location.
- "whitewashed" (the reviewer, on riverside ads and later single B-roll shots) = a lifted black point and low contrast:
  riverside blacks sat at 17 to 28% grey against 11 to 15% on the good set, saturation about 30% lower. Fix with big
  Blacks and Shadows moves plus Contrast, then check the darkest percentile (one shot went from 0.19 to 0.09 at the 1st
  percentile).
- "she looks BURNT too orange like a chicken nugget": a Saturation push turned skin orange. Use Vibrance for pop, not
  Saturation.
- "tooooo orange / breaking bad ish" on a website still made from the video look: a punchy video grade reads too warm
  on a still; calm skin and orange-yellow hues and protect the product's colours.
- "dont burn the colour grade please just make it look okay" for a pack of graded B-roll clips = a natural Rec.709 look,
  not the punchy ad grade.
- "make it look as it was" after re-cleaned audio versions of two clips broke the grade: the new files came in without
  the camera's log override.
- Music edits: a soft whole-picture bloom turned a football pitch neon until its threshold went up ("the greens are
  back to natural" was Claude's own check); colour floods were disliked twice.

## 2. Measure before you touch
- The editor is new to grading: give numbers, "stop when" targets and a reality test, not theory.
- When someone says "she looks pinkish", measure first (median skin colour in a face box on exported frames, early vs
  late). Once it was the daylight changing after 35 s, not the grade: only the pieces after that point got a change, and
  the complaint stopped. Why: "please confirm you're doing it right" is answered by numbers.
- Predict before you build: a colour model fitted from the reference render can show which pieces will need their own
  tweaks before anything is touched in Premiere.
- Report model warnings even after an approval: the model said the riverside ads would come out "too bright, a bit cyan,
  and flat"; the editor approved them, and the reviewer later called them whitewashed.
- Verify on REAL Premiere frames (Export Frame or an export) side by side with the reference before calling it done.
  Verify a restored look against the editor's own renders from before the change (face mean RGB within compression).
- When a grading notes document and the project disagree, the project's live values win (read them from the project
  dump): the notes said Temperature -4 and Exposure -0.2, the approved project held +5 and +1.0.

## 3. What good looks like, in numbers (backlit log talking heads, vertical ads)
From the editor's grading notes, measured on frames. Log footage is the camera's flat recording profile, which needs a
log override and a grade before it looks normal; luma is brightness on a 0 to 100 scale (IRE is the waveform's version
of it); skin hue is in HSV degrees; the vectorscope angle is where skin sits on Premiere's vectorscope.
- Face lit side 55 to 62 luma, shade side 45 to 50 (60 to 70 IRE is for direct light, not backlit faces).
- Skin hue 15 to 20 (HSV; under 10 reads pink); vectorscope angle about 123 (under 112 pink, over 130 orange).
- Darkest detail at 2 to 5; red channel under about 95; neutral checks on something known (a shaded grey sofa, a black
  lav mic).
- Fix pink with more green Tint and slight warmth, not a cooler Temperature ("Cooling made the pink worse").
- Raise Exposure in 0.1 steps and back off one step when hair or fabric texture goes flat.
- Use the white-balance eyedropper only on something truly white (a white T-shirt, never a cream sofa).
- Captions read 100 on the waveform: ignore them when measuring.
- Face light: a second, exposure-only grade on a feathered mask, only where required, per shot, never pasted.

## 4. Mixed sources under one look
- One look per location, cloned onto adjustment layers; B-roll from the same camera gets the same log override and a
  clip-level copy of the look.
- Rec.709 stock and YouTube archive get no log override: clone the master look but zero its log-specific basics
  (Tint, Exposure, Contrast, Highlights, Shadows, Whites, Blacks, Sharpen, Vibrance), keep curves, wheels and vignette for
  the house feel, then per clip Temperature 0 to +6, Saturation 85 to 95, Exposure -0.3 to +0.35; old SD archive also a
  little Sharpen and Exposure +0.3. Why: a master grade tuned for log burns Rec.709 footage.
- Old SD archive reads as archive: present it as archive rather than pretending it is sharp.
- A dimmer (spotlight, vignette) is cloned from a NEUTRAL grade (exposure only, no LUT, flat curves), never from the
  master look, or the look is applied twice.
- One grade across a montage (second reviewer): mixed grades make a montage "not cohesive".

## 5. Scope of a colour pass on a multi-piece project
- Change only the grade layers and the camera's own B-roll; skip muted items, keyframed grades (a tracked spotlight),
  face lights, archive and stock; guard so a grade shared by two looks never gets the change twice (134 grades
  inventoried, 96 edited, none in the wrong group).
- Build the pass on the editor's latest save as a new version; offer exports, do not start them if they are busy.

## 6. Presenters, stills and composites
- Match one presenter still to the others by numbers (brightness, contrast, colourfulness, warmth in a face band) on
  the cut-out's own opaque pixels, never with the background counted; target the mean of three reference poses and
  keep the closest of about six candidates. When new stills are already close, halve the old correction.
- One approved still set and wardrobe for a presenter everywhere: the presenter is the channel's visual anchor.
- A still cut-out sat into a warm room needs a light warm tint, lifted blacks, a blurred plate behind and shared grain;
  values and the 2.5D rig: motion-design and premiere-ae-editing.
- No fake life on stills (no breathing or sway): life comes from camera parallax, pose swaps, shadow, light wrap and
  grain.

## 7. Music edits: a light house look and colour as structure
- A fixed, light look keeps broadcast footage natural and lets the flashes do the work. The pilot's look (Lumetri is
  Premiere's colour panel): contrast 18, saturation 92, temperature -4, highlights -12, shadows -6, blacks -8;
  vignette 28; grain 3; bloom threshold 86, radius 60, intensity 0.16. A B&W chapter: saturation 0, contrast 40,
  exposure -0.4 with 12 fps posterize; colour returns through a light blow-out.
- Colour as structure (research): one colour or overlay family per edit; B&W or a tint for a quiet bar, colour back on
  the drop; change the flash colour per hit; then vs now = B&W past, colour present; end on a B&W card.
- Whole-picture bloom only with threshold 85+ and intensity 0.2 or less; grade and vignette sit below the transitions.
- Full colour floods: disliked twice, avoid.

## 8. Reference looks and brand colours
- The reference-set measured looks (an "analog night" mini-doc finish with crushed blacks, bloom and edge fringing; a "paper
  desk" look where sources keep their own colour and archive goes black and white): reference-looks.md. Use them only
  when a client asks for that look.
- Brand colours come from the brand's own hex (site CSS, brand guide), never sampled from another film ("weird", second
  reviewer). Check saturated brand colours in the H.264 export, not only in the comp: one bright brand orange rendered
  several levels off.
- Graded stills, bulk clip packs and log decodes: premiere-ae-editing grading.md.
