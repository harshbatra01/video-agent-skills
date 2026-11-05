#!/usr/bin/env python3
# Particles settle on the still lines of a slowly changing 3D wave pattern and turn in space. Abstract "AI mind" texture.
# Idea from 3d-chladni-render; written from scratch, no code copied. On black, so it can be screen-blended over footage.
# particle_mind.py <out.mp4> [--dur 3 --n 300000 --tint blue|warm]
import argparse,subprocess,numpy as np
from scipy.ndimage import gaussian_filter
a=argparse.ArgumentParser();a.add_argument('out')
for k,v in dict(w=1440,h=1080,fps=30,dur=3.0,n=300000,tint='blue').items(): a.add_argument('--'+k,type=type(v),default=v)
A=a.parse_args();W,H=A.w,A.h
rng=np.random.default_rng(5)
P=rng.uniform(-1,1,(A.n,3)).astype(np.float32);P=P[(P**2).sum(1)<1]
def field(P,m):
    x,y,z=(P*np.pi).T;n1,n2,n3=m
    f=np.sin(n1*x)*np.sin(n2*y)*np.sin(n3*z)+np.sin(n2*x)*np.sin(n3*y)*np.sin(n1*z)
    g=np.stack([n1*np.cos(n1*x)*np.sin(n2*y)*np.sin(n3*z)+n2*np.cos(n2*x)*np.sin(n3*y)*np.sin(n1*z),
      n2*np.sin(n1*x)*np.cos(n2*y)*np.sin(n3*z)+n3*np.sin(n2*x)*np.cos(n3*y)*np.sin(n1*z),
      n3*np.sin(n1*x)*np.sin(n2*y)*np.cos(n3*z)+n1*np.sin(n2*x)*np.sin(n3*y)*np.cos(n1*z)],1)
    return f,g
A1=np.array([2.,3.,4.]);A2=np.array([3.,2.,5.])
for _ in range(25):
    f,g=field(P,A1);P-=.02*(f/(1+(g*g).sum(1)**.5))[:,None]*g/(1e-3+(g*g).sum(1,keepdims=True)**.5)*5
tint=np.array([.55,.78,1.0]) if A.tint=='blue' else np.array([1.0,.72,.45])
e=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(A.fps),'-i','-','-c:v','libx264','-profile:v','high','-level','4.0','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',A.out],stdin=subprocess.PIPE)
N=int(A.dur*A.fps)
for i in range(N):
    t=i/N;m=A1+(A2-A1)*(t*t*(3-2*t))
    f,g=field(P,m);P-=(.06*f/(1e-3+(g*g).sum(1)**.5))[:,None]*g/(1e-3+(g*g).sum(1,keepdims=True)**.5)*2
    P+=rng.normal(0,.0012,P.shape).astype(np.float32)
    th=.5+.5*i/A.fps;c,s=np.cos(th),np.sin(th);x=P[:,0]*c+P[:,2]*s;z=-P[:,0]*s+P[:,2]*c;y=P[:,1]
    ca,sa=np.cos(.35),np.sin(.35);y,z=y*ca-z*sa,y*sa+z*ca
    d=1/(2.6-z);sc=H*1.25*(1+.08*i/N)
    px=(W/2+x*d*sc).astype(int);py=(H/2+y*d*sc).astype(int)
    ok=(px>=0)&(px<W)&(py>=0)&(py<H);im=np.zeros((H,W),np.float32)
    np.add.at(im,(py[ok],px[ok]),(.4+1.2*(z[ok]+1)/2))
    fine=gaussian_filter(im,.7);gl=gaussian_filter(im,10)
    v=1-np.exp(-(fine*.55+gl*1.6))
    fr=v[...,None]*tint+(v[...,None]**3)*.5
    e.stdin.write((np.clip(fr,0,1)*255).astype(np.uint8).tobytes())
e.stdin.close();e.wait()
