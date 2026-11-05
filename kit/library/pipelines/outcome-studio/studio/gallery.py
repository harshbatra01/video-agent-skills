"""gallery: one shareable proof board for a built batch (for the boss / client review).

python gallery.py <date> [<date> ...]   -> out/<first date>/gallery/index.html + img/ + vid/ (small copies, videos keep their sound)
                                         several dates (batches) go on one page, grouped by format
"""
import glob, html, json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
from render import FFMPEG

ROOT = os.path.dirname(os.path.abspath(__file__))

GROUPS = [('New video formats', ['race', 'thennow', 'countdown', 'sim100', 'quizclock', 'linestory']),
          ("After last night's games", ['matchline', 'goalclip', 'scoreboard']),
          ('Real footage and real screens', ['reel', 'livetape', 'hottake', 'pnl_edit', 'demo']), ('Series', ['aichat', 'wheel', 'timed', 'outof100']),
          ('Tests (no proof yet)', ['forecast']),
          ('Match day', ['matchday', 'radar', 'pick']), ('Debates and myths', ['fakereal', 'quiz']),
          ('Races', ['swing', 'barrace', 'ranking', 'pricetags', 'cheapest', 'tier']), ('Money and macro', ['breaking', 'number', 'ladder']),
          ("The client's formats", ['top3', 'howto', 'pnl']), ('After full time', ['replay', 'upset', 'comeback'])]
NAMES = {'matchday': 'Matchday chance card', 'radar': 'Upset radar', 'pick': 'Pick a side', 'fakereal': 'Fake vs real', 'quiz': 'Guess the %',
         'swing': 'Race swing', 'barrace': 'Chance race', 'ranking': 'Favourites ranking', 'pricetags': 'Price tags', 'cheapest': 'Cheapest dreams',
         'tier': 'Tier list', 'breaking': 'The market says', 'number': 'The number', 'ladder': 'Probability ladder', 'top3': 'Top 3 traders',
         'howto': 'How-to carousel', 'pnl': 'P&L card', 'replay': 'Full-time chart replay', 'upset': 'Upset retro', 'comeback': 'Comeback',
         'forecast': 'TEST, no proof yet: weather-skin videos by others flopped (4.8K views on a 172K page). Ours carries real chances every night; try 5 posts before relying on it.', 'thennow': 'Then vs now', 'reel': 'Tonight in 15 seconds (real footage)', 'matchline': 'Full-time line replay', 'scoreboard': "Last night's favourites", 'goalclip': 'Goal cam (real app, live)', 'race': 'If the title race was a race', 'countdown': "The money's top 6 countdown",
         'quizclock': 'Guess the favourite (timer quiz)', 'sim100': 'One match, played 100 times', 'linestory': 'The line story (one chart)',
         'livetape': "Partner hits share one device: the real app screen (967K views over the real Polymarket page). Ours: the real outcome.xyz app filmed live, Bitcoin's last 40 seconds.", 'hottake': 'Hot take + receipt', 'pnl_edit': 'P&L edit (client format)',
         'demo': 'App demo (real screens)', 'aichat': 'AI vs the money', 'wheel': 'Spin the wheel (client format)', 'timed': 'Call it in 3', 'outof100': 'Out of 100'}
WHY = {'matchday': 'Fixture cards hit 4.07M and 2.34M views on a 287K page. Ours carry the real chance for every result.',
       'radar': 'Original. Two posts per night: the underdogs before kickoff, the results the morning after.',
       'pick': 'This-or-that splits hit 3.8M to 7.5M plays with 2.3% to 8.2% shares, the best share rates in the research.',
       'fakereal': 'Original. Fake "Mbappe won the Ballon d\'Or" edits pulled 14.7M views; this answers them with the real number.',
       'quiz': 'A 7-slide quiz carousel got 29.6M plays on a 22K page. Answers sit in random positions so it cannot be gamed.',
       'swing': 'A Polymarket Ballon d\'Or top 5 ran at 9.7x its channel median. Only Outcome has the daily price history.',
       'barrace': 'Bar chart races hit 18.8M plays on TikTok. Built from the market\'s own daily prices.',
       'ranking': 'Favourites rankings ran at 17x to 56x on small accounts, without any market data.',
       'pricetags': 'Original. Rival fans send it to each other: what it costs to believe in your club.',
       'cheapest': 'Original. The longest shots on the board, in cents.', 'tier': 'Tier lists: 6.0M and 3.9M plays.',
       'breaking': 'Polymarket\'s biggest X posts are odds-move cards (14.9K likes, 7x median). TV now quotes these numbers.',
       'number': 'One giant number a day. Fastest to make, easy to recognise.',
       'ladder': 'Nobody else can make this: one market split into price levels (IPO value, Bitcoin targets).',
       'top3': 'The client\'s format, from real profile screenshots. Needs the client OK on showing usernames.',
       'howto': 'The client\'s format, over real outcome.xyz screens in a phone frame, so no chart or logo is covered.',
       'pnl': 'The client\'s format: our own card from on-chain data, transparent for the edit. Needs the username OK.',
       'replay': 'Original. The match told by the money, minute by minute, with goal markers.',
       'upset': 'Upset posts hit 2.15M views on a 14.7K page.', 'comeback': 'Original. The half-time chance, then the result.',
       'forecast': 'Original. Everyone knows "70% chance of rain". Tonight\'s games as a weather report: sunny, storm warning, upset watch. Forecast check next morning.',
       'race': 'Count-handicap ball races: 111K views; a marble "prediction" did 9x its page on 12 Oct. Nobody weights a race by real market odds yet. One honest draw, logged seed, daily series.',
       'countdown': 'Plain award countdowns did 10x to 105x their page size; odds-titled ones 0.22x, so the title stays plain and the % does the work.',
       'quizclock': 'Timer quizzes: 1.35M views on Goal Clash; quiz carousels 29.6M plays. Play-along, comment your score.',
       'sim100': '"100 people" grids: 144K views on a 4.51K page (32x). Football "played 100 times" is open ground: the biggest one found has 28K.',
       'linestory': 'One-chart spike explainers hit 3.97M (240x the channel). Only Outcome has the price history.',
       'livetape': 'The real outcome.xyz app filmed live: Bitcoin\'s last 40 seconds. A WSJ review found none of 1,105 prediction-market TikToks showed the real site.',
       'hottake': 'Hot take + market receipt: 2.81M views and 192.8K shares on a 78K page.',
       'pnl_edit': 'The client\'s format with our card from a real on-chain trade. Username masked until the client says yes.',
       'demo': 'The client\'s how-to, as video over real screens.', 'aichat': 'Series: AI vs the money, with a running score. The AI answer is a real model reply.',
       'wheel': 'The client\'s UGC format, faceless. The wheel lands on a logged random draw, then the money answers.',
       'thennow': 'Then-vs-now boards: 379K views on a 3.93K page (96x), 11 Oct. Only Outcome\'s price history can make the chance version. Weekly series.',
       'goalclip': 'The real app filmed during the match: the chance jumps on screen when the goal goes in. No broadcast footage, so no rights problem.',
       'reel': 'Real footage cut on the beat: one game per cut with its real chance; London gets Tower Bridge. Stock clips with free licences, no broadcast footage. Stadium sound underneath.',
       'matchline': 'Only Outcome has the minute-by-minute price: the match told by the money, kick-off to whistle, every goal a spike, resolved at full time. Built from the archive the morning after. Sides that barely traded are drawn faint and labelled.',
       'scoreboard': 'One fixed template after every match night: a page with 820 subscribers holds 16K to 34K views a day this way (39x). Ticks and crosses, read in a glance.',
       'timed': '3-2-1 then the answer.', 'outof100': 'What a % means, as 100 dots.'}


def kind_of(p):
    k = p.get('kind', '')
    return 'ladder' if k == 'ladder' else k


def small_img(src, dst, w=720):
    im = Image.open(src)
    if im.mode == 'RGBA':
        bg = Image.new('RGB', im.size, (11, 12, 15)); bg.paste(im, mask=im.split()[3]); im = bg
    im = im.convert('RGB'); im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    os.makedirs(os.path.dirname(dst), exist_ok=True); im.save(dst, quality=82, optimize=True)


def small_vid(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    subprocess.run([FFMPEG, '-y', '-loglevel', 'error', '-i', src, '-vf', 'scale=540:960', '-c:v', 'libx264', '-crf', '27', '-preset', 'medium',
                    '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-c:a', 'aac', '-b:a', '128k', dst], check=True)


def vid_secs(f):
    r = subprocess.run([FFMPEG, '-i', f], capture_output=True, text=True, errors='ignore').stderr
    import re
    m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', r)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)) if m else 0


def build(dates):
    dates = [dates] if isinstance(dates, str) else dates
    out = os.path.join(ROOT, 'out', dates[0], 'gallery'); os.makedirs(out, exist_ok=True)
    posts = []
    for date in dates:
        posts += _build_one(date, out)
    return out, posts


def _build_one(date, out):
    fin = sorted(glob.glob(os.path.join(ROOT, 'FINALS', date, '@*')))[0]
    batch = {}
    bp = os.path.join(ROOT, 'batches', '%s.json' % date)
    if os.path.exists(bp):
        batch = {p['id']: p for p in json.load(open(bp, encoding='utf-8'))['posts']}
    posts = []
    import re as _re
    latest = {}
    for d in sorted(glob.glob(os.path.join(fin, '[0-9][0-9]_*'))):           # a rebuilt post (NN_id_v2) replaces NN_id on the page
        if not os.path.isdir(d): continue
        base = _re.sub(r'_v\d+$', '', os.path.basename(d)[3:])            # the post id: renumbered or _vN rebuilds collapse to the newest
        v = os.path.getmtime(os.path.join(d, 'video.mp4')) if os.path.exists(os.path.join(d, 'video.mp4')) else os.path.getmtime(d)
        if base not in latest or v > latest[base][0]: latest[base] = (v, d)
    for d in sorted(x[1] for x in latest.values()):
        pid = os.path.basename(d)[3:]
        meta_p = os.path.join(ROOT, 'out', date, pid.split('_v')[0], 'post.json')
        meta = json.load(open(meta_p, encoding='utf-8')) if os.path.exists(meta_p) else {}
        slides = sorted(glob.glob(os.path.join(d, 'ig_*')), key=lambda f: int(os.path.basename(f).split('_')[1].split('.')[0]))
        imgs = []
        for i, f in enumerate(slides):
            rel = 'img/%s/%d.jpg' % (pid, i + 1); small_img(f, os.path.join(out, rel)); imgs.append(rel)
        vid = None; cover = None; secs = 0
        if os.path.exists(os.path.join(d, 'video.mp4')):
            vid = 'vid/%s.mp4' % pid; small_vid(os.path.join(d, 'video.mp4'), os.path.join(out, vid)); secs = vid_secs(os.path.join(d, 'video.mp4'))
        if os.path.exists(os.path.join(d, 'cover.jpg')):
            cover = 'img/%s/cover.jpg' % pid; small_img(os.path.join(d, 'cover.jpg'), os.path.join(out, cover), w=540)
        cap = open(os.path.join(d, 'caption.txt'), encoding='utf-8').read() if os.path.exists(os.path.join(d, 'caption.txt')) else ''
        e = batch.get(pid, {})
        posts.append({'id': pid, 'kind': kind_of(meta), 'imgs': imgs, 'vid': vid, 'cover': cover, 'secs': secs, 'caption': cap, 'when': e.get('when', ''),
                      'notes': e.get('notes') or meta.get('notes', ''), 'tt': len(glob.glob(os.path.join(d, 'tt_*')))})
    return posts


def page(date, posts, made=''):
    by = {}
    for p in posts: by.setdefault(p['kind'], []).append(p)
    E = html.escape
    def card(p):
        hold = 'HOLD' in (p['when'] or '').upper() or (p.get('notes') or '').startswith('HOLD')
        status = '<span class="chip hold">Hold: client OK on usernames</span>' if hold else '<span class="chip ready">Ready</span>'
        when = '' if hold or not p['when'] else '<span class="when">Post %s</span>' % E(p['when'])
        slides = ''.join('<img src="%s" alt="%s slide %d" loading="lazy">' % (s, E(NAMES.get(p['kind'], p['kind'])), i + 1) for i, s in enumerate(p['imgs']))
        tabs = ''
        if p['vid'] and p['imgs']:
            tabs = ('<div class="tabs" role="tablist"><button class="tab on" data-v="car">Carousel · %d</button><button class="tab" data-v="vid">Video</button></div>' % len(p['imgs']))
        media = '<div class="car" data-pane="car">%s</div>' % slides if p['imgs'] else ''
        if p['vid']:
            media += '<div class="vidwrap" data-pane="vid"%s><video src="%s" controls playsinline loop preload="none" poster="%s"></video></div>' % (
                ' hidden' if p['imgs'] else '', p['vid'], p['imgs'][0] if p['imgs'] else (p.get('cover') or ''))
        return ('<article class="post" id="%s"><header><h3>%s</h3>%s</header>%s<div class="frame">%s</div>'
                '<p class="why">%s</p>%s<div class="meta">%s<span class="fmt">%s</span></div>'
                '<details><summary>Caption</summary><pre>%s</pre></details></article>') % (
            E(p['id']), E(NAMES.get(p['kind'], p['kind'])), status, tabs, media, E(WHY.get(p['kind'], '')),
            ('<p class="note">%s</p>' % E(p['notes'])) if p.get('notes') and ('HOLD' in p['notes'] or 'placeholder' in p['notes'] or 'AI answer' in p['notes']) else '',
            when, ('%d IG slides%s' % (len(p['imgs']), (' · %d TikTok slides' % p['tt']) if p['tt'] else '')) if p['imgs'] else ('9:16 video · %d s · sound on' % round(p.get('secs') or 0)),
            E(p['caption']))
    sections = ''
    for title, kinds in GROUPS:
        items = [p for k in kinds for p in by.get(k, [])]
        if title == 'After full time' and not items:
            sections += ('<section><h2>After full time</h2><div class="later"><p><b>Full-time chart replay, upset retro, comeback and the radar results</b> '
                         'are built from minute-by-minute prices recorded live. Tonight\'s Champions League games are being recorded now; '
                         'these posts get added after full time.</p></div></section>')
            continue
        if items:
            sections += '<section><h2>%s</h2><div class="grid">%s</div></section>' % (E(title), ''.join(card(p) for p in items))
    n_slides = sum(len(p['imgs']) for p in posts); n_vid = sum(1 for p in posts if p['vid'])
    return TEMPLATE.replace('{{SECTIONS}}', sections).replace('{{N}}', str(len(posts))).replace('{{S}}', str(n_slides)).replace('{{V}}', str(n_vid)).replace('{{DATE}}', E(made or date))


TEMPLATE = r'''<title>Outcome Sample Batch</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap">
<style>
/* Proof board: every post is a phone-sized proof card, grouped by the job it does; the posts carry the colour, the board stays quiet. */
:root{--board:#E3E5E9;--card:#FFFFFF;--ink:#15171C;--muted:#59606C;--line:#C9CED6;--accent:#0A8FA8;--ready:#24804A;--hold:#C2410C;--chipbg:#EEF0F3;
  --display:'Anton','Arial Narrow',Impact,sans-serif;--body:'IBM Plex Sans','Segoe UI',system-ui,sans-serif;--mono:'IBM Plex Mono',ui-monospace,Consolas,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--board:#0F1115;--card:#171A20;--ink:#ECEEF2;--muted:#9AA1AD;--line:#2A2F38;--accent:#22D3EE;--ready:#6EE7A0;--hold:#FB923C;--chipbg:#20242C;color-scheme:dark}}
:root[data-theme="dark"]{--board:#0F1115;--card:#171A20;--ink:#ECEEF2;--muted:#9AA1AD;--line:#2A2F38;--accent:#22D3EE;--ready:#6EE7A0;--hold:#FB923C;--chipbg:#20242C;color-scheme:dark}
body{background:var(--board);color:var(--ink);font-family:var(--body);font-size:15px;line-height:1.5}
.wrap{max-width:1180px;margin:0 auto;padding-inline:clamp(16px,4vw,40px);padding-block:32px 64px;display:flex;flex-direction:column;gap:40px}
.top{display:flex;flex-direction:column;gap:14px;max-width:760px}
.eyebrow{font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
h1{font-family:var(--display);font-weight:400;font-size:clamp(40px,7vw,72px);line-height:.95;letter-spacing:.01em;text-transform:uppercase;text-wrap:balance}
.lede{font-size:17px;max-width:62ch}
.stats{display:flex;flex-wrap:wrap;gap:10px 28px;font-family:var(--mono);font-size:13px;color:var(--muted)}
.stats b{color:var(--ink);font-weight:600;font-variant-numeric:tabular-nums}
section{display:flex;flex-direction:column;gap:18px}
h2{font-family:var(--display);font-weight:400;font-size:30px;letter-spacing:.02em;text-transform:uppercase;border-top:2px solid var(--ink);padding-top:10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,330px),1fr));gap:22px}
.post{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px;display:flex;flex-direction:column;gap:10px;min-width:0}
.post header{display:flex;align-items:center;justify-content:space-between;gap:10px}
h3{font-size:16px;font-weight:700;letter-spacing:.01em}
.chip{font-family:var(--mono);font-size:11px;letter-spacing:.06em;text-transform:uppercase;padding:3px 8px;border-radius:999px;background:var(--chipbg);white-space:nowrap}
.chip.ready{color:var(--ready)} .chip.hold{color:var(--hold)}
.tabs{display:flex;gap:6px}
.tab{font:600 12px var(--mono);letter-spacing:.04em;padding:5px 10px;border-radius:8px;border:1px solid var(--line);background:transparent;color:var(--muted);cursor:pointer}
.tab.on{background:var(--ink);color:var(--card);border-color:var(--ink)}
.tab:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.frame{border-radius:10px;overflow:hidden;background:#0B0C0F}
.car{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:0;scrollbar-width:thin}
.car img{flex:0 0 100%;width:100%;aspect-ratio:4/5;object-fit:cover;scroll-snap-align:start;display:block}
.vidwrap{display:flex;justify-content:center;background:#0B0C0F}
.vidwrap video{width:100%;max-width:100%;aspect-ratio:9/16;max-height:620px;display:block;background:#0B0C0F}
.why{font-size:14px;color:var(--ink)}
.note{font-size:12.5px;color:var(--hold);border-left:2px solid var(--hold);padding-left:10px}
.meta{display:flex;flex-wrap:wrap;gap:6px 14px;font-family:var(--mono);font-size:12px;color:var(--muted)}
.when{color:var(--accent)}
details{border-top:1px solid var(--line);padding-top:8px}
summary{cursor:pointer;font-weight:600;font-size:13px}
pre{white-space:pre-wrap;word-break:break-word;font-family:var(--body);font-size:13px;color:var(--muted);margin-top:8px;max-height:240px;overflow:auto}
.later{background:var(--card);border:1px dashed var(--line);border-radius:14px;padding:18px;max-width:760px}
.rules{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:12px;font-size:14px}
.rules div{border-left:2px solid var(--accent);padding-left:12px}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto}}
</style>
<div class="wrap">
 <div class="top">
  <div class="eyebrow">Vision Clipping · Outcome faceless pages · {{DATE}}</div>
  <h1>Outcome sample batch</h1>
  <p class="lede">Every post here was built automatically from live Outcome market prices: real chances, time-stamped on screen. The new video formats come first: each has its own look, motion and sound (tap play, sound on). Below them, the carousel formats: each exports as an Instagram carousel (4:5), TikTok photo slides (9:16) and, where it moves, a 9:16 video.</p>
  <div class="stats"><span><b>{{N}}</b> posts</span><span><b>{{S}}</b> carousel slides</span><span><b>{{V}}</b> videos</span><span>prices: Hyperliquid + Outcome public data</span></div>
  <div class="rules"><div>No invented numbers. Every % comes from the market at build time.</div><div>Never covers Outcome's chart, names or logo. No "bet" language, no profit promises.</div><div>Facts outside the market (form, results) carry a source and date.</div></div>
 </div>
 {{SECTIONS}}
</div>
<script>
document.querySelectorAll('.post').forEach(card=>{
  card.querySelectorAll('.tab').forEach(t=>t.addEventListener('click',()=>{
    card.querySelectorAll('.tab').forEach(x=>x.classList.toggle('on',x===t));
    card.querySelectorAll('[data-pane]').forEach(p=>{p.hidden=p.dataset.pane!==t.dataset.v});
    const v=card.querySelector('video'); if(v){ if(t.dataset.v==='vid'){ v.play().catch(()=>{}); } else { v.pause(); } }
  }));
});
</script>
'''


if __name__ == '__main__':
    date = sys.argv[1]
    out, posts = build(sys.argv[1:])
    import datetime as dt
    made = dt.datetime.now(dt.timezone.utc).strftime('%d %b %Y, %H:%M UTC').lstrip('0')
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(page(date, posts, made))
    size = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(out) for f in fs)
    print(out, len(posts), 'posts', '%.1f MB' % (size / 1e6))
