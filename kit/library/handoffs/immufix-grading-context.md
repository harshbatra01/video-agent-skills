# Immufix Colour Grading: Full Context for Claude Code

Read this whole file before helping. It holds everything from an earlier chat about colour grading this footage in Adobe Premiere Pro (Lumetri Color). Last updated: 30 Sep 2026.

**Starter prompt to paste into Claude Code:**

> Read IMMUFIX_GRADING_CONTEXT.md fully. I'll give you screenshots of the Premiere Program Monitor, Lumetri panels and scopes. Measure them with the script in Section 11, tell me what's off, then give me the next 1 to 3 slider moves with a "stop when" target.

---

## 1. How to talk to me (the editor)

- I'm new to colour grading. Explain in 5th-grade English, from first principles, without dumbing down the content. Define a term the first time you use it.
- Keep replies short by default: 1 or 2 lines plus the next step. Go fuller only when I ask.
- Write in pointers of 2 or 3 lines max. Be straight and upfront, no fluff.
- **Never use em dashes (the long dash).** Use commas, colons or full stops.
- Give examples, links and "reality tests" (a quick way for me to check a claim myself).
- Use simple diagrams or images when they help.
- **Measure, don't guess.** When I share a screenshot, run the Section 11 script and quote the numbers.
- Slider values are starting points, not magic numbers. Always give a "stop when" target I can see on the scopes.
- My boss gives the notes and I carry them out. Turn vague notes ("kinda pinky", "brighter until it messes up") into exact slider moves plus a scope target.

---

## 2. The project

- **Client:** Immufix, a UK daily supplement brand. Ad campaign (videos plus static ads), audience 30+.
- **Look the boss wants:** his reference brand is AG1, so aim for clean, premium, natural and healthy. He dislikes a boring, corporate look.
- **Current work:** vertical 9:16 social cuts of a presenter talking to camera.
- **Shots seen so far:**
  1. **Bridge shot** (landscape): presenter in a white T-shirt on a wooden bridge over a river, overcast. It arrived very grey and washed out (LOG).
  2. **Sofa shot** (vertical cut): presenter in a dark dress (navy or deep purple, real colour unconfirmed) on a cream/oatmeal linen sofa, garden hedge behind, bright sun behind her (backlit). White captions such as "than it was" sit on a separate layer.

---

## 3. Footage facts

| Item | Value |
|---|---|
| Camera | **Blackmagic** (boss confirmed). Width 6048 matches Blackmagic full-frame 6K bodies (Cinema Camera 6K or PYXIS 6K) |
| Log profile | Probably Blackmagic Film Gen 5 (not confirmed) |
| Clip name example | `A003_09181219_C116`: reel A003, 18 Sep at 12:19, clip 116 (Blackmagic's naming pattern) |
| File being edited | `C:\VISION\IMMUFIX\repair\ENCODED RUSHES\Cleaned\A003_09181219_C116-esv2-50p-bg-10p-music-10p.mp4` |
| Format | H.264 MP4, 8-bit 4:2:0, 6048x3408, 25 fps, about 4 min, about 898 MB |
| Audio | Processed with Adobe Podcast Enhance Speech |
| What Premiere says | Color Space: Rec. 709 |
| The truth | The picture is still **LOG**. The re-encode stripped the camera info and labelled it Rec.709. Don't trust that label |
| Machine | Windows PC. Premiere 2025 or newer (it has Color Space Override, and Lumetri shows "Rec. 709 (Scene)") |

What this means:
- **8-bit** means little room to push. Big moves cause banding (stepped patches in smooth areas like skin or sky).
- If the original `.braw` files turn up, grading from them will be cleaner. None found so far.

---

## 4. Decisions so far (in order)

1. **Boss:** "Add the Rec.709 conversion back", meaning turn the grey LOG image into normal-looking video.
2. **The proper route (not used yet):** Blackmagic's own LUT `Blackmagic Gen 5 Film to Video.cube`, loaded in Lumetri > Basic Correction > Input LUT. It ships with DaVinci Resolve at `C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\LUT\Blackmagic Design\` (a hidden folder, so paste the path into File Explorer), or with Blackmagic's camera software, or a colleague can send it. You don't need to use DaVinci, only the file.
3. **What I actually did:** Interpret Footage > Color Space Override, and picked a **Sony** log option because it looked closest. It works as a starting point, but it's the wrong camera maths, so expect:
   - pink or magenta skin
   - neutral things in shade turning mauve (the shaded sofa)
   - dark colours leaning purple or blue (the black lav mic reads blue)
4. Built a base Lumetri grade on top (Section 5), then refined it over several feedback rounds (Section 6).
5. **Fallback:** if the pink can't be fixed cleanly, switch to the Blackmagic Gen 5 LUT route (override off, Input LUT on).

---

## 5. Lumetri settings (last full screenshot, grade v1)

Later rounds changed some of these (see Sections 6 and 7). **Ask me for fresh panel screenshots before relying on them.**

| Section | Setting | Value |
|---|---|---|
| Basic | Input LUT | None (the Sony override does the conversion) |
| Basic | Temperature | -4 (a mistake, see Section 8) |
| Basic | Tint | -3 |
| Basic | Saturation | 100 |
| Basic | Exposure | -0.2 |
| Basic | Contrast | +8 |
| Basic | Highlights | -20 |
| Basic | Shadows | +8 |
| Basic | Whites | -5 |
| Basic | Blacks | -6.9 |
| Creative | Faded Film | 0 |
| Creative | Sharpen | 13 |
| Creative | Vibrance | 13.2 |
| Creative | Saturation | 100 |
| Curves | RGB | Gentle S: lower-quarter point pulled down a little, upper-quarter point raised a little |
| Curves | Hue vs Sat | Flat (one point added but never moved, so it does nothing) |
| Color Wheels | Midtones | Untouched |
| Color Wheels | Shadows | Touched, but basically neutral |
| Color Wheels | Highlights | Nudged slightly warm |
| Color Wheels | Brightness sliders | All at 0 |
| Vignette | Amount / Midpoint / Roundness / Feather | -0.3 / 50 / 0 / 50 |

Also suggested, not confirmed as done:
- A **second Lumetri Color** with a tracked ellipse mask on the face (a "face light"), Exposure +0.5 to +1.0 inside the mask.
- A Lumetri preset called **"Immufix base"** for copying the grade to other clips.

---

## 6. Feedback rounds and measurements (sofa shot)

Measured from Program Monitor screenshots with the Section 11 script.
- **Luma and levels** use 0 to 100, like the Luma waveform.
- **Skin hue** is the HSV hue in degrees (peach is about 15 to 20, pink is under 10).
- **Angle** is the vectorscope angle (the skin line is about 123).

| Round | Face luma (lit / shade side) | Skin hue / angle | Darkest (0.5%) | Brightest (99.9%) | What was wrong |
|---|---|---|---|---|---|
| Sony override only | about 41 | about 2 / 105 | 11.4 | 79 | Flat and pink |
| Grade v1 | about 35 | 1 to 3 / 104 to 106 | 9.4 | 76 | Face too dark, pink, blacks grey |
| Grade v2 | about 48 / 39 | 9 to 12 / 111 to 115 | 8.1 | 78 | Still a bit grey (dress mostly at 14, darkest about 7) |
| **Grade v3 (latest)** | **about 55 / 45** | **6 to 12 / 109 to 115** | **8.1** | **85** | Boss: "kinda pinky", "fix white balance a little", "brighter until it messes up" |

Grade v3 details:
- **Shaded sofa** (right side): hue about 317, which is mauve. It should read grey-beige.
- **Black lav mic:** leans blue-violet (hue about 255). It should read neutral black. This is the best dark neutral in the frame.
- **Dress:** hue about 250, leaning violet. Its real colour is unconfirmed, so don't force it. Judge by the mic.
- **Sunlit sofa:** hue about 27, a fine cream.
- **Brightest channel** (red) peaks at 241 of 255. That leaves about +0.3 stop of room before the hair and sofa blow out.
- The captions reach pure white and their shadow reaches pure black, so **the display is fine**. The grey look came from the grade.

Simulation on grade v3 (rough, done on the screenshot):
- **White balance fix** (green +3.5%, blue -2.5%, extra blue -5% in the darks): skin hue 13 to 19 (angle 117 to 124, on the skin line), shaded sofa neutral, mic a little less blue.
- **Exposure +0.3 stop:** face about 61 on the lit side, 0.24% of pixels clipped. Fine.
- **Exposure +0.5 stop:** 1.9% clipped. This is the limit.
- **Exposure +0.8 stop:** 5% clipped. Sunlit hair and sofa go flat white ("messed up").

---

## 7. Next steps (open as of 30 Sep 2026)

The boss's latest notes: "kinda pinky", "fix white balance a little", and "increase brightness a bit until it messes up (then back off)". **Pink and white balance are the same fix.**

1. **White balance / pink** (Basic Correction):
   - Tint: about 4 to 6 more toward **green** (drag left).
   - Temperature: about **+2 to +3** (warmer).
   - **Stop when:** the skin blob sits on the vectorscope skin line, the shaded sofa looks grey-beige (not mauve), and the mic looks black (not blue).
   - If the darks still look purple, nudge the **Shadows** wheel crosshair a hair toward yellow-green (to the left).
2. **Brightness:** raise Exposure in **+0.1 steps**.
   - **Stop signs:** the red trace on the RGB waveform hits about 95 to 100, or the hair, sofa or forehead texture goes flat or waxy.
   - Then go **back one step**. Expect about +0.3 more than now.
   - If the face still wants more but the hair is clipping, pull Highlights down further, then push Exposure again.
3. **Blacks:** brightening lifts the blacks, so pull **Blacks** back down (you may need -20 to -25), or drag the RGB curve's bottom-left point slightly to the right. Target: the darkest dress folds at about 2 to 5, with the folds still visible.
4. **Update the "Immufix base" preset** and apply it to the other clips. Fine-tune Exposure and Temperature per clip, since the sun changes between shots.
5. **The face light is per shot** (the mask is tracked to that shot). Redo it on each clip instead of pasting it.
6. **Vignette test:** set Amount to -3 for a moment.
   - If all four corners darken, it's fine. Set it back to -0.3.
   - If only the top and bottom darken, the vignette is being drawn on the wide source frame and cropped away. Set it to 0 and put the vignette on an Adjustment Layer (File > New > Adjustment Layer) above the clips and below the captions.
   - It's unverified which way Premiere behaves here. The test settles it.
7. **Bridge shot:** it has a white T-shirt, so use the Lumetri **White Balance eyedropper** on the shirt.
8. **Final check on a phone**, since that's where the vertical ad will be watched.

---

## 8. Targets and lessons learned

**Targets for this footage**

| Thing | Target |
|---|---|
| Face, lit side | about 55 to 62 on the Luma waveform |
| Face, shade side | about 45 to 50 |
| Skin | On the vectorscope skin line (about 11 o'clock). HSV hue about 15 to 20. Under about 10 reads pink |
| Blacks | Darkest detail at about 2 to 5, with the detail still visible |
| Highlights | Red trace under about 95 on the RGB waveform. Hair and sofa keep their texture |
| Neutral checks | Shaded sofa grey-beige, mic black, sunlit sofa cream |
| Saturation | Use Vibrance (it protects skin) rather than Saturation |

**Lessons (don't repeat these mistakes)**

- **Cooling made the pink worse.** Pink skin has too much red and blue compared with green. The fix is more green Tint plus a little warmth, not Temperature minus.
- **"Face at 60 to 70 IRE" is for faces in direct light.** This face is backlit, so 45 to 62 is right. Going higher looks fake and blows out the hair.
- The Lumetri **Blacks slider is gentle**. You may need big values, or the curve's black point.
- **Hue vs Sat with one point** does nothing until you drag it, and then it moves the whole line. Use 3 points to isolate one colour.
- **Premiere's "Rec. 709" label is wrong** on these re-encoded files. The picture is LOG.
- The **white dashes at the top of the waveform are the captions** at 100. Ignore them.
- Use the **Luma waveform for brightness** and the **RGB waveform for colour balance and clipping**.
- **Don't use the White Balance eyedropper on the sofa shot.** Nothing in it is truly white: the sofa is cream and the captions are graphics.

---

## 9. Premiere click paths

- **Colour workspace:** Window > Workspaces > Color.
- **Scopes:** Window > Lumetri Scopes. Right-click the scope to pick Waveform Type (Luma or RGB) and Vectorscope YUV.
- **Colour space override:** select clips in the Project panel, right-click > Modify > Interpret Footage > Color Space Override.
- **Load a LUT:** Lumetri > Basic Correction > Input LUT > Browse.
- **Before/after:** untick the fx box next to Lumetri Color in Effect Controls.
- **Save a preset:** Effect Controls > right-click Lumetri Color > Save Preset.
- **Copy a grade:** select the graded clip and press Ctrl+C. Select the other clips, right-click > Paste Attributes, and tick Lumetri Color.
- **Face light:**
  1. Drag a second Lumetri Color from the Effects panel onto the clip.
  2. In Effect Controls, click the ellipse mask under that second Lumetri, and raise Mask Feather until no edge shows (often 200+ on 6K).
  3. Click **Track selected mask forward**.
  4. Set Exposure to +0.5 to +1.0 in that second Lumetri. Pick which Lumetri you're editing from the Lumetri panel's top menu, or twirl it open in Effect Controls.
- **Skin-only fix:** Lumetri > HSL Secondary > eyedropper on the cheek > tick Color/Gray to check the selection > small Temperature, Tint or Saturation nudges.
- **Adjustment layer:** File > New > Adjustment Layer, then drag it onto a track above the clips.

---

## 10. How Claude Code should help

Claude Code can't click inside Premiere. The loop is:

1. I save screenshots of the Program Monitor (plus the Lumetri panels and scopes) into this folder, for example `shots/`.
2. Claude reads the image, runs the script below, and reports face luma, skin hue and angle, blacks, highlights, clipping, and the neutral checks.
3. Claude gives the next 1 to 3 slider moves, each with a "stop when" target.
4. Optional: Claude makes a rough mock-up with `--simulate` so I can show the boss the direction. Always label it as a mock-up.

**Placing the measuring boxes:**
- Run `--grid` first and look at the grid image, then put boxes on the forehead, both cheeks, the chin, a neutral (the shaded sofa or the mic), the dress and the hedge.
- Keep boxes out of the caption band.

**Example boxes** for a 406x730 screenshot of the sofa shot, as (x0, y0, x1, y1). Scale them if the screenshot size differs, and note that the face moves between frames:

| Box | Coordinates |
|---|---|
| forehead | 180 105 230 125 |
| cheek left | 170 170 190 190 |
| cheek right | 225 170 245 190 |
| chin | 185 238 215 252 |
| chest | 200 300 230 330 |
| hedge | 20 60 100 110 |
| sunlit sofa | 3 420 20 560 |
| shaded sofa | 330 590 400 660 |
| dress | 150 600 300 700 |
| mic | 212 385 252 425 |
| caption band (exclude) | 0 350 406 380 |

Example run:

```
python analyze_frame.py shots/frame.png --exclude 0 350 406 380 --box forehead 180 105 230 125 --box chin 185 238 215 252 --box sofa_shade 330 590 400 660 --box mic 212 385 252 425 --simulate green=1.035 blue=0.975 shadow_blue=0.95 stops=0.3 blacks=0.06
```

---

## 11. Frame analysis script

Save as `analyze_frame.py`. Needs Python 3 and `pip install pillow numpy`.

```python
"""analyze_frame.py: measure a Premiere Program Monitor screenshot.

Needs: pip install pillow numpy

Usage:
  python analyze_frame.py frame.png --grid
      saves frame_grid.png with x/y numbers, to help you place boxes
  python analyze_frame.py frame.png --exclude 0 350 406 380 --box forehead 180 105 230 125 --box sofa_shade 330 590 400 660
      whole-frame levels (caption band excluded) + stats for each box
  python analyze_frame.py frame.png --exclude 0 350 406 380 --simulate green=1.035 blue=0.975 shadow_blue=0.95 stops=0.3 blacks=0.06
      also saves frame_sim.png: a rough preview of a white balance / exposure / blacks change

Reading the numbers:
  luma      0-100, same scale as the Lumetri Luma waveform
  hue       HSV hue in degrees. Skin ~15-20 is peach. Under ~10 reads pink
  angle     vectorscope angle (Rec.709 Cb/Cr). Skin line ~123. Red box ~103. Yellow box ~175
            90 = 12 o'clock, 123 = about 11 o'clock. Skin under ~112 reads pink, over ~130 reads orange
  clipped   % of pixels with any channel at full white (detail gone)
"""
import argparse
import colorsys
import math

import numpy as np
from PIL import Image, ImageDraw


def load(path):
    return np.asarray(Image.open(path).convert("RGB")).astype(float) / 255.0


def luma(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def region(a, box):
    x0, y0, x1, y1 = box
    r, g, b = (float(v) for v in a[y0:y1, x0:x1].reshape(-1, 3).mean(0))
    h, s, _ = colorsys.rgb_to_hsv(r, g, b)
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    angle = math.degrees(math.atan2((r - y) / 1.5748, (b - y) / 1.8556))
    return {
        "rgb": tuple(int(round(v * 255)) for v in (r, g, b)),
        "hue": round(h * 360, 1),
        "sat": round(s, 2),
        "luma": round(y * 100, 1),
        "angle": round(angle, 1),
    }


def levels(a, exclude=None):
    y = luma(a)
    mask = np.ones(y.shape, bool)
    if exclude:
        x0, y0, x1, y1 = exclude
        mask[y0:y1, x0:x1] = False
    v = y[mask] * 100
    pct = {q: round(float(np.percentile(v, q)), 1) for q in (0.5, 1, 5, 50, 95, 99, 99.9)}
    clipped = round(float(((a.max(2) >= 0.995) & mask).mean() * 100), 2)
    max_rgb = [int(round(float(a[..., c][mask].max() * 255))) for c in range(3)]
    return pct, clipped, max_rgb


def grid(path):
    im = Image.open(path).convert("RGB")
    d = ImageDraw.Draw(im)
    for y in range(0, im.height, 50):
        d.line([(0, y), (8, y)], fill=(255, 255, 0))
        d.text((10, y - 5), str(y), fill=(255, 255, 0))
    for x in range(0, im.width, 50):
        d.line([(x, 0), (x, 8)], fill=(255, 255, 0))
        d.text((x + 2, 10), str(x), fill=(255, 255, 0))
    out = path.rsplit(".", 1)[0] + "_grid.png"
    im.resize((im.width * 2, im.height * 2)).save(out)
    return out


def simulate(a, green=1.0, blue=1.0, shadow_blue=1.0, stops=0.0, blacks=0.0):
    """Rough preview only. Lumetri will not match this exactly."""
    x = a.copy()
    dark = np.clip(1 - luma(a) / 0.35, 0, 1)  # 1 in the darks, 0 above about 35
    x[..., 1] *= green  # more green = less magenta/pink (like Tint to the left)
    x[..., 2] *= blue  # less blue = warmer (like Temperature to the right)
    x[..., 2] *= 1 - (1 - shadow_blue) * dark  # extra warmth only in the darks
    x *= (2 ** stops) ** (1 / 2.4)  # exposure in stops (display gamma about 2.4)
    x -= blacks * np.clip(1 - x / 0.5, 0, 1) ** 2  # pull the darks down, leave mids/highs
    return np.clip(x, 0, 1)


def report(a, boxes, exclude):
    pct, clipped, max_rgb = levels(a, exclude)
    print("Levels (0-100):", pct)
    print("Clipped pixels: %s%%   Max R,G,B (0-255): %s" % (clipped, max_rgb))
    for name, box in boxes:
        print("%-12s %s" % (name, region(a, box)))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("image")
    p.add_argument("--grid", action="store_true")
    p.add_argument("--box", nargs=5, action="append", default=[], metavar=("NAME", "X0", "Y0", "X1", "Y1"))
    p.add_argument("--exclude", nargs=4, type=int, metavar=("X0", "Y0", "X1", "Y1"), help="caption band to ignore")
    p.add_argument("--simulate", nargs="*", metavar="KEY=VALUE")
    args = p.parse_args()

    if args.grid:
        print("Grid saved:", grid(args.image))
        return

    a = load(args.image)
    boxes = [(b[0], tuple(int(v) for v in b[1:])) for b in args.box]
    print("== NOW ==")
    report(a, boxes, args.exclude)

    if args.simulate is not None:
        kw = {k: float(v) for k, v in (s.split("=") for s in args.simulate)}
        s = simulate(a, **kw)
        if args.exclude:  # keep captions untouched
            x0, y0, x1, y1 = args.exclude
            s[y0:y1, x0:x1] = a[y0:y1, x0:x1]
        out = args.image.rsplit(".", 1)[0] + "_sim.png"
        Image.fromarray((s * 255).round().astype(np.uint8)).save(out)
        print("\n== SIMULATED", kw, "==")
        report(s, boxes, args.exclude)
        print("Preview saved:", out)


if __name__ == "__main__":
    main()
```

Notes:
- A screenshot shows display values, which are close to what the scopes show but not identical. Trust Premiere's scopes for final calls.
- `--simulate` is a direction check, not a promise of what Lumetri will do.

---

## 12. Links

- Adobe, colour management in Premiere: https://helpx.adobe.com/premiere/desktop/correct-color/set-up-color-management/about-color-management.html
- Adobe Community, loading a Blackmagic Gen 5 LUT in Premiere: https://community.adobe.com/t5/premiere-pro-discussions/blackmagic-gen-5-lut-not-loading-into-premiere-pro/td-p/11932774
- Blackmagic support downloads (camera software and Resolve, which include the LUTs): https://www.blackmagicdesign.com/support
- Color Finale, LUTs for Blackmagic Gen 4 and Gen 5 footage: https://colorfinale.com/blog/post/jan-2026-giveaway-12-25
- LOG to Rec.709 in Premiere (video): https://www.youtube.com/watch?v=h-qq869sLHQ
- Neat Video, order of effects in Premiere: https://www.neatvideo.com/blog/post/pr-order

---

## 13. Glossary (plain English)

- **LOG:** a camera recording mode that squeezes lots of light detail into the file. It looks grey and flat on purpose, like a zipped file.
- **Rec.709:** the normal colour standard for TVs, phones and YouTube. Converting LOG to Rec.709 "unzips" the image.
- **LUT:** a small recipe file (.cube) that turns one colour look into another, for example LOG into Rec.709.
- **White balance:** making white and grey things look truly white and grey, so every other colour falls into place. Temperature is blue to yellow, Tint is green to pink.
- **Waveform:** a graph of brightness. Left to right matches the picture; bottom is black (0), top is white (100).
- **Vectorscope:** a colour wheel graph. Distance from the centre is how colourful; direction is which colour. The **skin line** shows where healthy skin should point (about 11 o'clock).
- **Clipping / blown out:** brights hit 100 and lose all detail (flat white patches).
- **Crushed:** darks hit 0 and lose all detail (flat black patches).
- **Lifted or grey blacks:** the darkest parts sit well above 0, so the picture looks foggy.
- **Exposure:** overall brightness. **Highlights, Shadows, Whites, Blacks:** brightness of just the bright, dark, brightest and darkest parts.
- **Vibrance vs Saturation:** both add colour. Vibrance boosts dull colours and protects skin; Saturation boosts everything.
- **Mask and tracking:** a shape that limits an effect to one area (like her face), with tracking making the shape follow her as she moves.
- **Adjustment layer:** an empty clip on a track above the others. Effects on it apply to everything below.
- **8-bit and banding:** 8-bit files have fewer colour steps, so heavy grading can show visible steps (bands) in smooth areas.
