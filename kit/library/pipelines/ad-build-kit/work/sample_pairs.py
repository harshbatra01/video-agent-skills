import sys, json, numpy as np, time
sys.path.insert(0,'.')
from align import *
PX=0.48148149251937866
al=json.load(open('calib/align.json'))
FACE_C=(557,475); FACE_AX=(157+150,189+150)   # ellipse + feather margin
B=12  # block size in ref pixels
allp=[]
for t,d in al.items():
    t0=time.time()
    ref=load(d['ref']); raw=load(d['raw']); H='stretch'
    # refine around stored solution at k=4, stretch hypothesis
    k=4; rg=grad(down(gray(ref),k)); hh,ww=rg.shape
    v,u=np.mgrid[0:hh,0:ww].astype(np.float32); u=(u+0.5)*k; v=(v+0.5)*k; m=valid_mask(rg.shape,u,v)
    sg=grad(down(gray(raw),k)); best=(-1,)
    for Z in np.arange(d['Z']-0.01,d['Z']+0.0101,0.002):
        for dx in range(d['dx']-12,d['dx']+13,4):
            for dy in range(d['dy']-16,d['dy']+17,4):
                X,Y=ref_to_raw(u,v,Z,PX,dx,dy,H)
                c=ncc(rg,bilinear(sg,X/k-0.5,Y/k-0.5),m)
                if c>best[0]: best=(c,float(Z),dx,dy)
    c,Z,dx,dy=best
    # sample raw at every ref pixel from a 2x-downsampled raw (approximates Premiere's area-averaging downscale)
    raw2=down(raw,2)
    V,U=np.mgrid[0:1920,0:1080].astype(np.float32)
    X,Y=ref_to_raw(U+0.5,V+0.5,Z,PX,dx,dy,H)
    rs=bilinear(raw2,X/2-0.5,Y/2-0.5)
    # block stats
    def blocks(a): return a[:1920//B*B,:1080//B*B].reshape(1920//B,B,1080//B,B,-1).mean((1,3))
    rb=blocks(ref); sb=blocks(rs)
    rstd=ref[:1920//B*B,:1080//B*B].reshape(1920//B,B,1080//B,B,3).std((1,3)).mean(-1)
    sstd=rs[:1920//B*B,:1080//B*B].reshape(1920//B,B,1080//B,B,3).std((1,3)).mean(-1)
    by,bx=np.mgrid[0:1920//B,0:1080//B]; cu=(bx+0.5)*B; cv=(by+0.5)*B
    keep=(cu>70)&(cu<1010)&(cv>90)&(cv<1830)&~((cv>860)&(cv<1080))
    keep&=((cu-FACE_C[0])/FACE_AX[0])**2+((cv-FACE_C[1])/FACE_AX[1])**2>1
    keep&=(rstd<0.03)&(sstd<0.02)
    exp=1.0 if float(t)<17.05 else 0.7
    for (yy,xx) in zip(*np.nonzero(keep)):
        allp.append([float(t),exp,float(cu[yy,xx]),float(cv[yy,xx]),*map(float,sb[yy,xx]),*map(float,rb[yy,xx])])
    print(t,'ncc %.3f Z %.4f dx %d dy %d  blocks kept %d  %.0fs'%(c,Z,dx,dy,int(keep.sum()),time.time()-t0),flush=True)
np.save('calib/pairs.npy',np.array(allp,np.float32))
print('total pairs',len(allp))
