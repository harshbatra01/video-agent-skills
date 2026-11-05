"""Popular Shorts of a YouTube channel (InnerTube browse continuation) + subscriber count.
python -X utf8 ysp.py @handle [@handle2 ...] [-n 8]
"""
import re, sys, json, urllib.request
import vt


def chan_popular(h, n=8, tab="shorts", chip="Popular"):
    url = vt.ychan_url(h) + "/" + tab
    html = vt.http(url, headers=vt.CK)
    title = re.search(r"<title>(.*?)</title>", html)
    title = title.group(1) if title else "?"
    subs = re.search(r'([\d.,]+[KMB]? subscribers)', html)
    vids = re.search(r'([\d.,]+[KMB]? videos)', html)
    print("CHAN %s | %s | %s | %s" % (h, title, subs.group(1) if subs else "subs?", vids.group(1) if vids else "videos?"))
    key = re.search(r'"INNERTUBE_API_KEY":"([^"]+)"', html).group(1)
    ver = re.search(r'"INNERTUBE_CLIENT_VERSION":"([^"]+)"', html).group(1)
    tok = None
    for m in re.finditer(r'"text":"%s"' % chip, html):
        seg = html[max(0, m.start() - 200): m.start() + 1200]
        t = re.search(r'"token":"([^"]+)"', seg)
        if t:
            tok = t.group(1)
            break
    if not tok:
        print("  no %s chip; showing page default list" % chip)
        res = vt.ylock(html) if tab == "shorts" else []
        for r in res[:n]:
            print("  ", r[0], "|", r[1][:140])
        return
    body = json.dumps({"context": {"client": {"clientName": "WEB", "clientVersion": ver, "hl": "en", "gl": "US"}}, "continuation": tok}).encode()
    req = urllib.request.Request("https://www.youtube.com/youtubei/v1/browse?key=" + key, data=body, headers={"Content-Type": "application/json", "User-Agent": vt.UA, "Cookie": "CONSENT=YES+1; SOCS=CAI"})
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read().decode("utf-8", "replace")
    res = vt.ylock(raw)
    if not res:
        # long-form tab fallback: videoRenderer
        for m in re.finditer(r'"videoId":"([\w-]{11})".{0,1500}?"title":\{"runs":\[\{"text":"((?:[^"\\]|\\.)*)"', raw, re.S):
            res.append((m.group(1), m.group(2)))
    for r in res[:n]:
        print("  ", r[0], "|", r[1][:140])


if __name__ == "__main__":
    args = [a for a in sys.argv[1:]]
    n = 8
    if "-n" in args:
        i = args.index("-n")
        n = int(args[i + 1])
        del args[i: i + 2]
    for a in args:
        try:
            chan_popular(a, n)
        except Exception as e:
            print("ERR", a, e)
