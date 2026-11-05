"""facts: checkable pre-match facts for "pick a side" posts, straight from ESPN's public JSON (form, last meeting, matchday result).

python facts.py <league slug> <YYYYMMDD> "<home words>"    e.g.  python facts.py uefa.champions 20261013 "Atletico"
Prints a ready "facts" block for a batch (2 facts per side, numbers marked with *...* so they colour). Check before posting.
"""
import json, sys, urllib.request
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import ocdata as od

API = 'https://site.api.espn.com/apis/site/v2/sports/soccer/%s/%s'


def get(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': od.UA}), timeout=30))


def plain(t):
    import unicodedata
    return ''.join(c for c in unicodedata.normalize('NFKD', t or '') if not unicodedata.combining(c)).lower()


def event(league, day, words):
    sb = get(API % (league, 'scoreboard?dates=%s' % day))
    for ev in sb.get('events', []):
        if all(plain(w) in plain(ev.get('name', '')) for w in words.split()):
            return ev
    return None


def form_line(f):
    """ESPN form string like 'WWDLW' (oldest first) -> fact text"""
    w, d, l = f.count('W'), f.count('D'), f.count('L')
    if w == len(f): return 'Won all of their last *%d*' % len(f)
    if l == 0: return 'Unbeaten in their last *%d*: *%d* wins, *%d* draws' % (len(f), w, d)
    return 'Last %d: *%d* wins, *%d* draws, *%d* defeats' % (len(f), w, d, l)


def facts(league, day, words):
    """two checkable facts per side from ESPN's last-five-games block: current streak or form, then goals for and against"""
    ev = event(league, day, words)
    if not ev: return None
    s = get(API % (league, 'summary?event=%s' % ev['id']))
    out = {}
    for blk in s.get('lastFiveGames') or []:
        tid = str((blk.get('team') or {}).get('id')); name = (blk.get('team') or {}).get('displayName')
        games = blk.get('events') or []
        res = ''.join((g.get('gameResult') or '?')[:1] for g in games)
        streak = 0
        for r in reversed(res):
            if r == res[-1]: streak += 1
            else: break
        gf = ga = 0
        for g in games:
            try:
                hs, as_ = int(g.get('homeTeamScore')), int(g.get('awayTeamScore'))
            except (TypeError, ValueError):
                continue
            home = str(g.get('homeTeamId')) == tid
            gf += hs if home else as_; ga += as_ if home else hs
        lines = []
        if res and res[-1] == 'W' and streak >= 3: lines.append('Won their last *%d* games' % streak)
        elif res and res[-1] == 'L' and streak >= 2: lines.append('Lost their last *%d* games' % streak)
        elif res: lines.append('*%d* %s in their last *%d* games' % (res.count('W'), 'win' if res.count('W') == 1 else 'wins', len(res)))
        if games: lines.append('*%d* scored, *%d* conceded in those %d' % (gf, ga, len(games)))
        if name: out[name] = {'facts': lines, 'source': 'ESPN, %s' % day, 'results': [(g.get('gameDate', '')[:10], g.get('gameResult'), g.get('score'), g.get('atVs'), g.get('leagueName')) for g in games]}
    return {'event': ev.get('name'), 'facts': out}

if __name__ == '__main__':
    r = facts(*sys.argv[1:4])
    print(json.dumps(r, indent=1, ensure_ascii=False))
