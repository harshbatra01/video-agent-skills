// meta key: shake_chroma_impact
// meta title: Shake Chroma Transition
// meta order: 14
// meta refs: analysis/DdoSNUYvtPg/ref_shake_chroma_warp_24.53.png, analysis/DdoSNUYvtPg/ref_shake_chroma_warp_24.67.png, analysis/DdoSNUYvtPg/ref_shake_chroma_warp_24.73.png
// Staged copy: neutral names, fonts from FONTS (lib/effects_lib.jsx).
// Native stand-in for Sapphire S_Shake + S_DistortChroma on an adjustment layer over a cut (cut-4f to cut+8f, peak on the cut).
// S_Shake = Motion Tile with Mirror Edges (Wrap Reflect) + a Transform effect wiggled at 8.8 Hz with its own 360 shutter.
// S_DistortChroma (Lens: Source, Warp Red 0.5 / Blue 1.0) = a lens map made from the image's own edges (blur + Emboss,
// horizontal slope in red, vertical slope in green) driving Displacement Map on three single-channel copies added back up.
function build_shake_chroma_impact() {
    var CUT = 30;   // the cut frame of the edit underneath (frame M of the One-Frame Glitch Transition)

    function t(n) { return n / FPS; }
    function findComp(name) {
        for (var i = 1; i <= app.project.numItems; i++) { var it = app.project.item(i); if (it instanceof CompItem && it.name == name) return it; }
        return null;
    }
    function eff(l, nm) { return l.property("ADBE Effect Parade").property(nm); }
    function prm(e, nm) {
        for (var i = 1; i <= e.numProperties; i++) { if (e.property(i).name == nm || e.property(i).matchName == nm) return e.property(i); }
        return findProp(e, nm);
    }
    function setPrm(e, nm, v) { var p = prm(e, nm); if (!p) { log("  shake param missing: " + nm); return null; } try { p.setValue(v); } catch (er) { log("  shake param " + nm + ": " + er.toString()); } return p; }
    var DUMPED = {};
    function dump(e) {
        if (DUMPED[e.matchName]) return; DUMPED[e.matchName] = 1;
        var s = [];
        for (var i = 1; i <= e.numProperties; i++) s.push(e.property(i).name + "=" + e.property(i).matchName);
        log("  param list " + e.matchName + ": " + s.join(" | "));
    }
    // the hit: 0 at cut-4 (ease out), peak on the cut (sharp, exponential rise, fast drop), 0 at cut+8 (90 % ease in)
    // speeds fitted to the reel (Shake Amp 4.0 at the cut reads 1.24 two frames later, as in the reel's Effect Controls)
    function spike(prop, peak) {
        prop.setValueAtTime(t(CUT - 4), 0); prop.setValueAtTime(t(CUT), peak); prop.setValueAtTime(t(CUT + 8), 0);
        try {
            prop.setTemporalContinuousAtKey(2, false);
            prop.setTemporalEaseAtKey(1, [new KeyframeEase(0, 33)], [new KeyframeEase(0, 35)]);
            prop.setTemporalEaseAtKey(2, [new KeyframeEase(35.6 * peak, 10)], [new KeyframeEase(-11.25 * peak, 10)]);
            prop.setTemporalEaseAtKey(3, [new KeyframeEase(0, 90)], [new KeyframeEase(0, 33)]);
        } catch (e) { log("  shake param spike: " + e.toString()); }
    }

    // ---- the edit: the One-Frame Glitch Transition when it is in the project, else a plain hard cut of two stock shots
    var edit = findComp("One-Frame Glitch Transition");
    var DUR = edit ? edit.duration : 3.5;
    if (!edit) {
        var sa = sourceComp("Shake Chroma Transition - SOURCE A", "rain_street.mov", DUR, { start: 1.0 });
        var sb = sourceComp("Shake Chroma Transition - SOURCE B", "clouds_a.mov", DUR, { start: 1.0 });
        edit = effectComp("Shake Chroma Transition - edit (hard cut)", DUR);
        var la = addComp(edit, sa, "A"); la.outPoint = t(CUT);
        var lb = addComp(edit, sb, "B"); lb.inPoint = t(CUT);
    }

    // =====================================================================================================
    // 1. SHAKE (S_Shake): the edit + ADJ_SHAKE adjustment layer from cut-4 to cut+8
    var pre = effectComp("Shake Chroma Transition - shake", DUR);
    pre.motionBlur = true;
    addComp(pre, edit, "EDIT (your cut)");
    var adj = adjL(pre, "ADJ_SHAKE (S_Shake)");
    adj.inPoint = t(CUT - 4); adj.outPoint = t(CUT + 9);
    adj.motionBlur = true;
    slider(adj, "Shake Amp", 0);
    spike(eff(adj, "Shake Amp").property(1), 4.0);
    slider(adj, "Shake Seed", 4);
    var mt = fxp(adj, "ADBE Tile", null, "Motion Tile (Wrap X/Y Reflect)");
    dump(mt);
    setPrm(mt, "Output Width", 300); setPrm(mt, "Output Height", 300); setPrm(mt, "Mirror Edges", 1);
    var tf = fxp(adj, "ADBE Geometry2", null, "Transform (shake)");
    dump(tf);
    tf = eff(adj, "Transform (shake)");
    setPrm(tf, "ADBE Geometry2-0011", 1);     // Uniform Scale
    setPrm(tf, "ADBE Geometry2-0009", 0);     // Use Composition's Shutter Angle OFF
    setPrm(tf, "ADBE Geometry2-0010", 360);   // own Shutter Angle 360
    var amp = 'var a = effect("Shake Amp")("Slider"); var sd = Math.round(effect("Shake Seed")("Slider")); ';
    prm(tf, "ADBE Geometry2-0002").expression = amp + 'seedRandom(sd, true); wiggle(8.8, a * 70, 2, 0.5);';
    prm(tf, "ADBE Geometry2-0007").expression = amp + 'seedRandom(sd + 7, true); wiggle(8.8, a * 0.75, 1);';
    prm(tf, "ADBE Geometry2-0003").expression = amp + 'seedRandom(sd + 13, true); wiggle(8.8, a * 2.5, 1);';

    // =====================================================================================================
    // 2. LENS MAP (Lens: Source): the shaken picture's own edges as a slope map. Flat areas = 50 % grey = no push.
    var lmc = effectComp("Shake Chroma Transition - lens map", DUR);
    solidL(lmc, "BG black", [0, 0, 0]);
    var gl = [["GRAD X (slope across, in red)", 90, ["Take Green From", "Take Blue From"]], ["GRAD Y (slope down, in green)", 0, ["Take Red From", "Take Blue From"]]];
    for (var g = 0; g < gl.length; g++) {
        var gL = addComp(lmc, pre, gl[g][0]);
        boxBlur(gL, 28, 1);
        var em = fxp(gL, "ADBE Emboss", null, "Emboss");
        dump(em);
        em = eff(gL, "Emboss");
        setPrm(em, "Direction", gl[g][1]); setPrm(em, "Relief", 8); setPrm(em, "Contrast", 200);
        var sc = fxp(gL, "ADBE Shift Channels", null, "Shift Channels");
        dump(sc);
        sc = eff(gL, "Shift Channels");
        setPrm(sc, gl[g][2][0], 10); setPrm(sc, gl[g][2][1], 10);   // 10 = Full Off
        if (g > 0) gL.blendingMode = BlendingMode.ADD;
    }

    // =====================================================================================================
    // 3. MAIN (S_DistortChroma): three single-channel copies, each pushed along the lens map by its own weight
    var c = effectComp("Shake Chroma Transition", DUR);
    var ctl = c.layers.addNull(DUR); ctl.name = "CTRL"; P(ctl).setValue([80, 80]);
    slider(ctl, "Chroma Amt", 0);
    spike(eff(ctl, "Chroma Amt").property(1), 1.0);
    slider(ctl, "Warp px", 200);
    solidL(c, "BG black", [0, 0, 0]).moveToEnd();
    var map = addComp(c, lmc, "LENS MAP (hidden)");
    var chans = [["SC_B (Warp Blue 1.0)", 1.0, ["Take Red From", "Take Green From"]], ["SC_G (Warp Green 0.75)", 0.75, ["Take Red From", "Take Blue From"]], ["SC_R (Warp Red 0.5)", 0.5, ["Take Green From", "Take Blue From"]]];
    var cl = [];
    for (var i = 0; i < chans.length; i++) {
        var L = addComp(c, pre, chans[i][0]);
        var dm = fxp(L, "ADBE Displacement Map", null, "Displacement Map");
        dump(dm);
        cl.push(L);
        if (i > 0) L.blendingMode = BlendingMode.ADD;
    }
    map.moveBefore(cl[2]);
    ctl.moveToBeginning();
    map.enabled = false;
    for (i = 0; i < chans.length; i++) {
        var dmi = eff(cl[i], "Displacement Map");
        setPrm(dmi, "Displacement Map Layer", map.index);
        setPrm(dmi, "Use For Horizontal Displacement", 1);   // Red = slope across
        setPrm(dmi, "Use For Vertical Displacement", 2);     // Green = slope down
        setPrm(dmi, "Displacement Map Behavior", 2);         // Stretch Map to Fit
        setPrm(dmi, "Edge Behavior", 1);             // Wrap Pixels Around
        var ex = 'thisComp.layer("CTRL").effect("Chroma Amt")("Slider") * thisComp.layer("CTRL").effect("Warp px")("Slider") * ' + chans[i][1] + ';';
        prm(dmi, "Max Horizontal Displacement").expression = ex;
        prm(dmi, "Max Vertical Displacement").expression = ex;
        var sci = fxp(cl[i], "ADBE Shift Channels", null, "Shift Channels (keep " + chans[i][0].substr(3, 1) + ")");
        setPrm(sci, chans[i][2][0], 10); setPrm(sci, chans[i][2][1], 10);   // 10 = Full Off
    }

    try { c.markerProperty.setValueAtTime(t(CUT), new MarkerValue("cut (peak)")); } catch (em2) {}
    note(c, "A 12-frame hit on the cut that stands in for Sapphire S_Shake and S_DistortChroma. In the 'shake' precomp, ADJ_SHAKE spans cut-4 to cut+8 with Motion Tile (300 %, Mirror Edges, so the edges reflect in) and a Transform effect wiggled at 8.8 Hz with its own 360 shutter, driven by the 'Shake Amp' slider (0, 4 on the cut, 0). Here SC_R, SC_G and SC_B keep one colour channel each and Displacement Map pushes them along LENS MAP (the picture's own blurred edges run through Emboss, slope across in red and down in green) by 0.5, 0.75 and 1.0 times CTRL 'Chroma Amt' x 'Warp px', then they add back to the clean image, so every edge bends and splits into colour fringes. Move the hit by retiming the Shake Amp and Chroma Amt keys, change Shake Seed for a different shake, and put your own cut in EDIT.");
    return c;
}
