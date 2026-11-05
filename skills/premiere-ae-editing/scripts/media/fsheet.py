"""Every-frame contact sheets with labels.

usage: python fsheet.py video.mp4 outprefix start_frame end_frame [cols rows scale] [beats.json]
  scale = thumbnail width in px (height follows aspect). Each sheet = cols*rows consecutive frames.
  Labels: frame number, time, audio marks K (kick) S (snare) from beats.json, red border on big luma jumps (cuts/flashes).
"""
import sys, json
import numpy as np
import av
from PIL import Image, ImageDraw, ImageFont

path, prefix = sys.argv[1], sys.argv[2]
a, b = int(sys.argv[3]), int(sys.argv[4])
cols = int(sys.argv[5]) if len(sys.argv) > 5 else 12
rows = int(sys.argv[6]) if len(sys.argv) > 6 else 5
tw = int(sys.argv[7]) if len(sys.argv) > 7 else 108
bj = json.load(open(sys.argv[8])) if len(sys.argv) > 8 else None

c = av.open(path); s = c.streams.video[0]; s.thread_type = "AUTO"
fps = float(s.average_rate); W, H = s.codec_context.width, s.codec_context.height
th = int(round(tw * H / W))
frames = []
for i, fr in enumerate(c.decode(s)):
    if i < a: continue
    if i >= b: break
    frames.append(fr.reformat(width=tw, height=th, format="rgb24").to_ndarray())
c.close()

try:
    font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 11)
except Exception:
    font = ImageFont.load_default()

def marks(i):
    if not bj: return ""
    t0, t1 = (i - 0.5) / fps, (i + 0.5) / fps
    m = ""
    if any(t0 <= k[0] < t1 for k in bj["kicks"]): m += "K"
    if any(t0 <= k[0] < t1 for k in bj["snares"]): m += "S"
    return m

per = cols * rows; lab = 14; pad = 2
for si in range(0, len(frames), per):
    chunk = frames[si:si + per]
    sheet = Image.new("RGB", (cols * (tw + pad) + pad, rows * (th + lab + pad) + pad), (25, 25, 25))
    dr = ImageDraw.Draw(sheet)
    prev = frames[si - 1] if si > 0 else None
    for j, im in enumerate(chunk):
        fi = a + si + j
        x = pad + (j % cols) * (tw + pad); y = pad + (j // cols) * (th + lab + pad)
        sheet.paste(Image.fromarray(im), (x, y))
        p = frames[si + j - 1] if si + j > 0 else None
        if p is not None and np.abs(im.astype(int) - p.astype(int)).mean() > 25:
            dr.rectangle([x - 1, y - 1, x + tw, y + th], outline=(255, 40, 40), width=2)
        m = marks(fi)
        dr.text((x + 1, y + th + 1), f"{fi} {fi/fps:.2f}", fill=(230, 230, 230), font=font)
        if m:
            dr.text((x + tw - 8 * len(m) - 2, y + th + 1), m, fill=(0, 220, 255) if "K" in m else (255, 120, 255), font=font)
    out = f"{prefix}_{a+si:04d}-{a+si+len(chunk)-1:04d}.png"
    sheet.save(out)
    print(out, sheet.size)
