"""Graded Paula / product clips for Immufix social: per-clip natural grade baked into a .cube LUT, exported with ffmpeg
as 4K landscape (3840x2160) + vertical 1080x1920 (where the subject stays put), H.264 high quality, no audio.
usage: python clips.py [name_filter]"""
import os, sys, json, subprocess, glob
import numpy as np, av
from av.video.reformatter import Colorspace, ColorRange
from sl3 import grade
B = r'C:/VISION/IMMUFIX/repair/ENCODED RUSHES/B roll/'
OUT = r'C:/VISION/IMMUFIX/repair/Renders/Paula clips for <recipient>/'
LUTS = r'C:/Users/Kanishk/AppData/Local/Temp/claude/C--VISION-IMMUFIX-repair-ENCODED-RUSHES/b6d96195-2992-4138-a685-9dc3b5c5abcd/scratchpad/webstill/luts/'
LOOK = dict(warm=0.02, sat=1.06, contrast=1.06)
W, H = 6048, 3408
# name, clip, t0, t1, landscape crop (x0 fraction, width fraction) or None, vertical centre x fraction or None, group
CLIPS = [
    ('Paula holding pouch park 01', 'C120', 4.0, 10.0, None, 0.47, 'Paula'),
    ('Paula holding pouch park 02', 'C120', 19.0, 23.0, None, 0.50, 'Paula'),
    ('Paula holding two pouches park', 'C120', 27.5, 32.5, None, 0.50, 'Paula'),
    ('Pouch held checking watch', 'C121', 4.0, 13.0, None, 0.50, 'Paula'),
    ('Paula scooping low angle', 'C121', 50.0, 58.0, None, 0.50, 'Paula'),
    ('Paula pouring and shaking', 'C121', 84.0, 94.0, None, 0.50, 'Paula'),
    ('Paula kneeling shaking', 'C121', 100.0, 110.0, None, 0.50, 'Paula'),
    ('Paula drinking wide', 'C122', 12.0, 20.0, (0.0, 0.82), 0.45, 'Paula'),
    ('Paula drinking medium', 'C123', 2.0, 9.0, None, 0.425, 'Paula'),
    ('Paula smiling after drinking', 'C123', 21.4, 24.4, None, 0.42, 'Paula'),
    ('Paula lacing pink shoes close', 'C124', 3.0, 12.0, None, 0.48, 'Paula'),
    ('Paula catching breath close', 'C125', 74.0, 84.0, None, 0.55, 'Paula'),
    ('Paula calf stretch riverside', 'C126', 3.0, 12.0, (0.0, 0.88), 0.44, 'Paula'),
    ('Paula portrait low angle', 'C127', 1.0, 9.0, None, None, 'Paula'),
    ('Paula running park wide', 'C128', 26.0, 33.0, None, None, 'Paula'),
    ('Paula running toward camera 01', 'C129', 30.0, 41.0, None, 0.50, 'Paula'),
    ('Paula running toward camera 02', 'C129', 88.0, 99.0, None, 0.50, 'Paula'),
    ('Paula walking cooldown riverside', 'C130', 86.0, 94.0, None, 0.55, 'Paula'),
    ('Paula packing pouch in suitcase', 'C131', 14.0, 20.0, None, None, 'Paula'),
    ('Pouch on post', 'C132', 72.0, 80.0, None, 0.47, 'Product'),
    ('Pouch on table', 'C137', 4.0, 12.0, None, 0.46, 'Product'),
    ('Scoop pour into shaker', 'C140', 38.0, 42.0, None, 0.52, 'Product'),
    ('Pouch logo macro', 'C138', 2.0, 10.0, None, None, 'Product'),
]


def src(clip): return glob.glob(B + '*_%s.mp4' % clip)[0]


def sample(path, t):
    c = av.open(path); v = c.streams.video[0]; tb = v.time_base
    c.seek(int(max(0, t - 1.2) / tb), stream=v, backward=True)
    for fr in c.decode(v):
        if fr.pts * tb > t - 0.02:
            a = fr.reformat(width=960, height=540, format='rgb24', src_colorspace=Colorspace.ITU709, src_color_range=ColorRange.MPEG,
                            dst_color_range=ColorRange.JPEG).to_ndarray(); c.close(); return a.astype(np.float64) / 255


def luma(g): return 0.2126 * g[..., 0] + 0.7152 * g[..., 1] + 0.0722 * g[..., 2]


def clip_params(path, t0, t1, crop):
    fr = [sample(path, t) for t in (t0 + 0.3, (t0 + t1) / 2, t1 - 0.3)]
    if crop: fr = [f[:, int(crop[0] * 960):int((crop[0] + crop[1]) * 960)] for f in fr]
    g = np.concatenate([grade(f, **LOOK).reshape(-1, 3) for f in fr]); y = luma(g)
    b0, w0, m_nat = np.percentile(y, 1), np.percentile(y, 99.5), np.median(y)
    k = min(1.35, max(1.0, 0.9 / (w0 - b0)))
    m2 = np.median(np.clip((y - b0) * k + 0.04, 0, 1))
    target = max(m2, 0.85 * m_nat)
    gam = float(np.log(target) / np.log(m2)) if m2 > 0 else 1.0
    return dict(b0=float(b0), k=float(k), gamma=round(gam, 3), med=round(float(target), 3))


def full_chain(v, p):
    g = grade(v, **LOOK)
    g = np.clip((g - p['b0']) * p['k'] + 0.04, 0, 1)
    return np.power(g, p['gamma'])


def write_cube(path, p, size=65):
    gr = np.linspace(0, 1, size)
    b, g, r = np.meshgrid(gr, gr, gr, indexing='ij')
    out = full_chain(np.stack([r, g, b], -1).reshape(-1, 3), p)
    with open(path, 'w') as f:
        f.write('TITLE "immufix natural"\nLUT_3D_SIZE %d\nDOMAIN_MIN 0 0 0\nDOMAIN_MAX 1 1 1\n' % size)
        f.write('\n'.join('%.5f %.5f %.5f' % tuple(o) for o in out) + '\n')


def even(x): return int(round(x / 2)) * 2


def run(name, clip, t0, t1, crop, vx, group):
    path = src(clip); p = clip_params(path, t0, t1, crop)
    lut = name.replace(' ', '_') + '.cube'; write_cube(LUTS + lut, p)
    conv_in = 'flags=lanczos:in_color_matrix=bt709:in_range=tv,format=gbrp16le,lut3d=file=%s:interp=tetrahedral,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p' % lut
    enc = ['-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709',
           '-color_trc', 'bt709', '-color_range', 'tv', '-movflags', '+faststart', '-an']
    jobs = []
    cw = 'crop=%d:%d:%d:%d,' % (even(crop[1] * W), even(crop[1] * W * 9 / 16), even(crop[0] * W), even((H - crop[1] * W * 9 / 16) / 2)) if crop else ''
    jobs.append((OUT + '%s/Landscape 4K/%s.mp4' % (group, name), cw + 'scale=3840:2160:' + conv_in))
    if vx is not None:
        vw = even(H * 9 / 16); x0 = even(min(max(vx * W - vw / 2, 0), W - vw))
        jobs.append((OUT + '%s/Vertical 1080x1920/%s.mp4' % (group, name), 'crop=%d:%d:%d:0,scale=1080:1920:' % (vw, H, x0) + conv_in))
    for out, vf in jobs:
        os.makedirs(os.path.dirname(out), exist_ok=True)
        cmd = ['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-ss', '%.3f' % t0, '-i', path, '-t', '%.3f' % (t1 - t0), '-vf', vf] + enc + [out]
        r = subprocess.run(cmd, cwd=LUTS, capture_output=True, text=True)
        print('%-36s %-18s %s' % (name, out.split('/')[-2], 'ok %.0f MB' % (os.path.getsize(out) / 1e6) if r.returncode == 0 else 'FAIL ' + r.stderr[-300:]), flush=True)
    print('   params', json.dumps(p), flush=True)


if __name__ == '__main__':
    os.makedirs(LUTS, exist_ok=True)
    flt = sys.argv[1] if len(sys.argv) > 1 else ''
    for c in CLIPS:
        if flt in c[0]: run(*c)
