"""Footage catalog: split clip packs into shots, score them, tag them with CLIP, search them by text.

usage:
  python catalog.py build FOOTAGE_DIR OUT_DIR      shots + motion + sharpness + thumbnails (+ CLIP embeddings if available)
  python catalog.py tag OUT_DIR                    zero-shot tags (shot scale, action, kit, extras) into catalog.json
  python catalog.py strips OUT_DIR OUT.png a,b,c [K]  one row per shot, K frames across it with source seconds
  python catalog.py idscore OUT_DIR NAME           how clearly the subject (gallery NAME) is in each shot: subj, subj_h, subj_x
  python catalog.py search OUT_DIR "text" [N]      rank shots by a text description
  python catalog.py sheet OUT_DIR OUT.png [ids:a,b,c | q:text | from:K] [N]   contact sheet (id, length, top tags)
Run without -I (open_clip / torch live in the user site-packages). Footage files are only read.
"""
import sys, os, json, glob, math
import numpy as np
import av
from PIL import Image, ImageDraw, ImageFont

THUMB = (224, 126)      # stored per kept frame (for CLIP and sheets)
DET = (64, 36)          # cut detection size

# ------------------------------------------------------------------ shots
def scan(path):
    c = av.open(path); s = c.streams.video[0]; s.thread_type = "AUTO"
    fps = float(s.average_rate); keep_every = max(1, round(fps / 5))
    small, thumbs, tidx = [], [], []
    for i, fr in enumerate(c.decode(s)):
        small.append(fr.reformat(width=DET[0], height=DET[1], format="rgb24").to_ndarray())
        if i % keep_every == 0:
            thumbs.append(fr.reformat(width=THUMB[0], height=THUMB[1], format="rgb24").to_ndarray()); tidx.append(i)
    c.close()
    return fps, np.stack(small).astype(np.float32), thumbs, np.array(tidx)

def cuts_of(a):
    y = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]; n = len(y)
    flat = y.reshape(n, -1); std = flat.std(1)
    z = (flat - flat.mean(1, keepdims=True)) / (std[:, None] + 1e-6)
    hist = np.stack([np.histogramdd(a[i].reshape(-1, 3), bins=(6, 6, 6), range=((0, 256),) * 3)[0].ravel() for i in range(n)])
    hist /= hist.sum(1, keepdims=True)
    blank = std < 7; cuts = []
    def nb(i, step):
        k = i
        for _ in range(9):
            if 0 <= k < n and not blank[k]: return k
            k += step
        return None
    for i in range(1, n):
        pa, pb = nb(i - 1, -1), nb(i, 1)
        if pa is None or pb is None: continue
        if pb != i and not blank[i]: continue
        corr = float(np.dot(z[pa], z[pb]) / z.shape[1]); inter = float(np.minimum(hist[pa], hist[pb]).sum())
        if corr < 0.35 or (corr < 0.6 and inter < 0.55):
            if not cuts or i - cuts[-1] > 2: cuts.append(i)
    # motion per frame (phase correlation)
    win = np.outer(np.hanning(DET[1]), np.hanning(DET[0])); mot = np.zeros(n); Fp = None
    for i in range(n):
        F = np.fft.fft2((y[i] - y[i].mean()) * win)
        if Fp is not None:
            R = F * np.conj(Fp); R /= np.maximum(np.abs(R), 1e-6); cc = np.fft.ifft2(R).real
            py, px = np.unravel_index(np.argmax(cc), cc.shape)
            py = py - DET[1] if py > DET[1] // 2 else py; px = px - DET[0] if px > DET[0] // 2 else px
            mot[i] = math.hypot(px, py)
        Fp = F
    diff = np.zeros(n); diff[1:] = np.abs(y[1:] - y[:-1]).mean((1, 2))
    return cuts, blank, mot, diff, y.mean((1, 2))

def sharp(img):
    g = img.astype(np.float32).mean(2)
    lap = g[1:-1, 1:-1] * 4 - g[:-2, 1:-1] - g[2:, 1:-1] - g[1:-1, :-2] - g[1:-1, 2:]
    return float(lap.var())

def build(src, out):
    os.makedirs(os.path.join(out, "thumbs"), exist_ok=True)
    cat = {"files": [], "shots": []}
    for f in sorted(glob.glob(os.path.join(src, "*.mp4"))):
        fps, a, thumbs, tidx = scan(f)
        cuts, blank, mot, diff, ym = cuts_of(a)
        n = len(a); fid = len(cat["files"])
        cat["files"].append(dict(id=fid, path=f, fps=fps, frames=n))
        bounds = [0] + cuts + [n]
        for k in range(len(bounds) - 1):
            s, e = bounds[k], bounds[k + 1]
            if (e - s) / fps < 0.4: continue                       # too short to use
            if blank[s:e].mean() > 0.5: continue                   # black / white cards
            ks = [j for j, t in enumerate(tidx) if s <= t < e]
            if not ks: continue
            pick = [ks[len(ks) // 4], ks[len(ks) // 2], ks[(3 * len(ks)) // 4]]
            sid = f"{fid}_{k:03d}"
            for p_i, j in enumerate(pick):
                Image.fromarray(thumbs[j]).save(os.path.join(out, "thumbs", f"{sid}_{p_i}.jpg"), quality=80)
            m = mot[s + 1:e] if e - s > 1 else np.zeros(1)
            pk = int(np.argmax(m)) + s + 1 if len(m) else s
            cat["shots"].append(dict(id=sid, file=fid, s=s, e=e, t0=round(s / fps, 3), t1=round(e / fps, 3), dur=round((e - s) / fps, 2),
                                     motion=round(float(m.mean()), 2), motion_peak=round(float(m.max()), 2), peak_t=round(pk / fps, 3),
                                     sharp=round(float(np.median([sharp(thumbs[j]) for j in pick])), 1), luma=round(float(ym[s:e].mean()), 1)))
        print(f"{os.path.basename(f)[:60]}: {n} frames @ {fps:.2f}, shots kept {sum(1 for x in cat['shots'] if x['file'] == fid)}", flush=True)
    json.dump(cat, open(os.path.join(out, "catalog.json"), "w"), indent=0)
    try:
        embed(out)
    except Exception as ex:
        print("CLIP embeddings skipped:", str(ex)[:120])

# ------------------------------------------------------------------ CLIP
_M = {}
def clip():
    if not _M:
        import torch, open_clip
        m, _, pre = open_clip.create_model_and_transforms("ViT-L-14", pretrained="laion2b_s32b_b82k")
        dev = "cuda" if torch.cuda.is_available() else "cpu"
        m = m.to(dev).eval(); tok = open_clip.get_tokenizer("ViT-L-14")
        _M.update(m=m, pre=pre, tok=tok, dev=dev, torch=torch)
    return _M

def embed(out):
    M = clip(); torch = M["torch"]
    cat = json.load(open(os.path.join(out, "catalog.json")))
    vecs = []
    with torch.no_grad():
        for sh in cat["shots"]:
            ims = [M["pre"](Image.open(os.path.join(out, "thumbs", f"{sh['id']}_{i}.jpg"))) for i in range(3)]
            v = M["m"].encode_image(torch.stack(ims).to(M["dev"])).float()
            v = v / v.norm(dim=-1, keepdim=True); v = v.mean(0); v = v / v.norm()
            vecs.append(v.cpu().numpy())
    np.save(os.path.join(out, "emb.npy"), np.stack(vecs))
    print("embedded", len(vecs), "shots")

def text_vecs(texts):
    M = clip(); torch = M["torch"]
    with torch.no_grad():
        t = M["m"].encode_text(M["tok"](texts).to(M["dev"])).float()
        t = t / t.norm(dim=-1, keepdim=True)
    return t.cpu().numpy()

GROUPS = {
    "scale": {"face": "an extreme close-up of a footballer's face", "close": "a close-up shot of a football player from the chest up",
              "medium": "a medium shot of one football player full body", "wide": "a wide shot of a football pitch with many players",
              "aerial": "an aerial top-down view of a football pitch"},
    "action": {"dribble": "a football player dribbling the ball past a defender", "shoot": "a football player kicking the ball hard to shoot",
               "net": "the football hitting the back of the net in a goal", "celebrate": "a football player celebrating a goal",
               "hug": "football teammates hugging and celebrating together", "run": "a football player running fast without the ball",
               "walk": "a football player walking calmly on the pitch", "pose": "a football player posing and looking at the camera",
               "fans": "football fans cheering in the stands", "trophy": "a football player holding a trophy",
               "tunnel": "football players in the stadium tunnel before the match", "title": "a title card with large text on a plain background"},
    "kit": {"barca": "a football player in the FC Barcelona shirt with blue and dark red stripes", "spain": "a football player in the red Spain national team shirt",
            "white": "a football player in a white shirt", "other": "a football player in a yellow or green shirt"},
}

def tag(out):
    cat = json.load(open(os.path.join(out, "catalog.json"))); E = np.load(os.path.join(out, "emb.npy"))
    for g, d in GROUPS.items():
        T = text_vecs(list(d.values())); logits = 100 * E @ T.T
        p = np.exp(logits - logits.max(1, keepdims=True)); p /= p.sum(1, keepdims=True)
        keys = list(d.keys())
        for i, sh in enumerate(cat["shots"]):
            order = np.argsort(-p[i])[:2]
            sh[g] = [[keys[o], round(float(p[i][o]), 2)] for o in order]
    json.dump(cat, open(os.path.join(out, "catalog.json"), "w"), indent=0)
    from collections import Counter
    for g in GROUPS:
        print(g, Counter(sh[g][0][0] for sh in cat["shots"]).most_common())

def idscore(out, name, n=4):
    """how clearly the main subject (gallery `name`, see reframe.build_gallery) is in each shot: per shot `subj` = share of
    sampled frames where he is identified for sure, `subj_h` = his median box height (share of frame), `subj_x` = median
    centre x (share), `people` = median people count. Lets a planner skip shots where a team-mate fills the frame."""
    import reframe
    cat = json.load(open(os.path.join(out, "catalog.json"))); files = {f["id"]: f["path"] for f in cat["files"]}
    G = reframe.build_gallery(os.path.join(out, "catalog.json"), name)
    for sh in cat["shots"]:
        c = av.open(files[sh["file"]]); st = c.streams.video[0]; W, H = st.codec_context.width, st.codec_context.height
        hits, hs, xs, ns = 0, [], [], []
        for k in range(n):
            tq = sh["t0"] + (k + 1) / (n + 1) * (sh["t1"] - sh["t0"]); img = None
            c.seek(int(max(0, tq - 0.6) / st.time_base), stream=st)
            for fr in c.decode(st):
                if float(fr.pts * st.time_base) >= tq - 0.02:
                    img = fr.reformat(width=960, height=int(round(H * 960 / W / 2) * 2), format="rgb24").to_ndarray(); break
            if img is None: continue
            bx = [b for b in reframe.people(img) if (b[3] - b[1]) > img.shape[0] * 0.08]; ns.append(len(bx))
            if not bx: continue
            sc = reframe.id_score(img, bx, G); i = int(np.argmax(sc)); rest = sorted(sc)[:-1]
            if sc[i] > 0.62 and (not rest or sc[i] - max(rest) > 0.03):
                hits += 1; hs.append((bx[i][3] - bx[i][1]) / img.shape[0]); xs.append((bx[i][0] + bx[i][2]) / 2 / img.shape[1])
        c.close()
        sh["subj"] = round(hits / n, 2); sh["subj_h"] = round(float(np.median(hs)), 2) if hs else 0
        sh["subj_x"] = round(float(np.median(xs)), 2) if xs else 0; sh["people"] = int(np.median(ns)) if ns else 0
    json.dump(cat, open(os.path.join(out, "catalog.json"), "w"), indent=0)
    good = sum(1 for sh in cat["shots"] if sh["subj"] >= 0.75)
    print(f"idscore {name}: {good} of {len(cat['shots'])} shots show him clearly (subj >= 0.75)")

def search(out, q, n=12):
    cat = json.load(open(os.path.join(out, "catalog.json"))); E = np.load(os.path.join(out, "emb.npy"))
    s = E @ text_vecs([q])[0]; order = np.argsort(-s)[:n]
    return [(cat["shots"][i], float(s[i])) for i in order]

def sheet(out, png, sel=None, n=48):
    cat = json.load(open(os.path.join(out, "catalog.json"))); shots = cat["shots"]
    if sel and sel.startswith("q:"):
        shots = [s for s, _ in search(out, sel[2:], n)]
    elif sel and sel.startswith("ids:"):
        want = sel[4:].strip().split(","); by = {s["id"]: s for s in shots}; shots = [by[w] for w in want if w in by]
    elif sel and sel.startswith("from:"):
        k = int(sel[5:]); shots = shots[k:]
    shots = shots[:n]
    cols = 8; tw, th = 192, 108; lab = 30
    rows = (len(shots) + cols - 1) // cols
    img = Image.new("RGB", (cols * (tw + 4) + 4, rows * (th + lab + 4) + 4), (24, 24, 28)); d = ImageDraw.Draw(img)
    try: font = ImageFont.truetype(("C:/Windows/Fonts/arialbd.ttf" if sys.platform == "win32" else "/System/Library/Fonts/Supplemental/Arial Bold.ttf"), 11)
    except Exception: font = ImageFont.load_default()
    for k, sh in enumerate(shots):
        x = 4 + (k % cols) * (tw + 4); y = 4 + (k // cols) * (th + lab + 4)
        img.paste(Image.open(os.path.join(out, "thumbs", f"{sh['id']}_1.jpg")).resize((tw, th)), (x, y))
        t1 = f"{sh['id']} {sh['dur']}s m{sh['motion']}" + (f" id{sh['subj']:.2f}" if "subj" in sh else "")
        t2 = " ".join(sh[g][0][0] for g in ("scale", "action", "kit") if g in sh)
        d.text((x + 2, y + th + 2), t1, fill=(235, 235, 235), font=font); d.text((x + 2, y + th + 15), t2, fill=(150, 200, 255), font=font)
    img.save(png); print(png, img.size, len(shots), "shots")

def strips(out, png, ids, k=8, tw=176):
    """one row per shot, k frames spread over the shot, labelled with SOURCE seconds: for choosing src ranges"""
    cat = json.load(open(os.path.join(out, "catalog.json"))); by = {s["id"]: s for s in cat["shots"]}
    files = {f["id"]: f["path"] for f in cat["files"]}; th = int(tw * 9 / 16); lab = 13
    rows = [by[i] for i in ids.split(",") if i in by]
    img = Image.new("RGB", (60 + k * (tw + 2), len(rows) * (th + lab + 3) + 3), (24, 24, 28)); d = ImageDraw.Draw(img)
    font = ImageFont.truetype(("C:/Windows/Fonts/arialbd.ttf" if sys.platform == "win32" else "/System/Library/Fonts/Supplemental/Arial Bold.ttf"), 11)
    for r, sh in enumerate(rows):
        y = 3 + r * (th + lab + 3); d.text((3, y + th // 2 - 12), sh["id"], fill=(255, 220, 120), font=font)
        d.text((3, y + th // 2 + 2), f"id{sh.get('subj', 0):.2f}", fill=(150, 200, 255), font=font)
        ts = [sh["t0"] + (j + 0.5) / k * (sh["t1"] - sh["t0"]) for j in range(k)]
        c = av.open(files[sh["file"]]); st = c.streams.video[0]; st.thread_type = "AUTO"
        c.seek(int(max(0, sh["t0"] - 0.5) / st.time_base), stream=st); j = 0
        for fr in c.decode(st):
            t = float(fr.pts * st.time_base)
            if j < k and t >= ts[j]:
                x = 60 + j * (tw + 2); img.paste(Image.fromarray(fr.reformat(width=tw, height=th, format="rgb24").to_ndarray()), (x, y))
                d.text((x + 2, y + th + 1), f"{t:.2f}", fill=(230, 230, 230), font=font); j += 1
            if j >= k: break
        c.close()
    img.save(png); print(png, img.size, len(rows), "shots")

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "build": build(sys.argv[2], sys.argv[3])
    elif cmd == "embed": embed(sys.argv[2])
    elif cmd == "tag": tag(sys.argv[2])
    elif cmd == "idscore": idscore(sys.argv[2], sys.argv[3])
    elif cmd == "strips": strips(sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]) if len(sys.argv) > 5 else 8)
    elif cmd == "search":
        for sh, sc in search(sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 12):
            print(f"{sh['id']} {sc:.3f} {sh['dur']}s t{sh['t0']}-{sh['t1']} m{sh['motion']} {sh.get('scale', [['?']])[0][0]} {sh.get('action', [['?']])[0][0]}")
    elif cmd == "sheet": sheet(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None, int(sys.argv[5]) if len(sys.argv) > 5 else 48)
