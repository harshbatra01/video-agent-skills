"""Batch structure study: run anatomy (and optional Whisper) over every reference edit in a folder.

usage: python study.py REFS_DIR OUT_DIR [--words]
- names each ref with a short slug from its title
- skips refs already analysed (OUT_DIR/<slug>.json exists)
- --words also writes <slug>_words.json with hear.py (speech / lyric timings) when missing
Prints one summary block per ref (the .txt from anatomy).
Run WITHOUT -I only if --words is used (faster-whisper lives in the main site-packages; it imports fine either way).
"""
import sys, os, re, subprocess, glob

HERE = os.path.dirname(os.path.abspath(__file__))
HEAR = os.path.join((os.environ.get('PAE_SCRIPTS') or os.path.expanduser('~/.claude/skills/premiere-ae-editing/scripts')), 'media', 'hear.py')

def slug(name):
    name = re.sub(r"_\d{3,4}p$", "", os.path.splitext(os.path.basename(name))[0])
    words = re.findall(r"[A-Za-z0-9]+", name)
    s = "_".join(words[:5]).lower()
    return s[:40] or "ref"

def main():
    src, out = sys.argv[1], sys.argv[2]
    words = "--words" in sys.argv
    os.makedirs(out, exist_ok=True)
    files = sorted(glob.glob(os.path.join(src, "*.mp4")))
    for f in files:
        if f.endswith(".part"): continue
        s = slug(f)
        if not os.path.exists(os.path.join(out, s + ".json")):
            r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "anatomy.py"), f, out, "--name", s],
                               capture_output=True, text=True, encoding="utf-8", errors="replace")
            if r.returncode != 0:
                print(f"== {s}: anatomy FAILED {r.stderr.strip()[-300:]}"); continue
        if words and not os.path.exists(os.path.join(out, s + "_words.json")):
            subprocess.run([sys.executable, HEAR, f, os.path.join(out, s + "_words.json")], capture_output=True, text=True)
        txt = os.path.join(out, s + ".txt")
        print("== " + open(txt, encoding="utf-8").read().strip() if os.path.exists(txt) else f"== {s}: no summary")

if __name__ == "__main__":
    main()
