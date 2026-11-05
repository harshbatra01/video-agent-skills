"""motion: VIDEO formats (templates/motion.html, GSAP timelines, optional real footage under the graphics).

Builders return a post like formats.py does; the post's "video" is the main deliverable (1080x1920 MP4 with sound when given).
  timed       Call it in 3 seconds: question, 3-2-1 countdown, the money's answer
  wheel       Spin the wheel (the client's UGC format, faceless): the wheel picks, then the money answers. Day N series
  demo        App demo over real outcome.xyz screens: scroll, tap, amount, payout (needs `python howto.py capture`)
  clipbanner  Footage + a live chance banner that moves with the real price line (goal moments, from the archive)
  hottake     Hot take in big words over footage, then the receipt card with the real chances
  pnl_edit    The client's P&L card edit: our card drops in over event footage, CTA at the end
Footage comes in as a local clip file (fetch.py style: YouTube section downloads, X clips, your own edits).
"""
import json, os, random, time
import ocdata as od, formats as fm
from render import clip_frames, still_frames, file_url

ROOT = od.ROOT
CLIPS = os.path.join(ROOT, 'out', '_clipframes')


def _side_rows(m):
    rows = m['outcomes'] if m['kind'] == 'match3' else m['outcomes']
    out = []
    for r in rows:
        if r['label'] == 'Draw': out.append({'label': 'Draw', 'p': r['p'], 'color': '#5B616D'})
        else: out.append({'label': fm.team(r['label'])['short'], 'team': fm.team(r['label']), 'p': r['p']})
    return out


def timed(ms, match, question=None, pid=None, **_):
    import ocs
    m = ocs.find(ms, match)
    rows = _side_rows(m)
    best = max(range(len(rows)), key=lambda i: rows[i]['p'] if rows[i]['label'] != 'Draw' else -1)
    A, B = fm.team(m['outcomes'][0]['label']), fm.team(m['outcomes'][-1]['label'])
    q = question or 'Who wins %s v %s %s?' % (A['short'], B['short'], 'tonight' if fm.dayname(m['start']) == _today() else fm.dayname(m['start']).split(' ')[0])
    spec = {'fmt': 'timed', 'kicker': 'Call it in 3', 'question': q, 'sides': rows, 'best': best, 'ask': 'Did you call it? Comment 👇', 'stamp': fm.stamp()}
    cap = ('%s\n\nYou have 3 seconds. Then the money answers.\n\n%s\n\nChances from Outcome.xyz at %s. %s'
           % (q, ' / '.join('%s %d%%' % (r['label'], round(100 * r['p'])) for r in rows), fm.stamp(), fm.risk_line()))
    return fm._post(pid or 'timed_%s' % m['key'], 'timed', q, [], cap, video=spec)


def _today():
    import datetime as dt
    lab, off = fm.tz()
    return (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=off)).strftime('%a %d %b').replace(' 0', ' ')


def wheel(ms, match, day=1, seed=None, pid=None, **_):
    import ocs
    m = ocs.find(ms, match)
    rows = _side_rows(m)
    teams = [r for r in rows if r.get('team')]
    if len(teams) == 2:                                   # two reds (Atletico v United) would merge on the wheel
        a, b = fm.pair(teams[0]['team'], teams[1]['team']); teams[0]['team'], teams[1]['team'] = a, b
    segs = [{'label': r['label'], 'team': r.get('team'), 'color': r.get('color')} for r in rows]
    rnd = random.Random(seed if seed is not None else int(time.time()))
    land = rnd.randrange(len(segs))
    best = max(range(len(rows)), key=lambda i: rows[i]['p'])
    A, B = fm.team(m['outcomes'][0]['label']), fm.team(m['outcomes'][-1]['label'])
    spec = {'fmt': 'wheel', 'day': day, 'title': 'A wheel picks %s v %s' % (A['short'], B['short']), 'segments': segs, 'land': land,
            'money': rows, 'moneyBest': best, 'outro': 'Wheel or money? Results after full time.', 'stamp': fm.stamp()}
    cap = ('Day %d of letting a wheel pick the big games \U0001F3A1\n\nThe wheel says: %s. The money says: %s.\nWho is right? Results after full time.\n\n'
           'Chances from Outcome.xyz at %s. %s' % (day, segs[land]['label'], ' / '.join('%s %d%%' % (r['label'], round(100 * r['p'])) for r in rows), fm.stamp(), fm.risk_line()))
    return fm._post(pid or 'wheel_%s' % m['key'], 'wheel', 'Spin the wheel day %d' % day, [], cap, video=spec,
                    notes='Series: keep the day count going; post the result (wheel right or money right) the next day.')


def demo(ms=None, market='Q422', pid='demo', **_):
    cap_dir = os.path.join(ROOT, 'out', 'captures')
    pos = json.load(open(os.path.join(cap_dir, 'howto_pos.json'), encoding='utf-8'))
    ms = ms or od.markets()
    m = next((x for x in ms if x['key'] == market), None)
    home = m['outcomes'][0] if m else None
    team = fm.team(home['label'])['short'] if home else 'them'
    import re
    t100 = (pos.get('ticket100') or {}).get('text', '').replace('\n', ' | ')
    pay = re.search(r'Payout\s*\|?\s*\$([0-9,.]+)', t100)
    yes = (pos.get('market') or {}).get('yes') or [12, 1015, 179, 64]
    payrow = (pos.get('ticket100') or {}).get('payout') or [36, 971, 92, 29]
    screens = [{'img': file_url(os.path.join(cap_dir, f))} for f in ('howto_home.png', 'howto_market.png', 'howto_ticket100.png')]
    steps = [{'at': 0.5, 'lines': ['Find a market you know']}, {'at': 3.4, 'lines': ['Think %s win?' % team, 'Tap YES']},
             {'at': 6.6, 'lines': ['$100 on %s at %d%%' % (team, round(100 * home['p'])) if home else '$100', 'pays $%s if they win' % (pay.group(1) if pay else '?')]},
             {'at': 10.0, 'lines': ['Make your call on Outcome.xyz']}]
    moves = [{'at': 1.0, 'scroll': 300, 'd': 1.3},
             {'at': 3.0, 'show': 1}, {'at': 3.0, 'scroll': 0, 'd': .01}, {'at': 3.6, 'scroll': 430, 'd': 1.2},
             {'at': 5.1, 'tap': [yes[0] + yes[2] / 2, yes[1] + yes[3] / 2], 'scrollNow': 430}, {'at': 5.2, 'ring': yes, 'scrollNow': 430},
             {'at': 6.3, 'ringOff': True}, {'at': 6.3, 'show': 2}, {'at': 6.3, 'scroll': 430, 'd': .01},
             {'at': 7.4, 'ring': [18, payrow[1] - 14, 354, 58], 'scrollNow': 430}, {'at': 7.6, 'zoom': 1.12, 'origin': '50% 75%', 'd': .9},
             {'at': 9.6, 'ringOff': True}, {'at': 9.6, 'zoom': 1.0, 'd': .6}, {'at': 9.7, 'show': 0}, {'at': 9.7, 'scroll': 0, 'd': .01}]
    spec = {'fmt': 'demo', 'screens': screens, 'steps': steps, 'moves': moves, 'dur': 12.5}
    cap = ('How a call works on Outcome, in 12 seconds \U0001F447\n\n1. Find a market you know\n2. Think it happens? Tap YES\n3. $100 at %d%% pays $%s if they win\n\nReal screens from outcome.xyz (%s). %s'
           % (round(100 * home['p']) if home else 0, pay.group(1) if pay else '?', pos.get('made', ''), fm.risk_line()))
    return fm._post(pid, 'demo', 'App demo', [], cap, video=spec, notes='Re-run `python howto.py capture` before posting so the screens and numbers are fresh.')


def clipbanner(ms, clip, start, dur, title, team, label, series, event=None, left='', right='', focus=.5, pid='clipbanner', audio=True, **_):
    """series: [[t_seconds_into_clip, p], ...] (the real price line mapped onto clip time); event: {'at': s, 'badge': '+25%', 'up': True}"""
    cf = clip_frames(clip, start, dur, os.path.join(CLIPS, pid), focus=focus)
    spec = {'fmt': 'clipbanner', 'clip': cf, 'dur': dur, 'title': title, 'team': fm.team(team) if isinstance(team, str) else team, 'label': label,
            'series': series, 'event': event, 'left': left, 'right': right, 'stamp': fm.stamp()}
    p = fm._post(pid, 'clipbanner', title, [], title.replace('*', '').replace('^', ''), video=spec)
    if audio: p['audio'] = {'src': clip, 'start': start}
    return p


def hottake(ms, clip=None, start=0, lines=(), receipt=None, dur=9, cut=3.4, focus=.5, pid='hottake', audio=True, still=None, move=None, **_):
    """footage: a clip (clip + start) or a photo (still + move = {x0, x1, z0, z1})"""
    cf = still_frames(still, dur, os.path.join(CLIPS, pid), **(move or {})) if still else clip_frames(clip, start, dur, os.path.join(CLIPS, pid), focus=focus)
    if still: audio = False
    rows = receipt['rows']
    receipt = dict(receipt, max=max(r['p'] for r in rows))
    spec = {'fmt': 'hottake', 'clip': cf, 'dur': dur, 'cut': cut, 'lines': lines, 'receipt': receipt, 'stamp': fm.stamp()}
    p = fm._post(pid, 'hottake', ' '.join(lines), [], '', video=spec)
    if audio: p['audio'] = {'src': clip, 'start': start, 'gain': -4}
    return p


def pnl_edit(ms, clip=None, start=0, card=None, dur=8, focus=.5, pid='pnl_edit', audio=None, still=None, move=None, **_):
    cf = still_frames(still, dur, os.path.join(CLIPS, pid), **(move or {})) if still else clip_frames(clip, start, dur, os.path.join(CLIPS, pid), focus=focus)
    spec = dict(card, fmt='pnl_edit', clip=cf, dur=dur, cta=fm.brand().get('cta'))
    p = fm._post(pid, 'pnl_edit', card.get('title', ''), [], '', video=spec)
    if audio: p['audio'] = audio
    return p


def livetape(ms=None, tape=None, lead=40, tail=8, speed=1.6, pid=None, **_):
    """the real BTC 15-minute market filmed live (livetape.py btc15): the last `lead` seconds, the finish and `tail` seconds after"""
    import glob
    tape = tape or sorted(glob.glob(os.path.join(ROOT, 'footage', 'btc15m_*.mp4')))[-1]
    if not os.path.isabs(tape): tape = os.path.join(ROOT, tape)
    info = json.load(open(tape.replace('.mp4', '.json'), encoding='utf-8'))
    end = info['end_in_clip_s']; start = max(0, end - lead)
    vdur = (lead + tail) / speed
    cf = clip_frames(tape, start, vdur, os.path.join(CLIPS, pid or 'livetape'), speed=speed, focus_y=0.12)
    res = info.get('result') or ''
    tgt = info.get('target'); tgt_s = '${:,.0f}'.format(tgt) if tgt else 'the target'
    r_at = lead / speed
    steps = [{'at': 0.0, 'lines': ['Bitcoin has %d seconds' % lead, 'to finish above %s' % tgt_s]},
             {'at': r_at * 0.45, 'lines': ['UP or DOWN?', 'Watch the last seconds']}, {'at': r_at - 1.6, 'lines': ['3... 2... 1...']}]
    spec = {'fmt': 'livetape', 'clip': cf, 'dur': vdur + 3.2, 'steps': steps, 'result': res, 'resultAt': r_at,
            'endAt': vdur, 'endTitle': 'It finished *%s*' % res if res == 'UP' else 'It finished ^%s^' % res,
            'endSub': 'Every 15 minutes there is a new Bitcoin market on Outcome. Same question: up or down?',
            'cta': 'Call the next one on Outcome.xyz'}
    cap = ('Bitcoin had %d seconds to finish above %s. It finished %s.\n\nFilmed live on outcome.xyz, the BTC 15-minute market (%s UTC). '
           'Not financial advice. %s' % (lead, tgt_s, res, info['window_end_utc'][11:16], fm.risk_line()))
    p = fm._post(pid or 'livetape_%s' % os.path.basename(tape)[7:11], 'livetape', 'BTC 15-minute finish', [], cap, video=spec)
    return p


def _hundred(ps):
    """chances -> whole dots that add to 100 (largest remainder)"""
    raw = [100 * p for p in ps]; base = [int(x) for x in raw]
    for i in sorted(range(len(raw)), key=lambda i: -(raw[i] - base[i]))[:100 - sum(base)]: base[i] += 1
    return base


def outof100(ms, match=None, market=None, outcome=None, title=None, foot=None, pid=None, **_):
    """'If tonight was played 100 times': a match split into 100 dots; or one outcome lit inside 100 (market + outcome)"""
    import ocs
    if match:
        m = ocs.find(ms, match)
        A, B = fm.pair(fm.team(m['outcomes'][0]['label']), fm.team(m['outcomes'][-1]['label']))
        ps = [r['p'] for r in m['outcomes']]; tot = sum(ps); ps = [p / tot for p in ps]
        n = _hundred(ps)
        groups = [{'label': '%s wins' % A['short'], 'n': n[0], 'color': A['c1'] or '#D4FF3A', 'pulse': ps[0] >= ps[-1]},
                  {'label': 'draws', 'n': n[1], 'color': '#3A3F4A'},
                  {'label': '%s wins' % B['short'], 'n': n[2], 'color': B['c1'] or '#FF2E88', 'pulse': ps[-1] > ps[0]}]
        when = 'tonight' if fm.dayname(m['start']) == _today() else 'this game'
        title = title or 'If %s was played *100 times*' % ('%s v %s' % (A['short'], B['short']) if when == 'this game' else 'tonight\'s %s v %s' % (A['short'], B['short']))
        foot = foot or 'That is what %d%% means. Who do you have?' % round(100 * max(ps[0], ps[-1]))
        key = m['key']
    else:
        m = ocs.find(ms, market); r = ocs.outcome(m, outcome); n = _hundred([r['p'], 1 - r['p']])
        groups = [{'label': outcome, 'n': n[0], 'color': '#FF2E88', 'pulse': True}, {'label': 'not', 'n': n[1], 'color': '#3A3F4A'}]
        title = title or 'Out of *100*'; foot = foot or 'That is what %d%% means.' % round(100 * r['p']); key = m['key']
    spec = {'fmt': 'outof100', 'title': title, 'groups': groups, 'foot': foot, 'stamp': fm.stamp()}
    cap = ('%s\n\n%s\n\nChances from Outcome.xyz market prices at %s. %s' % (title.replace('*', ''), ' / '.join('%d %s' % (g['n'], g['label']) for g in groups), fm.stamp(), fm.risk_line()))
    return fm._post(pid or 'outof100_%s' % key, 'outof100', title, [], cap, video=spec)


def aichat(ms, match, ai_pick, ai_answer, day=1, score='', pid=None, **_):
    """AI vs the money. ai_pick = the side the AI named (a team name or 'Draw'); ai_answer = the AI's real reply text.
    Only use a real AI answer (asked fresh at build time); never write one by hand and call it AI."""
    import ocs
    m = ocs.find(ms, match)
    rows = _side_rows(m)
    best = max(range(len(rows)), key=lambda i: rows[i]['p'])
    A, B = fm.team(m['outcomes'][0]['label']), fm.team(m['outcomes'][-1]['label'])
    fav = rows[best]['label']
    pick_short = fm.team(ai_pick)['short'] if ai_pick != 'Draw' else 'Draw'
    agree = pick_short == fav
    q = 'Who wins %s v %s tonight? One answer.' % (A['short'], B['short'])
    spec = {'fmt': 'aichat', 'day': day, 'score': score, 'question': q, 'answer': ai_answer, 'money': rows, 'moneyBest': best,
            'agree': agree, 'verdict': 'They agree' if agree else 'They disagree', 'stamp': fm.stamp()}
    cap = ('AI vs the money, day %d \U0001F916\n\nThe AI says %s. The money says %s (%d%%). %s\n\nChances from Outcome.xyz at %s. %s'
           % (day, pick_short, fav, round(100 * rows[best]['p']), 'Who is right? Results after full time.', fm.stamp(), fm.risk_line()))
    return fm._post(pid or 'aichat_%s' % m['key'], 'aichat', 'AI vs the money', [], cap, video=spec,
                    notes='Series: track AI vs money wins in a running score; the AI answer must be a real model reply.')


# ================================================================== newer video formats (templates/motion_more.js), each with its own look
#   countdown  broadcast  the money's top N, revealed from the last place to the favourite
#   quizclock  tabloid    guess the favourite: 3-second clock per round, then the real chances
#   forecast   weather    tonight's football forecast: sunny (sure things), storms (coin flips), upset watch
#   race       neon       club balls race; the finishing order is a draw weighted by the real chances (seed logged)
#   sim100     paper      one match played 100 times, cells resolve then sort into blocks
#   linestory  terminal   one chart: the line draws itself, the event is pinned, the number that matters lands
CITY = {'Arsenal': 'London', 'Chelsea': 'London', 'Tottenham Hotspur': 'London', 'Viking': 'Stavanger', 'Inter Milan': 'Milan', 'AC Milan': 'Milan',
        'Galatasaray': 'Istanbul', 'Fenerbahce': 'Istanbul', 'RC Lens': 'Lens', 'Villarreal CF': 'Villarreal', 'Sabah Baku': 'Baku', 'Atletico Madrid': 'Madrid',
        'Real Madrid': 'Madrid', 'RB Leipzig': 'Leipzig', 'Slovan Bratislava': 'Bratislava', 'Manchester City': 'Manchester', 'Manchester United': 'Manchester',
        'FK Bodo/Glimt': 'Bodo', 'Aston Villa': 'Birmingham', 'AS Roma': 'Rome', 'Real Betis': 'Seville', 'LASK Linz': 'Linz', 'Feyenoord': 'Rotterdam',
        'FC Bayern Munich': 'Munich', 'Bayern Munich': 'Munich', 'FC Barcelona': 'Barcelona', 'Barcelona': 'Barcelona', 'Liverpool': 'Liverpool',
        'Paris Saint Germain': 'Paris', 'Paris Saint-Germain': 'Paris', 'Napoli': 'Naples', 'Borussia Dortmund': 'Dortmund', 'Juventus': 'Turin',
        'Sporting CP': 'Lisbon', 'Benfica': 'Lisbon', 'FC Porto': 'Porto', 'PSV Eindhoven': 'Eindhoven', 'Ajax': 'Amsterdam', 'Club Brugge': 'Bruges',
        'Newcastle United': 'Newcastle', 'Como': 'Como', 'AEK Athens': 'Athens', 'Olympiacos': 'Piraeus', 'Celtic': 'Glasgow', 'Rangers': 'Glasgow'}


def _lum(h):
    r, g, b = fm._rgb(h); return (.2126 * r + .7152 * g + .0722 * b) / 255


def _ink(t, alt='#141414'):
    """a team colour that reads on a light page (white kits switch to their second colour)"""
    c = t.get('c1') or alt
    return c if _lum(c) < .82 else (t.get('c2') if t.get('c2') and _lum(t['c2']) < .82 else alt)


def _sides(m):
    A, B = fm.pair(fm.team(m['outcomes'][0]['label']), fm.team(m['outcomes'][-1]['label']))
    pa, pb = m['outcomes'][0]['p'], m['outcomes'][-1]['p']
    dr = next((r['p'] for r in m['outcomes'] if r['label'] == 'Draw'), None)
    return A, B, pa, pb, dr


def _when(m):
    return ('Tonight, ' if fm.dayname(m['start']) == _today() else fm.dayname(m['start']).split(' ')[0] + ', ') + fm.ko(m['start'])


def _pc(p):
    return '<1%' if 0 < p < .005 else '%d%%' % round(100 * p)


def countdown(ms, market, n=8, title=None, kicker=None, foot=None, pid=None, **_):
    import ocs
    m = ocs.find(ms, market)
    kind = 'person' if 'Ballon' in (m.get('title') or '') else 'team'
    rows = sorted(fm.real_rows(m), key=lambda r: -r['p'])[:n]
    items = []
    for i, r in enumerate(rows):
        d24 = None
        try:
            first, _x = fm.change_24h(r['coin']); d24 = (r['p'] - first) if first is not None else None
        except Exception:
            pass
        ent = fm.entity(r['label'], kind)
        items.append({'rank': i + 1, 'label': ent['short'] if kind == 'team' else r['label'], 'team': ent, 'p': r['p'], 'd24': d24})
        time.sleep(.2)
    nice = {'UEFA Champions League winner': 'Champions League 2026/27', 'English Premier League winner': 'Premier League 2026/27', "Ballon d'Or": "Ballon d'Or 2026"}
    short = (m.get('short') or m['title']).strip()
    spec = {'fmt': 'countdown', 'kicker': kicker or nice.get(short, short), 'title': title or "Who wins it? The money's *top %d*" % len(items), 'items': items,
            'foot': foot or 'Who is too low? Comment 👇', 'stamp': fm.stamp()}
    cap = ("%s: the money's top %d right now \U0001F3C6\n\n%s\n\nWho is too low? Comment below.\n\nChances from Outcome.xyz market prices at %s. %s"
           % (spec['kicker'], len(items), '\n'.join('%d. %s %s' % (x['rank'], x['label'], _pc(x['p'])) for x in items), fm.stamp(), fm.risk_line()))
    return fm._post(pid or 'countdown_%s' % m['key'], 'countdown', spec['title'], [], cap, video=spec)


def quizclock(ms, matches, title='Guess the favourite', sub=None, clock=3, clock2=2.5, pid=None, **_):
    import ocs
    rounds = []
    for q in matches:
        m = ocs.find(ms, q); A, B, pa, pb, dr = _sides(m)
        rounds.append({'a': {'label': A['short'], 'team': A, 'p': pa}, 'b': {'label': B['short'], 'team': B, 'p': pb}, 'draw': dr, 'best': 0 if pa >= pb else 1,
                       'meta': '%s · %s' % (_when(m), 'Champions League' if 'Champions' in (m.get('comp') or '') else (m.get('comp') or ''))})
    spec = {'fmt': 'quizclock', 'title': title, 'sub': sub or 'Who does the money back? 3 seconds each.', 'rounds': rounds, 'clock': clock, 'clock2': clock2, 'stamp': fm.stamp()}
    fav = lambda r: r['b'] if r['best'] else r['a']
    dog = lambda r: r['a'] if r['best'] else r['b']
    tie = lambda r: round(100 * r['a']['p']) == round(100 * r['b']['p'])
    line = lambda r: ('%s v %s: %s %.1f%%, just ahead of %s %.1f%%' % (r['a']['label'], r['b']['label'], fav(r)['label'], 100 * fav(r)['p'], dog(r)['label'], 100 * dog(r)['p'])
                      if tie(r) else '%s v %s: %s %s' % (r['a']['label'], r['b']['label'], fav(r)['label'], _pc(fav(r)['p'])))
    cap = ('Guess the favourite ⏱️ %d games, 3 seconds each. Comment your score!\n\n%s\n\nChances from Outcome.xyz market prices at %s. %s'
           % (len(rounds), '\n'.join(line(r) for r in rounds), fm.stamp(), fm.risk_line()))
    return fm._post(pid or 'quizclock', 'quizclock', title, [], cap, video=spec)


def forecast(ms, comp='UEFA Champions League', keys=None, day=None, hero=None, pid=None, **_):
    """tonight's matches as a weather report: sunny = favourite 70%+, storm = no side above 50%, upset watch = the best long shots"""
    if keys:
        games = [next(x for x in ms if x['key'] == k) for k in keys]
    else:
        day = day or _today()
        games = [x for x in ms if x['kind'] == 'match3' and comp in (x.get('comp') or '') and fm.dayname(x['start']) == day]
    if not games: return None
    rows = []
    for m in games:
        A, B, pa, pb, dr = _sides(m)
        fav, dog, pf, pd = (A, B, pa, pb) if pa >= pb else (B, A, pb, pa)
        home = m['outcomes'][0]['label']
        rows.append({'m': m, 'A': A, 'B': B, 'fav': fav, 'dog': dog, 'pf': pf, 'pd': pd, 'dr': dr, 'city': CITY.get(home, fm.team(home)['short']),
                     'time': fm.ko(m['start']).split(' ')[0]})
    rows.sort(key=lambda r: -r['pf'])
    h = next((r for r in rows if r['m']['key'] == hero), rows[0]) if hero else rows[0]
    sunny = [r for r in rows if r['pf'] >= .7 and r is not h][:3]
    storm = sorted([r for r in rows if r['pf'] < .5 and r is not h], key=lambda r: r['pf'] - r['pd'])[:3]
    rest = sorted([r for r in rows if .5 <= r['pf'] < .7 and r is not h], key=lambda r: -r['pd'])[:3]
    ln = lambda r: '%s v %s' % (r['A']['short'], r['B']['short'])
    groups = []
    if sunny:
        groups.append({'title': 'Sunny spells', 'sub': 'The near-sure things', 'icon': 'sun', 'sky': 'A', 'label': 'FAVOURITE TO WIN',
                       'rows': [{'time': r['time'], 'city': r['city'], 'line': '%s · %s' % (ln(r), r['fav']['short']), 'p': r['pf'], 'icon': 'sun'} for r in sunny]})
    if storm:
        groups.append({'title': 'Storm warning', 'sub': 'Too close to call', 'icon': 'storm', 'sky': 'B', 'label': 'NOBODY ABOVE 50%', 'fx': 'thunder',
                       'rows': [{'time': r['time'], 'city': r['city'], 'line': '%s · %s just ahead' % (ln(r), r['fav']['short']), 'p': r['pf'],
                                 'icon': 'storm' if r['pf'] < .45 else 'cloud'} for r in storm]})
    if rest:
        groups.append({'title': 'Upset watch', 'sub': 'The best long shots', 'icon': 'bolt', 'sky': 'C', 'label': 'UNDERDOG CHANCE', 'fx': 'bolt',
                       'rows': [{'time': r['time'], 'city': r['city'], 'line': ('%s at %s' if r['dog'] is r['B'] else '%s v %s') % (r['dog']['short'], r['fav']['short']),
                                 'p': r['pd'], 'icon': 'bolt'} for r in rest]})
    wd = fm.dayname(h['m']['start']).split(' ')[0]
    full = {'Mon': 'Monday', 'Tue': 'Tuesday', 'Wed': 'Wednesday', 'Thu': 'Thursday', 'Fri': 'Friday', 'Sat': 'Saturday', 'Sun': 'Sunday'}.get(wd, wd)
    hp = h['pf']
    spec = {'fmt': 'forecast', 'when': '%s NIGHT · %s' % (full.upper(), 'CHAMPIONS LEAGUE' if 'Champions' in comp else comp.upper()),
            'hero': {'city': h['city'], 'p': hp, 'icon': 'sun' if hp >= .7 else 'partly' if hp >= .55 else 'cloud',
                     'cond': '%s for %s' % ('Sunny' if hp >= .7 else 'Mostly sunny' if hp >= .55 else 'Cloudy', h['fav']['short']),
                     'sub': 'Chance of a %s win: %s · Draw: %s' % (h['dog']['short'], _pc(h['pd']), _pc(h['dr'] or 0)),
                     'line': 'Kick-off %s · %s v %s' % (fm.ko(h['m']['start']), h['A']['short'], h['B']['short'])},
            'groups': groups, 'endTitle': 'Forecast check *tomorrow morning*', 'endSub': 'Did the sun shine? Who got caught in the storm?',
            'cta': fm.brand().get('cta') or 'Make your call on Outcome.xyz', 'stamp': fm.stamp()}
    cap = ("Tonight's football forecast ☀️⛈️\n\nSunniest spot: %s, %s %s.\n%s\n\nForecast check tomorrow morning.\n\nChances from Outcome.xyz market prices at %s. %s"
           % (h['city'], h['fav']['short'], _pc(hp), '\n'.join('%s: %s' % (g['title'], ', '.join('%s %s' % (r['line'].split(' · ')[0], _pc(r['p'])) for r in g['rows'])) for g in groups),
              fm.stamp(), fm.risk_line()))
    return fm._post(pid or 'forecast_%s' % h['m']['start'][:8], 'forecast', 'Football forecast', [], cap, video=spec,
                    notes='Series: post the forecast check the next morning (which sunny calls held, which storms broke).')


def race(ms, market, n=6, seed=None, race_no=1, title=None, pid=None, **_):
    """the finishing order is a weighted draw from the real chances (renormalised over the balls shown); the seed is logged so the race is not staged"""
    import ocs
    m = ocs.find(ms, market)
    rows = sorted(fm.real_rows(m), key=lambda r: -r['p'])[:n]
    balls = [{'label': fm.team(r['label'])['short'], 'team': fm.team(r['label']), 'p': r['p']} for r in rows]
    seed = int(time.strftime('%Y%m%d')) if seed is None else seed
    rnd = random.Random(seed); left = list(range(len(balls))); order = []
    while left:
        w = [balls[i]['p'] for i in left]; x = rnd.random() * sum(w); acc = 0; pick = left[-1]
        for i, wi in zip(left, w):
            acc += wi
            if x <= acc:
                pick = i; break
        order.append(pick); left.remove(pick)
    short = (m.get('short') or m['title']).strip()
    win = balls[order[0]]
    spec = {'fmt': 'race', 'kicker': 'Race #%d' % race_no, 'title': title or 'If the title race was a *race*', 'balls': balls, 'order': order, 'seed': seed,
            'note': "Each ball's chance to win this race is its real title chance on Outcome. One race, drawn at random with those chances. Animation, not a forecast.",
            'cta': 'Race #%d tomorrow. Who wins it? 👇' % (race_no + 1), 'stamp': fm.stamp()}
    cap = ("Race #%d of the %s \U0001F3C1 %s won this one.\n\nEach ball's chance to win = its real chance on Outcome:\n%s\n\n"
           "One race, drawn at random with those chances (seed %d). Animation, not a forecast. Race #%d tomorrow.\n\nChances from Outcome.xyz market prices at %s. %s"
           % (race_no, short.replace('English ', ''), win['label'], '\n'.join('%s %s' % (b['label'], _pc(b['p'])) for b in balls), seed, race_no + 1, fm.stamp(), fm.risk_line()))
    return fm._post(pid or 'race_%s_%d' % (m['key'], race_no), 'race', spec['title'], [], cap, video=spec,
                    notes='Series: keep the race count and a running tally of winners; the seed (date) is logged so the draw is reproducible.')


def sim100(ms, match, seed=None, title=None, pid=None, **_):
    import ocs
    m = ocs.find(ms, match); A, B, pa, pb, dr = _sides(m)
    tot = pa + pb + (dr or 0); n = _hundred([pa / tot, (dr or 0) / tot, pb / tot])
    ca, cb = _ink(A), _ink(B)
    dist = lambda x, y: sum((p - q) ** 2 for p, q in zip(fm._rgb(x), fm._rgb(y))) ** .5
    if dist(ca, cb) < 140:                                  # two reds (Atletico v United): the second side goes dark ink
        cb = next((c for c in (B.get('c2'), '#141414', '#1F4FD8') if c and _lum(c) < .82 and dist(ca, c) >= 140), '#141414')
    groups = [{'label': '%s win' % A['short'], 'short': '%s win' % A['short'], 'color': ca, 'n': n[0]}, {'label': 'Draw', 'short': 'draw', 'color': '#9A948A', 'n': n[1]},
              {'label': '%s win' % B['short'], 'short': '%s win' % B['short'], 'color': cb, 'n': n[2]}]
    seed = int(time.strftime('%Y%m%d')) if seed is None else seed
    seq = [0] * n[0] + [1] * n[1] + [2] * n[2]; random.Random(seed).shuffle(seq)
    dog = 2 if pb < pa else 0
    spec = {'fmt': 'sim100', 'kicker': ('%s · Champions League' % _when(m)) if 'Champions' in (m.get('comp') or '') else _when(m),
            'title': title or '%s v %s, played *100 times*' % (A['short'], B['short']), 'groups': groups, 'seq': seq, 'seed': seed, 'highlight': dog,
            'foot': 'Tonight is ONE of these 100. Which one? 👇', 'stamp': fm.stamp()}
    cap = ('%s v %s, played 100 times \U0001F4CA\n\n%d %s wins, %d draws, %d %s wins. That is what the chances mean.\nTonight is one of these 100. Which one?\n\n'
           'Chances from Outcome.xyz market prices at %s. %s' % (A['short'], B['short'], n[0], A['short'], n[1], n[2], B['short'], fm.stamp(), fm.risk_line()))
    return fm._post(pid or 'sim100_%s' % m['key'], 'sim100', spec['title'], [], cap, video=spec)


def linestory(ms, market, labels, names=None, days=24, title=None, kicker=None, hero_label=None, next_line=None, next_caption=None, foot=None, pid=None, **_):
    """two outcomes of one market as lines over `days` daily prices; the crossing (if any) is pinned"""
    import ocs, datetime as dt
    m = ocs.find(ms, market)
    end = int(time.time() * 1000); start = end - days * 86400000
    cols_ = ['#39FF14', '#FF4040']
    series = []
    for i, lab in enumerate(labels):
        r = ocs.outcome(m, lab)
        rows = od.candles(r['coin'], '1d', start, end); time.sleep(.25)
        pts = [[c[0], c[4]] for c in rows]
        if r.get('p') is not None: pts.append([end, r['p']])
        series.append({'label': (names or labels)[i], 'color': cols_[i % 2], 'pts': pts})
    s0, s1 = series[0]['pts'], series[1]['pts']
    v1 = {p[0]: p[1] for p in s1}
    ev = None
    for j in range(1, len(s0)):
        a, b = s0[j - 1], s0[j]
        if a[0] in v1 and b[0] in v1 and a[1] < v1[a[0]] and b[1] >= v1[b[0]]:
            ev = {'t': b[0], 'label': 'THE FLIP · %s' % dt.datetime.fromtimestamp(b[0] / 1000, dt.timezone.utc).strftime('%d %b').lstrip('0').upper()}
    upto = len(s0) if ev is None else next(j for j, p in enumerate(s0) if p[0] == ev['t'])
    lo = min(s0[:max(1, upto)], key=lambda p: p[1]); now = s0[-1]
    days_from = max(1, round((now[0] - lo[0]) / 86400000))
    delta = '%+d PTS IN %d DAYS' % (round(100 * (now[1] - lo[1])), days_from)
    fmtd = lambda x: dt.datetime.fromtimestamp(x / 1000, dt.timezone.utc).strftime('%d %b').lstrip('0').upper()
    spec = {'fmt': 'linestory', 'kicker': kicker or 'OUTCOME // %s' % (m.get('short') or m['title']).upper(), 'title': title or (m.get('short') or m['title']),
            'heroLabel': hero_label or 'CHANCE: %s' % series[0]['label'].upper(), 'delta': delta, 'series': series, 'event': ev,
            'xLabels': [[s0[0][0], fmtd(s0[0][0])], [now[0], 'NOW']], 'next': next_line or '', 'foot': foot or 'Will it flip back? 👇', 'stamp': fm.stamp()}
    cap = ('%s\n\n%s: %s to %s in %d days. %s: %s now.\n%s\n\nDaily chances from Outcome.xyz to %s. Not financial advice. %s'
           % (spec['title'], series[0]['label'], _pc(lo[1]), _pc(now[1]), days_from, series[1]['label'], _pc(s1[-1][1]), next_caption or next_line or '', fm.stamp(), fm.risk_line()))
    return fm._post(pid or 'linestory_%s' % m['key'], 'linestory', spec['title'], [], cap, video=spec)


def _plain(s):
    return (s or '').replace('*', '').replace('^', '').replace('~', '').replace('_', '')


def take(ms, market, labels, lines, still=None, clip=None, start=0, move=None, title=None, note=None, kicker='Receipt', cut=3.4, dur=9, pid=None, **_):
    """hot take in big words over footage (a photo with a camera move, or a clip), then the receipt: the real chances of `labels` in `market`"""
    import ocs
    m = ocs.find(ms, market)
    kind = 'person' if 'Ballon' in (m.get('title') or '') else 'team'
    rows = []
    for lab in labels:
        r = ocs.outcome(m, lab); rows.append({'label': r['label'], 'team': fm.entity(r['label'], kind), 'p': r['p']})
    if still and not os.path.isabs(still): still = os.path.join(ROOT, still)
    if clip and not os.path.isabs(clip): clip = os.path.join(ROOT, clip)
    short = (m.get('short') or m['title']).strip()
    receipt = {'kicker': kicker, 'title': title or "The money's *%s*" % short, 'rows': rows, 'note': note or ''}
    p = hottake(ms, clip=clip, start=start, lines=lines, receipt=receipt, dur=dur, cut=cut, pid=pid or 'take_%s' % m['key'], still=still, move=move)
    p['caption'] = ('%s?\n\nThe money says: %s.\n%s\n\nChances from Outcome.xyz market prices at %s. %s'
                    % (' '.join(_plain(l) for l in lines), ', '.join('%s %s' % (r['label'], _pc(r['p'])) for r in rows), _plain(note), fm.stamp(), fm.risk_line()))
    return p


def pnl_film(ms, username, coin=None, hours=2400, still=None, clip=None, start=0, move=None, title=None, side=None, mask=True, dur=7, pid=None, **_):
    """the client's P&L edit: our card from the real trade (traders.pnl_card) drops in over footage. mask=True hides the username (client OK pending)"""
    import traders
    card, info = traders.pnl_card(username, coin=coin, hours=hours, ms=ms)
    if title: card['title'] = title
    if side: card['side'] = side
    if mask: card['username'] = username[:1] + '•' * 5 + username[-2:]
    if still and not os.path.isabs(still): still = os.path.join(ROOT, still)
    if clip and not os.path.isabs(clip): clip = os.path.join(ROOT, clip)
    p = pnl_edit(ms, clip=clip, start=start, still=still, move=move, card=card, dur=dur, pid=pid or 'pnl_edit_%s' % username)
    p['caption'] = ('%s: %s.\n\nBought at %.0f cents, paid out $1.00 a share. %s shares, profit $%s.\n\nReal trade from Outcome\'s public data. Past results do not predict future results. %s'
                    % (card.get('title', ''), card.get('side', ''), 100 * (info.get('avg') or 0), '{:,.0f}'.format(info.get('bought') or 0),
                       '{:,.0f}'.format(info.get('profit') or 0), fm.risk_line()))
    p['notes'] = 'HOLD: a real trader. Username masked until the client OKs showing usernames.'
    return p


def goalclip(ms, key, n=1, hook=None, pid=None, **_):
    """the real outcome.xyz match page filmed live by goalcam.py: the price jumps on screen when the goal goes in.
    Works after the market has settled: team names and prices come from the goal-cam files, not the live market list."""
    base = os.path.join(ROOT, 'footage', 'goalcam_%s_%d' % (key, n))
    e = json.load(open(base + '.json', encoding='utf-8'))
    ev = json.load(open(os.path.join(ROOT, 'out', '_goalcam', key, 'events.json'), encoding='utf-8'))
    labels = ev.get('labels') or [x.strip() for x in ev['title'].split(' v ')]
    A, B = fm.pair(fm.team(labels[0]), fm.team(labels[-1]))
    # jump_in_clip_s comes from 10-second price polls and lands up to 5 s late: show the goal 2.5 s earlier so cause comes before effect
    J_clip = (e['jump_in_clip_s'] - 2.5) if e.get('jump_in_clip_s') is not None else max(0, e['event_in_clip_s'] - 25)
    import subprocess, re
    from render import FFMPEG
    r = subprocess.run([FFMPEG, '-i', e['clip']], capture_output=True, text=True, errors='ignore').stderr
    mm = re.search(r'Duration: (\d+):(\d+):([\d.]+)', r); clip_len = int(mm.group(2)) * 60 + float(mm.group(3)) if mm else 60
    start = max(0, J_clip - 4.0); dur = min(9.5, clip_len - start); J = J_clip - start
    cf = clip_frames(e['clip'], start, dur, os.path.join(CLIPS, pid or 'goalclip_%s_%d' % (key, n)), focus_y=0.2)
    side, badge, score = None, 'BIG MOVE', ''
    if e.get('kind') == 'score' and e.get('was'):
        h0, a0 = [int(x) for x in e['was'].split('-')]; h1, a1 = [int(x) for x in e['score'].split('-')]
        side = 0 if h1 > h0 else -1 if a1 > a0 else None
        badge = 'GOAL'; score = '%s %d-%d %s' % (A['short'], h1, a1, B['short'])
    pb, pa = e.get('p_before'), e.get('p_after')
    if side is None and pb and pa:
        side = 0 if abs(pa[0] - pb[0]) >= abs(pa[-1] - pb[-1]) else -1
    chip_ = None
    if pb and pa and side is not None and pb[side] is not None and pa[side] is not None:
        chip_ = {'team': A if side == 0 else B, 'from': pb[side], 'to': pa[side]}
    spec = {'fmt': 'goalclip', 'clip': cf, 'jump': J, 'endAt': min(dur, J + 5.0), 'dur': min(dur, J + 5.0) + 3.2, 'kicker': 'Live on Outcome',
            'hook': hook or '%s v %s: *watch the price*' % (A['short'], B['short']), 'badge': badge, 'score': score, 'chip': chip_,
            'endTitle': 'Every goal moves the *price*', 'endSub': 'The real Outcome app, filmed live during %s v %s.' % (A['short'], B['short']),
            'cta': fm.brand().get('cta') or 'Make your call on Outcome.xyz'}
    who = (A if side == 0 else B)['short'] if side is not None else None
    cap = ('%s\n\nFilmed live on outcome.xyz during %s v %s. %s %s' % (
        ('%s scored and their chance went from %s to %s in seconds.' % (who, _pc(chip_['from']), _pc(chip_['to']))) if (badge == 'GOAL' and chip_)
        else 'Watch the price move live.', A['short'], B['short'], 'The price is the crowd\'s chance.', fm.risk_line()))
    return fm._post(pid or 'goalclip_%s_%d' % (key, n), 'goalclip', '%s v %s' % (A['short'], B['short']), [], cap, video=spec,
                    notes='Screen recording of the public outcome.xyz match page (no broadcast footage).')


def _flag(ent):
    """a person's national flag (assets/flags, flag-icons MIT) as a file URL, or None"""
    c = (ent or {}).get('country')
    p = os.path.join(ROOT, 'assets', 'flags', '%s.svg' % c) if c else None
    return file_url(p) if p and os.path.exists(p) else None


def thennow(ms, market, days=30, n=3, title=None, kicker=None, foot=None, pid=None, **_):
    """Then vs Now: the top n of a market today, with their chance `days` ago (or the market's first day if it is younger) above"""
    import ocs, datetime as dt
    m = ocs.find(ms, market)
    kind = 'person' if 'Ballon' in (m.get('title') or '') else 'team'
    end = int(time.time() * 1000); target = end - days * 86400000
    items = []
    for r in sorted(fm.real_rows(m), key=lambda r: -r['p'])[:n]:
        c = od.candles(r['coin'], '1d', end - (days + 6) * 86400000, end); time.sleep(.25)
        if not c: continue
        th = min(c, key=lambda x: abs(x[0] - target))
        ent = fm.entity(r['label'], kind)
        items.append({'label': ent['short'] if kind == 'team' else r['label'], 'team': ent, 'flag': _flag(ent) if kind == 'person' else None,
                      'then': th[4], 'now': r['p'], 'then_t': th[0]})
    if len(items) < 2: return None
    t_then = min(x['then_t'] for x in items)
    span = max(1, round((end - t_then) / 86400000))
    d_then = dt.datetime.fromtimestamp(t_then / 1000, dt.timezone.utc).strftime('%d %b').lstrip('0').upper()
    short = (m.get('short') or m['title']).strip()
    nice = {'UEFA Champions League winner': 'Champions League', 'English Premier League winner': 'Premier League title', "Ballon d'Or": "Ballon d'Or"}.get(short, short)
    spec = {'fmt': 'thennow', 'kicker': kicker or '%s · CHANCE TO WIN' % nice.upper(), 'title': title or '%s: *then vs now*' % nice,
            'thenLabel': d_then, 'nowLabel': 'TODAY', 'span': '%d DAYS LATER' % span if span != 7 else 'ONE WEEK LATER', 'items': items,
            'foot': foot or 'Who moves next? Comment 👇', 'stamp': fm.stamp()}
    cap = ('%s, %s vs today \U0001F4C8\U0001F4C9\n\n%s\n\nWho moves next?\n\nDaily chances from Outcome.xyz to %s. %s'
           % (nice, d_then.title(), '\n'.join('%s: %s → %s' % (x['label'], _pc(x['then']), _pc(x['now'])) for x in items), fm.stamp(), fm.risk_line()))
    return fm._post(pid or 'thennow_%s' % m['key'], 'thennow', spec['title'], [], cap, video=spec)


# stock footage (footage/stock, Mixkit + Coverr free licences, frame-checked: no faces in focus, no logos); LICENCES.md lists every file
REEL_FOOTBALL = ['football/ball_turf_closeup_v', 'football/goal_net_pan', 'football/ball_rolling_closeup_v', 'football/stadium_stands_blur',
                 'football/ball_bounce_slowmo', 'football/pitch_aerial_day', 'football/ball_rolling_turf', 'football/players_warmup_blur',
                 'football/pickup_match_skyline_sunset']
REEL_CITY = {'London': 'city_night/london_tower_bridge_dusk', 'Paris': 'city_night/paris_arc_traffic_night'}


def _vdur(path):
    import subprocess, re
    from render import FFMPEG
    r = subprocess.run([FFMPEG, '-i', path], capture_output=True, text=True, errors='ignore').stderr
    m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', r)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)) if m else 0


def stock_cut(parts, out):
    """[(stock name, seconds), ...] -> one 1080x1920 30 fps clip, hard cuts, each part taken from about 1 s into its file"""
    import subprocess
    from render import FFMPEG
    cmd = [FFMPEG, '-y', '-loglevel', 'error']; flt = []
    for k, (name, d) in enumerate(parts):
        p = os.path.join(ROOT, 'footage', 'stock', name + '.mp4'); L = _vdur(p)
        cmd += ['-ss', '%.2f' % max(0, min(1.0, L - d - .2)), '-t', '%.3f' % d, '-i', p]
        flt.append('[%d:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1,setpts=PTS-STARTPTS[v%d]' % (k, k))
    flt.append(''.join('[v%d]' % k for k in range(len(parts))) + 'concat=n=%d:v=1:a=0[out]' % len(parts))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run(cmd + ['-filter_complex', ';'.join(flt), '-map', '[out]', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', out], check=True)
    return out


def reel(ms, comp='UEFA Champions League', day=None, keys=None, seg=1.45, title=None, pid=None, **_):
    """tonight's games in about 15 seconds: hard cuts on stock football footage (a city shot when the host city has one), one game per cut"""
    if keys:
        games = [next(x for x in ms if x['key'] == k) for k in keys]
    else:
        day = day or _today()
        games = [x for x in ms if x['kind'] == 'match3' and comp in (x.get('comp') or '') and fm.dayname(x['start']) == day]
    if not games: return None
    games.sort(key=lambda m: (m['start'], -max(m['outcomes'][0]['p'], m['outcomes'][-1]['p'])))
    intro, outro = 1.8, 3.4
    parts = [('football/pitch_aerial_night', intro)]; segs = []
    for i, m in enumerate(games):
        A, B, pa, pb, dr = _sides(m)
        city = CITY.get(m['outcomes'][0]['label'])
        parts.append((REEL_CITY.get(city) or REEL_FOOTBALL[i % len(REEL_FOOTBALL)], seg))
        segs.append({'at': intro + i * seg, 'dur': seg, 'a': {'label': A['short'], 'team': A}, 'b': {'label': B['short'], 'team': B},
                     'pa': pa, 'pb': pb, 'time': fm.ko(m['start'])})
    parts.append(('football/crowd_hands_backlit', outro))
    pid = pid or 'reel_%s' % games[0]['start'][:8]
    total = intro + len(games) * seg + outro
    src = stock_cut(parts, os.path.join(CLIPS, pid + '_src.mp4'))
    cf = clip_frames(src, 0, total, os.path.join(CLIPS, pid))
    n = len(games)
    spec = {'fmt': 'reel', 'clip': cf, 'dur': total - .1, 'segs': segs, 'outroAt': intro + n * seg, 'kicker': 'Tonight · Champions League' if 'Champions' in comp else 'Tonight',
            'title': title or "Tonight's %d games in *15 seconds*" % n, 'endTitle': 'Who are you *backing* tonight?', 'cta': fm.brand().get('cta') or 'Make your call on Outcome.xyz',
            'stamp': fm.stamp()}
    lines = []
    for g in segs:
        fav = g['a'] if g['pa'] >= g['pb'] else g['b']; pf = max(g['pa'], g['pb'])
        lines.append('%s v %s: %s' % (g['a']['label'], g['b']['label'], ('too close to call (%s / %s)' % (_pc(g['pa']), _pc(g['pb']))) if pf < .45 else '%s %s' % (fav['label'], _pc(pf))))
    cap = ("Tonight's Champions League in 15 seconds ⚽\n\n%s\n\nWho are you backing tonight?\n\nChances from Outcome.xyz market prices at %s. %s"
           % ('\n'.join(lines), fm.stamp(), fm.risk_line()))
    return fm._post(pid, 'reel', spec['title'], [], cap, video=spec, notes='Footage: stock clips (Mixkit and Coverr free licences, listed in footage/stock/LICENCES.md).')


def _bright(t, alt):
    """a team colour that shows on the dark night background"""
    c = t.get('c1') or alt
    if _lum(c) >= .2: return c
    return t['c2'] if t.get('c2') and _lum(t['c2']) >= .2 else alt


def _goal_times(a):
    """ESPN goals placed on the archived price line: the biggest jump of the scorer's line within 6 minutes of the estimated time"""
    import postmatch as pm
    out = []
    for g in (a.get('espn') or {}).get('goals', []):
        mn, extra = pm._min(g['min'])
        if mn is None: continue
        est = a['ko'] + (mn + extra + (17 if mn > 45 else 0)) * 60000
        line = a['lines'].get(a['home'] if g['side'] == 'home' else a['away']) or []
        win = [(line[i][0], line[i][1] - line[i - 1][1]) for i in range(1, len(line)) if abs(line[i][0] - est) <= 6 * 60000]
        t = max(win, key=lambda x: x[1])[0] if win else est
        out.append({'t': t, 'side': g['side'], 'label': "%s' %s" % (g['min'], g['who'])})
    return out


def _trade_lines(key, t0, a=None):
    """price lines for a match without goal-cam footage: real trades (candles WITH volume) plus 5-minute order-book snapshots
    kept only when the three chances add up to about 100% (a wide spread puts a mid anywhere), normalised, then a median of 3.
    Stale candles (no volume) are dropped: they repeat the last trade long after the match moved."""
    import glob as _g
    rows, coins = {}, {}
    for f in _g.glob(os.path.join(ROOT, 'data', 'archive', 'candles', key, '*.json')):
        x = json.load(open(f, encoding='utf-8')); coins[x['label']] = x['coin']
        rows[x['label']] = [(r[0], r[4]) for r in x['rows'] if r[0] >= t0 and (len(r) < 6 or float(r[5] or 0) > 0)]
    if a:
        labs = [a['home'], 'Draw', a['away']]
        if all(l in coins for l in labs):
            s = od.when(a['start'])
            days = {s.strftime('%Y%m%d'), (s + __import__('datetime').timedelta(hours=4)).strftime('%Y%m%d')} if s else set()
            for day in days:
                f = os.path.join(ROOT, 'data', 'archive', 'mids', day + '.jsonl')
                if not os.path.exists(f): continue
                for ln in open(f, encoding='utf-8'):
                    try: snap = json.loads(ln)
                    except ValueError: continue
                    if not (t0 <= snap['t'] <= t0 + 125 * 60000): continue
                    v = [snap['m'].get(coins[l]) for l in labs]
                    if any(x is None for x in v): continue
                    v = [float(x) for x in v]; tot = sum(v)
                    if abs(tot - 1) > .08: continue
                    for l, x in zip(labs, v): rows.setdefault(l, []).append((snap['t'], x / tot))
    out = {}
    for lab, pts in rows.items():
        pts = sorted(set(pts)); vs = [p for _, p in pts]
        out[lab] = [(pts[i][0], sorted(vs[max(0, i - 1):i + 2])[len(vs[max(0, i - 1):i + 2]) // 2]) for i in range(len(pts))]
    return out


def matchline(ms=None, key=None, focus=None, title=None, pid=None, **_):
    """the whole match told by the money, from the price archive (only games the archive saw live).
    Lines are traded prices; a side that barely traded is drawn faint and labelled, and the big number follows a line that really traded."""
    import postmatch as pm, datetime as dt
    a = pm.analyse(key)
    if not a or not a.get('espn') or not a['espn'].get('final'): return None
    A, B = fm.pair(fm.team(a['home']), fm.team(a['away']))
    ca, cb = _bright(A, '#D4FF3A'), _bright(B, '#FF2E88')
    dist = lambda x, y: sum((p - q) ** 2 for p, q in zip(fm._rgb(x), fm._rgb(y))) ** .5
    if dist(ca, cb) < 120: cb = max(('#22E1FF', '#D4FF3A', '#FFC83D', '#FF2E88', '#FFFFFF'), key=lambda c: dist(c, ca))   # the bright colour farthest from the home line
    t0 = a['ko'] - 4 * 60000
    tl_ = _trade_lines(key, t0, a); src_note = 'Real prices on Outcome (trades and the order book), from kick-off to the whistle.'
    gp = os.path.join(ROOT, 'out', '_goalcam', key, 'prices.jsonl')
    if os.path.exists(gp):                                   # filmed by goalcam.py: 10-second live prices, what the app showed
        polls = [json.loads(l) for l in open(gp) if l.strip()]
        labs = [a['home'], 'Draw', a['away']]                   # goalcam polls follow the market's outcome order: home, draw, away
        if len(polls) > 200:
            tl_ = {}
            for i, lab in enumerate(labs):
                pts = [(int(r['t'] * 1000), r['p'][i]) for r in polls if r['p'][i] is not None and int(r['t'] * 1000) >= t0]
                vs = [p for _, p in pts]
                tl_[lab] = [(pts[k][0], sorted(vs[max(0, k - 2):k + 3])[len(vs[max(0, k - 2):k + 3]) // 2]) for k in range(len(pts))]   # median of 5 polls
            src_note = 'Live prices on Outcome every 10 seconds, from kick-off to the whistle.'
    win = a.get('winner')
    end = max((t for l in tl_.values() for t, _ in l), default=a['ko'] + 113 * 60000)
    ft = next((t for t, p in tl_.get(win if win and win != 'Draw' else 'Draw', []) if t > a['ko'] + 95 * 60000 and p >= .97), min(end, a['ko'] + 113 * 60000))
    ser, changes = [], {}
    for lab, col, w in ((a['home'], ca, 8), ('Draw', '#8B919C', 5), (a['away'], cb, 8)):
        pts = [[t, p] for t, p in tl_.get(lab, []) if t <= ft]
        if not pts: pts = [[t0, a['pre'].get(lab) or 0]]
        if pts[0][0] > t0: pts.insert(0, [t0, pts[0][1]])
        if pts[-1][0] < ft: pts.append([ft, pts[-1][1]])
        pts.append([ft + 1, 1.0 if lab == (win or 'Draw') else 0.0])      # the market resolved: winner 100%, the rest 0%
        n_ch = sum(1 for i in range(1, len(pts)) if abs(pts[i][1] - pts[i - 1][1]) > 1e-9 and pts[i][0] >= a['ko'])
        changes[lab] = n_ch
        thin = n_ch < 5
        ser.append({'label': (fm.team(lab)['short'] if lab != 'Draw' else 'Draw') + (' (few trades)' if thin else ''), 'color': col, 'width': w, 'pts': pts, 'thin': thin})
    ev = a['espn']; score = '%d-%d' % (ev['home'], ev['away'])
    # the story: the winner (or the underdog when level); the big number follows that side if it traded, else the side that did
    if win and win != 'Draw': story = 0 if win == a['home'] else 1
    else: story = 0 if (a['pre'].get(a['home']) or 0) < (a['pre'].get(a['away']) or 0) else 1
    sl = a['home'] if story == 0 else a['away']
    if focus is None:
        focus = story if changes.get(sl, 0) >= 5 else (0 if changes.get(a['home'], 0) >= changes.get(a['away'], 0) else 1)
    fl = a['home'] if focus == 0 else a['away']
    steam = A if story == 0 else B; spre = a['pre'].get(sl) or 0; other = (B if story == 0 else A)['short']
    if win == sl and spre < .35:
        title = title or '*%s* had a *%d%%* chance %s %s' % (steam['short'], round(100 * spre), 'at' if story == 1 else 'against', other)
        end_t = '%d%% before kick-off. *They won %s.*' % (round(100 * spre), score)
    elif win == 'Draw' and spre < .2:
        title = title or '*%s* had *%d%%* against %s' % (steam['short'], round(100 * spre), other)
        end_t = '%d%% before kick-off. *They drew %s.*' % (round(100 * spre), score)
    else:
        g0 = (ev.get('goals') or [{}])[0].get('side')
        m0 = pm._min((ev.get('goals') or [{}])[0].get('min', '99'))[0] or 99
        if win and win != 'Draw' and g0 == ('home' if win == a['home'] else 'away') and m0 <= 10:
            wt = A if win == a['home'] else B
            title = title or '*%s* scored after *%d minutes*. Watch the price.' % (wt['short'], m0)
            end_t = '%s %s %s. *The price never looked back.*' % (A['short'], score, B['short'])
        elif win and win != 'Draw' and g0 and g0 != ('home' if win == a['home'] else 'away'):
            wt = A if win == a['home'] else B
            title = title or '*%s* went 1-0 down. *Watch the price.*' % wt['short']
            end_t = 'From 1-0 down to *%s %s %s*.' % (A['short'], score, B['short'])
        else:
            title = title or '%s %s %s, *told by the money*' % (A['short'], score, B['short'])
            end_t = '%s %s %s. *Every goal moved the price.*' % (A['short'], score, B['short'])
    goals = _goal_times(dict(a, lines={k: v for k, v in tl_.items()}))
    stamp = dt.datetime.fromtimestamp(a['ko'] / 1000, dt.timezone.utc).strftime('%d %b %Y').lstrip('0')
    spec = {'fmt': 'matchline', 'teams': [A, B], 'series': ser, 'goals': goals, 'ko': a['ko'], 't0': t0, 'ft': ft, 'focus': focus, 'pre': a['pre'].get(fl) or 0,
            'score': score, 'kicker': 'Full time · %s' % ('Champions League' if 'Champions' in (a.get('comp') or '') else (a.get('comp') or '')), 'title': title,
            'endTitle': end_t, 'endSub': src_note, 'cta': fm.brand().get('cta') or 'Make your call on Outcome.xyz',
            'stamp': stamp}
    gl = ', '.join(g['label'] for g in goals)
    cap = ('%s %s %s, told by the money \U0001F4C8\n\n%s\nGoals: %s\n\nPrices on Outcome.xyz during the match, %s. %s'
           % (A['short'], score, B['short'], end_t.replace('*', ''), gl, stamp, fm.risk_line()))
    return fm._post(pid or 'matchline_%s' % key, 'matchline', title, [], cap, video=spec)


def scoreboard(ms=None, keys=None, day=None, title=None, kicker=None, pid=None, **_):
    """last night's favourites: one row per game (the money's favourite at kick-off and its chance), a tick if it won, a cross if not"""
    import postmatch as pm, glob as _g
    if not keys:
        keys = sorted(os.path.basename(x) for x in _g.glob(os.path.join(ROOT, 'data', 'archive', 'candles', '*')))
    rows = []
    for k in keys:
        a = pm.analyse(k)
        if not a or not a.get('espn') or not a['espn'].get('final') or (day and not a['start'].startswith(day)): continue
        fav = a.get('fav'); ev = a['espn']; A, B = fm.team(a['home']), fm.team(a['away'])
        won = a.get('winner') == fav
        res = 'won' if won else ('drew' if a.get('winner') == 'Draw' else 'lost')
        rows.append({'team': fm.team(fav), 'p': a['pre'].get(fav) or 0, 'ok': won, 'line': '%s %d-%d %s' % (A['short'], ev['home'], ev['away'], B['short']),
                     'sub': '%s were favourites · %s' % (fm.team(fav)['short'], res), 'start': a['start']})
    if not rows: return None
    rows.sort(key=lambda r: (r['start'], -r['p']))
    n_ok = sum(r['ok'] for r in rows)
    spec = {'fmt': 'scoreboard', 'kicker': kicker or 'Last night · Champions League', 'title': title or 'Favourites went *%d for %d*' % (n_ok, len(rows)),
            'rows': rows, 'tally': '%d of %d favourites won' % (n_ok, len(rows)), 'stamp': fm.stamp()}
    cap = ("Last night the money's favourites went %d for %d ✅❌\n\n%s\n\nFavourite = the higher chance on Outcome.xyz at kick-off. %s"
           % (n_ok, len(rows), '\n'.join('%s %s (%s %s)' % ('✅' if r['ok'] else '❌', r['line'], r['team']['short'], _pc(r['p'])) for r in rows), fm.risk_line()))
    return fm._post(pid or 'scoreboard_%s' % rows[0]['start'][:8], 'scoreboard', spec['title'], [], cap, video=spec,
                    notes='Series: post the same board after every match night (a daily template holds views; research 22, N2).')


def render(st, v, out, size=(1080, 1920), hold=1.5):
    """a motion post's video with its sound baked in: the cue sheet comes from the template timeline (motion_more.js), else sfx.cues_for"""
    import sfx
    info = st.show(v, size) or {}
    dur = (info.get('dur') or 8) + hold
    lead = v.get('lead', .5)
    cues = st.js('window.getCues ? window.getCues() : []') or []
    cl = [(t - lead, nm, g) for t, nm, g in cues] if cues else sfx.cues_for(v, lead=lead)
    wav = sfx.mix([c for c in cl if c[0] >= 0], dur, out.replace('.mp4', '.wav'))
    return st.video(v, out, size, dur=dur, audio=wav)
