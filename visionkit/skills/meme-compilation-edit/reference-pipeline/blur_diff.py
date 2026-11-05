import json, os, sys
sys.path.insert(0, ".")
from extract_fx import decode_path
TPS = 254016000000
d = json.load(open("fx_delivered.json")); u = json.load(open("fx_user.json"))
mine = {m["name"]: m for m in d}; user = {m["name"]: m for m in u if m["name"] in mine}
ocr = {}
for l in open("img_ocr.jsonl"):
    r = json.loads(l); ocr[os.path.basename(r["file"]).replace(".webp.png", ".webp").replace(".WEBP.png", ".WEBP")] = r
def pv(c, n):
    for p in c["params"]:
        if p["name"] == n: return p
    return {}
def bx(pts):
    xs = [x for x, y in pts]; ys = [y for x, y in pts]
    return [round(min(xs), 3), round(min(ys), 3), round(max(xs), 3), round(max(ys), 3)]
def text_in(name, b):
    out = []
    for L in ocr[name]["lines"]:
        for w in L["words"]:
            cx, cy = (w["b"][0] + w["b"][2]) / 2, (w["b"][1] + w["b"][3]) / 2
            if b[0] <= cx <= b[2] and b[1] <= cy <= b[3]:
                out.append(w["t"])
    return " ".join(out)[:60]
def blurs(clip):
    mi = clip["media_in"]; out = []
    for c in clip["fx"]:
        if c["match"] not in ("AE.ADBE Gaussian Blur 2", "AE.ADBE Tint"): continue
        b = pv(c, "Blurriness")
        keys = [(round(int(k.split(",")[0]) / TPS - mi, 2), float(k.split(",")[1])) for k in (b.get("keys") or "").split(";") if k]
        e = {"inst": (c["instance"] or "").strip(), "blur": float(b["start"]) if b.get("start") else None, "keys": keys, "masks": []}
        for m in c["masks"]:
            p = pv(m, "Mask Path"); fe = pv(m, "Mask Feather").get("start")
            mm = {"feather": float(fe) if fe else None}
            inv = [q for q in m["params"] if q["name"] and "nvert" in q["name"].lower()]
            if p.get("keys"):
                mm["path"] = [(round(int(k.split(",")[0]) / TPS - mi, 2), bx(decode_path(k.split(",")[1]))) for k in p["keys"].split(";") if k]
            elif p.get("value_b64"):
                mm["box"] = bx(decode_path(p["value_b64"]))
            e["masks"].append(mm)
        out.append(e)
    return out
def same(a, b):
    if a["inst"] != b["inst"] or (a["blur"] or 0) != (b["blur"] or 0) or len(a["masks"]) != len(b["masks"]): return False
    if len(a["keys"]) != len(b["keys"]) or any(abs(x[0] - y[0]) > 0.04 or x[1] != y[1] for x, y in zip(a["keys"], b["keys"])): return False
    for ma, mb in zip(a["masks"], b["masks"]):
        if abs((ma["feather"] or 0) - (mb["feather"] or 0)) > 0.01: return False
        if ("box" in ma) != ("box" in mb): return False
        if "box" in ma and max(abs(x - y) for x, y in zip(ma["box"], mb["box"])) > 0.004: return False
        if "path" in ma:
            if len(ma["path"]) != len(mb["path"]): return False
            for (ta, ba), (tb, bb) in zip(ma["path"], mb["path"]):
                if abs(ta - tb) > 0.04 or max(abs(x - y) for x, y in zip(ba, bb)) > 0.004: return False
    return True
def desc(name, e):
    m = e["masks"][0] if e["masks"] else {}
    b = m.get("box") or (m.get("path") or [[0, [0, 0, 0, 0]]])[0][1]
    s = f"[{e['inst']}] blur {e['blur']} keys {e['keys']} feather {m.get('feather')} "
    s += f"box {b}" if "box" in m else f"wipe {[(t, bb[1]) for t, bb in m.get('path', [])]} x {b[0]}-{b[2]} bottom {b[3]}"
    return s + f"  «{text_in(name, b)}»" + ("" if len(e["masks"]) <= 1 else f" (+{len(e['masks']) - 1} more masks)")
shift = {}
for name in mine:
    A, B = blurs(mine[name]), blurs(user[name])
    used = set(); lines = []
    for a in A:
        hit = [k for k, b in enumerate(B) if k not in used and same(a, b)]
        if hit:
            used.add(hit[0]); continue
        lines.append("   - removed/changed: " + desc(name, a))
    for k, b in enumerate(B):
        if k not in used:
            lines.append("   + now:             " + desc(name, b))
    if lines:
        print(f"## {name}"); print("\n".join(lines))
