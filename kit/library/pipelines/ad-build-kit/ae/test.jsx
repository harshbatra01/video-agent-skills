// smoke test: build a tiny comp, save the project, render it, quit
app.beginSuppressDialogs();
try {
  var proj = app.newProject();
  var comp = proj.items.addComp("test", 540, 960, 1, 2, 60);
  comp.layers.addSolid([0.8, 0.6, 0.2], "gold", 540, 960, 1);
  var t = comp.layers.addText("HELLO");
  proj.save(new File("C:/Users/Kanishk/AppData/Local/Temp/claude/C--VISION-IMMUFIX-repair-ENCODED-RUSHES/b6d96195-2992-4138-a685-9dc3b5c5abcd/scratchpad/ae/test.aep"));
  var rq = proj.renderQueue.items.add(comp);
  var om = rq.outputModule(1);
  var names = om.templates.join(" | ");
  om.file = new File("C:/Users/Kanishk/AppData/Local/Temp/claude/C--VISION-IMMUFIX-repair-ENCODED-RUSHES/b6d96195-2992-4138-a685-9dc3b5c5abcd/scratchpad/ae/test_out");
  proj.renderQueue.render();
  proj.save();
  // write the template list into a comp name so we can read it back from the saved project (no file-write permission needed)
  proj.items.addComp("TEMPLATES:" + names.substr(0, 240), 4, 4, 1, 1, 1);
  proj.save();
} catch (e) {
  try { app.project.items.addComp("ERROR:" + e.toString().substr(0, 200), 4, 4, 1, 1, 1); app.project.save(); } catch (e2) {}
}
app.endSuppressDialogs(false);
app.quit();
