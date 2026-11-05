"""Design mockups (PIL) of the intro name title and the TRYIMMUFIX code card on graded full-res frames."""
import os, sys, json, pickle
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vgrab import grab
from model import *
HERE = os.path.dirname(os.path.abspath(__file__))
M = pickle.load(open(os.path.join(HERE, 'calib', 'model_v1.pkl'), 'rb'))
ads = json.load(open(os.path.join(HERE, 'ads_all.json')))
UF = r'C:\Users\Kanishk\AppData\Local\Microsoft\Windows\Fonts'
FONT = {
    'pn_semi': UF + r'\Proxima Nova Semibold.ttf', 'pn_reg': UF + r'\Proxima Nova Regular.ttf', 'pn_light': UF + r'\Proxima Nova Light.ttf',
    'pn_xb': UF + r'\Proxima Nova Extrabold.ttf', 'power': UF + r'\PowerGrotesk-Regular (1).ttf', 'sf_med': UF + r'\SFPRODISPLAYMEDIUM.OTF',
    'sf_bold': UF + r'\SFPRODISPLAYBOLD.OTF', 'gara_i': r'C:\Windows\Fonts\GARAIT.TTF', 'sf_reg': UF + r'\SFPRODISPLAYREGULAR.OTF',
}
CACHE = os.path.join(HERE, 'mock_frames'); os.makedirs(CACHE, exist_ok=True)


def graded_frame(key, t):
    p = os.path.join(CACHE, '%s_%.2f.png' % (key, t))
    if os.path.exists(p): return Image.open(p)
    uid = [u for u in ads if u.startswith(key)][0]; a = ads[uid]
    c = [c for c in a['clips'] if c['start'] <= t < c['end']][0]
    src = c['in'] + (t - c['start'])
    d = os.path.join(CACHE, 'tmp'); fs = grab(c['path'], src, 0.3, 1000, outdir=d, prefix='a', fast=True) or grab(c['path'], src, 0.8, 1000, outdir=d, prefix='a', fast=True)
    im = Image.open(fs[0]).convert('RGB'); sy = im.height / 3408.0
    px, py = [float(v) for v in c['pos'].split(':')]; s = float(c['scale']) / 100
    cx = 3024 + (540 - px * 1080) / s; cy = 1704 + (960 - py * 1920) / s; w = 1080 / s; h = 1920 / s
    crop = im.crop((int(cx - w / 2), int((cy - h / 2) * sy), int(cx + w / 2), int((cy + h / 2) * sy))).resize((1080, 1920), Image.LANCZOS)
    for f in fs: os.remove(f)
    g = Image.fromarray((M(np.asarray(crop).astype(np.float64) / 255, 0.0) * 255).astype(np.uint8))
    g.save(p); return g


def zoom(im, s, ax=0.5, ay=0.33):
    W, H = im.size
    w, h = W / s, H / s; x0 = ax * W - ax * w; y0 = ay * H - ay * h
    return im.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((W, H), Image.LANCZOS)


def text_w(font, s, track):
    return sum(font.getlength(ch) for ch in s) + track * font.size * (len(s) - 1)


def draw_tracked(d, xy, s, font, fill, track):
    x, y = xy
    for ch in s:
        d.text((x, y), ch, font=font, fill=fill); x += font.getlength(ch) + track * font.size


def shadowed(base, draw_fn, blur=10, opacity=110, offset=(0, 3)):
    """draw_fn(draw, color) onto an RGBA layer; soft shadow underneath."""
    W, H = base.size
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); draw_fn(ImageDraw.Draw(sh), (0, 0, 0, opacity))
    sh = sh.filter(ImageFilter.GaussianBlur(blur)); sh = sh.transform(sh.size, Image.AFFINE, (1, 0, -offset[0], 0, 1, -offset[1]))
    fg = Image.new('RGBA', (W, H), (0, 0, 0, 0)); draw_fn(ImageDraw.Draw(fg), None)
    out = base.convert('RGBA'); out.alpha_composite(sh); out.alpha_composite(fg); return out.convert('RGB')


def title(im, name, sub, x, y, style='A'):
    fn = ImageFont.truetype(FONT['pn_semi'], 27)
    fs = ImageFont.truetype(FONT['gara_i'] if style == 'B' else FONT['pn_light'], 25 if style == 'B' else 22)
    def draw(d, col):
        white = col or (255, 255, 255, 255); soft = col or (255, 255, 255, 222); line = col or (255, 255, 255, 190)
        draw_tracked(d, (x, y), name, fn, white, 0.16)
        ly = y + 44
        d.rectangle([x + 1, ly, x + 1 + 46, ly + 2], fill=line)
        draw_tracked(d, (x, ly + 12), sub, fs, soft, 0.02 if style == 'B' else 0.05)
    return shadowed(im, draw, blur=9, opacity=120, offset=(0, 2))


def code(im, label='USE CODE', main='TRYIMMUFIX', style='A'):
    W, H = im.size
    fl = ImageFont.truetype(FONT['pn_semi'], 28)
    fm = ImageFont.truetype(FONT['power'] if style == 'A' else FONT['pn_xb'], 112 if style == 'A' else 100)
    tr_m = 0.02 if style == 'A' else 0.03
    wl = text_w(fl, label, 0.32); wm = text_w(fm, main, tr_m)
    ym = H * 0.5 - 60; yl = ym - 58
    def draw(d, col):
        draw_tracked(d, ((W - wl) / 2, yl), label, fl, col or (255, 255, 255, 225), 0.32)
        draw_tracked(d, ((W - wm) / 2, ym), main, fm, col or (255, 255, 255, 255), tr_m)
        # hairlines either side of the label
        c = col or (255, 255, 255, 170); lx0 = (W - wl) / 2 - 18; lx1 = (W + wl) / 2 + 14; cy = yl + 17
        d.rectangle([lx0 - 44, cy, lx0, cy + 1], fill=c); d.rectangle([lx1, cy, lx1 + 44, cy + 1], fill=c)
    return shadowed(im, draw, blur=16, opacity=140, offset=(0, 4))


if __name__ == '__main__':
    mode = sys.argv[1]
    plan = json.loads(sys.argv[2])
    tiles = []
    for key, spec in plan.items():
        im = graded_frame(key, spec['t'])
        if 'zoom' in spec: im = zoom(im, spec['zoom'])
        if mode == 'title':
            im = title(im, spec.get('name', 'PAULA RADCLIFFE'), spec['sub'], spec['x'], spec['y'], spec.get('style', 'A'))
        else:
            im = code(im, style=spec.get('style', 'A'))
        tiles.append(im.resize((540, 960), Image.LANCZOS))
    S = Image.new('RGB', (540 * len(tiles), 960))
    for i, t in enumerate(tiles): S.paste(t, (540 * i, 0))
    out = os.path.join(HERE, 'mock_%s.png' % sys.argv[3]); S.save(out); print(out)
