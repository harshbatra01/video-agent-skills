#!/usr/bin/env python3
# Per-hit anatomy of a mix (no scipy): band levels (sub <60, low 60-250, lowmid 250-2k, high 2k-8k, air >8k) in 20 ms steps
# around each hit, decay time to -20 dB, spectral centroid, and the strongest steady pitches of the bed.
# sound_anatomy.py <video> <out.json> <hit times csv>
import json, subprocess, sys, numpy as np
SR = 48000
x = np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",sys.argv[1],"-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout, np.float32).astype(float)
hits = [float(t) for t in sys.argv[3].split(",")]
B = {"sub": (20, 60), "low": (60, 250), "lowmid": (250, 2000), "high": (2000, 8000), "air": (8000, 20000)}
win = int(0.04 * SR); hop = int(0.02 * SR); f = np.fft.rfftfreq(win, 1 / SR); hw = np.hanning(win)
def bands(t0, t1):
    rows = []
    for i in range(int(t0 * SR), int(t1 * SR) - win, hop):
        P = np.abs(np.fft.rfft(x[i:i + win] * hw)) ** 2
        rows.append({k: round(float(10 * np.log10(P[(f >= a) & (f < b)].sum() + 1e-12)), 1) for k, (a, b) in B.items()} | {"t": round(i / SR, 2), "centroid": int((f * P).sum() / (P.sum() + 1e-12))})
    return rows
out = {"hits": []}
for h in hits:
    r = bands(max(0, h - 0.1), h + 0.8); tot = [10 * np.log10(sum(10 ** (row[k] / 10) for k in B)) for row in r]
    pk = int(np.argmax(tot)); dec = next((round(r[j]["t"] - r[pk]["t"], 2) for j in range(pk, len(r)) if tot[j] < tot[pk] - 20), None)
    out["hits"].append({"t": h, "peak_t": r[pk]["t"], "peak_bands": {k: r[pk][k] for k in B}, "centroid_at_peak": r[pk]["centroid"], "decay_to_-20dB_s": dec})
# steady pitch of the bed: long FFT over quiet stretches
for name, (t0, t1) in {"bed_4.6-6.3": (4.6, 6.3), "bed_11.4-14.0": (11.4, 14.0), "intro_0.1-1.6": (0.1, 1.6)}.items():
    s = x[int(t0 * SR):int(t1 * SR)]; P = np.abs(np.fft.rfft(s * np.hanning(len(s)))); ff = np.fft.rfftfreq(len(s), 1 / SR)
    m = (ff > 25) & (ff < 2000); idx = np.argsort(P[m])[::-1]; peaks = []
    for i in idx:
        fr = ff[m][i]
        if all(abs(fr - p) > 6 for p in peaks): peaks.append(round(float(fr), 1))
        if len(peaks) == 8: break
    out[name] = {"top_pitches_hz": peaks, "rms_db": round(float(10 * np.log10((s ** 2).mean() + 1e-12)), 1)}
json.dump(out, open(sys.argv[2], "w"), indent=1); print(json.dumps(out)[:4000])
