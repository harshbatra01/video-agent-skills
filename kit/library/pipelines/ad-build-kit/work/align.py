import numpy as np, json
from PIL import Image
def load(f): return np.asarray(Image.open(f).convert('RGB')).astype(np.float32)/255.0
def gray(a): return a@np.array([0.2126,0.7152,0.0722],np.float32)
def down(a,k):
    h,w=a.shape[:2]; h2,w2=h//k,w//k
    return a[:h2*k,:w2*k].reshape(h2,k,w2,k,*a.shape[2:]).mean((1,3))
def bilinear(img, xs, ys):
    h,w=img.shape[:2]
    x0=np.clip(np.floor(xs).astype(int),0,w-2); y0=np.clip(np.floor(ys).astype(int),0,h-2)
    fx=np.clip(xs-x0,0,1); fy=np.clip(ys-y0,0,1)
    if img.ndim==3: fx=fx[...,None]; fy=fy[...,None]
    return (img[y0,x0]*(1-fx)*(1-fy)+img[y0,x0+1]*fx*(1-fy)+img[y0+1,x0]*(1-fx)*fy+img[y0+1,x0+1]*fx*fy)
def grad(g):
    gx=np.zeros_like(g); gy=np.zeros_like(g)
    gx[:,1:-1]=g[:,2:]-g[:,:-2]; gy[1:-1]=g[2:]-g[:-2]
    return np.sqrt(gx*gx+gy*gy)
def ref_to_raw(u,v,Z,px,dx=0,dy=0,H='pad',S=0.57):
    """u,v: reference pixel coords (full 1080x1920). returns raw pixel coords in VLC image."""
    up=540+(u-540)/Z; vp=960+(v-960)/Z
    X=3024+(up-px*1080)/S+dx; Y=1704+(vp-960)/S+dy
    if H=='stretch': Y=Y*3426/3408
    return X,Y
def ncc(a,b,m):
    a=a[m]; b=b[m]; a=a-a.mean(); b=b-b.mean()
    return float((a*b).sum()/np.sqrt((a*a).sum()*(b*b).sum()+1e-12))
def valid_mask(shape_uv, u, v):
    m=(u>60)&(u<1020)&(v>80)&(v<1840)
    m&=~((v>860)&(v<1080))   # caption band
    return m
def match(ref, raws, px, k=8, Zs=None, H_list=('pad','stretch')):
    """ref: full-res ref image; raws: list of full-res raw images. coarse search at factor k."""
    Zs=Zs if Zs is not None else np.arange(1.0,1.62,0.01)
    rg=grad(down(gray(ref),k))
    hh,ww=rg.shape
    v,u=np.mgrid[0:hh,0:ww].astype(np.float32); u=(u+0.5)*k; v=(v+0.5)*k
    m=valid_mask(rg.shape,u,v)
    best=(-1,)
    for ri,raw in enumerate(raws):
        sg=grad(down(gray(raw),k))
        for H in H_list:
            for Z in Zs:
                for dx in (-16,0,16):
                    for dy in (-16,0,16):
                        X,Y=ref_to_raw(u,v,Z,px,dx,dy,H)
                        s=bilinear(sg,X/k-0.5,Y/k-0.5)
                        c=ncc(rg,s,m)
                        if c>best[0]: best=(c,ri,H,float(Z),dx,dy)
    return best
def refine(ref, raw, px, H, Z0, dx0, dy0, k=2):
    rg=grad(down(gray(ref),k)); hh,ww=rg.shape
    v,u=np.mgrid[0:hh,0:ww].astype(np.float32); u=(u+0.5)*k; v=(v+0.5)*k
    m=valid_mask(rg.shape,u,v)
    sg=grad(down(gray(raw),k))
    best=(-1,)
    for Z in np.arange(Z0-0.012,Z0+0.0121,0.002):
        for dx in range(dx0-16,dx0+17,4):
            for dy in range(dy0-16,dy0+17,4):
                X,Y=ref_to_raw(u,v,Z,px,dx,dy,H)
                c=ncc(rg,bilinear(sg,X/k-0.5,Y/k-0.5),m)
                if c>best[0]: best=(c,float(Z),dx,dy)
    return best
