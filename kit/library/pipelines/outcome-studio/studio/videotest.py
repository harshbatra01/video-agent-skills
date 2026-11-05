"""videotest: render the animated version of a few formats (1080x1920 MP4) and a frame strip of each to check motion.

python videotest.py [fmt,fmt]
"""
import os, sys, time, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ocdata as od, formats as fm
from render import Studio, FFMPEG
from PIL import Image

OUT = os.path.join(od.ROOT, 'out', '_videotest')


def strip(mp4, out, n=6, w=216):
    """n frames across the clip side by side (one image to check the motion)"""
    import av
    c = av.open(mp4); st = c.streams.video[0]; frames = [f.to_image() for f in c.decode(st)]; c.close()
    pick = [frames[int(i * (len(frames) - 1) / (n - 1))] for i in range(n)]
    h = int(pick[0].height * w / pick[0].width); sh = Image.new('RGB', (n * (w + 4), h), (20, 20, 20))
    for i, im in enumerate(pick): sh.paste(im.resize((w, h)), (i * (w + 4), 0))
    sh.save(out, quality=85); return out, len(frames)


if __name__ == '__main__':
    only = set(sys.argv[1].split(',')) if len(sys.argv) > 1 else None
    ms = od.markets()
    bdo = next(m for m in ms if m['kind'] == 'winner' and 'Ballon' in m['title'])
    city = next(m for m in ms if m['kind'] == 'match3' and 'Manchester City' in m['title'])
    posts = [fm.swing(bdo, ['Harry Kane', 'Lamine Yamal'], days=9),
             fm.matchday(ms, 'UEFA Champions League', day=time.strftime('%Y%m%d', time.gmtime(time.time() + 86400))),
             fm.pick(city), fm.ladder_ipo(ms, 'Anthropic')]
    os.makedirs(OUT, exist_ok=True)
    with Studio(fm.brand()) as st:
        for p in posts:
            v = p.get('video')
            if not v or (only and v['fmt'] not in only): continue
            f = os.path.join(OUT, '%s.mp4' % p['id']); t0 = time.time()
            info = st.video(v, f, (1080, 1920))
            s, n = strip(f, f.replace('.mp4', '_strip.jpg'))
            print('%-28s %4.1fs video, %d frames, rendered in %.1fs -> %s' % (p['id'], info['dur'], n, time.time() - t0, os.path.basename(s)))
