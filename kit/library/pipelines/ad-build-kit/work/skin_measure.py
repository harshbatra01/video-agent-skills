"""Skin tone drift: median Lab of warm (R>G>B) pixels in the face/upper-body box of exported frames.
usage: python skin_measure.py name1 name2 ...  (from _claude_check_frames)"""
import sys
import numpy as np
from PIL import Image
D = r'C:\VISION\IMMUFIX\repair\ENCODED RUSHES\_claude_check_frames'


def to_lab(rgb):
    c = rgb / 255.0
    c = np.where(c > 0.04045, ((c + 0.055) / 1.055) ** 2.4, c / 12.92)
    M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    xyz = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[:, 1] - 16, 500 * (f[:, 0] - f[:, 1]), 200 * (f[:, 1] - f[:, 2])], 1)


for n in sys.argv[1:]:
    a = np.asarray(Image.open('%s\\%s.png' % (D, n)).convert('RGB')).astype(np.float32)
    box = a[120:760, 260:820].reshape(-1, 3)
    r, g, b = box[:, 0], box[:, 1], box[:, 2]
    skin = box[(r > g + 6) & (g > b + 4) & (r - b > 28) & (r > 95) & (r < 250)]
    lab = to_lab(skin)
    L, A_, B_ = np.median(lab, 0)
    print('%-14s n=%6d  L %.1f  a* %.2f  b* %.2f   (R/G %.3f  B/G %.3f)' % (n, len(skin), L, A_, B_, np.median(skin[:, 0] / skin[:, 1]), np.median(skin[:, 2] / skin[:, 1])))
