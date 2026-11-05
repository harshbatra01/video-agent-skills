# 08 Red team: a skeptical stranger scrolling Instagram and X on a phone

Version 1, 07:49 UTC. Inputs read: BRIEF.md, research/dhruvxr/STUDY.md (sections 1, 4, 6 ATN, 7, 8, 9).
05_RULE_BOOK.md and 06_SCRIPTS.md: not on disk yet at 07:49. Checked with ls every minute; review added below when they appear.

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
| 4 | One card per hold, 0.9 to 2.4 s, second burst | ATN has a 2.4 s stretch with no text (f67 to f121) at 2.2 to 4.3 s: "Nothing's happening." | SKIP | 2 | No stretch longer than 1.0 s without readable text before 5 s. Holds of 2.4 s only after the turn. |
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

## C. Corrected rule list (v1, against STUDY.md section 9; mapped to R# once 05_RULE_BOOK.md exists)
(pending 05_RULE_BOOK.md)

## D. Fixed script lines
(pending 06_SCRIPTS.md)

## E. Not checked
- No playback, no sound, no device test. Phone pt sizes and platform overlay positions are judged.
- No platform loudness or muting rules confirmed for X or Instagram in this sprint.
