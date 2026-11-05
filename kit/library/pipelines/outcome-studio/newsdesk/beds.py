"""beds: sound beds for clips that have no audio of their own (our app screen recordings), made from the studio's
real recorded house sounds (CC0, ../studio/assets/sfx/house). Cue times are seconds into the clip segment.

python beds.py btc <out.wav> <dur> <close_at>      clock ticks to the close, heartbeat under it, a hit and a ding at the result
python beds.py goal <out.wav> <dur> <goal_at>      stadium bed, crowd roar on the goal
python beds.py press <out.wav> <dur>               low crowd + photographers' shutters (post-match, player of the match)
python beds.py tv <out.wav> <dur>                  a match on the TV in the room (lifestyle clips whose own audio is someone's song)
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'studio'))
import sfx


def btc(out, dur, close):
    cues = [(0, 'file:heartbeat', -10), (11.4, 'file:heartbeat', -10)]
    t = 0.0
    while t < close - .05:
        cues.append((t, 'tick' if int(t) % 2 == 0 else 'tock', -6)); t += 1.0
    cues += [(close, 'hit', -4), (close + .05, 'ding', -8)]
    return sfx.mix(cues, dur, out)


def goal(out, dur, at):
    return sfx.mix([(0, 'file:crowd_bed', -12), (at, 'roar', -2)], dur, out)


def press(out, dur, _=0):
    """post-match pitch-side: low crowd, photographers' shutters"""
    shots = [.5, 1.1, 1.3, 2.4, 3.2, 3.9, 4.1, 5.6, 6.3, 6.8, 7.3, 8.1, 9.4, 10.2, 11.0]
    return sfx.mix([(0, 'file:crowd_bed', -18)] + [(t, 'file:shutter', -9 if i % 3 else -6) for i, t in enumerate(shots) if t < dur - .3], dur, out)


def tv(out, dur, _=0):
    """a match on in the room: the crowd from the TV, low"""
    return sfx.mix([(0, 'file:crowd_bed', -16)], dur, out)


if __name__ == '__main__':
    a = sys.argv[1:]
    if len(a) < 3: sys.exit(__doc__)
    fn = {'btc': btc, 'goal': goal, 'press': press, 'tv': tv}[a[0]]
    print(fn(a[1], float(a[2]), float(a[3]) if len(a) > 3 else 0))
