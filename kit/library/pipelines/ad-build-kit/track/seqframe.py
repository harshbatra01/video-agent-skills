"""Rebuild a pre-zoom, pre-grade sequence frame of an ad from its V1 A-roll piece (VLC grab + the piece's Motion).
usage: python seqframe.py ad_key out.png t1 t2 ...   (sheet of 270x480 tiles)"""
import sys, os, re, json, subprocess, glob, tempfile, shutil
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'prproj'))
VLC = os.environ.get('VLC_PATH') or next((p for p in (r'C:\Program Files\VideoLAN\VLC\vlc.exe', '/Applications/VLC.app/Contents/MacOS/VLC') if os.path.exists(p)), r'C:\Program Files\VideoLAN\VLC\vlc.exe')
HERE = os.path.dirname(os.path.abspath(__file__))
PIECES = os.path.join(HERE, 'pieces.json')

def load_pieces():
    if os.path.exists(PIECES): return json.load(open(PIECES))
    os.chdir(os.path.join(HERE, '..', 'prproj'))
    from build_project import Doc, TPS, for_claude_sequences, video_tracks, track_items
    from build_v4 import motion_of
    from build_ext import item_times
    doc = Doc('v4imp.xml'); out = {}
    for n, s in for_claude_sequences(doc):
        key = s.attrib['ObjectUID'][:8]; lst = []
        for it in track_items(doc, video_tracks(doc, s)[0]):
            i = it.attrib['ObjectID']; st, en, tin, vc = item_times(doc, i)
            t = doc.raw(i); sc = re.search(r'<SubClip ObjectRef="(\d+)"', t).group(1)
            ip = re.search(r'<InPoint>(-?\d+)<', doc.raw(re.search(r'<Clip ObjectRef="(\d+)"', doc.raw(sc)).group(1)))
            m = motion_of(doc, i); px, py = [float(v) for v in m['Position'].split(':')]
            path = None
            nm = re.search(r'<Name>([^<]*)</Name>', doc.raw(sc)).group(1)
            lst.append(dict(s=st / TPS, e=en / TPS, src=int(ip.group(1)) / TPS, px=px, py=py, scale=float(m['Scale']), name=nm))
        out[key] = lst
    os.chdir(HERE); json.dump(out, open(PIECES, 'w'), indent=0)
    return out

MEDIA = {'f233433f': r'C:\VISION\IMMUFIX\repair\ENCODED RUSHES\Cleaned\A003_09181253_C118-esv2-50p-bg-10p-music-10p.mp4',
         '974102f7': r'C:\VISION\IMMUFIX\repair\ENCODED RUSHES\Cleaned\A003_09181227_C117-esv2-50p-bg-10p-music-10p.mp4'}

def piece_at(pieces, key, t):
    for p in pieces[key]:
        if p['s'] - 1e-6 <= t < p['e'] - 1e-6: return p
    return pieces[key][-1]

def grab_src(path, src_t, width=1512):
    d = tempfile.mkdtemp(dir=HERE)
    subprocess.run([VLC, '--intf', 'dummy', '--dummy-quiet', '--vout', 'dummy', '--no-audio', '--avcodec-hw=none', '--start-time=%.3f' % src_t, '--stop-time=%.3f' % (src_t + 0.2),
                    '--video-filter=scene', '--scene-format=png', '--scene-ratio=1', '--scene-prefix=f_', '--scene-width=%d' % width, '--scene-path=' + d, '--play-and-exit', path, 'vlc://quit'],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    fs = sorted(glob.glob(os.path.join(d, 'f_*.png')))
    im = Image.open(fs[0]).convert('RGB') if fs else None
    shutil.rmtree(d, ignore_errors=True)
    return im

def to_seq(im, p, out_w=1080):
    """place a source frame (any size, full 6048x3408 field) into the 1080x1920 sequence frame with the piece's Motion"""
    sw, sh = 6048, 3408; k = out_w / 1080.0
    sc = p['scale'] / 100.0
    W, H = int(round(sw * sc * k)), int(round(sh * sc * k))
    big = im.resize((W, H), Image.BILINEAR)
    x0 = p['px'] * 1080 * k - W / 2; y0 = p['py'] * 1920 * k - H / 2
    out = Image.new('RGB', (out_w, int(round(1920 * k))))
    out.paste(big, (int(round(x0)), int(round(y0))))
    return out

if __name__ == '__main__':
    key, out = sys.argv[1], sys.argv[2]; ts = [float(x) for x in sys.argv[3:]]
    pieces = load_pieces(); tiles = []
    for t in ts:
        p = piece_at(pieces, key, t); st = p['src'] + (t - p['s'])
        im = grab_src(MEDIA[key], st)
        tile = to_seq(im, p, 270)
        ImageDraw.Draw(tile).text((4, 4), '%.2f' % t, fill=(255, 255, 0))
        tiles.append(tile)
    cols = min(len(tiles), 8); rows = (len(tiles) + cols - 1) // cols
    S = Image.new('RGB', (cols * 270, rows * 480))
    for i, tl in enumerate(tiles): S.paste(tl, ((i % cols) * 270, (i // cols) * 480))
    S.save(out); print(out, S.size)
