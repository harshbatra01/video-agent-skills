# 01. Pixel Reveal

Recipe name in the study: "The Pixel Reveal". Category: reveal. Source: a tutorial creator's reel (DeRssdegQgm). Confidence of the recipe: medium.

Native build: `../ae/effects/pixel_reveal.jsx` (function `build_pixel_reveal()`).

## What it looks like

A photo on a pure white background (#FFFFFF) appears as a field of hard-edged rectangular blocks. The grid is 55 x 55 blocks locked to the photo, so on the 845x564 on-screen photo each block is 15.4 x 10.25 px (34.9 x 19.6 px for a 1920x1080 layer). Revealed blocks show the photo at full colour and unrevealed blocks are white, with no soft edges and no fade inside a block, and once a block is revealed it never re-hides (static noise). The reveal starts at the bottom-right corner at f3-f4 and its front sweeps diagonally to the top-left corner. The front is ragged: single blocks pop ahead of it, holes stay behind it, and the 10-90% transition band is about 20% of the photo diagonal wide. Front position (50% of blocks revealed, as a fraction of the diagonal measured from top-left): f6 0.72, f8 0.65, f10 0.54, f12 0.45, f14 0.35, f16 0.29, f18 0.20, f20 0.16, f25 0.13, f30 0.10, and the last blocks on the top-left left edge disappear at f31-f32. Revealed area: 17% f6, 39% f8, 55% f10, 70% f12, 79% f14, 87% f16, 91% f18, about 97% f30, 100% f32. The front is fast through the bright end of the ramp and decelerates strongly toward the top-left (exponential, because Exposure is in stops), and the whole reveal takes about 1 s. In the reel the photo slides left with motion blur while it reveals (see kinetic_word_pan), and the blocks move with the photo.

## Inputs

- a still photo (any aspect; the reel used a 3:2 photo of pink lilies by a sunny window with a dark brown door frame on the right) with bright and dark areas
- a white background solid (#FFFFFF)

## Layer stack

Precomp 'PixelReveal' (the reel's 'Pre-comp 9'), 1920x1080 (or the photo's own size), 30 fps, from top to bottom. (1) 'Footage' = the photo (or a precomp holding it), Mode Normal, Track Matte = layer 2 with the Luma toggle (tooltip 'Luma Matte selected'), not inverted. (2) 'Footage' duplicate = matte source, auto-hidden, Mode Normal, carrying the whole effect stack. (3) 'Solid layer' white #FFFFFF, Normal. In the main comp this precomp sits at 845x564 (center 733.5,540.5 at rest), parented to the LAYOUT pan null, with motion blur on.

## Steps

1. Create a comp 'PixelReveal' at 1920x1080, 30 fps, 3 s. Add a white solid #FFFFFF named 'Solid layer' at the bottom.
2. Import the photo (or a 'Footage' precomp of it) above the solid, then duplicate it so there are two identical Footage layers.
3. On the BOTTOM Footage copy (layer 2) add, in this order: Gradient Ramp, Turbulent Noise, Mosaic, Exposure, Posterize.
4. Gradient Ramp: Start of Ramp (1.7, -11.4), Start Color #000000, End of Ramp (2175.3, 1214.2), End Color #FFFFFF, Ramp Shape Radial Ramp, Ramp Scatter 0, Blend With Original 0%. For a layer that is not 1920x1080 use start = (0.09% W, -1.06% H) and end = (113.3% W, 112.4% H).
5. Turbulent Noise: leave every parameter at default (static, no Evolution animation), but set Blending Mode = Overlay at Opacity 100% so the noise breaks up the ramp without replacing it (inferred, see unreadable).
6. Mosaic: Horizontal Blocks 55, Vertical Blocks 55, Sharp Colors off.
7. Exposure: Channels Master, Master Exposure keyframes 0:00:00:00 = -2.53 and 0:00:01:17 (frame 47) = 14.29, both LINEAR. Leave Offset 0, Gamma 1, Bypass Linear Light Conversion OFF.
8. Posterize: Level 2, which makes the matte pure black/white blocks.
9. On the TOP Footage copy (layer 1) set Track Matte to layer 2 and switch the matte type to Luma (not inverted). Layer 2's visibility switches off automatically.
10. To match the reel's intro timing, start the reveal 2 frames after the photo's first frame (keys at f2 and f49 of the main timeline).
11. Verify against ref_pixel_reveal_0.333.png (f10): about 55% revealed, with the front crossing the image centre on a diagonal. If the front is too clean, raise the Turbulent Noise contrast or try Soft Light. If it is noise-only with no direction, the blending mode is still None/Normal.

## Effects used

- **Gradient Ramp** (`ADBE Ramp`) on Footage (bottom, matte source): Start of Ramp 1.7, -11.4 (first shown -10.5, -11.4 before adjusting); Start Color #000000; End of Ramp 2175.3, 1214.2 (first shown 1922.3, 1074.0); End Color #FFFFFF; Ramp Shape Radial Ramp; Ramp Scatter 0.0; Blend With Original 0.0%
- **Turbulent Noise** (`ADBE AIF Perlin Noise 3D`) on Footage (bottom, matte source): Collapsed at Reset (defaults: Fractal Type Basic, Noise Type Soft Linear, Contrast 100, Brightness 0, Scale 100, Complexity 6, Sub Influence 70%, Sub Scaling 56, Evolution 0, not animated, Opacity 100%). Blending Mode INFERRED = Overlay.
- **Mosaic** (`ADBE Mosaic`) on Footage (bottom, matte source): Horizontal Blocks 55 (default 10 shown first); Vertical Blocks 55; Sharp Colors unchecked
- **Exposure** (`ADBE Exposure2`) on Footage (bottom, matte source): Master > Exposure KEYED: 0:00:00:00 = -2.53, 0:00:01:17 (f47) = 14.29, linear diamonds. Other params at Reset.
- **Posterize** (`ADBE Posterize`) on Footage (bottom, matte source): Level 2
- **Track Matte (layer setting)** (`layer.setTrackMatte(layer2, TrackMatteType.LUMA)`) on Footage (top, fill): Track Matte '2. Footage', Luma, not inverted

## Keyframes

Exposure > Master Exposure on the matte layer: frame 0 = -2.53, frame 47 (0:00:01:17) = 14.29, linear temporal interpolation. A Flow 2.0 panel showing 'cubic-bezier 1.00, -0.00, 1.00, 1.00' was open, but the keyframe icons stayed linear diamonds and the measured front matches linear keys, so do NOT apply that curve. In the reel's intro the same keys sit 2 frames later (f2 to f49 on the main timeline): first block f3-4, centre crossed f10-11, last block f32.

## Expressions

none

## Third-party plug-ins and native stand-ins

None needed: the effect is all native. The screen shows Flow 2.0, EaseCopy, Fast Layers, CompVault, EDITKIT, SuperFlow and TextExploder panels, but none of them is part of the effect.

## What the reel did not show (inferred)

Turbulent Noise was never expanded, so its Blending Mode and other parameters are not visible. With the documented None/Normal at 100% the noise would fully replace the ramp and the reveal would have no direction, but the finished reveal is clearly diagonal, so the preset must blend the noise. A simulation (ramp + fractal noise + 55x55 block mean + linear-light exposure + 0.5 threshold) matches the measured front curve best with Overlay at 100% plus a 2-frame key delay (Soft Light is close; Normal at 20-30% makes the tail far too fast), hence Overlay. The size of the photo layer used in the intro is unknown: the 55 blocks span the 3:2 photo, so the layer is the photo's own size, not 1920x1080, and the ramp values should be scaled by percentage. The Exposure property's internal match name was not shown: use Master > Exposure by name.
