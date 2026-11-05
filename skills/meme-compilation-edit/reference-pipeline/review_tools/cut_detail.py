import json, sys
import numpy as np
sys.path.insert(0, ".")
from tl import TL, TPS, TPF
from cut_diff import *   # data and helpers (an import, not exec)
def clip_of(c, f):
    for n, (a, b, s) in enumerate(c):
        if a <= f < b: return n, a, b
    return None
def prof(a, b):   # per-frame max dB
    return " ".join(f"{db[int(f*100/30):int((f+1)*100/30)].max():.0f}" for f in range(a, b))
for label, diff, mine, his in (("REMOVED", ks_d - ks_u, dc, uc), ("ADDED", ks_u - ks_d, uc, dc)):
    print(f"\n######## {label}")
    for a, b in runs(diff):
        n, ca, cb = clip_of(mine, a)
        where = "head" if a == ca and b < cb else "tail" if b == cb and a > ca else "whole clip" if (a, b) == (ca, cb) else "middle"
        # neighbours in the other version
        prev_ = [x for x in his if x[1] <= a]; next_ = [x for x in his if x[0] >= b]
        pe = max(prev_, key=lambda x: x[1])[1] if prev_ else None
        ns = min(next_, key=lambda x: x[0])[0] if next_ else None
        print(f"\nraw {a/30:.2f}-{b/30:.2f} ({b-a} f) = {where} of {'my' if label=='REMOVED' else 'his'} clip {n} [{ca/30:.2f}-{cb/30:.2f}]")
        print(f"   words before: «{text(a/30-2.0, a/30)}» | inside: «{text(a/30, b/30)}» | after: «{text(b/30, b/30+2.0)}»")
        lo, hi = max(a - 6, ca - 3), min(b + 6, cb + 3)
        print(f"   per-frame max dB {lo/30:.2f}..: {prof(lo, a)} [ {prof(a, b)} ] {prof(b, hi)}")
