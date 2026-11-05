"""Natural grade for the Immufix Sony log B-roll (S-Log3 / S-Gamut3.Cine, decoded as BT.709 limited range):
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
