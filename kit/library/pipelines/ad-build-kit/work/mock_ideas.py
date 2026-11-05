"""Storyboard mockups for the boss's motion-graphics notes, on real graded frames:
   1) 3 questions: our own 'ask me a question' card popping out of her phone
   2) 1 star reviews: 1/5 star rating + review card, then the 5-star twist
   3) 3 things to check: board tension (mosaic + glowing number badges) and the reveal with a gold marker circle
   4) Secret weapon: documentary time card"""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mock_titles import graded_frame
from mock_title_options import font, tw, cap, text, ctext, comp, rr, shadow, caption, W, H, GOLD


def star_pts(cx, cy, R, r=None, rot=-90):
    r = r or R * 0.45
    pts = []
    for i in range(10):
        a = math.radians(rot + i * 36); rad = R if i % 2 == 0 else r
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    return pts


def label(im, s):
    d = ImageDraw.Draw(im); d.rectangle([0, 0, im.width, 34], fill=(0, 0, 0)); d.text((8, 6), s, fill=(255, 255, 0), font=font('pn_semi', 20))
    return im


# ---------- 1) question card
def question_card(img, q_lines, n, scale=1.0, cy=1270):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    cw, ch = 760 * scale, (150 + 62 * len(q_lines)) * scale
    x0, y0 = W / 2 - cw / 2, cy - ch / 2
    rr(L, (x0, y0, x0 + cw, y0 + ch), 34 * scale, (255, 255, 255, 255))
    # gradient header (navy -> gold, brand colours)
    hdr = Image.new('RGBA', (int(cw), int(92 * scale)), (0, 0, 0, 0))
    g = np.linspace(0, 1, hdr.width)[None, :, None]
    col = (np.array([24, 33, 58]) * (1 - g) + np.array([207, 174, 99]) * g)
    arr = np.concatenate([np.repeat(col, hdr.height, 0), np.full((hdr.height, hdr.width, 1), 255)], -1).astype(np.uint8)
    hdr = Image.fromarray(arr, 'RGBA')
    m = Image.new('L', hdr.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, hdr.width, hdr.height + 40 * scale], radius=34 * scale, fill=255)
    hdr.putalpha(m); L.alpha_composite(hdr, (int(x0), int(y0)))
    fh = font('pn_xb', int(30 * scale)); fq = font('sf_bold', int(46 * scale)); fs = font('pn_semi', int(24 * scale))
    text(d, x0 + 40 * scale, y0 + 46 * scale + cap(fh) / 2, 'ASK PAULA', fh, (255, 255, 255, 255), 120)
    tag = 'QUESTION %d OF 3' % n
    text(d, x0 + cw - 40 * scale - tw(fs, tag, 80), y0 + 46 * scale + cap(fs) / 2, tag, fs, (255, 255, 255, 230), 80)
    for i, ln in enumerate(q_lines):
        ctext(d, W / 2, y0 + (92 + 50 + 62 * i) * scale + cap(fq) / 2, ln, fq, (18, 18, 22, 255))
    return comp(img, shadow(L, 26, 0.45))


# ---------- 2) star rating + review card
def rating(img, lit, cy=1120, review=None, typed=1.0):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    cw, ch = 820, 150 + (170 if review else 0)
    x0, y0 = W / 2 - cw / 2, cy - 75
    rr(L, (x0, y0, x0 + cw, y0 + ch), 30, (14, 14, 16, 236))
    ImageDraw.Draw(L).rounded_rectangle((x0, y0, x0 + cw, y0 + ch), radius=30, outline=(80, 80, 84, 255), width=2)
    for i in range(5):
        cx = W / 2 + (i - 2) * 112; pts = star_pts(cx, y0 + 75, 46)
        if i < lit:
            d.polygon(pts, fill=GOLD + (255,))
        else:
            d.polygon(pts, outline=(120, 120, 126, 255), width=4)
    if review:
        fr = font('pn_reg', 38); s = review[:max(1, int(len(review) * typed))]
        words, lines, cur = s.split(' '), [], ''
        for w_ in words:
            if tw(fr, (cur + ' ' + w_).strip()) > cw - 90: lines.append(cur); cur = w_
            else: cur = (cur + ' ' + w_).strip()
        lines.append(cur)
        for i, ln in enumerate(lines[:3]):
            text(d, x0 + 45, y0 + 175 + i * 50 + cap(fr), ln, fr, (235, 235, 235, 255))
    out = comp(img, shadow(L, 22, 0.4))
    if lit:   # glow on the lit star(s)
        G = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dg = ImageDraw.Draw(G)
        for i in range(lit): dg.polygon(star_pts(W / 2 + (i - 2) * 112, y0 + 75, 58), fill=GOLD + (150,))
        G = G.filter(ImageFilter.GaussianBlur(22)); out = comp(out, G); out = comp(out, L.crop((0, 0, W, H)))
    return out


# ---------- 3) whiteboard tension
BOARD_LINES = [(40, 520, 560, 640), (40, 690, 640, 860), (40, 900, 640, 1080)]   # approx text rows on the board at t=1.6 s


def mosaic(img, box, block=34):
    x0, y0, x1, y1 = [int(v) for v in box]
    reg = img.crop((x0, y0, x1, y1))
    small = reg.resize((max(1, (x1 - x0) // block), max(1, (y1 - y0) // block)), Image.BILINEAR)
    img = img.copy(); img.paste(small.resize(reg.size, Image.NEAREST), (x0, y0)); return img


def badges(img, glow=True, which=(1, 2, 3)):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    fb = font('pn_xb', 44)
    for n, (x0, y0, x1, y1) in enumerate(BOARD_LINES, 1):
        if n not in which: continue
        cx, cy = x1 + 52, (y0 + y1) / 2
        d.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill=GOLD + (255,))
        ctext(d, cx, cy + cap(fb) / 2, str(n), fb, (20, 16, 8, 255))
    out = img
    if glow:
        G = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dg = ImageDraw.Draw(G)
        dg.rounded_rectangle([20, 470, 720, 1400], radius=10, outline=(255, 236, 180, 200), width=18)
        out = comp(out, G.filter(ImageFilter.GaussianBlur(16)))
    return comp(out, shadow(L, 12, 0.5))


def marker_circle(img, box):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    x0, y0, x1, y1 = box; cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2 + 26, (y1 - y0) / 2 + 18
    pts = [(cx + rx * math.cos(math.radians(a)) * (1 + 0.04 * math.sin(a / 23)), cy + ry * math.sin(math.radians(a))) for a in range(-200, 175, 4)]
    d.line(pts, fill=GOLD + (255,), width=10, joint='curve')
    return comp(img, shadow(L, 6, 0.5))


def time_card(img, big, small):
    im = Image.fromarray((np.asarray(img.convert('L').convert('RGB')).astype(np.float64) * 0.55).astype(np.uint8))   # dim + mono archive look
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    fb, fs = font('cool_hc', 170), font('pn_semi', 34)
    ctext(d, W / 2, 1000, big, fb, (255, 255, 255, 255), 10)
    ctext(d, W / 2, 1070, small, fs, GOLD + (255,), 300)
    return comp(im, shadow(L, 16, 0.6))


if __name__ == '__main__':
    tiles = []
    # 1) 3 questions (she reads off her phone at ~3.6-8.2 s)
    q = graded_frame('974102f7', 5.0)
    tiles.append(label(caption(question_card(q, ['Why can\'t I just eat a', 'balanced diet instead?'], 1, scale=0.35, cy=1330), 'Why can\'t').resize((432, 768), Image.LANCZOS), '3Q  pops out of the phone'))
    tiles.append(label(caption(question_card(q, ['Why can\'t I just eat a', 'balanced diet instead?'], 1), 'we just eat').resize((432, 768), Image.LANCZOS), '3Q  question card settles'))
    # 2) 1 star reviews
    s = graded_frame('cd03e189', 1.6)
    tiles.append(label(caption(rating(s, 1), 'star reviews').resize((432, 768), Image.LANCZOS), '1 STAR  only one star lights'))
    tiles.append(label(caption(rating(s, 1, review='"My shelf used to be completely full of containers. Now there\'s just one pouch on it."', typed=0.8), 'my shelf').resize((432, 768), Image.LANCZOS), '1 STAR  review types in'))
    tiles.append(label(caption(rating(s, 5), 'I\'ll happily take').resize((432, 768), Image.LANCZOS), '1 STAR  twist: all 5 light up'))
    # 3) 3 things to check
    b = graded_frame('f233433f', 1.6)
    t1 = b
    for bx in BOARD_LINES: t1 = mosaic(t1, bx)
    tiles.append(label(caption(badges(t1), 'three things').resize((432, 768), Image.LANCZOS), 'BOARD  hidden + glowing 1-2-3'))
    t2 = b
    for bx in BOARD_LINES[1:]: t2 = mosaic(t2, bx)
    t2 = marker_circle(badges(t2, glow=False, which=(2, 3)), BOARD_LINES[0])
    tiles.append(label(caption(t2, 'no mega doses').resize((432, 768), Image.LANCZOS), 'BOARD  item 1 revealed + circled'))
    # 4) Secret weapon time card
    r = graded_frame('593f11c4', 1.6)
    tiles.append(label(time_card(r, 'THREE MONTHS LATER', 'DECEMBER 1998').resize((432, 768), Image.LANCZOS), 'SECRET WEAPON  doc time card'))
    S = Image.new('RGB', (432 * 4, 768 * 2), (0, 0, 0))
    for i, t in enumerate(tiles): S.paste(t, ((i % 4) * 432, (i // 4) * 768))
    S.save(os.path.join(HERE, 'idea_mockups.png'))
    print('ok')
