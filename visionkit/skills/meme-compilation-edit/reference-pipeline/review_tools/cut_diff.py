import json, sys
import numpy as np
sys.path.insert(0, ".")
from tl import TL, TPS, TPF
D = TL("delivered.xml"); U = TL("user.xml")
db = np.load("../data/db10ms.npy")
FLOOR = float(np.percentile(db, 10))
pieces = json.load(open("../data/pieces_asr.json"))
words = sorted([w for p in pieces for w in p["words"]], key=lambda w: w["s"])
def frames(T):
    return [(d["in"] // TPF, (d["in"] + d["end"] - d["start"]) // TPF, d["start"] // TPF) for d in T.tracks["A1"]["items"]]
dc, uc = frames(D), frames(U)
def kept_set(c):
    s = set()
    for a, b, _ in c: s.update(range(a, b))
    return s
ks_d, ks_u = kept_set(dc), kept_set(uc)
def runs(fr):
    fr = sorted(fr); out = []
    for f in fr:
        if out and f == out[-1][1]: out[-1][1] = f + 1
        else: out.append([f, f + 1])
    return out
def text(a, b):   # words overlapping raw seconds a..b
    return " ".join(w["w"] for w in words if w["e"] > a and w["s"] < b)
def lvl(a, b):
    seg = db[int(a * 100):int(b * 100)]
    return f"{seg.max():.0f}/{np.median(seg):.0f} dB" if len(seg) else "-"
def seq_d(f): return D.raw_to_seq(f / 30)
if __name__ == "__main__":
    print(f"room floor {FLOOR:.1f} dB")
    print("\n### raw frames I kept that he REMOVED")
    for a, b in runs(ks_d - ks_u):
        print(f"raw {a/30:8.2f}-{b/30:8.2f} ({b-a:4d} f) at my out {seq_d(a) or 0:7.2f}s  level max/med {lvl(a/30,b/30):14s} «{text(a/30, b/30)}»")
    print("\n### raw frames he ADDED (I had cut)")
    for a, b in runs(ks_u - ks_d):
        print(f"raw {a/30:8.2f}-{b/30:8.2f} ({b-a:4d} f) at his out {U.raw_to_seq(a/30) or 0:7.2f}s  level max/med {lvl(a/30,b/30):14s} «{text(a/30, b/30)}»")
    # order changes: compare sequence of raw segments
    print("\n### clip boundaries")
    print("delivered clips", len(dc), "user clips", len(uc))
