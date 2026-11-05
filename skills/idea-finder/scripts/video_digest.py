#!/usr/bin/env python3
"""Angle counts across the YouTube list, plus hooks, endings, keyword lines and top comments for chosen videos. Text only, no video download."""
import json, re, subprocess, sys
from pathlib import Path
JOB = Path(sys.argv[1]); RAW = JOB / 'research' / 'raw'; IDS = sys.argv[2:]
YTDLP = __import__('shutil').which('yt-dlp') or 'yt-dlp'
rows = json.loads((RAW / 'youtube.json').read_text())
ANGLES = dict(loss=r'lost|loss|\$8\dB|\b80\b|profit', warning=r'warn|terrif|scar|danger|risk|humanity', bubble=r'bubble|crash|con\b|disaster|lie|fake|problem|slow', invest=r'buy|stock|invest|\$\d+ ', worth=r'worth|valuation|trillion', explain=r'explain|numbers|breaks? down|what', founder=r'founder|amodei|dario|billionaire|pledge|charity')
print('ANGLE COUNTS IN TITLES (of %d):' % len(rows))
for k, rx in ANGLES.items():
    hit = [r for r in rows if re.search(rx, r['title'] or '', re.I)]
    print(' %-8s %3d videos, %9d views' % (k, len(hit), sum(r['views'] for r in hit)))
print('SHORT VIDEOS (under 3 min):')
for r in [x for x in rows if (x['secs'] or 999) <= 180][:12]:
    print(' %8s v | %3ss | %s | %s | %s' % (r['views'], r['secs'], r['id'], (r['channel'] or '')[:18], (r['title'] or '')[:70]))
KEY = re.compile(r'pledg|charit|80 ?%|80 percent|blackmail|shut ?down|50\.1|voting|benefit trust|left open ?ai|existential|nobody|no one', re.I)
for vid in IDS:
    d = RAW / 'v' / vid; d.mkdir(parents=True, exist_ok=True)
    subprocess.run([YTDLP, '--skip-download', '--no-warnings', '--write-auto-subs', '--write-subs', '--sub-langs', 'en,en-orig', '--sub-format', 'vtt', '--write-comments', '--write-info-json',
                    '--extractor-args', 'youtube:max_comments=150,all,0,0;comment_sort=top', '-o', str(d / 'v.%(ext)s'), 'https://www.youtube.com/watch?v=' + vid], capture_output=True, timeout=200)
    meta = json.loads((d / 'v.info.json').read_text()) if (d / 'v.info.json').exists() else {}
    vtt = next(iter(sorted(d.glob('*.vtt'))), None)
    words = []
    if vtt:
        for line in vtt.read_text(errors='ignore').splitlines():
            if '-->' in line or line.startswith(('WEBVTT', 'Kind:', 'Language:')) or not line.strip():
                continue
            line = re.sub(r'<[^>]+>', '', line).strip()
            if line and (not words or line != words[-1]):
                words.append(line)
    t = re.sub(r'\s+', ' ', ' '.join(words))
    # Auto captions roll, so drop repeated runs.
    w = t.split(); clean = []
    for x in w:
        if clean[-6:].count(x) < 2 or len(x) > 3:
            clean.append(x)
    t = ' '.join(clean); (d / 'transcript.txt').write_text(t)
    print('\n=== %s | %s | %s views' % (vid, meta.get('title', '?')[:80], meta.get('view_count')))
    print('HOOK:', t[:420]); print('END:', t[-260:])
    sents = re.split(r'(?<=[.?!])\s+', t)
    kw = [s[:190] for s in sents if KEY.search(s)]
    print('KEYWORD LINES (%d):' % len(kw)); [print(' -', s) for s in kw[:5]]
    cs = sorted(meta.get('comments') or [], key=lambda c: -(c.get('like_count') or 0))
    print('TOP COMMENTS:'); [print(' - [%s] %s' % (c.get('like_count'), re.sub(r'\s+', ' ', c.get('text') or '')[:170])) for c in cs[:7]]
