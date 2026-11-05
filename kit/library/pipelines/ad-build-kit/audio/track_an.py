"""Music track analysis for editing: beat grid (tempo from metadata, phase from spectral flux), downbeat phase,
per-bar loudness, and the final chord (first downbeat after the last loud bar, where the ending decay starts)."""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_sfx import read_wav

SR = 48000


def load(path):
    a, sr, _, _ = read_wav(path); assert sr == SR, sr
    return a[:, :2] if a.shape[1] >= 2 else np.repeat(a, 2, axis=1)


def flux_curve(x, hop=240, n=2048):
    frames = np.lib.stride_tricks.sliding_window_view(x, n)[::hop] * np.hanning(n)
    S = np.abs(np.fft.rfft(frames, axis=1))
    fl = np.maximum(np.diff(np.log1p(100 * S), axis=0), 0).sum(axis=1)
    t = (np.arange(len(fl)) + 1) * hop / SR + n / 2 / SR
    return t, fl


def grid(t, fl, bpm):
    def score(b, ph, step=1):
        ts = np.arange(ph, t[-1], 60.0 / b * step); idx = np.searchsorted(t, ts); idx = idx[idx < len(fl)]
        return fl[idx].mean()
    best = max((score(b, p), b, p) for b in np.arange(bpm - 0.3, bpm + 0.31, 0.02) for p in np.arange(0, 60.0 / bpm, 0.005))
    _, b, ph = best; beat = 60.0 / b
    bar_ph = max(((score(b, ph + k * beat, 4), ph + k * beat) for k in range(4)))[1]
    return b, beat, bar_ph % (4 * beat)


def analyze(path, bpm):
    a = load(path); x = a.mean(axis=1)
    t, fl = flux_curve(x)
    b, beat, d0 = grid(t, fl, bpm)
    bar = 4 * beat
    nb = int((len(x) / SR - d0) / bar)
    db = []
    for k in range(nb):
        s = int((d0 + k * bar) * SR); e = int((d0 + (k + 1) * bar) * SR)
        db.append(20 * np.log10(np.sqrt(np.mean(x[s:e] ** 2)) + 1e-9))
    db = np.array(db); top = db.max()
    loud = np.where(db >= top - 6)[0]
    last_loud = int(loud[-1])
    e_bar = min(last_loud + 1, nb - 1)
    E = d0 + e_bar * bar
    # downbeat strength (flux at each downbeat), for spotting section starts
    idx = np.searchsorted(t, d0 + np.arange(nb) * bar); idx = np.clip(idx, 0, len(fl) - 1)
    dstr = fl[idx] / (np.median(fl) + 1e-9)
    tail = len(x) / SR - E
    return dict(path=path, bpm=round(b, 2), beat=beat, bar=bar, d0=d0, n_bars=nb, bar_db=[round(v - top, 1) for v in db],
                down_strength=[round(float(v), 1) for v in dstr], E=E, E_bar=e_bar, tail=round(tail, 2), dur=len(x) / SR)


if __name__ == '__main__':
    r = analyze(sys.argv[1], float(sys.argv[2]))
    print('bpm %.2f bar %.3f d0 %.3f bars %d  final chord at bar %d = %.2f s (tail %.1f s of %.1f)' % (r['bpm'], r['bar'], r['d0'], r['n_bars'], r['E_bar'], r['E'], r['tail'], r['dur']))
    print(' '.join('%d:%.0f' % (k, v) for k, v in enumerate(r['bar_db'])))
    print('strong downbeats:', [k for k, v in enumerate(r['down_strength']) if v > 2.5])
