# B-roll report sheets + metrics. One mid-frame per shot, labelled with #, time, length and the words said.
# python3 -I broll_sheets.py <video> <shots.json> <words.json> <out_dir> <prefix>
# shots.json: list of {t0,t1} (ref_stats format, or an edit_vX.json list). Writes <prefix>_metrics.json and sheets.
# Metrics per shot: fill = share of the frame with picture detail (not flat black/blur bars, 16px tiles with local
#   contrast), sharp = Laplacian variance at 540 px wide (higher = crisper), motion = moving video vs still (aligned residual).
import json, subprocess, sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
v, sj, wj, od, px = sys.argv[1:6]
shots = json.load(open(sj)); W = json.load(open(wj))["words"]
fps = eval(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", v], capture_output=True, text=True).stdout)
def grab(t, w=540):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", v, "-frames:v", "1", "-vf", f"scale={w}:-2", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    import io; return Image.open(io.BytesIO(raw)).convert("RGB")
def fill(im):
    g = np.asarray(im.convert("L"), np.float32); h, w = g.shape; T = 16
    g = g[:h // T * T, :w // T * T].reshape(h // T, T, w // T, T)
    sd = g.std(axis=(1, 3)); mn = g.mean(axis=(1, 3))
    return float(((sd > 6) & (mn > 12)).mean())
def sharp(im):
    g = np.asarray(im.convert("L"), np.float32)
    lap = g[1:-1, 1:-1] * 4 - g[:-2, 1:-1] - g[2:, 1:-1] - g[1:-1, :-2] - g[1:-1, 2:]
    return float(lap.var())
def motion(t0, t1):
    if t1 - t0 < 0.25: return None
    a = np.asarray(grab(t0 + 0.08, 160).convert("L"), np.float32); b = np.asarray(grab(t1 - 0.08, 160).convert("L"), np.float32)
    best = 1e9
    for s in (0.94, 0.97, 1.0, 1.03, 1.06):
        A = np.asarray(Image.fromarray(a.astype(np.uint8)).resize((int(a.shape[1] * s), int(a.shape[0] * s))), np.float32)
        h, w = b.shape; cy, cx = (A.shape[0] - h) // 2, (A.shape[1] - w) // 2
        if s >= 1: A = A[cy:cy + h, cx:cx + w]
        else: A = np.pad(A, ((-cy, h - A.shape[0] + cy), (-cx, w - A.shape[1] + cx)), mode="edge")
        for dx in range(-4, 5, 2):
            for dy in range(-4, 5, 2):
                best = min(best, np.abs(np.roll(np.roll(A, dx, 1), dy, 0)[8:-8, 8:-8] - b[8:-8, 8:-8]).mean())
    return round(float(best), 1)
out = []
try: font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 15)
except Exception: font = ImageFont.load_default()
tiles = []
for i, s in enumerate(shots):
    t0, t1 = s["t0"], s["t1"]; tm = (t0 + t1) / 2
    im = grab(tm)
    said = " ".join(x["w"] for x in W if x["s"] < t1 and x["e"] > t0)
    m = motion(t0, t1)
    r = {"n": i + 1, "t0": round(t0, 2), "t1": round(t1, 2), "dur": round(t1 - t0, 2), "said": said,
         "fill": round(fill(im), 2), "sharp": round(sharp(im)), "motion": m,
         "kind": "too short" if m is None else ("video" if m > 6 else "still/push")}
    if "vis" in s: r["src"] = s["vis"].get("f", s["vis"].get("k")); r["fx"] = s.get("fx")
    out.append(r)
    th = im.resize((216, int(216 * im.height / im.width)))
    c = Image.new("RGB", (216, th.height + 58), (20, 20, 20)); c.paste(th, (0, 0)); d = ImageDraw.Draw(c)
    d.text((4, th.height + 2), f"#{i+1}  {t0:.2f}s  {t1-t0:.2f}s  {r['kind']}", fill=(255, 220, 0), font=font)
    d.text((4, th.height + 20), said[:30], fill=(255, 255, 255), font=font)
    d.text((4, th.height + 38), said[30:60], fill=(255, 255, 255), font=font)
    tiles.append(c)
json.dump(out, open(f"{od}/{px}_metrics.json", "w"), indent=0)
per = 24; cols = 8
for k in range(0, len(tiles), per):
    grp = tiles[k:k + per]; tw, th = grp[0].size; rows = (len(grp) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * th), (0, 0, 0))
    for j, t in enumerate(grp): sheet.paste(t, ((j % cols) * tw, (j // cols) * th))
    sheet.save(f"{od}/{px}_sheet_{k // per + 1:02d}.jpg", quality=85)
print(px, len(out), "shots; sheets", (len(tiles) + per - 1) // per)
