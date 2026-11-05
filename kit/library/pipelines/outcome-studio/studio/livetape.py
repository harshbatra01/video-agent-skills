"""livetape: film the REAL outcome.xyz app live (screen-recording style footage, no rights issues).

python livetape.py btc15 [seconds_before_end=90] [seconds_after_end=20]
    waits for the next BTC 15-minute window, films its last minute and a half at phone size, plus the result,
    and writes footage/btc15m_<HHMM>.mp4 (1080 wide, 30 fps) + footage/btc15m_<HHMM>.json (target, prices, result)
python livetape.py url <url> <seconds> [name]       film any outcome.xyz page for N seconds
Frames are captured as fast as Chrome paints (about 10 to 15 a second) and retimed to a steady 30 fps.
"""
import base64, datetime as dt, json, os, re, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ocdata as od, formats as fm
from render import Studio, FFMPEG
from capture import Capture

ROOT = od.ROOT
OUT = os.path.join(ROOT, 'footage')


def film(st, seconds, frames_dir, until=None, keep_clean=None):
    os.makedirs(frames_dir, exist_ok=True)
    for f in os.listdir(frames_dir): os.remove(os.path.join(frames_dir, f))
    stamps = []; t0 = time.time(); i = 0
    while (time.time() - t0) < seconds and (until is None or time.time() < until):
        if keep_clean and i % 15 == 0: keep_clean()
        data = base64.b64decode(st.call('Page.captureScreenshot', format='jpeg', quality=85, fromSurface=True)['data'])
        i += 1; open(os.path.join(frames_dir, '%05d.jpg' % i), 'wb').write(data); stamps.append(time.time())
    return stamps


def assemble(frames_dir, stamps, out):
    """variable-rate captures -> steady 30 fps mp4 (each frame shown for its real duration)"""
    lst = os.path.join(frames_dir, 'list.txt')
    with open(lst, 'w') as f:
        for k in range(len(stamps)):
            d = (stamps[k + 1] - stamps[k]) if k + 1 < len(stamps) else 1 / 15
            f.write("file '%05d.jpg'\nduration %.4f\n" % (k + 1, d))
        f.write("file '%05d.jpg'\n" % len(stamps))
    subprocess.run([FFMPEG, '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-vf', 'fps=30,scale=1080:-2:flags=lanczos,format=yuv420p',
                    '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', out], check=True)
    return out


def btc_window():
    """current BTC 15-minute window: (end time UTC, target price) from the live page title"""
    now = dt.datetime.now(dt.timezone.utc)
    end = now.replace(second=0, microsecond=0) + dt.timedelta(minutes=15 - now.minute % 15)
    return end


def btc15(before=90, after=20):
    end = btc_window()
    start_at = end.timestamp() - before
    wait = start_at - time.time()
    if wait < 5:                                           # too late for this window: take the next one
        end = end + dt.timedelta(minutes=15); start_at = end.timestamp() - before; wait = start_at - time.time()
    name = 'btc15m_%s' % end.strftime('%H%M')
    print('filming window ending %s UTC, starts in %.0f s' % (end.strftime('%H:%M'), wait), flush=True)
    with Studio(fm.brand()) as st:
        c = Capture(st)
        time.sleep(max(0, wait - 25))
        c.open('https://outcome.xyz/markets/crypto/out-btc-15m', w=390, h=844, scale=1080 / 390, wait=4)
        c.clean(); c.hide()
        title = st.js('document.title') or ''
        tgt = re.search(r'above ([0-9,]+)', title)
        time.sleep(max(0, start_at - time.time()))
        frames = os.path.join(ROOT, 'out', '_tape', name)
        stamps = film(st, before + after, frames, until=end.timestamp() + after, keep_clean=c.hide)
        after_text = (st.js('document.body.innerText') or '')[:600]
    mp4 = assemble(frames, stamps, os.path.join(OUT, name + '.mp4'))
    btc = od.hl({'type': 'candleSnapshot', 'req': {'coin': 'BTC', 'interval': '1m', 'startTime': int((end.timestamp() - 16 * 60) * 1000), 'endTime': int((end.timestamp() + 60) * 1000)}})
    info = {'window_end_utc': end.isoformat(), 'title': title, 'target': float(tgt.group(1).replace(',', '')) if tgt else None,
            'film_start': stamps[0] if stamps else None, 'film_end': stamps[-1] if stamps else None, 'frames': len(stamps),
            'end_in_clip_s': end.timestamp() - (stamps[0] if stamps else start_at), 'btc_1m': [[c['t'], float(c['c'])] for c in btc], 'page_after': after_text}
    if info['target'] and btc:
        last = [c for c in btc if c['t'] < end.timestamp() * 1000]
        if last: info['close_before_end'] = float(last[-1]['c']); info['result'] = 'UP' if info['close_before_end'] > info['target'] else 'DOWN'
    json.dump(info, open(os.path.join(OUT, name + '.json'), 'w'), indent=1)
    print(mp4, info.get('result'), '%d frames' % len(stamps))
    return mp4, info


if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'btc15':
        btc15(*(int(x) for x in a[1:3]))
    elif a and a[0] == 'url':
        with Studio(fm.brand()) as st:
            c = Capture(st); c.open(a[1], w=390, h=844, scale=1080 / 390, wait=4); c.clean(); c.hide()
            name = a[3] if len(a) > 3 else 'tape_%d' % time.time()
            fr = os.path.join(ROOT, 'out', '_tape', name); s = film(st, float(a[2]), fr, keep_clean=c.hide)
        print(assemble(fr, s, os.path.join(OUT, name + '.mp4')))
    else:
        print(__doc__)
