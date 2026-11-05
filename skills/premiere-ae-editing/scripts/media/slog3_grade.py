"""Natural grade for Sony S-Log3 / S-Gamut3.Cine footage without a vendor LUT (decoded as BT.709 limited range):
log -> scene linear -> Rec.709 primaries -> exposure -> soft filmic tone curve -> sRGB-ish display -> gentle saturation.
Also writes the whole chain as a .cube 3D LUT for ffmpeg (lut3d)."""
import numpy as np

M_SG3C_709 = np.array([[1.6269474, -0.5401385, -0.0868089],
                       [-0.1785155, 1.4179409, -0.2394254],
                       [-0.0444361, -0.1959199, 1.2403560]], np.float64)


def slog3_to_lin(v):
    """v = decoded full-range value 0-1 of a legal-range S-Log3 file -> scene linear reflectance (0.18 = grey)"""
    c = v * 876.0 + 64.0                                        # 10-bit code value
    return np.where(c >= 171.2102946929, (10.0 ** ((c - 420.0) / 261.5)) * 0.19 - 0.01, (c - 95.0) * 0.01125 / (171.2102946929 - 95.0))


def hable(x):
    A, B, C, D, E, F = 0.22, 0.30, 0.10, 0.20, 0.01, 0.30
    return ((x * (A * x + C * B) + D * E) / (x * (A * x + B) + D * F)) - E / F


def srgb_oetf(x):
    x = np.clip(x, 0, 1)
    return np.where(x <= 0.0031308, 12.92 * x, 1.055 * np.power(x, 1 / 2.4) - 0.055)


def grade(v, ev=0.0, sat=0.95, white=6.0, warm=0.0, lift=0.0, contrast=1.0):
    """v: (..., 3) decoded RGB 0-1. ev: exposure stops. white: scene value that maps to display white.
    contrast: >1 steeper around mid grey (applied in display space). warm: + = warmer (R up, B down)."""
    lin = slog3_to_lin(v) @ M_SG3C_709.T
    lin = np.maximum(lin, 0) * (2.0 ** ev) * 2.0               # x2: mid grey 0.18 -> 0.36 before the shoulder
    disp = hable(lin) / hable(np.float64(white))
    out = srgb_oetf(disp)
    if contrast != 1.0:
        out = 0.5 + (out - 0.5) * contrast
    if warm:
        out = out * np.array([1 + warm, 1.0, 1 - warm])
    y = (0.2126 * out[..., 0] + 0.7152 * out[..., 1] + 0.0722 * out[..., 2])[..., None]
    out = y + (out - y) * sat
    out = lift + out * (1 - lift)
    return np.clip(out, 0, 1)


def write_cube(path, size=33, **kw):
    g = np.linspace(0, 1, size)
    b, gg, r = np.meshgrid(g, g, g, indexing='ij')                  # .cube order: R fastest, then G, then B
    rgb = np.stack([r, gg, b], -1).reshape(-1, 3)
    out = grade(rgb, **kw)
    with open(path, 'w') as f:
        f.write('TITLE "immufix natural"\nLUT_3D_SIZE %d\nDOMAIN_MIN 0 0 0\nDOMAIN_MAX 1 1 1\n' % size)
        for o in out: f.write('%.6f %.6f %.6f\n' % tuple(o))
    return path


# ---- per-clip levels on top of the look (verified 12 Oct 2026 on 23 park / riverside / product clips):
# sample 3 frames of the clip, grade them, then black point -> 0.04 (1st percentile), white stretch k <= 1.35,
# and a gamma lift only if the mid-tones fell more than 15 %. Bake grade + levels into one 65^3 .cube per clip and run:
#   ffmpeg -ss T0 -i src.mp4 -t DUR -vf "scale=3840:2160:flags=lanczos:in_color_matrix=bt709:in_range=tv,format=gbrp16le,
#     lut3d=file=clip.cube:interp=tetrahedral,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p"
#     -c:v libx264 -preset slow -crf 16 -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -an out.mp4
# (run ffmpeg with cwd = the LUT folder: a "C:" path inside the filter needs escaping). ffmpeg output matched the numpy
# grade within ~3/255. Vertical 9:16: crop=H*9/16:H:x:0 before the scale, centre x on the subject (check first/mid/last frames).
LOOK = dict(warm=0.02, sat=1.06, contrast=1.06)


def clip_levels(frames, look=LOOK):
    """frames: list of decoded RGB 0-1 arrays from one clip -> dict(b0, k, gamma) for clip_chain()"""
    def luma(g): return 0.2126 * g[..., 0] + 0.7152 * g[..., 1] + 0.0722 * g[..., 2]
    g = np.concatenate([grade(f, **look).reshape(-1, 3) for f in frames]); y = luma(g)
    b0, w0, m_nat = np.percentile(y, 1), np.percentile(y, 99.5), np.median(y)
    k = min(1.35, max(1.0, 0.9 / (w0 - b0)))
    m2 = np.median(np.clip((y - b0) * k + 0.04, 0, 1))
    target = max(m2, 0.85 * m_nat)
    return dict(b0=float(b0), k=float(k), gamma=float(np.log(target) / np.log(m2)) if m2 > 0 else 1.0)


def clip_chain(v, p, look=LOOK):
    g = np.clip((grade(v, **look) - p['b0']) * p['k'] + 0.04, 0, 1)
    return np.power(g, p['gamma'])


def write_clip_cube(path, p, size=65, look=LOOK):
    gr = np.linspace(0, 1, size)
    b, g, r = np.meshgrid(gr, gr, gr, indexing='ij')
    out = clip_chain(np.stack([r, g, b], -1).reshape(-1, 3), p, look)
    with open(path, 'w') as f:
        f.write('LUT_3D_SIZE %d\nDOMAIN_MIN 0 0 0\nDOMAIN_MAX 1 1 1\n' % size)
        f.write('\n'.join('%.5f %.5f %.5f' % tuple(o) for o in out) + '\n')
    return path
