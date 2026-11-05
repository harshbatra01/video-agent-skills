#!/usr/bin/env python3
# Per-frame contrast inside a box: p99 luma minus median luma. Text on/off shows as a step. Confirm edges on crop_strip.py sheets.
# box_presence.py <video> <x> <y> <w> <h> [f0] [f1]
import subprocess, sys, numpy as np
v = sys.argv[1]; x, y, w, h = map(int, sys.argv[2:6]); f0 = int(sys.argv[6]) if len(sys.argv) > 6 else 0; f1 = int(sys.argv[7]) if len(sys.argv) > 7 else 99999
raw = subprocess.run(["ffmpeg","-v","error","-i",v,"-vf",f"crop={w}:{h}:{x}:{y}","-f","rawvideo","-pix_fmt","gray","-"],capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(float)
for i in range(max(f0,0), min(f1+1, len(fr))):
    a = fr[i]; print(i, int(np.percentile(a, 99) - np.median(a)), int(np.median(a)))
