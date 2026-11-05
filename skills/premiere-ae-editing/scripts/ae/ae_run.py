"""ae_run.py: run an After Effects script unattended and wait for it the safe way.

usage: python ae_run.py build.jsx [--timeout 3600] [--kill-stuck]

Why each step exists (all learned the hard way):
- AfterFX.exe -r HANDS the script to an already running AE. If one is open (maybe the user's!) or still quitting,
  the script runs there or render() silently does nothing. So this refuses to start while AfterFX.exe runs.
  --kill-stuck kills it first: only use that for an AE you started yourself that hung on the Home screen.
- AE does not always quit after app.quit(). Killing it as soon as the DONE flag appears left 1 MB stub .movs,
  so this waits until every output in <stem>_jobs.json has stopped growing, then gives AE 60 s to exit,
  then kills only the process it started.
- After a kill, the next AE launch can show "Crash Repair Options": the user (or you, by screen) clicks Continue.
Reads <stem>_DONE.txt and <stem>_log.txt next to the .jsx (ae_build.py / ae_assemble.py / ae_dump.py write those names).
"""
import sys, os, glob, time, json, subprocess, argparse


def ae_exe():
    # AfterFX.com (console launcher) first: on 13 Oct 2026 (AE 26.5 with the new Home screen) AfterFX.exe -r stopped
    # running scripts at all, while AfterFX.com -r ran them (and printed AE's console output).
    for name in ('AfterFX.com', 'AfterFX.exe'):
        c = sorted(glob.glob(r'C:\Program Files\Adobe\Adobe After Effects *\Support Files' + '\\' + name))
        if c: return c[-1]
    sys.exit('After Effects not found under C:\\Program Files\\Adobe')


def ae_running():
    # AE launched through AfterFX.com runs as "AfterFX.com" (seen 13 Oct 2026), not "AfterFX.exe": check both
    out = subprocess.run(['tasklist'], capture_output=True, text=True).stdout.lower()
    return 'afterfx.exe' in out or 'afterfx.com' in out


def sizes(jobs):
    out = {}
    for j in jobs:
        f = j['file']
        if '[#####]' in f:
            d = os.path.dirname(f); out[f] = (len(os.listdir(d)) if os.path.isdir(d) else 0, 0)
        else:
            out[f] = (1, os.path.getsize(f)) if os.path.exists(f) else (0, 0)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('jsx'); ap.add_argument('--timeout', type=int, default=3600); ap.add_argument('--kill-stuck', action='store_true')
    a = ap.parse_args()
    jsx = os.path.abspath(a.jsx); base = os.path.splitext(jsx)[0]
    done, logf, jobsf = base + '_DONE.txt', base + '_log.txt', base + '_jobs.json'
    jobs = json.load(open(jobsf)) if os.path.exists(jobsf) else []
    for _ in range(30):
        if not ae_running(): break
        time.sleep(2)
    if ae_running():
        if not a.kill_stuck:
            sys.exit('After Effects is already running. Ask the user to close it (or use --kill-stuck for an AE you started that hung).')
        subprocess.run(['taskkill', '/IM', 'AfterFX.exe', '/F'], capture_output=True); time.sleep(4)
    for f in (done, logf):
        if os.path.exists(f): os.remove(f)
    t0 = time.time()
    proc = subprocess.Popen([ae_exe(), '-r', jsx], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(15)
    t_start = time.time()
    while not os.path.exists(logf) and not os.path.exists(done):   # the generated jsx logs START first
        if time.time() - t_start > 150:
            print('NO START: AE never ran the script. Check Edit > Preferences > Scripting & Expressions > '
                  '"Allow Scripts to Write Files and Access Network" (the user must tick it; it was found off on 13 Oct 2026), '
                  'or AE is stuck on a dialog / the Home screen.')
            break
        time.sleep(3)
    while not os.path.exists(done) and os.path.exists(logf):
        if time.time() - t0 > a.timeout: print('TIMEOUT waiting for', os.path.basename(done)); break
        if not ae_running(): print('AE exited before the DONE flag (crash?)'); break
        time.sleep(5)
    prev = None
    for _ in range(120):                       # outputs must stop growing before anything is killed
        cur = sizes(jobs)
        if cur == prev: break
        prev = cur; time.sleep(5)
    for _ in range(30):
        if not ae_running(): break
        time.sleep(2)
    if ae_running():
        subprocess.run(['taskkill', '/PID', str(proc.pid), '/T', '/F'], capture_output=True); time.sleep(3)
        print('AE did not quit by itself: killed the instance this run started' + (' (another AfterFX.exe is still running!)' if ae_running() else ''))
    if os.path.exists(logf):
        for line in open(logf, encoding='utf-8', errors='replace'):
            if any(k in line for k in ('FAIL', 'FATAL', 'missing', 'error', 'status')) and not line.startswith('  param'): print('  ' + line.rstrip())
    for j in jobs:
        f = j['file']
        if '[#####]' in f:
            d = os.path.dirname(f); n = len(os.listdir(d)) if os.path.isdir(d) else 0; print('  %-28s %d frames' % (j['name'], n))
        else:
            print('  %-28s %s' % (j['name'], '%.1f MB' % (os.path.getsize(f) / 1e6) if os.path.exists(f) else 'MISSING'))
    print('took %.0f s' % (time.time() - t0))


# ======================================================================================================= macOS
# On a Mac this file runs mac_main() instead of main() (from the Mac port of this skill, Oct 2026). Windows never runs it.
# usage on a Mac: ~/.venvs/premiere-ae/bin/python ae_run.py build.jsx [--timeout 3600] [--ae 2026] [--keep-open]
# Why each step exists (learned on the Mac):
# - Scripts go in through AppleScript DoScript, which hands them to the RUNNING After Effects. If the user has a project
#   open there, a build script's app.newProject() would replace it, so this probes AE first and refuses when a project is
#   open (saved file, unsaved changes or any items). The generated scripts check the same thing again before building.
# - AE not running: it is launched hidden with `open -g <app>` (`open -a` did not start it), then pinged with a tiny probe
#   script until it answers. Only an AE this runner launched is quit at the end (TERM to its own PID if it will not quit).
# - DoScript always returns 0, and a modal dialog in AE makes it return without running anything, so the scripts write
#   their own log and DONE flag; after DONE every output in <stem>_jobs.json must stop growing before AE is quit.
# - On macOS the generated scripts never call app.quit(): this runner decides, so a .jsx run by hand from File > Scripts
#   never closes the user's AE. (On Windows they still quit AE themselves, which main() above relies on.)
_OSA = '''on run argv
    with timeout of (item 2 of argv as integer) seconds
        tell application "%s" to DoScript (item 1 of argv)
    end timeout
end run'''


def _mac_ae_app(ver):
    c = sorted(glob.glob('/Applications/Adobe After Effects %s/Adobe After Effects %s.app' % (ver, ver)))
    if not c: sys.exit('After Effects %s not found in /Applications' % ver)
    return c[-1], 'Adobe After Effects %s' % ver


def _mac_ae_pids(app):
    out = subprocess.run(['ps', '-axo', 'pid=,command='], capture_output=True, text=True).stdout
    exe = os.path.join(app, 'Contents', 'MacOS', 'After Effects')
    return [int(l.split(None, 1)[0]) for l in out.splitlines() if l.split(None, 1)[1:] and l.split(None, 1)[1].startswith(exe)]


def _mac_do_script(name, js, timeout, wait=True):
    args = ['osascript', '-e', _OSA % name, js, str(timeout)]
    if not wait: return subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return subprocess.run(args, capture_output=True, text=True, timeout=timeout + 30)


def _mac_probe(name, timeout=60):
    """-> dict(file, dirty, items) of AE's current project, or None if AE did not answer"""
    import tempfile
    fd, p = tempfile.mkstemp(suffix='.txt', prefix='ae_probe_'); os.close(fd); os.remove(p)
    js = ('(function(){var f=new File(%s);f.encoding="UTF-8";f.lineFeed="Unix";f.open("w");var p=app.project;'
          'f.write(((p&&p.file)?p.file.fsName:"") + "\\n" + (p&&p.dirty?1:0) + "\\n" + (p?p.numItems:0));f.close();})();') % json.dumps(p)
    try: _mac_do_script(name, js, timeout)
    except subprocess.TimeoutExpired: return None
    if not os.path.exists(p): return None
    try:
        fn, dirty, items = (open(p, encoding='utf-8').read().splitlines() + ['', '0', '0'])[:3]
        return dict(file=fn or None, dirty=dirty.strip() == '1', items=int(items or 0))
    finally: os.remove(p)


def mac_main():
    ap = argparse.ArgumentParser()
    ap.add_argument('jsx'); ap.add_argument('--timeout', type=int, default=3600); ap.add_argument('--ae', default='2026')
    ap.add_argument('--keep-open', action='store_true', help='leave an AE this runner launched open afterwards')
    a = ap.parse_args()
    app, name = _mac_ae_app(a.ae)
    jsx = os.path.abspath(a.jsx); base = os.path.splitext(jsx)[0]
    done, logf, jobsf = base + '_DONE.txt', base + '_log.txt', base + '_jobs.json'
    jobs = json.load(open(jobsf)) if os.path.exists(jobsf) else []

    launched = None
    if _mac_ae_pids(app):
        st = _mac_probe(name)
        if st is None:
            sys.exit('After Effects is running but did not answer a probe (a modal dialog open?). Ask the user to look at AE.')
        if st['file'] or st['dirty'] or st['items']:
            sys.exit('After Effects has a project open (%s, %s, %d items). Ask the user to save and close it first; '
                     'never build into their project.' % (st['file'] or 'untitled', 'UNSAVED changes' if st['dirty'] else 'saved', st['items']))
        print('AE %s already open with an empty untitled project: running there (it stays open)' % a.ae)
    else:
        subprocess.run(['open', '-g', app])
        t0 = time.time()
        while time.time() - t0 < 300:
            time.sleep(5)
            pids = _mac_ae_pids(app)
            if pids and _mac_probe(name, 30) is not None:
                launched = pids[0]; break
        if not launched: sys.exit('After Effects did not start / answer within 300 s')
        print('launched AE %s hidden (pid %d) in %.0f s' % (a.ae, launched, time.time() - t0))

    for f in (done, logf):
        if os.path.exists(f): os.remove(f)
    t0 = time.time()
    proc = _mac_do_script(name, 'var __AE_RUN = true; $.evalFile(%s);' % json.dumps(jsx), a.timeout, wait=False)
    while not os.path.exists(done):
        if time.time() - t0 > a.timeout: print('TIMEOUT waiting for', os.path.basename(done)); break
        if proc.poll() is not None and not os.path.exists(done):
            time.sleep(3)
            if not os.path.exists(done):
                out, err = proc.communicate()
                print('DoScript returned without the DONE flag (a modal dialog in AE, a script error before the log, or '
                      'AE Settings > Scripting & Expressions > "Allow Scripts to Write Files and Access Network" is off). '
                      'osascript: %s %s' % (out.strip(), err.strip()))
                break
        if not _mac_ae_pids(app): print('AE exited before the DONE flag (crash?)'); break
        time.sleep(3)
    prev = None
    for _ in range(120):                       # outputs must stop growing before AE is quit
        cur = sizes(jobs)
        if cur == prev: break
        prev = cur; time.sleep(5)
    if proc.poll() is None:
        try: proc.wait(timeout=60)
        except subprocess.TimeoutExpired: pass
    if launched and not a.keep_open:
        try: _mac_do_script(name, 'app.quit();', 60)
        except subprocess.TimeoutExpired: pass
        for _ in range(30):
            if launched not in _mac_ae_pids(app): break
            time.sleep(2)
        if launched in _mac_ae_pids(app):
            os.kill(launched, 15); time.sleep(5)
            print('AE did not quit by itself: sent TERM to the instance this run started (pid %d)' % launched)
    if os.path.exists(logf):
        for line in open(logf, encoding='utf-8', errors='replace'):
            if any(k in line for k in ('FAIL', 'FATAL', 'missing', 'error', 'status', 'refus')) and not line.startswith('  param'):
                print('  ' + line.rstrip())
    for j in jobs:
        f = j['file']
        if '[#####]' in f:
            d = os.path.dirname(f); n = len(os.listdir(d)) if os.path.isdir(d) else 0; print('  %-28s %d frames' % (j['name'], n))
        else:
            print('  %-28s %s' % (j['name'], '%.1f MB' % (os.path.getsize(f) / 1e6) if os.path.exists(f) else 'MISSING'))
    print('took %.0f s' % (time.time() - t0))


if __name__ == '__main__':
    if sys.platform == 'darwin': mac_main()
    else: main()
