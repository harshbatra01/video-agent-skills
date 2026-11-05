"""Compact YouTube metadata helper (no downloads).

usage:
  python yt.py search "query" [N]        -> title | channel | views | date | duration | url
  python yt.py meta URL [URL...]         -> one line each + most-replayed peaks (heatmap) if YouTube has them
  python yt.py heat URL                  -> the full most-replayed curve in 1/20 steps
yt-dlp sits in the user site-packages, so run this WITHOUT python -I.
"""
import sys, json
import yt_dlp

def ydl(extra=None):
    o = dict(quiet=True, no_warnings=True, skip_download=True, extract_flat=False)
    o.update(extra or {})
    return yt_dlp.YoutubeDL(o)

def fmt_views(v):
    if v is None: return "?"
    return f"{v/1e6:.2f}M" if v >= 1e6 else (f"{v/1e3:.0f}k" if v >= 1e3 else str(v))

def line(i):
    d = i.get("upload_date") or ""
    d = f"{d[:4]}-{d[4:6]}-{d[6:]}" if len(d) == 8 else d
    return f"{(i.get('title') or '')[:70]} | {i.get('channel') or i.get('uploader') or ''} | {fmt_views(i.get('view_count'))} | {d} | {i.get('duration') or '?'}s | {i.get('webpage_url') or i.get('url')}"

def peaks(i, n=3):
    hm = i.get("heatmap") or []
    if not hm: return ""
    top = sorted(hm, key=lambda h: -h.get("value", 0))[:n]
    return " peaks " + ", ".join(f"{h['start_time']:.0f}-{h['end_time']:.0f}s({h['value']:.2f})" for h in sorted(top, key=lambda h: h['start_time']))

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "search":
        n = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        with ydl({"extract_flat": "in_playlist"}) as y:
            r = y.extract_info(f"ytsearch{n}:{sys.argv[2]}", download=False)
        for e in r.get("entries", []):
            print(line(e))
    elif cmd == "meta":
        with ydl() as y:
            for u in sys.argv[2:]:
                try:
                    i = y.extract_info(u, download=False)
                    print(line(i) + peaks(i))
                except Exception as e:
                    print("ERR", u, str(e)[:120])
    elif cmd == "heat":
        with ydl() as y:
            i = y.extract_info(sys.argv[2], download=False)
        hm = i.get("heatmap") or []
        print(line(i))
        print(" ".join(f"{h['start_time']:.0f}:{h['value']:.2f}" for h in hm))
