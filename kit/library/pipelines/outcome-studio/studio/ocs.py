"""ocs: Outcome studio. Scan live markets, plan a day's posts, build them, check them on one sheet.

python ocs.py scan                      what is on today (matches, big movers, leaderboard, macro) -> out/scan/<ts>.md
python ocs.py plan [YYYY-MM-DD]         write batches/<date>.json with a suggested set of posts (edit it: headlines, captions, facts)
python ocs.py build batches/<date>.json [--only id1,id2] [--no-video]
                                        render every post: Instagram slides 1080x1350, TikTok slides 1080x1920, video 1080x1920
                                        -> FINALS/<date>/<page>/NN_<id>/ + captions.txt (posting order), working files in out/<date>/
python ocs.py sheet <date>              one contact sheet of the batch -> out/<date>/_sheet.jpg

Recipes (batch "recipe" field) and their args are listed in README.md. Numbers are pulled live at build time and stamped.
Changed posts never overwrite delivered ones: a rebuild of a post that already has finals writes NN_<id>_v2, _v3...
"""
import json, os, sys, time, glob, shutil, re, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ocdata as od, formats as fm
from render import Studio

ROOT = od.ROOT
IG, TT = (1080, 1350), (1080, 1920)
HOLD = 2.5                                  # seconds the last frame of a video stays up


import motion as mo
from render import MOTION_FMTS
MOTION_RECIPES = {'timed', 'wheel', 'demo', 'hottake', 'pnl_edit', 'livetape', 'outof100', 'aichat', 'countdown', 'quizclock', 'forecast',
                  'race', 'sim100', 'linestory', 'take', 'pnl_film', 'goalclip', 'thennow', 'reel', 'matchline', 'scoreboard'}


def today():
    return dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d')


# ------------------------------------------------------------------ finding markets
def find(ms, q, kind=None):
    """market by key ('Q412', 'O8573'), by kind ('fed'), or by words in its title ('Manchester City v Paris')"""
    if isinstance(q, dict): kind, q = q.get('kind', kind), q.get('q')
    cand = [m for m in ms if (not kind or m['kind'] == kind)]
    for m in cand:
        if q and m['key'] == q: return m
    if q:
        words = [w.lower() for w in re.split(r'\W+', q) if w]
        hits = [m for m in cand if all(w in (m['title'] + ' ' + (m.get('short') or '')).lower() for w in words)]
        hits.sort(key=lambda m: (not m['ok'], m.get('start') or ''))
        if hits: return hits[0]
    return cand[0] if (cand and not q) else None


def outcome(m, label):
    lab = label.lower()
    return next((r for r in m['outcomes'] if r['label'].lower() == lab), None) or next((r for r in m['outcomes'] if lab in r['label'].lower()), None)


# ------------------------------------------------------------------ recipes: batch entry -> post
def cook(ms, e, st=None):
    a = e.get('args', {}); r = e['recipe']
    if r == 'matchday':
        p = fm.matchday(ms, a.get('comp', 'UEFA Champions League'), day=a.get('day'), title=a.get('title'))
    elif r == 'pick':
        p = fm.pick(find(ms, a['match'], 'match3') or find(ms, a['match'], 'game2'), facts=e.get('facts'))
    elif r == 'swing':
        m = find(ms, a['market'])
        p = fm.swing(m, a['names'], days=a.get('days', 9), title=a.get('title'), sub=a.get('sub'))
    elif r == 'quiz':
        items = []
        for it in a['items']:
            m = find(ms, it['market']); o = outcome(m, it['outcome'])
            items.append({'q': it['q'], 'p': o['p'], 'context': it.get('context', ''),
                          'team': fm.team(it['team']) if it.get('team') else None, 'team2': fm.team(it['team2']) if it.get('team2') else None})
        p = fm.quiz(items, part=a.get('part', 1))
    elif r == 'breaking':
        m = find(ms, a['market']); o = outcome(m, a['outcome'])
        head = a['headline'].replace('{p}', '%d%%' % round(100 * o['p'])).replace('{a}', fm.a_an(100 * o['p']))
        p = fm.breaking(m, o['label'], head, note=a.get('note', ''), kicker=a.get('kicker', 'Market update'))
    elif r == 'tier':
        p = fm.tier(find(ms, a['market']), title=a.get('title'), sub=a.get('sub'))
    elif r == 'ladder_touch':
        p = fm.ladder_touch(ms, a.get('asset', 'BTC'))
    elif r == 'ladder_ipo':
        p = fm.ladder_ipo(ms, a.get('company', 'Anthropic'))
    elif r == 'pricetags':
        p = fm.pricetags(find(ms, a['market']), title=a.get('title'), sub=a.get('sub'), n=a.get('n', 8))
    elif r == 'number':
        m = find(ms, a['market']); o = outcome(m, a['outcome'])
        p = fm.number(o['p'], a['line'], sub=a.get('sub', ''), kicker=a.get('kicker', 'The number'))
    elif r == 'ranking':
        p = fm.ranking(find(ms, a['market']), title=a.get('title'), sub=a.get('sub'), n=a.get('n', 6))
    elif r == 'cheapest':
        p = fm.cheapest(fm.pick_cheapest(ms, n=a.get('n', 6)), title=a.get('title'), sub=a.get('sub'))
    elif r == 'top3':
        import traders
        p = traders.top3(ms, a.get('window', '24h'), capture=a.get('capture', True), st=st)
    elif r == 'howto':
        import howto
        if a.get('recapture', True): howto.capture(a.get('path', '/markets/sports/q%s' % str(a.get('market', 'Q422')).lstrip('Q')))
        p = howto.build(ms, a.get('market', 'Q422'))
    elif r == 'pnl':
        import traders
        spec, info = traders.pnl_card(a['username'], a.get('coin'), a.get('hours', 720), ms)
        spec['theme'] = a.get('theme', 'light')
        cap = ("%s called it: %s on %s %s\n\nBought %s shares at %.0f cents, paid out $%s. Profit $%s.\n\n"
               "Real trade from Outcome's public data. Past results do not predict future results. %s"
               % (a['username'], info['label'], info['title'], '\U0001F4C8', '{:,.0f}'.format(info['bought']), 100 * (info['avg'] or 0),
                  '{:,.0f}'.format(info['payout'] + info['proceeds']), '{:,.0f}'.format(info['profit']), fm.risk_line()))
        p = fm._post('pnl_%s' % a['username'], 'pnl', 'P&L card', [spec], cap, video=None, notes='Transparent card for the edit; needs the client OK on the username.')
        p['transparent'] = True
    elif r in ('replay', 'upset', 'comeback'):
        import postmatch
        p = getattr(postmatch, r)(ms, **a)
    elif r in MOTION_RECIPES:                   # video formats (motion.py): each renders with its own look and baked-in sound
        p = getattr(mo, r)(ms, **a)
    elif hasattr(fm, r):                        # newer recipes defined in formats.py take (ms, **args)
        p = getattr(fm, r)(ms, **a)
    else:
        raise ValueError('unknown recipe %s' % r)
    if not p: return None
    p['id'] = e.get('id') or p['id']
    for k in ('caption', 'when', 'notes'):
        if e.get(k): p[k] = e[k]
    if e.get('slides'):                         # per-slide overrides: {"0": {"title": "..."}}
        for i, ov in e['slides'].items(): p['slides'][int(i)].update(ov)
    if e.get('video') is False: p['video'] = None
    if e.get('video_over'): p['video'] = dict(p['video'] or {}, **e['video_over'])
    return p


# ------------------------------------------------------------------ build
def version_dir(d):
    if not os.path.exists(d): return d
    k = 2
    while os.path.exists('%s_v%d' % (d, k)): k += 1
    return '%s_v%d' % (d, k)


def build(batch_path, only=None, no_video=False):
    b = json.load(open(batch_path, encoding='utf-8'))
    date = b.get('date') or today(); brand = fm.brand()
    page = (b.get('page') or brand.get('handle') or '@page').lstrip('@')
    ms = od.markets()
    out = os.path.join(ROOT, 'out', date); fin = os.path.join(ROOT, 'FINALS', date, '@' + page)
    os.makedirs(out, exist_ok=True); os.makedirs(fin, exist_ok=True)
    caps = []; t0 = time.time(); n_img = n_vid = 0
    with Studio(brand) as st:
        for i, e in enumerate(b['posts']):
            if only and e.get('id') not in only: continue
            try:
                p = cook(ms, e, st)
            except Exception as ex:
                print('SKIP %s: %s' % (e.get('id'), ex)); continue
            if not p: print('SKIP %s: no data' % e.get('id')); continue
            pd_ = os.path.join(out, p['id']); os.makedirs(pd_, exist_ok=True)
            json.dump(p, open(os.path.join(pd_, 'post.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
            dst = version_dir(os.path.join(fin, '%02d_%s' % (i + 1, p['id'])))
            os.makedirs(dst, exist_ok=True)
            ext = '.png' if p.get('transparent') else '.jpg'
            for k, s in enumerate(p['slides']):
                for tag, size in (('ig', IG), ('tt', TT)):
                    f = os.path.join(pd_, '%s_%02d%s' % (tag, k + 1, ext)); st.still(s, f, size, transparent=bool(p.get('transparent'))); n_img += 1
                    shutil.copy(f, os.path.join(dst, '%s_%d%s' % (tag, k + 1, ext)))
            if p.get('video') and not no_video and e.get('video', True):
                f = os.path.join(pd_, 'video.mp4')
                if p['video'].get('fmt') in MOTION_FMTS:
                    mo.render(st, p['video'], f, TT)                    # sound from the timeline cue sheet
                    if not p['slides']:                                 # video-only post: frame 0 as the cover
                        c = os.path.join(pd_, 'cover.jpg'); st.still(p['video'], c, TT, t=p['video'].get('lead', .5)); shutil.copy(c, os.path.join(dst, 'cover.jpg'))
                else:
                    info = st.show(p['video'], TT) or {}
                    st.video(p['video'], f, TT, dur=(info.get('dur') or 4) + HOLD)
                n_vid += 1
                shutil.copy(f, os.path.join(dst, 'video.mp4'))
            cap = p['caption']
            if brand.get('disclosure') and not cap.startswith(brand['disclosure']): cap = brand['disclosure'] + ' ' + cap
            open(os.path.join(dst, 'caption.txt'), 'w', encoding='utf-8').write(cap)
            caps.append('[%02d] %s  (%s)%s\n%s\n' % (i + 1, p['id'], os.path.basename(dst), ('  [post ' + e['when'] + ']') if e.get('when') else '', cap))
            print('built %-28s %d slides%s' % (p['id'], len(p['slides']), ' + video' if p.get('video') and not no_video and e.get('video', True) else ''))
    cp = os.path.join(fin, 'captions.txt')
    mode = 'a' if os.path.exists(cp) and only else 'w'
    open(cp, mode, encoding='utf-8').write('\n'.join(caps))
    print('done: %d images, %d videos in %.0fs -> %s' % (n_img, n_vid, time.time() - t0, fin))
    return fin


def sheet(date, cell=270, cols=8):
    from PIL import Image, ImageDraw
    fin = glob.glob(os.path.join(ROOT, 'FINALS', date, '@*'))
    paths = []
    for f in fin:
        for d in sorted(glob.glob(os.path.join(f, '[0-9][0-9]_*'))):
            paths += sorted(glob.glob(os.path.join(d, 'ig_*.jpg')))[:-1] or sorted(glob.glob(os.path.join(d, 'ig_*.jpg')))
    ims = [Image.open(p).convert('RGB') for p in paths]
    if not ims: print('nothing to sheet'); return
    hs = [int(im.height * cell / im.width) for im in ims]; rows = (len(ims) + cols - 1) // cols; rh = max(hs) + 24
    sh = Image.new('RGB', (cols * (cell + 6), rows * rh), (25, 25, 25)); d = ImageDraw.Draw(sh)
    for i, (im, h) in enumerate(zip(ims, hs)):
        x, y = (i % cols) * (cell + 6), (i // cols) * rh
        sh.paste(im.resize((cell, h)), (x, y + 22)); d.text((x + 3, y + 5), os.path.basename(os.path.dirname(paths[i]))[:34] + '/' + os.path.basename(paths[i]), fill=(255, 255, 0))
    out = os.path.join(ROOT, 'out', date, '_sheet.jpg'); os.makedirs(os.path.dirname(out), exist_ok=True)
    sh.save(out, quality=86); print(out); return out


# ------------------------------------------------------------------ scan (what is worth posting today)
def scan():
    ms = od.markets(); now = dt.datetime.now(dt.timezone.utc)
    L = ['# Outcome scan %s' % now.strftime('%Y-%m-%d %H:%M UTC'), '']
    up = [m for m in ms if m['kind'] in ('match3', 'game2') and m['ok'] and od.when(m['start']) and now - dt.timedelta(hours=2) <= od.when(m['start']) <= now + dt.timedelta(hours=48)]
    up.sort(key=lambda m: m['start'])
    L.append('## Matches in the next 48 h (%d)' % len(up))
    for m in up:
        L.append('- %s %s  %s  %s' % (m['start'][4:8] + ' ' + m['start'][9:], m.get('comp', '')[:22], m['short'],
                                      ' / '.join('%s %d%%' % (r.get('short') or r['label'], round(100 * r['p'])) for r in m['outcomes'])))
    L += ['', '## Season and macro markets']
    for m in ms:
        if m['kind'] in ('winner', 'fed', 'ipo_cap', 'ipo_confirm') and m['ok']:
            L.append('- [%s] %s: %s' % (m['key'], m.get('short') or m['title'], ', '.join('%s %d%%' % (r['label'], round(100 * r['p'])) for r in m['outcomes'][:6])))
    # 24 h movers on season / macro markets (hourly candles)
    L += ['', '## Biggest 24 h moves (season, award, macro)']
    movers = []
    for m in ms:
        if m['kind'] not in ('winner', 'fed', 'ipo_cap', 'ipo_confirm', 'touch') or not m['ok']: continue
        for r in m['outcomes'][:6]:
            try:
                first, _ = fm.change_24h(r['coin'])
            except Exception:
                continue
            if first is not None and r['p'] is not None: movers.append((r['p'] - first, m, r))
            time.sleep(.15)
    movers.sort(key=lambda x: -abs(x[0]))
    for dlt, m, r in movers[:12]:
        L.append('- %+.0f pts  %s: %s now %d%%' % (100 * dlt, m.get('short') or m['title'], r['label'], round(100 * r['p'])))
    try:
        lb = od.leaderboard('24h', limit=5)
        L += ['', '## Top traders, last 24 h'] + ['- %s  %+.0f' % (x.get('username') or x.get('address', '')[:10], float(x.get('pnl') or 0)) for x in lb]
    except Exception as ex:
        L.append('leaderboard failed: %s' % ex)
    out = os.path.join(ROOT, 'out', 'scan'); os.makedirs(out, exist_ok=True)
    f = os.path.join(out, 'scan_%s.md' % now.strftime('%Y%m%d_%H%M')); open(f, 'w', encoding='utf-8').write('\n'.join(L))
    print('\n'.join(L)); print('\n->', f)


# ------------------------------------------------------------------ plan (a starting batch the editor then trims)
def plan(date=None):
    """a starting batch picked from what actually happened: last night's upsets and replays, today's games, real race moves,
    macro moves, plus the engagement formats. Edit it before building (facts for pick posts, captions, drop weak ones)."""
    import postmatch
    date = date or today(); ms = od.markets(); now = dt.datetime.now(dt.timezone.utc)
    d8 = date.replace('-', ''); nxt = (dt.datetime.strptime(d8, '%Y%m%d') + dt.timedelta(days=1)).strftime('%Y%m%d')
    posts, notes = [], []
    # 1. last night: games the archive saw, now finished (ESPN)
    fin = []
    for d in glob.glob(os.path.join(ROOT, 'data', 'archive', 'candles', 'Q*')):
        try:
            a = postmatch.analyse(os.path.basename(d))
        except Exception:
            continue
        if not a or not (a.get('espn') or {}).get('final'): continue
        s = od.when(a['start'])
        if s and now - s < dt.timedelta(hours=40): fin.append(a)
    for a in sorted(fin, key=lambda a: a['winner_pre'] or 1):
        if a.get('upset'): posts.append({'id': 'upset_%s' % a['key'], 'recipe': 'upset', 'args': {'key': a['key']}, 'when': 'morning'})
        elif a.get('comeback'): posts.append({'id': 'comeback_%s' % a['key'], 'recipe': 'comeback', 'args': {'key': a['key']}, 'when': 'morning'})
    if fin:
        def swing_size(a):
            ln = a['lines'].get(a.get('winner')) or []
            return (max(p for _, p in ln) - min(p for _, p in ln)) if ln else 0
        big = max(fin, key=swing_size)
        if not any(p['args'].get('key') == big['key'] for p in posts):
            posts.append({'id': 'replay_%s' % big['key'], 'recipe': 'replay', 'args': {'key': big['key']}, 'when': 'morning'})
        dogp = lambda a: min(a['pre'].get(a['home']) or 0, a['pre'].get(a['away']) or 0)
        dogs = sorted([a for a in fin if max(a['pre'].get(a['home']) or 0, a['pre'].get(a['away']) or 0) >= .55], key=lambda a: -dogp(a))[:3]
        if len(dogs) >= 3:
            posts.append({'id': 'radar_result', 'recipe': 'radar_result', 'args': {'keys': [a['key'] for a in dogs]}, 'when': 'morning'})
    # 2. today's games
    for comp, tag in (('UEFA Champions League', 'ucl'), ('UEFA Europa League', 'uel')):
        for day in (d8, nxt):
            if any(m['kind'] == 'match3' and m.get('comp') == comp and (m.get('start') or '').startswith(day) and m['ok'] for m in ms):
                posts.append({'id': 'matchday_%s_%s' % (tag, day), 'recipe': 'matchday', 'args': {'comp': comp, 'day': day}, 'when': 'morning' if day == d8 else 'evening before'})
                if day == d8 and fm.radar_items(ms, day, comp, 3):
                    posts.append({'id': 'radar_%s_%s' % (tag, day), 'recipe': 'radar', 'args': {'day': day, 'comp': comp, 'n': 3}, 'when': 'afternoon'})
                break
    games = [m for m in ms if m['kind'] == 'match3' and m['ok'] and (m.get('start') or '')[:8] == d8]
    big_names = ('Manchester', 'Real Madrid', 'Barcelona', 'Bayern', 'Arsenal', 'Liverpool', 'Paris', 'Juventus', 'Milan', 'Inter', 'Chelsea', 'Dortmund', 'Atletico', 'Roma')
    for g in sorted(games, key=lambda m: abs(m['outcomes'][0]['p'] - m['outcomes'][2]['p']) - (.25 if any(x in m['title'] for x in big_names) else 0))[:2]:
        posts.append({'id': 'pick_%s' % g['key'], 'recipe': 'pick', 'args': {'match': g['key']}, 'when': 'midday',
                      'facts': {}, '_todo': 'add 2 checked facts per side (form, table, head to head) with source + date, or leave empty'})
    # 3. races that really moved (7 days, 6+ points)
    end = int(time.time() * 1000)
    for m in ms:
        if m['kind'] != 'winner' or not m['ok']: continue
        moves = []
        for r in fm.real_rows(m)[:4]:
            try:
                c = od.candles(r['coin'], '1d', end - 8 * 86400000, end)
            except Exception:
                continue
            if len(c) >= 3 and r['p'] is not None: moves.append((r['p'] - c[0][4], r['label']))
            time.sleep(.2)
        moves.sort(key=lambda x: -abs(x[0]))
        if moves and abs(moves[0][0]) >= .06:
            names = [moves[0][1]] + [x[1] for x in moves[1:2]]
            posts.append({'id': 'swing_%s' % m['key'], 'recipe': 'swing', 'args': {'market': m['key'], 'names': names, 'days': 8}, 'when': 'any'})
            notes.append('%s: %s %+d pts in 7 days' % (m.get('short') or m['title'], moves[0][1], round(100 * moves[0][0])))
    # 4. macro
    fed = next((m for m in ms if m['kind'] == 'fed' and m['ok']), None)
    if fed:
        hike = next((r for r in fed['outcomes'] if r['label'] == 'Hike'), None)
        if hike:
            posts.append({'id': 'fed_%s' % d8, 'recipe': 'breaking', 'args': {'market': fed['key'], 'outcome': 'Hike',
                          'headline': 'Traders give the Fed {a} *{p}* chance of a ^rate hike^ this month', 'note': 'Not financial advice.'}, 'when': 'any'})
    if any(m['kind'] == 'ipo_cap' and m['ok'] for m in ms):
        posts.append({'id': 'ipo_ladder', 'recipe': 'ladder_ipo', 'args': {'company': 'Anthropic'}, 'when': 'any'})
    posts.append({'id': 'btc_ladder', 'recipe': 'ladder_touch', 'args': {'asset': 'BTC'}, 'when': 'optional'})
    # 5. engagement
    items = []
    for q, mk_, oc, tm in (('Arsenal win the Premier League', 'Premier League winner', 'Arsenal', 'Arsenal'),
                           ("Harry Kane wins the Ballon d'Or", "Ballon d'Or", 'Harry Kane', None),
                           ('Barcelona win the Champions League', 'Champions League winner', 'Barcelona', 'Barcelona')):
        if find(ms, mk_): items.append({'q': q, 'market': mk_, 'outcome': oc, 'team': tm})
    if games:
        g = max(games, key=lambda m: max(m['outcomes'][0]['p'], m['outcomes'][2]['p']))
        fav = max((g['outcomes'][0], g['outcomes'][2]), key=lambda r: r['p']); other = g['outcomes'][2] if fav is g['outcomes'][0] else g['outcomes'][0]
        items.append({'q': '%s beat %s tonight' % (fm.team(fav['label'])['short'], fm.team(other['label'])['short']), 'market': g['key'], 'outcome': fav['label'], 'team': fav['label'], 'team2': other['label']})
    if fed: items.append({'q': 'The Fed raises rates this month', 'market': fed['key'], 'outcome': 'Hike'})
    n_quiz = len(glob.glob(os.path.join(ROOT, 'FINALS', '*', '*', '*quiz*'))) + 1
    posts.append({'id': 'quiz_part%d' % n_quiz, 'recipe': 'quiz', 'args': {'part': n_quiz, 'items': items}, 'when': 'evening'})
    posts.append({'id': 'race_%s' % d8, 'recipe': 'barrace', 'args': {'market': ('Premier League winner', "Ballon d'Or", 'Champions League winner')[int(d8) % 3], 'days': 30}, 'when': 'optional, video first'})
    posts.append({'id': 'epl_pricetags', 'recipe': 'pricetags', 'args': {'market': 'Premier League winner', 'sub': 'Premier League 2026/27 winner'}, 'when': 'optional'})
    posts.append({'id': 'cheapest', 'recipe': 'cheapest', 'args': {'n': 6}, 'when': 'optional'})
    posts.append({'id': 'top3_traders', 'recipe': 'top3', 'args': {'window': '24h'}, 'when': 'HOLD until the client OKs usernames'})
    b = {'date': date, 'page': fm.brand().get('handle'), 'made': now.strftime('%Y-%m-%d %H:%M UTC'), 'signals': notes,
         '_how': 'Edit freely: drop weak posts, add facts to pick posts, write captions, set "when". Then: python ocs.py build batches/%s.json' % date,
         'posts': posts}
    f = os.path.join(ROOT, 'batches', '%s.json' % date)
    if os.path.exists(f): f = f.replace('.json', '_plan_%s.json' % now.strftime('%H%M'))
    json.dump(b, open(f, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print(f); print('%d posts; signals: %s' % (len(posts), '; '.join(notes) or 'none')); return f


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit()
    only = None
    if '--only' in a: only = set(a[a.index('--only') + 1].split(','))
    if a[0] == 'scan': scan()
    elif a[0] == 'plan': plan(a[1] if len(a) > 1 and not a[1].startswith('-') else None)
    elif a[0] == 'build': build(a[1], only, '--no-video' in a)
    elif a[0] == 'sheet': sheet(a[1] if len(a) > 1 else today())
    else: print(__doc__)
