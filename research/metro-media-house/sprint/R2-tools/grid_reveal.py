#!/usr/bin/env python3
"""Grid reveal opener: photo blurred, then 3x3 white blocks pop 2-3 at a time,
hold 2-3 frames, fade to the sharp photo over 3-4 frames. Faint 1px grid lines.
Usage: grid_reveal.py <image> <out.mp4> [--w 1920 --h 1080 --fps 25 --dur 1.5 --seed 1] [--sheet sheet.png]
"""
import argparse, random, subprocess
import numpy as np
from PIL import Image, ImageFilter, ImageOps

WHITE = np.array([0xF2, 0xF1, 0xEF], np.float32)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image"); ap.add_argument("out")
    ap.add_argument("--w", type=int, default=1920); ap.add_argument("--h", type=int, default=1080)
    ap.add_argument("--fps", type=int, default=25); ap.add_argument("--dur", type=float, default=1.5)
    ap.add_argument("--seed", type=int, default=1); ap.add_argument("--sheet", default=None)
    a = ap.parse_args()
    rng = random.Random(a.seed)
    img = ImageOps.fit(Image.open(a.image).convert("RGB"), (a.w, a.h), Image.LANCZOS)
    sharp = np.asarray(img, np.float32)
    blur = np.asarray(img.filter(ImageFilter.GaussianBlur(max(4, a.w // 60))), np.float32)
    n = int(round(a.fps * a.dur))
    xs = [round(i * a.w / 3) for i in range(4)]; ys = [round(i * a.h / 3) for i in range(4)]
    cells = [(r, c) for r in range(3) for c in range(3)]; rng.shuffle(cells)
    groups, i = [], 0
    while i < 9:
        k = min(rng.choice([2, 3]), 9 - i); groups.append(cells[i:i + k]); i += k
    span = max(1, int(a.fps * 1.0) - 7)  # all pops inside ~1 s incl. hold+fade
    sched = {}
    for gi, g in enumerate(groups):
        s = 2 + round(gi * span / max(1, len(groups) - 1))
        for cell in g:
            sched[cell] = (s, rng.choice([2, 3]), rng.choice([3, 4]))
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{a.w}x{a.h}", "-r", str(a.fps), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-crf", "18", a.out], stdin=subprocess.PIPE)
    frames = []
    for f in range(n):
        fr = blur.copy()
        for (r, c), (s, hold, fade) in sched.items():
            y0, y1, x0, x1 = ys[r], ys[r + 1], xs[c], xs[c + 1]
            if f < s: continue
            t = f - s
            if t < hold: fr[y0:y1, x0:x1] = WHITE
            elif t < hold + fade:
                al = (t - hold + 1) / (fade + 1)
                fr[y0:y1, x0:x1] = WHITE * (1 - al) + sharp[y0:y1, x0:x1] * al
            else: fr[y0:y1, x0:x1] = sharp[y0:y1, x0:x1]
        for x in xs[1:3]: fr[:, x] = fr[:, x] * 0.75 + 255 * 0.25
        for y in ys[1:3]: fr[y, :] = fr[y, :] * 0.75 + 255 * 0.25
        out = np.clip(fr, 0, 255).astype(np.uint8)
        ff.stdin.write(out.tobytes())
        if a.sheet: frames.append(Image.fromarray(out).resize((a.w // 4, a.h // 4)))
    ff.stdin.close(); ff.wait()
    if a.sheet and frames:
        cols = 6; tw, th = frames[0].size; rows = (len(frames) + cols - 1) // cols
        sh = Image.new("RGB", (cols * tw, rows * th), (20, 20, 20))
        for j, im in enumerate(frames): sh.paste(im, ((j % cols) * tw, (j // cols) * th))
        sh.save(a.sheet)
    print("wrote", a.out, n, "frames; groups", [len(g) for g in groups])

if __name__ == "__main__":
    main()
