#!/usr/bin/env python3
# Screen-photo document push: a page looks filmed off a monitor, the camera pushes to a line, a yellow marker sweeps across it.
# Idea from vibe-motion fisheye-motion; written from scratch, no code copied. Needs numpy, scipy, Pillow, ffmpeg.
# screen_push.py <page.png> <page_marked.png> <out.mp4> [--w 1440 --h 1080 --fps 30 --dur 3 --zoom 2.1 --bend 0.28 --moire 0.10]
import argparse,subprocess,numpy as np
from PIL import Image
from scipy.ndimage import map_coordinates,gaussian_filter
a=argparse.ArgumentParser();a.add_argument('page');a.add_argument('marked');a.add_argument('out')
for k,v in dict(w=1440,h=1080,fps=30,dur=3.0,zoom=2.1,bend=.28,moire=.10,z0=1.05).items(): a.add_argument('--'+k,type=type(v),default=v)
A=a.parse_args();W,H=A.w,A.h
P=np.asarray(Image.open(A.page).convert('RGB'),np.float32)/255
M=np.asarray(Image.open(A.marked).convert('RGB'),np.float32)/255
assert P.shape==M.shape
ph,pw=P.shape[:2]
mask=np.abs(P-M).sum(2)>.05
ys,xs=np.nonzero(mask);x0,x1=xs.min(),xs.max();fx,fy=(x0+x1)/2,ys.mean()
def ease(t,a,b):
    u=np.clip((t-a)/(b-a),0,1);return 1-(1-u)**3
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
nx=(xx-W/2)/(W/2);ny=(yy-H/2)/(W/2);r2=nx*nx+ny*ny
vig=np.clip(1-.62*r2**1.25,.12,1)[...,None]
rng=np.random.default_rng(7)
ff=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(A.fps),'-i','-','-c:v','libx264','-crf','16','-pix_fmt','yuv420p',A.out],stdin=subprocess.PIPE)
N=int(A.dur*A.fps)
for i in range(N):
    t=i/A.fps;p=ease(t,0,1.2)
    z=A.z0+(A.zoom-A.z0)*p
    cx=pw/2+(fx-pw/2)*p+6*np.sin(t*1.7);cy=ph/2+(fy-ph/2)*p+4*np.sin(t*1.3)
    scale=pw/W/z                            # source pixels per output pixel
    bend=1+A.bend*r2
    sx=cx+(xx-W/2)*bend*scale;sy=cy+(yy-H/2)*bend*scale
    rev=x0+(x1-x0+2)*ease(t,1.25,1.75)      # marker sweeps left to right
    src=np.where((mask&(np.arange(pw)[None,:]<=rev))[...,None],M,P)
    fr=np.stack([map_coordinates(src[...,c],[sy+(c-1)*r2*2.2*scale,sx+(c-1)*r2*2.2*scale],order=1,mode='constant',cval=0.02) for c in range(3)],-1)
    # scan lines bend with the picture, fixed lines stay on the sensor: together they give moire
    bent=.5+.5*np.sin(sy/scale*2*np.pi/3.4)
    fixed=.5+.5*np.sin(yy*2*np.pi/3.0+t*2)
    fr*= (1-A.moire*(1-bent*fixed)*1.6)[...,None]
    fr=fr*np.array([.97,.985,1.0])*.93+.018
    fr=fr+gaussian_filter(fr,(9,9,0))*.10   # soft screen glow
    fr=fr*vig+rng.normal(0,.008,(H,W,1))
    ff.stdin.write((np.clip(fr,0,1)*255).astype(np.uint8).tobytes())
ff.stdin.close();ff.wait()
print('focus',fx,fy,'frames',N)
