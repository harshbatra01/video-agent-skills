"""Filmstrip sheet from YouTube's own preview stills (frame0 + hq1/hq2/hq3, stills only).
python -X utf8 strip.py out.jpg id:label ...
"""
import sys, io, urllib.request
from PIL import Image, ImageDraw, ImageFont

out = sys.argv[1]
items = [a.split(":", 1) for a in sys.argv[2:]]
TW, TH = 150, 266
LAB = 18
sheet = Image.new("RGB", (4 * TW + 6, len(items) * (TH + LAB)), (20, 20, 20))
d = ImageDraw.Draw(sheet)
try:
    font = ImageFont.truetype("arial.ttf", 13)
except Exception:
    font = ImageFont.load_default()


def get(vid, name):
    try:
        req = urllib.request.Request("https://i.ytimg.com/vi/%s/%s" % (vid, name), headers={"User-Agent": "Mozilla/5.0"})
        return Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=20).read())).convert("RGB")
    except Exception:
        return None


for r, (vid, label) in enumerate(items):
    y = r * (TH + LAB)
    d.text((4, y + 2), "%s  (%s)" % (label[:50], vid), fill=(255, 255, 255), font=font)
    for c, name in enumerate(["frame0.jpg", "hq1.jpg", "hq2.jpg", "hq3.jpg"]):
        img = get(vid, name)
        if img is None:
            continue
        w, h = img.size
        if name != "frame0.jpg":
            # 4:3 frame with a letterboxed vertical video: crop the centre 9:16 column
            cw = int(h * 9 / 16)
            x0 = (w - cw) // 2
            img = img.crop((x0, 0, x0 + cw, h))
        img = img.resize((TW, TH))
        sheet.paste(img, (c * (TW + 2), y + LAB))
sheet.save(out, quality=85)
print("saved", out, sheet.size)
