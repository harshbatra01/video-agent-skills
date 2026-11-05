// iris_probe.jsx: open the fx_test2 project and report how the iris layers are wired (track matte, enabled, scale keys)
var HERE = File($.fileName).parent.fsName.replace(/\\/g, "/") + "/";
function w(name, s) { var f = new File(HERE + name); f.encoding = "UTF-8"; f.open("w"); f.write(s); f.close(); }
var LOG = [];
try {
    app.beginSuppressDialogs();
    app.open(new File(HERE + "../../../pilot/ae/fx_test2.aep"));
    var comp = null;
    for (var i = 1; i <= app.project.numItems; i++) { var it = app.project.item(i); if (it instanceof CompItem && it.name == "fx_test2") comp = it; }
    for (var j = 1; j <= comp.numLayers; j++) {
        var L = comp.layer(j);
        if (L.name.indexOf("iris") < 0 && L.name.indexOf("3_017") < 0 && L.name.indexOf("matte") < 0) continue;
        var s = j + " " + L.name + " | enabled " + L.enabled + " | in " + L.inPoint.toFixed(3) + " out " + L.outPoint.toFixed(3);
        try { s += " | hasTrackMatte " + L.hasTrackMatte + " type " + L.trackMatteType; } catch (e1) { s += " | tm? " + e1.toString(); }
        try { if (L.trackMatteLayer) s += " matteLayer=" + L.trackMatteLayer.index + ":" + L.trackMatteLayer.name; } catch (e2) {}
        try { s += " | isTrackMatte " + L.isTrackMatte; } catch (e3) {}
        var ep = L.property("ADBE Effect Parade"), names = [];
        for (var k = 1; k <= ep.numProperties; k++) names.push(ep.property(k).matchName);
        s += " | fx " + names.join(",");
        LOG.push(s);
    }
} catch (e) { LOG.push("ERR " + e.toString() + " line " + e.line); }
w("iris_probe_log.txt", LOG.join("\n"));
w("iris_probe_DONE.txt", "done");
try { app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES); } catch (eq) {}
app.quit();
