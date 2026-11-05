"""SFX cue sheets for the other 7 ads, generated from each overlay's own animation spec (same rules as the approved
3 things pass): pops on main caption words (5 rotating layered variants), ticks on kickers, counter ticks + lock on
numbers, rising pops on VITAMINS/MINERALS/NUTRIENTS, card/headline arrivals, marker strokes on highlights,
shimmer on the title, a fixed 'brand sting' on every code card, crowd bed under archive race footage.
Writes cues_all.json; offline mix check per ad."""
import os, sys, json, re
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import atools as A
from analyze_sfx import read_wav

AE = os.path.join(HERE, '..', 'ae')
KIT_DIR = r"C:\VISION\IMMUFIX\repair\ENCODED RUSHES\Audio\SFX kit"
SR = 48000
VOICE = -17.5          # dialogue loudness after gain staging (stereo LUFS)
SYNC = 0.010
SHORT = {'348e0ba6': 'i52', '404c5cb2': 'hr', '664b35b2': 'ps', '0991faf2': 'rp', 'cd03e189': 's1', '974102f7': 'q3', '593f11c4': 'sw'}
DLG_GAIN = {'348e0ba6': -1.8, '404c5cb2': 8.1, '974102f7': 1.9, '593f11c4': 2.5}
WHITE = RED = None
V1 = {   # v1 overlay specs (from gfx_v1.jsx)
    'i52_powders': ('cap', dict(kick=[['PROTEIN']], kIn=0.56, mains=[['POWDERS', 0.86]], strike=1.02)),
    'i52_pills': ('cap', dict(kick=[['VITAMIN']], kIn=0.0, mains=[['PILLS', 0.3]], strike=0.56)),
    'i52_shakes': ('cap', dict(kick=[['GREEN']], kIn=0.08, mains=[['SHAKES', 0.36]], strike=0.62)),
    's1_pouch': ('cap', dict(kick=[['JUST ONE']], kIn=0.42, mains=[['POUCH', 0.76]], strike=-1)),
    's1_pills': ('cap', dict(kick=[['A'], ['MULTITUDE'], ['OF']], kIn=0.02, mains=[['PILLS', 0.82], ['SUPPLEMENTS', 1.42]], strike=-1)),
    's1_scoop': ('cap', dict(kick=[['ONE SCOOP']], kIn=0.02, mains=[['A DAY', 0.56]], strike=-1)),
    's1_water': ('cap', dict(kick=[['MIXED WITH']], kIn=0.0, mains=[['WATER', 0.40]], strike=-1)),
    'sw_1998': ('counter', dict(a=0.04, b=0.62, tSub=0, sub='')),
    'hr_17': ('counter', dict(a=0.1, b=0.55, tSub=0.5, sub='YEARS')),
}
HERO_LOCK = {'hr_17', 'rp_wr', 'sw_1998'}          # numbers that also get a low boom
ARCHIVE = ('Paula Radcliffe', 'Thank you Paula', 'Best of motivation', 'Young Paula', '1998 IAAF')
NO_CROWD = {('664b35b2', 9.25), ('664b35b2', 10.45), ('664b35b2', 11.62), ('664b35b2', 12.62), ('593f11c4', 12.35)}   # lifestyle montage / training


def specs():
    sp = {}
    for fn in ('gfx_v2_specs.json', 'gfx_v3_specs.json'):
        for kind, s in json.load(open(os.path.join(AE, fn))): sp[s['name']] = (kind, s)
    sp.update(V1)
    return sp


class Rot:
    def __init__(self, names): self.names = names; self.i = 0; self.last = None
    def next(self):
        n = self.names[self.i % len(self.names)]; self.i += 1
        if n == self.last: n = self.names[self.i % len(self.names)]; self.i += 1
        self.last = n; return n


def events_for(key, ad, sp):
    ev = []; pops = Rot(['POP1', 'POP2', 'POP3', 'POP4', 'POP5']); ticks = Rot(['TICK1', 'TICK2', 'TICK3'])
    swish = Rot(['SWISH1', 'SWISH2', 'SWISH3']); glass = Rot(['GLASS1', 'GLASS2', 'GLASS3']); marks = Rot(['MARK1', 'MARK2'])
    def add(t, name, rel, what, at_start=False): ev.append(dict(t=round(t, 4), name=name, rel=rel, what=what, at_start=at_start))
    def count(t0, t1, what):
        d = t1 - t0; nm = 'COUNT_05' if d <= 0.6 else ('COUNT_09' if d <= 0.95 else 'COUNT_10')
        add(t0, nm, -13, what + ' counting', at_start=True)
    for o in ad['overlays']:
        S = o['start']; nm = o['name']; base = os.path.splitext(nm)[0]
        if nm.startswith('Title'):
            add(S + 0.15, 'SHIM1', -14, 'title in'); continue
        if nm.startswith('Code'):
            add(S + 0.08, 'SWISH1', -11, 'code card in'); add(S + 0.30, 'LOCK2', -9, 'code card lands (brand sting)'); continue
        if base.startswith('stars_1of5'):
            add(S + 0.07, 'SWISH2', -15, 'star outlines draw')
            add(S + 0.46, 'GLASS2', -9, 'first star lights'); add(S + 0.50, 'SHIM1', -15, 'star sparkle')
            for k in range(4): add(S + 0.64 + 0.08 * k, ['TICK1', 'TICK3'][k % 2], -15, 'star %d fails' % (k + 2))
            continue
        if base not in sp: continue
        kind, s = sp[base]
        if kind == 'cap':
            beats = s.get('beats') or [dict(kick=s.get('kick', []), kIn=s.get('kIn', 0), mains=s.get('mains', []), out=-1)]
            for b in beats:
                mains = b.get('mains', [])
                first_main = min([m[1] for m in mains] or [9])
                if b.get('kick') and first_main - b.get('kIn', 0) >= 0.35 and not (s.get('strike', -1) and s.get('strike', -1) > 0):
                    add(S + b['kIn'], ticks.next(), -14, base + ' kicker')
                for m in mains:
                    if len(m) > 2 and isinstance(m[2], dict):
                        c = m[2]; count(S + c['a'], S + c['b'], base + ' ' + m[0]); add(S + c['b'], 'LOCK2', -10, base + ' ' + m[0] + ' lands')
                        if base in HERO_LOCK: add(S + c['b'], 'BOOM2', -14, base + ' weight')
                    else:
                        add(S + m[1], pops.next(), -7, base + ' ' + m[0])
            if s.get('strike', -1) and s.get('strike', -1) > 0: add(S + s['strike'], 'SWISH2', -13, base + ' strike-through')
            if s.get('below'): add(S + s['below'][1], ticks.next(), -14, base + ' ' + s['below'][0])
        elif kind == 'stack':
            for (w, t, _), nm2, rel in zip(s['words'], ['POP1', 'POP1_up2', 'POP1_up4'], [-7, -6.5, -6]): add(S + t, nm2, rel, base + ' ' + w)
        elif kind == 'counter':
            count(S + s['a'], S + s['b'], base); add(S + s['b'], 'LOCK2', -10, base + ' lands')
            if base in HERO_LOCK: add(S + s['b'], 'BOOM2', -14, base + ' weight')
            if s.get('tSub', 0) and s['tSub'] > s['b'] + 0.15: add(S + s['tSub'], ticks.next(), -14, base + ' sub line')
        elif kind == 'window':
            add(S + s['tK'], ticks.next(), -14, base + ' kicker'); count(S + s['a'], S + s['b'], base)
            add(S + s['b'], pops.next(), -8, base + ' 20'); add(S + s['t30'], pops.next(), -8, base + ' 30')
        elif kind == 'card':
            add(S + 0.10, swish.next(), -11, base + ' question card in'); add(S + 0.25, glass.next(), -13, base + ' card lands')
        elif kind == 'article':
            add(S + 0.10, 'SWISH3', -11, base + ' headline card in')
            for h in s['hl']: add(S + (h[4] + h[5]) / 2, marks.next(), -12, base + ' highlight')
        elif kind == 'flash':
            add(S + 0.11, 'WHOOSH3', -12, 'white flash')
    # crowd bed under archive race footage (merged runs)
    runs = []
    for o in ad['overlays']:
        if o['name'].startswith(ARCHIVE) and (key, round(o['start'], 2)) not in NO_CROWD:
            if runs and o['start'] - runs[-1][1] < 0.05: runs[-1][1] = o['end']
            else: runs.append([o['start'], o['end']])
    for a, b in runs: ev.append(dict(t=a, name='CROWD1', rel=-19, what='crowd under archive %.2f-%.2f' % (a, b), at_start=True, end=b))
    if key == '593f11c4':   # the music jumps to its climax here
        add(14.30, 'WHOOSH1', -8, 'music lift into the win'); add(14.30, 'BOOM1', -10, 'win hit')
    # declutter: a tick never sits within 0.15 s of another accent
    acc = [e for e in ev if not e['name'].startswith(('TICK', 'COUNT', 'CROWD'))]
    ev = [e for e in ev if not (e['name'].startswith('TICK') and any(abs(a['t'] - e['t']) < 0.15 for a in acc))]
    return ev


def place(kit, ev, L):
    out = []
    for e in ev:
        k = kit[e['name']]
        t = e['t'] + SYNC
        start = t if e['at_start'] else t - k['peak_t']
        end = min(e.get('end', start + k['dur']), start + k['dur'], L)
        skip = max(0.0, -start); start = max(0.0, start)
        if end - start < 0.02: continue
        out.append(dict(e, file=k['file'], start=round(start, 4), end=round(end, 4), skip=round(skip, 4), gain_db=round(VOICE + e['rel'] - k['m_max'], 1)))
    return sorted(out, key=lambda x: x['start'])


def lanes(evs, n_lanes):
    """crowd beds get their own lane (index n_lanes, mapped to the track after the last SFX lane used); other sounds
    share n_lanes lanes. When none is free, trim the lane whose clip can lose its tail (never closer than 0.12 s
    after its hit), else drop the new sound (reported)."""
    kit = {k['name']: k for k in json.load(open(os.path.join(HERE, 'kit.json')))}
    ends = [-1.0] * n_lanes; last = [None] * n_lanes; out = []
    for e in evs:
        if e['name'].startswith('CROWD'):
            e['lane'] = 'crowd'; out.append(e); continue
        free = [i for i in range(n_lanes) if e['start'] >= ends[i] + 0.01]
        if free:
            i = free[0]
        else:
            ok = [j for j in range(n_lanes) if last[j]['start'] + kit[last[j]['name']]['peak_t'] + 0.12 <= e['start'] - 0.005]
            if not ok:
                print('   dropped %s at %.2f (%s): lanes busy' % (e['name'], e['t'], e['what'])); continue
            i = min(ok, key=lambda j: ends[j])
            last[i]['end'] = round(e['start'] - 0.005, 4); e['trimmed_prev'] = True
        e['lane'] = i; ends[i] = e['end']; last[i] = e; out.append(e)
    used = max([e['lane'] for e in out if e['lane'] != 'crowd'] + [0]) + 1
    for e in out:
        if e['lane'] == 'crowd': e['lane'] = used
    return out


def load(fn):
    a, sr, _, _ = read_wav(os.path.join(KIT_DIR, fn)); return a[:, :2]


if __name__ == '__main__':
    ads = json.load(open(os.path.join(HERE, 'ads_info.json')))
    kit = {k['name']: k for k in json.load(open(os.path.join(HERE, 'kit.json')))}
    music = {(m['key'], m['tag']): m for m in json.load(open(os.path.join(HERE, 'music_edits.json')))}
    sp = specs(); allc = {}
    for key, short in SHORT.items():
        ad = ads[key]; L = ad['L']
        ev = place(kit, events_for(key, ad, sp), L)
        ev = lanes(ev, 3)
        mus = music[(key, 'A')]
        # offline check: dialogue (with planned gain) + SFX + baked music
        dlg = np.load(os.path.join(HERE, 'dlg_%s.npy' % key)).astype(np.float64) * 10 ** (DLG_GAIN.get(key, 0) / 20)
        n = int(L * SR); d2 = np.repeat(np.pad(dlg, (0, max(0, n - len(dlg))))[:n, None], 2, axis=1)
        sfx = np.zeros((n, 2))
        for e in ev:
            x = load(e['file']); i0 = int(round(e['start'] * SR)); s0 = int(round(e['skip'] * SR)); m = int(round((e['end'] - e['start']) * SR))
            seg = x[s0:s0 + m] * 10 ** (e['gain_db'] / 20); sfx[i0:i0 + len(seg)] += seg[:n - i0]
        mu, _ = A.load_wav(os.path.join(r"C:\VISION\IMMUFIX\repair\ENCODED RUSHES\Audio\Music\Ad edits", mus['file'])) if False else (None, None)
        a, sr, _, _ = read_wav(os.path.join(r"C:\VISION\IMMUFIX\repair\ENCODED RUSHES\Audio\Music\Ad edits", mus['file'])); mu = a[:n, :2]
        mix = d2 + sfx + np.pad(mu, ((0, n - len(mu)), (0, 0)))
        print('%-3s L %.2f  %2d SFX (%d trims)  voice %.1f  music %.1f  sfx %.1f  MIX %.1f LUFS  %.1f dBTP' % (
            short, L, len(ev), sum(1 for e in ev if e.get('trimmed_prev')), A.lufs(d2, SR), A.lufs(mu, SR), A.lufs(sfx, SR), A.lufs(mix, SR), A.true_peak_db(mix)))
        allc[key] = dict(short=short, L=L, dialog_gain_change_db=DLG_GAIN.get(key, 0.0), music=mus['file'], events=ev)
    json.dump(allc, open(os.path.join(HERE, 'cues_all.json'), 'w'), indent=1)
    for key, c in allc.items():
        print(c['short'], ' '.join('%.2f:%s' % (e['t'], e['name']) for e in c['events']))
