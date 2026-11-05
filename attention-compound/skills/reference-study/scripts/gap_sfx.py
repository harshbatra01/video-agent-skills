#!/usr/bin/env python3
# SFX and music level from a finished mix, using only the gaps between spoken words, where voice cannot trigger the count.
import json, subprocess, sys, numpy as np
J=sys.argv[1]; E=sys.argv[2]; A=sys.argv[3]; L=sys.argv[4]
S=[('altman',f'{E}/ref/reference.mp4',f'{E}/ref/transcript.json',f'{L}/altman.json.hits'),
   ('ac_elon',f'{A}/raw1/reel.mp4',f'{A}/raw1.transcript.json',f'{L}/ac_elon.json.hits'),
   ('ac_max',f'{A}/raw2/reel.mp4',f'{A}/raw2.transcript.json',f'{L}/ac_max.json.hits'),
   ('asym',f'{A}/raw3/reel.mp4',f'{A}/raw3.transcript.json',f'{L}/asym.json.hits'),
   ('elon_v18',f'{E}/render/v18/Musk_Delaware_v18.mp4',f'{E}/vo/vo_v2b_final_words.json',f'{L}/elon_v18.json.hits'),
   ('voice_only',f'{J}/vo/v2/Anthropic_IPO_vo_v2_adam.mp3',f'{J}/vo/v2/words.json',f'{L}/voice.hits')]
out={}
for n,v,tp,hp in S:
    d=json.load(open(tp)); w=d['words'] if isinstance(d,dict) else d
    w=sorted((x.get('s',x.get('t0')),x.get('e',x.get('t1'))) for x in w)
    h=[x[0] for x in json.load(open(hp))]
    gaps=[(a[1]+.04,b[0]-.04) for a,b in zip(w,w[1:]) if b[0]-a[1]>0.12]
    g=sum(y-x for x,y in gaps); ih=[t for t in h if any(x<=t<=y for x,y in gaps)]
    SR=16000; x=np.frombuffer(subprocess.run(["ffmpeg","-nostdin","-v","error","-i",v,"-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout,np.float32)
    rms=lambda segs: 10*np.log10(np.mean(np.concatenate([x[int(a*SR):int(b*SR)]**2 for a,b in segs if b>a]))+1e-12)
    wd=rms([(a,b) for a,b in w]); gd=rms(gaps) if gaps else None
    out[n]=dict(words=len(w),gap_s=round(g,1),gap_hits=len(ih),per_gap_s=round(len(ih)/g,2) if g else None,voice_db=round(float(wd),1),gap_db=round(float(gd),1) if gd else None,under=round(float(wd-gd),1) if gd else None)
    print(n,out[n])
json.dump(out,open(f'{L}/gap_sfx.json','w'))
