---
name: dark-launch-reel
description: DRAFT. Build a dark monochrome motion-designer launch reel in the dhruvxr style. 16:9, 15 to 16.5 s, black base, a micro-montage first second, small grey sans text, one idea per card, a small mark on black at the end. Holds the measured style law, the opening budget, type spec, ffmpeg and PIL effect recipes, sound and rights rules, a checklist and 4 measuring tools. Use when the user asks for a launch reel, brand film, product teaser or text manifesto "like dhruvxr", or for a dark, fast, near-wordless motion piece. Rests on 2 videos only. Pair with reference-study and effect-library.
---

# Dark launch reel (draft)

Status: draft from the dhruvxr sprint, 5 Nov 2026. Not in `skills/` yet. Needs the user's verdict.
Folded in: sprint files `05_RULE_BOOK.md` (v1, 07:49 UTC, rules cited as R#), `07_BUILD_PLAN.md` (first version, 07:48 UTC) and the main flags of `08_RED_TEAM.md` (v1, 07:49 UTC).
Claude reads frames and numbers. It cannot watch motion or hear. Everything here comes from 2 posts by @_dhruvxr on X:
- **WHP**: Whop brand film, 1280x720, 30 fps, 16.49 s, voice-over, client logo end card.
- **ATN**: "attention" manifesto, 1280x720, 29.97 fps, 14.95 s, text only over music, signed "dhruv".

Full study: `research/dhruvxr/STUDY.md`. Shot list: `research/dhruvxr/raw/shots_by_hand.json`.

**Tags.** BOTH = seen in both videos (still only 2 videos). WHP or ATN = seen in one video only, so treat it as an option, not a law. Judged = my read, not measured.

## When to use
- The user wants a launch reel, brand film, product teaser or text manifesto in a dark, fast, near-wordless motion-designer style.
- The user names dhruvxr, or shares a reference with a black base, a first second of 1 to 4 frame shots, small grey sans text and a mark on black at the end.
- Not for narrated mini-docs (use `minidoc-reference-style`), talking heads, or anything that needs more than about 20 words on screen.

## Approved defaults (Gate 1, user)
- Spec piece in ATN style: text manifesto over music, no client logos.
- Sign-off: our own studio mark, placeholder "[STUDIO]".
- No real third-party logos.
- Opening: match the page's density, with one idea in 3 s.
- Loudness: -9 to -10 LUFS integrated, -1 dBTP true peak.
- Engine: ffmpeg plus PIL/numpy. No After Effects here.

## Build setup (from sprint file 07_BUILD_PLAN.md, first version 07:48 UTC)
- Spec piece: 1280x720, 30 fps, 15.0 s = 450 frames. STUDY.md's delivery default is 1920x1080 at 30 fps; both are fine. Pick one at intake and keep every pixel number below in % of frame height.
- Measured present: Python 3.13.18, numpy 2.5.3, Pillow 12.3.0, ffmpeg and ffprobe 6.1.1 with libx264. Filters present include perspective, gblur, geq, lutyuv, curves, rgbashift, displace, tblend, tmix, chromakey, vignette, noise, xfade, zoompan, loudnorm, ebur128, alimiter.
- Inter is installed at `/usr/share/fonts/opentype/inter/` (Regular, Medium, Italic, MediumItalic and more). DejaVu is also present.
- Headless Chrome works, but about 7 s per cold screenshot (07 measured 7.24 s). Render each HTML card once to PNG and reuse it; PIL cards are the fallback.
- scipy is NOT installed, so `skills/minidoc-reference-style/scripts/synth.py` will not run as is. Port its filters to numpy or use ffmpeg audio filters.
- `tts.py` is ElevenLabs only and its key is unset here. The ATN-style default has no voice anyway.
- Not present: After Effects, Premiere, any person-matte tool on Linux (`person_mask.js` is Mac only). Default for the cut-out device: hold our own text or dot form instead (07 G1).

## Style law (measured)
| Measure | WHP | ATN | Law for ours | Tag |
|---|---|---|---|---|
| Format | 1280x720, 30 fps | 1280x720, 29.97 fps | Deliver 1920x1080, 30 fps (1280x720 also fine) | BOTH |
| Length | 16.49 s | 14.95 s | 15 to 16.5 s | BOTH |
| Shots (by hand) | 31 | 26 | 26 to 31 | BOTH |
| Median shot | 0.20 s (6 f) | 0.13 s (4 f) | 4 to 6 f | BOTH |
| Shots of 4 f or less | 35% | 58% | 35 to 58% | BOTH |
| Shots in first 1 s / 3 s | 8 / 15 | 9 / 11 | 8 to 9 / 11 to 15 | BOTH |
| Holds after the burst | 0.9 to 2.4 s | 0.9 to 2.4 s | 0.9 to 2.4 s, one card or form each | BOTH |
| Mean brightness | 0.14 | 0.25 | 0.14 to 0.25 | BOTH |
| Near-black pixels | 78% | 63% | at least 60% | BOTH |
| Near-grey pixels | 97% | 86% | at least 85% | BOTH |
| Mean saturation | 0.02 | 0.06 | 0.02 to 0.06; fail above 0.08 (R58, margin judged) | BOTH |
| Vivid pixels | 0.3% | 2.2% | 0.3 to 2.2%, only on our product or mark; fail above 3% (R58, margin judged) | BOTH |
| Vivid hue split | red plus orange/yellow 74%, cyan/blue 25% | 51%, 40% | warm accent first, cyan/blue second; no full-frame tint (R59) | BOTH |
| Words on screen | about 12 | 20 | 12 to 20 | BOTH |
| White flash events (1 to 3 f) | 5 (the study's list shows 6 positions: f10, f45, f78 to f80, f195 to f196, f243 to f244, f322) | 0 | ATN-style default: 0 in the opening, at most 1 in the piece (R15) | WHP |
| End mark on black | 2.4 s | 2.7 s | 2.4 to 2.7 s | BOTH |
| Loudness | -14.1 LUFS, LRA 3.1, peak +0.1 dBFS | -5.4 LUFS, LRA 3.8, peak +2.1 dBFS (clipped) | -9 to -10 LUFS, -1 dBTP, LRA 3.1 to 3.8 LU (Gate 1 default plus R64, not a page number) | approved |

Shape of the 15 s (BOTH):
1. 0 to 1 s: burst of 8 to 9 shots on one idea.
2. Then holds of 0.9 to 2.4 s, one card or one form at a time.
3. One second, shorter burst after the middle: 4 to 7 shots of about 3 f within 0.7 to 0.8 s, placed between 43% and 69% of the run time (R7). WHP 4 shots in 0.7 s, f322 to f342; ATN 7 backgrounds at 3 f each, f192 to f215.
4. Last 2.5 to 5.7 s near-empty: a small centred mark on black, then black or a fade.

## Opening budget
- **0 to 1 s:** 8 to 9 shots, 1 to 4 frames each, hard cuts, all on one idea. ATN: brand-style cards every 4 f with words adding on at f2, f6 and f12.
- **By 3 s:** 11 to 15 shots in total, still one idea (Gate 1).
- **Words in the first 3 s:** about 5 to 6 (ATN 6 words by 2.2 s; WHP about 5 label words plus the VO "Ideas."). Default for ours: one claim card of up to 3 words in the first second, one problem card by 2.2 s.
- **First readable word:** f2 in ATN, f21 in WHP. Default: by f6. One idea readable by f90 (3.0 s), per Gate 1 and R13.
- **Frame numbers:** WHP is 30 fps, ATN 29.97 fps. We build at 30 fps, so ATN frame numbers can be used as they are (drift 0.45 f over 15 s, per 05).
- This breaks the repo's opening limits, which were set for narrated mini-docs (`reference-study`). The user approved the page's density for this job at Gate 1. Ask again before using it on another job.

## Type spec
- **Font:** Inter Regular or Medium. Judged closest free match, not fitted. ATN reads close to SF Pro Text.
- **Case:** sentence case, lower case where possible.
- **Colour:** grey-white ink #AA to #DF on black (measured). #F7 only on bright footage (snow). Not pure #FFFFFF on black.
- **Size:** ink height 2.2 to 4.6% of frame height (16 to 33 px on 720; 24 to 50 px on 1080). Ink height runs ascender to descender, not cap height.
- **Bigger lines:** at most 2, at 7.8 to 10% (56 to 72 px at 720, 84 to 108 px at 1080). The largest goes on the thesis (R20). ATN "It gets ignored." 7.8%, "It's earned" about 10%. WHP wordmark 5%.
- **Licence:** Inter is SIL OFL and installed here (07). Do not use SF Pro; its licence was not checked (R16).
- **ATN layout:** lines centred vertically at 50 to 54% of height. Split across the width (first half left, rest right) or word by word with wide gaps.
- **WHP layout (option):** italic corner labels with slashes like code comments ("// word //"), at x 8 to 18% or 82 to 90%, y 17% or 80 to 84%, soft glow.
- **Per card:** 1 to 5 words, median 2.5. 0.9 to 1.2 s per card. About 2 to 4 words a second.

### Text motion (frames at 30 fps, measured)
| Move | Frames | Source |
|---|---|---|
| Words add on one at a time | every 4 to 6 f | ATN f2, f6, f12 |
| Blur in to sharp | 2 to 3 f | WHP f21 to f23 |
| Right-to-left reveal | 3 to 6 f | ATN f122 to f127; WHP f421 to f424 |
| Fade up / fade out | 2 f up, 8 f out | WHP "ownership" f132, f197 to f204 |
| Big word flash | 2 f only | WHP "Audience" f76 to f77 |
| Card change | hard cut with the shot | ATN, most cards |
| End mark | no fade in, 56 f hold, about 24 f fade out | ATN f310, f366 to f390 |
| Dim and blink on a shot change | about 5 f | ATN f25 to f29 |
| Slow drift, two labels apart | about 25 px over 60 f, two keys | WHP "ownership" and phonetics from f138 |

Drop every other text move: bounces, overshoot, per-letter pops, typewriter cursor, slides, 3D flips, scale punches (R32).

## Copy
- 12 to 20 words on screen in total; ATN-style default 16 to 20 (R33). 1 to 5 words per card, median 2 to 3, each card 27 to 36 f.
- ATN argument, 8 cards: claim, problem, problem made concrete, turn (on the drop), old belief, thesis part 1, thesis part 2, sign-off.
- The turn is 1 word alone on its card at about 34% of run time, on a hard cut with the drop. On 450 f that is f153, 5.1 s (R36).
- The thesis is split across 2 cards (R37).
- A deliberate typo of our own only if the script needs it, max 1 (R24).
- One stretch of about 2.4 s with no text, where the picture carries the idea (ATN f67 to f121).
- Write our own lines. Never reuse theirs or the "prduct" misspelling.

## Effect recipes (ffmpeg plus PIL/numpy)
Pipeline default: draw every frame in PIL/numpy and pipe raw frames into ffmpeg.
`ffmpeg -f rawvideo -pix_fmt rgb24 -s 1920x1080 -r 30 -i - -i music.wav -c:v libx264 -crf 16 -pix_fmt yuv420p -c:a aac -b:a 320k -shortest out.mp4`
Numbers marked "judged" were not measured. Show 3 or 4 strengths on real frames before rolling an effect out (`effect-library` rule).
One or two headline effects per piece, no more (R46). Camera moves are two-key drifts or pushes, no hand-keyed paths (R55). Build every device from scratch; never their keyhole, Whop UI, cards, particle-to-logo or globe (R56).

| # | Effect | Measured | Recipe |
|---|---|---|---|
| 1 | Opening micro-montage | 8 to 9 shots of 1 to 4 f in 1 s | Cut list of (clip, in-frame, length 1 to 4 f). Read source frames with `ffmpeg -ss <t> -i clip -frames:v <n>`; hard cuts only |
| 2 | Monochrome base, colour only on product | brightness 0.14 to 0.25 | `hue=s=0,eq=contrast=1.1:brightness=-0.05` (values judged). Keep a colour layer for the product only, composited with a numpy mask |
| 3 | White flash | 1 to 3 f, WHP only | Replace frames with white (255). Max 3 whole-frame hits per video |
| 4 | White blowout into 1-bit threshold | 3 f to white, 5 f threshold (WHP f78 to f85) | numpy gain ramp 1 to 4 then clip; then `np.where(L > 128, 255, 0)` |
| 5 | Dot-matrix form with bloom | WHP f0 to f3, f245 to f286 | Sample a mask on a grid, draw square dots sized by mask value; bloom = sum of 3 Gaussian blurs, the wide one shrinking as the camera pulls back. 2 f white bloom on a hit. Proof in `jobs/dhruvxr-01/sprint/proof/dot_matrix_proof.py`: 640x360, 6 px grid, 4 px dots, ink up to #DF, 12 frames in 0.42 s. Its frame 0 was too dark (mean 0.055, near-black 88.2%), so a full shot needs a bigger form or footage behind it |
| 6 | Vertical-line screen texture | WHP live footage | Darken every 3rd pixel column by 5 to 8%: `a[:, ::3] *= 0.93` (spacing judged) |
| 7 | Corner label blur-in with glow | 3 f (WHP f21 to f23) | PIL text, `GaussianBlur` radius 6, 3, 0 over 3 frames (radii judged). Glow = blurred copy added at about 40% (judged) |
| 8 | Product UI tilted in 3D, focus pull | 2 f blur-in, slow drift (WHP f91 to f111) | `Image.transform(size, Image.PERSPECTIVE, coeffs)`, coeffs solved from 4 corner points; two-key drift; vignette |
| 9 | Scan-line tear plus log list | 9 to 18 f, between 1.4 and 4.3 s | Per frame, `np.roll` random bands (8 to 40 px tall, 20 to 120 px shift, judged), add white bars, flash a monospace log list |
| 10 | Right-to-left reveal | 3 to 6 f | Mask whose left edge moves from the right end of the text box to the left; `Image.composite` |
| 11 | Selection box around a word | 1 px box with corner handles (ATN f222 to f245) | `ImageDraw.rectangle` 1 px white; 4 square handles (6 to 8 px, judged) |
| 12 | Cut-out over swapping backgrounds | background every 3 f (ATN f180 to f215) | Needs a pre-keyed RGBA subject or green screen: `chromakey=0x00FF00:0.1:0.05`, then overlay on a background list. No Linux matting tool in the repo |
| 13 | Hard cut to black, then sign-off | 31 f black, mark with no fade, 56 f hold, 24 f fade out (ATN) | Black frames, then the "[STUDIO]" mark; fade with numpy alpha or `fade=t=out:st=<s>:d=0.8` |
| 14 | Grain and soft vignette | ATN eye and web wall | `noise=alls=6:allf=t,vignette=PI/5` (07 values, judged; try 6 to 8) |
| 15 | Rotating dot globe | WHP f343 to f410, dims over about 60 f | numpy Fibonacci-sphere points, rotate per frame, orthographic projection, faint red tint |
| 16 | Particles converging into a mark | 46 f, then 2 f bloom (WHP f195 to f243) | numpy points eased from random positions to points sampled on the mark |
| 17 | Montage inside an eye | ATN f30 to f66, slow push | Circular iris mask on a licensed eye macro; composite the montage inside it at reduced opacity (judged); red and cyan character grid at the left (R47) |
| 18 | Curved 3D wall of our own screens | ATN f67 to f152, hero screen lands f104, then darkens to black | PIL perspective warp per card, two-key moves, then a fade to black (R49) |

Glitch note: the repo bans box glitch in music edits. Whether this piece counts as a music edit was not checked (R52).

## Sound rules
- Music runs to the last frame. No silence, except an optional fade in the last 0.5 s (WHP, 15.96 s on). BOTH.
- Do not cut to the beat grid. Cuts on the grid were at or below chance in both. BOTH.
- Let sound hits follow picture changes: at least half of the 6 dB+ level jumps within 0.1 s (3 f) of a shot change (R60). WHP: 12 of 22 (55%) against 27% chance. WHP only, not heard.
- Put the drop on the turn card. ATN: bass drop at 5.0 to 5.1 s on "Attention". ATN only.
- Later bass hits in ATN: 5.1, 7.6, 10.1, 12.6 s, 2.5 s apart. Could be one bar at about 96 BPM. Judged.
- WHP opens on a sub-bass hit from 0.1 to 1.6 s, then dips to -26 dB at 2.1 to 2.6 s. WHP only.
- Loudness: -9 to -10 LUFS, -1 dBTP. Two-pass `loudnorm=I=-9.5:TP=-1:LRA=4`, then check with `ebur128=peak=true`. Never copy ATN's clipped +2.1 dBFS peak.
- Voice: the ATN-style spec has none by default. Any voice sample must be licensed or our own recording, logged in SOURCES.txt. Never reuse the ATN sample.

## Rights rules
- No real third-party logos, brand cards, product UI or wordmarks. ATN shows Apple, Meta, Whop, Wise, Figma, Adobe and ChatGPT; permission unknown. Use fictional marks designed from scratch.
- Sign off with our "[STUDIO]" mark. Never "dhruv", never the Whop mark.
- Copy no frame, layout or asset: not their keyhole, their Whop UI, their card designs or the "prduct" typo. Same kind of device, built from scratch.
- Footage, stills, UI, music and SFX: ours or licensed. Log each in `jobs/dhruvxr-01/SOURCES.txt`: file, source, licence, frames used (R71).
- No real platform badges (verified ticks) on our cards (R69).
- Fonts with an open licence only. Inter is SIL OFL (R73).
- Do not identify or reuse the references' music or voice sample.
- The MRI head clip is in both videos. It is not a must; copying it reads as a copy.

## Checklist
- [ ] 16:9, 1920x1080, 30 fps, 15 to 16.5 s.
- [ ] 8 to 9 shots in the first 1 s, 11 to 15 by 3 s, all on one idea.
- [ ] Median shot 4 to 6 f. Holds after the burst 0.9 to 2.4 s.
- [ ] One second burst after the middle.
- [ ] Brightness 0.14 to 0.25, near-black at least 60%, near-grey at least 85% (`colour_stats.py`).
- [ ] Colour only on our product or mark.
- [ ] 12 to 20 words on screen, 1 to 5 per card, about 1 s per card.
- [ ] Type: Inter, sentence case, #AA to #DF, body ink 2.2 to 4.6%, one line at 8 to 10% (`text_box.py`).
- [ ] Turn card on the drop. Cuts not on the beat grid (`sync_test.py`).
- [ ] Ends on "[STUDIO]" on black, ink about 5% of height (36 px at 720), on screen 2.4 to 2.7 s, music to the last frame (R65 to R67).
- [ ] One or two headline effects only. No text moves outside the table above.
- [ ] Loudness and true peak measured on the final encoded .mp4, not the WAV (08).
- [ ] -9 to -10 LUFS, true peak -1 dBTP or lower.
- [ ] No real third-party logos. SOURCES.txt complete.
- [ ] Effects shown at 3 or 4 strengths and approved before rollout.

## Tools (`research/dhruvxr/tools/`)
All need ffmpeg, ffprobe and numpy (PIL for `crop_strip.py`). Frames are 0-based.
| Tool | Usage | What it gives |
|---|---|---|
| `crop_strip.py` | `crop_strip.py <video> <x> <y> <w> <h> <f0> <f1> <out.jpg> [cols=8] [scale=1.0]` | Every frame of one box, tiled, frame number on each. Box in source pixels, f1 inclusive. For text in and out times to the frame |
| `text_box.py` | `text_box.py <video> <frame> <x> <y> <w> <h> [light\|dark] [thr=70]` | JSON: ink box in px, ink height px and %, x %, y centre %, mean ink colour hex. ±2 px. Busy backgrounds get picked up as ink |
| `sync_test.py` | `sync_test.py <video> <events.json> [extra_times_csv] [tol=0.067] [onset_pct=92]` | JSON: share of cuts, flashes and extra times (for example text in-times) within tol of an audio onset, against chance from 1000 random shifts. events.json comes from `cut_events.py` |
| `envelope.py` | `envelope.py <video> <out.json>` | 0.1 s rows: level in dB RMS, bass share under 150 Hz, voice-band share 300 to 3400 Hz. Finds hits, dips, drops and voice sections |
| `box_presence.py` (extra) | `box_presence.py <video> <x> <y> <w> <h> [f0] [f1]` | Per-frame contrast in a box. Text on and off shows as a step. Confirm on a `crop_strip.py` sheet |

Other repo tools named above: `skills/minidoc-reference-style/scripts/colour_stats.py` (brightness, near-black, near-grey, vivid share), `skills/minidoc-reference-style/scripts/cut_events.py` (makes the events.json for `sync_test.py`), `skills/reference-study/scripts/beat_map.py` (tempo and cuts on the beat grid). Source log for this job: `jobs/dhruvxr-01/SOURCES.txt`.

Tool limits seen in the study: `cut_events.py` thresholds were set on Altman. On this page it merged WHP's first 17 frames into one event and missed dark-to-dark cuts. For a micro-montage, count shots by hand on a `crop_strip.py` sheet. Tempo from `beat_map.py` was a weak fit on both videos.

### Check our render against the law (example, 1280x720)
```
T=research/dhruvxr/tools
python3 $T/crop_strip.py out.mp4 0 0 1280 720 0 89 first3s.jpg 10 0.2     # count shots in the first 3 s by hand
python3 $T/text_box.py out.mp4 40 160 300 960 120 light                   # ink height % and hex of one card
python3 skills/minidoc-reference-style/scripts/cut_events.py out.mp4 ...  # see that script for its arguments, then:
python3 $T/sync_test.py out.mp4 events.json "0.07,0.2,5.1" 0.067         # cuts should sit at or below chance
python3 $T/envelope.py out.mp4 env.json                                   # the drop should sit on the turn card
ffmpeg -i out.mp4 -af ebur128=peak=true -f null -                         # -9 to -10 LUFS, true peak -1 dBTP or lower
```
The boxes and times above are placeholders. Set them from our own cut list. The `cut_events.py` arguments were not checked for this draft.

## What rests on only 2 videos
- Everything. Treat BOTH items as a working law and single-video items as options.
- One video only: white flashes, dot-matrix forms, corner code labels, level hits on picture changes (WHP); the drop on the turn card, word-by-word add-on, selection box, cut-out over swapping backgrounds (ATN).
- Not checked: views, likes, retention, the page's other posts, playback, sound by ear, music IDs, which sounds are SFX, voice source, tools used, and whether 16:9 and 15 s are fixed rules.
- Tempo is very low trust (weak fits). Fonts are judged. Tool cut counts are low trust here; use the hand shot list.

## Conflicts with repo rules (user's call)
- Opening density breaks the repo's mini-doc opening limits. Approved for this job only.
- Body text 2.2 to 4.6% is under `effect-library`'s 5% readability rule. Default: body at 4.5% (49 px ink on 1080), the top of the measured range.
- WHP has 5 white flash events; `effect-library` caps whole-frame hits at 3. Default: 0 in the opening and at most 1 in the piece (R15).

## Red-team flags (08_RED_TEAM.md v1, judged, not yet the user's call)
These argue against parts of the measured style for a phone viewer. Phone sizes are estimates, not measured on a device.
- Frame 0 must not be black. Show the hook line, readable, on a lit frame, since feeds show frame 0 as the preview.
- Flash safety: no more than 3 large bright flashes in any 1 s (WCAG 2.3.1). Keep burst images at similar brightness.
- Text that carries the message: ink at least 6% of height (2.2% is about 4 pt on a phone). Keep 2 to 4% for texture labels only. This conflicts with the measured 2.2 to 4.6%.
- Make the turn work on mute: a visible change on the turn card, not only the drop.
- Keep text out of the bottom 15% and the corners (player controls). On a 4:5 Instagram layout, out of the bottom 20%.
- Make a separate 4:5 (1080x1350) layout for Instagram, not a crop.
- No logos at all, real or fictional, and nothing shaped like a famous mark.
- To not read as a copy, change at least 3 of: the thesis, the hook device, the turn device, the end layout.
