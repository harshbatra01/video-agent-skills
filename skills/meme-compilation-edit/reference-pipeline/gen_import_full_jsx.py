"""Import steps for the build: a fresh project with the recording and background, then the memes 20 per call, saving after
each call. One long script with ~170 imports stalled Premiere 2025 (Oct 11 2026): its import progress windows piled up
while the script held the UI thread. Short calls let Premiere close them in between."""
import json, sys
sys.path.insert(0, ".")
from gen_build_full_jsx import cfg, edl    # paths and images from the build generator (an import, not exec)
paths = [im["path"] for im in edl["images"]]
first = r"""
(function () {
var C = %s;
if (app.project && app.project.path === C.proj) return "ABORT: target project is open in Premiere";
var pf = new File(C.proj); if (pf.exists) return "ABORT: target project already exists, pick a new name";
if (!app.newProject(C.proj)) return "newProject failed";
var root = app.project.rootItem;
root.createBin("Memes");
app.project.importFiles([C.raw, C.white], true, root, false);
app.project.save();
var open = []; for (var q = 0; q < app.projects.numProjects; q++) open.push(app.projects[q].name);
return "project created; root items " + root.children.numItems + "; open projects: " + open.join(" | ");
})();
""" % json.dumps({"proj": cfg["proj"], "raw": cfg["raw"], "white": cfg["white"]})
open("import_00.jsx", "w").write(first)
chunk = r"""
(function () {
var C = %s;
if (!(app.project && app.project.path === C.proj)) return "ABORT: project not open";
var root = app.project.rootItem, memes = null;
for (var i = 0; i < root.children.numItems; i++) if (root.children[i].name === "Memes") memes = root.children[i];
app.project.importFiles(C.paths, true, memes, false);   // one call per 20 files: one progress window
app.project.save();
return "Memes bin now " + memes.children.numItems;
})();
"""
n = 0
for k in range(0, len(paths), 20):
    n += 1
    open("import_%02d.jsx" % n, "w").write(chunk % json.dumps({"proj": cfg["proj"], "paths": paths[k:k + 20]}))
print("import_00 +", n, "chunks for", len(paths), "memes")
