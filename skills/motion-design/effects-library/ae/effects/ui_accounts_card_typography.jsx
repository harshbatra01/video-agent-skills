// meta key: ui_accounts_card_typography
// meta title: Typography Rules
// meta order: 18
// meta refs: analysis/DbBHl9XPUvz/ref_ui_accounts_card_typography_14.00.png, analysis/DbBHl9XPUvz/ref_ui_accounts_card_typography_16.00.png, analysis/DbBHl9XPUvz/ref_ui_accounts_card_typography_20.00.png, analysis/DbBHl9XPUvz/ref_ui_accounts_card_typography_36.00.png, analysis/DbBHl9XPUvz/ref_ui_accounts_card_typography_41.00.png
// Staged copy: neutral names, fonts from FONTS (lib/effects_lib.jsx). Source: a friend's Mac effects library (Oct 2026).
// Technique demo (reel DbBHl9XPUvz, "UI design fundamentals part 1: typography"). The three rules are shown on the dark
// Accounts card with real AE features: letter spacing = a Source Text expression reading the CONTROLS sliders Track Big /
// Track Small (keyed), size = every text layer's size is Base Size / Size Ratio ^ tier (the reel's divide-by-1.25 rule,
// live), weight = hold keys on Source Text switching fonts. Focus-dim = the reel's 10-frame Easy Ease opacity pairs.
// Card measured on the reel (36.0 s frame) and laid out at 1.1x reel pixels around the frame centre.
function build_ui_accounts_card_typography() {
    var T = "Typography Rules";
    var NF = 180, D = NF / FPS, K = 1.1, DIM = 38;
    var BASE = 41, RATIO = 1.25;
    var B_LS1 = 10, B_LS2 = 40, B_OPEN = 58, B_SIZE = 78, B_FLAT = 84, B_FIX = 100, B_WEIGHT = 120, B_W1 = 126, B_W2 = 150;
    var IR = FONTS.uiRegular, IM = FONTS.uiMedium, IS = FONTS.uiSemiBold, IL = FONTS.uiLight, IB = FONTS.uiBold;
    var WHITE = [1, 1, 1];

    function X(x) { return 960 + (x - 538) * K; }
    function Y(y) { return 540 + (y - 987) * K; }
    function tierSize(t) { return BASE / Math.pow(RATIO, t); }

    var c = effectComp(T, D);
    c.motionBlur = true;
    try { c.shutterAngle = 180; } catch (es) {}
    solidL(c, "BG", hex("#FDFDFD"));

    // ---------------------------------------------------------------- CONTROLS (sizes + tracking live here)
    var ctl = controls(c);
    var sBase = slider(ctl, "Base Size", BASE);
    var sRatio = slider(ctl, "Size Ratio", RATIO);
    var sBig = slider(ctl, "Track Big", 10);
    var sSmall = slider(ctl, "Track Small", -170);

    // nulls with anchor = position, so children parented to them keep plain comp coordinates
    var drift = c.layers.addNull(D); drift.name = "DRIFT"; A(drift).setValue([960, 540]); P(drift).setValue([960, 540]);
    var CYC = Y(956);
    var cardN = c.layers.addNull(D); cardN.name = "CARD_NULL"; A(cardN).setValue([960, CYC]); P(cardN).setValue([960, CYC]);
    cardN.parent = drift;

    // ---------------------------------------------------------------- card shapes (bottom to top)
    var outer = rrect(c, "OUTER", 764 * K, 478 * K, 70 * K, hex("#030509"), null, 0, X(538), Y(956));
    var inner = rrect(c, "INNER", 706 * K, 337 * K, 45 * K, hex("#121418"), hex("#1A1C20"), 1.5, X(539), Y(997.5));
    var divider = rrect(c, "DIVIDER", 647 * K, 1.6, 0, hex("#1F2125"), null, 0, X(538.5), Y(972));
    var tile1 = rrect(c, "ICON_TILE 1", 54 * K, 52 * K, 12 * K, hex("#000000"), null, 0, X(242), Y(1024));
    var dia = rrect(c, "ICON 1 diamond", 17 * K, 17 * K, 2, null, hex("#E9A23B"), 2.6, X(242), Y(1024)); R(dia).setValue(45);
    var diaC = rrect(c, "ICON 1 diamond core", 6 * K, 6 * K, 1, hex("#E9A23B"), null, 0, X(242), Y(1024)); R(diaC).setValue(45);
    var tile2 = rrect(c, "ICON_TILE 2", 54 * K, 52 * K, 12 * K, hex("#000000"), null, 0, X(242), Y(1104));
    var pBack = txt(c, "P", IB, 30 * K, hex("#4C3FA8"), ParagraphJustification.CENTER_JUSTIFY, 0, X(242), Y(1104));
    pBack.name = "ICON 2 P shade"; centreAnchor(pBack); P(pBack).setValue([X(242) + 2, Y(1104) + 1.5]);
    var pFront = txt(c, "P", IB, 30 * K, hex("#8C7CF0"), ParagraphJustification.CENTER_JUSTIFY, 0, X(242), Y(1104));
    pFront.name = "ICON 2 P"; centreAnchor(pFront); P(pFront).setValue([X(242) - 1, Y(1104) - 1]);

    // ---------------------------------------------------------------- text layers: size from CONTROLS by tier
    function sizeExpr(tier, track) {
        var e = 'var c = thisComp.layer("CONTROLS");\n' +
                'var tier = ' + tier + ';   // 0 = biggest, each step down = divide by the Size Ratio\n' +
                'var size = c.effect("Base Size")("Slider") / Math.pow(c.effect("Size Ratio")("Slider"), tier);\n' +
                'text.sourceText.style.setFontSize(size)';
        if (track) e += '.setTracking(c.effect("' + track + '")("Slider"))';
        return e;
    }
    function tl(name, s, font, tier, col, just, track, x, y, trackSlider) {
        var l = txt(c, s, font, tierSize(tier), col, just, track, X(x), Y(y));
        l.name = name;
        l.property("Source Text").expression = sizeExpr(tier, trackSlider);
        return l;
    }
    var LJ = ParagraphJustification.LEFT_JUSTIFY, RJ = ParagraphJustification.RIGHT_JUSTIFY;
    var tAcc = tl("TXT_Accounts", "Accounts", IM, 1, WHITE, LJ, -10, 216, 797);
    var tTot = tl("TXT_Total", "Total", IR, 2, hex("#9EA0A4"), LJ, -28, 218, 889);
    var tBal = tl("TXT_Balance", "$4,237.23", IS, 0, WHITE, LJ, 0, 218, 937, "Track Big");
    var tL30 = tl("TXT_Last30", "last 30 days", IR, 3, hex("#999B9F"), RJ, 0, 862, 923);
    var tN1 = tl("TXT_Name1", "Crypto", IM, 1, WHITE, LJ, -60, 293, 1035);
    var tA1 = tl("TXT_Amt1", "$2,237.23", IM, 1, WHITE, RJ, 0, 858, 1034, "Track Small");
    var tN2 = tl("TXT_Name2", "Payments", IM, 1, WHITE, LJ, -60, 293, 1114);
    var tA2 = tl("TXT_Amt2", "$2,000", IM, 1, WHITE, RJ, -60, 855, 1113);

    // re-fetch the sliders: adding effects to CONTROLS invalidates earlier effect references
    function ctlFx(nm) { return ctl.property("ADBE Effect Parade").property(nm); }
    sBase = ctlFx("Base Size"); sRatio = ctlFx("Size Ratio"); sBig = ctlFx("Track Big"); sSmall = ctlFx("Track Small");
    var cardLayers = [outer, inner, divider, tile1, dia, diaC, tile2, pBack, pFront, tAcc, tTot, tBal, tL30, tN1, tA1, tN2, tA2];
    for (var i = 0; i < cardLayers.length; i++) cardLayers[i].parent = cardN;

    // ---------------------------------------------------------------- letter spacing (CONTROLS sliders, 14-frame Easy Ease)
    kf(sBig.property(1), [[B_LS1, 10], [B_LS1 + 12, -65]]);
    kf(sSmall.property(1), [[B_OPEN, -170], [B_OPEN + 12, -60]]);
    // ---------------------------------------------------------------- size: all one size (ratio 1), then divide by 1.25 per step
    kf(sRatio.property(1), [[B_FLAT, RATIO], [B_FLAT + 10, 1], [B_FIX, 1], [B_FIX + 12, RATIO]]);

    // ---------------------------------------------------------------- focus-dim: 10-frame Easy Ease opacity pairs
    var EL = { acc: [tAcc], tot: [tTot], bal: [tBal], l30: [tL30], ic1: [tile1, dia, diaC], n1: [tN1], a1: [tA1], ic2: [tile2, pBack, pFront], n2: [tN2], a2: [tA2] };
    var FOCUS = [[0, ["bal"]], [B_LS2, ["a1"]], [B_SIZE, ["acc", "tot", "l30"]], [B_WEIGHT, ["acc", "tot", "bal", "l30", "ic1", "n1", "a1", "ic2", "n2", "a2"]]];
    function inSet(set, k) { for (var q = 0; q < set.length; q++) if (set[q] == k) return true; return false; }
    for (var k in EL) {
        var ops = [];
        for (var s = 0; s < FOCUS.length; s++) ops.push(inSet(FOCUS[s][1], k) ? 100 : DIM);
        var list = [[0, ops[0]]];
        for (var s2 = 1; s2 < FOCUS.length; s2++) {
            if (ops[s2] != ops[s2 - 1]) { list.push([FOCUS[s2][0], ops[s2 - 1]]); list.push([FOCUS[s2][0] + 10, ops[s2]]); }
        }
        for (var m = 0; m < EL[k].length; m++) kf(O(EL[k][m]), list);
    }

    // ---------------------------------------------------------------- weight: everything SemiBold looks flat, then lighter small text
    function fontKey(l, f, font) { var st = l.property("Source Text"); var d = st.valueAtTime(f / FPS, true); d.font = font; st.setValueAtTime(f / FPS, d); }
    var WT = [[tAcc, IM], [tTot, IR], [tL30, IR], [tN1, IM], [tA1, IM], [tN2, IM], [tA2, IM]];
    for (var w = 0; w < WT.length; w++) {
        fontKey(WT[w][0], 0, WT[w][1]);
        fontKey(WT[w][0], B_W1, IS);
        fontKey(WT[w][0], B_W2, WT[w][1]);
    }

    // ---------------------------------------------------------------- entry: card rises 88 px with vertical Directional Blur
    kf(P(cardN), [[2, [960, CYC + 88], 33, 12], [12, [960, CYC], 85, 33]]);
    var entry = adjL(c, "ENTRY BLUR (Directional Blur 0 deg)");
    fxp(entry, "ADBE Motion Blur", [["Direction", 0], ["Blur Length", 0]], "Directional Blur");
    kf(entry.property("ADBE Effect Parade").property("Directional Blur").property("Blur Length"), [[2, 46, 33, 15], [8, 0, 80, 33]]);
    entry.inPoint = 0; entry.outPoint = F(10);
    var pop = adjL(c, "WEIGHT POP (2-frame blur)");
    gaussBlur(pop, 0);
    kf(pop.property("ADBE Effect Parade").property(1).property("ADBE Gaussian Blur 2-0001"), [[B_W1 - 1, 0], [B_W1, 6], [B_W1 + 2, 0], [B_W2 - 1, 0], [B_W2, 6], [B_W2 + 2, 0]]);
    function F(f) { return f / FPS; }

    // ---------------------------------------------------------------- headers: old one lifts and fades, new one rises in (8 frames)
    var HX = X(303), HY = Y(666);
    var HEAD = [["Letter Spacing", -4, B_SIZE - 4], ["Size", B_SIZE - 4, B_WEIGHT - 4], ["Weight", B_WEIGHT - 4, NF + 10]];
    var heads = [];
    for (var h = 0; h < HEAD.length; h++) {
        var hl = txt(c, HEAD[h][0], IL, 92 * K, hex("#0B0B0D"), LJ, -115, HX, HY);
        hl.name = "HEADER " + HEAD[h][0];
        hl.parent = drift;
        var fi = HEAD[h][1], fo = HEAD[h][2];
        var hb = gaussBlur(hl, 0);
        var hbp = hl.property("ADBE Effect Parade").property(1).property("ADBE Gaussian Blur 2-0001");
        if (fi >= 0) {
            kf(P(hl), [[fi, [HX, HY + 26], 33, 15], [fi + 9, [HX, HY], 85, 33]]);
            kf(O(hl), [[fi, 0, 33, 15], [fi + 6, 100, 70, 33]]);
            kf(hbp, [[fi, 10, 33, 15], [fi + 7, 0, 75, 33]]);
        } else {
            kf(P(hl), [[0, [HX, HY + 18], 33, 15], [8, [HX, HY], 85, 33]]);
            kf(O(hl), [[0, 0, 33, 15], [5, 100, 70, 33]]);
            kf(hbp, [[0, 10, 33, 15], [6, 0, 75, 33]]);
        }
        if (fo < NF) {
            kf(P(hl), [[fo, [HX, HY], 33, 60], [fo + 8, [HX, HY - 30], 33, 33]]);
            kf(O(hl), [[fo, 100, 33, 40], [fo + 7, 0, 33, 33]]);
            kf(hbp, [[fo, 0, 33, 40], [fo + 7, 8, 33, 33]]);
            hl.outPoint = F(fo + 8);
        }
        if (fi > 0) hl.inPoint = F(fi);
        heads.push(hl);
    }

    // ---------------------------------------------------------------- captions: black, hard swap with a 2-frame blur pop
    var capL = [];
    var CAPS = [["big text", 3, 21], ["can go tight", 21, B_LS2], ["small text", B_LS2, B_OPEN], ["needs space", B_OPEN, B_SIZE],
                ["all one size", B_SIZE + 2, B_FIX - 2], ["divide by 1.25", B_FIX - 2, B_WEIGHT], ["looks flat", B_WEIGHT + 2, B_W2 - 2], ["go lighter", B_W2 - 2, NF]];
    for (var q = 0; q < CAPS.length; q++) {
        var cl = txt(c, CAPS[q][0], IM, 113 * K, hex("#000000"), ParagraphJustification.CENTER_JUSTIFY, -50, X(538), Y(1362));
        cl.name = "CAPTION " + CAPS[q][0];
        cl.parent = drift;
        cl.inPoint = F(CAPS[q][1]); cl.outPoint = F(CAPS[q][2]);
        gaussBlur(cl, 0);
        kf(cl.property("ADBE Effect Parade").property(1).property("ADBE Gaussian Blur 2-0001"), [[CAPS[q][1], 10, 33, 15], [CAPS[q][1] + 2, 0, 80, 33]]);
        capL.push(cl);
    }

    // slow upward drift of the whole layout (the reel keeps moving after the card lands)
    kf(P(drift), [[0, [960, 548]], [NF, [960, 532]]]); linearKeys(P(drift));

    // stack order: CONTROLS, captions, headers, blur adjustments, card layers, BG
    entry.moveToBeginning(); pop.moveToBeginning();
    for (var hh = 0; hh < heads.length; hh++) heads[hh].moveToBeginning();
    for (var cc = 0; cc < capL.length; cc++) capL[cc].moveToBeginning();
    cardN.moveToBeginning(); drift.moveToBeginning(); ctl.moveToBeginning();

    // check that the style expressions evaluate (AE 2020+ text style API)
    var chk = [tAcc, tBal, tA1, tL30];
    for (var z = 0; z < chk.length; z++) {
        try { chk[z].property("Source Text").valueAtTime(F(100), false); var er = chk[z].property("Source Text").expressionError; if (er) log("  EXPR ERROR " + chk[z].name + ": " + er); }
        catch (ez) { log("  expr check " + ez.toString()); }
    }
    try { log("  fonts: Light " + app.fonts.getFontsByPostScriptName(IL).length + ", Bold " + app.fonts.getFontsByPostScriptName(IB).length + ", Medium " + app.fonts.getFontsByPostScriptName(IM).length); } catch (ef) { log("  font check " + ef.toString()); }

    note(c, "Typography rules on a UI card. Letter spacing: big text can go tight (Track Big 10 to -65) while small text needs space (Track Small -170 to -60), both CONTROLS sliders read by a Source Text expression. Size: every text layer is Base Size / Size Ratio ^ tier, so key Size Ratio from 1 (all one size, flat) to 1.25 to get the divide-by-1.25 scale. Weight: hold keys on Source Text set everything SemiBold (flat), then the small text back to Medium and Regular; focus-dim is 10-frame Easy Ease opacity pairs to 38 %.");
    return c;
}
