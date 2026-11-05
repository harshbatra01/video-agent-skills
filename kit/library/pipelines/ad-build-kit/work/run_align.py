import json, numpy as np, time, sys
sys.path.insert(0,'.')
from align import *
idx=json.load(open('calib/index.json'))
PX=0.48148149251937866
res={}
for t,d in idx.items():
    t0=time.time()
    refs=d['ref']; ref=load(refs[len(refs)//2])
    raws_f=d['raw']; raws=[]; keep=[]
    prev=None
    for f in raws_f:
        a=load(f)
        if prev is not None and np.array_equal(a,prev): continue
        raws.append(a); keep.append(f); prev=a
    c,ri,H,Z,dx,dy=match(ref,raws,PX)
    c2,Z2,dx2,dy2=refine(ref,raws[ri],PX,H,Z,dx,dy)
    # also score the other hypothesis at its own best for comparison
    Hother='stretch' if H=='pad' else 'pad'
    c3=match(ref,[raws[ri]],PX,H_list=(Hother,))[0]
    res[t]={'ref':refs[len(refs)//2],'raw':keep[ri],'H':H,'Z':Z2,'dx':dx2,'dy':dy2,'ncc':c2,'ncc_other_H':c3,'n_raw_unique':len(raws)}
    print(t, res[t]['raw'][-14:], H, 'Z=%.3f dx=%d dy=%d ncc=%.3f (other H %.3f)  %.0fs'%(Z2,dx2,dy2,c2,c3,time.time()-t0), flush=True)
json.dump(res,open('calib/align.json','w'),indent=1)
