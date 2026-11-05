"""scan: daily rap / music news digest that feeds the batch build.

usage: python scan.py [hours]        (default 30) -> out/scan/scan_<date>.md (short, for reading) + .json (everything)

Reads: the verified site and YouTube feeds in research/03-news-feeds.json, X accounts through the free fxtwitter API
(unofficial: retries with other letter cases), UK charts (Shazam GB top 200 / hip-hop / discovery, Apple Music GB),
Google Trends GB + US RSS, and Wikidata for rappers' birthdays and rap album anniversaries today and tomorrow.
Ranks artists by how many independent sources mention them in the window, plus chart and trend presence.
Detection only: anything legal, violent or "allegedly" still needs a press or police source before it is posted.
"""
import json, os, re, sys, csv, io, math, time, datetime as dt, urllib.request, urllib.parse, email.utils
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.abspath(__file__))
RES = os.environ.get('VC_RESEARCH_DIR') or next((d for d in (os.path.join(os.path.dirname(ROOT), 'research'),   # original layout
    os.path.join(os.path.dirname(os.path.dirname(ROOT)), 'research', 'music-pages')) if os.path.isdir(d)),     # boss-kit library layout
    os.path.join(os.path.dirname(ROOT), 'research'))
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36'}
X_ACCOUNTS = ['GreatBritishMC', 'GRMDAILY', 'UKHipHopDaily', 'ldn_grassroots', 'theshadeborough', 'officialcharts', 'trenchmag',
              'MusicWeek', 'linkuptv', 'Kurrco', 'DailyLoud', 'Rap', 'PopCrave', 'chartdata', 'DailyRapFacts', 'SaycheeseDGTL', 'HotNewHipHop']
X_LEAN = ['GreatBritishMC', 'GRMDAILY', 'UKHipHopDaily', 'linkuptv', 'officialcharts',
          'Rap', 'Kurrco', 'DailyLoud', 'SaycheeseDGTL', 'HotNewHipHop', 'chartdata', 'PopCrave']
UK_X = {'GreatBritishMC', 'GRMDAILY', 'UKHipHopDaily', 'ldn_grassroots', 'theshadeborough', 'officialcharts', 'trenchmag', 'MusicWeek', 'linkuptv'}
UK_SEED = ('Central Cee, Dave, Stormzy, Skepta, Headie One, Digga D, Morrisson, Clavish, Nemzzz, Casper TNG, OzzCash, Fredo, K-Trap, '
           'Unknown T, M Huncho, Aitch, Bugzy Malone, Ghetts, Kano, Giggs, J Hus, Krept, Konan, Potter Payper, Knucks, Little Simz, '
           'Kojey Radical, Pa Salieu, Jim Legxacy, EsDeeKid, Fakemink, Ceebo, Sainte, Loski, Ivorian Doll, Bandokay, D Block Europe, '
           'Young Adz, Dirtbike LB, Tion Wayne, Russ Millions, ArrDee, Lancey Foux, Kwengface, Abra Cadabra, Wretch 32, Chip, Wiley, '
           'Dizzee Rascal, Mist, Tennessee Thresher, Joe James, PIXY, Hamdi, Jordan Adetunji, CGM, 163Margs, Kibo, Bliss, Lil Rass, '
           'Jordan, Teeway, Sha Gz, Kairo Keyz, Nines, Avelino, Rimzee, Mastermind, Big Zuu, D Double E, Jme, Frisco, Novelist').split(', ')
ALIASES = {'Morrisson': ['Morrison'], 'Central Cee': ['Cench'], 'Digga D': ['Digga'], 'D Block Europe': ['DBE'], 'Kanye West': ['Kanye'],
           'A$AP Rocky': ['ASAP Rocky'], 'Tyler, The Creator': ['Tyler the Creator']}
SEED = UK_SEED + ('Drake, Kendrick Lamar, Travis Scott, Future, '
        'Young Thug, Lil Baby, Lil Durk, NBA YoungBoy, Playboi Carti, Kanye West, J. Cole, Nicki Minaj, Cardi B, Megan Thee Stallion, '
        '21 Savage, Metro Boomin, Gunna, Lil Wayne, Eminem, A$AP Rocky, Tyler, The Creator, Doechii, GloRilla, Sexyy Red, Ice Spice, '
        'Don Toliver, Offset, Quavo, Lil Uzi Vert, Ken Carson, Yeat, DDG, Diddy, 50 Cent, Jay-Z, Snoop Dogg, Lil Yachty, Rod Wave, '
        'North West, Ty Dolla Sign, Kai Cenat, Lil Tecca, Che, Nettspend, Destroy Lonely, Polo G, Pop Smoke, Sha EK, Kay Flock').split(', ')
CASE_ONLY = {'Dave', 'Chip', 'Mist', 'Future', 'Che', 'Hamdi', 'Offset', 'Yeat', 'Drake', 'Giggs', 'Bliss', 'Jordan', 'Nines', 'Jme', 'Digga'}
CAL_CACHE = os.path.join(ROOT, 'out', 'scan', 'calendar_cache.json')


def get(url, timeout=20, headers=None):
    try:
        req = urllib.request.Request(url, headers=dict(UA, **(headers or {})))
        with urllib.request.urlopen(req, timeout=timeout) as r: return r.read()
    except Exception:
        return None


def ts_of(s):
    if not s: return None
    try: return email.utils.parsedate_to_datetime(s).timestamp()
    except Exception: pass
    try: return dt.datetime.fromisoformat(s.strip().replace('Z', '+00:00')).timestamp()
    except Exception: return None


def parse_feed(b, src):
    out = []
    try: root = ET.fromstring(b)
    except Exception: return out
    for e in root.iter():
        tag = e.tag.split('}')[-1]
        if tag not in ('item', 'entry'): continue
        f = {c.tag.split('}')[-1]: c for c in e}
        title = (f.get('title').text or '').strip() if f.get('title') is not None else ''
        link = ''
        if f.get('link') is not None: link = f['link'].get('href') or (f['link'].text or '')
        when = None
        for k in ('pubDate', 'published', 'updated', 'date'):
            if f.get(k) is not None and f[k].text: when = ts_of(f[k].text); break
        vid = f.get('videoId').text if f.get('videoId') is not None else None
        out.append(dict(src=src, title=title, link=link.strip(), ts=when, video=vid))
    return out


def x_timeline(h):
    for v in (h, h.lower(), h[:1].upper() + h[1:].lower()):
        b = get('https://api.fxtwitter.com/2/profile/%s/statuses' % v)
        try: d = json.loads(b) if b else {}
        except Exception: d = {}
        if d.get('results'):
            out = []
            for t in d['results']:
                if t.get('reposted_by'): continue
                media = [m.get('url') for m in ((t.get('media') or {}).get('all') or []) if m.get('url')]
                out.append(dict(src='X @' + h, title=t.get('text', ''), link=t.get('url', ''), ts=float(t.get('created_timestamp') or 0),
                                views=int(t.get('views') or 0), media=media, replies=int(t.get('replies') or 0), quotes=int(t.get('quotes') or 0),
                                reposts=int(t.get('reposts') or 0), likes=int(t.get('likes') or 0), saves=int(t.get('bookmarks') or 0)))
            return out
        time.sleep(1.5)
    return []


def shazam(kind):
    b = get('https://www.shazam.com/services/charts/csv/' + kind)
    rows = []
    if not b: return rows
    txt = b.decode('utf-8', 'replace')
    lines = txt.splitlines()
    k = next((i for i, l in enumerate(lines) if l.lower().startswith('rank')), 0)
    for r in csv.DictReader(io.StringIO('\n'.join(lines[k:]))):
        low = {kk.lower().strip(): vv for kk, vv in r.items() if kk}
        rows.append(dict(rank=int(low.get('rank') or 0), artist=low.get('artist', ''), title=low.get('title', '')))
    return rows


def apple(cc):
    b = get('https://rss.marketingtools.apple.com/api/v2/%s/music/most-played/100/songs.json' % cc)
    try: return [dict(rank=i + 1, artist=x['artistName'], title=x['name'], genres=[g['name'] for g in x.get('genres', [])])
                 for i, x in enumerate(json.loads(b)['feed']['results'])]
    except Exception: return []


def gtrends(geo):
    b = get('https://trends.google.com/trending/rss?geo=' + geo)
    return [x['title'] for x in parse_feed(b, 'trends')] if b else []


def calendar(days=14):
    """rappers' birthdays and rap album anniversaries, cached by MM-DD for the next `days` days (Wikidata asks for
    gentle use: 2 queries per refresh, a minute apart, descriptive User-Agent)"""
    cache = json.load(open(CAL_CACHE, encoding='utf-8')) if os.path.exists(CAL_CACHE) else {}
    want = [dt.date.today() + dt.timedelta(days=i) for i in range(days)]
    if all(d.strftime('%m-%d') in cache for d in want[:2]): return cache
    pairs = ' || '.join('(MONTH(?x)=%d && DAY(?x)=%d)' % (d.month, d.day) for d in want)
    qs = {'birthdays': 'SELECT ?pLabel ?x ?links WHERE { ?p wdt:P106 wd:Q2252262 ; wdt:P569 ?x ; wikibase:sitelinks ?links ; wdt:P27 ?c . '
                       'VALUES ?c { wd:Q145 wd:Q30 } FILTER(?links > 15) FILTER(%s) SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } }' % pairs,
          'albums': 'SELECT ?aLabel ?x ?perfLabel ?links WHERE { ?a wdt:P31 wd:Q482994 ; wdt:P577 ?x ; wdt:P175 ?perf ; wikibase:sitelinks ?links . '
                    '?perf wdt:P106 wd:Q2252262 . FILTER(?links > 10) FILTER(%s) SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } }' % pairs}
    got = {}
    for n, (k, q) in enumerate(qs.items()):
        if n: time.sleep(65)
        b = get('https://query.wikidata.org/sparql?format=json&query=' + urllib.parse.quote(q), timeout=90,
                headers={'Accept': 'application/sparql-results+json', 'User-Agent': 'VisionClippingNewsDigest/0.1 (daily music news digest; small volume)'})
        try: got[k] = [{kk: v['value'] for kk, v in r.items()} for r in json.loads(b)['results']['bindings']]
        except Exception: got[k] = None
    if got.get('birthdays') is None and got.get('albums') is None: return cache       # rate-limited: keep the old cache
    for d in want:
        key = d.strftime('%m-%d'); day = cache.setdefault(key, {})
        for k in ('birthdays', 'albums'):
            if got.get(k) is not None:
                day[k] = sorted([r for r in got[k] if r['x'][5:10] == key], key=lambda r: -int(r.get('links', 0)))[:12]
    os.makedirs(os.path.dirname(CAL_CACHE), exist_ok=True)
    json.dump(cache, open(CAL_CACHE, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    return cache


STORY_TYPES = [('court / jail / police', r'court|jail|prison|sentenc|charged|arrest|release date|remand|lawsuit|sued|trial'),
               ('beef / diss / reply', r'\bdiss|beef|repl(?:y|ies|ied)|respond|clap ?back|shots? at|\bvs\b'),
               ('money / deals / prices', r'\$|£|million|billion|catalog|deal|paid|charging|price|net worth'),
               ('charts / numbers / records', r'#\d|chart|billboard|number one|no\. ?1|streams|debut|record|first (?:ever|time)|milestone|units|sold'),
               ('new release / out now', r'out now|new song|new single|\bdrops?\b|album|tracklist|premiere|video'),
               ('interview quote', r'says|said|speaks|reveals|explains|opens up|on why|told'),
               ('throwback / anniversary', r'years ago|on this day|throwback|anniversary'),
               ('fashion / fits / photos', r'📸|outfit|\bfits?\b|wearing|jewel|chain|tattoo|merch'),
               ('relationships / gossip', r'girlfriend|boyfriend|dating|divorce|pregnan|cheat|wife|husband')]


def story_types(od, now, days=7):
    """which kinds of story beat their page's usual views lately (our evidence for picking stories; grows with every scan)"""
    import glob, statistics as st
    seen, P = set(), []
    for f in sorted(glob.glob(os.path.join(od, 'scan_*.json'))):
        try: d = json.load(open(f, encoding='utf-8'))
        except Exception: continue
        for i in d.get('posts', []):
            if i['link'] in seen or i.get('over') is None or now - (i.get('ts') or 0) > days * 86400: continue
            seen.add(i['link']); P.append(i)
    out = []
    for name, rx in STORY_TYPES:
        g = [i for i in P if re.search(rx, i['title'], re.I)]
        if len(g) < 5: continue
        out.append((st.median(i['over'] for i in g), '- %s: x%.2f usual, %d%% broke out (x2+), share %.1f, talk %.1f (n=%d)' % (
            name, st.median(i['over'] for i in g), 100 * sum(i['over'] >= 2 for i in g) / len(g),
            st.median(i.get('share') or 0 for i in g), st.median(i.get('talk') or 0 for i in g), len(g))))
    return ['(%d posts; small samples are noisy)' % len(P)] + [r for _, r in sorted(out, reverse=True)]


def main(hours=30, full=False):
    """default = lean: only the main pages on X (they already cover the news). full = + 81 feeds, charts, trends, calendar."""
    now = time.time(); since = now - hours * 3600
    feeds, items = [], []
    if full:
        feeds = json.load(open(os.path.join(RES, '03-news-feeds.json'), encoding='utf-8'))
        feeds = [f for f in feeds if str(f.get('verified_today')).lower() == 'true' and f.get('feed_url') and f.get('kind') in ('site_rss', 'youtube_rss')]
        with ThreadPoolExecutor(12) as ex:
            for res in ex.map(lambda f: parse_feed(get(f['feed_url']) or b'', f['name'] + (' [UK]' if f.get('region') == 'UK' else '')), feeds):
                items += res
    xs = X_ACCOUNTS if full else X_LEAN
    with ThreadPoolExecutor(4) as ex:
        for res in ex.map(x_timeline, xs): items += res
    items = [i for i in items if i.get('ts') and i['ts'] >= since and i['title']]
    charts = {'shazam_gb': shazam('top-200/united-kingdom'), 'shazam_gb_hiphop': shazam('genre/united-kingdom/hip-hop-rap'),
              'shazam_gb_discovery': shazam('discovery/united-kingdom'), 'apple_gb': apple('gb'), 'apple_us': apple('us')} if full else \
        {k: [] for k in ('shazam_gb', 'shazam_gb_hiphop', 'shazam_gb_discovery', 'apple_gb', 'apple_us')}
    trends = {'GB': gtrends('GB'), 'US': gtrends('US')} if full else {'GB': [], 'US': []}
    cal = {'today': {}, 'tomorrow': {}}
    if full:
        cc = calendar(); today = dt.date.today(); tom = today + dt.timedelta(days=1)
        cal = {'today': cc.get(today.strftime('%m-%d'), {}), 'tomorrow': cc.get(tom.strftime('%m-%d'), {})}
    # artist list: seed + rap / discovery chart artists (features split out)
    names = set(SEED)
    for k, n in (('shazam_gb_hiphop', 60), ('shazam_gb_discovery', 40)):
        for r in charts[k][:n]:
            for a in re.split(r',| & | x | feat\.? | ft\.? ', r['artist'], flags=re.I):
                a = a.strip()
                if len(a) > 2: names.add(a)
    for r in cal['today'].get('birthdays', []) + cal['tomorrow'].get('birthdays', []): names.add(r['pLabel'])
    pats = {n: re.compile(r'(?<![\w$])(?:' + '|'.join(re.escape(v) for v in [n] + ALIASES.get(n, [])) + r')(?![\w])',
                          0 if n in CASE_ONLY else re.I) for n in names}
    agg = {}
    for it in items:
        for n, p in pats.items():
            if p.search(it['title']):
                a = agg.setdefault(n, dict(sources=set(), items=[], views=0, media=[], videos=[]))
                a['sources'].add(it['src']); a['items'].append(it); a['views'] += it.get('views', 0)
                a['media'] += it.get('media', []); a['videos'] += [it['video']] if it.get('video') else []
    rank_of = lambda chart, n: next((r['rank'] for r in charts[chart] if n.lower() in r['artist'].lower()), None)
    tr = ' | '.join(trends['GB'] + trends['US']).lower()
    rows = []
    for n, a in agg.items():
        w = sum(1.5 if ('[UK]' in s or s[4:] in UK_X) else 1.0 for s in a['sources'])
        sg, sh, ag = rank_of('shazam_gb', n), rank_of('shazam_gb_hiphop', n), rank_of('apple_gb', n)
        uk = n in UK_SEED or any('[UK]' in s or s[4:] in UK_X for s in a['sources'])
        score = (w + (2 if sg and sg <= 50 else 0) + (1 if sh and sh <= 20 else 0) + (1 if ag and ag <= 50 else 0)
                 + (3 if n.lower() in tr else 0) + (math.log10(a['views']) / 2 if a['views'] > 1000 else 0)) * (1.3 if uk else 1.0)
        rows.append(dict(artist=n, uk=uk, score=round(score, 1), n_sources=len(a['sources']), shazam_gb=sg, shazam_gb_hiphop=sh, apple_gb=ag,
                         trending=n.lower() in tr, views=a['views'], media=list(dict.fromkeys(a['media']))[:6],
                         youtube=list(dict.fromkeys(a['videos']))[:4],
                         items=[dict(src=i['src'], title=i['title'][:220], link=i['link'],
                                     age_h=round((now - i['ts']) / 3600, 1)) for i in sorted(a['items'], key=lambda i: -i['ts'])[:6]]))
    rows.sort(key=lambda r: -r['score'])
    viral = sorted([i for i in items if i.get('views', 0) > 50000], key=lambda i: -i['views'])[:12]
    # trending potential: a post doing several times its page's usual views is breaking out; replies + quotes per 1k views = debate
    by_src = {}
    for i in items:
        if i.get('views'): by_src.setdefault(i['src'], []).append(i['views'])
    med = {k: sorted(v)[len(v) // 2] for k, v in by_src.items() if len(v) >= 5}
    for i in items:
        if i.get('views') and i['src'] in med:
            i['over'] = round(i['views'] / max(1, med[i['src']]), 1)
            i['talk'] = round((i.get('replies', 0) + i.get('quotes', 0)) * 1000 / max(1, i['views']), 1)
            i['share'] = round((i.get('reposts', 0) + i.get('saves', 0)) * 1000 / max(1, i['views']), 1)
    breaking = sorted([i for i in items if i.get('over', 0) >= 2.5], key=lambda i: -i['over'])[:12]
    talked = sorted([i for i in items if i.get('views', 0) >= 5000 and i.get('talk')], key=lambda i: -i['talk'])[:8]
    od = os.path.join(ROOT, 'out', 'scan'); os.makedirs(od, exist_ok=True)
    stamp = dt.datetime.now().strftime('%Y-%m-%d_%H%M')
    json.dump(dict(generated=stamp, hours=hours, n_items=len(items), n_feeds=len(feeds), artists=rows, viral=viral,
                   posts=[{k: i.get(k) for k in ('src', 'title', 'link', 'ts', 'views', 'over', 'talk', 'share', 'media')} for i in items], charts=charts,
                   trends=trends, calendar=cal), open(os.path.join(od, 'scan_%s.json' % stamp), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=list)
    L = ['# Scan %s (last %dh): %d items from %d feeds + %d X accounts' % (stamp, hours, len(items), len(feeds), len(xs))]
    for head, sel in (('## UK top', [r for r in rows if r['uk']][:12]), ('## All top', [r for r in rows if not r['uk']][:15])):
      L += ['', head]
      for r in sel:
        flags = ' '.join(x for x in ['ShazamGB#%s' % r['shazam_gb'] if r['shazam_gb'] else '', 'AppleGB#%s' % r['apple_gb'] if r['apple_gb'] else '',
                                     'TRENDING' if r['trending'] else '', '%dk views' % (r['views'] // 1000) if r['views'] > 1000 else ''] if x)
        L.append('- **%s** score %s, %d sources %s' % (r['artist'], r['score'], r['n_sources'], flags))
        for i in r['items'][:3]: L.append('  - %.0fh %s: %s' % (i['age_h'], i['src'], i['title'][:150].replace('\n', ' ')))
    row = lambda i: '- x%s usual | %dk views | %s talk | %s share | %.0fh | %s %s : %s' % (
        i.get('over', '?'), i['views'] // 1000, i.get('talk', '?'), i.get('share', '?'), (now - i['ts']) / 3600 if i.get('ts') else 0,
        i['src'], i['link'], i['title'][:130].replace('\n', ' '))
    L += ['', "## Breaking out (views vs the page's usual; talk = replies+quotes per 1k views, share = reposts+saves per 1k)"] + [row(i) for i in breaking]
    L += ['', '## Most talked about (debate potential)'] + [row(i) for i in talked]
    L += ['', '## Viral X posts (no artist filter)'] + ['- %dk %s (media %d) %s : %s' % (i['views'] // 1000, i['src'], len(i.get('media', [])), i['link'],
                                                                                      i['title'][:140].replace('\n', ' ')) for i in viral]
    L += ['', "## What's working on the main pages (story types, last 7 days of scans)"] + story_types(od, now)
    if not full:
        p = os.path.join(od, 'scan_%s.md' % stamp); open(p, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
        print('%s | lean | items %d | artists matched %d | top: %s' % (p, len(items), len(rows), ', '.join(r['artist'] for r in rows[:8])))
        return
    L += ['', '## Calendar (Wikidata)']
    for k in ('today', 'tomorrow'):
        L.append('- %s birthdays: %s' % (k, ', '.join('%s (%s)' % (b['pLabel'], b['b'][:4]) for b in cal[k].get('birthdays', [])) or 'none'))
        L.append('- %s album anniversaries: %s' % (k, ', '.join('%s by %s (%s)' % (a['aLabel'], a.get('perfLabel', '?'), a['d'][:4]) for a in cal[k].get('albums', [])) or 'none'))
    L += ['', '## Charts', '- Shazam GB hip-hop top 10: ' + '; '.join('%s - %s' % (r['artist'], r['title']) for r in charts['shazam_gb_hiphop'][:10]),
          '- Shazam GB discovery top 10: ' + '; '.join('%s - %s' % (r['artist'], r['title']) for r in charts['shazam_gb_discovery'][:10]),
          '- Google Trends GB: ' + ', '.join(trends['GB'][:10])]
    p = os.path.join(od, 'scan_%s.md' % stamp); open(p, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('%s | items %d | artists matched %d | top: %s' % (p, len(items), len(rows), ', '.join(r['artist'] for r in rows[:8])))


if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if x != '--full']
    main(float(a[0]) if a else 30, full='--full' in sys.argv)
