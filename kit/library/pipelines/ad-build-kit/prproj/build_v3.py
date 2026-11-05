"""v3 on the user's latest save (zooms + titles v2):
  1. Title B: bold condensed name + gold pill, below the caption (above the board in 3 things), animated.
     1 star: title moves to 3.3-6.4 s so it follows the star animation.
  2. Colour: gentler punch on the riverside ads and the park ads (grade layer + camera B-roll Lumetri).
  3. Shot fixes: drinking (C123 @3.4), run focus (C129 @29.4), pouch hold (C137 @52.6, extended),
     hospital-pill stock swapped (3 things -> vitamin C tablet macro, 1 star -> supplement bottles).
Everything else stays byte-identical."""
import sys, re, json, gzip
sys.path.insert(0, '.')
from build_project import Doc, TPS, fmt, for_claude_sequences, video_tracks, track_items
from build_broll import chain_components, set_inout, set_track_items
from build_ext import set_times2, delete_obj, component_ids, delete_item, item_times, retime_item, ext_item
import build_zoom_gfx as Z
from build_title_v2 import ek, ekp, inline_blobs
sys.path.insert(0, '../work')
import gfx_plan
from PIL import ImageFont

UF = r'C:\Users\Kanishk\AppData\Local\Microsoft\Windows\Fonts'
Z.PIL_FONT['Coolvetica-HeavyComp'] = UF + r'\Coolvetica Hv Comp.otf'
Z.PIL_FONT['ProximaNova-Extrabld'] = UF + r'\Proxima Nova Extrabold.ttf'
W, H = 1080, 1920
F25, F60 = 10160640000, 4233600000
GOLD, INK = 0xCFAE63, 0x141008
NAME = ('Coolvetica-HeavyComp', 118, 10)
CRED = ('ProximaNova-Extrabld', 30, 60)
TITLE_Y = {'f233433f': 360}            # whiteboard ad: above the board (no captions there)
TITLE_Y_DEFAULT = 1128                 # name baseline, just below the caption line
TITLE_TIME = {'cd03e189': (3.8, 6.9)}  # 1 star: after the star animation (stars 0.55-3.80)
TITLE_NAME = 'Title - Paula Radcliffe'
REF = '348e0ba6'

GRADE_FIX = {   # Lumetri param index -> value (was: Temp 5, Exp 1.0, Contrast 8, Shadows 22.7, Blacks -25.9, Sat 100, Vibrance 13.2)
    'river': {14: 3.0, 19: 0.9, 20: 22.0, 22: 14.0, 24: -38.0, 16: 108.0, 42: 16.0},
    'park': {14: 4.0, 20: 16.0, 22: 18.0, 24: -32.0, 16: 104.0, 42: 15.0},
}
AD_GROUP = {'0991faf2': 'river', '974102f7': 'river', '593f11c4': 'river', 'f233433f': 'park', '404c5cb2': 'park'}

SWAPS = [   # (ad, B-roll start s, expected clip name part, new source in s, new end s or None)
    ('f233433f', 42.133, 'C123', 3.4, None),
    ('664b35b2', 4.167, 'C129', 29.4, None),
    ('593f11c4', 6.217, 'C137', 52.6, 478 * F60 / TPS),
]
REPLACE = [  # (ad, B-roll start s, old name part, new media name, cx, scale, src s)
    ('f233433f', 10.70, 'counting-pills', '3things_vitaminC-tablet_pexels-7033622_1080x1920.mp4', 0.5, 100.0, 0.0),
    ('cd03e189', 14.983, 'counting-pills', 'ranpro_supplement-bottles_pexels-7525915_1080x1920.mp4', 0.5, 100.0, 0.0),
]
STOCK_GRADE = {14: 4.0, 15: 0.0, 16: 100.0, 19: 0.0, 20: 0.0, 21: 0.0, 22: 0.0, 23: 0.0, 24: 0.0, 41: 0.0, 42: 0.0}   # light grade for Rec.709 stock
MEDIA_FR = {'3things_vitaminC-tablet_pexels-7033622_1080x1920.mp4': (F25, 1080, 1920),
            'ranpro_supplement-bottles_pexels-7525915_1080x1920.mp4': (TPS * 1001 // 30000, 1080, 1920)}


def cap_h(font, size):
    b = ImageFont.truetype(Z.PIL_FONT[font], size).getbbox('H'); return b[3] - b[1]


def text_layer2(doc, comp_num, text, font, size, pos_px, color, tracking, align, shadow, opacity_keys, pos_keys, scale_keys=None):
    oid, comp, P = Z.clone_template_component(doc, 'text', comp_num, text)
    P['0'][1] = Z.set_blob(P['0'][1], Z.json_blob(Z.text_doc(text, font, size, color, tracking, align, shadow)))
    P['2'][1] = Z.set_value(P['2'][1], '%s:%s' % (repr(pos_px[0] / W), repr(pos_px[1] / H)))
    if pos_keys: P['2'][1] = Z.set_keys(P['2'][1], pos_keys)
    P['3'][1] = Z.set_value(P['3'][1], '100.'); P['4'][1] = Z.set_value(P['4'][1], '100.'); P['5'][1] = Z.set_value(P['5'][1], 'true')
    if scale_keys: P['3'][1] = Z.set_keys(P['3'][1], scale_keys)
    P['7'][1] = Z.set_value(P['7'][1], '100.')
    if opacity_keys: P['7'][1] = Z.set_keys(P['7'][1], opacity_keys)
    P['8'][1] = Z.set_value(P['8'][1], '0:0')
    return oid, [comp] + [p for _, p in sorted(P.values(), key=lambda v: int(v[0]))]


def title_B(doc, cred, t0_media, dur, yb):
    t = lambda sec: t0_media + Z.s2t(sec)
    E = 1 / 3; cx = W / 2
    ws = Z.text_width(CRED[0], CRED[1], cred.upper(), CRED[2])
    ph = cap_h(CRED[0], CRED[1]) + 22; pw = ws + 44
    pill_top = yb + 22; pill_cy = pill_top + ph / 2; cred_base = pill_top + 11 + cap_h(CRED[0], CRED[1])
    comps, texts = [], []
    # name: rises 40 px, fades, settles from 106 % (snappy start, long settle); eases up and out at the end
    op = ek(t, [(0.00, 0, E, 0.3), (0.28, 100, 0.75, E), (dur - 0.45, 100, E, 0.7), (dur - 0.12, 0, 0.3, E)])
    pk = ekp(t, [(0.00, (cx, yb + 40), E, 0.12), (0.50, (cx, yb), 0.88, E), (dur - 0.45, (cx, yb), E, 0.7), (dur - 0.12, (cx, yb - 18), 0.3, E)])
    sk = ek(t, [(0.00, 106, E, 0.12), (0.50, 100, 0.88, E)])
    c, tx = text_layer2(doc, 50, 'PAULA RADCLIFFE', NAME[0], NAME[1], (cx, yb), 0xFFFFFF, NAME[2], 2, (80, 22, 2), op, pk, sk)
    comps.append(c); texts += tx
    # credential text: fades and lifts 8 px once the pill has opened
    op = ek(t, [(0.42, 0, E, 0.3), (0.62, 100, 0.75, E), (dur - 0.55, 100, E, 0.6), (dur - 0.40, 0, 0.4, E)])
    pk = ekp(t, [(0.42, (cx, cred_base + 8), E, 0.12), (0.70, (cx, cred_base), 0.88, E)])
    c, tx = text_layer2(doc, 51, cred.upper(), CRED[0], CRED[1], (cx, cred_base), INK, CRED[2], 2, None, op, pk)
    comps.append(c); texts += tx
    # gold pill: opens from the centre, closes at the end
    hs = ek(t, [(0.20, 0, E, 0.12), (0.55, 100, 0.88, E), (dur - 0.50, 100, E, 0.7), (dur - 0.18, 0, 0.3, E)])
    op = ek(t, [(0.20, 0, E, 0.3), (0.28, 100, 0.7, E), (dur - 0.24, 100, E, 0.5), (dur - 0.16, 0, 0.5, E)])
    c, tx = Z.shape_layer(doc, 52, 'Credential pill', Z.rrect_points(float(pw), float(ph), float(ph / 2)), Z.appearance(fill=GOLD, shadow=(35, 18, 3)),
                          (cx, pill_cy), (pw / 2, ph / 2), opacity=100.0, uniform=False, scale=100.0, hscale=0.0, opacity_keys=op, hscale_keys=hs)
    comps.append(c); texts += tx
    return comps, texts


def lumetri_ids(doc, ti_id):
    ch = re.search(r'<Components ObjectRef="(\d+)"', doc.raw(ti_id)).group(1)
    return [c for c in chain_components(doc, ch) if '<MatchName>AE.ADBE Lumetri</MatchName>' in doc.raw(c)]


def set_lumetri(doc, comp_id, vals, log_kf):
    t = doc.raw(comp_id)
    for idx, v in vals.items():
        pid = re.search(r'<Param Index="%d" ObjectRef="(\d+)"' % idx, t).group(1)
        p = doc.raw(pid)
        if '<Keyframes>' in p: log_kf.append((comp_id, idx))
        doc.replace_obj(pid, Z.set_value(p, fmt(v)))


def item_name(doc, ti_id):
    sc = re.search(r'<SubClip ObjectRef="(\d+)"', doc.raw(ti_id)).group(1)
    return re.search(r'<Name>([^<]*)</Name>', doc.raw(sc)).group(1)


def find_master(doc, name):
    for e in doc.root:
        if e.tag != 'ClipProjectItem' or e.findtext('.//ProjectItem/Name') != name: continue
        mc = doc.deref(e.find('MasterClip'))
        vc = [doc.deref(c) for c in mc.find('Clips') if doc.deref(c).tag == 'VideoClip'][0]
        fr, w, h = MEDIA_FR[name]
        return dict(master_vclip=vc.attrib['ObjectID'], mc_uid=mc.attrib['ObjectUID'], name=name, info=dict(fr=fr, w=w, h=h))
    raise KeyError(name)


def build(src_xml, out_path, log=print):
    doc = Doc(src_xml)
    orig_blobs = inline_blobs(doc.txt)
    seqs = {s.attrib['ObjectUID'][:8]: s for n, s in for_claude_sequences(doc)}
    new_objs, report, kf_hits = [], {}, []
    for key, seq in seqs.items():
        trs = video_tracks(doc, seq)
        broll_tr = trs[3] if key == REF else trs[2]
        grade_tr = trs[4] if key == REF else trs[3]
        top = trs[-1]
        rep = report[key] = {'name': seq.findtext('Name')}
        # ---- 1. title
        titles = [it for tr in trs for it in track_items(doc, tr) if item_name(doc, it.attrib['ObjectID']) == TITLE_NAME]
        assert len(titles) == 1, (key, len(titles))
        iid = titles[0].attrib['ObjectID']
        s, e, tin, vc = item_times(doc, iid)
        if key in TITLE_TIME:
            a, b = [int(round(x * TPS / F60)) * F60 for x in TITLE_TIME[key]]
            doc.replace_obj(iid, set_times2(doc.raw(iid), a, b)); doc.replace_obj(vc, set_inout(doc.raw(vc), tin, tin + (b - a))); s, e = a, b
        ch = re.search(r'<Components ObjectRef="(\d+)"', doc.raw(iid)).group(1)
        old = chain_components(doc, ch)
        comps, texts = title_B(doc, gfx_plan.TITLE[key]['sub'], tin, (e - s) / TPS, TITLE_Y.get(key, TITLE_Y_DEFAULT))
        for c in old:
            for k in component_ids(doc, c): delete_obj(doc, k)
        chtxt = doc.raw(ch)
        items = ''.join('\n\t\t\t\t<Component Index="%d" ObjectRef="%s"/>' % (i, c) for i, c in enumerate(comps))
        doc.replace_obj(ch, re.sub(r'<Components Version="1">.*?</Components>', '<Components Version="1">%s\n\t\t\t</Components>' % items, chtxt, flags=re.S))
        doc.replace_obj(iid, re.sub(r'<MZ.SequenceActions.NextShapeComponentNumber>\d+<', '<MZ.SequenceActions.NextShapeComponentNumber>53<', doc.raw(iid)))
        new_objs += texts
        rep['title'] = (round(s / TPS, 3), round(e / TPS, 3), TITLE_Y.get(key, TITLE_Y_DEFAULT))
        # ---- 2. colour
        if key in AD_GROUP:
            vals = GRADE_FIX[AD_GROUP[key]]; n_g = n_b = 0
            for it in track_items(doc, grade_tr):
                for c in lumetri_ids(doc, it.attrib['ObjectID']): set_lumetri(doc, c, vals, kf_hits); n_g += 1
            for it in track_items(doc, broll_tr):
                if item_name(doc, it.attrib['ObjectID']).startswith('A003_'):
                    for c in lumetri_ids(doc, it.attrib['ObjectID']): set_lumetri(doc, c, vals, kf_hits); n_b += 1
            rep['colour'] = (AD_GROUP[key], n_g, n_b)
        # ---- 3. swaps
        for ad, st, part, src, new_end in SWAPS:
            if ad != key: continue
            its = [it for it in track_items(doc, broll_tr) if abs(item_times(doc, it.attrib['ObjectID'])[0] / TPS - st) < 0.02]
            assert len(its) == 1 and part in item_name(doc, its[0].attrib['ObjectID']), (key, st, part)
            tid = its[0].attrib['ObjectID']; s0, e0, tin0, vc0 = item_times(doc, tid)
            if new_end:
                e1 = int(round(new_end * TPS / F60)) * F60
                # the grade piece that starts where the B-roll ended moves with it
                gp = [g for g in track_items(doc, grade_tr) if item_times(doc, g.attrib['ObjectID'])[0] == e0]
                assert len(gp) == 1, ('grade piece after', key, e0 / TPS)
                gs, ge, _, _ = item_times(doc, gp[0].attrib['ObjectID'])
                retime_item(doc, gp[0].attrib['ObjectID'], e1, ge)
                doc.replace_obj(tid, set_times2(doc.raw(tid), s0, e1)); e0 = e1
            new_in = int(round(src * 25)) * F25
            doc.replace_obj(vc0, set_inout(doc.raw(vc0), new_in, new_in + (e0 - s0)))
            rep.setdefault('swaps', []).append((part, round(s0 / TPS, 3), round(e0 / TPS, 3), src))
        for ad, st, part, media, cx, scale, src in REPLACE:
            if ad != key: continue
            its = [it for it in track_items(doc, broll_tr) if abs(item_times(doc, it.attrib['ObjectID'])[0] / TPS - st) < 0.02]
            assert len(its) == 1 and part in item_name(doc, its[0].attrib['ObjectID']), (key, st, part, [item_name(doc, i.attrib['ObjectID']) for i in its])
            tid = its[0].attrib['ObjectID']; s0, e0, _, _ = item_times(doc, tid)
            m = find_master(doc, media); fr = m['info']['fr']; w = m['info']['w']
            px = (540 - (cx * w - w / 2) * scale / 100) / 1080
            def has_fx(x):
                ch_ = re.search(r'<Components ObjectRef="(\d+)"', doc.raw(x)).group(1); cs = [doc.raw(c) for c in chain_components(doc, ch_)]
                return any('AE.ADBE Motion<' in c for c in cs) and any('AE.ADBE Lumetri<' in c for c in cs)
            tmpl = tid if has_fx(tid) else [it.attrib['ObjectID'] for it in track_items(doc, broll_tr) if has_fx(it.attrib['ObjectID'])][0]
            lum = {} if tmpl == tid else dict(STOCK_GRADE)
            nti, objs = ext_item(doc, tmpl, m, s0, e0, int(round(src * TPS / fr)) * fr, px, 0.5, scale, lum)
            new_objs += objs
            delete_item(doc, tid)
            ids = [it.attrib['ObjectID'] for it in track_items(doc, broll_tr) if it.attrib['ObjectID'] != tid] + [nti]
            rep.setdefault('replaced', []).append((part, media[:30], round(s0 / TPS, 3), round(e0 / TPS, 3)))
            rep['_order'] = (broll_tr.attrib['ObjectUID'], ids)
        log('%-44s %s' % (seq.findtext('Name')[:44], {k: v for k, v in rep.items() if k not in ('name', '_order')}))
    Z.append_objects(doc, new_objs)
    for key, rep in report.items():
        if '_order' in rep:
            uid, ids = rep.pop('_order')
            ids.sort(key=lambda x: item_times(doc, x)[0])
            set_track_items(doc, uid, ids)
    extra = dict(orig_blobs); extra.update(Z.T['blobs']); extra.update(Z.NEW_BLOBS)
    doc.txt, n = Z.normalize_blobs(doc.txt, extra)
    log('blob fixes %d, new blobs %d, keyframed colour params hit %d' % (n, len(Z.NEW_BLOBS), len(kf_hits)))
    xml_out = out_path + '.xml'
    open(xml_out, 'w', encoding='utf-8', newline='\n').write(doc.txt)
    with open(xml_out, 'rb') as f, gzip.open(out_path, 'wb') as g: g.write(f.read())
    return xml_out, report


if __name__ == '__main__':
    x, rep = build(sys.argv[1], sys.argv[2])
    json.dump(rep, open(sys.argv[2] + '.report.json', 'w'), indent=1, default=str)
