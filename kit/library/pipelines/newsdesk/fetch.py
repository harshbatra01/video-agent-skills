"""fetch: grab assets for posts (all saved under the path you give).

  python fetch.py yt <url|id> <start_s> <dur_s> <out.mp4>    YouTube section, 1080p max, H.264 preferred (yt-dlp + Deno + ffmpeg); dur 0 = whole video
  python fetch.py search "<query>" [n]                        YouTube search (id | title | channel | dur | views | upcoming premiere)
  python fetch.py peak <url|id> [dur_s] [skip_s]             start of the most replayed window (YouTube heatmap), for picking the clip
  python fetch.py loud <video> [dur_s] [skip_s]               start of the loudest window of a local video (when peak gives None)
  python fetch.py thumb <url|id> <out.jpg>                    YouTube max-res thumbnail (falls back to hq)
  python fetch.py frame <video> <sec> <out.jpg>               one frame as a photo (music videos make good artist photos)
  python fetch.py x <status url|id> <out_prefix>              every photo / video in an X post (fxtwitter API, no login)
  python fetch.py url <url> <out>                             any direct file
Instagram needs cookies (gallery-dl with a throwaway account); TikTok is blocked on this connection.
YouTube: every yt-dlp call goes through ytdlp(): one at a time, 6 s apart. A burst of ~15 parallel calls (8 Oct 2026) triggered
"Sign in to confirm you're not a bot" for about 15 minutes. Optional fallback: a throwaway account's cookies in secrets/youtube_cookies.txt.
"""
import json, os, re, sys, glob, shutil, subprocess, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36'}
WG = os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\WinGet\Packages')
FFMPEG = shutil.which('ffmpeg') or (glob.glob(os.path.join(WG, r'Gyan.FFmpeg*\*\bin\ffmpeg.exe')) or [None])[0]
DENO = shutil.which('deno') or (glob.glob(os.path.join(WG, r'DenoLand.Deno*\deno.exe')) or [None])[0]


def yt_id(s):
    m = re.search(r'(?:v=|youtu\.be/|shorts/|embed/)([\w-]{11})', s)
    return m.group(1) if m else s


def download(url, out):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r, open(out, 'wb') as f: shutil.copyfileobj(r, f)
    return out


def _env():
    return dict(os.environ, PATH=os.pathsep.join(p for p in (os.path.dirname(DENO or ''), os.path.dirname(FFMPEG or ''), os.environ['PATH']) if p))


YT_GAP = 6                                              # seconds between YouTube calls, across every fetch.py process
YT_COOKIES = os.path.join(ROOT, 'secrets', 'youtube_cookies.txt')   # optional, throwaway account only; never opened or printed here
BOT_HINT = ('YouTube bot check (too many requests from this connection). It lifts on its own, usually within the hour: wait and retry. '
            "If it keeps happening, export a THROWAWAY account's cookies to secrets/youtube_cookies.txt (README).")


def ytdlp(args, timeout=900):
    """run yt-dlp politely: one call at a time with a gap (bursts trigger YouTube's bot check), cookies only if the file exists"""
    import time
    lock, stamp = os.path.join(ROOT, 'out', '.yt_lock'), os.path.join(ROOT, 'out', '.yt_last')
    os.makedirs(os.path.dirname(lock), exist_ok=True)
    t0 = time.time()
    while True:                                          # cross-process lock (fetch.py may run in parallel shells)
        try: fd = os.open(lock, os.O_CREAT | os.O_EXCL); os.close(fd); break
        except FileExistsError:
            if time.time() - os.path.getmtime(lock) > 1200: os.remove(lock)   # stale lock from a killed run
            if time.time() - t0 > 1800: raise RuntimeError('yt lock timeout')
            time.sleep(1)
    try:
        last = os.path.getmtime(stamp) if os.path.exists(stamp) else 0
        if time.time() - last < YT_GAP: time.sleep(YT_GAP - (time.time() - last))
        cookies = ['--cookies', YT_COOKIES] if os.path.exists(YT_COOKIES) else []
        r = subprocess.run([sys.executable, '-m', 'yt_dlp', '--sleep-requests', '0.75', *cookies, *args],
                           capture_output=True, text=True, encoding='utf-8', errors='replace',
                           env=dict(_env(), PYTHONIOENCODING='utf-8'), timeout=timeout)
        open(stamp, 'w').close()
    finally:
        os.remove(lock)
    if 'not a bot' in (r.stderr or ''): raise RuntimeError(BOT_HINT)
    return r


def search(q, n=5):
    """YouTube search: id | title | channel | duration s | views | upcoming premiere?"""
    r = ytdlp(['--flat-playlist', '--no-warnings', '--print', '%(id)s | %(title)s | %(channel)s | %(duration)s | %(view_count)s | %(live_status)s',
               'ytsearch%d:%s' % (int(n), q)])
    return r.stdout.strip()


def peak(src, dur=15, skip=8):
    """Start (s) of the most replayed `dur`-second window, from YouTube's 'Most replayed' heatmap. None if the video has none."""
    r = ytdlp(['-q', '--no-warnings', '--no-playlist', '--skip-download', '--print', '%(heatmap)j', 'https://www.youtube.com/watch?v=' + yt_id(src)])
    try: h = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception: return None
    if not h: return None
    dur, end, best = float(dur), h[-1]['end_time'], None
    for seg in h:
        s, e = seg['start_time'], seg['start_time'] + float(dur)
        if s < skip or e > end: continue
        tot = sum(x['value'] * max(0, min(e, x['end_time']) - max(s, x['start_time'])) for x in h)
        if best is None or tot > best[1]: best = (s, tot)
    return round(best[0], 2) if best else None


def loud(path, dur=15, skip=10, tail=6):
    """Start (s) of the loudest `dur`-second window of a local video (fallback when there is no heatmap; hooks are usually the densest part)."""
    import av, numpy as np
    c = av.open(path); sr = c.streams.audio[0].rate
    rms = []; buf = np.zeros(0, np.float32); hop = sr // 2
    for f in c.decode(audio=0):
        buf = np.concatenate([buf, f.to_ndarray().astype(np.float32).mean(axis=0)])
        while len(buf) >= hop: rms.append(float(np.sqrt((buf[:hop] ** 2).mean()))); buf = buf[hop:]
    n, w = len(rms), int(float(dur) * 2)
    s0, s1 = int(float(skip) * 2), n - w - int(float(tail) * 2)
    if s1 <= s0: return 0.0
    cs = np.cumsum([0] + rms)
    i = max(range(s0, s1), key=lambda k: cs[k + w] - cs[k])
    return i / 2


def yt(src, start, dur, out):
    end = float(start) + float(dur)
    sec = ['--download-sections', '*%s-%s' % (start, end), '--force-keyframes-at-cuts'] if float(dur) > 0 else []   # dur 0 = whole video
    r = ytdlp(['-q', '--no-warnings', '--no-playlist', '-f', 'bv*[height<=1080][vcodec^=avc1]+ba[ext=m4a]/bv*[height<=1080]+ba/b[height<=1080]/b',
               *sec, '--merge-output-format', 'mp4', '--ffmpeg-location', os.path.dirname(FFMPEG), '-o', out,
               'https://www.youtube.com/watch?v=' + yt_id(src)])
    if r.returncode or not os.path.exists(out): raise RuntimeError((r.stderr or r.stdout)[-800:])
    return out


def thumb(src, out):
    vid = yt_id(src)
    for q in ('maxresdefault', 'hqdefault'):
        try: return download('https://i.ytimg.com/vi/%s/%s.jpg' % (vid, q), out)
        except Exception: pass
    raise RuntimeError('no thumbnail for ' + vid)


def frame(video, sec, out):
    subprocess.run([FFMPEG, '-y', '-loglevel', 'error', '-ss', str(sec), '-i', video, '-frames:v', '1', '-q:v', '2', out], check=True)
    return out


def x_media(src, prefix):
    sid = re.search(r'(\d{8,})', src).group(1)
    d = json.loads(urllib.request.urlopen(urllib.request.Request('https://api.fxtwitter.com/status/' + sid, headers=UA), timeout=30).read())
    t = d.get('tweet') or {}
    outs = []
    for i, m in enumerate(((t.get('media') or {}).get('all')) or []):
        url = m.get('url'); ext = '.mp4' if m.get('type') in ('video', 'gif') else '.jpg'
        if 'pbs.twimg.com' in url and ext == '.jpg': url = url.split('?')[0] + '?name=orig'
        outs.append(download(url, '%s_%d%s' % (prefix, i + 1, ext)))
    return dict(text=t.get('text', ''), author=(t.get('author') or {}).get('screen_name'), files=outs)


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    cmd = a[0]
    if cmd == 'yt': print(yt(a[1], a[2], a[3], a[4]))
    elif cmd == 'search': print(search(a[1], *a[2:3]))
    elif cmd == 'peak': print(peak(a[1], *a[2:4]))
    elif cmd == 'loud': print(loud(a[1], *a[2:4]))
    elif cmd == 'thumb': print(thumb(a[1], a[2]))
    elif cmd == 'frame': print(frame(a[1], a[2], a[3]))
    elif cmd == 'x': print(json.dumps(x_media(a[1], a[2]), ensure_ascii=False))
    elif cmd == 'url': print(download(a[1], a[2]))
    else: sys.exit(__doc__)
