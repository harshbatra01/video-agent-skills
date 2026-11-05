"""Recent posts of X accounts via the public syndication timeline (no login).
python -X utf8 x_tl.py <screen_name|saved .html> [...]
Prints: date | media | video seconds | likes | reposts | replies | quotes | permalink | text
Saves each raw page to ../part3/synd_<name>.html
"""
import sys, re, json, time, os, datetime
import vt

HERE = os.path.dirname(os.path.abspath(__file__))


def fetch(name):
    for i in range(4):
        try:
            return vt.http("https://syndication.twitter.com/srv/timeline-profile/screen-name/" + name, headers={"User-Agent": "Mozilla/5.0"})
        except Exception as e:
            if "429" in str(e):
                time.sleep(20 * (i + 1))
                continue
            raise
    raise RuntimeError("rate limited")


def parse(html, name):
    m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html, re.S)
    if not m:
        print("NO DATA", name)
        return
    data = json.loads(m.group(1))
    ents = data.get("props", {}).get("pageProps", {}).get("timeline", {}).get("entries", [])
    fol = None
    rows = []
    for e in ents:
        t = (e.get("content") or {}).get("tweet")
        if not t:
            continue
        u = t.get("user") or {}
        if u.get("screen_name", "").lower() == name.lower() and fol is None:
            fol = u.get("followers_count")
        media = (t.get("extended_entities") or {}).get("media") or (t.get("entities") or {}).get("media") or []
        kinds = sorted(set(x.get("type", "?") for x in media)) or ["text"]
        secs = ""
        for x in media:
            d = (x.get("video_info") or {}).get("duration_millis")
            if d:
                secs = "%.0fs" % (d / 1000)
            ar = (x.get("video_info") or {}).get("aspect_ratio")
            if ar:
                secs += " %d:%d" % tuple(ar)
        dt = datetime.datetime.strptime(t["created_at"], "%a %b %d %H:%M:%S %z %Y").strftime("%Y-%m-%d")
        rows.append((dt, "+".join(kinds), secs, t.get("favorite_count"), t.get("retweet_count"), t.get("reply_count"), t.get("quote_count"), "x.com" + (t.get("permalink") or ""), (t.get("full_text") or "").replace("\n", " ")[:140]))
    print("=== @%s followers=%s posts=%d" % (name, fol, len(rows)))
    for r in rows:
        print(" | ".join(str(x) for x in r))


if __name__ == "__main__":
    for n in sys.argv[1:]:
        try:
            if n.endswith(".html"):
                parse(open(n, encoding="utf-8").read(), os.path.basename(n)[6:-5])
                continue
            h = fetch(n)
            open(os.path.join(HERE, "..", "part3", "synd_%s.html" % n), "w", encoding="utf-8").write(h)
            parse(h, n)
            time.sleep(6)
        except Exception as e:
            print("ERR", n, e)
