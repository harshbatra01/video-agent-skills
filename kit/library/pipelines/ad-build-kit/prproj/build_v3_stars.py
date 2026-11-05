"""Place the AE star animation (ProRes 4444 + alpha, imported by Premiere) on the 1 star ad's graphics track.
usage: python build_v3_stars.py saved_v3.xml out.prproj [--probe]"""
import sys, re, gzip, uuid
sys.path.insert(0, '.')
from build_project import Doc, TPS, fmt, for_claude_sequences, video_tracks, track_items
from build_broll import strip_inline, clone_component, chain_components, clone_chain, set_track_items
from build_ext import set_times2, item_times
import build_zoom_gfx as Z

AD = 'cd03e189'
MEDIA = 'stars_1of5_alpha.mov'
F60 = 4233600000
START, END = 33 * F60, 228 * F60            # 0.55s -> 3.80s: gold star lands on "star" (1.0s), gone before the title
POS = (0.5, 1150 / 1920)                   # stars centre at y=1150, just under the caption line


def master(doc):
    for e in doc.root:
        if e.tag == 'ClipProjectItem' and e.findtext('.//ProjectItem/Name') == MEDIA:
            mc = doc.deref(e.find('MasterClip'))
            vc = [doc.deref(c) for c in mc.find('Clips') if doc.deref(c).tag == 'VideoClip'][0]
            return vc.attrib['ObjectID'], mc.attrib['ObjectUID']
    raise KeyError(MEDIA + ' not imported yet')


def static(ptxt):
    """drop keyframes from a cloned param so it holds its start value"""
    ptxt = re.sub(r'\n\t*<Keyframes>[^<]*</Keyframes>', '', ptxt)
    return ptxt.replace('<IsTimeVarying>true</IsTimeVarying>', '<IsTimeVarying>false</IsTimeVarying>')


def main(src, out, probe=False):
    doc = Doc(src)
    seq = [s for n, s in for_claude_sequences(doc) if s.attrib['ObjectUID'].startswith(AD)][0]
    trs = video_tracks(doc, seq)
    top, broll = trs[-1], trs[2]
    # template: a camera/stock B-roll item with a Motion component
    cands = []
    for it in track_items(doc, broll):
        tid = it.attrib['ObjectID']; ch = re.search(r'<Components ObjectRef="(\d+)"', doc.raw(tid)).group(1)
        names = [re.search(r'<MatchName>([^<]*)<', doc.raw(c)).group(1) for c in chain_components(doc, ch)]
        cands.append((tid, ch, names))
    if probe:
        for c in cands: print(c[0], round(item_times(doc, c[0])[0] / TPS, 2), c[2])
        print('top items', [(round(a / TPS, 2), round(b / TPS, 2)) for a, b, *_ in (item_times(doc, i.attrib['ObjectID']) for i in track_items(doc, top))])
        print(re.sub(r'<Param Index[^>]*/>\n?', '', doc.raw(cands[0][0]))[:1500])
        return
    tmpl, ch_id, names = [c for c in cands if 'AE.ADBE Motion' in c[2]][0]
    t = doc.raw(tmpl)
    mot = [c for c in chain_components(doc, ch_id) if '<MatchName>AE.ADBE Motion</MatchName>' in doc.raw(c)][0]
    nmot, mtexts = clone_component(doc, mot, {'Position': '%.6f:%.6f' % POS, 'Scale': 100.0})
    mtexts = [mtexts[0]] + [static(p) for p in mtexts[1:]]
    nch, chtxt = clone_chain(doc, ch_id, [nmot])
    mvc, mc_uid = master(doc)
    nvc, nsc, nti = doc.new_id(), doc.new_id(), doc.new_id()
    vctxt = strip_inline(doc.raw(mvc).replace('ObjectID="%s"' % mvc, 'ObjectID="%s"' % nvc, 1))
    vctxt = re.sub(r'\n\t\t\t<InUse>[^<]*</InUse>', '', vctxt)
    vctxt = re.sub(r'\n\t\t\t<(In|Out)Point>[^<]*</(In|Out)Point>', '', vctxt)
    vctxt = re.sub(r'(<Source ObjectRef="\d+"/>)', r'\1\n\t\t\t<OutPoint>%d</OutPoint>\n\t\t\t<InPoint>%d</InPoint>' % (END - START, 0), vctxt, 1)
    vctxt = re.sub(r'<ClipID>[^<]*</ClipID>', '<ClipID>%s</ClipID>' % uuid.uuid4(), vctxt)
    sc_id = re.search(r'<SubClip ObjectRef="(\d+)"', t).group(1)
    sctxt = doc.raw(sc_id).replace('ObjectID="%s"' % sc_id, 'ObjectID="%s"' % nsc, 1)
    sctxt = re.sub(r'(<Clip ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nvc, sctxt)
    sctxt = re.sub(r'(<MasterClip ObjectURef=")[^"]+(")', r'\g<1>%s\g<2>' % mc_uid, sctxt)
    sctxt = re.sub(r'<Name>[^<]*</Name>', '<Name>%s</Name>' % MEDIA, sctxt)
    titxt = t.replace('ObjectID="%s"' % tmpl, 'ObjectID="%s"' % nti, 1)
    titxt = re.sub(r'(<Components ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nch, titxt)
    titxt = re.sub(r'(<SubClip ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nsc, titxt)
    titxt = re.sub(r'\n\t\t\t<IsMuted>[^<]*</IsMuted>', '', titxt)
    titxt = set_times2(titxt, START, END)
    Z.append_objects(doc, mtexts + [chtxt, vctxt, sctxt, titxt])
    ids = [it.attrib['ObjectID'] for it in track_items(doc, top)] + [nti]
    for a in ids[:-1]:
        s, e = item_times(doc, a)[:2]
        assert e <= START or s >= END, 'overlap on top track %.2f-%.2f' % (s / TPS, e / TPS)
    ids.sort(key=lambda x: item_times(doc, x)[0])
    set_track_items(doc, top.attrib['ObjectUID'], ids)
    open(out + '.xml', 'w', encoding='utf-8', newline='\n').write(doc.txt)
    with open(out + '.xml', 'rb') as f, gzip.open(out, 'wb') as g: g.write(f.read())
    print('stars placed', START / TPS, END / TPS, 'template', tmpl, names)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], '--probe' in sys.argv)
