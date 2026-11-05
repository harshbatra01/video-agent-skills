"""Download a TikTok or YouTube video (media only) and build a timestamped contact sheet.
python -I -X utf8 grab.py <name> <url> [cols] [maxframes]
  TikTok: tikwm single-video API -> mp4 (or photo-mode images) + meta json
  YouTube: yt-dlp (low-res mp4 + m4a) + info json
Writes: videos/<name>.mp4 (or videos/<name>_NN.jpg), data/meta_<name>.json, sheets/<name>.jpg
Never executes anything it downloads.
"""
import sys, os, json, re, time, subprocess, shutil, urllib.request, urllib.parse, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import vt
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(HERE)
VID = os.path.join(ROOT, "videos")
SHEETS = os.path.join(ROOT, "sheets")
DATA = os.path.join(ROOT, "data")
FR = os.path.join(ROOT, "frames")
FFMPEG = shutil.which("ffmpeg")
FFPROBE = shutil.which("ffprobe")
UA = vt.UA


def dl(url, path):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://www.tikwm.com/"})
    with urllib.request.urlopen(req, timeout=120) as r, open(path, "wb") as f:
        shutil.copyfileobj(r, f)


def tiktok(name, url):
    j = None
    for _ in range(4):
        try:
            j = json.loads(vt.http("https://www.tikwm.com/api/", data={"url": url, "hd": "0"}, timeout=60))
            if j.get("code") == 0:
                break
        except Exception as e:
            j = {"code": -1, "msg": str(e)}
        time.sleep(2.5)
    if not j or j.get("code") != 0:
        raise RuntimeError("tikwm failed: %s" % (j or {}).get("msg"))
    d = j["data"]
    a = d.get("author", {}) or {}
    mi = d.get("music_info", {}) or {}
    meta = {"platform": "tiktok", "url": url, "author": a.get("unique_id"), "nick": a.get("nickname"),
            "date": datetime.datetime.fromtimestamp(d.get("create_time", 0), datetime.timezone.utc).strftime("%Y-%m-%d"),
            "views": d.get("play_count"), "likes": d.get("digg_count"), "comments": d.get("comment_count"),
            "shares": d.get("share_count"), "saves": d.get("collect_count"), "duration": d.get("duration"),
            "title": d.get("title"), "music": mi.get("title"), "music_author": mi.get("author"), "music_original": mi.get("original"),
            "is_photo": bool(d.get("images"))}
    files = []
    if d.get("images"):
        for i, im in enumerate(d["images"]):
            p = os.path.join(VID, "%s_%02d.jpg" % (name, i + 1))
            dl(im, p)
            files.append(p)
        meta["n_images"] = len(files)
    else:
        play = d.get("play") or d.get("wmplay")
        if play.startswith("/"):
            play = "https://www.tikwm.com" + play
        p = os.path.join(VID, name + ".mp4")
        dl(play, p)
        files.append(p)
    return meta, files


def youtube(name, url):
    out = os.path.join(VID, name + ".%(ext)s")
    info = os.path.join(DATA, "yt_" + name)
    cmd = [sys.executable, "-m", "yt_dlp", "--no-playlist", "--no-progress", "-f", "135+140/134+140/136+140/bv*[height<=960]+ba/b",
           "--merge-output-format", "mp4", "-o", out, "--write-info-json", "--no-write-comments", url]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    p = os.path.join(VID, name + ".mp4")
    js = os.path.join(VID, name + ".info.json")
    meta = {"platform": "youtube", "url": url}
    if os.path.exists(js):
        i = json.load(open(js, encoding="utf-8"))
        meta.update({"author": i.get("uploader_id") or i.get("channel"), "channel": i.get("channel"), "subs": i.get("channel_follower_count"),
                     "date": i.get("upload_date"), "views": i.get("view_count"), "likes": i.get("like_count"), "comments": i.get("comment_count"),
                     "duration": i.get("duration"), "title": i.get("title"), "description": (i.get("description") or "")[:500],
                     "track": i.get("track"), "artist": i.get("artist"), "width": i.get("width"), "height": i.get("height")})
        os.replace(js, os.path.join(DATA, "yt_info_%s.json" % name))
    if not os.path.exists(p):
        raise RuntimeError("yt-dlp failed: " + (r.stderr or r.stdout)[-400:])
    return meta, [p]


def duration(p):
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", p], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except Exception:
        return 0.0


def has_audio(p):
    r = subprocess.run([FFPROBE, "-v", "error", "-select_streams", "a", "-show_entries", "stream=codec_name", "-of", "csv=p=0", p], capture_output=True, text=True)
    return bool(r.stdout.strip())


def times(dur, maxframes):
    ts = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    ts = [t for t in ts if t < dur - 0.05]
    rest = maxframes - len(ts)
    if dur > 3.5 and rest > 0:
        step = (dur - 3.2) / rest
        ts += [round(3.0 + step * (k + 1), 1) for k in range(rest)]
    ts = sorted(set(min(t, max(0, dur - 0.15)) for t in ts))
    return ts


def frames(name, p, ts, width=240):
    d = os.path.join(FR, name)
    os.makedirs(d, exist_ok=True)
    out = []
    for t in ts:
        f = os.path.join(d, "f_%06.2f.jpg" % t)
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-ss", "%.2f" % t, "-i", p, "-frames:v", "1", "-vf", "scale=%d:-2" % width, "-q:v", "3", f], capture_output=True)
        if os.path.exists(f):
            out.append((t, f))
    return out


def sheet(name, items, title, cols=5, tw=240):
    ims = []
    for t, f in items:
        try:
            ims.append((t, Image.open(f).convert("RGB")))
        except Exception:
            pass
    if not ims:
        return None
    th = max(im.size[1] * tw // im.size[0] for _, im in ims)
    lab = 20
    rows = (len(ims) + cols - 1) // cols
    W, Hh = cols * (tw + 4), 34 + rows * (th + lab)
    S = Image.new("RGB", (W, Hh), (18, 18, 18))
    d = ImageDraw.Draw(S)
    try:
        font = ImageFont.truetype("arial.ttf", 15)
        fb = ImageFont.truetype("arialbd.ttf", 15)
    except Exception:
        font = fb = ImageFont.load_default()
    d.text((6, 8), title[:150], fill=(255, 255, 255), font=fb)
    for k, (t, im) in enumerate(ims):
        x, y = (k % cols) * (tw + 4), 34 + (k // cols) * (th + lab)
        im = im.resize((tw, im.size[1] * tw // im.size[0]))
        S.paste(im, (x, y + lab))
        d.text((x + 4, y + 2), ("%.1fs" % t) if isinstance(t, float) else str(t), fill=(255, 220, 60), font=fb)
    p = os.path.join(SHEETS, name + ".jpg")
    S.save(p, quality=82)
    return p


def main():
    name, url = sys.argv[1], sys.argv[2]
    cols = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    maxf = int(sys.argv[4]) if len(sys.argv) > 4 else 20
    for x in (VID, SHEETS, DATA, FR):
        os.makedirs(x, exist_ok=True)
    if "tiktok.com" in url:
        meta, files = tiktok(name, url)
    else:
        meta, files = youtube(name, url)
    if meta.get("is_photo"):
        items = [("slide %d" % (i + 1), f) for i, f in enumerate(files)]
        # shrink copies for the sheet
        small = []
        for lab, f in items:
            im = Image.open(f).convert("RGB")
            sp = os.path.join(FR, name + "_" + os.path.basename(f))
            os.makedirs(os.path.dirname(sp), exist_ok=True)
            im.resize((240, im.size[1] * 240 // im.size[0])).save(sp, quality=85)
            small.append((lab, sp))
        items = small
        meta["sheet_note"] = "photo mode, %d slides" % len(files)
    else:
        dur = duration(files[0])
        meta["file_duration"] = round(dur, 2)
        meta["has_audio"] = has_audio(files[0])
        items = frames(name, files[0], times(dur, maxf))
    title = "%s | @%s | %s | %s views | %ss | %s" % (name, meta.get("author"), meta.get("date"), "{:,}".format(meta.get("views") or 0), meta.get("duration"), (meta.get("music") or meta.get("track") or "")[:40])
    sp = sheet(name, items, title, cols)
    meta["sheet"] = sp
    json.dump(meta, open(os.path.join(DATA, "meta_%s.json" % name), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: meta.get(k) for k in ("author", "date", "views", "likes", "shares", "duration", "music", "music_author", "track", "subs", "title", "is_photo", "has_audio", "sheet")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
