# 08 Red team: a skeptical stranger scrolling Instagram and X on a phone

Version 2 (final), 07:53 UTC. Inputs read: BRIEF.md, research/dhruvxr/STUDY.md (sections 1, 4, 6 ATN, 7, 8, 9), 05_RULE_BOOK.md (v2, 07:52), 06_SCRIPTS.md (script 1 as read at 07:50; scripts 2 and 3 were "in progress" then and are NOT reviewed here). I did not edit 05 or 06.

How this was done: Claude cannot watch or hear. Every objection is judged from the study's measured numbers. Phone sizes are estimates, not measured on a device.
Severity: 3 = the stranger skips, is confused, or there is a rights risk; fix before anything else. 2 = it weakens the piece. 1 = polish.
Why codes: SKIP (gone in 1 s), CONF (confusion), AD (reads as an ad), COPY (reads as a copy of dhruvxr), RIGHTS, DARK (too dark or small on a phone), MSG (unclear message).

Phone math used below (judged): a 16:9 video in a phone feed is about 330 to 360 pt wide, so about 190 to 200 pt tall. 2.2% ink height is then about 4 pt; 4.6% is about 9 pt. Normal phone body text has a cap height of about 12 pt.

## A. STUDY.md section 9, item by item

| S9 # | Item | Stranger says | Why | Sev | Fix |
|---|---|---|---|---|---|
| 1 | 16:9, 15 to 16.5 s, 30 fps | "On Instagram it's a thin strip in the middle of my screen. I can't read it." | DARK, SKIP | 2 | Keep 16:9 as the X master. Make a separate 4:5 (1080x1350) Instagram layout, not a crop: a crop keeps only 45% of the width and cuts ATN-style split lines. |
| 2 | Black monochrome base, mean 0.14 to 0.25 | "Black box in my feed. Did it load?" | DARK, SKIP | 3 | Frame 0 must not be black and must show the hook line. No black frame before 5 s except one planned cut. Keep the dark base after the hook. |
| 3 | First-second burst, 8 to 9 shots of 1 to 4 f | "Flashing noise. I can't tell what anything is." Also: can trigger photosensitive viewers. | CONF, SKIP | 3 | Keep the burst, but pin one fixed text line on top through all of it (images change, the line does not move). Keep the swapped images at similar brightness: no full-frame black-to-white swaps. Run a flash check: no more than 3 large bright flashes in any 1 s (WCAG 2.3.1 general flash rule). |
| 4 | One card per hold, 0.9 to 2.4 s, second burst | ATN has a stretch with no text at f67 to f121, 2.24 to 4.04 s: "Nothing's happening." Note: STUDY.md section 7 calls it 2.4 s, but 55 f at 29.97 fps is 1.83 s (worked out here from the study's own frame numbers). | SKIP | 2 | No stretch longer than 1.0 s (30 f) without readable text before 5 s. Holds of 2.4 s only after the turn. |
| 5 | Small grey-white sans, ink 2.2 to 4.6% | "Tiny grey text. I'd need to zoom." 2.2% is about 4 pt on a phone. | DARK, MSG | 3 | Any line that carries the message: ink height at least 6% of frame height (about 12 pt). Thesis line 10 to 12%. Small 2 to 4% type only for texture labels that carry no meaning. Inter Medium, not Regular, below 8%. Ink #C8 to #E6 (fine on black; X re-encodes and thin grey strokes break up). |
| 6 | 12 to 20 words, 1 to 5 per card, about 1 s | Split lines ("attention isn't earned" left, "by features." right): "I read half and it's gone." | CONF | 2 | Minimum hold 0.9 s (27 f) per card, plus 0.3 s for a line split across the width. At most 3 words per card before 3 s. |
| 7 | Text motion from the references only | "This is a dhruv template." | COPY | 2 | Use at most 3 of the 5 devices. Add one device of our own (see section C, rule X1). |
| 8 | Dot-matrix form with a 2-frame white bloom | A 2-frame white bloom on black is a flash. | DARK (flash), CONF | 2 | Bloom covers under 25% of the frame, or happens once, at least 1 s away from any other flash. The dot form must read as an object in 1 s, not just texture. |
| 9 | Tilted 3D product screen | "Oh, it's an app ad. Skip." A made-up checkout with prices reads as a scam ad. | AD, RIGHTS | 2 | No prices, no "Pay" button, no checkout. If used, show our own studio work surface (timeline, canvas) with our own UI. Nothing that looks like Whop or Stripe. |
| 10 | Glitch between 1.4 and 4.3 s | "Is my video buffering?" | CONF | 1 | 9 to 12 f only, on a text change, never over a black frame, never a freeze-frame look. |
| 11 | The drop on the turn card | Most feed video starts muted (judged): the drop is never heard. | MSG | 2 | The turn must work on mute: a visible change on the turn card (scale jump, black to light, or the only colour moment). Sound is a bonus. |
| 12 | Small centred mark on black, 2.4 to 2.7 s | ATN ends with 1 s black, mark, 2 s black: up to 5.7 s of a 15 s piece is empty. "It's over" at 9 s, scroll. "[STUDIO]" means nothing to a stranger. | SKIP, MSG | 2 | Mark right after the thesis, hold 1.5 to 2.0 s, no trailing black over 0.5 s. Put the handle under the mark in 4%+ type. The last frame should cut cleanly back to frame 0 for the X loop. |
| 13 | Monochrome stock-like hands, eyes, crowds | "Generic stock. Seen it a thousand times." Faces need releases. | AD, RIGHTS | 2 | Prefer made images (type, dots, our own UI). Stock only with a licence logged in SOURCES.txt; no identifiable faces without a release. |
| 14 | Voice: brand VO or a voice sample | ATN's sample ("Yo, if you don't shut your mouth...") is almost certainly someone else's recording. | RIGHTS, MSG | 3 | Default: no voice at all (Gate 1 says text over music). If a voice is ever added, record it ourselves. No film, show or meme clips. |
| 15 | Brand-logo montage changed to fictional marks | The ATN hook works because I know those logos in 4 frames. Made-up marks mean nothing, and lookalike marks are a trademark risk. | CONF, RIGHTS | 3 | Do not use logos at all, real or fictional, and nothing shaped like a famous mark (no fruit, no infinity sign, no asterisk). Use plain made objects that read in 4 frames without a brand (see the script fix in D). |
| 16 | Loudness -9 to -10 LUFS, -1 dBTP | "Loud when I unmute." That's fine. The risk is the AAC encode pushing peaks over -1 dBTP. | RIGHTS (none), polish | 1 | Measure loudness and true peak on the final encoded .mp4, not on the WAV. |
| 17 | Cut-out over swapping backgrounds | Rough matte edges look cheap at phone size. | AD (cheap) | 1 | Only with a clean matte. Otherwise drop it. |
| 18 | Cylinder text wrap | Wrapped words are hard to read small. | MSG | 1 | Any word meant to be read must be flat and still for at least 0.5 s. |
| 19 | Own mark replaces "dhruv" | Placeholder "[STUDIO]" is not a name. | MSG | 1 | Replace before posting. Keep it as a placeholder in all files until the user names the studio. |
| 20 | Drop copying frames, layouts, assets | Items 1 to 12 together rebuild ATN beat by beat: black, small sans, brand burst, eye, "Attention" on the drop, lower-case name on black. "That's dhruv's video with the words changed." | COPY | 3 | Change at least 3 of: the thesis (not attention or perception), the hook device (not a logo burst), the turn device (not one word on a drop), the end layout. Keep the style family, change the content. |
| 21 | MRI head not a must | Fine. Also: an MRI reads as medical or creepy without context. | COPY, CONF | 1 | Drop it. |

## B. Cross-cutting objections (not in section 9)

| # | Stranger says | Why | Sev | Fix |
|---|---|---|---|---|
| B1 | "The preview is a black rectangle." X and Instagram show frame 0 or a poster before play. | SKIP | 3 | Frame 0 = the hook line, readable, on a lit frame. |
| B2 | Corner labels (WHP style, y 80 to 84%, x 82 to 90%) sit under the player's timer and mute button (judged). | DARK | 2 | Keep all text out of the bottom 15% and the corners. On 4:5 Instagram keep text out of the bottom 20%. |
| B3 | "Attention is earned by perception" is marketing talk. | AD, MSG | 2 | Say one concrete, checkable thing in plain words. No guru tone. |
| B4 | A post caption that claims a fact ("made overnight") that isn't true. | RIGHTS (trust) | 2 | Caption only states what is true. No invented numbers or stories. |

## C. 05_RULE_BOOK.md red team (R# = rule numbers in 05)

| R# | Stranger says | Why | Sev | Fix |
|---|---|---|---|---|
| R13 | First word "by f2 to f21": the preview frame can be an image with no words. "No idea what this is." | SKIP, CONF | 3 | First line readable on f0. |
| R19 | Body ink 2.2 to 4.6% = about 4 to 9 pt on a phone. | DARK, MSG | 3 | Lines that carry the message: at least 6% (65 px at 1080). |
| R35 + R36 + R37 + R66 | All four together = ATN's skeleton: claim, problem, one word on the drop at f153 (34%), thesis split in 2 cards, 31 f black, mark f310, 56 f hold, 24 f fade, 57 f black. "dhruv's video with new words." | COPY | 3 | Keep at most 2 of the 4. Move the turn off f153. End pattern of our own (see X7). R66 also clashes with R70 (no copied layout). |
| R47 + R48 + R49 | All three are USE, but they are ATN's own headline devices (eye montage, selection box on the thesis, curved wall with hero at f104). Also clashes with R46 (1 or 2 headline effects). | COPY | 3 | At most 1 ATN signature device per piece, never at ATN's frames. No selection box on the thesis line. |
| R14, R69 | Fictional marks in the burst: "Fake logos. Knock-offs?" The ATN hook only works because the logos are known. | CONF, RIGHTS | 3 | No marks at all in the burst, real or fictional, and nothing shaped like a famous mark. Use plain objects or outputs. |
| R10, R15, R50 | 8 to 9 shots in 1 s can flash. | DARK (flash) | 2 | Add X2: flash check. Burst shots at similar brightness. |
| R21 | Split lines across the width: "I read the left half, it's gone." | CONF | 2 | Split only after 3 s, each half 6%+, hold +9 f. |
| R26 | Word-by-word add on the opening is ATN's opening move. | COPY | 2 | Not on the opening card. Use it once, later. |
| R34 | 0.9 to 1.2 s per card at phone size is tight. | CONF | 2 | 27 f minimum; add 9 f per word above 3, and 9 f for a split line. |
| R38 | "Gap of about 2.4 s": the study's own frames give 1.83 s. A gap at 2 to 4 s is where strangers leave. | SKIP | 2 | Change to: no gap longer than 30 f before f150. |
| R9, R66 | Up to 5.7 s of black at the end of 15 s. "It's over" at 9.3 s. | SKIP | 2 | Black before the mark at most 10 f; tail at most 15 f; use the time on longer card holds. |
| R40, R41 | Stock hands and crowds plus a tilted app screen: "Ad. Skip." | AD, RIGHTS | 2 | No prices, no Pay buttons, no faces without a release. |
| R57 | Mean 0.14 to 0.25 from f0. | DARK | 2 | Judged default: f0 to f29 a little brighter than the rest; the hook line at #DF. |
| R61 | Drop on the turn: lost on mute. | MSG | 2 | The turn must also be a visible change (X4). |
| R62 vs 06 script 1 | R62 says music to the last frame; script 1 shot 18 to 20 cuts music to silence from f279. | CONF (team) | 1 | Follow R62. |
| R64 | AAC encode can push peaks over -1 dBTP. | polish | 1 | Measure on the encoded .mp4. |
| R1 | 16:9 only. On Instagram it's a thin strip. | DARK | 2 | X6: a 4:5 layout for Instagram, built, not cropped. |

### Corrected rule list (replaces or adds to 05; only changed rules listed)
- **R13 (fixed).** The hook line is readable on f0 and stays on screen through the whole burst (f0 to f29 at least). One idea by f90.
- **R19 (fixed).** Any line that carries the message: ink height 6 to 8% (65 to 86 px at 1080). Text at 2.2 to 4.6% only for labels that carry no meaning.
- **R20 (fixed).** Thesis line 10 to 12% (108 to 130 px). The turn line at least 8%.
- **R21 (fixed).** Split-across-width lines only after f90, each half at least 6%, and hold 9 f longer.
- **R26 (fixed).** Word-by-word add-on: not on the opening card; at most once.
- **R34 (fixed).** Card hold at least 27 f, plus 9 f per word above 3, plus 9 f if split.
- **R35 to R37 (fixed).** Keep the claim, problem, turn, thesis idea, but use at most 2 of: a 1-word turn, a turn at f153, a 2-card thesis.
- **R38 (fixed).** No gap without text longer than 30 f before f150. (The study's "2.4 s" is 1.83 s by its own frames.)
- **R14 and R69 (fixed).** No logos or marks in the burst, real or fictional. No shapes close to a known mark.
- **R47 to R49 (fixed).** At most 1 of: eye montage, selection box, curved wall, cut-out over swapping backgrounds (R45). Never at ATN's frame numbers; never a selection box on the thesis.
- **R66 (fixed).** Black before the mark at most 10 f; mark holds 60 to 72 f with a handle line under it at 4%; fade out 24 f; black tail at most 15 f; last frame loops cleanly to f0.
- **X1 (new).** One device of our own that ATN and WHP do not have, used at the turn or the thesis.
- **X2 (new).** Flash check: no more than 3 large bright flashes in any 1 s (WCAG 2.3.1 general flash rule). Burst shots at similar brightness.
- **X3 (new).** Safe zone: no text in the bottom 15% or the 4 corners (player controls, judged). On 4:5, nothing in the bottom 20%.
- **X4 (new).** Mute test: the piece must make sense with sound off. The turn is a visible change, not only the drop.
- **X5 (new).** UI in the picture has no readable words that compete with the card line.
- **X6 (new).** Instagram copy: a separate 4:5 (1080x1350) layout with the same cards at the same or larger size.
- **X7 (new).** Post caption states only true things. No invented "made overnight" story or numbers.

## D. 06_SCRIPTS.md red team (script 1 "Taste" only)

| Where | Stranger says | Why | Sev | Fix |
|---|---|---|---|---|
| Whole script | Line for line it is ATN: "Attention / attention isn't earned / by features / It's earned / by perception" becomes "Taste / taste isn't / a prompt / It's chosen / frame by frame", at ATN's frames (f2, f30, f122, f153, f180, f216, f246, f279, f310, f366). Glitch at ATN's f42 to f50; cut-out over 7 backgrounds at ATN's f192; selection box on the thesis at ATN's f216. | COPY | 3 | Use the fixed timeline below. |
| Shots 1 to 9 | 9 app screens with "Generate", "Make", "Create", "Done", "Publish": "Ad for an AI app." The UI word "Make" fights the card word "make". | AD, CONF | 3 | Show outputs appearing, no buttons, no readable UI words (X5). |
| Card 1 | "anyone" lands at f2; f0 is a UI screen with no card text. | SKIP | 3 | Whole line on f0 (R13 fixed). |
| Cards 1, 2, 4, 5, 8 | 3.0 to 3.5% ink: about 6 to 7 pt on a phone. The turn word "Taste" is only 3.5%. | DARK, MSG | 3 | 6 to 8%; turn 8%+; thesis 10 to 12%. |
| Gap f67 to f121 | 1.83 s with no words at 2.2 to 4.0 s. | SKIP | 2 | Fill it with card 2 (see fix). |
| Shot 12 (turn) | A thin white bezier and a 4 px handle drag on black: invisible on a phone, and the drop is muted. | DARK, MSG | 3 | Lines at least 6 px at 1080, drag at least 15% of frame width; the turn is the one lit object after the wall goes dark. |
| Message | "Taste" is a common talking point in AI-era design posts (judged): "another 'taste is the moat' post." "It's chosen" has no clear subject. | MSG | 2 | Name the subject: "Taste is chosen". |
| Shot 11 assets | "Same smiling avatar": faces, and generated images need their tool's terms. | RIGHTS | 2 | No faces. Objects only, made by us. |
| Shot 17 | 9 small frames of an "a" in a timeline: too small to see the change. | DARK | 2 | 3 large frames, or one big "a" that changes on each playhead step. This is our own device (X1). |
| Shots 18 to 20 | 5.7 s of black and a mark nobody knows; music cut to silence (clashes with R62). | SKIP, CONF | 2 | Fixed end below. |

### Script 1 fixed lines (15.0 s, 450 f, 30 fps)
| # | Words (exact) | In | Out | Dur | Ink | Picture and motion |
|---|---|---|---|---|---|---|
| 1 | "anyone can make anything now." | f0 | f59 | 2.00 s | 6% | Whole line on f0, hard cut in, no word add. Under it: 9 shots f0 to f29 of outputs popping in (no UI words, similar brightness), then f30 to f59 more outputs tiling out. |
| 2 | "Nothing stands out." | f60 | f134 | 2.50 s | 8% | Right-to-left reveal f60 to f65 (R27). Samey outputs pile up into a flat grid (not a curved wall). Glitch 9 f at f100 to f108 as the "hero" lands and looks like all the others. |
| 3 | "Taste isn't a prompt." | f135 | f209 | 2.50 s | 8% | TURN at f135 (4.50 s, 30%) with the drop. Everything goes black except one hand-drawn "a", lit. Visible on mute. |
| 4 | "Taste is chosen" | f210 | f269 | 2.00 s | 11% | Hard cut. The big "a" changes on each playhead step every 3 f (our own device, X1). No selection box. |
| 5 | "frame by frame." | f270 | f344 | 2.50 s | 11% | Blur-in 3 f (R28). 3 large refinement frames of the "a", playhead steps every 3 f. |
| (black) | none | f345 | f354 | 0.33 s | | Hard cut to black. Music plays on (R62). |
| 6 | "[STUDIO]" with "[@handle]" under it | f355 | f449 | 3.17 s | 5% mark, 4% handle | No fade in; hold f355 to f425 (71 f); fade out f426 to f449 (24 f). Last frame loops to f0. |

Words: 5 + 3 + 4 + 3 + 3 + 1 = 19 (handle not counted). Read-out: "anyone can make anything now. Nothing stands out. Taste isn't a prompt. Taste is chosen frame by frame. [STUDIO]"
Trade-off for the user: cards hold 2.0 to 2.5 s, slower than ATN's 0.9 to 1.2 s. The picture keeps the page's pace; the words slow down so a stranger can read them on a phone. Shot count and second burst still have to be re-checked against R5 and R7 once the shot list is redone.

## E. Not checked
- No playback, no sound, no device test. Phone pt sizes and platform overlay positions are judged.
- No platform loudness or muting rules confirmed for X or Instagram in this sprint.

## F. 06_SCRIPTS.md scripts 2 and 3 (skimmed at 07:53 from the card tables only; short review)

| Where | Stranger says | Why | Sev | Fix |
|---|---|---|---|---|
| Script 2, whole | A brand film for "[PRODUCT]" with a voice-over: "It's an ad. Skip." Also off Gate 1 (spec piece in ATN style, text over music). | AD, CONF | 3 | Park script 2 unless the user asks for a product film. |
| Script 2, cards 1 to 5, 8, 9 | "// Ideas //" at f21, a 2-frame word flash at f76, "@/ noise //" at f81, word plus phonetics at x 71 to 82%, y 77%, white flash f322, 3 f wordmark wipe: WHP's own frames and positions. | COPY | 3 | Same fix as script 1: new frames, X1 own device. |
| Script 2, card 2 | "Threads" for 2 f (0.07 s): nobody reads it. | MSG | 2 | Hold 27 f or drop. |
| Script 2, f0 to f20 | No text until f21. | SKIP | 3 | Line on f0 (R13 fixed). |
| Script 3, whole | Same ATN skeleton: word add at f2/f6/f12, right-to-left reveal at 7.8%, one-word turn "Feeling" at 3.5% on the drop at 34%, split "logos don't" / "stop thumbs." at 3.0%. | COPY, DARK | 3 | Fixed lines below. |
| Script 3, card 1 | A video about the first second whose first frame has no words. "You get one second" is a number claim (the script marks it UNCHECKED). | SKIP, MSG | 2 | Line on f0; drop the number. |
| Script 3, "logos don't stop thumbs." then a "[STUDIO]" mark | "It ends on a logo, lol." | MSG | 2 | Say "lead with", so the mark coming last fits. |

### Script 3 fixed lines (15.0 s, 450 f)
| # | Words (exact) | In | Out | Ink | Note |
|---|---|---|---|---|---|
| 1 | "You have a second." | f0 | f59 | 6% | On f0, burst under it |
| 2 | "Don't spend it on a logo." | f60 | f134 | 8% | Right-to-left reveal 6 f |
| 3 | "Lead with a feeling." | f135 | f209 | 8% | TURN at 4.5 s, visible on mute |
| 4 | "Frame one is the hook." | f210 | f344 | 11% | Thesis, our own device (X1) |
| 5 | "[STUDIO]" plus "[@handle]" | f355 | f449 | 5% / 4% | As script 1 fixed end |
Words: 4 + 6 + 4 + 5 + 1 = 20.

## G. Also not checked
- Scripts 2 and 3 were skimmed from their card tables at 07:53 only; their shot lists, assets and sound plans were not reviewed.
- Script 1 fixed timeline was not re-counted against R5 (26 to 31 shots) and R7 (second burst); that needs the redone shot list.
- WCAG 2.3.1 is cited from memory as "no more than 3 general flashes in any 1 s"; the exact luminance and area thresholds were not re-read in this sprint.
