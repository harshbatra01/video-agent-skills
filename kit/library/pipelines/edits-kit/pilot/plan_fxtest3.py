"""FX test reel 3: research pass 2 techniques (fx_lib section 14 + recipe T/V + silstack P + outline type) on real
Yamal clips from plan_v8.json. Writes plan_fxtest3.json; render and check every frame before using them in an edit.
"""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
v8 = json.load(open(os.path.join(HERE, "plan_v8.json")))
by = {}
for c in v8["clips"]: by.setdefault(c["name"].split(" ")[0] if not c["name"].startswith("goal") else c["name"], c)


def retime(cl, t0, t1, at=None):
    """the clip from its own start (or from edit time `at` of its original slot) placed at t0..t1"""
    rk = cl["rk"]; sp = (rk[-1][1] - rk[0][1]) / (rk[-1][0] - rk[0][0])
    a0 = rk[0][0] if at is None else at
    s0 = rk[0][1] + (a0 - rk[0][0]) * sp; dt = t0 - a0
    c = dict(cl, t0=t0, t1=t1, rk=[[t0, round(s0, 4)], [t1, round(s0 + (t1 - t0) * sp, 4)]], smooth=False)
    f = cl["focus"]
    if isinstance(f[0], list): c["focus"] = [[round(k[0] + dt, 4), k[1], k[2]] for k in f]
    return c


def subj(cl, t):
    m = json.load(open(cl["matte"]["file"][:-4] + ".json")); rk = cl["rk"]
    s = rk[0][1] + (t - rk[0][0]) * (rk[-1][1] - rk[0][1]) / (rk[-1][0] - rk[0][0])
    r = min([r for r in m["rows"] if r[1] > 0], key=lambda r: abs(r[0] - s))
    return round(r[8], 1), round(r[9] + 0.3 * (r[3] - r[9]), 1)


clips, trans, hits, words, labels = [], [], [], [], []
T = 0.0
def seg(name, dur, at=None):
    global T
    k = len(clips); clips.append(retime(by[name], round(T, 4), round(T + dur, 4), at)); T = round(T + dur, 4); return k

# 1 impact frames on a cut (inverted threshold, then threshold)
a = seg("0_032", 0.6); b = seg("1_040", 0.6); trans.append(dict(type="recipe", t=clips[b]["t0"], pattern="VT")); labels.append((clips[a]["t0"], "1 IMPACT FRAMES V T"))
# 2 poster silhouette stack (black player on white, then white on black)
a = seg("0_060", 0.6); b = seg("0_011", 0.7); trans.append(dict(type="silstack", t=clips[b]["t0"], clipB=b, pattern="PPK")); labels.append((clips[a]["t0"], "2 POSTER P P K"))
# 3 type flash
a = seg("0_042", 0.6); b = seg("3_014", 0.6); trans.append(dict(type="typeflash", t=clips[b]["t0"] - 2 / 30, word="NOW", pattern="WB", size=520)); labels.append((clips[a]["t0"], "3 TYPE FLASH"))
# 4 freeze clone across a run (one direction)
k = seg("0_078", 1.6); t0 = clips[k]["t0"]
trans.append(dict(type="freezeclone", clip=k, times=[t0 + 0.27, t0 + 0.6, t0 + 0.93], t_end=t0 + 1.27)); hits.append(dict(t=t0 + 1.27, sil=dict(clip=k, frames=[0, 2], glow=45)))
labels.append((t0, "4 FREEZE CLONE"))
# 5 ghost trail on a dribble
k = seg("3_017", 1.4); t0 = clips[k]["t0"]; trans.append(dict(type="ghost", clip=k, t0=t0 + 0.2, t1=t0 + 1.0, n=6, dt=0.05)); labels.append((t0, "5 GHOST TRAIL"))
# 6 pop-up freeze on the finish
k = seg("0_050", 1.4); t0 = clips[k]["t0"]; sx, sy = subj(clips[k], t0 + 0.5)
trans.append(dict(type="popfreeze", clip=k, t=t0 + 0.5, frames=9, sx=sx, sy=sy)); hits.append(dict(t=t0 + 0.5 + 9 / 30, shake=[22, 0.3]))
labels.append((t0, "6 POP FREEZE"))
# 7 photo print of the celebration
k = seg("goal celebration", 1.6); t0 = clips[k]["t0"]; trans.append(dict(type="print", clip=k, t=t0 + 0.5, frames=16, label="EURO 2024  ·  SEMI-FINAL  ·  FRANCE")); labels.append((t0, "7 PHOTO PRINT"))
# 8 numeral sandwich: hollow numeral behind him, heavy word in front, small label
k = seg("2_006", 1.6); t0 = clips[k]["t0"]
words.append(dict(text="10", t0=t0 + 0.2, t1=t0 + 1.6, style="outline", size=720, y=1240, behind=k, color=[1, 0.82, 0.3], stroke=7))
words.append(dict(text="YAMAL", t0=t0 + 0.35, t1=t0 + 1.6, style="hero", font="Coolvetica-HeavyComp", size=250, y=1290, depth_color=[0.62, 0.05, 0.18]))
words.append(dict(text="FC BARCELONA  ·  NUMBER 10", t0=t0 + 0.45, t1=t0 + 1.6, style="cap", y=1402, size=30))
labels.append((t0, "8 NUMERAL SANDWICH"))
for t_, s_ in labels: words.append(dict(text=s_, t0=round(t_, 4), t1=round(t_ + 0.5, 4), style="cap", y=420, size=34, tracking=200))
plan = dict(name="fx_test3", w=1080, h=1920, fps=30, dur=round(T, 4), band=v8["band"], audio=None,
            clips=clips, transitions=trans, hits=hits, words=words, look=v8["look"])
json.dump(plan, open(os.path.join(HERE, "plan_fxtest3.json"), "w"), indent=1)
print("fx test 3:", len(clips), "clips,", round(T, 2), "s;", [l[1] for l in labels])
