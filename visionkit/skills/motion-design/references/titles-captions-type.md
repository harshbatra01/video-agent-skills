# Titles, captions and type in motion

How type is set and animated, and the title, caption and card recipes our reviewers approved, with every value. The
general caption STYLE for a job (which caption look, chunk sizes, captions on or off) is editing-playbook's call; the
text helpers and font mechanics are in premiere-ae-editing `references/after-effects.md` sections 5-6.

## Contents
1. Rules for all type
2. Animating type: techniques
3. Approved recipes: vertical social ads
4. Approved recipes: premium explainers (16:9)
5. Captions in motion
6. Type and motion on native posts
7. Fonts and licences

## 1. Rules for all type
- **One text helper, one switch.** Route every string through one `txt()` helper with a font map and a premium switch.
  Why: when a reviewer said the type was "too poster ish, we wanted premium [calm]", restyling about 93 shots cost one
  switch plus re-renders. The switch that passed: Montserrat Black becomes Proxima Nova Semibold at 0.92x the size,
  tracking +30 on all-caps and +10 otherwise. Strings with not-equal, arrows, approx, star, tick or times signs go to the
  glyph fallback font (a missing glyph renders BLANK with no error).
- **Real font metrics.** Size plates and pills from the real font file: per-glyph widths plus tracking / 1000 x size per
  gap, cap height from the "H" box. It matched Premiere's layout. For tight fits confirm in After Effects with
  `sourceRectAtTime`: planning widths were up to 20 px off for Inter. A guessed width put words on top of each other.
- **Plan in baselines.** A point text's y is its baseline; capitals sit about 0.72 x size above it. A plan that treats y
  as the centre puts big words a third of their size too high (a 300 px word landed at the top edge).
- **Readable on a phone.** On 1080x1920 a name about 35 px over a dark plate and subtitles about 26 px; nothing under
  about 26 px; 16:9 overlines 56 px and up. Small text gets a plate (dark rounded, about 90%, a thin edge) or dark ink on
  a light card. Why: small white text on footage was rejected ("the white is clashing with the sky"). Labels on light
  coloured backgrounds go dark and big ("bigger and darker"). Small tags went +20% after "make it a biit more visible...
  not a lot just a bit".
- **Mock before you build.** Every title option on graded frames from every location the title will sit on, with the
  real caption at its real place, composited in linear light like Premiere. Check contrast on every background.
- **Never over a face or mouth**, and inside the platform's caption-safe zone. Everything not tied to an on-set prop
  lives in the lower caption zone with one shared bottom gradient, so graphics never clash. On paid Reels and Stories
  ads aim clear of the top ~14% and the bottom ~35% (about 270 and 670 px on 1080x1920) and never go inside the top
  220 px or the bottom 420 px (the smaller margin also quoted, used as the hard limit); organic and native posts keep
  text between about 15% and 65% of the height (section 6). A top-left title can sit under the Reels header and a 4:5
  feed crop cuts it, so for feeds move it to about 250 px from the top. Platform specs: social-video-formats
  `platforms-and-policies.md` section 3.
- **The user's placement is the brief.** They moved titles to the top-left by hand once; that spot then went to every ad.
- **Exact words.** The client's wording for names, badges and axis labels; headlines and quotes word for word; the text
  matches what is said ("WE FORMULATED" was wrong for "reformulated"). Use the brand's own hex, never one sampled from
  another film.
- **Hierarchy (from a typography demo):** sizes step by a 1.25 ratio (38 -> 30.4 -> 24.3 -> 19.5 px); big text can go
  tight, small text needs more space (a small amount set at about -60 was too tight and opened to about +10); lighter
  weights for small text (everything SemiBold looks flat); to focus one element, dim the rest to 38% with 10-frame Easy
  Ease pairs. Demo build: effects-library #18.
- **Tracking units.** A text animator's Tracking Amount is in pixels per character, not thousandths of an em: single
  digits for a subtle settle (150 blew a 28 px line up to 2,370 px wide).
- **Numbers.** Pick a font with lining numerals (After Effects has no figure setting) and fixed-width digits for a clock
  or counter, so numbers do not jitter as they change.

## 2. Animating type: techniques
- **Word by word:** a text animator (Opacity 0, or a rise) with an Expression Selector Based on Words and a per-word
  array of times reproduces a reference exactly. Simpler type-on by words: an Opacity 0 animator with a Range Selector
  Based On Words, Start keyed 0 -> 100 over the read time.
- **Typing:** our route is a Source Text substring expression (`typeOn`, about 18 characters a second). A cheaper route
  for long text: an Opacity animator with `textIndex > effect("typed")(1)` driven by a hold-keyed or two-key linear
  slider (`typed` in scene_lib.jsx). Keep both.
- **Letters rising out of a box:** track-matte the text with a sub-comp that holds the text and a box matte. Reference
  timing: the box appears one frame early, letters rise one frame apart, 6 frames each.
- **Gradient on text:** ours first: Gradient Ramp on the text layer itself fills only the letters, with start and end
  points in the LAYER's own space taken from `sourceRectAtTime`. Fallback when a ramp seems to ignore its points (most
  likely comp coordinates were passed): a comp-size solid with the ramp in comp coordinates, track-matted by the text.
- **Smooth text arrival (clean style captions):** blur 10 -> 0, opacity 0 -> 100, rise 12 px -> 0, two settle keys over
  5 frames (`cap` in scene_lib.jsx; `capRow` in motion_lib.jsx rises 14 px). The hero version (word range selector with
  opacity 0, blur 12 and a colour; two nulls whose eases overlap): effects-library #4.
- **Counters:** a Source Text expression `Math.round(ease(time, a, b, from, to))` plus a suffix, switching to a final
  string after a time (for "20-30"); on all RGB copies so they agree. Colour that follows progress: Fill Color by
  `linear()` on the same eased progress (green -> yellow at 0.55 -> red), and the bar's size from the same progress, so
  number, length and colour never disagree (a meter stayed pale yellow until this). Stepped counters (97, 98, 99 on a
  snare roll): the first segment eased, every later key HOLD, the text from an array of [time, value] steps.
- **Textured type with no plug-in:** Gradient Ramp on the text (layer space), Noise about 14% for grain inside the
  letters, a soft Glow, and an offset copy in a colour behind it that slides out 3% of the size on the slam (printed
  depth).
- **Soft caption glow:** a blurred duplicate of the captions precomp (Gaussian 28, 55% opacity) under the original.
- **Bigger or smaller after the fact:** scale the static value AND every keyframe value with one function; a +20% tag
  shifts its text down by (k - 1) x cap height / 2 and widens the pill keys by the same factor; timing untouched.
- Library builds for type: #3 wave blur text (a word resolves from hexagon bokeh), #4 smooth text transition, #6 cursor
  reveal, #18 typography rules (`effects-library.md`).

## 3. Approved recipes: vertical social ads (1080x1920, 60 fps)
Layout: kicker baseline y 1370, main caption baseline y 1590, a dark bottom gradient from y 980 to below the frame
(feather 420, 74%); info cards top-left (x 40, y 110, w 520); nothing over the face.

**Dynamic caption** ("the animated text which is dynamic looks nice keep it up"). Only on B-roll, with the subtitles under
it disabled.
- Main word: Coolvetica Heavy Comp 236 px fitted to 980 px; gradient white -> grey [0.77, 0.79, 0.82]; Glow (threshold
  60, radius 22, intensity 0.35); shadow (0.55, distance 5, softness 26); blur-in 26 over 0.2 s; scale 128 -> 100% in
  0.24 s (ease 80/20), then a drift to 103.5%; motion blur on.
- RGB split: two copies filled red [1, 0.05, 0.25] and cyan [0, 0.85, 1] in Add, +-22 px sliding in over 0.24 s, opacity
  0 -> 75 -> 0 over 0.3 s.
- Kicker: Proxima Nova Extrabold 54 px, tracking 60, word gap 20, one red word for the negative, rising 26 px in 0.2 s.
- A white flash 0 -> 24% -> 0 over 0.15 s on the cut; a red strike through rejected options.

**Stacked synced words** ("perfect"): one 230 px word per band at y 560 / 960 / 1360, each on its spoken word; the frame
dims to 34% in 0.12 s; a white rule 62% of the word's width x 6 px draws out from the centre 0.12-0.42 s after the word
(every rule white: a green rule inside the white stack was the one note).

**Partial-word roll** for two near-identical words (EFF[ICIENT -> ECTIVE]LY): fixed prefix and suffix; the middle rolls
(old slides up and out, new slides up and in) through two track-matte windows; spacing reproduces each full word's real
width, and the prefix and suffix slide sideways so the word stays centred; 0.24 s ease-in-out, RGB ghosts and a
101.5 -> 106 -> 101.5% punch.

**Frosted glass info card** (after every board-reveal concept was rejected and the user asked for "frost glass ish which
we reveal"): top-left, w 520 at x 40, y 110 (600 px cards covered her face); radius 28; near-black tint 22%; a white sheen
ramp over the top 160 px at 9%; a 1.5 px white edge at 34%; a soft shadow (20%, blur 34); a green tick circle 44 px with a
Trim Paths tick; kicker Proxima Nova Extrabold 30 px, tracking 130, words fading up on her words; main lines Coolvetica
112 px auto-fit; width reveal ease-out 0.38 s, exit ease-in 0.25 s. A definition grows the card in 0.30 s: white Proxima
Semibold 36 px on a 42% black inset panel, word and meaning only (no pronunciation, no "noun"; text on top of the panel,
or it is unreadable under the glass tint). The real blur behind the card is a Premiere adjustment layer (Gaussian Blur 42
under a 4-vertex rectangle mask, feather 2, its size keyed per frame from the geometry the AE build writes). Why: an alpha
overlay cannot blur the footage under it, and baking footage into AE breaks compile-in-Premiere. Not too opaque ("clean
the frostglass stuff... too opaque").

**A meter that "feels finished"**: label and number on top, a 900 px track at y 620, an eased count 1 -> 100x with the colour
going green -> yellow (at 55%) -> red, stopping at the track end on a red 5 x 76 px marker with a label ("MEGA DOSE"); the
number's glow pulses on landing; the whole graphic fades out exactly on the B-roll's last frame. Words: "it going offscreen
looks bad. add a line like in the start as well with some small text below so it feels finished... ease the animation
properly... make it fade as the broll ends".

**Question card** (own design: showing a platform's real UI in an ad needs the platform's permission): a white 900 px card
centred at y 1520, radius 42, a round avatar crop with a red ring, "ASK [NAME]" red 30 px tracking 160, a grey "Your
question" line, the question in 54 px typed on word by word while she reads it; pops 72 -> 104 -> 100% with a -5 deg
settle in 0.3 s; exits by a hard cut or a snap to 0 in the last 0.12 s. Research version: a frosted-glass blur of the shot
behind, a brand-colour header strip, scale 0 -> 106 -> 100% over about 8 frames with a soft shadow.

**Headline card** (only headlines that really ran, word for word): the real screenshot on a white rounded "paper" card; a
3D tilt in (Y -30 -> -7 -> -2 deg, X 9 -> 2 -> 0, scale 90 -> 100 -> 104%); the frame behind dimmed to 42%; the
highlighter = yellow [1, 0.81, 0.23] rounded rects in Multiply at 88% growing left to right over the exact words (rects
from a word map of the screenshot); a hard cut out. It lands on the payoff phrase, not the setup.

**Counters**: year counters (a year rolling back from today to the year of the story; "for 17 years"); spread them around,
never two back to back; land fast, hold, hard cut.

**Lower caption zone** for anything not tied to the on-set board: kicker 52 px red at y 1370, number 270 px at y 1580, unit
52 px at y 1698; the CTA card 120 px lower so its backdrop starts where the caption backdrop starts. Why: "this graphic and
gradient is over her face, do it in centre or down maybe, keep it coherent with other graphics as to not clash".

**CTA end card** (one reusable alpha element, timed to the CTA voice; "only create one for now and re use it"): kicker A
0.12-1.42 s, kicker B from 1.55 s (both 54 px at y 1060); a code pill 920 x 230 at y 1215 (glass 72%, a 3 px gold edge
[0.81, 0.68, 0.39], scaling 86 -> 100% from its centre: a shape that scales needs its anchor at its centre or it grows from
the corner); the code word 190 px at 2.62 s with a white flash; a shine sweep at 2.98 s; "20% OFF" 210 px counting up
3.12-3.82 s in a gold gradient. Ads without a code card get a 5 s CTA segment over product B-roll; a brand sting SFX on the
code.

**Name title** (the approved direction: bold condensed name plus a small gold pill, no box, below the caption line):
- Name in Coolvetica Heavy Comp 118 px, tracking 10, white, shadow (80, 22, 2), baseline y 1128 (just under the caption
  line; on a whiteboard ad above the board at y 360).
- Credential in Proxima Nova Extrabold 30 px, tracking 60, ink 0x141008, inside a gold pill 0xCFAE63 (height = cap + 22,
  width = text + 44, fully rounded).
- Name fades 0 -> 0.28 s, rises 40 px and settles from 106% by 0.5 s; the pill opens from the centre 0.20-0.55 s; the
  credential fades in 0.42-0.62 s and lifts 8 px; all reverse in the last 0.5 s.

**Code card** (plain white text vanished on a light T-shirt and a whiteboard): a dark card 640x206, radius 30, fill
0x0D0D0D, a 2 px stroke 0x5A5A5A, 97% opacity; rises 70 px and scales 92 -> 100% over 0.55 s; "USE CODE" in Proxima Nova
Semibold 25, tracking 350, grey 0xAFAFAF; the code in PowerGrotesk 88, tracking 30; starts on the word "code" and holds to
the end.

**1-of-5 stars** (an alpha element with no background box: "why do they have to have a background"):
- Five outline stars draw on (Trim Paths, white stroke 4, 0.06 s stagger).
- Star 1 fills gold (Gradient Ramp light to dark gold with an animated CC Light Sweep, seen through a star alpha matte) and
  pops 0 -> 118 -> 100% at 0.46 s with an additive blurred glow (Gaussian 34); it lands on the word "star".
- Stars 2-5 flicker gold, fail, dim to 52% and sag 5 px; exit at 3.0 s; comp markers at the SFX beats (ding 0.46, ticks
  0.64, whoosh 3.0).
- Comp 1080x400, 60 fps, 3.6 s; star radius 52, inner 24.4, gap 128, corner round 7.
- Never light all five: that implies a rating nobody can back up.

**Hide the list, reveal each item as it is said** (a "3 things" ad): blur every item on the on-set board under a "?" and
unblur each line on its word (wipes about 0.9-1.3 s); risers can build into each reveal. Why, in the reviewer's words:
"maybe we hide those 3 things first using blur or something with a question mark on top... we wanna keep em hooked". The
"?" is a 360 px heavy condensed glyph over a 300 px halo ellipse blurred 70 at 26% (round, never boxed), with a tiny bob
(sin 7.5 rad/s x 7 px, rotation sin 5.2 x 3 deg). Built in Premiere as an adjustment layer with Gaussian Blur 26 and one
mask per line following a tracker (mechanics: premiere-ae-editing).

**Spotlight instead of a tint highlight** ("this green mask is just bad... it feels cheap"): an adjustment layer with
Lumetri Exposure 0 -> -1 and Saturation 100 -> 76 over 0.2 s plus Gaussian Blur 0 -> 6, under an inverted tracked mask
(feather 60); the lit box grows from 2 lines to 4 on the second "here" (0.2 s). Outside luminance went 0.44 -> 0.30. A
Lumetri used as a dimmer is cloned from a NEUTRAL Lumetri, never from the master grade (a clone of the grade applies the
look twice).

**Idea bank for archive-heavy athlete ads** (research, each matched to a tutorial; check each against the taste file):
headline highlighter, a digital article as a 3D precomp, text behind the subject, 2.5D parallax photo, light leak, a
VHS/CRT archive look, a magazine cover, a then-vs-now split (stacked top and bottom for 9:16), a route line on a map, a race
clock locking on the record time (fixed-width digits), zoom through text, a freeze frame with a "that's me" arrow, a
planar-tracked blur reveal, a counter plus a meter, a dictionary card, an own Q&A card, kinetic type, a polaroid stack, a
flash transition with a shutter sound, a light sweep on the packshot, a speed ramp, text tracked onto the road, an
archive-to-today match cut, an echo trail, an out-of-frame pop, a 3D product end card. (Sticker outlines, marker circles
with boil and film burns were on the list; stickers and wobbly marks were rejected later in other genres.)

## 4. Approved recipes: premium explainers (16:9)
**"Premium calm" type**: a semibold humanist face (Proxima Nova Semibold), slightly smaller, wider tracking on caps,
sentence-case sub lines, thin accent bars, dark ink on light cards, pastel backdrops, one verdict stamp at most. Label spec:
a thin accent bar 56 x 5 px + Proxima Semibold 46 px + an optional Regular sub line at 0.6x, rising 18 px in 0.45 s with a
soft shadow. The client's next notes no longer mentioned type.

**The 3-pillar chapter transition** (the user's own design; brief: "2 diagonal lines seperating 3 diff scenes slightly
blurred with animated text ... the lines move and we zoom into the stuff"):
- Three scene comps split by two slanted lines driven by a control null (sliders L1 640, L2 1280, SLANT 105 px); panels
  masked from comp points and blurred (Box Blur 16 easing to 6 as the screen builds).
- Panels darkened with Exposure -1.2 (done pillars -1.9) plus a dark title band at 55% (120 px feather).
- Lines 10 px white with a glow and a soft shadow, drawn on with Trim Paths in 0.45 s, 0.1 s apart.
- Titles as badges with animated icons instead of 1, 2, 3 (the only note: "preferably all animated a bit"): a "?"
  rocking `8*Math.sin(time*2.6)`, a magnifier orbiting, a "$" doing a coin flip every 2.2 s.
- Go: the lines slide off to per-target positions in 0.8 s; the chosen panel moves to the centre, zooms to 116% (+3%
  drift) and sharpens to 0 blur. Done pillars show a green check and dim to 55%.
- The same three scene comps feed every overview, so it matches every time.

**An exact copy of an earlier graphic** (a score graphic; "use exactly that"): rebuild it from a dump of the old
project, not by eye. The art from the earlier composite with alpha (read its size and centre from the file); the shape
using the original path keys and their times; a fixed order for the items; the size of each step worked out from the
score with a written formula. Step mode: one item grows per step (about 0.45 s) with an icon pop. Labels in the old
face and size, near-black, staying on; widen the comp so long labels fit. Review note to expect: labels "bigger and
darker".

**YouTube end-screen plate**: after the last word the presenter eases over 1 s to 66% size and 134 room px to the left
(feet anchored); the right side darkens with a dark solid (520 px feather) to 40%. Check the frames against the element
zones on 1920x1080: video about x 1050-1810, y 300-730; subscribe about x 1500-1700, y 790-990. 15-20 s after the last
word, presenter and background only. Never add the elements yourself ("just leave space for youtube end elements. dont
manually add them"). The music lifts about 8 dB when the voice stops (Premiere level keys, never baked into the file).

**Graphics kit proposed for a review channel** (partly used): 2 fonts; fixed colours (green = studies back the claim, amber
= mixed, red = no backing); 4 card types (study card, source tag, "what the box says", verdict stamp); numbers as counts of
people ("9 of 30") rather than bare percentages; a small evidence pyramid; study card fields = claim, study type, n,
duration, funder, result in real units, one evidence grade; a radar with at most 2 products and a fixed axis order.

**Patterns that worked:**

| Need | Build |
|---|---|
| article or study proof | the screenshot as a card over a blurred background still, a highlighter on the exact words (OCR rects), a slow push; never crop the words being read |
| claim vs evidence | two cards and one verdict stamp, or a cork investigation board the camera crosses item by item (for that one beat only) |
| product price or spec | the product cut-out on a soft floor with a soft glow, an outline box on the price |
| grade or score | the channel's own scale graphic rebuilt exactly |
| big number | a counter that lands fast and holds, light ticks, a boom on the landing |
| time or dial | a clock face with ticks (60 + 12) that fills to the real number ("make 30 minutes animation fill up to where 30 is on clock") |
| comments or social proof | a rebuilt comment panel, never a real platform's UI without permission |
| labels on white documents | dark plates under pop labels |
| card to card | a match cut: same roll angle, same card size, pins fade |

**Collage techniques** (research, untested): scanned torn-paper PNG mattes beat Roughen Edges; paper texture in Multiply at
20-40%; card jitter with `posterizeTime(8); wiggle(8,1)` on rotation; a highlighter in Multiply at about 75% wiped over
8-12 frames with the rest dimmed to 40%; the paper-cutout explainer look = white outline and drop shadow, 12 fps stepped
motion, paper, shutter and thud sounds as items land.

## 5. Captions in motion
- **No captions while a designed graphic prints the spoken words or numbers** ("captions on top of text doesn't make
  sense"). Keep them over the presenter, footage and documents. When the voice reads text already on screen (a tweet, a
  letter), animate that text instead: a line reveal, dimming, a highlight that follows the words. One reference reel
  captioned only 31% of its spoken words for this reason. In our ads, captions under a graphic are DISABLED, never deleted.
- **Captions live on their own layer**: one captions comp for the whole film, or a native Premiere caption track, never
  inside scene comps, so they change without touching the animation. In Premiere caption tracks draw above all video
  tracks, so a graphic on a video track sits under the captions.
- **On the word:** each word or phrase appears on its first spoken frame and swaps with a hard cut; a word that starts
  within about 0.2 s before a cut appears on the cut.
- **Chunk sizes by look** (references; the style choice is editing-playbook's): news reels 3-4 words (never over 8),
  designed explainers a fixed 2 words locked to word onsets, mini-docs 1-3, desk-style docs build word by word up to
  about 6 then clear, VC cold opens 1-3 serif words blooming in over 3-6 frames. Two speakers get two caption colours.
- **Reading-paced reveals** (text cards, tweets, article highlights): blur what is not read yet; reveal about 0.35 s per
  line (one-liners 0.1-0.3 s); each wipe ends 0.2-0.4 s after its last word; chain reveals within 1 s; the opening wipe
  keeps line 1 readable, and a 2-line first block needs no blur.
- **Soft blur edges on scaled layers:** a mask feather in layer pixels shrinks with the layer, so enforce an on-screen
  minimum (20 px, 14 px for small boxes) and pad the box by at least half the feather. Why: "the blurs arent supposed to
  have a rigid end of them".
- **Slanted text:** boxes follow the text's own four-corner outline; an upright box was "way too big / sloppy".
- **Music posts:** subtitles for speech only, never lyrics; stop them before the song comes in.

## 6. Type and motion on native posts
- **House look** for news and faceless pages: a bold caps headline with coloured numbers, a tweet card over a clip,
  carousels, each client's own accent (one client: #1AFF57, second accent #FF3B30). Not the TikTok white box ("TOOO off
  beat").
- **Numbers in the accent colour**, automatically, on cards, video headlines and every carousel slide; tweet cards stay
  plain like real tweets; names that start with digits are skipped. Why: the number is usually the hook and colour makes it
  read first in a scroll.
- **Headline markup:** `*word*` = accent, `^word^` = second accent (red), 1-3 hook words. Accent by story type: beef,
  court, breaking #FF3B30; charts, money #30D158; throwback, birthday #FF9F0A; a news-brand orange #FF7A00; news #FFD60A.
  Colour tells the story type before the words.
- **Fonts:** a condensed face (Coolvetica) for card headlines only; Proxima Nova Extrabold for video headlines and the split
  caption box (a 5-font A/B on a real video showed the condensed face was hard to read on a phone); Impact for meme headers;
  Helvetica for tweet cards; Bahnschrift for numbers.
- **Page mark** = the page's profile picture + @handle, never a text wordmark; on videos a byline above the headline
  ("write @[page] and stuff instead to show it is a username").
- **Platform logo tile** (a rounded tile, radius 23%) instead of a label pill on platform stories; a logo reads faster.
- **Tweet cards** only for our own accounts; a photo tweet is drawn as a real tweet with the image inside; in videos the
  clip starts just under the card (card bottom + 30 px).
- **Emoji** iPhone-style (an Apple emoji PNG set). Burned-in headlines and hooks: at most one, at the end of the hook,
  never in a brand's closing line (the approved split layout's caption box is the exception: a fire and "!!"). Post
  captions carry 1 to 2.
- **Native text rules** (our 22 videos against 49 no-face references: readable words at once 10.5 vs 4; tiny words 27 vs
  0; text centre at 26% vs 50% of the height): 4-9 readable words at a time, nothing tiny; text mid-screen inside x 120-918
  and y 270-1250; cover text inside the central 1080x1350 band (the profile grid crops to 3:4); at most 2 text sizes,
  nothing under 40 px, nothing in the bottom 20% or the right 160 px; sources and risk lines in the post caption; no text
  on a real app's chart, logo or buttons.
- **Reel safe zone:** headline and face between about 15% and 65% of the height (grid crop at the top and bottom, app
  buttons on the right and bottom).
- **Reading speed:** on-screen text at about 15 characters a second (20 at most), at least 1.5 s; headlines 6-10 words,
  front-loaded; the headline fully on screen from frame 0 (no fade, no logo intro).
- **Real movement only:** motion comes from the footage or a live price line; 5-10% punch-ins on the number or the goal;
  hard cuts; something real moves in the first second; no 3D flips, no counting numbers, no slide-ins or wipes. Pick one of
  two native rhythms: one continuous shot with one line (memes, fan moments, screen recordings) or 3+ hard cuts per 10 s on
  the beat (edits). Our videos sat in between, "the worst of both".
- **Frame 0 is the cover:** every number on it is final and true, never mid-count; motion renders start 0.5 s in.
- **Show a number the way the audience sees it:** the real app screen (a recording, a crop or filmed on a phone) or one
  number in the text. Never a designed % card, gauge, bar, race or weather icon.
- **Borrowed 16:9 clips** can sit letterboxed on a black 9:16 canvas with the hook in the black space. A title card wider
  than the portrait frame goes full width on a blurred backdrop (keep its 4:3) instead of a crop that cuts its words.
- **Timing rules for data explainers** (for other clients; the rejected posts failed on their designed look, not on this
  timing): the 2-second test (freeze frame 0 and frame 60: a stranger can name the subject, the number and why it
  matters); frame 0 shows the subject and the number; one idea per scene, 2-4 s, at most 4 things on screen; a hero number
  at least 150 px, held still at least 0.5 s after it lands; text hold in seconds = max(1.0, 0.4 + 0.33 x words); a
  headline at most 7 words, 42 characters a line, 2 lines; the number reacts within 1-2 frames of the event; impact = a
  2-3 frame flash + a decaying 8-12 frame shake + a 105-112% punch in 4-6 frames + a hit sound, at most 2 per video; frame
  grid at 30 fps: tiny 4-6, normal 8-12, big 15-20, reveal 24-36 frames.
- Cards and overlays for posts are HTML templates rendered by headless Chrome: the pipeline is production-automation's.

## 7. Fonts and licences
- SF Pro is Apple's font and its licence is written for designing Apple-platform interfaces. For client videos prefer
  Inter (free, SIL Open Font Licence). A clean-style reviewer liked SF Pro Display (Bold for key words, Medium for small
  words, one size, white with a soft shadow); our house looks win, and the licence looks wrong for video.
- Fonts in our approved work that need their own licence on a new machine: Coolvetica Heavy Comp (check its licence for
  client work), Proxima Nova (Adobe Fonts), Galano Grotesque, PowerGrotesk.
- Font names per machine, glyph gaps (Proxima Nova has no check mark, arrows, approx, star or not-equal) and the glyph
  fallback font (Segoe UI Semibold on Windows, Arial Unicode MS on a Mac): premiere-ae-editing after-effects.md section 6.
- Premiere only sees fonts installed before it launched; a variable font may need its instance name (Inter-SemiBold).
