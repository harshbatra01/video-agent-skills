"""One command to prepare a new music edit: song analysis + footage catalog, ready for a plan script.

usage: python setup_edit.py EDIT_DIR SUBJECT [--song SONG_FILE_OR_YT_ID] [--footage YT_ID,YT_ID,...] [--max 1080]
  EDIT_DIR   e.g. edits-kit/edits/03_messi_quote  (created; layout below)
  SUBJECT    short name for the re-ID gallery (e.g. messi): used to score how clearly he is in each shot
Layout:  song/ (song.wav 48 kHz, song_22k.wav, beats.json, words.json)   footage/ (fNN_*.mp4)
         catalog/ (catalog.json, emb.npy, thumbs, sheet_*.png)            mattes/auto/ (filled later by plans)
Every step is cached: re-running skips what exists. Run WITHOUT python -I (torch, open_clip, yt-dlp live in the
user site-packages). Downloads go through the skill's ytdl.py (one at a time across sessions, PO-token server).
After it: read catalog/sheet_*.png, pick shots with catalog.py strips, write plan_*.py (see pilot/plan_v8.py).
"""
import sys, os, glob, json, subprocess, shutil, re

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join((os.environ.get('PAE_SCRIPTS') or os.path.expanduser('~/.claude/skills/premiere-ae-editing/scripts')), 'media')
PY = sys.executable


def arg(name, default=None):
    a = sys.argv
    return a[a.index(name) + 1] if name in a else default


def run(cmd, **kw):
    print(">", " ".join(str(c) for c in cmd)[:220], flush=True)
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([str(c) for c in cmd], env=env, **kw)
    if r.returncode: raise SystemExit(f"step failed ({r.returncode}): {cmd[1] if len(cmd) > 1 else cmd}")


def ascii_name(i, path):
    stem = re.sub(r"[^a-z0-9]+", "_", os.path.splitext(os.path.basename(path))[0].lower()).strip("_")[:40]
    return f"f{i}_{stem}.mp4"


def main():
    d, subject = sys.argv[1], sys.argv[2]
    for sub in ("song", "footage", "catalog", "mattes/auto", "ae", "renders", "qa"): os.makedirs(os.path.join(d, sub), exist_ok=True)
    song_dir, foot = os.path.join(d, "song"), os.path.join(d, "footage")
    # ---- song
    src = arg("--song")
    wav = os.path.join(song_dir, "song.wav")
    if src and not os.path.exists(wav):
        if not os.path.exists(src):            # a YouTube id / url: download (audio is cut from the video file)
            run([PY, os.path.join(SKILL, "ytdl.py"), src, "--out", song_dir, "--max", "720"])
            vids = [f for f in glob.glob(os.path.join(song_dir, "*.mp4"))]
            if not vids: raise SystemExit("song download failed")
            src = max(vids, key=os.path.getmtime)
        run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vn", "-ac", "2", "-ar", "48000", wav])
    if os.path.exists(wav):
        w22 = os.path.join(song_dir, "song_22k.wav")
        if not os.path.exists(w22): run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-ac", "1", "-ar", "22050", w22])
        bj = os.path.join(song_dir, "beats.json")
        if not os.path.exists(bj): run([PY, os.path.join(SKILL, "beats.py"), w22, bj, "30"])
        wj = os.path.join(song_dir, "words.json")
        if not os.path.exists(wj): run([PY, os.path.join(SKILL, "hear.py"), wav, wj])
    # ---- footage
    ids = [x for x in (arg("--footage") or "").split(",") if x]
    if ids:
        tmp = os.path.join(foot, "_dl"); os.makedirs(tmp, exist_ok=True)
        run([PY, os.path.join(SKILL, "ytdl.py")] + ids + ["--out", tmp, "--max", arg("--max", "1080")])
        have = len(glob.glob(os.path.join(foot, "f*.mp4")))
        for i, f in enumerate(sorted(glob.glob(os.path.join(tmp, "*.mp4")))):
            dst = os.path.join(foot, ascii_name(have + i, f))
            if not os.path.exists(dst): shutil.move(f, dst)
    cat = os.path.join(d, "catalog")
    if glob.glob(os.path.join(foot, "f*.mp4")):
        if not os.path.exists(os.path.join(cat, "catalog.json")): run([PY, os.path.join(KIT, "tools", "catalog.py"), "build", foot, cat])
        cj = json.load(open(os.path.join(cat, "catalog.json")))
        if cj["shots"] and "scale" not in cj["shots"][0]: run([PY, os.path.join(KIT, "tools", "catalog.py"), "tag", cat])
        cj = json.load(open(os.path.join(cat, "catalog.json")))
        if cj["shots"] and "subj" not in cj["shots"][0]: run([PY, os.path.join(KIT, "tools", "catalog.py"), "idscore", cat, subject])
        n = len(cj["shots"])
        for k in range(0, n, 48):
            png = os.path.join(cat, f"sheet_{k // 48}.png")
            if not os.path.exists(png): run([PY, os.path.join(KIT, "tools", "catalog.py"), "sheet", cat, png, f"from:{k}", "48"])
        print(f"catalog: {n} shots, {sum(1 for s in json.load(open(os.path.join(cat, 'catalog.json')))['shots'] if s.get('subj', 0) >= 0.75)} show {subject} clearly")
    print("ready:", d)


if __name__ == "__main__":
    main()
