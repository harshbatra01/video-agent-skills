"""timeline summary per For-claude sequence: every track item (video, captions) with start/end/name/muted"""
import sys, re, json
sys.path.insert(0, '.')
from build_project import Doc, TPS, for_claude_sequences, video_tracks, track_items
from build_v4 import caption_tracks, caption_items
def name_of(doc, ti):
    t = doc.raw(ti)
    m = re.search(r'<SubClip ObjectRef="(\d+)"', t)
    if not m: return '?'
    n = re.search(r'<Name>([^<]*)</Name>', doc.raw(m.group(1)))
    return n.group(1) if n else '?'
def times(doc, ti):
    t = doc.raw(ti)
    s = re.search(r'<Start>(-?\d+)</Start>', t); e = re.search(r'<End>(-?\d+)</End>', t)
    return (int(s.group(1)) if s else 0) / TPS, int(e.group(1)) / TPS
out = {}
doc = Doc(sys.argv[1])
for n, seq in for_claude_sequences(doc):
    key = seq.attrib['ObjectUID'][:8]; tr_out = []
    for k, tr in enumerate(video_tracks(doc, seq)):
        items = []
        for it in track_items(doc, tr):
            tid = it.attrib['ObjectID']; s, e = times(doc, tid)
            items.append([round(s, 3), round(e, 3), name_of(doc, tid), '<IsMuted>true</IsMuted>' in doc.raw(tid)])
        tr_out.append(sorted(items))
    caps = []
    for ctr in caption_tracks(doc, seq):
        for cid, cs, ce in caption_items(doc, ctr):
            caps.append([round(cs, 3), round(ce, 3), '<IsMuted>true</IsMuted>' in doc.raw(cid)])
    out[key] = dict(name=n, video=tr_out, caps=sorted(caps))
json.dump(out, open(sys.argv[2], 'w'), indent=0)
print('ok', len(out))
