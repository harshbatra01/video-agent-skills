"""Title v2 checks: only the title graphics' layers changed; new layers decode as designed."""
import sys, re, json, base64, struct
sys.path.insert(0, '.')
from build_project import Doc, TPS, for_claude_sequences, video_tracks, track_items
sys.path.insert(0, '../work')
import gfx_plan

old = Doc(sys.argv[1]); new = Doc(sys.argv[2])
ok = True


def fail(*a):
    global ok
    ok = False
    print('  FAIL', *a)


def params(doc, cid):
    out = []
    for pid in re.findall(r'<Param Index="\d+" ObjectRef="(\d+)"', doc.raw(cid)):
        pt = doc.raw(pid)
        sk = re.search(r'<StartKeyframe>([^<]*)<', pt); kf = re.search(r'<Keyframes>([^<]*)<', pt); bh = re.search(r'BinaryHash="([^"]+)"', pt)
        nm = re.search(r'<Name>([^<]*)</Name>', pt)
        out.append((nm.group(1) if nm else None, sk.group(1) if sk else None, kf.group(1) if kf else None, bh.group(1) if bh else None))
    return out


def blob(doc, h):
    m = re.search(r'BinaryHash="%s">([^<]+)<' % re.escape(h), doc.txt)
    return base64.b64decode(m.group(1))


def item_sig(doc, it):
    t = doc.raw(it.attrib['ObjectID'])
    s = re.search(r'<Start>(\d+)</Start>', t); e = int(re.search(r'<End>(\d+)</End>', t).group(1))
    sc = re.search(r'<SubClip ObjectRef="(\d+)"', t).group(1); st = doc.raw(sc)
    vc = re.search(r'<Clip ObjectRef="(\d+)"', st).group(1); vt = doc.raw(vc)
    ch = re.search(r'<Components ObjectRef="(\d+)"', t).group(1)
    comps = re.findall(r'<Component Index="\d+" ObjectRef="(\d+)"', doc.raw(ch))
    fx = []
    for c in comps:
        ps = params(doc, c)
        # blob hashes can be renamed by Premiere; compare decoded content instead
        ps = tuple((n, sk, kf, (blob(doc, h) if h and re.search(r'BinaryHash="%s">' % re.escape(h), doc.txt) else h)) for n, sk, kf, h in ps)
        fx.append((re.search(r'<MatchName>([^<]*)<', doc.raw(c)).group(1), ps))
    name = re.search(r'<Name>([^<]*)</Name>', st).group(1)
    return dict(start=int(s.group(1)) if s else 0, end=e, name=name, tin=re.search(r'<InPoint>(-?\d+)<', vt).group(1),
                tout=re.search(r'<OutPoint>(-?\d+)<', vt).group(1), fx=fx, comps=comps)


def tracks_sig(doc, seq):
    return [[item_sig(doc, it) for it in track_items(doc, tr)] for tr in video_tracks(doc, seq)]


os_ = {s.attrib['ObjectUID'][:8]: s for n, s in for_claude_sequences(old)}
ns_ = {s.attrib['ObjectUID'][:8]: s for n, s in for_claude_sequences(new)}
for key in os_:
    so, sn = os_[key], ns_[key]
    print('==', key, sn.findtext('Name')[:44])
    A, B = tracks_sig(old, so), tracks_sig(new, sn)
    if len(A) != len(B): fail('track count'); continue
    n_title = 0
    for ti, (ta, tb) in enumerate(zip(A, B)):
        if len(ta) != len(tb): fail('item count on V%d' % (ti + 1)); continue
        for a, b in zip(ta, tb):
            same_frame = all(a[k] == b[k] for k in ('start', 'end', 'name', 'tin', 'tout'))
            if not same_frame: fail('item timing/name changed on V%d: %s' % (ti + 1, a['name']))
            if a['name'] == 'Title - Paula Radcliffe':
                n_title += 1
                kinds = [f[0].replace('AE.ADBE ', '') for f in b['fx']]
                if kinds != ['Text', 'Text', 'Shape', 'Shape']: fail('title layers', kinds)
                texts = []
                for mn, ps in b['fx']:
                    if mn == 'AE.ADBE Text':
                        raw = ps[0][3]; n = struct.unpack_from('<Q', raw, 0)[0]
                        if n != len(raw) - 8: fail('text blob length')
                        d = json.loads(raw[8:].decode('utf-16-le'))['mTextParam']['mStyleSheet']
                        texts.append((d['mText'], d['mFontName']['mParamValues'][0][1], d['mFontSize']['mParamValues'][0][1], hex(d['mFillColor']['mParamValues'][0][1])))
                    else:
                        app = json.loads(ps[1][3][8:].decode('utf-16-le'))['mStyle']
                        texts.append(('shape', hex(app['mFillColor']), 'stroke' if app['mStrokeVisible'] else '-'))
                if texts[1][0] != gfx_plan.TITLE[key]['sub']: fail('subtitle', texts[1][0])
                print('   title %.2f-%.2f  %s' % (b['start'] / TPS, b['end'] / TPS, texts))
            elif a['fx'] != b['fx']:
                fail('effects changed on V%d item %s' % (ti + 1, a['name']))
    if n_title != 1: fail('titles found', n_title)
    # captions + audio untouched
    for tag in ('DataTrackGroup', 'AudioTrackGroup'):
        go = [old.deref(tg.find('Second')) for tg in so.find('TrackGroups') if old.deref(tg.find('Second')).tag == tag][0]
        gn = [new.deref(tg.find('Second')) for tg in sn.find('TrackGroups') if new.deref(tg.find('Second')).tag == tag][0]
        if old.raw(go.attrib['ObjectID']) != new.raw(gn.attrib['ObjectID']): fail(tag, 'changed')
        for t in go.find('.//Tracks'):
            if old.raw(t.attrib['ObjectURef'], uid=True) != new.raw(t.attrib['ObjectURef'], uid=True): fail(tag, 'track changed')
print('\nALL CHECKS PASSED' if ok else '\nSOME CHECKS FAILED')
