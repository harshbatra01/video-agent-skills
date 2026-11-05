# Depth: 2.5D and 3D moves

How to give stills and graphics depth and life without fake motion: the 2.5D room rig with its maths, presenter
compositing, gentle camera values, tracking without a 3D camera, 3D tilts in graphics and 3D renders from collaborators.
Rig scripting and keying mechanics: premiere-ae-editing `references/after-effects.md` sections 7-8.

## Contents
1. Life on stills: camera moves, never fake breathing
2. The 2.5D room rig (exact for planes)
3. The presenter in the rig
4. Poses and swaps
5. Camera values that passed
6. Tracking shots without a 3D camera, and parenting rules
7. 3D tilts and depth in graphics
8. 3D renders from collaborators
9. Depth maps
10. Render cost
11. Not built yet

## 1. Life on stills: camera moves, never fake breathing
- A still feels alive through a camera move (push-in, 2.5D depth planes, drift), word-timed pose swaps, a contact shadow,
  light wrap, a colour match and grain. Never fake breathing or body sway on a cut-out. Why, in the user's words:
  "breathing maybe would also look bad right now as its an image would look too ai". Offer breathing only as an
  off-by-default option if ever.
- New poses, blinks and lip-sync are the user's job with his own AI tools, not Claude's, unless he asks.
- When asked "can you do this?": split the answer into what can be done by script (cut-outs, room layers, camera drift,
  shadow, light wrap, colour match, grain, pose swaps, push-ins), what needs the user (new poses by AI, lip-sync, hand fixes
  on edges), then offer a small test from existing assets only. The 9 s test got its verdict before a whole video used it.

## 2. The 2.5D room rig (exact for planes)
- Cut the room image into planes along its measured floor lines (back wall, side wall, floor, window), 3 px overlap,
  4x-supersampled masks. Extend the window view past the glass with Content-Aware Fill so the frame can slide over it.
- Every layer has an inverse depth w; z = 1/w. Per plane w = A*X + B*Y + C. Example room: floor w = (Y - 550) / 672 with the
  horizon at y 550; the walls from the floor-line slopes (+0.188 and -0.231 through the corner at 757, 1222); the window
  plane w = 0.1.
- Screen mapping for a camera truck T, V and dolly D: x' = cx + ((x - cx) * z - T) / (z - D), and the same for y with V.
- Room planes: Corner Pin expressions on all 4 corners. The presenter and her shadow: position and scale (100 * z / (z - D))
  at their own depth (presenter w 1.9, the shadow on the wall w 1.05).
- One CAM null with 3 sliders (Truck X, Truck Y, Dolly %) drives everything. Check the last frame for gaps at the plane
  seams (none at these values).
- Planes come from one room image measured once; the generator writes the plane file and the rig per shot. The build
  mechanics are in premiere-ae-editing `references/after-effects.md` section 8.

## 3. The presenter in the rig
The approved values live here (premiere-ae-editing after-effects.md section 8 points to this section for them).
- POSES comp: word-timed swaps with a 2-frame dissolve.
- EDGE matte: white-filled poses minus a blurred black-filled copy (Box Blur 16).
- LIGHT WRAP: the room blurred 34 px, luma-matted by the edge, Screen 70%.
- SHADOW: the poses filled [0.12, 0.06, 0.03], Box Blur 26, Multiply 40%, offset (85, -14) room px on the wall. It read as
  "very subtle" in the test: right.
- Sit the cut-out into a warm room: Levels Output Black 6/255 and Gamma 0.96 on the presenter; Tint black [0.16, 0.08, 0.05]
  to white [1, 0.86, 0.72] at 12%; the room plate under Camera Lens Blur 7; the window plane Box Blur 5; grain = Noise 2.0 on
  a top adjustment layer.
- Colour-match a new still to the approved ones by numbers on opaque pixels only (alpha above 250), whole figure and a face
  band (12-36% of the height): linear luminance mean, L* spread, chroma, mean a* and b*; target = the mean of 3 reference
  poses; render about 6 Lumetri candidates and keep the closest. Mask the stats to the cut-out: a dropped alpha let the
  black background into the averages and every candidate read darker.

## 4. Poses and swaps
- Every pose comes from one master image at the same size and framing; a softer pose with different arms and papers made
  swaps "jump a little".
- Pose metrics per still: w, h, top (first opaque row), torso centre x, head centre x. Anchor each pose at its torso centre
  bottom and scale by one common target height over h (1455 / h on that job) so heads line up across swaps. When new stills are pixel-aligned with the old ones,
  only the cut-out folder changes: no timing or position edits.
- The presenter is the channel's visual anchor: one approved still set and wardrobe everywhere, never mixed versions.
- Keep presenter poses as single Premiere bin items used many times (build-in-Premiere rule): a wardrobe change baked into
  17 renders meant 17 re-renders.

## 5. Camera values that passed
- In video shots: Truck X +10 -> -10 px, Dolly 0 -> 2% over a shot.
- The first test used Truck X +20 -> -20 px and Dolly 0 -> 3.5% over 9 s with swaps, shadow and wrap all moving: "cool cool
  this works, just not this many movements together lol". Gentle wins; one movement at a time.
- Push-in rates for stills and presenters: `motion-rules.md` section 9.

## 6. Tracking shots without a 3D camera, and parenting rules
- Parent every world layer to a null whose position is `head - f(progress) * zoom`: the subject (the head of a rising line, a
  card) stays at a fixed screen point while the world moves. A control null with sliders (Progress, Head X / Y, Zoom) drives
  it. Why: cheap, editable, and the camera follows the action from a stable view (a 3D chase angle was rejected: "dont
  change angle like that").
- Parent children to a null BEFORE keyframing the null: parenting compensates for the parent's value at the current time, so a
  null keyed to start off-screen leaves every child offset forever. If the parent's scale is not 100% at t = 0, reset the
  child's scale and position after setting the parent.
- Parenting passes transforms, not opacity: child text that should fade with its card needs
  `thisLayer.parent.transform.opacity` in its opacity.
- A comp motion blur shutter of 60 degrees kept a fast tracking shot readable.
- Two nulls in a chain make overlapping moves easy (the smooth text transition: Null 10 brings the line in with a fast start
  and long settle; Null 11, keyed to start during Null 10's tail, pushes the whole group on a skewed bell).
- `toComp()` on a 3D layer returns [x, y, depth]: use x and y.

## 7. 3D tilts and depth in graphics
- Headline card: a 3D tilt in (Y -30 -> -7 -> -2 deg, X 9 -> 2 -> 0, scale 90 -> 100 -> 104%) over the dimmed frame.
- A notification cluster (library #17): the variations land with a small 3D tilt (X 16, Y -11 deg to 0 over 5 frames) and
  motion blur after a pull-back from one card to six (98 -> 44%, the speed peaking on the cut).
- A digital article as a 3D precomp, 3D polaroids with a camera push and depth of field (idea bank, untested).
- Shallow depth of field bands: blurred adjustment layers masked to the top and bottom with feather (`dofBands` in
  scene_lib.jsx).
- Number or word behind a subject (the cut-out in front, the type behind): `cracked-edits.md` section 7.1; a numeral
  sandwich adds a third depth layer (section 8).

## 8. 3D renders from collaborators
- Real 3D renders beat drawings and cartoon stand-ins (a drawn mouse got "this is ASSS"; the renders replaced it).
- Key green-screen renders, retime them so the hit lands on the word (a whip on "But inside", a laser on "laser", a device
  lineup at 2x), put a soft glow behind, nothing else on top. Mechanics: after-effects.md section 7.
- Brief the 3D artist: transparency instead of green screen, 30 fps (or 29.97) instead of 24, 4K if possible.
- Every 2D stand-in for a missing 3D shot is tagged "PLACEHOLDER" on screen and listed with exact timecodes for the artist,
  so a stand-in never ships by accident.

## 9. Depth maps
- Gradient Depth Reveal (library #7): pastel colour bands flow through a depth map (Colorama, or CC Toner sampling a looping
  palette by expression), then the clip reveals nearest first through Gradient Wipe with the depth map as its gradient,
  softness 100%. Taste: about 1 s of pure colour bands is a colour flood and a long abstract hold; only with the colour
  phase under 10 frames.
- No depth video: fake one from a vertical Gradient Ramp plus the clip's blurred luminance in Overlay, with Curves pushing the
  sky to black and the foreground to white.
- Depth-map strobe or fog for music edits (1-2 frames of a grey depth map on the snare) needs a free depth model and the
  user's OK to install.

## 10. Render cost
- Graphic and card shots render in seconds; rig shots are slow (lens blur on a 2528 x 1684 room): 3 presenter shots took
  about 6.5 min, a 26.8 s end shot 518 s (447 MB ProRes), all 17 presenter shots about 45 min, a 10:38 H.264 preview about
  20 min. Decide the re-render scope by shot type, and build so a presenter change is a Premiere relink, not a re-render.
- Fast Box Blur is far lighter than Camera Lens Blur on big precomps; precompose static parts.

## 11. Not built yet
- A 3D extruded word behind the subject (Blender is installed on the build PC), a world swap behind the cut-out for 0.5-1 s
  per drop, glass shatter, a material strobe (only the cut-out turns halftone for 2-3 frames).
