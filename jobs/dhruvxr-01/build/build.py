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

ap = argparse.ArgumentParser(); ap.add_argument("out", nargs="?", default=os.path.join(os.path.dirname(__file__), "out", "picture_v2.mp4"))
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


# ---------- real footage (build/assets, uploaded 6 Nov 2026; see assets/sources.txt) ----------
# slot: (file, start s in the trimmed clip, frames needed). Start times from sources.txt notes ("best at ...").
CLIPS = {"notification_stack": ("notification_stack.mp4", 2.0, 2), "sticky_notes": ("sticky_notes.mp4", 1.0, 2),
         "tangled_cables": ("tangled_cables.mp4", 3.0, 2), "alarm_clock": ("alarm_clock.mp4", 2.0, 5),
         "whiteboard": ("whiteboard.mp4", 7.3, 8), "typing_fast": ("typing_fast.mp4", 2.0, 9),
         "office_lowangle": ("office_lowangle.mp4", 6.8, 12), "office_crowd": ("office_crowd.mp4", 3.0, 5),
         "crowd_threshold": ("crowd_threshold.mp4", 4.0, 5), "crowd_above": ("crowd_above.mp4", 3.0, 5),
         "slowshutter_crowd": ("slowshutter_crowd.mp4", 3.0, 8), "stairwell": ("stairwell.mp4", 6.0, 6), "fisheye": ("fisheye.mp4", 4.0, 6)}
_clip_cache = {}
def clip_frames(slot):
    if slot in _clip_cache: return _clip_cache[slot]
    f, t0, n = CLIPS[slot]; path = os.path.join(ASSETS, f)
    if not os.path.exists(path): _clip_cache[slot] = None; return None
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t0), "-i", path, "-vf", f"fps=30,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
                          "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).astype(np.float32); _clip_cache[slot] = fr; return fr

def grade(a, black=0.06, white=0.90, gamma=0.92, contrast=1.15):
    """High-contrast monochrome like WHP: luma only, black point crushed (WHP blacks sit at 0 to 4), soft S-curve."""
    y = (a @ np.array([0.2126, 0.7152, 0.0722], np.float32)) / 255
    y = np.clip((y - black) / (white - black), 0, 1) ** gamma
    y = np.clip(0.5 + (y - 0.5) * contrast, 0, 1); y = y * y * (3 - 2 * y) * 0.35 + y * 0.65
    return (y * 255)[..., None] * np.ones(3, np.float32)

def barrel(a, k=0.35):
    """Fisheye-style barrel warp plus a round dark edge, for the climber shot (the clip is not a fisheye)."""
    y, x = np.mgrid[0:H, 0:W].astype(np.float32); nx, ny = (x - W / 2) / (W / 2), (y - H / 2) / (W / 2); r2 = nx ** 2 + ny ** 2
    f = 1 + k * r2; sx = np.clip(W / 2 + nx / f * (W / 2), 0, W - 1).astype(int); sy = np.clip(H / 2 + ny / f * (W / 2), 0, H - 1).astype(int)
    out = a[sy, sx]; edge = np.clip(1.25 - np.sqrt(r2) * 1.05, 0, 1)[..., None]; return out * edge

def footage(slot, g, f0, label):
    fr = clip_frames(slot)
    if fr is None or len(fr) == 0: return placeholder(g, label, sub=f"f{f0}")
    gp = GRADE_SLOT.get(slot, {})
    return grade(fr[min(g - f0, len(fr) - 1)], **gp)
GRADE_SLOT = {"whiteboard": dict(black=0.30, white=0.82, gamma=1.1, contrast=1.35)}   # v2 note: whiteboard read flat grey

def brand_png(name, width_px):
    """Linear's own files, unaltered (brand_notes.txt): only scaled, and composited after the finish."""
    im = Image.open(os.path.join(ASSETS, name)).convert("RGBA"); h = int(im.height * width_px / im.width)
    return im.resize((int(width_px), max(1, h)), Image.LANCZOS)
_coll = [os.path.join(ASSETS, f"collage_{i:02d}.jpg") for i in range(1, 10)]
COLL_FULL = [np.asarray(Image.open(p).convert("RGB").resize((640, 427)), np.uint8) if os.path.exists(p) else np.full((427, 640, 3), 60, np.uint8) for p in _coll]
COLL = [c.astype(np.float32) for c in COLL_FULL]
POST = []   # (rgba image, centre x, centre y, opacity) laid on top after grain and vignette

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
        slots = [(4, 5, "notification_stack"), (6, 7, "sticky_notes"), (8, 9, "tangled_cables"), (10, 10, None), (11, 15, "alarm_clock"),
                 (16, 23, "whiteboard"), (24, 32, "typing_fast"), (33, 44, "office_lowangle"),
                 (76, 77, "office_crowd"), (78, 80, "BLOWOUT"), (81, 85, "THRESHOLD"), (86, 90, "crowd_above")]
        for f0, f1, name in slots:
            if f0 <= g <= f1: break
        if name is None: a = blank(255)
        elif name == "BLOWOUT":
            k = {78: 0.6, 79: 0.85, 80: 1.0}[g]; fr = clip_frames("office_crowd")
            base = grade(fr[min(g - 76, len(fr) - 1)]) if fr is not None else placeholder(g, "office_crowd")
            a = np.clip(base * (1 + 2.5 * k) + 255 * k * 0.6, 0, 255)
        elif name == "THRESHOLD":
            p = footage("crowd_threshold", g, 81, "crowd_threshold"); a = np.where(blur(p, 1.0).mean(2, keepdims=True) > 118, 245.0, 8.0) * np.ones(3, np.float32)
        else: a = footage(name, g, f0, name)
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
    elif g <= 242:                               # v1: 14 soft glowing points (WHP has about 10 to 15) drift, then gather to the centre
        rng = np.random.default_rng(3); n = 14; p0 = np.c_[rng.uniform(0.1, 0.9, n) * W, rng.uniform(0.15, 0.85, n) * H]
        tgt = np.c_[W / 2 + rng.normal(0, 10 * S, n), H / 2 + rng.normal(0, 6 * S, n)]
        t = (g - 197) / 45; drift = np.c_[np.sin(np.arange(n) * 1.7) * 40 * S * t, np.cos(np.arange(n)) * 25 * S * t]
        k = ease_in(clamp01((t - 0.3) / 0.7)); pos = (p0 + drift) * (1 - k) + tgt * k
        a = blank(); br = 170 + 80 * rng.random(n); rr = max(1, int(2 * S))
        for (x, y), b in zip(pos.astype(int), br):
            if rr <= x < W - rr and rr <= y < H - rr: a[y - rr:y + rr + 1, x - rr:x + rr + 1] = b
        a = a + 0.9 * blur(a, 6) + 0.6 * blur(a, 22)
        if g <= 205: a = put_text(a, "focus", font("Inter-Regular", 27), (313 * S, 180 * S), fill=(190, 190, 190), alpha=1 - (g - 196) / 9)
        if g <= 205: a = put_text(a, "/ˈfōkəs/", font("Inter-Regular", 27), (932 * S, 540 * S), fill=(182, 182, 182), alpha=1 - (g - 196) / 9)
    elif g <= 286:                               # white bloom, then the logo with glow BEHIND it, pulling back
        y, x = np.mgrid[0:H, 0:W]; d = np.hypot(x - W / 2, y - H / 2)
        if g <= 244: a = 255 * np.exp(-(d / (520 * S)) ** 2)[..., None] * np.ones(3) + 30
        else:
            t = (g - 245) / 41; r = (300 - 210 * ease_out(clamp01(t * 1.6))) * S
            a = (120 * np.exp(-(d / r) ** 2))[..., None] * np.ones(3)
        if g >= 245:
            sc = 1.0 - 0.35 * ease_out(t); POST.append((brand_png("logo.png", 120 * S * sc), W / 2, H / 2, 1.0))
    elif g <= 321:                               # the mark as photo tiles, bursting into a collage; camera push; "this"
        t = (g - 287) / 34; s = 1 + 0.9 * ease_in(t); rng = np.random.default_rng(21)
        world = blank()
        if g <= 300:
            m = ring_mask(W / 2, H / 2, 46 * S, 74 * S); gp = int(10 * S); k = 0
            for yy in range(gp // 2, H, gp):
                for xx in range(gp // 2, W, gp):
                    if m[yy, xx] > 0 and rng.random() > 0.2:
                        ph = COLL[k % len(COLL)]; k += 1; cx0, cy0 = int(rng.uniform(0, ph.shape[1] - gp)), int(rng.uniform(0, ph.shape[0] - gp))
                        world[yy - gp // 2 + 1: yy + gp // 2, xx - gp // 2 + 1: xx + gp // 2] = ph[cy0:cy0 + gp - 1, cx0:cx0 + gp - 1] * 0.9
        else:
            spots = [(0.22, 0.14, 230, 150), (0.42, 0.10, 210, 140), (0.62, 0.16, 190, 130), (0.20, 0.40, 250, 160), (0.45, 0.36, 230, 150),
                     (0.66, 0.42, 200, 130), (0.30, 0.62, 180, 120), (0.52, 0.62, 220, 140), (0.74, 0.66, 170, 110)]
            for i, (fx, fy, w0, h0) in enumerate(spots):
                k = ease_out(clamp01((g - 301 - i) / 5)); w1, h1 = int(w0 * S * k), int(h0 * S * k)
                if w1 > 4 and h1 > 4:
                    ph = to_arr(Image.fromarray(COLL_FULL[i]).resize((w1, h1), Image.BICUBIC)); x0, y0 = int(W * fx), int(H * fy)
                    world[y0:y0 + h1, x0:x0 + w1] = ph[: H - y0, : W - x0]
            world = put_text(world, "[ 09:41 ]", font("Inter-Regular", 11), (200 * S, 668 * S), fill=(110, 110, 110))
        if 287 <= g <= 300 or 316 <= g <= 321: world = put_text(world, "this", font("Inter-Regular", 20), (205 * S, 150 * S), fill=(200, 200, 200))
        im = to_img(world).resize((int(W * s), int(H * s)), Image.BICUBIC); ox, oy = (im.width - W) // 2, (im.height - H) // 2
        a = to_arr(im.crop((ox, oy, ox + W, oy + H)))
    elif g == 322: a = blank(255)
    elif g <= 342:
        if g <= 330: a = footage("slowshutter_crowd", g, 323, "slowshutter_crowd")
        elif g <= 336: a = footage("stairwell", g, 331, "stairwell")
        else: a = barrel(footage("fisheye", g, 337, "fisheye"))
        lines = True
    elif g <= 410:                               # v1: halftone of a turning textured sphere on a fixed screen grid, stepped every 3 f
        gs = 343 + ((g - 343) // 3) * 3; t = (gs - 343) / 67
        gp = max(2, int(round(6 * S))); R = 200 * S; cx, cy = W * 0.48, H * 0.46
        ys, xs = np.mgrid[gp // 2:H:gp, gp // 2:W:gp].astype(np.float32); nx, ny = (xs - cx) / R, (ys - cy) / R; r2 = nx ** 2 + ny ** 2
        inside = r2 < 1; nz = np.sqrt(np.clip(1 - r2, 0, 1))
        lon = np.arctan2(nx, nz) + 0.9 * t + 1.3; lat = np.arcsin(np.clip(-ny, -1, 1))
        tex = 0.5 + 0.22 * np.sin(3 * lon + 2 * np.sin(2 * lat)) + 0.18 * np.sin(7 * lon - 3 * lat) + 0.12 * np.sin(11 * lat + 5 * lon)
        shade = np.clip(0.25 + 0.75 * (0.55 * nz - 0.45 * nx + 0.2), 0, 1)
        v = np.where(inside, np.clip(np.clip(tex, 0, 1) * shade * 1.35, 0, 1) * (1 - ease_in(t) * 0.97), 0)
        a = blank(); dmax = gp - max(1, int(S))
        for (yy, xx, vv) in zip(ys[inside].astype(int), xs[inside].astype(int), v[inside]):
            d = int(round(dmax * min(1, vv * 1.4)))
            if d >= 1: a[yy - d // 2:yy - d // 2 + d, xx - d // 2:xx - d // 2 + d] = (200 * vv + 40, 150 * vv + 25, 150 * vv + 25)
    elif g <= 420: a = blank()
    else:                                        # wordmark: right-to-left wipe over 3 f, brightness stepped every 3 f to f431
        a = blank(); steps = {421: 0.05, 424: 0.27, 427: 0.55, 430: 0.78, 433: 0.92, 436: 1.0}   # WHP's measured stepped fade
        lv = 0.0
        for k, v in steps.items():
            if g >= k: lv = v
        POST.append((brand_png("wordmark.png", 160 * S), W / 2, H / 2, lv))
    if 21 <= g <= 95: a = labels(a, g)
    a = finish(a, g, lines=lines)
    if POST:
        base = to_img(a).convert("RGBA")
        for im, cx, cy, op in POST:
            if op < 1: im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v, o=op: int(v * o)))
            base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))
        a = to_arr(base); POST.clear()
    return a

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
