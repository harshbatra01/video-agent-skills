# Download Commons videos by title, preferring a 720p (else 480p, else original) transcode; logs licence and author.
# python3 commons_video_get.py <out_dir> <list.tsv: local_name<TAB>File title>
import json, os, re, ssl, sys, time, urllib.parse, urllib.request, certifi
ctx = ssl.create_default_context(cafile=certifi.where()); UA = {"User-Agent": "minidoc-research/1.0 (personal video project)"}
out, lst = sys.argv[1:3]; cred = open(os.path.join(out, "CREDITS.tsv"), "a")
def get(u):
    for k in range(5):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), context=ctx, timeout=60))
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(30 * (k + 1)); continue
            raise
for line in open(lst):
    if not line.strip(): continue
    name, title = line.rstrip("\n").split("\t"); dest = os.path.join(out, name)
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({"action": "query", "format": "json", "titles": title,
        "prop": "videoinfo", "viprop": "url|size|derivatives|extmetadata", "viextmetadatafilter": "LicenseShortName|Artist"})
    p = list(get(u)["query"]["pages"].values())[0]
    if "videoinfo" not in p: print("NOT FOUND", title); continue
    vi = p["videoinfo"][0]; ders = {d.get("transcodekey"): d["src"] for d in vi.get("derivatives", [])}
    src = ders.get("720p.vp9.webm") or ders.get("720p.webm") or ders.get("480p.vp9.webm") or vi["url"]
    m = vi.get("extmetadata", {}); lic = m.get("LicenseShortName", {}).get("value", "?"); art = re.sub("<[^>]+>", "", m.get("Artist", {}).get("value", "?")).strip()
    if not os.path.exists(dest):
        time.sleep(2)
        with urllib.request.urlopen(urllib.request.Request(src, headers=UA), context=ctx, timeout=900) as r, open(dest, "wb") as f:
            while ch := r.read(1 << 20): f.write(ch)
    cred.write(f"{name}\t{title}\t{lic}\t{art}\thttps://commons.wikimedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}\n"); cred.flush()
    print("ok", name, round(os.path.getsize(dest) / 1e6, 1), "MB", lic, "|", src.rsplit(".", 2)[-2] if "transcoded" in src else "original"); time.sleep(2)
