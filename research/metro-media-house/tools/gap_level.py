#!/usr/bin/env python3
# Same level measurement as skills/reference-study/scripts/gap_sfx.py (voice RMS over word spans vs RMS in gaps > 0.12 s,
# trimmed 0.04 s each side), without its hard-wired job paths and without the sound-hit count. gap_level.py <video> <transcript.json>
import json, subprocess, sys, numpy as np
v, tp = sys.argv[1:3]
d = json.load(open(tp)); w = sorted((x['s'], x['e']) for x in d['words'])
gaps = [(a[1] + .04, b[0] - .04) for a, b in zip(w, w[1:]) if b[0] - a[1] > 0.12]
SR = 16000; x = np.frombuffer(subprocess.run(["ffmpeg","-nostdin","-v","error","-i",v,"-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout, np.float32)
rms = lambda segs: 10*np.log10(np.mean(np.concatenate([x[int(a*SR):int(b*SR)]**2 for a, b in segs if b > a])) + 1e-12)
wd = rms(w); gd = rms(gaps)
tail = (w[-1][1] + .1, len(x)/SR); head = (0, max(w[0][0] - .05, 0))
# longest gaps (voice stops) - candidate soundbites are not visible here because soundbite speech is transcribed too
lg = sorted(((round(b-a,2), round(a,2)) for a, b in gaps), reverse=True)[:5]
out = dict(words=len(w), gap_s=round(sum(b-a for a, b in gaps),1), voice_db=round(float(wd),1), gap_db=round(float(gd),1),
           music_under_voice_db=round(float(wd-gd),1), tail_s=round(tail[1]-tail[0],2),
           tail_db=round(float(rms([tail])),1) if tail[1]-tail[0] > .2 else None, longest_gaps=lg,
           wpm=round(len(w)/((w[-1][1]-w[0][0])/60),1))
print(json.dumps(out))
