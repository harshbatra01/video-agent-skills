// meta key: pixel_dither_background
// meta title: Pixel Dither Background
// meta order: 12
// meta refs: analysis/Ddtm_TUgYiZ/ref_pixel_dither_background_2.00.png, analysis/Ddtm_TUgYiZ/ref_pixel_dither_background_texture_2.00.png, analysis/Ddtm_TUgYiZ/ref_pixel_dither_background_3.00.png, analysis/DdtmTkIAf12/ref_pixel_dither_background_3.50.png
// Staged copy: neutral names, fonts from FONTS (lib/effects_lib.jsx).
// Two-colour ordered dither of a cloud clip: grey from the red channel, Mosaic into 4 px cells, minus a tiled 12 px threshold
// map (Subtract), then Threshold + Tint to ink and paper. A blocky pixel wordmark sits on top. Native rebuild of invideo's
// "Pixel Dither (Halftone)" shader.
function build_pixel_dither_background() {
    var DUR = 4;
    var MAIN = "Pixel Dither Background";

    // ---- SOURCE: cloud time-lapse, slowed to half speed (Time Stretch 200%, frame blending on)
    var src = sourceComp("Pixel Dither - SOURCE A", "clouds_a.mov", DUR, {});
    var sl = src.layer(1);
    try { sl.stretch = 200; sl.inPoint = 0; sl.outPoint = DUR; sl.frameBlendingType = FrameBlendingType.FRAME_MIX; src.frameBlending = true; } catch (es) { log("  stretch " + es.toString()); }

    // ---- pattern: the 12 x 12 px threshold tile (stock/pixel_dither_tile_12px.png, 8-bit grey). Each grey is the brightness a
    // pixel needs before it turns to paper: square rings that light up from the outside in (the ring texture in the mid-tones),
    // a 4 px lattice of ink dots that stays until near white and a 4 px lattice of paper dots that shows even in the sky.
    var pat = effectComp("Pixel Dither - pattern (12 px tile)", DUR, 12, 12);
    var tile = pat.layers.add(stock("pixel_dither_tile_12px.png"));
    tile.name = "threshold tile (edit me in any paint app)";
    P(tile).setValue([6, 6]); tile.quality = LayerQuality.DRAFT;

    // ---- threshold map: the tile repeated across the frame
    var map = effectComp("Pixel Dither - threshold map", DUR);
    var tl = addComp(map, pat, "pattern tile");
    P(tl).setValue([6, 6]);
    tl.quality = LayerQuality.DRAFT;
    var rt = fxp(tl, "CC RepeTile", [["Expand Right", 1920], ["Expand Down", 1080]], "CC RepeTile");

    // ---- wordmark: heavy serif, roughened, then 24 px blocks with a hard alpha cut
    var wm = effectComp("Pixel Dither - wordmark", DUR);
    var t = txt(wm, "TITLE", FONTS.serifBold, 430, [1, 1, 1], ParagraphJustification.CENTER_JUSTIFY, 0, 905, 540);
    t.name = "TITLE (placeholder wordmark)";
    var r = centreAnchor(t);
    P(t).setValue([905, 540]);
    var sx = 1440 / r.width * 100, sy = 350 / r.height * 100;
    S(t).setValue([sx, sy]);
    var re = fxp(t, "ADBE Roughen Edges", [["Border", 30], ["Edge Sharpness", 1], ["Fractal Influence", 1], ["Scale", 45], ["Complexity", 2]], "Roughen Edges");
    var wa = adjL(wm, "BLOCKS (Mosaic 24 px + hard alpha + fill)");
    fxp(wa, "ADBE Mosaic", [["Horizontal Blocks", 80], ["Vertical Blocks", 45], ["Sharp Colors", 1]], "Mosaic");
    var pv = fxp(wa, "ADBE Pro Levels2", [], "Levels (Individual Controls)");
    setDeep(pv, "Alpha Input Black", 120 / 255);
    pv = wa.property("ADBE Effect Parade").property("Levels (Individual Controls)");
    setDeep(pv, "Alpha Input White", 136 / 255);
    fxp(wa, "ADBE Fill", [["Color", hex("#7ECADD")]], "Fill");

    // ---- plate: grey (red channel) -> 4 px cells, minus the threshold map, then 1-bit ink/paper
    var plate = effectComp("Pixel Dither - plate", DUR);
    var lum = addComp(plate, src, "PD_Lum (red channel grey, 4 px cells)");
    var sc = fxp(lum, "ADBE Shift Channels", [], "Shift Channels (grey from red)");
    try { sc.property("Take Green From").setValue(2); } catch (e1) { log("  shift g " + e1.toString()); }
    sc = lum.property("ADBE Effect Parade").property("Shift Channels (grey from red)");
    try { sc.property("Take Blue From").setValue(2); } catch (e2) { log("  shift b " + e2.toString()); }
    fxp(lum, "ADBE Easy Levels2", [["Input Black", 80 / 255], ["Input White", 252 / 255], ["Gamma", 0.5]], "Levels");
    fxp(lum, "ADBE Mosaic", [["Horizontal Blocks", 480], ["Vertical Blocks", 270], ["Sharp Colors", 1]], "Mosaic (4 px)");
    var ml = addComp(plate, map, "PD_Map (threshold map, Subtract)");
    ml.blendingMode = BlendingMode.SUBTRACT;
    ml.quality = LayerQuality.DRAFT;
    var ad = adjL(plate, "ADJ_Dither (Threshold + Tint)");
    var th = fxp(ad, "ADBE Threshold2", [], "Threshold");
    th.property(1).setValue(1 / 255);   // Threshold Level is 0-1 in this AE
    fxp(ad, "ADBE Tint", [["Map Black To", hex("#5FB6CF")], ["Map White To", hex("#F3FBFD")], ["Amount to Tint", 100]], "Tint (ink + paper)");
    gaussBlur(ad, 0.6);   // the reel's softness (compression); set to 0 for crisp pixels
    var wl = addComp(plate, wm, "PD_Wordmark (above the dither)");

    // ---- main: the plate with a slow push, then a 3.75x punch-in that shows the dot cells
    var c = effectComp(MAIN, DUR);
    var pL = addComp(c, plate, "PLATE");
    A(pL).setValue([1150, 560]); P(pL).setValue([1150, 560]);
    keys(S(pL), [[0, [100, 100]], [2.5, [104, 104], 33, 33], [3.1, [375, 375], 85, 90]]);

    note(c, "Pixel dither. In 'plate', PD_Lum is the clip turned to grey from its red channel, Levels for contrast and Mosaic into 4 px cells; PD_Map is a 12 px grey threshold tile (the PNG in 'pattern') repeated by CC RepeTile and set to Subtract; ADJ_Dither then applies Threshold (Level 1) and Tint (ink #5FB6CF, paper #F3FBFD). Change the look with the PD_Lum Levels (Input Black sets how much sky turns solid ink), the Tint colours, or paint a different tile. The TITLE wordmark is placeholder text made blocky with Roughen Edges, Mosaic 24 px and a hard alpha Levels; swap the clip inside 'Pixel Dither - SOURCE A'.");
    return c;
}
