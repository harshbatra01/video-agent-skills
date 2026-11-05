import sys, os, json, hashlib, re
os.environ['PRX']=sys.argv[1]
exec(open('captions.py').read()); exec(open('fcseqs.py').read())
sys.path.insert(0,'../work'); import broll_plan
F60=4233600000
def lumvals(ce):
    ps=[deref(p) for p in ce.find('.//Params')]
    v={i:ps[i].findtext('StartKeyframe').split(',')[1] for i in (14,15,16,19,20,21,22,23,24,41,42,110)}
    blobs=tuple(p.find('StartKeyframeValue').attrib.get('BinaryHash') for p in ps if p.tag=='ArbVideoComponentParam')
    return v, hashlib.md5(str(blobs).encode()).hexdigest()[:6], ce.find('SubComponents') is not None
def fp_track(tr):
    items=tr.find('.//ClipItems/TrackItems'); out=[]
    for it in (items if items is not None else []):
        ti=deref(it); sc=deref(ti.find('.//SubClip')); vc=deref(sc.find('Clip'))
        out.append((ti.findtext('.//TrackItem/Start') or '0', ti.findtext('.//TrackItem/End'), sc.findtext('Name'), vc.findtext('.//InPoint'), vc.findtext('.//OutPoint'), [n for n,_ in effects(ti)]))
    return out
res={}
for nm,seq,mc in fc_seqs():
    key=seq.attrib['ObjectUID'][:8]; vg,trs=vtracks(seq)
    caps=hashlib.md5(json.dumps(seq_captions(seq)).encode()).hexdigest()[:8]
    audio=[]
    for tg in seq.find('TrackGroups'):
        g=deref(tg.find('Second'))
        if g.tag=='AudioTrackGroup':
            for t in g.find('.//Tracks'):
                tr=byuid[t.attrib['ObjectURef']]; items=tr.find('.//ClipItems/TrackItems')
                audio.append([(deref(i).findtext('.//TrackItem/Start'),deref(i).findtext('.//TrackItem/End')) for i in (items if items is not None else [])])
    res[key]={'name':seq.findtext('Name'),'ntracks':len(trs),'captions':caps,'audio':hashlib.md5(json.dumps(audio).encode()).hexdigest()[:8],
              'tracks':[fp_track(t) for t in trs],'nexttrack':vg.findtext('.//NextTrackID')}
    # deep details for grade/broll
    det=[]
    for ti_,tr in enumerate(trs):
        items=tr.find('.//ClipItems/TrackItems')
        for it in (items if items is not None else []):
            ti=deref(it); d={'track':ti_+1,'start':int(ti.findtext('.//TrackItem/Start') or 0),'end':int(ti.findtext('.//TrackItem/End'))}
            sc=deref(ti.find('.//SubClip')); vc=deref(sc.find('Clip')); d['name']=sc.findtext('Name'); d['in']=int(vc.findtext('.//InPoint') or 0); d['out']=int(vc.findtext('.//OutPoint') or 0)
            d['mc']=sc.find('MasterClip').attrib['ObjectURef']; d['src']=deref(vc.find('.//Source')).attrib.get('ObjectID')
            d['fx']=[]
            for n,ce in effects(ti):
                if n=='Lumetri Color': d['fx'].append(('Lumetri',)+lumvals(ce))
                elif n=='Motion':
                    mv={deref(p).findtext('Name'):deref(p).findtext('StartKeyframe').split(',')[1] for p in ce.find('.//Params') if deref(p).findtext('Name') in ('Position','Scale')}
                    d['fx'].append(('Motion',mv))
                else: d['fx'].append((n,))
            det.append(d)
    res[key]['detail']=det
json.dump(res,open(sys.argv[2],'w'),default=str,indent=0)
