"""v5 on v5imp.xml (= the user's v3 save + gfx_v1 renders, + gfx_v2 renders and stars v2 imported in Premiere).
Everything from v4 except: captions under graphics are DISABLED (not deleted); new archive B-roll from the user's YouTube
downloads; v2 graphics; tracked whiteboard blur / highlight masks and a tracked '?' in 3 things; live frosted-glass
blur behind the 3 things cards; retimed titles; B-roll fixes.
usage: python build_v5.py in.xml out.prproj"""
import sys, os, re, json, gzip, uuid
sys.path.insert(0, '.')
sys.path.insert(0, '../work')
from build_project import Doc, TPS, fmt, for_claude_sequences, video_tracks, track_items
from build_broll import chain_components, clone_chain, set_inout, set_track_items, clone_component
from build_ext import set_times2, delete_obj, component_ids, delete_item, item_times, retime_item, ext_item, clone_item, media_objects, bin_object
import build_zoom_gfx as Z
from build_title_v2 import ek, ekp, inline_blobs
from build_v3 import text_layer2, cap_h, lumetri_ids, set_lumetri, item_name, TITLE_NAME, TITLE_Y, TITLE_Y_DEFAULT, STOCK_GRADE, NAME, CRED, GOLD, INK
from build_v4 import find_master, motion_of, broll_track, grade_track, live, at, static, overlay_item, caption_tracks, caption_items, normalize_text_blobs, SWAP_TO_C132, STOCK_SWAP, REMOVE, LATE_TINT
import v5lib as L
import gfx_plan

HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(SCR, 'v5'))
from plan_broll import PLAN, SRC as ARCH_SRC, YT, motion as arch_motion
MG = r'C:\VISION\IMMUFIX\repair\ENCODED RUSHES\Motion graphics'
V2 = MG + r'\gfx_v2'
F60, F25 = 4233600000, 10160640000
W, H = 1080, 1920


def tk(sec): return int(round(sec * 60)) * F60
def ts(sec): return int(round(sec * TPS))


TITLE_TIME = {'f233433f': (0.4, 2.8), '974102f7': (0.4, 3.4), '593f11c4': (1.3, 2.70), 'cd03e189': (3.8, 6.43),
              '0991faf2': (0.4, 3.30), '404c5cb2': (0.4, 2.60), '664b35b2': (0.3, 2.0), '348e0ba6': (0.3, 2.18)}
TITLE_LAYOUT = {'f233433f': dict(k=0.80, left=52)}         # whiteboard ad: smaller, left of her face
C132_RANPRO_SHIFT = -0.208                                # ran professionally pouch pan: push left (fraction of frame width)
C137_1STAR_FIX = {19: 0.45, 20: 32.0, 24: -42.0, 22: 6.0, 16: 112.0, 23: -12.0}    # 1 star pouch shot: was washed out
C144_TRIM = ('974102f7', 20.03, 21.33)                    # 3 questions: Paula talks first, B-roll from 21.33
REPLACE_BROLL = {'664b35b2': [2.75, 4.17], '404c5cb2': [4.72], '593f11c4': [12.35]}   # existing B-roll starts replaced by archive
RETIME_BROLL = [('664b35b2', 9.82, 10.45, 11.62)]         # C136 travel shot now starts after the stage montage
TT_BROLL = [('f233433f', 31.74, 33.90, 'A003_09181332_C122.mp4', 14.0, 0.659)]   # drinking under ALMOST 100%
TT_POWDER = ('f233433f', 19.05)                            # powder B-roll: focus pull + push-in
ARCH_GRADE = {**STOCK_GRADE, 14: 3.0, 16: 96.0, 20: 8.0, 41: 16.0}
MODERN_GRADE = {**STOCK_GRADE, 14: 2.0, 16: 100.0}
V1_OVER = [('i52_powders', '348e0ba6', ('broll', 9.08)), ('i52_pills', '348e0ba6', ('broll', 10.37)), ('i52_shakes', '348e0ba6', ('broll', 11.12)),
           ('s1_pouch', 'cd03e189', ('broll', 6.45)), ('s1_pills', 'cd03e189', ('broll', 14.98)), ('s1_scoop', 'cd03e189', ('broll', 17.07)),
           ('s1_water', 'cd03e189', ('broll', 19.32)), ('tt_100', 'f233433f', ('broll', 38.03)), ('tt_since', 'f233433f', 42.55),
           ('sw_1998', '593f11c4', 0.0), ('hr_17', '404c5cb2', 1.45)]
NO_CAPTION_DISABLE = {'tt_qmark', 'fx_flash'}
BOARD_WIPES = {'L1': (4.00, 4.90), 'L2a': (15.05, 16.25), 'L2b': (16.25, 17.15), 'L3a': (28.15, 29.45), 'L3b': (29.50, 30.35)}
BOARD_BLUR_END = 30.62
HL_WIPES = {'L2a': (41.10, 41.32), 'L2b': (41.24, 41.46), 'L3a': (41.66, 41.88), 'L3b': (41.80, 42.02)}
HL_SPAN = (41.08, 42.13)


# ---------------------------------------------------------------- media lookups
def media_path_of_master(doc, cpi):
    mc = doc.deref(cpi.find('MasterClip'))
    for c in mc.find('Clips'):
        vc = doc.deref(c)
        if vc.tag != 'VideoClip': continue
        vt = doc.raw(vc.attrib['ObjectID'])
        src = doc.raw(re.search(r'<Source ObjectRef="(\d+)"', vt).group(1))
        m = re.search(r'<Media ObjectURef="([^"]+)"', src)
        if not m: return None, None
        media = doc.raw(m.group(1), uid=True)
        p = re.search(r'<FilePath>([^<]*)</FilePath>', media)
        return (p.group(1) if p else None), vc
    return None, None


def find_by_path(doc, path):
    want = os.path.normcase(os.path.normpath(path))
    for e in doc.root:
        if e.tag != 'ClipProjectItem': continue
        p, vc = media_path_of_master(doc, e)
        if p and os.path.normcase(os.path.normpath(p.replace('&amp;', '&'))) == want:
            name = e.findtext('.//ProjectItem/Name')
            m = find_master(doc, name) if name else None
            mc = doc.deref(e.find('MasterClip'))
            vt = doc.raw(vc.attrib['ObjectID'])
            src = doc.raw(re.search(r'<Source ObjectRef="(\d+)"', vt).group(1))
            media = doc.raw(re.search(r'<Media ObjectURef="([^"]+)"', src).group(1), uid=True)
            vs = doc.raw(re.search(r'<VideoStream ObjectRef="(\d+)"', media).group(1))
            fr = int(re.search(r'<FrameRate>(\d+)</FrameRate>', vs).group(1)); dur = int(re.search(r'<Duration>(\d+)</Duration>', vs).group(1))
            return dict(master_vclip=vc.attrib['ObjectID'], mc_uid=mc.attrib['ObjectUID'], name=name, info=dict(fr=fr, dur=dur))
    raise KeyError(path)


# ---------------------------------------------------------------- titles
def title_B2(doc, cred, t0_media, dur, yb, k=1.0, left=None):
    t = lambda sec: t0_media + Z.s2t(sec)
    E = 1 / 3
    ns, cs = round(NAME[1] * k), round(CRED[1] * k)
    wn = Z.text_width(NAME[0], ns, 'PAULA RADCLIFFE', NAME[2])
    cx = W / 2 if left is None else left + wn / 2
    ws = Z.text_width(CRED[0], cs, cred.upper(), CRED[2])
    ph = cap_h(CRED[0], cs) + 22 * k; pw = ws + 44 * k
    pill_top = yb + 22 * k; pill_cy = pill_top + ph / 2; cred_base = pill_top + 11 * k + cap_h(CRED[0], cs)
    comps, texts = [], []
    op = ek(t, [(0.00, 0, E, 0.3), (0.28, 100, 0.75, E), (dur - 0.45, 100, E, 0.7), (dur - 0.12, 0, 0.3, E)])
    pk = ekp(t, [(0.00, (cx, yb + 40), E, 0.12), (0.50, (cx, yb), 0.88, E), (dur - 0.45, (cx, yb), E, 0.7), (dur - 0.12, (cx, yb - 18), 0.3, E)])
    sk = ek(t, [(0.00, 106, E, 0.12), (0.50, 100, 0.88, E)])
    c, tx = text_layer2(doc, 50, 'PAULA RADCLIFFE', NAME[0], ns, (cx, yb), 0xFFFFFF, NAME[2], 2, (80, 22, 2), op, pk, sk)
    comps.append(c); texts += tx
    op = ek(t, [(0.42, 0, E, 0.3), (0.62, 100, 0.75, E), (dur - 0.55, 100, E, 0.6), (dur - 0.40, 0, 0.4, E)])
    pk = ekp(t, [(0.42, (cx, cred_base + 8), E, 0.12), (0.70, (cx, cred_base), 0.88, E)])
    c, tx = text_layer2(doc, 51, cred.upper(), CRED[0], cs, (cx, cred_base), INK, CRED[2], 2, None, op, pk)
    comps.append(c); texts += tx
    hs = ek(t, [(0.20, 0, E, 0.12), (0.55, 100, 0.88, E), (dur - 0.50, 100, E, 0.7), (dur - 0.18, 0, 0.3, E)])
    op = ek(t, [(0.20, 0, E, 0.3), (0.28, 100, 0.7, E), (dur - 0.24, 100, E, 0.5), (dur - 0.16, 0, 0.5, E)])
    c, tx = Z.shape_layer(doc, 52, 'Credential pill', Z.rrect_points(float(pw), float(ph), float(ph / 2)), Z.appearance(fill=GOLD, shadow=(35, 18, 3)),
                          (cx, pill_cy), (pw / 2, ph / 2), opacity=100.0, uniform=False, scale=100.0, hscale=0.0, opacity_keys=op, hscale_keys=hs)
    comps.append(c); texts += tx
    return comps, texts, (cx - wn / 2, cx + wn / 2)


def retitle(doc, trs, key, log):
    ti = [it.attrib['ObjectID'] for t_ in trs for it in track_items(doc, t_) if item_name(doc, it.attrib['ObjectID']) == TITLE_NAME][0]
    s, e, tin, vc = item_times(doc, ti)
    a, b = [tk(x) for x in TITLE_TIME[key]]
    doc.replace_obj(ti, set_times2(doc.raw(ti), a, b)); doc.replace_obj(vc, set_inout(doc.raw(vc), tin, tin + (b - a)))
    ch = re.search(r'<Components ObjectRef="(\d+)"', doc.raw(ti)).group(1)
    lay = TITLE_LAYOUT.get(key, {})
    comps, texts, span = title_B2(doc, gfx_plan.TITLE[key]['sub'], tin, (b - a) / TPS, TITLE_Y.get(key, TITLE_Y_DEFAULT), lay.get('k', 1.0), lay.get('left'))
    for c in chain_components(doc, ch):
        for k_ in component_ids(doc, c): delete_obj(doc, k_)
    items = ''.join('\n\t\t\t\t<Component Index="%d" ObjectRef="%s"/>' % (i, c) for i, c in enumerate(comps))
    doc.replace_obj(ch, re.sub(r'<Components Version="1">.*?</Components>', '<Components Version="1">%s\n\t\t\t</Components>' % items, doc.raw(ch), flags=re.S))
    log('title %s %s name x %.0f-%.0f' % (key, TITLE_TIME[key], span[0], span[1]))
    return texts


# ---------------------------------------------------------------- grade track surgery
def cut_grade(doc, gr, a, b, new_objs):
    """remove [a, b) ticks from the grade adjustment pieces (trim / split / delete); clones go straight into the track"""
    for g in list(live(doc, gr)):
        s, e, _, _ = item_times(doc, g)
        if e <= a or s >= b: continue
        if s >= a and e <= b:
            delete_item(doc, g); set_track_items(doc, gr.attrib['ObjectUID'], [x for x in live(doc, gr) if x != g]); continue
        if s < a and e > b:
            nti, objs = clone_item(doc, g, b, e); Z.append_objects(doc, objs)
            retime_item(doc, g, s, a)
            set_track_items(doc, gr.attrib['ObjectUID'], sorted(live(doc, gr) + [nti], key=lambda x: item_times(doc, x)[0]))
            continue
        if s < a: retime_item(doc, g, s, a)
        else: retime_item(doc, g, b, e)


def extend_grade_to(doc, gr, old_end, new_end):
    g = [x for x in live(doc, gr) if item_times(doc, x)[1] == old_end]
    assert len(g) == 1, ('no grade piece ends at', old_end / TPS)
    s, e, _, _ = item_times(doc, g[0]); retime_item(doc, g[0], s, new_end)


def track_ids_sorted(doc, tr, extra=()):
    ids = [i for i in live(doc, tr)] + [x for x in extra if x not in live(doc, tr)]
    ids = [i for i in ids if _exists(doc, i)]
    return sorted(set(ids), key=lambda x: item_times(doc, x)[0])


def _exists(doc, i):
    try: doc.raw(i); return True
    except KeyError: return False


# ---------------------------------------------------------------- 3 things masks
def board_blur_item(doc, tmpl_adj, M, log):
    """adjustment layer 0..BOARD_BLUR_END: Gaussian Blur with 5 tracked masks that wipe away left->right"""
    start, end = 0, tk(BOARD_BLUR_END)
    mt = lambda t: L.ADJ_IN + ts(t)
    rows = [r for r in M['blur'] if r['t'] < BOARD_BLUR_END]
    masks, objs = [], []
    for n, name in enumerate(['L1', 'L2a', 'L2b', 'L3a', 'L3b']):
        b = M['boxes'][name]
        x1, ycen = 540.0, 960.0                        # local path around a fixed anchor (right-middle)
        path = L.poly_pts([((x1 - b['w']) / W, (ycen - b['h'] / 2) / H), (x1 / W, (ycen - b['h'] / 2) / H),
                           (x1 / W, (ycen + b['h'] / 2) / H), ((x1 - b['w']) / W, (ycen + b['h'] / 2) / H)])
        anchor = (x1 / W, ycen / H)
        w0, w1 = BOARD_WIPES[name]
        pk, rk, swk, shk = '', '', '', ''
        for i, r in enumerate(rows):
            t = r['t']; tn = rows[i + 1]['t'] if i + 1 < len(rows) else t + 0.04
            hold = min(tn - 1 / 240.0, t + 0.04)
            x, y = r['pos'][name]; rot = r['rot'] + b['ang']
            for tt in (t, hold):
                if tt < 0: continue
                u = min(1.0, max(0.0, (tt - w0) / (w1 - w0))); u = u * u * (3 - 2 * u)
                pk += L.kf_point(mt(tt), x, y); rk += L.kf_scalar(mt(tt), rot)
                swk += L.kf_scalar(mt(tt), r['scale'] * 100 * (1 - u)); shk += L.kf_scalar(mt(tt), r['scale'] * 100)
        # inside the wipe windows sample finer (60 fps) so the reveal is smooth between source frames
        mc, mtx = L.mask_component(doc, n + 1, path, feather=16.0, anchor=anchor, pos=rows[0]['pos'][name], pos_keys=pk, rot_keys=rk, sw_keys=swk, sh_keys=shk)
        masks.append(mc); objs += mtx
    gc, gtx = L.gblur_component(doc, 3, 26.0, 'Board blur (tracked)', masks)
    objs += gtx
    nti, itx = L.adj_item(doc, tmpl_adj, start, end, [gc], name='Board blur')
    log('board blur masks: %d samples' % len(rows))
    return nti, objs + itx


def highlight_item(doc, tmpl_adj, M, log):
    s0, s1 = HL_SPAN
    start, end = tk(s0), tk(s1)
    mt = lambda t: L.ADJ_IN + ts(t) - start
    rows = M['hl']
    masks, objs = [], []
    for n, name in enumerate(['L2a', 'L2b', 'L3a', 'L3b']):
        b = M['boxes'][name]
        hh = b['h'] * 0.78
        x0, ycen = 540.0, 960.0                        # anchor left-middle: the highlight draws on left->right
        path = L.poly_pts([(x0 / W, (ycen - hh / 2) / H), ((x0 + b['w']) / W, (ycen - hh / 2) / H),
                           ((x0 + b['w']) / W, (ycen + hh / 2) / H), (x0 / W, (ycen + hh / 2) / H)])
        anchor = (x0 / W, ycen / H)
        w0, w1 = HL_WIPES[name]
        pk, rk, swk, shk = '', '', '', ''
        for i, r in enumerate(rows):
            t = r['t']
            if t < s0 - 0.05 or t > s1 + 0.05: continue
            tn = rows[i + 1]['t'] if i + 1 < len(rows) else t + 0.04
            hold = min(tn - 1 / 240.0, t + 0.04)
            for tt in (t, hold):
                if tt < s0 or tt > s1: continue
                u = min(1.0, max(0.0, (tt - w0) / (w1 - w0))); u = 1 - (1 - u) ** 3
                x, y = r['pos'][name]
                pk += L.kf_point(mt(tt), x, y); rk += L.kf_scalar(mt(tt), r['rot'] + b['ang'])
                swk += L.kf_scalar(mt(tt), r['scale'] * 100 * u); shk += L.kf_scalar(mt(tt), r['scale'] * 100)
        mc, mtx = L.mask_component(doc, n + 1, path, feather=7.0, anchor=anchor, pos=rows[0]['pos'][name], pos_keys=pk, rot_keys=rk, sw_keys=swk, sh_keys=shk)
        masks.append(mc); objs += mtx
    tc, ttx = L.tint_component(doc, 3, (150, 236, 120), 62.0, 'Board highlight (tracked)', masks)
    objs += ttx
    nti, itx = L.adj_item(doc, tmpl_adj, start, end, [tc], name='Board highlight')
    log('highlight masks')
    return nti, objs + itx


def glass_items(doc, tmpl_adj, geom, meta, log):
    """live frosted glass: Gaussian Blur on an adjustment layer under each glass card, masked to the card (per-frame reveal)"""
    out_ids, objs = [], []
    for name, g in sorted(geom.items()):
        s_seq = meta[name]['start']
        e3 = lambda u: 1 - (1 - min(1, max(0, u))) ** 3
        def sx(t):
            v = e3((t - g['tIn']) / 0.38)
            if g['tOut'] >= 0 and t >= g['tOut']: v = 1 - min(1, max(0, (t - g['tOut']) / 0.25)) ** 3
            return v
        def hh(t):
            if g['tG'] < 0: return g['h1']
            u = min(1, max(0, (t - g['tG']) / 0.30)); u = 4 * u ** 3 if u < 0.5 else 1 - (-2 * u + 2) ** 3 / 2
            return g['h1'] + (g['h2'] - g['h1']) * u
        phases = [(0.0, g['tG'] if g['tG'] >= 0 else g['dur'], g['h1'])]
        if g['tG'] >= 0: phases.append((g['tG'], g['dur'], g['h2']))
        for a, b, hp in phases:
            start, end = tk(s_seq + a), tk(s_seq + b)
            mt = lambda t: L.ADJ_IN + ts(s_seq + t) - start
            # 4-point path: Premiere's mask type here only accepts 4 vertices (an 8-point rounded rect made it blur the whole frame)
            x0n, y0n, x1n, y1n = g['x0'] / W, g['y0'] / H, (g['x0'] + g['w']) / W, (g['y0'] + hp) / H
            path = L.poly_pts([(x0n, y0n), (x1n, y0n), (x1n, y1n), (x0n, y1n)])
            anchor = (g['x0'] / W, g['y0'] / H)
            swk, shk = '', ''
            wins = [(g['tIn'], g['tIn'] + 0.38)]
            if g['tG'] >= 0: wins.append((g['tG'], g['tG'] + 0.30))
            if g['tOut'] >= 0: wins.append((g['tOut'], g['tOut'] + 0.25))
            for w0, w1 in wins:
                if w1 <= a or w0 >= b: continue
                for f in range(int(round(max(w0, a) * 60)), int(round(min(w1, b) * 60)) + 1):
                    t = f / 60.0
                    swk += L.kf_scalar(mt(t), max(0.0, sx(t)) * 100); shk += L.kf_scalar(mt(t), hh(t) / hp * 100)
            mc, mtx = L.mask_component(doc, 1, path, feather=2.0, anchor=anchor, pos=anchor, sw_keys=swk or None, sh_keys=shk or None)
            gc, gtx = L.gblur_component(doc, 3, 42.0, 'Glass blur ' + name, [mc])
            nti, itx = L.adj_item(doc, tmpl_adj, start, end, [gc], name='Glass blur ' + name)
            out_ids.append(nti); objs += mtx + gtx + itx
        log('glass %s %.2f-%.2f h %d/%d' % (name, s_seq, s_seq + g['dur'], g['h1'], g['h2']))
    return out_ids, objs


# ---------------------------------------------------------------- build
SKIP = set()


def build(src, out_path, log=print):
    doc = Doc(src)
    doc._pending_items = {}
    orig_blobs = inline_blobs(doc.txt); orig_txt = doc.txt
    seqs = {s.attrib['ObjectUID'][:8]: s for n, s in for_claude_sequences(doc)}
    meta = json.load(open(os.path.join(SCR, 'ae', 'gfx_v2_meta.json')))
    geom = json.load(open(os.path.join(V2, 'glass_geom.json')))
    M = json.load(open(os.path.join(SCR, 'track', 'masks_tt.json')))
    new_objs, rep = [], {}

    # ---- archive media (text import) + bin
    arch = {}
    uids = []
    if 'archive' not in SKIP:
        for key, (fn, w, h, fps) in ARCH_SRC.items():
            m, objs = media_objects(doc, YT + fn); arch[key] = m; new_objs += objs; uids.append(m['cpi_uid'])
        buid, btxt = bin_object(doc, 'Paula archive (v5)', uids); new_objs.append(btxt)
    Z.append_objects(doc, new_objs); new_objs = []

    held = seqs['404c5cb2']; c132_ref = at(doc, broll_track(video_tracks(doc, held), '404c5cb2'), 21.68)
    c132_mot = motion_of(doc, c132_ref)
    c132 = find_master(doc, 'A003_09181348_C132.mp4')
    for key, seq in seqs.items():
        trs = video_tracks(doc, seq); br, gr = broll_track(trs, key), grade_track(trs, key)
        r = rep[key] = {'name': seq.findtext('Name')[:30]}
        if key in TITLE_TIME: new_objs += retitle(doc, trs, key, log)
        # C137 hand-place -> C132 pouch slide
        for ad, st, src_s in SWAP_TO_C132:
            if ad != key: continue
            tid = at(doc, br, st); s0, e0, _, _ = item_times(doc, tid)
            px, py = [float(v) for v in c132_mot['Position'].split(':')]
            if key == '0991faf2': px += C132_RANPRO_SHIFT
            nti, objs = ext_item(doc, tid, c132, s0, e0, int(round(src_s * 25)) * F25, px, py, float(c132_mot['Scale']), {})
            new_objs += objs; delete_item(doc, tid); doc._pending_items.setdefault(br.attrib['ObjectUID'], []).append(nti)
            r.setdefault('swap', []).append((st, src_s, round(px, 4)))
        for ad, st, media, src_s in STOCK_SWAP:
            if ad != key: continue
            tid = at(doc, br, st); s0, e0, _, _ = item_times(doc, tid)
            tmpl = [x for x in live(doc, br) if motion_of(doc, x) and lumetri_ids(doc, x)][0]
            m = find_master(doc, media); fr = m['info']['fr']
            nti, objs = ext_item(doc, tmpl, m, s0, e0, int(round(src_s * TPS / fr)) * fr, 0.5, 0.5, 50.0, dict(STOCK_GRADE))
            new_objs += objs; delete_item(doc, tid); doc._pending_items.setdefault(br.attrib['ObjectUID'], []).append(nti)
        for ad, st, part in REMOVE:
            if ad != key: continue
            tid = at(doc, br, st); s0, e0, _, _ = item_times(doc, tid)
            extend_grade_to(doc, gr, s0, e0); delete_item(doc, tid)
        if key in LATE_TINT:
            from_s, vals = LATE_TINT[key]; kf = []
            for x in live(doc, gr):
                if item_times(doc, x)[0] / TPS >= from_s - 0.01:
                    for c in lumetri_ids(doc, x): set_lumetri(doc, c, vals, kf)
        # 1 star: washed-out pouch shot
        if key == 'cd03e189':
            tid = at(doc, br, 6.45); kf = []
            for c in lumetri_ids(doc, tid): set_lumetri(doc, c, C137_1STAR_FIX, kf)
            r['c137_fix'] = True
        # 3 questions: B-roll after "how does it work" starts later, grade stretched over the gap
        if key == C144_TRIM[0]:
            tid = at(doc, br, C144_TRIM[1]); s0, e0, _, _ = item_times(doc, tid)
            extend_grade_to(doc, gr, s0, tk(C144_TRIM[2])); retime_item(doc, tid, tk(C144_TRIM[2]), e0)
            r['c144_trim'] = C144_TRIM[1:]
        # replaced / retimed camera B-roll
        for st in ([] if 'archive' in SKIP else REPLACE_BROLL.get(key, [])):
            tid = at(doc, br, st); delete_item(doc, tid)
        for ad, st, ns, ne in RETIME_BROLL:
            if ad != key or 'archive' in SKIP: continue
            tid = at(doc, br, st); retime_item(doc, tid, tk(ns), tk(ne))
        # archive B-roll
        tmpl = [x for x in live(doc, br) if motion_of(doc, x) and lumetri_ids(doc, x)][0]
        for ad, s, e, akey, src_s, xs, zoom, label in PLAN:
            if ad != key or 'archive' in SKIP: continue
            a, b = tk(s), tk(e)
            covered = [x for x in live(doc, br) if item_times(doc, x)[0] < b and item_times(doc, x)[1] > a]
            assert not covered, ('B-roll overlap at', key, s, [item_name(doc, x) for x in covered])
            cut_grade(doc, gr, a, b, new_objs)
            px, py, sc = arch_motion(akey, xs, zoom)
            m = arch[akey]; fr = m['info']['fr']
            grade = MODERN_GRADE if (akey == 'STARS' and src_s >= 450) else ARCH_GRADE
            nti, objs = ext_item(doc, tmpl, m, a, b, int(round(src_s * TPS / fr)) * fr, px, py, sc, dict(grade))
            new_objs += objs; doc._pending_items.setdefault(br.attrib['ObjectUID'], []).append(nti)
            r.setdefault('archive', []).append((s, label))
        for ad, s, e, media, src_s, px in TT_BROLL:
            if ad != key: continue
            a, b = tk(s), tk(e)
            cut_grade(doc, gr, a, b, new_objs)
            tm = [x for x in live(doc, br) if 'C12' in item_name(doc, x) or 'C129' in item_name(doc, x)][0]
            mot = motion_of(doc, tm)
            nti, objs = ext_item(doc, tm, find_master(doc, media), a, b, int(round(src_s * 25)) * F25, px, 0.5, float(mot['Scale']), {})
            new_objs += objs; doc._pending_items.setdefault(br.attrib['ObjectUID'], []).append(nti)
            r.setdefault('broll_new', []).append((s, media[-8:]))
        Z.append_objects(doc, new_objs); new_objs = []
        for uid, ids in list(doc._pending_items.items()):
            tr = [t_ for t_ in trs if t_.attrib['ObjectUID'] == uid]
            if tr: set_track_items(doc, uid, track_ids_sorted(doc, tr[0], ids)); doc._pending_items.pop(uid)
        for t_ in (br, gr):
            set_track_items(doc, t_.attrib['ObjectUID'], track_ids_sorted(doc, t_))
        # sanity: no overlaps on B-roll / grade, and grade + B-roll never overlap
        for t_ in (br, gr):
            its = sorted(item_times(doc, x)[:2] for x in live(doc, t_))
            for (a1, b1), (a2, b2) in zip(its, its[1:]): assert b1 <= a2, ('overlap', key, a1 / TPS, b1 / TPS, a2 / TPS)
        bi = [item_times(doc, x)[:2] for x in live(doc, br)]; gi = [item_times(doc, x)[:2] for x in live(doc, gr)]
        for a1, b1 in bi:
            for a2, b2 in gi: assert b1 <= a2 or b2 <= a1, ('grade over B-roll', key, a1 / TPS, a2 / TPS)
    Z.append_objects(doc, new_objs); new_objs = []

    # ---- 3 things: powder shot focus pull + push-in
    seq = seqs['f233433f']; trs = video_tracks(doc, seq)
    if 'focus' not in SKIP:
        pid = at(doc, broll_track(trs, 'f233433f'), TT_POWDER[1])
        s0, e0, tin, vc = item_times(doc, pid)
        ch = re.search(r'<Components ObjectRef="(\d+)"', doc.raw(pid)).group(1)
        comps = chain_components(doc, ch)
        mot = [c for c in comps if '<MatchName>AE.ADBE Motion</MatchName>' in doc.raw(c)][0]
        sc_pid = re.search(r'<Param Index="1" ObjectRef="(\d+)"', doc.raw(mot)).group(1)
        sc_txt = doc.raw(sc_pid); assert '<Name>Scale</Name>' in sc_txt
        base_sc = float(re.search(r'<StartKeyframe>-?\d+,([^,]+),', sc_txt).group(1))
        doc.replace_obj(sc_pid, Z.set_keys(sc_txt, L.kf_scalar(tin, base_sc) + L.kf_scalar(tin + (e0 - s0), base_sc * 1.09)))
        bk = '%d,30.,5,0,0,0.33333333333333331,0,0.1;%d,0.,5,0,0,0.75,0,0.33333333333333331;' % (tin, tin + ts(0.42))
        gc, gtx = L.gblur_component(doc, 9, 30.0, 'Focus pull', None, blur_keys=bk)
        Z.append_objects(doc, gtx)
        doc.replace_obj(ch, re.sub(r'<Components Version="1">.*?</Components>', lambda m_: '<Components Version="1">%s\n\t\t\t</Components>' % ''.join(
            '\n\t\t\t\t<Component Index="%d" ObjectRef="%s"/>' % (i, c) for i, c in enumerate(comps + [gc])), doc.raw(ch), flags=re.S))

    # ---- 3 things: pre-zoom tracks (board blur + highlight, tracked '?')
    tmpl_adj = [x for x in live(doc, trs[1])][0]
    if 'tracks' not in SKIP:
        t_board = Z.add_track(doc, seq, 1, trs[1].attrib['ObjectUID'])
        t_q = Z.add_track(doc, seq, 2, trs[1].attrib['ObjectUID'])
        ids = []
        if 'masks' not in SKIP:
            b_id, objs = board_blur_item(doc, tmpl_adj, M, log); Z.append_objects(doc, objs)
            h_id, objs = highlight_item(doc, tmpl_adj, M, log); Z.append_objects(doc, objs)
            ids = [b_id, h_id]
        if ids: set_track_items(doc, t_board, ids)
        qm = find_by_path(doc, V2 + r'\tt_qmark.mov')
        tmpl_ov = [x for x in live(doc, broll_track(video_tracks(doc, seq), 'f233433f')) if motion_of(doc, x)][0]
        q_id, objs = overlay_item(doc, tmpl_ov, qm, tk(meta['tt_qmark']['start']), tk(meta['tt_qmark']['end']))
        Z.append_objects(doc, objs); set_track_items(doc, t_q, [q_id])
    # ---- 3 things: live glass blur under the cards (track above everything, below the overlay lanes)
    if 'glass' not in SKIP:
        trs = video_tracks(doc, seq)
        t_glass = Z.add_track(doc, seq, None, trs[-1].attrib['ObjectUID'])
        g_ids, objs = glass_items(doc, tmpl_adj, geom, meta, log); Z.append_objects(doc, objs)
        set_track_items(doc, t_glass, sorted(g_ids, key=lambda x: item_times(doc, x)[0]))

    # ---- overlays on new top tracks; captions under them disabled
    by_ad = {}
    for name, m in meta.items():
        if name == 'tt_qmark': continue
        mm = find_by_path(doc, V2 + '\\' + name + '.mov')
        by_ad.setdefault(m['ad'], []).append([name, tk(m['start']), tk(m['end']), mm])
    for name, ad, when in V1_OVER:
        trs = video_tracks(doc, seqs[ad])
        if isinstance(when, tuple):
            tid = at(doc, broll_track(trs, ad), when[1]); s0, e0, _, _ = item_times(doc, tid)
        else: s0, e0 = tk(when), None
        mm = find_by_path(doc, MG + r'\gfx_v1' + '\\' + name + '.mov'); d = mm['info']['dur']
        e1 = s0 + d if e0 is None else min(e0, s0 + d)
        by_ad.setdefault(ad, []).append([name, s0, e1, mm])
    # 1 star: fixed stars replace the v3 stars (old clip disabled, kept)
    stars_old = [x for t_ in video_tracks(doc, seqs['cd03e189']) for x in live(doc, t_) if 'stars_1of5_alpha' in item_name(doc, x)]
    for x in stars_old: L.disable_item(doc, x); s_, e_, _, _ = item_times(doc, x)
    st2 = find_by_path(doc, MG + r'\stars_1of5_v2_alpha.mov')
    by_ad['cd03e189'].append(['stars_v2', s_, e_, st2, (0.5, 1150 / 1920.0)])
    for ad, lst in by_ad.items():
        seq = seqs[ad]; lst.sort(key=lambda x: x[1])
        for a_, b_ in zip(lst, lst[1:]):
            if 0 < a_[2] - b_[1] <= tk(0.12): a_[2] = b_[1]
        lanes = []
        for it in lst:
            for ln in lanes:
                if ln[-1][2] <= it[1]: ln.append(it); break
            else: lanes.append([it])
        trs = video_tracks(doc, seq); tmpl_tr = trs[-1].attrib['ObjectUID']
        tmpl = [x for x in live(doc, broll_track(trs, ad)) if motion_of(doc, x)][0]
        for ln in lanes:
            uid = Z.add_track(doc, seq, None, tmpl_tr); ids = []
            for it in ln:
                name, s0, e1, mm = it[:4]
                nti, objs = overlay_item(doc, tmpl, mm, s0, e1)
                if len(it) > 4:                               # stars: positioned like v3 (y 1150)
                    objs = [re.sub(r'(<Name>Position</Name>.*?<StartKeyframe>-?\d+,)[^,]+', lambda m_: m_.group(1) + '%s:%s' % (repr(it[4][0]), repr(it[4][1])), o, count=1, flags=re.S) if '<Name>Position</Name>' in o else o for o in objs]
                Z.append_objects(doc, objs); ids.append(nti)
            set_track_items(doc, uid, ids)
        n_dis = 0
        wins = [(s0, e1) for name, s0, e1, *_ in lst if name not in NO_CAPTION_DISABLE and name != 'stars_v2']
        for ctr in caption_tracks(doc, seq):
            for cid, cs, ce in caption_items(doc, ctr):
                mid = (cs + ce) / 2
                if any(a <= mid <= b for a, b in wins) and 'disable' not in SKIP:
                    if L.disable_item(doc, cid): n_dis += 1
        rep[ad]['overlays'] = len(lst); rep[ad]['lanes'] = len(lanes); rep[ad]['captions_disabled'] = n_dis
    for k, r in rep.items(): log('%-9s %s' % (k, {a: b for a, b in r.items() if a != 'name'}))
    extra = dict(orig_blobs); extra.update(Z.T['blobs']); extra.update(Z.NEW_BLOBS)
    doc.txt, n = Z.normalize_blobs(doc.txt, extra)
    doc.txt, n2 = normalize_text_blobs(doc.txt, orig_txt)
    log('blob fixes %d, caption text blob fixes %d' % (n, n2))
    open(out_path + '.xml', 'w', encoding='utf-8', newline='\n').write(doc.txt)
    with open(out_path + '.xml', 'rb') as f, gzip.open(out_path, 'wb') as g: g.write(f.read())
    return rep


if __name__ == '__main__':
    SKIP.update(a[2:] for a in sys.argv[3:] if a.startswith('--'))
    build(sys.argv[1], sys.argv[2])
