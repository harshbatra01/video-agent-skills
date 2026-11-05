#!/usr/bin/env python3
# Every frame of one box of the picture, tiled, frame number on each. For text in/out times to the frame.
# crop_strip.py <video> <x> <y> <w> <h> <f0> <f1> <out.jpg> [cols] [scale]   (box in source pixels, f1 inclusive)
import subprocess, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
v = sys.argv[1]; x, y, w, h, f0, f1 = map(int, sys.argv[2:8]); out = sys.argv[8]
cols = int(sys.argv[9]) if len(sys.argv) > 9 else 8; sc = float(sys.argv[10]) if len(sys.argv) > 10 else 1.0
W, H = map(int, subprocess.run(["ffprobe","-v","error","-select_streams","v","-show_entries","stream=width,height","-of","csv=p=0",v],capture_output=True,text=True).stdout.strip().split(","))
raw = subprocess.run(["ffmpeg","-v","error","-i",v,"-vf",f"select=between(n\\,{f0}\\,{f1}),crop={w}:{h}:{x}:{y}","-vsync","0","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)
tw, th = int(w*sc), int(h*sc)+16; n = len(fr); S = Image.new("RGB", (cols*tw, ((n+cols-1)//cols)*th), (40,40,40)); d = ImageDraw.Draw(S)
try: F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
except OSError: F = ImageFont.load_default()
for i, a in enumerate(fr):
    X, Y = (i%cols)*tw, (i//cols)*th; S.paste(Image.fromarray(a).resize((tw, th-16)), (X, Y+16)); d.text((X+2, Y+1), f"f{f0+i}", font=F, fill=(255,220,0))
S.save(out, quality=90); print(n, "frames", f0, "to", f0+n-1)
