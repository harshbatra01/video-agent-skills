"""QA contact sheet of chosen time windows, every Nth frame, labelled with frame/time.

usage: python qasheet.py VIDEO OUT_PREFIX "a-b,c-d,..." [step_frames=2] [thumb_w=96] [cols=15] [--crop x0,y0,x1,y1] [--grid N]
Writes one sheet per window (several if long). Red border = big picture change from the previous kept frame.
--crop looks at one region of the frame (source pixels) at full detail: ball contact, a face in a wide shot.
"""
import sys
import numpy as np, av
from PIL import Image, ImageDraw, ImageFont

crop = None; grid = 0
if "--crop" in sys.argv:
    i = sys.argv.index("--crop"); crop = [int(v) for v in sys.argv[i + 1].split(",")]; del sys.argv[i:i + 2]
if "--grid" in sys.argv:     # source-pixel grid every N px, labelled: read prompt boxes / points straight off the sheet
    i = sys.argv.index("--grid"); grid = int(sys.argv[i + 1]); del sys.argv[i:i + 2]
path, prefix, wins = sys.argv[1], sys.argv[2], sys.argv[3]
step = int(sys.argv[4]) if len(sys.argv) > 4 else 2
tw = int(sys.argv[5]) if len(sys.argv) > 5 else 96
cols = int(sys.argv[6]) if len(sys.argv) > 6 else 15
spans = [tuple(float(x) for x in w.split("-")) for w in wins.split(",")]
c = av.open(path); s = c.streams.video[0]; fps = float(s.average_rate); W, H = s.codec_context.width, s.codec_context.height
th = int(round(tw * ((crop[3] - crop[1]) / (crop[2] - crop[0]) if crop else H / W)))
frames = {}
for i, fr in enumerate(c.decode(s)):
    t = i / fps
    if any(a <= t < b for a, b in spans) and i % step == 0:
        if crop:
            a = fr.to_ndarray(format="rgb24")[crop[1]:crop[3], crop[0]:crop[2]]
            frames[i] = np.asarray(Image.fromarray(a).resize((tw, th), Image.LANCZOS))
        else:
            frames[i] = fr.reformat(width=tw, height=th, format="rgb24").to_ndarray()
    if t > max(b for _, b in spans): break
c.close()
font = ImageFont.truetype(("C:/Windows/Fonts/arialbd.ttf" if sys.platform == "win32" else "/System/Library/Fonts/Supplemental/Arial Bold.ttf"), 10)
for a, b in spans:
    ids = [i for i in sorted(frames) if a <= i / fps < b]
    rows = (len(ids) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (tw + 2) + 2, rows * (th + 13) + 2), (25, 25, 25)); d = ImageDraw.Draw(sheet)
    prev = None
    for k, i in enumerate(ids):
        x = 2 + (k % cols) * (tw + 2); y = 2 + (k // cols) * (th + 13)
        sheet.paste(Image.fromarray(frames[i]), (x, y))
        if grid:
            ox, oy = (crop[0], crop[1]) if crop else (0, 0); sw = (crop[2] - crop[0]) if crop else W; kx = tw / sw
            for gx in range((ox // grid + 1) * grid, ox + sw, grid):
                px = x + int((gx - ox) * kx); d.line([(px, y), (px, y + th)], fill=(0, 255, 255), width=1); d.text((px + 2, y + 2), str(gx), fill=(0, 255, 255), font=font)
            sh_ = (crop[3] - crop[1]) if crop else H
            for gy in range((oy // grid + 1) * grid, oy + sh_, grid):
                py = y + int((gy - oy) * kx); d.line([(x, py), (x + tw, py)], fill=(0, 255, 255), width=1); d.text((x + 2, py + 2), str(gy), fill=(0, 255, 255), font=font)
        if prev is not None and np.abs(frames[i].astype(int) - prev.astype(int)).mean() > 30:
            d.rectangle([x - 1, y - 1, x + tw, y + th], outline=(255, 50, 50), width=2)
        prev = frames[i]
        d.text((x + 1, y + th + 1), f"{i/fps:.2f}", fill=(230, 230, 230), font=font)
    out = f"{prefix}_{a:05.2f}-{b:05.2f}.png"; sheet.save(out); print(out, sheet.size, len(ids), "frames")
