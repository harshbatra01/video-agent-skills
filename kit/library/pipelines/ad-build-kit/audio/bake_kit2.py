"""Kit additions for the roll-out: marker strokes (headline highlighter), crowd bed (archive race footage)."""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bake_kit import load, trim, finish, SR, HERE

kit = json.load(open(os.path.join(HERE, 'kit.json')))
names = {k['name'] for k in kit}
new = []
new.append(finish('MARK1', trim(load('MARK_DrawLine'), 'swell', max_len=0.9), 'swell', 'MARK_DrawLine (highlighter stroke)'))
new.append(finish('MARK2', trim(load('MARK_Drag'), 'swell', max_len=0.9), 'swell', 'MARK_Drag'))
c = load('CROWD_BigCheer')
seg = c[int(1.2 * SR):int(13.2 * SR)].copy()
fi = int(0.25 * SR); fo = int(0.8 * SR)
seg[:fi] *= np.linspace(0, 1, fi)[:, None]; seg[-fo:] *= np.linspace(1, 0, fo)[:, None]
new.append(finish('CROWD1', seg, 'bed', 'CROWD_BigCheer 1.2-13.2 s'))
kit = [k for k in kit if k['name'] not in {n['name'] for n in new}] + new
json.dump(kit, open(os.path.join(HERE, 'kit.json'), 'w'), indent=1)
print(len(kit), 'kit entries')
