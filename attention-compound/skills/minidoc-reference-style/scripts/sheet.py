# Labelled contact sheet. python3 sheet.py video <file> <every_s> <out.jpg>  |  python3 sheet.py stills <out.jpg> <img...>
import subprocess, sys, io
from PIL import Image, ImageDraw, ImageFont
F = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 18)
def tile(items, out, cols=6, w=320, h=180):
    rows = (len(items) + cols - 1) // cols; sheet = Image.new("RGB", (cols * w, rows * h), (20, 20, 20))
    for k, (im, lab) in enumerate(items):
        im.thumbnail((w, h)); x, y = (k % cols) * w, (k // cols) * h
        sheet.paste(im, (x + (w - im.width) // 2, y + (h - im.height) // 2))
        d = ImageDraw.Draw(sheet); d.rectangle((x, y, x + len(lab) * 10 + 6, y + 22), fill=(0, 0, 0)); d.text((x + 3, y + 2), lab, font=F, fill=(255, 220, 0))
    sheet.save(out, quality=85)
if sys.argv[1] == "video":
    f, every, out = sys.argv[2], float(sys.argv[3]), sys.argv[4]
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
    items, t = [], 1.0
    while t < dur:
        png = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", f, "-frames:v", "1", "-vf", "scale=320:-1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
        items.append((Image.open(io.BytesIO(png)).convert("RGB"), f"{int(t//60)}:{t%60:04.1f}")); t += every
    tile(items, out)
else:
    tile([(Image.open(p).convert("RGB"), p.split("/")[-1][:30]) for p in sys.argv[3:]], sys.argv[2], cols=4, w=400, h=300)
