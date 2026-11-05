#!/usr/bin/env python3
# A swinging light finds one word in the dark: sharp and bright in the beam, dim and soft outside it, then settles on the whole word.
# Idea from vibe-motion light-spotlight-render; written from scratch. spotlight_word.py <out.mp4> --word REAL [--dur 3]
import argparse,subprocess,numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from scipy.ndimage import gaussian_filter
a=argparse.ArgumentParser();a.add_argument('out')
for k,v in dict(w=1440,h=1080,fps=30,dur=3.0,word='REAL',size=330).items(): a.add_argument('--'+k,type=type(v),default=v)
A=a.parse_args();W,H=A.w,A.h
f=ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc',A.size,index=1)
t=Image.new('L',(W,H));d=ImageDraw.Draw(t);b=d.textbbox((0,0),A.word,font=f);d.text(((W-b[2]-b[0])/2,(H-b[3]-b[1])/2),A.word,font=f,fill=255)
sharp=np.asarray(t,np.float32)/255;soft=np.asarray(t.filter(ImageFilter.GaussianBlur(9)),np.float32)/255
yy,xx=np.mgrid[0:H,0:W].astype(np.float32);LX,LY=W/2,-260
ang=np.arctan2(xx-LX,yy-LY);dist=np.hypot(xx-LX,yy-LY)
rng=np.random.default_rng(2);dust=gaussian_filter(rng.random((H,W)).astype(np.float32),2.5);dust=(dust-dust.min())/(dust.max()-dust.min())
e=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(A.fps),'-i','-','-c:v','libx264','-profile:v','high','-level','4.0','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',A.out],stdin=subprocess.PIPE)
N=int(A.dur*A.fps);warm=np.array([1,.93,.8],np.float32)
for i in range(N):
    s=i/A.fps;settle=min(max(s-1.7,0)/.8,1);settle=settle*settle*(3-2*settle)
    c=.38*np.sin(s*3.4)*np.exp(-s*.55)*(1-settle)
    width=.13+.75*settle
    beam=np.clip(1-np.abs(ang-c)/width,0,1)**1.4
    fall=1/(1+(dist/1300)**2)
    wall=beam*fall*(.16+.10*dust)
    txt=np.maximum(sharp*beam**.5,soft*.05)
    v=(txt*(1.0)+wall)[...,None]*warm
    v=v+gaussian_filter(txt*beam,18)[...,None]*warm*.35
    v+=rng.normal(0,.006,(H,W,1))
    e.stdin.write((np.clip(v,0,1)*255).astype(np.uint8).tobytes())
e.stdin.close();e.wait()
