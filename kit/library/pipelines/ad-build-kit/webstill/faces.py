"""Face close-ups for every frame in a window: full-res face sharpness + a labelled sheet of the top frames.
usage: python faces.py CLIP t0 t1 fx0 fy0 fx1 fy1 out.png N"""
import sys
import av, numpy as np
from PIL import Image, ImageDraw, ImageFont
clip, t0, t1 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
fx0, fy0, fx1, fy1 = map(int, sys.argv[4:8]); out, N = sys.argv[8], int(sys.argv[9])
c = av.open(clip); v = c.streams.video[0]; v.thread_type = 'AUTO'; tb = v.time_base
c.seek(int(max(0, t0 - 1.2) / tb), stream=v, backward=True)
rows = []
for fr in c.decode(v):
    t = float(fr.pts * tb)
    if t < t0 - 0.01: continue
    if t > t1: break
    a = fr.to_ndarray(format='rgb24')[fy0:fy1, fx0:fx1]
    g = a.mean(axis=2).astype(np.float32)
    lap = g[1:-1, 1:-1] * 4 - g[:-2, 1:-1] - g[2:, 1:-1] - g[1:-1, :-2] - g[1:-1, 2:]
    rows.append((float(lap.var()), t, a))
c.close()
rows.sort(key=lambda r: -r[0])
pick = []
for s, t, a in rows:
    if all(abs(t - p[1]) >= 0.2 for p in pick): pick.append((s, t, a))
    if len(pick) >= N: break
pick.sort(key=lambda r: r[1])
def view(a):
    x = a.astype(np.float32) / 255
    x = np.clip((x - 0.10) / (0.72 - 0.10), 0, 1) ** 0.85
    g = x.mean(axis=2, keepdims=True); x = np.clip(g + (x - g) * 1.5, 0, 1)
    return Image.fromarray((x * 255).astype(np.uint8))
TW = 300; TH = int(TW * (fy1 - fy0) / (fx1 - fx0))
cols = 5; nr = (len(pick) + cols - 1) // cols
S = Image.new('RGB', (cols * TW, nr * TH), (20, 20, 20)); d = ImageDraw.Draw(S); f = ImageFont.truetype('arialbd.ttf', 16)
for i, (s, t, a) in enumerate(pick):
    x, y = (i % cols) * TW, (i // cols) * TH
    S.paste(view(a).resize((TW, TH)), (x, y)); lab = '%.2f  s%.0f' % (t, s)
    d.rectangle([x, y, x + 9 * len(lab), y + 20], fill=(0, 0, 0)); d.text((x + 3, y + 1), lab, fill=(255, 220, 0), font=f)
S.save(out); print(out, S.size, ['%.2f:%.0f' % (t, s) for s, t, a in pick])
print('face sharpness spread: best %.0f median %.0f worst %.0f' % (rows[0][0], rows[len(rows) // 2][0], rows[-1][0]))
