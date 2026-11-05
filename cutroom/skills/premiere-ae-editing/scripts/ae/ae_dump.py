"""Read-only dump of After Effects projects (comps, layers, in/out, parents, mattes, effects with matchNames,
keyframes, expressions, text with font/size/colour). Use it to learn how an existing .aep was built (a reference
animation, a template the user made) before copying its look by script.

usage: python ae_dump.py out.txt project1.aep [project2.aep ...]
Copies the .aep files into <out>_aecopy/ and opens the copies (the user's files are never opened), then runs AE
through ae_run.py. After Effects must be closed first.
"""
# macOS (from the Mac port, Oct 2026): AE may also be open with an EMPTY untitled project there; ae_run.py probes it and
# refuses anything else, and the dump script then leaves AE open instead of quitting it.
import sys, os, shutil, json, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    if len(sys.argv) < 3: sys.exit(__doc__)
    out = os.path.abspath(sys.argv[1]); base = os.path.splitext(out)[0]
    cdir = base + '_aecopy'; os.makedirs(cdir, exist_ok=True)
    files = []
    for p in sys.argv[2:]:
        dst = os.path.join(cdir, os.path.basename(p)); shutil.copy2(p, dst); files.append(dst.replace('\\', '/'))
    jsx = base + '_aedump.jsx'; stem = os.path.splitext(os.path.basename(jsx))[0]
    t = open(os.path.join(HERE, 'ae_dump.jsx'), encoding='utf-8').read()
    t = (t.replace('__HERE__', json.dumps(os.path.dirname(jsx).replace('\\', '/') + '/')).replace('__STEM__', json.dumps(stem))
          .replace('__FILES__', json.dumps(files)).replace('__OUT__', json.dumps(out.replace('\\', '/'))))
    open(jsx, 'w', encoding='utf-8').write(t)
    json.dump([], open(base + '_aedump_jobs.json', 'w'))
    subprocess.run([sys.executable, os.path.join(HERE, 'ae_run.py'), jsx, '--timeout', '900'])
    print('dump:', out, '(%d lines)' % (sum(1 for _ in open(out, encoding='utf-8')) if os.path.exists(out) else 0))
