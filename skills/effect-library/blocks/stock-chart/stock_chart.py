#!/usr/bin/env python3
# Candlestick chart draws left to right on a dark blue terminal, price counts with it, ends on a push-in. Real data only in an edit.
# Idea from vibe-motion remotion-candlestick; written from scratch. CSV columns: date,open,high,low,close.
# stock_chart.py <out.mp4> [--csv file --title TEXT --dur 3]. With no CSV it draws seeded fake data, stamped SAMPLE DATA.
import argparse,csv,subprocess,numpy as np
from PIL import Image,ImageDraw,ImageFont
a=argparse.ArgumentParser();a.add_argument('out')
for k,v in dict(w=1440,h=1080,fps=30,dur=3.0,csv='',title='SAMPLE').items(): a.add_argument('--'+k,type=type(v),default=v)
A=a.parse_args();W,H=A.w,A.h;S=2
if A.csv:
    R=list(csv.DictReader(open(A.csv)));D=np.array([[float(r[k]) for k in ('open','high','low','close')] for r in R]);stamp=''
else:
    rng=np.random.default_rng(11);c=100*np.exp(np.cumsum(rng.normal(.006,.024,70)));o=np.r_[100,c[:-1]]
    D=np.c_[o,np.maximum(o,c)*(1+rng.uniform(0,.012,70)),np.minimum(o,c)*(1-rng.uniform(0,.012,70)),c];stamp='SAMPLE DATA, NOT A REAL STOCK'
F='/System/Library/Fonts/HelveticaNeue.ttc'
fb=ImageFont.truetype(F,110*S,index=1);fm=ImageFont.truetype(F,30*S,index=0);fs=ImageFont.truetype(F,24*S,index=1)
n=len(D);lo,hi=D[:,2].min(),D[:,1].max()
L,Rt,T,B=90*S,(W-90)*S,230*S,(H-90)*S
X=lambda i:L+(Rt-L)*(i+.5)/n;Y=lambda p:B-(B-T)*(np.log(p)-np.log(lo))/(np.log(hi)-np.log(lo))
yy=np.linspace(0,1,H*S)[:,None,None];bg=(np.array([9,14,32])*(1-yy)+np.array([14,34,70])*yy)
bg=np.broadcast_to(bg,(H*S,W*S,3)).astype(np.uint8)
e=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(A.fps),'-i','-','-c:v','libx264','-profile:v','high','-level','4.0','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',A.out],stdin=subprocess.PIPE)
N=int(A.dur*A.fps);UP,DN=(46,235,150),(255,62,82);bw=max(4,int((Rt-L)/n*.62))
for f in range(N):
    t=f/N;u=1-(1-min(t/.8,1))**2;k=u*n
    im=Image.fromarray(bg.copy());d=ImageDraw.Draw(im)
    for g in range(6):
        y=T+(B-T)*g/5;d.line([L,y,Rt,y],fill=(40,60,100),width=2)
    last=0
    for i in range(int(np.ceil(k))):
        o,h,l,c=D[i];q=min(1,k-i);col=UP if c>=o else DN;x=X(i)
        cc=o+(c-o)*q;d.line([x,Y(o+(h-o)*q),x,Y(o+(l-o)*q)],fill=col,width=3)
        a1,a2=sorted([Y(o),Y(cc)]);d.rectangle([x-bw/2,a1,x+bw/2,max(a2,a1+3)],fill=col);last=cc
    d.text((L,60*S),f'{last:,.2f}',font=fb,fill=(245,248,255));d.text((L,190*S-14*S),A.title,font=fm,fill=(150,175,215))
    if stamp:d.text((Rt-d.textlength(stamp,font=fs),60*S),stamp,font=fs,fill=(255,200,60))
    z=1.0;cw,ch=int(W*S/z),int(H*S/z);x0=W*S-cw;y0=0
    e.stdin.write(im.crop((x0,y0,x0+cw,y0+ch)).resize((W,H),Image.LANCZOS).tobytes())
e.stdin.close();e.wait()
