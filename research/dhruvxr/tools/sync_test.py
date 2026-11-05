#!/usr/bin/env python3
# Do picture events land on audio onsets more than chance? Onsets = top 8% spectral-flux peaks of the full mix.
# Hit = event within +-tol s of an onset. Chance = mean hit rate of the same events shifted by 1000 random offsets (circular).
# sync_test.py <video> <events.json from cut_events.py> [extra_times_csv] [tol] [onset percentile, default 92]
import json, subprocess, sys, numpy as np
SR, HOP, N = 22050, 256, 1024
v, ev = sys.argv[1], sys.argv[2]; extra = [float(t) for t in sys.argv[3].split(",")] if len(sys.argv) > 3 and sys.argv[3] else []; tol = float(sys.argv[4]) if len(sys.argv) > 4 else 0.067
x = np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",v,"-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout, np.float32); dur = len(x)/SR
S = np.abs(np.array([np.fft.rfft(x[i:i+N]*np.hanning(N)) for i in range(0, len(x)-N, HOP)])); L = np.log1p(S*10)
flux = np.maximum(0, np.diff(L, axis=0)).sum(1); T = np.arange(len(flux))*HOP/SR
PCT = float(sys.argv[5]) if len(sys.argv) > 5 else 92; thr = np.percentile(flux, PCT); pk = np.array([T[i] for i in range(2, len(flux)-2) if flux[i] > thr and flux[i] == flux[i-2:i+3].max()])
def rate(ts): return float(np.mean([np.abs(pk - t).min() <= tol for t in ts])) if len(ts) else 0
E = json.load(open(ev)); fps = E["fps"]; cuts = [e["t"] for e in E["events"] if e["kind"] in ("CUT", "CUT+FLASH")]; flashes = [e["t"] for e in E["events"] if e["kind"] in ("FLASH", "CUT+FLASH")]
rng = np.random.default_rng(1)
def test(name, ts):
    ts = [t for t in ts if t < dur]; r = rate(ts); ch = np.mean([rate([(t+o) % dur for t in ts]) for o in rng.uniform(0.2, dur-0.2, 1000)])
    return {"set": name, "n": len(ts), "on_onset_pct": round(r*100), "chance_pct": round(ch*100), "times": [round(t, 2) for t in ts]}
out = {"onsets": len(pk), "onsets_per_s": round(len(pk)/dur, 2), "tol_s": tol, "tests": [test("cuts", cuts), test("flash events", flashes)] + ([test("text in-times", extra)] if extra else [])}
print(json.dumps(out))
