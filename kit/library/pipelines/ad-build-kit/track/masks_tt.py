"""Turn the board track into sequence-space mask transforms (pre-zoom, 1080x1920) for the 3 things ad.
Writes masks_tt.json: per sample {t, pos:{name:(x,y)}, rot, scale} with step-held samples per source frame,
plus the '?' track for the After Effects overlay."""
import json, os
import numpy as np
from tracker import mat
from board_def import LINES

HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
TR = json.load(open('track_tt.json'))
PIECES = json.load(open('pieces.json'))['f233433f']
K = 4 * 0.57                       # sequence px per reference px (frames are source/4, Motion scale 57 %)


def smooth(arr, passes=2):
    a = np.array(arr, float)
    for _ in range(passes):
        if len(a) < 3: break
        b = a.copy(); b[1:-1] = 0.25 * a[:-2] + 0.5 * a[1:-1] + 0.25 * a[2:]; a = b
    return a


def to_seq(p, x, y):
    return p['px'] * 1080 + (4 * x - 3024) * 0.57, p['py'] * 1920 + (4 * y - 1704) * 0.57


def piece_samples(pi):
    """[(t_seq, M(3x3 ref->frame))] for every tracked source frame visible in piece pi, smoothed"""
    p = PIECES[pi]
    ks = sorted(int(k) for k, v in TR.items() if v[7] == pi)
    if not ks: return []
    P = smooth([TR[str(k)][:6] for k in ks])
    out = []
    for k, prm in zip(ks, P):
        t = p['s'] + (k / 25.0 - p['src'])
        if t < p['s'] - 1e-6 or t >= p['e'] - 1e-6: continue
        out.append((t, mat(prm)))
    return out


def anchor_ref(name, side):
    cx, cy, w, h, ang = LINES[name]
    a = np.deg2rad(ang); d = {'right': w / 2, 'left': -w / 2, 'centre': 0.0}[side]
    return np.array([cx + np.cos(a) * d, cy + np.sin(a) * d])


def sim(M):
    A = M[:2, :2]
    th = np.degrees(np.arctan2(A[1, 0] - A[0, 1], A[0, 0] + A[1, 1]))
    s = np.sqrt(abs(np.linalg.det(A)))
    return th, s


def track_for(names_sides, t0, t1):
    """samples in [t0, t1): list of dict(t, piece, rot, scale, pos{name: (xn, yn)})"""
    rows = []
    for pi, p in enumerate(PIECES):
        if p['e'] <= t0 or p['s'] >= t1: continue
        for t, M in piece_samples(pi):
            if t < t0 - 0.05 or t >= t1 + 0.05: continue
            th, s = sim(M); pos = {}
            for name, side in names_sides:
                q = anchor_ref(name, side); q = M[:2, :2] @ q + M[:2, 2]
                X, Y = to_seq(p, q[0], q[1]); pos[name] = (X / 1080.0, Y / 1920.0)
            rows.append(dict(t=round(t, 5), piece=pi, rot=th, scale=s, pos=pos))
    rows.sort(key=lambda r: r['t'])
    return rows


def local_box(name, side):
    """axis-aligned box (pixels) around the anchor, for the static mask path, + anchor (normalized)"""
    cx, cy, w, h, ang = LINES[name]
    W, H = w * K, h * K
    return dict(w=W, h=H, side=side, ang=ang)


if __name__ == '__main__':
    blur = track_for([(n, 'right') for n in ('L1', 'L2a', 'L2b', 'L3a', 'L3b')], 0.0, 30.62)
    hl = track_for([(n, 'left') for n in ('L2a', 'L2b', 'L3a', 'L3b')], 40.12, 42.13)
    q = track_for([('L2a', 'centre')], 0.0, 4.08)
    # '?' sits in the middle of the text block: between L2a and L2b centres
    qt = []
    for r in track_for([('L2a', 'centre'), ('L2b', 'centre')], 0.0, 4.08):
        x = (r['pos']['L2a'][0] + r['pos']['L2b'][0]) / 2 * 1080; y = (r['pos']['L2a'][1] + r['pos']['L2b'][1]) / 2 * 1920
        qt.append([r['t'], x, y, r['rot'], r['scale'] * 100])
    boxes = {n: local_box(n, 'right') for n in LINES}
    json.dump(dict(blur=blur, hl=hl, qmark=qt, boxes=boxes, K=K), open('masks_tt.json', 'w'))
    print('blur samples', len(blur), 'hl', len(hl), 'qmark', len(qt))
    print('rot range %.1f..%.1f  scale %.3f..%.3f' % (min(r['rot'] for r in blur), max(r['rot'] for r in blur), min(r['scale'] for r in blur), max(r['scale'] for r in blur)))
