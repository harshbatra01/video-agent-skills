"""Urlebird (TikTok mirror) reader. Lists videos on a user or hashtag page with age, plays, likes, caption.
python -X utf8 ub.py user <handle> [...]     -> followers line + videos
python -X utf8 ub.py hash <tag> [...]
python -X utf8 ub.py page <urlebird url>
Output lines: id | age | plays | likes | comments | @author | caption
"""
import sys, os, re, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vt


def num(s):
    s = (s or "").strip().replace(",", "")
    m = re.match(r"([\d.]+)\s*([KMB])?", s)
    if not m:
        return 0
    return int(float(m.group(1)) * {"K": 1e3, "M": 1e6, "B": 1e9, None: 1}[m.group(2)])


def parse(h):
    rows = []
    for blk in re.split(r'<div class="thumb', h)[1:]:
        vid = re.search(r'urlebird\.com/video/(?:[^"/]*-)?(\d{18,20})/', blk)
        if not vid:
            continue
        age = re.search(r'fa-clock[^<]*</i>\s*([^<]+)<', blk)
        plays = re.search(r'fa-play[^<]*</i>\s*([^<]+)<', blk)
        likes = re.search(r'fa-heart[^<]*</i>\s*([^<]+)<', blk)
        com = re.search(r'fa-comment[^<]*</i>\s*([^<]+)<', blk)
        auth = re.search(r'class="author-name"><a href="[^"]*">@([^<]+)</a>', blk)
        cap = re.search(r'/video/[^"]*"><span>(.*?)</span>', blk, re.S)
        rows.append({"id": vid.group(1), "age": (age.group(1).strip() if age else "?"), "plays": num(plays.group(1)) if plays else 0,
                     "likes": num(likes.group(1)) if likes else 0, "comments": num(com.group(1)) if com else 0,
                     "author": auth.group(1) if auth else "?", "cap": H.unescape(H.unescape(re.sub(r"\s+", " ", cap.group(1)))).strip()[:120] if cap else ""})
    return rows


def header(h):
    out = {}
    for key, pat in [("followers", r'<b>([\d.,]+[KMB]?)</b>\s*<br[^>]*>\s*<span class="user">followers'), ("hearts", r'<b>([\d.,]+[KMB]?)</b>\s*<br[^>]*>\s*<span class="user">hearts'), ("videos", r'<b>([\d.,]+[KMB]?)</b>\s*<br[^>]*>\s*<span class="user">videos')]:
        m = re.search(pat, h, re.I | re.S)
        if m:
            out[key] = m.group(1)
    return out


def show(url, label):
    try:
        h = vt.http(url, timeout=60)
    except Exception as e:
        print("ERR", label, e)
        return []
    rows = parse(h)
    print("=== %s %s %d videos" % (label, header(h), len(rows)))
    for r in rows:
        print("%s | %s | %s | %s | %s | @%s | %s" % (r["id"], r["age"], "{:,}".format(r["plays"]), "{:,}".format(r["likes"]), r["comments"], r["author"], r["cap"]))
    return rows


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    for a in args:
        if cmd == "user":
            show("https://urlebird.com/user/%s/" % a.lstrip("@"), "@" + a.lstrip("@"))
        elif cmd == "hash":
            show("https://urlebird.com/hash/%s/" % a.lstrip("#"), "#" + a.lstrip("#"))
        else:
            show(a, a)
