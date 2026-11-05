"""Procedural overlay pack (our own, free): light leaks, light-bar sweeps, film burns, flare streaks.

All render on BLACK for Screen / Add blending, 1080x1920 (or --w/--h), 30 fps, H.264 NVENC (falls back to libx264).
usage: python overlays.py OUT_DIR [--w 1080 --h 1920 --fps 30] [--only name1,name2] [--palette warm|cool|barca|spain|white]
Each preset is a function of (t in 0..1, frame size) -> float RGB image; rendered at quarter size where it is smooth,
then upscaled, so a 3 s leak renders in seconds. Re-run with another --palette to get matching colour variants.
"""
import sys, os, subprocess, math
import numpy as np
from PIL import Image

PAL = {"warm": [(1.0, 0.45, 0.12), (1.0, 0.75, 0.35), (0.9, 0.2, 0.25)],
       "cool": [(0.25, 0.55, 1.0), (0.6, 0.85, 1.0), (0.55, 0.3, 1.0)],
       "barca": [(0.0, 0.3, 0.75), (0.65, 0.0, 0.25), (1.0, 0.8, 0.2)],
       "spain": [(0.85, 0.05, 0.1), (1.0, 0.75, 0.0), (1.0, 0.4, 0.1)],
       "white": [(1.0, 1.0, 1.0), (0.95, 0.95, 1.0), (1.0, 0.97, 0.9)]}

def rng(seed): return np.random.default_rng(seed)

def gauss_field(w, h, cx, cy, sx, sy):
    x = np.linspace(0, 1, w)[None, :]; y = np.linspace(0, 1, h)[:, None]
    return np.exp(-(((x - cx) / sx) ** 2 + ((y - cy) / sy) ** 2))

def smooth_noise(w, h, t, seed, scale=4):
    """cheap value noise: a few octaves of interpolated random grids that drift over t"""
    r = rng(seed); out = np.zeros((h, w))
    for o in range(3):
        gw, gh = scale * (2 ** o) + 2, int(scale * (2 ** o) * h / w) + 2
        g = r.random((gh, gw * 2))                       # twice as wide: drift by cropping, no wrap seam
        im = Image.fromarray((g * 255).astype(np.uint8)).resize((w * 2, h), Image.BICUBIC)
        a = np.asarray(im, np.float32) / 255
        off = int(min(w - 1, t * (o + 1) * 0.7 * w * 0.15))
        out += a[:, off:off + w] / (2 ** o)
    return out / out.max()

def leak(t, w, h, pal, seed=1):
    """organic light leak: 3 drifting colour blobs that bloom in and out (use 2-4 s)"""
    r = rng(seed); img = np.zeros((h, w, 3))
    env = math.sin(math.pi * t) ** 1.5                     # fade in and out over the clip
    for k in range(3):
        cx = 0.1 + 0.8 * r.random() + 0.25 * math.sin(2 * math.pi * (t * 0.6 + k / 3)); cy = r.random() * 1.0
        sx, sy = 0.25 + 0.3 * r.random(), 0.18 + 0.25 * r.random()
        f = gauss_field(w, h, cx, cy + 0.1 * math.cos(2 * math.pi * t + k), sx, sy)
        img += f[..., None] * np.array(pal[k % len(pal)])[None, None, :] * (0.6 + 0.4 * math.sin(2 * math.pi * (t * 1.3 + k * 0.4)) ** 2)
    n = smooth_noise(w, h, t, seed + 7)
    img *= (0.7 + 0.6 * n[..., None]) * env
    return np.clip(img, 0, 1.5)

def lightbar(t, w, h, pal, seed=2):
    """bright soft band sweeping top to bottom with grain (use 0.2-0.3 s = 6-9 frames)"""
    y = np.linspace(0, 1, h)[:, None]; pos = -0.25 + 1.5 * t
    band = np.exp(-((y - pos) / 0.11) ** 2) + 0.35 * np.exp(-((y - pos) / 0.3) ** 2)
    grain = 0.85 + 0.3 * rng(seed + int(t * 100)).random((h, w))
    col = np.array(pal[1])
    return np.clip(band[..., None] * grain[..., None] * col[None, None, :] * 1.6, 0, 1.5) * np.ones((h, w, 3))

def burn(t, w, h, pal, seed=3):
    """film burn: a hot spot grows from one edge and flares out (use 0.5-0.8 s)"""
    n = smooth_noise(w, h, t * 2, seed, scale=3)
    edge = gauss_field(w, h, 1.05, 0.35 + 0.2 * t, 0.25 + 0.9 * t, 0.35 + 0.9 * t)
    heat = np.clip(edge * (0.6 + n) * (1.6 * math.sin(math.pi * min(1, t * 1.2)) + 0.2), 0, 2)
    c_hot, c_mid, c_low = np.array([1, 0.97, 0.85]), np.array(pal[0]), np.array(pal[2])
    img = c_low[None, None, :] * np.clip(heat, 0, 0.5)[..., None] * 2 + c_mid[None, None, :] * np.clip(heat - 0.4, 0, 0.6)[..., None] * 1.6 \
        + c_hot[None, None, :] * np.clip(heat - 0.9, 0, 1)[..., None] * 1.5
    return np.clip(img, 0, 1.5)

def streak(t, w, h, pal, seed=4):
    """anamorphic flare streak across the frame centre (use 0.3-0.5 s on a hit)"""
    y = np.linspace(0, 1, h)[:, None]; x = np.linspace(0, 1, w)[None, :]
    env = math.exp(-((t - 0.15) / 0.12) ** 2) if t < 0.15 else math.exp(-(t - 0.15) / 0.25)
    core = np.exp(-((y - 0.5) / 0.004) ** 2) * np.exp(-((x - 0.5) / 0.6) ** 2)
    halo = np.exp(-((y - 0.5) / 0.03) ** 2) * np.exp(-((x - 0.5) / 0.35) ** 2) * 0.4
    hot = gauss_field(w, h, 0.5, 0.5, 0.05, 0.03) * 1.2
    col = np.array(pal[0]) * 0.6 + np.array([0.6, 0.8, 1.0]) * 0.4
    img = (core + halo)[..., None] * col[None, None, :] * 1.8 + hot[..., None] * np.array([1, 1, 1])[None, None, :]
    return np.clip(img * env, 0, 1.5)

PRESETS = {  # name: (fn, seconds, render scale)
    "leak_a": (lambda t, w, h, p: leak(t, w, h, p, 1), 3.0, 4),
    "leak_b": (lambda t, w, h, p: leak(t, w, h, p, 11), 2.0, 4),
    "lightbar": (lightbar, 0.27, 2),
    "burn": (burn, 0.7, 4),
    "streak": (streak, 0.45, 2),
}

def render(name, out, W, H, fps, pal):
    fn, secs, sc = PRESETS[name]; n = max(2, int(round(secs * fps))); w, h = W // sc, H // sc
    path = os.path.join(out, f"{name}.mp4")
    enc = ["-c:v", "h264_nvenc", "-preset", "p6", "-cq", "14"]
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-"] + enc + ["-pix_fmt", "yuv420p", path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        img = fn(i / (n - 1), w, h, pal)
        im = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8))
        if sc > 1: im = im.resize((W, H), Image.BICUBIC)
        p.stdin.write(im.tobytes())
    p.stdin.close(); p.wait()
    if p.returncode != 0:  # NVENC missing: retry on the CPU
        cmd[cmd.index("h264_nvenc")] = "libx264"; cmd[cmd.index("-preset") + 1] = "slow"; cmd[cmd.index("-cq")] = "-crf"
        return render_cpu(name, out, W, H, fps, pal, cmd)
    return path

def render_cpu(name, out, W, H, fps, pal, cmd):
    fn, secs, sc = PRESETS[name]; n = max(2, int(round(secs * fps))); w, h = W // sc, H // sc
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        im = Image.fromarray((np.clip(fn(i / (n - 1), w, h, pal), 0, 1) * 255).astype(np.uint8))
        if sc > 1: im = im.resize((W, H), Image.BICUBIC)
        p.stdin.write(im.tobytes())
    p.stdin.close(); p.wait(); return cmd[-1]

if __name__ == "__main__":
    out = sys.argv[1]; a = sys.argv
    W = int(a[a.index("--w") + 1]) if "--w" in a else 1080; H = int(a[a.index("--h") + 1]) if "--h" in a else 1920
    fps = float(a[a.index("--fps") + 1]) if "--fps" in a else 30
    pal = a[a.index("--palette") + 1] if "--palette" in a else "warm"
    only = a[a.index("--only") + 1].split(",") if "--only" in a else list(PRESETS)
    out = os.path.join(out, pal); os.makedirs(out, exist_ok=True)
    for nme in only:
        print(render(nme, out, W, H, fps, PAL[pal]))
