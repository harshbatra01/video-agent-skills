# Group big frame changes into events and classify each: CUT (new picture stays) or FLASH/FLICKER (snaps back).
# python3 cut_events.py <scores.json> <video> <out.json>
import json, subprocess, sys
import numpy as np
sc, video, out = sys.argv[1:4]
D = json.load(open(sc)); f = D["frames"]; fps = D["fps"]; n = len(f)
w, h = 160, 120
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", video, "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
V = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3).astype(np.float32)
def hist(k):
    x = np.concatenate([np.histogram(V[k][..., c], 16, (0, 256))[0] for c in range(3)]).astype(np.float32); return x / x.sum()
def dist(a, b): return float(np.abs(V[a].mean(2) - V[b].mean(2)).mean()), float(np.abs(hist(a) - hist(b)).sum())
cand = [x["i"] for x in f if x["diff"] > 20 or x["hdist"] > 0.3]
events, cur = [], []
for i in cand:
    if cur and i - cur[-1] > 2: events.append(cur); cur = []
    cur.append(i)
if cur: events.append(cur)
res = []
for ev in events:
    a, b = max(ev[0] - 1, 0), min(ev[-1] + 2, n - 1)   # frame before the event, frame settled after it
    d, hd = dist(a, b)
    peak = max(f[i]["luma"] for i in ev); base = (f[a]["luma"] + f[b]["luma"]) / 2
    kind = "CUT" if (d > 18 or hd > 0.35) else "FLASH" if peak - base > 40 else "FLICKER"
    if kind == "CUT" and peak - max(f[a]["luma"], f[b]["luma"]) > 40: kind = "CUT+FLASH"
    res.append({"start": ev[0], "end": ev[-1], "t": f[ev[0]]["t"], "frames": len(ev), "kind": kind, "before_after_diff": round(d, 1), "hdist": round(hd, 2), "peak_luma": peak})
json.dump({"fps": fps, "events": res}, open(out, "w"), indent=0)
from collections import Counter
print(Counter(r["kind"] for r in res), "events:", len(res))
