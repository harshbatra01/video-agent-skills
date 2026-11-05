# Per-frame scores for a video: mean luma, mean abs diff vs previous frame (on 160x120 gray), and colour-histogram distance.
# python3 frame_scores.py <video> <out.json>
import json, subprocess, sys
import numpy as np
v, out = sys.argv[1:3]
w, h = 160, 120
p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", v, "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
fps = eval(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", v], capture_output=True, text=True).stdout.strip())
rows, prev, prevh, i = [], None, None, 0
while True:
    b = p.stdout.read(w * h * 3)
    if len(b) < w * h * 3: break
    f = np.frombuffer(b, np.uint8).reshape(h, w, 3).astype(np.float32)
    g = f.mean(2)
    hist = np.concatenate([np.histogram(f[..., c], 16, (0, 256))[0] for c in range(3)]).astype(np.float32); hist /= hist.sum()
    d = float(np.abs(g - prev).mean()) if prev is not None else 0.0
    hd = float(np.abs(hist - prevh).sum()) if prevh is not None else 0.0
    rows.append({"i": i, "t": round(i / fps, 3), "luma": round(float(g.mean()), 1), "diff": round(d, 2), "hdist": round(hd, 3)})
    prev, prevh, i = g, hist, i + 1
json.dump({"fps": fps, "frames": rows}, open(out, "w"))
print(i, "frames at", round(fps, 3), "fps")
