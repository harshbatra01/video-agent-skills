"""Auto-matte every clip of an edit and frame it from the matte (free, local GPU).

Why: a person detector box jumps between players and gives no shape. A SAM 2 matte of the right player gives
1. framing that stays on HIM (centre of his head + shoulders, not the biggest body in shot),
2. a shape for every matte device (type behind him, outline, silhouette strobe, colour pop) on any clip, for free.

as a module (used by plan scripts):
  m = ensure(file, s0, s1, out_dir, box=None, point=None, gallery=None)
        SAM 2 matte of file[s0:s1] -> out_dir/auto_<stem>_<s0>_<s1>.mp4 + .json stats (cached: runs once per range).
        Prompt: box/point in source pixels (at source time prompt_t, default the first frame; SAM 2 then tracks both ways),
        else the person the re-ID gallery says is the subject, else the largest person. Returns dict(file, src0, fps, w, h, rows) (rows: see roto.make_matte).
  keys = matte_focus(m, t0, t1, rk)        edit-time focus keys [[t, x, y], ...] in source pixels (smoothed, speed capped)
  z = auto_zoom(m)                         >1 when the subject is small in frame (wide shots), 1 for close shots
  x, y, top = comp_point(m, clip, t, band=[y0, h])   where his head lands on screen (place type behind / next to him)
CLI check: python automatte.py CLIP S0 S1 OUT_DIR [x0,y0,x1,y1]
Run without -I (torch / sam2 live in the user site-packages).
"""
import sys, os, json, math
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def _first_frame(path, t):
    import av
    c = av.open(path); st = c.streams.video[0]; img = None
    c.seek(int(max(0, t - 1) / st.time_base), stream=st)
    for fr in c.decode(st):
        if float(fr.pts * st.time_base) >= t - 0.5 / float(st.average_rate):
            img = fr.to_ndarray(format="rgb24"); break
    c.close()
    return img


def subject_box(path, t, gallery=None, near=None):
    """box [x0,y0,x1,y1] (source px) of the subject at time t: the re-ID gallery's surest match, else the person nearest
    `near` (x, y), else the largest person. None if nobody is found."""
    import reframe
    img = _first_frame(path, t)
    if img is None: return None
    H, W = img.shape[:2]; k = W / 960
    small = np.ascontiguousarray(np.asarray(Image.fromarray(img).resize((960, int(round(H / k))))))
    bx = [b for b in reframe.people(small) if (b[3] - b[1]) > small.shape[0] * 0.08]
    if not bx: return None
    bx = [[v * k for v in b[:4]] for b in bx]
    if gallery is not None:
        sc = reframe.id_score(img, bx, gallery); i = int(np.argmax(sc)); rest = sorted(sc)[:-1]
        if sc[i] > 0.62 and (not rest or sc[i] - max(rest) > 0.03): return bx[i]
    if near is not None:
        return min(bx, key=lambda b: math.hypot((b[0] + b[2]) / 2 - near[0], (b[1] + b[3]) / 2 - near[1]))
    return max(bx, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))


def ensure(path, s0, s1, out_dir, box=None, point=None, gallery=None, near=None, pad=0.1, tag="", prompt_t=None, lo=None, hi=None):
    """lo / hi = the shot's own start / end (catalog): the padding must never reach into the next shot, or SAM 2 is
    prompted on (or tracks into) a different picture. Without a given prompt_t the subject is found mid-range and
    tracked both ways (first frames can be mid-transition)."""
    import roto, torch
    os.makedirs(out_dir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(path))[0]
    a, b = max(0.0, min(s0, s1) - pad), max(s0, s1) + pad
    if lo is not None: a = max(a, lo + 0.02)
    if hi is not None: b = min(b, hi - 0.02)
    if prompt_t is None and box is None and point is None: prompt_t = (min(s0, s1) + max(s0, s1)) / 2
    if box is not None or point is not None:     # a hand prompt is part of the cache key (a new box = a new matte)
        import hashlib; tag += "_p" + hashlib.md5(f"{box}{point}{prompt_t}".encode()).hexdigest()[:6]
    out = os.path.join(out_dir, f"auto_{stem}_{a:.2f}_{b:.2f}{tag}.mp4"); js = out[:-4] + ".json"
    if os.path.exists(out) and os.path.exists(js):
        return json.load(open(js))
    if box is None and point is None:
        # try the asked time, then other moments across the range: a rim close-up or a crowd frame can hold nobody
        tries = [a if prompt_t is None else prompt_t] + [a + (b - a) * f for f in (0.5, 0.25, 0.75, 0.1, 0.9)]
        for tt in tries:
            box = subject_box(path, tt, gallery, near)
            if box is not None: prompt_t = tt; break
        if box is None:
            print(f"matte SKIPPED {os.path.basename(path)} {a:.2f}-{b:.2f}: nobody found at any tried moment", flush=True)
            return None
    m = roto.make_matte(path, out, a, b, box=box, point=point, stats=True, prompt_t=prompt_t)
    m["prompt"] = dict(box=[round(v, 1) for v in box] if box is not None else None, point=point, t=prompt_t)
    json.dump(m, open(js, "w"))
    torch.cuda.empty_cache()
    good = [r for r in m["rows"] if r[1] > 0]
    print(f"matte {os.path.basename(out)}: {len(m['rows'])} frames, subject found in {len(good)}, "
          f"mean area {np.mean([r[1] for r in m['rows']]):.3f}", flush=True)
    return m


def _src_of(rk):
    def f(t):
        if t <= rk[0][0]: return rk[0][1]
        for (a, sa), (b, sb) in zip(rk, rk[1:]):
            if a <= t <= b: return sa + (sb - sa) * (t - a) / (b - a) if b > a else sb
        return rk[-1][1]
    return f


def path_of(m, win=0.3, cap=0.6, wide_body=0.5):
    """smoothed subject point per matte frame: x = centre of head + shoulders, y = between that and the body centre"""
    rows = m["rows"]; W = m["w"]
    t = np.array([r[0] for r in rows]); ok = np.array([r[1] > 0 for r in rows])
    if not ok.any(): return t, np.full(len(t), m["w"] / 2), np.full(len(t), m["h"] / 2)
    x = np.array([r[8] for r in rows], float); y = np.array([(r[9] + wide_body * (r[3] - r[9])) for r in rows], float)
    idx = np.where(ok)[0]                      # hold the last good point through frames where SAM 2 lost him
    for arr in (x, y):
        arr[~ok] = np.interp(np.where(~ok)[0], idx, arr[idx])
    n = max(1, int(round(win * m["fps"] / 2)))
    k = np.ones(2 * n + 1) / (2 * n + 1)
    xs = np.convolve(np.pad(x, n, mode="edge"), k, mode="valid"); ys = np.convolve(np.pad(y, n, mode="edge"), k, mode="valid")
    for i in range(1, len(xs)):               # glide: cap the virtual camera speed (source px per source second)
        dt = max(1e-3, t[i] - t[i - 1]); lim = cap * W * dt
        xs[i] = xs[i - 1] + max(-lim, min(lim, xs[i] - xs[i - 1])); ys[i] = ys[i - 1] + max(-lim, min(lim, ys[i] - ys[i - 1]))
    return t, xs, ys


def matte_focus(m, t0, t1, rk, every=0.1, **kw):
    """edit-time focus keys from the matte; rk = [[edit t, src t], ...]"""
    t, xs, ys = path_of(m, **kw); src = _src_of(rk); out = []
    n = max(1, int(round((t1 - t0) / every)))
    for i in range(n + 1):
        te = t0 + (t1 - t0) * i / n; s = src(te)
        out.append([round(te, 3), round(float(np.interp(s, t, xs)), 1), round(float(np.interp(s, t, ys)), 1)])
    return out


def _interp(keys, t):
    if not isinstance(keys, list): return keys
    if not isinstance(keys[0], list): return keys
    if t <= keys[0][0]: return keys[0][1:] if len(keys[0]) > 2 else keys[0][1]
    for a, b in zip(keys, keys[1:]):
        if a[0] <= t <= b[0]:
            u = (t - a[0]) / (b[0] - a[0]) if b[0] > a[0] else 1
            v = [x + (y - x) * u for x, y in zip(a[1:], b[1:])]
            return v if len(v) > 1 else v[0]
    return keys[-1][1:] if len(keys[-1]) > 2 else keys[-1][1]


def comp_point(m, clip, t, comp_w=1080, comp_h=1920, band=None):
    """where the subject's head + shoulders centre lands in COMP pixels at edit time t (same maths as edits_lib clip():
    cover the frame box, zoom, anchor = focus clamped so no black edges). Returns (x, y, top_y) or None if not found.
    Use it to put a number right behind his head, or a caption next to him, instead of guessing."""
    fw, fh = (comp_w, band[1]) if band else (comp_w, comp_h); fcx, fcy = comp_w / 2, (band[0] + band[1] / 2) if band else comp_h / 2
    s_src = _src_of(clip["rk"])(t)
    rows = [r for r in m["rows"] if r[1] > 0]
    if not rows: return None
    r = min(rows, key=lambda r: abs(r[0] - s_src))
    W, H = m["w"], m["h"]; z = _interp(clip.get("zoom", 1), t) or 1
    sc = max(fw / W, fh / H) * z; hw, hh = fw / 2 / sc, fh / 2 / sc
    f = clip.get("focus") or [0.5, 0.5]
    fx, fy = _interp(f, t) if isinstance(f[0], list) else f
    fx = fx * W if fx <= 1.5 else fx; fy = fy * H if fy <= 1.5 else fy
    ax = min(W - hw, max(hw, fx)); ay = min(H - hh, max(hh, fy))
    return (fcx + (r[8] - ax) * sc, fcy + (r[9] - ay) * sc, fcy + (r[5] - ay) * sc)


def auto_zoom(m, fill=0.55, zmax=1.8):
    """zoom so the subject's height is about `fill` of the frame; 1 when he already fills it or is cut by the bottom edge"""
    rows = [r for r in m["rows"] if r[1] > 0]
    if not rows: return 1.0
    hh = np.median([(r[7] - r[5]) / m["h"] for r in rows]); bottom = np.median([r[7] / m["h"] for r in rows])
    if bottom > 0.96 or hh >= fill: return 1.0
    return round(float(min(zmax, max(1.0, fill / max(hh, 1e-3)))), 3)


if __name__ == "__main__":
    p, a, b, od = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    bx = [float(v) for v in sys.argv[5].split(",")] if len(sys.argv) > 5 else None
    m = ensure(p, a, b, od, box=bx)
    print("zoom", auto_zoom(m)); print(matte_focus(m, 0, b - a, [[0, a], [b - a, b]], every=0.25))
