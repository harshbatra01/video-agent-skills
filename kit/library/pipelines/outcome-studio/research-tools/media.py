"""Media fetch + contact sheets (media files only, nothing downloaded is ever executed).
python -X utf8 media.py tt <name> <tiktok url>          TikTok via tikwm: saves videos/<name>.mp4 (or photo slides as img/<name>_N.jpg) + data/<name>.json
python -X utf8 media.py yt <name> <youtube url|id>       YouTube via yt-dlp (<=720p mp4) into videos/<name>.mp4
python -X utf8 media.py sheet <name> [n] [cols]         contact sheet of n frames with timestamps -> sheets/<name>.jpg
python -X utf8 media.py imgs <name> <img1> <img2> ...   sheet from still images (photo posts) -> sheets/<name>.jpg
"""
import sys, os, json, glob, subprocess, urllib.request, urllib.parse, time, io

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.abspath(os.path.join(HERE, ".."))
VID, IMG, SH, DATA = [os.path.join(R, d) for d in ("videos", "img", "sheets", "data")]
for d in (VID, IMG, SH, DATA):
    os.makedirs(d, exist_ok=True)
FFMPEG = glob.glob(os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg*\*\bin\ffmpeg.exe"))[0]
FFPROBE = FFMPEG.replace("ffmpeg.exe", "ffprobe.exe")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def dl(url, path, ref=None):
    h = {"User-Agent": UA}
    if ref:
        h["Referer"] = ref
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=180) as r, open(path, "wb") as f:
        f.write(r.read())
    return path


def tt(name, url):
    data = urllib.parse.urlencode({"url": url, "hd": "0"}).encode()
    j = None
    for i in range(4):
        try:
            req = urllib.request.Request("https://www.tikwm.com/api/", data=data, headers={"User-Agent": UA})
            j = json.loads(urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace"))
            if j.get("code") == 0:
                break
        except Exception as e:
            print("retry", e)
        time.sleep(2 + i * 2)
    if not j or j.get("code") != 0:
        print("ERR", url, j and j.get("msg"))
        return
    d = j["data"]
    json.dump(d, open(os.path.join(DATA, name + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    imgs = d.get("images") or []
    if imgs:
        for k, u in enumerate(imgs, 1):
            dl(u, os.path.join(IMG, "%s_%d.jpg" % (name, k)))
        print("photo post", name, len(imgs), "slides")
    else:
        u = d.get("play") or d.get("wmplay")
        if u.startswith("/"):
            u = "https://www.tikwm.com" + u
        dl(u, os.path.join(VID, name + ".mp4"))
        print("video", name, d.get("duration"), "s")
    a = d.get("author") or {}
    print("@%s | %s plays | %s likes | %s comments | %s shares | %s saves | %ss | %s" % (a.get("unique_id"), d.get("play_count"), d.get("digg_count"), d.get("comment_count"), d.get("share_count"), d.get("collect_count"), d.get("duration"), (d.get("title") or "")[:120]))


def yt(name, url):
    out = os.path.join(VID, name + ".%(ext)s")
    cmd = [sys.executable, "-m", "yt_dlp", "-q", "--no-warnings", "--no-playlist", "-f", "b[height<=720][ext=mp4]/bv*[height<=720][ext=mp4]+ba[ext=m4a]/b", "--merge-output-format", "mp4", "--ffmpeg-location", os.path.dirname(FFMPEG), "-o", out, url]
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(r.stdout[-300:], r.stderr[-300:])
    print("saved", glob.glob(os.path.join(VID, name + ".*")))


def dur(path):
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", path], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except Exception:
        return 0.0


def sheet(name, n=12, cols=6):
    from PIL import Image, ImageDraw, ImageFont
    src = os.path.join(VID, name + ".mp4")
    D = dur(src)
    n = int(n)
    cols = int(cols)
    ts = [D * (i + 0.5) / n for i in range(n)]
    frames = []
    for t in ts:
        p = subprocess.run([FFMPEG, "-v", "error", "-ss", "%.2f" % t, "-i", src, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "mjpeg", "-q:v", "3", "-"], capture_output=True)
        try:
            frames.append((t, Image.open(io.BytesIO(p.stdout)).convert("RGB")))
        except Exception:
            pass
    if not frames:
        print("no frames", name)
        return
    w0, h0 = frames[0][1].size
    TW = 300 if h0 >= w0 else 420
    TH = int(TW * h0 / w0)
    LAB = 22
    rows = (len(frames) + cols - 1) // cols
    S = Image.new("RGB", (cols * (TW + 4), rows * (TH + LAB) + 26), (18, 18, 18))
    d = ImageDraw.Draw(S)
    try:
        f = ImageFont.truetype("arial.ttf", 16)
    except Exception:
        f = ImageFont.load_default()
    d.text((6, 4), "%s  (%.1fs)" % (name, D), fill=(255, 255, 0), font=f)
    for i, (t, im) in enumerate(frames):
        x = (i % cols) * (TW + 4)
        y = 26 + (i // cols) * (TH + LAB)
        S.paste(im.resize((TW, TH)), (x, y + LAB))
        d.text((x + 4, y + 2), "%.1fs" % t, fill=(255, 255, 255), font=f)
    out = os.path.join(SH, name + ".jpg")
    S.save(out, quality=82)
    print("sheet", out, S.size)


def imgs(name, paths):
    from PIL import Image, ImageDraw, ImageFont
    ims = []
    for p in paths:
        try:
            ims.append((os.path.basename(p), Image.open(p).convert("RGB")))
        except Exception as e:
            print("skip", p, e)
    TW = 360
    cols = min(4, len(ims))
    LAB = 22
    cells = []
    for nm, im in ims:
        w, h = im.size
        cells.append((nm, im.resize((TW, int(TW * h / w)))))
    rows = (len(cells) + cols - 1) // cols
    rh = [max(c[1].size[1] for c in cells[r * cols:(r + 1) * cols]) for r in range(rows)]
    S = Image.new("RGB", (cols * (TW + 4), sum(rh) + rows * LAB + 26), (18, 18, 18))
    d = ImageDraw.Draw(S)
    try:
        f = ImageFont.truetype("arial.ttf", 15)
    except Exception:
        f = ImageFont.load_default()
    d.text((6, 4), name, fill=(255, 255, 0), font=f)
    y = 26
    for r in range(rows):
        for c, (nm, im) in enumerate(cells[r * cols:(r + 1) * cols]):
            x = c * (TW + 4)
            d.text((x + 4, y + 2), nm[:44], fill=(255, 255, 255), font=f)
            S.paste(im, (x, y + LAB))
        y += rh[r] + LAB
    out = os.path.join(SH, name + ".jpg")
    S.save(out, quality=82)
    print("sheet", out, S.size)


if __name__ == "__main__":
    cmd, a = sys.argv[1], sys.argv[2:]
    if cmd == "tt":
        tt(a[0], a[1])
    elif cmd == "yt":
        yt(a[0], a[1])
    elif cmd == "sheet":
        sheet(a[0], *(a[1:3]))
    elif cmd == "imgs":
        imgs(a[0], a[1:])
