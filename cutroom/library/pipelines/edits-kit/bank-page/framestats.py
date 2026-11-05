"""Per-frame stats for edit renders + version diffs.

usage: python framestats.py OUTDIR ref.mp4 other1.mp4 other2.mp4 ...
Writes OUTDIR/<name>.npz (thumbs 96x54 portrait-aware, stats) and OUTDIR/summary.txt
"""
import sys, os, json
import numpy as np
import av

def decode(path, tw, th):
    c = av.open(path)
    s = c.streams.video[0]
    s.thread_type = "AUTO"
    fps = float(s.average_rate)
    thumbs = []
    for fr in c.decode(s):
        img = fr.reformat(width=tw, height=th, format="rgb24").to_ndarray()
        thumbs.append(img)
    c.close()
    return fps, np.stack(thumbs).astype(np.float32)

def stats(th):
    r, g, b = th[..., 0], th[..., 1], th[..., 2]
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    mx = th.max(-1); mn = th.min(-1)
    sat = np.where(mx > 1, (mx - mn) / np.maximum(mx, 1), 0)
    ymean = y.mean((1, 2)); ystd = y.std((1, 2))
    satm = sat.mean((1, 2))
    # frame diff on luma
    d = np.zeros(len(y)); d[1:] = np.abs(y[1:] - y[:-1]).mean((1, 2))
    # edge energy (sharpness proxy)
    gx = np.abs(np.diff(y, axis=2)).mean((1, 2)); gy = np.abs(np.diff(y, axis=1)).mean((1, 2))
    edge = gx + gy
    # bright fraction (white flash) and dark fraction
    bright = (y > 235).mean((1, 2)); dark = (y < 20).mean((1, 2))
    # global shift via phase correlation between consecutive frames (center crop)
    shifts = np.zeros((len(y), 2))
    H, W = y.shape[1:]
    win = np.outer(np.hanning(H), np.hanning(W))
    F_prev = None
    for i in range(len(y)):
        F = np.fft.fft2((y[i] - y[i].mean()) * win)
        if F_prev is not None:
            R = F * np.conj(F_prev); R /= np.maximum(np.abs(R), 1e-6)
            cc = np.fft.ifft2(R).real
            py, px = np.unravel_index(np.argmax(cc), cc.shape)
            if py > H // 2: py -= H
            if px > W // 2: px -= W
            shifts[i] = (px, py)
        F_prev = F
    return dict(ymean=ymean, ystd=ystd, sat=satm, diff=d, edge=edge, bright=bright, dark=dark, shift=shifts)

def main():
    out = sys.argv[1]; files = sys.argv[2:]
    os.makedirs(out, exist_ok=True)
    data = {}
    for f in files:
        name = os.path.splitext(os.path.basename(f))[0]
        c = av.open(f); s = c.streams.video[0]; W, H = s.codec_context.width, s.codec_context.height; c.close()
        tw, th_ = (54, 96) if H > W else (96, 54)
        fps, th = decode(f, tw, th_)
        st = stats(th)
        np.savez_compressed(os.path.join(out, name + ".npz"), thumbs=th.astype(np.uint8), fps=fps, **st)
        data[name] = (fps, th, st)
        print(f"{name}: {len(th)} frames @ {fps:.3f} fps", flush=True)
    # version diffs vs first file
    ref = os.path.splitext(os.path.basename(files[0]))[0]
    rfps, rth, _ = data[ref]
    lines = []
    for name, (fps, th, st) in data.items():
        if name == ref: continue
        n = min(len(th), len(rth))
        d = np.abs(th[:n] - rth[:n]).mean((1, 2, 3))
        bad = d > 6.0
        ranges = []; i = 0
        while i < n:
            if bad[i]:
                j = i
                while j + 1 < n and bad[j + 1]: j += 1
                ranges.append((i, j, float(d[i:j + 1].max())))
                i = j + 1
            else:
                i += 1
        txt = ", ".join(f"f{a}-{b} ({a/fps:.2f}-{(b+1)/fps:.2f}s, max{m:.0f})" for a, b, m in ranges)
        lines.append(f"{name} vs {ref}: frames={len(th)} differing={int(bad.sum())} :: {txt}")
    with open(os.path.join(out, "versions.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))

if __name__ == "__main__":
    main()
