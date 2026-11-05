# 18. Typography Rules

Recipe name in the study: "Dark fintech 'Accounts' card with typography state changes and focus-dim". Category: ui. Source: a tutorial creator's reel (DbBHl9XPUvz). Confidence of the recipe: high.

Native build: `../ae/effects/ui_accounts_card_typography.jsx` (function `build_ui_accounts_card_typography()`).

## What it looks like

White #FDFDFD frame. Card 764x478 (71 % of width) at x156-920 y717-1195, radius ~70, fill #030509; inner panel inset 28 px, from y828 to ~1166, radius ~45, fill #121418 with a 1 px lighter top rim #17191C. Contents (Inter): 'Accounts' white ~32 px (x216); 'Total' #9EA0A4 ~26 px; '$4,237.23' white SemiBold ~38 px; 'last 30 days' #999B9F ~20 px right-aligned at x863; hairline divider; rows with 52x52 dark icon tiles (radius 12; yellow diamond mark, blue P mark), 'Crypto' / 'Payments' (neutral names; the reel showed two real brands) white SemiBold ~30 px at x292, amounts '$2,237.23' / '$2,000' right-aligned at x859. Header label above the card ('Letter Spacing' / 'Size' / 'Weight') black Inter Regular ~90 px, left x~300; black caption under the card ~115 px centred, baseline y~1360. States: (a) focus-dim: the discussed element stays #FFFFFF, all others drop to ~38 % (#5A5D60-#67696D; labels #434549), 10-frame Easy Ease; (b) letter spacing: big balance tracking tightens ('$ 4,237.23' -> '$4,237.23') while highlighted; small '$2,237.23' shown too tight (~-60) then opened to ~+10; (c) size: modular scale /1.25 (38 -> 30.4 -> 24.3 -> 19.5 px); (d) weight: all SemiBold looks flat, then small text set lighter (Medium/Regular). Also a 'broken' variant: outer #172274 navy, inner #707070 grey, crushed tracking (~-80), used with 'BREAK YOUR DESIGN'. The card enters rising from ~+80 px with vertical motion blur in ~10 frames and drifts slowly.

## Inputs

- no footage needed; two small brand-neutral icon glyphs (diamond, letter P)

## Layer stack

Comp ACCOUNTS_CARD 1076x1914: [1] CAPTION text | [2] HEADER text | [3] CARD_NULL parent: [4] TXT_* text layers (Accounts, Total, Balance, Last30, Name1, Amt1, Name2, Amt2) each with a 'Focus' opacity control | [5] ICON tiles | [6] DIVIDER shape | [7] INNER shape | [8] OUTER shape | [9] BG #FDFDFD. Optional: a CONTROL null with Dropdown/Slider 'Focus' and Sliders 'TrackBig', 'TrackSmall'.

## Steps

1. Build OUTER rect 764x478 roundness 70 #030509 and INNER rect 708x338 roundness 45 #121418 (top offset 111 px) with a 1 px #17191C stroke at 50 %.
2. Add the text layers with the sizes/colours above (scale ratio 1.25 between tiers).
3. Icon tiles: rect 52x52 roundness 12 #050608; simple diamond mark (#F0B90B-like yellow) and 'P' mark (#1C7FE0) as neutral glyphs.
4. Focus-dim: per text layer opacity keyframes 100 -> 38 (or expression on a Focus slider), 10-frame Easy Ease.
5. Letter spacing: Text Animator 'Tracking Amount' on Balance (0 -> -40) and on Amt1 (-60 -> +10), 10-frame Easy Ease at the VO cue.
6. Weight beat: hold-key swap of font style (SemiBold -> Medium) on the 4 small layers, with a 2-frame blur pop.
7. Header label swaps (Letter Spacing -> Size -> Weight) using blur_rise_swap_transition; caption phrases hard-swap with a 2-frame blur pop.
8. Card entry: CARD_NULL y +80 -> 0 over 10 frames (ease-out), Directional Blur Direction 0 length 30 -> 0 over 6 frames, opacity 0 -> 100 over 4 frames.
9. Broken variant: duplicate card, OUTER #172274, INNER #707070, tracking -80, swap with a 3-frame vertical blur smear.

## Effects used

- **Directional Blur** (`ADBE Motion Blur`) on CARD_NULL children (adjustment above card): Direction 0 deg (vertical), Blur Length 30 -> 0 over 6 frames on entry
- **Slider Control** (`ADBE Slider Control`) on CONTROL null: 'Focus' index 0-8; 'TrackBig'; 'TrackSmall'
- **Gaussian Blur** (`ADBE Gaussian Blur 2`) on CAPTION / swaps: Blurriness 10 -> 0 over 2 frames when a caption/state swaps

## Keyframes

Original AE timeline: Easy Ease keyframe pairs 10 frames apart (e.g. 23:17f -> 23:27f) on many layers for every state change. Reel cues: focus big balance 13.0 s, small amount 16.0 s, tracking open 19.0-21.0 s, size 23-26 s, weight 34-38 s.

## Expressions

Opacity on each TXT layer (give each a unique index i): var f = thisComp.layer('CONTROL').effect('Focus')('Slider'); var i = 3; (f < 0.5) ? 100 : (Math.abs(f - i) < 0.5 ? 100 : 38);  (keyframe Focus with hold keys and add smoothing via valueAtTime averaging, or simply keyframe opacities with 10-frame Easy Ease as the original did).

## Third-party plug-ins and native stand-ins

Original used BOUNCr and EaseCopy panels (workflow helpers only; not needed)

## What the reel did not show (inferred)

Exact tracking values in reel-scale are inferred from glyph spacing; the only read value is tracking -44 / size 298 -> 238.4 px / leading 225 px on the AE layer 'Total 3' in a much larger comp. Brand logos replaced with neutral glyphs on purpose.
