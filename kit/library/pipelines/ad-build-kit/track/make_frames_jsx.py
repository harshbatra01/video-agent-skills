"""plan the exact source frames needed for board tracking and write ae/frames_tt.jsx (AE renders them as PNG/TIFF)"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(HERE, 'pieces.json')))['f233433f']
BROLL = [(10.70, 13.18), (19.05, 21.20), (22.78, 25.27), (38.03, 40.12)]
NEED = [(0.0, 30.62), (40.12, 42.13)]
jobs = []
for i, p in enumerate(P):
    for a, b in NEED:
        s, e = max(p['s'], a), min(p['e'], b)
        if e - s <= 0.01:
            continue
        vis = [(s, e)]
        for bs, be in BROLL:
            nv = []
            for x, y in vis:
                if be <= x or bs >= y:
                    nv.append((x, y)); continue
                if x < bs: nv.append((x, bs))
                if be < y: nv.append((be, y))
            vis = nv
        for x, y in vis:
            if y - x > 0.01:
                f0 = int((p['src'] + (x - p['s'])) * 25 + 1e-6) - 1
                f1 = int((p['src'] + (y - p['s'])) * 25 + 1e-6) + 2
                jobs.append(dict(piece=i, s=x, e=y, f0=f0, f1=f1))
json.dump(jobs, open(os.path.join(HERE, 'tt_jobs.json'), 'w'), indent=0)
print(len(jobs), sum(j['f1'] - j['f0'] for j in jobs), 'frames')
js = ',\n'.join('[%d,%d,%d]' % (j['piece'], j['f0'], j['f1']) for j in jobs)
OUT = os.path.join(HERE, 'tt_frames').replace(os.sep, '/')
os.makedirs(os.path.join(HERE, 'tt_frames'), exist_ok=True)
jsx = r'''// render exact source frames of the 3 things A-roll (1512x852, 25 fps) for board tracking
app.beginSuppressDialogs();
var SRC = "C:/VISION/IMMUFIX/repair/ENCODED RUSHES/Cleaned/A003_09181253_C118-esv2-50p-bg-10p-music-10p.mp4";
var OUT = "%OUT%/";
var JOBS = [%JOBS%];
var LOG = [];
function writeFile(p, s) { var f = new File(p); f.encoding = "UTF-8"; f.open("w"); f.write(s); f.close(); }
try {
    var proj = app.newProject();
    var it = proj.importFile(new ImportOptions(new File(SRC)));
    LOG.push("footage " + it.width + "x" + it.height + " fps " + it.frameRate + " dur " + it.duration);
    var c = proj.items.addComp("src", 1512, 852, 1, it.duration, 25);
    var L = c.layers.add(it);
    L.property("ADBE Transform Group").property("ADBE Scale").setValue([25, 25]);
    L.property("ADBE Transform Group").property("ADBE Position").setValue([756, 426]);
    for (var j = 0; j < JOBS.length; j++) {
        var d = new Folder(OUT + "p" + JOBS[j][0] + "_" + JOBS[j][1]); if (!d.exists) d.create();
        var rq = proj.renderQueue.items.add(c);
        rq.timeSpanStart = JOBS[j][1] / 25; rq.timeSpanDuration = (JOBS[j][2] - JOBS[j][1]) / 25;
        var om = rq.outputModule(1);
        var ok = false;
        try { om.setSettings({"Format": "PNG Sequence"}); ok = true; } catch (e1) { LOG.push("setSettings PNG failed: " + e1.toString()); }
        if (!ok) om.applyTemplate("TIFF Sequence with Alpha");
        om.file = new File(d.fsName + "/f_[#####]." + (ok ? "png" : "tif"));
    }
    writeFile(OUT + "frames_log.txt", LOG.join("\n"));
    proj.renderQueue.render();
    LOG.push("render done");
} catch (err) { LOG.push("FATAL " + err.toString() + " line " + err.line); }
writeFile(OUT + "frames_log.txt", LOG.join("\n"));
writeFile(OUT + "DONE.txt", "done");
'''.replace('%OUT%', OUT).replace('%JOBS%', js)
open(os.path.join(HERE, '..', 'ae', 'frames_tt.jsx'), 'w').write(jsx)
print('wrote frames_tt.jsx')
