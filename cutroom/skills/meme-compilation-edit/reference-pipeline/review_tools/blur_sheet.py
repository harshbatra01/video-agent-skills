import json, os, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, ".")
from meme_diff import *   # data and helpers (an import, not exec)
def _font(size):
    """Arial on a Mac or Windows, DejaVu on Linux, else PIL's own font."""
    for p in ("/System/Library/Fonts/Supplemental/Arial.ttf", "C:/Windows/Fonts/arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            pass
    return ImageFont.load_default()
font = _font(14)
want = sys.argv[1].split(",")
tiles = []
for name in fd:
    if not any(name.startswith(w) for w in want): continue
    p = spec.get(name, {}).get("path")
    if not p or p.endswith(".mp4"): continue
    im = Image.open(p).convert("RGB"); w, h = im.size
    k = min(700 / w, 640 / h); im = im.resize((int(w * k), int(h * k))); W, H = im.size
    t = Image.new("RGB", (720, 700), "white"); t.paste(im, (10, 50)); d = ImageDraw.Draw(t)
    for T, clip, col, off in ((D, fd[name], (230, 0, 0), 0), (U, fu[name], (0, 160, 0), 3)):
        for n, e in enumerate(blurs(T, clip)):
            for m in e["masks"]:
                b = m.get("box") or m["path"][0][1]
                x0, y0, x1, y1 = 10 + b[0] * W + off, 50 + b[1] * H + off, 10 + b[2] * W - off, 50 + b[3] * H - off
                d.rectangle([x0, y0, x1, max(y0 + 2, y1)], outline=col, width=3 if col[0] else 2)
                lab = ("W" if "path" in m else "B") + str(n)
                d.text((x0 + 2, y0 + 1), lab, fill=col, font=font)
    d.text((10, 2), name[:80], fill="black", font=font)
    d.text((10, 20), "red = mine, green = his (W wipe, B box)", fill="black", font=font)
    tiles.append(t)
for s in range(0, len(tiles), 4):
    sheet = Image.new("RGB", (720 * 2, 700 * 2), "gray")
    for j, t in enumerate(tiles[s:s + 4]):
        sheet.paste(t, ((j % 2) * 720, (j // 2) * 700))
    sheet.save(f"blurs_{sys.argv[2]}_{s // 4 + 1}.png")
print(len(tiles))
