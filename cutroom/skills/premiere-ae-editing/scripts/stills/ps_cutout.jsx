// Photoshop: Select Subject (+ Select and Mask smart radius) -> layer mask -> PSD (editable mask) + PNG (alpha).
// Copy this file, set HERE and OUT, write ps_cutout_jobs.txt, run: $ps = New-Object -ComObject Photoshop.Application; $ps.DoJavaScriptFile("<copy>.jsx")
// macOS run line: osascript -e 'tell application "Adobe Photoshop 2026" to do javascript file (POSIX file "/abs/copy.jsx")'
// (ask the user before launching Photoshop if it is not already open)
// Reads the job list from ps_cutout_jobs.txt (one "src|name" per line). Writes ps_cutout_log.txt. Never touches the sources.
#target photoshop
app.displayDialogs = DialogModes.NO;
var HERE = "__HERE__";   // EDIT: folder holding ps_cutout_jobs.txt (log goes here too), forward slashes, trailing /
var OUT = "__OUT__";     // EDIT: output folder for <name>.psd + <name>.png, trailing /
var LOG = [];
function sid(s) { return stringIDToTypeID(s); }
function cid(s) { return charIDToTypeID(s); }
function readLines(p) { var f = new File(p); f.open("r"); var s = f.read(); f.close(); return s.split(/\r?\n/); }
function writeLog() { var f = new File(HERE + "ps_cutout_log.txt"); f.encoding = "UTF-8"; if (File.fs == "Macintosh") f.lineFeed = "Unix"; f.open("w"); f.write(LOG.join("\n")); f.close(); }

function selectSubject() {
    var d = new ActionDescriptor();
    d.putBoolean(sid("sampleAllLayers"), false);
    executeAction(sid("autoCutout"), d, DialogModes.NO);
}
function refineEdge() {
    // Select and Mask with smart radius; output back to a selection
    var d = new ActionDescriptor();
    d.putUnitDouble(sid("smartBrushRadius"), cid("#Pxl"), 4);
    d.putInteger(sid("smartBrushSmooth"), 0);
    d.putUnitDouble(sid("smartBrushFeather"), cid("#Pxl"), 0.0);
    d.putUnitDouble(sid("smartBrushContrast"), cid("#Prc"), 0);
    d.putUnitDouble(sid("smartBrushShiftEdge"), cid("#Prc"), 0);
    d.putBoolean(sid("sampleAllLayers"), false);
    d.putBoolean(sid("smartBrushUseSmartRadius"), true);
    d.putBoolean(sid("smartBrushDecontaminate"), false);
    d.putEnumerated(sid("refineEdgeOutput"), sid("refineEdgeOutput"), sid("selectionOutputToSelection"));
    executeAction(sid("smartBrushWorkspace"), d, DialogModes.NO);
}
function maskFromSelection() {
    var m = new ActionDescriptor();
    m.putClass(cid("Nw  "), cid("Chnl"));
    var r = new ActionReference(); r.putEnumerated(cid("Chnl"), cid("Chnl"), cid("Msk "));
    m.putReference(cid("At  "), r);
    m.putEnumerated(cid("Usng"), cid("UsrM"), cid("RvlS"));
    executeAction(cid("Mk  "), m, DialogModes.NO);
}

function cafEllipse(x, y, r) {
    var d = new ActionDescriptor(); var ref = new ActionReference();
    ref.putProperty(cid("Chnl"), cid("fsel")); d.putReference(cid("null"), ref);
    var e = new ActionDescriptor();
    e.putUnitDouble(cid("Top "), cid("#Pxl"), y - r); e.putUnitDouble(cid("Left"), cid("#Pxl"), x - r);
    e.putUnitDouble(cid("Btom"), cid("#Pxl"), y + r); e.putUnitDouble(cid("Rght"), cid("#Pxl"), x + r);
    d.putObject(cid("T   "), cid("Elps"), e); d.putBoolean(cid("AntA"), true);
    executeAction(cid("setd"), d, DialogModes.NO);
    var f = new ActionDescriptor();
    f.putEnumerated(cid("Usng"), cid("FlCn"), sid("contentAware"));
    f.putBoolean(sid("contentAwareColorAdaptationFill"), true);
    f.putUnitDouble(cid("Opct"), cid("#Prc"), 100);
    f.putEnumerated(cid("Md  "), cid("BlnM"), cid("Nrml"));
    executeAction(cid("Fl  "), f, DialogModes.NO);
    app.activeDocument.selection.deselect();
}

var jobs = readLines(HERE + "ps_cutout_jobs.txt");
for (var i = 0; i < jobs.length; i++) {
    if (!jobs[i]) continue;
    var parts = jobs[i].split("|"), srcPath = parts[0], nm = parts[1];
    var doc = null;
    try {
        doc = app.open(new File(srcPath));
        if (doc.mode != DocumentMode.RGB) doc.changeMode(ChangeMode.RGB);
        if (doc.bitsPerChannel != BitsPerChannelType.EIGHT) doc.bitsPerChannel = BitsPerChannelType.EIGHT;
        var lyr = doc.activeLayer;
        if (lyr.isBackgroundLayer) lyr.isBackgroundLayer = false;
        lyr.name = "Presenter";
        var spots = 0;
        if (parts.length > 2 && parts[2]) {
            var sp = parts[2].split(";");
            for (var q = 0; q < sp.length; q++) { var v = sp[q].split(","); cafEllipse(Number(v[0]), Number(v[1]), Number(v[2])); spots++; }
        }
        selectSubject();
        var refined = "no";
        try { refineEdge(); refined = "yes"; } catch (e1) { refined = "failed: " + e1.toString().substring(0, 120); }
        maskFromSelection();
        var psd = new PhotoshopSaveOptions(); psd.layers = true;
        doc.saveAs(new File(OUT + "psd/" + nm + ".psd"), psd, true, Extension.LOWERCASE);
        var png = new PNGSaveOptions(); png.compression = 6;
        doc.saveAs(new File(OUT + nm + "_ps.png"), png, true, Extension.LOWERCASE);
        LOG.push("OK " + nm + " " + doc.width.as("px") + "x" + doc.height.as("px") + " refine=" + refined + " cleaned=" + spots);
    } catch (e) {
        LOG.push("FAIL " + nm + ": " + e.toString() + " line " + e.line);
    }
    try { if (doc) doc.close(SaveOptions.DONOTSAVECHANGES); } catch (e2) {}
    writeLog();
}
LOG.push("DONE");
writeLog();
"done";

