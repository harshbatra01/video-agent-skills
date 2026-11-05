#!/usr/bin/env python3
"""Beat grid and energy map from a music file. beat_map.py <music> <out.json> [video for cut test]
Fits one steady tempo by a comb search on a spectral-flux onset curve, then scores how many strong onsets sit on the grid."""
import json, subprocess, sys
import numpy as np

SR, HOP, N = 22050, 512, 2048


def load(p):
    return np.frombuffer(subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32)


x = load(sys.argv[1]); dur = len(x) / SR
fr = SR / HOP; win = np.hanning(N)
S = np.abs(np.array([np.fft.rfft(x[i:i + N] * win) for i in range(0, len(x) - N, HOP)]))
L = np.log1p(S * 10)
flux = np.maximum(0, np.diff(L, axis=0)).sum(1); flux = flux - np.convolve(flux, np.ones(43) / 43, "same"); flux = np.maximum(flux, 0)
bass = np.maximum(0, np.diff(L[:, :int(150 / (SR / N))], axis=0)).sum(1)
T = np.arange(len(flux)) / fr


def fit(curve):
    best = []
    for bpm in np.arange(60, 180.01, 0.25):
        per = 60 / bpm * fr; scores = []
        for ph in np.arange(0, per, max(per / 32, 1)):
            idx = np.round(np.arange(ph, len(curve), per)).astype(int); idx = idx[idx < len(curve)]
            scores.append((curve[idx].mean(), ph))
        s, ph = max(scores); best.append((s / (curve.mean() + 1e-9), bpm, ph / fr))
    return sorted(best, reverse=True)


res = fit(flux)
top = []
for s, b, p in res:
    if all(abs(b - t[1]) > 1.5 for t in top): top.append((round(float(s), 2), float(b), round(float(p), 3)))
    if len(top) == 5: break
score, bpm, phase = top[0]
per = 60 / bpm
grid = np.arange(phase, dur, per)
thr = np.percentile(flux, 92); peaks = [i for i in range(2, len(flux) - 2) if flux[i] > thr and flux[i] == flux[i - 2:i + 3].max()]
pt = T[peaks]; dist = np.array([np.abs(grid - t).min() for t in pt]) if len(pt) else np.array([])
on = float((dist < .05).mean()) if len(dist) else 0
chance = min(1, 2 * .05 / per)
rms = [float(10 * np.log10(np.mean(x[int(i * SR):int((i + 2) * SR)] ** 2) + 1e-9)) for i in np.arange(0, dur - 2, 2)]
# strongest moments: big bass or flux jumps, at least 4 s apart
strength = flux / (flux.max() + 1e-9) + bass / (bass.max() + 1e-9)
order = np.argsort(strength)[::-1]; hits = []
for i in order:
    if all(abs(T[i] - h) > 4 for h in hits): hits.append(float(T[i]))
    if len(hits) == 10: break
out = dict(dur=round(dur, 2), bpm=bpm, phase=phase, beat_s=round(per, 3), candidates=top, onsets_on_grid=round(on, 2), chance=round(chance, 2),
           strongest=sorted(round(h, 2) for h in hits), rms_2s=[round(a, 1) for a in rms], grid=[round(float(g), 3) for g in grid])
if len(sys.argv) > 3:
    raw = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", sys.argv[3], "-vf", "scale=320:-2,select='gt(scene,0.25)',showinfo", "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
    import re
    cuts = [float(m) for m in re.findall(r"pts_time:([\d.]+)", raw)]
    d = np.array([np.abs(grid - c).min() for c in cuts]); half = np.arange(phase, dur, per / 2); d2 = np.array([np.abs(half - c).min() for c in cuts])
    out.update(cuts=len(cuts), cuts_on_beat=round(float((d < .07).mean()), 2), cuts_on_beat_chance=round(min(1, 2 * .07 / per), 2), cuts_on_half=round(float((d2 < .07).mean()), 2), cuts_on_half_chance=round(min(1, 2 * .07 / (per / 2)), 2), cut_times=[round(c, 2) for c in cuts])
json.dump(out, open(sys.argv[2], "w"))
print({k: v for k, v in out.items() if k not in ("grid", "cut_times")})
