# Colour numbers for a video, sampled at 2 frames a second. Usage: colour_stats.py <label> <video>
import subprocess,sys,json,numpy as np,colorsys,os
label,video=sys.argv[1:3]
W,H=160,120
raw=subprocess.run(['ffmpeg','-v','error','-i',video,'-vf',f'fps=2,scale={W}:{H}','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
fr=np.frombuffer(raw,np.uint8).reshape(-1,H,W,3).astype(float)
R,G,B=fr[...,0],fr[...,1],fr[...,2]
mx=fr.max(-1);mn=fr.min(-1);S=(mx-mn)/np.maximum(mx,1);V=mx/255
rg=R-G;yb=(R+G)/2-B
colourful=np.array([np.sqrt(rg[i].std()**2+yb[i].std()**2)+.3*np.sqrt(rg[i].mean()**2+yb[i].mean()**2) for i in range(len(fr))])
d=mx-mn;h=np.zeros_like(mx)
m=d>0
r=m&(mx==R);g=m&(mx==G)&~r;b=m&~r&~g
h[r]=((G-B)[r]/d[r])%6;h[g]=(B-R)[g]/d[g]+2;h[b]=(R-G)[b]/d[b]+4;h*=60
vivid=(S>.35)&(V>.25)
fam={'red':(h<20)|(h>=340),'orange_yellow':(h>=20)&(h<70),'green':(h>=70)&(h<170),'cyan_blue':(h>=170)&(h<260),'purple_pink':(h>=260)&(h<340)}
res={'label':label,'frames':len(fr),'mean_saturation':round(float(S.mean()),3),'mean_brightness':round(float(V.mean()),3),'colourfulness_median':round(float(np.median(colourful)),1),'colourfulness_p90':round(float(np.percentile(colourful,90)),1),'vivid_pixels_pct':round(float(vivid.mean()*100),1),'near_black_pct':round(float((V<.12).mean()*100),1),'near_grey_pct':round(float((S<.12).mean()*100),1)}
tot=max(vivid.sum(),1)
res['vivid_hue_share_pct']={k:round(float((vivid&v).sum()/tot*100)) for k,v in fam.items()}
print(json.dumps(res))
