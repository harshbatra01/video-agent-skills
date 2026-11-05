"""Audio tracks of one For-claude sequence: per item start/end, source name, clip Gain (dB), Volume Level (dB, static or keyframed), muted."""
import sys, re, json, math
sys.path.insert(0, '.')
from build_project import Doc, TPS, for_claude_sequences


def audio_tracks(doc, seq):
    for tg in seq.find('TrackGroups'):
        g = doc.deref(tg.find('Second'))
        if g.tag == 'AudioTrackGroup':
            return g, [doc.byuid[t.attrib['ObjectURef']] for t in g.find('.//Tracks')]
    return None, []


def lvl_db(v):
    v = float(v)
    return -999.0 if v <= 0 else round(20 * math.log10(v) + 15, 2)


def closure_text(doc, oid, depth=4):
    """raw text of an object plus objects it references (shallow), for regex scans"""
    seen = set(); out = []; todo = [(oid, 0)]
    while todo:
        k, d = todo.pop()
        if k in seen: continue
        seen.add(k)
        try: t = doc.raw(k)
        except KeyError: continue
        out.append(t)
        if d < depth:
            for r in re.findall(r'ObjectRef="(\d+)"', t): todo.append((r, d + 1))
    return '\n'.join(out)


def item_info(doc, tid):
    t = doc.raw(tid)
    s = int(re.search(r'<Start>(-?\d+)</Start>', t).group(1)) if '<Start>' in t else 0
    e = int(re.search(r'<End>(-?\d+)</End>', t).group(1))
    sub = re.search(r'<SubClip ObjectRef="(\d+)"', t)
    name = '?'; gain = None; tin = None
    if sub:
        st = doc.raw(sub.group(1))
        n = re.search(r'<Name>([^<]*)</Name>', st); name = n.group(1) if n else '?'
        c = re.search(r'<Clip ObjectRef="(\d+)"', st)
        if c:
            ct = doc.raw(c.group(1))
            g = re.search(r'<Gain>([^<]*)</Gain>', ct); gain = round(20 * math.log10(float(g.group(1))), 2) if g else 0.0
            ip = re.search(r'<InPoint>(-?\d+)</InPoint>', ct); tin = int(ip.group(1)) / TPS if ip else None
    comp = re.search(r'<Components ObjectRef="(\d+)"', t)
    levels = []
    if comp:
        ct = closure_text(doc, comp.group(1))
        for m in re.finditer(r'<AudioComponentParam [^>]*>(.*?)</AudioComponentParam>', ct, re.S):
            if '<Name>Level</Name>' in m.group(1):
                sk = re.search(r'<StartKeyframe>[^,]*,([^,]*),', m.group(1))
                kf = re.search(r'<Keyframes>([^<]*)</Keyframes>', m.group(1))
                levels.append((lvl_db(sk.group(1)) if sk else None, [(round(int(k.split(',')[0]) / TPS, 3), lvl_db(k.split(',')[1])) for k in kf.group(1).split(';') if k] if kf else None))
    tag = re.search(r'<Properties[^>]*>(.*?)</Properties>', t, re.S)
    es = 'dialog' if tag and 'dialog' in tag.group(1).lower() else ''
    return dict(start=round(s / TPS, 3), end=round(e / TPS, 3), name=name, gain_db=gain, src_in=tin, level=levels, muted='<IsMuted>true</IsMuted>' in t, es=es)


if __name__ == '__main__':
    doc = Doc(sys.argv[1]); want = sys.argv[2]
    for n, seq in for_claude_sequences(doc):
        if not seq.attrib['ObjectUID'].startswith(want): continue
        g, trs = audio_tracks(doc, seq)
        print(n, 'audio tracks:', len(trs))
        for k, tr in enumerate(trs):
            raw = doc.raw(tr.attrib['ObjectUID'], uid=True)
            m = re.search(r'<ClipItems Version="\d+">\s*<TrackItems Version="1">(.*?)</TrackItems>', raw, re.S)
            ids = re.findall(r'ObjectRef="(\d+)"', m.group(1)) if m else []
            print('A%d %s items %d' % (k + 1, tr.tag, len(ids)))
            for tid in ids:
                i = item_info(doc, tid)
                print('   %6.2f %6.2f gain %+.1f dB level %s %s %s %s' % (i['start'], i['end'], i['gain_db'] or 0, i['level'], i['es'], '[off]' if i['muted'] else '', i['name'][:40]))
