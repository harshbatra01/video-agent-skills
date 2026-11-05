// master_tail.jsx: final tidy-up of the library project, run after every effect is built.
// MAINS = [[mainComp, "NN Title"], ...] filled by the master specs. Renames each main comp to its numbered name unless an
// expression anywhere refers to the comp by its current name (renaming would break that expression), then removes
// empty precomp folders so effects without helper comps leave no clutter.
function collectExpressions(group, out) {
    for (var i = 1; i <= group.numProperties; i++) {
        var p = group.property(i);
        if (p.propertyType == PropertyType.PROPERTY) {
            try { if (p.canSetExpression && p.expression !== "") out.push(p.expression); } catch (e) {}
        } else { try { collectExpressions(p, out); } catch (e2) {} }
    }
}
function finishLibrary() {
    var ex = [];
    for (var i = 1; i <= app.project.numItems; i++) {
        var it = app.project.item(i);
        if (!(it instanceof CompItem)) continue;
        for (var j = 1; j <= it.numLayers; j++) { try { collectExpressions(it.layer(j), ex); } catch (e) {} }
    }
    var all = ex.join("\n");
    var renamed = 0, kept = 0;
    for (var m = 0; m < MAINS.length; m++) {
        var c = MAINS[m][0], nm = MAINS[m][1];
        if (all.indexOf('"' + c.name + '"') >= 0 || all.indexOf("'" + c.name + "'") >= 0) { kept++; log("kept name (referenced by an expression): " + c.name); continue; }
        c.name = nm; renamed++;
    }
    var removed = 0;
    for (var k = app.project.numItems; k >= 1; k--) {
        var f = app.project.item(k);
        if (f instanceof FolderItem && f.numItems == 0) { try { f.remove(); removed++; } catch (e3) {} }
    }
    log("finishLibrary: renamed " + renamed + ", kept " + kept + ", removed " + removed + " empty folders");
}
