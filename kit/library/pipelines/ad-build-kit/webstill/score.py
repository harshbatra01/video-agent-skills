"""Score frames of the pouch clips: sharpness (Laplacian variance) in the subject band + steadiness (diff to previous).
Writes scores_<clip>.json. usage: python score.py CLIP t0 t1 x0 x1"""
import sys, json, os
import av, numpy as np
path, t0, t1, x0, x1 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
c = av.open(path); v = c.streams.video[0]; v.thread_type = 'AUTO'; tb = v.time_base
c.seek(int(max(0, t0 - 1.0) / tb), stream=v, backward=True)
W, H = 1512, 852
out, prev = [], None
for fr in c.decode(v):
    t = float(fr.pts * tb)
    if t < t0 - 0.01: continue
    if t > t1: break
    g = fr.reformat(width=W, height=H, format='gray').to_ndarray().astype(np.float32)
    band = g[int(0.04 * H):int(0.80 * H), int(x0 * W):int(x1 * W)]
    lap = band[1:-1, 1:-1] * 4 - band[:-2, 1:-1] - band[2:, 1:-1] - band[1:-1, :-2] - band[1:-1, 2:]
    sharp = float(lap.var())
    mot = float(np.abs(band - prev).mean()) if prev is not None else 0.0
    prev = band
    out.append(dict(t=round(t, 3), sharp=round(sharp, 2), motion=round(mot, 3), mean=round(float(band.mean()), 1)))
c.close()
name = os.path.splitext(os.path.basename(path))[0]
json.dump(out, open('scores_%s_%d.json' % (name, int(t0)), 'w'))
s = sorted(out, key=lambda r: -r['sharp'])
print(name, len(out), 'frames; sharp p50 %.1f p90 %.1f max %.1f' % (np.percentile([r['sharp'] for r in out], 50), np.percentile([r['sharp'] for r in out], 90), s[0]['sharp']))
