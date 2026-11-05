#!/usr/bin/env python3
"""Timecoded contact sheet of one clip. scan_sheet.py <clip> <every_s> <out.jpg> [cols] [start] [end]"""
import subprocess, sys
from PIL import Image, ImageDraw, ImageFont
src, ev, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
cols = int(sys.argv[4]) if len(sys.argv) > 4 else 10
a = float(sys.argv[5]) if len(sys.argv) > 5 else 0
dur = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",src],capture_output=True,text=True).stdout)
b = float(sys.argv[6]) if len(sys.argv) > 6 else dur
W, H = 200, 113
raw = subprocess.run(["ffmpeg","-nostdin","-v","error","-ss",str(a),"-t",str(b-a),"-i",src,"-vf",f"fps=1/{ev},scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
n = len(raw)//(W*H*3); rows = (n+cols-1)//cols
S = Image.new("RGB",(cols*W,rows*H)); f = ImageFont.load_default()
try: f = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc",15)
except OSError: pass
d = ImageDraw.Draw(S)
for i in range(n):
    x,y = (i%cols)*W,(i//cols)*H
    S.paste(Image.frombuffer("RGB",(W,H),raw[i*W*H*3:(i+1)*W*H*3]),(x,y))
    t = f"{int(a+i*ev)}"; d.rectangle((x,y,x+d.textlength(t,font=f)+6,y+18),fill=(0,0,0)); d.text((x+3,y+1),t,font=f,fill=(255,230,60))
S.save(out,quality=78); print(out,n)
