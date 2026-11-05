import sys, json, os; sys.path.insert(0,'.')
from vgrab import grab
REF=r'C:\VISION\IMMUFIX\repair\ENCODED RUSHES\Reference for zooms and colour.mp4'
RAW=r'C:\VISION\IMMUFIX\repair\ENCODED RUSHES\Cleaned\A003_09181126_C108-esv2-50p-bg-10p-music-10p.mp4'
# (sequence time, clip start, clip in-point) from the reference sequence V1
cuts=[(0,37.83),(1.1667,39.32),(3.8333,42.60),(5.1167,44.20),(7.5167,79.48),(9.0833,81.28),(10.3667,82.83),(11.1167,83.88),(11.9667,102.03),(12.6833,102.92),(13.5167,106.08),(14.3167,107.23),(17.05,308.88),(18.9667,311.12),(19.9167,312.28),(20.2,312.68),(24.05,316.88),(26.8,350.28),(27.65,351.28),(28.3167,352.03),(29.1167,345.00)]
times=[2.5,6.3,8.3,15.7,18.0,22.0,25.5,29.6]
out={}
for t in times:
    st,inp=[c for c in cuts if c[0]<=t][-1]
    src=inp+(t-st)
    d=f'calib/t{t:05.2f}'
    rf=grab(REF, t-0.05, 0.1, 1, outdir=d, prefix='ref')
    sf=grab(RAW, src-0.2, 0.4, 1, outdir=d, prefix='raw')
    out[t]={'src':src,'ref':rf,'raw':sf}
    print(t, 'src %.2f'%src, len(rf), 'ref frames', len(sf), 'raw frames', flush=True)
json.dump(out, open('calib/index.json','w'), indent=1)
