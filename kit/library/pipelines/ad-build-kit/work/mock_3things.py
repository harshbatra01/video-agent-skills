"""3 things to check: board-reveal concepts + per-point inserts, mocked on real Premiere frames."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

random.seed(7)
FR = r'C:\VISION\IMMUFIX\repair\ENCODED RUSHES\_claude_check_frames'
UF = r'C:\Users\Kanishk\AppData\Local\Microsoft\Windows\Fonts'
COOL, XB, SB, RG = UF + r'\Coolvetica Hv Comp.otf', UF + r'\Proxima Nova Extrabold.ttf', UF + r'\Proxima Nova Semibold.ttf', UF + r'\Proxima Nova Regular.ttf'
GEOB, GEOI = r'C:\Windows\Fonts\georgiab.ttf', r'C:\Windows\Fonts\georgiai.ttf'
GOLD, GOLD_HI, HL = (207, 174, 99), (243, 199, 92), (255, 184, 34)
W, H = 1080, 1920
ITEMS = [[((64, 686), (536, 626), 96)],
         [((105, 860), (565, 770), 92), ((140, 938), (460, 893), 80)],
         [((165, 1103), (700, 962), 96), ((210, 1182), (535, 1088), 84)]]
BULLETS = [(38, 700), (86, 879), (158, 1096)]   # tick centres, just left of each bullet dot


def F(path, size): return ImageFont.truetype(path, size)
def frame(n): return Image.open('%s\\%s.png' % (FR, n)).convert('RGB')


def unit(p0, p1):
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]; L = math.hypot(dx, dy)
    return (dx / L, dy / L), (-dy / L, dx / L), L


def band(p0, p1, th, ext=14, t0=0.0, t1=1.0, jit=0.0, round_ends=True, n=28):
    """polygon for a stroke along p0->p1 (fraction t0..t1), rough edges if jit > 0, rounded ends"""
    d, nn, L = unit(p0, p1)
    a = (p0[0] + d[0] * (L * t0 - ext * (t0 == 0)), p0[1] + d[1] * (L * t0 - ext * (t0 == 0)))
    b = (p0[0] + d[0] * (L * t1 + ext * (t1 == 1)), p0[1] + d[1] * (L * t1 + ext * (t1 == 1)))
    r = th / 2; pts = []
    for i in range(n + 1):                       # top edge a -> b
        f = i / n; j = random.uniform(-jit, jit)
        pts.append((a[0] + (b[0] - a[0]) * f - nn[0] * (r + j), a[1] + (b[1] - a[1]) * f - nn[1] * (r + j)))
    if round_ends:
        for k in range(1, 8):                     # cap at b
            ang = -math.pi / 2 + math.pi * k / 8; rr = r + random.uniform(-jit, jit)
            pts.append((b[0] + d[0] * math.cos(ang) * rr * 0.55 + nn[0] * math.sin(ang) * rr,
                        b[1] + d[1] * math.cos(ang) * rr * 0.55 + nn[1] * math.sin(ang) * rr))
    for i in range(n + 1):                       # bottom edge b -> a
        f = 1 - i / n; j = random.uniform(-jit, jit)
        pts.append((a[0] + (b[0] - a[0]) * f + nn[0] * (r + j), a[1] + (b[1] - a[1]) * f + nn[1] * (r + j)))
    if round_ends:
        for k in range(1, 8):                     # cap at a
            ang = math.pi / 2 + math.pi * k / 8; rr = r + random.uniform(-jit, jit)
            pts.append((a[0] + d[0] * math.cos(ang) * rr * 0.55 + nn[0] * math.sin(ang) * rr,
                        a[1] + d[1] * math.cos(ang) * rr * 0.55 + nn[1] * math.sin(ang) * rr))
    return pts


def mask_of(polys, blur=1.2):
    m = Image.new('L', (W * 2, H * 2), 0); d = ImageDraw.Draw(m)
    for p in polys: d.polygon([(x * 2, y * 2) for x, y in p], fill=255)
    m = m.resize((W, H), Image.LANCZOS)
    return m.filter(ImageFilter.GaussianBlur(blur)) if blur else m


def comp(base, color, mask, alpha=1.0):
    over = Image.new('RGB', base.size, color)
    return Image.composite(over, base, mask.point(lambda v: int(v * alpha)))


def multiply(base, color, mask, alpha=1.0):
    a = np.asarray(base).astype(np.float32); c = np.array(color, np.float32) / 255
    m = (np.asarray(mask).astype(np.float32) / 255 * alpha)[..., None]
    return Image.fromarray(np.clip(a * (1 - m) + a * c * m, 0, 255).astype(np.uint8))


def screen(base, color, mask, strength=1.0):
    a = np.asarray(base).astype(np.float32) / 255; c = np.array(color, np.float32) / 255
    m = (np.asarray(mask).astype(np.float32) / 255 * strength)[..., None]
    out = 1 - (1 - a) * (1 - c * m)
    return Image.fromarray(np.clip(out * 255, 0, 255).astype(np.uint8))


def glow(base, mask, color, radius, strength):
    g = mask.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(radius))
    return screen(base, color, g, strength)


def marker(base, strokes, t0=0.0, t1=1.0, color=(17, 17, 19), jit=4.5):
    m = mask_of([band(p0, p1, th + 6, t0=t0, t1=t1, jit=jit) for p0, p1, th in strokes], 0.8)
    return comp(base, color, m, 0.97)


def highlight(base, strokes, t1=1.0, color=HL):
    m = mask_of([band(p0, p1, th - 4, t1=t1, jit=2.5) for p0, p1, th in strokes], 1.5)
    return multiply(base, color, m, 0.9)


def tick(base, pos, size=74, color=GOLD_HI, width=13, shadow=True):
    S = 4; size = float(size); pad = int(size * 2)
    lay = Image.new('L', (pad * S, pad * S), 0); d = ImageDraw.Draw(lay)
    pts = [(-0.42, 0.02), (-0.08, 0.36), (0.62, -0.58)]
    P = [((pad / 2 + x * size) * S, (pad / 2 + y * size) * S) for x, y in pts]
    d.line(P, fill=255, width=width * S, joint='curve')
    for p in (P[0], P[-1]): d.ellipse([p[0] - width * S / 2, p[1] - width * S / 2, p[0] + width * S / 2, p[1] + width * S / 2], fill=255)
    lay = lay.resize((pad, pad), Image.LANCZOS)
    full = Image.new('L', (W, H), 0); full.paste(lay, (int(pos[0] - pad / 2), int(pos[1] - pad / 2)))
    if shadow:
        sh = Image.new('L', (W, H), 0); sh.paste(lay, (int(pos[0] - pad / 2 + 3), int(pos[1] - pad / 2 + 5)))
        base = comp(base, (0, 0, 0), sh.filter(ImageFilter.GaussianBlur(5)), 0.45)
    base = glow(base, full, color, 10, 0.35)
    return comp(base, color, full)


def text_layer(txt, font, fill, shadow=(0, 0, 0, 120), sh_off=(0, 6), sh_blur=10, tracking=0):
    asc, desc = font.getmetrics()
    w = int(sum(font.getlength(c) for c in txt) + tracking * len(txt)) + 40; h = asc + desc + 40
    lay = Image.new('RGBA', (w + 60, h + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    x = 30 + 20
    for c in txt:
        d.text((x, 30 + 20), c, font=font, fill=fill); x += font.getlength(c) + tracking
    if shadow:
        a = lay.split()[3].filter(ImageFilter.GaussianBlur(sh_blur))
        sh = Image.new('RGBA', lay.size, shadow[:3] + (0,)); sh.putalpha(a.point(lambda v: v * shadow[3] // 255))
        out = Image.new('RGBA', lay.size, (0, 0, 0, 0)); out.alpha_composite(sh, sh_off); out.alpha_composite(lay)
        return out
    return lay


def paste(base, lay, xy, angle=0.0):
    if angle: lay = lay.rotate(angle, resample=Image.BICUBIC, expand=True)
    b = base.convert('RGBA'); b.alpha_composite(lay, (int(xy[0]), int(xy[1]))); return b.convert('RGB')


def glass(base, box, radius=34, tint=(255, 255, 255), tint_a=0.16, blur=22, border_a=0.45):
    x0, y0, x1, y1 = box
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rounded_rectangle(box, radius, fill=255)
    bl = base.filter(ImageFilter.GaussianBlur(blur))
    bl = Image.blend(bl, Image.new('RGB', base.size, tint), tint_a)
    sh = m.filter(ImageFilter.GaussianBlur(26))
    base = comp(base, (0, 0, 0), sh.transform(sh.size, Image.AFFINE, (1, 0, 0, 0, 1, -14)), 0.35)
    base = Image.composite(bl, base, m)
    e = Image.new('L', (W, H), 0); ImageDraw.Draw(e).rounded_rectangle(box, radius, outline=255, width=2)
    return comp(base, (255, 255, 255), e, border_a)


# ------------------------------------------------------------------ board treatments
def frosted(base, strokes, glow_strength=0.85, cell=17):
    """mosaic pane: the handwriting turns into warm grey blocks, gold glow leaks round the edge"""
    m = mask_of([band(p0, p1, th + 18, ext=22) for p0, p1, th in strokes], 0.8)
    mo = base.filter(ImageFilter.GaussianBlur(4)).resize((W // cell, H // cell), Image.BILINEAR).resize((W, H), Image.NEAREST)
    a = np.asarray(mo).astype(np.float32); inside = np.asarray(m) > 128
    white = np.percentile(a[inside], 92, axis=0)
    a = white - (white - a) * 2.0                              # hidden text reads as grey pixels on the board white
    a = a * 0.94 + np.array([255, 250, 240], np.float32) * 0.06
    # warm halo round the pane (normal blend: screen does nothing on a white board)
    halo = np.asarray(m.filter(ImageFilter.MaxFilter(13)).filter(ImageFilter.GaussianBlur(16))).astype(np.float32)
    halo = Image.fromarray(np.clip(halo - np.asarray(m).astype(np.float32) * 0.6, 0, 255).astype(np.uint8))
    lit = comp(base, (255, 176, 58), halo, 0.75 * glow_strength)
    out = Image.composite(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)), lit, m)
    edge = Image.fromarray(np.clip(np.asarray(m).astype(int) - np.asarray(m.filter(ImageFilter.MinFilter(5))).astype(int), 0, 255).astype(np.uint8))
    return comp(out, (255, 255, 255), edge, 0.6)


def shatter(base, strokes, front=0.5, cell=17):
    """frosted pill breaking into pixels from the left; pixels drift up-right and fade"""
    m = mask_of([band(p0, p1, th + 18, ext=22) for p0, p1, th in strokes], 0)
    fro = frosted(base, strokes, 0.7)
    p0, p1, th = strokes[0]; d, nn, L = unit(p0, p1)
    ma = np.asarray(m); fa = np.asarray(fro); out = base.copy(); dr = ImageDraw.Draw(out, 'RGBA')
    keep = np.zeros((H, W), np.uint8)
    for y in range(0, H, cell):
        for x in range(0, W, cell):
            if ma[min(y + cell // 2, H - 1), min(x + cell // 2, W - 1)] < 128: continue
            proj = ((x - p0[0]) * d[0] + (y - p0[1]) * d[1]) / L
            if proj > front + 0.06:
                keep[y:y + cell, x:x + cell] = 255
            elif proj > front - 0.35 and random.random() < 0.75:
                k = (front + 0.06 - proj) / 0.41
                col = tuple(int(v) for v in fa[min(y + 8, H - 1), min(x + 8, W - 1)])
                dx, dy = 70 * k * random.uniform(0.4, 1.2), -120 * k * random.uniform(0.3, 1.1)
                s = cell * (1 - 0.5 * k)
                dr.rectangle([x + dx, y + dy, x + dx + s, y + dy + s], fill=col + (int(235 * (1 - k)),))
    out = Image.composite(fro, out, Image.fromarray(keep).filter(ImageFilter.GaussianBlur(0.6)))
    fx = p0[0] + d[0] * L * front; fy = p0[1] + d[1] * L * front     # light streak at the break front
    streak = Image.new('L', (W, H), 0)
    ImageDraw.Draw(streak).line([(fx - nn[0] * 90, fy - nn[1] * 90), (fx + nn[0] * 90, fy + nn[1] * 90)], fill=255, width=10)
    out = screen(out, (255, 214, 120), streak.filter(ImageFilter.GaussianBlur(14)), 1.0)
    return screen(out, (255, 240, 200), streak.filter(ImageFilter.GaussianBlur(3)), 0.9)


def gold_under(base, strokes):
    p0, p1, th = strokes[-1]; d, nn, L = unit(p0, p1)
    q0 = (p0[0] + nn[0] * (th / 2 + 4), p0[1] + nn[1] * (th / 2 + 4)); q1 = (p1[0] + nn[0] * (th / 2 + 4), p1[1] + nn[1] * (th / 2 + 4))
    m = mask_of([band(q0, q1, 7, ext=0)], 0.6)
    base = glow(base, m, (255, 190, 70), 12, 0.8)
    return comp(base, GOLD_HI, m)


# ------------------------------------------------------------------ sheet helpers
PW, PH, CAP = 360, 640, 86


def sheet(title, sub, panels, out):
    n = len(panels); S = Image.new('RGB', (n * PW + (n - 1) * 8, 70 + PH + CAP), (14, 14, 16)); d = ImageDraw.Draw(S)
    d.text((14, 10), title, font=F(XB, 30), fill=(243, 199, 92)); d.text((14, 44), sub, font=F(SB, 19), fill=(205, 205, 205))
    for i, (img, t, line) in enumerate(panels):
        x = i * (PW + 8); S.paste(img.resize((PW, PH), Image.LANCZOS), (x, 70))
        d.text((x + 8, 70 + PH + 8), t, font=F(XB, 20), fill=(243, 199, 92))
        y = 70 + PH + 34
        for ln in line.split('\n'): d.text((x + 8, y), ln, font=F(SB, 17), fill=(225, 225, 225)); y += 22
    S.save(out); print(out, S.size)


base = frame('tt_15p0')

# ---- Concept 1: marker redaction -> highlighter + tick
a = base
for it in ITEMS: a = marker(a, it)
b = base
b = highlight(b, ITEMS[0], 0.62); b = marker(b, ITEMS[0], t0=0.62)
for it in ITEMS[1:]: b = marker(b, it)
c = highlight(base, ITEMS[0]); c = tick(c, BULLETS[0])
c = highlight(c, ITEMS[1][:1], 1.0); c = highlight(c, ITEMS[1][1:], 0.35); c = marker(c, ITEMS[1][1:], t0=0.35); c = marker(c, ITEMS[2])
dd = base
for i, it in enumerate(ITEMS): dd = highlight(dd, it); dd = tick(dd, BULLETS[i])
sheet('CONCEPT 1  ·  MARKER REVEAL', 'Lines start blacked out like a secret file. Each one is wiped clean by a highlighter on cue, then gets a gold tick. On theme: "things to check".',
      [(a, '0.2s  hidden', '"...these three things\nbefore buying"'), (b, '2.9s  wipe 1', '"Number one: no mega doses"\n(marker squeak SFX)'),
       (c, '14.5s  wipe 2', '"Number two: enhanced\nnutrient bioavailability"'), (dd, '27.7s  all ticked', '"Finally, better cellular\nuptake" (3 ticks pulse)')], 'concept1_marker.png')

# ---- Concept 2: frosted glass + glow -> pixel shatter reveal
a = base
for it in ITEMS: a = frosted(a, it)
b = shatter(base, ITEMS[0], front=0.55)
for it in ITEMS[1:]: b = frosted(b, it)
c = gold_under(base, ITEMS[0]); c = shatter(c, ITEMS[1], front=0.5); c = frosted(c, ITEMS[2])
dd = base
for it in ITEMS: dd = gold_under(dd, it)
sheet('CONCEPT 2  ·  FROSTED GLASS + GLOW', 'Boss note "glows behind mosaic". Lines sit under frosted glass with a warm glow leaking out. Each pane shatters into pixels with a light streak.',
      [(a, '0.2s  frosted', 'warm glow pulses on\n"these three things"'), (b, '2.9s  shatter 1', 'pixels fly off, gold streak,\nglass "tink" SFX'),
       (c, '14.5s  shatter 2', 'revealed lines keep a\ngold underline'), (dd, '27.7s  all lit', 'all three underlined,\none soft glow pulse')], 'concept2_glass.png')

# ---- Concept 3: board line lifts off as big type (works as captions)
def checkbox(img, x, y, s=64):
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rounded_rectangle([x, y, x + s, y + s], 14, fill=255)
    img = comp(img, (0, 0, 0), m.filter(ImageFilter.GaussianBlur(10)).transform(m.size, Image.AFFINE, (1, 0, 0, 0, 1, -6)), 0.35)
    img = comp(img, GOLD, m)
    return tick(img, (x + s * 0.5, y + s * 0.55), size=s * 0.62, color=(20, 16, 8), width=9, shadow=False)


def liftoff(img, lines, item, sub=None, y=150):
    img = highlight(img, ITEMS[item]); img = glow(img, mask_of([band(p0, p1, th) for p0, p1, th in ITEMS[item]], 0), (255, 190, 70), 18, 0.35)
    f = F(COOL, 150); yy = y
    for i, ln in enumerate(lines):
        lay = text_layer(ln, f, (255, 255, 255), tracking=4)
        img = paste(img, lay, (40 if i == 0 else 40, yy - 50), angle=0); yy += 132
    img = checkbox(img, 56, y - 70 - 6)
    lab = text_layer('CHECK', F(XB, 40), (255, 255, 255), shadow=(0, 0, 0, 200), sh_off=(0, 3), sh_blur=6, tracking=8)
    img = paste(img, lab, (88, y - 76 - 39))
    if sub:
        lay = text_layer(sub, F(SB, 34), (235, 235, 235), shadow=(0, 0, 0, 170), sh_off=(0, 3), sh_blur=6)
        img = paste(img, lay, (40, yy - 30))
    return img

b = liftoff(base, ['NO MEGA', 'DOSES'], 0)
c = liftoff(base, ['BIOAVAILABILITY'], 1, 'how much your body can actually use')
dd = liftoff(base, ['CELLULAR', 'UPTAKE'], 2, 'almost 100% into the cells')
sheet('CONCEPT 3  ·  LIFT-OFF TYPE', 'The line she is talking about glows gold on the board while big type lands above it. Doubles as captions since this ad has none.',
      [(b, '2.9s', '"No mega doses"\ntype slams in, box ticks'), (c, '14.5s', '"Bioavailability"\none-word slam + plain meaning'),
       (dd, '27.7s', '"Cellular uptake"\nsame system, third tick')], 'concept3_liftoff.png')

# ------------------------------------------------------------------ inserts
# 1) 100x meter over the vitamin C tablet
v = frame('tt_11p5_vitc')
fb, fx = F(COOL, 380), F(COOL, 250)
lay = text_layer('100', fb, (255, 255, 255), tracking=2); v = paste(v, lay, (90 - 50, 210 - 50))
xw = sum(fb.getlength(c) + 2 for c in '100')
lay = text_layer('x', fx, GOLD_HI); v = paste(v, lay, (90 + xw + 10 - 50, 210 + fb.getmetrics()[0] - fx.getmetrics()[0] - 50))
lab = text_layer('THE DAILY AMOUNT OF VITAMIN C', F(XB, 34), (255, 255, 255), shadow=(0, 0, 0, 170), sh_off=(0, 3), sh_blur=6, tracking=3)
v = paste(v, lab, (96, 660))
v = glass(v, (96, 760, 1000, 812), radius=26, tint_a=0.25)
fill = Image.new('L', (W, H), 0); ImageDraw.Draw(fill).rounded_rectangle((104, 768, 1080 + 60, 804), 18, fill=255)
v = glow(v, fill, (255, 120, 40), 18, 0.8); v = comp(v, (255, 104, 40), fill)
mk = Image.new('L', (W, H), 0); ImageDraw.Draw(mk).rectangle((116, 748, 121, 824), fill=255); v = comp(v, (255, 255, 255), mk)
lab = text_layer('DAILY NEED', F(XB, 24), (255, 255, 255), shadow=(0, 0, 0, 170), sh_off=(0, 2), sh_blur=4, tracking=3); v = paste(v, lab, (60, 812))
# 2) dictionary card
dct = frame('tt_15p0')
dct = glass(dct, (60, 1380, 1020, 1760), radius=40, tint=(20, 20, 24), tint_a=0.45, blur=26, border_a=0.35)
lay = text_layer('bi·o·a·vail·a·bil·i·ty', F(GEOB, 64), (255, 255, 255), shadow=None); dct = paste(dct, lay, (70, 1385))
lay = text_layer('noun', F(GEOI, 38), GOLD_HI, shadow=None); dct = paste(dct, lay, (70, 1470))
y = 1530
for ln in ['How much of a nutrient your body', 'can actually absorb and use.']:
    lay = text_layer(ln, F(RG, 44), (236, 236, 236), shadow=None); dct = paste(dct, lay, (70, y)); y += 58
# 3) years odometer over the drink
dr = frame('tt_43p3_drink')
X0, Y0 = 70, 300                                      # top-left, over the dark trees
lab = text_layer('TAKING IT SINCE', F(XB, 38), GOLD_HI, shadow=(0, 0, 0, 200), sh_off=(0, 3), sh_blur=6, tracking=6); dr = paste(dr, lab, (X0 - 50, Y0 - 60 - 50))
big = F(COOL, 300); asc = big.getmetrics()[0]
lay = text_layer('19', big, (255, 255, 255), tracking=2); dr = paste(dr, lay, (X0 - 50, Y0 - 50))
x2 = X0 + sum(big.getlength(c) + 2 for c in '19') + 4
lay = text_layer('98', big, (255, 255, 255), tracking=2); dr = paste(dr, lay, (x2 - 50, Y0 - 50))
lab = text_layer('then rolls on to 2026', F(SB, 38), (240, 240, 240), shadow=(0, 0, 0, 200), sh_off=(0, 3), sh_blur=6); dr = paste(dr, lab, (X0 - 50, Y0 + asc + 30 - 50))
# 4) 100% energy bar over the running shot
rn = frame('tt_40p0')
lab = text_layer('WORKING AT', F(XB, 40), (255, 255, 255), shadow=(0, 0, 0, 170), sh_off=(0, 3), sh_blur=6, tracking=6); rn = paste(rn, lab, (70, 1390))
lay = text_layer('100%', F(COOL, 260), (255, 255, 255), tracking=2); rn = paste(rn, lay, (60, 1420))
rn = glass(rn, (90, 1740, 990, 1784), radius=22, tint_a=0.25)
fill = Image.new('L', (W, H), 0); ImageDraw.Draw(fill).rounded_rectangle((98, 1748, 982, 1776), 14, fill=255)
rn = glow(rn, fill, (255, 190, 70), 16, 0.9); rn = comp(rn, GOLD_HI, fill)
sheet('PER-POINT INSERTS  ·  text that carries the ad (no captions here)', 'Quick graphics on the lines that need proof. Same type system as the title: Coolvetica, Proxima, gold.',
      [(v, '9.5s  "100 times the daily amount"', 'meter shoots past "daily need"\nand off screen, number counts up'),
       (dct, '15.5s  "bioavailability"', 'dictionary card slides up\nwhile she explains it'),
       (dr, '42.1s  "almost 30 years"', 'year counter rolls 1998 to\n2026 over the drink shot'),
       (rn, '37.5s  "work at 100%"', 'bar fills over her run,\nor big 100% behind her (mask)')], 'inserts_3things.png')
