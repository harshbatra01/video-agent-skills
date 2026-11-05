"""v6 on v6imp.xml (= the user's v5 save + Premiere-imported gfx_v3 renders), the user's 3 Oct review:
 3 things  '?' without the boxed glow; 100x meter starts with the vitamin C B-roll (B-roll now from 10.30);
           bioavailability card without 'noun' and readable; REFORMULATED; CAN ABSORB IT EFFICIENTLY -> EFFECTIVELY;
           'here and here' = tracked spotlight (rest of the frame dims + softens) instead of the green tint; glass blur redone
 all ads   VITAMINS / MINERALS / NUTRIENTS with white rules
 held      pool B-roll -> C126 calf stretch
 I'm 52    no archive under 'has always stuck'; pouch B-roll from 'Immufix'
 ran pro   mass start clip without its 5-frame head (legs + crowd shots only)
 people    B-roll rearranged per the user's notes, A-roll (graded) back at 3.83-5.93, 7.52-9.25, 13.57-15.48,
           montage Boston stage / Westin Tokyo / gala / Joan; packing shot + A-roll grade less washed out
Untouched objects stay byte-identical. usage: python build_v6.py in.xml out.prproj"""
import sys, os, re, json, gzip
sys.path.insert(0, '.')
sys.path.insert(0, '../work')
from build_project import Doc, TPS, fmt, for_claude_sequences, video_tracks, track_items
from build_broll import chain_components, set_inout, set_track_items
from build_ext import set_times2, delete_item, item_times, retime_item, ext_item, clone_item
import build_zoom_gfx as Z
from build_title_v2 import inline_blobs
from build_v3 import lumetri_ids, set_lumetri, item_name as _item_name
from build_v4 import motion_of, overlay_item, normalize_text_blobs
import v5lib as L
import build_v5 as B5

HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.dirname(HERE)
MG, V2 = B5.MG, B5.V2
V3 = MG + r'\gfx_v3'
YT, BR = B5.YT, r'C:\VISION\IMMUFIX\repair\ENCODED RUSHES\B roll' + '\\'
STARS = YT + 'Paula Radcliffe Chasing Stars_1080p.mp4'
F25 = 10160640000
W, H = 1080, 1920
tk, ts = B5.tk, B5.ts
V3_NAMES = ['tt_qmark', 'tt_p1', 'tt_meter', 'tt_p2', 'tt_powder', 'tt_vmn', 'tt_p3', 'q3_vmn', 'i52_vmn', 'rp_vmn']
PS_AROLL_FIX = {20: 14.0, 22: 15.0, 24: -36.0, 16: 105.0, 42: 15.0}            # was con 8, sha 22.7, blk -25.9, sat 100, vib 13.2
PS_PACKING_FIX = {19: 0.55, 20: 30.0, 22: 4.0, 23: -10.0, 24: -48.0, 16: 110.0, 42: 15.0}
SPOT = (41.08, 42.13)            # 'here and here'; the B-roll cut follows at 42.13
SPOT_FIRST, SPOT_SECOND = (41.10, 41.30), (41.66, 41.86)


def near(a, b, tol=0.025): return abs(a - b) < tol


def live(doc, tr):
    """clip items of a track (not its transitions), only ones that still exist"""
    t = doc.raw(tr.attrib['ObjectUID'], uid=True)
    m = re.search(r'<ClipItems Version="\d+">\s*<TrackItems Version="1">(.*?)</TrackItems>', t, re.S)
    out = []
    for i in (re.findall(r'<TrackItem Index="\d+" ObjectRef="(\d+)"/>', m.group(1)) if m else []):
        try: doc.raw(i); out.append(i)
        except KeyError: pass
    return out


def item_name(doc, ti):
    """clip name, '' for items without a source clip (e.g. a caption upgraded to a graphic)"""
    return _item_name(doc, ti) if '<SubClip ObjectRef=' in doc.raw(ti) else ''


def secs(x): return x / TPS


def src_ticks(sec, fr): return int(round(sec * TPS / fr)) * fr


def set_item(doc, ti, start, end, in_ticks):
    """move/trim a clip: timeline start/end (ticks) and its media in-point (ticks)"""
    s, e, tin, vc = item_times(doc, ti)
    doc.replace_obj(ti, set_times2(doc.raw(ti), start, end))
    doc.replace_obj(vc, set_inout(doc.raw(vc), in_ticks, in_ticks + (end - start)))


def items_at(doc, tr, sec, name_part=None):
    out = [i for i in live(doc, tr) if near(secs(item_times(doc, i)[0]), sec)]
    if name_part: out = [i for i in out if name_part in item_name(doc, i)]
    assert len(out) == 1, ('no unique item at', sec, name_part, [item_name(doc, i) for i in out])
    return out[0]


def track_with(doc, trs, pred):
    hits = [tr for tr in trs if any(pred(i) for i in live(doc, tr))]
    assert len(hits) == 1, ('tracks matching', len(hits))
    return hits[0]


def put_items(doc, tr, add=()):
    ids = list(dict.fromkeys(live(doc, tr) + list(add)))
    set_track_items(doc, tr.attrib['ObjectUID'], sorted(ids, key=lambda x: item_times(doc, x)[0]))


def motion_comp(doc, ti):
    ch = re.search(r'<Components ObjectRef="(\d+)"', doc.raw(ti)).group(1)
    return [c for c in chain_components(doc, ch) if '<MatchName>AE.ADBE Motion</MatchName>' in doc.raw(c)][0]


def set_named_param(doc, comp_id, name, value):
    for pid in re.findall(r'<Param Index="\d+" ObjectRef="(\d+)"', doc.raw(comp_id)):
        p = doc.raw(pid)
        if '<Name>%s</Name>' % name in p:
            doc.replace_obj(pid, Z.set_value(p, value)); return
    raise KeyError(name)


def param_by_index(doc, comp_id, idx):
    return re.search(r'<Param Index="%d" ObjectRef="(\d+)"' % idx, doc.raw(comp_id)).group(1)


def master_of(doc, ti):
    sc = re.search(r'<SubClip ObjectRef="(\d+)"', doc.raw(ti)).group(1)
    return re.search(r'<MasterClip ObjectURef="([^"]+)"', doc.raw(sc)).group(1)


# ---------------------------------------------------------------- overlays: gfx_v2 -> gfx_v3
def motion_template(doc, seq):
    """a clip with an explicit Motion component (Premiere drops default Motion from overlay items on save); prefer 1080x1920 media"""
    cands = [i for tr in video_tracks(doc, seq) for i in live(doc, tr) if '<Components ObjectRef=' in doc.raw(i) and motion_of(doc, i)]
    tall = [i for i in cands if '<FrameRect>0,0,1080,1920</FrameRect>' in doc.raw(i)]
    return (tall or cands)[0]


def swap_overlays(doc, seq, v2m, v3m, meta, log):
    n = 0
    tmpl = motion_template(doc, seq)
    for tr in video_tracks(doc, seq):
        new = []
        for ti in live(doc, tr):
            nm = item_name(doc, ti)
            base = nm[:-4] if nm.endswith('.mov') else None
            if base in V3_NAMES and master_of(doc, ti) == v2m[base]['mc_uid']:
                s, e, _, _ = item_times(doc, ti)
                if base == 'tt_meter': s, e = tk(meta[base]['start']), tk(meta[base]['end'])
                assert e - s <= v3m[base]['info']['dur'] + F25, ('overlay longer than its render', base)
                nti, objs = overlay_item(doc, tmpl, v3m[base], s, e)
                Z.append_objects(doc, objs); delete_item(doc, ti); new.append(nti); n += 1
                log('  overlay %s -> gfx_v3 %.2f-%.2f' % (base, secs(s), secs(e)))
        if new: put_items(doc, tr, new)
    return n


# ---------------------------------------------------------------- 3 things: tracked spotlight on 'here and here'
def neutral_lumetri(doc, seqs):
    """the user's exposure-only Lumetri in I'm 52 (no LUT, neutral curves): template for the spotlight dim"""
    gr = video_tracks(doc, seqs['348e0ba6'])[4]
    for ti in live(doc, gr):
        for c in lumetri_ids(doc, ti):
            con = doc.raw(param_by_index(doc, c, 20)); exp = doc.raw(param_by_index(doc, c, 19))
            if re.search(r'<StartKeyframe>-?\d+,0\.,', con) and re.search(r'<StartKeyframe>-?\d+,0\.49', exp):
                return c
    raise KeyError('neutral Lumetri')


def spotlight_item(doc, tmpl_adj, lum_tmpl, S, log):
    s0, s1 = SPOT
    start, end = tk(s0), tk(s1)
    mt = lambda t: L.ADJ_IN + ts(t) - start
    rows = [r for r in S['rows'] if s0 - 0.05 <= r[0] <= s1 + 0.02]
    w, h, f1 = S['w'], S['h'], S['f1']
    path = L.poly_pts([((540 - w / 2) / W, 960 / H), ((540 + w / 2) / W, 960 / H), ((540 + w / 2) / W, (960 + h) / H), ((540 - w / 2) / W, (960 + h) / H)])
    anchor = (540 / W, 960 / H)

    def hfrac(t):
        u = min(1.0, max(0.0, (t - SPOT_SECOND[0]) / (SPOT_SECOND[1] - SPOT_SECOND[0]))); u = u * u * (3 - 2 * u)
        return f1 + (1 - f1) * u
    pk = rk = swk = shk = ''
    for i, r in enumerate(rows):
        t = r[0]; tn = rows[i + 1][0] if i + 1 < len(rows) else t + 0.04
        hold = min(tn - 1 / 240.0, t + 0.04)
        for tt in (t, hold):
            if tt < s0 or tt > s1: continue
            pk += L.kf_point(mt(tt), r[1], r[2]); rk += L.kf_scalar(mt(tt), r[3])
            swk += L.kf_scalar(mt(tt), r[4]); shk += L.kf_scalar(mt(tt), r[4] * hfrac(tt))
    masks = []
    objs = []
    for n in (1, 2):
        mc, mtx = L.mask_component(doc, n, path, feather=60.0, anchor=anchor, pos=(rows[0][1], rows[0][2]), pos_keys=pk, rot_keys=rk,
                                   sw_keys=swk, sh_keys=shk, inverted=True)
        masks.append(mc); objs += mtx
    Z.append_objects(doc, objs)
    # dim + desaturate outside the lines (ramps in on the first 'here')
    lt = doc.raw(lum_tmpl)
    lc, ltx = L._clone(doc, lt, [doc.raw(p) for p in re.findall(r'<Param Index="\d+" ObjectRef="(\d+)"', lt)], 3, 'Spotlight dim',
                       {'Exposure': '0.'}, {}, sub_ids=[masks[0]])
    Z.append_objects(doc, ltx)
    a, b = SPOT_FIRST
    for idx, v0, v1 in ((19, 0.0, -1.0), (16, 100.0, 76.0)):
        pid = param_by_index(doc, lc, idx)
        doc.replace_obj(pid, Z.set_keys(Z.set_value(doc.raw(pid), fmt(v0)), L.kf_scalar(mt(a), v0) + L.kf_scalar(mt(b), v1)))
    gc, gtx = L.gblur_component(doc, 4, 0.0, 'Spotlight soften', [masks[1]], blur_keys=L.kf_scalar(mt(a), 0.0) + L.kf_scalar(mt(b), 6.0))
    Z.append_objects(doc, gtx)
    nti, itx = L.adj_item(doc, tmpl_adj, start, end, [lc, gc], name='Board spotlight')
    Z.append_objects(doc, itx)
    log('  spotlight %.2f-%.2f, %d track samples, lit area grows %.2f -> 1 at %.2f' % (s0, s1, len(rows), f1, SPOT_SECOND[0]))
    return nti


def build(src, out_path, log=print):
    doc = Doc(src)
    orig_blobs = inline_blobs(doc.txt); orig_txt = doc.txt
    seqs = {s.attrib['ObjectUID'][:8]: s for n, s in for_claude_sequences(doc)}
    meta = json.load(open(os.path.join(SCR, 'ae', 'gfx_v3_meta.json')))
    geom = json.load(open(os.path.join(V3, 'glass_geom.json')))
    S = json.load(open(os.path.join(SCR, 'track', 'spot_tt.json')))
    v2m = {b: B5.find_by_path(doc, V2 + '\\' + b + '.mov') for b in V3_NAMES}
    v3m = {b: B5.find_by_path(doc, V3 + '\\' + b + '.mov') for b in V3_NAMES + ['tt_eff']}

    log('overlays')
    for key in ('f233433f', '974102f7', '348e0ba6', '0991faf2'):
        n = swap_overlays(doc, seqs[key], v2m, v3m, meta, log)
        log(' %s: %d swapped' % (key, n))

    # ---------------- 3 things
    log('3 things')
    seq = seqs['f233433f']; trs = video_tracks(doc, seq)
    vit = [i for tr in trs for i in live(doc, tr) if item_name(doc, i).startswith('3things_vitaminC')]
    assert len(vit) == 1
    br = track_with(doc, trs, lambda i: i == vit[0])
    set_item(doc, vit[0], tk(10.30), tk(13.18), 0)
    gr = track_with(doc, trs, lambda i: item_name(doc, i) == 'Adjustment Layer' and near(secs(item_times(doc, i)[1]), 10.70) and item_times(doc, i)[0] == 0)
    g = [i for i in live(doc, gr) if near(secs(item_times(doc, i)[1]), 10.70)][0]
    retime_item(doc, g, 0, tk(10.30))
    log('  vitamin C B-roll 10.30-13.18 (grade before it ends 10.30)')
    board = track_with(doc, trs, lambda i: item_name(doc, i) == 'Board blur')
    tmpl_adj = [i for i in live(doc, board) if item_name(doc, i) == 'Board blur'][0]
    hl = [i for i in live(doc, board) if item_name(doc, i) == 'Board highlight']
    assert len(hl) == 1
    delete_item(doc, hl[0])
    sp = spotlight_item(doc, tmpl_adj, neutral_lumetri(doc, seqs), S, log)
    put_items(doc, board, [sp])
    glass = track_with(doc, trs, lambda i: item_name(doc, i).startswith('Glass blur'))
    for i in live(doc, glass): delete_item(doc, i)
    gids, objs = B5.glass_items(doc, tmpl_adj, geom, meta, log)
    Z.append_objects(doc, objs); put_items(doc, glass, gids)
    lane = track_with(doc, trs, lambda i: item_name(doc, i) == 'tt_p1.mov')
    nti, objs = overlay_item(doc, motion_template(doc, seq), v3m['tt_eff'], tk(meta['tt_eff']['start']), tk(meta['tt_eff']['end']))
    Z.append_objects(doc, objs); put_items(doc, lane, [nti])
    log('  tt_eff %.2f-%.2f' % (meta['tt_eff']['start'], meta['tt_eff']['end']))

    # ---------------- I'm 52
    log("I'm 52")
    seq = seqs['348e0ba6']; trs = video_tracks(doc, seq); br, gr = trs[3], trs[4]
    arch = items_at(doc, br, 12.68, 'Thank you Paula')
    a_s = item_times(doc, arch)[0]
    delete_item(doc, arch)
    pouch = items_at(doc, br, 13.40, 'C132')
    s, e, _, _ = item_times(doc, pouch); retime_item(doc, pouch, tk(13.52), e)
    g = [i for i in live(doc, gr) if abs(item_times(doc, i)[1] - a_s) < tk(0.02)]
    assert len(g) == 1
    retime_item(doc, g[0], item_times(doc, g[0])[0], tk(13.52))
    put_items(doc, br); put_items(doc, gr)
    log('  archive at 12.68 removed, A-roll + grade to 13.52, pouch 13.52-%.2f' % secs(e))

    # ---------------- ran professionally
    log('ran pro')
    seq = seqs['0991faf2']; trs = video_tracks(doc, seq); br = trs[2]
    ms = items_at(doc, br, 6.68, 'Thank you Paula')
    s, e, tin, _ = item_times(doc, ms)
    assert near(secs(tin), 32.00, 0.05), secs(tin)
    set_item(doc, ms, s, e, src_ticks(32.24, F25))
    log('  mass start in-point 32.00 -> 32.24 (legs + crowd shots only)')

    # ---------------- people are always surprised
    log('people surprised')
    seq = seqs['664b35b2']; trs = video_tracks(doc, seq); br, gr = trs[2], trs[3]
    stars = B5.find_by_path(doc, STARS); fr_st = stars['info']['fr']
    thank_fr = F25
    ids = {lab: items_at(doc, br, t, part) for lab, t, part in [
        ('arms', 2.75, 'Thank you'), ('bridge', 3.83, 'Thank you'), ('chicago', 4.85, 'Chasing'), ('heels', 7.52, 'Chasing'),
        ('gala', 8.38, 'Chasing'), ('london', 9.25, 'Chasing'), ('boston', 9.82, 'Chasing'), ('c136', 10.45, 'C136'),
        ('tokyo', 11.62, 'Chasing'), ('joan', 12.22, 'Chasing'), ('fans', 13.57, 'Thank you'), ('c131', 15.48, 'C131')]}
    set_item(doc, ids['bridge'], tk(2.75), tk(3.83), src_ticks(196.40, thank_fr))
    set_item(doc, ids['boston'], tk(9.25), tk(10.45), src_ticks(1473.60, fr_st))
    set_item(doc, ids['gala'], tk(11.62), tk(12.61), src_ticks(1138.00, fr_st))
    set_item(doc, ids['joan'], tk(12.61), tk(13.57), src_ticks(1326.30, fr_st))
    jpx, jpy, jsc = B5.arch_motion('STARS', 0.32, 1.0)
    set_named_param(doc, motion_comp(doc, ids['joan']), 'Position', '%.6f:%.6f' % (jpx, jpy))
    wpx, wpy, wsc = B5.arch_motion('STARS', 0.58, 1.0)
    westin, objs = ext_item(doc, ids['tokyo'], stars, tk(10.45), tk(11.62), src_ticks(552.30, fr_st), wpx, wpy, wsc, {})
    Z.append_objects(doc, objs)
    for lab in ('arms', 'chicago', 'heels', 'london', 'c136', 'tokyo', 'fans'): delete_item(doc, ids[lab])
    put_items(doc, br, [westin])
    g0 = [i for i in live(doc, gr) if item_times(doc, i)[0] == 0]
    assert len(g0) == 1
    new_g = []
    for a, b in ((3.83, 5.93), (7.52, 9.25), (13.57, 15.48)):
        nti, objs = clone_item(doc, g0[0], tk(a), tk(b)); Z.append_objects(doc, objs); new_g.append(nti)
    put_items(doc, gr, new_g)
    kf = []
    for i in live(doc, gr):
        for c in lumetri_ids(doc, i): set_lumetri(doc, c, PS_AROLL_FIX, kf)
    for c in lumetri_ids(doc, ids['c131']): set_lumetri(doc, c, PS_PACKING_FIX, kf)
    assert not kf, ('keyframed Lumetri values overwritten', kf)
    log('  B-roll: bridge 2.75-3.83, Boston 9.25-10.45, Westin 10.45-11.62, gala 11.62-12.61, Joan 12.61-13.57; 7 clips removed')
    log('  grade added 3.83-5.93, 7.52-9.25, 13.57-15.48; A-roll grade + packing shot deepened')

    # ---------------- i held the record
    log('held record')
    seq = seqs['404c5cb2']; trs = video_tracks(doc, seq); br = trs[2]
    pool = items_at(doc, br, 19.37, 'Chasing')
    c123 = items_at(doc, br, 16.32, 'C123')
    c126 = B5.find_by_path(doc, BR + 'A003_09181335_C126.mp4')
    sc = float(motion_of(doc, c123)['Scale'])
    px = (540 - (0.47 - 0.5) * 6048 * sc / 100) / 1080
    s, e, _, _ = item_times(doc, pool)
    nti, objs = ext_item(doc, c123, c126, s, e, src_ticks(31.0, F25), px, 0.5, sc, {})
    Z.append_objects(doc, objs); delete_item(doc, pool); put_items(doc, br, [nti])
    log('  pool -> C126 calf stretch %.2f-%.2f (src 31.0, scale %.1f, px %.3f)' % (secs(s), secs(e), sc, px))

    extra = dict(orig_blobs); extra.update(Z.T['blobs']); extra.update(Z.NEW_BLOBS)
    doc.txt, n = Z.normalize_blobs(doc.txt, extra)
    doc.txt, n2 = normalize_text_blobs(doc.txt, orig_txt)
    log('blob fixes %d, caption text blob fixes %d' % (n, n2))
    open(out_path + '.xml', 'w', encoding='utf-8', newline='\n').write(doc.txt)
    with open(out_path + '.xml', 'rb') as f, gzip.open(out_path, 'wb') as g:
        g.write(f.read())


if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2])
