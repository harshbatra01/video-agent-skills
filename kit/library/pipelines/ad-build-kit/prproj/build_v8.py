"""v8 = the user's saved v7 (+ "Ad edits" music bin, 3 new kit files) with the sound pass rolled out to all 8 ads:
- music: one baked edit per ad on A2 (3 things: the old 'Bring Them Home' clips are replaced),
- SFX on A3/A4 for the 7 other ads (cue sheets from scratchpad audio/cues_all.json; 3 things keeps its approved SFX),
- dialogue clip gain evened out (I'm 52 -1.8, held the record +8.1, 3 questions +1.9, secret weapon +2.5 dB),
- 1 star reviews gets a 4th audio track; the 3 new kit files are moved into the SFX kit bin."""
import sys, re, json, gzip, uuid, os, math
sys.path.insert(0, '.')
from build_project import Doc, TPS, for_claude_sequences
from audio_dump import audio_tracks
from build_v7 import ticks, gain_xml, track_item_ids, Builder

SRC = 'v8imp.xml'
OUT_XML = 'out/v8.prproj.xml'
OUT = r"C:\VISION\IMMUFIX\ads immufix - Claude zooms + titles v8.prproj"
AUD = os.path.join('..', 'audio')


def clip_index(doc):
    """file name -> (MasterClip uid, master's first Clip id, ClipProjectItem uid) for every audio file item"""
    out = {}
    for e in doc.root:
        if e.tag != 'ClipProjectItem': continue
        nm = e.findtext('.//ProjectItem/Name') or ''
        if not nm.lower().endswith('.wav'): continue
        mc_uid = e.find('MasterClip').attrib['ObjectURef']
        clip = re.search(r'<Clip Index="0" ObjectRef="(\d+)"', doc.raw(mc_uid, uid=True)).group(1)
        out[nm] = (mc_uid, clip, e.attrib['ObjectUID'])
    return out


def container_items(raw):
    m = re.search(r'(<ProjectItemContainer Version="\d+">\s*<Items Version="1">)(.*?)(</Items>)', raw, re.S)
    return m


def move_to_bin(doc, cpi_uids, bin_name):
    root = [e for e in doc.root if e.tag == 'RootProjectItem'][0]
    rkey = root.attrib.get('ObjectUID') or root.attrib.get('ObjectID'); ruid = 'ObjectUID' in root.attrib
    rraw = doc.raw(rkey, uid=ruid); m = container_items(rraw)
    items = re.findall(r'<Item Index="\d+" (ObjectU?Ref="[^"]+")/>', m.group(2))
    keep = [i for i in items if not any(u in i for u in cpi_uids)]
    moved = [i for i in items if any(u in i for u in cpi_uids)]
    assert len(moved) == len(cpi_uids), (len(moved), cpi_uids)
    body = ''.join('\n\t\t\t\t\t<Item Index="%d" %s/>' % (k, i) for k, i in enumerate(keep)) + '\n\t\t\t\t'
    doc.replace_obj(rkey, rraw[:m.start(2)] + body + rraw[m.end(2):], uid=ruid)
    b = [e for e in doc.root if e.tag == 'BinProjectItem' and e.findtext('.//ProjectItem/Name') == bin_name][0]
    braw = doc.raw(b.attrib['ObjectUID'], uid=True); m = container_items(braw)
    old = re.findall(r'<Item Index="\d+" (ObjectU?Ref="[^"]+")/>', m.group(2))
    body = ''.join('\n\t\t\t\t\t<Item Index="%d" %s/>' % (k, i) for k, i in enumerate(old + moved)) + '\n\t\t\t\t'
    doc.replace_obj(b.attrib['ObjectUID'], braw[:m.start(2)] + body + braw[m.end(2):], uid=True)


def delete_obj(doc, oid):
    s, e = doc.span(oid)
    # also swallow the newline that precedes the object
    doc.txt = doc.txt[:s - 1] + doc.txt[e:] if doc.txt[s - 1] == '\n' else doc.txt[:s] + doc.txt[e:]


def remove_audio_items(doc, tr_uid):
    """remove every clip item on an audio track (items we placed ourselves): item, chain, subclip, clip instance, secondary contents"""
    ids = track_item_ids(doc, tr_uid)
    for tid in ids:
        t = doc.raw(tid)
        chain = re.search(r'<Components ObjectRef="(\d+)"', t).group(1)
        sub = re.search(r'<SubClip ObjectRef="(\d+)"', t).group(1)
        clip = re.search(r'<Clip ObjectRef="(\d+)"', doc.raw(sub)).group(1)
        secs = re.findall(r'<SecondaryContentItem Index="\d+" ObjectRef="(\d+)"/>', doc.raw(clip))
        assert not re.search(r'<Component Index', doc.raw(chain)), 'chain has components, not ours'
        for o in [tid, chain, sub, clip] + secs: delete_obj(doc, o)
    raw = doc.raw(tr_uid, uid=True)
    raw2 = re.sub(r'(<ClipItems Version="\d+">)\s*<TrackItems Version="1">.*?</TrackItems>\s*', r'\1\n\t\t\t\t', raw, count=1, flags=re.S)
    doc.replace_obj(tr_uid, raw2, uid=True)
    return len(ids)


def put_track_items(doc, tr_uid, ids):
    raw = doc.raw(tr_uid, uid=True)
    assert not re.search(r'<ClipItems Version="\d+">\s*<TrackItems', raw), 'track not empty'
    lst = '<TrackItems Version="1">\n' + ''.join('\t\t\t\t\t<TrackItem Index="%d" ObjectRef="%s"/>\n' % (i, x) for i, x in enumerate(ids)) + '\t\t\t\t</TrackItems>\n\t\t\t\t'
    new = re.sub(r'(<ClipItems Version="\d+">\s*)(<MediaType>)', lambda m: m.group(1) + lst + m.group(2), raw, count=1)
    assert new != raw
    doc.replace_obj(tr_uid, new, uid=True)


def deep_clone(doc, oid, b, idmap):
    """clone an object and everything it references by ObjectRef (track-owned objects); returns the new id"""
    if oid in idmap: return idmap[oid]
    new = b.nid(); idmap[oid] = new
    t = doc.raw(oid)
    for r in set(re.findall(r'ObjectRef="(\d+)"', t)): deep_clone(doc, r, b, idmap)
    t = re.sub(r'(<\w+ ObjectID=")\d+(")', r'\g<1>%s\2' % new, t, count=1)
    t = re.sub(r'ObjectRef="(\d+)"', lambda m: 'ObjectRef="%s"' % idmap[m.group(1)], t)
    b.add(t)
    return new


def add_audio_track(doc, seq, b):
    g, trs = audio_tracks(doc, seq)                                      # parsed tree = the original tracks
    gid = g.attrib['ObjectID']; graw = doc.raw(gid)                     # live text = includes tracks added already
    live = re.findall(r'<Track Index="\d+" ObjectURef="([^"]+)"/>', graw)
    last = trs[-1].attrib['ObjectUID']; raw = doc.raw(last, uid=True)   # template: an original (empty) track
    next_id = int(re.search(r'<NextTrackID>(\d+)</NextTrackID>', graw).group(1))
    idx = len(live)
    idmap = {}
    comp = re.search(r'<Components ObjectRef="(\d+)"', raw).group(1); pan = re.search(r'<Panner ObjectRef="(\d+)"', raw).group(1)
    nc = deep_clone(doc, comp, b, idmap); npn = deep_clone(doc, pan, b, idmap)
    nu = str(uuid.uuid4())
    t = raw.replace(last, nu, 1)
    t = re.sub(r'<Index>\d+</Index>', '<Index>%d</Index>' % idx, t)
    t = re.sub(r'(</MediaType>\s*<Index>\d+</Index>\s*<ID>)\d+(</ID>)', r'\g<1>%d\2' % next_id, t, count=1)
    t = re.sub(r'<Components ObjectRef="\d+"/>', '<Components ObjectRef="%s"/>' % nc, t, count=1)
    t = re.sub(r'<Panner ObjectRef="\d+"/>', '<Panner ObjectRef="%s"/>' % npn, t, count=1)
    t = re.sub(r'(<Panner ObjectRef="\d+"/>\s*<ID>)[^<]*(</ID>)', r'\g<1>%s\g<2>' % uuid.uuid4(), t, count=1)
    assert re.search(r'<ClipItems Version="\d+">\s*<MediaType>', t), 'cloned track must be empty'
    doc.txt = doc.txt.replace('</PremiereData>', t + '\n</PremiereData>')   # in the text now: items get added to it later
    graw2 = graw.replace('</Tracks>', '\t<Track Index="%d" ObjectURef="%s"/>\n\t\t\t</Tracks>' % (idx, nu), 1)
    graw2 = re.sub(r'<NextTrackID>\d+</NextTrackID>', '<NextTrackID>%d</NextTrackID>' % (next_id + 1), graw2, count=1)
    doc.replace_obj(gid, graw2)
    sraw = doc.raw(seq.attrib['ObjectUID'], uid=True)
    m = re.search(r'(<HSL\.TimelinePatchingAndTargeting\.AudioPatches[^>]*>)(\[.*?\])(</)', sraw)
    patches = json.loads(m.group(2)); patches.append({"mNumber": -1, "mState": 0})
    sraw = sraw[:m.start(2)] + json.dumps(patches, separators=(',', ':')) + sraw[m.end(2):]
    doc.replace_obj(seq.attrib['ObjectUID'], sraw, uid=True)
    return nu


def scale_dialog_gain(doc, a1_ids, db):
    seen = set(); f = 10 ** (db / 20)
    for tid in a1_ids:
        sub = re.search(r'<SubClip ObjectRef="(\d+)"', doc.raw(tid)).group(1)
        cid = re.search(r'<Clip ObjectRef="(\d+)"', doc.raw(sub)).group(1)
        assert cid not in seen; seen.add(cid)
        ct = doc.raw(cid); g = re.search(r'<Gain>([^<]*)</Gain>', ct)
        if g: ct2 = ct.replace(g.group(0), '<Gain>%r</Gain>' % (float(g.group(1)) * f), 1)
        else: ct2 = ct.replace('</AudioChannelLayout>\n\t</AudioClip>', '</AudioChannelLayout>\n\t\t<Gain>%r</Gain>\n\t</AudioClip>' % f)
        assert ct2 != ct
        doc.replace_obj(cid, ct2)
    return len(seen)


def main():
    cues = json.load(open(os.path.join(AUD, 'cues_all.json')))
    medits = {(m['key'], m['tag']): m for m in json.load(open(os.path.join(AUD, 'music_edits.json')))}
    doc = Doc(SRC)
    idx = clip_index(doc)
    # tidy: the 3 new kit files were imported at the root -> SFX kit bin
    root_new = [idx[n][2] for n in ('IMX_MARK1.wav', 'IMX_MARK2.wav', 'IMX_CROWD1.wav')]
    try: move_to_bin(doc, root_new, 'SFX kit')
    except AssertionError as e: print('kit files not at root, left where they are', e)
    b = Builder(doc)
    seqs = {s.attrib['ObjectUID'][:8]: s for n, s in for_claude_sequences(doc)}
    tmpl_item = track_item_ids(doc, audio_tracks(doc, seqs['f233433f'])[1][0].attrib['ObjectUID'])[0]
    tmpl_chain = re.search(r'<Components ObjectRef="(\d+)"', doc.raw(tmpl_item)).group(1)
    report = []
    for key, seq in seqs.items():
        g, trs = audio_tracks(doc, seq)
        uids = [t.attrib['ObjectUID'] for t in trs]
        a1 = track_item_ids(doc, uids[0])
        if key == 'f233433f':
            n_old = remove_audio_items(doc, uids[1])
            mfile = medits[(key, 'A')]['file']; L = 48.25
            mc, mclip, _ = idx[mfile]
            cid = b.clip_instance(mclip, 0.0, L, 0.0)
            put_track_items(doc, uids[1], [b.track_item(tmpl_item, tmpl_chain, mc, mfile, cid, 0.0, L)])
            report.append('tt: replaced %d old music clips with %s' % (n_old, mfile)); continue
        c = cues[key]; L = c['L']
        if c['dialog_gain_change_db']:
            n = scale_dialog_gain(doc, a1, c['dialog_gain_change_db'])
        need = 2 + max(e['lane'] for e in c['events']) + 1
        added = 0
        while len(uids) < need:
            uids.append(add_audio_track(doc, seq, b)); added += 1
        for u in uids[1:need]: assert not track_item_ids(doc, u), (key, 'audio track not empty')
        mfile = c['music']; mc, mclip, _ = idx[mfile]
        cid = b.clip_instance(mclip, 0.0, L, 0.0)
        put_track_items(doc, uids[1], [b.track_item(tmpl_item, tmpl_chain, mc, mfile, cid, 0.0, L)])
        lanes = {}
        for e in sorted(c['events'], key=lambda e: e['start']):
            mc, mclip, _ = idx[e['file']]
            length = e['end'] - e['start']
            cid = b.clip_instance(mclip, e['skip'], e['skip'] + length, e['gain_db'])
            lanes.setdefault(e['lane'], []).append(b.track_item(tmpl_item, tmpl_chain, mc, e['file'], cid, e['start'], e['start'] + length))
        for k, ids in lanes.items(): put_track_items(doc, uids[2 + k], ids)
        report.append('%s: music %s, SFX per lane %s, dialogue %+.1f dB, tracks added %d' % (c['short'], mfile, {('A%d' % (3 + k)): len(v) for k, v in sorted(lanes.items())}, c['dialog_gain_change_db'], added))
    txt = doc.txt.replace('</PremiereData>', ''.join(x if x.endswith('\n') else x + '\n' for x in b.new) + '</PremiereData>')
    open(OUT_XML, 'w', encoding='utf-8').write(txt)
    with gzip.open(OUT, 'wb') as f: f.write(txt.encode('utf-8'))
    print('\n'.join(report)); print('new objects', len(b.new), '->', OUT)


if __name__ == '__main__':
    main()
