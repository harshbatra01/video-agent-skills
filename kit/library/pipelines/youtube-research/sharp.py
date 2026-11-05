"""Sharpness (variance of Laplacian-ish) per grabbed frame, measured inside a crop box (fractions of frame)."""
import sys, os, glob, re
import numpy as np
from PIL import Image
FPS = 24000 / 1001


def fnum(f):
    return int(re.search(r'g_(\d+)', os.path.basename(f)).group(1))


def sharpness(path, box=None):
    im = Image.open(path).convert('L')
    if box:
        W, H = im.size
        im = im.crop((int(box[0] * W), int(box[1] * H), int(box[2] * W), int(box[3] * H)))
    a = np.asarray(im, dtype=np.float32)
    lap = a[1:-1, 1:-1] * 4 - a[:-2, 1:-1] - a[2:, 1:-1] - a[1:-1, :-2] - a[1:-1, 2:]
    return float(lap.var())


def table(folder, t_from, t_to, box=None):
    out = []
    for f in sorted(glob.glob(os.path.join(folder, 'g_*.png'))):
        t = (fnum(f) - 1) / FPS
        if t_from <= t <= t_to:
            out.append((t, sharpness(f, box), f))
    return out


if __name__ == '__main__':
    folder, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
    box = tuple(map(float, sys.argv[4].split(','))) if len(sys.argv) > 4 else None
    for t, s, f in table(folder, a, b, box):
        print('%6.2f  %8.1f  %s' % (t, s, '#' * int(min(s, 2000) / 25)))
