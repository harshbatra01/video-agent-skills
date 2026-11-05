"""v3 semantic diff vs the user's save: list every changed item per track; captions/audio must be identical."""
import sys, re, json
sys.path.insert(0, '.')
from build_project import Doc, TPS, for_claude_sequences, video_tracks, track_items

old = Doc(sys.argv[1]); new = Doc(sys.argv[2])


def sig(doc, it):
    t = doc.raw(it.attrib['ObjectID'])
    s = re.search(r'<Start>(\d+)</Start>', t); e = int(re.search(r'<End>(\d+)</End>', t).group(1))
    sc = re.search(r'<SubClip ObjectRef="(\d+)"', t).group(1); st = doc.raw(sc)
    vc = re.search(r'<Clip ObjectRef="(\d+)"', st).group(1); vt = doc.raw(vc)
    ch = re.search(r'<Components ObjectRef="(\d+)"', t).group(1)
    fx = []
    for c in re.findall(r'<Component Index="\d+" ObjectRef="(\d+)"', doc.raw(ch)):
        ct = doc.raw(c); mn = re.search(r'<MatchName>([^<]*)<', ct).group(1)
        vals = []
        for pid in re.findall(r'<Param Index="\d+" ObjectRef="(\d+)"', ct):
            pt = doc.raw(pid); sk = re.search(r'<StartKeyframe>-?\d+,([^,]*),', pt); kf = re.search(r'<Keyframes>([^<]*)<', pt)
            vals.append((sk.group(1) if sk else None, kf.group(1)[:40] if kf else None))
        fx.append((mn.replace('AE.ADBE ', ''), tuple(vals)))
    return (round((int(s.group(1)) if s else 0) / TPS, 3), round(e / TPS, 3), re.search(r'<Name>([^<]*)</Name>', st).group(1)[:28],
            round(int(re.search(r'<InPoint>(-?\d+)<', vt).group(1)) / TPS, 3), tuple(fx))


ok = True
os_ = {s.attrib['ObjectUID'][:8]: s for n, s in for_claude_sequences(old)}
ns_ = {s.attrib['ObjectUID'][:8]: s for n, s in for_claude_sequences(new)}
for key in os_:
    so, sn = os_[key], ns_[key]
    to, tn = video_tracks(old, so), video_tracks(new, sn)
    if len(to) != len(tn): print(key, 'TRACK COUNT CHANGED'); ok = False
    print('==', key, sn.findtext('Name')[:40])
    for i, (a, b) in enumerate(zip(to, tn)):
        A = [sig(old, it) for it in track_items(old, a)]; B = [sig(new, it) for it in track_items(new, b)]
        if A == B: continue
        changed = []
        for x, y in zip(A, B):
            if x != y:
                what = []
                if x[:4] != y[:4]: what.append('%s %.2f-%.2f in %.2f -> %s %.2f-%.2f in %.2f' % (x[2], x[0], x[1], x[3], y[2], y[0], y[1], y[3]))
                if x[4] != y[4]:
                    fx_x = [f[0] for f in x[4]]; fx_y = [f[0] for f in y[4]]
                    what.append('fx %s -> %s' % (fx_x, fx_y) if fx_x != fx_y else 'fx values (%s)' % ','.join(f[0] for f, g in zip(x[4], y[4]) if f != g))
                changed.append('; '.join(what))
        if len(A) != len(B): changed.append('count %d -> %d' % (len(A), len(B)))
        print('   V%d: %d of %d items changed: %s' % (i + 1, len(changed), len(A), ' | '.join(changed[:3]) + (' ...' if len(changed) > 3 else '')))
    for tag in ('DataTrackGroup', 'AudioTrackGroup'):
        go = [old.deref(tg.find('Second')) for tg in so.find('TrackGroups') if old.deref(tg.find('Second')).tag == tag][0]
        gn = [new.deref(tg.find('Second')) for tg in sn.find('TrackGroups') if new.deref(tg.find('Second')).tag == tag][0]
        same = old.raw(go.attrib['ObjectID']) == new.raw(gn.attrib['ObjectID']) and all(
            old.raw(t.attrib['ObjectURef'], uid=True) == new.raw(t.attrib['ObjectURef'], uid=True) for t in go.find('.//Tracks'))
        if not same: print('   %s CHANGED' % tag); ok = False
print('CAPTIONS+AUDIO UNCHANGED' if ok else 'PROBLEM')
