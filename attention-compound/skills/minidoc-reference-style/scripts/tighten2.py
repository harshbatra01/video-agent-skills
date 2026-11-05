# Shorten pauses using the waveform only: silent runs (every 10 ms frame under -48 dB) longer than MAXG are cut to KEEP,
# with 60 ms of silence left on each side, so no word edge is touched. Longer KEEPs on given times (dramatic pauses).
# python3 tighten2.py <in.wav> <out.wav> [maxg keep] [t:keep,t:keep ...]   (t = approx time of the word AFTER the pause)
import subprocess, sys
import numpy as np
src, out = sys.argv[1:3]; MAXG = float(sys.argv[3]) if len(sys.argv) > 3 else 0.34; KEEP = float(sys.argv[4]) if len(sys.argv) > 4 else 0.24
SPEC = [tuple(map(float, x.split(":"))) for x in sys.argv[5].split(",")] if len(sys.argv) > 5 else []
SR = 48000; HOP = 480
a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
e = 20 * np.log10(np.sqrt((a[:len(a) // HOP * HOP].reshape(-1, HOP) ** 2).mean(1)) + 1e-9)
sil = e < -48; runs, i = [], 0
while i < len(sil):
    if sil[i]:
        j = i
        while j < len(sil) and sil[j]: j += 1
        runs.append((i / 100, j / 100)); i = j
    else: i += 1
cuts = []
for s, t in runs:
    if s < 0.05: continue                      # keep the head as is
    keep = next((k for at, k in SPEC if abs(at - t) < 0.6), KEEP)
    if t - s > max(MAXG, keep + 0.12):
        m = (s + t) / 2; r = (t - s - keep) / 2; cuts.append((m - r, m + r))
keep_rng, p = [], 0.0
for s, t in cuts: keep_rng.append((p, s)); p = t
keep_rng.append((p, None))
fc = "".join(f"[0:a]atrim={s:.3f}{':end=%.3f' % t if t else ''},asetpts=PTS-STARTPTS[p{i}];" for i, (s, t) in enumerate(keep_rng))
fc += "".join(f"[p{i}]" for i in range(len(keep_rng))) + f"concat=n={len(keep_rng)}:v=0:a=1[o]"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", fc, "-map", "[o]", out], check=True)
print(len(cuts), "pauses shortened, removed", round(sum(t - s for s, t in cuts), 2), "s")
