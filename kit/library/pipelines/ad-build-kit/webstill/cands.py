"""Candidate sheet: best frame per 1-s bin (sharp / (1 + 2 x motion)), cropped to the subject, quick LOG preview grade.
usage: python cands.py CLIP scores.json out.png x0 x1 y0 y1 bin1 bin2 ..."""
import sys, json
import av, numpy as np
from PIL import Image, ImageDraw, ImageFont
clip, sj, out = sys.argv[1], sys.argv[2], sys.argv[3]
x0, x1, y0, y1 = map(float, sys.argv[4:8])
bins = [int(b) for b in sys.argv[8:]]
R = json.load(open(sj))
best = {}
for x in R:
    s = int(x['t']); sc = x['sharp'] / (1 + 2 * x['motion'])
    if s in bins and (s not in best or sc > best[s][0]): best[s] = (sc, x['t'])
c = av.open(clip); v = c.streams.video[0]; v.thread_type = 'AUTO'; tb = v.time_base


def grab(t):
    c.seek(int(max(0, t - 1.2) / tb), stream=v, backward=True)
    for fr in c.decode(v):
        if fr.pts * tb >= t - 0.019: return fr.to_ndarray(format='rgb24')


def view(a):   # quick S-Log3-ish preview: levels + gamma + saturation (for judging only)
    x = a.astype(np.float32) / 255
    x = np.clip((x - 0.10) / (0.72 - 0.10), 0, 1) ** 0.85
    g = x.mean(axis=2, keepdims=True); x = np.clip(g + (x - g) * 1.5, 0, 1)
    return (x * 255).astype(np.uint8)


TW, TH = 330, 412
ims = []
for s in bins:
    if s not in best: continue
    t = best[s][1]; a = grab(t); h, w = a.shape[:2]
    crop = a[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)]
    im = Image.fromarray(view(crop)); im.thumbnail((TW, TH))
    ims.append(('%.2f' % t, im))
cols = 6; rows = (len(ims) + cols - 1) // cols
S = Image.new('RGB', (cols * TW, rows * TH), (25, 25, 25)); d = ImageDraw.Draw(S); f = ImageFont.truetype('arialbd.ttf', 18)
for i, (lab, im) in enumerate(ims):
    x, y = (i % cols) * TW, (i // cols) * TH
    S.paste(im, (x, y)); d.rectangle([x, y, x + 62, y + 24], fill=(0, 0, 0)); d.text((x + 4, y + 2), lab, fill=(255, 220, 0), font=f)
S.save(out); print(out, S.size, [l for l, _ in ims])
