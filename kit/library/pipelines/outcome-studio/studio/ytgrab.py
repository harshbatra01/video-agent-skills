"""ytgrab: footage from a YouTube video by playing it in our own headless Chrome (fallback when yt-dlp is blocked).

python ytgrab.py probe <id>                         is the player usable? prints duration and a test frame
python ytgrab.py sheet <id> [every_s=4]             contact sheet of the whole video (find the moment you want)
python ytgrab.py clip <id> <start_s> <dur_s> <out.mp4> [fps=30]
    frames are taken by seeking the player frame by frame (exact, not real time), then encoded at fps.
Sound is not captured (add music or the in-app sound). The player picks its quality from the window size (1920x1080).
"""
import base64, json, os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import formats as fm
from render import Studio, FFMPEG

ROOT = os.path.dirname(os.path.abspath(__file__))
PREP = r"""(async () => {
  let v = null;
  for (let i = 0; i < 60; i++) { v = document.querySelector('#movie_player video') || document.querySelector('video'); if (v && isFinite(v.duration) && v.duration > 0) break; await new Promise(r => setTimeout(r, 250)); }
  if (!v) return {err: 'no video'};
  v.muted = true; const mp = document.querySelector('#movie_player');
  try { mp && mp.setPlaybackQualityRange && mp.setPlaybackQualityRange('hd1080', 'hd1080'); } catch (e) {}
  try { await Promise.race([v.play(), new Promise(r => setTimeout(r, 3000))]); } catch (e) {}
  await new Promise(r => setTimeout(r, 3000)); v.pause();
  document.querySelectorAll('#masthead-container, ytd-masthead, #secondary, #below, tp-yt-iron-overlay-backdrop, ytd-popup-container, .ytp-ad-module')
    .forEach(e => e.style.setProperty('display', 'none', 'important'));
  document.querySelectorAll('.ytp-chrome-top, .ytp-chrome-bottom, .ytp-gradient-top, .ytp-gradient-bottom, .ytp-pause-overlay, .ytp-watermark, .ytp-ce-element, .ytp-spinner, .ytp-large-play-button')
    .forEach(e => e.style.setProperty('display', 'none', 'important'));
  Object.assign(v.style, {position: 'fixed', left: '0', top: '0', width: '100vw', height: '100vh', objectFit: 'contain', zIndex: 99999});
  return {dur: isFinite(v.duration) ? v.duration : null, w: v.videoWidth, h: v.videoHeight, ready: v.readyState, err: (document.querySelector('.ytp-error') || {}).innerText || null};
})()"""
SEEK = r"""(async (t) => { const v = document.querySelector('#movie_player video') || document.querySelector('video'); if (Math.abs(v.currentTime - t) < 0.001) return v.readyState;
  await new Promise(r => { const h = () => { v.removeEventListener('seeked', h); r(); }; v.addEventListener('seeked', h); v.currentTime = t; });
  for (let i = 0; i < 50 && v.readyState < 2; i++) await new Promise(r => setTimeout(r, 50));
  return v.readyState; })"""


def open_player(st, vid):
    st.size(1920, 1080)
    st.call('Page.navigate', url='https://www.youtube.com/watch?v=%s' % vid)
    time.sleep(7)
    st.loaded = False
    return st.js(PREP)


def shot(st):
    return base64.b64decode(st.call('Page.captureScreenshot', format='jpeg', quality=90, fromSurface=True)['data'])


def grab(vid, times, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    with Studio(fm.brand()) as st:
        info = open_player(st, vid)
        if not info or info.get('err') or not info.get('dur'): raise RuntimeError('player not usable: %s' % info)
        for i, t in enumerate(times):
            st.js('%s(%f)' % (SEEK, t))
            open(os.path.join(out_dir, '%05d.jpg' % (i + 1)), 'wb').write(shot(st))
    return info


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    if a[0] == 'probe':
        with Studio(fm.brand()) as st:
            info = open_player(st, a[1]); print(json.dumps(info))
            open(os.path.join(ROOT, 'out', 'yt_probe.jpg'), 'wb').write(shot(st))
    elif a[0] == 'sheet':
        every = float(a[2]) if len(a) > 2 else 4
        with Studio(fm.brand()) as st:
            info = open_player(st, a[1]); print(json.dumps(info))
        times = [k * every for k in range(int(info['dur'] // every))]
        d = os.path.join(ROOT, 'out', '_yt', a[1] + '_sheet'); grab(a[1], times, d)
        from PIL import Image, ImageDraw
        ims = [Image.open(os.path.join(d, '%05d.jpg' % (i + 1))).resize((320, 180)) for i in range(len(times))]
        cols = 6; rows = (len(ims) + cols - 1) // cols; sh = Image.new('RGB', (cols * 324, rows * 200), (20, 20, 20)); dr = ImageDraw.Draw(sh)
        for i, im in enumerate(ims):
            x, y = (i % cols) * 324, (i // cols) * 200; sh.paste(im, (x, y + 18)); dr.text((x + 4, y + 3), '%.0fs' % times[i], fill=(255, 255, 0))
        out = os.path.join(ROOT, 'out', '_yt', a[1] + '_sheet.jpg'); sh.save(out, quality=80); print(out)
    elif a[0] == 'clip':
        vid, start, dur, out = a[1], float(a[2]), float(a[3]), a[4]; fps = int(a[5]) if len(a) > 5 else 30
        times = [start + i / fps for i in range(int(dur * fps))]
        d = os.path.join(ROOT, 'out', '_yt', '%s_%d' % (vid, start)); grab(vid, times, d)
        subprocess.run([FFMPEG, '-y', '-loglevel', 'error', '-framerate', str(fps), '-i', os.path.join(d, '%05d.jpg'), '-c:v', 'libx264', '-crf', '17',
                        '-pix_fmt', 'yuv420p', out], check=True)
        print(out)
