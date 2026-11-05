"""Edit decision list for a full meme-compilation edit.

Inputs: assign.json (every phrase, its meme, flags), decisions.json (my review: cuts, reassignments,
per-meme overrides), OCR, loudness envelope. Output: edl_full.json in the same shape the build
and patch scripts use (cuts, images with crop/scale/pos/blurs), plus a printed summary.
"""
import json, os, math, re, subprocess, sys
import numpy as np
from PIL import Image
sys.path.insert(0, ".")
from tightbox import tight_word_box
from plan_blurs import plan, words_of
from crop_util import auto_crop, ocr_path, phone_crop, meta_crop, balance_margins, watermark_bar, tighten_margins

FPS = 30
CLIENT = "/CHANGE/ME/client folder/"
RAW = CLIENT + "CHANGE_ME recording.mp4"   # the narrator's raw screen recording
db = np.load("db10ms.npy")
pieces = json.load(open("assign.json"))
dec = json.load(open("decisions.json"))
ocr = {}
for l in open("img_ocr.jsonl"):
    r = json.loads(l)
    ocr[os.path.basename(r["file"]).replace(".webp.png", ".webp").replace(".WEBP.png", ".WEBP").replace(".mp4.png", ".mp4")] = r
for l in open("video_ocr.jsonl"):          # video memes: text read from a frame
    r = json.loads(l)
    ocr[os.path.basename(r["file"]).replace(".mp4.png", ".mp4")] = r

# ---- 1. apply review decisions ----
cut = set(dec.get("cut", []))
for k, f in dec.get("reassign", {}).items():
    pieces[int(k)]["meme"] = f
for k, b in dec.get("trim", {}).items():   # end a phrase early (cuts a restart inside it)
    pc = pieces[int(k)]
    pc["b"] = b
    pc["words"] = [w for w in pc["words"] if w["s"] < b]
    pc["hard_end"] = True
for k, a in dec.get("trim_start", {}).items():   # start a phrase late (cuts a repeated opening inside it)
    pc = pieces[int(k)]
    pc["a"] = a
    pc["words"] = [w for w in pc["words"] if w["s"] >= a - 0.05]
    pc["hard_start"] = True
order_a = sorted(range(len(pieces)), key=lambda i: pieces[i]["a"])
pos_a = {i: n for n, i in enumerate(order_a)}
def neighbours(i):
    """End of the phrase before and start of the phrase after (raw time), kept or not."""
    n = pos_a[i]
    prev_end = pieces[order_a[n - 1]]["b"] if n > 0 else None
    next_start = pieces[order_a[n + 1]]["a"] if n + 1 < len(order_a) else None
    return prev_end, next_start
kept = [(i, pc) for i, pc in enumerate(pieces) if i not in cut and pc["meme"]]
for k, after in dec.get("move_after", {}).items():   # a comment said after he had flipped to the next meme
    item = [x for x in kept if x[0] == int(k)][0]
    kept.remove(item)
    pos = [n for n, x in enumerate(kept) if x[0] == after][0]
    kept.insert(pos + 1, item)

# ---- 2. group into memes (consecutive phrases of the same meme) ----
groups = []
for i, pc in kept:
    if groups and groups[-1]["file"] == pc["meme"]:
        groups[-1]["idx"].append(i)
    else:
        groups.append({"file": pc["meme"], "idx": [i]})

# ---- 3. segments: contiguous kept phrases of one original region stay together ----
EDGE = -70.0      # a word's soft tail/onset runs while the raw voice stays at -70 dB or louder; quieter is room noise

def loud_bounds(a, b, words=(), hard_start=False, lo_lim=None, hi_lim=None):
    """Speech inside [a, b], cut the way the reviewer trims by hand (Oct 3 + Oct 4 2026 reviews):
    start 1-2 frames before the first sound at -70 dB or louder (a soft "s" rising out of the floor is kept),
    end about 3 frames after the word's decay drops under -70 dB. A breath next to the word is a separate bump
    after a dip, so the walk stops at the dip and the breath is left out, even when it sits at -58 to -70 dB."""
    i0, i1 = int(a * 100), int(b * 100)
    we = int((max(w["e"] for w in words) + 0.10) * 100) if words else i1
    loud = np.where(db[i0:i1] > -60)[0]
    if not len(loud):
        return a, b
    f0 = i0 + loud[0]
    # the phrase's last sound from the AUDIO (Whisper's word ends run up to 0.5 s early: "9999" was cut while he was still
    # saying it, Oct 11 2026), minus trailing breaths: a soft bump (peak under -55 dB) after a gap of 50 ms under -65 dB
    f1 = i0 + loud[-1]
    while True:
        q = f1
        while q > f0 and db[q] > -65:
            q -= 1                                 # back to the start of this bump
        gap_end = q
        while q > f0 and db[q] <= -65:
            q -= 1
        if q <= f0 or gap_end - q < 5 or db[gap_end + 1: f1 + 1].max() >= -55 or gap_end < we:
            break                                  # inside the last word (a final "d" or "t" release after its closure) stays
        f1 = q                                     # a soft bump after the words: a breath, end with the speech before it
    # onset: back from the first loud sample through the contiguous soft rise (at most 0.15 s), stopping at a dip
    lo = max(f0 - 15, 3, i0 if hard_start else i0 - 15)
    if lo_lim is not None:
        lo = max(lo, int(lo_lim * 100))
    k = f0
    while k - 1 > lo and db[k - 1] >= EDGE and not (db[k - 2] > db[k - 1] + 4 and db[k - 1] < -60):
        k -= 1
    start = k / 100 - 0.05
    if hard_start:
        start = max(start, a)                     # a hand trim (trim_start) is exact
    # tail: forward from the last loud sample through the decay (at most 0.35 s), stopping where a new bump starts
    hi = min(f1 + 35, len(db) - 5)
    if hi_lim is not None:
        hi = min(hi, int(hi_lim * 100))
    k = f1
    while k + 1 < hi and db[k + 1] >= EDGE:
        if db[k + 1] > db[k] + 4 and db[k] < -60 and db[k + 1: k + 26].max() < -55:
            break                                  # a soft separate bump after a dip: a breath, leave it out
        k += 1                                     # (a loud bump is the word's last syllable: "incognito" dips before "-to")
    e = k + 1                                      # handle of up to 0.10 s, stopping short of any new sound
    while e < min(k + 11, len(db) - 1) and db[e] <= -60:
        e += 1
    end = e / 100
    if hi_lim is not None:
        end = min(end, hi_lim)
    if lo_lim is not None:
        start = max(start, lo_lim)
    return start, end

def quiet_run(t0, t1, th=-60, need=0.4):
    """True if the audio between t0 and t1 holds a quiet stretch of at least `need` seconds (a real pause)."""
    seg = db[int(t0 * 100):int(t1 * 100)] < th
    run = best = 0
    for q in seg:
        run = run + 1 if q else 0
        best = max(best, run)
    return best >= need * 100

def piece_span(pc):
    """Returns (a, b, start_was_moved). Dead air at a phrase's edge is trimmed from the AUDIO, never from Whisper's word times
    (Whisper put "Procrastinate" 0.4 s late and the start cut into the word; "incognito" lasts a full second and a 0.6 s cap
    dropped its last syllable, Oct 11 2026). A phrase edge moves only past a real quiet stretch (0.4 s under -60 dB)."""
    a, b = pc["a"], pc["b"]
    i0, i1 = int(a * 100), int(b * 100)
    loud = np.where(db[i0:i1] > -60)[0]
    moved = False
    if len(loud):
        onset = (i0 + loud[0]) / 100
        if onset - a > 0.4:                         # quiet lead-in before the first sound
            a, moved = onset - 0.15, True
        last = (i0 + loud[-1]) / 100
        if b - last > 0.6:                          # quiet tail after the last sound
            b = last + 0.3
    return a, b, moved

cuts, out_f = [], 0
for gi, g in enumerate(groups):
    segs = []
    for i in g["idx"]:
        pc = pieces[i]
        pa, pb, moved = piece_span(pc)
        prev_end, next_start = neighbours(i)
        if segs and segs[-1]["region"] == pc["region"] and abs(segs[-1]["b"] - pa) < 0.02 and not segs[-1]["hard_end"]:
            segs[-1]["b"] = pb
            segs[-1]["words"] += pc["words"]
            segs[-1]["hi_lim"] = pb if pc.get("hard_end") else (next_start - 0.02 if next_start else None)
            segs[-1]["hard_end"] = bool(pc.get("hard_end"))
        else:
            segs.append({"region": pc["region"], "a": pa, "b": pb, "words": list(pc["words"]), "hard": moved or bool(pc.get("hard_start")),
                         "lo_lim": prev_end + 0.02 if prev_end else None,
                         "hi_lim": pb if pc.get("hard_end") else (next_start - 0.02 if next_start else None),
                         "hard_end": bool(pc.get("hard_end"))})
    for s in segs:
        a, b = loud_bounds(s["a"], s["b"], s["words"], s["hard"], s["lo_lim"], s["hi_lim"])
        fi, fo = int(math.floor(a * FPS)), int(math.ceil(b * FPS))
        if cuts and cuts[-1]["raw_out_f"] > fi and cuts[-1]["raw_in_f"] < fi:
            fi = cuts[-1]["raw_out_f"]
        if fo - fi < 3:
            continue
        cuts.append({"raw_in_f": fi, "raw_out_f": fo, "out_start_f": out_f, "img": gi})
        out_f += fo - fi
TOTAL_F = out_f

def raw_to_out(t):
    for c in cuts:   # cuts can be out of raw order when a phrase was moved
        a, b = c["raw_in_f"] / FPS, c["raw_out_f"] / FPS
        if a <= t <= b:
            return c["out_start_f"] / FPS + (t - a)
    nxt = [c for c in cuts if c["raw_in_f"] / FPS > t]
    return min(nxt, key=lambda c: c["raw_in_f"])["out_start_f"] / FPS if nxt else TOTAL_F / FPS

starts = {}
for c in cuts:
    starts.setdefault(c["img"], c["out_start_f"])
order = sorted(starts)

def onset_after(t, window=0.45, th=-60):
    i0 = int(round(t * 100))
    for i in range(i0, i0 + int(window * 100)):
        if db[i] > th:
            return i / 100
    return t

def onset_near(t, lo=-0.35, hi=0.25):
    for i in range(int((t + lo) * 100), int((t + hi) * 100)):
        if db[i] > -58 and db[i - 6:i].max() < -60:
            return i / 100
    return t

# ---- 4. geometry helpers ----
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

def mask_feather(img, box, lines, sc):
    """Feather in source pixels for a box/wipe mask: about 10 px once the meme is scaled onto the screen, and no wider
    than the space between the mask edge and the nearest line it does not cover (the reviewer, Oct 4 2026).
    NOTE: this is the Oct 4 rule; the Oct 13 rule (house-rules.md) is max(10, 20 / scale), see plan_pass.feather_for."""
    H = ocr[img]["h"]
    fe = min(10.0, 10.0 / sc)
    others = [L for L in ocr[img]["lines"] if L not in lines and L["b"][2] > box[0] and L["b"][0] < box[2]]
    gaps = [box[1] - L["b"][3] for L in others if L["b"][3] <= box[1] + 0.002] + [L["b"][1] - box[3] for L in others if L["b"][1] >= box[3] - 0.002]
    gaps = [g for g in gaps if g >= 0]
    if gaps:
        fe = min(fe, max(1.5, min(gaps) * H))
    return round(max(1.5, fe), 2)

def media_frames(img):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", img if img.startswith("/") else CLIENT + img],
                         capture_output=True, text=True).stdout.strip()
    return float(out) * FPS

# ---- 5. per meme ----
SEQ_W, SEQ_H, TARGET_H, MAX_W = 1920, 1080, 980, 1740
over = dec.get("memes", {})
images, report = [], []
for gi in order:
    g = groups[gi]
    name = g["file"]
    s_f = starts[gi]
    nxt = [starts[j] for j in order if starts[j] > s_f]
    e_f = min(nxt) if nxt else TOTAL_F
    ov = over.get(name, {})
    W, H = ocr[name]["w"], ocr[name]["h"]
    spoken_words = [ww for i in g["idx"] for w in pieces[i]["words"] for ww in words_of(w["w"])]
    crop = ov.get("crop") or meta_crop(name, ocr[name], phone_crop(name, ocr[name]) if H / W > 1.8 and W >= 1000 else auto_crop(name),
                                       spoken=spoken_words)
    if not ov.get("crop"):
        wb = watermark_bar(name)                 # the iFunny bar along the bottom edge
        if wb > crop["B"]:
            crop = dict(crop, B=wb)
    if not ov.get("keep_crop"):
        crop = balance_margins(name, crop)       # even white space above and below the text (the reviewer, Oct 11 2026)
    # trimming top/bottom margins only helps when it makes the meme bigger on screen; a wide meme is sized by its width
    if not ov.get("crop") and (crop["T"] or crop["B"]):
        full_h = H * (1 - (crop["T"] + crop["B"]) / 100); full_w = W * (1 - (crop["L"] + crop["R"]) / 100)
        if TARGET_H / H * full_w > MAX_W and TARGET_H / full_h * full_w > MAX_W:
            ph = meta_crop(name, ocr[name], {"L": crop["L"], "T": 0.0, "R": crop["R"], "B": 0.0}, spoken=spoken_words)
            crop = dict(crop, T=ph["T"], B=ph["B"])   # keep only the metadata trims
    if not ov.get("crop") and not ov.get("keep_crop"):
        crop = tighten_margins(name, crop)       # too much white space all round: tighten it (his tightening fix, Oct 11 2026)
    vis_w = W * (1 - (crop["L"] + crop["R"]) / 100); vis_h = H * (1 - (crop["T"] + crop["B"]) / 100)
    sc = TARGET_H / vis_h
    if vis_w * sc > MAX_W:
        sc = MAX_W / vis_w
    cx = (crop["L"] + 100 - crop["R"]) / 200; cy = (crop["T"] + 100 - crop["B"]) / 200
    pos = [0.5 - (cx - 0.5) * W * sc / SEQ_W, 0.5 - (cy - 0.5) * H * sc / SEQ_H]
    if ov.get("scale"):                          # his own placement from a hand-fixed save wins
        sc, pos = ov["scale"] / 100, list(ov["pos"])
    clip_start = s_f / FPS
    # timed words of this meme's kept phrases, in speaking order
    timed = []
    for i in g["idx"]:
        pc = pieces[i]
        for w in pc["words"]:
            for ww in words_of(w["w"]):
                timed.append((ww, max(w["s"], pc["a"]), w["e"]))
    blocks, auto = ([], []) if ov.get("no_auto") else plan(ocr[name]["lines"], timed)
    blurs = []
    def piece_start(t):
        for i in g["idx"]:
            pc = pieces[i]
            if abs(t - pc["a"]) < 0.02:   # the phrase's first word (its start is clamped to the phrase start)
                return pc["a"]
        return None
    def first_text(b):
        return (b.get("lines") or [{"t": b.get("word", "")}])[0]["t"]
    specs = [b for b in auto if not (ov.get("no_auto_reveals") and b["kind"] != "curse")
             and not any(first_text(b).startswith(p) for p in ov.get("drop_prefix", []))
             and not (b["kind"] == "curse" and b.get("word") in ov.get("drop_curse", []))]
    specs += ov.get("add", [])
    first_reveal = min([b for b in specs if b["kind"] in ("wipe", "box")], key=lambda b: b.get("raw_first", b.get("raw_t", 1e9)), default=None)
    for b in specs:
        if b["kind"] == "curse":
            if "words" in b:   # a word split by OCR (e.g. a censored letter): union of its pieces
                ws = [w["b"] for L in ocr[name]["lines"] for w in L["words"] if w["t"] in b["words"]]
                b["word_box"] = [min(w[0] for w in ws), min(w[1] for w in ws), max(w[2] for w in ws), max(w[3] for w in ws)]
            box, fe = tight_word_box(ocr_path(name), b["word_box"], sc)
            blurs.append({"kind": "curse", "box": box, "feather": fe, "label": b.get("word", "")})
            continue
        lines = b.get("lines") or ([ocr[name]["lines"][k] for k in b["line_idx"]] if "line_idx" in b else
                                   [L for L in ocr[name]["lines"] if any(L["t"].startswith(p) for p in b.get("prefixes", []))])
        box = b.get("box") or block_box(name, lines, extra=b.get("extra"))
        fe = mask_feather(name, box, lines, sc)
        label = lines[0]["t"] if lines else b.get("label", "")
        if b["kind"] == "box":
            rt = b["raw_t"]
            ps = piece_start(rt)
            on = onset_after(ps) if ps is not None else onset_near(rt)
            t = max(0.0, round((raw_to_out(on) - clip_start - 0.05) * FPS) / FPS)
            nl = b.get("n_lines") or len(lines) or 1
            if b.get("snap"):
                snap = b["snap"]
            elif nl <= 1:   # one line (label, punchline, one-line caption): a quick snap, 4-9 frames
                snap = max(4, min(9, round((b.get("spoken") or 0.5) * FPS * 0.25)))
            else:           # a multi-line comment or caption reveals at about 0.35 s per line (the reviewer, Oct 4 2026)
                snap = max(15, min(66, round(nl * 0.35 * FPS)))
                if b.get("spoken"):
                    snap = min(snap, max(15, round(b["spoken"] * FPS * 0.8)))
            blurs.append({"kind": "box", "box": box, "feather": fe, "keys": [[round(t, 4), 40.0], [round(t + snap / FPS, 4), 0.0]], "label": label})
        else:
            t0 = max(0.0, round((raw_to_out(onset_near(b["raw_first"])) - clip_start - 0.05) * FPS) / FPS)
            if b is first_reveal and b.get("n_lines_block", 0) >= 3 and not b.get("later"):
                tb = raw_to_out(onset_near(b.get("raw_block") or b["raw_first"])) - clip_start
                if tb <= 1.5:
                    t0 = 0.0    # he starts reading the block straight away: the wipe starts with the meme (his rule)
            if b.get("raw_end"):
                t1 = raw_to_out(b["raw_end"]) - clip_start + 0.25    # just after he finishes the last word
            else:
                t1 = raw_to_out(onset_near(b["raw_last"])) - clip_start + 0.25
            t1 = max(t0 + 15 / FPS, round(t1 * FPS) / FPS)
            blurs.append({"kind": "wipe", "box": box, "feather": fe, "path_keys": [round(t0, 4), round(t1, 4)], "label": label})
    # a reveal on text the crop removed is pointless (and a false match): drop it
    vis = (crop["L"] / 100, crop["T"] / 100, 1 - crop["R"] / 100, 1 - crop["B"] / 100)
    blurs = [bl for bl in blurs if bl["kind"] == "blackout" or
             (bl["box"][2] > vis[0] + 0.005 and bl["box"][0] < vis[2] - 0.005 and bl["box"][3] > vis[1] + 0.005 and bl["box"][1] < vis[3] - 0.005)]
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
    for prefix, word in ov.get("black_boxes", []):   # black squares over words he asked to hide
        L = [L for L in ocr[name]["lines"] if L["t"].startswith(prefix)][0]
        w = [w for w in L["words"] if w["t"] == word][0]["b"]
        h = w[3] - w[1]
        blurs.append({"kind": "blackout", "box": [round(w[0] - 0.012, 4), round(w[1] - 0.12 * h, 4), round(w[2] + 0.012, 4), round(w[3] + 0.12 * h, 4)],
                      "feather": 0.0, "label": word})
    entry = {"file": name, "path": ov.get("path", CLIENT + name), "w": W, "h": H, "start_f": s_f, "end_f": e_f, "crop": crop,
             "scale": round(sc * 100, 4), "pos": [round(float(pos[0]), 5), round(float(pos[1]), 5)], "blurs": blurs}
    if name.endswith(".mp4"):
        mf = media_frames(entry["path"])
        entry.update({"video": True, "media_f": mf, "speed": round(mf / (e_f - s_f), 6)})
        for b in blurs:  # keyframes live in media time on speed-changed clips
            pass
    images.append(entry)
    report.append(f"{s_f / FPS:8.2f}-{e_f / FPS:8.2f} {name[:44]:44s} " + " | ".join(
        f"{b['kind']}:{b['label'][:22]}" for b in blurs))

edl = {"fps": FPS, "raw": RAW, "total_f": TOTAL_F, "cuts": cuts, "images": images}
json.dump(edl, open("edl_full.json", "w"), indent=1)
open("edl_report.txt", "w").write("\n".join(report))
print(f"{len(images)} memes, {len(cuts)} cuts, length {TOTAL_F / FPS / 60:.0f}:{TOTAL_F / FPS % 60:05.2f}")
