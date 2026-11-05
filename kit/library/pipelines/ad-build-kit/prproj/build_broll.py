"""Add B-roll to every "For claude" ad and cut the master grade around it.

Layout produced
  7 ads:       V1 talking head | V2 B-roll (Motion framing + own Lumetri) | V3 master grade, cut around B-roll
  reference:   V1 | V2 zooms (disabled) | V3 zooms | V4 B-roll | V5 master grade (both Lumetri incl. face light), cut around B-roll
Every B-roll clip gets the C108 Sony override and a copy of that ad's master Lumetri (same values).
Text-level edits only; untouched objects stay byte-identical.
"""
import sys, re, uuid, json, gzip
sys.path.insert(0, '.')
from build_project import Doc, TPS, fmt, for_claude_sequences, video_tracks, track_items, media_video_streams
sys.path.insert(0, '../work')
import broll_plan

F60 = 4233600000           # one 60 fps sequence frame in ticks
F25 = 10160640000          # one 25 fps source frame in ticks
REF = '348e0ba6'
LUMETRI_IDX = {'Temperature': 14, 'Tint': 15, 'Exposure': 19}
INLINE = re.compile(r'(<(StartKeyframeValue|PremiereFilterPrivateData)( [^>]*?BinaryHash="[^"]+"))>[^<]+</\2>')


def strip_inline(txt):
    """clones only reference blob data (the original object keeps the single inline copy)"""
    return INLINE.sub(r'\1/>', txt)


def clone_component(doc, comp_id, overrides=None):
    """deep-copy a VideoFilterComponent with params and sub-components (masks). overrides: {param Name or index: value}"""
    overrides = overrides or {}
    comp = doc.raw(comp_id); new = doc.new_id(); out = []
    for idx, pid in re.findall(r'<Param Index="(\d+)" ObjectRef="(\d+)"\s*/>', comp):
        nid = doc.new_id()
        p = strip_inline(doc.raw(pid).replace('ObjectID="%s"' % pid, 'ObjectID="%s"' % nid, 1))
        p = re.sub(r'\n\t\t<CurrentValue>[^<]*</CurrentValue>', '', p)
        name = re.search(r'<Name>([^<]*)</Name>', p); name = name.group(1) if name else None
        key = int(idx) if int(idx) in overrides else name if name in overrides else None
        if key is not None:
            m = re.search(r'<StartKeyframe>(-?\d+),([^,]+),', p)
            val = overrides[key]
            p = p[:m.start(2)] + (val if isinstance(val, str) else fmt(val)) + p[m.end(2):]
        comp = re.sub(r'(<Param Index="%s" ObjectRef=")%s("\s*/>)' % (idx, pid), r'\g<1>%s\g<2>' % nid, comp)
        out.append(p)
    for idx, sid in re.findall(r'<SubComponent Index="(\d+)" ObjectRef="(\d+)"\s*/>', comp):
        nsid, sub = clone_component(doc, sid)
        comp = re.sub(r'(<SubComponent Index="%s" ObjectRef=")%s("\s*/>)' % (idx, sid), r'\g<1>%s\g<2>' % nsid, comp)
        out += sub
    comp = strip_inline(comp.replace('ObjectID="%s"' % comp_id, 'ObjectID="%s"' % new, 1))
    return new, [comp] + out


def chain_components(doc, chain_id):
    return re.findall(r'<Component Index="\d+" ObjectRef="(\d+)"\s*/>', doc.raw(chain_id))


def clone_chain(doc, chain_id, comp_ids_texts):
    """new chain object listing the given (already cloned) component ids"""
    new = doc.new_id()
    c = doc.raw(chain_id).replace('ObjectID="%s"' % chain_id, 'ObjectID="%s"' % new, 1)
    items = ''.join('\n\t\t\t\t<Component Index="%d" ObjectRef="%s"/>' % (i, cid) for i, cid in enumerate(comp_ids_texts))
    c = re.sub(r'<Components Version="1">.*?</Components>', '<Components Version="1">%s\n\t\t\t</Components>' % items, c, flags=re.S)
    return new, c


def set_times(ti_txt, start, end):
    ti_txt = re.sub(r'\n\t\t\t\t<Start>\d+</Start>', '', ti_txt)
    ti_txt = re.sub(r'<End>\d+</End>', '<End>%d</End>' % end, ti_txt)
    if start:
        ti_txt = ti_txt.replace('<TrackItem Version="4">', '<TrackItem Version="4">\n\t\t\t\t<Start>%d</Start>' % start, 1)
    return ti_txt


def set_inout(vc_txt, tin, tout):
    vc_txt = re.sub(r'<InPoint>\d+</InPoint>', '<InPoint>%d</InPoint>' % tin, vc_txt)
    vc_txt = re.sub(r'<OutPoint>\d+</OutPoint>', '<OutPoint>%d</OutPoint>' % tout, vc_txt)
    return vc_txt


def item_parts(doc, ti):
    sc = doc.deref(ti.find('.//SubClip')); vc = doc.deref(sc.find('Clip'))
    chain = doc.deref(ti.find('.//ComponentOwner/Components'))
    return ti.attrib['ObjectID'], sc.attrib['ObjectID'], vc.attrib['ObjectID'], chain.attrib['ObjectID']


def cut_item(doc, ti, remove):
    """split an adjustment-layer item into pieces avoiding the `remove` intervals (ticks).
    The first piece re-uses the original objects (edited in place); the rest are deep clones.
    Returns (list of track-item ids in time order, new object texts)."""
    ti_id, sc_id, vc_id, ch_id = item_parts(doc, ti)
    s = int(ti.findtext('.//TrackItem/Start') or 0); e = int(ti.findtext('.//TrackItem/End'))
    in0 = int(doc.deref(doc.deref(ti.find('.//SubClip')).find('Clip')).findtext('.//InPoint'))
    pieces = [(s, e)]
    for a, b in sorted(remove):
        nxt = []
        for p, q in pieces:
            if b <= p or a >= q: nxt.append((p, q)); continue
            if a > p: nxt.append((p, a))
            if b < q: nxt.append((b, q))
        pieces = nxt
    pieces = [(p, q) for p, q in pieces if q - p >= F60]
    ids, objs = [], []
    for k, (p, q) in enumerate(pieces):
        tin, tout = in0 + (p - s), in0 + (q - s)
        if k == 0:            # edit original in place
            doc.replace_obj(ti_id, set_times(doc.raw(ti_id), p, q))
            doc.replace_obj(vc_id, set_inout(doc.raw(vc_id), tin, tout))
            ids.append(ti_id); continue
        comp_ids = []
        for cid in chain_components(doc, ch_id):
            ncid, texts = clone_component(doc, cid); comp_ids.append(ncid); objs += texts
        nch, chtxt = clone_chain(doc, ch_id, comp_ids)
        nvc = doc.new_id(); nsc = doc.new_id(); nti = doc.new_id()
        vctxt = set_inout(strip_inline(doc.raw(vc_id).replace('ObjectID="%s"' % vc_id, 'ObjectID="%s"' % nvc, 1)), tin, tout)
        vctxt = re.sub(r'<ClipID>[^<]*</ClipID>', '<ClipID>%s</ClipID>' % uuid.uuid4(), vctxt)
        sctxt = doc.raw(sc_id).replace('ObjectID="%s"' % sc_id, 'ObjectID="%s"' % nsc, 1)
        sctxt = re.sub(r'(<Clip ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nvc, sctxt)
        titxt = doc.raw(ti_id).replace('ObjectID="%s"' % ti_id, 'ObjectID="%s"' % nti, 1)
        titxt = re.sub(r'(<Components ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nch, titxt)
        titxt = re.sub(r'(<SubClip ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nsc, titxt)
        titxt = set_times(titxt, p, q)
        objs += [chtxt, vctxt, sctxt, titxt]; ids.append(nti)
    return ids, objs


def broll_item(doc, aroll_ti, master_lumetri_id, broll, start, end, src_in, px, py, scale):
    """new V2 clip: A-roll item structure, B-roll media, Motion framing + master Lumetri"""
    ti_id, sc_id, vc_id, ch_id = item_parts(doc, aroll_ti)
    motion_id = chain_components(doc, ch_id)[0]
    nmot, mtexts = clone_component(doc, motion_id, {'Position': '%.6f:%.6f' % (px, py), 'Scale': float(scale)})
    nlum, ltexts = clone_component(doc, master_lumetri_id)
    nch, chtxt = clone_chain(doc, ch_id, [nmot, nlum])
    mvc = broll['master_vclip']
    nvc = doc.new_id(); nsc = doc.new_id(); nti = doc.new_id()
    vctxt = strip_inline(doc.raw(mvc).replace('ObjectID="%s"' % mvc, 'ObjectID="%s"' % nvc, 1))
    vctxt = re.sub(r'\n\t\t\t<InUse>[^<]*</InUse>', '', vctxt)
    vctxt = re.sub(r'(<Source ObjectRef="\d+"/>)', r'\1\n\t\t\t<OutPoint>%d</OutPoint>\n\t\t\t<InPoint>%d</InPoint>' % (src_in + (end - start), src_in), vctxt, 1)
    vctxt = re.sub(r'<ClipID>[^<]*</ClipID>', '<ClipID>%s</ClipID>' % uuid.uuid4(), vctxt)
    sctxt = doc.raw(sc_id).replace('ObjectID="%s"' % sc_id, 'ObjectID="%s"' % nsc, 1)
    sctxt = re.sub(r'(<Clip ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nvc, sctxt)
    sctxt = re.sub(r'(<MasterClip ObjectURef=")[^"]+(")', r'\g<1>%s\g<2>' % broll['mc_uid'], sctxt)
    sctxt = re.sub(r'<Name>[^<]*</Name>', '<Name>%s</Name>' % broll['name'], sctxt)
    titxt = doc.raw(ti_id).replace('ObjectID="%s"' % ti_id, 'ObjectID="%s"' % nti, 1)
    titxt = re.sub(r'(<Components ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nch, titxt)
    titxt = re.sub(r'(<SubClip ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nsc, titxt)
    titxt = re.sub(r'\n\t\t\t<IsMuted>[^<]*</IsMuted>', '', titxt)
    titxt = set_times(titxt, start, end)
    return nti, mtexts + ltexts + [chtxt, vctxt, sctxt, titxt]


def set_track_items(doc, track_uid, item_ids):
    t = doc.raw(track_uid, uid=True)
    block = '<TrackItems Version="1">%s\n\t\t\t\t</TrackItems>' % ''.join(
        '\n\t\t\t\t\t<TrackItem Index="%d" ObjectRef="%s"/>' % (i, x) for i, x in enumerate(item_ids))
    if '<TrackItems' in t:
        t = re.sub(r'<TrackItems Version="1">.*?</TrackItems>', block, t, flags=re.S)
    else:
        t = t.replace('<ClipItems Version="3">\n\t\t\t\t<MediaType>', '<ClipItems Version="3">\n\t\t\t\t%s\n\t\t\t\t<MediaType>' % block, 1)
    assert block in t
    doc.replace_obj(track_uid, t, uid=True)


def override(doc, stream_id, profile):
    t = doc.raw(stream_id)
    if '<OverriddenColorSpace>' in t:
        t2 = re.sub(r'<OverriddenColorSpace>[^<]*</OverriddenColorSpace>', '<OverriddenColorSpace>%s</OverriddenColorSpace>' % profile, t)
    else:
        t2 = t.replace('<IgnoreAlpha>true</IgnoreAlpha>', '<IgnoreAlpha>true</IgnoreAlpha>\n\t\t<OverriddenColorSpace>%s</OverriddenColorSpace>\n\t\t<InputLUTSpecified>true</InputLUTSpecified>' % profile, 1)
        t2 = t2.replace('\n\t\t<OriginalImageOrientationType>', '\n\t\t<IsColorSpacOverridden>true</IsColorSpacOverridden>\n\t\t<OriginalImageOrientationType>', 1)
        assert t2.count('<IsColorSpacOverridden>') == 1 and '<OverriddenColorSpace>' in t2
    doc.replace_obj(stream_id, t2)
    return t2 != t


def build(src_xml, out_path, log=print):
    doc = Doc(src_xml)
    report = {}
    # ---- B-roll bin: master clips, media, override
    root = [c for c in doc.root if c.tag == 'RootProjectItem'][0]
    bbin = [doc.deref(i) for i in root.find('.//ProjectItemContainer/Items') if doc.deref(i).tag == 'BinProjectItem' and doc.deref(i).findtext('.//ProjectItem/Name') == 'B roll'][0]
    streams = media_video_streams(doc)
    profile = doc.byid[streams['A003_09181126_C108-esv2-50p-bg-10p-music-10p.mp4']].findtext('OverriddenColorSpace')
    assert '1012,' in profile
    brolls = {}
    for it in bbin.find('.//ProjectItemContainer/Items'):
        cpi = doc.deref(it); mc = doc.deref(cpi.find('MasterClip'))
        for c in mc.find('Clips'):
            cl = doc.deref(c)
            if cl.tag == 'VideoClip':
                src = doc.deref(cl.find('.//Source')); media = doc.deref(src.find('.//Media'))
                fname = (media.findtext('FilePath') or '').split('\\')[-1]
                if fname in streams: override(doc, streams[fname], profile)
                if '\\B roll\\' in (media.findtext('FilePath') or ''):
                    brolls[fname[:-4]] = {'mc_uid': mc.attrib['ObjectUID'], 'master_vclip': cl.attrib['ObjectID'], 'name': fname}
    log('Sony override set on %d B-roll bin clips; %d B-roll masters indexed' % (len(bbin.find('.//ProjectItemContainer/Items')), len(brolls)))
    new_objs = []
    seqs = {s.attrib['ObjectUID'][:8]: (n, s) for n, s in for_claude_sequences(doc)}
    # an empty video track (V2 of any ad) is the template for the reference's new V5
    empty_track_template = doc.raw(video_tracks(doc, seqs['404c5cb2'][1])[1].attrib['ObjectUID'], uid=True)
    assert '<TrackItems' not in empty_track_template
    for key, plan in broll_plan.PLAN.items():
        name, seq = seqs[key]
        trs = video_tracks(doc, seq)
        v1 = track_items(doc, trs[0])
        cut_ticks = sorted({int(t.findtext('.//TrackItem/Start') or 0) for t in v1} | {int(t.findtext('.//TrackItem/End')) for t in v1})
        seq_end = max(int(t.findtext('.//TrackItem/End')) for t in v1)
        def snap(sec):
            tk = sec * TPS
            for c in cut_ticks:
                if abs(c - tk) < 0.021 * TPS: return c
            return int(round(tk / F60)) * F60
        if key == REF:
            grade_track, broll_track = trs[3], trs[3]
            grade_items = track_items(doc, grade_track)
        else:
            broll_track, grade_track = trs[1], trs[2]
            assert not track_items(doc, broll_track), 'V2 not empty in ' + name
            grade_items = track_items(doc, grade_track)
        # master Lumetri to copy onto B-roll: the un-masked Lumetri of the first grade item
        ch = doc.deref(grade_items[0].find('.//ComponentOwner/Components'))
        master_lum = [cid for cid in chain_components(doc, ch.attrib['ObjectID']) if doc.byid[cid].find('SubComponents') is None][0]
        # B-roll items
        intervals, b_ids = [], []
        for it in sorted(plan, key=lambda d: d['t0']):
            a, b = snap(it['t0']), snap(it['t1']); b = min(b, seq_end)
            s = it['scale'] / 100.0
            px = (540 - (it['cx'] * 6048 - 3024) * s) / 1080
            py = it.get('py', 0.5)
            src_in = int(round(it['src'] * 25)) * F25
            nti, objs = broll_item(doc, v1[0], master_lum, brolls[it['clip']], a, b, src_in, px, py, it['scale'])
            b_ids.append(nti); new_objs += objs; intervals.append((a, b))
        for (a1, b1), (a2, b2) in zip(intervals, intervals[1:]): assert b1 <= a2, ('overlap', name, b1, a2)
        # cut the master grade
        piece_ids = []
        for gi in grade_items:
            ids, objs = cut_item(doc, gi, intervals); piece_ids += ids; new_objs += objs
        if key == REF:
            # new top track V5 for the grade pieces, B-roll goes on V4
            new_uid = str(uuid.uuid4())
            vg = [doc.deref(tg.find('Second')) for tg in seq.find('TrackGroups') if doc.deref(tg.find('Second')).tag == 'VideoTrackGroup'][0]
            next_id = int(vg.findtext('.//NextTrackID'))
            t = empty_track_template.replace(re.search(r'ObjectUID="([^"]+)"', empty_track_template).group(1), new_uid, 1)
            t = re.sub(r'<Index>\d+</Index>', '<Index>4</Index>', t)
            t = re.sub(r'<ID>\d+</ID>', '<ID>%d</ID>' % next_id, t)
            new_objs.append(t)
            g = doc.raw(vg.attrib['ObjectID'])
            g = g.replace('\n\t\t\t</Tracks>', '\n\t\t\t\t<Track Index="4" ObjectURef="%s"/>\n\t\t\t</Tracks>' % new_uid, 1)
            g = g.replace('<NextTrackID>%d</NextTrackID>' % next_id, '<NextTrackID>%d</NextTrackID>' % (next_id + 1), 1)
            doc.replace_obj(vg.attrib['ObjectID'], g)
            set_track_items(doc, broll_track.attrib['ObjectUID'], b_ids)
            pending_v5 = (new_uid, piece_ids)
        else:
            set_track_items(doc, broll_track.attrib['ObjectUID'], b_ids)
            set_track_items(doc, grade_track.attrib['ObjectUID'], piece_ids)
        cover = sum(b - a for a, b in intervals) / seq_end
        report[key] = {'name': seq.findtext('Name'), 'broll': len(b_ids), 'grade_pieces': len(piece_ids), 'coverage': round(cover * 100, 1)}
        log('%-45s B-roll %d clips (%.0f%% of %.1fs), grade cut into %d pieces' % (seq.findtext('Name')[:45], len(b_ids), cover * 100, seq_end / TPS, len(piece_ids)))
    body = doc.txt.rstrip()
    assert body.endswith('</PremiereData>')
    body = body[:-len('</PremiereData>')].rstrip('\n')
    # new V5 track needs its TrackItems filled after it exists in the text
    doc.txt = body + '\n' + '\n'.join(new_objs) + '\n</PremiereData>\n'
    uid, ids = pending_v5
    set_track_items(doc, uid, ids)
    xml_out = out_path + '.xml'
    open(xml_out, 'w', encoding='utf-8', newline='\n').write(doc.txt)
    with open(xml_out, 'rb') as f, gzip.open(out_path, 'wb') as g: g.write(f.read())
    return xml_out, report


if __name__ == '__main__':
    x, rep = build(sys.argv[1], sys.argv[2])
    json.dump(rep, open(sys.argv[2] + '.report.json', 'w'), indent=1)
