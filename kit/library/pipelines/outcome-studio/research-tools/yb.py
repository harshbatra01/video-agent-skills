"""Batch YouTube helper (stats only, no video downloads). Run: python -X utf8 yb.py <cmd> ...
  ids <id|url> [...]                 parallel watch-page read: date, views, likes, channel, subs
  tag <hashtag> [pages] [since]      hashtag Shorts page + continuations, then stats; since = YYYY-MM-DD filter
  q "<query>" [period] [pages] [n]   Shorts search (type Shorts, view sort) + continuations, stats for top n
  chan <@handle> [n]                 a channel's Shorts tab (latest first) with stats
Output: one line per video: date | views | likes | subs | channel | id | title
"""
import sys, re, json, base64, urllib.parse, urllib.request, datetime, concurrent.futures as cf
import vt

MON = {m: i for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}


def pdate(s):
    m = re.search(r"([A-Z][a-z]{2}) (\d{1,2}), (\d{4})", s or "")
    if not m:
        return None
    return datetime.date(int(m.group(3)), MON[m.group(1)], int(m.group(2)))


def stats(vid):
    try:
        d = vt.yv(vid)
    except Exception as e:
        return {"id": vid, "err": str(e)[:80]}
    d["d"] = pdate(d.get("date", ""))
    return d


def show(rows, since=None):
    out = []
    for r in rows:
        if "err" in r:
            print("ERR", r["id"], r["err"])
            continue
        if since and r.get("d") and r["d"] < since:
            continue
        out.append(r)
    out.sort(key=lambda r: (r.get("d") or datetime.date(1900, 1, 1)), reverse=True)
    for r in out:
        print(" | ".join([str(r.get("d")), r.get("views", "?"), r.get("likes", "?"), (r.get("subs", "?") or "?").replace(" subscribers", ""), r.get("by", "?"), r["id"], r.get("title", "")[:100]]))
    return out


def many(ids, since=None, workers=8):
    ids = list(dict.fromkeys(ids))
    with cf.ThreadPoolExecutor(workers) as ex:
        rows = list(ex.map(stats, ids))
    return show(rows, since)


def cont_pages(html, endpoint, pages):
    key = re.search(r'"INNERTUBE_API_KEY":"([^"]+)"', html).group(1)
    ver = re.search(r'"INNERTUBE_CLIENT_VERSION":"([^"]+)"', html).group(1)
    vd = re.search(r'"VISITOR_DATA":"([^"]+)"', html)
    vd = vd.group(1) if vd else ""
    found = vt.ylock(html)
    raw = html
    for _ in range(pages):
        toks = re.findall(r'"continuationCommand":\s*\{\s*"token":\s*"([^"]+)"', raw)
        if not toks:
            break
        body = json.dumps({"context": {"client": {"clientName": "WEB", "clientVersion": ver, "hl": "en", "gl": "US", "visitorData": vd}}, "continuation": toks[-1]}).encode()
        req = urllib.request.Request("https://www.youtube.com/youtubei/v1/%s?key=%s&prettyPrint=false" % (endpoint, key), data=body, headers={"Content-Type": "application/json", "User-Agent": vt.UA, "Cookie": "CONSENT=YES+1; SOCS=CAI", "X-Goog-Visitor-Id": vd, "X-Youtube-Client-Name": "1", "X-Youtube-Client-Version": ver, "Origin": "https://www.youtube.com"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                raw = r.read().decode("utf-8", "replace")
        except Exception as e:
            print("cont ERR", e)
            break
        new = [(m.group(1), "") for m in re.finditer(r'"entityId":"shorts-shelf-item-([\w-]{11})"', raw)] or vt.ylock(raw)
        if not new:
            # search results in json use slightly different spacing
            new = [(m.group(1), "") for m in re.finditer(r'"entityId":\s*"shorts-shelf-item-([\w-]{11})"', raw)]
            new += [(m.group(1), "") for m in re.finditer(r'"videoId":\s*"([\w-]{11})"', raw)]
        found += new
    seen, res = set(), []
    for vid, acc in found:
        if vid not in seen:
            seen.add(vid)
            res.append((vid, acc))
    return res


def tag(t, pages=2, since=None):
    html = vt.http("https://www.youtube.com/hashtag/" + urllib.parse.quote(t) + "/shorts", headers=vt.CK)
    res = cont_pages(html, "browse", pages)
    print("TAG", t, len(res), "items")
    return many([r[0] for r in res], since)


def q(query, period="month", pages=1, n=20):
    pm = {"hour": 1, "today": 2, "week": 3, "month": 4, "year": 5}
    f = b""
    if period in pm:
        f += bytes([0x08, pm[period]])
    f += bytes([0x10, 0x09])
    b = bytes([0x08, 0x03]) + bytes([0x12, len(f)]) + f
    sp = urllib.parse.quote(base64.b64encode(b).decode())
    html = vt.http("https://www.youtube.com/results?search_query=" + urllib.parse.quote(query) + "&sp=" + sp, headers=vt.CK)
    res = cont_pages(html, "search", pages)
    print("Q", query, period, len(res), "items")
    return many([r[0] for r in res[:n]])


def chan(h, n=15):
    html = vt.http(vt.ychan_url(h) + "/shorts", headers=vt.CK)
    res = vt.ylock(html)
    subs = re.search(r'([\d.,]+[KMB]? subscribers)', html)
    print("CHAN", h, subs.group(1) if subs else "subs?", len(res), "shorts on first page")
    return many([r[0] for r in res[:n]])


if __name__ == "__main__":
    cmd, a = sys.argv[1], sys.argv[2:]
    if cmd == "ids":
        many([re.search(r"([\w-]{11})$", x.rstrip("/").split("?")[0]).group(1) if "/" in x else x for x in a])
    elif cmd == "tag":
        since = datetime.date.fromisoformat(a[2]) if len(a) > 2 else None
        tag(a[0], int(a[1]) if len(a) > 1 else 2, since)
    elif cmd == "q":
        q(a[0], a[1] if len(a) > 1 else "month", int(a[2]) if len(a) > 2 else 1, int(a[3]) if len(a) > 3 else 20)
    elif cmd == "chan":
        chan(a[0], int(a[1]) if len(a) > 1 else 15)
