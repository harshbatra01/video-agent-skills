"""3 things to check: SFX cue sheet + music edit plan, offline mix to check levels.
Times are sequence seconds where the sound's main peak must land (on the frame or just after, never early).
rel = loudness of the sound's loudest 400 ms relative to the dialogue's integrated loudness (LU)."""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import atools as A
from analyze_sfx import read_wav

HERE = os.path.dirname(os.path.abspath(__file__))
KIT_DIR = r"C:\VISION\IMMUFIX\repair\ENCODED RUSHES\Audio\SFX kit"
MUSIC = r"C:\VISION\IMMUFIX\repair\ENCODED RUSHES\Audio\Music\ES_Bring Them Home - Hampus Naeselius.wav"
SR = 48000
SEQ_END = 48.25
DIALOG_GAIN_DB = 8.0          # clip gain added to the 31 A1 dialogue clips

# (peak time, kit sound, rel LU, what it marks)
CUES = [
    (0.55, 'SHIM1', -14, '"?" swell + title in'),
    (0.57, 'QPOP1', -6, '"?" pops'),
    (3.60, 'SWISH2', -12, 'card 1 in, NUMBER ONE'),
    (4.02, 'POP1', -9, 'NO MEGA'),
    (4.58, 'TICK2', -15, 'DOSES'),
    (10.36, 'HUD1', -14, '100x meter appears'),
    (10.62, 'COUNT_10', -17, 'meter counts up (file starts here)'),
    (11.62, 'LOCK1', -11, 'MEGA DOSE lands'),
    (14.03, 'BOOM2', -14, 'Number two + music entrance'),
    (14.45, 'SWISH1', -12, 'card 2 in'),
    (15.10, 'TICK1', -16, 'ENHANCED'),
    (16.30, 'POP3', -9, 'BIOAVAILABILITY'),
    (17.15, 'GLASS2', -15, 'definition panel'),
    (19.06, 'POP4', -8, 'REFORMULATED (powder cut)'),
    (20.58, 'POP2', -10, 'YOUR BODY'),
    (22.90, 'POP1', -9, 'VITAMINS'),
    (23.42, 'POP1_up2', -8.5, 'MINERALS'),
    (24.10, 'POP1_up4', -8, 'NUTRIENTS'),
    (25.42, 'TICK3', -16, 'CAN ABSORB IT'),
    (26.30, 'POP5', -9, 'EFFICIENTLY'),
    (27.14, 'FLIP1', -12, 'roll to EFFECTIVELY'),
    (27.65, 'SWISH3', -12, 'card 3 in'),
    (28.18, 'TICK2', -16, 'BETTER'),
    (29.06, 'POP3', -9, 'UPTAKE'),
    (31.75, 'WHOOSH2', -13, 'ALMOST (runner cut)'),
    (32.17, 'COUNT_05', -16, '0 -> 100% (file starts here)'),
    (32.65, 'LOCK2', -11, '100% lands'),
    (35.22, 'TICK1', -16, 'IMMEDIATELY'),
    (36.10, 'POP2', -9, 'INTO THE CELLS'),
    (38.03, 'WHOOSH1', -9, 'cut to 100% shot + music climax'),
    (38.03, 'BOOM1', -10, 'climax hit'),
    (39.30, 'POP1', -7, '100%'),
    (41.10, 'LIGHT1', -11, 'spotlight on'),
    (41.66, 'LIGHT2', -13, 'spotlight widens'),
    (42.60, 'COUNT_09', -17, 'years counter (file starts here)'),
    (43.50, 'GLASS1', -16, 'counter lands'),
]
# level nudge after checking against the voice's local peaks (phones lose the low layers)
NUDGE = {'POP': 2, 'TICK': 2, 'SWISH': 1, 'GLASS': 2, 'COUNT': 4, 'LOCK': 1, 'WHOOSH': 1, 'HUD': 2, 'FLIP': 1}
SYNC_BIAS = 0.010   # sound may land a hair late, never early
START_AT_FILE_START = {'COUNT_10', 'COUNT_09', 'COUNT_05'}

# music: (seq start, seq end, track time at seq start, rel LU target for that section)
BAR = 240 / 90.0
D = lambda k: 2.6667 * k - 0.0067          # downbeat k of "Bring Them Home"
MUSIC_EDIT = [
    (0.0, 14.033, D(15) - 38.033, -16, 'intro pad'),
    (14.033, 38.033, D(15) - 38.033 + 14.033, -13, 'entrance on "Number two", build'),
    (38.033, SEQ_END, D(51), -11, 'climax from the cut, resolution chord at 46.03'),
]


def load(path):
    a, sr, _, _ = read_wav(path); assert sr == SR, (path, sr)
    return a[:, :2] if a.shape[1] >= 2 else np.repeat(a, 2, axis=1)


def place(out, x, t0, gain_db):
    i = int(round(t0 * SR)); g = 10 ** (gain_db / 20)
    if i < 0: x = x[-i:]; i = 0
    n = min(len(x), len(out) - i)
    if n > 0: out[i:i + n] += x[:n] * g


def plan():
    kit = {k['name']: k for k in json.load(open(os.path.join(HERE, 'kit.json')))}
    dia = np.load(os.path.join(HERE, 'tt_dialog.npy')).astype(np.float64) * 10 ** (DIALOG_GAIN_DB / 20)
    d_lufs = A.lufs(dia, SR)
    events = []
    for t, nm, rel, what in CUES:
        k = kit[nm]
        t = t + SYNC_BIAS
        rel = rel + next((v for k, v in NUDGE.items() if nm.startswith(k)), 0)
        start = t if nm in START_AT_FILE_START else t - k['peak_t']
        gain = (d_lufs + rel) - k['m_max']
        events.append(dict(t=round(t, 4), name=nm, file=k['file'], start=round(start, 4), dur=k['dur'], gain_db=round(gain, 1), rel=rel, what=what))
    # music section gains from each section's own loudness
    mus = load(MUSIC)
    msecs = []
    for s, e, src, rel, what in MUSIC_EDIT:
        seg = mus[int(src * SR):int((src + e - s) * SR)]
        sl = A.lufs(seg, SR)
        msecs.append(dict(start=s, end=e, src_in=round(src, 4), rel=rel, sect_lufs=round(sl, 1), gain_db=round(d_lufs + rel - sl, 1), what=what))
    return d_lufs, events, msecs, dia, mus


def assign_tracks(events, gap=0.02):
    ends = {'A3': -1, 'A4': -1}
    for ev in sorted(events, key=lambda e: e['start']):
        for tr in ('A3', 'A4'):
            if ev['start'] >= ends[tr] + gap:
                ev['track'] = tr; ends[tr] = ev['start'] + ev['dur']; break
        else:
            ev['track'] = 'A5'
    return events


if __name__ == '__main__':
    d_lufs, events, msecs, dia, mus = plan()
    events = assign_tracks(events)
    out_sfx = np.zeros((int(SEQ_END * SR), 2)); out_mus = np.zeros_like(out_sfx)
    for ev in events: place(out_sfx, load(os.path.join(KIT_DIR, ev['file'])), ev['start'], ev['gain_db'])
    for m in msecs:
        seg = mus[int(m['src_in'] * SR):int((m['src_in'] + m['end'] - m['start']) * SR)]
        place(out_mus, seg, m['start'], m['gain_db'])
    dia = dia[:len(out_sfx)]
    mix = dia + out_sfx + out_mus
    print('dialogue %.1f LUFS (with +%.0f dB gain), true peak %.1f dBTP' % (d_lufs, DIALOG_GAIN_DB, A.true_peak_db(dia)))
    print('music alone %.1f LUFS, sfx alone %.1f LUFS' % (A.lufs(out_mus, SR), A.lufs(out_sfx, SR)))
    print('MIX %.1f LUFS, true peak %.1f dBTP' % (A.lufs(mix, SR), A.true_peak_db(mix)))
    for m in msecs: print('  music %6.2f-%6.2f src %7.3f  section %.1f LUFS -> gain %+.1f dB (%s)' % (m['start'], m['end'], m['src_in'], m['sect_lufs'], m['gain_db'], m['what']))
    tr_count = {}
    for ev in events:
        tr_count[ev['track']] = tr_count.get(ev['track'], 0) + 1
        print('  %6.2f %-9s %s start %6.3f gain %+6.1f dB  %s' % (ev['t'], ev['name'], ev['track'], ev['start'], ev['gain_db'], ev['what']))
    print('tracks', tr_count)
    json.dump(dict(dialog_lufs=d_lufs, dialog_gain_db=DIALOG_GAIN_DB, events=events, music=msecs, music_file=MUSIC), open(os.path.join(HERE, 'cues_tt.json'), 'w'), indent=1)
    peak = np.abs(mix).max()
    A_w = os.path.join(HERE, 'tt_mix_preview.wav')
    import wave
    y = np.clip(mix / max(1.0, peak) * 0.98, -1, 1)
    with wave.open(A_w, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((y * 32767).astype('<i2').tobytes())
    np.save(os.path.join(HERE, 'tt_mix_parts.npy'), np.stack([dia.mean(axis=1), out_sfx.mean(axis=1), out_mus.mean(axis=1)]).astype(np.float32))
    print('preview ->', A_w)
