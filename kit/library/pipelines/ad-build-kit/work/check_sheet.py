"""Combine Premiere-exported check frames into small sheets.
usage: python check_sheet.py out.png [--crop y0 y1] [--w 270] [--cols 6] name1 name2 ...   (names without .png, from _claude_check_frames)"""
import sys, os
from PIL import Image, ImageDraw, ImageFont
D = r'C:\VISION\IMMUFIX\repair\ENCODED RUSHES\_claude_check_frames'
FONT = ImageFont.truetype(r'C:\Users\Kanishk\AppData\Local\Microsoft\Windows\Fonts\Proxima Nova Semibold.ttf', 15)
a = sys.argv[1:]; out = a.pop(0); crop = None; W = 270; cols = 6
while a and a[0].startswith('--'):
    k = a.pop(0)
    if k == '--crop': crop = (int(a.pop(0)), int(a.pop(0)))
    elif k == '--w': W = int(a.pop(0))
    elif k == '--cols': cols = int(a.pop(0))
tiles = []
for n in a:
    p = os.path.join(D, n + '.png')
    if not os.path.exists(p): print('missing', n); continue
    im = Image.open(p).convert('RGB')
    if crop: im = im.crop((0, crop[0], im.width, crop[1]))
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    ImageDraw.Draw(im).text((4, 2), n, fill=(255, 255, 0), font=FONT, stroke_width=2, stroke_fill=(0, 0, 0))
    tiles.append(im)
H = max(t.height for t in tiles); rows = (len(tiles) + cols - 1) // cols
S = Image.new('RGB', (cols * W, rows * H), (20, 20, 20))
for i, t in enumerate(tiles): S.paste(t, ((i % cols) * W, (i // cols) * H))
S.save(out); print(out, S.size)
