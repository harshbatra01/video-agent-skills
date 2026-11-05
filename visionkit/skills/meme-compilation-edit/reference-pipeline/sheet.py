"""Review sheets: each meme as it will appear (crop), with blur boxes: wipe blue, box green, curse red, blackout black."""
import json, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, ".")
from crop_util import ocr_path
edl = json.load(open("edl_full.json"))
ims = edl["images"]
only = sys.argv[1].split(",") if len(sys.argv) > 1 else None
if only:
    ims = [m for m in ims if m["file"] in only]
TW, TH = 360, 300
def _font(size):
    """Arial on a Mac or Windows, DejaVu on Linux, else PIL's own font."""
    for p in ("/System/Library/Fonts/Supplemental/Arial.ttf", "C:/Windows/Fonts/arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            pass
    return ImageFont.load_default()
font = _font(13)
col = {"wipe": (40, 90, 255), "box": (0, 170, 60), "curse": (230, 0, 0), "blackout": (0, 0, 0)}
cells = []
for m in ims:
    im = Image.open(ocr_path(m["file"])).convert("RGB")
    W, H = im.size
    c = m["crop"]
    x0, y0, x1, y1 = W * c["L"] / 100, H * c["T"] / 100, W * (1 - c["R"] / 100), H * (1 - c["B"] / 100)
    d = ImageDraw.Draw(im)
    for b in m["blurs"]:
        bx = b["box"]
        d.rectangle([bx[0] * W, bx[1] * H, bx[2] * W, bx[3] * H], outline=col[b["kind"]], width=max(3, W // 200))
    im = im.crop((int(x0), int(y0), int(x1), int(y1)))
    im.thumbnail((TW, TH - 34))
    cell = Image.new("RGB", (TW, TH), (235, 235, 235))
    cell.paste(im, ((TW - im.width) // 2, 34))
    dd = ImageDraw.Draw(cell)
    dd.text((4, 2), f"{m['start_f']/30:.1f}s {m['file']}", fill=(0, 0, 0), font=font)
    dd.text((4, 17), " ".join(f"{b['kind'][0]}{'@'+str(b['keys'][0][0]) if b['kind']=='box' else ('@'+str(b['path_keys'][0]) if b['kind']=='wipe' else '')}" for b in m["blurs"])[:60], fill=(90, 0, 0), font=font)
    cells.append(cell)
per = 16
for p in range(0, len(cells), per):
    chunk = cells[p:p + per]
    sheet = Image.new("RGB", (TW * 4, TH * ((len(chunk) + 3) // 4)), (255, 255, 255))
    for k, c in enumerate(chunk):
        sheet.paste(c, ((k % 4) * TW, (k // 4) * TH))
    sheet.save(f"review_{p // per + 1:02d}.png")
    print(f"review_{p // per + 1:02d}.png")
