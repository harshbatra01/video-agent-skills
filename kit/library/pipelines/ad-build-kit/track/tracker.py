"""Planar board tracker (numpy only): robust inverse-compositional affine Lucas-Kanade on a 3-level pyramid,
global rotation/scale/translation search at the start of every jump-cut piece.
Coordinates: 1512x852 frames (source / 4). Affine p = [a11-1, a21, a12, a22-1, tx, ty] maps reference -> frame."""
import numpy as np
from PIL import Image


def load_gray(path):
    a = np.asarray(Image.open(path).convert('RGB')).astype(np.float32)
    return 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]


def blur(a, r=1):
    """small separable box-ish blur (3 passes of 3-tap) to tame noise / aliasing"""
    k = np.array([0.25, 0.5, 0.25], np.float32)
    for _ in range(r):
        a = np.pad(a, 1, mode='edge')
        a = k[0] * a[:-2, 1:-1] + k[1] * a[1:-1, 1:-1] + k[2] * a[2:, 1:-1]
        a = np.pad(a, 1, mode='edge')
        a = k[0] * a[1:-1, :-2] + k[1] * a[1:-1, 1:-1] + k[2] * a[1:-1, 2:]
    return a


def down(a):
    a = blur(a, 1)
    h, w = a.shape
    return a[:h - h % 2:2, :w - w % 2:2] * 0.25 + a[1:h - h % 2:2, :w - w % 2:2] * 0.25 + a[:h - h % 2:2, 1:w - w % 2:2] * 0.25 + a[1:h - h % 2:2, 1:w - w % 2:2] * 0.25


def pyramid(a, n=3):
    out = [blur(a, 1)]
    for _ in range(n - 1): out.append(down(out[-1]))
    return out          # [full, half, quarter]


def bilinear(img, x, y):
    h, w = img.shape
    x = np.clip(x, 0, w - 1.001); y = np.clip(y, 0, h - 1.001)
    x0 = np.floor(x).astype(np.int32); y0 = np.floor(y).astype(np.int32)
    fx = x - x0; fy = y - y0
    a = img[y0, x0]; b = img[y0, x0 + 1]; c = img[y0 + 1, x0]; d = img[y0 + 1, x0 + 1]
    return a * (1 - fx) * (1 - fy) + b * fx * (1 - fy) + c * (1 - fx) * fy + d * fx * fy


def mat(p):
    return np.array([[1 + p[0], p[2], p[4]], [p[1], 1 + p[3], p[5]], [0, 0, 1]], np.float64)


def vec(M):
    return np.array([M[0, 0] - 1, M[1, 0], M[0, 1], M[1, 1] - 1, M[0, 2], M[1, 2]], np.float64)


def scale_p(p, f):
    """affine params at a pyramid level f times the resolution"""
    q = p.copy(); q[4] *= f; q[5] *= f
    return q


class Template:
    def __init__(self, ref_img, region_mask, levels=3):
        self.pyr = pyramid(ref_img, levels)
        self.lv = []
        m = region_mask.astype(np.float32)
        for k, T in enumerate(self.pyr):
            mk = m
            for _ in range(k): mk = down(mk)
            ys, xs = np.nonzero(mk > 0.5)
            gy, gx = np.gradient(T)
            g = np.hypot(gx, gy)[ys, xs]
            keep = g > np.percentile(g, 35)            # textured pixels only (text, frame edges)
            ys, xs = ys[keep], xs[keep]
            tv = T[ys, xs]; Gx = gx[ys, xs]; Gy = gy[ys, xs]
            X = xs.astype(np.float64); Y = ys.astype(np.float64)
            SD = np.stack([Gx * X, Gy * X, Gx * Y, Gy * Y, Gx, Gy], 1)
            self.lv.append(dict(xs=X, ys=Y, tv=(tv - tv.mean()) / (tv.std() + 1e-6), SD=SD, tstd=tv.std(), tmean=tv.mean()))

    def align(self, img_pyr, p, iters=(30, 15, 8)):
        """refine p (full-res params) for one frame; returns p, ncc"""
        p = p.copy()
        for k in reversed(range(len(self.lv))):
            L = self.lv[k]; f = 0.5 ** k; I = img_pyr[k]
            q = scale_p(p, f)
            for it in range(iters[k] if k < len(iters) else 10):
                M = mat(q)
                wx = M[0, 0] * L['xs'] + M[0, 1] * L['ys'] + M[0, 2]
                wy = M[1, 0] * L['xs'] + M[1, 1] * L['ys'] + M[1, 2]
                iv = bilinear(I, wx, wy)
                med = np.median(iv); mad = np.median(np.abs(iv - med)) * 1.4826 + 1e-6
                ivn = (iv - iv.mean()) / (iv.std() + 1e-6)
                e = ivn - L['tv']
                s = np.median(np.abs(e)) * 1.4826 + 1e-6
                c = 4.685 * s
                w = np.where(np.abs(e) < c, (1 - (e / c) ** 2) ** 2, 0.0)       # Tukey
                SD = L['SD'] / (L['tstd'] + 1e-6)
                H = (SD * w[:, None]).T @ SD
                b = (SD * w[:, None]).T @ e
                try: dp = np.linalg.solve(H + np.eye(6) * 1e-6, b)
                except np.linalg.LinAlgError: break
                # inverse compositional update: W(p) <- W(p) o W(dp)^-1
                q = vec(mat(q) @ np.linalg.inv(mat(dp)))
                if np.abs(dp[4:]).max() < 0.01 and np.abs(dp[:4]).max() < 1e-5: break
            p = scale_p(q, 1 / f)
        # final ncc at full res
        L = self.lv[0]; M = mat(p)
        iv = bilinear(img_pyr[0], M[0, 0] * L['xs'] + M[0, 1] * L['ys'] + M[0, 2], M[1, 0] * L['xs'] + M[1, 1] * L['ys'] + M[1, 2])
        ivn = (iv - iv.mean()) / (iv.std() + 1e-6)
        return p, float((ivn * L['tv']).mean())


def ncc_search(img, tmpl, tmask):
    """normalized cross-correlation of a masked template over an image (FFT); returns best (x, y) of template origin and score"""
    H, W = img.shape; h, w = tmpl.shape
    tm = tmask.astype(np.float64); n = tm.sum()
    t = (tmpl - (tmpl * tm).sum() / n) * tm
    t /= np.sqrt((t ** 2).sum()) + 1e-9
    F = lambda a: np.fft.rfft2(a, s=(H + h, W + w))
    iF = lambda a: np.fft.irfft2(a, s=(H + h, W + w))
    I = img.astype(np.float64)
    num = iF(F(I) * np.conj(F(t)))[:H - h + 1, :W - w + 1]
    s1 = iF(F(I) * np.conj(F(tm)))[:H - h + 1, :W - w + 1]
    s2 = iF(F(I * I) * np.conj(F(tm)))[:H - h + 1, :W - w + 1]
    var = np.maximum(s2 - s1 ** 2 / n, 1e-6)
    score = num / np.sqrt(var)
    y, x = np.unravel_index(np.argmax(score), score.shape)
    return x, y, float(score[y, x])


def global_init(tpl_img, quad, img, levels_down=2):
    """search rotation/scale/translation of the board (reference quad) in a new frame at 1/4 resolution.
    returns full-res affine params"""
    f = 0.5 ** levels_down
    T = tpl_img; I = img
    for _ in range(levels_down): T = down(T); I = down(I)
    q = np.asarray(quad, np.float64) * f
    cx, cy = q.mean(0)
    best = None
    for ang in np.arange(-24, 24.1, 2.0):
        for sc in (0.88, 0.94, 1.0, 1.06, 1.12):
            a = np.deg2rad(ang)
            R = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]]) * sc
            # bounding box of the transformed quad
            qq = (q - [cx, cy]) @ R.T
            x0, y0 = np.floor(qq.min(0)).astype(int) - 2; x1, y1 = np.ceil(qq.max(0)).astype(int) + 2
            gx, gy = np.meshgrid(np.arange(x0, x1), np.arange(y0, y1))
            Ri = np.linalg.inv(R)
            sx = Ri[0, 0] * gx + Ri[0, 1] * gy + cx; sy = Ri[1, 0] * gx + Ri[1, 1] * gy + cy
            patch = bilinear(T, sx, sy)
            # inside test against the reference quad (convex, either winding)
            cr = []
            for i in range(4):
                ax, ay = q[i]; bx, by = q[(i + 1) % 4]
                cr.append((bx - ax) * (sy - ay) - (by - ay) * (sx - ax))
            cr = np.stack(cr)
            inside = np.all(cr >= 0, 0) | np.all(cr <= 0, 0)
            if inside.sum() < 50: continue
            x, y, s = ncc_search(I, patch, inside)
            if best is None or s > best[0]: best = (s, ang, sc, x - x0, y - y0)
    s, ang, sc, ox, oy = best
    a = np.deg2rad(ang)
    R = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]]) * sc
    # frame point = R (ref - c) + (ox, oy)   (at 1/4 res)  -> full res
    t = np.array([ox, oy]) - R @ np.array([cx, cy])
    M = np.eye(3); M[:2, :2] = R; M[:2, 2] = t / f
    return vec(M), s, ang, sc
