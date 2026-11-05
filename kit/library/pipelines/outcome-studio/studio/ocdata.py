"""ocdata: read Outcome / Hyperliquid market data and turn it into clean, titled markets.

Sources (all public, no key; see research/15-data-triggers.md):
  Hyperliquid info API  POST https://api.hyperliquid.xyz/info   outcomeMeta, allMids, candleSnapshot, l2Book, userFillsByTime
  Outcome API           https://o1.outcome.xyz/api/v1           leaderboard, profile/lookup, portfolio/lookup, markets/lookup,
                                                                 markets/series, outcomes/settled, top-movers, sports live
Coin id of an outcome side = '#' + (10 * outcome id + side); side 0 = Yes (or participant A), side 1 = No (or B).
Price = chance: a mid of 0.663 = 66.3%. A mid of exactly 0.5 with no book is a placeholder: never publish it.
"""
import json, os, re, time, urllib.request, datetime as dt

ROOT = os.path.dirname(os.path.abspath(__file__))
HL = 'https://api.hyperliquid.xyz/info'
O1 = 'https://o1.outcome.xyz/api/v1'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
_last_o1 = [0.0]


def _req(url, body=None, timeout=30, tries=3):
    for i in range(tries):
        try:
            data = json.dumps(body).encode() if body is not None else None
            r = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json', 'User-Agent': UA})
            return json.load(urllib.request.urlopen(r, timeout=timeout))
        except Exception as e:
            if i == tries - 1: raise
            time.sleep(2 + 3 * i)


def hl(body):
    return _req(HL, body)


def o1(path, body=None):
    """Outcome API, kept under its 60 requests a minute limit"""
    wait = 1.1 - (time.time() - _last_o1[0])
    if wait > 0: time.sleep(wait)
    _last_o1[0] = time.time()
    return _req(O1 + path, body)


def desc(s):
    """'a:1|b:2' -> {'a': '1', 'b': '2'} (split on |, then on the first :)"""
    out = {}
    for part in (s or '').split('|'):
        if ':' in part:
            k, v = part.split(':', 1); out[k.strip()] = v.strip()
    return out


def when(s):
    """'20261013-1900' (UTC) -> aware datetime"""
    try: return dt.datetime.strptime(s, '%Y%m%d-%H%M').replace(tzinfo=dt.timezone.utc)
    except Exception: return None


def coin(oid, side=0):
    return '#%d' % (10 * int(oid) + side)


# short display names for clubs and players (long official names read badly on a phone)
SHORT = {'Paris Saint-Germain': 'PSG', 'Paris Saint Germain': 'PSG', 'FC Bayern Munich': 'Bayern', 'Bayern Munich': 'Bayern',
         'FC Barcelona': 'Barcelona', 'LOSC Lille': 'Lille', 'Manchester United': 'Man United', 'Manchester City': 'Man City',
         'Tottenham Hotspur': 'Spurs', 'Borussia Dortmund': 'Dortmund', 'Club Brugge': 'Club Brugge', 'Inter Milan': 'Inter',
         'Atletico Madrid': 'Atletico', 'RB Leipzig': 'Leipzig', 'PSV Eindhoven': 'PSV', 'FC Porto': 'Porto',
         'Sporting CP': 'Sporting', 'RC Lens': 'Lens', 'AS Roma': 'Roma', 'FK Bodo/Glimt': 'Bodo/Glimt', 'Bodo/Glimt': 'Bodo/Glimt',
         'SK Slavia Praha': 'Slavia Praha', 'Slovan Bratislava': 'Slovan', 'VfB Stuttgart': 'Stuttgart', 'Villarreal CF': 'Villarreal',
         'FC Shakhtar Donetsk': 'Shakhtar', 'Olympique de Marseille': 'Marseille', 'Olympique Lyonnais': 'Lyon',
         'Bayer Leverkusen': 'Leverkusen', 'Eintracht Frankfurt': 'Frankfurt', 'Real Betis': 'Betis', 'Aston Villa': 'Aston Villa',
         'Newcastle United': 'Newcastle', 'Nottingham Forest': 'Forest', 'West Ham United': 'West Ham', 'LASK Linz': 'LASK'}


def short(name):
    return SHORT.get(name, name)


ASSET = {'CL': 'Oil (WTI)', 'GOLD': 'Gold', 'SILVER': 'Silver', 'SP500': 'S&P 500', 'XYZ100': 'Nasdaq 100', 'US100': 'Nasdaq 100',
         'BTC': 'Bitcoin', 'ETH': 'Ethereum', 'SOL': 'Solana', 'HYPE': 'HYPE', 'MU': 'Micron', 'SPCX': 'SpaceX', 'TSM': 'TSMC'}


def nick(team):
    """NFL / NBA club -> nickname ('Los Angeles Rams' -> 'Rams'); football clubs -> short()"""
    if team in SHORT: return SHORT[team]
    w = team.split()
    return w[-1] if len(w) >= 2 and (w[-1][0].isupper() or w[-1][0].isdigit()) and team.split()[0] in NFL_CITY else team


NFL_CITY = {'Arizona', 'Atlanta', 'Baltimore', 'Buffalo', 'Carolina', 'Chicago', 'Cincinnati', 'Cleveland', 'Dallas', 'Denver', 'Detroit',
            'Green', 'Houston', 'Indianapolis', 'Jacksonville', 'Kansas', 'Las', 'Los', 'Miami', 'Minnesota', 'New', 'Philadelphia',
            'Pittsburgh', 'San', 'Seattle', 'Tampa', 'Tennessee', 'Washington', 'Oklahoma', 'Boston', 'Golden', 'Brooklyn', 'Orlando',
            'Portland', 'Sacramento', 'Toronto', 'Utah', 'Memphis', 'Milwaukee', 'Charlotte', 'Phoenix'}


def load_meta(path=None):
    if path: return json.load(open(path, encoding='utf-8'))
    return hl({'type': 'outcomeMeta'})


def load_mids():
    return hl({'type': 'allMids'})


def _p(mids, c):
    v = mids.get(c)
    return float(v) if v is not None else None


def markets(meta=None, mids=None, now=None):
    """every open market as a clean dict:
    {key, kind, title, short, comp, start (iso), venue, outcomes: [{oid, label, coin, p}], total, ok, note}
    kind: match3 (football home/draw/away), game2 (NFL style A v B), winner (tournament / award multi-outcome),
          fed, ipo_cap, ipo_confirm, touch (price target by a date), binary (price above X at time), bucket, series"""
    meta = meta or load_meta(); mids = mids or load_mids()
    now = now or dt.datetime.now(dt.timezone.utc)
    outs = {o['outcome']: o for o in meta['outcomes']}
    used, res = set(), []
    for q in meta['questions']:
        qd = desc(q['description']); name = q['name']; named = q['namedOutcomes']
        rows = []
        for oid in named:
            o = outs.get(oid)
            if not o: continue
            od = desc(o['description'])
            label = od.get('participant') or od.get('candidate') or od.get('company')
            if o['name'] == 'template:sportsContestDraw2': label = 'Draw'
            if o['name'].startswith('template:policyRate'):
                label = {'template:policyRateNoChange': 'No change', 'template:policyRateIncrease': 'Hike',
                         'template:policyRateDecrease': 'Cut'}[o['name']]
            if not label and o['name'].startswith('Recurring'): label = 'band %s' % od.get('index', '?')
            if o['name'] == 'template:awardOther': label = 'Other'
            rows.append({'oid': oid, 'label': label or o['name'], 'coin': coin(oid), 'p': _p(mids, coin(oid))})
            used.add(oid)
        used.add(q['fallbackOutcome'])
        m = {'key': 'Q%d' % q['question'], 'q': q['question'], 'outcomes': rows, 'venue': (outs.get(named[0]) or {}).get('venue') if named else None}
        if name == 'template:sportsContestResult':
            comp = qd.get('competition', '')
            a, b = rows[0]['label'] if rows else '?', rows[-1]['label'] if rows else '?'
            m.update(kind='match3', comp=comp, start=qd.get('scheduledStart'), title='%s v %s' % (a, b),
                     short='%s v %s' % (short(a), short(b)), home=a, away=b)
        elif name == 'template:sportsTournamentWinner':
            comp = qd.get('competition', '').strip(); season = qd.get('season', '')
            m.update(kind='winner', comp=comp, title='%s %s winner' % (season, comp), short='%s winner' % comp, season=season)
        elif name == 'template:awardWinner':
            m.update(kind='winner', comp=qd.get('award', ''), title='%s %s' % (qd.get('award', ''), qd.get('period', '')),
                     short=qd.get('award', ''), season=qd.get('period', ''))
        elif name == 'template:policyRateDecision':
            m.update(kind='fed', comp='Fed', title='Fed decision: %s' % qd.get('decisionLabel', ''), short='Fed %s' % qd.get('decisionLabel', ''),
                     deadline=qd.get('decisionDeadline'))
        elif name == 'Recurring':
            m.update(kind='bucket', comp=qd.get('underlying', ''), title='%s %s range' % (qd.get('underlying', ''), qd.get('period', '')),
                     thresholds=qd.get('priceThresholds'), expiry=qd.get('expiry'))
        else:
            m.update(kind='other', comp='', title=name)
        res.append(m)
    # stand-alone outcomes (two-sided: NFL games, price targets, IPO, 15-minute and daily up/down)
    for oid, o in outs.items():
        if oid in used: continue
        od = desc(o['description']); n = o['name']
        y, no = _p(mids, coin(oid, 0)), _p(mids, coin(oid, 1))
        m = {'key': 'O%d' % oid, 'oid': oid, 'venue': o.get('venue'), 'desc': od}
        if n == 'template:sportsContestWinner':
            a, b = od.get('participantA', '?'), od.get('participantB', '?')
            m.update(kind='game2', comp=od.get('competition', ''), start=od.get('scheduledStart'), title='%s v %s' % (a, b),
                     short='%s v %s' % (od.get('shortNameA', a), od.get('shortNameB', b)), home=a, away=b,
                     outcomes=[{'oid': oid, 'label': a, 'coin': coin(oid, 0), 'p': y}, {'oid': oid, 'label': b, 'coin': coin(oid, 1), 'p': no}])
        elif n == 'template:priceTouch':
            asset = od.get('perp', '').replace('xyz:', ''); tgt = od.get('target')
            m.update(kind='touch', comp=asset, asset=asset, asset_name=ASSET.get(asset, asset), target=float(tgt) if tgt else None, deadline=od.get('time'),
                     title='%s touches $%s by %s' % (ASSET.get(asset, asset), format(float(tgt), ',g') if tgt else '?', (when(od.get('time', '')) or now).strftime('%d %b').lstrip('0')), outcomes=[{'oid': oid, 'label': 'Yes', 'coin': coin(oid), 'p': y}])
        elif n == 'template:companyIpoFirstDayMarketCap':
            b_ = float(od.get('marketCapThresholdB', 0))
            m.update(kind='ipo_cap', comp=od.get('company', ''), threshold_b=b_, deadline=od.get('listingDeadline'),
                     title='%s first-day value above $%s' % (od.get('company'), ('%gT' % (b_ / 1000)) if b_ >= 1000 else '%gB' % b_),
                     outcomes=[{'oid': oid, 'label': 'Yes', 'coin': coin(oid), 'p': y}])
        elif n == 'template:companyIpoConfirmed':
            m.update(kind='ipo_confirm', comp=od.get('company', ''), deadline=od.get('dateTime'),
                     title='%s IPO confirmed by %s' % (od.get('company'), od.get('dateTime', '')[:8]), outcomes=[{'oid': oid, 'label': 'Yes', 'coin': coin(oid), 'p': y}])
        elif n in ('template:binaryPrice', 'template:binaryPriceExternal') or (n == 'Recurring' and od.get('class') == 'priceBinary'):
            asset = (od.get('perp') or od.get('shortName') or od.get('underlying') or '').replace('xyz:', '')
            m.update(kind='binary', comp=asset, asset=asset, threshold=od.get('threshold') or od.get('targetPrice'),
                     deadline=od.get('time') or od.get('expiry'), period=od.get('period'),
                     title='%s above %s at %s UTC' % (asset, od.get('threshold') or od.get('targetPrice'), od.get('time') or od.get('expiry')),
                     outcomes=[{'oid': oid, 'label': 'Up', 'coin': coin(oid, 0), 'p': y}, {'oid': oid, 'label': 'Down', 'coin': coin(oid, 1), 'p': no}])
        elif n in ('template:sportsTotal', 'template:sportsSpread'):
            continue                                            # totals and spreads: not used in posts
        else:
            continue
        res.append(m)
    # the same game or IPO line can be listed by two venues: keep Outcome's own ('out')
    seen = {}
    for m in res:
        if m['kind'] == 'game2': k = ('g', frozenset((m['home'], m['away'])), (m.get('start') or '')[:8])
        elif m['kind'] == 'ipo_cap': k = ('i', m['comp'], m['threshold_b'])
        elif m['kind'] == 'ipo_confirm': k = ('c', m['comp'], (m.get('deadline') or '')[:8])
        else: continue
        prev = seen.get(k)
        if prev is None or (prev.get('venue') != 'out' and m.get('venue') == 'out'): seen[k] = m
    keep = set(id(v) for v in seen.values())
    res = [m for m in res if m['kind'] not in ('game2', 'ipo_cap', 'ipo_confirm') or id(m) in keep]
    for m in res:
        if m['kind'] == 'winner':      # only the leading names are listed; drop untraded rows (exact 0.5 placeholders)
            m['outcomes'] = [r for r in m['outcomes'] if r.get('p') is not None and abs(r['p'] - 0.5) > 1e-9]
        if m['kind'] == 'game2':
            for r in m['outcomes']: r['short'] = nick(r['label'])
            m['short'] = '%s v %s' % (nick(m['home']), nick(m['away']))
        for r in m.get('outcomes', []): r.setdefault('short', short(r['label']))
    for m in res:
        ps = [r['p'] for r in m.get('outcomes', []) if r.get('p') is not None]
        m['total'] = round(sum(ps), 3) if ps else None
        placeholder = any(abs((r.get('p') or 0) - 0.5) < 1e-9 for r in m.get('outcomes', []))
        multi = m['kind'] in ('match3', 'fed', 'bucket')
        # a multi-outcome market is publishable when its named sides add up to about 100% (the fallback bucket takes the rest)
        m['ok'] = bool(ps) and not placeholder and (not multi or 0.9 <= m['total'] <= 1.06) and (m['kind'] != 'winner' or len(ps) >= 3)
        m['note'] = 'placeholder price' if placeholder else ('sides add to %.0f%%' % (100 * m['total']) if multi and m['total'] and not m['ok'] else '')
        if m.get('start'):
            s = when(m['start']); m['start_iso'] = s.isoformat() if s else None
        m['outcomes'] = sorted(m.get('outcomes', []), key=lambda r: -(r['p'] or 0)) if m['kind'] in ('winner',) else m.get('outcomes', [])
    return res


def candles(c, interval='1m', start=None, end=None):
    """price history of one outcome coin while it is live (gone after settlement); returns [(t_ms, open, high, low, close, vol)]"""
    end = end or int(time.time() * 1000); start = start or end - 6 * 3600 * 1000
    rows = hl({'type': 'candleSnapshot', 'req': {'coin': c, 'interval': interval, 'startTime': int(start), 'endTime': int(end)}}) or []
    return [(r['t'], float(r['o']), float(r['h']), float(r['l']), float(r['c']), float(r.get('v', 0))) for r in rows]


def leaderboard(duration='24h', by='pnl', order='desc', limit=50, offset=0):
    d = o1('/leaderboard', {'duration': duration, 'filter_by': by, 'order_by': order, 'offset': offset, 'limit': limit})
    rows = (d.get('data') or {}).get('rows') or []
    for r in rows:
        for k, v in list(r.items()):
            if isinstance(v, str) and re.fullmatch(r'-?\d+(\.\d+)?', v): r[k] = float(v)
    return rows


def profile(username):
    return o1('/profile/lookup', {'username': username})


def portfolio(username, window='30d'):
    return o1('/portfolio/lookup', {'username': username, 'window': window})


def lookup(oids):
    out = {}
    for i in range(0, len(oids), 50):
        d = o1('/markets/lookup', {'outcome_ids': list(oids[i:i + 50])})
        out.update((d.get('markets') if isinstance(d, dict) else None) or {})
    return out


if __name__ == '__main__':
    ms = markets()
    for m in sorted(ms, key=lambda m: (m['kind'], m.get('start') or '', m['title'])):
        if m['kind'] in ('binary',): continue
        top = ', '.join('%s %.0f%%' % (r['label'], 100 * r['p']) for r in m['outcomes'][:4] if r.get('p') is not None)
        print('%-10s %-6s %-8s %-48s %s %s' % (m['kind'], m['key'], (m.get('start') or '')[4:], m.get('short') or m['title'][:48], top, '' if m['ok'] else '[SKIP ' + m['note'] + ']'))
