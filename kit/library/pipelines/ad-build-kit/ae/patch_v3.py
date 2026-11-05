"""gfx_v3_body.jsx = gfx_v2_body.jsx + v3 fixes (white stack rules, unclipped blurs, readable definition without noun) + effRoll"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(HERE, 'gfx_v2_body.jsx'), encoding='utf-8').read()


def rep(a, b):
    global s
    assert s.count(a) == 1, ('pattern count', s.count(a), a[:70])
    s = s.replace(a, b)


# 1. stacked VITAMINS / MINERALS / NUTRIENTS: every rule white
rep('var ln = rrect(c, "rule " + i, wl, 6, 3, (i == 1 ? GREEN : WHITE), null, 0, 540, wd[2] + r.height * 0.5 + 34);',
    'var ln = rrect(c, "rule " + i, wl, 6, 3, WHITE, null, 0, 540, wd[2] + r.height * 0.5 + 34);')

# 2. glass: definition without the noun, directly under the word, readable
rep('''    var defL = null, nounL = null;
    if (sp.p2) {
        nounL = txt(c, sp.p2.noun, SERIFI, 33, GREEN, ParagraphJustification.LEFT_JUSTIFY, 0, x0 + pad, y0 + h1 + 8);
        defL = boxTxt(c, sp.p2.def, SEMI, 34, [0.96, 0.97, 0.98], maxW, 42, x0 + pad, y0 + h1 + 28);
        h2 = Math.round(h1 + 28 + rect(defL).height + pad);
    }''', '''    var defL = null, nounL = null, defTop = 0;
    if (sp.p2) {
        defTop = y0 + h1 + (sp.p2.noun ? 28 : 6);
        if (sp.p2.noun) nounL = txt(c, sp.p2.noun, SERIFI, 33, GREEN, ParagraphJustification.LEFT_JUSTIFY, 0, x0 + pad, y0 + h1 + 8);
        defL = boxTxt(c, sp.p2.def, SEMI, 36, WHITE, maxW - 16, 45, x0 + pad + 8, defTop);
        h2 = Math.round(defTop - y0 + rect(defL).height + pad + 8);
    }''')

# 3. glass shadow + "?" halo: blur must not be clipped to the layer box (Repeat Edge Pixels OFF)
rep('O(shadowL).setValue(20); var gb = fx(shadowL, "ADBE Gaussian Blur 2"); gb.property("ADBE Gaussian Blur 2-0001").setValue(34);',
    'O(shadowL).setValue(20); var gb = fx(shadowL, "ADBE Gaussian Blur 2"); gb.property("ADBE Gaussian Blur 2-0001").setValue(34); gb.property("ADBE Gaussian Blur 2-0003").setValue(0);')
rep('fx(halo, "ADBE Gaussian Blur 2").property("ADBE Gaussian Blur 2-0001").setValue(70); O(halo).setValue(0);',
    'var hb = fx(halo, "ADBE Gaussian Blur 2"); hb.property("ADBE Gaussian Blur 2-0001").setValue(70); hb.property("ADBE Gaussian Blur 2-0003").setValue(0); O(halo).setValue(0);')

# 4. definition text on top of the glass layers, dark inset panel behind it
rep('''    if (sp.p2) {
        var tp = sp.p2.t;
        keys(O(nounL), [[tp + 0.12, 0], [tp + 0.32, 100]]);
        keys(O(defL), [[tp + 0.2, 0], [tp + 0.42, 100]]);
        var pd = P(defL).value; keys(P(defL), [[tp + 0.2, [pd[0], pd[1] + 16]], [tp + 0.46, pd, 70, 33]]);
        shadow(nounL, 0.4, 2, 10); shadow(defL, 0.45, 2, 12);
        content.push(nounL); content.push(defL);
    }''', '''    if (sp.p2) {
        var tp = sp.p2.t;
        var py0 = defTop - 14, pnl = rrShape(c, "definition panel", w - 24, Math.round(y0 + h2 - 12 - py0), 18, [0, 0, 0], 100, null, 0, 0, x0 + 12, py0);
        keys(O(pnl), [[tp + 0.22, 0], [tp + 0.42, 42]]);
        defL.moveToBeginning();
        if (nounL) { nounL.moveToBeginning(); keys(O(nounL), [[tp + 0.12, 0], [tp + 0.32, 100]]); shadow(nounL, 0.4, 2, 10); content.push(nounL); }
        keys(O(defL), [[tp + 0.2, 0], [tp + 0.42, 100]]);
        var pd = P(defL).value; keys(P(defL), [[tp + 0.2, [pd[0], pd[1] + 16]], [tp + 0.46, pd, 70, 33]]);
        shadow(defL, 0.75, 2, 8);
        content.push(pnl); content.push(defL);
    }''')

s += open(os.path.join(HERE, 'effroll.jsx'), encoding='utf-8').read()
open(os.path.join(HERE, 'gfx_v3_body.jsx'), 'w', encoding='utf-8').write(s)
print('gfx_v3_body.jsx', len(s))
