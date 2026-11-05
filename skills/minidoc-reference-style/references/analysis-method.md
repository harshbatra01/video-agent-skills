# How to analyse a reference (and what each check misses)

1. `frame_scores.py ref.mp4 scores.json`: brightness, frame-to-frame change and colour-histogram change for every frame.
2. `cut_events.py scores.json ref.mp4 events.json`: groups big changes into events; CUT if the frame before and the frame
   settled after differ, FLASH if brightness spikes and snaps back, FLICKER otherwise. Long events hide micro-shots.
3. `event_sheets.py events.json ref.mp4 evsheet 25`: strips of every event. Look at all of them.
4. `ref_stats.py <dir> ref.mp4 transcript.json`: shot table with the words spoken over each shot, cuts a second per
   section, cut-to-word alignment, monochrome share, flash and black frames.
5. `motion_class.py ref.mp4 shots_ref.json`: moving footage vs stills per shot (threshold 0.9 on the residual after
   aligning zoom and pan). The reference was 67% moving. Do not use it on our own renders with grain.
6. `frame_strip.py ref.mp4 t0 t1 out.jpg`: every frame of a moment. Do this for the opener, every effect the user names,
   every rule break.
7. Corners at full resolution and the caption band at word ends (crops) for the frame-edge look and caption style.
8. Audio: voice loudness against loudness in the pauses (is the bed loud?), sub-band and air-band envelopes around the
   moments named (swells, clicks), whether the voice stops (soundbites).

## What went wrong before, and why
- Contact sheets of mid-shot stills showed composition but not motion, so "mostly video" was invisible until motion was
  measured. Always run step 5.
- Summarising sheets ("halftone portrait over a logo") hid multi-stage effects (the 9-grid). Every frame of every
  effect moment, step 6, written out as a timeline.
- The first pace check measured the median shot and then built to a different number. Compare the build with the same
  tools before showing it.
