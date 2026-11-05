import json, os, sys
sys.path.insert(0, ".")
from tl import TL, TPS, TPF
from extract_fx import decode_path
D = TL("delivered.xml"); U = TL("user.xml")
fd = {m["name"]: m for m in json.load(open("fx_delivered.json"))}
fu = {m["name"]: m for m in json.load(open("fx_user.json"))}
ocr = {}
for l in open("../data/img_ocr.jsonl"):
    r = json.loads(l); ocr[os.path.basename(r["file"]).replace(".webp.png", ".webp").replace(".WEBP.png", ".WEBP").replace(".mp4.png", ".mp4")] = r
for l in open("../data/video_ocr.jsonl"):
    r = json.loads(l); ocr[os.path.basename(r["file"]).replace(".mp4.png", ".mp4")] = r
edl = json.load(open("../data/edl_full.json"))
spec = {os.path.basename(im["path"]): im for im in edl["images"]}
def pv(c, n):
    for p in c["params"]:
        if p["name"] == n: return p
    return {}
def bx(pts):
    xs = [x for x, y in pts]; ys = [y for x, y in pts]
    return [round(min(xs), 3), round(min(ys), 3), round(max(xs), 3), round(max(ys), 3)]
def text_in(name, b):
    r = ocr.get(name.replace(" (H264)", ""))
    if not r: return "?"
    out = []
    for L in r["lines"]:
        for w in L["words"]:
            cx, cy = (w["b"][0] + w["b"][2]) / 2, (w["b"][1] + w["b"][3]) / 2
            if b[0] <= cx <= b[2] and b[1] <= cy <= b[3]: out.append(w["t"])
    return " ".join(out)[:70]
def raw_of(T, clip, media_ticks):
    """media time of a key -> raw recording seconds (what he is saying then)"""
    seq_t = clip["start"] * TPS + (media_ticks - clip["media_in"] * TPS) / clip.get("speed", 1)
    r = T.seq_to_raw(seq_t)
    return round(r, 2) if r is not None else None
def blurs(T, clip):
    out = []
    for c in clip["fx"]:
        if c["match"] not in ("AE.ADBE Gaussian Blur 2", "AE.ADBE Tint"): continue
        b = pv(c, "Blurriness")
        keys = [(raw_of(T, clip, int(k.split(",")[0])), float(k.split(",")[1])) for k in (b.get("keys") or "").split(";") if k]
        e = {"inst": (c["instance"] or "").strip(), "blur": float(b["start"]) if b.get("start") else None, "keys": keys, "masks": []}
        dims = pv(c, "Blur Dimensions").get("start"); rep = pv(c, "Repeat Edge Pixels").get("start")
        e["dims"] = dims; e["rep"] = rep
        for m in c["masks"]:
            p = pv(m, "Mask Path"); fe = pv(m, "Mask Feather").get("start")
            mm = {"feather": float(fe) if fe else None, "exp": pv(m, "Mask Expansion").get("start"), "op": pv(m, "Mask Opacity").get("start")}
            inv = [q for q in m["params"] if q["name"] and "nvert" in q["name"].lower()]
            mm["inv"] = inv[0].get("start") if inv else None
            if p.get("keys"):
                mm["path"] = [(raw_of(T, clip, int(k.split(",")[0])), bx(decode_path(k.split(",")[1]))) for k in p["keys"].split(";") if k]
            elif p.get("value_b64"):
                mm["box"] = bx(decode_path(p["value_b64"]))
            e["masks"].append(mm)
        out.append(e)
    return out
def crop(clip):
    for c in clip["fx"]:
        if c["match"] == "AE.ADBE AECrop":
            return {k: round(float(pv(c, k).get("start") or 0), 2) for k in ("Left", "Top", "Right", "Bottom")}
    return None
def motion(clip):
    for c in clip["fx"]:
        if c["match"] == "AE.ADBE Motion":
            sc = pv(c, "Scale").get("start"); pos = pv(c, "Position").get("start")
            return round(float(sc), 2) if sc else 100.0, pos
def desc_blur(name, e):
    s = f"[{e['inst']}] blur {e['blur']} keys {e['keys']}"
    for m in e["masks"]:
        b = m.get("box") or m["path"][0][1]
        if "box" in m: s += f" | box {b} fe {m['feather']}"
        else: s += f" | WIPE {[(t, bb[1]) for t, bb in m['path']]} x {b[0]}-{b[2]} bottom {b[3]} fe {m['feather']}"
        if m["inv"] not in (None, "false"): s += f" inv {m['inv']}"
        s += f" «{text_in(name, b)}»"
    if not e["masks"]: s += " (NO MASK)"
    return s
if __name__ == "__main__":
    uclips = fu
    report = []
    for name, a in fd.items():
        b = uclips[name]
        sa = TL.seq_to_raw(D, a["start"] * TPS + 1); sb = TL.seq_to_raw(U, b["start"] * TPS + 1)
        ea = TL.seq_to_raw(D, a["end"] * TPS - 1); eb = TL.seq_to_raw(U, b["end"] * TPS - 1)
        lines = []
        if sa is None or sb is None or abs(sa - sb) > 0.04 or abs(ea - eb) > 0.04:
            lines.append(f"   span raw {sa:.2f}-{ea:.2f} -> {sb:.2f}-{eb:.2f}  (seq {a['start']:.2f}-{a['end']:.2f} -> {b['start']:.2f}-{b['end']:.2f})")
        ca, cb = crop(a), crop(b)
        if ca != cb: lines.append(f"   crop {ca} -> {cb}")
        ma, mb = motion(a), motion(b)
        if ma != mb: lines.append(f"   motion scale/pos {ma} -> {mb}")
        A, B = blurs(D, a), blurs(U, b)
        if json.dumps(A) != json.dumps(B):
            for e in A: lines.append("   - " + desc_blur(name, e))
            for e in B: lines.append("   + " + desc_blur(name, e))
        if lines:
            sp = spec.get(name.replace(" (H264)", ""), {})
            report.append(f"\n## {name}  [{sp.get('w')}x{sp.get('h')}] his seq {b['start']:.2f}s")
            report += lines
    open("meme_diff.txt", "w").write("\n".join(report))
    print(len([l for l in report if l.startswith("\n## ")]), "memes changed")
