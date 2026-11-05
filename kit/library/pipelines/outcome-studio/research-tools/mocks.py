"""Render 4 proposal mock frames (1080x1920) with TikTok Sans in TikTok's own text treatments.
python -I mocks.py <mock dir> <font ttf> <out sheet.jpg>
"""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

D, FONT, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
EMOJI = r"C:\Windows\Fonts\seguiemj.ttf"
W, H = 1080, 1920
MINT, RED = (153, 255, 188), (255, 61, 94)
SIGNAL, ALERT = (26, 255, 87), (253, 108, 107)  # Outcome brand guide: Signal Green #1AFF57, Alert Red #FD6C6B


def font(size, style="SemiBold"):
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_name(style)
    return f


def text_w(d, s, f):
    return d.textlength(s, font=f)


def draw_runs(d, x, y, runs, f, ef, lh=None, pad_y=0):
    """runs: list of (text, colour, is_emoji); colour ("chip", rgb) = number on its own coloured box, black text"""
    for s, col, emo in runs:
        if emo:
            d.text((x, y - int(f.size * 0.08)), s, font=ef, embedded_color=True)
            x += text_w(d, s, ef)
        elif isinstance(col, tuple) and len(col) == 2 and col[0] == "chip":
            w = text_w(d, s, f)
            d.rounded_rectangle([x - 8, y - pad_y + 6, x + w + 8, y + (lh or f.size) - pad_y - 4], radius=int(f.size * 0.22), fill=col[1])
            d.text((x, y), s, font=f, fill=(0, 0, 0))
            x += w + 16
        else:
            d.text((x, y), s, font=f, fill=col)
            x += text_w(d, s, f)
    return x


def runs_w(d, runs, f, ef):
    return sum(text_w(d, s, ef if e else f) + (16 if (isinstance(c, tuple) and len(c) == 2 and c[0] == "chip") else 0) for s, c, e in runs)


def tiktok_box(img, lines, cy, size=56, style="SemiBold"):
    """TikTok 'Classic' text with the solid white background: each line its own rounded white box, black text."""
    d = ImageDraw.Draw(img)
    f = font(size, style)
    ef = ImageFont.truetype(EMOJI, int(size * 0.9))
    lh = int(size * 1.32)
    pad_x, pad_y, r = int(size * 0.42), int(size * 0.16), int(size * 0.32)
    top = cy - (lh * len(lines)) // 2
    for i, runs in enumerate(lines):
        tw = runs_w(d, runs, f, ef)
        x0 = (W - tw) / 2
        y0 = top + i * lh
        d.rounded_rectangle([x0 - pad_x, y0 - pad_y, x0 + tw + pad_x, y0 + lh - pad_y + 2], radius=r, fill=(255, 255, 255))
        draw_runs(d, x0, y0, [(s, (0, 0, 0) if c is None else c, e) for s, c, e in runs], f, ef, lh, pad_y)


def caption(img, runs, cy, size=92, style="ExtraBold", stroke=7):
    """CapCut-style spoken caption: white bold text, black outline, one keyword coloured."""
    d = ImageDraw.Draw(img)
    f = font(size, style)
    ef = ImageFont.truetype(EMOJI, int(size * 0.85))
    tw = runs_w(d, runs, f, ef)
    x = (W - tw) / 2
    y = cy - size // 2
    for s, col, emo in runs:
        if emo:
            d.text((x, y), s, font=ef, embedded_color=True)
            x += text_w(d, s, ef)
        else:
            d.text((x, y), s, font=f, fill=col or (255, 255, 255), stroke_width=stroke, stroke_fill=(0, 0, 0))
            x += text_w(d, s, f)


def cover_fit(src, w, h):
    s = max(w / src.width, h / src.height)
    im = src.resize((int(src.width * s + 0.5), int(src.height * s + 0.5)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


# A: real screen recording, letterboxed, headline box in the black bar
rec = Image.open(os.path.join(D, "goal150.png")).convert("RGB")
A = Image.new("RGB", (W, H), (0, 0, 0))
# punch-in on the part that matters (title, score, chart); the YES / NO buttons come back when the clip zooms out
crop = rec.crop((0, int(rec.height * 0.085), rec.width, int(rec.height * 0.80)))
sh = 1500
sw = int(crop.width * sh / crop.height)
A.paste(crop.resize((sw, sh), Image.LANCZOS), ((W - sw) // 2, 420))
tiktok_box(A, [[("Sporting went from 30% to ", None, False), ("53%", ("chip", SIGNAL), False)], [("in two minutes ", None, False), ("😳", None, True)]], 330, size=54)

# B: slideshow slide 1, photo + box (photo mode)
B = cover_fit(Image.open(os.path.join(D, "crowd.png")).convert("RGB"), W, H)
tiktok_box(B, [[("the ballon d'or is in 12 days.", None, False)], [("one name is at ", None, False), ("62%", ("chip", SIGNAL), False), (" ", None, False), ("👀", None, True)]], int(H * 0.36), size=56)

# C: spoken caption style over footage, number coloured mint (went up)
C = Image.open(os.path.join(D, "ball.png")).convert("RGB").resize((W, H), Image.LANCZOS)
caption(C, [("now ", None, False), ("53%", SIGNAL, False)], int(H * 0.63), size=110)
caption(C, [("sporting were 30%", None, False)], int(H * 0.555), size=64, stroke=5)

# D: cover check: A at grid size with the Instagram 3:4 crop and the TikTok bottom UI zone marked
Dm = A.copy()
dd = ImageDraw.Draw(Dm)
top34 = (H - 1440) // 2
for y in (top34, top34 + 1440):
    for x in range(0, W, 40):
        dd.line([x, y, x + 22, y], fill=(255, 0, 242), width=6)
dd.rectangle([0, int(H * 0.80), W, H], outline=(0, 255, 255), width=6)
f = font(40, "Bold")
dd.text((24, top34 + 12), "Instagram grid crop 3:4", font=f, fill=(255, 0, 242))
dd.text((24, int(H * 0.80) + 14), "TikTok caption + buttons zone", font=f, fill=(0, 255, 255))

tiles = [("A real screen recording + box", A), ("B slideshow slide 1", B), ("C spoken caption style", C), ("D cover check", Dm)]
TW = 360
THh = int(TW * H / W)
LAB = 34
sheet = Image.new("RGB", (len(tiles) * (TW + 10) + 10, THh + LAB + 20), (120, 120, 120))
sd = ImageDraw.Draw(sheet)
lf = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 18)
for i, (lab, im) in enumerate(tiles):
    x = 10 + i * (TW + 10)
    sheet.paste(im.resize((TW, THh), Image.LANCZOS), (x, 10))
    sd.rectangle([x, THh + 10, x + TW, THh + 10 + LAB], fill=(20, 20, 20))
    sd.text((x + 6, THh + 16), "MOCK " + lab, font=lf, fill=(255, 235, 0))
    im.save(os.path.join(D, "mock_%s.jpg" % lab[0]), quality=88)
sheet.save(OUT, quality=85)
print("saved", OUT, sheet.size)
