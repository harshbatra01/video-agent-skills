#!/usr/bin/env python3
# Tilted wall of playing video clips. Columns scroll in opposite directions, edges fall into dark.
# Idea from vibe-motion remotion-3d-ticker; written from scratch, no code copied. Needs numpy, scipy, ffmpeg.
# video_wall.py <out.mp4> <clip1> <clip2> ... [--dur 3 --tilt 28 --roll -7 --speed 70 --zoom 1.0 --zoom2 1.12 --start 8]
import argparse,subprocess,numpy as np
from scipy.ndimage import map_coordinates
a=argparse.ArgumentParser();a.add_argument('out');a.add_argument('clips',nargs='+')
for k,v in dict(w=1440,h=1080,fps=30,dur=3.0,tilt=28.0,roll=-7.0,speed=70.0,zoom=1.0,zoom2=1.12,start=8.0,cols=6,rows=5).items(): a.add_argument('--'+k,type=type(v),default=v)
A=a.parse_args();W,H=A.w,A.h;TW,TH,G=480,270,14;SF=15
n=int(A.dur*SF)+1
def load(p,off):
    r=subprocess.run(['ffmpeg','-v','error','-ss',str(off),'-i',p,'-t',str(A.dur+.2),'-vf',f'fps={SF},scale={TW}:{TH}:force_original_aspect_ratio=increase,crop={TW}:{TH}','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
    f=np.frombuffer(r,np.uint8).reshape(-1,TH,TW,3)
    return f
rng=np.random.default_rng(3)
need=A.cols*A.rows;T=[]
for i in range(need):
    p=A.clips[i%len(A.clips)];f=load(p,A.start+(i//len(A.clips))*17+rng.uniform(0,4))
    T.append(f if len(f)>=n else None)
pool=[t for t in T if t is not None];assert pool,'no clip long enough'
T=[t if t is not None else pool[i%len(pool)] for i,t in enumerate(T)]
CW,CH=TW+G,TH+G
wall=np.full((A.rows*CH,A.cols*CW,3),10,np.uint8)
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
ax,az=np.radians(A.tilt),np.radians(A.roll);F=1.5*W
u=(xx-W/2)/F;v=(yy-H/2)/F
c,s=np.cos(az),np.sin(az);u,v=u*c-v*s,u*s+v*c
ca,sa=np.cos(ax),np.sin(ax)
den=ca-v*sa            # ray meets the tilted plane; top of frame goes further away
px=u/den;py=v/den
vig=np.clip(1-.5*((xx-W/2)**2+(yy-H/2)**2)/(W/2)**2,.1,1)[...,None]
fade=np.clip(np.minimum(yy,H-yy)/(H*.2),0,1)[...,None]**.8
ff=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(A.fps),'-i','-','-c:v','libx264','-crf','17','-pix_fmt','yuv420p',A.out],stdin=subprocess.PIPE)
for i in range(int(A.dur*A.fps)):
    t=i/A.fps;k=min(int(t*SF),n-1)
    for j,f in enumerate(T):
        cc,r=j%A.cols,j//A.cols
        wall[r*CH:r*CH+TH,cc*CW:cc*CW+TW]=f[k]
    tmp=wall.copy()
    for cc in range(A.cols):
        sh=int((1 if cc%2 else -1)*A.speed*t+cc*97)
        tmp[:,cc*CW:(cc+1)*CW]=np.roll(wall[:,cc*CW:(cc+1)*CW],sh,axis=0)
    z=A.zoom+(A.zoom2-A.zoom)*(t/A.dur)
    sx=px*F/z+tmp.shape[1]/2;sy=py*F/z+tmp.shape[0]/2
    fr=np.stack([map_coordinates(tmp[...,c].astype(np.float32),[sy,sx],order=1,mode='grid-wrap') for c in range(3)],-1)/255
    fr=fr*vig*fade+rng.normal(0,.008,(H,W,1))
    ff.stdin.write((np.clip(fr,0,1)*255).astype(np.uint8).tobytes())
ff.stdin.close();ff.wait()
