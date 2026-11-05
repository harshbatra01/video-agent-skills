"""capture: real screenshots of outcome.xyz pages at phone size (for the How-to, Top 3 traders and Trader story formats).

python capture.py profile <username> [out.png]      the trader's profile page (banner, avatar, P&L chart, stats)
python capture.py market <url or path> [out.png]    a market page, e.g. /markets/sports/q412
python capture.py home [out.png]                    the home page (rewards banner, market cards)
Shots are 1170 px wide (iPhone 3x). The sign-in pop-up is closed before the shot. Never covers or edits Outcome's UI.
"""
import base64, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import Studio
import formats as fm

ROOT = os.path.dirname(os.path.abspath(__file__))
UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1'
CLOSE_POPUPS = r"""(() => {
  let n = 0;
  document.querySelectorAll('[role=dialog]').forEach(d => {
    const b = [...d.querySelectorAll('button')].find(b => /close/i.test(b.getAttribute('aria-label') || '') || /^\s*[×✕xX]\s*$/.test(b.textContent || '') || (b.querySelector('svg') && !b.textContent.trim() && b.getBoundingClientRect().width < 60));
    if (b) { b.click(); n++; }
  });
  return n; })()"""


HIDE_POPUPS = ("(() => { if (!document.documentElement) return false; if (!document.getElementById('oc-hide')) { const st = document.createElement('style'); st.id = 'oc-hide';"
               " st.textContent = '[role=dialog], [role=presentation][data-open], [data-radix-portal], [data-overlay], [vaul-drawer], [data-vaul-overlay] { display: none !important; }"
               " html, body { overflow: auto !important; pointer-events: auto !important; }'; (document.head || document.documentElement).appendChild(st); } return true; })()")


class Capture:
    def __init__(self, st):
        self.st = st

    def open(self, url, w=390, h=844, scale=3, wait=6):
        st = self.st
        st.call('Emulation.setDeviceMetricsOverride', width=w, height=h, deviceScaleFactor=scale, mobile=True)
        st.call('Emulation.setUserAgentOverride', userAgent=UA)
        st.call('Emulation.setDefaultBackgroundColorOverride')
        st.call('Page.navigate', url=url)
        t0 = time.time()
        while time.time() - t0 < 25:
            time.sleep(.5)
            try:
                if st.js('document.readyState') == 'complete': break
            except Exception: pass
        time.sleep(wait)
        for _ in range(3):
            n = st.js(CLOSE_POPUPS)
            for kind in ('keyDown', 'keyUp'):
                st.call('Input.dispatchKeyEvent', type=kind, key='Escape', code='Escape', windowsVirtualKeyCode=27)
            time.sleep(.8)
        st.loaded = False                      # the studio template must be reloaded after a capture
        return st.js('document.title')

    def clean(self, tries=5):
        """close any pop-up (sign-in, app banner) right before a shot; True when no dialog is left"""
        st = self.st
        for _ in range(tries):
            if not st.js("!!document.querySelector('[role=dialog]')"): return True
            st.js(CLOSE_POPUPS)
            for kind in ('keyDown', 'keyUp'):
                st.call('Input.dispatchKeyEvent', type=kind, key='Escape', code='Escape', windowsVirtualKeyCode=27)
            time.sleep(1.0)
        return not st.js("!!document.querySelector('[role=dialog]')")

    def hide(self):
        """keep pop-ups (sign-in, app banner) hidden with a style rule: React-safe, nothing is removed from the page"""
        return self.st.js(HIDE_POPUPS)

    def shot(self, out, clip=None, full=False):
        p = {'format': 'png', 'fromSurface': True}
        if full:
            dims = self.st.js('[document.documentElement.scrollWidth, document.documentElement.scrollHeight]')
            p['captureBeyondViewport'] = True; p['clip'] = {'x': 0, 'y': 0, 'width': dims[0], 'height': min(dims[1], 4000), 'scale': 1}
        elif clip:
            p['clip'] = dict(clip, scale=1)
        data = base64.b64decode(self.st.call('Page.captureScreenshot', **p)['data'])
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True); open(out, 'wb').write(data)
        return out

    def text(self, n=600):
        return (self.st.js('document.body.innerText') or '')[:n]


def main(a):
    kind = a[0]; out_dir = os.path.join(ROOT, 'out', 'captures'); os.makedirs(out_dir, exist_ok=True)
    with Studio(fm.brand()) as st:
        c = Capture(st)
        if kind == 'profile':
            url = 'https://outcome.xyz/profile/%s' % a[1]; out = a[2] if len(a) > 2 else os.path.join(out_dir, 'profile_%s.png' % a[1])
        elif kind == 'market':
            url = a[1] if a[1].startswith('http') else 'https://outcome.xyz' + a[1]; out = a[2] if len(a) > 2 else os.path.join(out_dir, 'market_%d.png' % int(time.time()))
        else:
            url = 'https://outcome.xyz/'; out = a[1] if len(a) > 1 else os.path.join(out_dir, 'home.png')
        title = c.open(url)
        c.shot(out)
        print(title, '|', c.text(300).replace('\n', ' | ')[:300]); print(out)


if __name__ == '__main__':
    main(sys.argv[1:] or ['home'])
