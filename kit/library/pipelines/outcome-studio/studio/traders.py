"""traders: real trader data for the client's formats (Top 3 traders, trader card, P&L card, trader story).

All numbers come from Outcome's public leaderboard API and the trader's public on-chain fills on Hyperliquid.
Usernames are shown as Outcome shows them. The client still has to OK naming traders in posts (see research/00-status.md).
"""
import os, time, json, datetime as dt
from collections import defaultdict
import ocdata as od
import formats as fm

ROOT = od.ROOT
_NAMES = {}
WIN = {'24h': ('24h', '1D', '24 hours'), '7d': ('168h', '7D', '7 days'), '30d': ('720h', '30D', '30 days'), 'all': ('all', 'ALL', 'all time')}


def coin_name(c, ms=None):
    """'#71850' -> {'title': ..., 'label': ..., 'kind': ...} (open markets from the live list, settled ones from Outcome's lookup)"""
    if c in _NAMES: return _NAMES[c]
    ms = ms or od.markets()
    for m in ms:
        for r in m.get('outcomes', []):
            if r['coin'] == c:
                _NAMES[c] = {'title': m.get('short') or m['title'], 'label': r['label'], 'kind': m['kind'], 'key': m['key']}; return _NAMES[c]
    n = int(c.lstrip('#+')); oid, side = n // 10, n % 10
    info = {'title': 'a settled market', 'label': 'Yes' if side == 0 else 'No', 'kind': '?', 'key': 'O%d' % oid}
    try:
        d = od.o1('/markets/lookup', {'outcome_ids': [oid]})
        mk = (((d or {}).get('data') or {}).get('markets') or {}).get(str(oid)) or {}
        o = mk.get('outcome') or {}
        info['stats'] = {'yes': o.get('yesStats'), 'no': o.get('noStats'), 'active': mk.get('is_active')}
        mm = od.markets({'outcomes': [{'outcome': oid, 'name': o.get('name') or '', 'description': o.get('description') or '',
                                       'sideSpecs': o.get('sideSpecs') or [], 'venue': o.get('deployerVenue')}], 'questions': []}, mids={})
        if mm:
            m = mm[0]; rows = m.get('outcomes') or []
            lab = rows[side]['label'] if len(rows) > side else info['label']
            info.update(title=m.get('short') or m['title'], label=lab, kind=m['kind'])
        else:
            dd = od.desc(o.get('description') or '')
            if dd.get('participant'): info.update(title='%s to win' % dd['participant'], label='Yes' if side == 0 else 'No')
    except Exception as ex:
        info['error'] = str(ex)
    _NAMES[c] = info
    return info


def fills(address, hours=24):
    end = int(time.time() * 1000); start = end - hours * 3600 * 1000; out = []
    while True:
        f = od.hl({'type': 'userFillsByTime', 'user': address, 'startTime': start, 'endTime': end}) or []
        out += f
        if len(f) < 2000: break
        start = max(x['time'] for x in f) + 1
    return out


def positions(fs):
    """fills -> per coin: shares bought, cost, avg price, sold proceeds, settlement payout, realised P&L"""
    agg = defaultdict(lambda: {'bought': 0.0, 'cost': 0.0, 'sold': 0.0, 'proceeds': 0.0, 'payout': 0.0, 'pnl': 0.0, 'n': 0, 'first': None, 'last': None})
    for x in fs:
        a = agg[x['coin']]; sz, px = float(x['sz']), float(x['px']); d = x.get('dir', '')
        a['pnl'] += float(x.get('closedPnl') or 0); a['n'] += 1
        a['first'] = min(a['first'] or x['time'], x['time']); a['last'] = max(a['last'] or 0, x['time'])
        if d == 'Settlement': a['payout'] += sz * px
        elif x['side'] == 'B': a['bought'] += sz; a['cost'] += sz * px
        else: a['sold'] += sz; a['proceeds'] += sz * px
    for c, a in agg.items():
        a['avg'] = a['cost'] / a['bought'] if a['bought'] else None
    return agg


def top(window='24h', n=3, by='pnl'):
    return od.leaderboard(WIN[window][0], by=by, limit=n)


def summary(row, window='24h', ms=None):
    """leaderboard row -> everything a trader slide needs"""
    u = row.get('username')
    if not u: return None
    try:
        pr = (od.profile(u) or {}).get('data') or {}
    except Exception:
        return None
    s = {'username': u, 'avatar': row.get('avatar') or pr.get('avatar'), 'pnl': float(row.get('pnl') or 0), 'volume': float(row.get('volume') or 0),
         'pnl_pct': row.get('pnl_pct'), 'address': pr.get('address'), 'joined': pr.get('created_at'), 'verified': row.get('x_verified')}
    try:
        ph = ((od.portfolio(u, WIN[window][1].lower()) or {}).get('data') or {}).get('pnlHistory') or []
        s['pnl_series'] = [[int(t), float(v)] for t, v in ph]
    except Exception:
        s['pnl_series'] = []
    if s['address']:
        hours = {'24h': 24, '7d': 168, '30d': 720}.get(window, 24)
        pos = positions(fills(s['address'], hours))
        best = max(pos.items(), key=lambda kv: kv[1]['pnl'], default=None)
        if best and best[1]['pnl'] > 0:
            nm = coin_name(best[0], ms)
            s['best'] = dict(best[1], coin=best[0], title=nm['title'], label=nm['label'])
        s['n_markets'] = len(pos)
    return s


def _short_money(v):
    return ('$%.1fK' % (v / 1000)).replace('.0K', 'K') if abs(v) >= 1000 else '$%d' % round(v)


def card_spec(s, rank=None, window='24h'):
    since = ''
    if s.get('joined'): since = 'On Outcome since %s' % dt.datetime.fromtimestamp(s['joined'] / 1000, dt.timezone.utc).strftime('%b %Y')
    pts = s.get('pnl_series') or []
    best = s.get('best')
    return {'fmt': 'trader_card', 'rank': rank, 'username': s['username'], 'avatar': s.get('avatar'), 'since': since, 'total': s['pnl'],
            'window': 'LAST ' + WIN[window][2].upper(), 'pnl': [[t, v] for t, v in pts],
            'stats': [['VOLUME', _short_money(s['volume'])], ['RETURN', '%+.0f%%' % (s['pnl_pct'] or 0)], ['MARKETS', str(s.get('n_markets') or '-')]],
            'best': ('Best call: *%s* on %s, *+%s*' % (best['label'], best['title'], _short_money(best['pnl']))) if best else ''}


def top3(ms=None, window='24h', capture=True, st=None):
    """Top 3 traders carousel: hook, #3, #2, #1 (real profile screenshots when capture works, data cards otherwise), CTA"""
    ms = ms or od.markets()
    sums = []
    for r in top(window, 8):                      # skip anonymous rows and profiles that do not load
        sm = summary(r, window, ms)
        if sm and sm.get('address'): sums.append(sm)
        if len(sums) == 3: break
    slides = [{'fmt': 'top3_hook', 'traders': [{'username': s['username'], 'avatar': s.get('avatar')} for s in sums], 'window': WIN[window][2]}]
    shots = {}
    if capture and st is not None:
        from capture import Capture
        c = Capture(st)
        for s in sums:
            try:
                f = os.path.join(ROOT, 'out', 'captures', 'profile_%s_%s.png' % (s['username'], WIN[window][1]))
                c.open('https://outcome.xyz/profile/%s' % s['username'], h=1000, wait=5)
                st.js("(() => { const b=[...document.querySelectorAll('*')].filter(e=>e.children.length===0 && e.textContent.trim()==='%s'); if(b.length) b[0].click(); return b.length })()" % WIN[window][1])
                time.sleep(3)
                pos = st.js("(() => { const f=t=>{const e=[...document.querySelectorAll('*')].find(e=>e.children.length===0 && e.textContent.trim()===t); if(!e) return null; const r=e.getBoundingClientRect(); return Math.round(r.y)}; const g=t=>{const e=[...document.querySelectorAll('*')].find(e=>e.children.length===0 && (e.textContent||'').includes(t)); if(!e) return null; const r=e.getBoundingClientRect(); return Math.round(r.y+r.height)}; return {pl:f('Profit / Loss'), tab:f('%s'), hof:f('Hall of Fame'), ot:g('Outcomes traded')} })()" % WIN[window][1])
                if not c.clean():
                    print('pop-up would not close on %s: using the data card' % s['username']); continue
                c.shot(f)
                if pos and pos.get('pl') and pos.get('tab'):
                    shots[s['username']] = {'img': fm_url(f), 'cropA': [3 * 74, 3 * ((pos.get('ot') or 268) + 16)], 'cropB': [3 * (pos['pl'] - 14), 3 * (pos['tab'] - 12)]}
            except Exception as ex:
                print('capture failed for %s: %s' % (s['username'], ex))
    for rank, s in zip((3, 2, 1), reversed(sums)):
        best = s.get('best')
        stat = '*%s* in %s%s' % (('+' if s['pnl'] >= 0 else '') + _short_money(s['pnl']), WIN[window][2], (', best call: *%s* on %s' % (best['label'], best['title'])) if best else '')
        sh = shots.get(s['username'])
        if sh: slides.append(dict({'fmt': 'rank_shot', 'rank': rank, 'stat': stat}, **sh))
        else: slides.append(card_spec(s, rank, window))
    slides.append(fm.cta(line1='Think you can *make the list*?'))
    names = ', '.join('#%d %s %s' % (3 - i, s['username'], ('+' if s['pnl'] >= 0 else '') + _short_money(s['pnl'])) for i, s in enumerate(reversed(sums)))
    cap = ('Top 3 traders on Outcome in the last %s \U0001F3C6\n\n%s\n\nReal profiles from Outcome\'s public leaderboard, %s. Past results do not predict future results. %s'
           % (WIN[window][2], names, fm.stamp(), fm.risk_line()))
    return fm._post('top3_%s' % window, 'top3', 'Top 3 traders %s' % WIN[window][2], slides, cap, notes='Needs the client OK on showing usernames.')


def fm_url(p):
    from render import file_url
    return file_url(p)


def pnl_card(username, coin=None, hours=720, ms=None):
    """our own P&L share card for a trader's best (or given) resolved position; transparent PNG for edits"""
    pr = (od.profile(username) or {}).get('data') or {}
    if coin:                                   # read back to the market's first trade so the buys are included
        first = ((coin_name(coin, ms).get('stats') or {}).get('yes') or {}).get('firstTrade')
        if first: hours = max(hours, int((time.time() * 1000 - first) / 3600000) + 2)
    pos = positions(fills(pr['address'], hours))
    if coin is None:
        coin = max(pos.items(), key=lambda kv: kv[1]['pnl'])[0]
        if not pos[coin]['bought']:            # the buys are older than the window: read further back for this coin
            return pnl_card(username, coin, hours, ms)
    a = pos[coin]; nm = coin_name(coin, ms)
    paid = a['payout'] + a['proceeds']
    rows = [['Shares', '{:,.0f}'.format(a['bought'])], ['Avg. price', '%.1f¢' % (100 * a['avg']) if a['avg'] else '-'],
            ['Bought', '${:,.0f}'.format(a['cost'])], ['Paid out', '${:,.0f}'.format(paid)]]
    when = dt.datetime.fromtimestamp((a['last'] or 0) / 1000, dt.timezone.utc).strftime('%d %b %Y').lstrip('0')
    spec = {'fmt': 'pnl_card', 'side': nm['label'].upper(), 'title': nm['title'].upper(), 'entry': '$%.2f' % a['avg'] if a['avg'] else '',
            'rows': rows, 'username': username, 'date': when}
    return spec, dict(a, coin=coin, title=nm['title'], label=nm['label'], profit=a['pnl'])
