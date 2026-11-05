# Correct whisper word starts against the waveform: a word whose start sits in silence or a breath (under -30 dB) moves to where speech resumes (over -28 dB).
# python3 fix_words.py <audio> <words.json> <out.json>
import json, subprocess, sys
import numpy as np
src, wj, out = sys.argv[1:4]; SR = 16000; HOP = 160
a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
e = 20 * np.log10(np.sqrt((a[:len(a) // HOP * HOP].reshape(-1, HOP) ** 2).mean(1)) + 1e-9)
D = json.load(open(wj)); n = 0
for w in D["words"]:
    i0, i1 = int(w["s"] * 100), int(w["e"] * 100)
    if i1 <= i0 + 2 or e[i0:i0 + 4].max() > -30: continue
    k = next((i for i in range(i0, i1) if e[i] > -28), None)
    if k is not None and k / 100 - w["s"] > 0.04:
        w["s"] = round(k / 100 - 0.02, 2); n += 1
json.dump(D, open(out, "w"), indent=0); print("corrected", n, "word starts")
