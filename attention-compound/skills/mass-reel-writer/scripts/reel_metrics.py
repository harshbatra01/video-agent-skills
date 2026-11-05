"""Measure short-form reel scripts the way we measured Rani's reels (Hindi, Hinglish or English).

usage: python3 -I tools/reel_metrics.py research/reference-rani/reels.json          (the 11 reels, plus correlations)
       python3 -I tools/reel_metrics.py --text "script text" [--secs 50]           (one script)
       python3 -I tools/reel_metrics.py --md 23-two-scripts-massy.md               (every '> ' block in a markdown file)

Counts are signals, not verdicts: 11 reels is a small sample, and views also depend on things a script can't show
(the cover, the edit, posting time, the account's momentum).
"""
import json, math, re, sys

ANCHORS = ['mamaearth', 'lenskart', 'boat', 'meta', 'whatsapp', 'godaddy', 'instagram', 'india', 'इंडिया', 'china',
           'चाइनीस', 'vietnam', 'राजस्थान', 'गुजरात', 'gujarat', 'metamucil', 'lucknow', 'agra', 'tajmahal', 'kannauj',
           'uttar pradesh', 'tripur', 'surat', 'ring road', 'ahmedabad', 'kalupur', 'jamnagar', 'rajkot', 'bhangri',
           'morbi', 'amazon', 'meesho', 'flipkart', 'chatgpt', 'openai', 'google', 'walmart', 'target', 'costco',
           'nike', 'etsy', 'shopify', 'bing', 'microsoft', 'copilot', 'youtube', 'maps', 'gemini', 'ebay']
NUM_WORDS = ['एक', 'दो', 'तीन', 'चार', 'पाँच', 'पांच', 'हज़ार', 'हजार', 'हजारो', 'लाख', 'लाखों', 'करोड़',
             'ek', 'do', 'teen', 'chaar', 'paanch', 'hazaar', 'lakh', 'crore', 'one', 'two', 'three', 'four', 'five',
             'six', 'eight', 'ten', 'hundred', 'thousand', 'million']
MONEY = r'(₹|\$|रुपये|रुपए|पैसे|paise|lakh|लाख|hazaar|हज़ार|हजार|\bcents?\b|\bfree\b|\bfees?\b|\bprice|\bdeal\b|cost)'
ORDINALS = r'(सबसे पहले|सबसे पहला|पहले|sabse pehl|dusra|teesra|दूसरा|तीसरा|\blast\b|फिर आता|phir hai|\bfirst\b|\bsecond\b|\bthird\b|and last|aur last)'
CONTRAST = r'(लेकिन|\bbut\b|बट|lekin|balki|बल्कि|दुख की बात|instead|actually|एक्चुअली)'
YOU_INFORMAL = r'(तुम|तुम्हें|तुम्हारा|तुम्हारे|tum\b|tumhe)'
YOU_FORMAL = r'(आप|आपको|आपके|आपका|\baap\b|aapko|aapke|aapka)'
YOU_EN = r'\b(you|your|yours|you\'re|you\'ll)\b'
IMPERATIVE_EN = r'(?:^|[.?!]\s+|,\s+(?:and|then)\s+|\bso\s+|\b(?:first|second|third|last|next|finally),\s+)(get|set|give|make|ask|check|comment|go|run|add|write|open|type|look|use|start|stop|buy|try|send|join|follow|download)\b|\byou (?:should|need to|have to|must)\b'
IMPERATIVE_HI = r'(\S+(?:ो|ओ)(?=[\s,.।?!]|$)|\b\w+(?:karo|lagao|lagaao|dhoondho|bhago|badhao|chalao|banao|jao)\b|मत\s|\bmat\b)'
NOT_IMPERATIVE_HI = {'तो', 'जो', 'वो', 'को', 'सो', 'दोस्त', 'हो', 'लो', 'दो'}
FIRST_PERSON = r'(मैं|मेरे|मुझे|मैंने|\bmain\b|mujhe|\bI\b|\bI\'d\b|\bmy\b|\bwe\b|\bus\b)'


def sentences(t):
    return [s for s in re.split(r'(?<=[.?!।])\s+', t.strip()) if s.strip()]


def measure(text, secs=None):
    t = text.strip()
    low = t.lower()
    words = t.split()
    sents = sentences(t)
    slen = [len(s.split()) for s in sents]
    digits = re.findall(r'\d[\d,]*(?:\.\d+)?', t)
    numwords = [w for w in re.findall(r"[\w']+", low) if w in NUM_WORDS]
    anchors = sorted({a for a in ANCHORS if a in low})
    first = sents[0] if sents else ''
    m = dict(
        words=len(words), sentences=len(sents),
        avg_sentence=round(sum(slen) / max(1, len(slen)), 1), longest_sentence=max(slen or [0]),
        numbers=len(digits) + len(numwords),
        numbers_per_100w=round(100 * (len(digits) + len(numwords)) / max(1, len(words)), 1),
        money_mentions=len(re.findall(MONEY, low)),
        named_anchors=len(anchors), anchors=', '.join(anchors),
        ordinals=len(re.findall(ORDINALS, low)), contrast=len(re.findall(CONTRAST, low)),
        questions=t.count('?'),
        you_informal=len(re.findall(YOU_INFORMAL, low)), you_formal=len(re.findall(YOU_FORMAL, low)),
        you_en=len(re.findall(YOU_EN, low)),
        first_person=len(re.findall(FIRST_PERSON, t)),
        instructions=len(re.findall(IMPERATIVE_EN, t, re.I | re.M)) + len([m for m in re.findall(IMPERATIVE_HI, t) if m.strip() not in NOT_IMPERATIVE_HI]),
        hook_words=len(first.split()),
        hook_has_number=bool(re.search(r'\d', first) or any(w in NUM_WORDS for w in re.findall(r"[\w']+", first.lower()))),
        hook_has_anchor=any(a in first.lower() for a in ANCHORS),
    )
    m['instructions_per_100w'] = round(100 * m['instructions'] / max(1, len(words)), 1)
    if secs:
        m['words_per_sec'] = round(len(words) / secs, 2)
    return m


def spearman(xs, ys):
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2 + 1
            i = j + 1
        return r
    rx, ry = rank(xs), rank(ys)
    n = len(xs)
    mx, my = sum(rx) / n, sum(ry) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    vx = math.sqrt(sum((a - mx) ** 2 for a in rx))
    vy = math.sqrt(sum((b - my) ** 2 for b in ry))
    return round(cov / (vx * vy), 2) if vx and vy else 0.0


COLS = ['words', 'words_per_sec', 'avg_sentence', 'longest_sentence', 'numbers', 'numbers_per_100w', 'money_mentions',
        'named_anchors', 'ordinals', 'contrast', 'instructions_per_100w', 'questions', 'you_informal', 'you_formal', 'you_en', 'first_person',
        'hook_words', 'hook_has_number', 'hook_has_anchor']


def main(argv):
    if '--text' in argv:
        t = argv[argv.index('--text') + 1]
        secs = float(argv[argv.index('--secs') + 1]) if '--secs' in argv else None
        print(json.dumps(measure(t, secs), ensure_ascii=False, indent=1))
        return
    if '--md' in argv:
        md = open(argv[argv.index('--md') + 1], encoding='utf-8').read()
        for sec in re.split(r'\n(?=#{1,3} )', md):
            q = [l[2:] for l in sec.splitlines() if l.startswith('> ')]
            if q:
                t = re.sub(r'\[[A-Z-]+[^\]]*\]', '', ' '.join(q))
                print('==', sec.splitlines()[0].lstrip('# '))
                print(json.dumps(measure(t, len(t.split()) / 2.7), ensure_ascii=False))
        return
    reels = json.load(open(argv[1], encoding='utf-8'))
    rows = []
    for r in reels:
        m = measure(r['text'], r.get('secs'))
        m.update(id=r['id'], views=r['views'], log_views=round(math.log10(r['views']), 2),
                 views_per_day=round(r['views'] / max(1, r.get('age_days', 1))), cta=r.get('cta', ''))
        rows.append(m)
    head = ['id', 'views', 'cta'] + COLS
    print('| ' + ' | '.join(head) + ' |')
    print('|' + ' --- |' * len(head))
    for m in sorted(rows, key=lambda m: -m['views']):
        print('| ' + ' | '.join(str(m.get(c, '')) for c in head) + ' |')
    print('\nSpearman rank correlation with views (n=%d; |r| above about 0.6 is worth noticing):' % len(rows))
    for c in COLS:
        xs = [float(m.get(c, 0)) for m in rows]
        if len(set(xs)) > 1:
            print(f'  {c:18} {spearman(xs, [m["views"] for m in rows]):+.2f}')


if __name__ == '__main__':
    main(sys.argv)
