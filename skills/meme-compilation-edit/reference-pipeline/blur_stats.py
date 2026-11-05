"""Mask statistics per effect instance name across projects.
usage: python blur_stats.py "TAG=fx_file.json" ...   (fx files from extract_fx.py)"""
import json, sys, os, collections, statistics
sys.path.insert(0, ".")
from extract_fx import decode_path
def pval(c, name):
    for p in c["params"]:
        if p["name"] == name: return p
    return {}
def bbox(pts):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; return [min(xs), min(ys), max(xs), max(ys)]
def rows_of(fxfile):
    out = []
    for m in json.load(open(fxfile)):
        scale = 100.0
        for c in m["fx"]:
            if c["match"] == "AE.ADBE Motion":
                v = pval(c, "Scale").get("start"); scale = float(v) if v else 100.0
        for c in m["fx"]:
            if "Gaussian" not in (c["match"] or ""): continue
            b = pval(c, "Blurriness"); rep = pval(c, " ").get("start")
            for mk in c["masks"]:
                path = pval(mk, "Mask Path")
                if path.get("value_b64"): pts = decode_path(path["value_b64"])
                elif path.get("keys"): pts = decode_path(path["keys"].split(";")[0].split(",")[1])
                else: pts = None
                out.append({"file": m["name"], "inst": c["instance"], "blur": b.get("start"), "blur_keys": b.get("keys", "")[:60],
                            "repeat_edges": rep, "feather": float(pval(mk, "Mask Feather").get("start") or 0),
                            "expansion": float(pval(mk, "Mask Expansion").get("start") or 0), "scale": scale,
                            "animated_path": bool(path.get("keys")), "bbox": bbox(pts) if pts else None})
    return out
PAIRS = [a.split("=", 1) for a in sys.argv[1:]] or [["EDITOR job A", "fx_editor_a.json"], ["EDITOR job B", "fx_editor_b.json"], ["MINE", "fx_mine.json"]]
for tag, f in PAIRS:
    R = rows_of(f)
    print("==", tag, len(R), "masks")
    by = collections.defaultdict(list)
    for r in R: by[r["inst"]].append(r)
    for inst, L in sorted(by.items(), key=lambda kv: -len(kv[1])):
        fe = [r["feather"] for r in L]; sc = [r["feather"] * r["scale"] / 100 for r in L]
        blurs = collections.Counter((r["blur"], r["blur_keys"][:25]) for r in L).most_common(3)
        print(f"  {inst!r:28s} n={len(L):3d} feather src med {statistics.median(fe):5.1f} (min {min(fe):.1f} max {max(fe):.1f}) | on screen med {statistics.median(sc):5.1f} | expansion {collections.Counter(r['expansion'] for r in L).most_common(2)} | repeat edges {collections.Counter(r['repeat_edges'] for r in L).most_common(2)} | blur {blurs}")
    json.dump(R, open(f.replace("fx_", "masks_"), "w"))
