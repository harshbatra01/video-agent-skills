// meta key: smooth_text_transition
// meta title: Smooth Text Transition
// meta order: 4
// meta refs: analysis/DaklnysP87i/ref_smooth_text_transition_1.13.png, analysis/DaklnysP87i/ref_smooth_text_transition_1.87.png, analysis/DaklnysP87i/ref_smooth_text_transition_2.13.png, analysis/DaklnysP87i/ref_smooth_text_transition_2.93.png
// Staged copy: neutral names, fonts from FONTS (lib/effects_lib.jsx). Source: a friend's Mac effects library (Oct 2026).
// DaklnysP87i: two text layers parented to Null 10, which is parented to Null 11. Null 10 brings the first line in
// with a fast-start / long-settle ease; Null 11 (keyed so it overlaps Null 10's tail) pushes the whole group left on a
// skewed bell so the second word lands in the centre. Both texts use the word-by-word blur/fade/colour reveal preset.
// Our frame = tutorial comp frame + OFF.
function build_smooth_text_transition() {
    var OFF = 6;
    var DUR = 3.5;
    var TITLE = "Smooth Text Transition";
    var FONT = FONTS.medium, SIZE = 260, INK = hex("#EDF2FB");

    function f(n) { return (n + OFF) / FPS; }
    function easeAt(prop, idx, inS, inI, outS, outI) {
        var n = 1;
        if (!prop.isSpatial && (prop.propertyValueType == PropertyValueType.TwoD || prop.propertyValueType == PropertyValueType.ThreeD)) n = prop.keyValue(idx).length;
        var a = [], b = [];
        for (var i = 0; i < n; i++) { a.push(new KeyframeEase(inS, inI)); b.push(new KeyframeEase(outS, outI)); }
        try { prop.setTemporalEaseAtKey(idx, a, b); } catch (e) { log("  ease " + prop.name + ": " + e.toString()); }
    }
    // kfe(prop, [[frame, value, inSpeed, inInf, outSpeed, outInf], ...]), frames in tutorial time (OFF added here)
    function kfe(prop, list) {
        for (var i = 0; i < list.length; i++) prop.setValueAtTime(f(list[i][0]), list[i][1]);
        for (var j = 0; j < list.length; j++) { var k = list[j]; easeAt(prop, prop.nearestKeyIndex(f(k[0])), k[2], k[3], k[4], k[5]); }
    }
    function anims(l) { return l.property("ADBE Text Properties").property("ADBE Text Animators"); }
    // the text preset: Animator 1 (Opacity 0, Blur 12, Fill Color steel blue) + Range Selector 1 based on words,
    // Ramp Up, Offset -100 % at the layer in-point -> +100 % 20 frames later (ease-out)
    function wordPreset(l, k0, k1, v0) {
        anims(l).addProperty("ADBE Text Animator");
        var an = anims(l).property(anims(l).numProperties); an.name = "Animator 1";
        var ap = anims(l).property("Animator 1").property("ADBE Text Animator Properties");
        ap.addProperty("ADBE Text Opacity");
        anims(l).property("Animator 1").property("ADBE Text Animator Properties").addProperty("ADBE Text Blur");
        anims(l).property("Animator 1").property("ADBE Text Animator Properties").addProperty("ADBE Text Fill Color");
        ap = anims(l).property("Animator 1").property("ADBE Text Animator Properties");
        ap.property("ADBE Text Opacity").setValue(0);
        ap.property("ADBE Text Blur").setValue([12, 12]);
        ap.property("ADBE Text Fill Color").setValue(hex("#3C7FB0"));
        anims(l).property("Animator 1").property("ADBE Text Selectors").addProperty("ADBE Text Selector");
        var sels = anims(l).property("Animator 1").property("ADBE Text Selectors");
        var sel = sels.property(sels.numProperties); sel.name = "Range Selector 1";
        var opts = [["ADBE Text Range Units", 1], ["ADBE Text Range Type2", 3], ["ADBE Text Selector Mode", 1], ["ADBE Text Selector Max Amount", 100],
                    ["ADBE Text Range Shape", 2], ["ADBE Text Percent Start", 0], ["ADBE Text Percent End", 60], ["ADBE Text Levels Max Ease", 0], ["ADBE Text Levels Min Ease", 0]];
        for (var i = 0; i < opts.length; i++) {
            var p = findProp(sel, opts[i][0]);
            if (!p) { log("  preset no " + opts[i][0]); continue; }
            try { p.setValue(opts[i][1]); } catch (e) { log("  preset " + opts[i][0] + ": " + e.toString()); }
        }
        sels = anims(l).property("Animator 1").property("ADBE Text Selectors");
        var off = findProp(sels.property(sels.numProperties), "ADBE Text Percent Offset");
        // Offset v0 at frame k0 -> +100 % at k1, ease-out (fast start, gentle end)
        off.setValueAtTime(f(k0), v0); off.setValueAtTime(f(k1), 100);
        easeAt(off, 1, 0, 10, k1 - k0 > 15 ? 300 : 450, 10); easeAt(off, 2, 0, 20, 0, 20);
    }
    function textL(comp, name, s) {
        var l = txt(comp, s, FONT, SIZE, INK, ParagraphJustification.CENTER_JUSTIFY, -20, 960, 540);
        l.name = name;
        centreAnchor(l);
        return l;
    }

    var c = effectComp(TITLE, DUR);
    c.motionBlur = true; c.shutterAngle = 360; c.shutterPhase = -180;
    try { c.motionBlurSamplesPerFrame = 16; } catch (e0) {}
    var bg = solidL(c, "Black Solid", [0, 0, 0]);

    // ---- text 1: in 0, out 35 f (the tutorial extended it 5 f for the fade)
    var t1 = textL(c, "Say hello to", "Say hello to");
    P(t1).setValue([960, 540]);
    t1.inPoint = f(0); t1.outPoint = f(35);
    wordPreset(t1, 0, 24, -40);
    kfe(O(t1), [[26, 100, 0, 33.3, 0, 33.3], [30, 0, 0, 33.3, 0, 33.3]]);
    t1.motionBlur = true;

    // ---- text 2: the duplicate, moved later (starts at 1:00) and 653 px to the right; hero gradient + glow
    var t2 = textL(c, "TITLE", "TITLE");
    P(t2).setValue([1613, 540]);
    t2.inPoint = f(30); t2.outPoint = DUR;
    // a single word reveals over the first few frames of the shorter sweep
    wordPreset(t2, 30, 40, -10);
    // Gradient Ramp (radial): cyan just left of the word's middle, deep blue at the ends; points follow the text box
    var gr = fxp(t2, "ADBE Ramp", [["ADBE Ramp-0002", hex("#1BEEF3")], ["ADBE Ramp-0004", hex("#062C9E")], ["ADBE Ramp-0005", 2], ["ADBE Ramp-0007", 0]], "Gradient Ramp");
    gr = t2.property("ADBE Effect Parade").property("Gradient Ramp");
    // effect points on a text layer sit in its comp-sized source, so layer space + half the layer size
    gr.property("ADBE Ramp-0001").expression = "var r=thisLayer.sourceRectAtTime(time,false); [r.left+r.width*0.45+thisLayer.width/2, r.top+r.height/2+thisLayer.height/2];";
    gr = t2.property("ADBE Effect Parade").property("Gradient Ramp");
    gr.property("ADBE Ramp-0003").expression = "var r=thisLayer.sourceRectAtTime(time,false); [r.left+r.width*0.87+thisLayer.width/2, r.top+r.height/2+thisLayer.height/2];";
    // soft cyan halo with native Glow (Deep Glow 2 is installed but unlicensed here)
    // only the bright cyan middle passes the threshold, so the halo sits around the centre letters
    fxp(t2, "ADBE Glo2", [["Glow Threshold", 75], ["Glow Radius", 150], ["Glow Intensity", 0.5]], "Glow (cyan halo)");
    t2.motionBlur = true;

    // ---- Null 10: both texts parented to it. Position 0 f moved 243 px right -> 1:00 home, fast start + long settle
    var n10 = c.layers.addNull(DUR); n10.name = "Null 10";
    A(n10).setValue([0, 0]); P(n10).setValue([960, 540]);
    // ---- Null 11: Null 10 parented to it; key at ~0:18 (overlapping Null 10's tail) -> 1:29 at 307,540
    var n11 = c.layers.addNull(DUR); n11.name = "Null 11";
    A(n11).setValue([0, 0]); P(n11).setValue([960, 540]);
    n10.parent = n11;
    P(n10).setValue([0, 0]);
    t1.parent = n10; t2.parent = n10;
    P(t1).setValue([0, 0]); P(t2).setValue([653, 0]);
    kfe(P(n10), [[0, [243, 0], 0, 6, 3250, 6], [30, [0, 0], 0, 60, 0, 60]]);
    kfe(P(n11), [[18, [960, 540], 0, 32.5, 0, 32.5], [59, [307, 540], 0, 95, 0, 95]]);
    n11.moveToBeginning();
    n10.moveAfter(n11);

    note(c, "Smooth text transition. Both text layers are parented to Null 10, and Null 10 is parented to Null 11. Null 10's Position keys (243 px right at 0 f, home at 1:00, fast start and long settle) bring the first line in; Null 11's keys (0:18 to 1:29, ending at 307,540 so the second word lands in the centre) push the whole group left on a slow-fast-slow curve that overlaps the end of Null 10's move. The first line fades out over the 4 frames before 1:00 and the second text starts at 1:00; both reveal word by word through Animator 1 (Range Selector 1 based on words, Ramp Up, End 60 %, Offset keyed up to 100 %). The second word gets a radial Gradient Ramp (cyan middle, deep blue ends) and a Glow; change the words in the two text layers and the travel by moving the null keys.");
    return c;
}
