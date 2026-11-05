// Immufix "1 star reviews": five outline stars draw on, only the first lights up gold.
// Builds the comp, saves the project, renders ProRes 4444 with alpha + an H.264 preview, then quits.
// Run: AfterFX.exe -r stars.jsx
app.exitAfterLaunchAndEval = false;
app.beginSuppressDialogs();
var OUT = "C:/VISION/IMMUFIX/repair/ENCODED RUSHES/Motion graphics/";
var BG = "C:/Users/Kanishk/AppData/Local/Temp/claude/C--VISION-IMMUFIX-repair-ENCODED-RUSHES/b6d96195-2992-4138-a685-9dc3b5c5abcd/scratchpad/ae/bg_1star.png";
var W = 1080, H = 400, FPS = 60, DUR = 3.6;
var CY = 200, R = 52, RI = 24.4, GAP = 128;
var GOLD = [0.851, 0.710, 0.400], GOLD_LIGHT = [1.0, 0.929, 0.710], GOLD_DARK = [0.690, 0.494, 0.180];

function hexEase(prop, idx, inInf, outInf) {
    var n = 1;
    if (!prop.isSpatial && (prop.propertyValueType == PropertyValueType.TwoD || prop.propertyValueType == PropertyValueType.ThreeD)) n = prop.keyValue(idx).length;
    var a = [], b = [];
    for (var i = 0; i < n; i++) { a.push(new KeyframeEase(0, inInf)); b.push(new KeyframeEase(0, outInf)); }
    prop.setTemporalEaseAtKey(idx, a, b);
}
// keys: [[t, v, inInfluence, outInfluence], ...]
function keys(prop, list) {
    for (var i = 0; i < list.length; i++) prop.setValueAtTime(list[i][0], list[i][1]);
    for (var j = 0; j < list.length; j++) {
        var k = prop.nearestKeyIndex(list[j][0]);
        hexEase(prop, k, list[j][2] || 33.3, list[j][3] || 33.3);
    }
}
function findIn(layer, matchName) {
    var gc = layer.property("ADBE Root Vectors Group").property(1).property("ADBE Vectors Group");
    for (var i = 1; i <= gc.numProperties; i++) if (gc.property(i).matchName == matchName) return gc.property(i);
    return null;
}
function starShape(comp, name, x, opts) {
    var lay = comp.layers.addShape();
    lay.name = name;
    var gc = lay.property("ADBE Root Vectors Group").addProperty("ADBE Vector Group").property("ADBE Vectors Group");
    var st = gc.addProperty("ADBE Vector Shape - Star");
    st.property("ADBE Vector Star Type").setValue(1);
    st.property("ADBE Vector Star Points").setValue(5);
    st.property("ADBE Vector Star Outer Radius").setValue(opts.r || R);
    st.property("ADBE Vector Star Inner Radius").setValue((opts.r || R) * RI / R);
    gc.addProperty("ADBE Vector Filter - RC").property("ADBE Vector RoundCorner Radius").setValue(7);
    var trim = null;
    if (opts.trim) trim = gc.addProperty("ADBE Vector Filter - Trim");
    if (opts.stroke) {
        var s = gc.addProperty("ADBE Vector Graphic - Stroke");
        s.property("ADBE Vector Stroke Color").setValue(opts.stroke);
        s.property("ADBE Vector Stroke Width").setValue(opts.width || 4);
        s.property("ADBE Vector Stroke Line Join").setValue(2);
    }
    if (opts.fill) {
        var f = gc.addProperty("ADBE Vector Graphic - Fill");
        f.property("ADBE Vector Fill Color").setValue(opts.fill);
    }
    lay.property("ADBE Transform Group").property("ADBE Position").setValue([x, CY]);
    return {layer: lay, trim: (opts.trim ? findIn(lay, "ADBE Vector Filter - Trim") : null)};
}

try {
    var proj = app.newProject();
    var comp = proj.items.addComp("Stars 1 of 5", W, H, 1, DUR, FPS);
    comp.motionBlur = true;
    comp.shutterAngle = 180;
    var X = [], i;
    for (i = 0; i < 5; i++) X.push(W / 2 + (i - 2) * GAP);
    var T_DRAW = 0.05, STAGGER = 0.06, T_LIGHT = 0.46, T_OUT = 3.0;

    // burst ring behind the gold star
    var ring = comp.layers.addShape();
    ring.name = "Burst ring";
    var rg = ring.property("ADBE Root Vectors Group").addProperty("ADBE Vector Group").property("ADBE Vectors Group");
    var el = rg.addProperty("ADBE Vector Shape - Ellipse");
    var rs = rg.addProperty("ADBE Vector Graphic - Stroke");
    rs.property("ADBE Vector Stroke Color").setValue(GOLD_LIGHT);
    rs.property("ADBE Vector Stroke Width").setValue(3);
    ring.property("ADBE Transform Group").property("ADBE Position").setValue([X[0], CY]);
    keys(findIn(ring, "ADBE Vector Shape - Ellipse").property("ADBE Vector Ellipse Size"), [[T_LIGHT, [70, 70], 33, 10], [T_LIGHT + 0.42, [210, 210], 85, 33]]);
    keys(ring.property("ADBE Transform Group").property("ADBE Opacity"), [[T_LIGHT - 0.01, 0], [T_LIGHT, 85, 33, 10], [T_LIGHT + 0.42, 0, 70, 33]]);

    // glow behind the gold star
    var glow = starShape(comp, "Gold glow", X[0], {fill: GOLD});
    glow.layer.blendingMode = BlendingMode.ADD;
    var gb = glow.layer.property("ADBE Effect Parade").addProperty("ADBE Gaussian Blur 2");
    gb.property("ADBE Gaussian Blur 2-0001").setValue(34);
    gb.property("ADBE Gaussian Blur 2-0003").setValue(0);   // repeat edge pixels OFF so the glow is not clipped to a box
    keys(glow.layer.property("ADBE Transform Group").property("ADBE Opacity"), [[T_LIGHT, 0], [T_LIGHT + 0.12, 95, 33, 15], [T_LIGHT + 0.6, 62, 60, 33],
        [1.6, 75], [2.2, 60], [2.8, 72], [T_OUT + 0.1, 0, 60, 33]]);
    keys(glow.layer.property("ADBE Transform Group").property("ADBE Scale"), [[T_LIGHT, [40, 40, 100], 33, 12], [T_LIGHT + 0.2, [135, 135, 100], 88, 33], [T_LIGHT + 0.5, [120, 120, 100]]]);

    // gold fill: gradient solid seen through a star matte that pops 0 -> 118 -> 100
    var grad = comp.layers.addSolid([1, 1, 1], "Gold gradient", W, H, 1, DUR);
    var ramp = grad.property("ADBE Effect Parade").addProperty("ADBE Ramp");
    ramp.property("ADBE Ramp-0001").setValue([X[0] - 20, CY - R]);
    ramp.property("ADBE Ramp-0002").setValue(GOLD_LIGHT);
    ramp.property("ADBE Ramp-0003").setValue([X[0] + 20, CY + R]);
    ramp.property("ADBE Ramp-0004").setValue(GOLD_DARK);
    var sweep = grad.property("ADBE Effect Parade").addProperty("CC Light Sweep");
    try {
        sweep.property("Direction").setValue(-28);
        sweep.property("Width").setValue(26);
        sweep.property("Sweep Intensity").setValue(90);
        sweep.property("Edge Intensity").setValue(0);
        keys(sweep.property("Center"), [[T_LIGHT + 0.10, [X[0] - 110, CY]], [T_LIGHT + 0.55, [X[0] + 110, CY], 60, 33], [2.15, [X[0] - 110, CY]], [2.55, [X[0] + 110, CY], 60, 33]]);
    } catch (e1) { }
    var matte = starShape(comp, "Gold matte", X[0], {fill: [1, 1, 1]});
    keys(matte.layer.property("ADBE Transform Group").property("ADBE Scale"), [[T_LIGHT, [0, 0, 100], 33, 10], [T_LIGHT + 0.17, [118, 118, 100], 85, 30],
        [T_LIGHT + 0.32, [100, 100, 100], 70, 33], [T_OUT, [100, 100, 100], 33, 75], [T_OUT + 0.22, [0, 0, 100], 85, 33]]);
    matte.layer.moveBefore(grad);
    try { grad.setTrackMatte(matte.layer, TrackMatteType.ALPHA); } catch (e2) { grad.trackMatteType = TrackMatteType.ALPHA; }

    // stars 2-5: gold flicker that fails, then they dim and sag a little
    for (i = 1; i < 5; i++) {
        var fl = starShape(comp, "Flicker " + (i + 1), X[i], {fill: GOLD});
        var t0 = T_LIGHT + 0.18 + (i - 1) * 0.08;
        keys(fl.layer.property("ADBE Transform Group").property("ADBE Opacity"), [[t0, 0], [t0 + 0.04, 42], [t0 + 0.09, 0], [t0 + 0.13, 22], [t0 + 0.18, 0]]);
    }

    // outlines draw on (Trim Paths), left to right; the lit one fades as its fill pops
    for (i = 0; i < 5; i++) {
        var o = starShape(comp, "Outline " + (i + 1), X[i], {stroke: [1, 1, 1], width: 4, trim: true});
        var ta = T_DRAW + i * STAGGER;
        keys(findIn(o.layer, "ADBE Vector Filter - Trim").property("ADBE Vector Trim End"), [[ta, 0, 33, 12], [ta + 0.34, 100, 88, 33]]);
        findIn(o.layer, "ADBE Vector Filter - Trim").property("ADBE Vector Trim Offset").setValue(-90);
        var tr = o.layer.property("ADBE Transform Group");
        keys(tr.property("ADBE Scale"), [[ta, [84, 84, 100], 33, 12], [ta + 0.34, [100, 100, 100], 88, 33]]);
        var ds = o.layer.property("ADBE Effect Parade").addProperty("ADBE Drop Shadow");
        ds.property("ADBE Drop Shadow-0002").setValue(0.55 * 255);   // opacity (0-255)
        ds.property("ADBE Drop Shadow-0004").setValue(2);            // distance
        ds.property("ADBE Drop Shadow-0005").setValue(10);           // softness
        if (i == 0) {
            keys(tr.property("ADBE Opacity"), [[ta, 0], [ta + 0.08, 90], [T_LIGHT + 0.05, 90], [T_LIGHT + 0.2, 0]]);
        } else {
            var td = T_LIGHT + 0.36 + (i - 1) * 0.08;
            keys(tr.property("ADBE Opacity"), [[ta, 0], [ta + 0.08, 90], [td, 90], [td + 0.25, 52, 60, 33], [T_OUT + 0.05 + (4 - i) * 0.04, 52], [T_OUT + 0.25 + (4 - i) * 0.04, 0]]);
            keys(tr.property("ADBE Position"), [[td, [X[i], CY]], [td + 0.3, [X[i], CY + 5], 70, 33]]);
        }
        o.layer.motionBlur = true;
    }
    matte.layer.motionBlur = true; glow.layer.motionBlur = true;

    comp.markerProperty.setValueAtTime(T_LIGHT, new MarkerValue("SFX: bright ding + sparkle"));
    comp.markerProperty.setValueAtTime(T_LIGHT + 0.18, new MarkerValue("SFX: 4 dull ticks (failed flickers)"));
    comp.markerProperty.setValueAtTime(T_OUT, new MarkerValue("SFX: soft whoosh out"));

    // preview comp over the real ad frame
    var prev = proj.items.addComp("Preview over ad", 1080, 1920, 1, DUR, FPS);
    var bg = proj.importFile(new ImportOptions(new File(BG)));
    prev.layers.add(bg);
    var sl = prev.layers.add(comp);
    sl.property("ADBE Transform Group").property("ADBE Position").setValue([540, 1150]);

    proj.save(new File(OUT + "stars_1of5_v2.aep"));
    var rq1 = proj.renderQueue.items.add(comp);
    rq1.outputModule(1).applyTemplate("High Quality with Alpha");
    rq1.outputModule(1).file = new File(OUT + "stars_1of5_v2_alpha");
    var rq2 = proj.renderQueue.items.add(prev);
    rq2.outputModule(1).applyTemplate("H.264 - Match Render Settings - 15 Mbps");
    rq2.outputModule(1).file = new File(OUT + "stars_1of5_v2_preview");
    proj.renderQueue.render();
    proj.save();
} catch (err) {
    try { app.project.items.addComp("ERROR " + err.toString().substr(0, 180) + " line " + err.line, 4, 4, 1, 1, 1); app.project.save(new File(OUT + "stars_1of5_v2_ERROR.aep")); } catch (e3) { }
}
app.endSuppressDialogs(false);
