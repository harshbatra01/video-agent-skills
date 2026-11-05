# Tilted video wall (test v2, 4 Nov 2026, waiting on the user's verdict)
Playing clips in tilted columns, scrolling in opposite directions, top and bottom fall into dark, slow push.
Use: `python3 video_wall.py out.mp4 clip1 clip2 ... --start 40 [--dur 3 --tilt 28 --roll -7 --speed 70]`. Takes 30 tiles, repeats clips at later points. About 25 s of machine time for 3 s.
Choose start points that avoid slates. Test uses Elon job clips only. Idea from vibe-motion remotion-3d-ticker, no code copied.
