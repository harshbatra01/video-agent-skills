#!/usr/bin/env python3
"""Idea radar: finds big AI and tech news and writes a ranked idea list. Free sources only. Never posts anything.

Mix of three open source tools:
- Horizon (MIT): its scrapers for RSS, Google News, Hacker News and Reddit, imported from ~/third-party/Horizon;
  its scoring scale, adapted in rubric.md.
- BuzzAgent (no licence, so ideas only, code written fresh here): cheap filters before AI, SimHash, TF-IDF story grouping.
- last30days (MIT): run as a program on the top events, for free community reaction.
Plus an X route (fxtwitter, unofficial) and its breakout rule (views against the page's own median).

Run with Horizon's Python:
  ~/third-party/Horizon/.venv/bin/python radar.py            full run
  ... radar.py --no-ai                                                 stop before AI, print filter counts
  ... radar.py --no-context                                            skip last30days
  ... radar.py --fresh                                                 ignore what earlier runs saw
  ... radar.py --days 14                                               look back over 14 days, saves nothing to the seen list
"""
import argparse, asyncio, hashlib, json, logging, math, os, re, sqlite3, statistics, subprocess, sys, tempfile, time
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
THIRD = Path(os.environ.get('RADAR_THIRD_PARTY', Path.home() / 'third-party'))
sys.path.insert(0, str(THIRD / 'Horizon'))
import httpx
from src.models import GoogleNewsConfig, HackerNewsConfig, RedditConfig, RedditSubredditConfig, RSSSourceConfig
from src.scrapers.google_news import GoogleNewsScraper
from src.scrapers.hackernews import HackerNewsScraper
from src.scrapers.reddit import RedditScraper
from src.scrapers.rss import RSSScraper

logging.disable(logging.WARNING)
UA = {'User-Agent': 'Mozilla/5.0'}
STOP = set('''a about after all also an and any are as at be because been but by can do does for from had has have he her his how i if in
into is it its me my no not of on or our out over she so than that the their them then there these they this to up us was we were what
when where which who why with you your'''.split())
# Paid-service keys are removed from anything we start, so nothing here can spend money by accident.
PAID_ENV = ('OPENAI_API_KEY', 'ELEVENLABS_API_KEY', 'ANTHROPIC_API_KEY', 'XAI_API_KEY', 'GOOGLE_API_KEY', 'GEMINI_API_KEY',
            'OPENROUTER_API_KEY', 'PERPLEXITY_API_KEY', 'APIFY_TOKEN', 'SCRAPECREATORS_API_KEY', 'X_BEARER_TOKEN')


def clean_env():
    env = {k: v for k, v in os.environ.items() if k not in PAID_ENV and k != 'CLAUDECODE'}
    return env


# ---------- 1. Collect ----------
def x_page(handle, primary, now, cutoff=None, max_pages=1):
    """One page's recent posts through fxtwitter, each measured against that page's own median views."""
    for v in (handle, handle.lower()):
        try:
            d = httpx.get('https://api.fxtwitter.com/2/profile/%s/statuses' % v, headers=UA, timeout=45).json()
        except Exception:
            d = {}
        posts = [t for t in d.get('results') or [] if not t.get('reposted_by') and not t.get('replying_to')]
        if posts:
            break
        time.sleep(1)
    else:
        return [], 'failed'
    # Look-back runs follow the cursor until the posts are older than the window.
    for _ in range(max_pages - 1):
        cursor = (d.get('cursor') or {}).get('bottom')
        if not cursor or not cutoff or min(float(t.get('created_timestamp') or now) for t in d.get('results') or [{}]) < cutoff:
            break
        time.sleep(0.4)
        try:
            d = httpx.get('https://api.fxtwitter.com/2/profile/%s/statuses' % v, params={'cursor': cursor}, headers=UA, timeout=45).json()
        except Exception:
            break
        posts += [t for t in d.get('results') or [] if not t.get('reposted_by') and not t.get('replying_to')]
    median = statistics.median(int(t.get('views') or 0) for t in posts) or 1
    out = []
    for t in posts:
        ts = float(t.get('created_timestamp') or 0)
        age_h = max((now - ts) / 3600, 0.5)
        # A young post has had less time to collect views, so expect less from it. The square root curve is a starting guess.
        expected = median * min(1.0, math.sqrt(age_h / 24))
        views = int(t.get('views') or 0)
        text = re.sub(r'\s+', ' ', t.get('text') or '').strip()
        if not text:
            continue
        out.append(dict(src='X @' + handle, kind='x', primary=primary, title=text[:240], text=text[:600], url=t.get('url') or '', ts=ts,
                        views=views, over=round(views / max(expected, 1), 2), likes=int(t.get('likes') or 0)))
    return out, 'ok'


def hn_back(cfg, since):
    """Hacker News front page only shows today, so look-back runs use its free Algolia search for the highest scored stories."""
    r = httpx.get('https://hn.algolia.com/api/v1/search', timeout=30, params={
        'tags': 'story', 'hitsPerPage': 300, 'numericFilters': 'created_at_i>%d,points>%d' % (since.timestamp(), cfg['hn_min_score'])})
    return [dict(src='Hacker News', kind='hacker news', primary=False, title=h.get('title') or '', text='',
                 url=h.get('url') or 'https://news.ycombinator.com/item?id=%s' % h.get('objectID'), ts=float(h['created_at_i']),
                 score=int(h.get('points') or 0)) for h in r.json().get('hits', []) if h.get('title')]


async def horizon_sources(cfg, since, days=None):
    """Horizon's own scrapers, unchanged."""
    items, status = [], {}
    async with httpx.AsyncClient(timeout=30, follow_redirects=True, headers=UA) as client:
        jobs = {}
        for name, feeds, primary in (('rss primary', cfg['rss_primary'], True), ('rss press', cfg['rss_press'], False)):
            jobs[name] = (RSSScraper([RSSSourceConfig(name=f['name'], url=f['url']) for f in feeds], client), primary)
        for q in cfg['google_news']:
            jobs['google news: ' + q] = (GoogleNewsScraper(GoogleNewsConfig(enabled=True, query=q, max_results=100 if days else 40), client), False)
        if not days:
            jobs['hacker news'] = (HackerNewsScraper(HackerNewsConfig(fetch_top_stories=cfg['hn_top'], min_score=cfg['hn_min_score']), client), False)
        jobs['reddit'] = (RedditScraper(RedditConfig(fetch_comments=0, subreddits=[
            RedditSubredditConfig(subreddit=s, sort='top', time_filter=('week' if days <= 7 else 'month') if days else 'day',
                                  fetch_limit=100 if days else 25, min_score=cfg['reddit_min_score'])
            for s in cfg['reddit']]), client), False)
        results = await asyncio.gather(*(j[0].fetch(since) for j in jobs.values()), return_exceptions=True)
    for (name, (_, primary)), res in zip(jobs.items(), results):
        if isinstance(res, Exception):
            status[name] = 'failed: %s' % type(res).__name__
            continue
        got = list(res.items)
        status[name] = len(got)
        for it in got:
            m = it.metadata or {}
            src = m.get('source_name') or m.get('feed_name') or m.get('subreddit') or it.author or name
            if name == 'hacker news':
                src = 'Hacker News'
            elif name == 'reddit':
                src = 'r/%s' % (m.get('subreddit') or it.author or '')
            items.append(dict(src=str(src), kind=name.split(':')[0].replace(' primary', '').replace(' press', ''), primary=primary,
                              title=it.title.strip(), text=re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', it.content or ''))[:500],
                              url=str(it.url), ts=it.published_at.timestamp(), score=int(m.get('score') or 0)))
    return items, status


# ---------- 2. Filters with no AI (BuzzAgent's idea, written fresh) ----------
def words(text, stop):
    return [w for w in re.findall(r"[a-z0-9][a-z0-9.\-+]*[a-z0-9]|[a-z0-9]", text.lower()) if w not in stop]


def norm_title(t):
    t = re.sub(r'\s+-\s+[^-]{2,40}$', '', t)  # Google News adds " - Publisher"
    t = re.sub(r'https?://\S+', ' ', t.lower())
    return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', ' ', t)).strip()


def simhash(text):
    t = text.lower()
    grams = [t[i:i + 3] for i in range(max(len(t) - 2, 0))]
    v = [0] * 64
    for g in grams:
        h = int.from_bytes(hashlib.blake2b(g.encode(), digest_size=8).digest(), 'big')
        for i in range(64):
            v[i] += 1 if h >> i & 1 else -1
    return sum(1 << i for i in range(64) if v[i] > 0)


def filters(items, cfg, db, fresh, now):
    counts = Counter(collected=len(items))
    noise = re.compile('|'.join(cfg['noise']), re.I)
    keys = re.compile(r'(?<![a-z])(' + '|'.join(cfg['keywords']) + r')(?![a-z])', re.I)
    cutoff = now - cfg['window_hours'] * 3600
    seen_run, hashes, kept = set(), [], []
    for it in sorted(items, key=lambda i: (not i['primary'], i['ts'])):
        title = norm_title(it['title'])
        it['norm'] = title
        if it['ts'] < cutoff:
            counts['too old'] += 1
            continue
        key = hashlib.sha256((it['url'] or title).encode()).hexdigest()[:20]
        it['key'] = key
        if key in seen_run or (not fresh and db.execute('select 1 from seen where key=?', (key,)).fetchone()):
            counts['seen before'] += 1
            continue
        seen_run.add(key)
        if noise.search(it['title']):
            counts['noise words'] += 1
            continue
        if not it['primary'] and not keys.search(it['title'] + ' ' + it['text'][:200]):
            counts['off topic'] += 1
            continue
        sh = simhash(title)
        twin = next((k for h, k in hashes if bin(h ^ sh).count('1') <= 3), None)
        if twin is not None:  # same headline elsewhere: count the source, keep one copy
            if it['src'] not in twin['also'] and it['src'] != twin['src']:
                twin['also'].append(it['src'])
            counts['near copy'] += 1
            continue
        it['also'] = []
        hashes.append((sh, it))
        kept.append(it)
    counts['kept'] = len(kept)
    return kept, counts


def tfidf(docs):
    df = Counter(w for d in docs for w in set(d))
    n = len(docs)
    vecs = []
    for d in docs:
        tf = Counter(d)
        v = {w: c * math.log((1 + n) / (1 + df[w]) + 1) for w, c in tf.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1
        vecs.append({w: x / norm for w, x in v.items()})
    return vecs


def cos(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(x * b.get(w, 0) for w, x in a.items())


def cluster(items, cfg):
    stop = STOP | set(cfg['stopwords_extra'])
    vecs = tfidf([words(it['norm'], stop) for it in items])
    groups = []
    for it, v in sorted(zip(items, vecs), key=lambda p: p[0]['ts']):
        best, best_sim = None, 0
        for g in groups:
            s = cos(v, g['centre'])
            if s > best_sim:
                best, best_sim = g, s
        if best and best_sim >= cfg['cluster_cosine']:
            best['items'].append(it)
            m = len(best['items'])
            keys = set(best['centre']) | set(v)
            c = {w: (best['centre'].get(w, 0) * (m - 1) + v.get(w, 0)) / m for w in keys}
            norm = math.sqrt(sum(x * x for x in c.values())) or 1
            best['centre'] = {w: x / norm for w, x in c.items()}
        else:
            groups.append(dict(items=[it], centre=v))
    return groups


def signal(group, cfg):
    """Decide with no AI whether a group has earned an AI look, and why."""
    items = group['items']
    sources = {s for i in items for s in [i['src']] + i['also']}
    primary = [i for i in items if i['primary'] and (i['kind'] != 'x' or i.get('over', 0) >= cfg['primary_min_over'])]
    over = max((i.get('over', 0) for i in items), default=0)
    hn = max((i.get('score', 0) for i in items if i['src'] == 'Hacker News'), default=0)
    why = []
    if primary:
        why.append('official post')
    if over >= cfg['breakout_over']:
        why.append('breakout %.1fx' % over)
    if len(sources) >= cfg['min_sources_for_event']:
        why.append('%d sources' % len(sources))
    if hn >= cfg['hn_strong_score']:
        why.append('HN %d' % hn)
    score = 3 * bool(primary) + min(math.log2(over + 1), 4) + min(len(sources), 8) * 0.75 + (hn >= cfg['hn_strong_score'])
    return dict(why=why, score=round(score, 2), sources=sorted(sources), over=over, first=min(i['ts'] for i in items))


# ---------- 3. Claude (the user's subscription through the Claude CLI, no API bill) ----------
def event_text(i, g):
    age_h = (time.time() - g['sig']['first']) / 3600
    lines = ['EVENT %d | first seen %.0f hours ago | sources: %s | signals: %s' % (i, age_h, ', '.join(g['sig']['sources'][:8]), ', '.join(g['sig']['why']))]
    top = sorted(g['items'], key=lambda x: (not x['primary'], -x.get('over', 0), -x.get('score', 0)))[:5]
    for it in top:
        extra = ' [views %s, %sx usual]' % (it['views'], it['over']) if it['kind'] == 'x' else ''
        lines.append('- %s%s: %s' % (it['src'], extra, (it['text'] or it['title'])[:420]))
    return '\n'.join(lines)


def ask_claude(events, cfg):
    rubric = (HERE / 'rubric.md').read_text()
    if cfg.get('look_back_days'):
        rubric += ('\nThis is a look-back over the past %d days to find video topics. Do not lower big_score because an event is days old. '
                   'Score freshness on the scale above, and set shelf_life_days to how many more days from today a video on it would still feel relevant. '
                   'Use 0 and a kill_reason if the moment has passed.\n' % cfg['look_back_days'])
    body = rubric + '\n\nEVENTS:\n\n' + '\n\n'.join(event_text(i, g) for i, g in events)
    with tempfile.TemporaryDirectory() as tmp:
        r = subprocess.run(['claude', '-p', '--model', cfg['ai']['model'], '--output-format', 'json', '--no-session-persistence',
                            '--setting-sources', '', '--tools', '', '--strict-mcp-config'],
                           input=body, capture_output=True, text=True, cwd=tmp, env=clean_env(), timeout=300)
    meta = json.loads(r.stdout)
    if meta.get('is_error'):
        raise RuntimeError(str(meta.get('result'))[:300])
    m = re.search(r'\[.*\]', meta['result'], re.S)
    usage = meta.get('usage', {})
    return json.loads(m.group(0)), usage.get('input_tokens', 0) + usage.get('cache_creation_input_tokens', 0) + usage.get('output_tokens', 0)


def score_events(groups, cfg):
    ranked = sorted((g for g in groups if g['sig']['why']), key=lambda g: -g['sig']['score'])[:cfg['ai']['max_events']]
    events = list(enumerate(ranked, 1))
    results, tokens, size = {}, 0, cfg['ai']['batch_size']
    for s in range(0, len(events), size):
        part = events[s:s + size]
        for attempt in (1, 2):
            try:
                rows, t = ask_claude(part, cfg)
                tokens += t
                results.update({int(r['id']): r for r in rows if 'id' in r})
                break
            except Exception as e:
                print('  AI batch failed (try %d): %s' % (attempt, str(e)[:160]))
    ideas = []
    for i, g in events:
        r = results.get(i)
        if not r:
            continue
        r['group'] = g
        ideas.append(r)
    by_id = {r['id']: r for r in ideas}
    for r in ideas:
        target = by_id.get(r.get('merge_with'))
        if target and target is not r:
            target['group']['items'] = target['group']['items'] + r['group']['items']
            target['group']['sig']['sources'] = sorted(set(target['group']['sig']['sources']) | set(r['group']['sig']['sources']))
            r['merged'] = True
    ideas = [r for r in ideas if not r.get('merged')]
    ideas.sort(key=lambda r: -float(r.get('big_score') or 0))
    return ideas, tokens, len(events)


# ---------- 4. Community reaction from last30days, free sources only ----------
def reaction(title, cfg):
    script = THIRD / 'last30days-skill' / 'skills' / 'last30days' / 'scripts' / 'last30days.py'
    sources = cfg['context']['sources']
    query = ' '.join(title.split()[:7])
    plan = dict(intent='breaking_news', freshness_mode='strict_recent', cluster_mode='story', source_weights={s: 1 for s in sources},
                subqueries=[dict(label='primary', search_query=query, ranking_query='What are people saying about %s?' % title,
                                 sources=sources, weight=1.0)])
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
        json.dump(plan, f)
    try:
        r = subprocess.run([sys.executable, str(script), title, '--quick', '--emit', 'json', '--search', ','.join(sources),
                            '--no-browser-cookies', '--plan', f.name], capture_output=True, text=True, env=clean_env(),
                           timeout=cfg['context']['timeout_s'], cwd=tempfile.gettempdir())
        return json.loads(r.stdout)
    except Exception as e:
        return dict(error=type(e).__name__)
    finally:
        os.unlink(f.name)


def reaction_lines(d):
    if d.get('error'):
        return ['Reaction check failed (%s).' % d['error']]
    rows = d.get('results') or []
    out = []
    for x in rows[:4]:
        title = x.get('title') or x.get('text') or ''
        out.append('- %s: %s %s' % (x.get('source', ''), str(title)[:110], x.get('url', '')))
    return out or ['No matching community posts found.']


# ---------- 5. Report ----------
def report(ideas, counts, status, groups, stats, cfg, out):
    when = datetime.now().strftime('%Y-%m-%d %H:%M')
    L = ['# Idea radar, %s' % when, '', 'Scores are AI judgments to check, not facts. Open the links before trusting any claim.', '']
    alerts = [r for r in ideas if float(r.get('big_score') or 0) >= cfg['alert_score']]
    L += ['**%d ideas at %s or above, out of %d scored.**' % (len(alerts), cfg['alert_score'], len(ideas)), '']
    for r in ideas:
        s = float(r.get('big_score') or 0)
        tag = 'MEGA ' if s >= cfg['mega_score'] else ''
        g = r['group']
        L += ['## %s%s/10: %s' % (tag, r.get('big_score'), r.get('title', '')), '',
              '- **What happened:** %s' % r.get('what_happened', ''),
              '- **Status:** %s. **Category:** %s. **Footage:** %s. **Stays fresh:** about %s days.' % (r.get('status'), r.get('category'), r.get('footage'), r.get('shelf_life_days')),
              '- **Parts:** who %s, mass appeal %s, consequence %s, freshness %s.' % (r.get('who'), r.get('mass_appeal'), r.get('consequence'), r.get('freshness')),
              '- **Why it passed the filter:** %s.' % ', '.join(g['sig']['why'])]
        for label, key in (('Why now', 'why_now'), ('What people miss', 'people_miss'), ('Video angle', 'video_angle'), ('Skip because', 'kill_reason')):
            if r.get(key):
                L.append('- **%s:** %s' % (label, r[key]))
        if r.get('reaction'):
            L += ['- **Community reaction (last30days):**'] + ['  ' + x for x in r['reaction']]
        L.append('- **Sources:**')
        top = sorted(g['items'], key=lambda x: (not x['primary'], -x.get('over', 0), -x.get('score', 0)))[:4]
        L += ['  - %s: %s' % (i['src'], i['url']) for i in top]
        L.append('')
    L += ['## How this run went', '', '| Stage | Count |', '|---|---|', '| Collected | %d |' % counts['collected']]
    for k in ('too old', 'seen before', 'noise words', 'off topic', 'near copy'):
        L.append('| Removed: %s | %d |' % (k, counts[k]))
    L += ['| Left after filters | %d |' % counts['kept'], '| Grouped into events | %d |' % stats['groups'], '| Events with a signal | %d |' % stats['signal'],
          '| Removed: already reported | %d |' % stats.get('known', 0),
          '| Sent to AI | %d |' % stats.get('sent', 0), '| Tokens used | %d |' % stats.get('tokens', 0), '| Run time, seconds | %d |' % stats['secs'], '']
    L += ['**Source results:** ' + '; '.join('%s: %s' % kv for kv in status.items()), '']
    out.write_text('\n'.join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-ai', action='store_true')
    ap.add_argument('--no-context', action='store_true')
    ap.add_argument('--fresh', action='store_true', help='ignore what earlier runs saw')
    ap.add_argument('--days', type=int, help='look back this many days; ignores and does not change the seen list')
    args = ap.parse_args()
    t0 = time.time()
    cfg = json.loads((HERE / 'config.json').read_text())
    if args.days:
        args.fresh = True
        cfg['window_hours'] = args.days * 24
        cfg['look_back_days'] = args.days
        cfg['ai']['max_events'] = 60
    (HERE / 'runs').mkdir(exist_ok=True)
    db = sqlite3.connect(HERE / 'radar.sqlite')
    db.execute('create table if not exists seen (key text primary key, ts real)')
    db.execute('create table if not exists events (id integer primary key, title text, ts real, score real)')
    now = time.time()
    since = datetime.now(timezone.utc) - timedelta(hours=cfg['window_hours'])

    items, status = [], {}
    for handles, primary in ((cfg['x_primary'], True), (cfg['x_watchers'], False)):
        for h in handles:
            got, st = x_page(h, primary, now, now - cfg['window_hours'] * 3600, 6 if args.days else 1)
            items += got
            status['X @' + h] = len(got) if st == 'ok' else st
            time.sleep(0.4)
    # fxtwitter times out now and then on big pages, so give the failed ones one more try.
    for handles, primary in ((cfg['x_primary'], True), (cfg['x_watchers'], False)):
        for h in handles:
            if status['X @' + h] == 'failed':
                time.sleep(5)
                got, st = x_page(h, primary, now, now - cfg['window_hours'] * 3600, 6 if args.days else 1)
                items += got
                status['X @' + h] = len(got) if st == 'ok' else st
    more, st = asyncio.run(horizon_sources(cfg, since, args.days))
    items += more
    status.update(st)
    if args.days:
        hn = hn_back(cfg, since)
        items += hn
        status['hacker news (search)'] = len(hn)

    kept, counts = filters(items, cfg, db, args.fresh, now)
    groups = cluster(kept, cfg)
    for g in groups:
        g['sig'] = signal(g, cfg)
    with_signal = [g for g in groups if g['sig']['why']]
    stats = dict(groups=len(groups), signal=len(with_signal), secs=0)

    # Events already reported in the last 72 hours stay quiet. Known gap: a big update to a reported event can stay quiet too.
    stop = STOP | set(cfg['stopwords_extra'])
    if not args.fresh:
        past = [r[0] for r in db.execute('select title from events where ts>?', (now - 72 * 3600,))]
        if past:
            texts = [words(norm_title(p), stop) for p in past] + [words(' '.join(i['norm'] for i in g['items'][:3]), stop) for g in with_signal]
            vecs = tfidf(texts)
            pv, gv = vecs[:len(past)], vecs[len(past):]
            for g, v in zip(with_signal, gv):
                g['known'] = any(cos(v, p) >= cfg['seen_event_cosine'] for p in pv)
            stats['known'] = sum(1 for g in with_signal if g.get('known'))
            for g in with_signal:
                if g.get('known'):
                    g['sig']['why'] = []

    print('Collected %d, kept %d, events %d, with signal %d, already reported %d' % (counts['collected'], counts['kept'], len(groups), len(with_signal), stats.get('known', 0)))
    print('Removed:', {k: counts[k] for k in ('too old', 'seen before', 'noise words', 'off topic', 'near copy')})
    failed = {k: v for k, v in status.items() if v == 'failed' or str(v).startswith('failed') or v == 0}
    print('Sources with nothing or failed:', failed or 'none')

    ideas = []
    if args.no_ai:
        for g in sorted(with_signal, key=lambda g: -g['sig']['score'])[:cfg['ai']['max_events']]:
            print('%5.2f | %-34s | %s' % (g['sig']['score'], ', '.join(g['sig']['why'])[:34], g['items'][0]['title'][:95]))
    else:
        ideas, tokens, sent = score_events(groups, cfg)
        stats.update(tokens=tokens, sent=sent)
        if not args.no_context:
            for r in [x for x in ideas if float(x.get('big_score') or 0) >= cfg['alert_score']][:cfg['context']['top']]:
                r['reaction'] = reaction_lines(reaction(r.get('title', ''), cfg))
        stats['secs'] = int(time.time() - t0)
        stamp = datetime.now().strftime('%Y-%m-%d_%H%M')
        if args.days:
            stamp = 'back%dd_%s' % (args.days, stamp)
        out = HERE / 'runs' / ('ideas_%s.md' % stamp)
        report(ideas, counts, status, groups, stats, cfg, out)
        slim = [{k: v for k, v in r.items() if k != 'group'} | {'sources': r['group']['sig']['sources'], 'urls': [i['url'] for i in r['group']['items'][:6]]} for r in ideas]
        (HERE / 'runs' / ('ideas_%s.json' % stamp)).write_text(json.dumps(slim, indent=1))
        print('Report:', out)
        for r in ideas[:12]:
            print('%4s | %-13s | %s' % (r.get('big_score'), str(r.get('status'))[:13], str(r.get('title'))[:90]))
        # Remember what was seen only after a successful run, so a failed run can be repeated.
        if ideas and not args.days:
            db.executemany('insert or ignore into seen values (?,?)', [(i['key'], now) for i in kept])
            db.executemany('insert into events (title,ts,score) values (?,?,?)', [(r.get('title', ''), now, float(r.get('big_score') or 0)) for r in ideas])
            db.commit()
    print('Time: %d s' % (time.time() - t0))


if __name__ == '__main__':
    main()
