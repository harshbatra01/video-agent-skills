# Download Commons files by title, one at a time, and log licence + author for credits.
# python3 commons_get.py <out_dir> <list.tsv: local_name<TAB>File title>
import json, os, ssl, sys, time, urllib.parse, urllib.request, certifi, re
ctx = ssl.create_default_context(cafile=certifi.where()); UA = {"User-Agent": "minidoc-research/1.0 (personal video project)"}
out, lst = sys.argv[1:3]; credits = []
def get_json(u):
    for k in range(6):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), context=ctx, timeout=60))
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(20 * (k + 1))
for line in open(lst):
    if not line.strip(): continue
    name, title = line.rstrip("\n").split("\t")
    dest = os.path.join(out, name)
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({"action": "query", "format": "json", "titles": title,
        "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiextmetadatafilter": "LicenseShortName|Artist"})
    p = list(get_json(u)["query"]["pages"].values())[0]
    if "imageinfo" not in p: print("NOT FOUND", title); continue
    ii = p["imageinfo"][0]; m = ii["extmetadata"]
    artist = re.sub("<[^>]+>", "", m.get("Artist", {}).get("value", "?")).strip()
    credits.append(f"{name}\t{title}\t{m.get('LicenseShortName', {}).get('value', '?')}\t{artist}\thttps://commons.wikimedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}")
    if not os.path.exists(dest):
        time.sleep(2)
        for k in range(6):   # 429: back off and retry (Wikimedia rate limit)
            try:
                with urllib.request.urlopen(urllib.request.Request(ii["url"], headers=UA), context=ctx, timeout=600) as r, open(dest, "wb") as f:
                    while chunk := r.read(1 << 20): f.write(chunk)
                break
            except urllib.error.HTTPError as e:
                if e.code != 429: raise
                time.sleep(20 * (k + 1))
    print("ok", name, round(os.path.getsize(dest) / 1e6, 1), "MB")
    time.sleep(6)
open(os.path.join(out, "CREDITS.tsv"), "w").write("\n".join(credits) + "\n")
