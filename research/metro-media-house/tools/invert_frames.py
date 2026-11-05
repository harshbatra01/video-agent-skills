#!/usr/bin/env python3
# Find single colour-inverted frames: frame k looks like the NEGATIVE of frame k-1 or k+1 (gray, 96x54).
# invert_frames.py <video>  -> prints count and times. Threshold judged on the flash sheets.
import subprocess, sys, json
import numpy as np
v = sys.argv[1]; w, h = 96, 54
fps = eval(subprocess.run(["ffprobe","-v","error","-select_streams","v","-show_entries","stream=r_frame_rate","-of","csv=p=0",v],capture_output=True,text=True).stdout)
raw = subprocess.run(["ffmpeg","-v","error","-i",v,"-vf",f"scale={w}:{h}","-f","rawvideo","-pix_fmt","gray","-"],capture_output=True).stdout
V = np.frombuffer(raw,np.uint8).reshape(-1,h,w).astype(np.float32)
def corr(a,b):
    a=a-a.mean(); b=b-b.mean(); d=np.sqrt((a*a).sum()*(b*b).sum()); return float((a*b).sum()/d) if d>0 else 0
hits=[]
for k in range(1,len(V)-1):
    c=min(corr(V[k],V[k-1]),corr(V[k],V[k+1])) if False else None
    cp=corr(V[k],V[k-1]); cn=corr(V[k],V[k+1])
    if min(cp,cn) < -0.5 or (cp < -0.6) or (cn < -0.6):
        hits.append(round(k/fps,2))
# merge neighbours (an inverted frame is negative vs both sides; keep one per 3 frames)
m=[]
for t in hits:
    if not m or t-m[-1] > 2.5/fps: m.append(t)
print(json.dumps({"video":v.split('/')[-2],"inverted_frames":len(m),"times":m}))
