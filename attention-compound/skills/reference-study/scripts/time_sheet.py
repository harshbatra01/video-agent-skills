#!/usr/bin/env python3
# time_sheet.py video out.jpg step_s width cols : frames with the second printed on each
import sys, subprocess, tempfile, os, glob
from PIL import Image, ImageDraw
v, o, st, w, cols = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
with tempfile.TemporaryDirectory() as t:
    subprocess.run(["ffmpeg","-nostdin","-v","error","-i",v,"-vf",f"fps=1/{st},scale={w}:-2",f"{t}/%04d.jpg"],check=True)
    fs=sorted(glob.glob(t+"/*.jpg")); a=Image.open(fs[0]); W,H=a.size; rows=(len(fs)+cols-1)//cols
    im=Image.new("RGB",(W*cols,H*rows))
    for i,f in enumerate(fs):
        x=Image.open(f); ImageDraw.Draw(x).rectangle((0,0,26,11),fill="black"); ImageDraw.Draw(x).text((1,0),f"{i*st:.0f}",fill="yellow")
        im.paste(x,((i%cols)*W,(i//cols)*H))
    im.save(o,quality=80); print(o,im.size,len(fs))
