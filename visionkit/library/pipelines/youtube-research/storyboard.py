"""Build a timestamped contact sheet from YouTube's scrubbing-preview storyboard (no video download)."""
import urllib.request, re, json, sys, io, math
from PIL import Image, ImageDraw
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36',
      'Accept-Language': 'en-GB,en;q=0.9'}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()


def sheet(vid, t_from=0, t_to=None, max_frames=160, out=None):
    h = get('https://www.youtube.com/watch?v=%s' % vid).decode('utf-8', 'ignore')
    m = re.search(r'"playerStoryboardSpecRenderer":\{"spec":"([^"]+)"', h)
    length = int(re.search(r'"lengthSeconds":"(\d+)"', h).group(1))
    spec = m.group(1).replace('\\u0026', '&')
    parts = spec.split('|')
    base = parts[0]
    levels = []
    for i, p in enumerate(parts[1:]):
        f = p.split('#')
        w, hh, count, cols, rows, interval = map(int, f[:6])
        name, sigh = f[6], f[7]
        levels.append(dict(L=i, w=w, h=hh, count=count, cols=cols, rows=rows, interval=interval, name=name, sigh=sigh))
    lv = levels[-1]
    t_to = t_to or length
    # frame times: storyboard frame k covers ~ k * (length/count) seconds when interval==0
    step = (lv['interval'] / 1000.0) if lv['interval'] else length / lv['count']
    idx = [k for k in range(lv['count']) if t_from <= k * step <= t_to]
    if len(idx) > max_frames:
        stride = math.ceil(len(idx) / max_frames); idx = idx[::stride]
    per = lv['cols'] * lv['rows']
    cache = {}
    tiles = []
    for k in idx:
        s = k // per
        if s not in cache:
            url = base.replace('$L', str(lv['L'])).replace('$N', lv['name'].replace('$M', str(s)))
            url += ('&' if '?' in url else '?') + 'sigh=' + lv['sigh']
            try:
                cache[s] = Image.open(io.BytesIO(get(url))).convert('RGB')
            except Exception as e:
                cache[s] = None
        img = cache[s]
        if img is None: continue
        j = k % per; c, r = j % lv['cols'], j // lv['cols']
        tile = img.crop((c * lv['w'], r * lv['h'], (c + 1) * lv['w'], (r + 1) * lv['h']))
        tiles.append((k * step, tile))
    cols = 8
    W, H = lv['w'], lv['h']
    S = Image.new('RGB', (cols * W, math.ceil(len(tiles) / cols) * (H + 14) + 16), (15, 15, 15))
    d = ImageDraw.Draw(S); d.text((3, 2), '%s  length %d:%02d  step %.1fs' % (vid, length // 60, length % 60, step), fill=(255, 255, 0))
    for i, (t, tile) in enumerate(tiles):
        x, y = (i % cols) * W, 16 + (i // cols) * (H + 14)
        S.paste(tile, (x, y + 14)); d.text((x + 2, y + 1), '%d:%02d:%02d' % (t // 3600, (t % 3600) // 60, t % 60) if t >= 3600 else '%d:%02d' % (t // 60, t % 60), fill=(255, 255, 255))
    S.save(out or ('sb_%s.png' % vid))
    return out or ('sb_%s.png' % vid), len(tiles), step, (lv['w'], lv['h'])


if __name__ == '__main__':
    vid = sys.argv[1]; a = float(sys.argv[2]) if len(sys.argv) > 2 else 0; b = float(sys.argv[3]) if len(sys.argv) > 3 else None
    print(sheet(vid, a, b, out='sb_%s_%d.png' % (vid, a)))
