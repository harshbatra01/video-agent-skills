"""YouTube search via the public results page (ytInitialData), many queries in parallel -> one JSON + compact table."""
import urllib.request, urllib.parse, json, re, sys, concurrent.futures as cf
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36',
      'Accept-Language': 'en-GB,en;q=0.9'}
DEC = json.JSONDecoder()


def fetch(q):
    url = 'https://www.youtube.com/results?search_query=' + urllib.parse.quote(q)
    h = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read().decode('utf-8', 'ignore')
    i = h.find('var ytInitialData = ')
    if i < 0: i = h.find('ytInitialData = ')
    data, _ = DEC.raw_decode(h, h.index('{', i))
    out = []

    def walk(o):
        if isinstance(o, dict):
            if 'videoRenderer' in o:
                v = o['videoRenderer']
                t = ''.join(r.get('text', '') for r in v.get('title', {}).get('runs', []))
                ch = ''.join(r.get('text', '') for r in v.get('ownerText', {}).get('runs', []))
                ln = v.get('lengthText', {}).get('simpleText', '')
                vc = v.get('viewCountText', {}).get('simpleText', '') or ''.join(r.get('text', '') for r in v.get('viewCountText', {}).get('runs', []))
                pt = v.get('publishedTimeText', {}).get('simpleText', '')
                out.append(dict(id=v.get('videoId'), title=t, channel=ch, len=ln, views=vc, age=pt))
                return
            for x in o.values(): walk(x)
        elif isinstance(o, list):
            for x in o: walk(x)
    walk(data)
    return q, out


if __name__ == '__main__':
    queries = [l.strip() for l in open(sys.argv[1], encoding='utf-8') if l.strip()]
    res = {}
    with cf.ThreadPoolExecutor(6) as ex:
        for q, out in ex.map(lambda q: (lambda r: r)(fetch(q)) if True else None, queries):
            res[q] = out
    json.dump(res, open(sys.argv[2], 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    seen = {}
    for q, out in res.items():
        for v in out[:int(sys.argv[3]) if len(sys.argv) > 3 else 8]:
            if v['id'] in seen: seen[v['id']]['q'].append(q[:18]); continue
            seen[v['id']] = dict(v, q=[q[:18]])
    for vid, v in seen.items():
        print('%s | %-7s | %-24s | %-10s | %s' % (vid, v['len'], v['channel'][:24], v['views'].replace(' views', '')[:10], v['title'][:90]))
    print('unique videos:', len(seen))
