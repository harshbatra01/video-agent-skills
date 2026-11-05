"""Auto-reframe: follow the main player so a 16:9 clip can be cropped to 9:16 without losing him.

usage (test): python reframe.py CLIP SRC_IN SRC_OUT [largest|center] [--sheet out.png]
as a module:  path = follow(clip, src_in, src_out, pick) -> [(src_t, x, y, w, h), ...] in source pixels
- person detector (torchvision Faster R-CNN v2, COCO) every ~1/15 s
- the target is picked on the first sample (largest person for close shots, nearest the centre for wide shots), then
  tracked by box overlap and distance; gaps hold the last position
- the path is smoothed (centred moving average, ~0.4 s) and its speed capped so the virtual camera glides
Results are cached next to the kit (cache/reframe.json) by file + range.
"""
import sys, os, json, math
import numpy as np
import av, torch

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(KIT, "cache", "reframe.json")
_DET = {}

def det():
    if not _DET:
        from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2, FasterRCNN_ResNet50_FPN_V2_Weights
        _DET["m"] = fasterrcnn_resnet50_fpn_v2(weights=FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT).eval().cuda()
    return _DET["m"]

def people(img):
    x = torch.from_numpy(img).permute(2, 0, 1).float().div(255).cuda()
    with torch.no_grad():
        r = det()([x])[0]
    return [b.tolist() + [float(s)] for b, l, s in zip(r["boxes"], r["labels"], r["scores"]) if int(l) == 1 and float(s) > 0.55]

# ------------------------------------------------------------------ subject re-identification (CLIP gallery)
_G = {}
def _clip():
    import catalog                      # same folder: open_clip ViT-L-14 loader
    return catalog.clip()

def embed_crops(imgs):
    M = _clip(); torch_ = M["torch"]
    from PIL import Image
    with torch_.no_grad():
        x = torch_.stack([M["pre"](Image.fromarray(im)) for im in imgs]).to(M["dev"])
        v = M["m"].encode_image(x).float(); v = v / v.norm(dim=-1, keepdim=True)
    return v.cpu().numpy()

def crop_box(img, b, pad=0.12):
    H, W = img.shape[:2]; w, h = b[2] - b[0], b[3] - b[1]
    x0, y0 = int(max(0, b[0] - pad * w)), int(max(0, b[1] - pad * h)); x1, y1 = int(min(W, b[2] + pad * w)), int(min(H, b[3] + pad * h))
    return img[y0:y1, x0:x1]

def build_gallery(catalog_json, name, max_items=40):
    """crops of the main subject from close/face shots; outliers (coaches, team-mates) dropped by mutual similarity"""
    path = os.path.join(KIT, "cache", f"gallery_{name}.npy")
    if os.path.exists(path): return np.load(path)
    cat = json.load(open(catalog_json, encoding="utf-8")); files = {f["id"]: f["path"] for f in cat["files"]}
    cands = [sh for sh in cat["shots"] if sh.get("scale", [["?"]])[0][0] in ("face", "close") and sh.get("action", [["?"]])[0][0] != "title"]
    crops = []
    for sh in cands[: max_items * 2]:
        c = av.open(files[sh["file"]]); st = c.streams.video[0]; tmid = (sh["t0"] + sh["t1"]) / 2
        c.seek(int(max(0, tmid - 0.5) / st.time_base), stream=st); img = None
        for fr in c.decode(st):
            if float(fr.pts * st.time_base) >= tmid: img = fr.to_ndarray(format="rgb24"); break
        c.close()
        if img is None: continue
        sc = img.shape[1] / 960; small = np.ascontiguousarray(img[:: max(1, int(round(sc))), :: max(1, int(round(sc)))])
        bx = people(small)
        if not bx: continue
        k = max(bx, key=lambda b: (b[2] - b[0]) * (b[3] - b[1])); f = img.shape[1] / small.shape[1]
        crops.append(crop_box(img, [v * f for v in k[:4]]))
    E = embed_crops(crops)
    S = E @ E.T; score = S.mean(1); keep = score >= np.quantile(score, 0.4)
    G = E[keep][: max_items]; os.makedirs(os.path.dirname(path), exist_ok=True); np.save(path, G)
    print(f"gallery {name}: {len(G)} of {len(E)} crops kept")
    return G

def id_score(img, boxes, G):
    if G is None or not boxes: return [0.0] * len(boxes)
    E = embed_crops([crop_box(img, b) for b in boxes]); S = E @ G.T
    return [float(np.sort(r)[-5:].mean()) for r in S]

def iou(a, b):
    x0, y0, x1, y1 = max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])
    i = max(0, x1 - x0) * max(0, y1 - y0); u = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - i
    return i / u if u > 0 else 0

def follow(clip, s0, s1, pick="largest", hz=15, gallery=None):
    key = f"{os.path.basename(clip)}|{s0:.3f}|{s1:.3f}|{pick}" + ("|id" if gallery is not None else "")
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    if key in cache: return cache[key]
    c = av.open(clip); s = c.streams.video[0]; s.thread_type = "AUTO"; fps = float(s.average_rate)
    W, H = s.codec_context.width, s.codec_context.height
    c.seek(int(max(0, s0 - 1) / s.time_base), stream=s)
    step = max(1, round(fps / hz)); samples = []; k = 0
    for fr in c.decode(s):
        t = float(fr.pts * s.time_base)
        if t < s0 - 0.5 / fps: continue
        if t > s1: break
        if k % step == 0:
            img = fr.reformat(width=960, height=int(round(H * 960 / W / 2) * 2), format="rgb24").to_ndarray()
            sc = W / 960
            bx = [b for b in people(img) if (b[3] - b[1]) > img.shape[0] * 0.08]
            ids = id_score(img, bx, gallery) if (gallery is not None and (len(samples) % 6 == 0 or not samples)) else [None] * len(bx)
            samples.append((t, [[b[0] * sc, b[1] * sc, b[2] * sc, b[3] * sc, b[4], i] for b, i in zip(bx, ids)]))
        k += 1
    c.close()
    path, cur = [], None
    for t, boxes in samples:
        scored = [b for b in boxes if b[5] is not None]
        if gallery is not None and scored:
            best_id = max(scored, key=lambda b: b[5])
            others = sorted([b[5] for b in scored])[:-1]
            sure = best_id[5] > 0.62 and (not others or best_id[5] - max(others) > 0.03)
            if sure and (cur is None or (cur[5] is not None and best_id[5] - cur[5] > 0.05) or iou(cur, best_id) < 0.1):
                if cur is None or iou(cur, best_id) < 0.3: cur = best_id
        if cur is None and boxes:
            if pick == "center":
                cur = min(boxes, key=lambda b: abs((b[0] + b[2]) / 2 - W / 2) + 0.5 * abs((b[1] + b[3]) / 2 - H / 2) - 0.3 * (b[3] - b[1]))
            else:
                cur = max(boxes, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]) * (1.2 - abs((b[0] + b[2]) / 2 - W / 2) / W))
        elif cur is not None and boxes:
            cx, cy = (cur[0] + cur[2]) / 2, (cur[1] + cur[3]) / 2; diag = math.hypot(cur[2] - cur[0], cur[3] - cur[1])
            best = max(boxes, key=lambda b: iou(cur, b) - math.hypot((b[0] + b[2]) / 2 - cx, (b[1] + b[3]) / 2 - cy) / (diag * 3 + 1))
            if iou(cur, best) > 0.05 or math.hypot((best[0] + best[2]) / 2 - cx, (best[1] + best[3]) / 2 - cy) < diag: cur = best
        if cur is not None:
            path.append([t, (cur[0] + cur[2]) / 2, (cur[1] + cur[3]) / 2, cur[2] - cur[0], cur[3] - cur[1]])
    if not path:
        path = [[s0, W / 2, H / 2, 0, 0], [s1, W / 2, H / 2, 0, 0]]
    # back-fill the start if the first detections came late
    if path[0][0] > s0 + 0.05: path.insert(0, [s0] + path[0][1:])
    # smooth: centred moving average over ~0.4 s, then cap the speed (px/s) so the crop glides
    arr = np.array(path, dtype=float); n = max(1, int(round(0.4 * hz)))
    sm = arr.copy()
    for col in (1, 2):
        pad = np.pad(arr[:, col], (n, n), mode="edge"); sm[:, col] = np.convolve(pad, np.ones(2 * n + 1) / (2 * n + 1), mode="valid")
    cap = W * 0.6
    for i in range(1, len(sm)):
        dt = max(1e-3, sm[i, 0] - sm[i - 1, 0]); dx = sm[i, 1] - sm[i - 1, 1]
        if abs(dx) > cap * dt: sm[i, 1] = sm[i - 1, 1] + math.copysign(cap * dt, dx)
    out = [[round(float(r[0]), 3), round(float(r[1]), 1), round(float(r[2]), 1), round(float(r[3]), 1), round(float(r[4]), 1)] for r in sm]
    cache[key] = out; os.makedirs(os.path.dirname(CACHE), exist_ok=True); json.dump(cache, open(CACHE, "w"))
    return out

def focus_keys(path, t0, s0, speed=1.0, every=0.2, rk=None):
    """source-time path -> edit-time focus keys [[t, x, y], ...]; rk maps edit t -> source t when given"""
    out = []; last = -1
    def src_to_edit(st):
        if rk:   # invert piecewise-linear remap
            for (a, sa), (b, sb) in zip(rk, rk[1:]):
                if min(sa, sb) - 1e-6 <= st <= max(sa, sb) + 1e-6 and sb != sa: return a + (st - sa) * (b - a) / (sb - sa)
            return None
        return t0 + (st - s0) / speed
    for r in path:
        te = src_to_edit(r[0])
        if te is None: continue
        if te - last >= every: out.append([round(te, 3), r[1], r[2]]); last = te
    return out

if __name__ == "__main__":
    clip, s0, s1 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]); pick = sys.argv[4] if len(sys.argv) > 4 and not sys.argv[4].startswith("--") else "largest"
    p = follow(clip, s0, s1, pick)
    print(len(p), "points; x range", min(r[1] for r in p), max(r[1] for r in p))
    for r in p[:: max(1, len(p) // 8)]: print(r)
