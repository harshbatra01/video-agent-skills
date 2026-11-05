"""postmatch: posts built after a game from the price archive (archive.py must have been running during the match).

python postmatch.py list [YYYYMMDD]        matches with archived minute prices + what each one qualifies for
Recipes for batches: replay (full-time chart replay video + still), upset (the crowd's underdog won), comeback (low half-time chance, then won).

Times: kickoff from Outcome's scheduledStart; goal minutes from ESPN (data/archive/scores); each goal marker snaps to the biggest
1-minute price jump within 6 minutes of its estimated time, so markers sit where the money actually reacted.
"""
import glob, json, os, re, sys, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ocdata as od, formats as fm

A = os.path.join(od.ROOT, 'data', 'archive')
ESPN_LG = {'UEFA Champions League': 'uefa.champions', 'UEFA Europa League': 'uefa.europa', 'English Premier League': 'eng.1'}


def _norm(s):
    import unicodedata                                       # Atlético -> atletico, so ESPN names match
    s = ''.join(c for c in unicodedata.normalize('NFKD', s or '') if not unicodedata.combining(c)).lower()
    for w in ('fc ', ' fc', 'afc ', ' afc', 'cf', 'sk ', 'rc ', 'jk', 'as ', 'losc ', 'tsg ', 'scu ', 'fk ', 'linz', 'munich', 'praha', 'donetsk'):
        s = s.replace(w, ' ')
    return re.sub(r'[^a-z]', '', s)


def load(key):
    files = glob.glob(os.path.join(A, 'candles', key, '*.json'))
    if not files: return None
    lines = [json.load(open(f, encoding='utf-8')) for f in files]
    meta = lines[0]
    out = {x['label']: [(r[0], r[4]) for r in x['rows']] for x in lines}
    coins = {x['label']: x['coin'] for x in lines}
    # fill quiet minutes (no trades = no candle) from the 5-minute price archive, then carry every line to the same end
    t_lo = min((r[0][0] for r in out.values() if r), default=0); t_hi = max((r[-1][0] for r in out.values() if r), default=0)
    s = od.when(meta['start'])
    for day in {s.strftime('%Y%m%d'), (s + dt.timedelta(hours=4)).strftime('%Y%m%d')} if s else ():
        f = os.path.join(A, 'mids', day + '.jsonl')
        if not os.path.exists(f): continue
        for ln in open(f, encoding='utf-8'):
            try: snap = json.loads(ln)
            except ValueError: continue
            if not (t_lo <= snap['t'] <= t_hi + 60000): continue
            for lab, c in coins.items():
                v = snap['m'].get(c)
                if v is not None: out[lab].append((snap['t'], float(v)))
    for lab in out:
        pts = sorted(set(out[lab]))
        if pts and pts[-1][0] < t_hi: pts.append((t_hi, pts[-1][1]))
        out[lab] = pts
    return {'key': key, 'title': meta['title'], 'comp': meta.get('comp'), 'start': meta['start'], 'lines': out, 'coins': coins}


def espn_event(comp, start, home, away):
    s = od.when(start); lg = ESPN_LG.get(comp)
    if not s or not lg: return None
    for f in glob.glob(os.path.join(A, 'scores', '%s_%s*.json' % (lg, s.strftime('%Y%m%d')))) + glob.glob(os.path.join(A, 'scores', '%s_*.json' % lg)):
        sb = json.load(open(f, encoding='utf-8'))
        for ev in sb.get('events', []):
            comp0 = ev['competitions'][0]; teams = {c['homeAway']: c for c in comp0['competitors']}
            hn, an = _norm(teams['home']['team']['displayName']), _norm(teams['away']['team']['displayName'])
            if (_norm(home)[:5] in hn or hn[:5] in _norm(home)) and (_norm(away)[:5] in an or an[:5] in _norm(away)):
                goals = []
                for d in comp0.get('details', []):
                    typ = (d.get('type') or {}).get('text', '')
                    if d.get('scoringPlay') or 'Goal' in typ:
                        side = 'home' if d.get('team', {}).get('id') == teams['home']['team']['id'] else 'away'
                        mins = (d.get('clock') or {}).get('displayValue', '').replace("'", '')
                        who = ((d.get('athletesInvolved') or [{}])[0]).get('shortName') or ((d.get('athletesInvolved') or [{}])[0]).get('displayName', '')
                        goals.append({'side': side, 'min': mins, 'who': who, 'own': 'Own' in typ, 'pen': 'Penalty' in typ})
                st = (comp0.get('status') or {}).get('type', {})
                return {'home': int(teams['home'].get('score') or 0), 'away': int(teams['away'].get('score') or 0), 'goals': goals,
                        'final': st.get('completed', False), 'state': st.get('description', ''), 'id': ev.get('id')}
    return None


def _min(m):
    """"45'+2" -> (45, 2); "67" -> (67, 0)"""
    m = str(m).replace("'", '')
    a, _, b = m.partition('+')
    try: return int(a), int(b or 0)
    except ValueError: return None, 0


def price_at(line, t):
    best = None
    for tt, p in line:
        if tt <= t: best = p
        else: break
    return best if best is not None else (line[0][1] if line else None)


def analyse(key):
    d = load(key)
    if not d: return None
    m = d['title'].split(' v '); home, away = m[0], m[-1]
    labels = list(d['lines'].keys())
    hl = next((l for l in labels if _norm(l) and (_norm(l)[:5] in _norm(home) or _norm(home)[:5] in _norm(l))), None)
    al = next((l for l in labels if l != hl and l != 'Draw' and (_norm(l)[:5] in _norm(away) or _norm(away)[:5] in _norm(l))), None)
    ko = int(od.when(d['start']).timestamp() * 1000)
    pre = {l: price_at(d['lines'][l], ko - 60000) for l in labels}
    ht = {l: price_at(d['lines'][l], ko + 49 * 60000) for l in labels}
    ev = espn_event(d['comp'], d['start'], hl or home, al or away)
    res = dict(d, home=hl or home, away=al or away, ko=ko, pre=pre, ht=ht, espn=ev)
    res['fav'] = max((l for l in (hl, al) if l), key=lambda l: pre.get(l) or 0, default=None)
    if ev and ev['final']:
        win = hl if ev['home'] > ev['away'] else (al if ev['away'] > ev['home'] else 'Draw')
        res['winner'] = win; res['winner_pre'] = pre.get(win); res['winner_ht'] = ht.get(win)
        res['upset'] = win != 'Draw' and (pre.get(win) or 1) < .35
        res['comeback'] = win != 'Draw' and (ht.get(win) or 1) < .25
    return res


def _markers(a):
    if not a.get('espn'): return []
    out = []
    for g in a['espn']['goals']:
        mn, extra = _min(g['min'])
        if mn is None: continue
        est = a['ko'] + (mn + extra + (17 if mn > 45 else 0)) * 60000          # 15 to 17 min half-time break
        line = a['lines'].get(a['home'] if g['side'] == 'home' else a['away']) or []
        win = [(i, line[i][0], line[i][1] - line[i - 1][1]) for i in range(1, len(line)) if abs(line[i][0] - est) <= 6 * 60000]
        t = max(win, key=lambda x: x[2])[1] if win else est
        team = fm.team(a['home'] if g['side'] == 'home' else a['away'])['short']
        out.append({'t': t, 'label': "%s' %s" % (g['min'], g['who'] or team), 'color': '#FFFFFF'})
    return out


def replay(ms=None, key=None, title=None, pid=None, **_):
    a = analyse(key)
    if not a: return None
    A_, B_ = fm.pair(fm.team(a['home']), fm.team(a['away']))
    end = max(t for l in a['lines'].values() for t, _ in l) if a['lines'] else a['ko']
    t0 = a['ko'] - 10 * 60000
    ser = []
    for lab, col in ((a['home'], 'lime'), ('Draw', 'grey'), (a['away'], 'pink')):
        line = [(t, p) for t, p in a['lines'].get(lab, []) if t >= t0]
        if len(line) > 1: ser.append({'label': fm.team(lab)['short'] if lab != 'Draw' else 'Draw', 'color': col, 'pts': [[t, p] for t, p in line], 'width': 8 if lab != 'Draw' else 5})
    ev = a.get('espn') or {}
    score = '%d-%d' % (ev['home'], ev['away']) if ev else ''
    xl = [[a['ko'], 'KO']]
    if end - a['ko'] > 60 * 60000: xl.append([a['ko'] + 62 * 60000, 'HT'])
    xl.append([end, 'FT' if ev.get('final') else 'Now'])
    if not title:
        fav = a.get('fav'); w = a.get('winner')
        if a.get('upset'): title = '^%s^ were *%d%%* at kickoff. They won.' % (fm.team(w)['short'], round(100 * a['winner_pre']))
        elif a.get('comeback'): title = 'At half-time the money gave ^%s^ *%d%%*.' % (fm.team(w)['short'], round(100 * a['winner_ht']))
        elif fav and a['pre'].get(fav): title = 'The money had *%s* at *%d%%* before kickoff' % (fm.team(fav)['short'], round(100 * a['pre'][fav]))
        else: title = 'The match, told by the money'
    spec = {'fmt': 'replay', 'teams': [A_, B_], 'score': score, 'title': title, 'series': ser, 'xLabels': xl, 'markers': _markers(a),
            'kicker': 'Full time' if ev.get('final') else 'Live', 'dur': 10, 'stamp': 'Minute prices to %s' % dt.datetime.fromtimestamp(end / 1000, dt.timezone.utc).strftime('%H:%M UTC')}
    goals = ', '.join("%s %s'" % (g['who'], g['min']) for g in (ev.get('goals') or []))
    cap = ('%s %s %s, told by the money \U0001F4C8\n\n%s\n%s\n\nMinute-by-minute chances from Outcome.xyz market prices. %s'
           % (A_['short'], score or 'v', B_['short'], title.replace('*', '').replace('^', ''), ('Goals: ' + goals) if goals else '', fm.risk_line()))
    return fm._post(pid or 'replay_%s' % key, 'replay', title, [spec, fm.cta(line1='Think you can *call it*?')], cap, video=dict(spec))


def upset(ms=None, key=None, pid=None, **_):
    a = analyse(key)
    if not a or not a.get('upset'): return None
    return replay(ms, key, pid=pid or 'upset_%s' % key)


def comeback(ms=None, key=None, pid=None, **_):
    a = analyse(key)
    if not a or not a.get('comeback'): return None
    return replay(ms, key, pid=pid or 'comeback_%s' % key,
                  title='At half-time the money gave ^%s^ *%d%%*. They won.' % (fm.team(a['winner'])['short'], round(100 * a['winner_ht'])))


def listing(day=None):
    for d in sorted(glob.glob(os.path.join(A, 'candles', '*'))):
        a = analyse(os.path.basename(d))
        if not a or (day and not a['start'].startswith(day)): continue
        ev = a.get('espn') or {}
        tags = [t for t in ('upset', 'comeback') if a.get(t)]
        print('%-6s %-34s %s  pre: %s  %s' % (a['key'], a['title'][:34], ('%d-%d %s' % (ev['home'], ev['away'], ev['state'])) if ev else 'no score',
                                            ', '.join('%s %d%%' % (l[:10], round(100 * (p or 0))) for l, p in a['pre'].items()), ' '.join(tags)))


if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'list': listing(a[1] if len(a) > 1 else None)
    else: print(__doc__)
