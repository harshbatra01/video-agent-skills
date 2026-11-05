"""QA sheet for the AE overlay renders: VLC grabs every 6th frame of each .mov, picks frames at given fractions,
composites them over a mid-grey checker so dark backdrops and white type both show. usage: python qa_gfx.py out.png frac1 [frac2] name..."""
import os, sys, glob, re, shutil, subprocess
from PIL import Image, ImageDraw
VLC = os.environ.get('VLC_PATH') or next((p for p in (r'C:\Program Files\VideoLAN\VLC\vlc.exe', '/Applications/VLC.app/Contents/MacOS/VLC') if os.path.exists(p)), r'C:\Program Files\VideoLAN\VLC\vlc.exe')
D = os.environ.get('GFXDIR', r"C:\VISION\IMMUFIX\repair\ENCODED RUSHES\Motion graphics\gfx_v2")
TMP = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'qa_tmp'))
args = sys.argv[1:]; out = args.pop(0)
fracs = []
while args and re.match(r'^0?\.\d+$|^1(\.0)?$', args[0]): fracs.append(float(args.pop(0)))
names = args or sorted(os.path.splitext(os.path.basename(f))[0] for f in glob.glob(D + r'\*.mov'))
W = 170; H = round(W * 16 / 9); tiles = []
for n in names:
    d = os.path.join(TMP, n); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    subprocess.run([VLC, '--intf', 'dummy', '--dummy-quiet', '--vout', 'dummy', '--no-audio', '--avcodec-hw=none', '--no-drop-late-frames', '--no-skip-frames',
                    '--video-filter=scene', '--scene-format=png', '--scene-ratio=6', '--scene-prefix=g_', '--scene-width=340', '--scene-path=' + d, '--play-and-exit',
                    os.path.join(D, n + '.mov'), 'vlc://quit'], capture_output=True, timeout=300)
    fs = sorted(glob.glob(d + r'\g_*.png'), key=lambda f: int(re.search(r'g_(\d+)', f).group(1)))
    for fr in fracs:
        bg = Image.new('RGB', (W, H), (96, 104, 112)); dr = ImageDraw.Draw(bg)
        for y in range(0, H, 20):
            for x in range(0, W, 20):
                if (x // 20 + y // 20) % 2: dr.rectangle([x, y, x + 19, y + 19], fill=(120, 128, 136))
        if fs:
            im = Image.open(fs[min(len(fs) - 1, int(fr * (len(fs) - 1)))])
            im = im.convert('RGBA').resize((W, H))
            bg.paste(im, (0, 0), im if im.mode == 'RGBA' else None)
        ImageDraw.Draw(bg).text((3, 2), '%s %.2f' % (n, fr), fill=(255, 255, 0))
        tiles.append(bg)
cols = 8; rows = (len(tiles) + cols - 1) // cols
S = Image.new('RGB', (cols * W, rows * H), (0, 0, 0))
for i, t in enumerate(tiles): S.paste(t, ((i % cols) * W, (i // cols) * H))
S.save(out); print(out, S.size, len(tiles))
