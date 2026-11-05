#!/usr/bin/env python3
# 0.1 s envelope of the mix: level (dB RMS), bass share (<150 Hz), voice-band share (300-3400 Hz). envelope.py <video> <out.json>
import numpy as np, subprocess, json, sys
x = np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",sys.argv[1],"-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout, np.float32).astype(float)
n = 1600; fr = np.fft.rfftfreq(n, 1/16000); rows = []
for i in range(0, len(x)-n, n):
    s = x[i:i+n]; F = np.abs(np.fft.rfft(s))**2; tot = F.sum()+1e-12
    rows.append(dict(t=round(i/16000, 1), db=round(float(10*np.log10((s**2).mean()+1e-12)), 1), bass=round(float(F[fr<150].sum()/tot), 2), voice=round(float(F[(fr>300)&(fr<3400)].sum()/tot), 2)))
json.dump(rows, open(sys.argv[2], "w")); print(" ".join(f"{r['t']}:{r['db']:.0f}/{r['bass']:.1f}/{r['voice']:.1f}" for r in rows))
