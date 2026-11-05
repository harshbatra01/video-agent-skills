"""Generate build_full.jsx: builds a full meme-compilation edit in Premiere 2025 from edl_full.json, run through the
Premiere bridge (pp.py --v 2025). Masks, preset names and clip gain are added afterwards by patch_full.py."""
import json, sys

edl = json.load(open("edl_full.json"))
OUT = "/CHANGE/ME/client folder/"
cfg = {
    "proj": OUT + (sys.argv[1] if len(sys.argv) > 1 else "CHANGE_ME edit.prproj"),
    "white": OUT + "Gray Background 1920x1080.png",   # the reference style's backgrounds are gray (editor's matte RGB 100)
    "seq": "CHANGE_ME sequence",
    "raw": edl["raw"],
    "total_f": edl["total_f"],
    "cuts": [[c["raw_in_f"], c["raw_out_f"], c["out_start_f"]] for c in edl["cuts"]],
    "images": [{"path": im["path"], "name": im["path"].split("/")[-1], "s": im["start_f"], "e": im["end_f"],
                "crop": im["crop"], "scale": im["scale"], "pos": im["pos"],
                "video": im.get("video", False), "media_f": im.get("media_f"), "speed": im.get("speed", 1.0),
                "blurs": [{"kind": b["kind"], "keys": b.get("keys")} for b in im["blurs"]]} for im in edl["images"]],
}

JSX = r"""
(function () {
var C = %s;
var TPF = 8467200000;
var log = [];
function T(f) { return String(f * TPF); }

// phase B: the project was created and filled by the import_*.jsx steps in this session and is open now
if (!(app.project && app.project.path === C.proj)) return "ABORT: run the import steps first (project not open)";
var root = app.project.rootItem;
var memes = null;
for (var bi = 0; bi < root.children.numItems; bi++) if (root.children[bi].name === "Memes") memes = root.children[bi];
if (!memes) return "ABORT: Memes bin missing";
function find(bin, name) { for (var i = 0; i < bin.children.numItems; i++) if (bin.children[i].name === name) return bin.children[i]; return null; }
var raw = find(root, C.raw.split("/").pop());
var white = find(root, C.white.split("/").pop());
var seq = app.project.createNewSequenceFromClips(C.seq, [raw], root);
app.project.activeSequence = seq;
function clearTrack(t) { for (var j = t.clips.numItems - 1; j >= 0; j--) t.clips[j].remove(false, false); }
for (var v = 0; v < seq.videoTracks.numTracks; v++) clearTrack(seq.videoTracks[v]);
for (var a = 0; a < seq.audioTracks.numTracks; a++) clearTrack(seq.audioTracks[a]);

// V2: white background for the whole edit
white.setInPoint(T(0), 4); white.setOutPoint(T(C.total_f), 4);
seq.videoTracks[1].overwriteClip(white, T(0));

// V3: memes (every overwrite is checked and retried: Premiere occasionally drops one)
function clipStarting(track, startF) { for (var i = 0; i < track.clips.numItems; i++) if (Number(track.clips[i].start.ticks) === startF * TPF) return track.clips[i]; return null; }
for (var m = 0; m < C.images.length; m++) {
  var im = C.images[m];
  var it = find(memes, im.name);
  if (!it) { log.push("MISSING project item " + im.name); continue; }
  for (var tries = 0; tries < 4; tries++) {
    if (im.video) { it.clearInPoint(); it.clearOutPoint(); }
    else { it.setInPoint(T(0), 4); it.setOutPoint(T(im.e - im.s), 4); }
    seq.videoTracks[2].overwriteClip(it, T(im.s));
    if (clipStarting(seq.videoTracks[2], im.s)) break;
    log.push(im.name + " did not land at " + im.s + " (attempt " + (tries + 1) + ")");
  }
  if (im.video) {
    app.enableQE();
    var qv = qe.project.getActiveSequence().getVideoTrackAt(2), qclip = null;
    for (var qq = 0; qq < qv.numItems; qq++) { var xx = qv.getItemAt(qq); if (xx.type === "Clip" && Number(xx.start.ticks) === im.s * TPF) qclip = xx; }
    var sres = "no QE clip";
    if (qclip) { try { sres = qclip.setSpeed(im.speed, "", false, false, false); } catch (e) { sres = "setSpeed error " + e; } }   // a multiplier
    var vc = clipStarting(seq.videoTracks[2], im.s);
    log.push("video " + im.name + " speed " + im.speed + " -> " + sres + "; clip " + (vc ? (Number(vc.end.ticks) - Number(vc.start.ticks)) / TPF : "MISSING") + " frames (slot " + (im.e - im.s) + ")");
  }
}
// voice goes down after the memes so a video meme's own audio can never replace it
// V1 + A1: the voiceover cuts
function startsAt(track, startF) { for (var i = 0; i < track.clips.numItems; i++) if (Number(track.clips[i].start.ticks) === startF * TPF) return true; return false; }
for (var k = 0; k < C.cuts.length; k++) {
  for (var attempt = 0; attempt < 4; attempt++) {   // an overwrite occasionally fails to land: check and place it again
    raw.clearInPoint(); raw.clearOutPoint();
    raw.setInPoint(T(C.cuts[k][0]), 4);
    raw.setOutPoint(T(C.cuts[k][1]), 4);
    seq.videoTracks[0].overwriteClip(raw, T(C.cuts[k][2]));
    if (startsAt(seq.videoTracks[0], C.cuts[k][2]) && startsAt(seq.audioTracks[0], C.cuts[k][2])) break;
    log.push("cut " + k + " at frame " + C.cuts[k][2] + " did not land (attempt " + (attempt + 1) + ")");
  }
}
raw.clearInPoint(); raw.clearOutPoint();
for (var a2 = 1; a2 < seq.audioTracks.numTracks; a2++) clearTrack(seq.audioTracks[a2]);  // the recording carries 3 identical audio streams
// the recording has the mic on the right channel only: copy it to the left on every voice clip
app.enableQE();
var qa = qe.project.getActiveSequence().getAudioTrackAt(0);
var FILL = qe.project.getAudioEffectByName("Fill Left with Right");
var nf = 0;
for (var q0 = 0; q0 < qa.numItems; q0++) { var ai = qa.getItemAt(q0); if (ai.type === "Clip") { ai.addAudioEffect(FILL); nf++; } }
log.push("Fill Left with Right on " + nf + " voice clips");
log.push("V1 cuts=" + seq.videoTracks[0].clips.numItems + " A1=" + seq.audioTracks[0].clips.numItems + " A2=" + seq.audioTracks[1].clips.numItems + " A3=" + seq.audioTracks[2].clips.numItems);

var v3 = seq.videoTracks[2];
log.push("V2=" + seq.videoTracks[1].clips.numItems + " V3=" + v3.clips.numItems);

app.enableQE();
var qt = qe.project.getActiveSequence().getVideoTrackAt(2);
var GB = qe.project.getVideoEffectByName("Gaussian Blur");
var CROP = qe.project.getVideoEffectByName("Crop");
var TINT = qe.project.getVideoEffectByName("Tint");
function qeItemAt(startF) {
  for (var q = 0; q < qt.numItems; q++) { var x = qt.getItemAt(q); if (x.type === "Clip" && Number(x.start.ticks) === startF * TPF) return x; }
  return null;
}
function comps(ti, mn) { var r = []; for (var c = 0; c < ti.components.numItems; c++) if (ti.components[c].matchName === mn) r.push(ti.components[c]); return r; }
function prop(cp, name) { for (var p = 0; p < cp.properties.numItems; p++) if (cp.properties[p].displayName === name) return cp.properties[p]; return null; }

for (var n = 0; n < C.images.length; n++) {
  var spec = C.images[n];
  var qi = qeItemAt(spec.s);
  if (!qi) { log.push("QE item missing for " + spec.name); continue; }
  var hasCrop = (spec.crop.L + spec.crop.T + spec.crop.R + spec.crop.B) > 0;
  for (var b = spec.blurs.length - 1; b >= 0; b--) qi.addVideoEffect(spec.blurs[b].kind === "blackout" ? TINT : GB);   // each add lands on top, so add in reverse
  if (hasCrop) qi.addVideoEffect(CROP);
  var ti = null;
  for (var c2 = 0; c2 < v3.clips.numItems; c2++) if (Number(v3.clips[c2].start.ticks) === spec.s * TPF) ti = v3.clips[c2];
  var motion = comps(ti, "AE.ADBE Motion")[0];
  prop(motion, "Scale").setValue(spec.scale, true);
  prop(motion, "Position").setValue([spec.pos[0], spec.pos[1]], true);
  if (hasCrop) {
    var cr = comps(ti, "AE.ADBE AECrop")[0];
    prop(cr, "Left").setValue(spec.crop.L, true); prop(cr, "Top").setValue(spec.crop.T, true);
    prop(cr, "Right").setValue(spec.crop.R, true); prop(cr, "Bottom").setValue(spec.crop.B, true);
  }
  var gbs = [];   // blur and black-box effects in stack order
  for (var cc = 0; cc < ti.components.numItems; cc++) { var mnm = ti.components[cc].matchName; if (mnm === "AE.ADBE Gaussian Blur 2" || mnm === "AE.ADBE Tint") gbs.push(ti.components[cc]); }
  var inTicks = Number(ti.inPoint.ticks);
  for (var g = 0; g < spec.blurs.length; g++) {
    var kind = spec.blurs[g].kind;
    if (kind === "blackout") {   // Tint with both ends mapped to black = solid black inside its mask
      var mb = prop(gbs[g], "Map Black To"), mw = prop(gbs[g], "Map White To"), am = prop(gbs[g], "Amount to Tint");
      if (mb) mb.setColorValue(255, 0, 0, 0, true); if (mw) mw.setColorValue(255, 0, 0, 0, true); if (am) am.setValue(100, true);
      if (!mb || !mw || !am) log.push("Tint params missing on " + spec.name);
      continue;
    }
    var bl = prop(gbs[g], "Blurriness");
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
  var order = []; for (var c3 = 0; c3 < ti.components.numItems; c3++) order.push(ti.components[c3].displayName);
  log.push(spec.name.substring(0, 28) + ": " + order.join(" > "));
}
// stills snap to a 29.97 grid and can land 1 frame short: force every end, then audit
function clipAt(track, startF) { for (var i = 0; i < track.clips.numItems; i++) if (Number(track.clips[i].start.ticks) === startF * TPF) return track.clips[i]; return null; }
function forceEnd(track, startF, endF, label) {
  var c = clipAt(track, startF);
  if (!c) return label + " missing";
  if (Number(c.end.ticks) !== endF * TPF) { var t = new Time(); t.ticks = T(endF); c.end = t; log.push("fixed end of " + label + ": " + (Number(clipAt(track, startF).end.ticks) / TPF) + " (wanted " + endF + ")"); }
  return Number(clipAt(track, startF).end.ticks) === endF * TPF ? "" : label + " end " + Number(clipAt(track, startF).end.ticks) / TPF + " != " + endF;
}
var problems = [];
for (var f = 0; f < C.images.length; f++) { var pr = forceEnd(v3, C.images[f].s, C.images[f].e, C.images[f].name); if (pr) problems.push(pr); }
var pw = forceEnd(seq.videoTracks[1], 0, C.total_f, "white background"); if (pw) problems.push(pw);
var qs = qe.project.getActiveSequence();
function emptyCheck(tr, label) { for (var i = 0; i < tr.numItems; i++) { var it = tr.getItemAt(i); if (it.type !== "Clip" && Number(it.start.ticks) < C.total_f * TPF) problems.push(label + " empty " + Number(it.start.ticks) / TPF + "-" + Number(it.end.ticks) / TPF); } }
emptyCheck(qs.getVideoTrackAt(0), "V1"); emptyCheck(qs.getVideoTrackAt(1), "V2"); emptyCheck(qs.getVideoTrackAt(2), "V3"); emptyCheck(qs.getAudioTrackAt(0), "A1");
if (Number(seq.end) !== C.total_f * TPF) problems.push("sequence end " + Number(seq.end) / TPF + " != " + C.total_f);
for (var ac = 0; ac < seq.audioTracks[0].clips.numItems; ac++) if (seq.audioTracks[0].clips[ac].name !== raw.name) problems.push("A1 clip " + ac + " is " + seq.audioTracks[0].clips[ac].name);
for (var at = 1; at < seq.audioTracks.numTracks; at++) if (seq.audioTracks[at].clips.numItems) problems.push("A" + (at + 1) + " not empty");
log.push(problems.length ? "GAP AUDIT FAILED: " + problems.join(" | ") : "gap audit ok: no empty frames on V1, V2, V3, A1");
app.project.save();
log.push("saved " + app.project.path);
app.project.closeDocument(0, 0);
return log.join("\n");
})();
"""
if __name__ == "__main__":
    open("build_full.jsx", "w").write(JSX % json.dumps(cfg))
    print("build_full.jsx written", len(JSX), "chars +", len(json.dumps(cfg)), "data")
