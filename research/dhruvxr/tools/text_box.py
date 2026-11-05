#!/usr/bin/env python3
# Measures the ink of light (or dark) text inside a hand-set box on one frame: ink bounding box in px and % of frame,
# ink height, mean ink colour. text_box.py <video> <frame> <x> <y> <w> <h> [light|dark] [thr]
# Ink = pixels at least thr luma levels brighter (or darker) than the box median. Judged boxes; ±2 px.
import subprocess, sys, json, numpy as np
v = sys.argv[1]; n, x, y, w, h = map(int, sys.argv[2:7]); mode = sys.argv[7] if len(sys.argv) > 7 else "light"; thr = float(sys.argv[8]) if len(sys.argv) > 8 else 70
W, H = map(int, subprocess.run(["ffprobe","-v","error","-select_streams","v","-show_entries","stream=width,height","-of","csv=p=0",v],capture_output=True,text=True).stdout.strip().split(","))
raw = subprocess.run(["ffmpeg","-v","error","-i",v,"-vf",f"select=eq(n\\,{n})","-frames:v","1","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
F = np.frombuffer(raw, np.uint8).reshape(H, W, 3).astype(float); B = F[y:y+h, x:x+w]; L = B @ [0.2126, 0.7152, 0.0722]
med = np.median(L); m = (L > med + thr) if mode == "light" else (L < med - thr)
ys, xs = np.nonzero(m)
if not len(ys): print(json.dumps({"frame": n, "ink": None})); sys.exit()
x0, x1, y0, y1 = x+xs.min(), x+xs.max(), y+ys.min(), y+ys.max(); col = B[m].mean(0)
print(json.dumps({"frame": n, "ink_px": [int(x0), int(y0), int(x1), int(y1)], "ink_h_px": int(y1-y0+1), "ink_h_pct": round((y1-y0+1)/H*100, 2),
 "x_pct": [round(x0/W*100,1), round(x1/W*100,1)], "y_centre_pct": round((y0+y1)/2/H*100, 1), "ink_rgb": [int(c) for c in col], "hex": "#%02X%02X%02X" % tuple(int(c) for c in col), "box_median_luma": round(float(med),1)}))
