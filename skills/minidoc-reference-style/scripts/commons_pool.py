# Build an image pool from Commons searches: open licences only (PD, CC0, CC BY), landscape or portrait >= 1000 px,
# downloads a 1600 px rendition. python3 commons_pool.py <out_dir> <queries.tsv: tag<TAB>query<TAB>count>
import json, os, ssl, sys, time, urllib.parse, urllib.request, re, certifi
ctx = ssl.create_default_context(cafile=certifi.where()); UA = {"User-Agent": "minidoc-research/1.0 (personal video project)"}
OK = re.compile(r"^(public domain|pd|cc0|cc by( \d\.\d)?)$", re.I)
out, qf = sys.argv[1:3]; credits = open(os.path.join(out, "CREDITS.tsv"), "a")
def get(u):
    for k in range(5):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), context=ctx, timeout=60))
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(30 * (k + 1)); continue
            raise
for line in open(qf):
    if not line.strip(): continue
    tag, q, cnt = line.rstrip("\n").split("\t"); cnt = int(cnt); got = 0
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({"action": "query", "format": "json", "generator": "search",
        "gsrsearch": q + " filetype:bitmap", "gsrnamespace": 6, "gsrlimit": 25, "prop": "imageinfo", "iiprop": "url|size|extmetadata",
        "iiurlwidth": 1600, "iiextmetadatafilter": "LicenseShortName|Artist"})
    pages = sorted(get(u).get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 0))
    for p in pages:
        if got >= cnt: break
        ii = p["imageinfo"][0]; m = ii.get("extmetadata", {}); lic = m.get("LicenseShortName", {}).get("value", "")
        if not OK.match(lic.strip()) or min(ii["width"], ii["height"]) < 900 or not p["title"].lower().endswith((".jpg", ".jpeg", ".png")): continue
        name = f"{tag}_{got + 1:02d}.jpg"; dest = os.path.join(out, name)
        if not os.path.exists(dest):
            time.sleep(1.5)
            try:
                with urllib.request.urlopen(urllib.request.Request(ii.get("thumburl", ii["url"]), headers=UA), context=ctx, timeout=120) as r: open(dest, "wb").write(r.read())
            except urllib.error.HTTPError as e:
                print("skip", e.code, p["title"]); time.sleep(20); continue
        artist = re.sub("<[^>]+>", "", m.get("Artist", {}).get("value", "?")).strip()
        credits.write(f"{name}\t{p['title']}\t{lic}\t{artist}\thttps://commons.wikimedia.org/wiki/{urllib.parse.quote(p['title'].replace(' ', '_'))}\n"); credits.flush()
        got += 1
    print(f"{tag}: {got}/{cnt}  ({q})"); time.sleep(4)
