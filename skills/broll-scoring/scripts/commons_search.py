# Search Wikimedia Commons files (metadata only). python3 commons_search.py "<query>" [limit] [filetype: bitmap|video]
import json, sys, urllib.request, urllib.parse, ssl, certifi
ctx = ssl.create_default_context(cafile=certifi.where())
q, lim = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 8
ft = f" filetype:{sys.argv[3]}" if len(sys.argv) > 3 else ""
u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({"action": "query", "format": "json", "generator": "search",
    "gsrsearch": q + ft, "gsrnamespace": 6, "gsrlimit": lim, "prop": "imageinfo", "iiprop": "url|size|extmetadata|mediatype",
    "iiextmetadatafilter": "LicenseShortName|DateTimeOriginal|Artist"})
req = urllib.request.Request(u, headers={"User-Agent": "minidoc-research/1.0 (personal video project)"})
d = json.load(urllib.request.urlopen(req, context=ctx, timeout=60))
for p in sorted(d.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 0)):
    ii = p["imageinfo"][0]; m = ii.get("extmetadata", {})
    lic = m.get("LicenseShortName", {}).get("value", "?"); dt = m.get("DateTimeOriginal", {}).get("value", "")[:10]
    print(f"{p['title'][5:][:70]:70} | {ii['width']}x{ii['height']} | {ii['size']/1e6:.1f}MB | {lic} | {dt}\n   {ii['url']}")
