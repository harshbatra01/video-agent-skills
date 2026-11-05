"""v4 on top of the user's v3 save (after Premiere imported the gfx_v1 renders):
titles retimed, C137 hand-place shots -> C132 pouch slide, 1 star stock swap, 3 questions veg shot out (grade extended),
optional late-grade tint fix, AE overlays on new top tracks, captions under overlays removed.
usage: python build_v4.py in.xml out.prproj [--no-overlays]"""
import sys, re, json, gzip, uuid
sys.path.insert(0, '.')
from build_project import Doc, TPS, fmt, for_claude_sequences, video_tracks, track_items
from build_broll import strip_inline, clone_component, chain_components, clone_chain, set_track_items, set_inout
from build_ext import set_times2, delete_obj, component_ids, delete_item, item_times, retime_item, ext_item
import build_zoom_gfx as Z
from build_title_v2 import inline_blobs
from build_v3 import title_B, item_name, lumetri_ids, set_lumetri, TITLE_NAME, TITLE_Y, TITLE_Y_DEFAULT, STOCK_GRADE
import gfx_plan

F60, F25 = 4233600000, 10160640000
def tk(sec): return int(round(sec * 60)) * F60

TITLE_TIME = {'f233433f': (0.4, 2.8), '974102f7': (0.4, 3.4), '593f11c4': (1.3, 5.8)}
SWAP_TO_C132 = [('348e0ba6', 13.40, 12.6), ('0991faf2', 13.25, 30.0)]          # (ad, B-roll start, C132 source s)
STOCK_SWAP = [('cd03e189', 14.98, 'hands_pills-poured-into-hand_pexels-6801319_2160x3840.mp4', 1.0)]
REMOVE = [('974102f7', 4.68, 'veg-closeup')]                                   # grade piece before it is extended over the gap
LATE_TINT = {'974102f7': (35.0, {19: 0.62, 14: 6.0, 15: -18.0, 20: 26.0})}   # 3 questions: light changes from 35 s (flatter, pink-lavender shadows)
# overlays: name -> (ad, start s or ('broll', start s), caption removal)
OVER = [
    ('i52_powders', '348e0ba6', ('broll', 9.08)), ('i52_pills', '348e0ba6', ('broll', 10.37)), ('i52_shakes', '348e0ba6', ('broll', 11.12)),
    ('s1_pouch', 'cd03e189', ('broll', 6.45)), ('s1_pills', 'cd03e189', ('broll', 14.98)), ('s1_scoop', 'cd03e189', ('broll', 17.07)), ('s1_water', 'cd03e189', ('broll', 19.32)),
    ('tt_100', 'f233433f', ('broll', 38.03)),
    ('q3_q1', '974102f7', 3.45), ('q3_news', '974102f7', 8.15), ('q3_q2', '974102f7', 18.55), ('q3_q3', '974102f7', 29.55), ('q3_since', '974102f7', 41.45),
    ('tt_p1', 'f233433f', 3.55), ('tt_meter', 'f233433f', 9.40), ('tt_p2', 'f233433f', 14.40), ('tt_dict', 'f233433f', 16.55),
    ('tt_p3', 'f233433f', 27.60), ('tt_ring', 'f233433f', 31.70), ('tt_since', 'f233433f', 42.55),
    ('sw_1998', '593f11c4', 0.0), ('hr_17', '404c5cb2', 1.45), ('rp_20', '0991faf2', 1.00), ('rp_16', '0991faf2', 4.30),
]


def find_master(doc, name):
    for e in doc.root:
        if e.tag != 'ClipProjectItem' or e.findtext('.//ProjectItem/Name') != name: continue
        mc = doc.deref(e.find('MasterClip'))
        vc = [doc.deref(c) for c in mc.find('Clips') if doc.deref(c).tag == 'VideoClip'][0]
        vt = doc.raw(vc.attrib['ObjectID'])
        src = doc.raw(re.search(r'<Source ObjectRef="(\d+)"', vt).group(1))
        media = doc.raw(re.search(r'<Media ObjectURef="([^"]+)"', src).group(1), uid=True)
        vs = doc.raw(re.search(r'<VideoStream ObjectRef="(\d+)"', media).group(1))
        fr = int(re.search(r'<FrameRate>(\d+)</FrameRate>', vs).group(1))
        dur = int(re.search(r'<Duration>(\d+)</Duration>', vs).group(1))
        return dict(master_vclip=vc.attrib['ObjectID'], mc_uid=mc.attrib['ObjectUID'], name=name, info=dict(fr=fr, dur=dur))
    raise KeyError(name)


def comp_params(doc, comp_id):
    out = {}
    for pid in re.findall(r'<Param Index="\d+" ObjectRef="(\d+)"', doc.raw(comp_id)):
        p = doc.raw(pid); n = re.search(r'<Name>([^<]*)</Name>', p); v = re.search(r'<StartKeyframe>-?\d+,([^,]+),', p)
        if n and v: out[n.group(1)] = v.group(1)
    return out


def motion_of(doc, ti):
    ch = re.search(r'<Components ObjectRef="(\d+)"', doc.raw(ti)).group(1)
    for c in chain_components(doc, ch):
        if '<MatchName>AE.ADBE Motion</MatchName>' in doc.raw(c): return comp_params(doc, c)
    return None


def broll_track(trs, key): return trs[3] if key == '348e0ba6' else trs[2]
def grade_track(trs, key): return trs[4] if key == '348e0ba6' else trs[3]


def live(doc, tr):
    """item ids on a track that still exist (the parsed tree can list items deleted from the text)"""
    out = []
    for i in re.findall(r'<TrackItem Index="\d+" ObjectRef="(\d+)"/>', doc.raw(tr.attrib['ObjectUID'], uid=True)):
        try: doc.raw(i); out.append(i)
        except KeyError: pass
    return out


def at(doc, tr, sec, tol=0.03):
    its = [i for i in live(doc, tr) if abs(item_times(doc, i)[0] / TPS - sec) < tol]
    assert len(its) == 1, ('no unique item at', sec, len(its))
    return its[0]


def static(ptxt):
    ptxt = re.sub(r'\n\t*<Keyframes>[^<]*</Keyframes>', '', ptxt)
    return ptxt.replace('<IsTimeVarying>true</IsTimeVarying>', '<IsTimeVarying>false</IsTimeVarying>')


def overlay_item(doc, tmpl, master, start, end):
    """graphic overlay: template structure, Motion only (centred, 100%), no grade"""
    t = doc.raw(tmpl)
    ch_id = re.search(r'<Components ObjectRef="(\d+)"', t).group(1)
    mot = [c for c in chain_components(doc, ch_id) if '<MatchName>AE.ADBE Motion</MatchName>' in doc.raw(c)][0]
    nmot, mtexts = clone_component(doc, mot, {'Position': '0.5:0.5', 'Scale': 100.0})
    mtexts = [mtexts[0]] + [static(p) for p in mtexts[1:]]
    nch, chtxt = clone_chain(doc, ch_id, [nmot])
    mvc = master['master_vclip']; nvc, nsc, nti = doc.new_id(), doc.new_id(), doc.new_id()
    vctxt = strip_inline(doc.raw(mvc).replace('ObjectID="%s"' % mvc, 'ObjectID="%s"' % nvc, 1))
    vctxt = re.sub(r'\n\t\t\t<InUse>[^<]*</InUse>', '', vctxt)
    vctxt = re.sub(r'\n\t\t\t<(In|Out)Point>[^<]*</(In|Out)Point>', '', vctxt)
    vctxt = re.sub(r'(<Source ObjectRef="\d+"/>)', lambda m: m.group(1) + '\n\t\t\t<OutPoint>%d</OutPoint>\n\t\t\t<InPoint>0</InPoint>' % (end - start), vctxt, count=1)
    vctxt = re.sub(r'<ClipID>[^<]*</ClipID>', '<ClipID>%s</ClipID>' % uuid.uuid4(), vctxt)
    sc_id = re.search(r'<SubClip ObjectRef="(\d+)"', t).group(1)
    sctxt = doc.raw(sc_id).replace('ObjectID="%s"' % sc_id, 'ObjectID="%s"' % nsc, 1)
    sctxt = re.sub(r'(<Clip ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nvc, sctxt)
    sctxt = re.sub(r'(<MasterClip ObjectURef=")[^"]+(")', r'\g<1>%s\g<2>' % master['mc_uid'], sctxt)
    sctxt = re.sub(r'<Name>[^<]*</Name>', '<Name>%s</Name>' % master['name'], sctxt)
    titxt = t.replace('ObjectID="%s"' % tmpl, 'ObjectID="%s"' % nti, 1)
    titxt = re.sub(r'(<Components ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nch, titxt)
    titxt = re.sub(r'(<SubClip ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nsc, titxt)
    titxt = re.sub(r'\n\t\t\t<IsMuted>[^<]*</IsMuted>', '', titxt)
    titxt = set_times2(titxt, start, end)
    return nti, mtexts + [chtxt, vctxt, sctxt, titxt]


def caption_tracks(doc, seq):
    g = [doc.deref(tg.find('Second')) for tg in seq.find('TrackGroups') if doc.deref(tg.find('Second')).tag == 'DataTrackGroup'][0]
    return [doc.deref(t) for t in g.find('.//Tracks')]


GC_TAGS = {'CaptionDataClipTrackItem', 'DataComponentChain', 'SubClip', 'TranscriptClip', 'DataMediaSource', 'Block',
           'MasterClip', 'ClipLoggingInfo', 'ClipChannelGroupVectorSerializer', 'Media', 'DataStream'}
REF = re.compile(r'Object(U?)Ref="([^"]+)"')


def remove_captions(doc, pairs):
    """unlink caption items from their tracks, then delete every object in their chains that nothing references any more"""
    cands, seen = [], set()
    for _, item in pairs:
        stack = [(item, False)]
        while stack:
            k, u = stack.pop()
            if (k, u) in seen: continue
            seen.add((k, u))
            try: t = doc.raw(k, uid=u)
            except KeyError: continue
            if re.match(r'\s*<(\w+)', t).group(1) not in GC_TAGS: continue
            cands.append((k, u)); stack += [(r, bool(m)) for m, r in REF.findall(t)]
    by_track = {}
    for tr_uid, item in pairs: by_track.setdefault(tr_uid, set()).add(item)
    for tr_uid, items in by_track.items():
        t = doc.raw(tr_uid, uid=True)
        ids = [i for i in re.findall(r'<TrackItem Index="\d+" ObjectRef="(\d+)"/>', t) if i not in items]
        block = ''.join('\n\t\t\t\t\t\t<TrackItem Index="%d" ObjectRef="%s"/>' % (k, i) for k, i in enumerate(ids))
        doc.replace_obj(tr_uid, re.sub(r'<TrackItems Version="1">.*?</TrackItems>', lambda m_: '<TrackItems Version="1">%s\n\t\t\t\t\t</TrackItems>' % block, t, flags=re.S), uid=True)
    count = {}
    for m, r in REF.findall(doc.txt): count[(r, bool(m))] = count.get((r, bool(m)), 0) + 1
    gone, changed = 0, True
    while changed:
        changed = False
        for c in list(cands):
            if count.get(c, 0) > 0: continue
            try: t = doc.raw(c[0], uid=c[1])
            except KeyError: cands.remove(c); continue
            for m, r in REF.findall(t): count[(r, bool(m))] -= 1
            s, e = doc.span(c[0], c[1])
            if doc.txt[e:e + 1] == '\n': e += 1
            doc.txt = doc.txt[:s] + doc.txt[e:]
            cands.remove(c); gone += 1; changed = True
    return gone


ANYBLOB = re.compile(r'<(FormattedTextData)( [^>]*?BinaryHash="([^"]+)")(/>|>([^<]*)</FormattedTextData>)')


def normalize_text_blobs(txt, orig):
    """caption text blobs: the first remaining use of each hash must carry the data"""
    data = {}
    for m in ANYBLOB.finditer(orig):
        if m.group(4) != '/>' and (m.group(5) or '').strip(): data.setdefault(m.group(3), m.group(5))
    seen, edits = set(), []
    for m in ANYBLOB.finditer(txt):
        h = m.group(3); inline = m.group(4) != '/>' and bool((m.group(5) or '').strip())
        if h not in seen:
            seen.add(h)
            if not inline: edits.append((m.start(), m.end(), '<%s%s>%s</%s>' % (m.group(1), m.group(2), data[h], m.group(1))))
        elif inline: edits.append((m.start(), m.end(), '<%s%s/>' % (m.group(1), m.group(2))))
    for a, b, rep in sorted(edits, reverse=True): txt = txt[:a] + rep + txt[b:]
    return txt, len(edits)


def caption_items(doc, tr):
    out = []
    for i in re.findall(r'<TrackItem Index="\d+" ObjectRef="(\d+)"/>', doc.raw(tr.attrib['ObjectUID'], uid=True)):
        t = doc.raw(i); s = re.search(r'<Start>(-?\d+)</Start>', t)
        out.append((i, int(s.group(1)) if s else 0, int(re.search(r'<End>(\d+)</End>', t).group(1))))
    return out


def build(src, out_path, overlays=True, log=print):
    doc = Doc(src)
    orig_blobs = inline_blobs(doc.txt)
    orig_txt = doc.txt
    seqs = {s.attrib['ObjectUID'][:8]: s for n, s in for_claude_sequences(doc)}
    new_objs, rep = [], {}
    held = seqs['404c5cb2']; c132_ref = at(doc, broll_track(video_tracks(doc, held), '404c5cb2'), 21.68)
    c132_mot = motion_of(doc, c132_ref); assert 'C132' in item_name(doc, c132_ref)
    c132 = find_master(doc, 'A003_09181348_C132.mp4')
    for key, seq in seqs.items():
        trs = video_tracks(doc, seq); br, gr = broll_track(trs, key), grade_track(trs, key)
        r = rep[key] = {'name': seq.findtext('Name')[:30]}
        # ---- titles
        if key in TITLE_TIME:
            ti = [it.attrib['ObjectID'] for t_ in trs for it in track_items(doc, t_) if item_name(doc, it.attrib['ObjectID']) == TITLE_NAME][0]
            s, e, tin, vc = item_times(doc, ti)
            a, b = [tk(x) for x in TITLE_TIME[key]]
            doc.replace_obj(ti, set_times2(doc.raw(ti), a, b)); doc.replace_obj(vc, set_inout(doc.raw(vc), tin, tin + (b - a)))
            ch = re.search(r'<Components ObjectRef="(\d+)"', doc.raw(ti)).group(1)
            comps, texts = title_B(doc, gfx_plan.TITLE[key]['sub'], tin, (b - a) / TPS, TITLE_Y.get(key, TITLE_Y_DEFAULT))
            for c in chain_components(doc, ch):
                for k_ in component_ids(doc, c): delete_obj(doc, k_)
            items = ''.join('\n\t\t\t\t<Component Index="%d" ObjectRef="%s"/>' % (i, c) for i, c in enumerate(comps))
            doc.replace_obj(ch, re.sub(r'<Components Version="1">.*?</Components>', '<Components Version="1">%s\n\t\t\t</Components>' % items, doc.raw(ch), flags=re.S))
            new_objs += texts; r['title'] = TITLE_TIME[key]
        # ---- C137 hand-place -> C132 pouch slide (framing from I held the record)
        for ad, st, src_s in SWAP_TO_C132:
            if ad != key: continue
            tid = at(doc, br, st); assert 'C137' in item_name(doc, tid)
            s0, e0, _, _ = item_times(doc, tid)
            px, py = [float(v) for v in c132_mot['Position'].split(':')]
            nti, objs = ext_item(doc, tid, c132, s0, e0, int(round(src_s * 25)) * F25, px, py, float(c132_mot['Scale']), {})
            new_objs += objs; delete_item(doc, tid)
            ids = [x.attrib['ObjectID'] for x in track_items(doc, br) if x.attrib['ObjectID'] != tid] + [nti]
            r.setdefault('_order', []).append((br.attrib['ObjectUID'], ids))
            r.setdefault('swap', []).append(('C137->C132', st, src_s))
        # ---- 1 star stock swap (template: a graded B-roll item with Motion)
        for ad, st, media, src_s in STOCK_SWAP:
            if ad != key: continue
            tid = at(doc, br, st); s0, e0, _, _ = item_times(doc, tid)
            tmpl = [it.attrib['ObjectID'] for it in track_items(doc, br) if motion_of(doc, it.attrib['ObjectID']) and lumetri_ids(doc, it.attrib['ObjectID'])][0]
            m = find_master(doc, media); fr = m['info']['fr']
            nti, objs = ext_item(doc, tmpl, m, s0, e0, int(round(src_s * TPS / fr)) * fr, 0.5, 0.5, 50.0, dict(STOCK_GRADE))
            new_objs += objs; delete_item(doc, tid)
            ids = [x.attrib['ObjectID'] for x in track_items(doc, br) if x.attrib['ObjectID'] != tid] + [nti]
            r.setdefault('_order', []).append((br.attrib['ObjectUID'], ids))
            r.setdefault('stock', []).append((media[:28], st))
        # ---- remove a B-roll item and stretch the grade piece before it over the gap
        for ad, st, part in REMOVE:
            if ad != key: continue
            tid = at(doc, br, st); assert part in item_name(doc, tid)
            s0, e0, _, _ = item_times(doc, tid)
            g = [x.attrib['ObjectID'] for x in track_items(doc, gr) if item_times(doc, x.attrib['ObjectID'])[1] == s0]
            assert len(g) == 1, ('no grade piece ends at', st)
            gs, ge, _, _ = item_times(doc, g[0]); retime_item(doc, g[0], gs, e0)
            delete_item(doc, tid)
            ids = [x.attrib['ObjectID'] for x in track_items(doc, br) if x.attrib['ObjectID'] != tid]
            set_track_items(doc, br.attrib['ObjectUID'], ids)
            r['removed'] = (part, st)
        # ---- late-segment tint fix on the grade pieces
        if key in LATE_TINT:
            from_s, vals = LATE_TINT[key]; n = 0; kf = []
            for x in track_items(doc, gr):
                if item_times(doc, x.attrib['ObjectID'])[0] / TPS >= from_s - 0.01:
                    for c in lumetri_ids(doc, x.attrib['ObjectID']): set_lumetri(doc, c, vals, kf); n += 1
            r['late_tint'] = (from_s, vals, n)
    Z.append_objects(doc, new_objs); new_objs = []
    for key, r in rep.items():
        for uid, ids in r.pop('_order', []):
            ids.sort(key=lambda x: item_times(doc, x)[0]); set_track_items(doc, uid, ids)
    # ---- overlays on new top tracks + captions under them removed
    if overlays:
        by_ad = {}
        for name, ad, when in OVER:
            seq = seqs[ad]; trs = video_tracks(doc, seq)
            if isinstance(when, tuple):
                tid = at(doc, broll_track(trs, ad), when[1]); s0, e0, _, _ = item_times(doc, tid)
            else:
                s0, e0 = tk(when), None
            m = find_master(doc, name + '.mov'); d = m['info']['dur']
            e1 = s0 + d if e0 is None else min(e0, s0 + d)
            by_ad.setdefault(ad, []).append([name, s0, e1, m])
        for ad, lst in by_ad.items():
            seq = seqs[ad]; lst.sort(key=lambda x: x[1])
            for a_, b_ in zip(lst, lst[1:]):          # tiny overlaps: trim the earlier one
                if 0 < a_[2] - b_[1] <= tk(0.12): a_[2] = b_[1]
            lanes = []
            for it in lst:
                for ln in lanes:
                    if ln[-1][2] <= it[1]: ln.append(it); break
                else: lanes.append([it])
            trs = video_tracks(doc, seq); tmpl_tr = trs[-1].attrib['ObjectUID']
            tmpl = [x for x in live(doc, broll_track(trs, ad)) if motion_of(doc, x)][0]
            for ln in lanes:
                uid = Z.add_track(doc, seq, None, tmpl_tr)
                ids = []
                for name, s0, e1, m in ln:
                    nti, objs = overlay_item(doc, tmpl, m, s0, e1)
                    Z.append_objects(doc, objs); ids.append(nti)
                set_track_items(doc, uid, ids)
            rep[ad]['overlays'] = [(x[0], round(x[1] / TPS, 2), round(x[2] / TPS, 2)) for x in lst]
            rep[ad]['lanes'] = len(lanes)
            # captions: drop the ones whose middle falls under an overlay
            pairs = []
            for ctr in caption_tracks(doc, seq):
                for cid, cs, ce in caption_items(doc, ctr):
                    mid = (cs + ce) / 2
                    if any(s0 <= mid <= e1 for _, s0, e1, _ in lst): pairs.append((ctr.attrib['ObjectUID'], cid))
            rep[ad]['captions_removed'] = (len(pairs), remove_captions(doc, pairs)) if pairs else 0
    for k, r in rep.items(): log('%-9s %s' % (k, {a: b for a, b in r.items() if a != 'name'}))
    extra = dict(orig_blobs); extra.update(Z.T['blobs']); extra.update(Z.NEW_BLOBS)
    doc.txt, n = Z.normalize_blobs(doc.txt, extra)
    doc.txt, n2 = normalize_text_blobs(doc.txt, orig_txt)
    log('blob fixes %d, caption text blob fixes %d' % (n, n2))
    open(out_path + '.xml', 'w', encoding='utf-8', newline='\n').write(doc.txt)
    with open(out_path + '.xml', 'rb') as f, gzip.open(out_path, 'wb') as g: g.write(f.read())
    return rep


if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2], overlays='--no-overlays' not in sys.argv)
