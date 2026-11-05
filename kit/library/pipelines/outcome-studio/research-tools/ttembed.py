"""Latest posts of a TikTok account from the creator embed page, read through r.jina.ai (TikTok is blocked here).
python -X utf8 ttembed.py <handle> [...]
Prints: date (from the video id) | id | views if present | caption
Works for non-verified accounts; verified brand accounts usually return an empty list.
"""
import sys, re, json, datetime, os
import vt

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "part3")


def emb(h):
    html = vt.http("https://r.jina.ai/https://www.tiktok.com/embed/@" + h, headers={"X-Return-Format": "html"}, timeout=90)
    open(os.path.join(OUT, "embed_%s.html" % h), "w", encoding="utf-8").write(html)
    i = html.find('"videoList"')
    if i < 0:
        print("=== @%s no videoList" % h)
        return
    try:
        arr, _ = json.JSONDecoder().raw_decode(html[i + len('"videoList":'):])
    except Exception as e:
        print("=== @%s parse error %s" % (h, e))
        return
    fol = re.search(r'"followerCount":(\d+)', html)
    print("=== @%s followers=%s videos=%d" % (h, fol.group(1) if fol else "?", len(arr)))
    for v in arr:
        vid = str(v.get("id") or v.get("itemId") or "")
        try:
            d = datetime.datetime.fromtimestamp(int(vid) >> 32, datetime.timezone.utc).strftime("%Y-%m-%d")
        except Exception:
            d = "?"
        views = v.get("playCount") or (v.get("stats") or {}).get("playCount")
        cap = (v.get("desc") or v.get("title") or "").replace("\n", " ")[:110]
        print("%s | %s | views %s | %s" % (d, vid, views, cap))


if __name__ == "__main__":
    for h in sys.argv[1:]:
        try:
            emb(h)
        except Exception as e:
            print("ERR", h, e)
