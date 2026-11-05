"""Word view of every clip edge in a cut list, for setting tight edges fast (shorts, hooks, standalones).

    python -I edge_words.py CUT.txt PREPDIR [--fps 30]

For each clip prints the subtitle on screen at the in and out, the words around each edge, and a tight suggestion:
in = first word start - 0.04 s (never before the subtitle that carries it if a different subtitle shows before),
out = last word end + 0.2 s (capped 1 frame before the next subtitle and 0.05 s before the next word).
Words: subtitle-aligned (words_sub.json) inside subtitles, WhisperX outside them, words over 1.5 s ignored.
Flags: CENSOR (digital silence near the edge), COMMA (the line at the out goes on), DIGITS (word ends unreliable)."""
import json
import os
import re
import sys

import numpy as np


def load(prep):
    caps = json.load(open(os.path.join(prep, 'captions_exact.json'), encoding='utf-8'))
    ws = []
    for name in ('words_sub.json', 'words.json'):
        p = os.path.join(prep, name)
        if not os.path.exists(p):
            continue
        segs = json.load(open(p, encoding='utf-8'))['segments']
        got = [(w[0], w[1], w[2]) if isinstance(w, list) else (w.get('word'), w.get('start'), w.get('end'))
               for s in segs for w in s.get('words', [])]
        got = [w for w in got if w[1] is not None and w[2] is not None and w[2] - w[1] <= 1.5]
        if name == 'words.json':
            got = [w for w in got if not any(c['s'] - 0.2 < w[1] < c['e'] + 0.2 for c in caps)]
        ws += got
    ws.sort(key=lambda w: w[1])
    env = np.load(os.path.join(prep, 'env.npy')).astype(np.float32)
    raw = []
    p = os.path.join(prep, 'words.json')
    if os.path.exists(p):
        segs = json.load(open(p, encoding='utf-8'))['segments']
        raw = [(w[0], w[1], w[2]) if isinstance(w, list) else (w.get('word'), w.get('start'), w.get('end'))
               for s in segs for w in s.get('words', [])]
        raw = sorted(w for w in raw if w[1] is not None and w[2] is not None and w[2] - w[1] <= 1.5)
    return caps, ws, env, raw


def sub_at(caps, t):
    for c in caps:
        if c['s'] - 1e-3 <= t < c['e']:
            return c
    return None


def mutes(env, a, b):
    x = env[max(0, int(a * 100)):int(b * 100)]
    return [round(a + i / 100, 2) for i in range(len(x)) if x[i] < -90 and (i == 0 or x[i - 1] >= -90)]


def main():
    cut, prep = sys.argv[1], sys.argv[2]
    fps = float(sys.argv[sys.argv.index('--fps') + 1]) if '--fps' in sys.argv else 30.0
    caps, ws, env, raw = load(prep)
    part = None
    for ln in open(cut, encoding='utf-8'):
        s = ln.strip()
        if s in ('[hook]', '[story]'):
            part = s[1:-1]
            continue
        m = re.match(r'^([eh]:)?([\d.]+) > ([eh]:)?([\d.]+)', s)
        if not m or not part:
            continue
        a, b = float(m.group(2)), float(m.group(4))
        note = s.split('|', 1)[1].strip()[:60] if '|' in s else ''
        print(f'== {part} {a:.2f} > {b:.2f}  {note}')
        # in side
        first = next((w for w in ws if w[2] > a + 0.03), None)
        prev = [w for w in ws if w[2] <= a + 0.03 and w[2] > a - 1.0]
        ci, cp = sub_at(caps, a), sub_at(caps, a - 1 / fps)
        sug_in = first[1] - 0.04 if first else a
        if first and ci and cp and ci is not cp and sug_in < ci['s']:
            sug_in = ci['s']  # the line before would flash: start on the subtitle switch
        nxt_sub = next((c for c in caps if c['s'] > a + 1e-3), None)
        if first and first[1] > (nxt_sub['s'] if nxt_sub else 1e9):
            sug_in = max(sug_in, nxt_sub['s'])
        flags = []
        if mutes(env, a - 0.3, a + 0.3):
            flags.append('CENSOR near in')
        print(f"   IN  sub [{ci['text'][:40] + ' %.3f-%.3f' % (ci['s'], ci['e']) if ci else '-'}]  "
              f"prev word: {prev[-1][0] + '@%.2f-%.2f' % prev[-1][1:] if prev else '-'}  "
              f"first word: {first[0] + '@%.2f-%.2f' % first[1:] if first else '-'}  -> tight in {sug_in:.2f} {' '.join(flags)}")
        # out side
        last = [w for w in ws if w[1] < b - 0.03]
        last = last[-1] if last else None
        nw = next((w for w in ws if w[1] >= b - 0.03), None)
        co = sub_at(caps, b - 1 / fps)
        ns = next((c for c in caps if c['s'] > b - 1 / fps + 1e-3), None)
        sug_out = last[2] + 0.2 if last else b
        if nw:
            sug_out = min(sug_out, nw[1] - 0.05)
        if ns and co is not ns:
            sug_out = min(sug_out, ns['s'] - 0.5 / fps)
        flags = []
        if co and co['text'].rstrip().endswith(','):
            flags.append('COMMA: line goes on')
        if co and any(ch.isdigit() for ch in co['text']):
            flags.append('DIGITS')
        if mutes(env, b - 0.3, b + 0.3):
            flags.append('CENSOR near out')
        print(f"   OUT sub [{co['text'][:40] + ' %.3f-%.3f' % (co['s'], co['e']) if co else '-'}]  "
              f"last word: {last[0] + '@%.2f-%.2f' % last[1:] if last else '-'}  "
              f"next word: {nw[0] + '@%.2f-%.2f' % nw[1:] if nw else '-'}  "
              f"next sub @{ns['s']:.3f}" if ns else '', end='')
        print(f"  -> tight out {sug_out:.2f} {' '.join(flags)}")
        # 14 Oct: subtitles can END BEFORE the voice (and start after it): check the raw ASR words across both edges
        cross_out = [w for w in raw if w[1] < b - 0.05 and w[2] > b + 0.08]
        after = [w for w in raw if b - 0.05 <= w[1] < b + 0.25]
        cross_in = [w for w in raw if w[1] < a - 0.08 and w[2] > a + 0.05]
        cross_out = [w for w in cross_out if w[2] - w[1] <= 1.0]  # ASR smears shouted words over 1 s: ignore those
        if cross_out:
            print('   !! CUT INSIDE A WORD at the out (raw ASR): ' + ' '.join(f'{w[0]}@{w[1]:.2f}-{w[2]:.2f}' for w in cross_out[:3]))
        elif after:
            print('   .. next raw word starts right after the out: ' + ' '.join(f'{w[0]}@{w[1]:.2f}-{w[2]:.2f}' for w in after[:2]))
        cross_in = [w for w in cross_in if w[2] - w[1] <= 1.0]
        if cross_in:
            print('   !! CUT INSIDE A WORD at the in (raw ASR): ' + ' '.join(f'{w[0]}@{w[1]:.2f}-{w[2]:.2f}' for w in cross_in[:3]))
        # pauses inside the clip (review 4: hooks and shorts keep no pause over about 0.3 s)
        inner = [w for w in ws if w[1] >= a - 0.05 and w[2] <= b + 0.05]
        gaps = [(p[2], q[1]) for p, q in zip(inner, inner[1:]) if q[1] - p[2] > 0.35]
        if gaps:
            print('   PAUSES inside: ' + ' '.join(f'{x:.2f}-{y:.2f}({y - x:.1f})' for x, y in gaps))


if __name__ == '__main__':
    main()
