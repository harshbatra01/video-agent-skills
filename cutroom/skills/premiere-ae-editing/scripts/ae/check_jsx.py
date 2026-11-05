"""Syntax-check ExtendScript before spending an After Effects launch on it.
usage: python check_jsx.py build.jsx [more.jsx ...]
- parses the whole file with esprima (pip install esprima; installed here) and every eval'd spec string of a
  'var BUILDERS = [...]' array (ae_build.py output), printing the line and message of each error
- warns about things ES3 ExtendScript does not have: let/const, arrow functions, template strings, Array
  indexOf/map/forEach/filter (String indexOf is fine), JSON."""
import sys, json, re
import esprima

ES3 = [(r'\blet\s+\w', 'let'), (r'\bconst\s+\w', 'const'), (r'=>', 'arrow function'), (r'`', 'template string'),
       (r'\]\s*\.\s*(map|forEach|filter|indexOf)\(', 'Array method'), (r'\bJSON\.', 'JSON')]


def check(src, label):
    bad = 0
    src = re.sub(r'(?m)^﻿?\s*#(target|include|includepath|targetengine|strict|script)\b.*$', '', src)   # ExtendScript directives
    try: esprima.parseScript(src)
    except Exception as e: print('SYNTAX %s: %s' % (label, e)); bad += 1
    for pat, what in ES3:
        for m in re.finditer(pat, src):
            line = src.count('\n', 0, m.start()) + 1
            print('ES3 WARNING %s line %d: %s' % (label, line, what)); break
    return bad


for f in sys.argv[1:]:
    s = open(f, encoding='utf-8').read()
    bad = check(s, f)
    k = s.find('var BUILDERS = ')
    n = 0
    if k >= 0:
        arr, _ = json.JSONDecoder().raw_decode(s[k + len('var BUILDERS = '):])
        n = len(arr)
        for i, b in enumerate(arr): bad += check(b, '%s spec %d' % (f, i))
    print(f, 'ok' if not bad else 'BAD', ('%d specs' % n) if n else '')
