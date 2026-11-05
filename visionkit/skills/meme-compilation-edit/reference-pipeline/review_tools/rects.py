import json, os, sys
sys.path.insert(0, ".")
fd = {m["name"]: m for m in json.load(open("fx_delivered.json"))}
fu = {m["name"]: m for m in json.load(open("fx_user.json"))}
edl = json.load(open("../data/edl_full.json"))
size = {}
for im in edl["images"]:
    n = os.path.basename(im["path"]); size[n] = (im["w"], im["h"])
def pv(c, n):
    for p in c["params"]:
        if p["name"] == n: return p
    return {}
def geo(clip):
    w, h = size.get(clip["name"], (None, None))
    if w is None:
        for k, v in size.items():
            if clip["name"].startswith(k[:20]): w, h = v
    crop = {"Left": 0, "Top": 0, "Right": 0, "Bottom": 0}; sc = 100.0; pos = (0.5, 0.5); anc = (0.5, 0.5)
    for c in clip["fx"]:
        if c["match"] == "AE.ADBE AECrop":
            crop = {k: float(pv(c, k).get("start") or 0) for k in crop}
        if c["match"] == "AE.ADBE Motion":
            s = pv(c, "Scale").get("start"); sc = float(s) if s else 100.0
            p = pv(c, "Position").get("start"); pos = tuple(map(float, p.split(":"))) if p else pos
            a = pv(c, "Anchor Point").get("start"); anc = tuple(map(float, a.split(":"))) if a else anc
            u = pv(c, "Uniform Scale").get("start")
    k = sc / 100
    L = pos[0]*1920 + (crop["Left"]/100 - anc[0]) * w * k
    R = pos[0]*1920 + (1 - crop["Right"]/100 - anc[0]) * w * k
    T = pos[1]*1080 + (crop["Top"]/100 - anc[1]) * h * k
    B = pos[1]*1080 + (1 - crop["Bottom"]/100 - anc[1]) * h * k
    return [round(L), round(T), round(R), round(B)], crop, sc, pos, anc
rows = []
for n, a in fd.items():
    ga = geo(a); gb = geo(fu[n])
    rows.append((n, ga, gb))
    ra, rb = ga[0], gb[0]
    if ra != rb:
        print(f"{n[:40]:40s} mine {ra} h{ra[3]-ra[1]} w{ra[2]-ra[0]} | his {rb} h{rb[3]-rb[1]} w{rb[2]-rb[0]}  anc {tuple(round(x,3) for x in gb[4])}")
json.dump([(n, ga[0], gb[0], ga[1], gb[1]) for n, ga, gb in rows], open("rects.json", "w"))
import collections
print("\nHIS visible heights:", sorted(r[2][3]-r[2][1] for r in rows)[:10], "...", sorted(r[2][3]-r[2][1] for r in rows)[-10:])
print("HIS top margins:", collections.Counter(r[2][1] for r in rows).most_common(8))
print("HIS bottom margins:", collections.Counter(1080 - r[2][3] for r in rows).most_common(8))
