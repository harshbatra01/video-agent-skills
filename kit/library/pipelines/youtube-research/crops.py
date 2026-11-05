"""Native-resolution 9:16 crops from grabbed frames, laid side by side with timestamps.
spec: list of (folder, time_s, cx) ; cx = crop centre as a fraction of source width."""
import os, glob, re, sys
from PIL import Image, ImageDraw
FPS = 24000 / 1001


def frame_at(folder, t):
    fs = sorted(glob.glob(os.path.join(folder, 'g_*.png')))
    best = min(fs, key=lambda f: abs((int(re.search(r'g_(\d+)', os.path.basename(f)).group(1)) - 1) / FPS - t))
    return best, (int(re.search(r'g_(\d+)', os.path.basename(best)).group(1)) - 1) / FPS


def vcrop(im, cx, zoom=1.0, cy=0.5):
    W, H = im.size
    ch = H / zoom; cw = ch * 9 / 16
    x0 = min(max(cx * W - cw / 2, 0), W - cw)
    y0 = min(max(cy * H - ch / 2, 0), H - ch)
    return im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch)))


def panel(spec, out, h=720):
    tiles = []
    for folder, t, cx, *rest in spec:
        zoom = rest[0] if rest else 1.0
        f, tt = frame_at(folder, t)
        im = Image.open(f).convert('RGB')
        c = vcrop(im, cx, zoom) if im.width > im.height else im
        c = c.resize((round(h * 9 / 16), h), Image.LANCZOS)
        tiles.append((tt, cx, zoom, c))
    W = sum(c.width for *_, c in tiles) + 6 * (len(tiles) - 1)
    S = Image.new('RGB', (W, h + 18), (10, 10, 10)); d = ImageDraw.Draw(S); x = 0
    for tt, cx, zoom, c in tiles:
        S.paste(c, (x, 18)); d.text((x + 3, 3), '%.2fs cx%.2f z%.2f' % (tt, cx, zoom), fill=(255, 255, 0)); x += c.width + 6
    S.save(out)
    return out
