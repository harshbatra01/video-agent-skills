"""FX test reel v1: every optical transition from tools/ae/fx_lib.jsx on a real cut (1.2 s each), band layout, plus
an aura span. Clips come from plan_v5.json (same mattes). Writes plan_fxtest.json; render, then compare each cut
frame by frame with the reference moment it copies (tools/compare.py).
"""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.dirname(HERE)
v5 = json.load(open(os.path.join(HERE, "plan_v5.json")))
by = {}
for c in v5["clips"]: by.setdefault(c["name"].split(" ")[0], c)


def retime(cl, t0, t1):
    rk = cl["rk"]; sp = (rk[-1][1] - rk[0][1]) / (rk[-1][0] - rk[0][0]); s0 = rk[0][1]; dt = t0 - rk[0][0]
    c = dict(cl, t0=t0, t1=t1, rk=[[t0, s0], [t1, round(s0 + (t1 - t0) * sp, 4)]], smooth=False)
    f = cl["focus"]
    if isinstance(f[0], list): c["focus"] = [[round(k[0] + dt, 4), k[1], k[2]] for k in f]
    return c


SEG = 1.2
LEAK = os.path.join(KIT, "assets", "overlays", "warm", "leak_a.mp4")
tests = [
    ("blowout", "0_032", "1_040", dict(leak=LEAK)),                                          # TikTok compilation 106.6
    ("zoomrush", "0_060", "0_064", dict(amt=1.5, blur=95, chroma=True)),                     # Speed x Ronaldo 12.57
    ("smear", "0_042", "3_014", dict(vertical=True, tint=[1, 0.88, 0.3])),                   # LeBron 16.87
    ("paint", "0_078", "0_080", dict(color=[0.3, 0.95, 1])),                                 # Messi SHOCK 13.37
    ("vortex", "1_006", "3_017", dict(spin=30)),                                             # LeBron 29.38
    ("recipe", "0_050", "0_061", dict(pattern="EKEKSDSDCC", line=[1, 0.85, 0.3])),          # LeBron 41.87
    ("flood", "0_011", "1_034", dict(steps=[[[1, 0.38, 0.0], 2, 66, 72], [[1, 0.9, 0.12], 4, 92, 92], [[1, 0.17, 0.1], 7, 98, 80]])),  # Mbappe NC 20.78
    ("defocus", "0_028", "0_027", dict(cast=[1, 0.28, 0.2])),                                # Hero +5h 14.38
    ("rays", "1_021", "1_009", dict()),                                                      # Speed x Ronaldo 26.37
]
clips, trans, auras = [], [], []
for i, (ty, a, b, kw) in enumerate(tests):
    t0 = round(i * SEG, 4); tc = round(t0 + SEG / 2, 4); t1 = round(t0 + SEG, 4)
    ka = len(clips); clips.append(retime(by[a], t0, tc)); kb = len(clips); clips.append(retime(by[b], tc, t1))
    tr = dict(type=ty, t=tc, **kw)
    if ty == "zoomrush" and kw.get("chroma"): tr["chroma"] = kb
    if ty == "shatter": tr["clipA"] = ka
    if ty == "rays": tr.update(x=540, y=860)
    trans.append(tr)
# aura on a held hero moment (Messi SHOCK 17.90 purple aura)
t0 = round(len(tests) * SEG, 4); k = len(clips)
endc = [c for c in v5["clips"] if "arms wide" in c["name"]][0]          # its matte runs 3 s (a retime must stay inside it)
clips.append(retime(endc, t0, t0 + 1.6))
auras.append(dict(clip=k, t0=t0, t1=t0 + 1.6, color=[0.62, 0.2, 1], grow=16, soft=24))
plan = dict(name="fx_test", w=1080, h=1920, fps=30, dur=round(t0 + 1.6, 4), band=v5["band"], audio=None,
            clips=clips, transitions=trans, auras=auras, hits=[], words=[], look=v5["look"])
json.dump(plan, open(os.path.join(HERE, "plan_fxtest.json"), "w"), indent=1)
print("fx test:", len(clips), "clips,", len(trans), "transitions + 1 aura,", plan["dur"], "s; cuts at", [t["t"] for t in trans])
