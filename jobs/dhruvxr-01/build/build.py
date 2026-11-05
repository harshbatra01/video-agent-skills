#!/usr/bin/env python3
"""dhruvxr-01: Linear spec brand film in the WHP style. One build script, edited forward.
Timing is WHP's measured frame grid (research/dhruvxr/STUDY.md, raw/shots_by_hand.json), 30 fps, 495 frames.
Code-made shots are real. Footage, app recording and Linear logo slots are labelled placeholders until the files exist
(the network policy blocks linear.app, YouTube and stock sites). Picture only: sound comes later.

usage: python3 build.py [out.mp4] [--scale 1.0|1.5] [--only f0-f1]
"""
import sys, os, subprocess, math, argparse
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ap = argparse.ArgumentParser(); ap.add_argument("out", nargs="?", default=os.path.join(os.path.dirname(__file__), "out", "animatic_v0.mp4"))
ap.add_argument("--scale", type=float, default=1.0); ap.add_argument("--only", default=None)
A = ap.parse_args()
S = A.scale; W, H = int(1280 * S), int(720 * S); FPS = 30; N = 495
FD = "/usr/share/fonts/opentype/inter/"
def font(name, px): return ImageFont.truetype(FD + name + ".otf", max(6, int(px * S)))
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
ASSETS = os.path.join(os.path.dirname(__file__), "assets")   # footage/<slot>.mp4|png, logo.png, wordmark.png, ui.mp4|png when they exist

# ---------- helpers ----------
def blank(v=0): return np.full((H, W, 3), v, np.float32)
def to_img(a): return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
def to_arr(im): return np.asarray(im.convert("RGB"), np.float32)
def blur(a, r): return to_arr(to_img(a).filter(ImageFilter.GaussianBlur(r * S))) if r > 0 else a
def ease_out(t): return 1 - (1 - t) ** 3
def ease_in(t): return t ** 3
def clamp01(t): return max(0.0, min(1.0, t))

_vig = None
def finish(a, g, lines=False, grain=4.0):
    """Shared finish: vertical-line texture on footage-like shots, grain, soft vignette (to 0.75 at the corners)."""
    global _vig
    if _vig is None:
        y, x = np.mgrid[0:H, 0:W]; r = np.hypot((x - W / 2) / (W / 2), (y - H / 2) / (H / 2)) / math.sqrt(2)
        _vig = (1 - 0.25 * np.clip(r, 0, 1) ** 2)[..., None].astype(np.float32)
    if lines:
        col = np.ones(W, np.float32); col[::3] = 0.93; a = a * col[None, :, None]
    if grain:
        a = a + np.random.default_rng(g).normal(0, grain, (H, W, 1)).astype(np.float32)
    return a * _vig

def text_rgba(txt, fnt, fill):
    l, t, r, b = fnt.getbbox(txt); im = Image.new("RGBA", (r - l + 8, b - t + 8), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((4 - l, 4 - t), txt, font=fnt, fill=fill); return im

def put_text(a, txt, fnt, xy, fill=(223, 223, 223), anchor="lt", glow=0.0, blur_r=0.0, alpha=1.0):
    """Draw text on an array. xy in output pixels; anchor lt (left-top of ink) or mm (centre of ink). Optional glow and blur."""
    t = text_rgba(txt, fnt, fill + (255,))
    if blur_r > 0: t = t.filter(ImageFilter.GaussianBlur(blur_r * S))
    x, y = xy
    if anchor == "mm": x, y = x - t.width / 2, y - t.height / 2
    base = to_img(a).convert("RGBA"); layer = Image.new("RGBA", base.size, (0, 0, 0, 0)); layer.paste(t, (int(x), int(y)), t)
    if alpha < 1: layer.putalpha(layer.getchannel("A").point(lambda v: int(v * alpha)))
    if glow > 0:
        gl = layer.filter(ImageFilter.GaussianBlur(5 * S)); ga = np.asarray(gl, np.float32)
        out = to_arr(Image.alpha_composite(base, layer)); return out + ga[..., :3] * (ga[..., 3:] / 255) * glow
    return to_arr(Image.alpha_composite(base, layer))

def placeholder(g, label, tone=22, sub=""):
    """A clearly marked footage slot: dark frame, soft light, the slot name. Swapped for real footage when assets exist."""
    a = blank(tone); y, x = np.mgrid[0:H, 0:W]
    a += 18 * np.exp(-(((x - W * 0.55) / (W * 0.5)) ** 2 + ((y - H * 0.45) / (H * 0.6)) ** 2))[..., None]
    a = put_text(a, "FOOTAGE: " + label, font("Inter-Medium", 22), (W / 2, H / 2), fill=(120, 120, 120), anchor="mm")
    if sub: a = put_text(a, sub, font("Inter-Regular", 15), (W / 2, H / 2 + 30 * S), fill=(85, 85, 85), anchor="mm")
    return a

def dots_from_mask(mask, grid, dot, color=(205, 205, 205), dropout=0.0, seed=7, jitter_on=None):
    """Square dots on a grid wherever mask (H x W, 0..1) is lit at the cell centre. Brightness follows the mask."""
    gp, dp = max(2, int(round(grid * S))), max(1, int(round(dot * S)))
    out = blank(); rng = np.random.default_rng(seed)
    ys = np.arange(gp // 2, H, gp); xs = np.arange(gp // 2, W, gp)
    keep = rng.random((len(ys), len(xs))) >= dropout
    c = np.array(color, np.float32)
    for i, yy in enumerate(ys):
        row = mask[yy, xs]
        for j in np.nonzero((row > 0.08) & keep[i])[0]:
            xx = xs[j]; out[yy - dp // 2: yy - dp // 2 + dp, xx - dp // 2: xx - dp // 2 + dp] = c * row[j]
    return out

def glow(a, k=1.0):
    """Layered Gaussian glow (radius 4, 16, 64 at 0.25, 0.30, 0.60k + 0.10), from 11_DOT_PROOF_CHECK.md."""
    return a + 0.25 * blur(a, 4) + 0.30 * blur(a, 16) + (0.60 * k + 0.10) * blur(a, 64)

def ring_mask(cx, cy, r0, r1):
    y, x = np.mgrid[0:H, 0:W]; d = np.hypot(x - cx, y - cy); return ((d >= r0) & (d <= r1)).astype(np.float32)

def crosshair_mask(cx, cy, r):
    im = Image.new("L", (W, H), 0); d = ImageDraw.Draw(im); w = int(r * 0.16)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=255, width=w)
    d.ellipse((cx - r * 0.45, cy - r * 0.45, cx + r * 0.45, cy + r * 0.45), outline=200, width=int(w * 0.8))
    d.ellipse((cx - r * 0.1, cy - r * 0.1, cx + r * 0.1, cy + r * 0.1), fill=255)
    for sx, sy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        d.line((cx + sx * r * 0.62, cy + sy * r * 0.62, cx + sx * r * 1.35, cy + sy * r * 1.35), fill=230, width=w)
    return np.asarray(im, np.float32) / 255

def perspective(img, quad):
    """Warp img (PIL) so its corners land on quad [(x,y) tl, tr, br, bl] in a W x H frame."""
    w, h = img.size; src = [(0, 0), (w, 0), (w, h), (0, h)]; M = []; B = []
    for (X, Y), (x, y) in zip(quad, src):
        M.append([X, Y, 1, 0, 0, 0, -x * X, -x * Y]); M.append([0, 0, 0, X, Y, 1, -y * X, -y * Y]); B += [x, y]
    c = np.linalg.solve(np.array(M, float), np.array(B, float))
    return img.transform((W, H), Image.PERSPECTIVE, tuple(c), Image.BICUBIC, fillcolor=(0, 0, 0))

LOG = ["a3f9c21  fix cycle sync on reopen", "7be04d2  ship triage view", "0c1e9f8  move issue to Done", "e45a7b0  cut backlog by half",
       "91d2c3e  keyboard nav for lists", "5f6a8b1  merge focus mode", "c0ffee4  remove noisy alerts", "2d9e7a3  roadmap: Q1 locked",
       "b8c1f20  speed up search", "6a7e3d9  one view, every team", "f00d1e5  close stale tickets", "3e5b7c8  ship it"]
def log_frame(g, offset=0):
    a = blank(4); F = ImageFont.truetype(MONO, int(13 * S))
    im = to_img(a); d = ImageDraw.Draw(im)
    for i in range(40):
        ln = LOG[(i + offset) % len(LOG)]; y = int((8 + i * 18) * S) - 4 * S
        d.text((int(40 * S), y), ln, font=F, fill=(150, 150, 150) if i % 5 else (220, 220, 220))
        d.text((int(380 * S), y), "ok", font=F, fill=(110, 110, 110))
    return to_arr(im)

def band_glitch(a, g, strength):
    rng = np.random.default_rng(1000 + g); out = a.copy(); y = 0
    while y < H:
        h = int(rng.integers(8, 41) * S)
        if rng.random() < 0.55 * strength: out[y:y + h] = np.roll(a[y:y + h], int(rng.integers(20, 121) * S * rng.choice([-1, 1])), axis=1)
        y += h
    for _ in range(int(2 * strength + 0.5)):
        yy = int(rng.integers(0, H - 3)); out[yy:yy + max(1, int(2 * S))] = 255
    return out

# ---------- shot builders (global frame g) ----------
def ui_card():
    """Placeholder for the Linear app recording, as a card that can be tilted."""
    p = os.path.join(ASSETS, "ui.png")
    if os.path.exists(p): return Image.open(p).convert("RGB")
    cw, ch = int(900 * S), int(540 * S); im = Image.new("RGB", (cw, ch), (16, 16, 18)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, cw - 1, ch - 1), outline=(60, 60, 64), width=max(1, int(2 * S)))
    d.rectangle((0, 0, int(190 * S), ch), fill=(22, 22, 25))
    for i in range(9):
        y = int((70 + i * 48) * S); d.rounded_rectangle((int(220 * S), y, cw - int(30 * S), y + int(34 * S)), radius=int(6 * S), fill=(28, 28, 32))
    F = font("Inter-Medium", 22); d.text((int(240 * S), int(20 * S)), "APP RECORDING: Linear issue list (to record)", font=F, fill=(130, 130, 130))
    return im

def tilt_quad(t):
    """Tilted card corners; slow drift over the shot (two-key move, settle ease)."""
    dx = -30 * S * ease_out(t); cx, cy = W * 0.52 + dx, H * 0.47
    return [(cx - 330 * S, cy - 190 * S), (cx + 400 * S, cy - 230 * S), (cx + 420 * S, cy + 215 * S), (cx - 345 * S, cy + 170 * S)]

LABELS = {}
def labels(a, g):
    """WHP-style corner labels (italic, glow) and the 2-frame big word, at WHP's measured frames."""
    fi = font("Inter-Italic", 20)
    if 21 <= g <= 74:
        br = {21: 6, 22: 3}.get(g, 0); a = put_text(a, "// noise //", fi, (150 * S, 112 * S), fill=(205, 205, 205), glow=0.6, blur_r=br)
    if 28 <= g <= 76:
        br = {28: 6, 29: 3}.get(g, 0); a = put_text(a, "@ noise //", fi, (1052 * S, 597 * S), fill=(231, 231, 231), glow=0.6, blur_r=br)
    if 76 <= g <= 77: a = put_text(a, "Backlog", font("Inter-Italic", 58), (W / 2, H / 2), fill=(245, 245, 245), anchor="mm", glow=0.9)
    if 81 <= g <= 95: a = put_text(a, "// backlog 999+", font("Inter-Italic", 17), (1032 * S, 113 * S), fill=(176, 176, 176), glow=0.5)
    if 84 <= g <= 95: a = put_text(a, "@/ priority //", font("Inter-Italic", 17), (102 * S, 572 * S), fill=(180, 180, 180), glow=0.5)
    return a

def frame(g):
    lines = False
    if g <= 3:                                   # dotted ring (our shape, an empty status circle)
        m = ring_mask(W / 2, H / 2, 46 * S, 62 * S); a = glow(dots_from_mask(m, 4, 3, dropout=0.35), 0.8)
        if g == 2: a = np.roll(a, int(14 * S), axis=1) * 0.8 + a * 0.4
    elif g <= 44 or 76 <= g <= 90:
        slots = [(4, 5, "notification stack"), (6, 7, "sticky-note wall"), (8, 9, "tangled cables"), (10, 10, None), (11, 15, "alarm clock macro"),
                 (16, 23, "crossed-out whiteboard"), (24, 32, "hands typing fast"), (33, 44, "crowded office, low angle"),
                 (76, 77, "crowded open-plan office"), (78, 80, "BLOWOUT"), (81, 85, "THRESHOLD"), (86, 90, "crowd from above")]
        for f0, f1, name in slots:
            if f0 <= g <= f1: break
        if name is None: a = blank(255)
        elif name == "BLOWOUT":
            k = {78: 0.6, 79: 0.85, 80: 1.0}[g]; a = placeholder(g, "crowded open-plan office") * (1 - k) + 255 * k
        elif name == "THRESHOLD":
            p = placeholder(g, "crowd, 1-bit threshold", tone=60); a = np.where(p.mean(2, keepdims=True) > 70, 245.0, 8.0) * np.ones(3, np.float32)
        else: a = placeholder(g, name, sub=f"f{f0} to f{f1}")
        lines = name not in (None, "BLOWOUT", "THRESHOLD")
    elif g == 45: a = blank(255)
    elif g <= 75:                                # cursor blinking on a blank page, B&W macro, slow push
        t = (g - 46) / 29; s = 1 + 0.04 * t
        pg = Image.new("RGB", (W, H), (214, 214, 214)); d = ImageDraw.Draw(pg)
        d.text((int(380 * S), int(250 * S)), "Untitled", font=font("Inter-Medium", 34), fill=(178, 178, 178))
        if (g - 46) % 16 < 9: d.rectangle((int(380 * S), int(312 * S), int(383 * S), int(352 * S)), fill=(30, 30, 30))
        pg = pg.resize((int(W * s), int(H * s)), Image.BICUBIC); ox, oy = (pg.width - W) // 2, (pg.height - H) // 2
        a = to_arr(pg.crop((ox, oy, ox + W, oy + H)))
        y = np.arange(H)[:, None, None]; a = a * (0.55 + 0.45 * np.exp(-((y - H * 0.45) / (H * 0.42)) ** 2))   # light falloff
        a = blur(a, 1.2); lines = True
    elif g <= 111:                               # app recording, tilted, 2-frame focus pull
        t = (g - 91) / 20; a = to_arr(perspective(ui_card(), tilt_quad(t)))
        if g <= 92: a = blur(a, {91: 8, 92: 3}[g])
        a = a * 0.95
    elif g <= 129:                               # scan-line tear, our own commit log, white smear and bars
        base = to_arr(perspective(ui_card(), tilt_quad(1.0)))
        if g <= 117: a = band_glitch(base, g, 1.0 - (g - 112) / 8)
        elif g == 118 or 123 <= g <= 127: a = band_glitch(log_frame(g, g), g, 0.5)
        elif g <= 122: a = np.where(blur(base, 6).mean(2, keepdims=True) > 20, 245.0, 10.0) * np.ones(3, np.float32); a = band_glitch(a, g, 1.0)
        else:
            a = blank(6); rng = np.random.default_rng(g)
            for _ in range(14):
                y0 = int(rng.integers(0, H)); a[y0:y0 + int(rng.integers(4, 22) * S), :int(rng.integers(W // 3, W))] = 235
    elif g <= 194:                               # white into a dot-matrix crosshair; "focus" + phonetics drifting apart
        m = crosshair_mask(W / 2, H * 0.47, 120 * S); dots = dots_from_mask(m, 6, 4, color=(150, 150, 150), dropout=0.3)
        rng = np.random.default_rng(5); field = dots_from_mask((np.random.default_rng(9).random((H, W)) > 0.995).astype(np.float32) * 0.5, 6, 3)
        a = glow(dots, 0.6) + field * 0.6
        if g <= 132: k = {130: 1.0, 131: 0.5, 132: 0.12}[g]; a = a * (1 - k) + 255 * k
        if g >= 132:
            t = (g - 132) / 62; al = 0.5 if g == 132 else 1.0
            a = put_text(a, "focus", font("Inter-Regular", 27), (338 * S - 25 * S * t, 180 * S), fill=(190, 190, 190), alpha=al)
        if g >= 138:
            t = (g - 138) / 56; al = 0.5 if g == 138 else 1.0
            a = put_text(a, "/ˈfōkəs/", font("Inter-Regular", 27), (912 * S + 20 * S * t, 540 * S), fill=(182, 182, 182), alpha=al)
    elif g <= 196: a = blank(255)
    elif g <= 242:                               # particles drift, then gather to the centre
        rng = np.random.default_rng(3); n = 420; p0 = np.c_[rng.uniform(0, W, n), rng.uniform(0, H, n)]
        tgt = np.c_[W / 2 + rng.normal(0, 14 * S, n), H / 2 + rng.normal(0, 10 * S, n)]
        t = (g - 197) / 45; drift = np.c_[np.sin(np.arange(n)) * 30 * S * t, -20 * S * t * np.ones(n)]
        k = ease_in(clamp01((t - 0.35) / 0.65)); pos = (p0 + drift) * (1 - k) + tgt * k
        a = blank(); br = 120 + 100 * rng.random(n)
        for (x, y), b in zip(pos.astype(int), br):
            if 1 <= x < W - 2 and 1 <= y < H - 2: a[y - 1:y + 2, x - 1:x + 2] = b
        a = glow(a, 0.4)
        if g <= 205: a = put_text(a, "focus", font("Inter-Regular", 27), (313 * S, 180 * S), fill=(190, 190, 190), alpha=1 - (g - 196) / 9)
        if g <= 205: a = put_text(a, "/ˈfōkəs/", font("Inter-Regular", 27), (932 * S, 540 * S), fill=(182, 182, 182), alpha=1 - (g - 196) / 9)
    elif g <= 286:                               # white bloom, then the logo with glow BEHIND it, pulling back
        y, x = np.mgrid[0:H, 0:W]; d = np.hypot(x - W / 2, y - H / 2)
        if g <= 244: a = 255 * np.exp(-(d / (520 * S)) ** 2)[..., None] * np.ones(3) + 30
        else:
            t = (g - 245) / 41; r = (300 - 210 * ease_out(clamp01(t * 1.6))) * S
            a = (120 * np.exp(-(d / r) ** 2))[..., None] * np.ones(3)
        if g >= 245:
            sc = 1.0 - 0.35 * ease_out(t); a = put_text(a, "[ Linear logo ]", font("Inter-Medium", 30 * sc), (W / 2, H / 2), fill=(235, 235, 235), anchor="mm")
    elif g <= 321:                               # the mark as photo tiles, bursting into a collage; camera push; "this"
        t = (g - 287) / 34; s = 1 + 0.9 * ease_in(t); rng = np.random.default_rng(21)
        world = blank()
        if g <= 300:
            for i in range(90):
                x0, y0 = W / 2 + rng.normal(0, 70 * S), H / 2 + rng.normal(0, 28 * S); sz = int(9 * S)
                v = rng.integers(60, 200); world[int(y0):int(y0) + sz, int(x0):int(x0) + sz] = v
        else:
            for i in range(9):
                x0, y0 = W * rng.uniform(0.2, 0.75), H * rng.uniform(0.15, 0.6); w0, h0 = int(rng.uniform(120, 260) * S), int(rng.uniform(80, 170) * S)
                k = ease_out(clamp01((g - 301 - i) / 6)); world[int(y0):int(y0) + int(h0 * k), int(x0):int(x0) + int(w0 * k)] = 30 + 8 * i
                if k > 0.9: world = put_text(world, "PHOTO", font("Inter-Medium", 12), (x0 + 8 * S, y0 + 6 * S), fill=(120, 120, 120))
            world = put_text(world, "[ 09:41 ]", font("Inter-Regular", 11), (200 * S, 668 * S), fill=(110, 110, 110))
        if 287 <= g <= 300 or 316 <= g <= 321: world = put_text(world, "this", font("Inter-Regular", 20), (205 * S, 150 * S), fill=(200, 200, 200))
        im = to_img(world).resize((int(W * s), int(H * s)), Image.BICUBIC); ox, oy = (im.width - W) // 2, (im.height - H) // 2
        a = to_arr(im.crop((ox, oy, ox + W, oy + H)))
    elif g == 322: a = blank(255)
    elif g <= 342:
        name = "slow-shutter crowd, terminal" if g <= 330 else "spiral stairwell, looking down" if g <= 336 else "fisheye, person climbing"
        a = placeholder(g, name); lines = True
    elif g <= 410:                               # dot globe turning and fading, stepped every 3 frames (10 fps)
        gs = 343 + ((g - 343) // 3) * 3; t = (gs - 343) / 67
        n = 2200; i = np.arange(n) + 0.5; phi = np.arccos(1 - 2 * i / n); th = math.pi * (1 + 5 ** 0.5) * i + t * 1.2
        X, Y, Z = np.cos(th) * np.sin(phi), np.cos(phi), np.sin(th) * np.sin(phi)
        R = 175 * S; cx, cy = W * 0.45, H * 0.42; vis = Z > 0
        a = blank(); lvl = (1 - ease_in(t)) * 140
        for x, y, z in zip(X[vis], Y[vis], Z[vis]):
            px, py = int(cx + R * x), int(cy - R * y); a[py:py + max(1, int(2 * S)), px:px + max(1, int(2 * S))] = lvl * (0.35 + 0.65 * z)
        a[..., 0] *= 1.08
    elif g <= 420: a = blank()
    else:                                        # wordmark: right-to-left wipe over 3 f, brightness stepped every 3 f to f431
        a = blank(); txt = "[ Linear wordmark ]"; F = font("Inter-SemiBold", 30)
        steps = {421: 0.05, 424: 0.27, 427: 0.55, 430: 0.78, 433: 0.92, 436: 1.0}
        lv = 0.0
        for k, v in steps.items():
            if g >= k: lv = v
        c = int(242 * lv); a = put_text(a, txt, F, (W / 2, H / 2), fill=(c, c, c), anchor="mm")
        if g <= 423:
            frac = {421: 0.35, 422: 0.65, 423: 1.0}[g]; a[:, : int(W / 2 - 150 * S + (1 - frac) * 300 * S)] = 0
    if 21 <= g <= 95: a = labels(a, g)
    return finish(a, g, lines=lines)

# ---------- render ----------
if __name__ == "__main__":
    os.makedirs(os.path.dirname(os.path.abspath(A.out)), exist_ok=True)
    rng_frames = range(N)
    if A.only: f0, f1 = map(int, A.only.split("-")); rng_frames = range(f0, f1 + 1)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", "-r", str(FPS), A.out], stdin=subprocess.PIPE)
    for g in rng_frames:
        p.stdin.write(np.clip(frame(g), 0, 255).astype(np.uint8).tobytes())
        if g % 50 == 0: print("frame", g, flush=True)
    p.stdin.close(); p.wait(); print("wrote", A.out)
