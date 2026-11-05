// exposure_probe.jsx: does Exposure respond to setValue vs setValueAtTime, before / after other effects are added?
// Renders 4 one-frame PNGs of a mid-grey solid under different adjustment-layer setups; read the pixel values after.
var HERE = File($.fileName).parent.fsName.replace(/\\/g, "/") + "/";
function w(name, s) { var f = new File(HERE + name); f.encoding = "UTF-8"; f.open("w"); f.write(s); f.close(); }
var LOG = [];
try {
    app.beginSuppressDialogs(); app.newProject();
    var tests = ["setValue", "setValueAtTime", "setValue_then_BW", "byName"];
    for (var i = 0; i < tests.length; i++) {
        var c = app.project.items.addComp("probe_" + tests[i], 64, 64, 1, 1 / 30, 30);
        c.layers.addSolid([0.4, 0.4, 0.4], "grey", 64, 64, 1, 1 / 30);
        var a = c.layers.addSolid([1, 1, 1], "adj", 64, 64, 1, 1 / 30); a.adjustmentLayer = true;
        var ep = a.property("ADBE Effect Parade"); ep.addProperty("ADBE Exposure2"); var ex = ep.property(ep.numProperties);
        if (tests[i] == "setValue") ex.property("ADBE Exposure2-0003").setValue(1.8);
        if (tests[i] == "setValueAtTime") ex.property("ADBE Exposure2-0003").setValueAtTime(0, 1.8);
        if (tests[i] == "setValue_then_BW") { ex.property("ADBE Exposure2-0003").setValue(1.8); ep.addProperty("ADBE Black&White"); }
        if (tests[i] == "byName") { var p = null; for (var k = 1; k <= ex.numProperties; k++) if (ex.property(k).name == "Exposure") p = ex.property(k); if (p) p.setValue(1.8); }
        LOG.push(tests[i] + ": value now " + ex.property("ADBE Exposure2-0003").value + " | matchName check " + ex.property("ADBE Exposure2-0003").name);
        c.saveFrameToPng(0, new File(HERE + "probe_" + tests[i] + ".png"));
    }
} catch (e) { LOG.push("ERR " + e.toString() + " line " + e.line); }
w("exposure_probe_log.txt", LOG.join("\n"));
$.sleep(4000);
w("exposure_probe_DONE.txt", "done");
try { app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES); } catch (eq) {}
app.quit();
