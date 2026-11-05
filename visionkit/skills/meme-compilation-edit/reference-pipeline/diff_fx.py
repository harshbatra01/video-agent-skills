import json, sys
sys.path.insert(0, ".")
from extract_fx import decode_path
TPS = 254016000000
d = json.load(open("fx_delivered.json")); u = json.load(open("fx_user.json"))
mine = {m["name"]: m for m in d}
user = {m["name"]: m for m in u if m["name"] in mine}

def pv(c, name):
    for p in c["params"]:
        if p["name"] == name:
            return p
    return {}

def keys(p, mi):
    out = []
    for k in (p.get("keys") or "").split(";"):
        if not k: continue
        f = k.split(",")
        out.append((round(int(f[0]) / TPS - mi, 2), f[1]))
    return out

def box(pts):
    xs = [x for x, y in pts]; ys = [y for x, y in pts]
    return [round(min(xs), 3), round(min(ys), 3), round(max(xs), 3), round(max(ys), 3)]

def mask_info(m, mi):
    p = pv(m, "Mask Path")
    info = {"feather": pv(m, "Mask Feather").get("start"), "expansion": pv(m, "Mask Expansion").get("start"),
            "opacity": pv(m, "Mask Opacity").get("start")}
    if p.get("keys"):
        info["path_keys"] = [(round(int(k.split(",")[0]) / TPS - mi, 2), box(decode_path(k.split(",")[1])))
                             for k in p["keys"].split(";") if k]
    elif p.get("value_b64"):
        info["box"] = box(decode_path(p["value_b64"]))
    inv = [q for q in m["params"] if q["name"] and "nvert" in q["name"]]
    if inv: info["inverted"] = inv[0].get("start")
    return info

def summary(clip):
    mi = clip["media_in"]
    s = {"fx": []}
    for c in clip["fx"]:
        e = {"match": c["match"].replace("AE.ADBE ", ""), "instance": c["instance"]}
        if c["match"] == "AE.ADBE Motion":
            e.update({k: pv(c, k).get("start") for k in ("Scale", "Position", "Anchor Point")})
        elif c["match"] == "AE.ADBE AECrop":
            e.update({k: pv(c, k).get("start") for k in ("Left", "Top", "Right", "Bottom")})
        elif c["match"] in ("AE.ADBE Gaussian Blur 2", "AE.ADBE Tint"):
            b = pv(c, "Blurriness")
            e["blur"] = b.get("start"); e["blur_keys"] = keys(b, mi)
            e["masks"] = [mask_info(m, mi) for m in c["masks"]]
        elif c["match"] not in ("AE.ADBE Opacity",):
            e["params"] = {p["name"]: p.get("start") for p in c["params"] if p["name"] and p.get("start")}
        if c["match"] != "AE.ADBE Opacity" or pv(c, "Opacity").get("start") not in (None, "100."):
            s["fx"].append(e)
    return s

out = []
for name, a in mine.items():
    b = user[name]
    sa, sb = summary(a), summary(b)
    if json.dumps(sa) == json.dumps(sb):
        continue
    out.append(f"\n## {name}  (now at {b['start']:.2f}s in the merged timeline)")
    fa = [(e["match"], e["instance"]) for e in sa["fx"]]; fb = [(e["match"], e["instance"]) for e in sb["fx"]]
    if fa != fb:
        out.append(f"   effects: {fa}\n        ->  {fb}")
    # pair effects by order within the same match type
    for typ in sorted(set(e["match"] for e in sa["fx"] + sb["fx"])):
        xa = [e for e in sa["fx"] if e["match"] == typ]; xb = [e for e in sb["fx"] if e["match"] == typ]
        for k in range(max(len(xa), len(xb))):
            ea = xa[k] if k < len(xa) else None; eb = xb[k] if k < len(xb) else None
            if json.dumps(ea) != json.dumps(eb):
                out.append(f"   {typ} #{k}:\n      was {json.dumps(ea)}\n      now {json.dumps(eb)}")
print("\n".join(out))
print("\nchanged memes:", sum(1 for l in out if l.startswith("\n## ")), "of", len(mine))
