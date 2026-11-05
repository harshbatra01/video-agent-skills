import sys, json, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, '.')
from mock_titles import graded_frame, FONT, text_w, draw_tracked

def rrect_mask(W, H, box, r, scale=4):
    m = Image.new('L', (W * scale, H * scale), 0)
    x0, y0, x1, y1 = [v * scale for v in box]
    ImageDraw.Draw(m).rounded_rectangle([x0, y0, x1, y1], radius=r * scale, fill=255)
    return m.resize((W, H), Image.LANCZOS)

def card(im, cw=640, ch=206, r=30, fill=(13, 13, 13), fop=0.84, stroke=(96, 96, 96), sw=2, font='power', size=88, track=0.03):
    W, H = im.size; cx, cy = W / 2, H / 2
    box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
    base = im.convert('RGBA')
    # soft shadow
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sm = rrect_mask(W, H, (box[0], box[1] + 10, box[2], box[3] + 10), r)
    sh.putalpha(sm.point(lambda v: int(v * 0.35))); sh = sh.filter(ImageFilter.GaussianBlur(22)); base.alpha_composite(sh)
    # fill + stroke
    outer = rrect_mask(W, H, box, r); inner = rrect_mask(W, H, (box[0] + sw, box[1] + sw, box[2] - sw, box[3] - sw), r - sw)
    st = Image.new('RGBA', (W, H), stroke + (0,)); st.putalpha(outer); base.alpha_composite(st)
    fl = Image.new('RGBA', (W, H), fill + (0,)); fl.putalpha(inner.point(lambda v: int(v * fop))); base.alpha_composite(fl)
    d = ImageDraw.Draw(base)
    fl_ = ImageFont.truetype(FONT['pn_semi'], 25); fm = ImageFont.truetype(FONT[font], size)
    lab = 'USE CODE'; wl = text_w(fl_, lab, 0.35)
    draw_tracked(d, (cx - wl / 2, box[1] + 30), lab, fl_, (175, 175, 175, 255), 0.35)
    wm = text_w(fm, 'TRYIMMUFIX', track)
    asc, desc = fm.getmetrics()
    draw_tracked(d, (cx - wm / 2, box[1] + 70), 'TRYIMMUFIX', fm, (255, 255, 255, 255), track)
    return base.convert('RGB')

plan = json.loads(sys.argv[1]); tiles = []
for key, spec in plan.items():
    im = graded_frame(key, spec['t'])
    tiles.append(card(im, font=spec.get('font', 'power'), size=spec.get('size', 88)).resize((540, 960), Image.LANCZOS))
S = Image.new('RGB', (540 * len(tiles), 960))
for i, t in enumerate(tiles): S.paste(t, (540 * i, 0))
S.save('mock_card.png'); print('ok')
