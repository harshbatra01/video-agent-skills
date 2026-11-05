# Music analysis under a voice-over without extra installs: onset envelopes in the sub band (kicks, booms, <150 Hz) and the
# top band (hats, risers, >5 kHz), tempo by autocorrelation, beat grid phase, and the strongest hits.
# python3 beats.py <media> <out.json> [vo_words.json to mask speech]
import json, subprocess, sys
import numpy as np
from scipy.signal import butter, sosfiltfilt, find_peaks
SR = 22050; HOP = 256
a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", sys.argv[1], "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
def band(lo, hi):
    sos = butter(4, [lo, hi] if lo else hi, "bandpass" if lo else "lowpass", fs=SR, output="sos"); return sosfiltfilt(sos, a)
def env(x):
    n = len(x) // HOP; e = np.sqrt((x[:n * HOP].reshape(n, HOP) ** 2).mean(1)); le = np.log1p(100 * e)
    fl = np.maximum(np.diff(le, prepend=le[0]), 0); return fl / (fl.max() + 1e-9), e
sub, sub_rms = env(band(None, 150)); top, _ = env(band(5000, 10000)); mid, _ = env(band(150, 5000))
fr = SR / HOP; t = np.arange(len(sub)) / fr
onset = 0.6 * sub + 0.4 * top
# tempo: autocorrelation of the onset envelope, 70-180 bpm
ac = np.correlate(onset - onset.mean(), onset - onset.mean(), "full")[len(onset) - 1:]
lags = np.arange(len(ac)) / fr; ok = (lags > 60 / 180) & (lags < 60 / 70)
cands = sorted(((ac[i], 60 / lags[i]) for i in np.where(ok)[0]), reverse=True)[:5]
bpm = cands[0][1]; period = 60 / bpm
# phase: shift of the grid that catches the most onset energy
phases = np.linspace(0, period, 60, endpoint=False)
score = [onset[np.clip(((np.arange(0, t[-1], period) + p) * fr).astype(int), 0, len(onset) - 1)].sum() for p in phases]
ph = phases[int(np.argmax(score))]; grid = np.arange(ph, t[-1], period)
# hits: strong sub-band peaks (booms, drops), and top-band peaks (risers end, hats, whooshes)
pk, pr = find_peaks(sub, height=0.35, distance=int(0.12 * fr)); hits = [{"t": round(float(t[i]), 3), "s": round(float(pr["peak_heights"][k]), 2)} for k, i in enumerate(pk)]
pk2, pr2 = find_peaks(top, height=0.4, distance=int(0.08 * fr)); tops = [{"t": round(float(t[i]), 3), "s": round(float(pr2["peak_heights"][k]), 2)} for k, i in enumerate(pk2)]
on_grid = np.mean([np.min(np.abs(grid - h["t"])) < 0.05 for h in hits]) if hits else 0
json.dump({"bpm_candidates": [[round(b, 1), round(float(s), 1)] for s, b in cands], "bpm": round(bpm, 2), "phase": round(float(ph), 3),
           "grid": [round(float(x), 3) for x in grid], "sub_hits": hits, "top_hits": tops,
           "sub_rms_db_per_sec": [round(float(20 * np.log10(sub_rms[int(i * fr):int((i + 1) * fr)].mean() + 1e-9)), 1) for i in range(int(t[-1]))]}, open(sys.argv[2], "w"))
print(f"bpm {bpm:.1f} (candidates {[round(b,1) for s,b in cands]}) phase {ph:.3f}s | sub hits {len(hits)} ({on_grid:.0%} on the beat grid) | top hits {len(tops)}")
