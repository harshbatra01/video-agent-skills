"""Tracked spotlight box over the 'here and here' lines (L2a+L2b, then +L3a+L3b), anchor = top-centre. Writes spot_tt.json"""
import json, os
import numpy as np
import masks_tt as MT
from board_def import LINES, box_corners
ANG = -4.0
a = np.deg2rad(-ANG); R = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])   # rotates the board frame upright
def aligned(names):
    pts = np.vstack([box_corners(*LINES[n]) for n in names]) @ R.T
    return pts.min(0), pts.max(0)
lo, hi = aligned(['L2a', 'L2b', 'L3a', 'L3b'])
lo2, hi2 = aligned(['L2a', 'L2b'])
mx, my = 14.0, 8.0
lo = lo - [mx, my]; hi = hi + [mx, my]; hi2 = hi2 + [mx, my]
w, h = hi - lo; f1 = (hi2[1] - lo[1]) / h
top_c = R.T @ np.array([(lo[0] + hi[0]) / 2, lo[1]])          # top-centre back in board coordinates
rows = []
for pi, p in enumerate(MT.PIECES):
    if p['e'] <= 40.9 or p['s'] >= 42.3: continue
    for t, M in MT.piece_samples(pi):
        if t < 40.9 or t > 42.3: continue
        th, s = MT.sim(M)
        q = M[:2, :2] @ top_c + M[:2, 2]
        X, Y = MT.to_seq(p, q[0], q[1])
        rows.append([round(t, 5), X / 1080.0, Y / 1920.0, th + ANG, s * 100])
rows.sort()
out = dict(rows=rows, w=w * MT.K, h=h * MT.K, f1=f1)
json.dump(out, open('spot_tt.json', 'w'))
print('rows', len(rows), 't %.2f-%.2f' % (rows[0][0], rows[-1][0]), 'box %.0f x %.0f seq px' % (w * MT.K, h * MT.K), 'f1 %.3f' % f1)
