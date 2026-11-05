"""goalcam: film the REAL outcome.xyz match page during a live game and keep only the moments that matter
(a goal on ESPN's scoreboard, or a big jump in the price), as screen-recording footage with no broadcast rights issue.

python goalcam.py run Q405 Q407 Q412 ...     one headless Chrome per match: waits for kick-off (minus 2 min), films at about 4 fps
                                            into a rolling 4-minute buffer, keeps [-150 s, +60 s] around every event, stops after
                                            full time (or when the market settles). Leave it running; it keeps the PC awake.
python goalcam.py cut Q412                  every kept event -> footage/goalcam_<key>_<n>.mp4 (30 fps, real time) + events.json
python goalcam.py test Q422 40              film any match page for 40 s, fake an event at 20 s, cut it (checks the whole chain)
Events: ESPN score change (polled every 20 s) or a move of 8+ points in the home/away price within 60 s (polled every 10 s).
"""
import base64, ctypes, datetime as dt, glob, json, os, shutil, subprocess, sys, threading, time
from statistics import median
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ocdata as od, formats as fm
from render import Studio, FFMPEG
from capture import Capture

ROOT = od.ROOT
BASE = os.path.join(ROOT, 'out', '_goalcam')
FPS = 4.0
KEEP_BEFORE, KEEP_AFTER, RING = 150, 60, 240
ESPN = 'https://site.api.espn.com/apis/site/v2/sports/soccer/%s/scoreboard?dates=%s'
LEAGUES = {'UEFA Champions League': 'uefa.champions', 'UEFA Europa League': 'uefa.europa', 'English Premier League': 'eng.1'}


def log(key, msg):
    line = '%s %s %s' % (time.strftime('%H:%M:%S'), key, msg)
    print(line, flush=True)
    open(os.path.join(BASE, 'goalcam.log'), 'a', encoding='utf-8').write(line + '\n')


def espn_event(m):
    """the ESPN event for this market (by both team names), or None"""
    import facts
    lg = next((v for k, v in LEAGUES.items() if k in (m.get('comp') or '')), None)
    if not lg: return None, None
    day = od.when(m['start']).strftime('%Y%m%d')
    try:
        sb = facts.get(ESPN % (lg, day))
    except Exception:
        return lg, None
    # each side matches on its short name or its full label (PSG vs "Paris Saint-Germain", Man City vs "Manchester City")
    keys = []
    for i in (0, -1):
        lab = m['outcomes'][i]['label']
        keys.append({facts.plain(x).replace('-', ' ').split()[0] for x in (fm.team(lab)['short'], lab) if x and facts.plain(x).split()})
    for ev in sb.get('events', []):
        nm = facts.plain(ev.get('name', '')).replace('-', ' ')
        if any(k in nm for k in keys[0]) and any(k in nm for k in keys[1]): return lg, ev['id']
    return lg, None


def espn_state(lg, eid, day):
    import facts
    sb = facts.get(ESPN % (lg, day))
    ev = next((e for e in sb.get('events', []) if e['id'] == eid), None)
    if not ev: return None
    c = ev['competitions'][0]; st = c.get('status') or ev.get('status') or {}
    sc = {x.get('homeAway'): x.get('score') for x in c.get('competitors', [])}
    return {'score': '%s-%s' % (sc.get('home'), sc.get('away')), 'clock': st.get('displayClock'), 'state': (st.get('type') or {}).get('state'),
            'detail': (st.get('type') or {}).get('shortDetail')}


def prices(m):
    mids = od.load_mids()
    return [od._p(mids, r['coin']) for r in m['outcomes']]


class Cam:
    def __init__(self, key, ms):
        self.key = key; self.m = next(x for x in ms if x['key'] == key)
        self.dir = os.path.join(BASE, key); self.ring = os.path.join(self.dir, 'ring'); self.keep = os.path.join(self.dir, 'keep')
        for d in (self.ring, self.keep): os.makedirs(d, exist_ok=True)
        self.events = []; self.marks = []; self.stop = False
        self.lg, self.eid = espn_event(self.m)
        self.day = od.when(self.m['start']).strftime('%Y%m%d')

    def url(self):
        return 'https://outcome.xyz/markets/sports/q%s' % self.key.lstrip('Q')

    def mark(self, t, kind, info):
        self.events.append(dict(info, t=t, kind=kind)); self.marks.append((t - KEEP_BEFORE, t + KEEP_AFTER))
        json.dump({'key': self.key, 'title': self.m['title'], 'labels': [r['label'] for r in self.m['outcomes']], 'events': self.events}, open(os.path.join(self.dir, 'events.json'), 'w'), indent=1)
        log(self.key, 'EVENT %s %s' % (kind, info))

    def kept(self, t):
        return any(a <= t <= b for a, b in self.marks)

    def watch(self, until):
        last_s = None; hist = []
        t_espn = t_px = 0
        while not self.stop and time.time() < until:
            now = time.time()
            if now - t_px >= 10:
                t_px = now
                try:
                    p = prices(self.m); hist.append((now, p)); hist[:] = [h for h in hist if now - h[0] <= 130]
                    open(os.path.join(self.dir, 'prices.jsonl'), 'a').write(json.dumps({'t': now, 'p': p}) + '\n')
                    # a move must HOLD: median of the last 30 s against the median 60 to 120 s ago (one-poll spikes in a thin book are noise)
                    for i in (0, len(p) - 1):
                        new_ = [h[1][i] for h in hist if now - h[0] <= 30 and h[1][i] is not None]
                        old_ = [h[1][i] for h in hist if 60 <= now - h[0] <= 120 and h[1][i] is not None]
                        if len(new_) >= 3 and len(old_) >= 3 and abs(median(new_) - median(old_)) >= .08 and not any(abs(now - e['t']) < 90 for e in self.events):
                            self.mark(now - 30, 'price', {'from': [median([h[1][k] for h in hist if 60 <= now - h[0] <= 120 and h[1][k] is not None] or [0]) for k in range(len(p))],
                                                          'to': [median([h[1][k] for h in hist if now - h[0] <= 30 and h[1][k] is not None] or [0]) for k in range(len(p))]}); break
                    if p[0] is not None and (p[0] > .995 or p[0] < .005) and (p[-1] is not None and (p[-1] > .995 or p[-1] < .005)):
                        log(self.key, 'market looks settled'); self.stop = True
                except Exception as ex:
                    log(self.key, 'price poll error %s' % ex)
            if self.eid and now - t_espn >= 20:
                t_espn = now
                try:
                    s = espn_state(self.lg, self.eid, self.day)
                    if s:
                        if last_s and s['score'] != last_s['score']: self.mark(now, 'score', {'score': s['score'], 'was': last_s['score'], 'clock': s['clock']})
                        if s['state'] == 'post' and not getattr(self, 'ended', None):
                            self.ended = now; log(self.key, 'full time %s' % s['score'])
                        last_s = s
                except Exception as ex:
                    log(self.key, 'espn poll error %s' % ex)
            if getattr(self, 'ended', None) and now - self.ended > 180: self.stop = True
            time.sleep(1)

    def _open(self, c):
        """load the match page; False when it did not load (network down): the caller retries, nothing here may kill the camera"""
        try:
            c.open(self.url(), w=390, h=844, scale=1080 / 390, wait=5)
            try: c.clean()
            except Exception: pass
            c.hide()
            return bool(c.st.js("!!document.body && location.hostname.indexOf('outcome') >= 0 && document.body.innerText.length > 200"))
        except Exception as ex:
            log(self.key, 'page load failed (%s), retrying' % str(ex)[:80]); return False

    def film(self, until):
        with Studio(fm.brand()) as st:
            c = Capture(st); ok = self._open(c)
            log(self.key, 'filming %s%s' % (self.url(), '' if ok else ' (page not loaded yet)'))
            i = 0; last_prune = time.time(); last_try = time.time()
            while not self.stop and time.time() < until:
                t = time.time()
                if not ok:                                          # keep retrying the page every 15 s until it loads
                    if t - last_try > 15: last_try = t; ok = self._open(c)
                    if not ok: time.sleep(1); continue
                    log(self.key, 'page loaded, filming')
                if i % 20 == 0:
                    try:
                        c.hide()
                        if i % 240 == 0 and not st.js("!!document.body && document.body.innerText.length > 200"): ok = False; continue
                    except Exception:
                        ok = False; continue
                try:
                    data = base64.b64decode(st.call('Page.captureScreenshot', format='jpeg', quality=72, fromSurface=True)['data'])
                    open(os.path.join(self.ring, '%.3f.jpg' % t), 'wb').write(data)
                except Exception as ex:
                    log(self.key, 'shot error %s' % str(ex)[:80]); time.sleep(2); ok = False
                i += 1
                if time.time() - last_prune > 20:
                    last_prune = time.time()
                    try: self.prune()
                    except Exception as ex: log(self.key, 'prune error %s' % ex)
                time.sleep(max(0, 1 / FPS - (time.time() - t)))
            self.prune(final=True)
        log(self.key, 'stopped, %d events' % len(self.events))

    def prune(self, final=False):
        now = time.time()
        for f in glob.glob(os.path.join(self.ring, '*.jpg')):
            t = float(os.path.basename(f)[:-4])
            if self.kept(t): shutil.move(f, os.path.join(self.keep, os.path.basename(f)))
            elif final or now - t > RING: os.remove(f)

    def run(self, start_at, max_s=150 * 60):
        wait = start_at - time.time()
        if wait > 0: log(self.key, 'waiting %.0f min for kick-off' % (wait / 60)); time.sleep(wait)
        until = time.time() + max_s
        th = threading.Thread(target=self.watch, args=(until,), daemon=True); th.start()
        while not self.stop and time.time() < until:               # a crashed camera restarts instead of dying silently
            try:
                self.film(until)
            except Exception as ex:
                log(self.key, 'camera crashed (%s), restarting in 5 s' % str(ex)[:100]); time.sleep(5)
        self.stop = True


def jump_time(d, e):
    """when the price really moved: the first poll in the event window that is past half of the window's biggest move (10 s resolution)"""
    f = os.path.join(d, 'prices.jsonl')
    if not os.path.exists(f): return None, None, None
    rows = [json.loads(l) for l in open(f) if l.strip()]
    rows = [r for r in rows if e['t'] - KEEP_BEFORE <= r['t'] <= e['t'] + KEEP_AFTER and r['p'] and r['p'][0] is not None]
    if len(rows) < 3: return None, None, None
    p0 = rows[0]['p'][0]; far = max(rows, key=lambda r: abs(r['p'][0] - p0))
    if abs(far['p'][0] - p0) < .04: return None, None, None
    tj = next(r['t'] for r in rows if abs(r['p'][0] - p0) >= abs(far['p'][0] - p0) / 2) - 5
    pb = [r['p'] for r in rows if r['t'] <= tj - 5][-1:] or [rows[0]['p']]
    pa = [r['p'] for r in rows if r['t'] >= tj + 35][:1] or [rows[-1]['p']]
    return tj, pb[0], pa[0]


def cut(key):
    d = os.path.join(BASE, key); ev = json.load(open(os.path.join(d, 'events.json'), encoding='utf-8'))
    frames = sorted(glob.glob(os.path.join(d, 'keep', '*.jpg')), key=lambda f: float(os.path.basename(f)[:-4]))
    outs = []
    pf = os.path.join(d, 'prices.jsonl')
    polls = [json.loads(l) for l in open(pf) if l.strip()] if os.path.exists(pf) else []
    for n, e in enumerate(ev['events']):
        if e.get('kind') == 'price' and polls:                       # keep a price event only if the move held (one-poll flickers are thin-book noise)
            def med(a, b, i):
                v = [r['p'][i] for r in polls if a <= r['t'] - e['t'] <= b and r['p'][i] is not None]
                return median(v) if len(v) >= 3 else None
            held = any(med(-120, -40, i) is not None and med(20, 60, i) is not None and abs(med(20, 60, i) - med(-120, -40, i)) >= .06 for i in (0, -1))
            if not held:
                print('skip %s event %d: the move did not hold' % (key, n + 1)); continue
        sel = [f for f in frames if e['t'] - KEEP_BEFORE <= float(os.path.basename(f)[:-4]) <= e['t'] + KEEP_AFTER]
        if len(sel) < 10: continue
        ts = [float(os.path.basename(f)[:-4]) for f in sel]
        lst = os.path.join(d, 'list_%d.txt' % n)
        with open(lst, 'w') as fh:
            for k, f in enumerate(sel):
                fh.write("file '%s'\nduration %.4f\n" % (f.replace('\\', '/'), (ts[k + 1] - ts[k]) if k + 1 < len(sel) else 1 / FPS))
            fh.write("file '%s'\n" % sel[-1].replace('\\', '/'))
        out = os.path.join(ROOT, 'footage', 'goalcam_%s_%d.mp4' % (key, n + 1))
        subprocess.run([FFMPEG, '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-vf', 'fps=30,scale=1080:-2:flags=lanczos,format=yuv420p',
                        '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', out], check=True)
        jump, pb, pa = jump_time(d, e)
        e2 = dict(e, clip=out, clip_start=ts[0], event_in_clip_s=e['t'] - ts[0], jump_in_clip_s=(jump - ts[0]) if jump else None, p_before=pb, p_after=pa)
        json.dump(e2, open(out.replace('.mp4', '.json'), 'w'), indent=1); outs.append(out)
        print(out, e['kind'], e.get('score') or '', 'event at %.1f s' % e2['event_in_clip_s'])
    return outs


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    os.makedirs(BASE, exist_ok=True)
    if a[0] == 'run':
        try: ctypes.windll.kernel32.SetThreadExecutionState(0x80000001)     # no idle sleep while filming (Windows)
        except AttributeError: pass                                       # Mac: start it under `caffeinate -i` instead
        ms = od.markets(); cams = []
        for key in a[1:]:
            cam = Cam(key, ms); ko = od.when(cam.m['start']).timestamp()
            log(key, '%s, kick-off %s UTC, ESPN event %s' % (cam.m['title'], od.when(cam.m['start']).strftime('%H:%M'), cam.eid))
            th = threading.Thread(target=cam.run, args=(ko - 120,)); th.start(); cams.append(th); time.sleep(3)
        for th in cams: th.join()
        for key in a[1:]:
            try: cut(key)
            except Exception as ex: log(key, 'cut error %s' % ex)
    elif a[0] == 'cut':
        for key in a[1:]: cut(key)
    elif a[0] == 'test':
        ms = od.markets(); key = a[1]; secs = float(a[2]) if len(a) > 2 else 40
        cam = Cam(key, ms)
        threading.Timer(secs / 2, lambda: cam.mark(time.time(), 'test', {'note': 'fake event'})).start()
        cam.film(time.time() + secs); print(cut(key))
