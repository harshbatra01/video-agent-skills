"""Title graphics ('Title - Paula Radcliffe') per sequence: component list with key params (position, scale, h-scale, opacity, keyframe counts)."""
import sys, re
sys.path.insert(0, '.')
from build_project import Doc, TPS, for_claude_sequences, video_tracks


def comp_params(doc, cid):
    t = doc.raw(cid)
    name = re.search(r'<DisplayName>([^<]*)</DisplayName>', t); mn = re.search(r'<MatchName>([^<]*)</MatchName>', t)
    ps = {}
    for idx, pid in re.findall(r'<Param Index="(\d+)" ObjectRef="(\d+)"', t):
        p = doc.raw(pid)
        sk = re.search(r'<StartKeyframe>[^,]*,([^,]*),', p)
        kf = re.search(r'<Keyframes>([^<]*)</Keyframes>', p)
        nm = re.search(r'<Name>([^<]*)</Name>', p)
        ps[int(idx)] = (pid, nm.group(1) if nm else '', sk.group(1) if sk else None, len(kf.group(1).split(';')) - 1 if kf else 0)
    return (name.group(1) if name else '?'), (mn.group(1) if mn else '?'), ps


def titles(path):
    doc = Doc(path); out = {}
    for n, seq in for_claude_sequences(doc):
        key = seq.attrib['ObjectUID'][:8]
        for tr in video_tracks(doc, seq):
            raw = doc.raw(tr.attrib['ObjectUID'], uid=True)
            m = re.search(r'<ClipItems Version="\d+">\s*<TrackItems Version="1">(.*?)</TrackItems>', raw, re.S)
            for tid in (re.findall(r'ObjectRef="(\d+)"', m.group(1)) if m else []):
                t = doc.raw(tid); sub = re.search(r'<SubClip ObjectRef="(\d+)"', t)
                if not sub: continue
                nm = re.search(r'<Name>([^<]*)</Name>', doc.raw(sub.group(1)))
                if not nm or not nm.group(1).startswith('Title'): continue
                ch = re.search(r'<Components ObjectRef="(\d+)"', t).group(1)
                comps = re.findall(r'<Component Index="\d+" ObjectRef="(\d+)"', doc.raw(ch))
                out[key] = (tid, [(c,) + comp_params(doc, c) for c in comps])
    return doc, out


if __name__ == '__main__':
    doc, out = titles(sys.argv[1])
    for key, (tid, comps) in out.items():
        print('==', key, 'item', tid)
        for cid, dn, mn, ps in comps:
            short = {i: (v[1][:10], v[2][:24] if v[2] else None, v[3]) for i, v in ps.items() if i in (2, 3, 4, 5, 6, 7, 8)}
            print('   %s %-18s %-14s %s' % (cid, dn[:18], mn[-14:], short))
