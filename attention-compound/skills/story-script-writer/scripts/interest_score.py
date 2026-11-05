#!/usr/bin/env python3
"""Measures whether a script is a story or an information exchange.

Input: a text file, one sentence per line, each starting with a tag:
  E| someone does something or something happens, you can picture it
  T| a question, a promise or a reversal line
  I| explains or describes, nothing happens
Blank lines and lines starting with # are skipped. The tags are your judgement.
Run: python3 interest_score.py script_tagged.txt [more.txt ...]
"""
import re, sys

REFS = "reference range (4 scripts): event 40-79%, info 4-31%, info run 1-5, sentence 10.7-15.6, ease 68-80"

def syllables(word):
    word = re.sub(r"[^a-z]", "", word.lower())
    if not word:
        return 0
    n = len(re.findall(r"[aeiouy]+", word))
    if word.endswith("e") and not word.endswith("le") and n > 1:
        n -= 1
    return max(n, 1)

def load(path):
    lines = []
    for no, raw in enumerate(open(path, encoding="utf-8"), 1):
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            continue
        m = re.match(r"([ETI])\|\s*(.+)", raw)
        if not m:
            sys.exit(f"{path} line {no}: start the line with E|, T| or I|")
        lines.append((m.group(1), m.group(2)))
    if not lines:
        sys.exit(f"{path}: no tagged lines")
    return lines

def measure(lines):
    words_by_line = [re.findall(r"[A-Za-z0-9'.,-]*[A-Za-z0-9]", t) for _, t in lines]
    counts = [len(w) for w in words_by_line]
    alpha = [w for ws in words_by_line for w in ws if re.search(r"[A-Za-z]", w)]
    sylls = [syllables(w) for w in alpha]
    total = sum(counts)
    tag = {t: sum(c for (g, _), c in zip(lines, counts) if g == t) for t in "ETI"}
    run = best = 0
    for g, _ in lines:
        run = run + 1 if g == "I" else 0
        best = max(best, run)
    before = 0
    for (g, _), c in zip(lines, counts):
        if g == "E":
            break
        before += c
    ease = 206.835 - 1.015 * (total / len(lines)) - 84.6 * (sum(sylls) / len(alpha))
    return dict(words=total, sentences=len(lines), avg_sentence=round(total / len(lines), 1),
                longest_sentence=max(counts), event_pct=round(100 * tag["E"] / total),
                tension_pct=round(100 * tag["T"] / total), info_pct=round(100 * tag["I"] / total),
                longest_info_run=best, pct_before_first_event=round(100 * before / total),
                hard_word_pct=round(100 * sum(x >= 3 for x in sylls) / len(alpha), 1), reading_ease=round(ease))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for path in sys.argv[1:]:
        print(path)
        for k, v in measure(load(path)).items():
            print(f"  {k:24}{v}")
    print(REFS)
