"""Video-metadata helper (no video downloads).
Usage (run with: python -X utf8 vt.py ...):
  tt <tiktok video url> [...]    single video stats via tikwm + follower count
  ttu <unique_id> [...]          TikTok user stats via tikwm
  tq "keywords" [n]              tikwm keyword search
  tposts <unique_id> [n]         tikwm user posts
  yv <video id or url> [...]     YouTube video: title, views, date, length, channel, subs
  ys <@handle|url> [n]           YouTube /shorts tab: videos with views
  yc <@handle|url>               YouTube channel header
  yq "query" [views|rel] [year|month|week|today|any] [1|0]   YouTube search (sorted, short filter)
  x <tweet id or url> [...]      X post via syndication
"""
import sys, json, re, time, urllib.request, urllib.parse, urllib.error, datetime, base64

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
CK = {"Cookie": "CONSENT=YES+1; SOCS=CAI"}


def http(url, data=None, headers=None, timeout=30):
    h = {"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"}
    if headers:
        h.update(headers)
    if data is not None and isinstance(data, dict):
        data = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=data, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", "replace")[:200]
        except Exception:
            pass
        raise RuntimeError("HTTP %s %s" % (e.code, body))


def tt(url):
    j = None
    for attempt in range(3):
        try:
            raw = http("https://www.tikwm.com/api/", data={"url": url, "hd": "0"})
            j = json.loads(raw)
            if j.get("code") == 0:
                break
            if "Limit" in str(j.get("msg", "")):
                time.sleep(2)
                continue
            print("ERR", url, j.get("msg"))
            return None
        except Exception as e:
            print("ERR", url, e)
            time.sleep(2)
    if not j or j.get("code") != 0:
        return None
    d = j["data"]
    a = d.get("author", {})
    ct = datetime.datetime.fromtimestamp(d.get("create_time", 0), datetime.timezone.utc).strftime("%Y-%m-%d")
    out = {
        "url": url,
        "author": a.get("unique_id"),
        "nick": a.get("nickname"),
        "date": ct,
        "views": d.get("play_count"),
        "likes": d.get("digg_count"),
        "comments": d.get("comment_count"),
        "shares": d.get("share_count"),
        "saves": d.get("collect_count"),
        "dur": d.get("duration"),
        "title": (d.get("title") or "")[:140],
        "music": (d.get("music_info", {}) or {}).get("title"),
        "music_author": (d.get("music_info", {}) or {}).get("author"),
    }
    try:
        out.update(tprof(a.get("unique_id", "")))
    except Exception as e:
        out["followers"] = "ERR " + str(e)[:40]
    return out


_PROF = {}


def tprof(uid):
    """follower count via r.jina.ai reader (html format) on the TikTok profile page"""
    if uid in _PROF:
        return _PROF[uid]
    h = http("https://r.jina.ai/https://www.tiktok.com/@" + uid, headers={"X-Return-Format": "html"}, timeout=60)
    r = {}
    m = re.search(r'"stats":\{"followerCount":(\d+),"followingCount":\d+,"heart":\d+,"heartCount":(\d+),"videoCount":(\d+)', h)
    if m:
        r = {"followers": int(m.group(1)), "hearts_total": int(m.group(2)), "videos_total": int(m.group(3))}
    else:
        r = {"followers": "n/a"}
    _PROF[uid] = r
    return r


def ttu(uid):
    try:
        u = json.loads(http("https://www.tikwm.com/api/user/info?unique_id=" + urllib.parse.quote(uid)))
        if u.get("code") == 0:
            st = u["data"]["stats"]
            us = u["data"]["user"]
            return {"user": uid, "nick": us.get("nickname"), "followers": st.get("followerCount"), "videos": st.get("videoCount"), "hearts": st.get("heartCount"), "bio": (us.get("signature") or "")[:120]}
        return {"user": uid, "err": u.get("msg")}
    except Exception as e:
        return {"user": uid, "err": str(e)[:120]}


def ytjson(html, name):
    m = re.search(name + r"\s*=\s*", html)
    if not m:
        return None
    try:
        obj, _ = json.JSONDecoder().raw_decode(html[m.end():])
        return obj
    except Exception:
        return None


def yv(v):
    m = re.search(r"(?:v=|shorts/|youtu\.be/)([\w-]{11})", v)
    vid = m.group(1) if m else v
    html = http("https://www.youtube.com/watch?v=" + vid, headers=CK)
    out = {"id": vid}
    try:
        oe = json.loads(http("https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote("https://www.youtube.com/watch?v=" + vid)))
        out["title"] = oe.get("title", "")[:110]
        out["by"] = oe.get("author_name", "") + " " + oe.get("author_url", "").replace("https://www.youtube.com/", "")
    except Exception as e:
        out["title"] = "oembed ERR " + str(e)[:50]
    for m in re.finditer(r'"factoidRenderer":\{"value":\{"simpleText":"([^"]+)"\},"label":\{"simpleText":"([^"]+)"', html):
        if m.group(2) in ("Views", "Likes"):
            out[m.group(2).lower()] = m.group(1)
    if "views" not in out:
        s = re.search(r'"shortViewCount":\{"simpleText":"([^"]+)"', html)
        if s:
            out["views"] = s.group(1)
    d = re.search(r'"dateText":\{"simpleText":"([^"]+)"', html)
    if d:
        out["date"] = d.group(1)
    l = re.search(r'"lengthSeconds":"(\d+)"', html)
    if l:
        out["len"] = l.group(1)
    m2 = re.search(r'"subscriberCountText":\{"accessibility":\{"accessibilityData":\{"label":"([^"]+)"', html)
    if not m2:
        m2 = re.search(r'"subscriberCountText":\{"simpleText":"([^"]+)"', html)
    if m2:
        out["subs"] = m2.group(1)
    return out


def ychan_url(h):
    if h.startswith("http"):
        return h.rstrip("/")
    if h.startswith("@"):
        return "https://www.youtube.com/" + h
    return "https://www.youtube.com/@" + h


def yc(h):
    html = http(ychan_url(h), headers=CK)
    out = {"chan": h}
    t = re.search(r"<title>(.*?)</title>", html)
    out["title"] = t.group(1) if t else None
    for pat, key in [(r'"subscriberCountText":"([^"]+)"', "subs"), (r'"videosCountText":"([^"]+)"', "videos"), (r'([\d.,]+[KM]? subscribers)', "subs2"), (r'"content":"([\d.,KM]+ videos)"', "videos2")]:
        m = re.search(pat, html)
        if m:
            out[key] = m.group(1)
    return out


def ylock(html):
    res = []
    for m in re.finditer(r'"shortsLockupViewModel":\s*\{\s*"entityId":\s*"shorts-shelf-item-([\w-]{11})",\s*"accessibilityText":\s*"((?:[^"\\]|\\.)*)"', html):
        res.append((m.group(1), m.group(2).encode().decode("unicode_escape", "ignore") if "\\u" in m.group(2) else m.group(2)))
    return res


def ys(h, n=12):
    html = http(ychan_url(h) + "/shorts", headers=CK)
    res = ylock(html)
    t = re.search(r"<title>(.*?)</title>", html)
    subs = re.search(r'([\d.,]+[KM]? subscribers)', html)
    print("CHAN", h, "|", t.group(1) if t else None, "|", subs.group(1) if subs else "subs?")
    for r in res[:n]:
        print(r[0], "|", r[1][:150])
    return res


def yh(tag, n=15):
    html = http("https://www.youtube.com/hashtag/" + urllib.parse.quote(tag) + "/shorts", headers=CK)
    res = ylock(html)
    print("HASHTAG", tag, len(res))
    for r in res[:n]:
        print(r[0], "|", r[1][:150])
    return res


def yq(query, sort="views", period="year", short=True, n=15):
    pm = {"hour": 1, "today": 2, "week": 3, "month": 4, "year": 5}
    f = b""
    if period in pm:
        f += bytes([0x08, pm[period]])
    f += bytes([0x10, 0x01])
    if short:
        f += bytes([0x18, 0x01])
    b = b""
    if sort == "views":
        b += bytes([0x08, 0x03])
    b += bytes([0x12, len(f)]) + f
    sp = urllib.parse.quote(base64.b64encode(b).decode())
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(query) + "&sp=" + sp
    html = http(url, headers=CK)
    out = []
    for m in re.finditer(r'"videoRenderer":\{"videoId":"([\w-]{11})"', html):
        seg = html[m.start(): m.start() + 7000]
        title = re.search(r'"title":\{"runs":\[\{"text":"((?:[^"\\]|\\.)*)"', seg)
        views = re.search(r'"viewCountText":\{"simpleText":"([^"]*)"', seg)
        pub = re.search(r'"publishedTimeText":\{"simpleText":"([^"]*)"', seg)
        ln = re.search(r'"lengthText":\{"accessibility":\{"accessibilityData":\{"label":"[^"]*"\}\},"simpleText":"([^"]*)"', seg)
        ch = re.search(r'"ownerText":\{"runs":\[\{"text":"((?:[^"\\]|\\.)*)"', seg)
        hd = re.search(r'"canonicalBaseUrl":"(/@[^"]+)"', seg)
        out.append((m.group(1), (title.group(1) if title else "")[:90], views.group(1) if views else "", pub.group(1) if pub else "", ln.group(1) if ln else "", ch.group(1) if ch else "", hd.group(1) if hd else ""))
    # Shorts shelf items
    for vid, acc in ylock(html):
        out.append((vid, acc[:150], "", "SHELF", "short", "", ""))
    seen = set()
    res = []
    for o in out:
        if o[0] in seen:
            continue
        seen.add(o[0])
        res.append(o)
    for o in res[:n]:
        print(" | ".join(o))
    if not res:
        print("NO RESULTS (len html %d)" % len(html))
    return res


def ysrch(query, n=14):
    """default (unfiltered) YouTube search: videos + Shorts shelf"""
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(query)
    html = http(url, headers=CK)
    seen = set()
    rows = []
    for m in re.finditer(r'"videoRenderer":\{"videoId":"([\w-]{11})"', html):
        seg = html[m.start(): m.start() + 7000]
        title = re.search(r'"title":\{"runs":\[\{"text":"((?:[^"\\]|\\.)*)"', seg)
        views = re.search(r'"viewCountText":\{"simpleText":"([^"]*)"', seg)
        pub = re.search(r'"publishedTimeText":\{"simpleText":"([^"]*)"', seg)
        ch = re.search(r'"ownerText":\{"runs":\[\{"text":"((?:[^"\\]|\\.)*)"', seg)
        hd = re.search(r'"canonicalBaseUrl":"(/@[^"]+)"', seg)
        if m.group(1) in seen:
            continue
        seen.add(m.group(1))
        rows.append("V %s | %s | %s | %s | %s %s" % (m.group(1), (title.group(1) if title else "")[:80], views.group(1) if views else "", pub.group(1) if pub else "", ch.group(1) if ch else "", hd.group(1) if hd else ""))
    for vid, acc in ylock(html):
        if vid in seen:
            continue
        seen.add(vid)
        rows.append("S %s | %s" % (vid, acc[:140]))
    for r in rows[:n]:
        print(r)
    if not rows:
        print("NO RESULTS")


def yss(query, sort="views", period="year", n=12):
    """YouTube Shorts-only search (type 9), sorted by view count, period filter"""
    pm = {"hour": 1, "today": 2, "week": 3, "month": 4, "year": 5}
    f = b""
    if period in pm:
        f += bytes([0x08, pm[period]])
    f += bytes([0x10, 0x09])
    b = bytes([0x12, len(f)]) + f
    sp = urllib.parse.quote(base64.b64encode(b).decode())
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(query) + "&sp=" + sp
    html = http(url, headers=CK)
    res = ylock(html)

    def vnum(acc):
        m = re.search(r"([\d.,]+) (thousand|million|billion)? ?views", acc)
        if not m:
            return 0
        x = float(m.group(1).replace(",", ""))
        return x * {"thousand": 1e3, "million": 1e6, "billion": 1e9, None: 1}[m.group(2)]

    res.sort(key=lambda r: -vnum(r[1]))
    print("=== %s [%s] %d found" % (query, period, len(res)))
    for vid, acc in res[:n]:
        print(vid, "|", acc[:125])
    if not res:
        print("NO RESULTS")


def tq(keywords, n=12):
    raw = http("https://www.tikwm.com/api/feed/search", data={"keywords": keywords, "count": str(n), "cursor": "0", "web": "1", "hd": "0"})
    j = json.loads(raw)
    if j.get("code") != 0:
        print("ERR", j.get("msg"))
        return
    for v in j["data"].get("videos", []):
        a = v.get("author", {})
        d = datetime.datetime.fromtimestamp(v.get("create_time", 0), datetime.timezone.utc).strftime("%Y-%m-%d")
        print("%s | @%s | views %s | likes %s | shares %s | dur %s | %s | https://www.tiktok.com/@%s/video/%s" % (d, a.get("unique_id"), v.get("play_count"), v.get("digg_count"), v.get("share_count"), v.get("duration"), (v.get("title") or "")[:80].replace("\n", " "), a.get("unique_id"), v.get("video_id")))


def tposts(uid, n=20):
    raw = http("https://www.tikwm.com/api/user/posts", data={"unique_id": uid, "count": str(n), "cursor": "0", "hd": "0"})
    j = json.loads(raw)
    if j.get("code") != 0:
        print("ERR", j.get("msg"))
        return
    for v in j["data"].get("videos", []):
        d = datetime.datetime.fromtimestamp(v.get("create_time", 0), datetime.timezone.utc).strftime("%Y-%m-%d")
        print("%s | views %s | likes %s | shares %s | saves %s | dur %s | %s | %s" % (d, v.get("play_count"), v.get("digg_count"), v.get("share_count"), v.get("collect_count"), v.get("duration"), (v.get("title") or "")[:70].replace("\n", " "), v.get("video_id")))


def x(i):
    m = re.search(r"status/(\d+)", i)
    tid = m.group(1) if m else i
    j = json.loads(http("https://cdn.syndication.twimg.com/tweet-result?id=%s&token=a" % tid))
    u = j.get("user", {})
    return {
        "id": tid,
        "user": u.get("screen_name"),
        "date": j.get("created_at"),
        "likes": j.get("favorite_count"),
        "replies": j.get("conversation_count"),
        "text": (j.get("text") or "")[:160],
        "video": bool(j.get("video")),
    }


if __name__ == "__main__":
    cmd = sys.argv[1]
    args = sys.argv[2:]
    if cmd == "tt":
        for a in args:
            print(json.dumps(tt(a), ensure_ascii=False))
            time.sleep(1.2)
    elif cmd == "ttu":
        for a in args:
            print(json.dumps(ttu(a), ensure_ascii=False))
            time.sleep(1.2)
    elif cmd == "yv":
        for a in args:
            try:
                print(json.dumps(yv(a), ensure_ascii=False))
            except Exception as e:
                print("ERR", a, e)
    elif cmd == "yc":
        for a in args:
            try:
                print(json.dumps(yc(a), ensure_ascii=False))
            except Exception as e:
                print("ERR", a, e)
    elif cmd == "ys":
        ys(args[0], int(args[1]) if len(args) > 1 else 12)
    elif cmd == "yss":
        # yss "query" [period] [n]
        for q in args[:1]:
            try:
                yss(q, "views", args[1] if len(args) > 1 else "year", int(args[2]) if len(args) > 2 else 12)
            except Exception as e:
                print("ERR", q, e)
    elif cmd == "ysr":
        for a in args:
            print("=== " + a)
            try:
                ysrch(a)
            except Exception as e:
                print("ERR", a, e)
    elif cmd == "yh":
        for a in args:
            try:
                yh(a, 15)
            except Exception as e:
                print("ERR", a, e)
    elif cmd == "yq":
        q = args[0]
        sort = args[1] if len(args) > 1 else "views"
        period = args[2] if len(args) > 2 else "year"
        short = (args[3] != "0") if len(args) > 3 else True
        yq(q, sort, period, short)
    elif cmd == "tq":
        try:
            tq(args[0], int(args[1]) if len(args) > 1 else 12)
        except Exception as e:
            print("ERR", e)
    elif cmd == "tposts":
        try:
            tposts(args[0], int(args[1]) if len(args) > 1 else 20)
        except Exception as e:
            print("ERR", e)
    elif cmd == "x":
        for a in args:
            try:
                print(json.dumps(x(a), ensure_ascii=False))
            except Exception as e:
                print("ERR", a, e)
