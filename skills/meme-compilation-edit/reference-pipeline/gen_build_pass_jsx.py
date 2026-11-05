"""Generate build_pass.jsx: opens the copy of the editor's project (CHANGE_ME edit.prproj) in Premiere 2025
and, on every meme slot of his V3 track, sets the size and adds Crop + Gaussian Blur effects from data/edl_pass.json.
His voice cuts, background and meme timing are not touched. Masks and preset names are added afterwards by
patch_pass.py (Premiere's scripting cannot make masks)."""
import json

edl = json.load(open("data/edl_pass.json"))
OUT = "/CHANGE/ME/client or editor folder/"
cfg = {
    "proj": OUT + "CHANGE_ME edit.prproj",
    "seq": edl["seq"],
    "n_v3": len(edl["images"]),
    "images": [{"idx": im["idx"], "name": im["file"], "s": round(im["start"] * 30), "skip": im.get("skip", False),
                "crop": im.get("crop"), "scale": im.get("scale"), "pos": im.get("pos"), "speed": im.get("speed", 1.0),
                "blurs": [{"kind": b["kind"], "keys": b.get("keys")} for b in im.get("blurs", [])]} for im in edl["images"]],
}

JSX = r"""
(function () {
var C = %s;
var TPF = 8467200000;
var log = [];
function T(f) { return String(f * TPF); }
app.openDocument(C.proj, true, true, true, true);
if (!(app.project && app.project.path === C.proj)) return "ABORT: the copy did not open as the active project (" + (app.project ? app.project.path : "none") + ")";
var seq = null;
for (var si = 0; si < app.project.sequences.numSequences; si++) if (app.project.sequences[si].name === C.seq) seq = app.project.sequences[si];
if (!seq) return "ABORT: sequence " + C.seq + " missing";
app.project.openSequence(seq.sequenceID);
app.project.activeSequence = seq;
var v3 = seq.videoTracks[2];
if (v3.clips.numItems !== C.n_v3) return "ABORT: V3 has " + v3.clips.numItems + " clips, plan has " + C.n_v3;

app.enableQE();
var qs = qe.project.getActiveSequence();
var qt = qs.getVideoTrackAt(2);
var GB = qe.project.getVideoEffectByName("Gaussian Blur");
var CROP = qe.project.getVideoEffectByName("Crop");
function qeItemAt(startF) {
  for (var q = 0; q < qt.numItems; q++) { var x = qt.getItemAt(q); if (x.type === "Clip" && Number(x.start.ticks) === startF * TPF) return x; }
  return null;
}
function clipAt(startF) { for (var i = 0; i < v3.clips.numItems; i++) if (Number(v3.clips[i].start.ticks) === startF * TPF) return v3.clips[i]; return null; }
function comps(ti, mn) { var r = []; for (var c = 0; c < ti.components.numItems; c++) if (ti.components[c].matchName === mn) r.push(ti.components[c]); return r; }
function prop(cp, name) { for (var p = 0; p < cp.properties.numItems; p++) if (cp.properties[p].displayName === name) return cp.properties[p]; return null; }

var done = 0, skipped = 0;
for (var n = 0; n < C.images.length; n++) {
  var spec = C.images[n];
  if (spec.skip) { skipped++; continue; }
  var ti = clipAt(spec.s), qi = qeItemAt(spec.s);
  if (!ti || !qi) { log.push("MISSING slot " + spec.idx + " " + spec.name + " at frame " + spec.s); continue; }
  if (ti.name !== spec.name) log.push("NAME slot " + spec.idx + ": timeline has " + ti.name + ", plan has " + spec.name);
  var hasCrop = (spec.crop.L + spec.crop.T + spec.crop.R + spec.crop.B) > 0;
  for (var b = spec.blurs.length - 1; b >= 0; b--) qi.addVideoEffect(GB);   // each add lands on top, so add in reverse
  if (hasCrop) qi.addVideoEffect(CROP);
  ti = clipAt(spec.s);
  var motion = comps(ti, "AE.ADBE Motion")[0];
  prop(motion, "Scale").setValue(spec.scale, true);
  prop(motion, "Position").setValue([spec.pos[0], spec.pos[1]], true);
  if (hasCrop) {
    var cr = comps(ti, "AE.ADBE AECrop")[0];
    prop(cr, "Left").setValue(spec.crop.L, true); prop(cr, "Top").setValue(spec.crop.T, true);
    prop(cr, "Right").setValue(spec.crop.R, true); prop(cr, "Bottom").setValue(spec.crop.B, true);
  }
  var gbs = comps(ti, "AE.ADBE Gaussian Blur 2");
  if (gbs.length !== spec.blurs.length) log.push("BLUR COUNT slot " + spec.idx + ": " + gbs.length + " vs " + spec.blurs.length);
  var inTicks = Number(ti.inPoint.ticks);
  for (var g = 0; g < spec.blurs.length && g < gbs.length; g++) {
    var kind = spec.blurs[g].kind;
    var bl = prop(gbs[g], "Blurriness");
    var rep = prop(gbs[g], "Repeat Edge Pixels"); if (rep) rep.setValue(true, true);
    if (kind === "curse") bl.setValue(100, true);
    else if (kind === "wipe") bl.setValue(40, true);
    else {
      bl.setTimeVarying(true);
      var keys = spec.blurs[g].keys;
      for (var kk = 0; kk < keys.length; kk++) {
        var t = new Time(); t.ticks = String(inTicks + Math.round(keys[kk][0] * 30 * spec.speed) * TPF);
        bl.addKey(t); bl.setValueAtKey(t, keys[kk][1], true);
      }
    }
  }
  done++;
}
log.push("effects on " + done + " memes, " + skipped + " left as the editor made them");
// nothing moved: V1/A1/V3 counts and the sequence end are unchanged
log.push("V1=" + seq.videoTracks[0].clips.numItems + " A1=" + seq.audioTracks[0].clips.numItems + " V3=" + v3.clips.numItems + " end=" + Number(seq.end) / TPF);
app.project.save();
log.push("saved " + app.project.path);
app.project.closeDocument(0, 0);
return log.join("\n");
})();
"""
open("build_pass.jsx", "w").write(JSX % json.dumps(cfg))
print("build_pass.jsx written", len(JSX), "chars +", len(json.dumps(cfg)), "data")
