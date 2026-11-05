"""v9 = the user's saved v8 (their own music / SFX edits, re-cleaned C105 + C108 audio, imported gfx_v4 renders,
CTA voice, Paradigm Shift ending) + review fixes:
  1. colour: the Sony log override restored on the two re-cleaned sources (C105 / C108 "VERSION 2"),
  2. title credential tags 20 % bigger (gold pill + text, centred, animation kept),
  3. hr_window ("vulnerable for 20 minutes") swapped for the gfx_v4 render that sits in the caption zone,
  4. a reusable 5 s CTA end segment appended to the ads without a code card (held the record, 3 things):
     3 product B-roll shots, the cta_end card, the CTA voice, SFX, and the user's music run into its final chord."""
import sys, re, json, gzip, uuid, os, math
sys.path.insert(0, '.')
from build_project import Doc, TPS, fmt, for_claude_sequences, video_tracks, set_override
from build_broll import strip_inline, clone_component, chain_components, clone_chain, set_inout
from build_ext import set_times2
from build_v4 import overlay_item
from build_v6 import live, motion_template
from audio_dump import audio_tracks
from build_v7 import ticks as aticks, Builder, track_item_ids
from title_dump import titles

SRC = 'v9imp.xml'
OUT_XML = 'out/v9.prproj.xml'
OUT = r"C:\VISION\IMMUFIX\ads immufix - Claude zooms + titles v9.prproj"
AUD = os.path.join('..', 'audio')
PROFILE = '{"baseColorProfile":{"colorProfileData":"AQAAAP////8=","colorProfileName":"1012,1001,1,Narrow,YCC,8-bit,Scene-Referred"},"baseProfileType":1}'
F60 = TPS // 60
TAG_SCALE = 1.20
CAP_H = 20.4                     # cap height (px) of the 30 px ProximaNova Extrabold credential
CTA_ADS = {'404c5cb2': dict(broll_track=2, gfx_track=5), 'f233433f': dict(broll_track=4, gfx_track=8)}
CTA_LEN = 5.0
CTA_SHOTS = [  # (media name part, template in-point (s) to pick the graded/framed template item, new in-point (s), length (s))
    ('C132', 12.72, 72.00, 1.70),   # pouch on the post (static part, calm behind the kicker)
    ('C141', 4.00, 4.00, 1.60),     # scoop macro
    ('C121', 8.00, 8.00, 1.70),     # Paula holding the pouch
]
VO_GAIN_DB = -3.0                # CTA voice (-14.6 LUFS) to the ads' dialogue level
BAR = 240 / 138.0                # Paradigm Shift
END_FILE = 'IMX_MUSIC_ParadigmShift_CTA_ending.wav'
END_PRE = 0.010                  # the ending file starts 10 ms before its downbeat
VOICE = -17.5
CTA_SFX = [  # (time after the CTA start, kit sound, rel LU, at_start)
    (0.02, 'WHOOSH2', -13, False), (0.12, 'TICK2', -16, False), (1.55, 'TICK1', -16, False),
    (2.62, 'SWISH1', -12, False), (2.85, 'LOCK2', -11, False), (3.12, 'COUNT_09', -16, True), (3.82, 'POP2', -10, False)]


def tk(sec): return int(round(sec * 60)) * F60


def secs(t): return t / TPS


# ------------------------------------------------------------------ generic param edits
def edit_param(doc, pid, fn):
    """fn(value_string) -> value_string, applied to the StartKeyframe value and every keyframe value"""
    p = doc.raw(pid)
    def sk(m): return m.group(1) + fn(m.group(2)) + m.group(3)
    p2 = re.sub(r'(<StartKeyframe>-?\d+,)([^,]*)(,)', sk, p, count=1)
    def kfs(m):
        keys = [k for k in m.group(1).split(';') if k]
        out = []
        for k in keys:
            f = k.split(','); f[1] = fn(f[1]); out.append(','.join(f))
        return '<Keyframes>' + ';'.join(out) + ';</Keyframes>'
    p2 = re.sub(r'<Keyframes>([^<]*)</Keyframes>', kfs, p2)
    doc.replace_obj(pid, p2)


def scale_val(f):
    return lambda v: fmt(float(v) * f)


def shift_y(dy):
    def g(v):
        x, y = v.split(':'); return '%s:%r' % (x, float(y) + dy)
    return g


def shift_xy(dx, dy):
    def g(v):
        x, y = v.split(':'); return '%r:%r' % (float(x) + dx, float(y) + dy)
    return g


# ------------------------------------------------------------------ 2. title tags
def bigger_tags(doc, log):
    _, ts = titles_live(doc)
    for key, (tid, comps) in ts.items():
        texts = [c for c in comps if c[2] == 'AE.ADBE Text']; shapes = [c for c in comps if c[2] == 'AE.ADBE Shape']
        assert len(texts) == 2 and len(shapes) == 1, (key, len(texts), len(shapes))
        ypos = lambda c: float(c[3][2][2].split(':')[1])
        cred = max(texts, key=ypos); pill = shapes[0]
        cid, _, _, ps = cred
        pid_, _, _, pps = pill
        # a title near the left edge (3 things) grows to the right so its left margin stays put
        cx = float(pps[3][2].split(':')[0]); half = float(pps[9][2].split(':')[0])
        dx = (TAG_SCALE - 1) * half if cx - TAG_SCALE * half < 0.02 else 0.0
        edit_param(doc, ps[3][0], lambda v: fmt(TAG_SCALE * 100.0))          # Scale 100 -> 120
        edit_param(doc, ps[2][0], shift_xy(dx, (TAG_SCALE - 1) * CAP_H / 2 / 1920.0))
        edit_param(doc, pps[4][0], lambda v: fmt(TAG_SCALE * 100.0))          # height scale
        edit_param(doc, pps[5][0], scale_val(TAG_SCALE))                      # width scale keys (open / close)
        if dx: edit_param(doc, pps[3][0], shift_xy(dx, 0.0))
        log('  %s: credential tag x%.2f%s' % (key, TAG_SCALE, ' (shifted right %.1f px)' % (dx * 1080) if dx else ''))


def titles_live(doc):
    """title_dump.titles works on a file; re-run its logic on this doc"""
    import title_dump as T
    out = {}
    for n, seq in for_claude_sequences(doc):
        key = seq.attrib['ObjectUID'][:8]
        for tr in video_tracks(doc, seq):
            for tid in live(doc, tr):
                t = doc.raw(tid); sub = re.search(r'<SubClip ObjectRef="(\d+)"', t)
                if not sub: continue
                nm = re.search(r'<Name>([^<]*)</Name>', doc.raw(sub.group(1)))
                if not nm or not nm.group(1).startswith('Title'): continue
                ch = re.search(r'<Components ObjectRef="(\d+)"', t).group(1)
                comps = re.findall(r'<Component Index="\d+" ObjectRef="(\d+)"', doc.raw(ch))
                out[key] = (tid, [(c,) + T.comp_params(doc, c) for c in comps])
    return doc, out


# ------------------------------------------------------------------ media helpers
def masters_by_path(doc, needle):
    """[(ClipProjectItem name, MasterClip uid, first clip id, media path)] whose media path contains needle"""
    out = []
    for e in doc.root:
        if e.tag != 'ClipProjectItem' or e.find('MasterClip') is None: continue
        mc = e.find('MasterClip').attrib['ObjectURef']
        try: mraw = doc.raw(mc, uid=True)
        except KeyError: continue
        cl = re.search(r'<Clip Index="0" ObjectRef="(\d+)"', mraw)
        if not cl: continue
        src = re.search(r'<Source ObjectRef="(\d+)"', doc.raw(cl.group(1)))
        if not src: continue
        med = re.search(r'<Media ObjectURef="([^"]+)"', doc.raw(src.group(1)))
        if not med: continue
        fp = re.search(r'<FilePath>([^<]*)</FilePath>', doc.raw(med.group(1), uid=True)).group(1)
        if needle in fp: out.append((e.findtext('.//ProjectItem/Name'), mc, cl.group(1), fp))
    return out


def media_streams(doc, needle):
    out = []
    for e in doc.root:
        if e.tag != 'Media': continue
        fp = e.findtext('FilePath') or ''
        vs = e.find('VideoStream')
        if needle in fp and vs is not None: out.append((fp, vs.attrib['ObjectRef']))
    return out


def put_after(doc, tr_uid, new_ids):
    """append clip items to a track (keeps existing items, re-indexes)"""
    raw = doc.raw(tr_uid, uid=True)
    m = re.search(r'(<ClipItems Version="\d+">\s*<TrackItems Version="1">)(.*?)(</TrackItems>)', raw, re.S)
    if m:
        old = re.findall(r'<TrackItem Index="\d+" ObjectRef="(\d+)"/>', m.group(2))
        body = ''.join('\n\t\t\t\t\t<TrackItem Index="%d" ObjectRef="%s"/>' % (i, x) for i, x in enumerate(old + list(new_ids))) + '\n\t\t\t\t'
        raw2 = raw[:m.start(2)] + body + raw[m.end(2):]
    else:
        lst = '<TrackItems Version="1">\n' + ''.join('\t\t\t\t\t<TrackItem Index="%d" ObjectRef="%s"/>\n' % (i, x) for i, x in enumerate(new_ids)) + '\t\t\t\t</TrackItems>\n\t\t\t\t'
        raw2 = re.sub(r'(<ClipItems Version="\d+">\s*)(<MediaType>)', lambda mm: mm.group(1) + lst + mm.group(2), raw, count=1)
    assert raw2 != raw
    doc.replace_obj(tr_uid, raw2, uid=True)


def item_bounds(doc, tid):
    t = doc.raw(tid)
    s = int(re.search(r'<Start>(\d+)</Start>', t).group(1)) if '<Start>' in t else 0
    e = int(re.search(r'<End>(\d+)</End>', t).group(1))
    return s, e


def clip_of(doc, tid):
    sub = re.search(r'<SubClip ObjectRef="(\d+)"', doc.raw(tid)).group(1)
    return sub, re.search(r'<Clip ObjectRef="(\d+)"', doc.raw(sub)).group(1)


def media_fps_ticks(doc, clip_id):
    src = re.search(r'<Source ObjectRef="(\d+)"', doc.raw(clip_id)).group(1)
    med = re.search(r'<Media ObjectURef="([^"]+)"', doc.raw(src)).group(1)
    vs = re.search(r'<VideoStream ObjectRef="(\d+)"', doc.raw(med, uid=True)).group(1)
    return int(re.search(r'<FrameRate>(\d+)</FrameRate>', doc.raw(vs)).group(1))


def clone_at(doc, ti_id, start, end, tin_ticks):
    """deep clone of a video track item (all effects) at a new time with a new source in-point"""
    t = doc.raw(ti_id)
    sc_id, vc_id = clip_of(doc, ti_id)
    ch_id = re.search(r'<Components ObjectRef="(\d+)"', t).group(1)
    objs, comp_ids = [], []
    for cid in chain_components(doc, ch_id):
        ncid, texts = clone_component(doc, cid); comp_ids.append(ncid); objs += texts
    nch, chtxt = clone_chain(doc, ch_id, comp_ids)
    nvc, nsc, nti = doc.new_id(), doc.new_id(), doc.new_id()
    vctxt = set_inout(strip_inline(doc.raw(vc_id).replace('ObjectID="%s"' % vc_id, 'ObjectID="%s"' % nvc, 1)), tin_ticks, tin_ticks + (end - start))
    vctxt = re.sub(r'<ClipID>[^<]*</ClipID>', '<ClipID>%s</ClipID>' % uuid.uuid4(), vctxt)
    sctxt = re.sub(r'(<Clip ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nvc, doc.raw(sc_id).replace('ObjectID="%s"' % sc_id, 'ObjectID="%s"' % nsc, 1))
    titxt = t.replace('ObjectID="%s"' % ti_id, 'ObjectID="%s"' % nti, 1)
    titxt = re.sub(r'(<Components ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nch, titxt)
    titxt = re.sub(r'(<SubClip ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nsc, titxt)
    titxt = re.sub(r'\n\t*<IsMuted>[^<]*</IsMuted>', '', titxt)
    titxt = re.sub(r'(</ClipTrackItem>\s*<ID>)[^<]*(</ID>)', r'\g<1>%s\g<2>' % uuid.uuid4(), titxt, count=1)
    titxt = set_times2(titxt, start, end)
    return nti, objs + [chtxt, vctxt, sctxt, titxt]


def find_broll_template(doc, part, tin_s):
    """an existing (graded, framed) B-roll item of that media near that in-point, any ad"""
    best = None
    for n, seq in for_claude_sequences(doc):
        for tr in video_tracks(doc, seq):
            for tid in live(doc, tr):
                t = doc.raw(tid); sub = re.search(r'<SubClip ObjectRef="(\d+)"', t)
                if not sub or '<Components ObjectRef=' not in t: continue
                nm = re.search(r'<Name>([^<]*)</Name>', doc.raw(sub.group(1)))
                if not nm or part not in nm.group(1) or not nm.group(1).startswith('A003'): continue
                _, vc = clip_of(doc, tid)
                ip = re.search(r'<InPoint>(-?\d+)</InPoint>', doc.raw(vc))
                if not ip: continue
                d = abs(int(ip.group(1)) / TPS - tin_s)
                if best is None or d < best[0]: best = (d, tid)
    assert best and best[0] < 0.6, (part, tin_s, best)
    return best[1]


def swap_media(doc, tid, mc_uid, master_clip_id, log_name):
    """point an existing item at another master (same length render): new clip instance, old one removed"""
    sub, old_vc = clip_of(doc, tid)
    s, e = item_bounds(doc, tid)
    ip = int(re.search(r'<InPoint>(-?\d+)</InPoint>', doc.raw(old_vc)).group(1))
    nvc = doc.new_id()
    v = strip_inline(doc.raw(master_clip_id).replace('ObjectID="%s"' % master_clip_id, 'ObjectID="%s"' % nvc, 1))
    v = re.sub(r'\n\t*<InUse>[^<]*</InUse>', '', v)
    v = re.sub(r'\n\t*<(In|Out)Point>[^<]*</(In|Out)Point>', '', v)
    v = re.sub(r'(<Source ObjectRef="\d+"/>)', lambda m: m.group(1) + '\n\t\t\t<OutPoint>%d</OutPoint>\n\t\t\t<InPoint>%d</InPoint>' % (ip + e - s, ip), v, count=1)
    v = re.sub(r'<ClipID>[^<]*</ClipID>', '<ClipID>%s</ClipID>' % uuid.uuid4(), v)
    st = doc.raw(sub)
    st = re.sub(r'(<Clip ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nvc, st)
    st = re.sub(r'(<MasterClip ObjectURef=")[^"]+(")', r'\g<1>%s\g<2>' % mc_uid, st)
    doc.replace_obj(sub, st)
    s0, e0 = doc.span(old_vc); doc.txt = doc.txt[:s0 - 1] + doc.txt[e0:]
    return v


def main():
    log = print
    doc = Doc(SRC)
    seqs = {s.attrib['ObjectUID'][:8]: s for n, s in for_claude_sequences(doc)}
    new_objs = []
    # 1. colour override on the re-cleaned sources
    for needle in ('VERSION 2', 'VERSSION 2'):
        for fp, vs in media_streams(doc, needle):
            ch = set_override(doc, vs, PROFILE); log('colour override %s %s' % (os.path.basename(fp)[:40], 'set' if ch else 'already set'))
    # 2. bigger credential tags
    bigger_tags(doc, log)
    # 3. hr_window -> gfx_v4
    v4 = {n: (mc, cl) for n, mc, cl, fp in masters_by_path(doc, 'gfx_v4')}
    hr_tracks = video_tracks(doc, seqs['404c5cb2'])
    swapped = 0
    for tr in hr_tracks:
        for tid in live(doc, tr):
            sub = re.search(r'<SubClip ObjectRef="(\d+)"', doc.raw(tid))
            if not sub: continue
            nm = re.search(r'<Name>([^<]*)</Name>', doc.raw(sub.group(1)))
            if nm and nm.group(1) == 'hr_window.mov':
                mc, cl = v4['hr_window.mov']
                new_objs.append(swap_media(doc, tid, mc, cl, 'hr_window')); swapped += 1
    log('hr_window swapped: %d' % swapped)
    # 4. CTA end segment
    kit = {k['name']: k for k in json.load(open(os.path.join(AUD, 'kit.json')))}
    def master_named(name):
        for e in doc.root:
            if e.tag == 'ClipProjectItem' and e.findtext('.//ProjectItem/Name') == name:
                mc = e.find('MasterClip').attrib['ObjectURef']
                return mc, re.search(r'<Clip Index="0" ObjectRef="(\d+)"', doc.raw(mc, uid=True)).group(1)
        raise KeyError(name)
    cta_mc, cta_cl = v4['cta_end.mov']
    vo = [x for x in masters_by_path(doc, 'ElevenLabs_2026-10-04T00_57_52')]; assert len(vo) == 1, vo
    vo_name, vo_mc, vo_cl, _ = vo[0]
    end_mc, end_cl = master_named(END_FILE)
    b = Builder(doc)
    for key, cfg in CTA_ADS.items():
        seq = seqs[key]; vts = video_tracks(doc, seq)
        L = max(item_bounds(doc, t)[1] for t in live(doc, vts[0])) / TPS
        L = round(L * 60) / 60.0
        T0 = tk(L)
        # B-roll shots
        t = 0.0; shot_ids = []
        for part, tmpl_in, new_in, dur in CTA_SHOTS:
            tmpl = find_broll_template(doc, part, tmpl_in)
            _, vc = clip_of(doc, tmpl); fr = media_fps_ticks(doc, vc)
            s, e = tk(L + t), tk(L + t + dur)
            nti, objs = clone_at(doc, tmpl, s, e, int(round(new_in * TPS / fr)) * fr)
            new_objs += objs; shot_ids.append(nti); t += dur
        assert abs(t - CTA_LEN) < 1e-6
        # graphic
        tmpl = motion_template(doc, seq)
        gid, gobjs = overlay_item(doc, tmpl, dict(master_vclip=cta_cl, mc_uid=cta_mc, name='cta_end.mov'), T0, tk(L + CTA_LEN))
        # card 120 px lower: its backdrop then starts where the captions' backdrop starts
        moved = 0
        for i, o in enumerate(gobjs):
            if '<Name>Position</Name>' in o and '<StartKeyframe>' in o and moved == 0:
                gobjs[i] = re.sub(r'(<StartKeyframe>-?\d+,)[^,]*(,)', r'\g<1>0.5:%r\g<2>' % (0.5 + 120 / 1920.0), o, count=1); moved += 1
        assert moved == 1, 'CTA position not set'
        new_objs += gobjs
        # audio
        g, ats = audio_tracks(doc, seq); auids = [a.attrib['ObjectUID'] for a in ats]
        a1 = track_item_ids(doc, auids[0]); tmpl_a = a1[0]
        tmpl_chain = re.search(r'<Components ObjectRef="(\d+)"', doc.raw(tmpl_a)).group(1)
        cid = b.clip_instance(vo_cl, 0.0, 4.41, VO_GAIN_DB)
        vo_item = b.track_item(tmpl_a, tmpl_chain, vo_mc, vo_name, cid, L, L + 4.41)
        # music: the user's last Paradigm Shift clip runs to the first downbeat inside the CTA, then the ending file
        mus = [i for i in track_item_ids(doc, auids[1])]
        last = max(mus, key=lambda i: item_bounds(doc, i)[1])
        sub, mclip = clip_of(doc, last)
        ms, me = item_bounds(doc, last)
        mct = doc.raw(mclip)
        ip = int(re.search(r'<InPoint>(-?\d+)</InPoint>', mct).group(1)) / TPS
        g_db = 20 * math.log10(float(re.search(r'<Gain>([^<]*)</Gain>', mct).group(1))) if '<Gain>' in mct else 0.0
        src_L = ip + (L - ms / TPS)
        k = math.ceil(src_L / BAR - 1e-6); Tc = L + (k * BAR - src_L)
        doc.replace_obj(last, re.sub(r'<End>\d+</End>', '<End>%d</End>' % aticks(Tc), doc.raw(last)))
        mct2 = re.sub(r'<OutPoint>-?\d+</OutPoint>', '<OutPoint>%d</OutPoint>' % aticks(ip + (Tc - ms / TPS)), mct)
        doc.replace_obj(mclip, mct2)
        e_start = Tc - END_PRE; e_len = min(4.688, L + CTA_LEN - e_start)
        cid = b.clip_instance(end_cl, 0.0, e_len, g_db)
        end_item = b.track_item(tmpl_a, tmpl_chain, end_mc, END_FILE, cid, e_start, e_start + e_len)
        # SFX
        sfx = {0: [], 1: []}; lane_end = [L, L]
        for dt, nm, rel, at_start in CTA_SFX:
            kk = kit[nm]; f = kk['file']; mc, cl = master_named(f)
            st = L + dt if at_start else L + dt + 0.010 - kk['peak_t']
            ln = kk['dur'] if nm != 'COUNT_09' else 0.68
            lane = 0 if st >= lane_end[0] else 1
            gain = VOICE + rel - kk['m_max']
            cid = b.clip_instance(cl, 0.0, ln, gain)
            sfx[lane].append(b.track_item(tmpl_a, tmpl_chain, mc, f, cid, st, st + ln)); lane_end[lane] = st + ln
        # all new items go after L on their tracks (tracks are empty there)
        for u in auids[2:4] + [auids[0], auids[1]]:
            for i in track_item_ids(doc, u):
                assert item_bounds(doc, i)[1] <= aticks(Tc) + 1 or u in (auids[1],), (key, 'track busy after L')
        put_after(doc, vts[cfg['broll_track']].attrib['ObjectUID'], shot_ids)
        put_after(doc, vts[cfg['gfx_track']].attrib['ObjectUID'], [gid])
        put_after(doc, auids[0], [vo_item]); put_after(doc, auids[1], [end_item])
        put_after(doc, auids[2], sfx[0]); put_after(doc, auids[3], sfx[1])
        log('%s: CTA %.3f-%.3f, music cut %.3f (downbeat %d), final chord at %.3f, %d SFX' % (key, L, L + CTA_LEN, Tc, k, Tc + 2 * BAR, len(CTA_SFX)))
    txt = doc.txt.replace('</PremiereData>', ''.join(x if x.endswith('\n') else x + '\n' for x in new_objs + b.new) + '</PremiereData>')
    open(OUT_XML, 'w', encoding='utf-8').write(txt)
    with gzip.open(OUT, 'wb') as f: f.write(txt.encode('utf-8'))
    log('-> ' + OUT)


if __name__ == '__main__':
    main()
