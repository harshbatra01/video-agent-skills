#!/usr/bin/env python3
"""Cheap context scan for a topic: free sources, scripts only, no AI. Writes raw JSON to research/raw and prints a short digest.
Usage: context_scan.py <job_dir> <since YYYYMMDD>. Queries are set below for this job."""
import json, re, subprocess, sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

JOB, SINCE = Path(sys.argv[1]), sys.argv[2]
RAW = JOB / 'research' / 'raw'
YTDLP = __import__('shutil').which('yt-dlp') or 'yt-dlp'
YT_Q = ['Anthropic IPO', 'Anthropic S-1 filing', 'Anthropic going public', 'Anthropic IPO explained', 'Anthropic lost 80 billion', 'Anthropic IPO shorts']
REDDIT_Q = ['anthropic ipo', 'anthropic s-1', 'anthropic filing loss']
SEEDS = ['anthropic ipo', 'anthropic stock', 'is anthropic', 'why is anthropic', 'how much is anthropic', 'can i buy anthropic', 'anthropic s-1', 'who owns anthropic']
UA = {'User-Agent': 'Mozilla/5.0'}
since_ts = datetime.strptime(SINCE, '%Y%m%d').replace(tzinfo=timezone.utc).timestamp()


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()


def youtube():
    ids = {}
    for q in YT_Q:
        for pre in ('ytsearchdate40', 'ytsearch40'):
            r = subprocess.run([YTDLP, '--flat-playlist', '-J', '--no-warnings', '%s:%s' % (pre, q)], capture_output=True, text=True, timeout=120)
            try:
                for e in json.loads(r.stdout).get('entries') or []:
                    if e.get('id') and re.search(r'anthropic|claude', e.get('title') or '', re.I):
                        ids[e['id']] = e
            except Exception:
                pass
    rows = []
    for vid in ids:
        r = subprocess.run([YTDLP, '-J', '--skip-download', '--no-warnings', 'https://www.youtube.com/watch?v=' + vid], capture_output=True, text=True, timeout=60)
        try:
            d = json.loads(r.stdout)
        except Exception:
            continue
        if (d.get('upload_date') or '0') < SINCE:
            continue
        subs, views = d.get('channel_follower_count') or 0, d.get('view_count') or 0
        rows.append(dict(id=vid, title=d.get('title'), channel=d.get('channel'), subs=subs, views=views, likes=d.get('like_count'), comments=d.get('comment_count'),
                         date=d.get('upload_date'), secs=d.get('duration'), ratio=round(views / max(subs, 1000), 2), url=d.get('webpage_url')))
    rows.sort(key=lambda x: -x['views'])
    (RAW / 'youtube.json').write_text(json.dumps(rows, indent=1))
    return rows, len(ids)


def reddit():
    rows, status = {}, []
    for q in REDDIT_Q:
        try:
            xml = get('https://www.reddit.com/search.rss?' + urllib.parse.urlencode(dict(q=q, sort='relevance', t='week', limit=50)))
            ns = {'a': 'http://www.w3.org/2005/Atom'}
            for e in ET.fromstring(xml).findall('a:entry', ns):
                u = e.find('a:link', ns).get('href')
                cat = e.find('a:category', ns)
                rows[u] = dict(title=e.find('a:title', ns).text, sub=cat.get('term') if cat is not None else '', url=u, date=(e.find('a:updated', ns).text or '')[:10])
            status.append('%s ok' % q)
        except Exception as ex:
            status.append('%s %s' % (q, ex))
        time.sleep(8)
    rows = list(rows.values())
    (RAW / 'reddit.json').write_text(json.dumps(rows, indent=1))
    return rows, status


def hn():
    url = 'https://hn.algolia.com/api/v1/search?' + urllib.parse.urlencode(dict(query='Anthropic', tags='story', hitsPerPage=100, numericFilters='created_at_i>%d,points>30' % since_ts))
    hits = [h for h in json.loads(get(url))['hits'] if re.search(r'ipo|s-1|public|filing|prospectus', h.get('title') or '', re.I)]
    hits.sort(key=lambda h: -(h.get('points') or 0))
    out = []
    for h in hits[:5]:
        item = json.loads(get('https://hn.algolia.com/api/v1/items/%s' % h['objectID']))
        kids = sorted(item.get('children') or [], key=lambda c: -(len(c.get('children') or [])))[:15]
        out.append(dict(title=h['title'], points=h['points'], n=h.get('num_comments'), id=h['objectID'],
                        top=[re.sub(r'<[^>]+>', ' ', c.get('text') or '')[:350] for c in kids]))
    (RAW / 'hn.json').write_text(json.dumps(out, indent=1))
    return out


def suggest():
    out = {}
    for s in SEEDS:
        try:
            out[s] = json.loads(get('https://suggestqueries.google.com/complete/search?' + urllib.parse.urlencode(dict(client='firefox', q=s))))[1]
        except Exception as ex:
            out[s] = ['failed: %s' % ex]
        time.sleep(1)
    (RAW / 'autocomplete.json').write_text(json.dumps(out, indent=1))
    return out


if '--no-youtube' not in sys.argv:
    yt, seen = youtube()
    print('YOUTUBE: %d found, %d since %s' % (seen, len(yt), SINCE))
    for r in yt[:25]:
        print('%9s v | %8s subs | %5ss | %s | %s | %s | %s' % (r['views'], r['subs'], r['secs'], r['date'], r['id'], (r['channel'] or '')[:22], (r['title'] or '')[:85]))
rd, st = reddit()
print('\nREDDIT:', len(rd), st)
for r in rd[:30]:
    print('%s | %s | %s' % (r['date'], r['sub'], (r['title'] or '')[:95]))
print('\nHACKER NEWS:')
for h in hn():
    print('%s pts, %s comments | %s' % (h['points'], h['n'], h['title'][:90]))
print('\nAUTOCOMPLETE:')
for k, v in suggest().items():
    print(k, '->', '; '.join(v[:8]))
