# R2 grid reveal (opener effect #1)

Script: sprint/R2-tools/grid_reveal.py

Usage: python3 grid_reveal.py <image> <out.mp4> [--w 1920 --h 1080 --fps 25 --dur 1.5 --seed 1] [--sheet sheet.png]

What it does: photo starts blurred; 3x3 grid; white #F2F1EF blocks pop into random cells 2 to 3 at a time inside about 1 s; each block holds 2 to 3 frames then fades to the sharp photo over 3 to 4 frames; 1 px grid lines at 25% white stay visible.

Test (ran OK): 960x540, 25 fps, 1.5 s, 38 frames, groups 2,2,3,2. Files in sprint/R2-tools/test/: placeholder.png (generated PIL placeholder), test_grid_reveal.mp4, contact_sheet.png (every frame).

Comparison with strips/*_000-003.jpg by eye: NOT done in this sprint (out of time). Timing and colours follow STUDY.md spec only; check the contact sheet against the strips next.

Missing: subject cut-out (subject over the grid), background swap, any easing on the fade, matching blur strength to the reference.
