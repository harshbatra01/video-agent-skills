"""vcn: Vision Clipping news post builder (cards + simple videos), placeholder branding in brand.json.

usage:
  python vcn.py build batches/x.json [--only id1,id2]   -> FINALS/<batch>/@<page>/NN_<post>.png|mp4 + captions.txt per page;
                                                           Premiere layers + .xml in out/<batch>/premiere
  python vcn.py sheet <batch name> [sheet.png] [--only id1,id2]  -> out/<batch>/_sheet.png, one labelled contact sheet of the finals
  python vcn.py drive <batch name>                       -> Google Drive: RAP POSTS VISION/<DD MM YYYY>/<page>/ (finals + captions.txt)

Cards (1080x1350 PNG): uk, raptv, meme, tweet, chart, list. Rendered from templates/card.html by headless Chrome.
Videos (1080x1920 MP4, 30 fps): split, uk, meme, tweet, quote (any post with a "clip"). ffmpeg puts the clip, the
template overlay (transparent PNG) and the audio together, and also writes <id>_base.mp4 (clip layer), <id>_overlay.png
and <id>_audio.wav plus <id>.xml (FCP7 XML: File > Import in Premiere gives an editable 3-track sequence).
Headline markup: *word* = accent colour, ^word^ = second accent (red). See README.md and captions.md.
"""
import json, os, re, sys, shutil, subprocess, urllib.parse, urllib.request, glob
from xml.sax.saxutils import escape as xesc

ROOT = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(ROOT, 'templates', 'card.html')
SKILL = (os.environ.get('PAE_SCRIPTS') or os.path.expanduser('~/.claude/skills/premiere-ae-editing/scripts'))
CHROME = os.environ.get('CHROME_PATH') or next((p for p in (r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                           r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
                           '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome') if os.path.exists(p)), None)
FFMPEG = shutil.which('ffmpeg') or (glob.glob(os.path.expandvars(
    r'%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg*\*\bin\ffmpeg.exe')) or [None])[0]
FONT_DIRS = [d for d in os.environ.get('VC_FONT_DIRS', '').split(os.pathsep) if d] + [
    r'C:\Windows\Fonts', os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Windows\Fonts'), os.path.expanduser('~/Library/Fonts'), '/Library/Fonts', '/System/Library/Fonts/Supplemental', '/System/Library/Fonts']
FONTS = {'VCHead': 'Coolvetica Hv Comp.otf', 'VCMeme': 'impact.ttf', 'VCBox': 'Proxima Nova Extrabold.ttf',
         'VCSemi': 'Proxima Nova Semibold.ttf', 'VCReg': 'Proxima Nova Regular.ttf', 'VCTw': 'Helvetica.ttf',
         'VCTwB': 'Helvetica-Bold.ttf', 'VCNum': 'bahnschrift.ttf'}
EMO = os.path.join(ROOT, 'assets', 'emoji')
EMOJI = {'\U0001F525': '1f525.png', '\u203C\uFE0F': '203c.png', '\u203C': '203c.png', '\U0001F440': '1f440.png'}
CARD, VIDEO, FPS = (1080, 1350), (1080, 1920), 30
CARD_ONLY, VIDEO_ONLY = {'raptv', 'chart', 'list', 'vs', 'ytc'}, {'split', 'quote', 'tt'}
SPLIT_Y = 560          # top of the clip in the split layout (photos + caption box sit above it)
# accent per story type, the way the leaders colour-code (RapTV orange, Link Up yellow/green, red for beef and court)
THEMES = {'beef': '#FF3B30', 'court': '#FF3B30', 'breaking': '#FF3B30', 'charts': '#30D158', 'money': '#30D158',
          'throwback': '#FF9F0A', 'birthday': '#FF9F0A', 'raptv': '#FF7A00', 'news': '#FFD60A'}


# platform badges: simple-icons glyph (cached in assets/logos) as (glyph colour, tile colour, glyph scale); or give a png path
LOGOS = {'applemusic': ('#FA243C', '#fff', 1.0), 'spotify': ('#1ED760', '#000', .74), 'shazam': ('#fff', '#0088FF', .72),
         'youtube': ('#FF0000', '#fff', .8), 'youtubemusic': ('#FF0000', '#fff', .8), 'tiktok': ('#fff', '#000', .62),
         'billboard': ('#000', '#fff', .9), 'instagram': ('#fff', '#E4405F', .62), 'x': ('#fff', '#000', .56),
         'soundcloud': ('#FF5500', '#fff', .8), 'genius': ('#000', '#FFFF64', .6)}
LOGO_CDN = 'https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/%s.svg'
EMOJI_CDN = 'https://cdn.jsdelivr.net/npm/emoji-datasource-apple/img/apple/%s/%s.png'       # iPhone-style emoji, cached in assets/emoji
EMO_RE = re.compile('[\U0001F1E6-\U0001F1FF]{2}|[‼⁉←-⇿⌀-⏿☀-➿⬀-⯿\U0001F000-\U0001FAFF]'
                    '️?[\U0001F3FB-\U0001F3FF]?(?:‍[☀-➿\U0001F000-\U0001FAFF]️?[\U0001F3FB-\U0001F3FF]?)*')


def emoji_map(texts):
    """every emoji in the texts -> local iPhone-style PNG (downloaded once). Unknown ones fall back to the system font."""
    out = {}
    for t in texts:
        for seq in EMO_RE.findall(t or ''):
            if seq in out: continue
            cps = ['%x' % ord(c) for c in seq]
            for name in dict.fromkeys(['-'.join(cps), '-'.join(c for c in cps if c != 'fe0f')]):
                f = os.path.join(EMO, name + '.png')
                for size in ('160', '64'):
                    if os.path.exists(f): break
                    try:
                        req = urllib.request.Request(EMOJI_CDN % (size, name), headers={'User-Agent': 'Mozilla/5.0'})
                        data = urllib.request.urlopen(req, timeout=20).read()
                        if data[:4] == b'\x89PNG': open(f, 'wb').write(data)
                    except Exception: pass
                if os.path.exists(f): out[seq] = file_url(f); break
    return out


def logo_spec(v):
    """post 'logo': simple-icons slug ('applemusic') or an image path -> what templates/card.html draws"""
    if isinstance(v, dict) or not v: return v
    if re.search(r'\.(png|jpe?g|webp|svg)$', v, re.I) and os.path.exists(here(v)): return {'src': local(v)}
    f = os.path.join(ROOT, 'assets', 'logos', v + '.svg')
    if not os.path.exists(f):
        os.makedirs(os.path.dirname(f), exist_ok=True)
        data = urllib.request.urlopen(urllib.request.Request(LOGO_CDN % v, headers={'User-Agent': 'Mozilla/5.0'}), timeout=20).read()
        open(f, 'wb').write(data)
    fg, bg, sc = LOGOS.get(v, ('#fff', '#111', .6))
    return {'svg': re.sub(r'<title>.*?</title>', '', open(f, encoding='utf-8').read()), 'fg': fg, 'bg': bg, 'scale': sc}


def font_file(name):
    for d in FONT_DIRS:
        p = os.path.join(d, name)
        if os.path.exists(p): return p
    raise FileNotFoundError(name)


def here(p):
    """batch paths may be relative to the vc-news folder"""
    return p if not p or os.path.isabs(p) else os.path.join(ROOT, p)


def _furl(p, host=''):
    """file URL for a Windows (C:/x) or a Mac (/Users/x) path; host 'localhost' for the FCP7 XML writers"""
    a = os.path.abspath(p).replace('\\', '/')
    return 'file://' + host + ('' if a.startswith('/') else '/') + urllib.parse.quote(a, safe='/:')


def file_url(p):
    return _furl(here(p))


def local(p):
    return file_url(p) if p and not str(p).startswith(('http', 'file:', 'data:')) else p


def render(post, brand, out_png, size, video=False, tmp=None):
    """fill templates/card.html with the post and screenshot it with headless Chrome (transparent background)"""
    d = dict(post, brand=dict(brand), w=size[0], h=size[1], video=video)
    acct = (brand.get('accounts') or {}).get(post.get('account') or brand.get('default_account'))
    if acct:                                                          # which of our pages this post is for
        d['brand'].update(acct)
        if acct.get('avatar') and not os.path.isabs(acct['avatar']): d['brand']['avatar'] = os.path.join(ROOT, acct['avatar'])
    if post.get('accent') or post.get('theme') in THEMES:             # highlight colour per story type
        d['brand']['accent'] = post.get('accent') or THEMES[post['theme']]
    for k in ('photo', 'cover'):
        d[k] = local(d.get(k))
    if d.get('inset'): d['inset'] = dict(d['inset'], src=local(d['inset']['src']))
    d['faces'] = [dict(f, src=local(f['src'])) for f in d.get('faces', [])]
    d['photos'] = [dict(p, src=local(p['src'])) if isinstance(p, dict) else {'src': local(p)} for p in d.get('photos', [])]
    d['items'] = [dict(i, cover=local(i.get('cover'))) for i in d.get('items', [])]
    for k in ('logo', 'avatar'):
        d['brand'][k] = local(d['brand'].get(k))
    if d.get('logo'): d['logo'] = logo_spec(d['logo'])
    if (d.get('comment') or {}).get('avatar'): d['comment'] = dict(d['comment'], avatar=local(d['comment']['avatar']))
    d['emoji'] = emoji_map([post.get(k) for k in ('headline', 'label', 'sub', 'title', 'stats', 'artist')] +
                           [x.get(k) for x in post.get('items', []) for k in ('artist', 'title')])
    fonts = dict(FONTS, **(brand.get('fonts') or {}), **((acct or {}).get('fonts') or {}), **(post.get('fonts') or {}))   # house fonts, per page if set
    css = ''.join("@font-face{font-family:%s;src:url('%s')}" % (k, file_url(font_file(v))) for k, v in fonts.items())
    data = json.dumps(d, ensure_ascii=False).replace('</', '<\\/')
    html = open(TPL, encoding='utf-8').read().replace('/*FONTS*/', css).replace('/*DATA*/null', data)
    tmp = tmp or os.path.join(os.path.dirname(out_png), '_html'); os.makedirs(tmp, exist_ok=True)
    hp = os.path.join(tmp, os.path.splitext(os.path.basename(out_png))[0] + '.html')
    open(hp, 'w', encoding='utf-8').write(html)
    if os.path.exists(out_png): os.remove(out_png)
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                    '--window-size=%d,%d' % size, '--default-background-color=00000000', '--virtual-time-budget=6000',
                    '--user-data-dir=' + os.path.join(ROOT, '_chrome_profile'), '--screenshot=' + out_png, file_url(hp)],
                   capture_output=True, timeout=180)
    from PIL import Image
    im = Image.open(out_png)
    if im.size != size:
        im = im.crop((0, 0) + size) if im.size[0] >= size[0] and im.size[1] >= size[1] else im.resize(size)
    if not video: im = im.convert('RGB')
    im.save(out_png)
    return out_png


def probe(p):
    import av
    with av.open(p) as c:
        v = c.streams.video[0] if c.streams.video else None
        return dict(w=v.width if v else 0, h=v.height if v else 0, audio=bool(c.streams.audio), dur=float(c.duration or 0) / 1e6)


def bars(c):
    """crop for burned-in letterbox / pillarbox bars: (filter prefix, w, h). clip 'crop': false = off, 'w:h:x:y' = manual, else ffmpeg cropdetect over 4 s"""
    info = probe(c['path']); w, h = info['w'], info['h']
    if c.get('crop') is False: return '', w, h
    if isinstance(c.get('crop'), str): m = [c['crop'].split(':')]
    else:
        r = subprocess.run([FFMPEG, '-hide_banner', '-ss', str(float(c.get('in', 0)) + 0.5), '-t', '4', '-i', c['path'],
                            '-vf', 'cropdetect=24:2:0', '-f', 'null', '-'], capture_output=True, text=True)
        m = re.findall(r'crop=(\d+):(\d+):(\d+):(\d+)', r.stderr)
    if not m: return '', w, h
    cw, ch, x, y = map(int, m[-1])
    if (ch < h * 0.92 or cw < w * 0.92) and cw > w * 0.4 and ch > h * 0.4: return 'crop=%d:%d:%d:%d,' % (cw, ch, x, y), cw, ch
    return '', w, h


def fitcrop(w, h, fx=0.5, fy=0.5):
    return ('scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d:(iw-%d)*%s:(ih-%d)*%s,setsar=1'
            % (w, h, w, h, w, fx, h, fy))


SWEARS = {'fuck': 'f*ck', 'fucking': 'f*cking', 'shit': 'sh*t', 'bitch': 'b*tch', 'nigga': 'n*gga', 'motherfucker': 'm*therf*cker'}


def censor(t):
    """burned-in captions get the usual page-style stars (the audio is untouched)"""
    return re.sub(r"[A-Za-z']+", lambda m: SWEARS.get(m.group(0).lower(), m.group(0)), t)


def make_subs(post, od, dur):
    """burned-in captions for speech clips: local Whisper word times -> ASS, 3 words per line, white with black outline"""
    from PIL import ImageFont
    c, pid = post['clip'], post['id']
    wav = os.path.join(od, pid + '_16k.wav')
    subprocess.run([FFMPEG, '-y', '-loglevel', 'error', '-ss', str(c.get('in', 0)), '-t', str(dur), '-i', c['path'], '-vn',
                    '-ac', '1', '-ar', '16000', wav], check=True)
    wj = wav[:-4] + '_words.json'
    subprocess.run([sys.executable, os.path.join(SKILL, 'media', 'hear.py'), wav, wj], check=True, capture_output=True)
    dj = json.load(open(wj, encoding='utf-8'))
    words = [w for w in dj['words'] if w['s'] < float(post.get('subs_until', 1e9))]
    seg_starts = [sg['s'] for sg in dj.get('segments', [])]                 # Whisper's sentence starts = line breaks too
    fdir = os.path.join(od, '_fonts'); os.makedirs(fdir, exist_ok=True)
    ff = font_file(FONTS['VCBox']); shutil.copy(ff, fdir)
    fam = ImageFont.truetype(ff, 20).getname()[0]

    def ts(t):
        t = max(0.0, t); return '%d:%02d:%05.2f' % (t // 3600, (t % 3600) // 60, t % 60)
    ev = []
    # lines follow the speech: a phrase ends at a pause (>0.3 s) or punctuation; long phrases split into even chunks of up to 4 words
    phrases, cur = [], []
    for k, w in enumerate(words):
        cur.append(w)
        nxt = words[k + 1] if k + 1 < len(words) else None
        if not nxt or nxt['s'] - w['e'] > 0.3 or re.search(r'[.!?]$', w['w'].strip()) or any(w['s'] < st <= nxt['s'] + 0.01 for st in seg_starts):
            phrases.append(cur); cur = []
    groups = []
    for ph in phrases:
        n = -(-len(ph) // 4); size = -(-len(ph) // n)
        groups += [ph[j:j + size] for j in range(0, len(ph), size)]
    for i, g in enumerate(groups):
        txt = censor(' '.join(w['w'] for w in g)).upper().replace('{', '').replace('}', '')
        end = groups[i + 1][0]['s'] if i + 1 < len(groups) else g[-1]['e']
        ev.append('Dialogue: 0,%s,%s,Cap,,0,0,0,,%s' % (ts(g[0]['s']), ts(min(end, g[-1]['e'] + 0.4)), txt))
    ass = ('[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, '
           'PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, '
           'Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Cap,%s,70,&H00FFFFFF,'
           '&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,6,0,2,80,80,%d,1\n\n[Events]\nFormat: Layer, Start, End, '
           'Style, Name, MarginL, MarginR, MarginV, Effect, Text\n' % (fam, post.get('subs_margin', 560))) + '\n'.join(ev) + '\n'
    ap = os.path.join(od, pid + '.ass'); open(ap, 'w', encoding='utf-8').write(ass)
    return os.path.basename(ap)


def video(post, brand, pd, tmp, mp4):
    """pd = Premiere folder (overlay, clip layer, audio, xml), tmp = scratch, mp4 = the final video"""
    pid, fmt, c = post['id'], post['fmt'], dict(post['clip'], path=here(post['clip']['path']))
    post = dict(post, clip=c)
    if (post.get('audio') or {}).get('song'): post['audio'] = dict(post['audio'], song=here(post['audio']['song']))
    dur = float(c.get('dur', 15)); fx, fy = c.get('fx', 0.5), c.get('fy', 0.5)
    ov = os.path.join(pd, pid + '_overlay.png')
    vp = dict(post, fmt='uk', pos='top', quote=True) if fmt == 'quote' else post
    render(vp, brand, ov, VIDEO, video=True, tmp=tmp)
    a = post.get('audio', {'mode': 'clip'}); mode = a.get('mode', 'clip')
    inp = ['-ss', str(c.get('in', 0)), '-t', str(dur), '-i', c['path'], '-loop', '1', '-framerate', str(FPS), '-t', str(dur), '-i', ov]
    if mode in ('song', 'mix'): inp += ['-ss', str(a.get('song_in', 0)), '-t', str(dur), '-i', a['song']]
    cb, cw, ch = bars(c)
    if c.get('pre'): cb = c['pre'] + ',' + cb          # e.g. delogo=x:y:w:h over another page's burned-in caption
    if fmt == 'split':
        g = '[0:v]%s%s[v];color=c=black:s=1080x1920:r=%d:d=%s[bg];[bg][v]overlay=0:%d:shortest=1[b]' % (
            cb, fitcrop(1080, 1920 - SPLIT_Y, fx, fy), FPS, dur, SPLIT_Y)
    elif fmt == 'meme' or c.get('fill', 'blur' if fmt == 'tweet' else 'crop') == 'blur':
        if fmt == 'tweet':                                       # clip starts under the tweet card (card bottom read from the overlay alpha)
            from PIL import Image
            top = Image.open(ov).getchannel('A').point(lambda v: 255 if v > 128 else 0).getbbox()[3] + 30
        else: top = post.get('band', 460) if fmt == 'meme' else 0
        area = 1920 - top
        if ch / max(1, cw) >= area / 1080:                       # tall source: fill the area
            fg, y = fitcrop(1080, area, fx, fy), str(top)
        elif fmt in ('tweet', 'meme'):   # wide source, full width: right under a tweet card / centred under a meme band
            fg, y = 'scale=1080:-2,setsar=1', (str(top) if fmt == 'tweet' else '%d+(%d-h)/2' % (top, area))
        else:   # uk headline video: a box at least 760 tall (very wide clips lose some sides), centred at y 650 above the headline
            bh = max(760, int(round(1080 * ch / max(1, cw) / 2)) * 2)
            fg, y = fitcrop(1080, bh, fx, fy), str(650 - bh // 2)
        g = ('[0:v]%ssplit=2[x1][x2];[x1]%s,boxblur=30:2,eq=brightness=-0.22[bgv];[x2]%s[fg];'
             '[bgv][fg]overlay=0:%s:shortest=1,fps=%d[b]') % (cb, fitcrop(1080, 1920), fg, y, FPS)
    else:
        g = '[0:v]%s%s,fps=%d[b]' % (cb, fitcrop(1080, 1920, fx, fy), FPS)
    subs = make_subs(post, tmp, dur) if post.get('subs') else None
    g += ';[b]split=2[b1][b2];[b1][1:v]overlay=0:0:shortest=1' + ('[o1];[o1]subtitles=%s:fontsdir=_fonts[ov]' % subs if subs else '[ov]')
    norm = 'afade=t=out:st=%.3f:d=1,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000' % max(0.0, dur - 1)
    if mode == 'clip': g += ';[0:a]%s[a]' % norm
    elif mode == 'song': g += ';[2:a]%s[a]' % norm
    else: g += ';[2:a]volume=%sdB[s];[0:a][s]amix=inputs=2:duration=first:normalize=0,%s[a]' % (a.get('bed_db', -14), norm)
    g += ';[a]asplit=2[a1][a2]'
    base, wav = (os.path.join(pd, pid + s) for s in ('_base.mp4', '_audio.wav'))
    enc = ['-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-t', str(dur)]
    cmd = [FFMPEG, '-y', '-hide_banner', '-loglevel', 'error'] + inp + ['-filter_complex', g,
           '-map', '[ov]', '-map', '[a1]'] + enc + ['-preset', 'medium', '-crf', '19', '-c:a', 'aac', '-b:a', '192k',
           '-movflags', '+faststart', mp4, '-map', '[b2]', '-an'] + enc + ['-preset', 'veryfast', '-crf', '20', base,
           '-map', '[a2]', '-c:a', 'pcm_s16le', '-t', str(dur), wav]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=tmp)
    if r.returncode: raise RuntimeError(r.stderr[-1200:])
    write_xml(pid, pd, dur, base, ov, wav)
    write_source_xml(post, pd)
    return mp4


def write_xml(pid, od, dur, base, ov, wav):
    """FCP7 XML for File > Import in Premiere: V1 clip layer, V2 template overlay, A1 audio"""
    fr = int(round(dur * FPS)); rate = '<rate><timebase>%d</timebase><ntsc>FALSE</ntsc></rate>' % FPS

    def url(p): return _furl(p, 'localhost')

    def item(i, p, kind):
        n = xesc(os.path.basename(p))
        media = ('<media><video><samplecharacteristics>%s<width>1080</width><height>1920</height></samplecharacteristics></video></media>' % rate
                 if kind == 'v' else '<media><audio><samplecharacteristics><depth>16</depth><samplerate>48000</samplerate>'
                 '</samplecharacteristics><channelcount>2</channelcount></audio></media>')
        src = '<sourcetrack><mediatype>audio</mediatype><trackindex>1</trackindex></sourcetrack>' if kind == 'a' else ''
        return ('<clipitem id="ci-%d"><name>%s</name><enabled>TRUE</enabled><duration>%d</duration>%s<start>0</start><end>%d</end>'
                '<in>0</in><out>%d</out><file id="f-%d"><name>%s</name><pathurl>%s</pathurl>%s<duration>%d</duration>%s</file>%s</clipitem>'
                % (i, n, fr, rate, fr, fr, i, n, url(p), rate, fr, media, src))
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n<xmeml version="4"><sequence id="seq-1"><name>%s</name>'
           '<duration>%d</duration>%s<media><video><format><samplecharacteristics>%s<width>1080</width><height>1920</height>'
           '<pixelaspectratio>square</pixelaspectratio></samplecharacteristics></format><track>%s</track><track>%s</track></video>'
           '<audio><track>%s</track></audio></media></sequence></xmeml>\n'
           % (xesc(pid), fr, rate, rate, item(1, base, 'v'), item(2, ov, 'v'), item(3, wav, 'a')))
    open(os.path.join(od, pid + '.xml'), 'w', encoding='utf-8').write(xml)


def version_of(path, is_dir=False):
    """the user's rule (9 Oct 2026): never replace a delivered post. Free name: path, else path_v2, path_v3... -> (path, '_vN' or '')"""
    if not os.path.exists(path): return path, ''
    stem, ext = (path, '') if is_dir else os.path.splitext(path)
    n = 2
    while os.path.exists('%s_v%d%s' % (stem, n, ext)): n += 1
    return '%s_v%d%s' % (stem, n, ext), '_v%d' % n


def slug(pid):
    return re.sub(r'^[a-z]\d+[a-z]*_', '', pid)          # "z1_headie" -> "headie"


def write_source_xml(post, pd):
    """<id>_source.xml: V1 = the WHOLE source clip, cut to our window and scaled like the render, so the Slip tool (Y) can pick
    another part in Premiere; A1 = its own audio, linked (slips with it); V2 = the headline overlay. Sequence runs at the source fps."""
    import av
    c, pid, fmt = post['clip'], post['id'], post['fmt']
    src = here(c['path'])
    with av.open(src) as f:
        v = f.streams.video[0]; fps = int(round(float(v.average_rate or 30))); w, h = v.width, v.height
        total = int(f.duration / 1e6 * fps); has_a = bool(f.streams.audio)
    dur = float(c.get('dur', 15)); fr = int(round(dur * fps)); fin = int(round(float(c.get('in', 0)) * fps))
    if fmt == 'split': sc = max(1080 / w, (1920 - SPLIT_Y) / h)                                     # fills the clip area under the photos
    elif fmt in ('tweet', 'meme') or c.get('fill', 'blur' if fmt == 'tweet' else 'crop') == 'blur': sc = 1080 / w   # full width
    else: sc = max(1080 / w, 1920 / h)                                                             # full-bleed crop
    rate = '<rate><timebase>%d</timebase><ntsc>FALSE</ntsc></rate>' % fps
    url = lambda p: _furl(p, 'localhost')
    links = ('<link><linkclipref>v-src</linkclipref><mediatype>video</mediatype><trackindex>1</trackindex><clipindex>1</clipindex></link>'
             + ('<link><linkclipref>a-src</linkclipref><mediatype>audio</mediatype><trackindex>1</trackindex><clipindex>1</clipindex></link>' if has_a else ''))
    srcfile = ('<file id="f-src"><name>%s</name><pathurl>%s</pathurl>%s<duration>%d</duration><media><video><samplecharacteristics>%s'
               '<width>%d</width><height>%d</height></samplecharacteristics></video>%s</media></file>') % (
        xesc(os.path.basename(src)), url(src), rate, total, rate, w, h,
        '<audio><samplecharacteristics><depth>16</depth><samplerate>48000</samplerate></samplecharacteristics><channelcount>2</channelcount></audio>' if has_a else '')
    motion = ('<filter><effect><name>Basic Motion</name><effectid>basic</effectid><effectcategory>motion</effectcategory><effecttype>motion</effecttype>'
              '<mediatype>video</mediatype><parameter><parameterid>scale</parameterid><name>Scale</name><valuemin>0</valuemin><valuemax>1000</valuemax>'
              '<value>%.2f</value></parameter></effect></filter>') % (sc * 100)
    vsrc = ('<clipitem id="v-src"><name>%s</name><enabled>TRUE</enabled><duration>%d</duration>%s<start>0</start><end>%d</end><in>%d</in><out>%d</out>'
            '%s%s%s</clipitem>') % (xesc(os.path.basename(src)), total, rate, fr, fin, fin + fr, srcfile, motion, links)
    ov = os.path.join(pd, pid + '_overlay.png')
    vov = ('<clipitem id="v-ov"><name>%s</name><enabled>TRUE</enabled><duration>%d</duration>%s<start>0</start><end>%d</end><in>0</in><out>%d</out>'
           '<file id="f-ov"><name>%s</name><pathurl>%s</pathurl>%s<duration>%d</duration><media><video><samplecharacteristics>%s<width>1080</width>'
           '<height>1920</height></samplecharacteristics></video></media></file></clipitem>') % (
        xesc(os.path.basename(ov)), fr, rate, fr, fr, xesc(os.path.basename(ov)), url(ov), rate, fr, rate)
    asrc = ('<track><clipitem id="a-src"><name>%s</name><enabled>TRUE</enabled><duration>%d</duration>%s<start>0</start><end>%d</end><in>%d</in>'
            '<out>%d</out><file id="f-src"/><sourcetrack><mediatype>audio</mediatype><trackindex>1</trackindex></sourcetrack>%s</clipitem></track>') % (
        xesc(os.path.basename(src)), total, rate, fr, fin, fin + fr, links) if has_a else '<track/>'
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n<xmeml version="4"><sequence id="seq-src"><name>%s (full source)</name>'
           '<duration>%d</duration>%s<media><video><format><samplecharacteristics>%s<width>1080</width><height>1920</height>'
           '<pixelaspectratio>square</pixelaspectratio></samplecharacteristics></format><track>%s</track><track>%s</track></video>'
           '<audio>%s</audio></media></sequence></xmeml>\n') % (xesc(pid), fr, rate, rate, vsrc, vov, asrc)
    p = os.path.join(pd, pid + '_source.xml'); open(p, 'w', encoding='utf-8').write(xml)
    return p


def build(batch, only=None):
    """finals -> FINALS/<batch>/@<account>/NN_<post>.mp4|png + captions.txt (posting order per page);
    Premiere layers + xml -> out/<batch>/premiere; scratch -> out/<batch>/_temp"""
    B = json.load(open(batch, encoding='utf-8'))
    brand = json.load(open(os.path.join(ROOT, 'brand.json'), encoding='utf-8'))
    name = B.get('name') or os.path.splitext(os.path.basename(batch))[0]
    wd, fd = os.path.join(ROOT, 'out', name), os.path.join(ROOT, 'FINALS', name)
    pd, tmp = os.path.join(wd, 'premiere'), os.path.join(wd, '_temp')
    for d in (pd, tmp): os.makedirs(d, exist_ok=True)
    num, caps, ok = {}, {}, 0
    for p in B['posts']:
        if B.get('account') and not p.get('account'): p['account'] = B['account']
        acct = p.get('account') or brand.get('default_account')
        num[acct] = num.get(acct, 0) + 1
        is_video = p['fmt'] in VIDEO_ONLY or bool(p.get('clip') and p['fmt'] not in CARD_ONLY)
        fname = '%02d_%s.%s' % (num[acct], slug(p['id']), 'mp4' if is_video else 'png')
        carousel = bool(p.get('slides') and not is_video)
        stem, ext = fname[:-4], ('' if carousel else fname[-4:])
        ad = os.path.join(fd, '@' + acct)
        caps.setdefault(acct, []).append((p, stem, ext, carousel, is_video))
        if only and p['id'] not in only: continue
        os.makedirs(ad, exist_ok=True)
        target, vs = version_of(os.path.join(ad, stem + ext), carousel)   # never overwrite a delivered post: _v2, _v3...
        q = dict(p, id=p['id'] + vs)                                        # Premiere and scratch files get the version too
        try:
            if carousel:                                   # carousel: folder NN_post/ with 1.png = the card, then one slide per extra photo
                os.makedirs(target, exist_ok=True); out = os.path.join(target, '1.png')
                for k, sl in enumerate(p['slides']):
                    render(dict(dict({k2: p[k2] for k2 in ('theme', 'accent') if p.get(k2)}, fmt='slide'), **dict(sl, id='%s_s%d' % (q['id'], k + 2), account=acct)), brand, os.path.join(target, '%d.png' % (k + 2)), CARD, tmp=tmp)
            else: out = target
            video(q, brand, pd, tmp, out) if is_video else render(q, brand, out, CARD, tmp=tmp)
            if p.get('story') and not is_video:           # 9:16 Story still (vs: room for a poll sticker)
                render(dict(q, id=q['id'] + '_story'), brand, version_of(os.path.join(ad, stem + '_story.png'))[0], VIDEO, video=True, tmp=tmp)
            ok += 1; print('OK  ', p['id'], '->', os.path.relpath(out, ROOT))
        except Exception as e:
            print('FAIL', p['id'], str(e)[-400:])
    for acct, entries in caps.items():                    # captions.txt lists every version that exists on disk
        ad = os.path.join(fd, '@' + acct); os.makedirs(ad, exist_ok=True); out_lines = []
        for p, stem, ext, carousel, is_video in entries:
            vers = [stem + ext] + sorted((f for f in os.listdir(ad) if re.fullmatch(re.escape(stem) + r'_v\d+' + re.escape(ext), f)),
                                         key=lambda f: int(re.search(r'_v(\d+)', f).group(1)))
            name = ' / '.join(v + ('/' if carousel else '') for v in vers if os.path.exists(os.path.join(ad, v)) or v == stem + ext)
            if carousel: name += '  (carousel, %d slides)' % (len(p['slides']) + 1)
            if len(vers) > 1: name += '  (latest: %s)' % vers[-1]
            extra = ('\nstory: %s_story.png%s' % (stem, ', add a poll sticker: ' + p['poll'] if p.get('poll') else '') if p.get('story') and not is_video else '') + \
                    ('\npin as first comment: ' + p['pin'] if p.get('pin') else '')
            out_lines.append('%s%s\n%s%s\n' % (name, '   [post %s]' % p['when'] if p.get('when') else '', p.get('caption', ''), extra))
        open(os.path.join(ad, 'captions.txt'), 'w', encoding='utf-8').write('\n'.join(out_lines))
    print('%d built -> %s  (Premiere layers in %s)' % (ok, fd, pd))


DRIVE = os.environ.get('VC_DRIVE_DIR') or r'G:\My Drive\RAP POSTS VISION'   # Google Drive for desktop, the posting folder (Mac: ~/Library/CloudStorage/GoogleDrive-<account>/My Drive/RAP POSTS VISION)
DRIVE_PAGE = {'zonegbp': 'zonegbp', 'beatswitchfm': 'beatswitch'}


def to_drive(name, root=DRIVE):
    """copy a batch's finals into Drive the way the user sorts it (from his 10 Oct folder): '<DD MM YYYY>/<page>/' holding the
    video(s), the carousel slides loose as 1.png, 2.png... (subfolders only if a page has more than one carousel), and captions.txt.
    Identical files are skipped; a changed file never replaces the old one (_v2, _v3: the user's rule)."""
    import filecmp
    if not os.path.isdir(root): sys.exit('Drive folder not found: ' + root)
    fd = os.path.join(ROOT, 'FINALS', name)
    y, m, d = name[:10].split('-')
    day = os.path.join(root, '%s %s %s' % (d, m, y))
    copied = 0
    for ad in sorted(glob.glob(os.path.join(fd, '@*'))):
        acct = os.path.basename(ad)[1:]
        dest = os.path.join(day, DRIVE_PAGE.get(acct, acct)); os.makedirs(dest, exist_ok=True)
        carousels = [p for p in sorted(glob.glob(os.path.join(ad, '*'))) if os.path.isdir(p)]
        jobs = [(f, os.path.basename(f)) for f in sorted(glob.glob(os.path.join(ad, '*.*')))]
        for cd in carousels:
            for f in sorted(glob.glob(os.path.join(cd, '*.png')), key=lambda f: int(re.sub(r'\D', '', os.path.basename(f)) or 0)):
                jobs.append((f, os.path.basename(f) if len(carousels) == 1 else os.path.join(os.path.basename(cd), os.path.basename(f))))
        for src, rel in jobs:
            dst = os.path.join(dest, rel); os.makedirs(os.path.dirname(dst), exist_ok=True)
            if os.path.exists(dst):
                if filecmp.cmp(src, dst, shallow=False): continue
                if rel != 'captions.txt': dst = version_of(dst)[0]     # captions.txt is the page's index: always refreshed
            shutil.copy2(src, dst); copied += 1
    print('%d files -> %s' % (copied, day))
    return day


def sheet(src, out=None, only=None):
    """one contact sheet of a batch's finals: every card, plus 2 frames of every video (only = post ids)"""
    from PIL import Image, ImageDraw, ImageFont
    sys.path.insert(0, os.path.join(SKILL, 'media')); from frames import Grabber
    name = os.path.basename(os.path.normpath(src))
    fd = os.path.join(ROOT, 'FINALS', name) if os.path.isdir(os.path.join(ROOT, 'FINALS', name)) else src
    files = [f for f in sorted(glob.glob(os.path.join(fd, '**', '*.*'), recursive=True)) if f.endswith(('.png', '.mp4'))
             and not os.path.basename(f).startswith('_') and not f.endswith(('_overlay.png', '_base.mp4'))
             and (not only or any(slug(o) in os.path.relpath(f, fd) for o in only))]
    lab = lambda f: os.path.relpath(f, fd).replace('\\', '/').rsplit('.', 1)[0]
    tiles = []
    for f in files:
        if f.endswith('.png'): tiles.append((lab(f), Image.open(f).convert('RGB'))); continue
        g = Grabber(f); d = probe(f)['dur']
        for t in (1.0, d * 0.6): tiles.append(('%s %.0fs' % (lab(f), t), g.at(t).convert('RGB')))
        g.close()
    cw, ch, cols = 216, 384, 6
    S = Image.new('RGB', (cw * cols, ch * ((len(tiles) + cols - 1) // cols)), (40, 40, 40)); dr = ImageDraw.Draw(S)
    try: fnt = ImageFont.truetype('arialbd.ttf', 13)
    except OSError: fnt = ImageFont.load_default()
    for i, (lab, im) in enumerate(tiles):
        im.thumbnail((cw - 4, ch - 20)); x, y = (i % cols) * cw, (i // cols) * ch
        S.paste(im, (x + 2, y + 18)); dr.text((x + 3, y + 2), lab[:30], fill=(255, 220, 0), font=fnt)
    out = out or os.path.join(ROOT, 'out', name, '_sheet.png'); os.makedirs(os.path.dirname(out), exist_ok=True)
    S.save(out); print(out, S.size, len(tiles), 'tiles')


if __name__ == '__main__':
    if len(sys.argv) < 3: sys.exit(__doc__)
    if sys.argv[1] == 'build':
        only = sys.argv[sys.argv.index('--only') + 1].split(',') if '--only' in sys.argv else None
        build(sys.argv[2], only)
    elif sys.argv[1] == 'drive':
        to_drive(sys.argv[2])
    elif sys.argv[1] == 'sheet':
        only = sys.argv[sys.argv.index('--only') + 1].split(',') if '--only' in sys.argv else None
        args = [a for a in sys.argv[3:] if a != '--only' and (not only or a != ','.join(only))]
        sheet(sys.argv[2], args[0] if args else None, only)
