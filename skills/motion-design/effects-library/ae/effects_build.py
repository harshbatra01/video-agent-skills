"""effects_build.py: build and render the effects library in After Effects 2026, one AE job at a time.

Adapted from a friend's Mac harness (Oct 2026). Same commands and file layout; it now picks the runner it finds:
  - our runner on Windows: ae_build.py + ae_run.py + check_jsx.py from the premiere-ae-editing skill. ae_run.py refuses
    to start while ANY After Effects runs and quits AE when the job is done. No dialog handling: if AE shows a dialog,
    stop and ask the user (never kill their AE).
  - our runner on a Mac: the same ae_run.py runs its mac_main() branch (osascript DoScript). It probes AE itself and
    refuses when a project is open, reuses an AE that has only an empty untitled project, launches AE hidden when it is
    closed and quits only an AE it launched. No dialog handling: a dialog makes the run stop with a message.
  - the friend's Mac runner: an ae_run.py that has ae_app / ae_pids / probe / do_script. Then AE stays open between
    jobs (--keep-open), an empty untitled project is reused, and known build dialogs can be dismissed (needs _tools/wins
    built with swiftc and an OCR helper in FX_OCR).
The builds were tuned in the sRGB IEC61966-2.1 working space: this harness always asks for it (AE 2026 starts new
projects in Rec.709 Gamma 2.4, which shifts sRGB PNG colours and the dither tile's thresholds).

usage (Bash timeout 600000 for real runs):
  python effects_build.py test KEY[,KEY2,...] [--times 0.5,1,2.5] [--wait 420] [--dry-run]
      Builds ae/effects/KEY.jsx (function build_KEY) alone into a scratch project, renders the main comp to
      ae/_test/KEY/KEY.mp4, saves ae/_test/KEY/KEY_test.aep and writes ae/_test/KEY/sheet.png
      (row 1: the reference frames named in the file's meta refs; row 2: our render at --times or 8 even times).
  python effects_build.py master [--keys a,b] [--no-render] [--version v1] [--showreel] [--dry-run]
      Builds every effects/*.jsx into "FX Library vN.aep" (next to the effects-library folder) and renders each main
      comp (plus a "00 Showreel" comp with --showreel) to renders/vN/.
  python effects_build.py status
      Says who holds the After Effects lock and how many callers are queued.
  --dry-run writes the .jsx and runs check_jsx.py on it. It never starts After Effects.

Settings (environment):
  AE_SCRIPTS  folder holding ae_build.py, ae_run.py, check_jsx.py. When it is not set: <PAE_SCRIPTS>/ae (PAE_SCRIPTS is
              the skill's scripts/ folder, the variable the kit library's pipelines read), else
              ~/.claude/skills/premiere-ae-editing/scripts/ae
  FX_FONTS    JSON font overrides by role, e.g. {"regular": "Inter-Regular", "medium": "Inter-Medium", "bold": "Inter-Bold"}
              (roles: regular, medium, bold, serifBold, uiRegular, uiMedium, uiSemiBold, uiLight, uiBold)
  FX_OCR      Mac only: the OCR helper used to read dialog text (a compiled Vision OCR tool that writes JSON)

Effect file header (first lines of ae/effects/KEY.jsx; NOT "// @key": ExtendScript reads //@ lines as directives and
shows a syntax error dialog that blocks AE):
  // meta key: pixel_reveal
  // meta title: Pixel Reveal
  // meta order: 1
  // meta refs: analysis/<reel id>/ref_pixel_reveal_14.0.png, ...      (reference frames; not shipped: sheet says MISSING)
  // meta size: 1920x1080        (optional, default 1920x1080)
  // meta fps: 30                (optional, default 30)
Each file defines build_KEY() that builds its comps with effectComp()/sourceComp() from lib/effects_lib.jsx and returns
the main comp. ES3 ExtendScript only.
"""
import sys, os, re, json, time, glob, shutil, subprocess, argparse, inspect

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)                         # the effects-library folder
SCRIPTS = os.path.expanduser(os.environ.get('AE_SCRIPTS') or
                             (os.path.join(os.environ['PAE_SCRIPTS'], 'ae') if os.environ.get('PAE_SCRIPTS') else
                              '~/.claude/skills/premiere-ae-editing/scripts/ae'))
sys.path.insert(0, SCRIPTS)
from ae_build import write_jsx  # noqa: E402
import ae_run  # noqa: E402

PY = sys.executable
IS_WIN = os.name == 'nt'
MAC_RUNNER = all(hasattr(ae_run, n) for n in ('ae_app', 'ae_pids', 'probe', 'do_script'))   # the friend's Mac runner
OUR_MAC = (not IS_WIN) and (not MAC_RUNNER) and hasattr(ae_run, 'mac_main')                 # our ae_run.py on a Mac
LOCK = os.path.join(HERE, '_lock')
QUEUE = os.path.join(HERE, '_queue')
STOCK = os.path.join(STUDY, 'stock').replace('\\', '/') + '/'
ROOT_FOLDER = 'FX Library (scripted build)'          # distinctive: the Mac cleanup only closes untitled projects holding it
STALE = 1500   # seconds a lock may be held before it counts as stale
# The builds were tuned in an sRGB working space (AE 2026 defaults to Rec.709 Gamma 2.4, which shifts sRGB PNG colours).
WORKING_SPACE_SPEC = ('try { app.project.workingSpace = "sRGB IEC61966-2.1"; } '
                      'catch (ews) { log("working space fail " + ews.toString()); }')


def alive(pid):
    """Is this process still running? On Windows os.kill(pid, 0) is NOT a test (signal 0 = CTRL_C_EVENT there), so
    ask the kernel instead."""
    if IS_WIN:
        import ctypes
        k = ctypes.windll.kernel32
        h = k.OpenProcess(0x1000, False, int(pid))    # PROCESS_QUERY_LIMITED_INFORMATION
        if not h:
            return False
        code = ctypes.c_ulong()
        ok = k.GetExitCodeProcess(h, ctypes.byref(code))
        k.CloseHandle(h)
        return bool(ok) and code.value == 259         # STILL_ACTIVE
    try:
        os.kill(pid, 0); return True
    except PermissionError:
        return True                                   # running, owned by someone else
    except OSError:
        return False


def lock_owner():
    try:
        pid, ts, who = (open(os.path.join(LOCK, 'owner')).read().split(' ', 2) + ['', '', ''])[:3]
        return int(pid), float(ts), who.strip()
    except Exception: return None


def acquire(label, max_wait):
    os.makedirs(QUEUE, exist_ok=True)
    ticket = os.path.join(QUEUE, '%.6f_%d' % (time.time(), os.getpid()))
    open(ticket, 'w').write(label)
    t0, said = time.time(), False
    try:
        while True:
            # drop dead tickets, find whether we are first in line
            tickets = sorted(os.listdir(QUEUE))
            live = []
            for t in tickets:
                try: pid = int(t.split('_')[1])
                except Exception: continue
                if alive(pid): live.append(t)
                else:
                    try: os.remove(os.path.join(QUEUE, t))
                    except OSError: pass
            first = live and live[0] == os.path.basename(ticket)
            if os.path.isdir(LOCK):
                own = lock_owner()
                if own is None:
                    if time.time() - os.path.getmtime(LOCK) > 60: shutil.rmtree(LOCK, ignore_errors=True)
                elif not alive(own[0]) or time.time() - own[1] > STALE:
                    print('breaking stale AE lock held by pid %d (%s)' % (own[0], own[2])); shutil.rmtree(LOCK, ignore_errors=True)
            if first:
                try:
                    os.mkdir(LOCK)
                    open(os.path.join(LOCK, 'owner'), 'w').write('%d %f %s' % (os.getpid(), time.time(), label))
                    print('AE lock acquired after %.0f s' % (time.time() - t0)); return True
                except FileExistsError: pass
            if not said:
                own = lock_owner(); print('waiting for After Effects (held by: %s; %d in queue)' % (own[2] if own else '?', len(live))); said = True
            if time.time() - t0 > max_wait:
                print('AE BUSY: waited %.0f s, retry the same command' % (time.time() - t0)); return False
            time.sleep(3)
    finally:
        try: os.remove(ticket)
        except OSError: pass


def release():
    own = lock_owner()
    if own and own[0] == os.getpid(): shutil.rmtree(LOCK, ignore_errors=True)


CLEANUP_JS = '''(function(){var f=new File(%s);f.encoding="UTF-8";f.lineFeed="Unix";f.open("w");var r="none";
try{var p=app.project; if(p && !p.file && p.numItems>0){var ours=false;for(var i=1;i<=p.numItems;i++){if(p.item(i).name==%s && p.item(i) instanceof FolderItem) ours=true;}
if(ours){p.close(CloseOptions.DO_NOT_SAVE_CHANGES); r="closed leftover build project";} else r="foreign untitled project";}}catch(e){r="err "+e.toString();}
f.write(r);f.close();})();'''

KNOWN_DIALOGS = ('unable to execute script', 'syntax error', 'crash repair', 'disk cache', 'scripting plugin is not installed',
                 'unable to call', 'is not a function', 'undefined is not')


def dismiss_dialogs():
    """Mac runner only. AE dialogs (script syntax error, crash repair, disk cache warning) block DoScript for everyone.
    Screenshot each small on-screen AE window into ae/_dialogs/, OCR it, and press Return (the default button) while AE is
    frontmost, but ONLY when every dialog is one of KNOWN_DIALOGS (never one of the user's own dialogs, e.g. a save prompt).
    Needs macOS Accessibility permission for System Events: the user grants it, never a script."""
    if IS_WIN or not MAC_RUNNER:
        return False
    wins = os.path.join(HERE, '_tools', 'wins')
    ocr = os.environ.get('FX_OCR', '')
    if not (os.path.exists(wins) and ocr and os.path.exists(ocr)):
        return False
    try: out = subprocess.run([wins], capture_output=True, text=True, timeout=20).stdout
    except Exception: return False
    dl = [l for l in out.splitlines() if 'ONSCREEN' in l and ' - ' not in l.split('|')[1]]
    if not dl: return False
    ddir = os.path.join(HERE, '_dialogs'); os.makedirs(ddir, exist_ok=True)
    pngs = []
    for l in dl:
        num = l.split()[0]; png = os.path.join(ddir, '%d_%s.png' % (int(time.time()), num))
        subprocess.run(['screencapture', '-x', '-l', num, png]); pngs.append(png)
    oj = os.path.join(ddir, 'ocr_%d.json' % int(time.time()))
    subprocess.run([ocr, oj] + pngs, capture_output=True)
    try: texts = json.load(open(oj))
    except Exception: texts = {}
    for png in pngs:
        t = ' '.join(x.get('text', '') for x in texts.get(os.path.basename(png), [])).lower()
        print('AE dialog found (%s): %s' % (os.path.basename(png), t[:160]))
        if not any(k in t for k in KNOWN_DIALOGS):
            print('  not a known build dialog: leaving it alone (it may be the user\'s). Stop and report this.'); return False
    subprocess.run(['open', '-a', ae_run.ae_app('2026')[0]]); time.sleep(1.5)
    for _ in dl:
        fm = subprocess.run(['osascript', '-e', 'tell application "System Events" to get name of first process whose frontmost is true'],
                            capture_output=True, text=True).stdout
        if 'After Effects' not in fm: break
        subprocess.run(['osascript', '-e', 'tell application "System Events" to key code 36']); time.sleep(1.2)
    subprocess.run(['osascript', '-e', 'tell application "System Events" to set visible of (first process whose name contains "After Effects") to false'],
                   capture_output=True)
    return True


def ae_ready():
    """Our runner on Windows: AE must not be running at all. Our runner on a Mac: ae_run.py probes AE itself and refuses
    when a project is open, so nothing to do here. Friend's Mac runner: AE is either not running or has an empty project
    (our own leftover untitled build project is closed)."""
    if OUR_MAC:
        return True
    if not MAC_RUNNER:
        if not IS_WIN:
            print('Not Windows, and the ae_run.py in AE_SCRIPTS has neither a mac_main() branch nor the DoScript functions '
                  '(ae_app / ae_pids / probe / do_script). Point AE_SCRIPTS at the premiere-ae-editing scripts/ae folder '
                  '(see README). --dry-run still works.')
            return False
        if ae_run.ae_running():
            print('After Effects is running. Our runner never builds into an open AE: ask the user to save and close it.')
            return False
        return True
    app, name = ae_run.ae_app('2026')
    if not ae_run.ae_pids(app): return True
    st = ae_run.probe(name)
    for attempt in range(3):
        if st is not None: break
        if not dismiss_dialogs(): break
        time.sleep(2); st = ae_run.probe(name)
    if st is None:
        print('After Effects is running but does not answer (a modal dialog?). Stop and report this; do not kill AE.'); return False
    if st['file']:
        print('After Effects has a saved project open (%s): not ours. Stop and report this.' % st['file']); return False
    if st['items'] or st['dirty']:
        out = os.path.join(HERE, '_cleanup_result.txt')
        if os.path.exists(out): os.remove(out)
        ae_run.do_script(name, CLEANUP_JS % (json.dumps(out), json.dumps(ROOT_FOLDER)), 60)
        r = open(out).read() if os.path.exists(out) else 'no answer'
        print('AE had an untitled project open: %s' % r)
        if not r.startswith('closed'): return False
    return True


def header(path):
    h = {}
    for line in open(path, encoding='utf-8'):
        m = re.match(r'\s*//\s*meta\s+(\w+)\s*:\s*(.*)$', line)
        if m: h[m.group(1)] = m.group(2).strip()
        elif line.strip() and not line.strip().startswith('//'): break
    h.setdefault('key', os.path.splitext(os.path.basename(path))[0])
    h.setdefault('title', h['key'].replace('_', ' ').title())
    h['order'] = float(h.get('order', 99))
    w, hh = (h.get('size') or '1920x1080').lower().split('x')
    h['w'], h['h'], h['fps'] = int(w), int(hh), float(h.get('fps', 30))
    h['refs'] = [r.strip() for r in (h.get('refs') or '').split(',') if r.strip()]
    return h


def font_overrides():
    raw = os.environ.get('FX_FONTS', '').strip()
    if not raw:
        return {}
    try:
        d = json.loads(raw)
        return {str(k): str(v) for k, v in d.items()}
    except Exception as e:
        sys.exit('FX_FONTS is not valid JSON: %s' % e)


def globals_lib(path, extra=''):
    s = ('var STOCK = %s;\nvar ROOTF = null;\nvar EFFECT_FOLDER = null;\nvar FONT_OVERRIDES = %s;\n%s\n') % (
        json.dumps(STOCK), json.dumps(font_overrides()), extra)
    open(path, 'w', encoding='utf-8').write(s); return path


def write(jsx_path, shots, specs, **kw):
    """write_jsx from whichever runner is installed, always in the sRGB working space the builds were tuned in.
    A write_jsx with a working_space parameter gets the name explicitly (its 'auto' default keeps AE's Rec.709 Gamma 2.4
    on Windows); an older write_jsx without it gets the setting as the first spec."""
    if 'working_space' in inspect.signature(write_jsx).parameters:
        kw.setdefault('working_space', 'sRGB IEC61966-2.1')
    else:
        specs = [WORKING_SPACE_SPEC] + list(specs)
    return write_jsx(jsx_path, shots, specs, **kw)


def check(jsx):
    chk = subprocess.run([PY, os.path.join(SCRIPTS, 'check_jsx.py'), jsx], capture_output=True, text=True)
    out = (chk.stdout + chk.stderr).strip()
    return out, ('BAD' in out or 'SYNTAX' in out or 'ES3' in out or chk.returncode != 0)


def run_jsx(jsx, label, max_wait):
    if not acquire(label, max_wait): return False
    try:
        if not ae_ready(): return False
        cmd = [PY, os.path.join(SCRIPTS, 'ae_run.py'), jsx, '--timeout', '1500'] + (['--keep-open'] if MAC_RUNNER else [])
        r = subprocess.run(cmd, capture_output=True, text=True)
        print(r.stdout.strip()); print(r.stderr.strip()) if r.stderr.strip() else None
        if OUR_MAC and r.returncode != 0:
            print('ae_run.py stopped (see its message above: usually a project open in After Effects). Nothing was built.')
            return False
        return True
    finally:
        release()


def spec_for(h, num=None):
    k = h['key']
    title = ('%02d %s' % (num, h['title'])) if num is not None else h['title']
    return ('ROOTF = folder(%s); EFFECT_FOLDER = folder(%s, ROOTF); SHOTS[%s] = build_%s(); '
            'if (SHOTS[%s]) { SHOTS[%s].parentFolder = EFFECT_FOLDER; } EFFECT_FOLDER = null;') % (
        json.dumps(ROOT_FOLDER), json.dumps(title), json.dumps(k), k, json.dumps(k), json.dumps(k))


def spec_master(h, num):
    """Library layout: numbered main comps together at the top of the root folder, helper comps in
    _Precomps and sources/<NN Title>/ (finishLibrary in lib/master_tail.jsx renames and tidies at the end)."""
    k = h['key']; title = '%02d %s' % (num, h['title'])
    return ('ROOTF = folder(%s); var PRECOMPF = folder("_Precomps and sources", ROOTF); EFFECT_FOLDER = folder(%s, PRECOMPF); '
            'SHOTS[%s] = build_%s(); if (SHOTS[%s]) { SHOTS[%s].parentFolder = ROOTF; MAINS.push([SHOTS[%s], %s]); } EFFECT_FOLDER = null;') % (
        json.dumps(ROOT_FOLDER), json.dumps(title), json.dumps(k), k, json.dumps(k), json.dumps(k), json.dumps(k), json.dumps(title))


def sheet(out_png, video, times, refs):
    import av
    from PIL import Image, ImageDraw
    rows = []
    if refs:
        ims = []
        for r in refs:
            p = r if os.path.isabs(r) else os.path.join(STUDY, r)
            try: ims.append((os.path.basename(p), Image.open(p).convert('RGB')))
            except Exception: ims.append(('MISSING ' + os.path.basename(p), Image.new('RGB', (480, 270), 'gray')))
        rows.append(('REFERENCE', ims))
    got = []
    if os.path.exists(video):
        c = av.open(video); st = c.streams.video[0]
        dur = float(st.duration * st.time_base) if st.duration else float(c.duration / 1e6)
        if not times: times = [round(dur * (i + 0.5) / 8, 2) for i in range(8)]
        want = sorted(times); fr = {}
        for f in c.decode(st):
            t = float(f.pts * st.time_base)
            for w in want:
                if w not in fr and t >= w - 0.5 / 30: fr[w] = f.to_image()
            if len(fr) == len(want): break
        c.close()
        got = [('%.2fs' % t, fr[t]) for t in times if t in fr]
    rows.append(('OURS', got))
    H = 270; lab = 18
    widths = [sum(int(im.width * H / im.height) for _, im in r[1]) or 480 for r in rows]
    S = Image.new('RGB', (max(widths), len(rows) * (H + lab + 6)), (24, 24, 24)); d = ImageDraw.Draw(S)
    y = 0
    for name, ims in rows:
        x = 0
        for lbl, im in ims:
            w = int(im.width * H / im.height); S.paste(im.resize((w, H)), (x, y + lab)); d.text((x + 4, y + 3), name + ' ' + lbl, fill=(255, 220, 0)); x += w
        y += H + lab + 6
    if S.width > 2400: S = S.resize((2400, int(S.height * 2400 / S.width)))
    S.save(out_png); return out_png


def cmd_test(a):
    keys = [k.strip() for k in a.key.split(',') if k.strip()]
    hs = []
    for key in keys:
        src = os.path.join(HERE, 'effects', key + '.jsx')
        if not os.path.exists(src): sys.exit('no such effect file: ' + src)
        for i, line in enumerate(open(src, encoding='utf-8')):
            if re.match(r'\s*//\s*@', line) or re.match(r'\s*#(include|target|script)', line):
                sys.exit('line %d of %s starts with //@ or #include: ExtendScript treats that as a directive (syntax error dialog '
                         'that blocks AE for everyone). Reword the comment.' % (i + 1, src))
        h = dict(header(src), file=src)
        if h['key'] != key: sys.exit('%s: meta key "%s" must equal the file name' % (src, h['key']))
        hs.append(h)
    if len(set((h['w'], h['h'], h['fps']) for h in hs)) > 1: sys.exit('test several keys together only when they share size and fps')
    for h in hs:
        d = os.path.join(HERE, '_test', h['key']); os.makedirs(d, exist_ok=True)
        o = os.path.join(d, h['key'] + '.mp4')
        if os.path.exists(o) and not a.dry_run: os.remove(o)
    bname = keys[0] if len(keys) == 1 else '_batch_' + '_'.join(k[:10] for k in keys)[:80]
    bdir = os.path.join(HERE, '_test', bname); os.makedirs(bdir, exist_ok=True)
    glib = globals_lib(os.path.join(bdir, '_globals.jsx'))
    shots = [dict(name=h['key'], template='h264') for h in hs]
    jsx = write(os.path.join(bdir, bname + '_test.jsx'), shots, [spec_for(h) for h in hs], out_dir=bdir,
                libs=[glib, os.path.join(HERE, 'lib', 'effects_lib.jsx')] + [h['file'] for h in hs], w=hs[0]['w'], h=hs[0]['h'],
                fps=hs[0]['fps'], aep_path=os.path.join(bdir, bname + '_test.aep'), only=[])
    out, bad = check(jsx)
    if bad or a.dry_run:
        print(out)
        if bad: sys.exit('fix the syntax / ES3 problems first (no AE run)')
        print('dry run: wrote %s, After Effects not started' % jsx); return
    if not run_jsx(jsx, 'test ' + ','.join(keys), a.wait): sys.exit(2)
    logf = os.path.splitext(jsx)[0] + '_log.txt'
    if os.path.exists(logf):
        lines = [l.rstrip() for l in open(logf, encoding='utf-8', errors='replace')]
        badl = [l for l in lines if any(k in l for k in ('FAIL', 'FATAL', 'error', 'param', 'fxp', 'deep', 'cannot', 'missing', 'refus'))]
        print('log: %s (%d lines)%s' % (logf, len(lines), '' if badl else ', no problems logged'))
        for l in badl[:40]: print('  ' + l)
    times = [float(x) for x in a.times.split(',')] if a.times else None
    for h in hs:
        d = os.path.join(HERE, '_test', h['key'])
        src_mp4 = os.path.join(bdir, h['key'] + '.mp4'); out_mp4 = os.path.join(d, h['key'] + '.mp4')
        if os.path.exists(src_mp4) and src_mp4 != out_mp4: shutil.move(src_mp4, out_mp4)
        if os.path.exists(out_mp4):
            print('render %s: %s' % (h['key'], out_mp4))
            print('sheet %s: %s' % (h['key'], sheet(os.path.join(d, 'sheet.png'), out_mp4, times, h['refs'])))
        else:
            print('NO RENDER for %s (see log)' % h['key'])
    print('scratch project (open a COPY only if you need to inspect):', os.path.join(bdir, bname + '_test.aep'))


def cmd_master(a):
    files = sorted(glob.glob(os.path.join(HERE, 'effects', '*.jsx')))
    hs = [dict(header(f), file=f) for f in files]
    if a.keys: hs = [h for h in hs if h['key'] in a.keys.split(',')]
    import esprima
    good = []
    for h in hs:   # builders edit files live: skip any file that would break the one big master script
        src = open(h['file'], encoding='utf-8').read()
        why = None
        if re.search(r'(?m)^\s*//\s*@', src): why = '//@ comment'
        elif not re.search(r'function\s+build_%s\s*\(' % re.escape(h['key']), src): why = 'no build_%s()' % h['key']
        else:
            try: esprima.parseScript(src)
            except Exception as e: why = 'syntax: %s' % e
        if why: print('SKIP %s (%s)' % (h['key'], why))
        else: good.append(h)
    hs = good
    hs.sort(key=lambda h: (h['order'], h['key']))
    rdir = os.path.join(STUDY, 'renders', a.version); os.makedirs(rdir, exist_ok=True)
    bdir = os.path.join(HERE, '_master', a.version); os.makedirs(bdir, exist_ok=True)
    glib = globals_lib(os.path.join(bdir, '_globals.jsx'), 'var MAINS = [];')
    specs = [spec_master(h, i + 1) for i, h in enumerate(hs)]
    shots = [dict(name=h['key'], template='h264') for h in hs]
    reel = os.path.join(HERE, 'lib', 'showreel.jsx')
    if a.showreel and os.path.exists(reel):
        specs.append('ROOTF = folder(%s); SHOTS["00_showreel"] = buildShowreel(%s);' % (json.dumps(ROOT_FOLDER), json.dumps([[h['key'], h['title']] for h in hs])))
    specs.append('finishLibrary();')
    libs = [glib, os.path.join(HERE, 'lib', 'effects_lib.jsx'), os.path.join(HERE, 'lib', 'master_tail.jsx')] + [h['file'] for h in hs]
    if a.showreel and os.path.exists(reel): libs.append(reel)
    aep = os.path.join(STUDY, 'FX Library %s.aep' % a.version)
    print('%d effects go into %s' % (len(hs), os.path.basename(aep)))
    jsx = write(os.path.join(bdir, 'master_%s.jsx' % a.version), shots if not a.no_render else [], specs, out_dir=rdir, libs=libs,
                w=1920, h=1080, fps=30, aep_path=aep, only=[])
    out, bad = check(jsx); print(out)
    if bad: sys.exit('fix the syntax / ES3 problems first (no AE run)')
    if a.dry_run:
        print('dry run: wrote %s, After Effects not started' % jsx); return
    if not run_jsx(jsx, 'master ' + a.version, a.wait): sys.exit(2)
    logf = os.path.splitext(jsx)[0] + '_log.txt'
    if os.path.exists(logf):
        for l in open(logf, encoding='utf-8', errors='replace'):
            if any(k in l for k in ('FAIL', 'FATAL', 'error', 'status', 'missing')): print('  ' + l.rstrip())
    print('aep:', aep, 'exists' if os.path.exists(aep) else 'MISSING')


def cmd_status(a):
    own = lock_owner()
    q = os.listdir(QUEUE) if os.path.isdir(QUEUE) else []
    kind = ('friend Mac (DoScript)' if MAC_RUNNER else 'ours, Mac (mac_main, DoScript)' if OUR_MAC
            else 'ours, Windows (AfterFX.com -r)' if IS_WIN else 'none usable (AE_SCRIPTS has no Mac branch)')
    print('runner:', kind, '| scripts:', SCRIPTS)
    print('lock:', ('pid %d for %.0f s (%s)' % (own[0], time.time() - own[1], own[2])) if own else 'free', '| queue:', len(q))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest='cmd', required=True)
    t = sp.add_parser('test'); t.add_argument('key'); t.add_argument('--times'); t.add_argument('--wait', type=int, default=420)
    t.add_argument('--dry-run', action='store_true')
    m = sp.add_parser('master'); m.add_argument('--keys'); m.add_argument('--no-render', action='store_true'); m.add_argument('--version', default='v1')
    m.add_argument('--wait', type=int, default=3000); m.add_argument('--showreel', action='store_true'); m.add_argument('--dry-run', action='store_true')
    sp.add_parser('status')
    a = ap.parse_args()
    {'test': cmd_test, 'master': cmd_master, 'status': cmd_status}[a.cmd](a)
