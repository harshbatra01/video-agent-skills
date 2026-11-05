"""Build a graded copy of the Immufix Premiere project.

Text-level surgery on the decompressed .prproj XML so untouched content stays byte-identical:
  1. Sony colour-space override (same value as C108, the reference) on every clip the ads use.
  2. One adjustment layer on V3 of each "For claude" ad (except the reference, Sequence 04),
     spanning the whole ad, carrying a clone of the reference's main Lumetri Color
     (curves, wheels, vignette etc. identical) with optional per-ad slider overrides.

Usage (from python):  build(src_xml, out_prproj, overrides={seq_uid: {param_index: value}})
"""
import re, uuid, gzip, json, sys, os
import xml.etree.ElementTree as ET

TPS = 254016000000
ADJ_IN = 914457600000000            # adjustment-layer media starts at 1 hour
REF_SEQ = '348e0ba6-6399-40a6-9ee0-464c6e30c80f'   # "Sequence 04" / I'm 52 now reframed Copy 01 (reference)
ADJ_MASTER = 'e91c2436-c194-4ff9-8cf5-08b1fa146b8c'  # "Adjustment Layer" master clip used by the reference
REF_OVERRIDE = 'OverriddenColorSpace'

# Lumetri param index -> name (main-grade sliders we may touch)
LUMETRI = {'Temperature': 14, 'Tint': 15, 'Saturation': 16, 'Exposure': 19, 'Contrast': 20, 'Highlights': 21,
           'Shadows': 22, 'Whites': 23, 'Blacks': 24, 'FadedFilm': 40, 'Sharpen': 41, 'Vibrance': 42,
           'CreativeSaturation': 43, 'VignetteAmount': 110}


def fmt(v):
    s = ('%.6f' % float(v)).rstrip('0')
    return s if s != '-0.' else '0.'


class Doc:
    def __init__(self, path):
        self.txt = open(path, encoding='utf-8').read()
        self.root = ET.fromstring(self.txt)
        self.byid = {e.attrib['ObjectID']: e for e in self.root if 'ObjectID' in e.attrib}
        self.byuid = {e.attrib['ObjectUID']: e for e in self.root if 'ObjectUID' in e.attrib}
        self.next_id = max(int(k) for k in self.byid) + 1

    def deref(self, e):
        if e is None: return None
        if 'ObjectRef' in e.attrib: return self.byid.get(e.attrib['ObjectRef'])
        if 'ObjectURef' in e.attrib: return self.byuid.get(e.attrib['ObjectURef'])
        return e

    def new_id(self):
        i = self.next_id; self.next_id += 1; return str(i)

    # raw text of a top-level object
    def span(self, key, uid=False):
        attr = 'ObjectUID' if uid else 'ObjectID'
        m = re.search(r'\n\t<(\w+) %s="%s" ' % (attr, re.escape(key)), self.txt)
        if not m: raise KeyError(key)
        tag = m.group(1); start = m.start() + 1
        close = '\n\t</%s>' % tag
        end = self.txt.index(close, start) + len(close)
        return start, end

    def raw(self, key, uid=False):
        s, e = self.span(key, uid); return self.txt[s:e]

    def replace_obj(self, key, new_text, uid=False):
        s, e = self.span(key, uid); self.txt = self.txt[:s] + new_text + self.txt[e:]


def media_video_streams(doc):
    """file name -> VideoStream ObjectID"""
    out = {}
    for e in doc.root:
        if e.tag != 'Media': continue
        fp = e.findtext('FilePath') or ''
        vs = e.find('VideoStream')
        if vs is not None and 'ObjectRef' in vs.attrib:
            out[fp.split('\\')[-1]] = vs.attrib['ObjectRef']
    return out


def for_claude_sequences(doc):
    root = [c for c in doc.root if c.tag == 'RootProjectItem'][0]
    fc = None
    for it in root.find('.//ProjectItemContainer/Items'):
        e = doc.deref(it)
        if e.tag == 'BinProjectItem' and e.findtext('.//ProjectItem/Name') == 'For claude': fc = e
    seqs = []
    for it in fc.find('.//ProjectItemContainer/Items'):
        cpi = doc.deref(it); mc = doc.deref(cpi.find('MasterClip'))
        for c in mc.find('Clips'):
            src = doc.deref(doc.deref(c).find('.//Source'))
            if src is not None and src.tag == 'VideoSequenceSource':
                seqs.append((cpi.findtext('.//ProjectItem/Name'), doc.byuid[src.find('.//Sequence').attrib['ObjectURef']]))
                break
    return seqs


def video_tracks(doc, seq):
    for tg in seq.find('TrackGroups'):
        g = doc.deref(tg.find('Second'))
        if g.tag == 'VideoTrackGroup':
            return [doc.byuid[t.attrib['ObjectURef']] for t in g.find('.//Tracks')]


def track_items(doc, tr):
    items = tr.find('.//ClipItems/TrackItems')
    return [doc.deref(i) for i in items] if items is not None else []


def seq_media_files(doc, seq):
    files = set()
    for tr in video_tracks(doc, seq):
        for ti in track_items(doc, tr):
            sc = doc.deref(ti.find('.//SubClip')); clip = doc.deref(sc.find('Clip'))
            src = doc.deref(clip.find('.//Source'))
            if src is not None and src.tag == 'VideoMediaSource':
                m = doc.deref(src.find('.//Media'))
                fp = m.findtext('FilePath') or ''
                if fp.lower().endswith('.mp4'): files.add(fp.split('\\')[-1])
    return files


def reference_template(doc):
    """(track item id, subclip id, videoclip id, chain id, main lumetri id) of the reference's first V4 layer"""
    seq = doc.byuid[REF_SEQ]
    v4 = video_tracks(doc, seq)[3]
    ti = track_items(doc, v4)[0]
    chain = doc.deref(ti.find('.//ComponentOwner/Components'))
    comps = [doc.deref(c) for c in chain.find('.//ComponentChain/Components')]
    main = [c for c in comps if c.find('SubComponents') is None][0]   # the un-masked Lumetri = main grade
    sc = doc.deref(ti.find('.//SubClip')); vc = doc.deref(sc.find('Clip'))
    return ti.attrib['ObjectID'], sc.attrib['ObjectID'], vc.attrib['ObjectID'], chain.attrib['ObjectID'], main.attrib['ObjectID']


def clone_lumetri(doc, main_id, overrides):
    """returns (new component id, [object texts])"""
    comp_txt = doc.raw(main_id)
    new_comp = doc.new_id()
    texts = []
    param_refs = re.findall(r'<Param Index="(\d+)" ObjectRef="(\d+)"\s*/>', comp_txt)
    mapping = {}
    for idx, pid in param_refs:
        nid = doc.new_id(); mapping[pid] = nid
        ptxt = doc.raw(pid)
        ptxt = ptxt.replace('ObjectID="%s"' % pid, 'ObjectID="%s"' % nid, 1)
        ptxt = re.sub(r'\n\t\t<CurrentValue>[^<]*</CurrentValue>', '', ptxt)      # drop stale UI caches
        i = int(idx)
        for name, pidx in LUMETRI.items():
            if pidx == i and name in overrides:
                m = re.search(r'<StartKeyframe>(-?\d+),([^,]+),', ptxt)
                assert m, (name, ptxt[:200])
                ptxt = ptxt[:m.start(2)] + fmt(overrides[name]) + ptxt[m.end(2):]
        texts.append(ptxt)
    for pid, nid in mapping.items():
        comp_txt = re.sub(r'(<Param Index="\d+" ObjectRef=")%s("\s*/>)' % pid, r'\g<1>%s\g<2>' % nid, comp_txt)
    comp_txt = comp_txt.replace('ObjectID="%s"' % main_id, 'ObjectID="%s"' % new_comp, 1)
    return new_comp, [comp_txt] + texts


def add_adjustment_layer(doc, seq, tmpl, overrides, clip_name='Adjustment Layer'):
    ti_id, sc_id, vc_id, chain_id, main_id = tmpl
    trs = video_tracks(doc, seq)
    v1_end = max(int(ti.findtext('.//TrackItem/End')) for ti in track_items(doc, trs[0]))
    target = trs[2]                                   # V3
    assert not track_items(doc, target), 'V3 is not empty in ' + seq.findtext('Name')
    lum_id, lum_texts = clone_lumetri(doc, main_id, overrides)
    n_ti, n_sc, n_vc, n_chain = doc.new_id(), doc.new_id(), doc.new_id(), doc.new_id()
    # component chain: one Lumetri, id 3 (first effect after Motion=1, Opacity=2)
    chain = doc.raw(chain_id).replace('ObjectID="%s"' % chain_id, 'ObjectID="%s"' % n_chain, 1)
    chain = re.sub(r'<Components Version="1">.*?</Components>',
                   '<Components Version="1">\n\t\t\t\t<Component Index="0" ObjectRef="%s"/>\n\t\t\t</Components>' % lum_id,
                   chain, flags=re.S)
    ti = doc.raw(ti_id).replace('ObjectID="%s"' % ti_id, 'ObjectID="%s"' % n_ti, 1)
    ti = re.sub(r'(<Components ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % n_chain, ti)
    ti = re.sub(r'(<SubClip ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % n_sc, ti)
    ti = re.sub(r'<Start>\d+</Start>', '', ti)
    ti = re.sub(r'<End>\d+</End>', '<End>%d</End>' % v1_end, ti)
    sc = doc.raw(sc_id).replace('ObjectID="%s"' % sc_id, 'ObjectID="%s"' % n_sc, 1)
    sc = re.sub(r'(<Clip ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % n_vc, sc)
    sc = re.sub(r'<Name>[^<]*</Name>', '<Name>%s</Name>' % clip_name, sc)
    vc = doc.raw(vc_id).replace('ObjectID="%s"' % vc_id, 'ObjectID="%s"' % n_vc, 1)
    vc = re.sub(r'<InPoint>\d+</InPoint>', '<InPoint>%d</InPoint>' % ADJ_IN, vc)
    vc = re.sub(r'<OutPoint>\d+</OutPoint>', '<OutPoint>%d</OutPoint>' % (ADJ_IN + v1_end), vc)
    vc = re.sub(r'<ClipID>[^<]*</ClipID>', '<ClipID>%s</ClipID>' % uuid.uuid4(), vc)
    # hook the item into V3
    tuid = target.attrib['ObjectUID']
    ttxt = doc.raw(tuid, uid=True)
    assert '<TrackItems' not in ttxt
    ttxt2 = ttxt.replace('<ClipItems Version="3">\n\t\t\t\t<MediaType>',
                         '<ClipItems Version="3">\n\t\t\t\t<TrackItems Version="1">\n\t\t\t\t\t<TrackItem Index="0" ObjectRef="%s"/>\n\t\t\t\t</TrackItems>\n\t\t\t\t<MediaType>' % n_ti, 1)
    assert ttxt2 != ttxt, 'could not hook track'
    doc.replace_obj(tuid, ttxt2, uid=True)
    new_objs = [ti, sc, vc, chain] + lum_texts
    return v1_end, new_objs


def set_override(doc, stream_id, profile_json):
    t = doc.raw(stream_id)
    if REF_OVERRIDE in t:
        t2 = re.sub(r'<OverriddenColorSpace>[^<]*</OverriddenColorSpace>', '<OverriddenColorSpace>%s</OverriddenColorSpace>' % profile_json, t)
    else:
        t2 = t.replace('<IgnoreAlpha>true</IgnoreAlpha>',
                       '<IgnoreAlpha>true</IgnoreAlpha>\n\t\t<OverriddenColorSpace>%s</OverriddenColorSpace>\n\t\t<InputLUTSpecified>true</InputLUTSpecified>' % profile_json, 1)
        t2 = t2.replace('<FieldTypeIsUncertain>true</FieldTypeIsUncertain>',
                        '<FieldTypeIsUncertain>true</FieldTypeIsUncertain>\n\t\t<IsColorSpacOverridden>true</IsColorSpacOverridden>', 1)
        assert '<IsColorSpacOverridden>' in t2 and '<OverriddenColorSpace>' in t2, 'override insert failed for ' + stream_id
    changed = t2 != t
    doc.replace_obj(stream_id, t2)
    return changed


def build(src_xml, out_path, overrides=None, clip_name='Adjustment Layer', log=print):
    overrides = overrides or {}
    doc = Doc(src_xml)
    streams = media_video_streams(doc)
    ref_stream = streams['A003_09181126_C108-esv2-50p-bg-10p-music-10p.mp4']
    profile = doc.byid[ref_stream].findtext('OverriddenColorSpace')
    assert profile and '1012,' in profile
    tmpl = reference_template(doc)
    seqs = [(n, s) for n, s in for_claude_sequences(doc) if s.attrib['ObjectUID'] != REF_SEQ]
    # 1. overrides on every clip used by the ads
    files = set()
    for n, s in seqs: files |= seq_media_files(doc, s)
    for f in sorted(files):
        ch = set_override(doc, streams[f], profile)
        log('override %-60s %s' % (f, 'set' if ch else 'already C108 option'))
    # 2. adjustment layers
    new_objs = []
    for n, s in seqs:
        uid = s.attrib['ObjectUID']
        end, objs = add_adjustment_layer(doc, s, tmpl, overrides.get(uid, {}), clip_name)
        new_objs += objs
        log('grade layer on V3 of %-45s 0 - %.2fs  overrides=%s' % (s.findtext('Name')[:45], end / TPS, overrides.get(uid, {})))
    tail = '\n</PremiereData>'
    assert doc.txt.rstrip().endswith('</PremiereData>')
    body = doc.txt.rstrip()[:-len('</PremiereData>')].rstrip('\n')
    doc.txt = body + '\n' + '\n'.join(new_objs) + tail + '\n'
    xml_out = out_path + '.xml'
    open(xml_out, 'w', encoding='utf-8', newline='\n').write(doc.txt)
    with open(xml_out, 'rb') as f, gzip.open(out_path, 'wb') as g: g.write(f.read())
    return xml_out


if __name__ == '__main__':
    src, out = sys.argv[1], sys.argv[2]
    ov = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else {}
    build(src, out, ov)
