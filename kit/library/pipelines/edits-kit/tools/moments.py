"""Find an edit's most intense moments (transitions, flash stacks, effect bursts) and lay out every frame around them.

usage: python moments.py VIDEO OUT_PREFIX [--n 8] [--win 12] [--tw 160] [--skip-start 0] [--skip-end 0]
writes OUT_PREFIX.png (one row per moment, every frame, labelled) and OUT_PREFIX.json (per-frame metrics summary +
the moments). Metrics per frame (on a small copy of the picture):
  change   mean luma difference to the previous frame (cuts, flashes, whips)
  invert   luma correlation with the previous frame below -0.25 (a negative / inverted frame)
  hue      mean chroma change (colour flashes, hue cycling)
  blur     sharpness drop vs the local median (motion-blur / zoom-blur / whip frames)
  white    near-white frames (flash), black (dip)
Moments = the 12-frame windows with the most combined activity, at least 1 s apart. Use it to study how a top edit
builds its transitions frame by frame, and to compare our renders with theirs the same way.
"""
import sys, json
import numpy as np
import av
from PIL import Image, ImageDraw, ImageFont


def arg(name, default, cast=float):
    a = sys.argv
    return cast(a[a.index(name) + 1]) if name in a else default


def scan(path, w=96):
    c = av.open(path); s = c.streams.video[0]; s.thread_type = "AUTO"; fps = float(s.average_rate)
    H = int(round(s.codec_context.height * w / s.codec_context.width / 2) * 2)
    fr_rgb = []
    for fr in c.decode(s):
        fr_rgb.append(fr.reformat(width=w, height=H, format="rgb24").to_ndarray())
    c.close()
    return fps, np.stack(fr_rgb).astype(np.float32)


def metrics(a):
    y = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    n = len(y); flat = y.reshape(n, -1)
    z = (flat - flat.mean(1, keepdims=True)) / (flat.std(1, keepdims=True) + 1e-6)
    corr = np.ones(n); corr[1:] = (z[1:] * z[:-1]).mean(1)
    change = np.zeros(n); change[1:] = np.abs(y[1:] - y[:-1]).mean((1, 2))
    cb = a[..., 2] - y; cr = a[..., 0] - y
    hue = np.zeros(n); hue[1:] = (np.abs(cb[1:] - cb[:-1]) + np.abs(cr[1:] - cr[:-1])).mean((1, 2)) / 2
    gy = np.abs(np.diff(y, axis=1)).mean((1, 2)) + np.abs(np.diff(y, axis=2)).mean((1, 2))
    med = np.array([np.median(gy[max(0, i - 15): i + 16]) for i in range(n)])
    blur = np.clip(1 - gy / (med + 1e-6), 0, 1)
    mean = y.mean((1, 2)); sat = (a.max(3) - a.min(3)).mean((1, 2))
    return dict(change=change, corr=corr, hue=hue, blur=blur, mean=mean, sat=sat)


def main():
    path, prefix = sys.argv[1], sys.argv[2]
    n_m = int(arg("--n", 8)); win = int(arg("--win", 12)); tw = int(arg("--tw", 160))
    s0 = arg("--skip-start", 0.0); s1 = arg("--skip-end", 0.0)
    fps, a = scan(path)
    # measure the PICTURE only: crop letterbox / pillarbox bars found on the median frame (bars would make every
    # white frame grey and every bar edge look like structure)
    y_ = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    med = np.median(y_, axis=0); rows = np.where(med.mean(1) > 14)[0]; cols = np.where(med.mean(0) > 14)[0]
    if len(rows) > 4 and len(cols) > 4: a = a[:, rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1]
    m = metrics(a); n = len(a)
    inv = m["corr"] < -0.25
    score = m["change"] / 25 + 3.0 * inv + m["hue"] / 12 + 1.5 * (m["blur"] > 0.45) + 1.0 * (m["mean"] > 215) + 0.5 * (m["mean"] < 12)
    lo, hi = int(s0 * fps), n - int(s1 * fps)
    ws = np.convolve(score, np.ones(win), mode="same")
    picks = []
    order = np.argsort(-ws)
    for i in order:
        if i < lo + win // 2 or i > hi - win // 2: continue
        if all(abs(i - p) > fps * 1.0 for p in picks): picks.append(int(i))
        if len(picks) >= n_m: break
    picks.sort()
    # second pass: frames at display size
    want = {}
    for p in picks:
        for k in range(p - win // 2, p - win // 2 + win): want[k] = None
    c = av.open(path); st = c.streams.video[0]; th = int(round(tw * st.codec_context.height / st.codec_context.width))
    for i, fr in enumerate(c.decode(st)):
        if i in want: want[i] = fr.reformat(width=tw, height=th, format="rgb24").to_image()
        if i > max(want): break
    c.close()
    font = ImageFont.truetype(("C:/Windows/Fonts/arialbd.ttf" if sys.platform == "win32" else "/System/Library/Fonts/Supplemental/Arial Bold.ttf"), 11)
    sheet = Image.new("RGB", (win * (tw + 2) + 2, len(picks) * (th + 14) + 2), (24, 24, 28)); d = ImageDraw.Draw(sheet)
    for r, p in enumerate(picks):
        for j, k in enumerate(range(p - win // 2, p - win // 2 + win)):
            x = 2 + j * (tw + 2); y = 2 + r * (th + 14)
            if want.get(k) is not None: sheet.paste(want[k], (x, y))
            tag = ("INV " if 0 <= k < n and inv[k] else "") + ("BLR " if 0 <= k < n and m["blur"][k] > 0.45 else "")
            col = (255, 120, 120) if tag else (220, 220, 220)
            d.text((x + 2, y + th + 1), f"{k / fps:.2f} {tag}", fill=col, font=font)
    sheet.save(prefix + ".png")
    summ = dict(file=path, fps=fps, frames=n, dur=round(n / fps, 2),
                inverts=int(inv.sum()), invert_times=[round(i / fps, 2) for i in np.where(inv)[0]][:60],
                blur_frames=int((m["blur"] > 0.45).sum()), white_frames=int((m["mean"] > 215).sum()),
                big_changes=int((m["change"] > 30).sum()), hue_bursts=int((m["hue"] > 12).sum()),
                mean_sat=round(float(m["sat"].mean()), 1), moments=[round(p / fps, 2) for p in picks])
    json.dump(summ, open(prefix + ".json", "w"), indent=1)
    print(json.dumps({k: v for k, v in summ.items() if k not in ("invert_times",)}))


if __name__ == "__main__":
    main()
