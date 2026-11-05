import urllib.request, re, json, sys, concurrent.futures as cf
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36',
      'Accept-Language': 'en-GB,en;q=0.9'}
DEC = json.JSONDecoder()


def jstr(h, key):
    i = h.find('"%s":' % key)
    if i < 0: return None
    try:
        val, _ = DEC.raw_decode(h, i + len(key) + 3)
        return val
    except Exception:
        return None


def info(vid):
    try:
        h = urllib.request.urlopen(urllib.request.Request('https://www.youtube.com/watch?v=%s' % vid, headers=UA), timeout=30).read().decode('utf-8', 'ignore')
    except Exception as e:
        return vid, {'err': str(e)}
    d = {'len': int(jstr(h, 'lengthSeconds') or 0), 'channel': jstr(h, 'ownerChannelName'), 'desc': jstr(h, 'shortDescription') or '',
         'uploaded': jstr(h, 'uploadDate'), 'title': None}
    m = re.search(r'<meta name="title" content="([^"]*)"', h)
    d['title'] = m.group(1) if m else None
    m = re.search(r'"playabilityStatus":\{"status":"([A-Z_]+)"', h)
    d['status'] = m.group(1) if m else None
    return vid, d


with cf.ThreadPoolExecutor(6) as ex:
    for vid, d in ex.map(info, sys.argv[1:]):
        if 'err' in d:
            print(vid, 'ERR', d['err']); continue
        L = d['len']
        print('== %s | %s | %d:%02d | %s | uploaded %s | %s' % (vid, d['channel'], L // 60, L % 60, d['title'], (d['uploaded'] or '')[:10], d['status']))
        desc = d['desc'].replace('\n', ' / ')
        if desc: print('   desc:', desc[:350])
