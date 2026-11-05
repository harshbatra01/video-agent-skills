"""List likely restarts (a piece that repeats the opening of the one before). Mac (Apple Silicon) only as written:
mlx-whisper. On Windows use faster-whisper (see README)."""
import json, re, wave, numpy as np, mlx_whisper
db=np.load("db10ms.npy"); edl=json.load(open("edl_full.json"))
w=wave.open("raw_a0.wav"); x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
pieces=[]
for c in edl["cuts"]:
    a,b=c["raw_in_f"]/30,c["raw_out_f"]/30
    seg=db[int(a*100):int(b*100)]
    quiet=seg<-62
    # split at internal quiet runs >= 0.18 s
    cuts=[];i=0
    while i<len(quiet):
        if quiet[i]:
            j=i
            while j<len(quiet) and quiet[j]: j+=1
            if j-i>=18 and i>0 and j<len(quiet): cuts.append((i+j)//2)
            i=j
        else: i+=1
    bounds=[0]+cuts+[len(seg)]
    for s,e in zip(bounds[:-1],bounds[1:]):
        if e-s>=15: pieces.append((round(a+s/100,2),round(a+e/100,2),c["img"]))
def norm(t): return re.sub(r"[^a-z0-9 ]","",t.lower()).split()
out=[]
for (a,b,img) in pieces:
    clip=np.concatenate([np.zeros(8000,np.float32),x[int(a*16000):int(b*16000)],np.zeros(8000,np.float32)])
    r=mlx_whisper.transcribe(clip,path_or_hf_repo="mlx-community/whisper-large-v3-turbo",language="en",condition_on_previous_text=False)
    out.append((a,b,img,r["text"].strip()))
json.dump(out,open("pieces.json","w"),indent=1)
print(len(out),"pieces")
for k in range(len(out)-1):
    a,b,i1,t1=out[k]; c,d,i2,t2=out[k+1]
    w1,w2=norm(t1),norm(t2)
    if not w1 or not w2: continue
    common=0
    while common<min(len(w1),len(w2)) and w1[common]==w2[common]: common+=1
    if common>=2 or (len(w1)>=1 and w2[:len(w1)]==w1):
        print(f"RESTART? {a}-{b} '{t1}'  ->  {c}-{d} '{t2}'")
