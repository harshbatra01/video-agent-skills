"""Research helper for file 24 (UGC to faceless). Run: python -X utf8 m.py <cmd> ...
  tt <tiktok url> [...]            tikwm stats + followers (urlebird) -> one JSON line each, appended to ../data/tt_stats.jsonl
  ubu <handle> [...]               urlebird user page: followers + recent videos (plays)
  ubt <hashtag> [...]              urlebird hashtag page: recent videos (plays)
  dl <name> <url>                  download media only to ../videos/<name>.mp4 (TikTok via tikwm play URL, else yt-dlp)
  sheet <name> [cols]              contact sheet with timestamps -> ../sheets/<name>.jpg
  asr <name> [...]                 faster-whisper transcript with timestamps -> ../data/asr_<name>.txt
Media files are never executed, only read by ffmpeg / whisper.
"""
import sys, os, re, json, time, glob, shutil, subprocess, datetime, urllib.request, urllib.parse, html as htmlmod

BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
VID, SHEET, DATA = (os.path.join(BASE, d) for d in ("videos", "sheets", "data"))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
FFMPEG = shutil.which("ffmpeg") or (glob.glob(os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg*\*\bin\ffmpeg.exe")) or [None])[0]
FFPROBE = shutil.which("ffprobe") or (FFMPEG[:-10] + "ffprobe.exe" if FFMPEG else None)


def http(url, data=None, headers=None, timeout=40):
    h = {"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"}
    if headers:
        h.update(headers)
    if isinstance(data, dict):
        data = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=data, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def knum(s):
    s = (s or "").strip().replace(",", "")
    m = re.match(r"([\d.]+)\s*([KMB]?)", s)
    if not m:
        return None
    return int(float(m.group(1)) * {"": 1, "K": 1e3, "M": 1e6, "B": 1e9}[m.group(2)])


def ub_cards(h):
    out = []
    for blk in re.split(r'<div class="thumb wc">', h)[1:]:
        user = re.search(r'urlebird\.com/user/([^/"]+)/', blk)
        vid = re.search(r'urlebird\.com/video/(?:[^"]*?-)?(\d{15,})/', blk)
        plays = re.search(r'fa-play"[^>]*></i>\s*([^<]+)<', blk)
        likes = re.search(r'fa-heart"[^>]*></i>\s*([^<]+)<', blk)
        age = re.search(r'fa-clock"[^>]*></i>\s*([^<]+)<', blk)
        cap = re.search(r'<div class="info3">.*?<span>(.*?)</span>', blk, re.S)
        if vid:
            out.append({"user": user.group(1) if user else "?", "id": vid.group(1), "plays": (plays.group(1).strip() if plays else "?"),
                        "likes": (likes.group(1).strip() if likes else "?"), "age": (age.group(1).strip() if age else "?"),
                        "cap": htmlmod.unescape(cap.group(1)).strip()[:110] if cap else ""})
    return out


_FOL = {}


def ub_user(handle, show=True):
    h = http("https://urlebird.com/user/%s/" % handle)
    st = {}
    for val, lab in re.findall(r'<b>([^<]+)</b>\s*<br[^>]*>\s*<span class="user">(\w+)</span>', h):
        st[lab] = val
    _FOL[handle] = st.get("followers")
    if show:
        print("=== @%s followers %s hearts %s videos %s" % (handle, st.get("followers"), st.get("hearts"), st.get("videos")))
        for c in ub_cards(h):
            print("  %s | plays %s | likes %s | %s | %s" % (c["id"], c["plays"], c["likes"], c["age"], c["cap"]))
    return st


def ub_tag(tag):
    h = http("https://urlebird.com/hash/%s/" % urllib.parse.quote(tag))
    cards = ub_cards(h)
    print("=== #%s %d recent" % (tag, len(cards)))
    for c in sorted(cards, key=lambda c: -(knum(c["plays"]) or 0)):
        print("  @%s | %s | plays %s | likes %s | %s | %s" % (c["user"], c["id"], c["plays"], c["likes"], c["age"], c["cap"]))


def tikwm(url):
    for attempt in range(4):
        try:
            j = json.loads(http("https://www.tikwm.com/api/", data={"url": url, "hd": "0"}))
        except Exception as e:
            j = {"code": -1, "msg": str(e)}
        if j.get("code") == 0:
            return j["data"]
        time.sleep(2.5)
    print("ERR tikwm", url, j.get("msg"))
    return None


def tt(url):
    d = tikwm(url)
    if not d:
        return None
    a = d.get("author", {}) or {}
    uid = a.get("unique_id")
    if uid and uid not in _FOL:
        try:
            ub_user(uid, show=False)
        except Exception as e:
            _FOL[uid] = "ERR"
    ci = d.get("commerce_info") or {}
    out = {"url": "https://www.tiktok.com/@%s/video/%s" % (uid, d.get("id")), "author": uid,
           "date": datetime.datetime.fromtimestamp(d.get("create_time", 0), datetime.timezone.utc).strftime("%Y-%m-%d"),
           "views": d.get("play_count"), "likes": d.get("digg_count"), "comments": d.get("comment_count"), "shares": d.get("share_count"),
           "saves": d.get("collect_count"), "dur": d.get("duration"), "followers": _FOL.get(uid),
           "branded": ci.get("branded_content_type"), "is_ad": d.get("is_ad"),
           "music": ((d.get("music_info") or {}).get("title") or "")[:60], "music_author": ((d.get("music_info") or {}).get("author") or "")[:40],
           "title": (d.get("title") or "").replace("\n", " ")[:160], "images": len(d.get("images") or [])}
    fo = knum(out["followers"]) if isinstance(out["followers"], str) else None
    out["ratio"] = round(out["views"] / fo, 2) if fo and out.get("views") else None
    with open(os.path.join(DATA, "tt_stats.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(out, ensure_ascii=False) + "\n")
    return out, d


def dl(name, url):
    dst = os.path.join(VID, name + ".mp4")
    if os.path.exists(dst) and os.path.getsize(dst) > 10000:
        print("exists", dst)
        return dst
    if "tiktok.com" in url:
        r = tt(url)
        if not r:
            return None
        out, d = r
        print(json.dumps(out, ensure_ascii=False))
        if d.get("images"):
            # photo carousel: save the images and the music, build a simple slideshow file for the sheet
            imgdir = os.path.join(VID, name + "_imgs")
            os.makedirs(imgdir, exist_ok=True)
            for i, iu in enumerate(d["images"]):
                urllib.request.urlretrieve(iu, os.path.join(imgdir, "%02d.jpg" % i))
            print("photo post, %d images -> %s" % (len(d["images"]), imgdir))
            return imgdir
        play = d.get("play") or d.get("wmplay")
        if play.startswith("/"):
            play = "https://www.tikwm.com" + play
        req = urllib.request.Request(play, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=120) as r, open(dst, "wb") as f:
            f.write(r.read())
    else:
        cmd = [sys.executable, "-m", "yt_dlp", "--no-playlist", "-f", "bv*[height<=1280]+ba/b", "--merge-output-format", "mp4",
               "-o", os.path.join(VID, name + ".%(ext)s"), url]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=300)
    if os.path.exists(dst):
        print("saved", dst, os.path.getsize(dst))
        return dst
    print("FAILED", name, url)
    return None


def probe(path):
    p = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration:stream=width,height,codec_type", "-of", "json", path],
                       capture_output=True, text=True)
    j = json.loads(p.stdout or "{}")
    dur = float(j.get("format", {}).get("duration", 0) or 0)
    w = h = 0
    for s in j.get("streams", []):
        if s.get("codec_type") == "video":
            w, h = s.get("width"), s.get("height")
    return dur, w, h


def sheet(name, cols=8, mini=False):
    from PIL import Image, ImageDraw, ImageFont
    src = os.path.join(VID, name + ".mp4")
    dur, w, h = probe(src)
    # dense at the start (hook), then spread across the rest
    ts = [0.0, 1.0, 2.0, 3.0] if mini else [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0]
    t = 4.5 if mini else 5.0
    step = max(1.5, (dur - t) / (8.0 if mini else 24.0))
    while t < dur - 0.3:
        ts.append(round(t, 1))
        t += step
    ts = [x for x in ts if x < max(dur - 0.05, 0.1)]
    if dur > 1 and dur - 0.4 not in ts:
        ts.append(round(dur - 0.4, 1))
    tw = 170 if mini else 240
    th = int(tw * (h / w)) if w else 426
    th = min(th, 460)
    rows = (len(ts) + cols - 1) // cols
    lab = 22
    sh = Image.new("RGB", (cols * (tw + 4), rows * (th + lab) + 30), (16, 16, 16))
    d = ImageDraw.Draw(sh)
    try:
        font = ImageFont.truetype("arialbd.ttf", 15)
        fsm = ImageFont.truetype("arial.ttf", 14)
    except Exception:
        font = fsm = ImageFont.load_default()
    d.text((6, 6), "%s  |  %.1f s  |  %dx%d" % (name, dur, w, h), fill=(255, 220, 90), font=fsm)
    tmp = os.path.join(DATA, "_frame.jpg")
    for i, t in enumerate(ts):
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-ss", "%.2f" % t, "-i", src, "-frames:v", "1", "-q:v", "3", tmp])
        x, y = (i % cols) * (tw + 4), 30 + (i // cols) * (th + lab)
        d.text((x + 4, y + 2), "%.1fs" % t, fill=(255, 255, 255), font=font)
        if os.path.exists(tmp):
            im = Image.open(tmp).convert("RGB")
            im = im.resize((tw, int(tw * im.height / im.width)))
            sh.paste(im.crop((0, 0, tw, th)), (x, y + lab))
            os.remove(tmp)
    out = os.path.join(SHEET, name + ("_mini" if mini else "") + ".jpg")
    sh.save(out, quality=82)
    print("sheet", out, sh.size, "frames", len(ts))


_MODEL = None


def asr(name):
    global _MODEL
    from faster_whisper import WhisperModel
    if _MODEL is None:
        try:
            _MODEL = WhisperModel("mobiuslabsgmbh/faster-whisper-large-v3-turbo", device="cuda", compute_type="float16")
        except Exception as e:
            print("cuda failed", e, "-> cpu small")
            _MODEL = WhisperModel("Systran/faster-whisper-small", device="cpu", compute_type="int8")
    import numpy as np
    src = os.path.join(VID, name + ".mp4")
    pcm = subprocess.run([FFMPEG, "-loglevel", "error", "-i", src, "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True).stdout
    audio = np.frombuffer(pcm, dtype=np.float32)
    if audio.size < 1600:
        print("=== asr", name, "no audio")
        return
    segs, info = _MODEL.transcribe(audio, vad_filter=True, beam_size=1)
    lines = ["%5.1f-%5.1f %s" % (s.start, s.end, s.text.strip()) for s in segs]
    txt = "lang %s (%.2f)\n" % (info.language, info.language_probability) + "\n".join(lines)
    open(os.path.join(DATA, "asr_%s.txt" % name), "w", encoding="utf-8").write(txt)
    print("=== asr", name)
    print(txt[:3000])


# ---------- urlebird pagination (the site's own "load more" calls) ----------
import http.cookiejar as _cookiejar
_CJ = _cookiejar.CookieJar()
_OP = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(_CJ))


def ub_get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
    with _OP.open(req, timeout=40) as r:
        return r.read().decode("utf-8", "replace")


def ub_post(action, data):
    body = urllib.parse.urlencode({"action": action, "data": json.dumps(data)}).encode()
    req = urllib.request.Request("https://urlebird.com/ajax/", data=body, headers={"User-Agent": UA, "X-Requested-With": "XMLHttpRequest",
                                                                                   "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"})
    with _OP.open(req, timeout=40) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def attr(h, btn, name):
    m = re.search(r'id="%s"[^>]*?data-%s="([^"]*)"' % (btn, name), h) or re.search(r'%s"[^>]*?data-%s="([^"]*)"' % (btn, name), h)
    return m.group(1) if m else None


def ub_search_all(q, pages=3):
    h = ub_get("https://urlebird.com/search/?q=" + urllib.parse.quote(q))
    cards = ub_cards(h)
    dq, dc, dx = attr(h, "search_load_more", "q"), attr(h, "search_load_more", "c"), attr(h, "search_load_more", "x")
    for _ in range(pages - 1):
        if not dq:
            break
        try:
            j = ub_post("search", {"q": dq, "c": dc, "x": dx, "lang": ""})
        except Exception as e:
            print("  load more ERR", e)
            break
        if not j.get("thumbs"):
            break
        cards += ub_cards('<div class="thumb wc">' + j["thumbs"].split('<div class="thumb wc">', 1)[-1] if '<div class="thumb wc">' in j["thumbs"] else j["thumbs"])
        cards += []
        dq, dc, dx = j.get("q"), j.get("c"), j.get("x")
        if j.get("has_more") is False:
            break
        time.sleep(1.0)
    return cards


def ub_user_all(handle, pages=3):
    h = ub_get("https://urlebird.com/user/%s/" % handle)
    st = {lab: val for val, lab in re.findall(r'<b>([^<]+)</b>\s*<br[^>]*>\s*<span class="user">(\w+)</span>', h)}
    _FOL[handle] = st.get("followers")
    cards = ub_cards(h)
    uid, sec, cur, pg, x = (attr(h, "load_more", k) for k in ("user-id", "sec-uid", "cursor", "page", "x"))
    for _ in range(pages - 1):
        if not (uid and sec and cur):
            break
        try:
            j = ub_post("user", {"user_id": uid, "sec_uid": sec, "cursor": cur, "lang": "", "page": pg, "x": x})
        except Exception as e:
            print("  load more ERR", e)
            break
        if not j.get("thumbs") or j.get("cursor") is None:
            break
        cards += ub_cards(j["thumbs"])
        cur, pg, x, uid, sec = j.get("cursor"), j.get("page"), j.get("x"), j.get("u", uid), j.get("s", sec)
        if j.get("has_more") in (0, False, "0"):
            break
        time.sleep(1.0)
    return st, cards


def show_cards(title, cards, n=40, fol=None):
    seen, rows = set(), []
    for c in cards:
        if c["id"] in seen:
            continue
        seen.add(c["id"])
        rows.append(c)
    rows.sort(key=lambda c: -(knum(c["plays"]) or 0))
    print("=== %s (%d videos)%s" % (title, len(rows), (" followers %s" % fol) if fol else ""))
    for c in rows[:n]:
        print("  @%s | %s | plays %s | likes %s | %s | %s" % (c["user"], c["id"], c["plays"], c["likes"], c["age"], c["cap"]))
    return rows


if __name__ == "__main__":
    cmd, a = sys.argv[1], sys.argv[2:]
    if cmd == "tt":
        for u in a:
            r = tt(u)
            if r:
                print(json.dumps(r[0], ensure_ascii=False))
            time.sleep(1.0)
    elif cmd == "ubu":
        for x in a:
            try:
                ub_user(x)
            except Exception as e:
                print("ERR", x, e)
            time.sleep(1.0)
    elif cmd == "ubt":
        for x in a:
            try:
                ub_tag(x)
            except Exception as e:
                print("ERR", x, e)
            time.sleep(1.0)
    elif cmd == "dl":
        dl(a[0], a[1])
    elif cmd == "sheet":
        sheet(a[0], int(a[1]) if len(a) > 1 else 8)
    elif cmd == "msheet":
        for x in a:
            sheet(x, 7, mini=True)
    elif cmd == "ubs":
        pages = int(a[0]); 
        for q in a[1:]:
            try:
                show_cards("search: " + q, ub_search_all(q, pages), 30)
            except Exception as e:
                print("ERR", q, e)
            time.sleep(1.5)
    elif cmd == "ubua":
        pages = int(a[0])
        for hnd in a[1:]:
            try:
                st, cards = ub_user_all(hnd, pages)
                show_cards("@" + hnd, cards, 12, "%s hearts %s videos %s" % (st.get("followers"), st.get("hearts"), st.get("videos")))
            except Exception as e:
                print("ERR", hnd, e)
            time.sleep(1.5)
    elif cmd == "asr":
        for x in a:
            asr(x)


