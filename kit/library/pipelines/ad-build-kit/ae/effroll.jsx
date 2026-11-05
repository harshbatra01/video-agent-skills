
// ---------------------------------------------------------------- EFFICIENTLY -> EFFECTIVELY: EFF and LY stay put, the middle rolls like a counter
// sp: name, dur, kick:[[text,color]], kIn, pre, midA, midB, post, t0 (first word in), tR (roll starts)
function effRoll(sp) {
    var c = newComp(sp.name, sp.dur);
    c.motionBlur = true;
    backdrop(c, 980, H + 80, 420, 74, 0);
    kickRow(c, sp.kick, sp.kIn, KICK_Y);
    var wordA = sp.pre + sp.midA + sp.post, wordB = sp.pre + sp.midB + sp.post;
    var size = 236, base = MAIN_Y, k;
    function inkW(s2, sz) { var l = txt(c, s2, BIG, sz, WHITE, ParagraphJustification.LEFT_JUSTIFY, 14, 0, 0); var r = rect(l); l.remove(); return r; }
    var mA = inkW(wordA, size), mB = inkW(wordB, size);
    if (Math.max(mA.width, mB.width) > 960) { size = size * 960 / Math.max(mA.width, mB.width); mA = inkW(wordA, size); mB = inkW(wordB, size); }
    var capH = mA.height;
    var inner = app.project.items.addComp(sp.name + " word", W, H, 1, sp.dur, FPS);
    inner.motionBlur = true;
    function piece(s2) {
        var l = txt(inner, s2, BIG, size, WHITE, ParagraphJustification.LEFT_JUSTIFY, 14, 0, base);
        l.motionBlur = true;
        return [l, rect(l)];
    }
    var pre = piece(sp.pre), post = piece(sp.post), mida = piece(sp.midA), midb = piece(sp.midB);
    // spacing that reproduces each full word's set width
    var gapA = (mA.width - pre[1].width - mida[1].width - post[1].width) / 2;
    var gapB = (mB.width - pre[1].width - midb[1].width - post[1].width) / 2;
    var leftA = 540 - mA.width / 2, leftB = 540 - mB.width / 2;
    var tR = sp.tR, D = 0.24, travel = capH + 60;
    function u(t) { return easeInOutCubic((t - tR) / D); }
    function left(t) { return leftA + (leftB - leftA) * u(t); }
    function px(pc, inkLeft) { return inkLeft - pc[1].left; }
    function gap(t) { return gapA + (gapB - gapA) * u(t); }
    frameKeys(P(pre[0]), tR, tR + D, function (t) { return [px(pre, left(t)), base]; });
    frameKeys(P(mida[0]), tR, tR + D, function (t) { return [px(mida, left(t) + pre[1].width + gap(t)), base - travel * u(t)]; });
    frameKeys(P(midb[0]), tR, tR + D, function (t) { return [px(midb, left(t) + pre[1].width + gap(t)), base + travel * (1 - u(t))]; });
    frameKeys(P(post[0]), tR, tR + D, function (t) {
        var wm = mida[1].width + (midb[1].width - mida[1].width) * u(t);
        return [px(post, left(t) + pre[1].width + gap(t) + wm + gap(t)), base];
    });
    // fixed window: the middle letters roll in and out of the word band only
    var x0 = Math.min(leftA, leftB) - 40, x1 = Math.max(leftA + mA.width, leftB + mB.width) + 40;
    var wins = [];
    for (k = 0; k < 2; k++) {
        var wl = inner.layers.addShape(); wl.name = "roll window " + k;
        var gc = shapeGroup(wl), rc = gc.addProperty("ADBE Vector Shape - Rect");
        rc.property("ADBE Vector Rect Size").setValue([x1 - x0, capH + 30]); rc.property("ADBE Vector Rect Position").setValue([0, 0]);
        gc.addProperty("ADBE Vector Graphic - Fill").property("ADBE Vector Fill Color").setValue([1, 1, 1]);
        A(wl).setValue([0, 0]); P(wl).setValue([(x0 + x1) / 2, base - capH / 2 + 2]);
        wins.push(wl);
    }
    matte(mida[0], wins[0]); matte(midb[0], wins[1]);
    for (k = 0; k < 2; k++) { try { wins[k].enabled = false; } catch (eW) { } }
    var pcs = [pre[0], post[0], mida[0], midb[0]];
    for (k = 0; k < pcs.length; k++) gradText(pcs[k], WHITE, GREY);
    // outer: main + RGB ghosts; pop on the first word, punch + ghost flash on the roll
    var cy = base - capH / 2;
    function lay() { var L = c.layers.add(inner); A(L).setValue([540, cy]); P(L).setValue([540, cy]); L.motionBlur = true; return L; }
    var red = lay(), cyan = lay(), main = lay();
    fx(red, "ADBE Fill").property("Color").setValue([1, 0.05, 0.25]); fx(cyan, "ADBE Fill").property("Color").setValue([0.0, 0.85, 1]);
    red.blendingMode = BlendingMode.ADD; cyan.blendingMode = BlendingMode.ADD;
    var t0 = sp.t0, end = sp.dur;
    var sk = [[t0, [128, 128]], [t0 + 0.24, [100, 100], 80, 20], [tR, [101.5, 101.5]], [tR + 0.1, [106, 106], 33, 60], [tR + 0.34, [101.5, 101.5], 60, 33], [end, [103.5, 103.5]]];
    keys(S(main), sk); keys(S(red), sk); keys(S(cyan), sk);
    keys(O(main), [[t0, 0], [t0 + 0.06, 100]]);
    keys(P(red), [[t0, [540 - 22, cy]], [t0 + 0.24, [540, cy], 70, 33], [tR, [540, cy]], [tR + 0.05, [540 - 16, cy]], [tR + 0.26, [540, cy], 70, 33]]);
    keys(P(cyan), [[t0, [540 + 22, cy]], [t0 + 0.24, [540, cy], 70, 33], [tR, [540, cy]], [tR + 0.05, [540 + 16, cy]], [tR + 0.26, [540, cy], 70, 33]]);
    keys(O(red), [[t0, 0], [t0 + 0.04, 75], [t0 + 0.3, 0], [tR, 0], [tR + 0.04, 60], [tR + 0.28, 0]]);
    keys(O(cyan), [[t0, 0], [t0 + 0.04, 75], [t0 + 0.3, 0], [tR, 0], [tR + 0.04, 60], [tR + 0.28, 0]]);
    glow(main, 60, 22, 0.35); shadow(main, 0.55, 5, 26); blurIn(main, t0, 26, 0.2);
    return c;
}
