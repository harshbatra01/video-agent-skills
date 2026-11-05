"""v7 = saved v6 (with the "SFX kit" + "Music" bins imported in Premiere) + 3 things sound pass:
music edit on A2, SFX on A3/A4 (peak-aligned, per-clip Audio Gain), +8 dB Audio Gain on the A1 dialogue clips.
Everything is driven by scratchpad audio/cues_tt.json (built by audio/cues_tt.py)."""
import sys, re, json, gzip, uuid, os
sys.path.insert(0, '.')
from build_project import Doc, TPS, for_claude_sequences
from audio_dump import audio_tracks

SRC = 'v7imp.xml'
OUT_XML = 'out/v7.prproj.xml'
OUT = r"C:\VISION\IMMUFIX\ads immufix - Claude zooms + titles v7.prproj"
CUES = os.path.join('..', 'audio', 'cues_tt.json')
SEQ_KEY = 'f233433f'
SAMPLE = TPS // 48000            # 5292000 ticks per 48 kHz sample


def ticks(sec):
    return int(round(sec * TPS / SAMPLE)) * SAMPLE


def gain_xml(db):
    return '<Gain>%r</Gain>' % (10 ** (db / 20.0))


def master_index(doc):
    """file name -> (MasterClip uid, master AudioClip id) for clips in the SFX kit / Music bins"""
    out = {}
    for b in doc.root:
        if b.tag != 'BinProjectItem' or b.findtext('.//ProjectItem/Name') not in ('SFX kit', 'Music'): continue
        for it in b.find('.//ProjectItemContainer/Items'):
            cpi = doc.deref(it)
            mc_uid = cpi.find('MasterClip').attrib['ObjectURef']
            mc = doc.raw(mc_uid, uid=True)
            clip_id = re.search(r'<Clip Index="0" ObjectRef="(\d+)"', mc).group(1)
            out[cpi.findtext('.//ProjectItem/Name')] = (mc_uid, clip_id)
    return out


def track_item_ids(doc, tr_uid):
    raw = doc.raw(tr_uid, uid=True)
    m = re.search(r'<ClipItems Version="\d+">\s*<TrackItems Version="1">(.*?)</TrackItems>', raw, re.S)
    return re.findall(r'ObjectRef="(\d+)"', m.group(1)) if m else []


class Builder:
    def __init__(self, doc):
        self.doc = doc; self.new = []; self.node_id = 2000000

    def nid(self): return self.doc.new_id()

    def add(self, txt): self.new.append(txt)

    def clip_instance(self, master_clip_id, in_s, out_s, gain_db):
        m = self.doc.raw(master_clip_id)
        new_id = self.nid()
        t = re.sub(r'(<AudioClip ObjectID=")\d+(")', r'\g<1>%s\2' % new_id, m, count=1)
        t = t.replace('<InUse>false</InUse>', '').replace('<InUse>true</InUse>', '')
        t = re.sub(r'<ClipID>[^<]*</ClipID>', '<OutPoint>%d</OutPoint>\n\t\t\t<InPoint>%d</InPoint>\n\t\t\t<ClipID>%s</ClipID>' % (ticks(out_s), ticks(in_s), uuid.uuid4()), t, count=1)
        # fresh SecondaryContent objects (same media source, same channel index)
        def sc(mo):
            old = self.doc.raw(mo.group(2)); sid = self.nid()
            self.add(re.sub(r'(<SecondaryContent ObjectID=")\d+(")', r'\g<1>%s\2' % sid, old, count=1))
            return '%sObjectRef="%s"/>' % (mo.group(1), sid)
        t = re.sub(r'(<SecondaryContentItem Index="\d+" )ObjectRef="(\d+)"/>', sc, t)
        t = t.replace('</AudioChannelLayout>\n\t</AudioClip>', '</AudioChannelLayout>\n\t\t%s\n\t</AudioClip>' % gain_xml(gain_db))
        assert '<Gain>' in t, 'gain not inserted'
        self.add(t)
        return new_id

    def track_item(self, tmpl_item, tmpl_chain, mc_uid, name, clip_id, start_s, end_s):
        chain_id = self.nid()
        self.add(re.sub(r'(<AudioComponentChain ObjectID=")\d+(")', r'\g<1>%s\2' % chain_id, self.doc.raw(tmpl_chain), count=1))
        sub_id = self.nid()
        self.add('\t<SubClip ObjectID="%s" ClassID="e0c58dc9-dbdd-4166-aef7-5db7e3f22e84" Version="6">\n\t\t<Clip ObjectRef="%s"/>\n'
                 '\t\t<MasterClip ObjectURef="%s"/>\n\t\t<Name>%s</Name>\n\t\t<OrigChGrp>0</OrigChGrp>\n\t</SubClip>\n' % (sub_id, clip_id, mc_uid, name))
        item_id = self.nid(); self.node_id += 1
        t = self.doc.raw(tmpl_item)
        t = re.sub(r'(<AudioClipTrackItem ObjectID=")\d+(")', r'\g<1>%s\2' % item_id, t, count=1)
        t = re.sub(r'<Components ObjectRef="\d+"/>', '<Components ObjectRef="%s"/>' % chain_id, t, count=1)
        t = re.sub(r'<SubClip ObjectRef="\d+"/>', '<SubClip ObjectRef="%s"/>' % sub_id, t, count=1)
        t = re.sub(r'<Properties Version="1">.*?</Properties>', '<Properties Version="1">\n\t\t\t\t\t</Properties>', t, count=1, flags=re.S)
        t = re.sub(r'(<Node Version="1">\s*<Properties Version="1">\s*</Properties>\s*<ID>)\d+(</ID>)', r'\g<1>%d\2' % self.node_id, t, count=1)
        t = re.sub(r'\s*<Start>-?\d+</Start>', '', t)
        t = re.sub(r'<End>-?\d+</End>', '<Start>%d</Start>\n\t\t\t\t<End>%d</End>' % (ticks(start_s), ticks(end_s)), t, count=1)
        t = re.sub(r'(</ClipTrackItem>\s*<ID>)[^<]*(</ID>)', r'\g<1>%s\2' % uuid.uuid4(), t, count=1)
        self.add(t)
        return item_id


def set_track_items(doc, tr_uid, ids):
    raw = doc.raw(tr_uid, uid=True)
    assert not re.search(r'<ClipItems Version="\d+">\s*<TrackItems', raw), 'track not empty'
    lst = '<TrackItems Version="1">\n' + ''.join('\t\t\t\t<TrackItem Index="%d" ObjectRef="%s"/>\n' % (i, x) for i, x in enumerate(ids)) + '\t\t\t\t</TrackItems>\n\t\t\t\t'
    new = re.sub(r'(<ClipItems Version="\d+">\s*)(<MediaType>)', lambda m: m.group(1) + lst + m.group(2), raw, count=1)
    assert new != raw
    doc.replace_obj(tr_uid, new, uid=True)


def main():
    cues = json.load(open(CUES))
    doc = Doc(SRC)
    seq = [s for n, s in for_claude_sequences(doc) if s.attrib['ObjectUID'].startswith(SEQ_KEY)][0]
    g, trs = audio_tracks(doc, seq)
    uids = [t.attrib['ObjectUID'] for t in trs]
    a1 = track_item_ids(doc, uids[0])
    assert len(a1) == 31, len(a1)
    tmpl_item = a1[0]
    tmpl_chain = re.search(r'<Components ObjectRef="(\d+)"', doc.raw(tmpl_item)).group(1)
    masters = master_index(doc)
    b = Builder(doc)
    # dialogue gain on the 31 A1 clips (each item has its own AudioClip instance)
    seen = set()
    for tid in a1:
        sub = re.search(r'<SubClip ObjectRef="(\d+)"', doc.raw(tid)).group(1)
        cid = re.search(r'<Clip ObjectRef="(\d+)"', doc.raw(sub)).group(1)
        assert cid not in seen; seen.add(cid)
        ct = doc.raw(cid)
        assert '<Gain>' not in ct
        doc.replace_obj(cid, ct.replace('</AudioChannelLayout>\n\t</AudioClip>', '</AudioChannelLayout>\n\t\t%s\n\t</AudioClip>' % gain_xml(cues['dialog_gain_db'])))
        assert '<Gain>' in doc.raw(cid)
    # music on A2
    mfile = os.path.basename(cues['music_file'])
    mc_uid, mclip = masters[mfile]
    music_ids = []
    for m in cues['music']:
        dur = m['end'] - m['start']
        cid = b.clip_instance(mclip, m['src_in'], m['src_in'] + dur, m['gain_db'])
        music_ids.append(b.track_item(tmpl_item, tmpl_chain, mc_uid, mfile, cid, m['start'], m['end']))
    # SFX on A3 / A4
    lanes = {'A3': [], 'A4': []}
    for ev in sorted(cues['events'], key=lambda e: e['start']):
        mc_uid, mclip = masters[ev['file']]
        start = max(0.0, ev['start']); skip = start - ev['start']
        end = min(ev['start'] + ev['dur'], 48.25)
        cid = b.clip_instance(mclip, skip, skip + (end - start), ev['gain_db'])
        lanes[ev['track']].append(b.track_item(tmpl_item, tmpl_chain, mc_uid, ev['file'], cid, start, end))
    set_track_items(doc, uids[1], music_ids)
    set_track_items(doc, uids[2], lanes['A3'])
    set_track_items(doc, uids[3], lanes['A4'])
    txt = doc.txt.replace('</PremiereData>', ''.join(x if x.endswith('\n') else x + '\n' for x in b.new) + '</PremiereData>')
    open(OUT_XML, 'w', encoding='utf-8').write(txt)
    with gzip.open(OUT, 'wb') as f: f.write(txt.encode('utf-8'))
    print('music clips', len(music_ids), 'A3', len(lanes['A3']), 'A4', len(lanes['A4']), 'new objects', len(b.new), '->', OUT)


if __name__ == '__main__':
    main()
