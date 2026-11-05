"""Premium star rating, no background: rounded gold stars with glow + thin outline stars, floating over her dress.
Storyboard: outlines draw on -> one star fills gold -> (twist) all five fill."""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mock_titles import graded_frame
from mock_title_options import comp, caption, font, W, H

SS = 4


def star_mask(cx, cy, R, round_px=7, inner=0.47):
    """rounded 5-point star as an L mask at frame size (supersampled, corners softened)"""
    m = Image.new('L', (W * SS, H * SS), 0)
    pts = []
    for i in range(10):
        a = math.radians(-90 + i * 36); r = R if i % 2 == 0 else R * inner
        pts.append(((cx + r * math.cos(a)) * SS, (cy + r * math.sin(a)) * SS))
    ImageDraw.Draw(m).polygon(pts, fill=255)
    m = m.filter(ImageFilter.GaussianBlur(round_px * SS / 2)).point(lambda v: 255 if v > 128 else 0)   # round the corners
    return m.resize((W, H), Image.LANCZOS)


def gold_fill(mask, cy, R):
    """vertical gold gradient with a top highlight, cut by mask -> RGBA"""
    y = np.arange(H)[:, None]
    t = np.clip((y - (cy - R)) / (2 * R), 0, 1)
    top, mid, bot = np.array([255, 236, 178]), np.array([222, 182, 98]), np.array([166, 118, 44])
    col = np.where(t[..., None] < 0.45, top + (mid - top) * (t[..., None] / 0.45), mid + (bot - mid) * ((t[..., None] - 0.45) / 0.55))
    col = np.broadcast_to(col, (H, W, 3))
    a = np.asarray(mask)[..., None]
    return Image.fromarray(np.concatenate([col, a], -1).astype(np.uint8), 'RGBA')


def outline(mask, width=3, alpha=170):
    m = np.asarray(mask).astype(np.float32) / 255
    inner = np.asarray(mask.filter(ImageFilter.MinFilter(width * 2 + 1))).astype(np.float32) / 255
    edge = np.clip(m - inner, 0, 1)
    arr = np.zeros((H, W, 4), np.uint8); arr[..., :3] = 255; arr[..., 3] = (edge * alpha).astype(np.uint8)
    return Image.fromarray(arr, 'RGBA')


def stars(img, lit, cy=1150, R=52, gap=128, outlines=True, shine=False):
    out = img
    xs = [W / 2 + (i - 2) * gap for i in range(5)]
    masks = [star_mask(x, cy, R) for x in xs]
    # soft drop shadow under everything (reads on light and dark backgrounds)
    sh = Image.new('L', (W, H), 0)
    for i, m in enumerate(masks):
        if i < lit or outlines: sh = Image.fromarray(np.maximum(np.asarray(sh), np.asarray(m)))
    sh = sh.filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.45))
    S = Image.new('RGBA', (W, H), (0, 0, 0, 0)); S.putalpha(sh); out = comp(out, S)
    for i, m in enumerate(masks):
        if i < lit:
            glow = gold_fill(m.filter(ImageFilter.MaxFilter(9)), cy, R)
            g = glow.split()[3].filter(ImageFilter.GaussianBlur(26)).point(lambda v: int(v * 0.85))
            G = Image.new('RGBA', (W, H), (240, 196, 110, 0)); G.putalpha(g); out = comp(out, G)
            out = comp(out, gold_fill(m, cy, R))
            if shine:   # diagonal light sweep across the lit star
                sw = Image.new('L', (W, H), 0)
                ImageDraw.Draw(sw).polygon([(xs[i] - 70, cy + R), (xs[i] - 40, cy + R), (xs[i] + 30, cy - R), (xs[i] + 0, cy - R)], fill=200)
                sw = Image.fromarray((np.asarray(sw).astype(np.float32) * np.asarray(m).astype(np.float32) / 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))
                L = Image.new('RGBA', (W, H), (255, 255, 255, 0)); L.putalpha(sw); out = comp(out, L)
        elif outlines:
            out = comp(out, outline(m))
    return out


def label(im, s):
    d = ImageDraw.Draw(im); d.rectangle([0, 0, im.width, 34], fill=(0, 0, 0)); d.text((8, 6), s, fill=(255, 255, 0), font=font('pn_semi', 20))
    return im


if __name__ == '__main__':
    a = graded_frame('cd03e189', 1.6); b = graded_frame('cd03e189', 10.0)
    frames = [label(caption(stars(a, 0), 'some one').resize((432, 768), Image.LANCZOS), '1  outlines draw on'),
              label(caption(stars(a, 1, shine=True), 'star reviews').resize((432, 768), Image.LANCZOS), '2  one star fills gold + shine'),
              label(caption(stars(b, 5), 'review I\'ll').resize((432, 768), Image.LANCZOS), '3  twist: all five fill')]
    S = Image.new('RGB', (432 * 3, 768))
    for i, f in enumerate(frames): S.paste(f, (432 * i, 0))
    S.save(os.path.join(HERE, 'stars_premium.png'))
    big = caption(stars(a, 1, shine=True), 'star reviews').crop((140, 860, 940, 1320)).resize((800, 460), Image.LANCZOS)
    big.save(os.path.join(HERE, 'stars_premium_zoom.png'))
    print('ok')
