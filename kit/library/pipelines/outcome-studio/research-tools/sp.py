"""12-month top posts of an X or TikTok account via socialpruf.com (public page), then exact stats per post.
python -X utf8 sp.py <x|tiktok> <handle> [n] [nostats]
Prints the header metrics, similar accounts, then one line per top post:
  X:      date | views | likes | reposts | replies | quotes | saves | media | url | text   (fxtwitter)
  TikTok: date | plays | likes | comments | shares | saves | secs | url | caption        (tikwm)
Raw page saved to ../data/sp_<platform>_<handle>.html
"""
import sys, os, re, json, time, html as H, datetime, urllib.request, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def get(url, data=None, timeout=60):
    req = urllib.request.Request(url, data=data, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def page(platform, h):
    p = os.path.join(DATA, "sp_%s_%s.html" % (platform, h))
    s = get("https://socialpruf.com/%s/%s" % (platform, h))
    open(p, "w", encoding="utf-8").write(s)
    return s


def header(s):
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S)
    t = H.unescape(re.sub(r"<[^>]+>", "\n", t))
    lines = [x.strip() for x in t.split("\n") if x.strip()]
    out = {}
    for k in ("followers", "impressions", "views", "likes", "comments", "posts", "engagement", "Average per post"):
        if k in lines:
            i = lines.index(k)
            out[k] = lines[i + 1] if i + 1 < len(lines) else "?"
    rng = next((x for x in lines if re.match(r"[A-Z][a-z]{2} \d+, \d{4} - ", x)), "")
    return out, rng


def similar(s, platform):
    hs = re.findall(r'href="https://socialpruf.com/%s/([A-Za-z0-9_.]+)"' % platform, s)
    seen = []
    for x in hs:
        if x not in seen:
            seen.append(x)
    return seen


def ids(s):
    out = []
    for m in re.finditer(r"thumbnails/(\d+)", s):
        if m.group(1) not in out:
            out.append(m.group(1))
    return out


def xstat(i):
    try:
        j = json.loads(get("https://api.fxtwitter.com/status/" + i))
        t = j.get("tweet")
        if not t:
            return "ERR %s" % i
        med = (t.get("media") or {}).get("all") or []
        k = "+".join(sorted(set(m.get("type", "?") for m in med))) or "text"
        d = datetime.datetime.fromtimestamp(t.get("created_timestamp", 0), datetime.timezone.utc).strftime("%Y-%m-%d")
        return " | ".join(str(x) for x in [d, t.get("views"), t.get("likes"), t.get("reposts", t.get("retweets")), t.get("replies"), t.get("quotes"), t.get("bookmarks"), k, t.get("url"), (t.get("text") or "").replace("\n", " ")[:170]])
    except Exception as e:
        return "ERR %s %s" % (i, e)


def tstat(h, i):
    url = "https://www.tiktok.com/@%s/video/%s" % (h, i)
    for a in range(3):
        try:
            j = json.loads(get("https://www.tikwm.com/api/", data=urllib.parse.urlencode({"url": url, "hd": "0"}).encode()))
            if j.get("code") == 0:
                d = j["data"]
                dt = datetime.datetime.fromtimestamp(d.get("create_time", 0), datetime.timezone.utc).strftime("%Y-%m-%d")
                kind = "photo%d" % len(d.get("images")) if d.get("images") else "%ss" % d.get("duration")
                return " | ".join(str(x) for x in [dt, d.get("play_count"), d.get("digg_count"), d.get("comment_count"), d.get("share_count"), d.get("collect_count"), kind, url, (d.get("title") or "").replace("\n", " ")[:150]])
            time.sleep(1.5)
        except Exception as e:
            time.sleep(2)
    try:
        dt = datetime.datetime.fromtimestamp(int(i) >> 32, datetime.timezone.utc).strftime("%Y-%m-%d")
    except Exception:
        dt = "?"
    return "%s | (tikwm failed) | %s" % (dt, url)


if __name__ == "__main__":
    platform, h = sys.argv[1], sys.argv[2]
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 12
    nostats = len(sys.argv) > 4
    s = page(platform, h)
    hd, rng = header(s)
    print("=== %s @%s %s | %s" % (platform, h, rng, " | ".join("%s %s" % kv for kv in hd.items())))
    print("similar:", ", ".join(similar(s, platform)[:25]))
    for i in ids(s)[:n]:
        if nostats:
            print(i)
            continue
        print(xstat(i) if platform == "x" else tstat(h, i))
        time.sleep(1.1 if platform == "tiktok" else 0.4)
