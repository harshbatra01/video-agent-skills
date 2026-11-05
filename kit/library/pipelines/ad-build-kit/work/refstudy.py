"""Study a reference edit: grab every Nth frame (no drops), detect cuts, write timestamped contact sheets."""
import subprocess, os, glob, re, sys, math
import numpy as np
from PIL import Image, ImageDraw
VLC = os.environ.get('VLC_PATH') or next((p for p in (r'C:\Program Files\VideoLAN\VLC\vlc.exe', '/Applications/VLC.app/Contents/MacOS/VLC') if os.path.exists(p)), r'C:\Program Files\VideoLAN\VLC\vlc.exe')
HERE = os.path.dirname(os.path.abspath(__file__))


def grab_all(src, out, every, rate=1.0):
    os.makedirs(out, exist_ok=True)
    for f in glob.glob(os.path.join(out, 'g_*.png')): os.remove(f)
    cmd = [VLC, '--intf', 'dummy', '--dummy-quiet', '--vout', 'dummy', '--no-audio', '--avcodec-hw=none',
           '--no-drop-late-frames', '--no-skip-frames', '--rate=%g' % rate, '--video-filter=scene', '--scene-format=png',
           '--scene-ratio=%d' % every, '--scene-prefix=g_', '--scene-width=270', '--scene-path=' + out, '--play-and-exit', src, 'vlc://quit']
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=1800)
    return sorted(glob.glob(os.path.join(out, 'g_*.png')), key=lambda f: int(re.search(r'g_(\d+)', f).group(1)))


def num(f): return int(re.search(r'g_(\d+)', os.path.basename(f)).group(1))


def analyse(out, fps):
    fs = sorted(glob.glob(os.path.join(out, 'g_*.png')), key=num)
    arr = [np.asarray(Image.open(f).convert('L').resize((54, 96)), np.float32) for f in fs]
    diffs = [0.0] + [float(np.mean(np.abs(a - b))) for a, b in zip(arr, arr[1:])]
    return fs, diffs


def sheet(fs, diffs, fps, out_png, cols=10, tw=135, mark=12.0, t_from=0, t_to=1e9):
    sel = [(f, d) for f, d in zip(fs, diffs) if t_from <= (num(f) - 1) / fps <= t_to]
    im0 = Image.open(sel[0][0]); th = round(tw * im0.height / im0.width)
    rows = math.ceil(len(sel) / cols)
    S = Image.new('RGB', (cols * tw, rows * (th + 14)), (10, 10, 10)); d = ImageDraw.Draw(S)
    for i, (f, df) in enumerate(sel):
        x, y = (i % cols) * tw, (i // cols) * (th + 14)
        S.paste(Image.open(f).convert('RGB').resize((tw, th)), (x, y + 14))
        d.text((x + 2, y + 1), '%.2f%s' % ((num(f) - 1) / fps, ' CUT' if df > mark else ''), fill=(255, 80, 80) if df > mark else (255, 255, 0))
    S.save(out_png)


if __name__ == '__main__':
    src, out, every, fps = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4])
    if len(sys.argv) < 6 or sys.argv[5] != 'skipgrab':
        fs = grab_all(src, out, every)
        print('grabbed', len(fs))
    fs, diffs = analyse(out, fps)
    cuts = [(num(f) - 1) / fps for f, d in zip(fs, diffs) if d > 12.0]
    print('frames', len(fs), 'cut-like jumps (>12):', len(cuts))
    print(' '.join('%.2f' % c for c in cuts))
    dur = (num(fs[-1]) - 1) / fps
    for a in range(0, int(dur) + 1, 10):
        sheet(fs, diffs, fps, os.path.join(HERE, 'refsheet_%02d.png' % a), t_from=a, t_to=a + 10 - 1e-6)
    print('sheets written')
