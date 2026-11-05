"""formats: turn live Outcome markets into post specs (slides for templates/studio.html + a caption draft).

Every builder returns a post: {id, kind, title, slides: [spec, ...], video: spec or None, caption, notes}
Numbers come straight from the market data with a time stamp; nothing is estimated. Captions are drafts: read them.
"""
import json, os, random, time, datetime as dt
import ocdata as od

ROOT = od.ROOT
_TEAMS = None
# fallback colours until assets/teams.json exists (primary, secondary)
FALLBACK = {'Arsenal': ('#EF0107', '#FFFFFF', 'ARS'), 'Manchester City': ('#6CABDD', '#1C2C5B', 'MCI'), 'Chelsea': ('#034694', '#FFFFFF', 'CHE'),
            'Liverpool': ('#C8102E', '#FFFFFF', 'LIV'), 'Tottenham Hotspur': ('#132257', '#FFFFFF', 'TOT'), 'Manchester United': ('#DA291C', '#FBE122', 'MUN'),
            'Barcelona': ('#A50044', '#004D98', 'BAR'), 'FC Barcelona': ('#A50044', '#004D98', 'BAR'), 'Bayern Munich': ('#DC052D', '#FFFFFF', 'FCB'),
            'FC Bayern Munich': ('#DC052D', '#FFFFFF', 'FCB'), 'Real Madrid': ('#FFFFFF', '#00529F', 'RMA'), 'Paris Saint-Germain': ('#004170', '#DA291C', 'PSG'),
            'Paris Saint Germain': ('#004170', '#DA291C', 'PSG'), 'Inter Milan': ('#0068A8', '#000000', 'INT'), 'Atletico Madrid': ('#CB3524', '#272E61', 'ATM'),
            'Juventus': ('#000000', '#FFFFFF', 'JUV'), 'Borussia Dortmund': ('#FDE100', '#000000', 'BVB'), 'Napoli': ('#12A0D7', '#FFFFFF', 'NAP'),
            'AC Milan': ('#FB090B', '#000000', 'MIL'), 'AS Roma': ('#8E1F2F', '#F0BC42', 'ROM'), 'Aston Villa': ('#670E36', '#95BFE5', 'AVL'),
            'Galatasaray': ('#A90432', '#FDB912', 'GAL'), 'Fenerbahce': ('#163962', '#FFED00', 'FEN'), 'LOSC Lille': ('#E01E13', '#20325F', 'LIL'),
            'Club Brugge': ('#0E5AA7', '#000000', 'BRU'), 'RB Leipzig': ('#DD0741', '#FFFFFF', 'RBL'), 'PSV Eindhoven': ('#ED1C24', '#FFFFFF', 'PSV'),
            'Villarreal CF': ('#FFE667', '#005187', 'VIL'), 'Viking': ('#003B7A', '#FFFFFF', 'VIK'), 'RC Lens': ('#EC1C24', '#FFE500', 'RCL'),
            'Sporting CP': ('#008057', '#FFFFFF', 'SCP'), 'Sabah Baku': ('#0057B8', '#FFFFFF', 'SAB'), 'SK Slavia Praha': ('#E30613', '#FFFFFF', 'SLA'),
            'Feyenoord': ('#E00000', '#FFFFFF', 'FEY'), 'Como': ('#1C3F94', '#FFFFFF', 'COM'), 'LASK Linz': ('#000000', '#FFFFFF', 'LSK'),
            'FC Shakhtar Donetsk': ('#F26522', '#000000', 'SHA'), 'AEK Athens': ('#FFD700', '#000000', 'AEK'), 'FK Bodo/Glimt': ('#FFD200', '#000000', 'BOD'),
            'Real Betis': ('#00954C', '#FFFFFF', 'BET'), 'FC Porto': ('#00428C', '#FFFFFF', 'POR'), 'Slovan Bratislava': ('#5BB3E5', '#FFFFFF', 'SLO'),
            'VfB Stuttgart': ('#E32219', '#FFFFFF', 'VFB'), 'Benfica': ('#E20E0E', '#FFFFFF', 'BEN')}


def teams():
    global _TEAMS
    if _TEAMS is None:
        _TEAMS = {}
        p = os.path.join(ROOT, 'assets', 'teams.json')
        if os.path.exists(p):
            data = json.load(open(p, encoding='utf-8'))
            rows = data if isinstance(data, list) else data.get('teams', [])
            for t in rows:
                for n in [t.get('name')] + list(t.get('aliases') or []):
                    if n: _TEAMS[n.lower()] = t
    return _TEAMS


# house colour picks that read better on a full-bleed split than the reference data (club identity colours)
OVERRIDE = {'AS Roma': ('#8E1F2F', '#F0BC42'), 'Real Madrid': ('#FFFFFF', '#00529F'), 'Juventus': ('#111111', '#FFFFFF'),
            'Tottenham Hotspur': ('#FFFFFF', '#132257'), 'Inter Milan': ('#0068A8', '#111111')}


def team(name):
    t = teams().get((name or '').lower())
    if t:
        c1, c2 = OVERRIDE.get(t.get('name'), OVERRIDE.get(name, (t.get('primary') or t.get('c1'), t.get('secondary') or t.get('c2'))))
        return {'name': name, 'short': t.get('short') or od.short(name), 'code': t.get('code'), 'c1': c1, 'c2': c2, 'country': t.get('country')}
    fb = FALLBACK.get(name)
    return {'name': name, 'short': od.nick(name) if name not in od.SHORT else od.short(name), 'code': fb[2] if fb else None,
            'c1': fb[0] if fb else None, 'c2': fb[1] if fb else None}


def _rgb(h):
    h = (h or '#777777').lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) if len(h) == 6 else (120, 120, 120)


def pair(A, B):
    """two sides of a split: when the main colours clash, the second side switches to its other colour (or white / black)"""
    dist = lambda x, y: sum((p - q) ** 2 for p, q in zip(_rgb(x), _rgb(y))) ** .5
    if dist(A['c1'], B['c1']) < 140:
        alt = B.get('c2') if B.get('c2') and dist(A['c1'], B['c2']) >= 140 else ('#FFFFFF' if sum(_rgb(A['c1'])) < 380 else '#111111')
        B = dict(B, c1=alt, c2=B['c1'] if dist(alt, B['c1']) > 140 else ('#111111' if sum(_rgb(alt)) > 380 else '#FFFFFF'))
    return A, B


def person(name):
    """players and candidates: initials chip (a flag can be added once assets/players.json has nationalities)"""
    parts = [w for w in (name or '?').replace('-', ' ').split() if w[:1].isalpha()]
    code = ''.join(w[0] for w in parts[:2]).upper() or '?'
    pl = {}
    pp = os.path.join(ROOT, 'assets', 'players.json')
    if os.path.exists(pp):
        data = json.load(open(pp, encoding='utf-8')); rows = data if isinstance(data, list) else data.get('players', [])
        pl = next((x for x in rows if (x.get('name') or '').lower() == (name or '').lower()), {}) or {}
    return {'name': name, 'short': pl.get('short') or name, 'code': code, 'c1': '#2A2F3A', 'c2': '#D4FF3A', 'country': pl.get('nationality') or pl.get('country')}


def entity(label, kind):
    return person(label) if kind == 'person' else team(label)


def a_an(n):
    """'an 18%', 'a 62%': spoken numbers starting with 8, 11, 18, 80-89 take 'an'"""
    n = int(round(n))
    return 'an' if (str(n).startswith('8') or n in (11, 18)) else 'a'


def real_rows(m):
    return [r for r in m['outcomes'] if r['label'] not in ('Other',) and r.get('p') is not None]


def brand():
    return json.load(open(os.path.join(ROOT, 'brand.json'), encoding='utf-8'))


def tz():
    b = brand(); z = b.get('tz') or {'label': 'CEST', 'offset': 2}
    return z['label'], z['offset']


def stamp(now=None):
    now = now or dt.datetime.now(dt.timezone.utc)
    return now.strftime('%d %b %Y, %H:%M UTC').lstrip('0')


def ko(start):
    s = od.when(start)
    if not s: return ''
    lab, off = tz()
    return (s + dt.timedelta(hours=off)).strftime('%H:%M ') + lab


def dayname(start):
    s = od.when(start); lab, off = tz()
    return (s + dt.timedelta(hours=off)).strftime('%a %d %b').replace(' 0', ' ') if s else ''


def cta(**kw):
    return dict({'fmt': 'cta'}, **kw)


def _post(pid, kind, title, slides, caption, video=None, notes=''):
    return {'id': pid, 'kind': kind, 'title': title, 'slides': slides, 'video': video, 'caption': caption, 'notes': notes}


def _tags(*extra):
    return ' '.join(extra)


def risk_line():
    b = brand(); return b.get('risk', '')


# ---------------------------------------------------------------- L1 matchday card
def matchday(ms, comp='UEFA Champions League', day=None, title=None, pid=None):
    games = [m for m in ms if m['kind'] == 'match3' and m.get('comp') == comp and m['ok'] and (not day or (m.get('start') or '').startswith(day))]
    games.sort(key=lambda m: (m['start'], -max(m['outcomes'][0]['p'], m['outcomes'][2]['p'])))
    if not games: return None
    rows = []
    for m in games:
        h, d, a = m['outcomes']
        rows.append({'home': team(h['label']), 'away': team(a['label']), 'ph': h['p'], 'pd': d['p'], 'pa': a['p'], 'ko': ko(m['start']), 'key': m['key']})
    fav = [max(r['ph'], r['pa']) for r in rows]
    safest = fav.index(max(fav))
    flip = min(range(len(rows)), key=lambda i: abs(rows[i]['ph'] - rows[i]['pa']))
    # upset watch: the strongest favourite whose underdog still has 10%+ (a real shot)
    upset = max((i for i in range(len(rows)) if min(rows[i]['ph'], rows[i]['pa']) >= .1 and i not in (safest, flip)),
                key=lambda i: fav[i], default=None)
    short = {'UEFA Champions League': 'Champions League', 'UEFA Europa League': 'Europa League'}.get(comp, comp)
    when = dayname(games[0]['start'])
    lab, off = tz(); today = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=off)).strftime('%a %d %b').replace(' 0', ' ')
    head = title or ("Tonight's *%s*" % short if when == today else "%s's *%s*" % (od.when(games[0]['start']).strftime('%A'), short))
    per = 5; pages = [list(range(i, min(i + per, len(rows)))) for i in range(0, len(rows), per)]
    slides = []
    for k, idx in enumerate(pages):
        loc = lambda g: idx.index(g) if g in idx else None
        slides.append({'fmt': 'matchday', 'title': head + (' (%d/%d)' % (k + 1, len(pages)) if len(pages) > 1 else ''),
                       'sub': 'Chance to win, priced by real money on Outcome. %s' % when, 'games': [rows[i] for i in idx],
                       'safest': loc(safest), 'flip': loc(flip), 'upset': loc(upset), 'label': when})
    spec = slides[0]
    sf, fl = rows[safest], rows[flip]
    sfn = sf['home']['short'] if sf['ph'] > sf['pa'] else sf['away']['short']
    cap = ('%s %s, priced by real money \U0001F440\n\nSafest call: %s at %s. Coin flip: %s v %s.\nWhich one goes wrong tonight?\n\n'
           'Chances from Outcome.xyz market prices at %s. %s\n%s' % (short, when, sfn, '%d%%' % round(100 * max(sf['ph'], sf['pa'])),
                                                                        fl['home']['short'], fl['away']['short'], stamp(), risk_line(),
                                                                        _tags('#championsleague' if 'Champions' in comp else '#europaleague', '#football', '#ucl' if 'Champions' in comp else '#uel')))
    vid = dict(slides[0], games=rows, safest=safest, flip=flip, upset=upset, title=head)
    return _post(pid or 'matchday_%s' % (day or 'next'), 'matchday', '%s %s' % (short, when), slides + [cta()], cap, video=vid)


# ---------------------------------------------------------------- L2 pick a side
def pick(m, facts=None, pid=None):
    h, d, a = m['outcomes'] if m['kind'] == 'match3' else (m['outcomes'][0], None, m['outcomes'][1])
    A, B = pair(team(h['label']), team(a['label']))
    q = {'fmt': 'split_q', 'teams': [A, B], 'line': '%s or %s?' % (A['short'], B['short']), 'when': ('%s %s' % (dayname(m['start']).split(' ')[0], ko(m['start']).split(' ')[0])) if m.get('start') else '',
         'prompt': "Pick a side. The money's answer is on the last slide"}
    slides = [q]
    facts = facts or {}
    for t in (A, B):
        f = facts.get(t['name']) or facts.get(t['short'])
        if f: slides.append({'fmt': 'pick_facts', 'team': t, 'facts': f['facts'], 'factSource': f.get('source', '')})
    rv = {'fmt': 'split_reveal', 'teams': [A, B], 'ph': h['p'], 'pd': d['p'] if d else None, 'pa': a['p'], 'stamp': stamp()}
    slides += [rv, cta(line1='Think you can *call it*?')]
    cap = ('%s or %s? ⚔️\n\nPick a side before you swipe. The money\'s answer is on the last slide.\n\n'
           'Chances from Outcome.xyz at %s. %s\n%s' % (A['short'], B['short'], stamp(), risk_line(), _tags('#football', '#championsleague')))
    video = dict(q, fmt='split_video', ph=h['p'], pd=d['p'] if d else None, pa=a['p'], stamp=stamp())
    return _post(pid or 'pick_%s' % m['key'], 'pick', '%s v %s' % (A['short'], B['short']), slides, cap, video=video)


# ---------------------------------------------------------------- L3 race swing
def swing(m, names, days=9, title=None, sub=None, pid=None, colors=('lime', 'pink', 'cyan')):
    end = int(time.time() * 1000); start = end - days * 86400 * 1000
    series, deltas = [], []
    for i, nm in enumerate(names):
        r = next((r for r in m['outcomes'] if r['label'] == nm), None)
        if not r: continue
        rows = od.candles(r['coin'], '1d', start, end)
        pts = [[c[0], c[4]] for c in rows]
        if r.get('p') is not None and pts: pts[-1][1] = r['p']                 # today's point = the live mid
        if len(pts) < 2: continue
        series.append({'label': nm, 'color': colors[i % len(colors)], 'pts': pts})
        deltas.append({'label': od.short(nm), 'from': pts[0][1], 'to': pts[-1][1], 'span': 'in %d days' % (len(pts) - 1)})
        time.sleep(.3)
    if not series: return None
    t0 = series[0]['pts'][0][0]; t1 = series[0]['pts'][-1][0]
    xl = [[t0, time.strftime('%d %b', time.gmtime(t0 / 1000)).lstrip('0')], [t1, 'Now']]
    lead = deltas[0]
    title = title or '%s *%d%%* → *%d%%*' % (lead['label'].upper(), round(100 * lead['from']), round(100 * lead['to']))
    spec = {'fmt': 'swing', 'title': title, 'sub': sub or '%s chance on Outcome, last %d days' % (m.get('short') or m['title'], days),
            'series': series, 'deltas': deltas[:2], 'xLabels': xl, 'yMin': 0, 'label': m.get('short') or ''}
    cap = ('%s\n\n%s\nThe money moved fast this week. Who wins it?\n\nChances from Outcome.xyz daily prices to %s. %s\n%s'
           % ((m.get('short') or m['title']), '\n'.join('%s: %d%% → %d%%' % (x['label'], round(100 * x['from']), round(100 * x['to'])) for x in deltas),
              stamp(), risk_line(), _tags('#ballondor' if 'Ballon' in (m.get('title') or '') else '#football', '#football')))
    return _post(pid or 'swing_%s' % m['key'], 'swing', title, [spec, cta()], cap, video=dict(spec, dur=7))


# ---------------------------------------------------------------- L4 guess the %
def _options(p, seed):
    """three choices with the real one at a random position (low, middle or high), so the quiz cannot be gamed"""
    rnd = random.Random(seed); real = max(1, min(99, round(100 * p)))
    for _ in range(300):
        pos = rnd.choice([0, 1, 2]); step = rnd.choice([12, 15, 20, 25])
        cand = []
        for i in range(3):
            if i == pos: cand.append(real)
            else: cand.append(int(round((real + (i - pos) * step + rnd.choice([-3, 0, 3])) / 5.0) * 5))
        if all(1 <= c <= 99 for c in cand) and len(set(cand)) == 3 and min(abs(a - b) for a in cand for b in cand if a != b) >= 8:
            return ['%d%%' % c for c in cand]
    return ['%d%%' % real]


def quiz(items, part=1, pid=None):
    """items: [{'q': question text, 'p': chance, 'team': team dict or None, 'context': str}]"""
    n = len(items)
    slides = [{'fmt': 'quiz_cover', 'part': part, 'preview': [x['q'] for x in items[:3]]}]
    for i, x in enumerate(items):
        slides.append({'fmt': 'quiz_q', 'idx': i + 1, 'n': n, 'q': x['q'], 'context': x.get('context', ''), 'team': x.get('team'), 'team2': x.get('team2'),
                       'options': _options(x['p'], x['q'])})
    slides.append({'fmt': 'quiz_answers', 'items': [{'q': x['q'], 'p': x['p']} for x in items]})
    slides.append(cta(line1='How many did you *get*?'))
    cap = ('Guess the %% \U0001F9E0 Part %d\n\nWhat chance does real money give each of these? Comment your score out of %d.\n\n'
           'Answers from Outcome.xyz market prices at %s. %s\n%s' % (part, n, stamp(), risk_line(), _tags('#quiz', '#football', '#guessthe')))
    return _post(pid or 'quiz_part%d' % part, 'quiz', 'Guess the %% part %d' % part, slides, cap)


# ---------------------------------------------------------------- L5 the market says
def change_24h(coin_, hours=24):
    end = int(time.time() * 1000); rows = od.candles(coin_, '1h', end - hours * 3600 * 1000, end)
    return (rows[0][1] if rows else None), rows


def breaking(m, label, headline, note='', kicker='Market update', pid=None, days=7):
    r = next(r for r in m['outcomes'] if r['label'] == label)
    end = int(time.time() * 1000)
    daily = od.candles(r['coin'], '1d', end - days * 86400 * 1000, end)
    first24, _ = change_24h(r['coin'])
    delta = (r['p'] - first24) if first24 is not None else None
    pts = [[c[0], c[4]] for c in daily]
    if pts: pts[-1][1] = r['p']
    xl = [[pts[0][0], time.strftime('%d %b', time.gmtime(pts[0][0] / 1000)).lstrip('0')], [pts[-1][0], 'Now']] if len(pts) > 1 else None
    spec = {'fmt': 'breaking', 'kicker': kicker, 'headline': headline, 'p': r['p'], 'delta': delta, 'series': pts if len(pts) > 2 else None,
            'xLabels': xl, 'note': note, 'down': False}
    cap = ('%s\n\n%s\n\nFrom Outcome.xyz market prices at %s. Not financial advice. %s\n%s'
           % (headline.replace('*', '').replace('^', ''), note.replace('*', '').replace('^', ''), stamp(), risk_line(), _tags('#markets', '#finance')))
    return _post(pid or 'breaking_%s' % m['key'], 'breaking', headline, [spec, cta()], cap, video=dict(spec))


# ---------------------------------------------------------------- L6 tier list
def tier(m, title=None, sub=None, cuts=(('S', .2), ('A', .1), ('B', .05), ('C', 0)), pid=None):
    tiers = [{'name': n, 'items': []} for n, _ in cuts]
    kind = 'person' if 'Ballon' in (m.get('title') or '') else 'team'
    for r in real_rows(m):
        for (n, lo), t in zip(cuts, tiers):
            if r['p'] >= lo: t['items'].append({'team': entity(r['label'], kind), 'p': r['p']}); break
    spec = {'fmt': 'tier', 'title': title or '%s, *ranked by real money*' % (m.get('short') or m['title']), 'sub': sub or 'Tier = the chance traders give each one', 'tiers': tiers}
    cap = ('%s tier list, set by real money \U0001F4CA\n\nWho is too high? Who is too low?\n\nChances from Outcome.xyz at %s. %s\n%s'
           % (m.get('short') or m['title'], stamp(), risk_line(), _tags('#football', '#tierlist')))
    return _post(pid or 'tier_%s' % m['key'], 'tier', spec['title'], [spec, cta()], cap, video=dict(spec))


# ---------------------------------------------------------------- L7 probability ladder
def ladder(rungs, title, sub, note='', label='Price map', pid='ladder', caption=None, labelW=None):
    spec = {'fmt': 'ladder', 'title': title, 'sub': sub, 'rungs': rungs, 'note': note, 'label': label, 'labelW': labelW}
    cap = caption or ('%s\n\n%s\n\nFrom Outcome.xyz market prices at %s. Not financial advice. %s' % (title.replace('*', ''), sub.replace('*', ''), stamp(), risk_line()))
    return _post(pid, 'ladder', title, [spec, cta()], cap, video=dict(spec))


def ladder_touch(ms, asset='BTC', pid=None):
    rows = sorted([m for m in ms if m['kind'] == 'touch' and m.get('asset') == asset and m['ok']], key=lambda m: -m['target'])
    if not rows: return None
    mids = od.load_mids(); now_px = float(mids.get(asset, 0) or 0)
    rungs = []
    for m in rows:
        if now_px and m['target'] < now_px and not any(r.get('now') for r in rungs):
            rungs.append({'label': '$%s' % format(int(now_px), ','), 'now': True})
        rungs.append({'label': ('$%s' % format(int(m['target']), ',')), 'p': m['outcomes'][0]['p']})
    nm = rows[0].get('asset_name') or asset
    dl = od.when(rows[0]['deadline']); dls = dl.strftime('%d %b').lstrip('0') if dl else ''
    return ladder(rungs, 'Where does *%s* go by %s?' % (nm, dls), 'Chance %s touches each price before %s. It trades at $%s now.' % (nm, dls, format(int(now_px), ',')),
                  pid=pid or 'ladder_%s' % asset.lower(), label='%s targets' % nm)


def ladder_ipo(ms, company='Anthropic', pid=None):
    rows = sorted([m for m in ms if m['kind'] == 'ipo_cap' and m['comp'] == company and m['ok']], key=lambda m: -m['threshold_b'])
    if not rows: return None
    rungs = [{'label': '$%gT' % (m['threshold_b'] / 1000) if m['threshold_b'] >= 1000 else '$%gB' % m['threshold_b'], 'p': m['outcomes'][0]['p']} for m in rows]
    conf = [m for m in ms if m['kind'] == 'ipo_confirm' and m['comp'] == company and m['ok']]
    note = ' '.join('IPO confirmed by %s: *%s*.' % (od.when(m['deadline']).strftime('%d %b').lstrip('0'), '%d%%' % round(100 * m['outcomes'][0]['p'])) for m in conf if od.when(m['deadline']))
    return ladder(rungs, '%s\'s first-day value: *what the money says*' % company, 'Chance %s is worth more than each level on its first trading day' % company,
                  note=note, pid=pid or 'ladder_ipo_%s' % company.lower(), label='IPO watch', labelW=230)


# ---------------------------------------------------------------- price tags, the number, cheapest dreams, ranking
def pricetags(m, title=None, sub=None, pid=None, n=8):
    kind = 'person' if 'Ballon' in (m.get('title') or '') else 'team'
    items = [{'team': entity(r['label'], kind), 'p': r['p']} for r in real_rows(m)[:n]]
    spec = {'fmt': 'pricetags', 'title': title or 'What it costs to *believe*', 'sub': sub or (m.get('short') or m['title']), 'items': items}
    last = items[-1]
    cap = ('What it costs to believe \U0001F3F7️ %s\n\nA YES share pays $1 if it happens, so the price is the chance. %s cost %s.\nWhich one is a bargain?\n\n'
           'Prices from Outcome.xyz at %s. %s\n%s' % (m.get('short') or m['title'], last['team']['short'], '%d cents' % round(100 * last['p']), stamp(), risk_line(), _tags('#football', '#premierleague')))
    return _post(pid or 'tags_%s' % m['key'], 'pricetags', spec['title'], [spec, cta()], cap, video=dict(spec))


def number(p, line, sub='', kicker='The number', pid='number', caption=None):
    spec = {'fmt': 'number', 'big': '%d%%' % round(100 * p), 'bigValue': round(100 * p), 'line': line, 'sub': sub, 'kicker': kicker}
    cap = caption or ('%d%%. %s\n\n%s\n\nFrom Outcome.xyz market prices at %s. %s' % (round(100 * p), line.replace('*', ''), sub.replace('*', ''), stamp(), risk_line()))
    return _post(pid, 'number', line, [spec], cap, video=dict(spec))


def cheapest(items, title=None, sub=None, pid='cheapest'):
    spec = {'fmt': 'cheapest', 'title': title or 'The cheapest *dreams* on the board', 'sub': sub or 'A YES share pays $1 if it happens. These cost pennies.', 'items': items}
    cap = ('The cheapest dreams on the board \U0001F4AD\n\n%s\n\nWhich one actually happens?\n\nPrices from Outcome.xyz at %s. %s'
           % ('\n'.join('%s: %s' % (x['text'].replace('*', ''), '%d cents' % max(1, round(100 * x['p']))) for x in items), stamp(), risk_line()))
    return _post(pid, 'cheapest', spec['title'], [spec, cta()], cap, video=dict(spec))


def ranking(m, title=None, sub=None, n=6, pid=None):
    kind = 'person' if 'Ballon' in (m.get('title') or '') else 'team'
    items = [{'label': od.short(r['label']), 'team': entity(r['label'], kind), 'p': r['p']} for r in real_rows(m)[:n]]
    spec = {'fmt': 'ranking', 'title': title or '%s: *the favourites*' % (m.get('short') or m['title']), 'sub': sub or 'Ranked by the chance real money gives each one', 'items': items}
    cap = ('%s favourites, ranked by real money\n\n%s\n\nChances from Outcome.xyz at %s. %s'
           % (m.get('short') or m['title'], '\n'.join('%d. %s %d%%' % (i + 1, x['label'], round(100 * x['p'])) for i, x in enumerate(items)), stamp(), risk_line()))
    return _post(pid or 'rank_%s' % m['key'], 'ranking', spec['title'], [spec, cta()], cap, video=dict(spec))


# ---------------------------------------------------------------- cheapest dreams picker
COMP_SHORT = {'English Premier League': 'Premier League', 'UEFA Champions League': 'Champions League', 'USA National Football League (NFL)': 'Super Bowl',
              'NBA': 'NBA title', 'MLB Championship': 'World Series'}


def pick_cheapest(ms, n=6, lo=.003, hi=.06):
    """the lowest-priced real outcomes: season long shots plus the biggest underdogs of the next 48 hours"""
    now = dt.datetime.now(dt.timezone.utc); season, games = [], []
    for m in ms:
        if not m['ok']: continue
        if m['kind'] == 'winner':
            comp = COMP_SHORT.get((m.get('comp') or '').strip(), m.get('comp') or '')
            for r in real_rows(m):
                if lo <= r['p'] <= hi:
                    if 'Ballon' in (m.get('title') or ''):
                        season.append({'text': "%s wins the *Ballon d'Or*" % r['label'], 'p': r['p'], 'team': person(r['label'])})
                    else:
                        season.append({'text': '%s win the *%s*' % (team(r['label'])['short'], comp), 'p': r['p'], 'team': team(r['label'])})
        elif m['kind'] in ('match3', 'game2') and m.get('start'):
            s = od.when(m['start'])
            if not s or not (now <= s <= now + dt.timedelta(hours=48)): continue
            sides = [m['outcomes'][0], m['outcomes'][-1]]
            dog, fav = sorted(sides, key=lambda r: r['p'])
            if dog['p'] <= .12:
                games.append({'text': '%s beat *%s* (%s)' % (team(dog['label'])['short'], team(fav['label'])['short'], dayname(m['start']).split(' ')[0]),
                              'p': dog['p'], 'team': team(dog['label'])})
    season.sort(key=lambda x: -x['p']); games.sort(key=lambda x: x['p'])
    k = min(len(games), n // 2)
    out = games[:k] + season[:n - k]
    return sorted(out, key=lambda x: x['p'])


# ---------------------------------------------------------------- originals: Fake vs Real, Upset Radar
def fakereal(ms, claim, market, outcome_label, line='', note='', claim_note='Seen on social media, ' , stamp_text='NOT YET', pid=None, **_):
    """counter a viral false claim with the real chance; `claim` must quote a claim that is really circulating (say where in claim_note)"""
    import ocs
    m = ocs.find(ms, market); r = ocs.outcome(m, outcome_label)
    kind = 'person' if 'Ballon' in (m.get('title') or '') else 'team'
    spec = {'fmt': 'fakereal', 'claim': claim, 'claimNote': claim_note, 'stamp_text': stamp_text, 'p': r['p'], 'entity': entity(r['label'], kind),
            'line': line or 'chance for %s on Outcome' % (od.short(r['label'])), 'note': note}
    cap = ('The internet says: %s\nThe money says: %d%%.\n\n%s\n\nChance from Outcome.xyz market prices at %s. %s'
           % (claim.replace('*', '').replace('^', ''), round(100 * r['p']), note.replace('*', '').replace('^', ''), stamp(), risk_line()))
    return _post(pid or 'fakereal_%s' % m['key'], 'fakereal', claim, [spec, cta(line1='Check the *money*, not the rumours')], cap, video=dict(spec))


def radar_items(ms, day, comp=None, n=3):
    rows = []
    for m in ms:
        if m['kind'] != 'match3' or not m['ok'] or not (m.get('start') or '').startswith(day): continue
        if comp and m.get('comp') != comp: continue
        h, d_, a = m['outcomes']
        fav, dog = (h, a) if h['p'] >= a['p'] else (a, h)
        if fav['p'] < .55: continue                                   # a real favourite, so an underdog win is an upset
        rows.append({'dog': team(dog['label']), 'fav': team(fav['label']), 'p': dog['p'], 'key': m['key'],
                     'when': '%s, %s' % (dayname(m['start']).split(' ')[0], ko(m['start']))})
    rows.sort(key=lambda x: -x['p'])
    return rows[:n]


def radar(ms, day, comp=None, n=3, pid=None, **_):
    items = radar_items(ms, day, comp, n)
    if not items: return None
    spec = {'fmt': 'radar', 'title': 'Upset *radar*', 'sub': 'The underdogs the money gives the best shot tonight', 'items': items}
    cap = ('Upset radar \U0001F4E1\n\n%s\n\nWill any of them land? Results tomorrow.\n\nChances from Outcome.xyz at %s. %s\n#championsleague #football'
           % ('\n'.join('%s to beat %s: %d%%' % (x['dog']['short'], x['fav']['short'], round(100 * x['p'])) for x in items), stamp(), risk_line()))
    return _post(pid or 'radar_%s' % day, 'radar', 'Upset radar', [spec, cta()], cap, video=dict(spec),
                 notes='Keep this batch file: the callback post reads the same games after full time (recipe radar_result).')


def radar_result(ms, keys, pid=None, **_):
    """the callback: same games, with the results from ESPN (needs the archive to have seen them)"""
    import postmatch
    items, hits = [], 0
    for k in keys:
        a = postmatch.analyse(k)
        if not a or not a.get('espn') or not a['espn'].get('final'): continue
        pre = a['pre']; fav = max((a['home'], a['away']), key=lambda l: pre.get(l) or 0); dog = a['away'] if fav == a['home'] else a['home']
        ev = a['espn']; hit = a.get('winner') == dog; hits += hit
        items.append({'dog': team(dog), 'fav': team(fav), 'p': pre.get(dog) or 0, 'hit': hit,
                      'result': '%s %d-%d %s' % (team(a['home'])['short'], ev['home'], ev['away'], team(a['away'])['short'])})
    if not items: return None
    spec = {'fmt': 'radar', 'title': 'Upset radar: *the results*', 'sub': 'Last night\'s underdogs, and what happened', 'items': items,
            'score': '*%d* of %d hit' % (hits, len(items))}
    cap = ('Upset radar, the results: %d of %d hit\n\n%s\n\nPre-match chances from Outcome.xyz. %s'
           % (hits, len(items), '\n'.join('%s (%d%%): %s' % (x['dog']['short'], round(100 * x['p']), 'happened' if x['hit'] else x['result']) for x in items), risk_line()))
    return _post(pid or 'radar_result', 'radar', 'Upset radar results', [spec, cta()], cap, video=dict(spec))


# ---------------------------------------------------------------- chance race (bar chart race)
PALETTE = ['#D4FF3A', '#22E1FF', '#FFC83D', '#FF2E88', '#B28CFF', '#FF8A3D', '#7CFFB2', '#F4F5F7']


def barrace(ms, market, days=30, n=6, title=None, sub=None, pid=None, **_):
    import ocs
    m = ocs.find(ms, market)
    if not m: return None
    kind = 'person' if 'Ballon' in (m.get('title') or '') else 'team'
    end = int(time.time() * 1000); start = end - days * 86400000
    series = {}
    for r in real_rows(m)[:n]:
        rows = od.candles(r['coin'], '1d', start, end)
        if rows: series[r['label']] = {c[0] // 86400000: c[4] for c in rows}
        time.sleep(.25)
    if len(series) < 3: return None
    dkeys = sorted(set(k for v in series.values() for k in v))
    items = []
    for i, (lab, v) in enumerate(series.items()):
        vals, last = [], None
        for k in dkeys:
            last = v.get(k, last); vals.append(last if last is not None else 0)
        live = next((r['p'] for r in m['outcomes'] if r['label'] == lab), None)
        if live is not None: vals[-1] = live
        items.append({'team': entity(lab, kind), 'v': vals, 'color': PALETTE[i % len(PALETTE)]})
    day_lab = [dt.datetime.fromtimestamp(k * 86400, dt.timezone.utc).strftime('%d %b').lstrip('0') for k in dkeys]
    span = len(dkeys)
    nice = {'English Premier League winner': 'The Premier League *title race*', 'UEFA Champions League winner': 'The Champions League *race*',
            "Ballon d'Or": "The Ballon d'Or *race*", 'USA National Football League (NFL) winner': 'The Super Bowl *race*', 'NBA winner': 'The NBA title *race*'}
    spec = {'fmt': 'barrace', 'title': title or nice.get((m.get('short') or '').strip(), '%s: *the race*' % (m.get('short') or m['title'])), 'sub': sub or 'Chance on Outcome, every day for the last %d days' % span,
            'items': items, 'days': day_lab, 'dur': max(8, min(16, span * .45))}
    final = sorted(items, key=lambda x: -x['v'][-1])
    cap = ('%s, the race so far \U0001F3C1\n\n%s\n\nDaily chances from Outcome.xyz, %s to %s. %s'
           % (m.get('short') or m['title'], '\n'.join('%s: %d%% \u2192 %d%%' % (x['team']['short'], round(100 * x['v'][0]), round(100 * x['v'][-1])) for x in final[:4]),
              day_lab[0], day_lab[-1], risk_line()))
    return _post(pid or 'race_%s' % m['key'], 'barrace', spec['title'], [dict(spec)], cap, video=dict(spec))
