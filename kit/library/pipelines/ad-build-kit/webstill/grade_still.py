"""Website still: learn the approved ad grade (LOG source -> final render) from C121 in 'Secret weapon v4' (same park,
same camera, same Lumetri as every C121 use), apply it to C120 at 21.56 s, crop 4:5, export."""
import os, sys
import av, numpy as np
from PIL import Image, ImageFilter
from av.video.reformatter import Colorspace, ColorRange
B = r'C:/VISION/IMMUFIX/repair/ENCODED RUSHES/B roll/'
REN = r'C:/VISION/IMMUFIX/repair/Renders/V4s/Secret weapon v4.mp4'
OUTD = r'C:/VISION/IMMUFIX/repair/Renders/Website stills'
os.makedirs(OUTD, exist_ok=True)


def frame_at(path, t, fps):
    c = av.open(path); v = c.streams.video[0]; v.thread_type = 'AUTO'; tb = v.time_base
    c.seek(int(max(0, t - 1.5) / tb), stream=v, backward=True)
    for fr in c.decode(v):
        if fr.pts * tb > t - 0.5 / fps:
            a = fr.reformat(format='rgb24', src_colorspace=Colorspace.ITU709, src_color_range=ColorRange.MPEG,
                            dst_color_range=ColorRange.JPEG).to_ndarray()
            c.close(); return a, float(fr.pts * tb)


# 1. reference pair: render t = 17.5 s (Secret weapon C121 item 17.2-18.8833, src in 14.0, Motion scale 57 centred)
ren, tr = frame_at(REN, 17.5, 60)
src_t = 14.0 + (tr - 17.2)
c121, ts = frame_at(B + 'A003_09181330_C121.mp4', src_t - 0.02, 25)     # frame whose interval holds src_t
print('render t %.4f -> src %.4f, source frame t %.4f' % (tr, src_t, ts))
S = 0.57; x0 = (0 - 540) / S + 3024; x1 = (1080 - 540) / S + 3024; y0 = (0 - 960) / S + 1704; y1 = (1920 - 960) / S + 1704
aligned = np.asarray(Image.fromarray(c121).resize((1080, 1920), Image.BICUBIC, box=(x0, y0, x1, y1))).astype(np.float32) / 255
target = ren.astype(np.float32) / 255
# alignment check: best integer shift of gradient images
def grad(a): g = a.mean(2); return np.abs(np.diff(g, axis=1))[:-1] + np.abs(np.diff(g, axis=0))[:, :-1]
ga, gt = grad(aligned), grad(target); best = None
for dy in range(-4, 5):
    for dx in range(-4, 5):
        A = ga[8 + dy:-8 + dy, 8 + dx:-8 + dx]; T = gt[8:-8, 8:-8]
        r = np.corrcoef(A.ravel()[::7], T.ravel()[::7])[0, 1]
        if best is None or r > best[0]: best = (r, dx, dy)
print('alignment corr %.3f at shift dx %d dy %d' % best)
_, dx, dy = best
A = aligned[8 + dy:1920 - 8 + dy, 8 + dx:1080 - 8 + dx]; T = target[8:-8, 8:-8]


def feats(x, deg):
    r, g, b = x[..., 0], x[..., 1], x[..., 2]
    f = [np.ones_like(r), r, g, b, r * r, g * g, b * b, r * g, r * b, g * b]
    if deg >= 3: f += [r ** 3, g ** 3, b ** 3, r * r * g, r * r * b, g * g * r, g * g * b, b * b * r, b * b * g, r * g * b]
    if deg >= 4: f += [r ** 4, g ** 4, b ** 4, r ** 3 * g, r ** 3 * b, g ** 3 * r, g ** 3 * b, b ** 3 * r, b ** 3 * g,
                       r * r * g * g, r * r * b * b, g * g * b * b, r * r * g * b, g * g * r * b, b * b * r * g]
    return np.stack(f, -1)


X = A[::3, ::3].reshape(-1, 3); Y = T[::3, ::3].reshape(-1, 3)
rng = np.random.default_rng(0); idx = rng.permutation(len(X)); tr_i, va_i = idx[:len(idx) * 4 // 5], idx[len(idx) * 4 // 5:]
models = {}
for deg in (3, 4):
    keep = tr_i
    for it in range(3):                        # robust: drop pixels covered by captions / graphics
        F = feats(X[keep], deg); W, *_ = np.linalg.lstsq(F, Y[keep], rcond=None)
        res = np.abs(feats(X[tr_i], deg) @ W - Y[tr_i]).max(1)
        keep = tr_i[res < np.percentile(res, 85)]
    pv = feats(X[va_i], deg) @ W; rv = np.abs(pv - Y[va_i]).max(1); good = rv < np.percentile(rv, 85)
    rms = np.sqrt(((pv[good] - Y[va_i][good]) ** 2).mean()) * 255
    models[deg] = (rms, W); print('deg %d: validation RMS %.2f (8-bit units, clean 85%%)' % (deg, rms))
deg = min(models, key=lambda k: models[k][0]); W = models[deg][1]
apply = lambda x: np.clip(feats(x, deg) @ W, 0, 1)
# validation picture: render | model on source | difference x4
pm = apply(A)
cmp_ = np.concatenate([T, pm, np.clip(np.abs(pm - T) * 4, 0, 1)], 1)
Image.fromarray((cmp_ * 255).astype(np.uint8)).resize((3 * 300, int(300 * T.shape[0] / T.shape[1]))).save('fit_check.png')
# 2. the still: C120 at 21.56 s, 4:5 crop 2400x3000 around Paula + pouch
c120, t120 = frame_at(B + 'A003_09181328_C120.mp4', 21.56, 25)
cx0, cy0, CW, CH = 1825, 100, 2400, 3000
crop = c120[cy0:cy0 + CH, cx0:cx0 + CW].astype(np.float32) / 255
outp = np.zeros_like(crop)
for r0 in range(0, CH, 300): outp[r0:r0 + 300] = apply(crop[r0:r0 + 300])
im = Image.fromarray((outp * 255 + 0.5).astype(np.uint8)).filter(ImageFilter.UnsharpMask(radius=2.0, percent=55, threshold=2))
base = os.path.join(OUTD, 'Paula holding Immufix - website still')
im.save(base + '.jpg', quality=95, subsampling=0); im.save(base + '.png')
pv = im.copy(); pv.thumbnail((600, 750)); pv.save('still_preview.png')
print('C120 frame t %.3f; saved %s.jpg/.png %s (deg %d)' % (t120, base, im.size, deg))
