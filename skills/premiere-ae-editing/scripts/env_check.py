"""First thing on a new job: what is installed and running on this PC. usage: python env_check.py
Prints Adobe app paths + versions, which of Premiere / After Effects / Media Encoder / Photoshop are running now,
Python modules, VLC / ExifTool / Chrome, and the fonts the scripts use. Takes a couple of seconds."""
import glob, os, subprocess, sys, importlib


# ---- macOS branch (from the Mac port of this skill, Oct 2026). Windows never runs it: the Windows checks below are unchanged.
# usage on a Mac: ~/.venvs/premiere-ae/bin/python env_check.py   (adds bridge ports, venvs, Swift helpers, disk space)
def _mac_env_check():
    import plistlib, shutil, socket
    sk = os.path.dirname(os.path.abspath(__file__))

    def ver_app(app):
        try: return plistlib.load(open(os.path.join(app, 'Contents', 'Info.plist'), 'rb')).get('CFBundleShortVersionString', '?')
        except Exception: return '?'

    print('== Adobe apps')
    apps = sorted(glob.glob('/Applications/Adobe */Adobe *.app'))
    for a in apps:
        if any(k in a for k in ('Premiere', 'After Effects', 'Media Encoder', 'Photoshop', 'Audition', 'Illustrator')):
            print('  %-62s %s' % (os.path.basename(a), ver_app(a)))
    ps = subprocess.run(['ps', '-axo', 'command='], capture_output=True, text=True).stdout.splitlines()
    running = []
    for a in apps:
        exe_dir = os.path.join(a, 'Contents', 'MacOS') + '/'
        mains = {'Premiere': os.path.basename(a)[:-4], 'After Effects': 'After Effects', 'Media Encoder': os.path.basename(a)[:-4],
                 'Photoshop': os.path.basename(a)[:-4]}
        for k, exe in mains.items():
            if k in a and any(l.startswith(exe_dir + exe) and 'CEPHtml' not in l and 'crashpad' not in l for l in ps):
                running.append(os.path.basename(a)[:-4])
    print('== running now:', ', '.join(sorted(set(running))) or 'none of the Adobe apps')
    print("   (Premiere often has the user's own projects open: never quit, restart or save over them without asking)")

    def port_open(p):
        s = socket.socket(); s.settimeout(0.5)
        try: return s.connect_ex(('127.0.0.1', p)) == 0
        finally: s.close()

    tok = os.path.exists(os.path.expanduser('~/.editbridge_token'))   # existence only: never read or print the token
    print('== CEP bridge: token file %s | port 47915 (Premiere 2026) %s | port 47916 (Premiere 2025) %s'
          % ('ok' if tok else 'MISSING (bridge/install_bridge.sh, ask first)', 'listening' if port_open(47915) else 'closed',
             'listening' if port_open(47916) else 'closed'))
    print('== Python', sys.version.split()[0], sys.executable)
    for m, need in (('av', 1), ('numpy', 1), ('PIL', 1), ('esprima', 1), ('faster_whisper', 0)):
        try:
            mod = importlib.import_module(m); print('  %-15s %s' % (m, getattr(mod, '__version__', 'ok')))
        except Exception as e:
            print('  %-15s %s (%s)' % (m, 'MISSING' if need else 'not installed (optional: hear.py fallback when mlx-whisper is missing)', type(e).__name__))
    print('  tools venv: python3 -m venv ~/.venvs/premiere-ae && ~/.venvs/premiere-ae/bin/pip install av numpy pillow esprima')
    mw = os.path.expanduser('~/.venvs/mlx-whisper/bin/python')
    print('  mlx-whisper venv (hear.py on Apple Silicon):', 'ok' if os.path.exists(mw) else
          'MISSING: python3 -m venv ~/.venvs/mlx-whisper && ~/.venvs/mlx-whisper/bin/pip install mlx-whisper')
    print('== tools')
    for t in ('ffmpeg', 'ffprobe', 'swiftc', 'yt-dlp'):
        print('  %-10s %s' % (t, shutil.which(t) or 'missing'))
    print('  %-10s %s' % ('Chrome', 'ok' if os.path.exists('/Applications/Google Chrome.app') else 'missing'))
    for b in ('media/ocr', 'media/fontcheck'):
        p = os.path.join(sk, b)
        print('  %-10s %s' % (os.path.basename(b), 'built' if os.path.exists(p) else 'not built: swiftc -O %s.swift -o %s' % (p, p)))
    du = shutil.disk_usage(os.path.expanduser('~'))
    print('== disk: %.0f GB free of %.0f GB' % (du.free / 1e9, du.total / 1e9))
    print('== fonts (PostScript names the AE libraries use: ae_lib, motion_lib, scene_lib)')
    fc = os.path.join(sk, 'media', 'fontcheck')
    names = ['ProximaNova-Semibold', 'ProximaNova-Regular', 'Montserrat-Black', 'ArialUnicodeMS', 'Arial-Black',
             'DMSerifDisplay-Italic', 'Didot-Bold', 'SFProDisplay-Medium', 'SFProDisplay-Bold', 'JetBrainsMono-Regular',
             'Inter-SemiBold', 'Inter-ExtraBold']
    if os.path.exists(fc):
        out = subprocess.run([fc] + names, capture_output=True, text=True).stdout
        for l in out.splitlines(): print('  ' + l)
    else:
        print('  fontcheck not built (see tools above)')


if sys.platform == 'darwin':
    _mac_env_check()
    sys.exit(0)


def ver(exe):
    try:
        out = subprocess.run(['powershell', '-NoProfile', '-Command', '(Get-Item "%s").VersionInfo.ProductVersion' % exe], capture_output=True, text=True, timeout=20).stdout.strip()
        return out or '?'
    except Exception: return '?'

print('== Adobe')
for pat in (r'C:\Program Files\Adobe\Adobe Premiere Pro *\Adobe Premiere Pro.exe', r'C:\Program Files\Adobe\Adobe After Effects *\Support Files\AfterFX.exe',
            r'C:\Program Files\Adobe\Adobe Media Encoder *\Adobe Media Encoder.exe', r'C:\Program Files\Adobe\Adobe Photoshop *\Photoshop.exe'):
    hits = sorted(glob.glob(pat))
    print('  %-60s %s' % (hits[-1] if hits else pat + '  (not found)', ver(hits[-1]) if hits else ''))
tl = subprocess.run(['tasklist'], capture_output=True, text=True).stdout
print('== running now:', ', '.join(n for n in ('Adobe Premiere Pro.exe', 'AfterFX.exe', 'Adobe Media Encoder.exe', 'Photoshop.exe') if n in tl) or 'none of the Adobe apps')
print('== Python', sys.version.split()[0])
for m in ('av', 'numpy', 'PIL', 'esprima', 'faster_whisper'):
    try:
        mod = importlib.import_module(m); print('  %-15s %s' % (m, getattr(mod, '__version__', 'ok')))
    except Exception as e: print('  %-15s MISSING (%s)' % (m, type(e).__name__))
print('== tools')
for p in (r'C:\Program Files\VideoLAN\VLC\vlc.exe', os.path.expandvars(r'%LOCALAPPDATA%\Programs\ExifTool\ExifTool.exe'),
          r'C:\Program Files\Google\Chrome\Application\chrome.exe', r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'):
    print('  %-75s %s' % (p, 'ok' if os.path.exists(p) else 'missing'))
print('  ffmpeg on PATH:', 'yes' if subprocess.run('where ffmpeg', shell=True, capture_output=True).returncode == 0 else 'no (use PyAV)')
print('== fonts (PostScript names the AE scripts use)')
fd = os.path.expandvars(r'%WINDIR%\Fonts'); ud = os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Windows\Fonts')
names = [f.lower() for d in (fd, ud) if os.path.isdir(d) for f in os.listdir(d)]
for want in ('proximanova', 'montserrat', 'segoeui', 'coolvetica', 'powergrotesk'):
    print('  %-14s %s' % (want, 'yes' if any(want in n.replace(' ', '').replace('-', '') for n in names) else 'not in Windows font folders (may be Adobe Fonts: check in AE)'))
