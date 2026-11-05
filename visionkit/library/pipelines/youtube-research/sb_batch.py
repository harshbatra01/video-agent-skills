"""Storyboard contact sheets for a list of YouTube ids (no video download): <= max tiles each, timestamped, labelled."""
import sys, os, json, math, io, re, urllib.request, concurrent.futures as cf
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from storyboard import get

HERE = os.path.dirname(os.path.abspath(__file__))


def levels(vid):
    h = get('https://www.youtube.com/watch?v=%s' % vid).decode('utf-8', 'ignore')
    m = re.search(r'"playerStoryboardSpecRenderer":\{"spec":"([^"]+)"', h)
    length = int(re.search(r'"lengthSeconds":"(\d+)"', h).group(1))
    title = re.search(r'<meta name="title" content="([^"]*)"', h)
    spec = m.group(1).replace('\\u0026', '&'); parts = spec.split('|'); base = parts[0]; lv = []
    for i, p in enumerate(parts[1:]):
        f = p.split('#'); w, hh, count, cols, rows, interval = map(int, f[:6])
        lv.append(dict(L=i, w=w, h=hh, count=count, cols=cols, rows=rows, interval=interval, name=f[6], sigh=f[7]))
    return base, lv, length, (title.group(1) if title else vid)


def sheet(vid, label, t_from=0, t_to=None, max_tiles=60, cols=10):
    base, lvs, length, title = levels(vid)
    lv = lvs[-1]
    t_to = min(t_to or length, length)
    step = (lv['interval'] / 1000.0) if lv['interval'] else length / lv['count']
    idx = [k for k in range(lv['count']) if t_from <= k * step <= t_to]
    if len(idx) > max_tiles:
        stride = math.ceil(len(idx) / max_tiles); idx = idx[::stride]
    per = lv['cols'] * lv['rows']; cache = {}; tiles = []
    for k in idx:
        s = k // per
        if s not in cache:
            url = base.replace('$L', str(lv['L'])).replace('$N', lv['name'].replace('$M', str(s)))
            url += ('&' if '?' in url else '?') + 'sigh=' + lv['sigh']
            try: cache[s] = Image.open(io.BytesIO(get(url))).convert('RGB')
            except Exception: cache[s] = None
        img = cache[s]
        if img is None: continue
        j = k % per; c, r = j % lv['cols'], j // lv['cols']
        tiles.append((k * step, img.crop((c * lv['w'], r * lv['h'], (c + 1) * lv['w'], (r + 1) * lv['h']))))
    W, H = lv['w'], lv['h']
    S = Image.new('RGB', (cols * W, math.ceil(len(tiles) / cols) * (H + 12) + 18), (12, 12, 12)); d = ImageDraw.Draw(S)
    d.text((3, 3), '%s  %s  [%s]  %d:%02d' % (label, vid, title[:80], length // 60, length % 60), fill=(255, 255, 0))
    for i, (t, tile) in enumerate(tiles):
        x, y = (i % cols) * W, 18 + (i // cols) * (H + 12)
        S.paste(tile, (x, y + 12)); d.text((x + 2, y), '%d:%02d' % (t // 60, t % 60), fill=(255, 255, 255))
    out = os.path.join(HERE, 'sbx_%s.png' % label)
    S.save(out)
    return label, vid, length, title, len(tiles), S.size


if __name__ == '__main__':
    jobs = json.loads(open(sys.argv[1], encoding='utf-8').read())
    with cf.ThreadPoolExecutor(4) as ex:
        futs = [ex.submit(sheet, **j) for j in jobs]
        for f in futs:
            try: print(f.result(), flush=True)
            except Exception as e: print('ERR', e, flush=True)
