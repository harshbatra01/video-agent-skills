"""Semantic checks for the zoom + graphics build against the user's saved project."""
import sys, re, json, base64, struct
sys.path.insert(0, '.')
from build_project import Doc, TPS, for_claude_sequences, video_tracks, track_items
sys.path.insert(0, '../work')
import zoom_plan, gfx_plan

old = Doc(sys.argv[1]); new = Doc(sys.argv[2])
ADJ_IN = 914457600000000
ok = True


def fail(*a):
    global ok
    ok = False
    print('  FAIL', *a)


def item_sig(doc, it):
    t = doc.raw(it.attrib['ObjectID'])
    s = re.search(r'<Start>(\d+)</Start>', t); e = int(re.search(r'<End>(\d+)</End>', t).group(1))
    sc = re.search(r'<SubClip ObjectRef="(\d+)"', t).group(1); st = doc.raw(sc)
    vc = re.search(r'<Clip ObjectRef="(\d+)"', st).group(1); vt = doc.raw(vc)
    ch = re.search(r'<Components ObjectRef="(\d+)"', t).group(1)
    fx = []
    for c in re.findall(r'<Component Index="\d+" ObjectRef="(\d+)"', doc.raw(ch)):
        ct = doc.raw(c)
        vals = []
        for pid in re.findall(r'<Param Index="\d+" ObjectRef="(\d+)"', ct):
            pt = doc.raw(pid)
            sk = re.search(r'<StartKeyframe>([^<]*)<', pt); kf = re.search(r'<Keyframes>([^<]*)<', pt); bh = re.search(r'BinaryHash="([^"]+)"', pt)
            vals.append((sk.group(1) if sk else None, kf.group(1) if kf else None, bh.group(1) if bh else None))
        fx.append((re.search(r'<MatchName>([^<]*)<', ct).group(1), tuple(vals)))
    return (int(s.group(1)) if s else 0, e, re.search(r'<Name>([^<]*)</Name>', st).group(1),
            re.search(r'<InPoint>(-?\d+)<', vt).group(1), re.search(r'<OutPoint>(-?\d+)<', vt).group(1), '<IsMuted>true' in t, tuple(fx))


def keys(ptxt):
    kf = re.search(r'<Keyframes>([^<]*)<', ptxt)
    out = []
    for k in kf.group(1).split(';'):
        if not k: continue
        f = k.split(','); out.append((int(f[0]), float(f[1].rstrip('.') or 0) if ':' not in f[1] else f[1]))
    return out


def val_at(ks, t):
    """value at a key time (or held before/after); boundaries are key times so this is exact there"""
    if t <= ks[0][0]: return ks[0][1]
    if t >= ks[-1][0]: return ks[-1][1]
    for (t0, v0), (t1, v1) in zip(ks, ks[1:]):
        if t0 <= t <= t1:
            if t == t0: return v0
            if t == t1: return v1
            return v0 + (v1 - v0) * (t - t0) / (t1 - t0)      # rough (linear) for mid points


def blob_text(doc, h):
    m = re.search(r'BinaryHash="%s">([^<]+)<' % re.escape(h), doc.txt)
    raw = base64.b64decode(m.group(1))
    n = struct.unpack_from('<Q', raw, 0)[0]
    assert n == len(raw) - 8, 'blob length header'
    return json.loads(raw[8:].decode('utf-16-le'))


oseqs = {s.attrib['ObjectUID'][:8]: s for n, s in for_claude_sequences(old)}
nseqs = {s.attrib['ObjectUID'][:8]: s for n, s in for_claude_sequences(new)}
for key in oseqs:
    so, sn = oseqs[key], nseqs[key]
    print('==', key, sn.findtext('Name')[:40])
    to, tn = video_tracks(old, so), video_tracks(new, sn)
    # track indices consistent with the group order
    for i, tr in enumerate(tn):
        idx = set(re.findall(r'<Index>(\d+)</Index>', new.raw(tr.attrib['ObjectUID'], uid=True)))
        if idx != {str(i)}: fail('track %d index fields %s' % (i, idx))
    zoomed = key in zoom_plan.ZOOM
    mapping = {0: 0, 1: 2, 2: 3} if zoomed else {i: i for i in range(len(to))}
    exp_n = len(to) + (2 if zoomed else 1)
    if len(tn) != exp_n: fail('track count %d expected %d' % (len(tn), exp_n))
    for oi, ni in mapping.items():
        a = [item_sig(old, it) for it in track_items(old, to[oi])]; b = [item_sig(new, it) for it in track_items(new, tn[ni])]
        if a != b: fail('track V%d -> V%d changed' % (oi + 1, ni + 1))
    # captions / audio untouched (compare raw text of data + audio track objects)
    for tag in ('DataTrackGroup', 'AudioTrackGroup'):
        go = [old.deref(tg.find('Second')) for tg in so.find('TrackGroups') if old.deref(tg.find('Second')).tag == tag][0]
        gn = [new.deref(tg.find('Second')) for tg in sn.find('TrackGroups') if new.deref(tg.find('Second')).tag == tag][0]
        if old.raw(go.attrib['ObjectID']) != new.raw(gn.attrib['ObjectID']): fail(tag, 'changed')
        for t in go.find('.//Tracks'):
            u = t.attrib['ObjectURef']
            if old.raw(u, uid=True) != new.raw(u, uid=True): fail(tag, 'track changed')
    seq_end = max(int(t.findtext('.//TrackItem/End')) for t in track_items(new, tn[0]))
    # ---- zooms
    if zoomed:
        zi = track_items(new, tn[1]); t = 0; prev_end = None; mx = 0
        spec = zoom_plan.ZOOM[key]
        for it in zi:
            s, e, name, tin, tout, muted, fx = item_sig(new, it)
            if s != t: fail('zoom gap/overlap at %.3f' % (s / TPS))
            t = e
            if int(tin) != ADJ_IN or int(tout) != ADJ_IN + (e - s): fail('zoom in/out points')
            if len(fx) != 2 or any(f[0] != 'AE.ADBE Geometry2' for f in fx): fail('zoom chain', [f[0] for f in fx])
            ch = re.search(r'<Components ObjectRef="(\d+)"', new.raw(it.attrib['ObjectID'])).group(1)
            prods = []
            for when in (ADJ_IN, ADJ_IN + (e - s)):
                p = 1.0
                for c in re.findall(r'<Component Index="\d+" ObjectRef="(\d+)"', new.raw(ch)):
                    ct = new.raw(c)
                    for pid in re.findall(r'<Param Index="\d+" ObjectRef="(\d+)"', ct):
                        pt = new.raw(pid)
                        if '<Name>Scale Height</Name>' in pt: p *= val_at(keys(pt), when) / 100
                        if '<Name>Anchor Point</Name>' in pt or '<Name>Position</Name>' in pt:
                            v = re.search(r'<StartKeyframe>-?\d+,([^,]+),', pt).group(1)
                            if v != '%s:%s' % (repr(float(spec['anchor'][0])), repr(float(spec['anchor'][1]))): fail('anchor', v)
                        if '<Name>Sampling</Name>' in pt and ',1,' not in re.search(r'<StartKeyframe>([^<]*)<', pt).group(1) + ',': fail('sampling')
                prods.append(p)
            mx = max(mx, *prods)
            if prev_end is not None and abs(prods[0] - prev_end) > 0.004: fail('zoom jump at %.3f: %.4f -> %.4f' % (s / TPS, prev_end, prods[0]))
            prev_end = prods[1]
            print('   zoom %6.3f-%6.3f  %5.1f%% -> %5.1f%%' % (s / TPS, e / TPS, prods[0] * 100, prods[1] * 100))
        if t != seq_end: fail('zooms end at %.3f not %.3f' % (t / TPS, seq_end / TPS))
        if mx > 1.25: fail('zoom too tight: %.3f' % mx)
    # ---- graphics
    gi = track_items(new, tn[-1])
    exp = 2 if key in gfx_plan.CODE else 1
    if len(gi) != exp: fail('graphics count', len(gi))
    for it in gi:
        s, e, name, tin, tout, muted, fx = item_sig(new, it)
        texts = []
        for mn, vals in fx:
            if mn == 'AE.ADBE Text':
                d = blob_text(new, vals[0][2])
                ss = d['mTextParam']['mStyleSheet']
                texts.append((ss['mText'], ss['mFontName']['mParamValues'][0][1], ss['mFontSize']['mParamValues'][0][1]))
            elif mn == 'AE.ADBE Shape':
                blob_text(new, vals[1][2])       # appearance decodes
        print('   gfx  %6.3f-%6.3f  %-26s %s' % (s / TPS, e / TPS, name, texts))
        if name.startswith('Code') and e != seq_end: fail('code does not run to the end')
print('\nALL CHECKS PASSED' if ok else '\nSOME CHECKS FAILED')
