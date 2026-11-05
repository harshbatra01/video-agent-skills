"""Contact sheets of the exported clips: one per group and orientation (middle frame, name + length under each)."""
import os, glob, sys
sys.path.insert(0, os.path.join((os.environ.get('PAE_SCRIPTS') or os.path.expanduser('~/.claude/skills/premiere-ae-editing/scripts')), 'media'))
from frames import Grabber, info
from PIL import Image, ImageDraw, ImageFont
OUT = r'C:/VISION/IMMUFIX/repair/Renders/Paula clips for <recipient>/'
f = ImageFont.truetype('arialbd.ttf', 15)
made = []
for group in ('Paula', 'Product'):
    for orient, (TW, TH, cols) in (('Landscape 4K', (384, 216, 4)), ('Vertical 1080x1920', (180, 320, 7))):
        files = sorted(glob.glob(OUT + '%s/%s/*.mp4' % (group, orient)))
        if not files: continue
        rows = (len(files) + cols - 1) // cols; LH = 22
        S = Image.new('RGB', (cols * TW, rows * (TH + LH)), (18, 18, 18)); d = ImageDraw.Draw(S)
        for i, p in enumerate(files):
            m = info(p); g = Grabber(p); im = g.at(m['duration'] / 2).convert('RGB').resize((TW, TH)); g.close()
            x, y = (i % cols) * TW, (i // cols) * (TH + LH)
            S.paste(im, (x, y)); lab = '%s (%.0fs)' % (os.path.splitext(os.path.basename(p))[0], m['duration'])
            while d.textlength(lab, font=f) > TW - 6 and len(lab) > 8: lab = lab[:-5] + '...'
            d.text((x + 4, y + TH + 3), lab, fill=(235, 235, 235), font=f)
        dst = OUT + '%s/%s/_contact sheet.jpg' % (group, orient); S.save(dst, quality=90); made.append(dst)
        print(dst, S.size, len(files), 'clips')
