"""Cut on the audio, not on speech-to-text times: snap cut points, clean voice-over edges, edge scan, restart flags.

Whisper word starts land 0.1-1.0 s early or late (often inside the pause before the word), so B-roll cut on raw
Whisper times looked "not cut properly and not synced" to the user. Every edge here comes from the audio.

Default: ABSOLUTE levels, the clean voice-over rules measured on a reviewer's own fixes of a quiet narrator recording.
  level     dBFS RMS in 10 ms windows of the loudest channel of the RAW file (before any clip gain; the loudest channel
            because a voice recorded on one side reads 6 dB low in a mono mix)
  -70 dB    a word's soft tail and soft onset run down to here; room noise (about -72 to -80 dB) is dead air
  start     1-2 frames before the first frame at -70 dB or louder (a soft "s" rising out of the floor stays)
  end       about 3 frames after the last frame at -70 dB or louder (at most 5), stopping short of any new sound
  consonant a bump after a short silence INSIDE the last word ("stan-d", "secon-ds") is part of the word: kept
  breath    a separate soft bump (peak under -55 dB) after a 50 ms dip, OUTSIDE the words: cut at both ends, even at
            -58 to -70 dB. Without a transcript a soft edge bump is kept and flagged (it may be a consonant).
  -55 dB    edge scan: no cut edge may have audio over -55 dB on BOTH sides (that edge chops a sound). It must find nothing.
  restarts  phrases that begin like the phrase before ("Gen Z won't- Gen Z won't"), words repeated back to back,
            cut-off words, words stretched over 0.8 s and speech with no transcript words are flagged. A whole-file
            transcript merges restarts: transcribe each piece on its own (--wav-dir) on narrator recordings.
--rel: the older RELATIVE rule. The snap modes (phrase@after, --at) then give exactly the old output: a pause is 80 ms
  quieter than the local floor + 10 dB, cut 50 ms before speech resumes. The voice-over modes measure every level from
  the recording's own floor instead (edge = floor + 10 dB, the other levels keep their spacing). Use it on noisy field
  audio (dashcam, street, events), where the floor sits far above -70 dB; the tool warns when it does.

usage:
  python speech_cuts.py MEDIA WORDS.json "phrase@after" ...   cut time where the sentence starting with phrase begins
                                                               (searched from 'after' seconds on)
  python speech_cuts.py MEDIA --at 12.4 15.9 ...               snap raw times to where speech resumes
  python speech_cuts.py MEDIA --keep 12.0-15.5 20.1-24.0 ...   clean in/out for phrases you keep. With --words WORDS.json
                                                               each range is read through its own words: the sound
                                                               pieces holding them are kept whole (also past the range
                                                               when the transcript ends a phrase early), other phrases'
                                                               sounds and breaths at the edges are left out. Without
                                                               words the sound inside each range is used as given.
  python speech_cuts.py MEDIA --scan 12.03-15.63 ...           edge scan of a cut list (or --scan CUTS.json)
  python speech_cuts.py MEDIA [WORDS.json] --phrases           every phrase: clean in/out, text, flags, edge scan
options: --rel   --fps 30 (frame grid for in/out)   --edge -70   --loud -55   --json OUT.json (--keep, --phrases)
         --wav-dir DIR (--phrases: writes each piece as a WAV to transcribe on its own with hear.py; run again with
         the same DIR once the .json files are there, and the restart checks use those texts)
WORDS.json = hear.py output ({"words": [{"s", "e", "w", "p"}]}). Times are seconds in the media file.
CUTS.json = [[in, out], ...] or [{"in": s, "out": s}, ...] (the --json output of --keep or --phrases works).
Exit code 1 when the edge scan finds a problem (--scan, --keep, --phrases). Check a few cuts by ear before building.
"""
import sys, os, json, re, math, wave
import numpy as np

HOP = 0.005          # relative envelope (the older rule)
AHOP = 0.01          # absolute levels: 10 ms windows
EDGE, LOUD = -70.0, -55.0
FLOOR_WARN, QUIET_WARN = -65.0, -45.0


def envelope(path, sr=16000):
    """5 ms RMS envelope in dB with 20 ms smoothing (PyAV decode, mono)"""
    import av
    out = []
    with av.open(path) as c:
        rs = av.AudioResampler(format='s16', layout='mono', rate=sr)
        for f in c.decode(audio=0):
            for g in rs.resample(f): out.append(g.to_ndarray().reshape(-1))
        for g in rs.resample(None): out.append(g.to_ndarray().reshape(-1))
    x = np.concatenate(out).astype(np.float32) / 32768
    hop = int(sr * HOP); n = len(x) // hop
    env = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
    return np.convolve(env, np.ones(4) / 4, mode='same')


def snap(env, pred):
    i0, i1 = max(0, int((pred - 0.5) / HOP)), int((pred + 0.8) / HOP)
    seg = env[i0:i1]
    floor = np.percentile(env[max(0, int((pred - 6) / HOP)):int((pred + 6) / HOP)], 10)
    quiet = seg < floor + 10
    runs, st = [], None
    for k, q in enumerate(quiet):
        if q and st is None: st = k
        if (not q or k == len(quiet) - 1) and st is not None:
            e = k if not q else k + 1
            if (e - st) * HOP >= 0.08: runs.append((st, e))
            st = None
    if runs:
        st, e = min(runs, key=lambda r: abs((i0 + r[1]) * HOP - (pred + 0.15)))
        return round((i0 + e) * HOP - 0.05, 3), 'pause'
    lo, hi = max(0, int((pred - 0.3) / HOP) - i0), int((pred + 0.4) / HOP) - i0
    k = lo + int(np.argmin(seg[lo:hi]))
    return round((i0 + k) * HOP, 3), 'dip'


def norm(s): return re.sub(r"[^a-z0-9']", '', s.lower())


def phrase_time(words, phrase, after):
    ws = [norm(x) for x in phrase.split()]
    for i, w in enumerate(words):
        if w['s'] < after - 0.5: continue
        if all(i + j < len(words) and norm(words[i + j]['w']) == ws[j] for j in range(len(ws))): return w['s']
    raise KeyError('phrase not found: %s after %.1f' % (phrase, after))


# ------------------------------------------------------------------ absolute levels (the voice-over rules)
def levels(path):
    """dBFS RMS per 10 ms window of the loudest channel, from the raw file at its own sample rate (no gain)"""
    import av
    out, carry = [], None
    with av.open(path) as c:
        st = c.streams.audio[0]
        sr = st.rate or st.codec_context.sample_rate or 48000
        if sr % 100: sr = 48000                       # a 10 ms window must hold a whole number of samples
        hop = sr // 100
        rs = av.AudioResampler(format='fltp', rate=sr)   # float planes, the file's own channels

        def eat(g):
            nonlocal carry
            a = g.to_ndarray().astype(np.float64)
            if carry is not None and carry.shape[1]: a = np.concatenate([carry, a], axis=1)
            n = a.shape[1] // hop
            if n: out.append((a[:, :n * hop].reshape(a.shape[0], n, hop) ** 2).mean(2).max(0))
            carry = a[:, n * hop:]
        for f in c.decode(audio=0):
            for g in rs.resample(f): eat(g)
        for g in rs.resample(None): eat(g)
    ms = np.concatenate(out) if out else np.zeros(0)
    return np.maximum(10 * np.log10(ms + 1e-12), -120.0)


def thresholds(db, rel=False, edge=None, loud=None):
    """the four levels every rule uses. Absolute: edge -70, sound -60 (a phrase's real sound), gap -65 (the dip
    between a word and a breath), loud -55. --rel: the same spacing from the recording's floor (edge = floor + 10).
    The floor is the 10th percentile of the windows that are not digital silence."""
    live = db[db > -110] if len(db) else db
    floor = float(np.percentile(live, 10)) if len(live) else -120.0
    e = edge if edge is not None else (floor + 10 if rel else EDGE)
    lo = loud if loud is not None else e + (LOUD - EDGE)
    return dict(edge=e, sound=e + 10, gap=e + 5, loud=lo, floor=floor,
                speech=float(np.percentile(db, 95)) if len(db) else -120.0, rel=rel)


def _runs(mask):
    """[(start, end)] of the True runs of a boolean array (end exclusive)"""
    m = np.concatenate([[0], np.asarray(mask, dtype=np.int8), [0]])
    d = np.diff(m)
    return [(int(a), int(b)) for a, b in zip(np.where(d == 1)[0], np.where(d == -1)[0])]


def _rise(db, k, stop, step, E):
    """walk from a phrase's first (step -1) or last (step +1) real sound outwards through its soft rise or decay at the
    edge level or above, at most to index `stop`. Reaching the floor (under E) ends it there: returns (k, True). A level
    4 dB over the lowest one passed is a separate sound (a breath, a click, the next word) joined by a dip that never
    reached the floor, and running into the limit means the same: the edge is then the dip's quietest point (k, False)."""
    m, kmin = db[k], k
    while 0 <= k + step < len(db) and (k + step - stop) * step <= 0:
        j = k + step
        if db[j] < E: return k, True
        if db[j] > m + 4: return kmin, False
        k = j
        if db[k] < m: m, kmin = db[k], k
    if not 0 <= k + step < len(db): return k, True      # the file starts or ends here
    return kmin, False


def clean_edges(db, a, b, th, fps=30.0, words=(), lo_lim=None, hi_lim=None):
    """clean in/out for one phrase whose sound lies inside [a, b] (source seconds), on the fps frame grid.
    words = that phrase's transcript words (they decide breath vs final consonant). lo_lim / hi_lim: never cut past
    these (the neighbours). Returns dict(in, out, in_f, out_f, first, last, notes) or None when [a, b] holds no sound."""
    E, S, G, Lo = th['edge'], th['sound'], th['gap'], th['loud']
    n = len(db)
    i0, i1 = max(0, int(a / AHOP)), min(n, int(math.ceil(b / AHOP)))
    if i1 <= i0: return None
    snd = np.where(db[i0:i1] > S)[0]
    if not len(snd): return None
    f0, f1, notes = i0 + int(snd[0]), i0 + int(snd[-1]), []
    ws = int((min(w['s'] for w in words) - 0.10) / AHOP) if words else None
    we = int((max(w['e'] for w in words) + 0.10) / AHOP) if words else None
    while True:                                     # leading soft bumps: a breath before the words?
        q = f0
        while q < f1 and db[q] > G: q += 1
        gap0 = q
        while q < f1 and db[q] <= G: q += 1
        if q >= f1 or q - gap0 < 5: break
        pk = db[f0:gap0].max()
        if pk >= Lo:                                # loud: never cut by rule; a short one outside the words may be a click
            if gap0 - f0 < 8 and (ws is None or gap0 <= ws):
                notes.append('short loud sound at %.2f s (peak %.0f dB, %d ms) before the words: a click? kept, listen'
                             % (f0 * AHOP, pk, (gap0 - f0) * 10))
            break
        if ws is None or gap0 > ws:
            notes.append('soft sound before the words at %.2f s (peak %.0f dB): breath? kept, listen' % (f0 * AHOP, pk))
            break
        notes.append('breath cut at %.2f s (peak %.0f dB)' % (f0 * AHOP, pk))
        f0 = q + int(np.argmax(db[q:f1 + 1] > S))
    while True:                                     # trailing soft bumps: final consonant (inside the word) or breath?
        q = f1
        while q > f0 and db[q] > G: q -= 1
        gap1 = q
        while q > f0 and db[q] <= G: q -= 1
        if q <= f0 or gap1 - q < 5: break
        pk = db[gap1 + 1:f1 + 1].max()
        if pk >= Lo:                                # loud: a final consonant or another word; a short one after the words: a click?
            if f1 - gap1 < 8 and (we is None or gap1 >= we):
                notes.append('short loud sound at %.2f s (peak %.0f dB) after %s: a click%s? kept, listen'
                             % ((gap1 + 1) * AHOP, pk, 'a gap' if we is None else 'the words',
                                ' or final consonant' if we is None else ''))
            break
        if we is None:
            notes.append('soft sound after a gap at %.2f s (peak %.0f dB): final consonant or breath? kept, listen'
                         % ((gap1 + 1) * AHOP, pk))
            break
        if gap1 < we: break                         # inside the last word: its final consonant stays
        notes.append('breath cut at %.2f s (peak %.0f dB)' % ((gap1 + 1) * AHOP, pk))
        f1 = q
    lo = max(f0 - 15, 0)                            # at most 0.15 s of soft rise
    if lo_lim is not None: lo = max(lo, int(math.ceil(lo_lim / AHOP)))
    k0, floor0 = _rise(db, f0, min(lo, f0), -1, E)
    hi = min(f1 + 35, n - 1)                        # at most 0.35 s of decay
    if hi_lim is not None: hi = min(hi, int(hi_lim / AHOP) - 1)
    k1, floor1 = _rise(db, f1, max(hi, f1), +1, E)
    first, last = k0 * AHOP, (k1 + 1) * AHOP
    if floor0:                                      # 1 to 2 frames before the first frame at the edge level
        fi = int(math.floor((first - 1.5 / fps) * fps + 1e-6))
        pre = db[max(0, int(fi / fps / AHOP)):k0]
        if len(pre) and pre.max() > G:              # another sound inside that handle: start on the onset's own frame
            fi = int(math.floor(first * fps + 1e-6)); notes.append('tight start: a sound ends just before it')
    else:                                           # joined to a sound before by a dip: cut at the dip's quietest point
        fi = int(round((first + AHOP / 2) * fps))
        notes.append('start cut in a dip at %.2f s (%.0f dB): no quiet floor before it' % (first, db[k0]))
    if floor1:                                      # about 3 frames of handle after the last frame at the edge level...
        m = int(round(3.0 / fps / AHOP))
        nxt = np.where(db[k1 + 1:min(n, k1 + 1 + m)] > G)[0]
        if len(nxt):                                # ...stopping short of a new sound
            fo = max(int(math.ceil(last * fps - 1e-6)), int(math.floor((k1 + 1 + int(nxt[0])) * AHOP * fps + 1e-6)))
        else:
            fo = int(math.ceil((last + 3.0 / fps) * fps - 1e-6))
    else:
        last = k1 * AHOP + AHOP / 2
        fo = int(round(last * fps))
        notes.append('end cut in a dip at %.2f s (%.0f dB): no quiet floor after it' % (last, db[k1]))
    if lo_lim is not None: fi = max(fi, int(math.ceil(lo_lim * fps - 1e-6)))
    if hi_lim is not None: fo = min(fo, int(math.floor(hi_lim * fps + 1e-6)))
    fi = max(fi, 0); fo = max(fo, fi + 1)
    return {'in': round(fi / fps, 3), 'out': round(fo / fps, 3), 'in_f': fi, 'out_f': fo, 'first': round(first, 3),
            'last': round(last, 3), 'notes': notes}


def snap_abs(db, pred, th, fps=30.0):
    """picture cut for a predicted sentence start, absolute rule: the next speech after a real pause (80 ms under the
    edge level; soft bumps under 'loud' in it are breaths, not speech), 1.5 frames before its first sound"""
    E, S, G, Lo = th['edge'], th['sound'], th['gap'], th['loud']
    n = len(db)
    i0, i1 = max(0, int((pred - 0.5) / AHOP)), min(n, int((pred + 0.8) / AHOP))
    cands = set()
    for a, b in _runs(db[i0:i1] < E):
        if b - a < 8: continue
        k, lim = i0 + b, min(n, i0 + b + 100)
        while k < lim:                              # skip breaths: the first bump that reaches 'loud' is speech
            if db[k] > S:
                e = k
                while e < n and db[e] > G: e += 1
                if db[k:e].max() >= Lo: break
                k = e
            else:
                k += 1
        if k < lim:
            k0, fl = _rise(db, k, max(i0 + a, k - 15), -1, E)
            cands.add(round(max(0.0, k0 * AHOP - 1.5 / fps) if fl else k0 * AHOP + AHOP / 2, 3))
    if cands:
        return min(cands, key=lambda c: abs(c - (pred + 0.15))), 'pause'
    lo, hi = max(0, int((pred - 0.3) / AHOP)), min(n, int((pred + 0.4) / AHOP))
    if hi <= lo: return round(pred, 3), 'dip'
    return round((lo + int(np.argmin(db[lo:hi]))) * AHOP, 3), 'dip'


def edge_scan(db, cuts, th):
    """cuts = [(in, out)] in source seconds, in timeline order. An edge with audio over th['loud'] on BOTH sides chops a
    sound. Windows: 80 ms dropped / first 50 ms kept at an in point, last 50 ms kept / 80 ms dropped at an out point.
    Cuts that join seamlessly in the source (out == next in) make no edge there."""
    def lvl(t0, t1):
        s = db[max(0, int(round(t0 / AHOP))):max(0, int(round(t1 / AHOP)))]
        return float(s.max()) if len(s) else -120.0
    Lo, probs = th['loud'], []
    for k, (a, b) in enumerate(cuts):
        if not (k and abs(cuts[k - 1][1] - a) < 0.001):
            x, y = lvl(a - 0.08, a), lvl(a, a + 0.05)
            if x > Lo and y > Lo: probs.append(('START', k, a, x, y))
        if not (k + 1 < len(cuts) and abs(cuts[k + 1][0] - b) < 0.001):
            x, y = lvl(b - 0.05, b), lvl(b, b + 0.08)
            if x > Lo and y > Lo: probs.append(('END', k, b, x, y))
    return probs


def pieces(db, th, split=0.18, fill=0.20, minlen=0.08, i0=0, i1=None):
    """phrase pieces from the audio: sound over th['sound'], split where nothing reaches that level for more than
    0.20 s (a pause, even with a soft breath in it) or where it stays 2 dB under it for 0.18 s or more (pieces shorter
    than 0.08 s, clicks, are dropped). i0 / i1 limit the search to those 10 ms windows."""
    seg = db[i0:i1]
    idx = np.where(seg > th['sound'])[0]
    if not len(idx): return []
    need, gap, out, s, p = int(round(split / AHOP)), int(round(fill / AHOP)), [], int(idx[0]), int(idx[0])
    for i in idx[1:]:
        i = int(i)
        if i - p > 1:
            r = _runs(seg[p + 1:i] < th['sound'] - 2)
            if i - p - 1 > gap or (r and max(e - a for a, e in r) >= need): out.append((s, p + 1)); s = i
        p = i
    out.append((s, p + 1))
    return [((a + i0) * AHOP, (b + i0) * AHOP) for a, b in out if (b - a) * AHOP >= minlen]


def keep_span(db, a, b, th, own, other):
    """what a --keep range stands for, read from the transcript: every sound piece (split at real pauses) that holds one
    of the range's own words, first to last, even where a piece runs past the range (Whisper starts or ends a phrase
    early or late). Pieces at the edges that hold only other phrases' words, or only a breath, are left out.
    Returns (A, B, lo_lim, hi_lim, notes) for clean_edges."""
    sp = pieces(db, th, minlen=0.0, i0=max(0, int((a - 1.5) / AHOP)), i1=min(len(db), int((b + 1.5) / AHOP)))
    if not sp: return a, b, None, None, []
    short = lambda k: sp[k][1] - sp[k][0] < 0.08          # a click or a short noise, never grown into
    lab = [set() for _ in sp]
    for w, mine in [(w, True) for w in own] + [(w, False) for w in other if w['e'] > a - 2 and w['s'] < b + 2]:
        k, ov = max(((k, min(y, w['e']) - max(x, w['s'])) for k, (x, y) in enumerate(sp)), key=lambda t: t[1])
        if ov > -0.3: lab[k].add(mine)
    ownk = [k for k in range(len(sp)) if True in lab[k]]
    if not ownk: return a, b, None, None, ["none of this range's words sit on a sound: the range is used as given"]
    pk = lambda k: float(db[int(sp[k][0] / AHOP):int(math.ceil(sp[k][1] / AHOP))].max())
    k0, k1, notes = ownk[0], ownk[-1], []
    while k0 > 0 and not lab[k0 - 1] and not short(k0 - 1) and pk(k0 - 1) >= th['loud'] and sp[k0 - 1][0] >= a:
        k0 -= 1; notes.append('kept %.2f-%.2f s: speech-level sound with no transcript words, inside the range' % sp[k0])
    while k1 + 1 < len(sp) and not lab[k1 + 1] and not short(k1 + 1) and pk(k1 + 1) >= th['loud'] and sp[k1 + 1][1] <= b:
        k1 += 1; notes.append('kept %.2f-%.2f s: speech-level sound with no transcript words, inside the range' % sp[k1])
    A, B = sp[k0][0], sp[k1][1]
    lo_lim = sp[k0 - 1][1] + 0.02 if k0 > 0 else None
    hi_lim = sp[k1 + 1][0] - 0.02 if k1 + 1 < len(sp) else None
    mid = lambda w: (w['s'] + w['e']) / 2
    w_first, w_last = min(own, key=lambda w: w['s']), max(own, key=lambda w: w['e'])
    before = [w for w in other if w['s'] < w_first['s'] and w['e'] > sp[k0][0] - 0.3]
    after = [w for w in other if w['s'] > w_last['s'] and w['s'] < sp[k1][1] + 0.3]
    if False in lab[k0] and before:                 # no pause before this phrase: the quietest point between the words
        w1 = max(before, key=lambda w: w['s'])
        A = lo_lim = _quietest(db, mid(w1), mid(w_first))
        notes.append('no pause before it: cut at the quietest point after "%s" (%.2f s, %.0f dB)' % (w1['w'], A, db[int(A / AHOP)]))
    if False in lab[k1] and after:
        w2 = min(after, key=lambda w: w['s'])
        B = hi_lim = _quietest(db, mid(w_last), mid(w2))
        notes.append('no pause after it: cut at the quietest point before "%s" (%.2f s, %.0f dB)' % (w2['w'], B, db[int(B / AHOP)]))
    if A < a - 0.05: notes.append('followed the sound back to %.2f s, before the range start' % A)
    if B > b + 0.05: notes.append('followed the sound on to %.2f s, past the range end (the transcript ended it early)' % B)
    for k in list(range(k0)) + list(range(k1 + 1, len(sp))):
        x, y = sp[k]
        if y > a and x < b:
            notes.append('left out %.2f-%.2f s inside the range: %s' % (x, y, 'another phrase' if lab[k] else
                         'a click or short noise' if short(k) else 'breath or noise' if pk(k) < th['loud'] else
                         'speech with no transcript words, listen'))
    return A, B, lo_lim, hi_lim, notes


def _quietest(db, t0, t1):
    """time of the quietest 10 ms window between t0 and t1 (its middle)"""
    i0, i1 = max(0, int(t0 / AHOP)), min(len(db), int(math.ceil(t1 / AHOP)))
    if i1 <= i0: return round(t0, 3)
    return round((i0 + int(np.argmin(db[i0:i1])) + 0.5) * AHOP, 3)


def repeat_flag(toks, times=None):
    """a word or run of up to 4 words said twice back to back: the sign of a restart"""
    for n in (4, 3, 2, 1):
        hit = next((i for i in range(len(toks) - 2 * n + 1) if toks[i:i + n] == toks[i + n:i + 2 * n]), None)
        if hit is not None:
            return 'restart? "%s" twice%s: keep the second' % (' '.join(toks[hit:hit + n]), (' at %.2f s' % times[hit]) if times else '')
    return None


def text_flags(words):
    """restart signs inside one phrase: words repeated back to back, cut-off words, stretched words"""
    flags = []
    tw = [(w, norm(w['w'])) for w in words]
    tw = [(w, t) for w, t in tw if t]
    rf = repeat_flag([t for _, t in tw], [w['s'] for w, _ in tw])
    if rf: flags.append(rf)
    for k, (w, t) in enumerate(tw):
        nxt = tw[k + 1] if k + 1 < len(tw) else None
        if w['w'].rstrip().endswith(('-', '\u2013', '\u2014')) or (nxt and len(t) >= 4 and len(nxt[1]) >= len(t) + 2
                                                                   and nxt[1].startswith(t)):
            flags.append('cut-off word? "%s"%s at %.2f s' % (w['w'], (' before "%s"' % nxt[0]['w']) if nxt else '', w['s']))
    for w in words:
        if w['e'] - w['s'] > 0.8:
            flags.append('stretched: "%s" lasts %.1f s at %.2f s (a hidden pause or merged restart: listen)'
                         % (w['w'], w['e'] - w['s'], w['s']))
    return flags


def restart_pairs(texts):
    """{piece index: [flags]} for neighbours where the later phrase begins like the earlier one (the earlier is the try)"""
    out = {}
    for k in range(len(texts) - 1):
        w1, w2 = texts[k], texts[k + 1]
        if not w1 or not w2: continue
        c = 0
        while c < min(len(w1), len(w2)) and w1[c] == w2[c]: c += 1
        if c >= 2 or w2[:len(w1)] == w1:
            out.setdefault(k, []).append('restart? the next phrase starts the same way ("%s"): this is likely the first try'
                                         % ' '.join(w2[:max(c, 1)]))
            out.setdefault(k + 1, []).append('restart of the phrase before')
    return out


def _mono16k(path):
    import av
    out = []
    with av.open(path) as c:
        rs = av.AudioResampler(format='s16', layout='mono', rate=16000)
        for f in c.decode(audio=0):
            for g in rs.resample(f): out.append(g.to_ndarray().reshape(-1))
        for g in rs.resample(None): out.append(g.to_ndarray().reshape(-1))
    return np.concatenate(out).astype(np.int16)


def _write_wav(path, x):
    with wave.open(path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(16000); w.writeframes(x.tobytes())


def _assign(words, spans):
    """each word to the span it overlaps most (or the nearest within 0.5 s); returns per-span lists and the leftovers"""
    per, left = [[] for _ in spans], []
    for w in words:
        best, bk = None, -1e9
        for k, (a, b) in enumerate(spans):
            ov = min(b, w['e']) - max(a, w['s'])
            if ov > bk: best, bk = k, ov
        if best is not None and bk > -0.5: per[best].append(w)
        else: left.append(w)
    return per, left


def _ranges(vals):
    out = []
    for v in vals:
        m = re.match(r'^\s*(\d+(?:\.\d*)?)\s*[-:]\s*(\d+(?:\.\d*)?)\s*$', v)
        if not m: sys.exit('not a range (use A-B in seconds): %r' % v)
        out.append((float(m.group(1)), float(m.group(2))))
    return out


def _cuts_from(vals):
    if len(vals) == 1 and vals[0].lower().endswith('.json'):
        J = json.load(open(vals[0], encoding='utf-8'))
        if isinstance(J, dict): J = J.get('cuts') or J.get('phrases') or []
        return [(float(c['in']), float(c['out'])) if isinstance(c, dict) else (float(c[0]), float(c[1])) for c in J]
    return _ranges(vals)


def _header(th, fps):
    mode = ('relative: edge = floor + 10 = %.0f dB, loud %.0f dB' % (th['edge'], th['loud']) if th['rel'] else
            'absolute: edge %.0f dB, loud %.0f dB' % (th['edge'], th['loud']))
    print('levels: floor %.1f dB, speech %.1f dB (95th pct) | %s | frames at %g fps' % (th['floor'], th['speech'], mode, fps))


def _warn(th):
    if th['rel']: return
    if th['floor'] > FLOOR_WARN:
        print('WARNING: the room floor is %.0f dB, above %.0f dB: not a clean voice-over recording. The -70 dB rules '
              'would read room noise as speech: use --rel.' % (th['floor'], FLOOR_WARN), file=sys.stderr)
    elif th['floor'] > th['edge'] - 2:
        print('NOTE: the room floor (%.0f dB) sits close to the %.0f dB edge level: many edges will be cut in dips '
              'instead of on the floor; --rel may suit this recording better.' % (th['floor'], th['edge']), file=sys.stderr)
    elif th['speech'] < QUIET_WARN:
        print('WARNING: the recording is very quiet (speech about %.0f dB): the -55 dB breath and scan limits assume a '
              'normal raw voice level; check flagged breaths by ear, or use --rel.' % th['speech'], file=sys.stderr)


def _print_scan(db, cuts, th, words=()):
    probs = edge_scan(db, cuts, th)
    if not probs:
        print('edge scan: clean (%d cuts; no edge has audio over %.0f dB on both sides)' % (len(cuts), th['loud'])); return 0
    print('edge scan: %d PROBLEM(S): these edges chop a sound (audio over %.0f dB on both sides)' % (len(probs), th['loud']))
    for kind, k, t, x, y in probs:
        near = ' '.join(w['w'] for w in words if t - 0.8 < w['e'] and w['s'] < t + 0.6)
        print('  %-5s cut %d at %.3f s: %.0f / %.0f dB%s' % (kind, k + 1, t, x, y, ('  "%s"' % near) if near else ''))
    return len(probs)


def main(argv):
    if len(argv) < 3: sys.exit(__doc__)
    opts = dict(rel=False, fps=30.0, edge=None, loud=None, json=None, wav_dir=None, words=None)
    pos, i = [], 1
    while i < len(argv):
        x = argv[i]
        if x == '--rel': opts['rel'] = True
        elif x in ('--fps', '--edge', '--loud', '--json', '--wav-dir', '--words'):
            if i + 1 >= len(argv): sys.exit('%s needs a value' % x)
            v, k = argv[i + 1], x[2:].replace('-', '_')
            opts[k] = float(v) if k in ('fps', 'edge', 'loud') else v; i += 1
        else: pos.append(x)
        i += 1
    if len(pos) < 2: sys.exit(__doc__)
    media, rest = pos[0], pos[1:]
    mode = next((m for m in ('--at', '--keep', '--scan', '--phrases') if m in rest), None)
    fps = opts['fps']
    if mode is None or mode == '--at':             # the snap modes (with --rel exactly the older output)
        if opts['rel']:
            env, snapper = envelope(media), snap
        else:
            db = levels(media); th = thresholds(db, False, opts['edge'], opts['loud']); _warn(th)
            env, snapper = None, (lambda _e, t: snap_abs(db, t, th, fps))
        def safe(t):                                # the older rule raised ValueError past the end of the media
            try: return snapper(env, t)
            except ValueError: return None
        if mode == '--at':
            for t in rest[rest.index('--at') + 1:]:
                r = safe(float(t))
                print('%8.3f -> %8.3f %s' % ((float(t),) + r) if r else '%8.3f -> past the end of the media' % float(t))
        else:
            W = json.load(open(rest[0], encoding='utf-8'))['words']
            for arg in rest[1:]:
                ph, after = arg.rsplit('@', 1) if '@' in arg else (arg, '0')
                p = phrase_time(W, ph, float(after)); r = safe(p)
                if r is None: print('%-40s whisper %8.3f -> past the end of the media' % (ph[:40], p)); continue
                print('%-40s whisper %8.3f -> cut %8.3f (%s)' % (ph[:40], p, max(float(after), r[0]), r[1]))
        return 0
    db = levels(media)
    th = thresholds(db, opts['rel'], opts['edge'], opts['loud'])
    vals = rest[rest.index(mode) + 1:]
    wfile = opts['words'] or next((v for v in rest[:rest.index(mode)] if v.lower().endswith('.json')), None)
    words = json.load(open(wfile, encoding='utf-8'))['words'] if wfile else []
    _header(th, fps); _warn(th)
    if mode == '--scan':
        return 1 if _print_scan(db, _cuts_from(vals), th, words) else 0
    if mode == '--keep':
        rng = _ranges(vals); rows = []
        mid = lambda w: (w['s'] + w['e']) / 2
        per = [[w for w in words if a <= mid(w) <= b] for a, b in rng]          # a range's own words
        print('  #   given            in       out      frames        sound           text')
        for k, (a, b) in enumerate(rng):
            if words:                                   # read the range through its words and the sound pieces
                A, B, lo_lim, hi_lim, kn = keep_span(db, a, b, th, per[k], [w for w in words if not a <= mid(w) <= b])
            else:
                A, B, lo_lim, hi_lim, kn = a, b, None, None, []
            r = clean_edges(db, A, B, th, fps, per[k], lo_lim, hi_lim)
            if r is None:
                print('  %-3d %7.2f-%-7.2f  no sound above %.0f dB in this range' % (k + 1, a, b, th['sound'])); continue
            r['notes'] = kn + r['notes']
            if not words:                               # without a transcript the range is taken as given: say so at its edges
                if db[max(0, int(b / AHOP)):int((b + 0.3) / AHOP)].max(initial=-120.0) > th['loud']:
                    r['notes'].append('sound over %.0f dB within 0.3 s after %.2f: does the phrase run past the range?' % (th['loud'], b))
                if db[max(0, int((a - 0.3) / AHOP)):max(0, int(a / AHOP))].max(initial=-120.0) > th['loud']:
                    r['notes'].append('sound over %.0f dB within 0.3 s before %.2f: does the phrase start earlier?' % (th['loud'], a))
            if rows and r['in_f'] < rows[-1]['out_f']:
                r['notes'].append('overlaps the range before by %d frames' % (rows[-1]['out_f'] - r['in_f']))
            txt, fl = ' '.join(w['w'] for w in per[k]), text_flags(per[k])
            print('  %-3d %7.2f-%-7.2f %8.3f %8.3f  %6d-%-6d %7.2f-%-7.2f %s' % (k + 1, a, b, r['in'], r['out'], r['in_f'],
                                                                         r['out_f'], r['first'], r['last'], ('"%s"' % txt[:50]) if txt else ''))
            for nt in r['notes'] + fl: print('        - ' + nt)
            rows.append(dict(a=a, b=b, text=txt, flags=fl, **r))
        bad = _print_scan(db, [(r['in'], r['out']) for r in rows], th, words)
        if opts['json']: json.dump(rows, open(opts['json'], 'w', encoding='utf-8'), indent=1)
        return 1 if bad else 0
    # --phrases
    sp = pieces(db, th)
    per, left = _assign(words, sp) if words else ([[] for _ in sp], [])
    texts = [[norm(w['w']) for w in ws if norm(w['w'])] for ws in per]
    own = {}
    if opts['wav_dir']:
        os.makedirs(opts['wav_dir'], exist_ok=True)
        for k, (a, b) in enumerate(sp):
            jf = os.path.join(opts['wav_dir'], 'p%03d_%.2f.json' % (k + 1, a))
            if os.path.exists(jf):
                J = json.load(open(jf, encoding='utf-8'))
                own[k] = [norm(t) for t in ' '.join(s['text'] for s in J.get('segments', [])).split() if norm(t)]
    texts = [own.get(k, t) for k, t in enumerate(texts)]
    pairs = restart_pairs(texts)
    rows, nflag, prev_o = [], 0, None
    print('  #   in       out      frames        text                                                flags')
    for k, (a, b) in enumerate(sp):
        lo_lim = (sp[k - 1][1] + 0.02) if k else None
        hi_lim = (sp[k + 1][0] - 0.02) if k + 1 < len(sp) else None
        r = clean_edges(db, a, b, th, fps, per[k], lo_lim, hi_lim)
        if r is None: continue
        pk = float(db[int(a / AHOP):int(math.ceil(b / AHOP))].max())
        flags = list(pairs.get(k, []))
        if k in own:
            rf = repeat_flag(own[k])
            if rf: flags.append(rf + ' (its own transcript)')
            if not own[k] and pk >= th['loud']: flags.append('its own transcript is empty: a mumble or noise? listen')
            flags += [f for f in text_flags(per[k]) if not f.startswith('restart?')]
        else:
            flags += text_flags(per[k])
            if not per[k] and pk >= th['loud'] and words:
                flags.append('speech with no transcript words: a restart or mumble the transcript dropped? transcribe it on its own')
        if pk < th['loud']:
            flags.append('soft sound only (peak %.0f dB): breath or noise, cut' % pk)
        if prev_o is not None and r['in_f'] < prev_o:
            r['notes'].append('overlaps the phrase before by %d frames' % (prev_o - r['in_f']))
        prev_o = r['out_f']
        txt = ' '.join(w['w'] for w in per[k]) if per[k] else ('(no words)' if words else '')
        nflag += bool(flags)
        print('  %-3d %8.3f %8.3f  %6d-%-6d %-52s %s' % (k + 1, r['in'], r['out'], r['in_f'], r['out_f'],
                                                       (('"%s"' % txt) if per[k] else txt)[:52], '; '.join(flags)))
        for nt in r['notes']: print('        - ' + nt)
        rows.append(dict(n=k + 1, a=round(a, 2), b=round(b, 2), text=txt, peak=round(pk, 1), flags=flags, **r))
    if left: print('words with no sound under them (transcript inventions?): %s' % ' '.join('%s@%.2f' % (w['w'], w['s']) for w in left[:20]))
    bad = _print_scan(db, [(r['in'], r['out']) for r in rows], th, words)
    src = ('their own transcripts (%d pieces)' % len(own)) if own else ('the whole-file transcript' if words else 'no transcript')
    print('restart checks: %d of %d phrases flagged, from %s' % (nflag, len(rows), src))
    if opts['wav_dir'] and len(own) < len(rows):
        x = _mono16k(media); pad = np.zeros(8000, np.int16); nw = 0
        for r in rows:
            base = os.path.join(opts['wav_dir'], 'p%03d_%.2f' % (r['n'], r['a']))
            if os.path.exists(base + '.json'): continue
            _write_wav(base + '.wav', np.concatenate([pad, x[int(r['in'] * 16000):int(r['out'] * 16000)], pad])); nw += 1
        hear = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hear.py')
        print('wrote %d piece WAVs to %s (0.5 s of silence each side). Transcribe each on its own, then run this again '
              'with the same --wav-dir:\n  for f in "%s"/*.wav; do python "%s" "$f" "${f%%.wav}.json"; done'
              % (nw, opts['wav_dir'], opts['wav_dir'].replace('\\', '/'), hear.replace('\\', '/')))
    elif words and not own:
        print('narrator recordings: transcribe each phrase on its own to catch restarts the whole-file transcript merged '
              '(--wav-dir DIR)')
    if opts['json']: json.dump(rows, open(opts['json'], 'w', encoding='utf-8'), indent=1)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
