"""Rebuild the 3 things dialogue track (A1) at 48 kHz from the cleaned source, measure loudness/peaks, write tt_dialog.wav"""
import json, os, sys, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import atools as A
SRC = r"C:\VISION\IMMUFIX\repair\ENCODED RUSHES\Cleaned\A003_09181253_C118-esv2-50p-bg-10p-music-10p.mp4"
HERE = os.path.dirname(os.path.abspath(__file__))
items = json.load(open(os.path.join(HERE, 'tt_a1.json')))
SR = 48000
# group pieces into source chunks
rngs = sorted([(i[2], i[2] + i[1] - i[0]) for i in items])
chunks = []
for a, b in rngs:
    if chunks and a - chunks[-1][1] < 6: chunks[-1][1] = max(chunks[-1][1], b)
    else: chunks.append([a, b])
cache = {}
for k, (a, b) in enumerate(chunks):
    p = os.path.join(HERE, 'tmp_tt_%02d.wav' % k)
    if not os.path.exists(p): A.extract_wav(SRC, p, a - 0.5, b + 0.5)
    x, sr = A.load_wav(p); assert sr == SR
    cache[k] = (a - 0.5, x)
out = np.zeros((int(48.25 * SR) + 10, 2))
for s, e, tin in items:
    k = [i for i, (a, b) in enumerate(chunks) if a - 1e-6 <= tin <= b][0]
    c0, x = cache[k]; i0 = int(round((tin - c0) * SR)); n = int(round((e - s) * SR))
    seg = x[i0:i0 + n]
    out[int(round(s * SR)):int(round(s * SR)) + len(seg)] = seg
np.save(os.path.join(HERE, 'tt_dialog.npy'), out.astype(np.float32))
print('chunks', len(chunks), 'LUFS %.1f  true peak %.1f dBTP' % (A.lufs(out, SR), A.true_peak_db(out)))
t, st = A.short_term(out, SR)
print('short-term LUFS p50 %.1f p90 %.1f max %.1f' % (np.percentile(st[st > -60], 50), np.percentile(st[st > -60], 90), st.max()))
m = np.abs(out).max(axis=1); blk = int(0.05 * SR); pk = np.array([m[i:i + blk].max() for i in range(0, len(m) - blk, blk)])
print('50 ms block peaks dBFS: p50 %.1f p90 %.1f p99 %.1f max %.1f' % tuple(20 * np.log10(np.percentile(pk[pk > 1e-4], q) + 1e-9) for q in (50, 90, 99, 100)))
