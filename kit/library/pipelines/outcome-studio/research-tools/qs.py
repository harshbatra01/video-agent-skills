"""Run many YouTube Shorts searches at once (Shorts filter, period filter), list hits by views.
python -X utf8 qs.py <period: year|month|week|any> <n per query> "query 1" "query 2" ...
Prints: === query, then  id | views | title (from YouTube's accessibility text)
"""
import sys, re, base64, urllib.parse, concurrent.futures as cf
import vt


def vnum(acc):
    m = re.search(r"([\d.,]+) (thousand|million|billion)? ?views", acc)
    if not m:
        return 0
    x = float(m.group(1).replace(",", ""))
    return x * {"thousand": 1e3, "million": 1e6, "billion": 1e9, None: 1}[m.group(2)]


def one(query, period):
    pm = {"hour": 1, "today": 2, "week": 3, "month": 4, "year": 5}
    f = b""
    if period in pm:
        f += bytes([0x08, pm[period]])
    f += bytes([0x10, 0x09])
    b = bytes([0x12, len(f)]) + f
    sp = urllib.parse.quote(base64.b64encode(b).decode())
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(query) + "&sp=" + sp + "&gl=US&hl=en"
    try:
        html = vt.http(url, headers=vt.CK)
    except Exception as e:
        return query, [("ERR", str(e)[:80])]
    res = vt.ylock(html)
    res.sort(key=lambda r: -vnum(r[1]))
    return query, res


if __name__ == "__main__":
    period, n, qs = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
    with cf.ThreadPoolExecutor(6) as ex:
        outs = list(ex.map(lambda q: one(q, period), qs))
    for q, res in outs:
        print("=== %s [%s] %d" % (q, period, len(res)))
        for vid, acc in res[:n]:
            v = vnum(acc)
            t = re.sub(r",? [\d.,]+ (thousand |million |billion )?views - play Short$", "", acc)
            print("  %s | %s | %s" % (vid, "{:,.0f}".format(v), t[:110]))
