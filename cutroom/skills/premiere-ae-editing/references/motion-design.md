# Building graphics, titles and motion with these tools (mechanics only)

Which device to use, how it should move, the approved recipes with every value, and what reviewers loved or rejected
live in the motion-design skill (`references/effect-vocabulary-and-taste.md` for verdicts, `references/titles-captions-type.md`
for titles, cards, captions and end screens, `references/motion-rules.md` for eases, zooms and timing,
`references/depth-2.5d-3d.md` for stills in depth) and in editing-playbook (`references/taste-verdicts.md`,
`references/captions-and-on-screen-text.md`). This file says where each kind of graphic gets built, which helper builds
it, and how to check it before anyone sees it.

## 1. Where a graphic gets built

| Kind | Build it as | Read |
|---|---|---|
| Simple title, plate, code card, credit pill | Premiere graphic by text (a clone of a graphic the user made) | prproj-format.md section 9, prproj-recipes R26 |
| Zooms on the A-roll, blur boxes, spotlights, tracked board masks, the blur under a glass card | Premiere adjustment layers with Transform / Gaussian Blur / Lumetri and masks | prproj-recipes R18-R22 |
| Animated captions, cards, counters, meters, scales, chapter maps, keyed 3D renders | After Effects element (alpha .mov) on a top track | after-effects.md |
| Cards and overlays made in bulk (news cards, carousels) | HTML template screenshotted by headless Chrome | stills-and-sources.md |
| Stills in depth (presenter in a room) | After Effects 2.5D rig, delivered as a moving plate | after-effects.md section 8 |
| Flash transitions and strobes for music edits | After Effects per-frame recipes, or the user's Premiere recipes | transitions.md |

Why the split: a review change stays one relink or one layer edit (SKILL.md rule 10).

## 2. Helpers for the patterns that worked

| Need | Build with |
|---|---|
| Article / study proof | `imgCard` of the screenshot over `stillBg`, `highlighter` on OCR rects (timing.md OCR), slow push |
| Claim vs evidence | two `imgCard`s and one stamp, or a cork board the camera crosses item by item (a camera null, section 8 of after-effects.md) |
| Product price / spec | product cut-out (stills-and-sources.md) on `softBand` with `softEllipse` behind, `outlineBox` on the price |
| Grade / score graphic | the channel's own graphic rebuilt from its .aep (`ae_dump.py`, after-effects.md section 9) |
| Big number, counter, meter | Source Text expressions driven by one eased progress (after-effects.md section 6), counter sounds from audio.md section 7 |
| Chapter map | scene precomps masked by `createPath` from comp points (`fromComp`), lines drawn with Trim Paths, sliders on a control null |
| 3D render slot | `keyL` (Keylight), `remapL` to land the hit on the word, `softEllipse` glow behind (after-effects.md section 7) |
| Comments / social proof | a rebuilt panel (never a platform's real UI in ads without permission) |
| Board reveal (whiteboard) | tracked blur masks per line in Premiere (prproj-recipes R21) |
| Time / dial | a clock face with ticks drawn by shape layers; fills keyed to the real minutes |
| Clean techy moves (no overshoot) | `k2` / `chain` with named eases (after-effects.md section 13); `popIn` overshoots to 1.1x by default, so set it on purpose |

## 3. Before you deliver a graphic
1. Sheet of 3-4 frames per shot (in, middle, last frame) at 480 px: read it once, fix, re-render only what failed.
2. Check glyphs (blank symbols, after-effects.md section 6), clipped glows (trap 10), half-cut icons, text over faces,
   text that leaves too early, leftover entrance keys that dim an item meant to hold (trap 45).
3. Check timing against the voice: the word the graphic illustrates is under it (word times: timing.md).
4. Effects that last 1-3 frames: every frame (`fsheet.py`) and both sides of every transition.
5. After Effects builds with footage: footage audio off, proven by subtracting the song or the mix (after-effects.md
   section 12).
6. YouTube end screens: draw the usual element zones on the last frames and check nothing important sits under them
   (1920x1080: video about x 1050-1810, y 300-730; subscribe about x 1500-1700, y 790-990). Never add the elements
   yourself; the user adds them in YouTube Studio.
7. Check it in the Premiere timeline at its real time: it can differ from your edit list if the user moved things.
