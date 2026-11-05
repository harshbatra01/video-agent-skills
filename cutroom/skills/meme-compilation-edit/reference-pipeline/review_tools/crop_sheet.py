import json, os
from PIL import Image, ImageDraw, ImageFont
rows = json.load(open("rects.json"))
edl = json.load(open("../data/edl_full.json"))
path = {os.path.basename(im["path"]): im["path"] for im in edl["images"]}
def _font(size):
    """Arial on a Mac or Windows, DejaVu on Linux, else PIL's own font."""
    for p in ("/System/Library/Fonts/Supplemental/Arial.ttf", "C:/Windows/Fonts/arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            pass
    return ImageFont.load_default()
font = _font(15)
tiles = []
for n, ra, rb, ca, cb in rows:
    ca = ca or {"Left": 0, "Top": 0, "Right": 0, "Bottom": 0}; cb = cb or {"Left": 0, "Top": 0, "Right": 0, "Bottom": 0}
    if all(abs(ca[k] - cb[k]) < 0.3 for k in ca): continue
    p = path.get(n)
    if not p or p.endswith(".mp4"): continue
    im = Image.open(p).convert("RGB"); w, h = im.size
    k = min(460 / w, 460 / h); im = im.resize((int(w * k), int(h * k)))
    W, H = im.size
    t = Image.new("RGB", (480, 520), "white"); t.paste(im, (10, 40))
    d = ImageDraw.Draw(t)
    for c, col, wd in ((ca, (230, 0, 0), 5), (cb, (0, 170, 0), 2)):
        x0 = 10 + W * c["Left"] / 100; x1 = 10 + W * (1 - c["Right"] / 100)
        y0 = 40 + H * c["Top"] / 100; y1 = 40 + H * (1 - c["Bottom"] / 100)
        d.rectangle([x0, y0, x1, y1], outline=col, width=wd)
    d.text((10, 2), n[:52], fill="black", font=font)
    d.text((10, 20), "mine L%.1f T%.1f R%.1f B%.1f  his L%.1f T%.1f R%.1f B%.1f" % (ca["Left"], ca["Top"], ca["Right"], ca["Bottom"], cb["Left"], cb["Top"], cb["Right"], cb["Bottom"]), fill="black", font=font)
    tiles.append(t)
print(len(tiles), "tiles")
for s in range(0, len(tiles), 8):
    sheet = Image.new("RGB", (480 * 4, 520 * 2), "gray")
    for j, t in enumerate(tiles[s:s + 8]):
        sheet.paste(t, ((j % 4) * 480, (j // 4) * 520))
    sheet.save(f"crops_{s // 8 + 1}.png")
