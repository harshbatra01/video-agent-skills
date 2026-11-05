"""Generic .prproj dump: every sequence, every track item (time, media, in/out, speed, effects + keyframe counts,
masks, graphic text), audio items (level/gain), transitions, captions, transcripts, project media list.
usage: python prproj_dump.py project.prproj > out.txt"""
import gzip, sys, re, base64, struct, os
import xml.etree.ElementTree as ET

TPS = 254016000000
# --own-names (default on macOS, from the Mac port; opt-in on Windows, whose default output is unchanged): head each
# sequence with its OWN <Name> and add the bin item's name when the two differ. Both matter: prproj_lib.find_sequence()
# matches the sequence's own <Name>, a sequence renamed by script (seq.name = ... through the bridge) keeps its old bin
# name, and in 220 Windows project files checked on 14 Oct 2026 (mostly auto-saves) they differed for 1,524 of 2,513
# sequences (bin item "Sequence 04", sequence and master clip renamed to the hook line).
OWN_NAMES = sys.platform == 'darwin' or '--own-names' in sys.argv
path = [a for a in sys.argv[1:] if a != '--own-names'][0]
raw = gzip.open(path, 'rb').read().decode('utf-8')
root = ET.fromstring(raw)
byid, byuid = {}, {}
for e in root:
    if 'ObjectID' in e.attrib: byid[e.attrib['ObjectID']] = e
    if 'ObjectUID' in e.attrib: byuid[e.attrib['ObjectUID']] = e


def deref(e):
    if e is None: return None
    if 'ObjectRef' in e.attrib: return byid.get(e.attrib['ObjectRef'])
    if 'ObjectURef' in e.attrib: return byuid.get(e.attrib['ObjectURef'])
    return e


def sec(t): return int(t) / TPS if t else 0.0  # Premiere omits zero Start/InPoint


def strings_in_blob(b64, minlen=2):
    try: b = base64.b64decode(b64)
    except Exception: return []
    out = []
    # UTF-16LE runs
    for m in re.finditer(rb'(?:[\x20-\x7e\xa0-\xff]\x00){%d,}' % minlen, b):
        out.append(m.group(0).decode('utf-16le', 'ignore'))
    # UTF-8 runs
    for m in re.finditer(rb'[\x20-\x7e]{%d,}' % (minlen + 2), b):
        s = m.group(0).decode('latin1')
        if s not in out: out.append(s)
    return out


def blob_text(param):
    """text strings from a Source Text style blob (legacy JSON or binary)"""
    for tag in ('StartKeyframeValue', 'BinaryValue', 'Value'):
        pass
    txts = []
    for el in param.iter():
        if el.text and el.attrib.get('Encoding') == 'base64':
            txts += strings_in_blob(el.text)
    return txts


def media_of_clip(clip):
    """clip = VideoClip/AudioClip element -> (kind, name, in, out, speed)"""
    c = clip.find('Clip')
    src = deref(c.find('Source')) if c is not None else None
    inp = c.findtext('InPoint') if c is not None else None
    outp = c.findtext('OutPoint') if c is not None else None
    spd = c.findtext('PlaybackSpeed') if c is not None else None
    if src is None: return ('?', '?', inp, outp, spd)
    if src.tag == 'VideoSequenceSource' or src.tag == 'AudioSequenceSource':
        sq = byuid.get(src.find('.//Sequence').attrib.get('ObjectURef')) if src.find('.//Sequence') is not None else None
        return ('NEST', seq_names.get(sq.attrib['ObjectUID'], '?') if sq is not None else '?', inp, outp, spd)
    med = deref(src.find('.//Media'))
    if med is None: return ('?', src.tag, inp, outp, spd)
    fp = med.findtext('FilePath') or ''
    title = med.findtext('Title') or ''
    if fp.isdigit() or not fp: return ('GFX', title or fp, inp, outp, spd)
    return ('FILE', os.path.basename(fp.replace('\\', '/')), inp, outp, spd)


def comp_summary(comp_el):
    mn = comp_el.findtext('.//MatchName') or comp_el.tag
    dn = comp_el.findtext('.//DisplayName') or ''
    params = []
    texts = []
    for p in comp_el.findall('.//Params/Param'):
        pe = deref(p)
        if pe is None: continue
        nm = pe.findtext('Name') or ''
        kf = pe.findtext('Keyframes') or ''
        nk = len([k for k in kf.split(';') if k.strip()])
        sk = pe.findtext('StartKeyframe') or ''
        val = sk.split(',')[1] if sk.count(',') >= 1 else ''
        if pe.tag == 'ArbVideoComponentParam' and ('Text' in mn or 'Source Text' in nm):
            texts += blob_text(pe)
        params.append((p.attrib.get('Index'), nm, val, nk))
    masks = 0
    for sc in comp_el.findall('.//SubComponents/SubComponent'):
        se = deref(sc)
        if se is not None and 'Mask' in (se.findtext('.//MatchName') or ''): masks += 1
    return mn, dn, params, masks, texts


DEFAULTS = {'Position': {'0.5:0.5'}, 'Scale': {'100.', '100'}, 'Opacity': {'100.', '100'}, 'Rotation': {'0.', '0'},
            'Anchor Point': {'0.5:0.5'}, 'Uniform Scale': {'true'}, 'Scale Width': {'100.', '100'}, 'Anti-flicker Filter': {'0.', '0'}}


def fx_line(chain_ref):
    chain = deref(chain_ref)
    if chain is None: return [], []
    out, texts = [], []
    for c in chain.findall('.//Components/Component'):
        ce = deref(c)
        if ce is None: continue
        mn, dn, params, masks, tx = comp_summary(ce)
        texts += tx
        short = mn.replace('AE.ADBE ', '').replace('AE.', '')
        bits = []
        for idx, nm, val, nk in params:
            if nk: bits.append('%s~%dkf' % (nm or idx, nk))
            elif nm in DEFAULTS and val in DEFAULTS[nm]: continue
            elif short in ('Motion', 'Opacity') and nm and val and len(val) < 24: bits.append('%s=%s' % (nm, val))
        if short in ('Motion', 'Opacity') and not bits and not masks: continue
        if short in ('Text', 'Shape', 'Capsule', 'Vector Motion'): bits = [b for b in bits if '~' in b]
        out.append('%s%s%s' % (dn or short, ('[' + ', '.join(bits[:8]) + ']') if bits else '', (' masks=%d' % masks) if masks else ''))
    return out, texts


# sequence names
seq_names = {}
for cpi in root.iter('ClipProjectItem'):
    name = cpi.findtext('.//ProjectItem/Name')
    mc = deref(cpi.find('MasterClip'))
    if mc is None: continue
    for c in mc.findall('.//Clips/Clip'):
        ce = deref(c)
        src = deref(ce.find('.//Source')) if ce is not None else None
        if src is not None and src.tag == 'VideoSequenceSource':
            sq = src.find('.//Sequence')
            if sq is not None: seq_names[sq.attrib['ObjectURef']] = name
            break

print('PROJECT', path)
print('sequences:', len(seq_names))
for uid, name in seq_names.items():
    seq = byuid.get(uid)
    if seq is None: continue
    binnote = ''
    if OWN_NAMES:
        own = seq.findtext('Name')
        if own and own != name: name, binnote = own, '  [bin item "%s"]' % name
    print('\n' + '=' * 100)
    groups = []
    for tg in seq.find('TrackGroups'):
        g = deref(tg.find('Second'))
        if g is not None: groups.append(g)
    fr = None; rect = None
    for g in groups:
        if g.tag == 'VideoTrackGroup':
            fr = g.findtext('.//FrameRate'); rect = g.findtext('.//FrameRect')
    fps = TPS / int(fr) if fr else 0
    print('SEQUENCE "%s"  %s  %.3f fps%s' % (name, rect, fps, binnote))
    for g in groups:
        kind = g.tag
        tracks = [byuid.get(t.attrib['ObjectURef']) for t in g.findall('.//Tracks/Track')]
        for ti_, tr in enumerate(tracks):
            if tr is None: continue
            items = tr.find('.//ClipItems/TrackItems')
            items = [deref(i) for i in items] if items is not None else []
            trans = tr.find('.//TransitionItems/TrackItems')
            trans = [deref(i) for i in trans] if trans is not None else []
            label = {'VideoTrackGroup': 'V', 'AudioTrackGroup': 'A', 'DataTrackGroup': 'C'}.get(kind, kind) + str(ti_ + 1)
            muted = tr.findtext('.//IsMuted')
            if not items and not trans: continue
            print('-- %s  %d items%s%s' % (label, len(items), '  %d transitions' % len(trans) if trans else '', '  TRACK MUTED' if muted == 'true' else ''))
            for it in items:
                if it is None: continue
                st = it.findtext('.//TrackItem/Start'); en = it.findtext('.//TrackItem/End')
                dis = ' DISABLED' if it.findtext('.//IsMuted') == 'true' else ''
                sub = deref(it.find('.//SubClip'))
                if it.tag.startswith('CaptionData'):
                    tx = []
                    for el in it.iter():
                        pass
                    print('   %7.2f-%7.2f caption%s' % (sec(st), sec(en), dis)); continue
                media = ('?', '?', None, None, None)
                if sub is not None:
                    clip = deref(sub.find('Clip'))
                    if clip is not None: media = media_of_clip(clip)
                fx, texts = fx_line(it.find('.//ComponentOwner/Components'))
                kindm, mname, inp, outp, spd = media
                io = ''
                if outp:
                    io = ' src %.2f-%.2f' % (sec(inp), sec(outp))
                sp = ' speed %s' % spd if spd and spd not in ('1', '1.') else ''
                gain = ''
                if it.tag == 'AudioClipTrackItem' and sub is not None:
                    clip = deref(sub.find('Clip'))
                    g_ = clip.findtext('.//Gain') if clip is not None else None
                    if g_: gain = ' gain %.1fdB' % (20 * __import__('math').log10(float(g_))) if float(g_) > 0 else ''
                print('   %7.2f-%7.2f %-4s %-44s%s%s%s%s' % (sec(st), sec(en), kindm, mname[:44], io, sp, gain, dis))
                if fx: print('        fx: ' + ' | '.join(fx))
                if texts:
                    t2 = [t for t in texts if len(t.strip()) > 1 and not re.match(r'^[\W\d_]+$', t)]
                    if t2: print('        text: ' + ' / '.join(t2[:12])[:400])
            for tt in trans:
                if tt is None: continue
                st = tt.findtext('.//TrackItem/Start'); en = tt.findtext('.//TrackItem/End')
                fx, _ = fx_line(tt.find('.//ComponentOwner/Components'))
                mn = tt.findtext('.//MatchName') or ''
                print('   %7.2f-%7.2f TRANSITION %s %s' % (sec(st), sec(en), mn, ' '.join(fx)))

# transcripts
print('\nTRANSCRIPTS:', len(re.findall(r'<TranscriptData', raw)))
print('CAPTION blocks:', len(re.findall(r'<FormattedTextData', raw)))
# all media files in project
print('\nMEDIA FILES:')
seen = set()
for med in root.iter('Media'):
    fp = med.findtext('FilePath') or ''
    if fp and not fp.isdigit() and fp not in seen:
        seen.add(fp); print('  ', fp)
