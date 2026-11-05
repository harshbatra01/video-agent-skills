"""Merge per-frame video stats with audio events into an event timeline.

usage: python timeline.py stats.npz beats.json out.txt
Flags per frame: CUT (diff spike), FLASH+ (luma jump up), DARK (luma drop), BW (low sat), SHAKE (big shift),
BLUR (edge drop), and audio K/S/H/O/B (kick, snare, hat, onset, beat-grid) at that frame (+-0.5 frame).
"""
import sys, json
import numpy as np

st = np.load(sys.argv[1]); bj = json.load(open(sys.argv[2])); out = sys.argv[3]
fps = float(st["fps"]); n = len(st["ymean"])
y, d, sat, edge, br, dk, sh = st["ymean"], st["diff"], st["sat"], st["edge"], st["bright"], st["dark"], st["shift"]

def med(a, i, r=4):
    a0, b0 = max(0, i - r), min(len(a), i + r + 1)
    return float(np.median(a[a0:b0]))

def ev(lst, i):
    t0, t1 = (i - 0.5) / fps, (i + 0.5) / fps
    return any(t0 <= (e[0] if isinstance(e, (list, tuple)) else e) < t1 for e in lst)

rows = []; counts = {}
for i in range(n):
    f = []
    if d[i] > 18 and d[i] > 2.2 * med(d, i): f.append("CUT")
    if i > 0 and y[i] - y[i - 1] > 25: f.append("FLASH+")
    if br[i] > 0.25: f.append(f"WHITE{int(br[i]*100)}")
    if i > 0 and y[i - 1] - y[i] > 25: f.append("DROP")
    if dk[i] > 0.6: f.append(f"BLACK{int(dk[i]*100)}")
    if sat[i] < 0.06: f.append("BW")
    m = float(np.hypot(*sh[i]))
    if m >= 4: f.append(f"MOVE{m:.0f}")
    if edge[i] < 0.55 * med(edge, i, 6): f.append("BLUR")
    a = []
    if ev(bj["kicks"], i): a.append("K")
    if ev(bj["snares"], i): a.append("S")
    if ev(bj["hats"], i): a.append("H")
    if ev(bj["onsets"], i): a.append("O")
    if ev(bj["beats"], i): a.append("B")
    for k in f: counts[k.rstrip("0123456789")] = counts.get(k.rstrip("0123456789"), 0) + 1
    if f or "K" in a or "S" in a:
        rows.append(f"f{i:03d} {i/fps:6.2f}s  y{y[i]:5.0f} sat{sat[i]:.2f} d{d[i]:5.1f}  {' '.join(f):28s} | {''.join(a)}")
open(out, "w").write("\n".join(rows) + "\n")
# sync score: cuts within 1 frame of a kick/snare/onset
cuts = [i for i in range(n) if d[i] > 18 and d[i] > 2.2 * med(d, i)]
def near(lst, i, tol=1.5):
    t = i / fps
    return min((abs((e[0] if isinstance(e, (list, tuple)) else e) - t) for e in lst), default=9) <= tol / fps
hits = sum(1 for i in cuts if near(bj["onsets"], i) or near(bj["kicks"], i) or near(bj["snares"], i))
print(f"frames {n}, fps {fps}, flags: {counts}")
print(f"cuts {len(cuts)}; on an onset/kick/snare (+-1.5f): {hits}; bpm {bj['bpm']}")
print("cut frames:", " ".join(str(c) for c in cuts))
