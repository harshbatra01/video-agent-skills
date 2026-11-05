# Estimate sound hits (clicks, impacts, whooshes) in a finished mix, per window. Voice can trigger it, so it is a rough count.
# sound_hits.py <media> [json_out]. Click: high band jumps fast and falls fast. Impact: low band jumps fast.
import sys,json,subprocess,numpy as np
from scipy.signal import butter,sosfilt
SR=24000
x=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",sys.argv[1],"-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout,np.float32).copy()
hop=int(SR*.005)
def env(sig):
    n=len(sig)//hop; return 10*np.log10((sig[:n*hop].reshape(n,hop)**2).mean(1)+1e-9)
hi=env(sosfilt(butter(4,3000,"hp",fs=SR,output="sos"),x)); lo=env(sosfilt(butter(4,150,"lp",fs=SR,output="sos"),x))
hits=[]
def scan(e,rise,fall,kind):
    last=-1
    for i in range(12,len(e)-16):
        before=np.median(e[i-12:i-2]); peak=e[i:i+4].max()
        if peak-before>=rise and i-last>=10 and (fall is None or peak-e[i+6:i+16].min()>=fall) and peak>-50:
            hits.append((round(i*.005,3),kind)); last=i
scan(hi,14,10,"click"); scan(lo,12,None,"impact")
hits.sort()
t=np.array([h[0] for h in hits]) if hits else np.array([])
dur=len(x)/SR
r={"dur":round(dur,1),"total":len(hits),"per_min":round(len(hits)/dur*60,1),"first5":int((t<5).sum()),"first5_click":sum(1 for a,k in hits if a<5 and k=="click"),"first5_impact":sum(1 for a,k in hits if a<5 and k=="impact"),"first10":int((t<10).sum())}
print(json.dumps(r))
if len(sys.argv)>2: json.dump(hits,open(sys.argv[2],"w"))
