# Screen-photo document push (test v1, 4 Nov 2026, waiting on the user's verdict)
Page looks filmed off a monitor: lens bend, moire, dark corners, slight colour fringe. Camera pushes to one line, then a yellow marker sweeps it.
Use: `python3 screen_push.py page.png page_marked.png out.mp4 [--dur 3 --zoom 2.1 --bend 0.28 --moire 0.10]`. Marked page = same page with the line highlighted.
Timing: push 0 to 1.2 s, marker 1.25 to 1.75 s. About 0.5 s of machine time per frame at 1440x1080.
Built in Python, not HyperFrames: per-pixel bend and moire are simpler here, no Chrome render. Idea from vibe-motion fisheye-motion, no code copied.
Test uses labelled sample text. Replace with the real page before use.
