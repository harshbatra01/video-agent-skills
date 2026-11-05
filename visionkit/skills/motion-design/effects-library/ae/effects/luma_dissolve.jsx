// meta key: luma_dissolve
// meta title: Luma Dissolve
// meta order: 2
// meta refs: analysis/DeURRG7vITo/ref_luma_dissolve_0.200.png, analysis/DeURRG7vITo/ref_luma_dissolve_0.333.png, analysis/DeURRG7vITo/ref_luma_dissolve_0.467.png, analysis/DeURRG7vITo/ref_luma_dissolve_1.733.png, analysis/DeURRG7vITo/ref_luma_dissolve_1.767.png, analysis/DeURRG7vITo/ref_luma_dissolve_1.867.png
// Staged copy: neutral names, fonts from FONTS (lib/effects_lib.jsx).
// Native rebuild of Sapphire S_DissolveLuma: Gradient Wipe with the clip as its own gradient layer, Invert Gradient on.
// Tested in AE 2026: Gradient Wipe (inverted) gives alpha = ((1 + s)(1 - c) - L) / s, the same curve the analysts measured
// for S_DissolveLuma (c = Transition Completion, s = Transition Softness, L = pixel luma), so the look is identical.
function build_luma_dissolve() {
    var T0 = 6;               // frames of white before the reveal starts (reel frame n = our frame T0 + n)
    var DUR = 3.0;
    var BW = 836, BH = 564;   // the 3:2 clip box of the reel
    var CY = 544;

    function f(n) { return (T0 + n) / FPS; }
    // auto-bezier position keys (smooth speed through every key, no stops)
    function smoothX(prop, list, y, dx) {
        for (var i = 0; i < list.length; i++) prop.setValueAtTime(f(list[i][0]), [list[i][1] + dx, y]);
        for (var j = 1; j <= prop.numKeys; j++) { try { prop.setTemporalAutoBezierAtKey(j, true); prop.setTemporalContinuousAtKey(j, true); } catch (e) {} }
    }
    function word(comp, s, font, size, tracking, col) {
        var l = txt(comp, s, font, size, col, ParagraphJustification.LEFT_JUSTIFY, tracking, 0, 0);
        l.name = s;
        return l;
    }
    // lay words left to right, right edge at xr, on a baseline; returns the layers
    function rowRight(comp, words, font, size, tracking, col, xr, base, gap) {
        var ls = [], ws = [], total = 0, i;
        for (i = 0; i < words.length; i++) {
            var l = word(comp, words[i], font, size, tracking, col);
            var r = rect(l);
            ls.push(l); ws.push([r.left, r.width]); total += r.width;
        }
        total += gap * (words.length - 1);
        var x = xr - total;
        for (i = 0; i < ls.length; i++) { P(ls[i]).setValue([x - ws[i][0], base]); x += ws[i][1] + gap; }
        return ls;
    }
    function fadeWord(l, a, b, outA, outB) {
        var o = O(l);
        if (outA !== undefined) kf(o, [[T0 + a, 0], [T0 + b, 100, 33, 80], [T0 + outA, 100], [T0 + outB, 0]]);
        else kf(o, [[T0 + a, 0], [T0 + b, 100, 33, 80]]);
        var g = gaussBlur(l, 0);
        kf(g.property("ADBE Gaussian Blur 2-0001"), [[T0 + a, 8], [T0 + b + 2, 0, 33, 80]]);
    }
    function rectMask(l, x0, y0, x1, y1, feather) {
        var m = l.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
        var s = new Shape(); s.vertices = [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]; s.closed = true;
        m.property("ADBE Mask Shape").setValue(s);
        if (feather) m.property("ADBE Mask Feather").setValue([feather, feather]);
        return m;
    }

    // ---- SOURCE: the clip that dissolves (swap the footage inside to reuse)
    var src = sourceComp("Luma Dissolve - SOURCE A", "field_runner.mov", DUR, { w: BW, h: BH, start: 1.2, crop: [180, 0, 1800, 1080] });
    // The dissolve runs on the clip's own brightness, so its pace depends on the shot. The reel's runner shot is dark
    // (median luma 0.23, darkest 10 % below 0.05). This optional grade pulls the bright stock shot into the same range:
    // shadows crushed to true black (they appear first), mids darkened, the sky pulled down like a grad filter.
    var gr = adjL(src, "GRADE 1 dark punchy (optional)");
    var lv = fx(gr, "ADBE Easy Levels2"); lv.name = "Levels";
    lv = gr.property("ADBE Effect Parade").property("Levels");
    setp(lv, "Input Black", 0.20); setp(lv, "Input White", 0.95); setp(lv, "Gamma", 0.6);
    lumetri(gr, { temp: 12, sat: 110 });
    var gs = adjL(src, "GRADE 2 sky grad (optional)");
    var lv2 = fx(gs, "ADBE Easy Levels2"); lv2.name = "Levels (sky down)";
    lv2 = gs.property("ADBE Effect Parade").property("Levels (sky down)");
    setp(lv2, "Output White", 0.5);
    rectMask(gs, -40, -200, BW + 40, 300, 150);

    // ---- main comp
    var c = effectComp("Luma Dissolve", DUR);
    c.motionBlur = true;
    c.shutterAngle = 270;
    var bg = solidL(c, "BG white", hex("#FFFFFF"));

    var clip = addComp(c, src, "Runner (Gradient Wipe on itself)");
    clip.motionBlur = false;   // layer motion blur would smear the dissolve pattern while the row slides
    fxp(clip, "ADBE Gradient Wipe", [["Transition Softness", 0.1], ["Gradient Placement", 3], ["Invert Gradient", 1]], "Gradient Wipe (native S_DissolveLuma)");
    var gw = clip.property("ADBE Effect Parade").property("Gradient Wipe (native S_DissolveLuma)");
    try { gw.property("Gradient Layer").setValue(clip.index); } catch (eg) { log("  gradient layer: " + eg.toString()); }
    gw = clip.property("ADBE Effect Parade").property("Gradient Wipe (native S_DissolveLuma)");
    var tc = gw.property("Transition Completion");
    // reveal: 100 -> 0 over 30 f, Easy Ease 33/33. Exit: 0 -> 100 over 11 f, out 33 / in 100 (fast start, long tail).
    // Scripting reads this percent as 0-1 (1 = 100 %).
    kf(tc, [[T0 + 0, 1, 33.33, 33.33], [T0 + 30, 0, 33.33, 33.33], [T0 + 49, 0, 33.33, 33.33], [T0 + 60, 1, 100, 33.33]]);

    // ---- "This is called" rides with the clip (right edge 11 px left of the box)
    var cap = rowRight(c, ["This", "is", "called"], FONTS.medium, 60, -45, hex("#0A0A0A"), -11, CY + 22, 13);
    fadeWord(cap[0], 1, 3, 18, 24);
    fadeWord(cap[1], 4, 7, 18, 24);
    fadeWord(cap[2], 8, 11, 18, 24);

    // ---- title, right aligned to x 1612, baselines 540 / 633
    var t1 = rowRight(c, ["The", "Luma"], FONTS.regular, 107, -10, hex("#111111"), 1612, 540, 26);
    var t2 = rowRight(c, ["Dissolve"], FONTS.regular, 107, -10, hex("#111111"), 1614, 633, 0);
    fadeWord(t1[0], 23, 27, 46, 63);
    fadeWord(t1[1], 29, 33, 46, 63);
    fadeWord(t2[0], 35, 39, 46, 63);

    // ---- nulls first (parent while nothing is keyed, then key them)
    var PX = 1500;
    var push = c.layers.addNull(DUR); push.name = "PUSH in";
    P(push).setValue([1060, CY]);
    var row = c.layers.addNull(DUR); row.name = "ROW slide";
    P(row).setValue([PX, CY]);
    row.parent = push;
    P(clip).setValue([PX, CY]);
    clip.parent = row;
    for (var q = 0; q < cap.length; q++) {
        var pv = P(cap[q]).value; P(cap[q]).setValue([pv[0] + PX - BW / 2, pv[1]]);
        cap[q].parent = row; cap[q].motionBlur = true;
    }
    var tl = [t1[0], t1[1], t2[0]];
    for (q = 0; q < tl.length; q++) tl[q].parent = push;
    // ROW slide: an entry that decelerates (clip centre x measured in the reel: f9 1167, f12 1110, f20 915, f30 767, f40 733)
    // ROW is parented to PUSH, so its values are in PUSH's layer space: absolute - PUSH position + PUSH anchor
    var pan = A(push).value;
    smoothX(P(row), [[-5, 1590], [1, 1500], [6, 1250], [13, 1090], [19, 960], [25, 814], [32, 755], [48, 722]], pan[1], pan[0] - 1060);
    // PUSH: slow push-in about (1060, 544) that accelerates into the exit (100 -> 125 % over f40-f60)
    var ps = S(push);
    var pk = [[40, 100], [44, 101], [48, 104], [52, 108.9], [56, 115.8], [60, 124.7]];   // ease-in measured from the reel
    for (q = 0; q < pk.length; q++) ps.setValueAtTime(f(pk[q][0]), [pk[q][1], pk[q][1]]);
    for (q = 1; q <= ps.numKeys; q++) { try { ps.setTemporalAutoBezierAtKey(q, true); } catch (ei) {} }

    note(c, "Luma Dissolve: the clip appears and disappears by its own brightness, darks first in and last out. The Runner layer has Gradient Wipe with Gradient Layer = itself, Stretch Gradient to Fit, Invert Gradient on and Transition Softness 10 %; Transition Completion is keyed 100 to 0 % over 30 frames (Easy Ease) to reveal and 0 to 100 % over 11 frames (out 33 %, in 100 %) to dissolve out. Raise Softness to 30-50 % for a washed, dreamy fade. Swap the shot inside 'Luma Dissolve - SOURCE A' (its grade layers are optional), or put a second clip under the Runner instead of the white solid for a clip-to-clip transition.");
    return c;
}
