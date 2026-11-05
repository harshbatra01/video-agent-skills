"""HEAD-probe Pexels CDN for the available renditions of shortlisted clips (no downloads)."""
import json, concurrent.futures as cf, urllib.request, sys
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36'}
SHORT = {  # id: sd preview size from the search page ('' = unknown)
 '12893568': '360x640', '6032135': '506x960', '6297755': '360x640', '4661333': '506x960', '7615545': '360x640',
 '7615546': '360x640', '6801319': '360x640', '7930758': '360x640', '7033622': '360x640', '8676954': '360x640',
 '35675125': '', '7889571': '506x960', '8455765': '506x960', '8801823': '360x640', '8801827': '360x640',
 '8802446': '360x640', '8802444': '360x640', '39322844': '', '7982709': '360x640', '8122968': '360x640',
 '6396064': '360x640', '8263997': '360x640', '8044794': '360x640', '6782216': '360x640', '29236674': '',
 '37925060': '', '35460855': '', '29851224': '', '35219401': '', '27441395': '', '6454262': '360x640',
 '29639944': '', '10047234': '960x506', '8107399': '506x960', '11075637': '640x360', '4492602': '640x360',
 '5723722': '506x960'}
SIZES = {'portrait': [(2160, 3840), (1440, 2560), (1080, 1920), (720, 1280)],
         'tall': [(2160, 4096), (1080, 2048), (720, 1366)],
         'landscape': [(3840, 2160), (2560, 1440), (1920, 1080), (1280, 720)],
         'wide': [(4096, 2160), (2048, 1080), (1366, 720)]}
FPS = [24, 25, 30, 50, 60]


def kinds(prev):
    if not prev: return ['portrait', 'tall', 'landscape', 'wide']
    w, h = map(int, prev.split('x'))
    r = w / h
    if r < 0.54: return ['tall', 'portrait']
    if r < 0.6: return ['portrait', 'tall']
    if r > 1.85: return ['wide', 'landscape']
    return ['landscape', 'wide']


def head(url):
    try:
        req = urllib.request.Request(url, headers=UA, method='HEAD')
        with urllib.request.urlopen(req, timeout=20) as r:
            return int(r.headers.get('Content-Length') or 0) if r.status == 200 else None
    except Exception:
        return None


jobs = []
for vid, prev in SHORT.items():
    for k in kinds(prev):
        for (w, h) in SIZES[k]:
            tag = 'uhd' if min(w, h) >= 1440 else 'hd'
            for f in FPS:
                jobs.append((vid, w, h, f, 'https://videos.pexels.com/video-files/%s/%s-%s_%d_%d_%dfps.mp4' % (vid, vid, tag, w, h, f)))
with cf.ThreadPoolExecutor(24) as ex:
    res = list(ex.map(lambda j: (j, head(j[4])), jobs))
found = {}
for (vid, w, h, f, url), size in res:
    if size: found.setdefault(vid, []).append({'w': w, 'h': h, 'fps': f, 'mb': round(size / 1e6, 1), 'url': url})
for vid in SHORT:
    fl = sorted(found.get(vid, []), key=lambda d: -d['w'] * d['h'])
    print(vid, ' | '.join('%dx%d@%d %.0fMB' % (d['w'], d['h'], d['fps'], d['mb']) for d in fl) or 'NOT FOUND')
json.dump(found, open('probe.json', 'w'), indent=1)
