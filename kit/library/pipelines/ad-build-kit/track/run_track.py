"""Track the whiteboard through every visible 3 things piece; writes track_tt.json {frame_index: [p0..p5, ncc]} and a QA sheet."""
import json, os, glob, re, sys
import numpy as np
from PIL import Image, ImageDraw
from tracker import Template, load_gray, pyramid, global_init, mat
from board_def import REF_FRAME, BOARD, LINES, box_corners, region_mask

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
ref = load_gray(REF_FRAME)
T = Template(ref, region_mask(ref.shape))
jobs = json.load(open('tt_jobs.json'))
only = set(int(x) for x in sys.argv[1].split(',')) if len(sys.argv) > 1 else None
out = json.load(open('track_tt.json')) if os.path.exists('track_tt.json') else {}
for j in jobs:
    if only is not None and j['piece'] not in only: continue
    d = 'tt_frames/p%d_%d' % (j['piece'], j['f0'])
    fs = sorted(glob.glob(d + '/f_*.tif'), key=lambda f: int(re.search(r'f_(\d+)', f).group(1)))
    if not fs: print('no frames', d); continue
    p = None
    for i, f in enumerate(fs):
        k = int(re.search(r'f_(\d+)', f).group(1))
        img = load_gray(f); P = pyramid(img, 3)
        if p is None:
            p0, s, ang, sc = global_init(ref, BOARD, img)
            p, ncc = T.align(P, p0, iters=(40, 20, 10))
            print('piece %d start f%d: init ncc %.2f ang %.0f sc %.2f -> ncc %.3f' % (j['piece'], k, s, ang, sc, ncc), flush=True)
        else:
            p, ncc = T.align(P, p)
        out[str(k)] = [float(x) for x in p] + [ncc, j['piece']]
    json.dump(out, open('track_tt.json', 'w'))
    nc = [out[str(int(re.search(r'f_(\d+)', f).group(1)))][6] for f in fs]
    print('piece %d: %d frames, ncc min %.3f mean %.3f' % (j['piece'], len(fs), min(nc), sum(nc) / len(nc)), flush=True)

# QA sheet: first / middle / last frame of each piece with the line boxes warped in
tiles = []
for j in jobs:
    if only is not None and j['piece'] not in only: continue
    d = 'tt_frames/p%d_%d' % (j['piece'], j['f0'])
    fs = sorted(glob.glob(d + '/f_*.tif'), key=lambda f: int(re.search(r'f_(\d+)', f).group(1)))
    if not fs: continue
    for f in (fs[0], fs[len(fs) // 2], fs[-1]):
        k = int(re.search(r'f_(\d+)', f).group(1)); r = out.get(str(k))
        if r is None: continue
        im = Image.open(f).convert('RGB'); dr = ImageDraw.Draw(im); M = mat(np.array(r[:6]))
        for name, b in LINES.items():
            c = box_corners(*b); c = (M[:2, :2] @ c.T).T + M[:2, 2]
            dr.polygon([tuple(x) for x in c], outline=(0, 255, 0))
        q = np.array(BOARD, float); q = (M[:2, :2] @ q.T).T + M[:2, 2]
        dr.polygon([tuple(x) for x in q], outline=(255, 0, 0))
        cx, cy = q.mean(0)
        tile = im.crop((int(cx) - 260, int(cy) - 300, int(cx) + 260, int(cy) + 300)).resize((260, 300))
        ImageDraw.Draw(tile).text((3, 3), 'p%d f%d %.2f' % (j['piece'], k, r[6]), fill=(255, 255, 0))
        tiles.append(tile)
cols = 12; rows = (len(tiles) + cols - 1) // cols
S = Image.new('RGB', (cols * 260, max(1, rows) * 300))
for i, t in enumerate(tiles): S.paste(t, ((i % cols) * 260, (i // cols) * 300))
S.save('track_qa.png'); print('track_qa.png', S.size)
