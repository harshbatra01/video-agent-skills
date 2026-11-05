"""Onsets / tempo / beat grid from a wav (mono). numpy only.

usage: python beats.py in.wav out.json [fps]
"""
import sys, json, wave
import numpy as np

def load(path):
    w = wave.open(path, "rb")
    sr = w.getframerate(); n = w.getnframes(); ch = w.getnchannels()
    x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768
    if ch > 1: x = x.reshape(-1, ch).mean(1)
    return sr, x

def stft_mag(x, n_fft=2048, hop=256):
    win = np.hanning(n_fft)
    frames = 1 + (len(x) - n_fft) // hop
    idx = np.arange(n_fft)[None, :] + hop * np.arange(frames)[:, None]
    return np.abs(np.fft.rfft(x[idx] * win, axis=1))

def flux(S, lo, hi, sr, n_fft):
    f = np.fft.rfftfreq(n_fft, 1 / sr)
    band = (f >= lo) & (f < hi)
    L = np.log1p(100 * S[:, band])
    d = np.diff(L, axis=0); d[d < 0] = 0
    e = np.concatenate([[0], d.sum(1)])
    return e / (e.max() + 1e-9)

def peaks(e, hop, sr, k=1.5, w=7, min_gap=0.09):
    # adaptive threshold: moving mean + k * moving std
    n = len(e); out = []
    pad = 20
    for i in range(1, n - 1):
        a, b = max(0, i - pad), min(n, i + pad)
        thr = e[a:b].mean() + k * e[a:b].std()
        if e[i] > thr and e[i] == e[max(0, i - w):i + w + 1].max():
            t = i * hop / sr
            if not out or t - out[-1][0] > min_gap:
                out.append((t, float(e[i])))
    return out

def tempo(e, hop, sr):
    ac = np.correlate(e - e.mean(), e - e.mean(), "full")[len(e) - 1:]
    lags = np.arange(len(ac)) * hop / sr
    best = None
    for bpm in np.arange(60, 200, 0.25):
        lag = 60 / bpm
        i = int(round(lag * sr / hop))
        if i < len(ac):
            # sum harmonics for robustness
            v = ac[i] + 0.5 * ac[min(len(ac) - 1, 2 * i)]
            if best is None or v > best[1]: best = (bpm, v)
    return best[0]

def grid(e, hop, sr, bpm, dur):
    period = 60 / bpm
    best = None
    for ph in np.arange(0, period, 0.005):
        ts = np.arange(ph, dur, period)
        idx = np.clip((ts * sr / hop).round().astype(int), 0, len(e) - 1)
        v = e[idx].sum()
        if best is None or v > best[1]: best = (ph, v)
    return [round(float(t), 3) for t in np.arange(best[0], dur, period)]

def main():
    wav, out = sys.argv[1], sys.argv[2]
    fps = float(sys.argv[3]) if len(sys.argv) > 3 else 30.0
    sr, x = load(wav)
    n_fft, hop = 2048, 256
    S = stft_mag(x, n_fft, hop)
    full = flux(S, 30, 11000, sr, n_fft)
    kick = flux(S, 30, 150, sr, n_fft)
    snare = flux(S, 1500, 6000, sr, n_fft)
    hat = flux(S, 6000, 11000, sr, n_fft)
    dur = len(x) / sr
    bpm = tempo(full, hop, sr)
    beats = grid(full, hop, sr, bpm, dur)
    # RMS loudness per video frame (for drops / builds)
    spf = int(sr / fps)
    rms = [float(np.sqrt((x[i:i + spf] ** 2).mean() + 1e-12)) for i in range(0, len(x) - spf, spf)]
    res = dict(sr=sr, dur=dur, bpm=bpm, beats=beats,
               onsets=peaks(full, hop, sr), kicks=peaks(kick, hop, sr, k=1.8), snares=peaks(snare, hop, sr, k=1.8),
               hats=peaks(hat, hop, sr, k=2.0), rms_db=[round(20 * np.log10(r), 1) for r in rms])
    json.dump(res, open(out, "w"), indent=0)
    print(f"dur {dur:.2f}s bpm {bpm:.2f} beats {len(beats)} onsets {len(res['onsets'])} kicks {len(res['kicks'])} snares {len(res['snares'])} hats {len(res['hats'])}")

if __name__ == "__main__":
    main()
