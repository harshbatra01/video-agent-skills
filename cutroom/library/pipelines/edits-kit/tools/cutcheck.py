"""Find hidden cuts inside source ranges (a 'shot' from the catalog can still contain a cut).

usage: python cutcheck.py PLAN.json            -> lists every plan clip whose source range crosses a cut
as a module: cuts_in(file, s0, s1) -> [source seconds of cuts]
Two rules, either one counts: structure change (normalized-luma correlation < 0.45) or a luma jump that is
> 16 and > 3x the local median (the rule that caught every cut in our own GASS edit).
"""
import sys, json
import numpy as np
import av

def cuts_in(path, s0, s1, w=64, h=36):
    c = av.open(path); st = c.streams.video[0]; st.thread_type = "AUTO"
    c.seek(int(max(0, s0 - 0.5) / st.time_base), stream=st)
    fr_t, ys = [], []
    for fr in c.decode(st):
        t = float(fr.pts * st.time_base)
        if t < s0 - 0.05: continue
        if t > s1 + 0.05: break
        a = fr.reformat(width=w, height=h, format="gray").to_ndarray().astype(np.float32)
        fr_t.append(t); ys.append(a)
    c.close()
    if len(ys) < 3: return []
    y = np.stack(ys); n = len(y); flat = y.reshape(n, -1)
    z = (flat - flat.mean(1, keepdims=True)) / (flat.std(1, keepdims=True) + 1e-6)
    d = np.zeros(n); d[1:] = np.abs(y[1:] - y[:-1]).mean((1, 2))
    out = []
    for i in range(1, n):
        corr = float(np.dot(z[i], z[i - 1]) / z.shape[1])
        med = float(np.median(d[max(1, i - 6):i + 7]))
        if corr < 0.45 or (d[i] > 16 and d[i] > 3 * max(med, 1)):
            if not out or fr_t[i] - out[-1] > 0.1: out.append(round(fr_t[i], 3))
    return out

if __name__ == "__main__":
    plan = json.load(open(sys.argv[1], encoding="utf-8"))
    for k, cl in enumerate(plan["clips"]):
        if "rk" in cl: s0, s1 = min(r[1] for r in cl["rk"]), max(r[1] for r in cl["rk"])
        else: s0 = cl["src"]; s1 = s0 + (cl["t1"] - cl["t0"]) * cl.get("speed", 1.0)
        cs = cuts_in(cl["file"], s0, s1 + 0.05)
        inner = [t for t in cs if s0 + 0.01 < t <= s1 + 0.01]       # a cut ON the last used frame shows 1 frame of the next shot
        print(f"{k:2d} {cl['name']:<14} src {s0:8.3f}-{s1:8.3f}  {'HIDDEN CUT at ' + str(inner) if inner else 'clean'}")
