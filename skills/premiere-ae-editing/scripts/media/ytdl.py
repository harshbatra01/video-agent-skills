"""Download YouTube videos in 1080p H.264 (Premiere-friendly), working around YouTube's bot checks.

READ FIRST: this route works around YouTube's bot check (the PO-token step below) and may break YouTube's Terms of
Service, even for a client's own uploads. Use it only for footage you have the rights to use, and only when the user
asks for a YouTube download; the user (the business owner) decides whether to use this route at all. The cleaner
route is the original files from the client or the rights holder, which are better quality too. It uses no sign-in
and no cookies, so private and paid videos stay out of reach.

usage: python ytdl.py URL_OR_ID [...] [--out DIR] [--max 1080] [--meta-only]
       (no video given, or --help: prints this and exits before anything starts)

How it works (Oct 2026): YouTube only serves HD streams to clients that present a "PO token". The
bgutil-ytdlp-pot-provider plugin (pip) asks a small local token server (Deno, in the folder
bgutil-ytdlp-pot-provider in the user's home folder: %USERPROFILE% on Windows, ~ on a Mac) for one; this script
starts that server if it is not running, then runs yt-dlp with the mobile-web client, which gets 1080p60 with a token
and no account. Files are named "<title>_<height>p.mp4"; download-archive.txt in OUT skips videos already fetched.
If YouTube changes again: pip install -U yt-dlp[default] bgutil-ytdlp-pot-provider, and update the
server (git pull + deno install in its server folder) to the matching version.
macOS: untested. The folders below resolve on a Mac, but ensure_server() starts the token server with Windows-only
process flags, so start the server yourself first (then this script only pings it) until the port is done.
"""
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.request

HOME = os.path.join(os.path.expanduser('~'), 'bgutil-ytdlp-pot-provider', 'server')   # ~ = %USERPROFILE% on Windows
PING = 'http://127.0.0.1:4416/ping'
CLIENTS = ['mweb', 'web_safari', 'tv']  # first is best; the others are fallbacks
LOCK = os.path.join(os.environ.get('TEMP') or tempfile.gettempdir(), 'ytdl_one_at_a_time.lock')   # %TEMP% on Windows


def take_turn():
    """One YouTube download at a time across EVERY session on this PC: two at once get blocked (403, 'format not
    available', or stuck at 0 bytes; 13 Oct, three sessions downloading together). A lock file older than 20 min is stale."""
    while True:
        try:
            fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            return
        except FileExistsError:
            try:  # stale: older than 20 min, or its process is gone (a killed download leaves the lock behind)
                pid = int(open(LOCK).read().strip() or 0)
                if time.time() - os.path.getmtime(LOCK) > 1200 or not _alive(pid):
                    os.remove(LOCK)
                    continue
            except (OSError, ValueError):
                pass
            time.sleep(3)


def _alive(pid):
    """Is a process still running? (Windows API: never os.kill(pid, 0) here, that terminates it on Windows.)"""
    if os.name != 'nt':
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False
    import ctypes
    k = ctypes.windll.kernel32
    h = k.OpenProcess(0x1000, False, pid)  # PROCESS_QUERY_LIMITED_INFORMATION
    if not h:
        return False
    code = ctypes.c_ulong()
    k.GetExitCodeProcess(h, ctypes.byref(code))
    k.CloseHandle(h)
    return code.value == 259  # STILL_ACTIVE


def end_turn():
    try:
        os.remove(LOCK)
    except OSError:
        pass


def server_up():
    try:
        with urllib.request.urlopen(PING, timeout=2) as r:
            return json.loads(r.read()).get('version')
    except Exception:
        return None


def ensure_server():
    v = server_up()
    if v:
        return v
    flags = 0x00000008 | 0x00000200  # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP: keeps running after we exit
    log = open(os.path.join(os.path.dirname(HOME), 'server.log'), 'a')
    subprocess.Popen(['deno', 'run', '--allow-env', '--allow-net', '--allow-ffi=.', '--allow-read=.', '../src/main.ts'],
                     cwd=os.path.join(HOME, 'node_modules'), stdout=log, stderr=log, creationflags=flags)
    for _ in range(40):
        time.sleep(0.5)
        v = server_up()
        if v:
            return v
    raise SystemExit('token server did not start: see ' + os.path.join(os.path.dirname(HOME), 'server.log'))


def main():
    args = [a for a in sys.argv[1:]]
    out = args[args.index('--out') + 1] if '--out' in args else '.'
    mx = args[args.index('--max') + 1] if '--max' in args else '1080'
    meta = '--meta-only' in args
    vids = [a for i, a in enumerate(args) if not a.startswith('--') and (i == 0 or args[i - 1] not in ('--out', '--max'))]
    if not vids or '--help' in args or '-h' in args:   # usage only: never start the token server for it
        sys.exit(__doc__)
    print('token server', ensure_server())
    os.makedirs(out, exist_ok=True)
    for v in vids:
        url = v if v.startswith('http') else f'https://www.youtube.com/watch?v={v}'
        take_turn()
        try:
            got = fetch(url, v, out, mx, meta)
        finally:
            end_turn()
        if not got:
            print(f'{v}: ALL CLIENTS FAILED')


def fetch(url, v, out, mx, meta):
    for c in CLIENTS:
        cmd = [sys.executable, '-m', 'yt_dlp', '--no-warnings', '--extractor-args', f'youtube:player_client={c}',
               '--sleep-requests', '1']
        if meta:
            cmd += ['-J', '--skip-download', url]
        else:
            # no '/b' fallback: on 12 Oct a response without the adaptive formats silently gave a 360p file; failing here
            # moves on to the next client instead
            cmd += ['-f', f'bv*[vcodec^=avc1][height<={mx}][height>=720]+ba[ext=m4a]/bv*[height<={mx}][height>=720]+ba',
                    '--merge-output-format', 'mp4', '--download-archive', os.path.join(out, 'download-archive.txt'),
                    '-o', os.path.join(out, '%(title)s_%(height)sp.%(ext)s'),
                    '--print', 'after_move:filepath', url]
        try:  # a throttled download can sit at 0 bytes forever: give up on this client and free the turn
            r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace',
                               timeout=120 if meta else 1200)
        except subprocess.TimeoutExpired:
            print(f'{v}: client {c} timed out')
            continue
        if r.returncode == 0:
            print(r.stdout.strip()[-400:] if not meta else f'{v}: metadata ok ({len(r.stdout)} bytes)')
            return True
        print(f'{v}: client {c} failed: {r.stderr.strip()[-200:]}')
    return False


if __name__ == '__main__':
    main()
