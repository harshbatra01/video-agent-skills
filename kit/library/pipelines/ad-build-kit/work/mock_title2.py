"""Title v2 mockup: bigger text on a smoked plate (linear-light blend like Premiere), on graded frames of every ad."""
import os, sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mock_titles import graded_frame, zoom, FONT
UF = r'C:\Users\Kanishk\AppData\Local\Microsoft\Windows\Fonts'
FONT['pn_reg'] = UF + r'\Proxima Nova Regular.ttf'
HERE = os.path.dirname(os.path.abspath(__file__))


def tw(font, s, track):
    return sum(font.getlength(c) for c in s) + track / 1000 * font.size * (len(s) - 1)


def srgb2lin(a): return np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
def lin2srgb(a): return np.where(a <= 0.0031308, a * 12.92, 1.055 * np.power(np.clip(a, 0, None), 1 / 2.4) - 0.055)


def layout(sub, S):
    fn = ImageFont.truetype(FONT['pn_semi'], S['name_px']); fs = ImageFont.truetype(FONT['pn_reg'], S['sub_px'])
    wn = tw(fn, 'PAULA RADCLIFFE', S['name_trk']); ws = tw(fs, sub, S['sub_trk'])
    asc_n = fn.getmetrics()[0]; asc_s = fs.getmetrics()[0]
    cap_n = fn.getbbox('H')[3] - fn.getbbox('H')[1]; cap_s = fs.getbbox('H')[3] - fs.getbbox('H')[1]
    pw = max(wn, ws) + S['pad_l'] + S['pad_r']
    # vertical: pad, name caps, gap, line, gap, subtitle caps (+ descender room), pad
    base_n = S['pad_t'] + cap_n
    line_y = base_n + S['gap1']
    base_s = line_y + S['line_h'] + S['gap2'] + cap_s
    ph = base_s + S['pad_b']
    return dict(fn=fn, fs=fs, wn=wn, ws=ws, asc_n=asc_n, asc_s=asc_s, pw=pw, ph=ph, base_n=base_n, line_y=line_y, base_s=base_s)


def render(im, sub, S, x0, y0):
    L = layout(sub, S)
    W, H = im.size
    # plate mask (supersampled rounded rect)
    ss = 4
    m = Image.new('L', (W * ss, H * ss), 0)
    ImageDraw.Draw(m).rounded_rectangle([x0 * ss, y0 * ss, (x0 + L['pw']) * ss, (y0 + L['ph']) * ss], radius=S['radius'] * ss, fill=255)
    m = np.asarray(m.resize((W, H), Image.LANCZOS)).astype(np.float64)[..., None] / 255 * S['plate_op']
    bg = srgb2lin(np.asarray(im.convert('RGB')).astype(np.float64) / 255)
    plate = srgb2lin(np.array(S['plate_rgb']) / 255.0)
    out = bg * (1 - m) + plate * m
    img = Image.fromarray((lin2srgb(out) * 255).clip(0, 255).astype(np.uint8)).convert('RGBA')
    d = ImageDraw.Draw(img)
    x = x0 + S['pad_l']
    def draw_tracked(y_base, s, f, fill, trk, asc):
        xx = x
        for ch in s:
            d.text((xx, y0 + y_base - asc), ch, font=f, fill=fill); xx += f.getlength(ch) + trk / 1000 * f.size
    draw_tracked(L['base_n'], 'PAULA RADCLIFFE', L['fn'], (255, 255, 255, 255), S['name_trk'], L['asc_n'])
    d.rectangle([x, y0 + L['line_y'], x + S['line_w'], y0 + L['line_y'] + S['line_h'] - 1], fill=S['line_rgb'] + (255,))
    draw_tracked(L['base_s'], sub, L['fs'], S['sub_rgb'] + (255,), S['sub_trk'], L['asc_s'])
    return img.convert('RGB'), L


STYLE = dict(name_px=34, name_trk=60, sub_px=26, sub_trk=15, pad_l=20, pad_r=22, pad_t=18, pad_b=19, gap1=13, gap2=13, line_w=42, line_h=2,
             radius=12, plate_rgb=(12, 12, 12), plate_op=0.88, line_rgb=(255, 255, 255), sub_rgb=(226, 226, 226))

if __name__ == '__main__':
    plan = json.loads(sys.argv[1]); x0 = int(sys.argv[2]) if len(sys.argv) > 2 else 40; y0 = int(sys.argv[3]) if len(sys.argv) > 3 else 196
    tiles = []
    for key, spec in plan.items():
        im = graded_frame(key, spec['t'])
        if spec.get('zoom'): im = zoom(im, spec['zoom'])
        out, L = render(im, spec['sub'], STYLE, x0, y0)
        print(key, 'plate %.0f x %.0f px, right edge x=%.0f, bottom y=%.0f' % (L['pw'], L['ph'], x0 + L['pw'], y0 + L['ph']))
        tiles.append(out.resize((540, 960), Image.LANCZOS))
    S = Image.new('RGB', (540 * len(tiles), 960))
    for i, t in enumerate(tiles): S.paste(t, (540 * i, 0))
    S.save(os.path.join(HERE, 'mock_title2.png'))
