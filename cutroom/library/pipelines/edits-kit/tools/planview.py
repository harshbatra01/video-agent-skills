"""Plan preview: see every clip's 9:16 framing (and its matte and type) BEFORE spending an After Effects render.

usage: python planview.py PLAN.json OUT.png [thumb_w=96] [per_row=5]
For each clip: 3 frames (start, middle, end) cropped exactly like build_edit / edits_lib clip() will crop them
(cover scale x zoom, anchor = focus, clamped so no black edges). Red tint = the clip's matte (the subject).
Yellow boxes = words on screen at that moment (rough size; a word's y is its BASELINE, caps rise 0.72 x size above it). Cyan lines = the 10% / 76% type safe zone.
Label: clip number, edit start, name, zoom; the label turns red if the subject is outside the middle 60% of the frame.
"""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import av
from PIL import Image, ImageDraw, ImageFont


def interp(keys, t):
    if not isinstance(keys, list): return keys
    if t <= keys[0][0]: return keys[0][1:] if len(keys[0]) > 2 else keys[0][1]
    for a, b in zip(keys, keys[1:]):
        if a[0] <= t <= b[0]:
            u = (t - a[0]) / (b[0] - a[0]) if b[0] > a[0] else 1
            v = [x + (y - x) * u for x, y in zip(a[1:], b[1:])]
            return v if len(v) > 1 else v[0]
    return keys[-1][1:] if len(keys[-1]) > 2 else keys[-1][1]


def src_at(cl, t):
    rk = cl.get("rk") or [[cl["t0"], cl["src"]], [cl["t1"], cl["src"] + (cl["t1"] - cl["t0"]) * cl.get("speed", 1.0)]]
    return interp(rk, t)


def frame_at(path, t, cache={}):
    c = cache.get(path)
    if c is None: c = cache[path] = av.open(path)
    st = c.streams.video[0]
    c.seek(int(max(0, t - 1.0) / st.time_base), stream=st)
    for fr in c.decode(st):
        if float(fr.pts * st.time_base) >= t - 0.5 / float(st.average_rate):
            return fr.to_ndarray(format="rgb24")
    return None


def main():
    plan = json.load(open(sys.argv[1], encoding="utf-8")); out = sys.argv[2]
    tw = int(sys.argv[3]) if len(sys.argv) > 3 else 96; per = int(sys.argv[4]) if len(sys.argv) > 4 else 5
    CW, CH = plan["w"], plan["h"]; th = int(round(tw * CH / CW)); lab = 26; gap = 6
    clips = plan["clips"]; rows = (len(clips) + per - 1) // per
    sheet = Image.new("RGB", (per * (3 * tw + 2 * 2 + gap) + gap, rows * (th + lab + gap) + gap), (22, 22, 26))
    d = ImageDraw.Draw(sheet); font = ImageFont.truetype(("C:/Windows/Fonts/arialbd.ttf" if sys.platform == "win32" else "/System/Library/Fonts/Supplemental/Arial Bold.ttf"), 10)
    for k, cl in enumerate(clips):
        gx = gap + (k % per) * (3 * tw + 4 + gap); gy = gap + (k // per) * (th + lab + gap)
        d0 = cl["t1"] - cl["t0"]; ts = [cl["t0"] + 0.08 * d0, cl["t0"] + 0.5 * d0, cl["t1"] - 0.08 * d0]
        off = False
        for j, t in enumerate(ts):
            s = src_at(cl, t); img = frame_at(cl["file"], s)
            if img is None: continue
            H, W = img.shape[:2]; band = plan.get("band"); BW, BH = (CW, band[1]) if band else (CW, CH)
            ax0, ay0, ax1, ay1 = cl.get("active") or [0, 0, W, H]
            base = max(BW / (ax1 - ax0), BH / (ay1 - ay0)); z = interp(cl.get("zoom", 1), t) or 1; sc = base * z
            f = cl.get("focus")
            if f and isinstance(f[0], list): fx, fy = interp(f, t)
            elif f: fx, fy = f
            else: fx, fy = W / 2, H / 2
            fx = fx * W if fx <= 1.5 else fx; fy = fy * H if fy <= 1.5 else fy
            hw, hh = BW / 2 / sc, BH / 2 / sc
            cx = min(ax1 - hw, max(ax0 + hw, fx)); cy = min(ay1 - hh, max(ay0 + hh, fy))
            box = (int(cx - hw), int(cy - hh), int(cx + hw), int(cy + hh))
            bth = int(round(th * BH / CH)); by = int(round(th * band[0] / CH)) if band else 0
            crop = Image.fromarray(img).crop(box).resize((tw, bth))
            if cl.get("fit"):          # whole frame letterboxed over a dark copy, like edits_lib fitClip
                fh = int(round(tw * H / W)); bgc = Image.fromarray((np.asarray(crop) * 0.35).astype(np.uint8))
                bgc.paste(Image.fromarray(img).resize((tw, fh)), (0, (th - fh) // 2)); crop = bgc; cl = dict(cl, matte=None)
            m = cl.get("matte")
            if m:
                mi = frame_at(m["file"], s - m["src0"])
                if mi is not None:
                    a = np.asarray(Image.fromarray(mi[..., 0]).crop(box).resize((tw, bth))).astype(np.float32) / 255
                    ca = np.asarray(crop).astype(np.float32); tint = np.array([255, 40, 40], np.float32)
                    crop = Image.fromarray((ca * (1 - 0.35 * a[..., None]) + tint * 0.35 * a[..., None]).astype(np.uint8))
                    ys, xs = np.nonzero(a > 0.5)
                    if len(xs) and not (0.2 * tw < xs.mean() < 0.8 * tw): off = True
            if bth != th:                 # letterbox: the band on black
                full = Image.new("RGB", (tw, th), (0, 0, 0)); full.paste(crop, (0, by)); crop = full
            x = gx + j * (tw + 2); sheet.paste(crop, (x, gy)); dd = ImageDraw.Draw(sheet)
            for yy in (0.10, 0.76): dd.line([(x, gy + yy * th), (x + tw, gy + yy * th)], fill=(0, 200, 220), width=1)
            for w in plan.get("words", []):
                if w["t0"] <= t < w["t1"]:
                    sz = w.get("size", 190); n = len(w["text"]); tr = w.get("tracking", 0) / 1000
                    try:                     # real metrics of the font AE will use
                        import typeset
                        ww, wh = typeset.measure(w["text"], w.get("font", "ProximaNova-Semibold" if w.get("style") == "cap" else "GalanoGrotesque-Black"), sz, w.get("tracking", 0))
                    except Exception:
                        ww = n * sz * (0.62 + tr); wh = 0.72 * sz
                    px, py = w.get("x", CW / 2), w.get("y", CH / 2)   # y = BASELINE
                    r = [(px - ww / 2) / CW * tw, (py - wh) / CH * th, (px + ww / 2) / CW * tw, py / CH * th]
                    dd.rectangle([x + r[0], gy + r[1], x + r[2], gy + r[3]], outline=(255, 220, 0), width=1)
        zl = cl.get("zoom", 1); zs = f"{zl:.2f}" if not isinstance(zl, list) else f"{zl[0][1]:.2f}>{zl[-1][1]:.2f}"
        d.text((gx, gy + th + 2), f"{k:02d} {cl['t0']:.2f}-{cl['t1']:.2f} z{zs}", fill=(255, 90, 90) if off else (235, 235, 235), font=font)
        d.text((gx, gy + th + 13), cl.get("name", "")[:30], fill=(150, 200, 255), font=font)
    sheet.save(out); print(out, sheet.size, len(clips), "clips")


if __name__ == "__main__":
    main()
