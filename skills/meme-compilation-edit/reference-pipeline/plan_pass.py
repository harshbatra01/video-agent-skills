"""Blur and crop plan for a "blur and crop pass" on a human editor's finished cut (Oct 13 2026).

The editor's timeline stays exactly as he made it (voice cuts on V1/A1 with +15 dB, meme slots on V3). This plans what goes
on each meme: the crop (house rules + the Oct 13 edge rules), the size, and the reveal and curse blurs with the editor's
soft settings. Output: data/edl_pass.json (one entry per V3 item, in timeline order) + data/edl_pass_report.txt.

Oct 13 2026 review notes applied here (the reviewer / the client, on our full edit):
  - "the blurs arent supposed to have a rigid end of them, it should be soft" / "the blurs itself shouldnt have edges":
    every mask gets the editor's feather, 10 px in the image's own pixels (ours were 1.5-6 px, 2-6 px on screen).
  - "the memes swearwords are also blurred too aggressively, can you check [the editor's] files?": curse boxes keep the editor's
    strength but get his soft 10 px feather and at least 5 image px of padding (tightbox.py).
  - "Like this is way too big / sloppy" (a reveal box on a slanted shop sign): a one-line box on slanted text follows
    the text's own outline (four corners from the OCR), not a big upright rectangle around it.
  - "you need to make sure the edges of memes are cut properly": unread panels at the bottom of a stacked meme and the
    carousel-dots pill on phone screenshots come off (crop_util.unread_tail_crop, carousel_pill).
"""
import json, os, re, sys
import numpy as np
from PIL import Image

sys.path.insert(0, ".")
from tightbox import tight_word_box
from plan_blurs import plan, words_of
import crop_util as cu
from crop_util import (auto_crop, ocr_path, phone_crop, meta_crop, balance_margins, watermark_bar, tighten_margins,
                       unread_tail_crop, carousel_pill)

FPS = 30
CLIENT = cu.CLIENT
FEATHER = 10.0                      # mask feather in image pixels (the editor's files: every mask is 10)
FEATHER_MIN_SCREEN = 20.0           # and never under 20 px on screen (check frames, Oct 13 2026: on phone screenshots shown
                                    # at 40-90% a flat 10 image px was 7-9 px on screen and a half-revealed line still
                                    # looked cut, the "rigid end" from the review)

def feather_for(sc):
    return round(max(FEATHER, FEATHER_MIN_SCREEN / sc), 2)
SEQ_W, SEQ_H, TARGET_H, MAX_W = 1920, 1080, 980, 1740

SEQ = "CHANGE_ME sequence"          # the editor's sequence name
T = json.load(open("data/editor_timeline.json"))
V1, V3 = T["V1"], T["V3"]
P = json.load(open("pieces_asr.json"))
assert len(P) == len(V1), (len(P), len(V1))
db = np.load("data/db10ms.npy")
dec = json.load(open("decisions_pass.json")) if os.path.exists("decisions_pass.json") else {}
over = dec.get("memes", {})
TOTAL = V1[-1]["end"]

ocr = {}
for l in open("img_ocr.jsonl"):
    r = json.loads(l)
    n = os.path.basename(r["file"])
    for ext in (".webp.png", ".WEBP.png", ".gif.png", ".GIF.png", ".mp4.png"):
        if n.endswith(ext):
            n = n[: -4]
    ocr[n] = r


def raw_to_out(t):
    """recording time -> sequence time, through the editor's voice clips"""
    for c in V1:
        a = c["in"]; b = a + c["end"] - c["start"]
        if a - 1e-6 <= t <= b + 1e-6:
            return c["start"] + (t - a)
    nxt = [c for c in V1 if c["in"] > t]
    return nxt[0]["start"] if nxt else TOTAL


def onset_after(t, window=0.45, th=-60):
    i0 = int(round(t * 100))
    for i in range(i0, min(len(db), i0 + int(window * 100))):
        if db[i] > th:
            return i / 100
    return t


def onset_near(t, lo=-0.35, hi=0.25):
    for i in range(max(6, int((t + lo) * 100)), min(len(db), int((t + hi) * 100))):
        if db[i] > -58 and db[i - 6:i].max() < -60:
            return i / 100
    return t


def block_box(img, lines, padx=0.012, pad_line=0.35, extra=None):
    x0 = min(L["b"][0] for L in lines); x1 = max(L["b"][2] for L in lines)
    y0 = min(L["b"][1] for L in lines); y1 = max(L["b"][3] for L in lines)
    lh = float(np.median([L["b"][3] - L["b"][1] for L in lines]))
    others = [L for L in ocr[img]["lines"] if L not in lines]
    above = [L["b"][3] for L in others if L["b"][3] <= y0 + 0.004 and L["b"][2] > x0 and L["b"][0] < x1]
    below = [L["b"][1] for L in others if L["b"][1] >= y1 - 0.004 and L["b"][2] > x0 and L["b"][0] < x1]
    top = y0 - pad_line * lh
    if above and max(above) > top:
        top = (max(above) + y0) / 2
    bot = y1 + pad_line * lh
    if below and min(below) < bot:
        bot = (min(below) + y1) / 2
    box = [x0 - padx, top, x1 + padx, bot]
    if extra:
        box[2] = max(box[2], extra.get("x1", box[2])); box[3] = max(box[3], extra.get("y1", box[3]))
    return [round(float(v), 4) for v in box]


def slanted_quad(img, L, padx=0.012, pad_line=0.35):
    """Four-corner outline around one slanted text line (a shop sign in a photo), padded along and across the text.
    None when the line is level (an upright box fits it already)."""
    q = L.get("q")
    if not q:
        return None
    W, H = ocr[img]["w"], ocr[img]["h"]
    pts = np.array([[x * W, y * H] for x, y in q], float)            # TL, TR, BR, BL in pixels
    along = pts[1] - pts[0]
    if abs(along[0]) < 1 or abs(along[1] / along[0]) < 0.03:
        return None
    u = along / np.linalg.norm(along)
    v = np.array([-u[1], u[0]])                                       # across the text, pointing down the page
    if v[1] < 0:
        v = -v
    lh = float(np.dot(pts[3] - pts[0], v))
    px, py = padx * W, pad_line * lh
    out = [pts[0] - u * px - v * py, pts[1] + u * px - v * py, pts[2] + u * px + v * py, pts[3] - u * px + v * py]
    return [[round(float(x / W), 4), round(float(y / H), 4)] for x, y in out]


def media_seconds(path):
    import subprocess
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True).stdout.strip()
    return float(out or 0)


images, report = [], []
for idx, it in enumerate(V3):
    name = it["name"]
    s, e = it["start"], it["end"]
    entry = {"idx": idx, "file": name, "start": s, "end": e, "in": it["in"], "speed": it["speed"]}
    if name not in ocr:                                               # a nested sequence: left as the editor made it
        entry["skip"] = True
        images.append(entry)
        report.append(f"{s:8.2f}-{e:8.2f} {name[:44]:44s} (left as the editor made it)")
        continue
    ov = over.get(name, {})
    W, H = ocr[name]["w"], ocr[name]["h"]
    ks = [k for k, c in enumerate(V1) if c["start"] >= s - 0.02 and c["end"] <= e + 0.02]
    spoken_words = [ww for k in ks for w in P[k]["words"] for ww in words_of(w["w"])]
    timed = []
    for k in ks:
        for w in P[k]["words"]:
            for ww in words_of(w["w"]):
                timed.append((ww, max(w["s"], P[k]["a"]), w["e"]))

    # ---- crop ----
    crop = ov.get("crop") or meta_crop(name, ocr[name], phone_crop(name, ocr[name]) if H / W > 1.8 and W >= 1000 else auto_crop(name),
                                       spoken=spoken_words)
    if not ov.get("crop"):
        wb = watermark_bar(name)                                     # the iFunny bar along the bottom edge
        if wb > crop["B"]:
            crop = dict(crop, B=wb)
        before = dict(crop)
        crop = unread_tail_crop(name, crop, spoken_words)            # unread panels at the bottom (Oct 13 2026)
        crop = carousel_pill(name, crop)                              # carousel dots on phone screenshots (Oct 13 2026)
        if crop != before:
            entry["edge_rule"] = True
    if not ov.get("keep_crop"):
        crop = balance_margins(name, crop)
    if not ov.get("crop") and (crop["T"] or crop["B"]):
        full_h = H * (1 - (crop["T"] + crop["B"]) / 100); full_w = W * (1 - (crop["L"] + crop["R"]) / 100)
        if TARGET_H / H * full_w > MAX_W and TARGET_H / full_h * full_w > MAX_W:
            ph = meta_crop(name, ocr[name], {"L": crop["L"], "T": 0.0, "R": crop["R"], "B": 0.0}, spoken=spoken_words)
            keep_b = max(ph["B"], unread_tail_crop(name, dict(crop, T=0.0, B=0.0), spoken_words)["B"])
            crop = dict(crop, T=ph["T"], B=keep_b)
    if not ov.get("crop") and not ov.get("keep_crop"):
        before = dict(crop)
        crop = tighten_margins(name, crop)                            # too much white space (Oct 11 2026)
        if crop != before:
            entry["tightened"] = True

    # ---- size ----
    vis_w = W * (1 - (crop["L"] + crop["R"]) / 100); vis_h = H * (1 - (crop["T"] + crop["B"]) / 100)
    sc = TARGET_H / vis_h
    if vis_w * sc > MAX_W:
        sc = MAX_W / vis_w
    cx = (crop["L"] + 100 - crop["R"]) / 200; cy = (crop["T"] + 100 - crop["B"]) / 200
    pos = [0.5 - (cx - 0.5) * W * sc / SEQ_W, 0.5 - (cy - 0.5) * H * sc / SEQ_H]
    if ov.get("scale"):
        sc, pos = ov["scale"] / 100, list(ov["pos"])

    # ---- blurs ----
    blocks, auto = ([], []) if ov.get("no_auto") else plan(ocr[name]["lines"], timed)
    piece_starts = [P[k]["a"] for k in ks]

    def piece_start(t):
        for a in piece_starts:
            if abs(t - a) < 0.02:
                return a
        return None

    def first_text(b):
        return (b.get("lines") or [{"t": b.get("word", "")}])[0]["t"]

    specs = [b for b in auto if not (ov.get("no_auto_reveals") and b["kind"] != "curse")
             and not any(first_text(b).startswith(p) for p in ov.get("drop_prefix", []))
             and not (b["kind"] == "curse" and b.get("word") in ov.get("drop_curse", []))]
    specs += ov.get("add", [])
    first_reveal = min([b for b in specs if b["kind"] in ("wipe", "box")], key=lambda b: b.get("raw_first", b.get("raw_t", 1e9)), default=None)
    blurs = []
    for b in specs:
        if b["kind"] == "curse":
            if "words" in b:
                ws = [w["b"] for L in ocr[name]["lines"] for w in L["words"] if w["t"] in b["words"]]
                b["word_box"] = [min(w[0] for w in ws), min(w[1] for w in ws), max(w[2] for w in ws), max(w[3] for w in ws)]
            box, fe = tight_word_box(ocr_path(name), b["word_box"], sc)
            blurs.append({"kind": "curse", "box": box, "feather": fe, "label": b.get("word", "")})
            continue
        lines = b.get("lines") or ([ocr[name]["lines"][k] for k in b["line_idx"]] if "line_idx" in b else
                                   [L for L in ocr[name]["lines"] if any(L["t"].startswith(p) for p in b.get("prefixes", []))])
        box = b.get("box") or block_box(name, lines, extra=b.get("extra"))
        label = lines[0]["t"] if lines else b.get("label", "")
        if b["kind"] == "box":
            if len(lines) == 1 and not b.get("box"):
                q = slanted_quad(name, lines[0])
                if q:
                    box = q                                           # follows the slant of a sign in a photo
            rt = b["raw_t"]
            ps = piece_start(rt)
            on = onset_after(ps) if ps is not None else onset_near(rt)
            t = max(0.0, round((raw_to_out(on) - s - 0.05) * FPS) / FPS)
            nl = b.get("n_lines") or len(lines) or 1
            if b.get("snap"):
                snap = b["snap"]
            elif nl <= 1:
                snap = max(4, min(9, round((b.get("spoken") or 0.5) * FPS * 0.25)))
            else:
                snap = max(15, min(66, round(nl * 0.35 * FPS)))
                if b.get("spoken"):
                    snap = min(snap, max(15, round(b["spoken"] * FPS * 0.8)))
            blurs.append({"kind": "box", "box": box, "feather": feather_for(sc), "keys": [[round(t, 4), 40.0], [round(t + snap / FPS, 4), 0.0]], "label": label})
        else:
            t0 = max(0.0, round((raw_to_out(onset_near(b["raw_first"])) - s - 0.05) * FPS) / FPS)
            if b is first_reveal and b.get("n_lines_block", 0) >= 3 and not b.get("later"):
                tb = raw_to_out(onset_near(b.get("raw_block") or b["raw_first"])) - s
                if tb <= 1.5:
                    t0 = 0.0
            if b.get("raw_end"):
                t1 = raw_to_out(b["raw_end"]) - s + 0.25
            else:
                t1 = raw_to_out(onset_near(b["raw_last"])) - s + 0.25
            t1 = max(t0 + 15 / FPS, round(t1 * FPS) / FPS)
            blurs.append({"kind": "wipe", "box": box, "feather": feather_for(sc), "path_keys": [round(t0, 4), round(t1, 4)], "label": label})

    def bbox_of(bx):
        if len(bx) == 4 and isinstance(bx[0], (list, tuple)):
            xs = [p[0] for p in bx]; ys = [p[1] for p in bx]
            return [min(xs), min(ys), max(xs), max(ys)]
        return bx
    vis = (crop["L"] / 100, crop["T"] / 100, 1 - crop["R"] / 100, 1 - crop["B"] / 100)
    blurs = [bl for bl in blurs if (bbox_of(bl["box"])[2] > vis[0] + 0.005 and bbox_of(bl["box"])[0] < vis[2] - 0.005 and
                                    bbox_of(bl["box"])[3] > vis[1] + 0.005 and bbox_of(bl["box"])[1] < vis[3] - 0.005)]
    dur = e - s
    for bl in blurs:                                                  # keys never run past the meme's slot
        if bl["kind"] == "box":
            bl["keys"] = [[min(k[0], round(dur - 2 / FPS, 4)), k[1]] for k in bl["keys"]]
        if bl["kind"] == "wipe":
            bl["path_keys"] = [min(bl["path_keys"][0], round(dur - 16 / FPS, 4)), min(bl["path_keys"][1], round(dur - 1 / FPS, 4))]
    starts_ = sorted((bl["keys"][0][0] if bl["kind"] == "box" else bl["path_keys"][0], id(bl)) for bl in blurs if bl["kind"] in ("box", "wipe"))
    for bl in blurs:
        if bl["kind"] != "wipe":
            continue
        t0, t1 = bl["path_keys"]
        nxt = [st for st, ident in starts_ if ident != id(bl) and st > t0 + 0.3]
        if nxt:
            ns = min(nxt)
            if ns - t1 <= 1.0 or t1 > ns:
                t1 = max(t0 + 15 / FPS, ns)
        bl["path_keys"] = [t0, round(round(t1 * FPS) / FPS, 4)]
    path = ov.get("path", CLIENT + name)
    entry.update({"path": path, "w": W, "h": H, "crop": crop, "scale": round(sc * 100, 4),
                  "pos": [round(float(pos[0]), 5), round(float(pos[1]), 5)], "blurs": blurs,
                  "video": name.lower().endswith((".mp4", ".gif")), "words": " ".join(w for w, _, _ in timed)[:160]})
    images.append(entry)
    report.append(f"{s:8.2f}-{e:8.2f} {name[:44]:44s} crop " + " ".join(f"{k}{crop[k]:g}" for k in "LTRB") +
                  f" sc {sc * 100:.1f} | " + " | ".join(f"{b['kind']}:{b['label'][:22]}" for b in blurs))

json.dump({"fps": FPS, "seq": SEQ, "images": images}, open("data/edl_pass.json", "w"), indent=1)
open("data/edl_pass_report.txt", "w").write("\n".join(report))
nb = sum(len(i.get("blurs", [])) for i in images)
kinds = {}
for i in images:
    for b in i.get("blurs", []):
        kinds[b["kind"]] = kinds.get(b["kind"], 0) + 1
crops = sum(1 for i in images if not i.get("skip") and any(i["crop"][k] for k in "LTRB"))
print(f"{len(images)} meme slots, {crops} with a crop, {nb} masks {kinds}")
