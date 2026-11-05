"""Draw the 9:16 crop window that reframe.follow() picked on a few frames, to check the tracking at a glance.

usage: python reframe_check.py CLIP SRC_IN SRC_OUT PICK OUT.png [zoom]
"""
import sys, av
from PIL import Image, ImageDraw
from reframe import follow, build_gallery
import os

clip, s0, s1, pick, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4], sys.argv[5]
zoom = float(sys.argv[6]) if len(sys.argv) > 6 else 1.0
G = build_gallery(os.path.join(os.path.dirname(__file__), '..', 'pilot', 'catalog', 'catalog.json'), 'yamal') if pick.endswith('+id') else None
path = follow(clip, s0, s1, pick.replace('+id', ''), gallery=G)
want = [s0 + (s1 - s0) * k / 3 for k in range(4)]
c = av.open(clip); s = c.streams.video[0]; c.seek(int(max(0, s0 - 1) / s.time_base), stream=s)
W, H = s.codec_context.width, s.codec_context.height
win_w = H * 9 / 16 / zoom; win_h = H / zoom
got = []
for fr in c.decode(s):
    t = float(fr.pts * s.time_base)
    if want and t >= want[0]:
        p = min(path, key=lambda r: abs(r[0] - t))
        im = fr.to_image(); d = ImageDraw.Draw(im)
        x0 = min(max(0, p[1] - win_w / 2), W - win_w); y0 = min(max(0, p[2] - win_h / 2), H - win_h)
        d.rectangle([x0, y0, x0 + win_w, y0 + win_h], outline=(255, 60, 60), width=6)
        if p[3]: d.rectangle([p[1] - p[3] / 2, p[2] - p[4] / 2, p[1] + p[3] / 2, p[2] + p[4] / 2], outline=(60, 255, 60), width=3)
        got.append(im.resize((W // 4, H // 4))); want.pop(0)
    if not want or t > s1: break
c.close()
sheet = Image.new("RGB", (len(got) * (W // 4 + 4), H // 4), (30, 30, 30))
for i, im in enumerate(got): sheet.paste(im, (i * (W // 4 + 4), 0))
sheet.save(out); print(out, sheet.size)
