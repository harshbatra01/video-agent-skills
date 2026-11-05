// ================================================================ v2 builders
function fr(t) { return Math.round(t * FPS) / FPS; }
function clamp01(x) { return x < 0 ? 0 : (x > 1 ? 1 : x); }
function easeOutCubic(u) { u = clamp01(u); return 1 - Math.pow(1 - u, 3); }
function easeInCubic(u) { u = clamp01(u); return u * u * u; }
function easeInOutCubic(u) { u = clamp01(u); return u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2; }
// per-frame linear keys of f(t) over [t0, t1]
function frameKeys(prop, t0, t1, f) {
    var a = Math.round(t0 * FPS), b = Math.round(t1 * FPS), ts = [], vs = [];
    for (var k = a; k <= b; k++) { ts.push(k / FPS); vs.push(f(k / FPS)); }
    prop.setValuesAtTimes(ts, vs);
    for (var i = 1; i <= prop.numKeys; i++) prop.setInterpolationTypeAtKey(i, KeyframeInterpolationType.LINEAR, KeyframeInterpolationType.LINEAR);
}
function setText(l, s) { var p = l.property("Source Text"), d = p.value; d.text = s; p.setValue(d); }
function countExpr(c) {
    return "var v = Math.round(ease(time, " + c.a + ", " + c.b + ", " + c.from + ", " + c.to + ")); '" + (c.pre || "") + "' + v + '" + (c.suf || "") + "';";
}
function bigWord(c, s, t0, y, maxW, size, count) {
    // reference-reel big word: RGB split ghosts, gradient fill, glow, shadow, blur-in, scale pop
    var copies = [];
    for (var cc = 0; cc < 3; cc++) {
        var lm = txt(c, s, BIG, size || 236, WHITE, ParagraphJustification.CENTER_JUSTIFY, 14, 540, y);
        fitWidth(lm, maxW || 980); centreAnchor(lm); copies.push(lm);
    }
    var main = copies[2], red = copies[0], cyan = copies[1];
    fx(red, "ADBE Fill").property("Color").setValue([1, 0.05, 0.25]);
    fx(cyan, "ADBE Fill").property("Color").setValue([0.0, 0.85, 1]);
    red.blendingMode = BlendingMode.ADD; cyan.blendingMode = BlendingMode.ADD;
    var pc = P(main).value;
    keys(P(red), [[t0, [pc[0] - 22, pc[1]]], [t0 + 0.24, pc, 70, 33]]);
    keys(P(cyan), [[t0, [pc[0] + 22, pc[1]]], [t0 + 0.24, pc, 70, 33]]);
    keys(O(red), [[t0, 0], [t0 + 0.04, 75], [t0 + 0.3, 0]]);
    keys(O(cyan), [[t0, 0], [t0 + 0.04, 75], [t0 + 0.3, 0]]);
    gradText(main, WHITE, GREY); glow(main, 60, 22, 0.35); shadow(main, 0.55, 5, 26); blurIn(main, t0, 26, 0.2);
    keys(S(red), [[t0, [128, 128]], [t0 + 0.24, [100, 100], 80, 20]]); keys(S(cyan), [[t0, [128, 128]], [t0 + 0.24, [100, 100], 80, 20]]);
    main.motionBlur = true; red.motionBlur = true; cyan.motionBlur = true;
    if (count) for (var q = 0; q < 3; q++) copies[q].property("Source Text").expression = countExpr(count);
    return {main: main, red: red, cyan: cyan, pc: pc};
}
function kickRow(c, parts, t0, y, size) {
    var row = [], tot = 0, GAP = 20, els = [];
    for (var i = 0; i < parts.length; i++) {
        var l = txt(c, parts[i][0], KICK, size || 54, parts[i][1], ParagraphJustification.LEFT_JUSTIFY, 60, 0, y);
        var r = rect(l); row.push([l, r]); tot += r.width;
    }
    tot += GAP * (row.length - 1);
    var x = 540 - tot / 2;
    for (var k = 0; k < row.length; k++) {
        var lk = row[k][0], rk = row[k][1];
        P(lk).setValue([x - rk.left, y]); x += rk.width + GAP;
        shadow(lk, 0.6, 3, 18);
        keys(O(lk), [[t0, 0], [t0 + 0.14, 100]]);
        keys(P(lk), [[t0, [P(lk).value[0], y + 26]], [t0 + 0.2, [P(lk).value[0], y], 70, 33]]);
        els.push(lk);
    }
    return els;
}
function exitBeat(els, t) {
    for (var i = 0; i < els.length; i++) {
        var o = O(els[i]); o.setValueAtTime(t, o.valueAtTime(t, false)); o.setValueAtTime(t + 0.1, 0);
    }
}
// sp: name, dur, bdIn, beats:[{kick:[[t,c]], kIn, mains:[[text, tIn, count]], out}], below:[text, t]
function caption2(sp) {
    var c = newComp(sp.name, sp.dur);
    c.motionBlur = true;
    backdrop(c, 980, H + 80, 420, 74, sp.bdIn ? 0 : null);
    for (var b = 0; b < sp.beats.length; b++) {
        var bt = sp.beats[b], els = [];
        if (bt.kick && bt.kick.length) els = els.concat(kickRow(c, bt.kick, bt.kIn, KICK_Y, bt.kickSize));
        for (var m = 0; m < bt.mains.length; m++) {
            var mn = bt.mains[m], t0 = mn[1], t1 = (m + 1 < bt.mains.length) ? bt.mains[m + 1][1] : -1;
            var w = bigWord(c, mn[0], t0, MAIN_Y, 980, bt.size || 236, mn[2] || null);
            var endT = (t1 > 0) ? t1 : (bt.out > 0 ? bt.out : sp.dur);
            keys(S(w.main), [[t0, [128, 128]], [t0 + 0.24, [100, 100], 80, 20], [endT, [103.5, 103.5]]]);
            if (t1 > 0) keys(O(w.main), [[t0, 0], [t0 + 0.06, 100], [t1 - 0.02, 100], [t1 + 0.06, 0]]);
            else keys(O(w.main), [[t0, 0], [t0 + 0.06, 100]]);
            els.push(w.main);
        }
        if (bt.out > 0) exitBeat(els, bt.out);
    }
    if (sp.below) {
        var bl = txt(c, sp.below[0], KICK, 58, WHITE, ParagraphJustification.CENTER_JUSTIFY, 80, 540, MAIN_Y + 150);
        shadow(bl, 0.6, 3, 18);
        keys(O(bl), [[sp.below[1], 0], [sp.below[1] + 0.14, 100]]);
        keys(P(bl), [[sp.below[1], [540, MAIN_Y + 176]], [sp.below[1] + 0.2, [540, MAIN_Y + 150], 70, 33]]);
    }
    if (sp.flash !== false) { var fl = solid(c, "flash", [1, 1, 1]); keys(O(fl), [[0, 0], [0.033, 24], [0.15, 0]]); }
    return c;
}
// VITAMINS / MINERALS / NUTRIENTS: one big word per band, synced
function stack(sp) {
    var c = newComp(sp.name, sp.dur);
    c.motionBlur = true;
    var dm = solid(c, "dim", [0, 0, 0]); keys(O(dm), [[0, 0], [0.12, 34]]);
    for (var i = 0; i < sp.words.length; i++) {
        var wd = sp.words[i];
        var w = bigWord(c, wd[0], wd[1], wd[2], 940, 230, null);
        keys(S(w.main), [[wd[1], [128, 128]], [wd[1] + 0.24, [100, 100], 80, 20], [sp.dur, [104, 104]]]);
        keys(O(w.main), [[wd[1], 0], [wd[1] + 0.06, 100]]);
        // a thin rule under each word draws out from the centre
        var r = rect(w.main), wl = r.width * 0.62;
        var ln = rrect(c, "rule " + i, wl, 6, 3, (i == 1 ? GREEN : WHITE), null, 0, 540, wd[2] + r.height * 0.5 + 34);
        keys(S(ln), [[wd[1] + 0.12, [0, 100]], [wd[1] + 0.42, [100, 100], 80, 20]]);
        keys(O(ln), [[wd[1] + 0.11, 0], [wd[1] + 0.12, 90]]);
        shadow(ln, 0.5, 2, 10);
    }
    var fl = solid(c, "flash", [1, 1, 1]); keys(O(fl), [[0, 0], [0.033, 24], [0.15, 0]]);
    return c;
}
// question card, v2 exits: 'cut' (stays to the end) or 'pop' (snaps away in the last 0.12 s)
function qcard2(sp) {
    var inner = newComp(sp.name + " card", sp.dur);
    var cardW = 900, x0 = 90, padX = 44, cy = 1520;
    var q = boxTxt(inner, sp.q, SEMI, 54, INK, cardW - 2 * padX, 64, x0 + padX, 0);
    var rq = rect(q), cardH = 40 + 80 + 26 + rq.height + 46, top = cy - cardH / 2;
    P(q).setValue([x0 + padX - rq.left, top + 40 + 80 + 26 - rq.top]);
    var card = rrect(inner, "card", cardW, cardH, 42, WHITE, null, 0, 540, cy);
    card.moveToEnd();
    var av = imageLayer(inner, "avatar_src.png");
    S(av).setValue([80 / 3.8, 80 / 3.8]); P(av).setValue([x0 + padX + 40, top + 40 + 40]);
    var avm = ellipse(inner, "avatar mask", 80, WHITE, null, 0, x0 + padX + 40, top + 40 + 40);
    avm.moveBefore(av); matte(av, avm);
    ellipse(inner, "avatar ring", 86, null, RED, 3, x0 + padX + 40, top + 40 + 40);
    txt(inner, "ASK PAULA", KICK, 30, RED, ParagraphJustification.LEFT_JUSTIFY, 160, x0 + padX + 98, top + 40 + 51);
    txt(inner, "Your question", SEMI, 24, [0.45, 0.46, 0.5], ParagraphJustification.LEFT_JUSTIFY, 20, x0 + padX + 98, top + 40 + 82);
    try {
        var an = q.property("ADBE Text Properties").property("ADBE Text Animators").addProperty("ADBE Text Animator");
        an.property("ADBE Text Animator Properties").addProperty("ADBE Text Opacity").setValue(0);
        var sel = an.property("ADBE Text Selectors").addProperty("ADBE Text Selector");
        sel.property("ADBE Text Range Advanced").property("ADBE Text Range Type2").setValue(3);
        keys(sel.property("ADBE Text Percent Start"), [[sp.tA, 0], [sp.tB, 100]]);
    } catch (e) { log(sp.name + " type-on failed: " + e.toString()); }
    var c = newComp(sp.name, sp.dur), L = c.layers.add(inner);
    A(L).setValue([540, cy]); P(L).setValue([540, cy]);
    var sk = [[0, [72, 72]], [0.17, [104, 104], 33, 50], [0.3, [100, 100], 50, 33]];
    if (sp.exit == "pop") sk = sk.concat([[sp.dur - 0.13, [100, 100], 33, 60], [sp.dur - 0.01, [0, 0], 85, 33]]);
    keys(S(L), sk);
    keys(R(L), [[0, -5], [0.3, 0]]);
    keys(O(L), [[0, 0], [0.08, 100]]);
    shadow(L, 0.32, 16, 60);
    return c;
}
// article card (any image): sp.img, iw, ih, cw (card px), hl:[[x0,x1,y0,y1,t0,t1]] in image px, exit 'cut'|'pop', y
function article2(sp) {
    var pad = 30, sc = (sp.cw - 2 * pad) / sp.iw, ch = Math.round(sp.ih * sc + 2 * pad), cw = sp.cw;
    var inner = app.project.items.addComp(sp.name + " card", cw, ch, 1, sp.dur, FPS);
    rrect(inner, "paper", cw, ch, 28, WHITE, null, 0, cw / 2, ch / 2);
    var img = imageLayer(inner, sp.img);
    S(img).setValue([sc * 100, sc * 100]); P(img).setValue([cw / 2, ch / 2]);
    for (var i = 0; i < sp.hl.length; i++) {
        var h = sp.hl[i], x0 = pad + (h[0] - 6) * sc, x1 = pad + (h[1] + 6) * sc, y0 = pad + (h[2] - 2) * sc, y1 = pad + (h[3] + 4) * sc;
        var hl = rrect(inner, "highlight " + i, x1 - x0, y1 - y0, 6, HL, null, 0, 0, 0);
        A(hl).setValue([-(x1 - x0) / 2, 0]); P(hl).setValue([x0, (y0 + y1) / 2]);
        hl.blendingMode = BlendingMode.MULTIPLY; O(hl).setValue(88);
        keys(S(hl), [[h[4], [0, 100]], [h[5], [100, 100], 50, 50]]);
    }
    var c = newComp(sp.name, sp.dur);
    var bd = solid(c, "dim", [0, 0, 0]);
    var y = sp.y || 930;
    var L = c.layers.add(inner); L.threeDLayer = true;
    A(L).setValue([cw / 2, ch / 2, 0]); P(L).setValue([540, y, 0]);
    var sk = [[0, [90, 90, 90]], [0.45, [100, 100, 100], 70, 33], [sp.dur, [104, 104, 104]]];
    if (sp.exit == "pop") {
        sk = [[0, [90, 90, 90]], [0.45, [100, 100, 100], 70, 33], [sp.dur - 0.14, [103, 103, 103]], [sp.dur - 0.01, [0, 0, 0], 85, 33]];
        keys(O(bd), [[0, 0], [0.3, 42], [sp.dur - 0.14, 42], [sp.dur - 0.01, 0]]);
    } else keys(O(bd), [[0, 0], [0.3, 42]]);
    keys(S(L), sk);
    keys(tr(L).property("ADBE Rotate Y"), [[0, -30], [0.5, -7, 70, 33], [sp.dur, -2]]);
    keys(tr(L).property("ADBE Rotate X"), [[0, 9], [0.5, 2, 70, 33], [sp.dur, 0]]);
    keys(O(L), [[0, 0], [0.12, 100]]);
    shadow(L, 0.45, 22, 70);
    return c;
}
// ---------------------------------------------------------------- glass card v2 (the blur comes from a masked adjustment layer in Premiere)
// sp: name, dur, x0, y0, w, kick:[[word,t]], main:[[line,t]], tIn, tOut (-1 = none), p2:{t, noun, def}
var GEOM = {};
function rrShape(comp, name, w, h, r, fill, fillOp, stroke, sw, strokeOp, x0, y0) {
    var l = comp.layers.addShape(); l.name = name;
    var gc = shapeGroup(l);
    var rc = gc.addProperty("ADBE Vector Shape - Rect");
    rc.property("ADBE Vector Rect Size").setValue([w, h]); rc.property("ADBE Vector Rect Position").setValue([w / 2, h / 2]);
    rc.property("ADBE Vector Rect Roundness").setValue(r);
    if (stroke) { var st = gc.addProperty("ADBE Vector Graphic - Stroke"); st.property("ADBE Vector Stroke Color").setValue(stroke); st.property("ADBE Vector Stroke Width").setValue(sw); st.property("ADBE Vector Stroke Opacity").setValue(strokeOp); }
    if (fill) { var f = gc.addProperty("ADBE Vector Graphic - Fill"); f.property("ADBE Vector Fill Color").setValue(fill); f.property("ADBE Vector Fill Opacity").setValue(fillOp); }
    P(l).setValue([x0, y0]); A(l).setValue([0, 0]);
    return l;
}
function glass2(sp) {
    var c = newComp(sp.name, sp.dur);
    var x0 = sp.x0, y0 = sp.y0, w = sp.w, pad = 32, row = 46, r = 28, maxW = w - 2 * pad;
    var size = 112, widest = 0, tmp, i;
    for (i = 0; i < sp.main.length; i++) { tmp = txt(c, sp.main[i][0], BIG, size, WHITE, ParagraphJustification.LEFT_JUSTIFY, 12, 0, 0); widest = Math.max(widest, rect(tmp).width); tmp.remove(); }
    if (widest > maxW) size = size * maxW / widest;
    var capH = size * 0.74, gap = size * 0.96;
    var h1 = Math.round(pad + row + 18 + capH + gap * (sp.main.length - 1) + pad), h2 = h1;
    var defL = null, nounL = null;
    if (sp.p2) {
        nounL = txt(c, sp.p2.noun, SERIFI, 33, GREEN, ParagraphJustification.LEFT_JUSTIFY, 0, x0 + pad, y0 + h1 + 8);
        defL = boxTxt(c, sp.p2.def, SEMI, 34, [0.96, 0.97, 0.98], maxW, 42, x0 + pad, y0 + h1 + 28);
        h2 = Math.round(h1 + 28 + rect(defL).height + pad);
    }
    var tIn = sp.tIn, tOut = sp.tOut, tG = sp.p2 ? sp.p2.t : -1;
    function sx(t) { var v = easeOutCubic((t - tIn) / 0.38); if (tOut >= 0 && t >= tOut) v = 1 - easeInCubic((t - tOut) / 0.25); return v; }
    function hh(t) { return (tG >= 0) ? h1 + (h2 - h1) * easeInOutCubic((t - tG) / 0.30) : h1; }
    GEOM[sp.name] = {x0: x0, y0: y0, w: w, h1: h1, h2: h2, r: r, tIn: tIn, tOut: tOut, tG: tG, dur: sp.dur};
    var shadowL = rrShape(c, "glass shadow", w, h2, r, [0, 0, 0], 100, null, 0, 0, x0, y0 + 14);
    O(shadowL).setValue(20); var gb = fx(shadowL, "ADBE Gaussian Blur 2"); gb.property("ADBE Gaussian Blur 2-0001").setValue(34);
    var tint = rrShape(c, "glass tint", w, h2, r, [0.02, 0.03, 0.05], 22, null, 0, 0, x0, y0);
    var sheen = rrShape(c, "glass sheen", w, h2, r, [1, 1, 1], 100, null, 0, 0, x0, y0);
    var rmp = fx(sheen, "ADBE Ramp");
    rmp.property("ADBE Ramp-0001").setValue([x0, y0]); rmp.property("ADBE Ramp-0002").setValue([1, 1, 1]);
    rmp.property("ADBE Ramp-0003").setValue([x0, y0 + 160]); rmp.property("ADBE Ramp-0004").setValue([1, 1, 1]);
    O(sheen).setValue(9);
    try { fx(sheen, "ADBE Set Matte3"); } catch (eM) { }
    var sheenMask = sheen.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
    var ms = new Shape(); ms.vertices = [[x0 - 10, y0 - 10], [x0 + w + 10, y0 - 10], [x0 + w + 10, y0 + 70], [x0 - 10, y0 + 70]]; ms.closed = true;
    sheenMask.property("ADBE Mask Shape").setValue(ms); sheenMask.property("ADBE Mask Feather").setValue([0, 60]);
    var edge = rrShape(c, "glass edge", w, h2, r, null, 0, [1, 1, 1], 1.5, 100, x0, y0);
    O(edge).setValue(34);
    var cards = [shadowL, tint, sheen, edge];
    // per-frame width (reveal / exit) and height (dictionary growth); hold outside the windows
    for (var k = 0; k < cards.length; k++) {
        var rp = findIn(cards[k], "ADBE Vector Shape - Rect");
        var sz = rp.property("ADBE Vector Rect Size"), ps = rp.property("ADBE Vector Rect Position");
        var wins = [[tIn, tIn + 0.38]];
        if (tG >= 0) wins.push([tG, tG + 0.30]);
        if (tOut >= 0) wins.push([tOut, tOut + 0.25]);
        for (var wi = 0; wi < wins.length; wi++) {
            (function (a, b) {
                frameKeys(sz, a, b, function (t) { return [Math.max(0.01, w * sx(t)), hh(t)]; });
                frameKeys(ps, a, b, function (t) { return [w * sx(t) / 2, hh(t) / 2]; });
            })(wins[wi][0], wins[wi][1]);
        }
    }
    // content
    var tx = x0 + pad + 22, ty = y0 + pad + 22;
    var ic = ellipse(c, "tick circle", 44, GREEN, null, 0, tx, ty);
    keys(S(ic), [[tIn + 0.15, [0, 0]], [tIn + 0.29, [118, 118]], [tIn + 0.41, [100, 100]]]);
    var tk = tickPath(c, "tick", 28, WHITE, 6, tx, ty + 2);
    keys(findIn(tk, "ADBE Vector Filter - Trim").property("ADBE Vector Trim End"), [[tIn + 0.25, 0], [tIn + 0.45, 100, 33, 70]]);
    var content = [ic, tk];
    var kx = tx + 38;
    for (i = 0; i < sp.kick.length; i++) {
        var kw = txt(c, sp.kick[i][0], KICK, 30, WHITE, ParagraphJustification.LEFT_JUSTIFY, 130, kx, ty + 11);
        var kr = rect(kw); var t0 = sp.kick[i][1];
        keys(O(kw), [[t0, 0], [t0 + 0.22, 95]]);
        keys(P(kw), [[t0, [kx, ty + 24]], [t0 + 0.3, [kx, ty + 10], 70, 33]]);
        blurIn(kw, t0, 10, 0.2);
        shadow(kw, 0.45, 2, 10);
        kx += kr.width + 14; content.push(kw);
    }
    for (var m = 0; m < sp.main.length; m++) {
        var by = y0 + pad + row + 18 + capH + gap * m, tm = sp.main[m][1];
        var mn = txt(c, sp.main[m][0], BIG, size, WHITE, ParagraphJustification.LEFT_JUSTIFY, 12, x0 + pad - 4, by);
        gradText(mn, WHITE, [0.86, 0.88, 0.91]); shadow(mn, 0.45, 4, 20);
        keys(O(mn), [[tm, 0], [tm + 0.12, 100]]);
        keys(P(mn), [[tm, [x0 + pad - 4, by + 30]], [tm + 0.3, [x0 + pad - 4, by], 80, 20]]);
        blurIn(mn, tm, 18, 0.22); content.push(mn);
    }
    if (sp.p2) {
        var tp = sp.p2.t;
        keys(O(nounL), [[tp + 0.12, 0], [tp + 0.32, 100]]);
        keys(O(defL), [[tp + 0.2, 0], [tp + 0.42, 100]]);
        var pd = P(defL).value; keys(P(defL), [[tp + 0.2, [pd[0], pd[1] + 16]], [tp + 0.46, pd, 70, 33]]);
        shadow(nounL, 0.4, 2, 10); shadow(defL, 0.45, 2, 12);
        content.push(nounL); content.push(defL);
    }
    if (tOut >= 0) for (var q = 0; q < content.length; q++) {
        var o = O(content[q]); o.setValueAtTime(tOut, o.valueAtTime(tOut, false)); o.setValueAtTime(tOut + 0.12, 0);
    }
    return c;
}
// ---------------------------------------------------------------- 100x meter v2: stops at the track end with a closing tick
function meter2(sp) {
    var c = newComp(sp.name, sp.dur);
    var bd = backdrop(c, -100, 820, 360, 58, null); keys(O(bd), [[0, 0], [0.2, 58], [sp.fo, 58], [sp.dur, 0]]);
    var X0 = 90, X1 = 990, Y = 620, TW = X1 - X0;
    var prog = "clamp((time - " + sp.c0 + ") / " + (sp.c1 - sp.c0) + ", 0, 1)";
    var ease = "var u = " + prog + "; var e = u < 0.5 ? 4*u*u*u : 1 - Math.pow(-2*u + 2, 3) / 2;";
    var lb = txt(c, "THE DAILY AMOUNT OF VITAMIN C", KICK, 31, WHITE, ParagraphJustification.LEFT_JUSTIFY, 120, 92, 545);
    keys(O(lb), [[0.05, 0], [0.3, 95]]);
    var num = txt(c, "100x", BIG, 250, WHITE, ParagraphJustification.LEFT_JUSTIFY, 8, 84, 470);
    num.property("Source Text").expression = ease + " Math.round(1 + 99 * e) + 'x'";
    shadow(num, 0.5, 5, 24);
    var gn = glow(num, 50, 30, 0.0); keys(gn.property("Glow Intensity"), [[sp.c1, 0], [sp.c1 + 0.1, 0.9], [sp.c1 + 0.6, 0.35]]);
    keys(O(num), [[0.05, 0], [0.25, 100]]);
    var track = rrect(c, "track", TW, 40, 20, WHITE, WHITE, 2, 540, Y); keys(O(track), [[0.05, 0], [0.3, 18]]);
    var mk = rrect(c, "need marker", 5, 76, 2, WHITE, null, 0, X0 + 11, Y);
    var ml = txt(c, "DAILY NEED", KICK, 21, WHITE, ParagraphJustification.LEFT_JUSTIFY, 100, 92, 690);
    keys(O(mk), [[0.15, 0], [0.35, 100]]); keys(O(ml), [[0.15, 0], [0.35, 90]]);
    var bar = c.layers.addShape(); bar.name = "fill";
    var gc = shapeGroup(bar);
    var rc = gc.addProperty("ADBE Vector Shape - Rect"); rc.property("ADBE Vector Rect Roundness").setValue(20);
    gc.addProperty("ADBE Vector Graphic - Fill");
    var rs = findIn(bar, "ADBE Vector Shape - Rect"), fill = findIn(bar, "ADBE Vector Graphic - Fill");
    rs.property("ADBE Vector Rect Size").expression = ease + " [Math.max(10, " + TW + " * e), 40]";
    rs.property("ADBE Vector Rect Position").expression = ease + " [Math.max(10, " + TW + " * e) / 2, 0]";
    fill.property("ADBE Vector Fill Color").expression = ease + " var g=[0.204,0.82,0.482,1], y=[1,0.79,0.235,1], r=[1,0.231,0.188,1]; e<0.55 ? linear(e,0,0.55,g,y) : linear(e,0.55,1,y,r);";
    P(bar).setValue([X0, Y]);
    glow(bar, 62, 24, 0.5);
    keys(O(bar), [[sp.c0 - 0.02, 0], [sp.c0, 100]]);
    // closing tick + label at the end of the track
    var ek = rrect(c, "dose marker", 5, 76, 2, RED, null, 0, X1 - 3, Y);
    var el = txt(c, sp.endLabel, KICK, 21, RED, ParagraphJustification.RIGHT_JUSTIFY, 100, X1, 690);
    keys(O(ek), [[sp.c1 - 0.02, 0], [sp.c1 + 0.06, 100]]); keys(S(ek), [[sp.c1 - 0.02, [100, 40]], [sp.c1 + 0.14, [100, 100], 70, 33]]);
    keys(O(el), [[sp.c1, 0], [sp.c1 + 0.2, 100]]);
    keys(P(el), [[sp.c1, [X1, 706]], [sp.c1 + 0.26, [X1, 690], 70, 33]]);
    shadow(el, 0.5, 2, 10);
    // the whole graphic eases out and finishes exactly on the B-roll cut
    var all = [lb, num, track, mk, ml, bar, ek, el];
    for (var i = 0; i < all.length; i++) { var o = O(all[i]); o.setValueAtTime(sp.fo, o.valueAtTime(sp.fo, false)); o.setValueAtTime(sp.dur - 1 / FPS, 0); }
    return c;
}
// ---------------------------------------------------------------- tracked "?" on the whiteboard (pre-zoom track)
// sp: name, dur, track:[[t, x, y, rotDeg, scale%]], tIn, tOut
function qmark(sp) {
    var c = newComp(sp.name, sp.dur);
    var nl = c.layers.addNull(sp.dur); nl.name = "board track";
    var ts = [], ps = [], rs = [], ss = [];
    for (var i = 0; i < sp.track.length; i++) { ts.push(sp.track[i][0]); ps.push([sp.track[i][1], sp.track[i][2]]); rs.push(sp.track[i][3]); ss.push([sp.track[i][4], sp.track[i][4]]); }
    P(nl).setValuesAtTimes(ts, ps); R(nl).setValuesAtTimes(ts, rs); S(nl).setValuesAtTimes(ts, ss);
    var halo = ellipse(c, "halo", 300, WHITE, null, 0, 0, 0); halo.parent = nl; P(halo).setValue([0, 0]);
    fx(halo, "ADBE Gaussian Blur 2").property("ADBE Gaussian Blur 2-0001").setValue(70); O(halo).setValue(0);
    keys(O(halo), [[sp.tIn, 0], [sp.tIn + 0.3, 26], [sp.tOut, 26], [sp.tOut + 0.15, 0]]);
    var q = txt(c, "?", BIG, 360, WHITE, ParagraphJustification.CENTER_JUSTIFY, 0, 0, 0);
    centreAnchor(q); q.parent = nl; P(q).setValue([0, 0]);
    gradText(q, WHITE, [0.88, 0.9, 0.93]); shadow(q, 0.6, 6, 30); glow(q, 70, 18, 0.25);
    keys(S(q), [[sp.tIn, [0, 0]], [sp.tIn + 0.2, [116, 116], 33, 60], [sp.tIn + 0.34, [100, 100], 60, 33], [sp.tOut, [100, 100]], [sp.tOut + 0.15, [0, 0], 85, 33]]);
    q.property("ADBE Transform Group").property("ADBE Position").expression = "value + [0, Math.sin((time - " + sp.tIn + ") * 7.5) * 7]";
    q.property("ADBE Transform Group").property("ADBE Rotate Z").expression = "Math.sin((time - " + sp.tIn + ") * 5.2) * 3";
    q.motionBlur = true; c.motionBlur = true;
    return c;
}
// ---------------------------------------------------------------- immune window (held record): 20 -> 20-30 MINUTES
function windowGfx(sp) {
    var c = newComp(sp.name, sp.dur);
    backdrop(c, -100, 820, 360, 58, 0);
    var k = txt(c, "VULNERABLE FOR", KICK, 40, RED, ParagraphJustification.CENTER_JUSTIFY, 200, 540, 300);
    shadow(k, 0.55, 3, 14); keys(O(k), [[sp.tK, 0], [sp.tK + 0.16, 100]]); keys(P(k), [[sp.tK, [540, 326]], [sp.tK + 0.22, [540, 300], 70, 33]]);
    var n = txt(c, "20–30", BIG, 280, WHITE, ParagraphJustification.CENTER_JUSTIFY, 6, 540, 580);
    var r = rect(n); A(n).setValue([r.left + r.width / 2, r.top + r.height / 2]); P(n).setValue([540 + r.left + r.width / 2, 580 + r.top + r.height / 2]);
    n.property("Source Text").expression = "time < " + sp.t30 + " ? String(Math.round(ease(time, " + sp.a + ", " + sp.b + ", 0, 20))) : '20–30';";
    gradText(n, WHITE, GREY); shadow(n, 0.55, 5, 24); glow(n, 60, 20, 0.3);
    keys(O(n), [[sp.a - 0.02, 0], [sp.a + 0.06, 100]]);
    keys(S(n), [[sp.a, [92, 92]], [sp.a + 0.2, [100, 100]], [sp.t30 - 0.01, [100, 100]], [sp.t30 + 0.07, [110, 110]], [sp.t30 + 0.26, [100, 100]]]);
    var u = txt(c, "MINUTES", KICK, 40, WHITE, ParagraphJustification.CENTER_JUSTIFY, 220, 540, 676);
    shadow(u, 0.55, 3, 14); keys(O(u), [[sp.tU, 0], [sp.tU + 0.16, 100]]); keys(P(u), [[sp.tU, [540, 700]], [sp.tU + 0.22, [540, 676], 70, 33]]);
    return c;
}
function flashGfx(sp) {
    var c = newComp(sp.name, sp.dur);
    var fl = solid(c, "flash", [1, 1, 1]); keys(O(fl), [[0, 0], [0.04, 62], [sp.dur, 0, 33, 60]]);
    return c;
}
