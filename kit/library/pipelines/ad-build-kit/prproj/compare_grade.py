"""Before (V3 render frame) / after (Premiere export) sheet + stats for the colour pass.
usage: python compare_grade.py out.png pairs.json"""
import sys, json, glob, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
CF = 'C:/VISION/IMMUFIX/repair/ENCODED RUSHES/_claude_check_frames/'
pairs = json.load(open(sys.argv[2]))
W, H = 270, 480
font = ImageFont.truetype('arial.ttf', 14)
cols = 6; rows = (len(pairs) * 2 + cols - 1) // cols
S = Image.new('RGB', (cols * W, rows * (H + 18)), (25, 25, 25)); d = ImageDraw.Draw(S)
def stats(im):
    a = np.asarray(im.convert('RGB').resize((540, 960))).astype(np.float32) / 255.0
    y = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    mx, mn = a.max(axis=2), a.min(axis=2)
    return 'p1 %.2f p50 %.2f p99 %.2f clip %.1f%% sat %.2f' % (np.percentile(y, 1), np.percentile(y, 50), np.percentile(y, 99), (y > 0.97).mean() * 100, ((mx - mn) / (mx + 1e-6)).mean())
k = 0
for label, before, after in pairs:
    b = Image.open(glob.glob('v3frames/*/' + before + '.png')[0]); a = Image.open(CF + after)
    for tag, im in (('V3 ' + label, b), ('v10 ' + label, a)):
        x, y = (k % cols) * W, (k // cols) * (H + 18)
        S.paste(im.convert('RGB').resize((W, H)), (x, y + 18)); d.text((x + 3, y + 2), tag, fill=(255, 220, 0), font=font)
        print('%-26s %s' % (tag, stats(im))); k += 1
S.save(sys.argv[1]); print(S.size)
