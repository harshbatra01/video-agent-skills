# Proof of STUDY.md effect #2: a form made of square dots with a soft bloom. Small size only.
# 640x360, 12 frames at 30 fps (0.4 s). Bloom shrinks over the frames like WHP f245 to f286.
import os, subprocess, time
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
t0 = time.time()
W, H, N = 640, 360, 12
OUT = os.path.dirname(os.path.abspath(__file__))
FONT = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
# Mask: our placeholder mark "[STUDIO]" (no third-party logo), drawn large then sampled.
mask = Image.new("L", (W, H), 0)
d = ImageDraw.Draw(mask)
f = ImageFont.truetype(FONT, 120)
bb = d.textbbox((0, 0), "[STUDIO]", font=f)
d.text(((W - (bb[2] - bb[0])) / 2 - bb[0], (H - (bb[3] - bb[1])) / 2 - bb[1]), "[STUDIO]", font=f, fill=255)
m = np.asarray(mask, dtype=np.float32) / 255.0
PITCH, DOT = 6, 4  # 6 px grid, 4 px square dots
frames = []
for i in range(N):
    dots = Image.new("L", (W, H), 0)
    dd = ImageDraw.Draw(dots)
    for y in range(PITCH // 2, H, PITCH):
        for x in range(PITCH // 2, W, PITCH):
            if m[y, x] > 0.5:
                v = int(0xDF * (0.85 + 0.15 * np.sin(0.9 * x + 1.3 * y + i)))  # grey-white ink, slight shimmer
                dd.rectangle([x - DOT // 2, y - DOT // 2, x + DOT // 2 - 1, y + DOT // 2 - 1], fill=v)
    a = np.asarray(dots, dtype=np.float32)
    k = 1.0 - i / (N - 1)  # glow shrinks over time
    glow = np.zeros_like(a)
    for r, g in ((4, 0.6), (12, 0.45), (32, 0.35 * k + 0.05)):  # Gaussian glow stack
        glow += g * np.asarray(dots.filter(ImageFilter.GaussianBlur(r)), dtype=np.float32)
    out = np.clip(a + glow, 0, 255).astype(np.uint8)
    frames.append(out)
    Image.fromarray(out).save(os.path.join(OUT, f"dot_{i:02d}.png"))
# Encode a tiny proof clip with ffmpeg (yuv420p, CRF 18).
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-i", os.path.join(OUT, "dot_%02d.png"),
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", os.path.join(OUT, "dot_matrix_proof.mp4")], check=True)
f0 = frames[0].astype(np.float32) / 255.0
print(f"frames={N} size={W}x{H} mean_brightness_f0={f0.mean():.3f} near_black_f0={(f0 < 0.1).mean()*100:.1f}% runtime={time.time()-t0:.2f}s")
