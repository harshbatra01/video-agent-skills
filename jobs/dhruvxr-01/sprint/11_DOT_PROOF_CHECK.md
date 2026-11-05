# 11 Dot proof check (proof/dot_matrix_proof.py vs WHP)

Written 07:53 UTC. Proof script not edited. M = measured with numpy on the PNG/JPG files. J = judged by eye from stills/strips (Claude cannot watch video). Not checked: motion between frames beyond the strips, the full-res frames between f000 and f288, colour of dots, final 1920x1080 scale.

## What the proof does now (from the script, M)
- 640x360 frame. PITCH 6 px, DOT 4 px square (dot = 0.67 of pitch, 2 px gap).
- Glow = dots + 0.6 x blur(4) + 0.45 x blur(12) + (0.35k+0.05) x blur(32); k goes 1 to 0 over 12 frames (0.4 s at 30 fps).

## Side by side
| Item | Proof | WHP reference | Source |
|---|---|---|---|
| Form width / frame width | 81% (x 61-580 of 640) | 19% (f000 mark x 521-758 of 1280); 19% (f288 mark x 519-757) | M |
| Form height / frame height | 29% | 17% (f000), 17% (f288 mark y 293-415); keyhole about 40% tall, 15% wide | M for f000/f288, J for keyhole strip |
| Dot pitch, % of frame width | 0.94% (6/640) | coarse phase f288: 12 px of 1280 = 0.94%; fine phase f000: about 4-5 px of 1280 = 0.3-0.4% | f288 M (autocorrelation lag 12, runs of 7-8 px on); f000 J (dots merge at JPEG res, autocorr unreliable) |
| Dot / pitch ratio | 0.67 | f288 about 0.6-0.67 (7-8 px on, 4-5 px off) | M row scan |
| Dots across the whole form | about 87 | f288 about 20; f000 about 50-60 | f288 M, f000 J |
| Dot shape | hard white squares | f288 squares, some filled with tiny photo tiles; f000 small, slightly rounded (J, JPEG blur) | J |
| Dropout (dots off inside form) | none | f000 shows many dark holes inside the mark; pixel on-fraction is 0.51 in a 100x60 crop (threshold 128), but that count mixes grid gaps with dropout, so the dropout rate itself is not measured | J (on-fraction M) |
| Brightness of dots | 255 | near white (max 255) in f000/f288; keyhole outline dim grey, about 40-50% | M max; keyhole J |
| Glow at frame 0, from form edge (0-255) | +5 px: 24.6, +10: 13.0, +20: 6.0, +40: 2.0 (640 scale) = +10/+20/+40/+80 px at 1280 scale | f000 at 1280: +5: 15.7, +10: 15.1, +20: 10.4, +40: 8.0, +80: 4.9 | M |
| Glow at end | frame 11: +5: 20.9, +10: 8.0, +20: 2.0, +40: 0 | f288: +5 to +80 all about 1 (no glow in coarse phase) | M |
| Ghost dot field around form | none | f000 and keyhole strip both show a faint dim dot field around the form, about 2-5% level | J |
| Glow timing | linear shrink over 12 frames, no flash | strip 08-10: full-frame white bloom 8.10-8.13 (2 frames), decays to a tight halo by about 8.63 (about 15 frames), tight halo holds to 9.53, hard cut to no-glow coarse dots at 9.57 | J from strip |

## Changes to make (numbers are for a 1280x720 proof; scale x1.5 for 1920x1080)
1. Shrink the form. WHP is 19% of width (M). An 8-glyph "[STUDIO]" at 19% is unreadable, so use 35-40% of width (448-512 px at 1280) as a compromise (J). This is the biggest gap.
2. Keep two dot phases, as WHP does:
   - Fine phase (glowing): PITCH 4, DOT 3 at 1280 (J from f000). Gives about 9-10 dots per glyph at 35% width.
   - Coarse phase (no glow): PITCH 12, DOT 8 at 1280 (M from f288). The current proof's 6/4 at 640 already equals this in frame terms; only the form size is wrong.
3. Add dropout in the fine phase: turn off about 30-40% of dots at random, fixed per dot (J by eye from f000; flicker rate not checked).
4. Glow shape: flatter and wider, weaker near the edge. Suggested stack at 1280: (r 4, 0.25), (r 16, 0.30), (r 64, 0.60k + 0.10). Target from f000 (M): about 15 at +5 px, about 10 at +20 px, about 5 at +80 px. Current proof is too hot near the dots (about 25 at +10 px equivalent) and dies too fast (2 at +80 px equivalent). Weights are J; check by re-measuring the ring values after a re-run.
5. Glow timing: start with a 2-frame full-frame white bloom (frame mean near 200-255, J), decay over about 15 frames to the tight halo, hold, then hard cut to the coarse phase with glow 0.
6. Add a faint ghost dot field around the form: same grid, about 3% brightness (8/255), filling about 2x the form's box (J).
7. Optional: keyhole-style outline-only forms at about 45% brightness with a faint ring halo (J from strip 04-06).

## Measured vs judged, in one line
Measured: form fill, f288 pitch and dot size, glow ring values, proof parameters. Judged: f000 fine pitch, dropout rate, dot rounding, ghost field level, flash and decay frame counts, keyhole size and brightness, all suggested weights.
