"""Title v2: swap the layers inside every "Title - Paula Radcliffe" graphic for a bigger, readable design.

Design (1080x1920): dark rounded plate (90 %, thin grey edge, soft shadow) at the top left beside Paula's head,
PAULA RADCLIFFE (Proxima Nova Semibold 35, white) / 44 px gold hairline (Immufix pouch gold) /
subtitle (Proxima Nova Regular 26, light grey). Plate eases up + fades in, text and line follow staggered,
everything eases out before the clip ends. Only the title graphics' layers change; timing, tracks and
every other object in the user's saved project stay as they are.
Colour ints in Premiere's text/shape JSON are 0xRRGGBB (checked against Adobe's own .mogrt templates).
"""
import sys, os, re, json, gzip
sys.path.insert(0, '.')
from build_project import Doc, TPS, for_claude_sequences, video_tracks, track_items
from build_broll import chain_components
from build_ext import delete_obj, component_ids
import build_zoom_gfx as Z
sys.path.insert(0, '../work')
import gfx_plan
from PIL import ImageFont

UF = r'C:\Users\Kanishk\AppData\Local\Microsoft\Windows\Fonts'
Z.PIL_FONT['ProximaNova-Regular'] = UF + r'\Proxima Nova Regular.ttf'
W, H = 1080, 1920
X0 = 30                                            # plate left edge
NAME_BASELINE = 105                                # where the user placed the name by hand (1 star / 3 questions / 3 things)
NAME = ('ProximaNova-Semibold', 35, 60, 0xFFFFFF)  # font, size px, tracking, colour
SUB = ('ProximaNova-Regular', 26, 15, 0xE2E2E2)
PAD_L, PAD_R, PAD_T, PAD_B = 20, 22, 18, 20
GAP1, GAP2 = 12, 12
LINE_W, LINE_H = 44, 3
RADIUS = 12
PLATE_FILL, PLATE_OP = 0x0C0C0C, 90.0
PLATE_STROKE, PLATE_STROKE_W = 0x4A4A4A, 1.5
GOLD = 0xCFAE63                                    # (207,174,99)
TITLE_NAME = 'Title - Paula Radcliffe'


def cap_height(font, size):
    b = ImageFont.truetype(Z.PIL_FONT[font], size).getbbox('H')
    return b[3] - b[1]


def plate_top():
    return NAME_BASELINE - PAD_T - cap_height(NAME[0], NAME[1])


def layout(sub):
    Y0 = plate_top()
    wn = Z.text_width(NAME[0], NAME[1], 'PAULA RADCLIFFE', NAME[2])
    ws = Z.text_width(SUB[0], SUB[1], sub, SUB[2])
    pw = round(max(wn, ws) + PAD_L + PAD_R)
    base_n = Y0 + PAD_T + cap_height(NAME[0], NAME[1])
    line_top = base_n + GAP1
    base_s = line_top + LINE_H + GAP2 + cap_height(SUB[0], SUB[1])
    ph = round(base_s + PAD_B - Y0)
    return dict(pw=pw, ph=ph, tx=X0 + PAD_L, base_n=base_n, line_top=line_top, base_s=base_s, wn=wn, ws=ws, y0=Y0)


def ek(tsec_fn, pts):
    """eased scalar keys: pts = [(sec, value, in_infl, out_infl)]"""
    return ''.join(Z.kf_scalar(tsec_fn(s), v, 5, 0, ini, 0, outi) for s, v, ini, outi in pts)


def ekp(tsec_fn, pts):
    return ''.join(Z.kf_point(tsec_fn(s), x / W, y / H, 5, 0, ini, 0, outi) for s, (x, y), ini, outi in pts)


def title_layers(doc, sub, t0_media, dur):
    L = layout(sub)
    t = lambda sec: t0_media + Z.s2t(sec)
    E, S = 1 / 3, 1 / 3                               # neutral influences
    comps, texts = [], []
    # --- name (top of the stack)
    for num, txt, (font, size, trk, col), yb, d in ((50, 'PAULA RADCLIFFE', NAME, L['base_n'], 0.14),
                                                    (51, sub, SUB, L['base_s'], 0.26)):
        op = ek(t, [(d, 0, E, 0.3), (d + 0.40, 100, 0.75, S), (dur - 0.62, 100, S, 0.7), (dur - 0.30, 0, 0.3, S)])
        pk = ekp(t, [(d, (L['tx'], yb + 12), E, 0.12), (d + 0.62, (L['tx'], yb), 0.88, S),
                     (dur - 0.62, (L['tx'], yb), S, 0.7), (dur - 0.30, (L['tx'], yb - 5), 0.3, S)])
        c, tx = Z.text_layer(doc, num, txt, font, size, (L['tx'], yb), color=col, tracking=trk, align=0, shadow=None,
                             opacity_keys=op, pos_keys=pk)
        comps.append(c); texts += tx
    # --- gold hairline: grows from the left, collapses back
    hs = ek(t, [(0.30, 0, E, 0.12), (0.88, 100, 0.88, S), (dur - 0.66, 100, S, 0.7), (dur - 0.30, 0, 0.3, S)])
    op = ek(t, [(0.30, 0, E, 0.3), (0.42, 100, 0.7, S), (dur - 0.42, 100, S, 0.5), (dur - 0.30, 0, 0.5, S)])
    c, tx = Z.shape_layer(doc, 52, 'Gold line', Z.rect_points(float(LINE_W), float(LINE_H)), Z.appearance(fill=GOLD),
                          (L['tx'], L['line_top'] + LINE_H / 2), (0.0, LINE_H / 2), opacity=100.0, uniform=False,
                          scale=100.0, hscale=0.0, opacity_keys=op, hscale_keys=hs)
    comps.append(c); texts += tx
    # --- plate (bottom of the stack): rise 12 px + fade + 96 -> 100 % scale, eases out at the end
    cx, cy = X0 + L['pw'] / 2, L['y0'] + L['ph'] / 2
    op = ek(t, [(0.0, 0, E, 0.3), (0.40, PLATE_OP, 0.7, S), (dur - 0.42, PLATE_OP, S, 0.6), (dur - 0.04, 0, 0.35, S)])
    pk = ekp(t, [(0.0, (cx, cy + 12), E, 0.12), (0.58, (cx, cy), 0.88, S), (dur - 0.42, (cx, cy), S, 0.6), (dur - 0.04, (cx, cy - 4), 0.35, S)])
    sk = ek(t, [(0.0, 96, E, 0.12), (0.58, 100, 0.88, S), (dur - 0.42, 100, S, 0.6), (dur - 0.04, 98.5, 0.35, S)])
    c, tx = Z.shape_layer(doc, 53, 'Title plate', Z.rrect_points(float(L['pw']), float(L['ph']), float(RADIUS)),
                          Z.appearance(fill=PLATE_FILL, stroke=PLATE_STROKE, stroke_w=PLATE_STROKE_W, shadow=(30, 28, 6)),
                          (cx, cy), (L['pw'] / 2, L['ph'] / 2), opacity=PLATE_OP, uniform=True, scale=100.0, hscale=100.0,
                          opacity_keys=op, pos_keys=pk, scale_keys=sk)
    comps.append(c); texts += tx
    return comps, texts, L


def inline_blobs(txt):
    out = {}
    for m in Z.BLOB.finditer(txt):
        if m.group(4) != '/>' and (m.group(5) or '').strip(): out.setdefault(m.group(3), m.group(5))
    return out


def build(src_xml, out_path, log=print):
    doc = Doc(src_xml)
    orig_blobs = inline_blobs(doc.txt)
    report = {}
    new_objs = []
    for name, seq in for_claude_sequences(doc):
        key = seq.attrib['ObjectUID'][:8]
        top = video_tracks(doc, seq)[-1]
        titles = []
        for it in track_items(doc, top):
            sc = doc.deref(it.find('.//SubClip'))
            if sc.findtext('Name') == TITLE_NAME: titles.append(it)
        assert len(titles) == 1, (name, len(titles))
        it = titles[0]; iid = it.attrib['ObjectID']
        t_item = doc.raw(iid)
        s = re.search(r'<Start>(\d+)</Start>', t_item); s = int(s.group(1)) if s else 0
        e = int(re.search(r'<End>(\d+)</End>', t_item).group(1))
        sc_id = re.search(r'<SubClip ObjectRef="(\d+)"', t_item).group(1)
        vc_id = re.search(r'<Clip ObjectRef="(\d+)"', doc.raw(sc_id)).group(1)
        tin = int(re.search(r'<InPoint>(-?\d+)</InPoint>', doc.raw(vc_id)).group(1))
        ch = re.search(r'<Components ObjectRef="(\d+)"', t_item).group(1)
        old = chain_components(doc, ch)
        kinds = sorted(re.search(r'<MatchName>([^<]*)<', doc.raw(c)).group(1) for c in old)
        user_motion = 'AE.ADBE Motion' in kinds          # the user's own move/scale; the new layout replaces it
        assert [k for k in kinds if k != 'AE.ADBE Motion'] == ['AE.ADBE Shape', 'AE.ADBE Text', 'AE.ADBE Text'], (name, kinds)
        comps, texts, L = title_layers(doc, gfx_plan.TITLE[key]['sub'], tin, (e - s) / TPS)
        for c in old:
            for k in component_ids(doc, c): delete_obj(doc, k)
        chtxt = doc.raw(ch)
        items = ''.join('\n\t\t\t\t<Component Index="%d" ObjectRef="%s"/>' % (i, c) for i, c in enumerate(comps))
        chtxt2 = re.sub(r'<Components Version="1">.*?</Components>', '<Components Version="1">%s\n\t\t\t</Components>' % items, chtxt, flags=re.S)
        assert chtxt2 != chtxt
        doc.replace_obj(ch, chtxt2)
        t_item = doc.raw(iid)
        t_item2 = re.sub(r'<MZ.SequenceActions.NextShapeComponentNumber>\d+<', '<MZ.SequenceActions.NextShapeComponentNumber>54<', t_item)
        doc.replace_obj(iid, t_item2)
        new_objs += texts
        report[key] = dict(name=seq.findtext('Name'), start=round(s / TPS, 3), end=round(e / TPS, 3), sub=gfx_plan.TITLE[key]['sub'],
                           plate=(X0, L['y0'], L['pw'], L['ph']), name_w=round(L['wn'], 1), sub_w=round(L['ws'], 1), removed_user_motion=user_motion)
        log('%-44s title %.2f-%.2f  plate %dx%d at (%d,%d)  "%s"%s' % (seq.findtext('Name')[:44], s / TPS, e / TPS, L['pw'], L['ph'], X0, L['y0'], gfx_plan.TITLE[key]['sub'], '  (user Motion removed)' if user_motion else ''))
    Z.append_objects(doc, new_objs)
    extra = dict(orig_blobs); extra.update(Z.T['blobs']); extra.update(Z.NEW_BLOBS)
    doc.txt, n = Z.normalize_blobs(doc.txt, extra)
    log('blob fixes %d, new blobs %d' % (n, len(Z.NEW_BLOBS)))
    xml_out = out_path + '.xml'
    open(xml_out, 'w', encoding='utf-8', newline='\n').write(doc.txt)
    with open(xml_out, 'rb') as f, gzip.open(out_path, 'wb') as g: g.write(f.read())
    return xml_out, report


if __name__ == '__main__':
    x, rep = build(sys.argv[1], sys.argv[2])
    json.dump(rep, open(sys.argv[2] + '.report.json', 'w'), indent=1)
