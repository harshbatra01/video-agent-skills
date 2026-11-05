# 17. Essential Graphics Template

Recipe name in the study: "Essential Graphics notification template + variations". Category: technique_demo. Source: a tutorial creator's reel (DaSns3-PXuz). Confidence of the recipe: high.

Native build: `../ae/effects/eg_notification_template_variations.jsx` (function `build_eg_notification_template_variations()`).

## What it looks like

A dark iOS-style notification pill: near-black fill #05070C with a subtle glossy bevel on the right/bottom edge (#2A2D35) and a soft drop shadow; left a rounded-square app icon; title in white Medium ('Messages', a placeholder app name), message below in grey #8A8F99 ('4+ new messages'), 'now.' in grey at the right. In a 1080x1920 comp it is ~885x228 px (radius ~56, icon ~128 px, title ~62 px, message ~52 px, 'now.' ~40 px). The reel shows it alone, then zooms out (fast, with motion blur) to a white frame holding six instances at ~40 % in a staggered pattern (top-left corners for a 1076x1914 frame: top-centre 362,752; mid-left 119,865; mid-right 606,865; centre 362,972; bottom-left 119,1078; bottom-right 606,1078; each 352x88). All six start identical; at f306-f312 five swap (blur crossfade, ~6 frames) to different apps and messages (e.g. 'Chat / 7 unread messages.', 'Team / Message from X Media.', 'Payments / Payout balance: $10K.', 'Wallet / Received $400...', 'Clips / ...posted a new video.'; the reel showed real app names, replaced here by neutral ones) while the centre one stays; the cluster drifts slowly. Technique: one comp 'UI' with its text Source Text and icon exposed in Window > Essential Graphics (Name 'Notification', Primary 'UI'), nested six times, each instance's Essential Properties edited in the Properties panel instead of duplicating comps.

## Inputs

- 6 small app-icon images or simple placeholder icons (do not use real brand logos; coloured rounded squares with a glyph are fine)
- six title/message text pairs

## Layer stack

Comp 'UI' (1080x1920): 1 T 'now.'; 2 T '4+ new messages'; 3 T 'Messages' (title); 4 icon layers (footage or shape icons; selected by a Dropdown control); 5 shape 'Main container' (rounded rect + Bevel/edge highlight + Drop Shadow). Comp 'Main' (1080x1920): six 'UI' precomp layers arranged in the staggered grid, white bg #FDFDFD, optional camera/null for the zoom-out.

## Steps

1. Build comp 'UI' 1080x1920. 'Main container': rounded rect 885x228, roundness 56, fill #05070C; add a second rect stroke 3 px with a linear gradient or a Bevel Alpha for the glossy right/bottom edge; Drop Shadow black 45 %, distance 18, softness 50.
2. Icon: 128x128 rounded-square layers (one per app variant) at container-left + 40 px, stacked; add a Dropdown Menu Control 'Icon' on a controller (or on the UI comp's top layer) with items Messages/Chat/Team/Payments/Wallet/Clips and set each icon layer's Opacity expression to show only the chosen index.
3. Texts: title SFProDisplay-Medium 62 px #FFFFFF; message SFProDisplay-Regular 52 px #8A8F99; 'now.' SFProDisplay-Regular 40 px #8A8F99 right-aligned 40 px from the right edge.
4. Essential Graphics: comp.openInEssentialGraphics(); add Source Text of title, message and now. with addToMotionGraphicsTemplateAs(comp, 'Title' / 'Message' / 'Time'), and the Dropdown 'Menu' property as 'Icon'. Set the EGP name to 'Notification' (comp.motionGraphicsTemplateName).
5. Comp 'Main': nest 'UI' six times at 40 % scale in the staggered positions (scale the measured 1076-frame coordinates by 1.0037 for 1080x1920).
6. Set each instance's master properties via layer.essentialProperty('Title').setValue(...) etc. For the swap animation, keyframe the Essential Properties with hold keys at the swap frame and add an adjustment layer Gaussian Blur pulse 0 -> 14 -> 0 over 6 frames around it.
7. Zoom-out intro: a single instance at 100 % scaling to 40 % over 6 frames with motion blur, then the five others pop in (scale 80 -> 100 %, opacity 0 -> 100, 4 frames, staggered 2 frames).

## Effects used

- **Drop Shadow** (`ADBE Drop Shadow`) on Main container: Color #000000; Opacity 45 %; Direction 180; Distance 18; Softness 50 (estimated).
- **Bevel Alpha** (`ADBE Bevel Alpha`) on Main container: Edge Thickness 4; Light Angle -45 deg; Light Color white; Light Intensity 0.25 (estimated glossy edge).
- **Dropdown Menu Control** (`ADBE Dropdown Control`) on UI controller: Items Messages, Chat, Team, Payments, Wallet, Clips (substitute for the reel's media-replacement logo property).
- **Gaussian Blur** (`ADBE Gaussian Blur 2`) on swap adjustment: 0 -> 14 -> 0 over 6 frames at the swap.

## Keyframes

Swap at reel f306-f312 (6 frames) with hold keys on Essential Properties; zoom-out f264-f270; drift over the cluster (scale 100 -> 103 % over 2 s).

## Expressions

Icon layer Opacity: (thisComp.layer('Controller').effect('Icon')('Menu').value == INDEX) ? 100 : 0. Read on screen: EGP Name 'Notification', Primary 'UI', properties 'now.', '4+ new messages', 'Messages' (Source Text) and an app-logo PNG (media replacement; the reel used a real app's logo).

## Third-party plug-ins and native stand-ins

None. The reel used a media-replacement footage property for the logo; the Dropdown Menu Control is the script-friendly native substitute.

## What the reel did not show (inferred)

Card fonts look like Inter/SF Pro Medium at small size (not identifiable); bevel and shadow values estimated; the 'Main container' internals (shape fills/effects) were never expanded on screen. Real brand logos should not be reproduced; use placeholders.
