"""analyze_frame.py: measure a Premiere Program Monitor screenshot.

Needs: pip install pillow numpy

Usage:
  python analyze_frame.py frame.png --grid
      saves frame_grid.png with x/y numbers, to help you place boxes
  python analyze_frame.py frame.png --exclude 0 350 406 380 --box forehead 180 105 230 125 --box sofa_shade 330 590 400 660
      whole-frame levels (caption band excluded) + stats for each box
  python analyze_frame.py frame.png --exclude 0 350 406 380 --simulate green=1.035 blue=0.975 shadow_blue=0.95 stops=0.3 blacks=0.06
      also saves frame_sim.png: a rough preview of a white balance / exposure / blacks change

Reading the numbers:
  luma      0-100, same scale as the Lumetri Luma waveform
  hue       HSV hue in degrees. Skin ~15-20 is peach. Under ~10 reads pink
  angle     vectorscope angle (Rec.709 Cb/Cr). Skin line ~123. Red box ~103. Yellow box ~175
            90 = 12 o'clock, 123 = about 11 o'clock. Skin under ~112 reads pink, over ~130 reads orange
  clipped   % of pixels with any channel at full white (detail gone)
"""
import argparse
import colorsys
import math

import numpy as np
from PIL import Image, ImageDraw


def load(path):
    return np.asarray(Image.open(path).convert("RGB")).astype(float) / 255.0


def luma(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def region(a, box):
    x0, y0, x1, y1 = box
    r, g, b = (float(v) for v in a[y0:y1, x0:x1].reshape(-1, 3).mean(0))
    h, s, _ = colorsys.rgb_to_hsv(r, g, b)
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    angle = math.degrees(math.atan2((r - y) / 1.5748, (b - y) / 1.8556))
    return {
        "rgb": tuple(int(round(v * 255)) for v in (r, g, b)),
        "hue": round(h * 360, 1),
        "sat": round(s, 2),
        "luma": round(y * 100, 1),
        "angle": round(angle, 1),
    }


def levels(a, exclude=None):
    y = luma(a)
    mask = np.ones(y.shape, bool)
    if exclude:
        x0, y0, x1, y1 = exclude
        mask[y0:y1, x0:x1] = False
    v = y[mask] * 100
    pct = {q: round(float(np.percentile(v, q)), 1) for q in (0.5, 1, 5, 50, 95, 99, 99.9)}
    clipped = round(float(((a.max(2) >= 0.995) & mask).mean() * 100), 2)
    max_rgb = [int(round(float(a[..., c][mask].max() * 255))) for c in range(3)]
    return pct, clipped, max_rgb


def grid(path):
    im = Image.open(path).convert("RGB")
    d = ImageDraw.Draw(im)
    for y in range(0, im.height, 50):
        d.line([(0, y), (8, y)], fill=(255, 255, 0))
        d.text((10, y - 5), str(y), fill=(255, 255, 0))
    for x in range(0, im.width, 50):
        d.line([(x, 0), (x, 8)], fill=(255, 255, 0))
        d.text((x + 2, 10), str(x), fill=(255, 255, 0))
    out = path.rsplit(".", 1)[0] + "_grid.png"
    im.resize((im.width * 2, im.height * 2)).save(out)
    return out


def simulate(a, green=1.0, blue=1.0, shadow_blue=1.0, stops=0.0, blacks=0.0):
    """Rough preview only. Lumetri will not match this exactly."""
    x = a.copy()
    dark = np.clip(1 - luma(a) / 0.35, 0, 1)  # 1 in the darks, 0 above about 35
    x[..., 1] *= green  # more green = less magenta/pink (like Tint to the left)
    x[..., 2] *= blue  # less blue = warmer (like Temperature to the right)
    x[..., 2] *= 1 - (1 - shadow_blue) * dark  # extra warmth only in the darks
    x *= (2 ** stops) ** (1 / 2.4)  # exposure in stops (display gamma about 2.4)
    x -= blacks * np.clip(1 - x / 0.5, 0, 1) ** 2  # pull the darks down, leave mids/highs
    return np.clip(x, 0, 1)


def report(a, boxes, exclude):
    pct, clipped, max_rgb = levels(a, exclude)
    print("Levels (0-100):", pct)
    print("Clipped pixels: %s%%   Max R,G,B (0-255): %s" % (clipped, max_rgb))
    for name, box in boxes:
        print("%-12s %s" % (name, region(a, box)))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("image")
    p.add_argument("--grid", action="store_true")
    p.add_argument("--box", nargs=5, action="append", default=[], metavar=("NAME", "X0", "Y0", "X1", "Y1"))
    p.add_argument("--exclude", nargs=4, type=int, metavar=("X0", "Y0", "X1", "Y1"), help="caption band to ignore")
    p.add_argument("--simulate", nargs="*", metavar="KEY=VALUE")
    args = p.parse_args()

    if args.grid:
        print("Grid saved:", grid(args.image))
        return

    a = load(args.image)
    boxes = [(b[0], tuple(int(v) for v in b[1:])) for b in args.box]
    print("== NOW ==")
    report(a, boxes, args.exclude)

    if args.simulate is not None:
        kw = {k: float(v) for k, v in (s.split("=") for s in args.simulate)}
        s = simulate(a, **kw)
        if args.exclude:  # keep captions untouched
            x0, y0, x1, y1 = args.exclude
            s[y0:y1, x0:x1] = a[y0:y1, x0:x1]
        out = args.image.rsplit(".", 1)[0] + "_sim.png"
        Image.fromarray((s * 255).round().astype(np.uint8)).save(out)
        print("\n== SIMULATED", kw, "==")
        report(s, boxes, args.exclude)
        print("Preview saved:", out)


if __name__ == "__main__":
    main()
