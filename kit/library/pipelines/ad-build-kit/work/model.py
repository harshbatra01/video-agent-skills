import numpy as np
LUMA=np.array([0.2126,0.7152,0.0722])
def slog3_decode(v):
    code=(64.0+np.asarray(v,np.float64)*876.0)            # 10-bit code from normalized video level
    hi=(10**((code-420.0)/261.5))*(0.18+0.01)-0.01
    lo=(code-95.0)*0.01125/(171.2102946929-95.0)
    return np.where(code>=171.2102946929,hi,lo)
XYZ2709=np.array([[3.2409699419,-1.5373831776,-0.4986107603],[-0.9692436363,1.8759675015,0.0415550574],[0.0556300797,-0.2039769589,1.0569715142]])
SG3C=np.array([[0.5990839208,0.2489255161,0.1024464902],[0.2150758201,0.8850685017,-0.1001443219],[-0.0320658495,-0.0276583907,1.1487819910]])
SG3=np.array([[0.7064827132,0.1288010498,0.1151721641],[0.2709796708,0.7866064112,-0.0575860820],[-0.0096778454,0.0046000375,1.0941355587]])
GAMUT={'sg3cine':XYZ2709@SG3C,'sg3':XYZ2709@SG3,'none':np.eye(3)}
class Curve:
    """shared monotone tone curve in log2 domain, piecewise linear."""
    def __init__(self,knots,vals): self.k=np.asarray(knots); self.v=np.asarray(vals)
    def __call__(self,x):
        lx=np.log2(np.maximum(x,1e-5)); return np.interp(lx,self.k,self.v)
def fit_curve(x,y,knots):
    lx=np.log2(np.maximum(x,1e-5)).ravel(); y=y.ravel()
    vals=[]
    # least squares piecewise-linear (hat basis) fit
    K=len(knots); A=np.zeros((len(lx),K))
    idx=np.clip(np.searchsorted(knots,lx)-1,0,K-2)
    f=np.clip((lx-knots[idx])/(knots[idx+1]-knots[idx]),0,1)
    A[np.arange(len(lx)),idx]=1-f; A[np.arange(len(lx)),idx+1]=f
    # small smoothness regularization
    D=np.diff(np.eye(K),2,axis=0)*0.02*np.sqrt(len(lx)/K)
    sol=np.linalg.lstsq(np.vstack([A,D]),np.concatenate([y,np.zeros(len(D))]),rcond=None)[0]
    sol=np.maximum.accumulate(sol)   # enforce monotone
    return Curve(knots,sol)
def luma(a): return a@LUMA
class GradeModel:
    """raw VLC RGB -> predicted Premiere output. Per-ad knobs: dEV (stops), wb gains (r,b relative)."""
    def __init__(self,gamut,wb,G,satk=None,satv=None,post=None):
        self.M=GAMUT[gamut]; self.wb=np.asarray(wb); self.G=G; self.satk=satk; self.satv=satv; self.post=post
    def scene(self,raw,dEV=0.0,wbadj=(1,1,1)):
        l=slog3_decode(raw)@self.M.T
        return l*self.wb*np.asarray(wbadj)*(2.0**np.asarray(dEV))[...,None] if np.ndim(dEV) else l*self.wb*np.asarray(wbadj)*(2.0**dEV)
    def __call__(self,raw,dEV=0.0,wbadj=(1,1,1)):
        y=self.G(self.scene(raw,dEV,wbadj))
        if self.post is not None: y=y@self.post.T
        if self.satk is not None:
            Y=luma(y)[...,None]; k=np.interp(Y[...,0],self.satk,self.satv)[...,None]
            y=Y+k*(y-Y)
        return np.clip(y,0,1)
