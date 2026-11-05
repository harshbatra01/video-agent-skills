"""Calmer grade for the website still: v1 (ad look) -> less orange skin / yellow foliage, slightly cooler, softer contrast.
Pouch keeps most of its brand colour. Writes '... website still v2' .jpg/.png (v1 kept) + a v1|v2 preview."""
import numpy as np, colorsys
from PIL import Image, ImageFilter
D = r'C:/VISION/IMMUFIX/repair/Renders/Website stills/'
a = np.asarray(Image.open(D + 'Paula holding Immufix - website still.png').convert('RGB')).astype(np.float32) / 255
H, W = a.shape[:2]


def hsv(x):
    mx = x.max(-1); mn = x.min(-1); dlt = mx - mn + 1e-6
    r, g, b = x[..., 0], x[..., 1], x[..., 2]
    h = np.where(mx == r, ((g - b) / dlt) % 6, np.where(mx == g, (b - r) / dlt + 2, (r - g) / dlt + 4)) * 60
    return h, dlt / (mx + 1e-6), mx


y = (0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2])[..., None]
h, s, v = hsv(a)
# saturation: global 0.80, oranges/yellows (skin, autumn leaves, foliage) down to about 0.62 overall
band = np.exp(-((((h - 30) + 180) % 360 - 180) / 22.0) ** 2)          # centred on orange-yellow 30 deg
k = 0.80 * (1 - 0.22 * band)
b = y + (a - y) * k[..., None]
# white balance: a touch cooler and less green (the white tee stays white)
b = b * np.array([0.975, 0.985, 1.03], np.float32)
# softer contrast: lift the darkest tones a little, gentle roll-off at the top
b = 0.018 + b * 0.965
b = b - 0.06 * (b - 0.5) * (1 - np.abs(2 * b - 1))                    # flattens the mid S-curve slightly
b = np.clip(b, 0, 1)
# keep the pouch closer to its real colours (feathered box over the pouch)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
def box(x0, x1, y0, y1, f):
    return np.clip(np.minimum.reduce([(xx - x0) / f, (x1 - xx) / f, (yy - y0) / f, (y1 - yy) / f]), 0, 1)
m = box(215, 950, 980, 1965, 40)[..., None] * 0.55
out = b * (1 - m) + (a * np.array([0.985, 0.99, 1.015], np.float32)) * m
im = Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8))
base = D + 'Paula holding Immufix - website still v2'
im.save(base + '.jpg', quality=95, subsampling=0); im.save(base + '.png')
# report the same patches before / after
P = {'forehead': (1425, 500), 'cheek': (1560, 760), 'neck': (1475, 1075), 'forearm (shadow)': (1500, 2300), 'shirt': (1750, 1500),
     'foliage': (250, 700), 'ground leaves': (400, 2850), 'pouch navy': (750, 1500), 'IMMUFIX gold': (550, 1590)}
A2 = np.asarray(im).astype(np.float32) / 255
for kname, (x, yv) in P.items():
    p1 = a[yv - 20:yv + 20, x - 20:x + 20].reshape(-1, 3).mean(0); p2 = A2[yv - 20:yv + 20, x - 20:x + 20].reshape(-1, 3).mean(0)
    h1, s1, _ = colorsys.rgb_to_hsv(*p1); h2, s2, _ = colorsys.rgb_to_hsv(*p2)
    print('%-17s v1 rgb %3d %3d %3d sat %.2f  ->  v2 rgb %3d %3d %3d sat %.2f' % (kname, *(p1 * 255), s1, *(p2 * 255), s2))
v1 = Image.fromarray((a * 255).astype(np.uint8)).resize((400, 500)); v2 = im.resize((400, 500))
S = Image.new('RGB', (808, 500), (90, 90, 90)); S.paste(v1, (0, 0)); S.paste(v2, (408, 0)); S.save('v1_v2.png')
print('saved', base)
