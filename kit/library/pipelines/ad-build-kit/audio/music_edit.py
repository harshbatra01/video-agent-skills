"""Bar-accurate music edits for each ad, baked to WAV (48 kHz / 24-bit, exactly the ad length):
- the track's final chord lands on the code card (or the last line), the rest is either a clean late start or
  the track's intro + one cut on a downbeat chosen by harmonic (chroma) and loudness match, aligned to a visual moment;
- level: music sits LU_UNDER below the voice, a slow leveler keeps it within -5/+2 LU of that, +3 dB lift in speech gaps."""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import atools as A
from track_an import analyze, load, SR
from bake_kit import write24

MUSIC = r"C:\VISION\IMMUFIX\repair\ENCODED RUSHES\Audio\Music"
OUT = os.path.join(MUSIC, "Ad edits")
VOICE_LUFS = -17.5            # every ad's dialogue is normalised to this (stereo)
LU_UNDER = 14.0


def bar_chroma(x, d0, bar, nb):
    out = []
    for k in range(nb):
        s = int((d0 + k * bar) * SR); e = int((d0 + (k + 1) * bar) * SR)
        seg = x[s:e]
        sp = np.abs(np.fft.rfft(seg * np.hanning(len(seg))))
        f = np.fft.rfftfreq(len(seg), 1 / SR); ok = (f > 55) & (f < 2000)
        pc = (np.round(12 * np.log2(f[ok] / 261.63)) % 12).astype(int)
        c = np.bincount(pc, weights=sp[ok], minlength=12); out.append(c / (np.linalg.norm(c) + 1e-9))
    return np.array(out)


def plan(an, chroma, L, e_target, window, hints, force_cut=None):
    d0, bar, eb = an['d0'], an['bar'], an['E_bar']
    D = lambda k: d0 + k * bar
    db = np.array(an['bar_db']); best = None
    lo, hi = window
    def consider(c):
        nonlocal best
        if best is None or c['cost'] < best['cost']: best = c
    # (1) no cut: start inside the track so the final chord lands on target
    for s in (range(0, eb) if force_cut is None else []):
        A0 = D(s); e_seq = D(eb) - A0
        for shift in [e_seq - e_target]:
            A_ = A0 + shift; es = D(eb) - A_
            if not (lo <= es <= hi) or A_ < -0.6: continue
            cost = 0.25 + (0.0 if (eb - s) % 4 == 0 else 0.12) + 0.03 * max(0, db[s] + 6) + 0.2 * abs(es - e_target)
            if s == 0 and A_ <= d0 + 0.05: cost -= 0.25          # it really is the track's own start
            consider(dict(kind='nocut', A=A_, s=s, E_seq=es, cost=cost))
    # (2) intro + one cut: bars [start .. m) then [j .. end], j = eb - n
    for n in range(2, 17):
        j = eb - n
        for m in range(2, j - 1):
            c0 = D(m)
            dist = (1 - chroma[m] @ chroma[j]) + 0.5 * (1 - chroma[m - 1] @ chroma[j - 1])
            jump = abs(db[j] - db[m])
            base = 1.6 * dist + 0.025 * jump + (0 if n % 4 == 0 else 0.12) + (0 if m % 4 == 0 else 0.08)
            opts = [(c0 + n * bar - e_target, 0.0)]                # put the final chord exactly on target
            for h, w in hints: opts.append((c0 - h, -0.15 * w))      # or put the cut exactly on a visual moment
            if force_cut is not None: opts = [(c0 - force_cut, 0.0)]
            for A_, bonus in opts:
                if A_ < -0.6 or A_ > d0 + 1.5: continue
                es = c0 + n * bar - A_
                if not (lo <= es <= hi): continue
                consider(dict(kind='cut', A=A_, m=m, j=j, n=n, cut_seq=c0 - A_, E_seq=es, dist=round(dist, 3), jump=round(jump, 1),
                              cost=base + bonus + 0.2 * abs(es - e_target)))
    return best


def render(x2, an, p, L):
    """x2: stereo track. returns the raw edit (no gain) of length L"""
    n = int(round(L * SR)); out = np.zeros((n, 2))
    d0, bar = an['d0'], an['bar']
    def put(seq_t0, src_t0, src_t1):
        i = int(round(seq_t0 * SR)); s0 = int(round(src_t0 * SR)); s1 = int(round(src_t1 * SR))
        if s0 < 0: i -= s0; s0 = 0
        seg = x2[s0:s1]; k = min(len(seg), n - i)
        if k > 0 and i >= 0: out[i:i + k] += seg[:k]
    if p['kind'] == 'nocut':
        put(-p['A'] if p['A'] < 0 else 0.0, max(0.0, p['A']), max(0.0, p['A']) + L)
        fade_in = 0.35 if p['A'] > d0 + 0.05 else 0.01
    else:
        cut = p['cut_seq']; xf = 0.03
        src_cut_a = d0 + p['m'] * bar; src_cut_b = d0 + p['j'] * bar
        a = np.zeros_like(out); b = np.zeros_like(out)
        def putto(buf, seq_t0, src_t0, src_t1):
            i = int(round(seq_t0 * SR)); s0 = int(round(src_t0 * SR)); s1 = int(round(src_t1 * SR))
            if s0 < 0: i -= s0; s0 = 0
            seg = x2[s0:s1]; k = min(len(seg), n - i)
            if k > 0: buf[i:i + k] += seg[:k]
        putto(a, max(0.0, -p['A']), max(0.0, p['A']), src_cut_a + xf)
        putto(b, cut - xf, src_cut_b - xf, src_cut_b - xf + (L - cut + xf))
        t = np.arange(n) / SR
        w = np.clip((t - (cut - xf)) / xf, 0, 1); ga = np.cos(w * np.pi / 2); gb = np.sin(w * np.pi / 2)
        out = a * ga[:, None] + b * gb[:, None]
        fade_in = 0.35 if p['A'] > d0 + 0.05 else 0.01
    fi = int(fade_in * SR); out[:fi] *= np.linspace(0, 1, fi)[:, None]
    fo = int(0.5 * SR); out[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
    return out


def gain_curve(edit, dlg_mono, L, target_lufs):
    n = len(edit); t = np.arange(n) / SR
    # slow leveler around the target
    tt, st = A.short_term(edit, SR, win=3.0, hop=0.1)
    st = np.where(st < -70, target_lufs - 5, st)
    desired = np.clip(st, target_lufs - 5, target_lufs + 2)
    g = desired - st
    k = 15; g = np.convolve(np.pad(g, (k, k), mode='edge'), np.ones(2 * k + 1) / (2 * k + 1), mode='valid')
    gl = np.interp(t, tt, g)
    # speech gaps lift
    hop = int(0.01 * SR); w = int(0.03 * SR)
    env = np.array([np.sqrt(np.mean(dlg_mono[i:i + w] ** 2) + 1e-12) for i in range(0, len(dlg_mono) - w, hop)])
    edb = 20 * np.log10(env); thr = np.percentile(edb, 95) - 25
    act = edb > thr
    gap = np.zeros(len(act))
    i = 0
    while i < len(act):
        if not act[i]:
            j = i
            while j < len(act) and not act[j]: j += 1
            if (j - i) * 0.01 >= 0.40:
                a0 = i + 10; a1 = j - 15
                if a1 > a0: gap[a0:a1] = 1.0
            i = j
        else: i += 1
    lift = np.convolve(gap, np.ones(25) / 25, mode='same') * 3.0
    gt = np.interp(t, np.arange(len(lift)) * 0.01, lift, right=lift[-1] if len(lift) else 0)
    return gl + gt


def make(key, short, L, e_target, window, hints, track_file, bpm, tag, dlg_gain_db=0.0, force_cut=None):
    path = os.path.join(MUSIC, track_file)
    an = analyze(path, bpm)
    x2 = load(path); xm = x2.mean(axis=1)
    ch = bar_chroma(xm, an['d0'], an['bar'], an['n_bars'])
    p = plan(an, ch, L, e_target, window, hints, force_cut)
    raw = render(x2, an, p, L)
    dlg = np.load(os.path.join(HERE, 'dlg_%s.npy' % key)).astype(np.float64) * 10 ** (dlg_gain_db / 20)
    dlg = np.pad(dlg, (0, max(0, len(raw) - len(dlg))))[:len(raw)]
    target = VOICE_LUFS - LU_UNDER
    # base gain from the music's loudness over the whole edit, then shape
    base = target - A.lufs(raw, SR)
    g = gain_curve(raw * 10 ** (base / 20), dlg, L, target) + base
    out = raw * (10 ** (g / 20))[:, None]
    pk = np.abs(out).max()
    if pk > 0.89: out *= 0.89 / pk
    os.makedirs(OUT, exist_ok=True)
    fn = 'IMX_MUSIC_%s_%s_%s.wav' % (short, tag, os.path.splitext(track_file)[0].replace('ES_', '').split(' - ')[0].split(' (')[0].replace("'", '').replace(' ', ''))
    write24(os.path.join(OUT, fn), out)
    voice_st = A.lufs(np.repeat(dlg[:, None], 2, axis=1), SR)
    rel = A.lufs(out, SR) - voice_st
    info = dict(key=key, short=short, tag=tag, file=fn, track=track_file, bpm=an['bpm'], bar=round(an['bar'], 4), plan={k: (round(v, 3) if isinstance(v, float) else v) for k, v in p.items()},
                music_lufs=round(A.lufs(out, SR), 1), voice_lufs=round(voice_st, 1), rel=round(rel, 1), L=L)
    print('%-3s %s %-34s %s  E at %.2f (target %.2f)  music %.1f LUFS = %+.1f LU vs voice  %s' % (
        short, tag, track_file[3:37], ('cut %.2f (bars %d->%d, chroma %.2f, jump %.0f dB)' % (p['cut_seq'], p['m'], p['j'], p['dist'], p['jump'])) if p['kind'] == 'cut' else 'no cut, starts %.2fs in' % p['A'],
        p['E_seq'], e_target, info['music_lufs'], rel, fn))
    return info


ADS = {
    # key: (short, L, E target, window, hints [(t, weight)], [(file, bpm)...] main first, dialogue gain change dB)
    'f233433f': ('tt', 48.25, 47.17, (46.6, 47.7), [(38.033, 2), (31.733, 1), (42.133, 1), (25.267, 1), (19.05, 1), (14.40, 1)],
                 [("ES_The Key - Dream Cave.wav", 105), ("ES_Unknown Phenomenon - Dream Cave.wav", 99), ("ES_Organic Foundation - Jay Varton.wav", 95)], 0.0),
    '974102f7': ('q3', 45.283, 42.70, (42.4, 43.2), [(39.85, 1), (37.0, 1), (32.183, 1), (29.55, 2), (24.2, 1), (21.333, 1), (18.55, 2), (13.5, 1), (10.95, 1)],
                 [("ES_From Tree to Paper - Clarence Reed.wav", 100), ("ES_Gravel Road Mystery - Kikoru.wav", 122)], 1.9),
    'cd03e189': ('s1', 24.10, 20.733, (20.45, 21.2), [(19.317, 1), (17.067, 1), (14.983, 1), (6.45, 1), (3.8, 1)],
                 [("ES_What Happens in the Park - Claude Signet.wav", 115), ("ES_Gossip Talk - Arthur Benson.wav", 90)], 0.0),
    '348e0ba6': ('i52', 30.167, 26.80, (26.5, 27.3), [(21.283, 1), (18.967, 1), (17.05, 1), (15.967, 1), (13.517, 1), (11.117, 1), (9.083, 1)],
                 [("ES_Don't Waste My Time (Instrumental Version) - Victor Lundberg.wav", 90), ("ES_Eventually (Instrumental Version) - Arch Tremors.wav", 105)], -1.8),
    '664b35b2': ('ps', 29.883, 26.517, (26.2, 27.0), [(24.083, 1), (20.717, 1), (15.483, 1), (13.567, 1), (9.25, 1), (5.933, 1)],
                 [("ES_Say It (Instrumental Version) - Elijah N.wav", 108), ("ES_Making Me Feel Alright (Instrumental Version) - Caro Be & Leviate.wav", 110)], 0.0),
    '404c5cb2': ('hr', 29.283, 28.283, (27.9, 28.7), [(26.767, 1), (23.55, 1), (21.683, 1), (19.367, 1), (16.317, 1), (14.3, 1), (11.317, 1), (6.667, 1)],
                 [("ES_The Legend Begins - Christoffer Moe Ditlevsen.wav", 110), ("ES_Colossus - Dream Cave.wav", 105)], 8.1),
    '0991faf2': ('rp', 29.20, 26.10, (25.8, 26.6), [(24.783, 1), (22.3, 1), (19.75, 1), (15.617, 1), (13.25, 1), (8.183, 1), (6.683, 1)],
                 [("ES_Boost - Dream Cave.wav", 88), ("ES_Among the Clouds - Helmut Schenker.wav", 110)], 0.0),
    '593f11c4': ('sw', 24.833, 22.283, (21.8, 23.1), [(14.3, 3), (12.35, 1), (17.2, 1), (9.033, 1), (6.217, 1)],
                 [("ES_The Hour of Truth - Christoffer Moe Ditlevsen.wav", 117), ("ES_I'll Fly Far Away - Dream Cave.wav", 83)], 2.5),
}

FORCE = {'593f11c4': 14.30}   # Secret weapon: subdued intro, the climax lands on 'Three months later I won'

if __name__ == '__main__':
    want = sys.argv[1:] or list(ADS)
    res = []
    for key in want:
        short, L, et, win, hints, tracks, dg = ADS[key]
        for k, (f, bpm) in enumerate(tracks):
            res.append(make(key, short, L, et, win, hints, f, bpm, 'ABC'[k], dg, FORCE.get(key)))
    old = {}
    pj = os.path.join(HERE, 'music_edits.json')
    if os.path.exists(pj): old = {(r['key'], r['tag']): r for r in json.load(open(pj))}
    for r in res: old[(r['key'], r['tag'])] = r
    json.dump(list(old.values()), open(pj, 'w'), indent=1)
