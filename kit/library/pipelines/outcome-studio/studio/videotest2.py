"""videotest2: render the photo-based footage formats with sound effects (P&L edit, hot take)."""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ocdata as od, formats as fm, motion as mo, traders as tr, sfx
from render import Studio
from videotest import strip

OUT = os.path.join(od.ROOT, 'out', '_selftest')
PHOTO = os.path.join(od.ROOT, 'footage', 'wcfinal_tsn_1.jpg')


def render_with_sound(st, p, f, hold=1.5):
    v = p['video']
    info = st.show(v, (1080, 1920)) or {}
    dur = (info.get('dur') or 8) + hold
    wav = sfx.mix(sfx.cues_for(v, lead=v.get('lead', .5)), dur, f.replace('.mp4', '.wav'))
    st.video(v, f, (1080, 1920), dur=dur, audio=wav)
    return strip(f, f.replace('.mp4', '_strip.jpg'), n=7, w=200)


if __name__ == '__main__':
    ms = od.markets()
    card, info = tr.pnl_card('trader-J', coin='#2120', hours=24 * 100, ms=ms)
    print({k: info.get(k) for k in ('title', 'label', 'bought', 'avg', 'payout', 'profit')})
    card = dict(card, title='2026 WORLD CUP CHAMPION', side='SPAIN')
    pe = mo.pnl_edit(ms, still=PHOTO, move={'x0': .6, 'x1': .64, 'z0': 1.0, 'z1': 1.18}, card=card, dur=7, pid='pnl_edit_wc')
    bdo = next(m for m in ms if m['kind'] == 'winner' and 'Ballon' in m['title'])
    kane = next(r for r in bdo['outcomes'] if r['label'] == 'Harry Kane'); yamal = next(r for r in bdo['outcomes'] if r['label'] == 'Lamine Yamal')
    ht = mo.hottake(ms, still=PHOTO, move={'x0': .3, 'x1': .63, 'z0': 1.0, 'z1': 1.1}, lines=['Yamal is the', '*best player*', 'on the planet'],
                    receipt={'kicker': 'Receipt', 'title': "The money's *Ballon d'Or*", 'rows': [{'label': 'Harry Kane', 'team': fm.person('Harry Kane'), 'p': kane['p']},
                             {'label': 'Lamine Yamal', 'team': fm.person('Lamine Yamal'), 'p': yamal['p']}], 'note': 'Ceremony on *26 Oct*. Who wins it?'},
                    dur=9, cut=3.4, pid='hottake_yamal')
    with Studio(fm.brand()) as st:
        for p in (pe, ht):
            t0 = time.time(); print(render_with_sound(st, p, os.path.join(OUT, p['id'] + '.mp4')), '%.0fs' % (time.time() - t0))
