# Every frame between two times as a labelled sheet. python3 frame_strip.py <video> <t0> <t1> <out.jpg> [cols] [w]
import glob, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont
v, t0, t1, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
cols = int(sys.argv[5]) if len(sys.argv) > 5 else 6; w = int(sys.argv[6]) if len(sys.argv) > 6 else 360
fps = eval(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", v], capture_output=True, text=True).stdout)
with tempfile.TemporaryDirectory() as td:
    subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t0), "-i", v, "-t", str(t1 - t0), "-vf", f"scale={w}:-2", f"{td}/%04d.png"], check=True)
    ims = [Image.open(f).convert("RGB") for f in sorted(glob.glob(f"{td}/*.png"))]
h = ims[0].height; F = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 16)
S = Image.new("RGB", (cols * w, ((len(ims) + cols - 1) // cols) * h)); d = ImageDraw.Draw(S)
for n, im in enumerate(ims):
    x, y = (n % cols) * w, (n // cols) * h; S.paste(im, (x, y)); d.rectangle((x, y, x + 64, y + 20), fill=(0, 0, 0)); d.text((x + 3, y + 2), f"{t0 + n / fps:.2f}", font=F, fill=(255, 230, 0))
S.save(out, quality=85); print(len(ims), "frames")
