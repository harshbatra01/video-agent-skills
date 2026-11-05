"""Bigger crops of chosen frames in one labelled sheet.

usage: python picks.py video.mp4 out.png "f1,f2,..." [crop y0 y1] [thumb_w] [cols]
  crop band y0..y1 in source pixels (default whole frame).
"""
import sys
import av
from PIL import Image, ImageDraw, ImageFont

path, out = sys.argv[1], sys.argv[2]
want = [int(x) for x in sys.argv[3].split(",")]
y0 = int(sys.argv[4]) if len(sys.argv) > 4 else None
y1 = int(sys.argv[5]) if len(sys.argv) > 5 else None
tw = int(sys.argv[6]) if len(sys.argv) > 6 else 405
cols = int(sys.argv[7]) if len(sys.argv) > 7 else 4
c = av.open(path); s = c.streams.video[0]; fps = float(s.average_rate)
got = {}
for i, fr in enumerate(c.decode(s)):
    if i in want:
        im = fr.to_image()
        if y0 is not None: im = im.crop((0, y0, im.width, y1))
        got[i] = im.resize((tw, int(round(tw * im.height / im.width))), Image.LANCZOS)
    if i > max(want): break
c.close()
th = next(iter(got.values())).height
font = ImageFont.truetype(("C:/Windows/Fonts/arialbd.ttf" if sys.platform == "win32" else "/System/Library/Fonts/Supplemental/Arial Bold.ttf"), 14)
rows = (len(want) + cols - 1) // cols
sheet = Image.new("RGB", (cols * (tw + 4) + 4, rows * (th + 22) + 4), (25, 25, 25))
d = ImageDraw.Draw(sheet)
for k, f in enumerate(want):
    x = 4 + (k % cols) * (tw + 4); y = 4 + (k // cols) * (th + 22)
    sheet.paste(got[f], (x, y)); d.text((x + 2, y + th + 3), f"f{f}  {f/fps:.2f}s", fill=(240, 240, 240), font=font)
sheet.save(out); print(out, sheet.size)
