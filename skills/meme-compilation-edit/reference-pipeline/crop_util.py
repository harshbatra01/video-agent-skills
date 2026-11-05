"""Crops for memes: as few as possible (phone app bars, metadata rows, watermarks, big empty margins), always balanced."""
import numpy as np, re, os
from PIL import Image
CLIENT = "/CHANGE/ME/client or editor folder/"
HERE = os.path.dirname(os.path.abspath(__file__))   # works with Windows backslash paths too
def auto_crop(img):
    """Most memes need no crop at all (the reviewer, Oct 11 2026: "overall pattern im noticing is just an overuse of crops.
    most memes probably dont require any cropping"). This only trims big empty margins and real bars, and nothing that
    makes the meme lopsided.
      - Top / bottom: only a plain margin bigger than 15% of the height is trimmed (balance_margins then sets the
        final margin). Thin frames and borders stay: trimming one off the bottom alone looked like a random cut on a
        poster meme.
      - Sides: only black pillarbox bars at least 5% wide on BOTH sides, the same amount off each, never a band that
        touches text. White side margins are the meme's own and stay: trimming only the right margin of a captioned
        photo meme (its left margin held the caption) made it look lopsided."""
    a = np.asarray(Image.open(ocr_path(img)).convert("RGB")).astype(int)
    H, W, _ = a.shape
    crop = {"L": 0.0, "T": 0.0, "R": 0.0, "B": 0.0}
    def band(get, n):
        ref = get(0).astype(float).mean(axis=0)
        k = 0
        while k < n - 1:
            line = get(k)
            if (np.abs(line - ref).max(axis=1) < 24).mean() > 0.997:
                k += 1
            else:
                break
        return k, ref
    side_cut = {}
    top_dark = a[:max(2, int(0.01 * H))].mean(axis=(0, 1)).max() < 45   # a black frame all round (demotivational poster)
    bot_dark = a[H - max(2, int(0.01 * H)):].mean(axis=(0, 1)).max() < 45
    for side, get, n in (("T", lambda k: a[k], H), ("B", lambda k: a[H - 1 - k], H),
                         ("L", lambda k: a[:, k], W), ("R", lambda k: a[:, W - 1 - k], W)):
        k, ref = band(get, n)
        if side in "TB":
            # only a big empty margin (over 15% of the height) is worth trimming; balance_margins sets what is left
            if k / n > 0.15:
                amount = (k - int(0.05 * n)) / n * 100
                if not text_in_band(img, side, amount / 100 + 0.004):
                    crop[side] = round(float(amount), 3)
            continue
        if k / n < 0.05:
            continue                                       # thin borders stay
        if ref.max() > 45 or top_dark or bot_dark:
            continue                                       # only black pillarbox bars; white margins and frames are the meme's own
        amount = k / n * 100 - 0.3                         # stop just inside the bar
        if amount <= 0 or text_in_band(img, side, amount / 100 + 0.006):
            continue
        side_cut[side] = (amount, ref)
    if len(side_cut) == 2:
        both = min(side_cut["L"][0], side_cut["R"][0])     # black bars on both sides: the same amount off each
        crop["L"] = crop["R"] = round(float(both), 3)
    return crop

_OCR = {}
def _ocr_lines(img):
    if not _OCR:
        import json, os
        for l in open(HERE + "/img_ocr.jsonl"):
            r = json.loads(l)
            _OCR[os.path.basename(r["file"]).replace(".webp.png", ".webp").replace(".WEBP.png", ".WEBP").replace(".mp4.png", ".mp4").replace(".gif.png", ".gif").replace(".GIF.png", ".GIF")] = r
    return _OCR.get(img, {}).get("lines", [])

def text_in_band(img, side, frac):
    """True if any OCR word reaches into the outer `frac` of the image on that side."""
    for L in _ocr_lines(img):
        for w in L.get("words", []) or [L]:
            b = w["b"]
            if (side == "L" and b[0] < frac) or (side == "R" and b[2] > 1 - frac) or \
               (side == "T" and b[1] < frac) or (side == "B" and b[3] > 1 - frac):
                return True
    return False

def watermark_bar(img):
    """The iFunny bar: a near-black strip (about 1-6% of the height) along the bottom edge holding the yellow iFunny logo
    on its right. OCR reads the stylised logo as "ecunny.co" and the like, so this goes by pixels (the reviewer, Oct 11 2026:
    "watermark you missed here"). Returns the bottom crop in percent, or 0."""
    a = np.asarray(Image.open(ocr_path(img)).convert("RGB")).astype(int)
    H, W, _ = a.shape
    dark = (a.max(axis=2) < 60).mean(axis=1)
    k = 0
    while k < H and dark[H - 1 - k] > 0.85:
        k += 1
    if not (0.008 * H <= k <= 0.06 * H) or dark[H - 1 - k] > 0.5:
        return 0.0
    band = a[H - k:]
    yellow = ((band[..., 0] > 180) & (band[..., 1] > 150) & (band[..., 2] < 90))
    if yellow[:, W // 2:].mean() < 0.004:              # the logo sits on the right half
        return 0.0
    return round(k / H * 100 + 0.1, 3)

def ocr_path(img):
    if img.endswith(".mp4"):
        return HERE + "/vframes/" + img + ".png"
    p = CLIENT + img
    return p if not img.lower().endswith((".webp", ".gif")) else HERE + "/imgconv/" + img + ".png"



TOP_CHROME = re.compile(r"(comments?|comentários|replies|^X(\.com)?$|^r/|^Join$|^\d+$|^[^a-z]*$|Search:|Post comments)", re.I)
UI_LINE = re.compile(r"^(Reply|Responder|Antworten|Vote|Share|View \d+.*|.*View \d+ (more )?repl.*|Add comment.*|Hide.*|"
                     r".*\bcomments?\b.*|.*comentários.*|.*Antworten anzeigen.*|Replies|Post comments.*|Follow|Join|Top|Most relevant.*|"
                     r"\d[\d,.]*\s*[KkMm]?|[•·:+X|J\-—~ ]+|\d+[hdmw]|\d+[hdmw] Reply|.*\d+[hdmw]\s*Reply)$", re.I)

def phone_crop(img, o):
    """Phone screenshot: keep the post itself (name/handle, text, media), cut the status bar, app chrome
    and the reply/comment bars, top and bottom only (the editor's 'Crop Normal' preset on phone shots)."""
    a = np.asarray(Image.open(ocr_path(img)).convert("RGB")).astype(int)
    H, W, _ = a.shape
    lines = [L for L in o["lines"] if L["b"][1] > 0.065 and L["b"][3] < 0.95]
    def words(t):
        return re.findall(r"[a-z]{2,}", t.lower())
    content = [L for L in lines if not UI_LINE.match(L["t"].strip())
               and (len(words(L["t"])) >= 2 or any(len(w) >= 3 for w in words(L["t"])))]
    if content:
        top = min(L["b"][1] for L in content); bot = max(L["b"][3] for L in content)
    else:
        top = bot = 0.5                                  # no text: the band through the middle of the screen
    # the post header (display name, @handle, time) right above the first text line
    for _ in range(3):
        above = [L for L in lines if top - 0.05 < L["b"][3] <= top + 0.002 and not TOP_CHROME.search(L["t"].strip())]
        if not above:
            break
        top = min(L["b"][1] for L in above)
    # media (photos, charts) touching the text block: dense non-background rows
    bg = np.median(np.concatenate([a[:, :8].reshape(-1, 3), a[:, -8:].reshape(-1, 3)]), axis=0)
    dense = (np.abs(a - bg).max(axis=2) > 40).mean(axis=1) > 0.25
    runs, y = [], 0
    while y < H:
        if dense[y]:
            y2 = y
            while y2 + 1 < H and dense[y2 + 1:y2 + 6].any():
                y2 += 1
            if (y2 - y) / H >= 0.03:
                runs.append((y / H, (y2 + 1) / H))
            y = y2 + 1
        else:
            y += 1
    changed = True
    while changed:
        changed = False
        for r0, r1 in runs:
            if r0 < 0.065 or r1 > 0.95:
                continue
            if ((bot - 0.002 <= r0 <= bot + 0.04 and r1 > bot) or (top - 0.04 <= r1 <= top + 0.002 and r0 < top)
                    or (r0 < bot and r1 > top and (r0 < top - 0.01 or r1 > bot + 0.01))):   # card/photo overlapping the text
                top, bot = min(top, r0), max(bot, r1)
                changed = True
    # dark phone UI around a photo / video still or a light card: keep the whole non-dark band that holds the text
    # (a caption overlaid on a video still left only the caption band before, Oct 11 2026)
    darkfrac = (a.max(axis=2) < 28).mean(axis=1)
    if darkfrac[: int(0.05 * H)].mean() > 0.6:          # dark status bar: a dark-UI screenshot
        light = darkfrac < 0.85
        y0 = int(0.06 * H)
        bands, y = [], y0
        while y < int(0.93 * H):
            if light[y]:
                y2 = y
                while y2 + 1 < int(0.93 * H) and light[y2 + 1: y2 + 1 + max(1, int(0.006 * H))].any():
                    y2 += 1
                if (y2 - y) / H >= 0.10:
                    bands.append((y / H, (y2 + 1) / H))
                y = y2 + 1
            else:
                y += 1
        hit = [bd for bd in bands if bd[0] <= bot and bd[1] >= top]
        if hit:
            b0, b1 = min(bd[0] for bd in hit), max(bd[1] for bd in hit)
            if b0 <= top and b1 >= bot:                  # the band holds all the text: crop to the band edges exactly
                return {"L": 0.0, "T": round(b0 * 100 + 0.1, 3), "R": 0.0, "B": round((1 - b1) * 100 + 0.1, 3)}
            top, bot = min(top, b0 + 0.002), max(bot, b1 - 0.002)
    if not content:
        return {"L": 0.0, "T": 0.0, "R": 0.0, "B": 0.0}
    pad = 0.012
    t_edge, b_edge = top - pad, bot + pad
    # never slice through a neighbouring line: stop halfway to it
    for L in o["lines"]:
        if L["b"][3] <= top + 0.002 and L["b"][3] > t_edge:
            t_edge = max(t_edge, (L["b"][3] + top) / 2)
        if L["b"][1] >= bot - 0.002 and L["b"][1] < b_edge:
            b_edge = min(b_edge, (L["b"][1] + bot) / 2)
    return {"L": 0.0, "T": round(max(0.0, t_edge) * 100, 3), "R": 0.0, "B": round(max(0.0, 1 - b_edge) * 100, 3)}


# metadata that is not part of the meme (the reviewer cropped all of these off by hand, Oct 3 2026);
# a tweet's "time · date · Views" row stays (he kept it on four tweets)
META_RE = re.compile(r"^\d{1,2}/\d{1,2}/\d{2,4},?\s+\d{1,2}:\d{2}(\s*[AaPp][Mm])?$|^\d{1,2}:\d{2}(\s*[AaPp][Mm])?(\s*[•·]\s*[\w/ ,.]+)*$|Twitter (for |Web App)|View (Tweet|post) activity|^\d+\s+Retweets?\b|You (Retweeted|reposted)|^Like\s*Re?ply|^Reply$|^Responder$|Show replies|\d+\s+replies\b|"
                     r"^Image:|Posted in r/|^reddit$|Made with|mematic|boredpanda\.com|9gag(\.com)?|memedroid|GraphJam|ifunny|\w*unny\.co\b|TwitterShots|imgflip|^\d+\s*(comments?|Kommentare)$|^Relevant|View quotes|View activity", re.I)

REACTION_RE = re.compile(r"^\s*\d+\s*[smhdw]\b.*\b(Reply|Like)\b|^\s*(Like\s*)?Reply\b|\bReply\b\s*[\d.,]+\s*[KkMm]?\s*$|^\s*[\d.,]+\s*[KkMm]?\s*$", re.I)
EXTRA_META_RE = re.compile(r"Twitter for (iPhone|Android|iPad|Web App)|^\d+\s+(seconds?|minutes?|hours?|days?|weeks?)\s+ago$|^insta\s*@|^@\w+$", re.I)

_PIX = {}
def _gap_edge(img, y, toward_lower, limit, line_h=None):
    """Where to cut next to a metadata line at normalised height y. Walks from the line toward the kept content
    through plain rows and cuts halfway across that plain gap. A watermark printed ON a picture (imgflip.com in a
    corner) has no plain gap: the cut goes right at the watermark, so the picture above it stays (the old halfway-to-
    the-previous-text-line rule cut 44% off one meme because the photo between had no text, Oct 11 2026)."""
    if img not in _PIX:
        _PIX[img] = np.asarray(Image.open(ocr_path(img)).convert("RGB")).astype(int)
    a = _PIX[img]; H = a.shape[0]
    def plain(r):
        row = a[r]
        med = np.median(row, axis=0)
        return (np.abs(row - med).max(axis=1) > 40).mean() < 0.004
    yp = int(round(y * H)); lim = int(round(limit * H))
    step = 1 if toward_lower else -1
    inside = lambda r: (r < lim if toward_lower else r > lim) and 0 <= r < H
    r = yp + step * 2
    # the rest of the header next to the line (an avatar hangs below a handle): skip up to 1.5 line heights of it
    reach = int(1.5 * line_h * H) if line_h else 20
    k = 0
    while inside(r) and not plain(r) and k <= reach:
        r += step; k += 1
    if not inside(r) or not plain(r):                 # still on a picture: the line is printed on it, cut tight
        return (yp + step) / H
    p0 = r
    while inside(r) and plain(r):
        r += step
    return (p0 + r) / 2 / H

def meta_crop(img, o, crop, spoken=()):
    """Push the top/bottom crop past metadata lines that sit at the edge of what is visible.
    A line he reads aloud stays. A bottom reaction row ("3d Reply  26.2K") stays when a reaction row also
    shows higher up in the crop, so the two match (the reviewer, Oct 6 2026); only the "View N replies" link under it goes."""
    T, B = crop["T"] / 100, crop["B"] / 100
    lines = [L for L in o["lines"] if L["b"][1] >= T - 0.002 and L["b"][3] <= 1 - B + 0.002]
    if not lines:
        return crop
    spoken = set(spoken)
    def read_aloud(L):
        ws = re.findall(r"[a-z]{3,}", L["t"].lower())
        return len(ws) >= 1 and sum(w in spoken for w in ws) >= max(1, (len(ws) + 1) // 2)
    def is_meta(L):
        t = L["t"].strip()
        return (META_RE.search(t) or EXTRA_META_RE.search(t)) and "Views" not in t and not read_aloud(L)
    def reaction(L):
        return bool(REACTION_RE.search(L["t"].strip()))
    def edge_watermark(L, nb):
        """A short line he never reads, alone at the very top or bottom edge with clear space to the content: a watermark
        or credit (a page name under a tweet, Oct 11 2026)."""
        h = L["b"][3] - L["b"][1]
        words = re.findall(r"[A-Za-z0-9']+", L["t"])
        at_edge = L["b"][3] > 0.92 or L["b"][1] < 0.08
        alone = nb is None or abs((L["b"][1] - nb["b"][3]) if nb["b"][3] <= L["b"][1] else (nb["b"][1] - L["b"][3])) > 1.5 * h
        if not (at_edge and alone and 1 <= len(words) <= 4 and not read_aloud(L)):
            return False
        # it must sit in a plain margin (not printed on the photo, like a news logo inside a chyron): the rows between
        # the line and the content are plain over at least one line height
        if img not in _PIX:
            _PIX[img] = np.asarray(Image.open(ocr_path(img)).convert("RGB")).astype(int)
        a = _PIX[img]; HH = a.shape[0]
        hp = max(2, int(h * HH))
        if L["b"][3] > 0.92:
            r0, r1 = int(L["b"][1] * HH) - hp - 2, int(L["b"][1] * HH) - 2
        else:
            r0, r1 = int(L["b"][3] * HH) + 2, int(L["b"][3] * HH) + hp + 2
        r0, r1 = max(0, r0), min(HH, r1)
        if r1 <= r0:
            return False
        band = a[r0:r1]
        med = np.median(band.reshape(-1, 3), axis=0)
        return (np.abs(band - med).max(axis=2) > 40).mean() < 0.01
    lines.sort(key=lambda L: L["b"][1])
    # bottom edge
    while len(lines) > 1:
        bot = lines[-1]
        if bot["b"][1] <= 1 - B - 0.12 or not (is_meta(bot) or edge_watermark(bot, lines[-2])):
            break
        if reaction(bot) and any(reaction(L) for L in lines[:-1] if L["b"][3] < bot["b"][1] - 0.03):
            break                     # matches the reaction row above it: keep
        rest = lines[:-1]
        edge = _gap_edge(img, bot["b"][1], False, max(L["b"][3] for L in rest), bot["b"][3] - bot["b"][1])
        B = max(B, 1 - edge); lines = rest
    # top edge
    while len(lines) > 1:
        top = lines[0]
        if top["b"][3] >= T + 0.12 or not (is_meta(top) or edge_watermark(top, lines[1])):
            break
        rest = lines[1:]
        edge = _gap_edge(img, top["b"][3], True, min(L["b"][1] for L in rest), top["b"][3] - top["b"][1])
        T = max(T, edge); lines = rest
    out = dict(crop)
    out["T"], out["B"] = round(T * 100, 3), round(B * 100, 3)
    return out


def balance_margins(img, crop, report=None):
    """Keep the white space balanced (the reviewer, Oct 11 2026: "maintain balance with the white space"; on one captioned photo
    the old 3% pad left 14 px of white above the caption and 42 px under it, and he wanted them about equal).

    Works on the plain margins at the top and bottom crop edges:
      1. Caption rule: when the first thing inside a plain edge margin is text and that text block ends at a picture
         (a caption above or below a photo), the margin at the edge matches the white gap between the text and the
         picture.
      2. Otherwise, when both the top and the bottom edge sit in plain margins, the two margins are made equal.
    A margin grows back only through plain rows (never into a line, bar or photo that was cropped off, keeping a safety
    gap) and never past the image edge. It shrinks only when it is more than twice the target, and never below half a
    text line, so nothing ends up tight against the edge."""
    a = np.asarray(Image.open(ocr_path(img)).convert("RGB")).astype(int)
    H, W, _ = a.shape
    T0 = int(round(crop["T"] / 100 * H))
    B0 = H - int(round(crop["B"] / 100 * H))          # visible rows are [T0, B0)
    x0 = int(round(W * crop["L"] / 100)); x1 = W - int(round(W * crop["R"] / 100))
    m = max(2, int(0.02 * (x1 - x0)))
    cols = a[:, x0 + m: x1 - m]
    lines = [L for L in _ocr_lines(img) if L["b"][2] > x0 / W and L["b"][0] < x1 / W
             and L["b"][1] * H >= T0 - 2 and L["b"][3] * H <= B0 + 2]
    lh = float(np.median([(L["b"][3] - L["b"][1]) * H for L in lines])) if lines else 0.03 * H
    text_rows = np.zeros(H, bool)
    pad = max(1, int(0.15 * lh))
    for L in lines:
        text_rows[max(0, int(L["b"][1] * H) - pad): min(H, int(L["b"][3] * H) + pad + 1)] = True

    def side_info(side):
        edge = T0 if side == "T" else B0 - 1
        step = 1 if side == "T" else -1
        band = cols[edge: edge + 3] if side == "T" else cols[max(0, edge - 2): edge + 1]
        bg = np.median(band.reshape(-1, 3), axis=0)
        if np.abs(band - bg).max(axis=2).mean() > 6:
            return None                                # the edge cuts through content: nothing to balance
        offbg = (np.abs(cols - bg).max(axis=2) > 40).mean(axis=1)
        plain = offbg < 0.004
        inner_lim = B0 if side == "T" else T0 - 1
        y = edge
        while y != inner_lim and plain[y]:
            y += step
        if y == inner_lim:
            return None
        c1 = y                                         # first content row seen from this edge
        info = {"c1": c1, "margin": abs(c1 - edge), "text": bool(text_rows[c1]), "gap": None}
        if info["text"]:                               # walk the text block to what ends it
            last_text = c1
            while y != inner_lim:
                if text_rows[y]:
                    if abs(y - last_text) > 1.5 * lh:
                        break                          # a second text block after a long gap
                    last_text = y
                elif not plain[y]:
                    ys = [y + step * k for k in range(14) if 0 <= y + step * k < H]
                    if sum(1 for q in ys if offbg[q] > 0.5 and not text_rows[q]) >= 4:
                        info["gap"] = abs(y - last_text) - 1      # white between the caption and a picture
                    break
                y += step
        out_lim = -1 if side == "T" else H             # room to grow outward through plain rows
        z, grow = edge - step, 0
        while z != out_lim and plain[z]:
            grow += 1
            z -= step
        if z != out_lim:                               # stopped at something that was cropped off: keep clear of it
            grow = max(0, grow - max(3, int(0.25 * grow)))
        info["grow"] = grow
        info["floor"] = max(3, int(0.5 * lh))
        return info

    info = {s: side_info(s) for s in ("T", "B")}
    target = {s: info[s]["gap"] for s in ("T", "B")
              if info[s] and info[s]["gap"] is not None and info[s]["gap"] >= 0.4 * lh}
    t, b = info["T"], info["B"]
    if t and b and not target and min(t["margin"], b["margin"]) >= 3:   # both edges sit in real margins: make them equal
        eq = min(max(t["margin"], b["margin"]), t["margin"] + t["grow"], b["margin"] + b["grow"])
        target = {"T": eq, "B": eq}
    out = dict(crop)
    if crop["T"] <= 0 and crop["B"] <= 0:
        return out                                     # never crop a meme just to balance it (the reviewer: most memes need no crop)
    for s, want in target.items():
        i = info[s]
        if want >= i["margin"]:
            new_margin = min(want, i["margin"] + i["grow"])          # give white space back
        elif i["margin"] > 2 * want:
            new_margin = max(i["floor"], want)                         # clearly lopsided: trim, but not tight
            if new_margin >= i["margin"]:
                continue
        else:
            continue                                                   # close enough
        new_margin = min(new_margin, i["margin"] + i["grow"])
        if abs(new_margin - i["margin"]) < max(3, 0.006 * H):
            continue
        if s == "T":
            out["T"] = round(max(0.0, (i["c1"] - new_margin) / H * 100), 3)
        else:
            out["B"] = round(max(0.0, (H - 1 - (i["c1"] + new_margin)) / H * 100), 3)
        if report is not None:
            why = "caption gap" if i["gap"] is not None and s in target and target[s] == i["gap"] else "match other edge"
            report.append(f"{img[:34]:34s} {s}: margin {i['margin']} -> {new_margin} px ({why} {want}, room {i['grow']})")
    return out


TIGHT_TRIGGER = 0.10     # a plain margin of 10% or more of the image counts as too much white space (his example: 10-15%)

def tighten_margins(img, crop, report=None):
    """Too much white space around a meme gets tightened (the reviewer, Oct 11 2026, on a product photo meme: "see how ive tighted
    this meme, this can be done if there is too much white space"). Its white margins were 46-53 px on a 460x360 image
    (10-15%). He left about 12-16 px at the sides and 10 px under the photo, and 33 px above the caption, the same as
    the 32 px gap between the caption and the photo.
      - Only light plain margins count, and only when one of them is TIGHT_TRIGGER of the image or more. Normal margins
        stay, because most memes need no crop at all.
      - The white space is the lightest plain edge colour. A pale panel inside it (an app review on a light lavender
        card) is content, so its edges are never cut.
      - Each plain margin then goes to about 3.5% of the image's short side (his own tightening on three memes left
        2.4-4.4%). A side whose outermost content is text keeps
        one line height instead, so text never sits tight against the edge (a 3% right margin on a left-aligned Tumblr
        post put "store." against the edge). Left and right end the same where the meme allows it.
      - A caption at the top or bottom edge keeps a margin equal to its gap to the picture, so it sits in the same white
        space on both sides. Text with no picture next to it keeps one line height.
      - A drawing that floats in its own white panel (more white between it and the next picture than at the edge,
        like the heart over the "others / five mins crafts" panel) keeps its margin: trimming only the edge side
        pushed the heart against the top.
      - Edges only move inward through plain rows and columns, so no content is cut."""
    a = np.asarray(Image.open(ocr_path(img)).convert("RGB")).astype(int)
    H, W, _ = a.shape
    x0 = int(round(W * crop["L"] / 100)); x1 = W - int(round(W * crop["R"] / 100))
    y0 = int(round(H * crop["T"] / 100)); y1 = H - int(round(H * crop["B"] / 100))
    v = a[y0:y1, x0:x1]
    h, w = v.shape[:2]
    if h < 20 or w < 20:
        return crop
    meds = []
    for e in (v[0], v[-1], v[:, 0], v[:, -1]):
        md = np.median(e, axis=0)
        if md.min() >= 200 and (np.abs(e - md).max(axis=1) > 8).mean() < 0.03:
            meds.append(md)
    if not meds:
        return crop                                    # dark frames and busy edges are the meme's own
    bg = max(meds, key=lambda md: md.sum())            # the lightest plain edge is the white space
    off = np.abs(v - bg).max(axis=2) > 8
    rows, cols = off.mean(axis=1), off.mean(axis=0)
    r = np.where(rows > 0.004)[0]; c = np.where(cols > 0.004)[0]
    if not len(r) or not len(c):
        return crop
    m = {"T": int(r.min()), "B": int(h - 1 - r.max()), "L": int(c.min()), "R": int(w - 1 - c.max())}
    if max(m[s] / (H if s in "TB" else W) for s in m) < TIGHT_TRIGGER:
        return crop
    pad = max(4, int(round(0.035 * min(W, H))))      # his hand tightening left 2.4-4.4% of the short side, 3.7% on average
    lines = [L for L in _ocr_lines(img) if L["b"][2] * W > x0 and L["b"][0] * W < x1
             and L["b"][1] * H >= y0 - 2 and L["b"][3] * H <= y1 + 2]
    lh = float(np.median([(L["b"][3] - L["b"][1]) * H for L in lines])) if lines else 0.0
    text = np.zeros(h, bool)
    for L in lines:
        text[max(0, int(L["b"][1] * H) - y0): max(0, min(h, int(np.ceil(L["b"][3] * H)) - y0))] = True
    runs = []                                          # [content?, first row, last row] inside the visible area
    for y in range(h):
        s = bool(rows[y] > 0.004)
        if runs and runs[-1][0] == s:
            runs[-1][2] = y
        else:
            runs.append([s, y, y])

    blocks = []                                        # content runs, with specks (a few stray rows) joined to their neighbour
    for R in runs:
        if not R[0]:
            continue
        if blocks and R[2] - R[1] + 1 < max(4, 0.01 * h) and R[1] - blocks[-1][2] <= max(16, 0.03 * h):
            blocks[-1][2] = R[2]
        else:
            blocks.append(list(R))

    def edge_target(side):
        content = blocks if side == "T" else blocks[::-1]
        if not content or not lh:
            return pad
        is_text = lambda R: text[R[1]: R[2] + 1].mean() >= 0.6
        if not is_text(content[0]):
            if len(content) > 1:
                R0, R1 = content[0], content[1]
                space = (R1[1] - R0[2] - 1) if side == "T" else (R0[1] - R1[2] - 1)
                if space > m[side]:
                    return m[side]                     # a drawing floating in its own white panel: leave the panel alone
            return pad                                 # a picture at the edge: a thin margin
        gap, prev = None, content[0]
        for R in content[1:]:
            space = (R[1] - prev[2] - 1) if side == "T" else (prev[1] - R[2] - 1)
            if is_text(R):
                if space > 3 * lh:
                    break                              # a second block of text far away
                prev = R
                continue
            if R[2] - R[1] + 1 >= 2 * lh and rows[R[1]: R[2] + 1].mean() >= 0.3:
                gap = space                            # the white between the caption and its picture
            break
        return max(pad, gap) if gap is not None else max(pad, int(round(lh)))

    def side_target(side):
        if not lh:
            return pad
        band = max(2, int(0.02 * w))
        xs = slice(int(c.min()), int(c.min()) + band) if side == "L" else slice(int(c.max()) - band + 1, int(c.max()) + 1)
        ys = np.where(off[:, xs].any(axis=1))[0]
        if not len(ys):
            return pad
        in_text = np.zeros(len(ys), bool)
        for L in lines:
            lx0, lx1 = L["b"][0] * W - x0, L["b"][2] * W - x0
            if (lx0 <= c.min() + band + 0.01 * w) if side == "L" else (lx1 >= c.max() - band - 0.01 * w):
                in_text |= (ys >= L["b"][1] * H - y0 - 2) & (ys <= L["b"][3] * H - y0 + 2)
        return max(pad, int(round(lh))) if in_text.mean() >= 0.6 else pad

    lr = max(side_target("L"), side_target("R"))
    new = {"T": min(m["T"], edge_target("T")), "B": min(m["B"], edge_target("B")),
           "L": min(m["L"], lr), "R": min(m["R"], lr)}
    lo, hi = sorted(("L", "R"), key=lambda q: new[q])
    if new[lo] >= pad:
        new[hi] = new[lo]                              # match the narrower side so left and right look the same
    out = dict(crop)
    for s in ("T", "B", "L", "R"):
        dim = H if s in "TB" else W
        if m[s] - new[s] < max(3, 0.015 * dim):
            continue                                   # already close
        out[s] = round(crop[s] + (m[s] - new[s]) / dim * 100, 3)
        if report is not None:
            report.append(f"{img[:34]:34s} {s}: margin {m[s]} -> {new[s]} px (pad {pad}, line {lh:.0f})")
    return out



def _words2(t):
    return re.findall(r"[a-z]{2,}", t.lower())

def is_read(line, spoken):
    """A text line counts as read when most of its words were spoken, or when its letters closely match some stretch
    of what he said ("That's her actual super power" read as "that's actually her superpower")."""
    ws = _words2(line["t"])
    if not ws:
        return False
    sp = [re.sub(r"[^a-z]", "", w.lower()) for w in spoken]
    sp = [w for w in sp if w]
    hit = sum(1 for w in ws if w in set(sp))
    if hit >= max(1, int(0.5 * len(ws) + 0.5)) or hit >= 4:
        return True
    from difflib import SequenceMatcher
    target = "".join(ws)
    if len(target) < 6:
        return False
    n = len(ws)
    for i in range(len(sp)):
        for j in range(i + max(1, n - 2), min(len(sp), i + n + 3) + 1):
            if SequenceMatcher(None, target, "".join(sp[i:j])).ratio() >= 0.8:
                return True
    return False

def unread_tail_crop(img, crop, spoken):
    """Stacked memes: a panel at the bottom that he never reads comes off, so the part he reads fills the frame.
    The reviewer, Oct 13 2026 ("you need to make sure the edges of memes are cut properly"): on a tall stacked meme
    (640x1920) he cut Bottom 50%, exactly at the top of a green sponsor ad panel
    with two troll faces under it, none of which was read.
    The cut only happens at a flat-coloured panel edge with unread text inside that panel, below every line he reads,
    and only when it removes at least 15% of the height. A photo under a caption is never cut this way."""
    a = np.asarray(Image.open(ocr_path(img)).convert("RGB")).astype(int)
    H, W, _ = a.shape
    y_top, y_bot = crop["T"] / 100 * H, H - crop["B"] / 100 * H
    lines = [L for L in _ocr_lines(img) if L["b"][1] * H >= y_top - 2 and L["b"][3] * H <= y_bot + 2]
    read = [L for L in lines if is_read(L, spoken)]
    if not read:
        return crop
    last_read = max(L["b"][3] for L in read) * H
    tail = [L for L in lines if L["b"][1] * H > last_read and len(_words2(L["t"])) >= 2 and not is_read(L, spoken)
            and not META_RE.search(L["t"]) and not EXTRA_META_RE.search(L["t"])]     # a watermark is not a panel
    if not tail:
        return crop
    first_unread = min(L["b"][1] for L in tail) * H
    med = np.median(a, axis=1)
    best = None
    for y in range(int(last_read) + 2, int(first_unread)):
        jump = np.abs(med[y] - med[y - 1]).max()
        if jump < 60:
            continue
        # what starts here must be a flat panel that runs all the way down to the unread text (the green ad panel);
        # a white gap between grid rows followed by a photo, or a photo with a caption on it, is not one
        seg = a[y + 1: int(first_unread)]
        if len(seg) < 3:
            continue
        bgc = np.median(seg.reshape(-1, 3), axis=0)
        flat_rows = (np.abs(seg - bgc).max(axis=2) < 30).mean(axis=1) > 0.9
        if flat_rows.mean() >= 0.85:
            best = y
            break
    if best is None or (y_bot - best) < 0.15 * H:
        return crop
    out = dict(crop)
    out["B"] = round((H - best) / H * 100, 3)
    return out

def under_photo_trim(img, crop, spoken):
    """Phone screenshots of a post: the crop ends at the photo's bottom edge. Carousel dots ("• • • •"), a dark strip
    and the app bar under the photo are not the meme (the reviewer, Oct 13 2026, a food post screenshot: our crop kept the
    dots row and a black band under the photo). Only when nothing he reads sits below the photo."""
    a = np.asarray(Image.open(ocr_path(img)).convert("RGB")).astype(int)
    H, W, _ = a.shape
    y0, y1 = int(crop["T"] / 100 * H), H - int(crop["B"] / 100 * H)
    v = a[y0:y1]
    if len(v) < 50:
        return crop
    busy = a.std(axis=2).mean(axis=1)[y0:y1] + np.abs(np.diff(v, axis=1)).mean(axis=(1, 2))
    photo = busy > 12                                       # rows inside a photo are busy across the width
    ys = np.where(photo)[0]
    if not len(ys):
        return crop
    pb = ys.max()                                           # last busy row
    # the last photo run: walk up from the bottom-most busy row to a gap
    run_end = pb
    while run_end > 0 and not photo[run_end]:
        run_end -= 1
    below = len(v) - 1 - run_end
    if below < 0.01 * H or below > 0.12 * H:
        return crop
    lines_below = [L for L in _ocr_lines(img) if L["b"][1] * H >= y0 + run_end and L["b"][3] * H <= y1 + 2]
    if any(is_read(L, spoken) for L in lines_below):
        return crop
    out = dict(crop)
    out["B"] = round((H - (y0 + run_end + 1)) / H * 100 + 0.05, 3)
    return out

def carousel_pill(img, crop):
    """Instagram carousel dots: a dark pill holding 3-6 small dots drawn over the bottom of the photo. It is app UI, so
    the bottom edge moves up to just above the pill (the reviewer, Oct 13 2026, a food post screenshot: our crop ended at the
    photo's edge and left the pill on screen). Returns the new crop, or the same one when there is no pill."""
    a = np.asarray(Image.open(ocr_path(img)).convert("RGB")).astype(int)
    H, W, _ = a.shape
    if not (H / W > 1.8 and W >= 1000):
        return crop                                        # only phone screenshots carry the app's carousel dots
    y1 = H - int(round(crop["B"] / 100 * H))
    y0 = max(int(round(crop["T"] / 100 * H)), y1 - int(0.12 * H))
    lum = a[y0:y1].mean(axis=2)
    cx0, cx1 = int(0.30 * W), int(0.70 * W)
    hits = []
    for r in range(lum.shape[0]):
        seg = lum[r, cx0:cx1]
        bright = seg > 140
        runs, c = [], 0
        while c < len(seg):
            if bright[c]:
                d = c
                while d < len(seg) and bright[d]:
                    d += 1
                runs.append((c, d))
                c = d
            else:
                c += 1
        runs = [(c, d) for c, d in runs if d - c >= 0.004 * W]       # specks of photo texture are not dots
        dots = [(c, d) for c, d in runs if d - c <= 0.03 * W]
        if not (3 <= len(dots) <= 6) or len(dots) != len(runs):
            continue
        widths = np.array([d - c for c, d in dots], float)
        if widths.std() > 0.25 * widths.mean():
            continue                                       # carousel dots are all the same size
        centers = [(c + d) / 2 for c, d in dots]
        gaps = np.diff(centers)
        if gaps.std() > 0.25 * gaps.mean() or gaps.mean() > 0.06 * W:
            continue
        between = np.concatenate([seg[d:c2] for (c1, d), (c2, _) in zip(dots, dots[1:])])
        if not len(between) or between.mean() > 110:      # the dots sit on a dark pill
            continue
        mid = cx0 + (centers[0] + centers[-1]) / 2
        if abs(mid - W / 2) > 0.06 * W:
            continue
        hits.append(r)
    if len(hits) < max(2, int(0.003 * H)):
        return crop
    dot_h = hits[-1] - hits[0] + 1
    top = y0 + hits[0] - int(1.2 * dot_h) - int(0.004 * H)   # above the pill's rounded top
    out = dict(crop)
    out["B"] = round((H - top) / H * 100, 3)
    return out
