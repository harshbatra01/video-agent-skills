// meta key: whip_pan_wipe
// meta title: Whip Pan Transition
// meta order: 10
// meta refs: analysis/Dd9E5Q9AtyT/ref_whip_pan_wipe_0.87.png, analysis/Dd9E5Q9AtyT/ref_whip_pan_wipe_0.97.png, analysis/Dd9E5Q9AtyT/ref_whip_pan_wipe_1.10.png, analysis/Dd9E5Q9AtyT/ref_whip_pan_wipe_1.27.png
// Staged copy: neutral names, fonts from FONTS (lib/effects_lib.jsx).
// A camera whip faked at every hard cut, always travelling left to right. Each shot: Motion Tile (mirror edges, so the
// slide never shows an edge) > Transform (own 360 degree shutter, slides the frame) > Directional Blur 90 degrees.
// Timing measured on the reel's After panel: 1 partial-blur frame, about 10 frames of full horizontal smear centred on the
// cut, then the incoming shot lands sharp in one frame. A 2-frame dissolve inside the smear swaps the shots.
function build_whip_pan_wipe() {
    var MAIN = "Whip Pan Transition";
    var DUR = 4.0;
    var CUTS = [45, 65, 90];   // cut frames (reel: 33, 53, 78 in its own timeline); the incoming shot is 50 % on top here
    var OUT_TRAVEL = 1900;     // px the outgoing frame slides right over its 8 whip frames (ease-in, fastest on the cut)
    var IN_TRAVEL = 1700;      // px the incoming frame still has to travel when it appears (ease-out into the landing)
    var TILT = 30;             // px of vertical drift during the whip (bands of the smear move, like a hand-held whip)
    var PEAK = 1000;           // Directional Blur Blur Length on the smear frames

    function t(n) { return n / FPS; }
    function byName(eff, nm) {
        for (var i = 1; i <= eff.numProperties; i++) { var p = eff.property(i); if (p.name == nm) return p; }
        return findProp(eff, nm);
    }
    function useCompShutter(eff) {
        for (var i = 1; i <= eff.numProperties; i++) { var p = eff.property(i); if (p.name.substr(0, 7) == "Use Com") return p; }
        return null;
    }
    function setLinear(prop, frames) {
        for (var k = 1; k <= prop.numKeys; k++) {
            var kt = Math.round(prop.keyTime(k) * FPS);
            for (var q = 0; q < frames.length; q++) if (kt == frames[q]) prop.setInterpolationTypeAtKey(k, KeyframeInterpolationType.LINEAR, KeyframeInterpolationType.LINEAR);
        }
    }

    // one shot with the whip stack. cin / cout = the cuts it enters / leaves at (null = none)
    function shot(c, src, name, cin, cout) {
        var L = addComp(c, src, name);
        L.motionBlur = true;
        L.inPoint = cin === null ? 0 : t(cin - 1);
        L.outPoint = cout === null ? DUR : t(cout + 1);
        fxp(L, "ADBE Tile", [["Output Width", 300], ["Output Height", 130], ["Mirror Edges", 1]], "Motion Tile");
        var tr2 = fxp(L, "ADBE Geometry2", null, "Transform");
        var u = useCompShutter(tr2); if (u) u.setValue(0); else log("  whip param: no Use Composition's Shutter Angle");
        var sa = byName(tr2, "Shutter Angle"); if (sa) sa.setValue(360); else log("  whip param: no Shutter Angle");
        fxp(L, "ADBE Motion Blur", [["Direction", 90], ["Blur Length", 0]], "Directional Blur");
        var ep = L.property("ADBE Effect Parade");
        var pos = byName(ep.property("Transform"), "Position");
        var bl = ep.property("Directional Blur").property("Blur Length");
        var pk = [], bk = [], lin = [];
        if (cin !== null) {
            // incoming: appears mid-smear (still travelling right), lands sharp at cin + 5
            pk.push([cin - 1, [960 - IN_TRAVEL, 540 - TILT]]); pk.push([cin + 5, [960, 540], 85, 33]); lin.push(cin - 1);
            bk.push([cin - 1, PEAK]); bk.push([cin + 4, PEAK]); bk.push([cin + 5, 0]);
            var o = O(L);
            kf(o, [[cin - 1, 0], [cin + 1, 100]]); linearKeys(o);
        }
        if (cout !== null) {
            // outgoing: one partial frame (cout - 6), full smear from cout - 5, accelerating right the whole time
            pk.push([cout - 7, [960, 540], 33, 90]); pk.push([cout + 1, [960 + OUT_TRAVEL, 540 + TILT]]); lin.push(cout + 1);
            bk.push([cout - 7, 0]); bk.push([cout - 6, 200]); bk.push([cout - 5, PEAK]); bk.push([cout + 1, PEAK]);
        }
        kf(pos, pk);
        setLinear(pos, lin);
        kf(bl, bk); linearKeys(bl);
        // CONTROLS scale the keyed values without touching the keys
        bl.expression = 'value * thisComp.layer("CONTROLS").effect("Smear Amount %")("Slider") / 100;';
        pos.expression = 'var k = thisComp.layer("CONTROLS").effect("Whip Distance %")("Slider") / 100; var c0 = [960, 540]; c0 + (value - c0) * k;';
        return L;
    }
    function sfx(c, file, name, peakT, peakInFile, db) {
        var a = c.layers.add(stock(file));
        a.name = name;
        a.startTime = peakT - peakInFile;
        try { a.property("ADBE Audio Group").property("ADBE Audio Levels").setValue([db, db]); } catch (e) { log("  whip param: audio level " + e.toString()); }
        return a;
    }

    // sources: a road / car sequence like the reel (subject front, driver POV, action on a ramp, road ahead)
    var srcA = sourceComp(MAIN + " - SOURCE A", "jogger.mov", DUR, { start: 1.0 });
    var srcB = sourceComp(MAIN + " - SOURCE B", "taxi_interior.mov", DUR, { start: 1.5 });
    var srcC = sourceComp(MAIN + " - SOURCE C", "skater.mov", DUR, { start: 0.1 });
    var srcD = sourceComp(MAIN + " - SOURCE D", "rain_street.mov", DUR, { start: 0.5 });

    var c = effectComp(MAIN, DUR);
    c.motionBlur = true;
    solidL(c, "BG black", [0, 0, 0]);
    var ctl = controls(c);
    slider(ctl, "Smear Amount %", 100);
    slider(ctl, "Whip Distance %", 100);
    // bottom to top: each incoming shot sits above the one it replaces
    var s1 = shot(c, srcA, "SHOT 1 (whips out)", null, CUTS[0]);
    var s2 = shot(c, srcB, "SHOT 2 (whips in + out)", CUTS[0], CUTS[1]);
    var s3 = shot(c, srcC, "SHOT 3 (whips in + out)", CUTS[1], CUTS[2]);
    var s4 = shot(c, srcD, "SHOT 4 (whips in)", CUTS[2], null);
    ctl.moveToBeginning();

    // whoosh on every cut, loudest point on the cut frame; a heavier low hit under the middle cut
    for (var m = 0; m < CUTS.length; m++) {
        sfx(c, "sfx_layering/sfx_mid_whoosh.mp3", "WHOOSH " + (m + 1) + " (peak on cut)", t(CUTS[m]), 0.2, 2);
        try { c.markerProperty.setValueAtTime(t(CUTS[m]), new MarkerValue("cut " + (m + 1))); } catch (em) {}
    }
    var sub = sfx(c, "sfx_layering/sfx_low_boom.mp3", "SUB HIT (key cut)", t(CUTS[1]), 0.233, -8);
    try {   // cut the boom's long tail so it does not bury the next whoosh
        var lv = sub.property("ADBE Audio Group").property("ADBE Audio Levels");
        lv.setValueAtTime(t(CUTS[1] + 6), [-8, -8]); lv.setValueAtTime(t(CUTS[1] + 18), [-48, -48]);
        sub.outPoint = t(CUTS[1] + 19);
    } catch (eb) { log("  whip param: boom fade " + eb.toString()); }

    note(c, "Whip Pan Transition: every hard cut hides inside a left-to-right camera whip. Each shot runs Motion Tile (300 x 130 %, mirror edges) > Transform (own 360 degree shutter) sliding the frame right with an ease-in > Directional Blur 90 degrees keyed 0, 200, then 1000 for the smear frames. The incoming shot fades up over 2 frames inside the smear and lands sharp 5 frames after the cut. Scale the whole thing with the CONTROLS sliders; move a cut by sliding both shot layers and their keys together.");
    return c;
}
