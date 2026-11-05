// effects_probe.jsx: list every effect this After Effects has (category, name, matchName) and the parameters of the
// ones the transition library wants. Writes effects_list.txt and effects_params.txt next to this file.
// Run: python ae_run.py effects_probe.jsx  (it waits for effects_probe_DONE.txt)
var HERE = File($.fileName).parent.fsName.replace(/\\/g, "/") + "/";
function w(name, s) { var f = new File(HERE + name); f.encoding = "UTF-8"; f.open("w"); f.write(s); f.close(); }
w("effects_probe_log.txt", "START " + app.version);
try {
    var out = [];
    for (var i = 0; i < app.effects.length; i++) { var e = app.effects[i]; out.push(e.category + "\t" + e.displayName + "\t" + e.matchName); }
    w("effects_list.txt", out.join("\n"));
    app.newProject();
    var c = app.project.items.addComp("p", 200, 200, 1, 2, 30);
    var a = c.layers.addSolid([1, 1, 1], "s", 200, 200, 1, 2);
    var want = ["ADBE VR Chromatic Aberrations", "CC Wide Time", "ADBE Wave Warp", "ADBE Optics Compensation", "ADBE Radial Blur",
                "ADBE Invert", "ADBE Posterize Time", "ADBE Echo", "CC Radial Fast Blur", "ADBE Displacement Map",
                "ADBE Turbulent Displace", "ADBE Bulge", "ADBE 4ColorGradient", "ADBE Shift Channels", "CC Composite",
                "ADBE Motion Blur", "ADBE Fractal Noise", "ADBE Tint", "ADBE Black&White", "ADBE Threshold2", "CC Light Rays",
                "CC Lens", "ADBE Glo2", "ADBE Exposure2", "ADBE Venetian Blinds", "ADBE Linear Wipe", "CC Scale Wipe",
                "ADBE Twirl", "ADBE Polar Coordinates", "ADBE Mosaic", "ADBE Brightness & Contrast 2", "ADBE Hue Saturation",
                "CC Toner", "ADBE Tritone", "ADBE Colorama", "ADBE Set Matte3", "ADBE Channel Mixer", "ADBE Fill"];
    var lines = [];
    for (var k = 0; k < want.length; k++) {
        var ep = a.property("ADBE Effect Parade");
        try {
            var fx = ep.addProperty(want[k]);
            var ps = [];
            for (var j = 1; j <= fx.numProperties; j++) { var p = fx.property(j); ps.push(p.matchName + "=" + p.name); }
            lines.push(want[k] + " OK :: " + ps.join(" | "));
            fx.remove();
        } catch (er) { lines.push(want[k] + " MISSING " + er.toString()); }
    }
    w("effects_params.txt", lines.join("\n"));
} catch (err) { w("effects_probe_err.txt", err.toString()); }
w("effects_probe_DONE.txt", "done");
try { app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES); } catch (eq) {}
app.quit();
