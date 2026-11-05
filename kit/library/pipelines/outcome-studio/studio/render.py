"""render: one headless Chrome for a whole batch, driven over the DevTools protocol.

    with Studio(brand) as st:
        st.still(spec, 'out.png', (1080, 1350))            # PNG (transparent=True keeps the alpha for overlays)
        st.video(spec, 'out.mp4', (1080, 1920), dur=10)    # frames from window.renderAt(t) piped into ffmpeg

templates/studio.html holds every format (window.show(spec) builds a slide, window.renderAt(t) poses it at time t).
"""
import base64, glob, json, os, shutil, socket, subprocess, time, urllib.parse, urllib.request
from websockets.sync.client import connect

ROOT = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(ROOT, 'templates', 'studio.html')
TPLS = {'studio': TPL, 'motion': os.path.join(ROOT, 'templates', 'motion.html')}
MOTION_FMTS = {'timed', 'wheel', 'demo', 'clipbanner', 'hottake', 'pnl_edit', 'livetape', 'outof100', 'aichat',
               'countdown', 'quizclock', 'forecast', 'race', 'sim100', 'linestory', 'goalclip', 'thennow', 'reel', 'matchline', 'scoreboard'}
# extra families for the motion look kit (templates/motion_more.js LOOKS)
LOOK_FONTS = {'LookBebas': ['BebasNeue-Regular.ttf'], 'LookArchivo': ['ArchivoBlack-Regular.ttf'], 'LookMono': ['JetBrainsMono-Variable.ttf'],
              'LookInter': ['Inter-Variable.ttf'], 'LookAnton': ['Anton-Regular.ttf']}
CHROME = os.environ.get('CHROME_PATH') or next((p for p in (r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                           r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
                           '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome') if os.path.exists(p)), None)
FFMPEG = shutil.which('ffmpeg') or (glob.glob(os.path.expandvars(
    r'%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg*\*\bin\ffmpeg.exe')) or [None])[0]
FONT_DIRS = [os.path.join(ROOT, 'assets', 'fonts'), r'C:\Windows\Fonts', os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Windows\Fonts'),
             os.path.expanduser('~/Library/Fonts'), '/Library/Fonts', '/System/Library/Fonts/Supplemental', '/System/Library/Fonts']


def file_url(p):
    a = os.path.abspath(p).replace('\\', '/')                                  # Windows C:/x or Mac /Users/x
    return 'file://' + ('' if a.startswith('/') else '/') + urllib.parse.quote(a, safe='/:')


def font_file(names):
    """first existing file among the candidates (our assets/fonts and its subfolders first, then Windows fonts)"""
    for n in ([names] if isinstance(names, str) else names):
        for d in FONT_DIRS:
            hits = sorted(glob.glob(os.path.join(d, '**', n), recursive=True)) if d.endswith('fonts') and 'assets' in d else                 (glob.glob(os.path.join(d, n)) if '*' in n else [os.path.join(d, n)])
            for p in hits:
                if os.path.exists(p) and 'Italic' not in os.path.basename(p): return p
    return None


def _free_port():
    s = socket.socket(); s.bind(('127.0.0.1', 0)); p = s.getsockname()[1]; s.close(); return p


def clip_frames(src, start, dur, out_dir, size=(1080, 1920), fps=30, focus=0.5, speed=1.0, focus_y=0.5):
    """cut a clip into JPG frames that fill the canvas (cover crop around a horizontal focus 0..1); returns the spec block for templates"""
    os.makedirs(out_dir, exist_ok=True)
    for f in glob.glob(os.path.join(out_dir, '*.jpg')): os.remove(f)
    W, H = size
    vf = ('setpts=PTS/%g,fps=%d,scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d:(in_w-%d)*%g:(in_h-%d)*%g'
          % (speed, fps, W, H, W, H, W, focus, H, focus_y))
    subprocess.run([FFMPEG, '-y', '-loglevel', 'error', '-ss', '%.3f' % start, '-t', '%.3f' % (dur * speed), '-i', src, '-vf', vf, '-q:v', '3',
                    os.path.join(out_dir, '%05d.jpg')], check=True)
    n = len(glob.glob(os.path.join(out_dir, '*.jpg')))
    return {'dir': file_url(out_dir) + '/', 'n': n, 'fps': fps, 'offset': 0}


def still_frames(img, dur, out_dir, size=(1080, 1920), fps=30, x0=0.5, x1=0.5, z0=1.0, z1=1.12, y=0.5):
    """a camera move over a photo (pan from x0 to x1 across the width, push from zoom z0 to z1, eased), as JPG frames for the clip layer.
    Real camera moves only: no fake breathing or wobble on people."""
    from PIL import Image
    os.makedirs(out_dir, exist_ok=True)
    for f in glob.glob(os.path.join(out_dir, '*.jpg')): os.remove(f)
    im = Image.open(img).convert('RGB'); W, H = size; iw, ih = im.size; ar = W / H
    n = int(round(dur * fps))
    for i in range(n):
        t = i / max(1, n - 1); e = t * t * (3 - 2 * t)
        z = z0 + (z1 - z0) * e
        ch = min(ih, iw / ar) / z; cw = ch * ar
        cx = (x0 + (x1 - x0) * e) * iw; cy = y * ih
        l = min(max(0, cx - cw / 2), iw - cw); tp = min(max(0, cy - ch / 2), ih - ch)
        im.crop((int(l), int(tp), int(l + cw), int(tp + ch))).resize(size, Image.LANCZOS).save(os.path.join(out_dir, '%05d.jpg' % (i + 1)), quality=90)
    return {'dir': file_url(out_dir) + '/', 'n': n, 'fps': fps, 'offset': 0}


class Studio:
    def __init__(self, brand, fonts=None):
        self.brand = brand
        self.fonts = fonts or brand.get('fonts') or {}
        self.port = _free_port()
        prof = os.path.join(ROOT, '_chrome_profile', 'p%d' % self.port)     # one profile per instance: two Chromes can run side by side
        self.proc = subprocess.Popen([CHROME, '--headless=new', '--remote-debugging-port=%d' % self.port, '--user-data-dir=' + prof,
                                      '--hide-scrollbars', '--force-device-scale-factor=1', '--allow-file-access-from-files',
                                      '--no-first-run', '--no-default-browser-check', '--disable-extensions', '--mute-audio',
                                      'about:blank'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(150):
            try:
                pages = json.load(urllib.request.urlopen('http://127.0.0.1:%d/json/list' % self.port, timeout=2))
                page = next(p for p in pages if p.get('type') == 'page'); break
            except Exception:
                time.sleep(0.1)
        else:
            raise RuntimeError('Chrome did not start')
        self.ws = connect(page['webSocketDebuggerUrl'], max_size=None, open_timeout=20)
        self.n = 0
        self.call('Page.enable'); self.call('Runtime.enable')
        self.loaded = False
        self.tpl = None

    # --- protocol plumbing
    def call(self, method, **params):
        self.n += 1; mid = self.n
        self.ws.send(json.dumps({'id': mid, 'method': method, 'params': params}))
        while True:
            msg = json.loads(self.ws.recv(timeout=120))
            if msg.get('id') == mid:
                if 'error' in msg: raise RuntimeError('%s: %s' % (method, msg['error']))
                return msg.get('result', {})

    def js(self, expr):
        r = self.call('Runtime.evaluate', expression=expr, awaitPromise=True, returnByValue=True)
        if r.get('exceptionDetails'):
            raise RuntimeError('JS: %s' % json.dumps(r['exceptionDetails'])[:600])
        return (r.get('result') or {}).get('value')

    def size(self, w, h):
        self.call('Emulation.setDeviceMetricsOverride', width=w, height=h, deviceScaleFactor=1, mobile=False)

    def load(self, tpl='studio'):
        """open a template (studio = stills and light motion, motion = GSAP timelines + footage), with the house fonts injected"""
        css = []
        for fam, names in (dict(self.fonts, **LOOK_FONTS) if tpl == 'motion' else self.fonts).items():
            f = font_file(names)
            if f:
                wt = 'font-weight:100 900;' if ('Variable' in f or '[' in f) else ''
                css.append("@font-face{font-family:'%s';src:url('%s');%s}" % (fam, file_url(f), wt))
        html = open(TPLS[tpl], encoding='utf-8').read().replace('/*FONTS*/', '\n'.join(css))
        if '<!--GSAP-->' in html:
            html = html.replace('<!--GSAP-->', '<script>' + open(os.path.join(ROOT, 'assets', 'js', 'gsap.min.js'), encoding='utf-8').read() + '</script>')
        if '<!--MORE-->' in html:
            html = html.replace('<!--MORE-->', '<script>' + open(os.path.join(ROOT, 'templates', 'motion_more.js'), encoding='utf-8').read() + '</script>')
        tmp = os.path.join(ROOT, 'out', '_html'); os.makedirs(tmp, exist_ok=True)
        hp = os.path.join(tmp, '%s_live_%d.html' % (tpl, self.port)); open(hp, 'w', encoding='utf-8').write(html)
        self.call('Page.navigate', url=file_url(hp))
        for _ in range(300):
            try:
                if self.js('window.__ready === true'): break
            except Exception: pass
            time.sleep(0.05)
        self.js('document.fonts.ready.then(() => true)')
        self.loaded = True; self.tpl = tpl

    def show(self, spec, size, transparent=False):
        tpl = spec.get('tpl') or ('motion' if spec.get('fmt') in MOTION_FMTS else 'studio')
        if not self.loaded or self.tpl != tpl: self.load(tpl)
        self.size(*size)
        self.call('Emulation.setDefaultBackgroundColorOverride', **({'color': {'r': 0, 'g': 0, 'b': 0, 'a': 0}} if transparent else {}))
        spec = dict(spec, w=size[0], h=size[1], brand=dict(self.brand, **(spec.get('brand') or {})), transparent=transparent,
                    assets=file_url(os.path.join(ROOT, 'assets')) + '/')
        return self.js('window.show(%s)' % json.dumps(spec, ensure_ascii=False))

    def _shot(self, fmt='png', quality=None):
        p = {'format': fmt, 'fromSurface': True}
        if quality: p['quality'] = quality
        return base64.b64decode(self.call('Page.captureScreenshot', **p)['data'])

    # --- outputs
    def still(self, spec, out, size=(1080, 1350), transparent=False, t=None):
        info = self.show(spec, size, transparent) or {}
        self.js('window.renderAt(%s)' % json.dumps(t if t is not None else info.get('dur', 0) + 99))
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        data = self._shot('png')
        if out.lower().endswith('.jpg'):
            from PIL import Image; import io
            Image.open(io.BytesIO(data)).convert('RGB').save(out, quality=94)
        else:
            open(out, 'wb').write(data)
        return info

    def video(self, spec, out, size=(1080, 1920), dur=None, fps=30, audio=None, audio_start=0, audio_gain=0, lead=None):
        info = self.show(spec, size) or {}
        dur = dur or info.get('dur') or 8
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        cmd = [FFMPEG, '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(fps), '-c:v', 'mjpeg', '-i', '-']
        if audio:
            cmd += ['-ss', '%.3f' % audio_start, '-i', audio, '-map', '0:v', '-map', '1:a', '-shortest', '-c:a', 'aac', '-b:a', '192k',
                    '-af', 'volume=%gdB,afade=t=in:st=0:d=0.15,afade=t=out:st=%.2f:d=0.8' % (audio_gain, max(0, dur - 0.8))]
        cmd += ['-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'medium', '-r', str(fps), '-movflags', '+faststart', out]
        ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        n = int(round(dur * fps))
        # motion formats start a beat in, so the hook is already on screen in the first frame (the thumbnail)
        lead = spec.get('lead', 0.5 if self.tpl == 'motion' else 0) if lead is None else lead
        for i in range(n):
            self.js('window.renderAt(%f)' % (lead + i / fps))
            ff.stdin.write(self._shot('jpeg', 93))
        ff.stdin.close(); ff.wait()
        return dict(info, dur=dur, frames=n)

    def close(self):
        try: self.ws.close()
        except Exception: pass
        try: self.proc.terminate(); self.proc.wait(5)
        except Exception: pass
        try: shutil.rmtree(os.path.join(ROOT, '_chrome_profile', 'p%d' % self.port), ignore_errors=True)
        except Exception: pass

    def __enter__(self): return self
    def __exit__(self, *a): self.close()
