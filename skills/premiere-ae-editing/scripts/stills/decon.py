"""Edge colour decontamination for cutouts: removes the studio-background colour baked into semi-transparent
(hair) pixels. C = a*F + (1-a)*B  ->  F = (C - (1-a)*B) / a, with B estimated from the real background around her.
usage: python decon.py source_image cutout_ps.png out.png"""
import sys
import numpy as np
from PIL import Image


def box(x, r):
    """box blur (separable, cumsum) along both axes, same size; x is float HxW or HxWxC"""
    for ax in (0, 1):
        c = np.cumsum(np.pad(x, [(r + 1, r) if a == ax else (0, 0) for a in range(x.ndim)], mode='edge'), axis=ax)
        sl_hi = [slice(None)] * x.ndim; sl_lo = [slice(None)] * x.ndim
        sl_hi[ax] = slice(2 * r + 1, None); sl_lo[ax] = slice(0, -(2 * r + 1))
        x = (c[tuple(sl_hi)] - c[tuple(sl_lo)]) / (2 * r + 1)
    return x


def gblur(x, r):
    for _ in range(3): x = box(x, r)
    return x


def normconv(val, w, r):
    num = gblur(val * w[..., None], r); den = gblur(w, r)[..., None]
    return num / np.maximum(den, 1e-6), den[..., 0]


src, cut, out = sys.argv[1:4]
C = np.asarray(Image.open(src).convert('RGB')).astype(np.float64)
cp = np.asarray(Image.open(cut).convert('RGBA')).astype(np.float64)
if cp.shape[:2] != C.shape[:2]: raise SystemExit('size mismatch %s vs %s' % (cp.shape, C.shape))
a = cp[..., 3] / 255.0
# background estimate from clearly-background pixels
bgm = (a < 0.02).astype(np.float64)
B, wb = normconv(C, bgm, 18)
B2, wb2 = normconv(C, bgm, 60)
B = np.where((wb < 0.02)[..., None], B2, B)
B = np.where((wb2 < 0.002)[..., None], (C * bgm[..., None]).sum((0, 1)) / max(bgm.sum(), 1), B)
aa = np.maximum(a, 0.05)[..., None]
F = np.clip((C - (1 - a[..., None]) * B) / aa, 0, 255)
# smooth estimate for very thin strands (weights favour solid pixels)
Fs, _ = normconv(F, a ** 2, 3)
t = np.clip((a - 0.12) / 0.38, 0, 1)[..., None]
Fo = np.where(a[..., None] >= 0.5, F, t * F + (1 - t) * Fs)
Fo = np.where(a[..., None] >= 0.985, C, Fo)
# fill RGB under fully transparent pixels with nearby foreground colour (clean edges when scaled)
Fd, _ = normconv(Fo, (a > 0.3).astype(np.float64), 6)
Fo = np.where(a[..., None] < 0.01, Fd, Fo)
res = np.dstack([np.clip(Fo, 0, 255), a * 255]).round().astype(np.uint8)
Image.fromarray(res, 'RGBA').save(out)
edge = (a > 0.03) & (a < 0.97)
print('%s: edge px %d, mean |change| on edges %.1f' % (out.split('/')[-1], edge.sum(), np.abs(Fo - C)[edge].mean()))
