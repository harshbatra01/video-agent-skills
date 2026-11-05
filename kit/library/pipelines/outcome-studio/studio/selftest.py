"""selftest: render every format once from live data and put them on one contact sheet (out/_selftest/_sheet.jpg).

python selftest.py [ig|tt] [fmt,fmt]      ig = 1080x1350 (default), tt = 1080x1920
"""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ocdata as od, formats as fm
from render import Studio
from PIL import Image, ImageDraw

OUT = os.path.join(od.ROOT, 'out', '_selftest')


def sheet(paths, out, cell=360, cols=6):
    ims = [Image.open(p).convert('RGB') for p in paths]
    hs = [int(im.height * cell / im.width) for im in ims]; rows = (len(ims) + cols - 1) // cols
    rh = [max(hs[r * cols:(r + 1) * cols]) + 26 for r in range(rows)]
    sh = Image.new('RGB', (cols * (cell + 8), sum(rh)), (30, 30, 30)); d = ImageDraw.Draw(sh); y = 0
    for r in range(rows):
        for c in range(cols):
            i = r * cols + c
            if i >= len(ims): break
            x = c * (cell + 8); sh.paste(ims[i].resize((cell, hs[i])), (x, y + 24)); d.text((x + 4, y + 6), os.path.basename(paths[i])[:48], fill=(255, 255, 0))
        y += rh[r]
    sh.save(out, quality=86); return out


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'ig'
    only = set(sys.argv[2].split(',')) if len(sys.argv) > 2 else None
    size = (1080, 1350) if mode == 'ig' else (1080, 1920)
    ms = od.markets()
    get = lambda key: next(m for m in ms if m['key'] == key)
    posts = []
    md = fm.matchday(ms, 'UEFA Champions League', day=time.strftime('%Y%m%d', time.gmtime(time.time() + 86400)))
    if md: posts.append(md)
    city = next((m for m in ms if m['kind'] == 'match3' and 'Manchester City' in m['title'] and m['ok']), None)
    if city: posts.append(fm.pick(city, {'Manchester City': {'facts': ['Fact one about *City* goes here', 'Fact two with a *number*'], 'source': 'ESPN'},
                                         'Paris Saint Germain': {'facts': ['Fact one about *PSG*', 'Fact two'], 'source': 'ESPN'}}))
    bdo = next(m for m in ms if m['kind'] == 'winner' and 'Ballon' in m['title'])
    posts.append(fm.swing(bdo, ['Harry Kane', 'Lamine Yamal'], days=9, sub='Ballon d\'Or chance on Outcome, last 9 days'))
    epl = next(m for m in ms if m['kind'] == 'winner' and 'Premier' in m['title'])
    ucl = next(m for m in ms if m['kind'] == 'winner' and 'Champions' in m['title'])
    fed = next(m for m in ms if m['kind'] == 'fed' and m['ok'])
    hike = next(r for r in fed['outcomes'] if r['label'] == 'Hike')
    posts.append(fm.quiz([{'q': 'Arsenal win the Premier League', 'p': epl['outcomes'][0]['p'], 'team': fm.team('Arsenal'), 'context': '2026/27 season'},
                          {'q': 'Harry Kane wins the Ballon d\'Or', 'p': bdo['outcomes'][0]['p']},
                          {'q': 'The Fed raises rates in October', 'p': hike['p']}]))
    posts.append(fm.breaking(fed, 'Hike', 'Traders give the Fed %s *%d%%* chance of a ^rate hike^ this month' % (fm.a_an(100 * hike['p']), round(100 * hike['p'])),
                             note='No change: *%d%%*. Cut: *<1%%*.' % round(100 * next(r for r in fed['outcomes'] if r['label'] == 'No change')['p'])))
    posts.append(fm.tier(ucl, title='Champions League winner, *ranked by real money*'))
    posts.append(fm.ladder_touch(ms, 'BTC'))
    posts.append(fm.ladder_ipo(ms, 'Anthropic'))
    posts.append(fm.pricetags(epl, sub='Premier League 2026/27 winner'))
    posts.append(fm.number(next(r for r in fed['outcomes'] if r['label'] == 'No change')['p'], 'Chance the *Fed holds* rates in October', sub='Hike *%d%%*. Cut *<1%%*.' % round(100 * hike['p'])))
    posts.append(fm.ranking(bdo, title="Ballon d'Or 2026: *the favourites*"))
    posts = [p for p in posts if p]
    os.makedirs(OUT, exist_ok=True); outs = []
    t0 = time.time()
    with Studio(fm.brand()) as st:
        for p in posts:
            for i, s in enumerate(p['slides']):
                if only and s['fmt'] not in only: continue
                f = os.path.join(OUT, '%s_%02d_%s_%s.jpg' % (p['id'], i, s['fmt'], mode))
                st.still(s, f, size); outs.append(f)
    print('rendered %d slides in %.1fs' % (len(outs), time.time() - t0))
    print(sheet(outs, os.path.join(OUT, '_sheet_%s.jpg' % mode)))
