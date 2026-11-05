"""Cut QA: flag cuts that end or start while he is still talking (loud audio right at the edit)."""
import json, sys
import numpy as np
db = np.load("db10ms.npy")
P = json.load(open("pieces_asr.json"))
W = sorted([w for p in P for w in p["words"]], key=lambda w: w["s"])
def lvl(t0, t1):
    seg = db[int(t0 * 100):int(t1 * 100)]
    return float(seg.max()) if len(seg) else -120.0
def qc(edl_path):
    E = json.load(open(edl_path))
    bad = []
    for n, c in enumerate(E["cuts"]):
        a, b = c["raw_in_f"] / 30, c["raw_out_f"] / 30
        out_end = lvl(b - 0.05, b)           # last 50 ms kept
        after = lvl(b, b + 0.08)             # next 80 ms dropped
        before = lvl(a - 0.08, a)
        out_start = lvl(a, a + 0.05)
        if out_end > -55 and after > -55:
            bad.append((n, "END", round(b, 2), round(out_end), round(after), " ".join(w["w"] for w in W if b - 1.0 < w["e"] and w["s"] < b + 0.6), c["out_start_f"] + c["raw_out_f"] - c["raw_in_f"]))
        if out_start > -55 and before > -55:
            bad.append((n, "START", round(a, 2), round(before), round(out_start), " ".join(w["w"] for w in W if a - 0.6 < w["e"] and w["s"] < a + 1.0), c["out_start_f"]))
    return bad
if __name__ == "__main__":
    for row in qc(sys.argv[1]):
        n, kind, t, l1, l2, words, of = row
        print(f"cut {n:3d} {kind:5s} raw {t:8.2f}  out {of/30:7.2f}s  levels {l1}/{l2} dB  «{words}»")
