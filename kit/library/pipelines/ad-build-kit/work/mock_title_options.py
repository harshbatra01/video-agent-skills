"""Centred title options for the boss's "make it stand out / middle chest" note, mocked on real graded frames with the
real caption position (PowerGrotesk, centred at y~960) so we can judge clashes. Linear-light compositing like Premiere."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
UF = r'C:\Users\Kanishk\AppData\Local\Microsoft\Windows\Fonts'
F = {'pn_semi': UF + r'\Proxima Nova Semibold.ttf', 'pn_reg': UF + r'\Proxima Nova Regular.ttf', 'pn_xb': UF + r'\Proxima Nova Extrabold.ttf',
     'power': UF + r'\PowerGrotesk-Regular (1).ttf', 'cool_hc': UF + r'\Coolvetica Hv Comp.otf', 'galano': UF + r'\Galano GrotesqueBlack.otf',
     'bodoni': r'C:\Windows\Fonts\BOD_R.TTF', 'bodoni_i': r'C:\Windows\Fonts\BOD_I.TTF', 'sf_bold': UF + r'\SFPRODISPLAYBOLD.OTF'}
W, H = 1080, 1920
GOLD = (207, 174, 99)


def font(k, s): return ImageFont.truetype(F[k], s)


def tw(f, s, trk=0): return sum(f.getlength(c) for c in s) + trk / 1000 * f.size * (len(s) - 1)


def cap(f): b = f.getbbox('H'); return b[3] - b[1]


def text(d, x, y_base, s, f, fill, trk=0):
    asc = f.getmetrics()[0]
    for ch in s:
        d.text((x, y_base - asc), ch, font=f, fill=fill); x += f.getlength(ch) + trk / 1000 * f.size


def ctext(d, cx, y_base, s, f, fill, trk=0): text(d, cx - tw(f, s, trk) / 2, y_base, s, f, fill, trk)


def lin(a): return np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
def srgb(a): return np.where(a <= 0.0031308, a * 12.92, 1.055 * np.power(np.clip(a, 0, None), 1 / 2.4) - 0.055)


def comp(base, layer):
    """alpha-composite RGBA layer over RGB base in linear light"""
    b = lin(np.asarray(base.convert('RGB')).astype(np.float64) / 255)
    l = np.asarray(layer).astype(np.float64) / 255
    a = l[..., 3:4]; c = lin(l[..., :3])
    return Image.fromarray((srgb(b * (1 - a) + c * a) * 255).clip(0, 255).astype(np.uint8))


def rr(layer, box, r, fill):
    ss = 4; m = Image.new('L', (W * ss, H * ss), 0)
    ImageDraw.Draw(m).rounded_rectangle([v * ss for v in box], radius=r * ss, fill=255)
    m = m.resize((W, H), Image.LANCZOS)
    col = Image.new('RGBA', (W, H), fill[:3] + (0,)); col.putalpha(m.point(lambda v: int(v * fill[3] / 255)))
    layer.alpha_composite(col)


def shadow(layer, blur, op):
    a = layer.split()[3].filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * op))
    s = Image.new('RGBA', layer.size, (0, 0, 0, 0)); s.putalpha(a); out = Image.new('RGBA', layer.size, (0, 0, 0, 0))
    out.alpha_composite(s); out.alpha_composite(layer); return out


def caption(img, words):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    ctext(d, W / 2, 985, words, font('power', 70), (255, 255, 255, 255))
    return comp(img, shadow(L, 7, 0.55))


def frosted(img, box, r, tint=(255, 255, 255), tint_a=0.10, blur=26):
    """blurred-glass panel (needs an adjustment layer + blur + track matte in Premiere)"""
    bl = img.filter(ImageFilter.GaussianBlur(blur))
    ss = 4; m = Image.new('L', (W * ss, H * ss), 0)
    ImageDraw.Draw(m).rounded_rectangle([v * ss for v in box], radius=r * ss, fill=255); m = m.resize((W, H), Image.LANCZOS)
    out = Image.composite(bl, img, m)
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); rr(L, box, r, tint + (int(255 * tint_a),))
    ImageDraw.Draw(L).rounded_rectangle(box, radius=r, outline=(255, 255, 255, 70), width=2)
    return comp(out, L)


# ---------------- options
def opt_A(img, cred):   # centred plate, bigger, above the caption
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    fn, fs = font('pn_semi', 46), font('pn_reg', 33)
    wn, ws = tw(fn, 'PAULA RADCLIFFE', 80), tw(fs, cred, 20)
    pw = max(wn, ws) + 64; top = 700
    box = (W / 2 - pw / 2, top, W / 2 + pw / 2, top + 150)
    rr(L, box, 18, (10, 10, 10, 235))
    ImageDraw.Draw(L).rounded_rectangle(box, radius=18, outline=(90, 90, 90, 255), width=2)
    ctext(d, W / 2, top + 30 + cap(fn), 'PAULA RADCLIFFE', fn, (255, 255, 255, 255), 80)
    d.rectangle([W / 2 - 30, top + 30 + cap(fn) + 16, W / 2 + 30, top + 30 + cap(fn) + 19], fill=GOLD + (255,))
    ctext(d, W / 2, top + 30 + cap(fn) + 19 + 16 + cap(fs), cred, fs, (230, 230, 230, 255), 20)
    return comp(img, shadow(L, 18, 0.35))


def opt_B(img, cred):   # bold condensed name + gold pill credential (no box), above the caption
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    fn = font('cool_hc', 118); fs = font('pn_xb', 30)
    yb = 820
    ctext(d, W / 2, yb, 'PAULA RADCLIFFE', fn, (255, 255, 255, 255), 10)
    ws = tw(fs, cred.upper(), 60); ph = cap(fs) + 22
    pill = (W / 2 - ws / 2 - 22, yb + 22, W / 2 + ws / 2 + 22, yb + 22 + ph)
    rr(L, pill, ph / 2, GOLD + (255,))
    ctext(d, W / 2, pill[1] + 11 + cap(fs), cred.upper(), fs, (20, 16, 8, 255), 60)
    return comp(img, shadow(L, 14, 0.75))


def opt_C(img, cred):   # sports-broadcast strap below the caption (gold block + dark bar)
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    fn, fs = font('galano', 50), font('pn_semi', 28)
    wn, ws = tw(fn, 'PAULA RADCLIFFE', 20), tw(fs, cred.upper(), 120)
    bw = max(wn, ws) + 70 + 26; x0 = W / 2 - bw / 2; top = 1060
    rr(L, (x0, top, x0 + bw, top + 84), 6, (12, 12, 14, 240))
    rr(L, (x0, top, x0 + 14, top + 84), 3, GOLD + (255,))
    text(d, x0 + 40, top + 18 + cap(fn), 'PAULA RADCLIFFE', fn, (255, 255, 255, 255), 20)
    rr(L, (x0 + 26, top + 84, x0 + 26 + ws + 30, top + 84 + 44), 4, GOLD + (255,))
    text(d, x0 + 41, top + 84 + 11 + cap(fs), cred.upper(), fs, (20, 16, 8, 255), 120)
    return comp(img, shadow(L, 16, 0.4))


def opt_D(img, cred):   # frosted glass card, editorial serif name, above the caption
    fn, fs = font('bodoni', 64), font('pn_semi', 25)
    wn, ws = tw(fn, 'Paula Radcliffe', 0), tw(fs, cred.upper(), 220)
    pw = max(wn, ws) + 90; top = 676
    box = (W / 2 - pw / 2, top, W / 2 + pw / 2, top + 172)
    out = frosted(img, box, 24)
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    ctext(d, W / 2, top + 34 + cap(fn), 'Paula Radcliffe', fn, (255, 255, 255, 255))
    d.rectangle([W / 2 - 24, top + 34 + cap(fn) + 20, W / 2 + 24, top + 34 + cap(fn) + 22], fill=GOLD + (255,))
    ctext(d, W / 2, top + 34 + cap(fn) + 22 + 20 + cap(fs), cred.upper(), fs, (245, 240, 230, 255), 220)
    return comp(out, shadow(L, 10, 0.5))


if __name__ == '__main__':
    sys.path.insert(0, HERE)
    from mock_titles import graded_frame
    frames = [('348e0ba6', 1.6, 'a lot harder'), ('593f11c4', 1.6, 'My season')]
    opts = [('A  Centred plate', opt_A), ('B  Bold name + gold pill', opt_B), ('C  Broadcast strap', opt_C), ('D  Frosted glass + serif', opt_D)]
    cred = 'Marathon World Record Holder'
    rows = []
    for key, t, cw in frames:
        base = graded_frame(key, t)
        row = []
        for lab, fn in opts:
            im = caption(fn(base, cred), cw)
            im = im.resize((432, 768), Image.LANCZOS)
            ImageDraw.Draw(im).text((8, 8), lab, fill=(255, 255, 0), font=font('pn_semi', 22))
            row.append(im)
        rows.append(row)
    S = Image.new('RGB', (432 * 4, 768 * 2), (0, 0, 0))
    for r, row in enumerate(rows):
        for c, im in enumerate(row): S.paste(im, (432 * c, 768 * r))
    S.save(os.path.join(HERE, 'title_options.png'))
    # close-ups of the chest area
    Z = Image.new('RGB', (540 * 4, 520 * 2), (0, 0, 0))
    for r, (key, t, cw) in enumerate(frames):
        base = graded_frame(key, t)
        for c, (lab, fn) in enumerate(opts):
            im = caption(fn(base, cred), cw).crop((0, 600, 1080, 1640)).resize((540, 520), Image.LANCZOS)
            Z.paste(im, (540 * c, 520 * r))
    Z.save(os.path.join(HERE, 'title_options_zoom.png'))
    print('ok')


def opt_E(img, cred):   # dark frosted glass + bold condensed name + gold pill (recommended blend)
    fn = font('cool_hc', 104); fs = font('pn_xb', 27)
    wn = tw(fn, 'PAULA RADCLIFFE', 10); ws = tw(fs, cred.upper(), 60)
    pw = max(wn, ws + 44) + 76; top = 660; ph = 196
    box = (W / 2 - pw / 2, top, W / 2 + pw / 2, top + ph)
    out = frosted(img, box, 26, tint=(8, 8, 10), tint_a=0.55, blur=30)
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    yb = top + 30 + cap(fn)
    ctext(d, W / 2, yb, 'PAULA RADCLIFFE', fn, (255, 255, 255, 255), 10)
    pill_h = cap(fs) + 20
    pill = (W / 2 - ws / 2 - 22, yb + 20, W / 2 + ws / 2 + 22, yb + 20 + pill_h)
    rr(L, pill, pill_h / 2, GOLD + (255,))
    ctext(d, W / 2, pill[1] + 10 + cap(fs), cred.upper(), fs, (20, 16, 8, 255), 60)
    return comp(out, L)


if __name__ == '__main__':
    frames = [('348e0ba6', 1.6, 'a lot harder'), ('593f11c4', 1.6, 'My season'), ('f233433f', 1.6, 'three things'), ('974102f7', 1.6, 'questions')]
    tiles = []
    for key, t, cw in frames:
        im = caption(opt_E(graded_frame(key, t), 'Marathon World Record Holder'), cw).resize((432, 768), Image.LANCZOS)
        ImageDraw.Draw(im).text((8, 8), 'E  Dark glass + bold name', fill=(255, 255, 0), font=font('pn_semi', 22))
        tiles.append(im)
    S = Image.new('RGB', (432 * 4, 768))
    for i, im in enumerate(tiles): S.paste(im, (432 * i, 0))
    S.save(os.path.join(HERE, 'title_option_E.png'))
    print('E ok')
