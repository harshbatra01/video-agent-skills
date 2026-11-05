"""Zooms + intro titles + TRYIMMUFIX code cards on the user's latest saved project.

Zooms (7 ads): new track V2 directly above the talking head (B-roll -> V3, grade -> V4), one adjustment
layer per segment carrying two Transform effects cloned from the user's reference zoom layer
("Malice Constant Zoom In Slow" + punch), keyframes rewritten per the plan, anchor near Paula's face.
Graphics (all 8 ads): new top track with Essential Graphics clips (text + shape layers, per-layer keyframes).
Everything else stays byte-identical.
"""
import sys, os, re, uuid, gzip, json, base64, struct, math
sys.path.insert(0, '.')
from build_project import Doc, TPS, fmt, for_claude_sequences, video_tracks, track_items
from build_broll import strip_inline, clone_component, chain_components, clone_chain, set_inout, set_track_items
from build_ext import set_times2
sys.path.insert(0, '../work')
import zoom_plan, gfx_plan
from PIL import ImageFont

F60 = 4233600000
ADJ_IN = 914457600000000          # adjustment-layer media time origin (1 h), as in the project
GFX_IN = 914457600000000          # graphic clips use the same media-time origin
REF = '348e0ba6'
W, H = 1080, 1920
HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, 'gfx_templates.json')))
TEXT_DOC = json.load(open(os.path.join(HERE, 'text_doc_template.json'), encoding='utf-8'))
APPEAR = json.load(open(os.path.join(HERE, 'appearance_template.json'), encoding='utf-8'))
UF = r'C:\Users\Kanishk\AppData\Local\Microsoft\Windows\Fonts'
PIL_FONT = {'ProximaNova-Semibold': UF + r'\Proxima Nova Semibold.ttf', 'ProximaNova-Light': UF + r'\Proxima Nova Light.ttf',
            'PowerGrotesk-Regular': UF + r'\PowerGrotesk-Regular (1).ttf'}
NEW_BLOBS = {}                    # hash -> base64 data for blobs created here


def s2t(sec): return int(round(sec * TPS))


def num(x):
    x = float(x)
    return '%d' % x if x == int(x) else repr(x)


# ---------------------------------------------------------------- keyframes
def kf_scalar(t, v, interp=5, ins=0.0, ini=1 / 3, outs=0.0, outi=1 / 3):
    return '%d,%s,%d,0,%s,%s,%s,%s;' % (t, fmt(v), interp, num(ins), num(ini), num(outs), num(outi))


def kf_point(t, x, y, interp=5, ins=0.0, ini=1 / 3, outs=0.0, outi=1 / 3):
    return '%d,%s:%s,%d,0,%s,%s,%s,%s,5,4,0,0,0,0;' % (t, repr(float(x)), repr(float(y)), interp, num(ins), num(ini), num(outs), num(outi))


def ease_keys(points, fn=kf_scalar):
    """points: list of (t_ticks, value, in_infl, out_infl) with bezier interp and zero speeds (eases)."""
    s = ''
    for t, v, ini, outi in points:
        if fn is kf_scalar: s += kf_scalar(t, v, 5, 0, ini, 0, outi)
        else: s += kf_point(t, v[0], v[1], 5, 0, ini, 0, outi)
    return s


# ---------------------------------------------------------------- param text helpers
def set_value(ptxt, val):
    m = re.search(r'<StartKeyframe>(-?\d+),([^,]+),', ptxt)
    return ptxt[:m.start(2)] + val + ptxt[m.end(2):]


def set_keys(ptxt, keys):
    ptxt = re.sub(r'\n\t\t<Keyframes>[^<]*</Keyframes>', '', ptxt)
    if '<IsTimeVarying>' in ptxt:
        ptxt = re.sub(r'<IsTimeVarying>[^<]*</IsTimeVarying>', '<IsTimeVarying>true</IsTimeVarying>', ptxt)
    else:
        ptxt = ptxt.replace('\n\t\t<StartKeyframe>', '\n\t\t<IsTimeVarying>true</IsTimeVarying>\n\t\t<StartKeyframe>', 1)
    return re.sub(r'(<StartKeyframe>[^<]*</StartKeyframe>)', lambda m: m.group(1) + '\n\t\t<Keyframes>%s</Keyframes>' % keys, ptxt, 1)


def new_hash(nbytes):
    h = uuid.uuid4().hex[:24]
    return '%s-%s-%s-%s-%s%08x' % (h[0:8], h[8:12], h[12:16], h[16:20], h[20:24], nbytes + 12)


def set_blob(ptxt, raw):
    h = new_hash(len(raw)); b64 = base64.b64encode(raw).decode()
    NEW_BLOBS[h] = b64
    return re.sub(r'<StartKeyframeValue Encoding="base64" BinaryHash="[^"]+"\s*(/>|>[^<]*</StartKeyframeValue>)',
                  '<StartKeyframeValue Encoding="base64" BinaryHash="%s">%s</StartKeyframeValue>' % (h, b64), ptxt, 1)


def json_blob(obj):
    u16 = json.dumps(obj, ensure_ascii=False, separators=(',', ':')).encode('utf-16-le')
    return struct.pack('<Q', len(u16)) + u16


def text_doc(text, font, size, color=16777215, tracking=0, align=0, shadow=None, leading=0):
    d = json.loads(json.dumps(TEXT_DOC))
    tp = d['mTextParam']; ss = tp['mStyleSheet']
    tp['mAlignment'] = align; tp['mLeading'] = leading
    if shadow:
        tp.update(mShadowVisible=True, mShadowColor=0, mShadowOpacity=shadow[0], mShadowBlur=shadow[1], mShadowOffset=shadow[2], mShadowAngle=90, mShadowSize=0)
    else:
        tp['mShadowVisible'] = False
    ss['mFontName'] = {'mParamValues': [[0, font]]}
    ss['mFontSize'] = {'mParamValues': [[0, float(size)]]}
    ss['mFillColor'] = {'mParamValues': [[0, color]]}
    ss['mFillVisible'] = {'mParamValues': [[0, True]]}
    ss['mStrokeVisible'] = {'mParamValues': [[0, False]]}
    ss['mTracking'] = {'mParamValues': [[0, tracking]]}
    ss['mText'] = text
    return d


def appearance(fill=None, stroke=None, stroke_w=1.0, shadow=None):
    d = json.loads(json.dumps(APPEAR)); st = d['mStyle']
    st['mFillVisible'] = fill is not None
    if fill is not None: st['mFillColor'] = fill
    st['mStrokeVisible'] = stroke is not None
    if stroke is not None: st['mStrokeColor'] = stroke; st['mStrokeWidth'] = stroke_w
    if shadow:
        st.update(mShadowVisible=True, mShadowColor=0, mShadowOpacity=shadow[0], mShadowBlur=shadow[1], mShadowOffset=shadow[2], mShadowAngle=90, mShadowSize=0)
    return d


def path_blob(points, closed=True):
    b = struct.pack('<II', 2, len(points))
    for x, y in points: b += struct.pack('<7f', 0.0, x, y, x, y, x, y)
    return b + (b'\x01' if closed else b'\x00')


def rect_points(w, h):
    return [(0.0, 0.0), (w, 0.0), (w, h), (0.0, h)]


def rrect_points(w, h, r, n=14):
    pts = []
    for cx, cy, a0 in ((r, r, 180), (w - r, r, 270), (w - r, h - r, 0), (r, h - r, 90)):
        for i in range(n + 1):
            a = math.radians(a0 + 90 * i / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


# ---------------------------------------------------------------- graphic layers
def clone_template_component(doc, kind, comp_num, inst):
    """fresh copy of the CTA text/shape layer component + params. returns (comp_oid, comp_text, {idx: [oid, text]})"""
    tpl = T[kind]
    comp_oid = doc.new_id()
    params = {}
    comp = tpl['comp']
    for idx, ptxt in sorted(tpl['params'].items(), key=lambda kv: int(kv[0])):
        nid = doc.new_id()
        old = re.search(r'ObjectID="(\d+)"', ptxt).group(1)
        p = ptxt.replace('ObjectID="%s"' % old, 'ObjectID="%s"' % nid, 1).strip('\n')
        p = re.sub(r'\n\t\t<CurrentValue>[^<]*</CurrentValue>', '', p)
        p = re.sub(r'(<StartKeyframeValue Encoding="base64" BinaryHash="[^"]+")>[^<]*</StartKeyframeValue>', r'\1/>', p)
        params[idx] = [nid, p]
        comp = re.sub(r'(<Param Index="%s" ObjectRef=")\d+("\s*/>)' % idx, r'\g<1>%s\g<2>' % nid, comp)
    old = re.search(r'ObjectID="(\d+)"', comp).group(1)
    comp = comp.replace('ObjectID="%s"' % old, 'ObjectID="%s"' % comp_oid, 1).strip('\n')
    comp = re.sub(r'<BE.VideoComponentChain.ChildPinID>\d+</BE.VideoComponentChain.ChildPinID>', '<BE.VideoComponentChain.ChildPinID>%d</BE.VideoComponentChain.ChildPinID>' % comp_num, comp)
    comp = re.sub(r'<ID>\d+</ID>', '<ID>%d</ID>' % comp_num, comp, 1)
    comp = re.sub(r'<InstanceName>[^<]*</InstanceName>', lambda m: '<InstanceName>%s</InstanceName>' % inst, comp)
    return comp_oid, comp, params


def text_layer(doc, comp_num, text, font, size, pos_px, color=16777215, tracking=0, align=0, shadow=None,
               opacity_keys=None, pos_keys=None, opacity=100.0):
    oid, comp, P = clone_template_component(doc, 'text', comp_num, text)
    P['0'][1] = set_blob(P['0'][1], json_blob(text_doc(text, font, size, color, tracking, align, shadow)))
    pos = '%s:%s' % (repr(pos_px[0] / W), repr(pos_px[1] / H))
    P['2'][1] = set_value(P['2'][1], pos)
    if pos_keys: P['2'][1] = set_keys(P['2'][1], pos_keys)
    P['3'][1] = set_value(P['3'][1], '100.'); P['4'][1] = set_value(P['4'][1], '100.'); P['5'][1] = set_value(P['5'][1], 'true')
    P['7'][1] = set_value(P['7'][1], fmt(opacity))
    if opacity_keys: P['7'][1] = set_keys(P['7'][1], opacity_keys)
    P['8'][1] = set_value(P['8'][1], '0:0')
    return oid, [comp] + [p for _, p in sorted(P.values(), key=lambda v: int(v[0]))]


def shape_layer(doc, comp_num, name, points, appear, pos_px, anchor_px, opacity=100.0, uniform=True, scale=100.0, hscale=100.0,
                opacity_keys=None, pos_keys=None, scale_keys=None, hscale_keys=None):
    oid, comp, P = clone_template_component(doc, 'shape', comp_num, name)
    P['0'][1] = set_blob(P['0'][1], path_blob(points))
    P['1'][1] = set_blob(P['1'][1], json_blob(appear))
    P['3'][1] = set_value(P['3'][1], '%s:%s' % (repr(pos_px[0] / W), repr(pos_px[1] / H)))
    if pos_keys: P['3'][1] = set_keys(P['3'][1], pos_keys)
    P['4'][1] = set_value(P['4'][1], fmt(scale))
    if scale_keys: P['4'][1] = set_keys(P['4'][1], scale_keys)
    P['5'][1] = set_value(P['5'][1], fmt(hscale))
    if hscale_keys: P['5'][1] = set_keys(P['5'][1], hscale_keys)
    P['6'][1] = set_value(P['6'][1], 'true' if uniform else 'false')
    P['8'][1] = set_value(P['8'][1], fmt(opacity))
    if opacity_keys: P['8'][1] = set_keys(P['8'][1], opacity_keys)
    P['9'][1] = set_value(P['9'][1], '%s:%s' % (repr(anchor_px[0] / W), repr(anchor_px[1] / H)))
    return oid, [comp] + [p for _, p in sorted(P.values(), key=lambda v: int(v[0]))]


def graphic_clip(doc, name, start, end, comp_ids, comp_texts, next_shape_num):
    """a timeline Graphic: own hidden master (synthetic GRAV media) + track item + chain of layers"""
    idmap = {}
    for o in T['master']:
        m = re.search(r'Object(U?)ID="([^"]+)"', o)
        idmap[m.group(2)] = str(uuid.uuid4()) if m.group(1) == 'U' else doc.new_id()
    texts = []
    for o in T['master']:
        t = o.strip('\n')
        for old, new in idmap.items():
            t = t.replace('ObjectID="%s"' % old, 'ObjectID="%s"' % new).replace('ObjectUID="%s"' % old, 'ObjectUID="%s"' % new)
            t = t.replace('ObjectRef="%s"' % old, 'ObjectRef="%s"' % new).replace('ObjectURef="%s"' % old, 'ObjectURef="%s"' % new)
        t = re.sub(r'<ClipID>[^<]*</ClipID>', '<ClipID>%s</ClipID>' % uuid.uuid4(), t)
        t = t.replace('ClassID="a36e4719-3ec6-4a0c-ab11-8b4aab377aa5" Version="22"', 'ClassID="a36e4719-3ec6-4a0c-ab11-8b4aab377aa5" Version="23"')
        texts.append(t)
    mc_uid = [idmap[k] for k in idmap if T['master'][0].find('ObjectUID="%s"' % k) >= 0][0]
    vms = [idmap[k] for k in idmap if any(o.startswith('\n\t<VideoMediaSource') and 'ObjectID="%s"' % k in o for o in T['master'])][0]
    dur = end - start
    nvc, nsc, nch, nti = doc.new_id(), doc.new_id(), doc.new_id(), doc.new_id()
    vc = T['clip'].strip('\n')
    vc = re.sub(r'ObjectID="\d+"', 'ObjectID="%s"' % nvc, vc, 1)
    vc = re.sub(r'<Source ObjectRef="\d+"/>', '<Source ObjectRef="%s"/>' % vms, vc)
    vc = re.sub(r'<ClipID>[^<]*</ClipID>', '<ClipID>%s</ClipID>' % uuid.uuid4(), vc)
    vc = set_inout(vc, GFX_IN, GFX_IN + dur)
    vc = re.sub(r'\n\t*<AdjustmentLayer>true</AdjustmentLayer>', '', vc)   # a plain title is not an adjustment layer
    assert '<AdjustmentLayer>' not in vc
    sc = T['subclip'].strip('\n')
    sc = re.sub(r'ObjectID="\d+"', 'ObjectID="%s"' % nsc, sc, 1)
    sc = re.sub(r'<Clip ObjectRef="\d+"/>', '<Clip ObjectRef="%s"/>' % nvc, sc)
    sc = re.sub(r'<MasterClip ObjectURef="[^"]+"/>', '<MasterClip ObjectURef="%s"/>' % mc_uid, sc)
    sc = re.sub(r'<Name>[^<]*</Name>', lambda m: '<Name>%s</Name>' % name, sc)
    ch = T['chain'].strip('\n')
    ch = re.sub(r'ObjectID="\d+"', 'ObjectID="%s"' % nch, ch, 1)
    items = ''.join('\n\t\t\t\t<Component Index="%d" ObjectRef="%s"/>' % (i, c) for i, c in enumerate(comp_ids))
    ch = re.sub(r'<Components Version="1">.*?</Components>', '<Components Version="1">%s\n\t\t\t</Components>' % items, ch, flags=re.S)
    ti = T['item'].strip('\n')
    ti = re.sub(r'ObjectID="\d+"', 'ObjectID="%s"' % nti, ti, 1)
    ti = re.sub(r'<Components ObjectRef="\d+"/>', '<Components ObjectRef="%s"/>' % nch, ti)
    ti = re.sub(r'<SubClip ObjectRef="\d+"/>', '<SubClip ObjectRef="%s"/>' % nsc, ti)
    ti = re.sub(r'\n\t\t<IntroDuration>\d+</IntroDuration>', '', ti)
    ti = re.sub(r'<MZ.SequenceActions.NextShapeComponentNumber>\d+<', '<MZ.SequenceActions.NextShapeComponentNumber>%d<' % next_shape_num, ti)
    ti = set_times2(ti, start, end)
    return nti, texts + [vc, sc, ch, ti] + comp_texts


def pil_ascent(font, size):
    return ImageFont.truetype(PIL_FONT[font], size).getmetrics()[0]


def text_width(font, size, text, tracking):
    f = ImageFont.truetype(PIL_FONT[font], size)
    return sum(f.getlength(c) for c in text) + tracking / 1000.0 * size * (len(text) - 1)


# ---------------------------------------------------------------- designs
EASE_OUT = (0.15, 0.85)      # (out influence of first key, in influence of second key): snappy start, long settle
EASE_IN = (0.70, 0.25)


def title_graphic(doc, key, start, end):
    spec = gfx_plan.TITLE[key]; x = gfx_plan.TITLE_X; yb = spec['y']
    t = lambda sec: GFX_IN + s2t(sec)
    dur = (end - start) / TPS
    o_a, o_b = EASE_OUT; i_a, i_b = EASE_IN
    name, sub = 'PAULA RADCLIFFE', spec['sub']
    y_line = yb + 14; y_sub = yb + 41
    comps, texts = [], []
    # 1 hairline: grows from the left, collapses back at the end
    lw, lh = 46.0, 2.0
    hs = (kf_scalar(t(0.00), 0, 5, 0, 1 / 3, 0, o_a) + kf_scalar(t(0.60), 100, 5, 0, o_b, 0, 1 / 3) +
          kf_scalar(t(dur - 0.55), 100, 5, 0, 1 / 3, 0, i_a) + kf_scalar(t(dur - 0.05), 0, 5, 0, i_b, 0, 1 / 3))
    op = (kf_scalar(t(0.00), 0, 5, 0, 1 / 3, 0, 0.3) + kf_scalar(t(0.20), 80, 5, 0, 0.7, 0, 1 / 3) +
          kf_scalar(t(dur - 0.30), 80, 5, 0, 1 / 3, 0, i_a) + kf_scalar(t(dur - 0.05), 0, 5, 0, i_b, 0, 1 / 3))
    c, tx = shape_layer(doc, 50, 'Title line', rect_points(lw, lh), appearance(fill=16777215), (x, y_line), (0.0, lh / 2),
                        opacity=80.0, uniform=False, scale=100.0, hscale=0.0, opacity_keys=op, hscale_keys=hs)
    comps.append(c); texts += tx
    # 2 name, 3 subtitle: fade + rise, staggered; fade out before the line collapses
    for num_, txt, font, size, trk, yy, delay, peak in ((51, name, 'ProximaNova-Semibold', 27, 160, yb, 0.12, 100.0),
                                                        (52, sub, 'ProximaNova-Light', 22, 60, y_sub, 0.26, 92.0)):
        op = (kf_scalar(t(delay), 0, 5, 0, 1 / 3, 0, o_a) + kf_scalar(t(delay + 0.50), peak, 5, 0, o_b, 0, 1 / 3) +
              kf_scalar(t(dur - 0.60), peak, 5, 0, 1 / 3, 0, i_a) + kf_scalar(t(dur - 0.25), 0, 5, 0, i_b, 0, 1 / 3))
        pk = (kf_point(t(delay), x / W, (yy + 12) / H, 5, 0, 1 / 3, 0, o_a) + kf_point(t(delay + 0.60), x / W, yy / H, 5, 0, o_b, 0, 1 / 3) +
              kf_point(t(dur - 0.60), x / W, yy / H, 5, 0, 1 / 3, 0, i_a) + kf_point(t(dur - 0.25), x / W, (yy - 6) / H, 5, 0, i_b, 0, 1 / 3))
        c, tx = text_layer(doc, num_, txt, font, size, (x, yy), tracking=trk, align=0, shadow=(45, 16, 2),
                           opacity_keys=op, pos_keys=pk, opacity=peak)
        comps.append(c); texts += tx
    return graphic_clip(doc, 'Title - Paula Radcliffe', start, end, comps, texts, 53)


def code_graphic(doc, start, end):
    t = lambda sec: GFX_IN + s2t(sec)
    o_a, o_b = EASE_OUT
    cw, ch, r = 640.0, 206.0, 30.0
    cx, cy = W / 2, H / 2
    top = cy - ch / 2
    comps, texts = [], []
    # card: rises 70 px, fades in, scales 92 -> 100 (anchor at its centre)
    op = kf_scalar(t(0.0), 0, 5, 0, 1 / 3, 0, 0.3) + kf_scalar(t(0.35), 97, 5, 0, 0.75, 0, 1 / 3)
    pk = kf_point(t(0.0), cx / W, (cy + 70) / H, 5, 0, 1 / 3, 0, o_a) + kf_point(t(0.55), cx / W, cy / H, 5, 0, o_b, 0, 1 / 3)
    sk = kf_scalar(t(0.0), 92, 5, 0, 1 / 3, 0, o_a) + kf_scalar(t(0.55), 100, 5, 0, o_b, 0, 1 / 3)
    c, tx = shape_layer(doc, 50, 'Code card', rrect_points(cw, ch, r), appearance(fill=0x0D0D0D, stroke=0x5A5A5A, stroke_w=2.0, shadow=(35, 40, 10)),
                        (cx, cy), (cw / 2, ch / 2), opacity=97.0, uniform=True, scale=100.0, hscale=100.0,
                        opacity_keys=op, pos_keys=pk, scale_keys=sk)
    comps.append(c); texts += tx
    # label + code: staggered fade + rise
    lab_font, lab_size, lab_trk = 'ProximaNova-Semibold', 25, 350
    code_font, code_size, code_trk = 'PowerGrotesk-Regular', 88, 30
    y_lab = top + 30 + pil_ascent(lab_font, lab_size)
    y_code = top + 70 + pil_ascent(code_font, code_size)
    for num_, txt, font, size, trk, yy, delay, rise, col in ((51, 'USE CODE', lab_font, lab_size, lab_trk, y_lab, 0.10, 40, 0xAFAFAF),
                                                              (52, 'TRYIMMUFIX', code_font, code_size, code_trk, y_code, 0.14, 50, 0xFFFFFF)):
        op = kf_scalar(t(delay), 0, 5, 0, 1 / 3, 0, 0.3) + kf_scalar(t(delay + 0.36), 100, 5, 0, 0.75, 0, 1 / 3)
        pk = kf_point(t(delay), cx / W, (yy + rise) / H, 5, 0, 1 / 3, 0, o_a) + kf_point(t(delay + 0.50), cx / W, yy / H, 5, 0, o_b, 0, 1 / 3)
        c, tx = text_layer(doc, num_, txt, font, size, (cx, yy), color=col, tracking=trk, align=2, shadow=None,
                           opacity_keys=op, pos_keys=pk)
        comps.append(c); texts += tx
    comps = comps[1:] + comps[:1]          # Premiere draws the first layer on top: texts first, card last (underneath)
    return graphic_clip(doc, 'Code - TRYIMMUFIX', start, end, comps, texts, 53)


# ---------------------------------------------------------------- zooms
def zoom_keys(kind, dur, spec, s_prev=None):
    """returns (slow_keys, quick_keys, slow_end_value) in media ticks from ADJ_IN"""
    t = lambda sec: ADJ_IN + s2t(sec)
    P = spec['punch']; Q, D = spec['intro']
    if kind == 'intro':
        qd = min(0.8667, dur)
        quick = kf_scalar(t(0), Q, 5, 0, 1 / 3, 0, 0.37058903365339191) + kf_scalar(t(qd), 100, 5, 0, 1, 0, 1 / 3)
        slow = kf_scalar(t(0), D, 5, 0, 1 / 3, 0, 1 / 3) + kf_scalar(t(dur), 100, 5, 0, 1 / 3, 0, 1 / 3)
        return slow, quick, 100.0
    if kind == 'push':
        rate = spec['rate']; S = 100.0 + rate * dur
        qd = min(1.1333, dur)
        quick = kf_scalar(t(0), 100, 5, 0, 1 / 3, 0, 0.28915076719576721) + kf_scalar(t(qd), P, 5, 0, 0.90951303727196586, 0, 1 / 3)
        slow = kf_scalar(t(0), 100, 0, 0, 1 / 6, rate, 1 / 6) + kf_scalar(t(dur), S, 0, rate, 1 / 6, 0, 1 / 6)
        return slow, quick, S
    if kind == 'pull':
        S = s_prev; v = (100.0 - S) / dur
        qd = min(1.1167, dur)
        quick = kf_scalar(t(0), P, 5, 0, 1 / 3, 0, 0.37058903365339191) + kf_scalar(t(qd), 100, 5, 0, 1, 0, 1 / 3)
        slow = kf_scalar(t(0), S, 0, 0, 1 / 6, v, 1 / 6) + kf_scalar(t(dur), 100, 0, v, 1 / 6, 0, 1 / 6)
        return slow, quick, 100.0
    raise ValueError(kind)


def find_zoom_template(doc, seq):
    for tr in video_tracks(doc, seq):
        for it in track_items(doc, tr):
            t = doc.raw(it.attrib['ObjectID'])
            if '<IsMuted>true</IsMuted>' in t: continue
            ch = re.search(r'<Components ObjectRef="(\d+)"', t).group(1)
            comps = chain_components(doc, ch)
            if len(comps) == 2 and all('<MatchName>AE.ADBE Geometry2</MatchName>' in doc.raw(c) for c in comps) and \
                    'Constant Zoom In Slow' in doc.raw(comps[0]):
                return it.attrib['ObjectID']
    raise RuntimeError('reference zoom template not found')


def zoom_item(doc, tmpl, start, end, slow_keys, quick_keys, anchor, names):
    t = doc.raw(tmpl)
    sc_id = re.search(r'<SubClip ObjectRef="(\d+)"', t).group(1)
    ch_id = re.search(r'<Components ObjectRef="(\d+)"', t).group(1)
    vc_id = re.search(r'<Clip ObjectRef="(\d+)"', doc.raw(sc_id)).group(1)
    comps = chain_components(doc, ch_id)          # [slow drift, quick punch] as in the reference
    new_ids, objs = [], []
    a = '%s:%s' % (repr(float(anchor[0])), repr(float(anchor[1])))
    for cid, keys, nm in zip(comps, (slow_keys, quick_keys), names):
        ncid, texts = clone_component(doc, cid, {'Anchor Point': a, 'Position': a, 'Sampling': '1'})
        for i, tx in enumerate(texts):
            if '<Name>Scale Height</Name>' in tx:
                texts[i] = set_keys(tx, keys)
        texts[0] = re.sub(r'<InstanceName>[^<]*</InstanceName>', '<InstanceName>%s</InstanceName>' % nm, texts[0])
        new_ids.append(ncid); objs += texts
    nch, chtxt = clone_chain(doc, ch_id, new_ids)
    nvc, nsc, nti = doc.new_id(), doc.new_id(), doc.new_id()
    vctxt = set_inout(strip_inline(doc.raw(vc_id).replace('ObjectID="%s"' % vc_id, 'ObjectID="%s"' % nvc, 1)), ADJ_IN, ADJ_IN + (end - start))
    vctxt = re.sub(r'<ClipID>[^<]*</ClipID>', '<ClipID>%s</ClipID>' % uuid.uuid4(), vctxt)
    sctxt = re.sub(r'(<Clip ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nvc, doc.raw(sc_id).replace('ObjectID="%s"' % sc_id, 'ObjectID="%s"' % nsc, 1))
    titxt = t.replace('ObjectID="%s"' % tmpl, 'ObjectID="%s"' % nti, 1)
    titxt = re.sub(r'(<Components ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nch, titxt)
    titxt = re.sub(r'(<SubClip ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nsc, titxt)
    titxt = set_times2(titxt, start, end)
    return nti, objs + [chtxt, vctxt, sctxt, titxt]


# ---------------------------------------------------------------- tracks
def append_objects(doc, objs):
    body = doc.txt.rstrip()
    assert body.endswith('</PremiereData>')
    doc.txt = body[:-len('</PremiereData>')].rstrip('\n') + '\n' + '\n'.join(o.strip('\n') for o in objs) + '\n</PremiereData>\n'


def add_track(doc, seq, at, template_uid):
    """insert an empty video track at index `at` (0 = V1); tracks above shift up by one"""
    vg = [doc.deref(tg.find('Second')) for tg in seq.find('TrackGroups') if doc.deref(tg.find('Second')).tag == 'VideoTrackGroup'][0]
    g = doc.raw(vg.attrib['ObjectID'])
    order = re.findall(r'<Track Index="(\d+)" ObjectURef="([^"]+)"/>', g)
    if at is None: at = len(order)
    next_id = int(re.search(r'<NextTrackID>(\d+)</NextTrackID>', g).group(1))
    new_uid = str(uuid.uuid4())
    t = doc.raw(template_uid, uid=True).replace('ObjectUID="%s"' % template_uid, 'ObjectUID="%s"' % new_uid, 1)
    t = re.sub(r'\n\t\t\t\t<TrackItems Version="1">.*?</TrackItems>', '', t, flags=re.S)
    t = re.sub(r'<Index>\d+</Index>', '<Index>%d</Index>' % at, t)
    t, n_id = re.subn(r'(<Index>\d+</Index>\s*<ID>)\d+(</ID>)', lambda m: '%s%d%s' % (m.group(1), next_id, m.group(2)), t, 1)
    assert n_id == 1, 'track ID not found'
    assert '<TrackItems' not in t
    for idx, uid in order:
        if int(idx) >= at:
            tt = doc.raw(uid, uid=True)
            doc.replace_obj(uid, re.sub(r'<Index>%s</Index>' % idx, '<Index>%d</Index>' % (int(idx) + 1), tt), uid=True)
    uids = [u for _, u in order]; uids.insert(at, new_uid)
    block = ''.join('\n\t\t\t\t<Track Index="%d" ObjectURef="%s"/>' % (i, u) for i, u in enumerate(uids))
    g = re.sub(r'<Tracks Version="1">.*?\n\t\t\t</Tracks>', '<Tracks Version="1">%s\n\t\t\t</Tracks>' % block, g, flags=re.S)
    g = g.replace('<NextTrackID>%d</NextTrackID>' % next_id, '<NextTrackID>%d</NextTrackID>' % (next_id + 1), 1)
    doc.replace_obj(vg.attrib['ObjectID'], g)
    # sequence patching state lists one entry per video track
    st = doc.raw(seq.attrib['ObjectUID'], uid=True)
    st2 = re.sub(r'(<HSL.TimelinePatchingAndTargeting.VideoPatches[^>]*>\[)(.*?)(\]</HSL)', lambda m: m.group(1) + m.group(2) + ',{"mNumber":-1,"mState":0}' + m.group(3), st, 1)
    doc.replace_obj(seq.attrib['ObjectUID'], st2, uid=True)
    append_objects(doc, [t])
    return new_uid


# ---------------------------------------------------------------- blobs
BLOB = re.compile(r'<(StartKeyframeValue|PremiereFilterPrivateData|ModificationState)( [^>]*?BinaryHash="([^"]+)")(/>|>([^<]*)</\1>)')


def normalize_blobs(txt, extra):
    data = dict(extra)
    for m in BLOB.finditer(txt):
        if m.group(4) != '/>' and m.group(5) and m.group(5).strip(): data.setdefault(m.group(3), m.group(5))
    seen, edits = set(), []
    for m in BLOB.finditer(txt):
        h = m.group(3); inline = m.group(4) != '/>' and bool((m.group(5) or '').strip())
        if h not in seen:
            seen.add(h)
            if not inline:
                assert h in data, 'no data for blob ' + h
                edits.append((m.start(), m.end(), '<%s%s>%s</%s>' % (m.group(1), m.group(2), data[h], m.group(1))))
        elif inline:
            edits.append((m.start(), m.end(), '<%s%s/>' % (m.group(1), m.group(2))))
    for s, e, rep in sorted(edits, reverse=True):
        txt = txt[:s] + rep + txt[e:]
    return txt, len(edits)


# ---------------------------------------------------------------- build
def build(src_xml, out_path, log=print):
    doc = Doc(src_xml)
    report = {}
    seqs = {s.attrib['ObjectUID'][:8]: (n, s) for n, s in for_claude_sequences(doc)}
    tmpl_zoom = find_zoom_template(doc, seqs[REF][1])
    for key, (name, seq) in seqs.items():
        trs = video_tracks(doc, seq)
        v1 = track_items(doc, trs[0])
        seq_end = max(int(t.findtext('.//TrackItem/End')) for t in v1)
        cut_ticks = sorted({int(t.findtext('.//TrackItem/Start') or 0) for t in v1} | {seq_end})
        rep = report[key] = {'name': seq.findtext('Name')}
        tmpl_track = (trs[3] if key == REF else trs[1]).attrib['ObjectUID']     # the B-roll track (plain, enabled)
        # ---- zooms (not on the reference: it has the user's own)
        if key in zoom_plan.ZOOM:
            spec = zoom_plan.ZOOM[key]
            broll_ends = sorted(int(t.findtext('.//TrackItem/End')) for t in track_items(doc, trs[1]))

            def snap(sec):
                if sec is None: return seq_end
                tk = s2t(sec)
                for c in cut_ticks + broll_ends:
                    if abs(c - tk) < 0.03 * TPS: return c
                return int(round(tk / F60)) * F60
            zt = add_track(doc, seq, 1, tmpl_track)
            ids, objs, s_prev, segs = [], [], None, []
            for seg in spec['segs']:
                kind, a, b = seg[0], snap(seg[1]), snap(seg[2])
                sp = dict(spec); sp['rate'] = seg[3] if len(seg) > 3 else 0
                slow, quick, s_end = zoom_keys(kind, (b - a) / TPS, sp, s_prev)
                names = {'intro': ('Zoom intro drift', 'Zoom intro punch'), 'push': ('Zoom drift in', 'Zoom punch in'),
                         'pull': ('Zoom drift out', 'Zoom punch out')}[kind]
                nti, o = zoom_item(doc, tmpl_zoom, a, b, slow, quick, spec['anchor'], names)
                ids.append(nti); objs += o; s_prev = s_end if kind == 'push' else None
                segs.append((kind, round(a / TPS, 3), round(b / TPS, 3)))
            assert segs[0][1] == 0 and s2t(segs[-1][2]) - seq_end < TPS * 0.001
            append_objects(doc, objs)
            set_track_items(doc, zt, ids)
            rep['zoom_segments'] = segs
        # ---- graphics on a new top track
        gt = add_track(doc, seq, None, tmpl_track)                 # new top track
        g_ids, g_objs = [], []
        a, b = s2t(gfx_plan.TITLE_IN), s2t(gfx_plan.TITLE_OUT)
        a, b = int(round(a / F60)) * F60, int(round(b / F60)) * F60
        nti, o = title_graphic(doc, key, a, b); g_ids.append((a, nti)); g_objs += o
        rep['title'] = (gfx_plan.TITLE[key]['sub'], round(a / TPS, 3), round(b / TPS, 3))
        if key in gfx_plan.CODE:
            tk = s2t(gfx_plan.CODE[key])
            a = min(cut_ticks, key=lambda c: abs(c - tk)) if min(abs(c - tk) for c in cut_ticks) < 0.03 * TPS else int(round(tk / F60)) * F60
            nti, o = code_graphic(doc, a, seq_end); g_ids.append((a, nti)); g_objs += o
            rep['code'] = (round(a / TPS, 3), round(seq_end / TPS, 3))
        append_objects(doc, g_objs)
        set_track_items(doc, gt, [x for _, x in sorted(g_ids)])
        log('%-42s zoom segs %-2s | title %s | code %s' % (seq.findtext('Name')[:42], len(rep.get('zoom_segments', [])), rep['title'][0], rep.get('code')))
    extra = dict(T['blobs']); extra.update(NEW_BLOBS)
    doc.txt, n = normalize_blobs(doc.txt, extra)
    log('blob fixes: %d, new blobs: %d' % (n, len(NEW_BLOBS)))
    xml_out = out_path + '.xml'
    open(xml_out, 'w', encoding='utf-8', newline='\n').write(doc.txt)
    with open(xml_out, 'rb') as f, gzip.open(out_path, 'wb') as g: g.write(f.read())
    return xml_out, report


if __name__ == '__main__':
    x, rep = build(sys.argv[1], sys.argv[2])
    json.dump(rep, open(sys.argv[2] + '.report.json', 'w'), indent=1)
