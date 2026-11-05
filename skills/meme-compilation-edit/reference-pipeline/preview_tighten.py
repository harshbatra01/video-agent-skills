"""Which memes the tighten rule changes, shown as they sit on screen (1920x1080 on the gray background): now | tightened."""
import json, sys
sys.path.insert(0, ".")
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import crop_util as cu
E = json.load(open("edl_full.json")); dec = json.load(open("decisions.json")); over = dec.get("memes", {})
TARGET_H, MAX_W, S = 980, 1740, 0.25
def _font(size):
    """Arial on a Mac or Windows, DejaVu on Linux, else PIL's own font."""
    for p in ("/System/Library/Fonts/Supplemental/Arial.ttf", "C:/Windows/Fonts/arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            pass
    return ImageFont.load_default()
font = _font(13)
def frame(name, crop):
    im = Image.open(cu.ocr_path(name)).convert("RGB"); W, H = im.size
    box = (int(W * crop["L"] / 100), int(H * crop["T"] / 100), W - int(W * crop["R"] / 100), H - int(H * crop["B"] / 100))
    v = im.crop(box); sc = TARGET_H / v.height
    if v.width * sc > MAX_W: sc = MAX_W / v.width
    v = v.resize((max(1, int(v.width * sc * S)), max(1, int(v.height * sc * S))), Image.LANCZOS)
    f = Image.new("RGB", (int(1920 * S), int(1080 * S)), (100, 100, 100))
    f.paste(v, ((f.width - v.width) // 2, (f.height - v.height) // 2)); return f, round(sc * 100, 1)
rows, rep = [], []
for im in E["images"]:
    n = im["file"]
    if n.endswith(".mp4") or over.get(n, {}).get("crop") or over.get(n, {}).get("keep_crop"): continue
    r0 = len(rep); new = cu.tighten_margins(n, im["crop"], rep)
    if new != im["crop"]: rows.append((n, im["crop"], new, rep[r0:]))
print(len(rows), "memes change"); print("\n".join(rep))
cw, ch = int(1920 * S), int(1080 * S)
for p in range(0, len(rows), 8):
    sheet = Image.new("RGB", (2 * cw + 30, len(rows[p:p + 8]) * (ch + 22)), "white"); d = ImageDraw.Draw(sheet)
    for i, (n, a, b, why) in enumerate(rows[p:p + 8]):
        y = i * (ch + 22)
        fa, sa = frame(n, a); fb, sb = frame(n, b)
        sheet.paste(fa, (0, y + 20)); sheet.paste(fb, (cw + 30, y + 20))
        d.text((4, y + 3), f"{p + i + 1}. {n[:40]}  now {sa}%", fill="black", font=font)
        d.text((cw + 34, y + 3), "tight " + " ".join(f"{s}{b[s]:g}" for s in "LTRB") + f"  {sb}%", fill="black", font=font)
    sheet.save(f"tighten_sheet_{p // 8 + 1}.png")
