# Per shot: is it moving video or a still? Inside each shot, align consecutive frames for zoom/pan (best of a few scales and
# shifts) and measure what is left. Stills with a push leave almost nothing; real video leaves motion.
# python3 motion_class.py <video> <shots.json from ref_stats> [out.json]
import json, subprocess, sys
import numpy as np
from PIL import Image
v, sj = sys.argv[1:3]; shots = json.load(open(sj))
fps = eval(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", v], capture_output=True, text=True).stdout)
w, h = 96, 72
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", v, "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True).stdout
V = np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.float32)
def residual(a, b):
    best = 1e9
    for s in (0.97, 0.985, 1.0, 1.015, 1.03):
        im = Image.fromarray(a.astype(np.uint8)).resize((int(w * s), int(h * s)), Image.BILINEAR)
        A = np.asarray(im, np.float32); cy, cx = (A.shape[0] - h) // 2, (A.shape[1] - w) // 2
        A = A[cy:cy + h, cx:cx + w] if s > 1 else np.pad(A, ((-cy, h - A.shape[0] + cy), (-cx, w - A.shape[1] + cx)), mode="edge") if s < 1 else A
        for dx in (-2, -1, 0, 1, 2):
            for dy in (-1, 0, 1):
                best = min(best, np.abs(np.roll(np.roll(A, dx, 1), dy, 0)[4:-4, 6:-6] - b[4:-4, 6:-6]).mean())
    return best
out = []
for s in shots:
    a0, a1 = int(s["t0"] * fps) + 2, int(s["t1"] * fps) - 2
    if a1 - a0 < 3: out.append({**s, "motion": None, "kind": "too short"}); continue
    r = [residual(V[k], V[k + 1]) for k in range(a0, a1 - 1)]
    m = float(np.median(r)); out.append({**s, "motion": round(m, 2), "kind": "video" if m > 2.2 else "still"})
json.dump(out, open(sys.argv[3] if len(sys.argv) > 3 else "motion.json", "w"), indent=0)
k = [o["kind"] for o in out]; tot = lambda kk: sum(o["dur"] for o in out if o["kind"] == kk)
print(f"shots: video {k.count('video')}, still {k.count('still')}, too short {k.count('too short')} | screen time video {tot('video'):.1f} s, still {tot('still'):.1f} s, short {tot('too short'):.1f} s")
