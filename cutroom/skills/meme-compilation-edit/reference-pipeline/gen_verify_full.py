"""verify_full.jsx: reopen the patched project in Premiere 2025, export check frames, leave it open for review."""
import json
picks = json.load(open("verify_picks.json"))
PROJ = "/CHANGE/ME/<job> edit v2.prproj"
OUT = "/CHANGE/ME/check frames/"
SEQ = "CHANGE_ME sequence"
frames = []
for name, a, b, c in picks:
    for f in sorted(set((b, c))):
        frames.append([f, name[:20].replace(" ", "_") + "_" + str(f)])
def tc(f):
    s, fr = divmod(f, 30); m, s = divmod(s, 60); h, m = divmod(m, 60)
    return "%02d;%02d;%02d;%02d" % (h, m, s, fr)
JSX = r"""
(function () {
var P = %s, OUT = %s, FR = %s, SEQ = %s;
var log = [];
if (!(app.project && app.project.path === P)) { if (!app.openDocument(P, true, true, true, true)) return "open failed"; }
var seq = null;
for (var i = 0; i < app.project.sequences.numSequences; i++) if (app.project.sequences[i].name === SEQ) seq = app.project.sequences[i];
if (!seq) return "sequence missing";
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
open("verify_full.jsx", "w").write(JSX % (json.dumps(PROJ), json.dumps(OUT), json.dumps([[f, tc(f), n] for f, n in frames]), json.dumps(SEQ)))
print("verify_full.jsx", len(frames), "frames")
