import base64, html, os, sys
sys.path.insert(0, '.')
from pull_data import CLIPS, MANUAL, ARCHIVE, ADS, PX

E = html.escape


def thumb(vid):
    p = 'thumbs/%s.jpg' % vid
    if not os.path.exists(p): return ''
    return 'data:image/jpeg;base64,' + base64.b64encode(open(p, 'rb').read()).decode()


def pill(kind):
    return {'free': '<span class="pill ok">Free, I can download</span>',
            'manual': '<span class="pill warn">Free, download from page</span>',
            'licence': '<span class="pill lic">Needs licence</span>',
            'shoot': '<span class="pill shoot">Shoot it</span>'}[kind]


def clip_card(kind, ref):
    if kind in ('px', 'manual'):
        if kind == 'px':
            desc, res, mb = CLIPS[ref]; meta = '%s &middot; %d MB' % (res.replace('x', '&times;'), mb); p = pill('free')
        else:
            desc = MANUAL[ref]; meta = 'resolution on page'; p = pill('manual')
        return ('<a class="clip" href="%s" target="_blank" rel="noopener"><img src="%s" alt="%s" loading="lazy">'
                '<span class="cmeta"><span class="cid">Pexels %s</span><span class="cdesc">%s</span><span class="cres">%s</span>%s</span></a>') % (
            PX % ref, thumb(ref), E(desc), ref, E(desc), meta, p)
    if kind == 'archive':
        return '<div class="clip text"><span class="cmeta"><span class="cid">Paula archive</span><span class="cdesc">%s</span>%s</span></div>' % (E(ref), pill('licence'))
    return '<div class="clip text"><span class="cmeta"><span class="cid">Shoot</span><span class="cdesc">%s</span>%s</span></div>' % (E(ref), pill('shoot'))


free_ids = []
for _, _, rows in ADS:
    for _, _, picks, _ in rows:
        for k, r in picks:
            if k == 'px' and r not in free_ids: free_ids.append(r)
for extra in ('6454262', '7615546', '8122968'):
    if extra not in free_ids: free_ids.append(extra)
total_mb = sum(CLIPS[i][2] for i in free_ids)
n_lines = sum(len(r) for _, _, r in ADS)

out = []
out.append('''<title>Immufix B-roll Pull List</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..100,500..800&family=Public+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;600&display=swap">
<style>
/* Layout: an editor's pull list. One column, archive first, then each ad as timecoded rows with clip cards. */
:root{--bg:#f4f6f9;--surface:#ffffff;--ink:#141b2d;--muted:#566077;--line:#dce1ea;--gold:#86661a;--gold-soft:#f1e7cc;
--ok:#1d7349;--ok-bg:#dff2e8;--warn:#94570a;--warn-bg:#fbeedb;--lic:#a93a33;--lic-bg:#f8e1df;--shoot:#34508e;--shoot-bg:#e2e9f7;
--display:"Archivo","Arial Narrow",system-ui,sans-serif;--body:"Public Sans",system-ui,-apple-system,"Segoe UI",sans-serif;--mono:"JetBrains Mono",ui-monospace,Consolas,monospace}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#0c1220;--surface:#141b2c;--ink:#e7eaf2;--muted:#9ba4b9;--line:#263049;--gold:#d8b35a;--gold-soft:#30291a;
--ok:#57c996;--ok-bg:#15291f;--warn:#e7a54b;--warn-bg:#2d2213;--lic:#f08880;--lic-bg:#2e1716;--shoot:#93adea;--shoot-bg:#18213a;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#0c1220;--surface:#141b2c;--ink:#e7eaf2;--muted:#9ba4b9;--line:#263049;--gold:#d8b35a;--gold-soft:#30291a;
--ok:#57c996;--ok-bg:#15291f;--warn:#e7a54b;--warn-bg:#2d2213;--lic:#f08880;--lic-bg:#2e1716;--shoot:#93adea;--shoot-bg:#18213a;color-scheme:dark}
body{background:var(--bg);color:var(--ink);font:15px/1.55 var(--body)}
.wrap{max-width:1080px;margin:0 auto;padding-inline:20px;padding-block:28px 64px;display:flex;flex-direction:column;gap:40px}
h1,h2,h3{font-family:var(--display);font-stretch:85%;text-wrap:balance;margin:0}
h1{font-size:clamp(30px,5vw,46px);font-weight:800;letter-spacing:-.01em;line-height:1.05}
h2{font-size:24px;font-weight:750;letter-spacing:.005em;display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
h2 small{font:600 11px/1 var(--body);letter-spacing:.12em;text-transform:uppercase;color:var(--gold)}
h3{font-size:19px;font-weight:700}
p{margin:0;max-width:68ch}
a{color:inherit}
.muted{color:var(--muted)}
header{display:flex;flex-direction:column;gap:12px;border-bottom:2px solid var(--ink);padding-bottom:22px}
.eyebrow{font:600 11px/1 var(--body);letter-spacing:.14em;text-transform:uppercase;color:var(--gold)}
.stats{display:flex;flex-wrap:wrap;gap:10px 24px;font-variant-numeric:tabular-nums}
.stats b{font:700 20px/1 var(--display);font-stretch:85%;margin-right:6px}
.legend{display:flex;flex-wrap:wrap;gap:8px}
.pill{display:inline-block;font:600 11px/1.2 var(--body);letter-spacing:.02em;padding:4px 8px;border-radius:999px;white-space:nowrap}
.pill.ok{color:var(--ok);background:var(--ok-bg)}.pill.warn{color:var(--warn);background:var(--warn-bg)}
.pill.lic{color:var(--lic);background:var(--lic-bg)}.pill.shoot{color:var(--shoot);background:var(--shoot-bg)}
section{display:flex;flex-direction:column;gap:16px}
.note{background:var(--gold-soft);border-radius:10px;padding:14px 16px;display:flex;flex-direction:column;gap:8px}
.arch{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
.acard{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:16px;display:flex;flex-direction:column;gap:8px;min-width:0}
.acard .prio{font:600 11px/1 var(--body);letter-spacing:.1em;text-transform:uppercase;color:var(--gold)}
.acard ul{margin:0;padding-left:18px;display:flex;flex-direction:column;gap:3px}
.owner{font-size:13px;color:var(--muted)}
.ad{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:18px;display:flex;flex-direction:column;gap:6px}
.ad .seq{font:500 12px/1 var(--mono);color:var(--muted)}
.row{display:grid;grid-template-columns:minmax(0,300px) minmax(0,1fr);gap:18px;padding-block:16px;border-top:1px solid var(--line)}
.row:first-of-type{border-top:0}
.tc{font:600 12px/1 var(--mono);color:var(--gold);letter-spacing:.02em;font-variant-numeric:tabular-nums}
.words{font:600 16px/1.35 var(--display);font-stretch:92%;margin-top:6px}
.rnote{font-size:13px;color:var(--muted);margin-top:6px}
.clips{display:flex;flex-wrap:wrap;gap:12px;align-content:flex-start}
.clip{display:flex;gap:10px;width:260px;max-width:100%;background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:8px;text-decoration:none;min-width:0}
.clip:hover,.clip:focus-visible{border-color:var(--gold);outline:none}
.clip img{width:64px;height:114px;object-fit:cover;border-radius:6px;flex:none;background:var(--line)}
.clip.text{align-items:center}
.cmeta{display:flex;flex-direction:column;gap:5px;min-width:0}
.cid{font:600 11px/1 var(--mono);color:var(--muted)}
.cdesc{font-size:13px;line-height:1.35}
.cres{font:400 11px/1.2 var(--mono);color:var(--muted);font-variant-numeric:tabular-nums}
table{border-collapse:collapse;width:100%;font-size:13px}
.tablewrap{overflow-x:auto;background:var(--surface);border:1px solid var(--line);border-radius:12px}
th,td{text-align:left;padding:8px 12px;border-bottom:1px solid var(--line);white-space:nowrap}
th{font:600 11px/1 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
td.num{font-family:var(--mono);font-variant-numeric:tabular-nums}
.flags{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
.flag{background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--lic);border-radius:10px;padding:14px 16px;display:flex;flex-direction:column;gap:6px;min-width:0}
.flag.mid{border-left-color:var(--warn)}
@media (max-width:720px){.row{grid-template-columns:1fr}.clip{width:100%}}
@media (prefers-reduced-motion:no-preference){.clip{transition:border-color .15s}}
</style>''')
out.append('<div class="wrap">')
out.append('<header><span class="eyebrow">Immufix x Paula Radcliffe &middot; 8 vertical ads &middot; 30 Sep 2026</span>'
           '<h1>Immufix B-roll Pull List</h1>'
           '<p class="muted">External footage for the lines our own B-roll does not cover yet. Paula\'s real race archive first, then free stock per line, then what to shoot and what to check with compliance.</p>'
           '<div class="stats"><span><b>%d</b>open lines covered</span><span><b>%d</b>free clips ready to download (%d MB)</span><span><b>%d</b>free clips to grab by hand</span><span><b>%d</b>archive sources</span></div>'
           '<div class="legend">%s%s%s%s</div></header>' % (n_lines, len(free_ids), total_mb, len(MANUAL), len(ARCHIVE), pill('free'), pill('manual'), pill('licence'), pill('shoot')))

# archive
out.append('<section id="archive"><h2>Paula\'s race archive <small>needs clearance</small></h2>')
out.append('<div class="note"><p><b>This footage exists and looks great, but none of it is free to use in a paid ad.</b> Everything on Getty is marked editorial, and London Marathon Events Ltd says commercial use of marathon footage needs its prior written approval. I have not downloaded any of it.</p>'
           '<p>Fastest route: ask Paula\'s team first. She is a co-owner, so she may already hold personal archive and has direct contacts at London Marathon Events, British Athletics and the BBC. Then request commercial quotes from Getty ("contact us" on each clip) stating: paid social ads, UK, vertical crops, run length.</p>'
           '<p class="muted">Avoid entirely: the 2004 Athens drop-out, the 2005 London roadside moment, and any doping-story clips.</p></div>')
out.append('<div class="arch">')
for a in ARCHIVE:
    links = ''.join('<li><a href="%s" target="_blank" rel="noopener">%s</a></li>' % (E(u), E(t)) for t, u in a['links'])
    out.append('<div class="acard"><span class="prio">Priority: %s</span><h3>%s</h3><p>%s</p><p class="owner">Rights: %s</p><ul>%s</ul></div>' % (E(a['priority']), E(a['event']), E(a['why']), E(a['owner']), links))
out.append('</div></section>')

# per ad
out.append('<section id="ads"><h2>By ad <small>open lines only</small></h2>')
for name, seq, rows in ADS:
    out.append('<div class="ad"><h3>%s</h3><span class="seq">%s</span>' % (E(name), E(seq)))
    for tc, words, picks, note in rows:
        cards = ''.join(clip_card(k, r) for k, r in picks)
        out.append('<div class="row"><div><span class="tc">%s s</span><p class="words">&ldquo;%s&rdquo;</p>%s</div><div class="clips">%s</div></div>' % (
            E(tc), E(words), ('<p class="rnote">%s</p>' % E(note)) if note else '', cards))
    out.append('</div>')
out.append('</section>')

# shoot list
out.append('<section id="shoot"><h2>Shoot list <small>better than any stock</small></h2><div class="note">'
           '<p><b>The supplement shelf, before and after</b> (1 star reviews, also works for Ran professionally). One kitchen shelf crammed with 10 to 15 generic tubs and bottles, labels turned away. Then the same framing with only the Immufix pouch. Locked-off, vertical, 5 seconds each. No free library has this.</p>'
           '<p><b>Hands scooping Immufix into water, side light</b>, if you want a cleaner version of our C140 pour for the "one scoop" lines.</p></div></section>')

# compliance
out.append('<section id="compliance"><h2>Compliance flags <small>from your ASA note and the brief</small></h2><div class="flags">'
           '<div class="flag"><h3>Secret weapon</h3><p>The script runs illness (post viral fatigue) &rarr; Immufix &rarr; back to training &rarr; won the race. Your ASA note lists exactly that sequence as high risk, even for a true story. B-roll of illness or of the win would strengthen the implied claim. Worth a legal read before we add archive here.</p></div>'
           '<div class="flag mid"><h3>&ldquo;Under the weather, two scoops&rdquo;</h3><p>I picked rain on a window on purpose. Anything showing a sick person would read as a treatment claim.</p></div>'
           '<div class="flag mid"><h3>Absorption and immune lines</h3><p>&ldquo;Almost 100% ... taken into the cells&rdquo; (3 things) and the immune lines (I held the record) are strong claims. The brief says not to claim superior absorption without evidence. I left cell visuals as optional and kept virus-looking imagery out.</p></div>'
           '<div class="flag mid"><h3>Stock people</h3><p>The Pexels licence forbids implying the people shown endorse the product, or showing them in a bad light. Keep stock faces away from the pouch, and do not present the stock family as Paula\'s family.</p></div>'
           '</div></section>')

# downloads
rows = ''.join('<tr><td class="num">%s</td><td>%s</td><td class="num">%s</td><td class="num">%d MB</td></tr>' % (i, E(CLIPS[i][0]), CLIPS[i][1].replace('x', '&times;'), CLIPS[i][2]) for i in free_ids)
mrows = ''.join('<tr><td class="num"><a href="%s" target="_blank" rel="noopener">%s</a></td><td>%s</td></tr>' % (PX % i, i, E(d)) for i, d in MANUAL.items())
out.append('<section id="downloads"><h2>Downloads <small>all from Pexels, free licence</small></h2>'
           '<p>Pexels licence: free for commercial use, no credit needed, editing allowed. Not allowed: implying the people shown endorse the product, showing identifiable people in a bad light, or reselling the clips.</p>'
           '<h3>Ready for me to download (%d files, about %d MB)</h3><div class="tablewrap"><table><thead><tr><th>Pexels ID</th><th>Shot</th><th>File</th><th>Size</th></tr></thead><tbody>%s</tbody></table></div>'
           '<h3>Free, but grab from the page (%d clips)</h3><p class="muted">Newer Pexels uploads use unpredictable file names, and the clip pages sit behind a human check that I will not click through.</p>'
           '<div class="tablewrap"><table><thead><tr><th>Pexels ID</th><th>Shot</th></tr></thead><tbody>%s</tbody></table></div></section>' % (len(free_ids), total_mb, rows, len(MANUAL), mrows))
out.append('</div>')
open('Immufix_Broll_Pull_List.html', 'w', encoding='utf-8').write('\n'.join(out))
print('written', sum(len(x) for x in out) // 1024, 'KB;', len(free_ids), 'free files', total_mb, 'MB')
