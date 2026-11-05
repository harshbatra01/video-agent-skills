// threshold_probe.jsx: what scale does Threshold's Level use from a script? Renders a horizontal black-to-white ramp
// through Threshold at several levels; the black/white edge position in each PNG gives the effective level.
var HERE = File($.fileName).parent.fsName.replace(/\\/g, "/") + "/";
function w(name, s) { var f = new File(HERE + name); f.encoding = "UTF-8"; f.open("w"); f.write(s); f.close(); }
var LOG = [];
try {
    app.beginSuppressDialogs(); app.newProject();
    LOG.push("bpc " + app.project.bitsPerChannel);
    var levels = [0.43, 110, 28000];
    for (var i = 0; i < levels.length; i++) {
        var c = app.project.items.addComp("thr" + i, 256, 16, 1, 1 / 30, 30);
        var s = c.layers.addSolid([1, 1, 1], "ramp", 256, 16, 1, 1 / 30);
        var ep = s.property("ADBE Effect Parade"); ep.addProperty("ADBE Ramp"); var r = ep.property(ep.numProperties);
        r.property("ADBE Ramp-0001").setValue([0, 8]); r.property("ADBE Ramp-0002").setValue([0, 0, 0]);
        r.property("ADBE Ramp-0003").setValue([256, 8]); r.property("ADBE Ramp-0004").setValue([1, 1, 1]);
        var a = c.layers.addSolid([1, 1, 1], "adj", 256, 16, 1, 1 / 30); a.adjustmentLayer = true;
        var ap = a.property("ADBE Effect Parade"); ap.addProperty("ADBE Threshold2"); var th = ap.property(ap.numProperties);
        var msg = "";
        try { th.property("ADBE Threshold2-0001").setValue(levels[i]); msg = "set ok"; } catch (e1) { msg = "set ERR " + e1.toString(); }
        LOG.push("level " + levels[i] + ": " + msg + " | reads back " + th.property("ADBE Threshold2-0001").value);
        c.saveFrameToPng(0, new File(HERE + "thr_" + i + ".png"));
    }
} catch (e) { LOG.push("ERR " + e.toString() + " line " + e.line); }
w("threshold_probe_log.txt", LOG.join("\n"));
$.sleep(4000);
w("threshold_probe_DONE.txt", "done");
try { app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES); } catch (eq) {}
app.quit();
