"""Transition test reel: every transition in edits_lib "transitions v2" on a real cut, 1.2 s each, band layout.
Reuses clips (and their mattes) from plan_v4.json. Writes plan_ttest.json; render it and review frame by frame
before a transition goes into an edit.
"""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
v4 = json.load(open(os.path.join(HERE, "plan_v4.json")))
by = {c["name"].split(" ")[0]: c for c in v4["clips"]}


def retime(cl, t0, t1):
    rk = cl["rk"]; sp = (rk[1][1] - rk[0][1]) / (rk[1][0] - rk[0][0]); s0 = rk[0][1]; dt = t0 - rk[0][0]
    c = dict(cl, t0=t0, t1=t1, rk=[[t0, s0], [t1, round(s0 + (t1 - t0) * sp, 4)]])
    f = cl["focus"]
    if isinstance(f[0], list): c["focus"] = [[round(k[0] + dt, 4), k[1], k[2]] for k in f]
    return c


def subject_src(cl, t):
    m = json.load(open(cl["matte"]["file"][:-4] + ".json")); s = cl["rk"][0][1] + (t - cl["rk"][0][0]) * (cl["rk"][1][1] - cl["rk"][0][1]) / (cl["rk"][1][0] - cl["rk"][0][0])
    r = min([r for r in m["rows"] if r[1] > 0], key=lambda r: abs(r[0] - s)); return round(r[8], 1), round(r[9], 1)


SEG = 1.2; tests = [("invert", "0_032", "1_040", dict(pattern="I.I")),
                    ("invert", "0_028", "0_027", dict(pattern="IN.NB")),
                    ("cflash", "0_011", "1_034", dict()),
                    ("glitch", "0_042", "3_014", dict()),
                    ("spin", "0_060", "1_006", dict(deg=18)),
                    ("shutter", "0_078", "0_080", dict()),
                    ("rgb", "0_080", "0_050", dict(frames=6, px=30)),
                    ("pop", "0_061", "3_020", dict())]
clips, trans, words = [], [], []
for i, (ty, a, b, kw) in enumerate(tests):
    t0 = i * SEG; tc = round(t0 + SEG / 2, 4); t1 = round(t0 + SEG, 4)
    ka = len(clips); clips.append(retime(by[a], t0, tc)); kb = len(clips); clips.append(retime(by[b], tc, t1))
    tr = dict(type=ty, t=tc, **kw)
    if ty == "rgb": tr.update(clipA=ka, clipB=kb)
    if ty == "pop": sx, sy = subject_src(clips[kb], tc); tr.update(clip=kb, sx=sx, sy=sy)
    trans.append(tr)
    words.append(dict(text=f"{i + 1} {ty.upper()} {kw.get('pattern', '')}", t0=t0, t1=t1, style="cap", y=420, size=40, tracking=300))
plan = dict(name="transition_test", w=1080, h=1920, fps=30, dur=round(len(tests) * SEG, 4), band=v4["band"],
            audio=None, clips=clips, transitions=trans, words=words, hits=[], look=v4["look"],
            looks=[dict(t0=round(1 * SEG + SEG / 2, 4), t1=round(2 * SEG, 4), cc=dict(sat=0, con=40, exp=-0.4))])
json.dump(plan, open(os.path.join(HERE, "plan_ttest.json"), "w"), indent=1)
print("test reel:", len(clips), "clips,", len(trans), "transitions,", plan["dur"], "s")
