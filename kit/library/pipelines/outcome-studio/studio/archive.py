"""archive: save Outcome prices while markets are live (Hyperliquid deletes a market's history the moment it settles).

python archive.py            run forever (every 5 minutes); stop with Ctrl+C or by killing the process
python archive.py --once     one cycle (for a test)

Writes under data/archive/:
  mids/YYYYMMDD.jsonl         every 5 min: {"t": ms, "m": {coin: mid}} for all outcome coins + BTC/ETH/SOL/HYPE perps
  meta/YYYYMMDD-HHMM.json     the market list whenever it changes (maps coins to questions later)
  candles/<key>/<coin>.json   1-minute candles of every match that is live or just finished (the chart-replay source)
  scores/<league>_<date>.json ESPN scoreboard (goal minutes, cards) for football days with Outcome markets
  series/<category>.json      15-minute and daily up/down results, merged (Outcome keeps only the last 50)
  archive.log                 one line per cycle
"""
import json, os, sys, time, hashlib, traceback, datetime as dt, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ocdata as od

A = os.path.join(od.ROOT, 'data', 'archive')
PERPS = ('BTC', 'ETH', 'SOL', 'HYPE')
SERIES = ('out-btc-15m', 'out-eth-15m', 'out-hype-15m')
ESPN = {'UEFA Champions League': 'uefa.champions', 'UEFA Europa League': 'uefa.europa', 'English Premier League': 'eng.1'}
WINDOW = {'match3': (90, 150), 'game2': (90, 260)}       # minutes before kickoff / after kickoff to record 1m candles
state = {'meta_hash': None, 'series_at': 0, 'meta': None, 'meta_at': 0}


def log(msg):
    os.makedirs(A, exist_ok=True)
    line = '%s %s' % (dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), msg)
    open(os.path.join(A, 'archive.log'), 'a', encoding='utf-8').write(line + '\n'); print(line, flush=True)


def save_json(p, obj):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    tmp = p + '.tmp'; json.dump(obj, open(tmp, 'w', encoding='utf-8')); os.replace(tmp, p)


def cycle():
    now = dt.datetime.now(dt.timezone.utc); t = int(time.time() * 1000)
    mids = od.load_mids()
    keep = {k: v for k, v in mids.items() if k.startswith('#') or k in PERPS}
    p = os.path.join(A, 'mids', now.strftime('%Y%m%d') + '.jsonl'); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'a', encoding='utf-8').write(json.dumps({'t': t, 'm': keep}, separators=(',', ':')) + '\n')
    if state['meta'] is None or time.time() - state['meta_at'] > 1800:
        state['meta'] = od.load_meta(); state['meta_at'] = time.time()
        h = hashlib.md5(json.dumps(state['meta'], sort_keys=True).encode()).hexdigest()
        if h != state['meta_hash']:
            save_json(os.path.join(A, 'meta', now.strftime('%Y%m%d-%H%M') + '.json'), state['meta']); state['meta_hash'] = h
    ms = od.markets(state['meta'], mids, now)
    live, n_c = [], 0
    for m in ms:
        if m['kind'] not in WINDOW or not m.get('start'): continue
        s = od.when(m['start']); pre, post = WINDOW[m['kind']]
        if not s or not (s - dt.timedelta(minutes=pre) <= now <= s + dt.timedelta(minutes=post)): continue
        live.append(m['short'])
        start_ms = int((s - dt.timedelta(minutes=pre)).timestamp() * 1000)
        for r in m['outcomes']:
            try:
                rows = od.candles(r['coin'], '1m', start_ms, t)
            except Exception:
                continue
            f = os.path.join(A, 'candles', m['key'], r['coin'].lstrip('#') + '.json')
            old = json.load(open(f)) if os.path.exists(f) else {'rows': []}
            if len(rows) >= len(old.get('rows', [])):          # never overwrite with a shorter history (settled = empty)
                save_json(f, {'key': m['key'], 'title': m['title'], 'comp': m.get('comp'), 'start': m['start'],
                              'label': r['label'], 'coin': r['coin'], 'interval': '1m', 'saved': t, 'rows': rows})
                n_c += 1
            time.sleep(0.25)
    # football scores for days with live matches (goal minutes for replays)
    leagues = {ESPN[m['comp']] for m in ms if m['kind'] == 'match3' and m['short'] in live and m.get('comp') in ESPN}
    for lg in leagues:
        try:
            day = now.strftime('%Y%m%d')
            url = 'https://site.api.espn.com/apis/site/v2/sports/soccer/%s/scoreboard?dates=%s' % (lg, day)
            sb = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': od.UA}), timeout=30))
            save_json(os.path.join(A, 'scores', '%s_%s.json' % (lg, day)), sb)
        except Exception as e:
            log('espn %s failed: %s' % (lg, e))
    if any(m['kind'] == 'game2' and m['short'] in live for m in ms):
        try:
            url = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard'
            sb = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': od.UA}), timeout=30))
            save_json(os.path.join(A, 'scores', 'nfl_%s.json' % now.strftime('%Y%m%d')), sb)
        except Exception as e:
            log('espn nfl failed: %s' % e)
    # recurring 15-minute series: Outcome keeps 50 results (12.5 h), so merge every 3 hours
    if time.time() - state['series_at'] > 3 * 3600:
        for cat in SERIES:
            try:
                d = od.o1('/markets/series?category=%s&past=50' % cat)
                f = os.path.join(A, 'series', cat + '.json')
                old = json.load(open(f)) if os.path.exists(f) else {}
                items = d.get('data') if isinstance(d, dict) and 'data' in d else d
                old.setdefault('raw', []).append({'t': t, 'data': items})
                old['raw'] = old['raw'][-60:]
                save_json(f, old)
            except Exception as e:
                log('series %s failed: %s' % (cat, e))
        state['series_at'] = time.time()
    log('ok: %d prices, live: %s, candle files: %d' % (len(keep), ', '.join(live) or 'none', n_c))


def keep_awake():
    """ask Windows not to idle-sleep while the archive runs (released automatically when this process ends;
    a closed lid or a manual Sleep still sleeps). No setting is changed."""
    try:
        import ctypes
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)   # ES_CONTINUOUS | ES_SYSTEM_REQUIRED
        return True
    except Exception:
        return False


if __name__ == '__main__':
    once = '--once' in sys.argv
    if not once and '--allow-sleep' not in sys.argv:
        log('keep-awake while archiving: %s' % keep_awake())
    while True:
        try:
            cycle()
        except Exception as e:
            log('cycle failed: %s' % traceback.format_exc().splitlines()[-1])
        if once: break
        time.sleep(300 - (time.time() % 300) + 2)                 # on the 5-minute marks
