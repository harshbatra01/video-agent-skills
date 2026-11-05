"""videotest3: the newer motion formats (look kit, motion_more.js) on today's data.

python videotest3.py sheet [name ...]     one contact sheet per format (frames across the timeline) for a quick layout check
python videotest3.py video [name ...]     full renders with the sound baked in, plus a strip
Names: countdown quizclock forecast race sim100 linestory
"""
import io, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ocdata as od, formats as fm, motion as mo
from render import Studio
from videotest import strip

OUT = os.path.join(od.ROOT, 'out', '_selftest')


def posts(ms):
    return {
        'countdown': lambda: mo.countdown(ms, 'Q199', n=8),
        'quizclock': lambda: mo.quizclock(ms, ['Q410', 'Q407', 'Q411', 'Q405']),
        'forecast': lambda: mo.forecast(ms),
        'race': lambda: mo.race(ms, 'Q198', n=6),
        'sim100': lambda: mo.sim100(ms, 'Q407'),
        'linestory': lambda: mo.linestory(ms, 'Q289', ['No change', 'Hike'], names=['Hold', 'Hike'], days=24, title='The money flipped on the Fed',
                                          kicker='OUTCOME // FED DECISION, 28 OCT', hero_label='CHANCE THE FED HOLDS RATES',
                                          next_line='NEXT: US INFLATION, 14 OCT 12:30 UTC'),
    }


def sheet(st, v, out, n=9, w=240, times=None):
    from PIL import Image, ImageDraw
    info = st.show(v, (1080, 1920)) or {}
    dur = info.get('dur') or 10
    times = times or [0.5 + k * (dur - 0.5) / (n - 1) for k in range(n)]
    h = int(w * 1920 / 1080); sh = Image.new('RGB', (len(times) * (w + 6), h + 24), (30, 30, 30)); dr = ImageDraw.Draw(sh)
    for i, t in enumerate(times):
        st.js('window.renderAt(%f)' % t)
        im = Image.open(io.BytesIO(st._shot('jpeg', 85))).convert('RGB').resize((w, h))
        sh.paste(im, (i * (w + 6), 24)); dr.text((i * (w + 6) + 4, 4), '%.1fs' % t, fill=(255, 255, 0))
    sh.save(out, quality=85)
    return dur


if __name__ == '__main__':
    a = sys.argv[1:] or ['sheet']
    ms = od.markets(); P = posts(ms)
    names = a[1:] or list(P)
    with Studio(fm.brand()) as st:
        for nm in names:
            t0 = time.time(); p = P[nm]()
            if not p: print(nm, 'no data'); continue
            if a[0] == 'sheet':
                f = os.path.join(OUT, '_sheet_%s.jpg' % nm); d = sheet(st, p['video'], f); print(nm, 'dur %.1f' % d, f, '%.0fs' % (time.time() - t0))
            else:
                f = os.path.join(OUT, p['id'] + '.mp4'); mo.render(st, p['video'], f)
                print(nm, strip(f, f.replace('.mp4', '_strip.jpg'), n=7, w=200), '%.0fs' % (time.time() - t0))
