"""Cover-frame sheet for TikTok videos (tikwm single-video API; stills only, no video download).
python -X utf8 ttcovers.py out.jpg <url>:<label> ...
"""
import sys, io, json, time, urllib.request
from PIL import Image, ImageDraw, ImageFont
import vt

out = sys.argv[1]
items = []
for a in sys.argv[2:]:
    u, _, lab = a.rpartition(":") if a.count(":") > 1 else (a, "", "")
    items.append((u, lab))
TW, TH, LAB = 200, 356, 30
cols = min(4, len(items))
rows = (len(items) + cols - 1) // cols
sheet = Image.new("RGB", (cols * (TW + 4), rows * (TH + LAB)), (20, 20, 20))
d = ImageDraw.Draw(sheet)
try:
    font = ImageFont.truetype("arial.ttf", 12)
except Exception:
    font = ImageFont.load_default()
for i, (u, lab) in enumerate(items):
    x, y = (i % cols) * (TW + 4), (i // cols) * (TH + LAB)
    d.text((x + 3, y + 2), lab[:34], fill=(255, 255, 255), font=font)
    d.text((x + 3, y + 15), u.rsplit("/", 1)[-1][:34], fill=(170, 170, 170), font=font)
    try:
        j = json.loads(vt.http("https://www.tikwm.com/api/", data={"url": u, "hd": "0"}))
        c = j["data"].get("origin_cover") or j["data"].get("cover")
        if c.startswith("/"):
            c = "https://www.tikwm.com" + c
        img = Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(c, headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read())).convert("RGB")
        img = img.resize((TW, TH))
        sheet.paste(img, (x, y + LAB))
    except Exception as e:
        d.text((x + 3, y + 40), "ERR " + str(e)[:30], fill=(255, 80, 80), font=font)
    time.sleep(1.2)
sheet.save(out, quality=85)
print("saved", out, sheet.size)
