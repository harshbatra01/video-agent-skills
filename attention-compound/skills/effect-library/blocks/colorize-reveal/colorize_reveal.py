#!/usr/bin/env python3
# Black and white with spin blur; colour sweeps in from the left under a sideways smear; spin settles from the centre out; soft glow.
# Idea from vibe-motion colorize; written from scratch, no code copied. Needs numpy, scipy, ffmpeg. Input: video or image.
# colorize_reveal.py <in> <out.mp4> [--ss 0 --dur 3 --reveal 1.4 --spin 7 --smear 90]
import argparse,subprocess,numpy as np
from scipy.ndimage import map_coordinates,uniform_filter1d,gaussian_filter,zoom
a=argparse.ArgumentParser();a.add_argument('src');a.add_argument('out')
for k,v in dict(w=1440,h=1080,fps=30,ss=0.0,dur=3.0,reveal=1.4,spin=7.0,smear=90).items(): a.add_argument('--'+k,type=type(v),default=v)
A=a.parse_args();W,H=A.w,A.h
vf=f'fps={A.fps},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}'
inp=['-loop','1','-i',A.src] if A.src.lower().endswith(('.png','.jpg','.jpeg','.webp')) else ['-ss',str(A.ss),'-i',A.src]
d=subprocess.Popen(['ffmpeg','-v','error',*inp,'-t',str(A.dur),'-vf',vf,'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
e=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(A.fps),'-i','-','-c:v','libx264','-crf','16','-pix_fmt','yuv420p',A.out],stdin=subprocess.PIPE)
sm=lambda u:u*u*(3-2*u)
w2,h2=W//2,H//2
y2,x2=np.mgrid[0:h2,0:w2].astype(np.float32);dx=x2-w2/2;dy=y2-h2/2
rad=np.sqrt(dx*dx+dy*dy)/np.hypot(w2/2,h2/2)
xx=np.arange(W,dtype=np.float32)[None,:]
LUMA=np.array([.3,.59,.11],np.float32);i=0;NS=9
while True:
    b=d.stdout.read(W*H*3)
    if len(b)<W*H*3: break
    t=i/A.fps;i+=1
    f=np.frombuffer(b,np.uint8).reshape(H,W,3).astype(np.float32)/255
    u=min(t/A.reveal,1)
    if u<1:
        # spin blur, fading from the centre outward. Half size for speed.
        small=f[::2,::2][:h2,:w2];acc=np.zeros_like(small)
        amp=np.radians(A.spin)*(1-sm(np.clip((u*1.5-rad*.5),0,1)))
        for n in range(NS):
            th=amp*(n/(NS-1)-.5);c,s=np.cos(th),np.sin(th)
            sx=w2/2+dx*c-dy*s;sy=h2/2+dx*s+dy*c
            for ch in range(3): acc[...,ch]+=map_coordinates(small[...,ch],[sy,sx],order=1,mode='nearest')
        spun=zoom(acc/NS,(H/h2,W/w2,1),order=1)[:H,:W]
        weight=np.clip(amp/np.radians(A.spin)*3,0,1)
        weight=zoom(weight,(H/h2,W/w2),order=1)[:H,:W,None]
        pic=f*(1-weight)+spun*weight
    else: pic=f
    # colour edge moves left to right, with a sideways smear around it
    edge=-.15*W+1.3*W*sm(u)
    soft=.12*W
    col=np.clip((edge-xx)/soft+.5,0,1)[...,None]
    grey=(pic@LUMA)[...,None]*np.array([.96,.98,1.0])
    out=grey*(1-col)+pic*col
    if 0<u<1:
        k=np.exp(-((xx-edge)/(.16*W))**2)[...,None]
        out=out*(1-k)+uniform_filter1d(out,A.smear,axis=1,mode='nearest')*k
    glow=gaussian_filter(out[::4,::4],(6,6,0));glow=zoom(glow,(H/glow.shape[0],W/glow.shape[1],1),order=1)[:H,:W]
    out=out+glow*(.10+.14*(1-sm(np.clip((t-A.reveal)/.8,0,1))))
    e.stdin.write((np.clip(out,0,1)*255).astype(np.uint8).tobytes())
e.stdin.close();e.wait();d.wait()
