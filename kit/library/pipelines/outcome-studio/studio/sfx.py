"""sfx: our own sound effects, synthesised (no licence questions), mixed to a cue list and written as a WAV for render.Studio.video.

Cue: (time_s, name, gain_db). Names: tick, tock, whoosh, hit, riser, pop, click, blip, ratchet (one wheel click), sub (low boom),
     ding, thud, thunder, crack (lightning zap), chime (weather bumper), beep, beephi (start lights), glitch, type.
Mix target: about -16 LUFS-ish peak-safe (we normalise peaks to -3 dBFS); leave room for a trending sound added in-app.
"""
import os, wave
import numpy as np

SR = 48000


def _env(n, a=0.002, r=0.08):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / max(r, 1e-4))
    return e


def _noise(n, seed=0):
    return np.random.default_rng(seed).standard_normal(n)


def _lp(x, k=8):
    """cheap low-pass: moving average"""
    if k <= 1: return x
    c = np.cumsum(np.insert(x, 0, 0.0)); y = (c[k:] - c[:-k]) / k
    return np.concatenate([y, np.zeros(len(x) - len(y))])


def sound(name, seed=0):
    if name == 'tick':
        n = int(.05 * SR); t = np.arange(n) / SR
        return (np.sin(2 * np.pi * 2400 * t) * .6 + _noise(n, seed) * .25) * _env(n, .0005, .012)
    if name == 'tock':
        n = int(.07 * SR); t = np.arange(n) / SR
        return (np.sin(2 * np.pi * 1400 * t) * .7 + _noise(n, seed) * .15) * _env(n, .0005, .02)
    if name == 'click':
        n = int(.025 * SR); return _noise(n, seed) * _env(n, .0002, .004) * .8
    if name == 'ratchet':
        n = int(.03 * SR); t = np.arange(n) / SR
        return (_noise(n, seed) * .5 + np.sin(2 * np.pi * 3200 * t) * .3) * _env(n, .0002, .006)
    if name == 'pop':
        n = int(.09 * SR); t = np.arange(n) / SR; f = 900 * np.exp(-t * 25) + 300
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, .001, .03) * .7
    if name == 'blip':
        n = int(.16 * SR); t = np.arange(n) / SR
        return (np.sin(2 * np.pi * 1320 * t) * (t < .07) + np.sin(2 * np.pi * 1760 * t) * (t >= .07)) * _env(n, .002, .09) * .5
    if name == 'whoosh':
        n = int(.45 * SR); t = np.arange(n) / SR
        x = _noise(n, seed); bands = [_lp(x, k) for k in (40, 18, 8, 4)]
        w = np.linspace(0, 1, n); y = sum(b * np.clip(1 - abs(w * 3 - i), 0, 1) for i, b in enumerate(bands))
        return y * np.sin(np.pi * np.clip(t / .45, 0, 1)) ** 2 * 1.6
    if name == 'riser':
        n = int(1.2 * SR); t = np.arange(n) / SR; f = 180 + 900 * (t / 1.2) ** 2
        return (np.sin(2 * np.pi * np.cumsum(f) / SR) * .35 + _lp(_noise(n, seed), 6) * .4) * (t / 1.2) ** 2
    if name == 'hit':
        n = int(.6 * SR); t = np.arange(n) / SR; f = 110 * np.exp(-t * 8) + 45
        body = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, .001, .22)
        crack = _lp(_noise(n, seed), 2) * _env(n, .0005, .03) * .6
        return body * .9 + crack
    if name == 'sub':
        n = int(.9 * SR); t = np.arange(n) / SR; f = 60 * np.exp(-t * 2) + 30
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, .002, .35)
    if name == 'ding':
        n = int(.9 * SR); t = np.arange(n) / SR
        return (np.sin(2 * np.pi * 1568 * t) + .5 * np.sin(2 * np.pi * 2352 * t) + .25 * np.sin(2 * np.pi * 3136 * t)) * _env(n, .001, .25) * .45
    if name == 'thud':
        n = int(.35 * SR); t = np.arange(n) / SR; f = 140 * np.exp(-t * 18) + 55
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, .001, .09) + _lp(_noise(n, seed), 3) * _env(n, .0005, .012) * .5
    if name == 'thunder':
        n = int(2.4 * SR); t = np.arange(n) / SR
        rumble = _lp(_noise(n, seed), 60) * 6 * np.minimum(1, t / .05) * np.exp(-t / .9) * (1 + .5 * np.sin(2 * np.pi * 3.3 * t))
        crack = _lp(_noise(n, seed + 1), 2) * _env(n, .001, .05) * .8
        return rumble + crack
    if name == 'crack':
        n = int(.4 * SR); t = np.arange(n) / SR
        zap = _noise(n, seed) * .6 * (np.sin(2 * np.pi * 60 * t) > 0) * _env(n, .0005, .08)
        return zap + np.sin(2 * np.pi * np.cumsum(900 * np.exp(-t * 12) + 80) / SR) * _env(n, .001, .12) * .6
    if name == 'chime':
        out = np.zeros(int(1.2 * SR))
        for k, fr in enumerate((784, 988, 1175)):
            n = int(.7 * SR); t = np.arange(n) / SR
            s = (np.sin(2 * np.pi * fr * t) + .3 * np.sin(2 * np.pi * 2 * fr * t)) * _env(n, .004, .22) * .45
            a = int(k * .14 * SR); out[a:a + n] += s[:len(out) - a]
        return out
    if name in ('beep', 'beephi'):
        fr = 880 if name == 'beep' else 1760; n = int((.18 if name == 'beep' else .45) * SR); t = np.arange(n) / SR
        return np.sign(np.sin(2 * np.pi * fr * t)) * .25 * _env(n, .002, .12 if name == 'beep' else .3)
    if name == 'glitch':
        n = int(.22 * SR); t = np.arange(n) / SR
        sq = np.sign(np.sin(2 * np.pi * (220 + 880 * (np.floor(t * 40) % 4)) * t))
        return (sq * .35 + _noise(n, seed) * .3) * (np.floor(t * 60) % 2) * _env(n, .001, .1)
    if name == 'type':
        n = int(.03 * SR); return _lp(_noise(n, seed), 2) * _env(n, .0003, .006) * .7
    raise ValueError(name)


# real recorded sounds (assets/sfx/house: CC0, Kenney + Freesound, 48 kHz mono, peak -3 dBFS, sfx.json = hit offsets).
# cue name -> (house file, gain dB, max length s). The file is placed so its hit lands on the cue time; risers keep
# "cue = start" like the synth one. Names without a house file (chime, crack, beephi) stay synthesised.
HOUSE = {'whoosh': ('whoosh_short', 0, 0), 'hit': ('hit_boom', -2, 1.6), 'sub': ('sub_drop', -2, 1.4), 'riser': ('riser_1s', 0, 0),
         'tick': ('tick_a', 0, 0), 'tock': ('tock_a', 0, 0), 'pop': ('pop_a', -2, 0), 'click': ('click_soft', 0, 0), 'ratchet': ('click_ui', -2, 0),
         'ding': ('ding_correct', -2, 0), 'thud': ('thud', 0, 0), 'thunder': ('thunder', 0, 3.5), 'glitch': ('glitch', -2, .4),
         'type': ('click_soft', -4, 0), 'beep': ('beep', -2, 0), 'blip': ('odds_up', -2, 0),
         'roar': ('crowd_roar', 0, 7), 'whistle': ('whistle_short', 0, 0), 'gasp': ('crowd_gasp', 0, 3)}
_HOUSE_CACHE = {}


def house(name):
    """(samples, hit offset in seconds) for a cue name, or None when there is no house file.
    'file:<name>' plays assets/sfx/house/<name>.wav whole from the cue time (beds: crowd_bed, rain_bed, wind)."""
    if name.startswith('file:'):
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'sfx', 'house', name[5:] + '.wav')
        if not os.path.exists(p): return None
        with wave.open(p) as w:
            x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float64) / 32768
            if w.getnchannels() == 2: x = x.reshape(-1, 2).mean(axis=1)
        return (x, 0.0)
    if name not in HOUSE: return None
    if name in _HOUSE_CACHE: return _HOUSE_CACHE[name]
    import json
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'sfx', 'house')
    try:
        meta = json.load(open(os.path.join(base, 'sfx.json'), encoding='utf-8'))
        fn, db, mx = HOUSE[name]; m = meta[fn]
        with wave.open(os.path.join(base, os.path.basename(m['file']) if m.get('file') else fn + '.wav')) as w:
            x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float64) / 32768
            if w.getnchannels() == 2: x = x.reshape(-1, 2).mean(axis=1)
        if mx:
            x = x[:int(mx * SR)].copy(); fade = min(len(x), int(.25 * SR)); x[-fade:] *= np.linspace(1, 0, fade)
        off = 0.0 if name == 'riser' else float(m.get('hit_offset_s') or 0)
        r = (x * 10 ** (db / 20), off)
    except Exception:
        r = None
    _HOUSE_CACHE[name] = r
    return r


def mix(cues, dur, out, synth=False):
    buf = np.zeros(int((dur + 1) * SR))
    for i, (t, name, db) in enumerate(cues):
        h = None if synth else house(name)
        if not h and name.startswith('file:'): continue
        s, off = (h if h else (sound(name, seed=i), 0.0))
        s = s * (10 ** (db / 20))
        a = int((t - off) * SR); b = min(len(buf), a + len(s))
        if a < 0: s = s[-a:]; a = 0
        if a < len(buf): buf[a:b] += s[:b - a]
    buf = buf[:int(dur * SR)]
    pk = np.max(np.abs(buf)) or 1
    buf = buf / pk * (10 ** (-3 / 20))
    pcm = (np.clip(buf, -1, 1) * 32767).astype(np.int16)
    st = np.repeat(pcm[:, None], 2, axis=1)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with wave.open(out, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
    return out


def cues_for(spec, lead=0.0):
    """default sound design per motion format (times in video seconds: the template time minus the render lead)"""
    f = spec.get('fmt'); c = []
    T = lambda x: x - lead
    if f == 'timed':
        c += [(T(.1), 'pop', -6), (T(.4), 'whoosh', -10)] + [(T(1.5 + i), 'tick', -4) for i in range(3)] + [(T(4.4), 'riser', -12), (T(4.5), 'hit', 0), (T(4.9), 'whoosh', -10)]
    elif f == 'wheel':
        c += [(T(.1), 'pop', -6), (T(.45), 'whoosh', -9)]
        t, gap = 1.0, .045                                     # clicks that slow down like the wheel (power4 ease-out)
        while t < 5.1:
            c.append((T(t), 'ratchet', -9)); gap *= 1.085; t += gap
        c += [(T(5.3), 'hit', 0), (T(7.0), 'whoosh', -8), (T(7.3), 'pop', -8)]
    elif f == 'outof100':
        c += [(T(.1), 'whoosh', -10)] + [(T(1.0 + k * .022 * 5), 'click', -16) for k in range(20)] + [(T(4.0), 'riser', -14), (T(4.6), 'hit', -3)]
    elif f == 'aichat':
        c += [(T(.2), 'blip', -8)] + [(T(.3 + k * .09), 'click', -18) for k in range(22)] + [(T(2.8), 'blip', -8)] + \
             [(T(3.6 + k * .08), 'click', -18) for k in range(28)] + [(T(7.0), 'whoosh', -8), (T(9.0), 'hit', -2)]
    elif f == 'livetape':
        ra = spec.get('resultAt') or 0
        c += [(T(.05), 'whoosh', -10)] + [(T(ra - 3 + k), 'tick', -4) for k in range(3)] + [(T(ra - .05), 'hit', 0), (T(ra), 'sub', -4)]
        if spec.get('endAt'): c.append((T(spec['endAt']), 'whoosh', -8))
    elif f in ('pnl_edit',):
        at = spec.get('cardAt') or 1.2
        c += [(T(max(0, at - 1.2)), 'riser', -10), (T(at), 'hit', 0), (T(at), 'sub', -3)] + [(T(at + .5 + k * .15), 'click', -12) for k in range(4)] + [(T(at + 2), 'whoosh', -10)]
    elif f == 'hottake':
        cut = spec.get('cut') or 3.2
        n_words = sum(len(l.split()) for l in spec.get('lines', []))
        c += [(T(.2 + k * .12), 'pop', -12) for k in range(min(n_words, 12))] + [(T(cut - 1.0), 'riser', -10), (T(cut), 'hit', 0), (T(cut + .3), 'whoosh', -10)]
    elif f in ('clipbanner',):
        ev = (spec.get('event') or {}).get('at')
        c += [(T(.3), 'whoosh', -10)] + ([(T(ev - .05), 'hit', 0), (T(ev), 'sub', -4)] if ev else [])
    elif f == 'demo':
        for s in spec.get('steps', []): c.append((T(s['at']), 'pop', -8))
        for m in spec.get('moves', []):
            if m.get('tap'): c.append((T(m['at']), 'click', -4))
            if m.get('ring'): c.append((T(m['at']), 'blip', -10))
            if m.get('show') is not None and m['at'] > .5: c.append((T(m['at'] - .1), 'whoosh', -12))
    return [x for x in c if x[0] >= 0]
