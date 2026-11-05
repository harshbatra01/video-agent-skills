"""howto: the client's How-to carousel from REAL outcome.xyz screens (home, a market page, the YES/NO buttons).

python howto.py capture [market path]     fresh screenshots + element positions -> out/captures/howto_*.png, howto_pos.json
Then the "howto" recipe in a batch builds 5 slides: hook, find a market, make the call, payout, CTA.
Text boxes are TikTok-style (white box, black text). Arrows and circles point at real UI; nothing on the UI is changed or covered
except where a text box sits over empty space (never over the chart, the names or the Outcome logo).
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ocdata as od, formats as fm
from render import Studio, file_url
from capture import Capture

ROOT = od.ROOT
CAP = os.path.join(ROOT, 'out', 'captures')
FIND_JS = r"""((reText, sel) => { const re = new RegExp(reText);
  const e = [...document.querySelectorAll(sel || '*')].filter(e => re.test((e.textContent || '').trim()))
           .sort((a, b) => (a.textContent || '').length - (b.textContent || '').length)[0];
  if (!e) return null; const r = e.getBoundingClientRect(); return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)]; })"""


def find(st, pattern, sel='*'):
    return st.js('%s(%s, %s)' % (FIND_JS, json.dumps(pattern), json.dumps(sel)))


def capture(market='/markets/sports/q422'):
    os.makedirs(CAP, exist_ok=True); pos = {}
    with Studio(fm.brand()) as st:
        c = Capture(st)
        c.open('https://outcome.xyz/', h=1100, wait=6); c.clean()
        pos['home'] = {'payout': find(st, r'^\$100 → \$[0-9,]+$', 'span,div,p'), 'sports': find(st, r'^Sports$', 'a,button,span,div'),
                       'rewards': find(st, r'TRADE TO\s*EARN', 'div,span,p')}
        c.shot(os.path.join(CAP, 'howto_home.png'))
        c.open('https://outcome.xyz' + market, h=1100, wait=6); c.clean()
        pos['market'] = {'yes': find(st, r'^YES', 'button'), 'no': find(st, r'^NO', 'button'), 'title': find(st, r'^UCL:', 'h1,h2,div,span'),
                         'text': (st.js('document.body.innerText') or '')[:300]}
        c.shot(os.path.join(CAP, 'howto_market.png'))
        b = pos['market'].get('yes')
        if b:
            st.js("(() => { const b=[...document.querySelectorAll('button')].find(e=>/^YES/.test((e.textContent||'').trim())); if(b) b.click(); return !!b })()")
            time.sleep(3)
            pos['ticket'] = {'text': (st.js('document.body.innerText') or '')[:500], 'dialog': st.js("!!document.querySelector('[role=dialog]')"),
                             'amount': find(st, r'^Amount$', 'div,span,p,label'), 'payout': find(st, r'^(To win|Payout|Potential payout)', 'div,span,p')}
            c.shot(os.path.join(CAP, 'howto_ticket.png'))
            # a realistic amount (the client rule: $1,000 or less): press +100 and read the payout the app shows
            st.js("(() => { const b=[...document.querySelectorAll('button')].find(e=>(e.textContent||'').trim()==='+100'); if(b) b.click(); return !!b })()")
            time.sleep(2.5)
            pos['ticket100'] = {'text': (st.js("(() => { const d=document.querySelector('[role=dialog]'); return d ? d.innerText : '' })()") or '')[:600],
                                'amount': find(st, r'^\$100(\.00)?$', 'div,span,p,input'), 'payout': find(st, r'(To win|Payout|payout)', 'div,span,p')}
            c.shot(os.path.join(CAP, 'howto_ticket100.png'))
    pos['made'] = time.strftime('%Y-%m-%d %H:%M')
    json.dump(pos, open(os.path.join(CAP, 'howto_pos.json'), 'w'), indent=1)
    return pos


def build(ms=None, market_key='Q422', pid='howto'):
    """5 slides from the last capture (run `python howto.py capture` first, same market)"""
    import re
    pos = json.load(open(os.path.join(CAP, 'howto_pos.json'), encoding='utf-8'))
    ms = ms or od.markets()
    m = next((x for x in ms if x['key'] == market_key), None)
    home = m['outcomes'][0] if m else None
    t100 = (pos.get('ticket100') or {}).get('text', '')
    pay = re.search(r'Payout\s*\|?\s*\$([0-9,.]+)', t100.replace('\n', ' | '))
    shares = re.search(r'([0-9,]+) Yes', t100)
    team_short = fm.team(home['label'])['short'] if home else 'your team'
    pct = '%d%%' % round(100 * home['p']) if home else ''
    url = lambda f: file_url(os.path.join(CAP, f))
    yes, no = (pos.get('market') or {}).get('yes'), (pos.get('market') or {}).get('no')
    payrow = (pos.get('ticket100') or {}).get('payout')
    slides = [
        {'fmt': 'howto', 'img': url('howto_market.png'), 'y0': 58, 'boxes': [{'lines': ['How to make your', 'first call on Outcome.xyz']}]},
        {'fmt': 'howto', 'img': url('howto_home.png'), 'y0': 40, 'step': '1',
         'boxes': [{'lines': ['Find a market you know']}, {'lines': [{'t': 'Pick an event you understand and read its rules', 'size': 40}]}],
         'arrows': [[230, 300, 76, 112, -70]]},
        {'fmt': 'howto', 'img': url('howto_market.png'), 'focus': (yes or [0, 1015])[1], 'focusAt': .8, 'step': '2', 'maxY': 1100,
         'circles': [c for c in (yes, no) if c], 'boxes': [{'lines': ['Think %s win? Buy YES' % team_short, "Think they won't? Buy NO"]}]},
        {'fmt': 'howto', 'img': url('howto_ticket100.png'), 'focus': (payrow or [0, 971])[1], 'focusAt': .72, 'step': '3', 'maxY': 1100,
         'circles': [[18, (payrow or [0, 971])[1] - 14, 354, 58, '#7CFFB2']] if payrow else [],
         'boxes': [{'lines': ['$100 on %s at %s' % (team_short, pct), 'pays $%s if they win' % (pay.group(1) if pay else '?')]}]},
        {'fmt': 'howto', 'img': url('howto_home.png'), 'y0': 30, 'glow': 'cyan',
         'boxes': [{'lines': ['Ready to make your call?', 'Trade with zero fees on outcome.xyz']}]},
    ]
    for s in slides:
        s['boxes'] = [b for b in s['boxes'] if b['lines']]
    cap = ('How to make your first call on Outcome \U0001F447\n\n1. Find a market you know\n2. Think it happens? Buy YES. Think it won\'t? Buy NO\n'
           '3. $100 on %s at %s pays $%s if they win (from the app, %s)\n\n%s' % (team_short, pct, pay.group(1) if pay else '?', pos.get('made', ''), fm.risk_line()))
    return fm._post(pid, 'howto', 'How to make your first call', slides, cap, notes='Screens captured %s. Re-run `python howto.py capture` before posting.' % pos.get('made', ''))


if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'capture':
        print(json.dumps(capture(*(a[1:2] or [])), indent=1)[:1500])
    else:
        print(__doc__)
