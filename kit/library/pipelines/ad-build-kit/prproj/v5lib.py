"""v5 helpers: effect components cloned from real Premiere templates (Gaussian Blur, Tint, Mask2), adjustment-layer clips
with arbitrary effects, mask path blobs, keyframe strings, disabling track items."""
import re, json, struct, uuid, os
import build_zoom_gfx as Z
from build_project import TPS, fmt
from build_broll import strip_inline, chain_components, clone_chain, set_inout
from build_ext import set_times2

HERE = os.path.dirname(os.path.abspath(__file__))
ADJ_IN = Z.ADJ_IN
GBLUR = json.load(open(os.path.join(HERE, 'tmpl_gblur.json')))
TINT = json.load(open(os.path.join(HERE, 'tmpl_tint.json')))
_MASK_TMPL = {}


def mask_template_id(doc):
    """the Mask2 sub-component with a real path (face light in the reference sequence); found by type, never by a fixed id"""
    if doc in _MASK_TMPL: return _MASK_TMPL[doc]
    for m in re.finditer(r'\n\t<VideoFilterComponent ObjectID="(\d+)"', doc.txt):
        oid = m.group(1); t = doc.raw(oid)
        if '<MatchName>AE.ADBE AEMask2</MatchName>' not in t: continue
        for pid in re.findall(r'<Param Index="\d+" ObjectRef="(\d+)"', t):
            p = doc.raw(pid)
            if '<Name>Path</Name>' in p and re.search(r'BinaryHash="[^"]+"\s*>[A-Za-z0-9+/=\s]{60,}<', p):
                _MASK_TMPL[doc] = oid; return oid
    raise KeyError('no Mask2 template with a path')


def num(v):
    v = float(v)
    return repr(v) if v != int(v) else '%d.' % v


def kf_scalar(t, v, interp=0):
    return '%d,%s,%d,0,0,0.33333333333333331,0,0.33333333333333331;' % (t, num(v), interp)


def kf_point(t, x, y, interp=0):
    return '%d,%s:%s,%d,0,0,0.33333333333333331,0,0.33333333333333331,5,4,0,0,0,0;' % (t, repr(float(x)), repr(float(y)), interp)


def color64(r, g, b, a=255):
    return str((a << 56) | (r << 40) | (g << 24) | (b << 8))


def path_blob(pts, closed=True):
    """pts: list of (x, y, inx, iny, outx, outy) normalized to the layer frame (absolute tangent positions)"""
    b = struct.pack('<III', 2, 1, 31062) + b'\x00' + struct.pack('<II', 2, len(pts))
    for p in pts: b += struct.pack('<I6f', 1, *p)
    return b + (b'\x01' if closed else b'\x00')


def poly_pts(corners):
    return [(x, y, x, y, x, y) for x, y in corners]


def rrect_pts(x0, y0, x1, y1, r, W=1080.0, H=1920.0):
    """rounded rectangle in pixels -> 8 bezier vertices normalized (clockwise from top-left arc end)"""
    k = 0.5523 * r
    P = []
    def v(x, y, ix, iy, ox, oy): P.append((x / W, y / H, ix / W, iy / H, ox / W, oy / H))
    v(x0 + r, y0, x0 + r - k, y0, x0 + r, y0); v(x1 - r, y0, x1 - r, y0, x1 - r + k, y0)
    v(x1, y0 + r, x1, y0 + r - k, x1, y0 + r); v(x1, y1 - r, x1, y1 - r, x1, y1 - r + k)
    v(x1 - r, y1, x1 - r + k, y1, x1 - r, y1); v(x0 + r, y1, x0 + r, y1, x0 + r - k, y1)
    v(x0, y1 - r, x0, y1 - r + k, x0, y1 - r); v(x0, y0 + r, x0, y0 + r, x0, y0 + r - k)
    return P


def _set_param(ptxt, value=None, keys=None):
    if value is not None: ptxt = Z.set_value(ptxt, value)
    if keys: ptxt = Z.set_keys(ptxt, keys)
    ptxt = re.sub(r'\n\t\t<CurrentValue>[^<]*</CurrentValue>', '', ptxt)
    return ptxt


def _clone(doc, comp_txt, param_txts, cid_in_chain, instance, values, keys, blobs=None, sub_ids=None):
    """clone a component + params with fresh ObjectIDs; values/keys/blobs keyed by param Name (or ParameterID as 'pid:N')"""
    ncomp = doc.new_id(); texts = []; refs = []
    for pt in param_txts:
        oid = re.search(r'ObjectID="(\d+)"', pt).group(1); nid = doc.new_id()
        t = pt.replace('ObjectID="%s"' % oid, 'ObjectID="%s"' % nid, 1)
        nm = re.search(r'<Name>([^<]*)</Name>', t); nm = nm.group(1) if nm else ''
        pid = 'pid:' + re.search(r'<ParameterID>(\d+)</ParameterID>', t).group(1)
        if not any(k in keys and keys[k] for k in (nm, pid)):      # template animation must never leak into the clone
            t = re.sub(r'\n\t*<Keyframes>[^<]*</Keyframes>', '', t)
            t = t.replace('<IsTimeVarying>true</IsTimeVarying>', '<IsTimeVarying>false</IsTimeVarying>')
        for key in (nm, pid):
            if key in values or key in keys:
                t = _set_param(t, values.get(key), keys.get(key))
            if blobs and key in blobs:
                t = Z.set_blob(t, blobs[key])
        texts.append(t); refs.append(nid)
    c = comp_txt
    oid = re.search(r'ObjectID="(\d+)"', c).group(1)
    c = c.replace('ObjectID="%s"' % oid, 'ObjectID="%s"' % ncomp, 1)
    old = re.findall(r'<Param Index="(\d+)" ObjectRef="(\d+)"/>', c)
    for (idx, o), n in zip(old, refs): c = c.replace('<Param Index="%s" ObjectRef="%s"/>' % (idx, o), '<Param Index="%s" ObjectRef="%s"/>' % (idx, n), 1)
    c = re.sub(r'<ID>\d+</ID>', '<ID>%d</ID>' % cid_in_chain, c, 1)
    if instance is not None:
        if '<InstanceName>' in c: c = re.sub(r'<InstanceName>[^<]*</InstanceName>', '<InstanceName>%s</InstanceName>' % instance, c, 1)
        else: c = c.replace('</DisplayName>', '</DisplayName>\n\t\t\t<InstanceName>%s</InstanceName>' % instance, 1)
    c = re.sub(r'\n\t\t<SubComponents Version="1">.*?</SubComponents>', '', c, flags=re.S)
    if sub_ids:
        blk = '\n\t\t<SubComponents Version="1">' + ''.join('\n\t\t\t<SubComponent Index="%d" ObjectRef="%s"/>' % (i, s) for i, s in enumerate(sub_ids)) + '\n\t\t</SubComponents>'
        c = c.replace('\n\t\t<MatchName>', blk + '\n\t\t<MatchName>', 1)
        if 'NextComponentNumber' not in c:
            c = c.replace('<Component Version="7">', '<Component Version="7">\n\t\t\t<Node Version="1">\n\t\t\t\t<Properties Version="1">\n'
                          '\t\t\t\t\t<BE.VideoFilterComponent.NextComponentNumber>%d</BE.VideoFilterComponent.NextComponentNumber>\n'
                          '\t\t\t\t</Properties>\n\t\t\t</Node>' % (len(sub_ids) + 1), 1) if '<Node Version="1">' not in c.split('<Params')[0] else \
                c.replace('<Properties Version="1">', '<Properties Version="1">\n\t\t\t\t\t<BE.VideoFilterComponent.NextComponentNumber>%d</BE.VideoFilterComponent.NextComponentNumber>' % (len(sub_ids) + 1), 1)
    return ncomp, [c] + texts


def mask_component(doc, n, path, feather=12.0, expansion=0.0, opacity=100.0, mtype=1, pos=None, anchor=None,
                   pos_keys=None, rot_keys=None, sw_keys=None, sh_keys=None, op_keys=None, inverted=False):
    """Premiere Mask2 sub-component. path = list of vertex tuples (normalized). pos/anchor normalized 'x:y' strings or tuples."""
    ct = doc.raw(mask_template_id(doc))
    assert '<MatchName>AE.ADBE AEMask2</MatchName>' in ct
    pts = [doc.raw(p) for p in re.findall(r'<Param Index="\d+" ObjectRef="(\d+)"', ct)]
    xs = [p[0] for p in path]; ys = [p[1] for p in path]
    c = ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2)
    anchor = anchor or c; pos = pos or anchor
    pstr = lambda q: '%s:%s' % (repr(float(q[0])), repr(float(q[1])))
    values = {'Position': pstr(pos), 'Anchor Point': pstr(anchor), 'Feather': num(feather), 'Expansion': num(expansion),
              'Opacity': num(opacity), 'Type': str(mtype), 'Scale': '1:1', 'Scale Height': '100.', 'Scale Width': '100.', 'Rotation': '0.',
              'Uniform Scale': 'false', 'pid:17': 'true' if inverted else 'false'}
    keys = {}
    if pos_keys: keys['Position'] = pos_keys
    if rot_keys: keys['Rotation'] = rot_keys
    if sw_keys: keys['Scale Width'] = sw_keys
    if sh_keys: keys['Scale Height'] = sh_keys
    if op_keys: keys['Opacity'] = op_keys
    ncomp, texts = _clone(doc, ct, pts, 0, '%02d' % n, values, keys, blobs={'Path': path_blob(path)})
    texts[0] = re.sub(r'<InstanceName>[^<]*</InstanceName>', '<InstanceName>%02d</InstanceName>' % n, texts[0])
    return ncomp, texts


def gblur_component(doc, cid, blurriness, instance, mask_ids=None, blur_keys=None):
    return _clone(doc, GBLUR['comp'], GBLUR['params'], cid, instance, {'Blurriness': num(blurriness), 'pid:3': 'true'},
                  {'Blurriness': blur_keys} if blur_keys else {}, sub_ids=mask_ids)


def tint_component(doc, cid, white_rgb, amount, instance, mask_ids=None, amount_keys=None):
    return _clone(doc, TINT['comp'], TINT['params'], cid, instance,
                  {'Map Black To': color64(0, 0, 0), 'Map White To': color64(*white_rgb), 'Amount to Tint': num(amount)},
                  {'Amount to Tint': amount_keys} if amount_keys else {}, sub_ids=mask_ids)


def adj_item(doc, tmpl_ti, start, end, comp_ids, name=None):
    """new adjustment-layer clip on the structure of an existing one (zoom layer), carrying the given components"""
    t = doc.raw(tmpl_ti)
    sc_id = re.search(r'<SubClip ObjectRef="(\d+)"', t).group(1)
    ch_id = re.search(r'<Components ObjectRef="(\d+)"', t).group(1)
    vc_id = re.search(r'<Clip ObjectRef="(\d+)"', doc.raw(sc_id)).group(1)
    nch, chtxt = clone_chain(doc, ch_id, comp_ids)
    nvc, nsc, nti = doc.new_id(), doc.new_id(), doc.new_id()
    vctxt = set_inout(strip_inline(doc.raw(vc_id).replace('ObjectID="%s"' % vc_id, 'ObjectID="%s"' % nvc, 1)), ADJ_IN, ADJ_IN + (end - start))
    vctxt = re.sub(r'<ClipID>[^<]*</ClipID>', '<ClipID>%s</ClipID>' % uuid.uuid4(), vctxt)
    sctxt = re.sub(r'(<Clip ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nvc, doc.raw(sc_id).replace('ObjectID="%s"' % sc_id, 'ObjectID="%s"' % nsc, 1))
    if name: sctxt = re.sub(r'<Name>[^<]*</Name>', '<Name>%s</Name>' % name, sctxt, 1)
    titxt = t.replace('ObjectID="%s"' % tmpl_ti, 'ObjectID="%s"' % nti, 1)
    titxt = re.sub(r'(<Components ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nch, titxt)
    titxt = re.sub(r'(<SubClip ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nsc, titxt)
    titxt = re.sub(r'\n\t\t\t<IsMuted>[^<]*</IsMuted>', '', titxt)
    titxt = set_times2(titxt, start, end)
    return nti, [chtxt, vctxt, sctxt, titxt]


def disable_item(doc, ti):
    t = doc.raw(ti)
    if '<IsMuted>true</IsMuted>' in t: return False
    t2 = re.sub(r'(\n(\t+)<SubClip ObjectRef="\d+"/>)', lambda m: m.group(1) + '\n' + m.group(2) + '<IsMuted>true</IsMuted>', t, 1)
    assert t2 != t
    doc.replace_obj(ti, t2)
    return True
