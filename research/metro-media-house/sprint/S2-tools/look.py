import json, subprocess, sys, os, numpy as np
from PIL import Image, ImageDraw
from concurrent.futures import ThreadPoolExecutor
R='/home/user/video-agent-skills'; M=R+'/research/metro-media-house'; OUT=M+'/sprint/S2-sheets'
IDS={'PAL':'DclpjyxhKF6','ACK':'DdHKc5GBqT-','EIN':'Dee-mp9BJqG','YC':'DfFsUfUx0dZ'}
W,H=240,136
def fps(v):
    o=subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=avg_frame_rate','-of','csv=p=0',v],capture_output=True,text=True).stdout.strip()
    a,b=o.split('/'); return float(a)/float(b)
def grab_all(v):
    p=subprocess.run(['ffmpeg','-v','error','-i',v,'-vf',f'scale={W}:{H}','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True)
    return np.frombuffer(p.stdout,np.uint8).reshape(-1,H,W,3)
def stats(fr):
    f=fr.astype(np.float32)
    Y=0.2126*f[...,0]+0.7152*f[...,1]+0.0722*f[...,2]
    mx=f.max(-1); mn=f.min(-1); S=np.where(mx>0,(mx-mn)/np.maximum(mx,1),0)
    p2,p50,p98=np.percentile(Y,[2,50,98])
    rb=(f[...,0].mean()-f[...,2].mean())
    return dict(p2=p2,p50=p50,p98=p98,con=p98-p2,sat=S.mean(),rb=rb,clip=(Y>=250).mean()*100,crush=(Y<=5).mean()*100)
def do(k):
    vid=IDS[k]; v=f'{R}/reference-reels/{vid}/reel.mp4'
    shots=json.load(open(f'{M}/raw/{vid}/shots_ref.json'))
    F=fps(v); A=grab_all(v); n=len(A)
    mids=[(s['t0']+s['t1'])/2 for s in shots]
    idx=[min(n-1,int(round(t*F))) for t in mids]
    tiles=A[idx]; cols=10; rows=(len(tiles)+cols-1)//cols; lab=14
    sheet=Image.new('RGB',(cols*W,rows*(H+lab)),(30,30,30)); d=ImageDraw.Draw(sheet)
    for i,(t,tl) in enumerate(zip(mids,tiles)):
        x=(i%cols)*W; y=(i//cols)*(H+lab); sheet.paste(Image.fromarray(tl),(x,y)); d.text((x+3,y+H+1),f'#{i} {t:.1f}s',fill=(255,255,0))
    sheet.save(f'{OUT}/{k}_{vid}_shotmids.jpg',quality=85)
    st=[stats(t) for t in tiles]
    agg={q:float(np.median([s[q] for s in st])) for q in st[0]}
    agg['warm_share']=float(np.mean([s['rb']>8 for s in st])*100); agg['cool_share']=float(np.mean([s['rb']<-8 for s in st])*100)
    agg['mono_share']=float(np.mean([s['sat']<0.10 for s in st])*100); agg['clip_frames_share']=float(np.mean([s['clip']>1 for s in st])*100)
    agg['crush_frames_share']=float(np.mean([s['crush']>5 for s in st])*100)
    agg['n_shots']=len(st); agg['fps']=F; agg['n_frames']=n
    # captions: 8 words spread
    tr=json.load(open(f'{R}/reference-reels/{vid}/reel.transcript.json')); ws=tr['words'] if isinstance(tr,dict) else tr
    pick=[ws[int(i)] for i in np.linspace(2,len(ws)-3,8)]
    cap=[]
    for wd in pick:
        t=(wd['s']+wd['e'])/2; fn=f'/tmp/claude-0/-home-user-video-agent-skills/aa32bfaf-1a67-5e6e-bba4-24f779ee2ca6/scratchpad/{k}_{t:.2f}.png'
        subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{t:.3f}','-i',v,'-frames:v','1',fn])
        im=np.asarray(Image.open(fn).convert('RGB')).astype(np.int16); h,w=im.shape[:2]
        mx=im.max(-1); mn=im.min(-1)
        white=(mn>=225)&((mx-mn)<=25)
        rows_w=white.sum(1); band=slice(int(h*.30),int(h*.95))
        rr=np.arange(h); sel=(rows_w>w*0.01); sel[:int(h*.30)]=False
        if sel.sum()>3:
            ys=rr[sel]; cols_=np.where(white[ys].any(0))[0]
            cap.append(dict(word=wd['w'],t=round(t,2),y_top=round(ys.min()/h*100,1),y_bot=round(ys.max()/h*100,1),y_c=round(np.average(ys,weights=rows_w[ys])/h*100,1),x0=round(cols_.min()/w*100,1),x1=round(cols_.max()/w*100,1),file=os.path.basename(fn)))
        else: cap.append(dict(word=wd['w'],t=round(t,2),y_c=None,file=os.path.basename(fn)))
    agg['captions']=cap
    agg['colour_json']=json.load(open(f'{M}/raw/{vid}/colour.json'))
    return k,agg
with ThreadPoolExecutor(4) as ex: res=dict(ex.map(do,IDS))
json.dump(res,open(f'{M}/sprint/S2-tools/look_stats.json','w'),indent=1,default=float)
for k,a in res.items():
    print(k,{q:(round(v,3) if isinstance(v,float) else v) for q,v in a.items() if q not in('captions','colour_json')})
    for c in a['captions']: print('  ',c)
    cj=a['colour_json']; print('  colour.json sat',cj.get('mean_saturation'),'bright',cj.get('mean_brightness'),'near_grey',cj.get('near_grey_pct'),'near_black',cj.get('near_black_pct'))
