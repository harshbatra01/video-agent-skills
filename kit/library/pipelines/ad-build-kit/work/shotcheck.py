"""Contact sheets of B-roll source ranges as they appear in the vertical crop (graded with the calibrated model),
with a sharpness score on the subject area, to pick replacement in-points for shots the boss flagged."""
import os, sys, json, pickle, glob, re, subprocess, math
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from model import *
HERE = os.path.dirname(os.path.abspath(__file__))
M = pickle.load(open(os.path.join(HERE, 'calib', 'model_v1.pkl'), 'rb'))
VLC = os.environ.get('VLC_PATH') or next((p for p in (r'C:\Program Files\VideoLAN\VLC\vlc.exe', '/Applications/VLC.app/Contents/MacOS/VLC') if os.path.exists(p)), r'C:\Program Files\VideoLAN\VLC\vlc.exe')
BR = r'C:\VISION\IMMUFIX\repair\ENCODED RUSHES\B roll'


def grab_range(clip, t0, t1, every, out):
    os.makedirs(out, exist_ok=True)
    for f in glob.glob(os.path.join(out, 'g_*.png')): os.remove(f)
    cmd = [VLC, '--intf', 'dummy', '--dummy-quiet', '--vout', 'dummy', '--no-audio', '--avcodec-hw=none', '--no-drop-late-frames', '--no-skip-frames',
           '--rate=0.5', '--video-filter=scene', '--scene-format=png', '--scene-ratio=%d' % every, '--scene-prefix=g_', '--scene-path=' + out,
           '--start-time=%.3f' % t0, '--stop-time=%.3f' % t1, '--play-and-exit', os.path.join(BR, clip + '.mp4'), 'vlc://quit']
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=1800)
    return sorted(glob.glob(os.path.join(out, 'g_*.png')), key=lambda f: int(re.search(r'g_(\d+)', f).group(1)))


def lap(a):
    return float((a[1:-1, 1:-1] * 4 - a[:-2, 1:-1] - a[2:, 1:-1] - a[1:-1, :-2] - a[1:-1, 2:]).var())


def sheet(clip, t0, t1, every, cx, scale=57, cols=8, tw=180, box=(0.25, 0.1, 0.75, 0.6), name=None):
    out = os.path.join(HERE, 'shotcheck', clip + '_%d' % int(t0))
    fs = grab_range(clip, t0, t1, every, out)
    tiles = []
    for k, f in enumerate(fs):
        t = t0 + k * every / 25.0
        im = Image.open(f).convert('RGB'); sy = im.height / 3408.0
        s = scale / 100.0; w = 1080 / s; h = 1920 / s; X = cx * 6048
        crop = im.crop((int(X - w / 2), int((1704 - h / 2) * sy), int(X + w / 2), int((1704 + h / 2) * sy)))
        g = np.asarray(crop.convert('L').resize((540, 960)), np.float32)
        bx = [int(v) for v in (box[0] * 540, box[1] * 960, box[2] * 540, box[3] * 960)]
        sharp = lap(g[bx[1]:bx[3], bx[0]:bx[2]])
        small = crop.resize((tw, round(tw * 16 / 9)), Image.BOX)
        graded = Image.fromarray((M(np.asarray(small).astype(np.float64) / 255, 0.0) * 255).astype(np.uint8))
        ImageDraw.Draw(graded).text((3, 3), '%.1fs  sh %.0f' % (t, sharp), fill=(255, 255, 0))
        tiles.append(graded)
    th = tiles[0].height; rows = math.ceil(len(tiles) / cols)
    S = Image.new('RGB', (cols * tw, rows * th), (0, 0, 0))
    for i, im in enumerate(tiles): S.paste(im, ((i % cols) * tw, (i // cols) * th))
    p = os.path.join(HERE, 'shotcheck_%s.png' % (name or clip)); S.save(p); return p


if __name__ == '__main__':
    jobs = json.loads(sys.argv[1])
    for j in jobs:
        print(sheet(**j), flush=True)
