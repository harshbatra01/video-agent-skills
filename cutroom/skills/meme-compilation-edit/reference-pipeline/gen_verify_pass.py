"""verify_pass.jsx: open the patched copy of the editor's project in Premiere 2025 and export check frames:
every curse blur (after the reveals), every slanted-text box (mid-snap), wipes mid-way (soft edge check), and the memes
whose crop came from the Oct 13 edge rules. Leaves the project open for review."""
import json, sys
edl = json.load(open("data/edl_pass.json"))
SEQ = edl["seq"]
PROJ = "/CHANGE/ME/<editor project copy> edit.prproj"
OUT = "/CHANGE/ME/check frames/"
extra = set(sys.argv[1:])                 # extra meme names to include
frames = {}
def add(f, label):
    frames.setdefault(int(f), label)
wipes = 0
for im in edl["images"]:
    if im.get("skip"):
        continue
    s, e = round(im["start"] * 30), round(im["end"] * 30)
    tag = im["file"][:18].replace(" ", "_")
    kinds = [b["kind"] for b in im["blurs"]]
    if "curse" in kinds:
        add(e - 3, f"curse_{tag}")
    for b in im["blurs"]:
        if b["kind"] == "box" and isinstance(b["box"][0], list):
            add(s + round((b["keys"][0][0] + b["keys"][1][0]) / 2 * 30), f"quad_{tag}")
        if b["kind"] == "wipe" and wipes < 10:
            t0, t1 = b["path_keys"]
            add(s + round((t0 + 0.4 * (t1 - t0)) * 30), f"wipe_{tag}")
            wipes += 1
    if im.get("edge_rule") or im["file"] in extra:
        add(e - 3, f"edge_{tag}")
def tc(f):
    sec, fr = divmod(f, 30); m, sec = divmod(sec, 60); h, m = divmod(m, 60)
    return "%02d;%02d;%02d;%02d" % (h, m, sec, fr)
FR = [[f, tc(f), "%05d_%s" % (f, lab)] for f, lab in sorted(frames.items())]
JSX = r"""
(function () {
var P = %s, OUT = %s, FR = %s, SEQ = %s;
var log = [];
if (!(app.project && app.project.path === P)) { if (!app.openDocument(P, true, true, true, true)) return "open failed"; }
var seq = null;
for (var i = 0; i < app.project.sequences.numSequences; i++) if (app.project.sequences[i].name === SEQ) seq = app.project.sequences[i];
if (!seq) return "sequence missing";
app.project.openSequence(seq.sequenceID);
app.project.activeSequence = seq;
app.enableQE();
var q = qe.project.getActiveSequence();
var f0 = new Folder(OUT); if (!f0.exists) f0.create();
for (var pass = 0; pass < 2; pass++) {          // the first export after opening can show "Media pending"
  for (var k = 0; k < FR.length; k++) q.exportFramePNG(FR[k][1], OUT + FR[k][2] + ".png");
  $.sleep(4000);
}
log.push("exported " + FR.length + " frames; V1=" + seq.videoTracks[0].clips.numItems + " V3=" + seq.videoTracks[2].clips.numItems + " A1=" + seq.audioTracks[0].clips.numItems);
return log.join("\n");
})();
"""
open("verify_pass.jsx", "w").write(JSX % (json.dumps(PROJ), json.dumps(OUT), json.dumps(FR), json.dumps(SEQ)))
print("verify_pass.jsx", len(FR), "frames")
