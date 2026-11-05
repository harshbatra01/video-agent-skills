# Reference house style: blurs, crops and cut timing

One client's narrated meme compilations (5 jobs, 29 Sep to 13 Oct 2026). Every line here is a correction that was
made at least once: by the client's own human editor (their finished projects), by the reviewer fixing delivered
projects himself (he changed 62 of 64 memes on one job and 129 of 169 on another, and his saves were diffed against
the delivered files), and by the client's notes. Where two reviews disagreed, the newer one wins and is written here.
A new client's brief wins over all of it; keep the numbers as starting points.

## Contents
1. Timeline and sizing
2. Blurs: wipes, boxes, curse words, feathers
3. Crops
4. Cut timing on the narrator's voice
5. Narrator behaviour to handle
6. Delivery

## 1. Timeline and sizing

- Premiere Pro only (2025 on the reference jobs), no After Effects. Long-form 16:9 compilations (not the client's Shorts).
- **V1**: the raw screen recording (the narrator reads memes in a Drive preview), silence-cut. **A1**: its audio with
  **+15 dB clip gain** (Gain value 5.6234130859375). Why: the raw voice sits low; the editor uses +15 dB on every clip.
  On most recordings the voice is on the RIGHT channel only (all three audio streams identical): put "Fill Left with
  Right" on every voice clip. Check each recording; one had voice on both.
- **V2**: a full-length **grey** background (Color Matte or PNG, RGB 125 in the editor's project, RGB 100 in others).
  Never white: the reviewer put Contrast -100 on a white background in the first test.
- **V3**: the clean meme files synced to the voice. No transitions.
- **Size**: the visible (post-crop) meme about 980 px tall (he lands on 966 to 984), its top edge about 50 to 58 px from
  the frame top, at most 1740 px wide, centred. Rescale after every re-crop.
- 4 or 5 shouted clips need their gain trimmed below +15 dB so they do not clip (patch_full.py caps each clip's peak at
  -0.5 dBFS).
- Video memes: keep their speed changes (a 6.2x speed-up was accepted); VP9-in-MP4 files must become H.264 first.

## 2. Blurs: wipes, boxes, curse words, feathers

The idea: text the narrator has not read yet is blurred and is revealed as he reads it. Why: the viewer reads along
with him instead of ahead of him.

### Presets
- The client editor's presets: a base wipe (Gaussian 40, wipe), a small box (Gaussian 40 to 0, box) and a small curse
  blur (Gaussian 100, static).
- The reviewer's own: Gaussian 29 with mask feather 10 for wipes, snaps and curse words, plus crop presets (normal,
  big meme T41 / B43, bottom 3.46% for one meme site's bar) and a drop shadow. For masks he adds himself he uses the
  2.75 s-style snap for one-liners and the 1.5 s-style wipe for blocks.
- His Premiere 2026 presets use a third-party blur (FilmImpact Impact Blur); where it is missing, use Gaussian Blur.
- Name each effect instance after the client's own preset (`NAMES` in patch_full.py / patch_pass.py) so their editor
  recognises every blur in Effect Controls.

### The opening wipe
- When the meme opens with a text block, the first text line stays visible and the rest of the opening text is wiped
  (the mask's top edge slides down to the bottom with two keys as he reads). Why: line 1 is the hook; the rest would be
  read ahead.
- **No blur on a 2-line first block** (he deleted all 13 of them on one job and re-added none on the next).
- If the first line is a separate title ("Shark fact:"), wipe the whole paragraph under it, including that paragraph's
  first line.
- The wipe box covers the text lines only, not a flair tag under them.
- **First key**: at the meme's start when he starts reading straight away; if he comments first, when he starts reading
  that block.
- **End key**: about 0.2 to 0.4 s after the last word ends (not on the transcript's word end, which runs early). If the
  next reveal follows within about 1 s, end exactly where it starts so the two chain. Never let a wipe run into the
  next phrase.
- A line that starts "word:" inside a sentence is not a speaker label ("...whoever / you are: you have improved..."); it
  is a speaker turn only when the line above ends a sentence or is a short name line.

### Later blocks and boxes
- Blocks of 3+ lines that he reads or reacts to for about 3 s or more get a wipe, even when centred.
- **One box per caption or label, covering all its lines** (he merged split 2-line pairs; each 2-line grid label is one
  unit).
- **Ramp length** (how long a box takes to clear): a one-line punchline label or caption 0.1 to 0.3 s (keys 31 to 0);
  one-word replies 4 to 7 frames; a multi-line comment about 0.35 s per line (0.7 to 1.1 s for 2 to 3 lines, up to
  about 2.2 s for a long comment read slowly). Why: the reveal should match reading speed.
- **A box covers only what is being revealed**: leave the commenter's name and time line visible, and a meme format's
  fixed label ("you receive:"); never cover the "Like · Reply" row.
- **Reveal everything he reads aloud**: captions, chart labels, speech bubbles, a search query inside a video meme.
  Transcription mishears short labels, so match them loosely, and align repeated label text by the word that differs.
- Dialogue memes: one snap per turn. Quote tweets: he reads the top comment last, so reveal bottom-up as he reads.
- One-word punchline replies ("F", "m") need a manual box.

### Curse words
- **Blur anything that goes against YouTube guidelines**, mild ones included: crap, deadass, damn / hell-type
  profanity, f-words, s-words, b-words, ass, tf, mfs, slurs, sexual terms, and sensitive words like suicide or
  executed; usernames that contain them too. Words that only look edgy (prison) stay. The client's editor
  under-blurred: do not copy that. Words the narrator self-censors aloud (he says "awful" for a swear) still get
  blurred in the image. Why: the channel's monetisation depends on it.
- When a word is blurred only because it is on the policy list (murder, NAKED in "STARK NAKED"), flag it in the report.
- **Tight boxes**: hug the letters (about 4 to 5 image px around the word in the editor's files), at least 5 image px
  of padding so the letters sit under the full-strength part, no neighbouring-line ascenders, no trailing punctuation
  (tightbox.py measures the real letters).
- **Not harsh**: the client said curse blurs were "too aggressive" when they showed as flat boxes with hard edges.
  Gaussian 100 static with feather 10 (the editor's setup); if 100 still reads as a blank box, use the lighter Gaussian
  29, feather 10.

### Feathers (latest rule, 13 Oct 2026)
- Client: "the blurs arent supposed to have a rigid end of them, it should be soft". Every mask in the editor's
  projects and in the reviewer's presets uses **Mask Feather 10 (in the image's own pixels), Expansion 0, Repeat Edge
  Pixels on**. Feather is in layer pixels, so it scales with the meme.
- **Also never under 20 px on screen** (14 px for curse boxes): on big phone screenshots shown at 40 to 90%, a flat 10
  image px is only 4 to 9 px on screen and a half-revealed line looks sliced. Feather = max(10, 20 / scale) for wipes
  and boxes, max(10, 14 / scale) for curses, with padding of at least half the feather so letters stay covered.
  (plan_pass.py follows this; build_full_edl.py still has the Oct 4 cap and needs the same change.)

### Boxes on text inside photos
- A reveal box on text in a photo hugs the text. On slanted text (a shop sign) the box follows the text's own
  four-corner outline, padded slightly; an upright box over a slanted sign covered 50% x 23% of the image and was called
  "way too big / sloppy".

## 3. Crops

### Crop as little as possible
The reviewer: "overall pattern im noticing is just an overuse of crops. most memes probably dont require any
cropping". v1 cropped 74 of 171 memes, v2 cropped 19. No crop by default. Crop only for:
- phone app bars and status bars, "< Thread" bars, search headers;
- footers and metadata rows ("Twitter for iPhone", timestamps, news-source rows, "Posted in r/... by u/...", "Made
  with ...", "Show replies", "7 replies ›", unread replies at the bottom);
- watermarks (below) and reposter headers (a meme page's name and post time above the meme; the tweet author's own name
  and handle stay);
- rows cut in half at an edge, unless he reads them.
Thin frames and borders stay (trimming one white border off one side looked like a "random crop"). Dark frames stay
(demotivational posters).

### Balance the white space
"maintain balance with the white space": where a crop edge sits in a margin, the white space on the two sides of the
text should match. Caption above a photo: the margin above the caption equals the gap between caption and photo. Text
panel edge to edge: equal top and bottom margins. Side trims: none, or the same on both sides. Never add a crop just to
balance a meme that has none.

### Too much white space: tighten
A plain light margin of 10% or more of the image gets tightened to about 3.5% of the short side ("see how ive tighted
this meme"). His example: crop L7.3 / T5.6 / R6.5 / B10.7 on a 460x360 image with 46 to 53 px margins, leaving 12 to 16
px at the sides and the top margin equal to the caption-photo gap. Exceptions: next to text keep about one line height
and match the other side; a pale card or panel is content (never cut its edges); a drawing floating in its own white
panel keeps its margin. On tall memes he trims wide white sides for the look alone.

### Watermarks
- A short line (1 to 4 words) he never reads, alone at the very top or bottom edge on plain background, is a
  watermark: crop it off and trim the outer padding to the card evenly (about 1 to 2% of the height above and below).
- A meme site's bar (a near-black strip with a yellow logo on the right): detect it from pixels (OCR misreads the
  logo) and crop exactly the bar (1.48% of the height on one meme; his preset is 3.46%).
- A watermark printed on the picture (a meme-maker's name in a corner): cut a thin strip right above it. Never cut
  halfway to the previous text line: that rule once cut 44% off a meme because a photo sat between the caption and the
  watermark (his fix was a 4.55% bottom crop).

### Edges cut properly (13 Oct 2026)
- Unread panels at the bottom of a stacked meme come off (an ad panel and reaction faces under two read panels: Crop
  Bottom 50% exactly at the top of the unread panel, then rescale). Only cut at a flat-coloured panel edge with unread
  text, below every line he reads, and only when it removes 15% or more. A photo under a caption is never cut this way.
- Carousel dots on phone screenshots (3 to 6 equal dots on a dark pill near the bottom centre) come off: crop above the
  pill and rescale. Phone screenshots only (the rule fired on movie posters until it was limited).

### Never cut into content
- Side trims of 1 to 2.5% clipped the first letter of every line on tight screenshots; he undid 15 of them.
- Do not cut into a photo, a second photo, the bottom of a comment and its reaction row, or a caption he reads.
- **Matching reaction rows**: if a reaction row ("4d Reply ♥24.5K") shows near the top of the crop, keep the bottom one
  too ("if there is reaction on top keep it in the bottom as well if its there so visually it looks good"); the
  "View N replies" link below it still goes. A lone bottom "Like · Reply" row can go.
- Side trims are only for black pillarbox bars of 5%+ on both sides, the same amount off each.
- Phone screenshots: keep the whole post (caption plus the photo or photos under it, and any image attached to a
  comment). Tweet "time · date · Views" rows and the engagement row are optional.

## 4. Cut timing on the narrator's voice

- **Never cut before he finishes a word.** Take phrase edges from the audio; transcript word times run up to 0.5 s off.
- **Handles**: keep a word's soft tail down to about -70 dB on the raw recording (before the +15 dB gain), cut within 1
  to 3 frames; starts 1 to 2 frames before the first frame at -70 dB or louder, ends about 3 (at most 5) frames after the
  last. -72 to -80 dB is room noise. Why an absolute level: a relative threshold (floor + 12 dB) treated room noise as
  speech.
- Inside the last word, a bump after a short silence is the final consonant: keep it. A soft bump after the words with
  a peak under -55 dB is a breath: cut it. Breaths are cut at both ends even at -58 to -70 dB.
- Before every build, scan every cut for an edge where the audio is louder than -55 dB on both sides; it must find
  nothing (`cut_qc.py`).
- Remove dead air, including pauses inside a question and its answer.
- Cut false starts, restarts (transcribe each phrase on its own to catch them), the first copy of a repeated word at a
  join (with a 4-frame audio crossfade) and clear mumbles; keep ordinary short comments (about 150 were kept on one job).
- Check short transcript pieces before cutting them: a piece glued to a kept phrase is often the rest of its last word.
- Click and peak scan the padding: a mouse click once sat inside a cut's padding.

## 5. Narrator behaviour to handle

- He leaves instructions for the editor in the recording ("use the HQ copy", "remove the read reply part", "put a black
  square over" a word): do what he asks and cut the instruction. A black square = a Tint black box with a mask.
- He abandons some memes mid-sentence: cut those reads and leave the file unused (list unused files in the report).
- He sometimes reads memes off-screen (toolbar hidden, or the screen frozen on one file for minutes): identify memes by
  matching his words against every image's OCR, not only the title bar.
- He flips back to a meme to add a comment: move that phrase back to its meme.
- OCR quirks to plan for: "1 can" for "I can", "Imao" for "lmao", odd spaces in screenshot file names, abbreviations
  (ppl, u, w/) that break line matching until mapped.

## 6. Delivery

- Build into a NEW project file next to the client's files ("<job> edit.prproj", then "v2"); keep the client's or the
  human editor's project untouched; no "Claude" in any name.
- Leave it open in Premiere for review; do not export unless asked.
- Before handing over, copy the delivered project into the build folder as `delivered_baseline.prproj` (he edits in
  place). Keep backups out of the client folder.
- Report: counts (memes, cuts, masks by type, crops), unused files and why, policy-only curse blurs, open calls (a long
  aside kept or cut, a username not blurred), anything not checked.
- When he sends fixes, diff his save against the baseline (review_tools) and add each correction to these rules and to
  the code defaults.

Source: adapted from a friend's Mac skill set (Oct 2026)
