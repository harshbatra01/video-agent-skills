# 07 Build plan: one 15 s spec piece in the dhruvxr ATN style
Status: final, 07:51 UTC, 5 Nov 2026. Plan only. Nothing rendered except one small proof (section 6).
Inputs: research/dhruvxr/STUDY.md sections 4, 5, 6 and 9; jobs/dhruvxr-01/sprint/BRIEF.md (Gate 1 defaults).
Tags: **[M]** = measured in this environment today. **[J]** = judged (estimate or opinion). **[S]** = number taken from STUDY.md.

## 0. Tools present [M]
- Python 3.13.18. numpy 2.5.3. Pillow 12.3.0.
- ffmpeg 6.1.1-3ubuntu5 and ffprobe 6.1.1-3ubuntu5. libx264 encode works (used by the proof).
- ffmpeg filters present: perspective, gblur, geq, lut, lutyuv, curves, rgbashift, displace, tblend, tmix, chromakey, colorkey, vignette, noise, xfade, zoompan, loudnorm, ebur128, alimiter, lowpass, highpass, aecho, afade, aevalsrc, anoisesrc, amix.
- Node 22 at /opt/node22/bin/node. Google Chrome for Testing 153.0.8010.12 at /usr/bin/google-chrome (headless HTML to PNG works: one 640x360 test card rendered in 7.24 s cold start with `--headless=new --no-sandbox`, text level 0.867 = #DDD as set; test file kept in the scratchpad, not the repo).
- Fonts: 119 fc-list entries. **Inter is installed**: /usr/share/fonts/opentype/inter/ has Inter-Regular, Inter-Medium, Inter-Italic, Inter-MediumItalic, Inter-Thin, Inter-SemiBoldItalic and Inter Display cuts (.otf). DejaVu Sans, Serif and Sans Mono also present.
- **scipy is NOT installed.** skills/minidoc-reference-style/scripts/synth.py imports scipy (butter, sosfilt, fftconvolve), so it will not run as is.
- tts.py is ElevenLabs only (needs the ELEVENLABS_API_KEY env var and network). The env var is unset in this shell. Not run.
- Not present: After Effects, Premiere, any Linux person-matte tool (person_mask.js is Mac only [S]).

## 1. The piece (Gate 1 defaults)
- 1280x720 master (STUDY.md item 1 says 1920x1080 delivery is also possible; default here: build at 1280x720, matching the reference, and note 1080p as an option). 30 fps. 15.0 s = 450 frames.
- ATN style: text manifesto over music. No client logos, no real third-party logos. Sign-off "[STUDIO]".
- One idea in the first 3 s (claim complete by f89).
- Loudness -9 to -10 LUFS integrated (target -9.5), true peak -1 dBTP.
- Black base: mean brightness 0.14 to 0.25, near-black 63 to 78% [S]. Monochrome; colour only on our own mark or product piece.
- Type: Inter Regular or Medium, sentence case, ink #AA to #DF, ink height 2.2 to 4.6% of 720 (16 to 33 px); one larger thesis line at 8 to 10% (58 to 72 px) [S].
- Copy: 12 to 20 words on screen, 1 to 5 words per card, argument shape claim, problem, turn, thesis, sign-off [S]. The words themselves are written at the script gate (G2), not in this plan. No copied ATN lines, no copied "prduct" typo (STUDY.md item 20).

### Frame plan (450 f at 30 fps, mapped from ATN proportions) [J]
| Frames | s | Picture | Text | Effect # | Sound |
|---|---|---|---|---|---|
| f0 to f29 | 0.0 to 1.0 | 8 shots of 3 to 4 f: our own fictional marks and cards, or monochrome stock on one idea | Claim, words add every 4 to 6 f | 1, 15 | Opening hit from f0 |
| f30 to f89 | 1.0 to 3.0 | One held form: dot-matrix form (or eye macro if licensed footage is found) | Claim ends | 2 (or 16) | Bed |
| f45 to f53 | 1.5 to 1.77 | Rectangle glitch insert, 9 f, inside 1.4 to 4.3 s [S] | | 17 | Glitch SFX |
| f90 to f149 | 3.0 to 5.0 | Curved wall of designed-from-scratch screens, darkening to black | Problem line, right-to-left reveal over 6 f | 18, 19 | Riser |
| f150 to f179 | 5.0 to 6.0 | Hard cut on the drop | Turn word, held | 23-style hard cut | Bass drop at 5.0 s |
| f180 to f215 | 6.0 to 7.2 | Second burst: 7 backgrounds at 3 f each behind a held subject (text block or dot form, not a person) | Turn line, split left and right | 20 (substitute) | Hit at about 6.8 s |
| f216 to f245 | 7.2 to 8.2 | Thesis word in a 1 px selection box with handles | Thesis, 8 to 10% ink height | 22 | Hit at about 7.7 s |
| f246 to f278 | 8.2 to 9.3 | Held monochrome footage or dot form | Thesis ends | 3 or 12 | |
| f279 to f309 | 9.3 to 10.3 | Black, 31 f | | 23 | Music plays on |
| f310 to f365 | 10.3 to 12.2 | "[STUDIO]" centred, no fade in, 56 f hold | Sign-off | 23 | |
| f366 to f389 | 12.2 to 13.0 | Sign-off fades out over 24 f | | 23 | |
| f390 to f449 | 13.0 to 15.0 | Black, 60 f | | | Music to the last frame [S] |

## 2. Assets: source and licence type
| Asset | Needed for | Where it could come from | Licence type | Note |
|---|---|---|---|---|
| Monochrome stock footage (hands, eyes, crowds) | Burst, holds | Wikimedia Commons via skills/minidoc-reference-style/scripts/commons_search.py, commons_get.py, commons_video_get.py (they read LicenseShortName) | Per file: CC0, Public Domain, CC BY, CC BY-SA. Reject NC and ND | Network reach to Commons not checked today. Log every file in jobs/dhruvxr-01/SOURCES.txt with author and licence |
| Same, alternative | Burst, holds | Our own shoot (phone, monochrome grade in ffmpeg) | Owned | Best for rights; needs a person and a day [J] |
| Same, alternative | Burst | Stock sites with their own free licences (Pexels, Pixabay) | Site licence, not CC; terms vary | Not checked. Download only if the network policy allows; no workarounds |
| Eye macro (for effect 16) | f30 to f89 option | Commons search "eye macro", or own shoot | As above | If none found, use the dot form instead |
| Procedural backgrounds, dot forms, particles, globe, noise | Many | Generated in numpy and PIL | Owned (our code) | No third-party input |
| Product UI screens and website wall | f90 to f149 | Designed from scratch as HTML, shot in headless Chrome, or drawn in PIL | Owned | No real company UI; fictional names only |
| Brand-style profile cards | f0 to f29 | HTML templates (production-automation card pipeline: HTML in headless Chrome plus ffmpeg) with fictional marks | Owned | Gate 1: no real third-party logos |
| Sign-off mark "[STUDIO]" | f310 to f389 | Set in Inter Medium | Inter: SIL Open Font License 1.1 | Placeholder until the studio mark exists |
| Font, body | All text | Inter Regular and Medium, installed | SIL OFL 1.1 | SF Pro (ATN's closer match) is Apple-licensed and not installed; do not use |
| Font, mono | Log list, character grid | DejaVu Sans Mono, installed | DejaVu/Bitstream Vera licence (free, permissive) | |
| Music bed | Whole piece | Synthesised in numpy (port synth.py, see gap G4), or ffmpeg aevalsrc and anoisesrc with lowpass/highpass | Owned | Or a licensed library track logged in SOURCES.txt (licence type: royalty-free library, terms per track) |
| SFX: sub hit, glitch, whoosh, riser | Hits on picture changes | synth.py functions impact(), glitch(), whoosh(), riser() once ported off scipy; or ffmpeg anoisesrc plus filters | Owned | |
| Voice sample | Optional (ATN opens on one) | Default: none. Options: ElevenLabs via tts.py (needs key and network; licence per ElevenLabs terms), or our own recording | Per service terms, or owned | No film or song samples without a licence |

## 3. Effects from STUDY.md section 5: build method here
Docs named below: skills/motion-design/references/native-looks.md, titles-captions-type.md, transitions.md. Recipes: skills/motion-design/effects-library/recipes/. Blocks: skills/effect-library/blocks/. Scripts: skills/minidoc-reference-style/scripts/.
"In piece" = used in this 15 s ATN-style plan. All others are WHP effects kept here as a costed menu.
| # | Effect | In piece | Build method (ffmpeg / PIL / numpy) | Repo help |
|---|---|---|---|---|
| 1 | Opening micro-montage | Yes, f0 to f29 | Cut list in a JSON (shot id, in frame, out frame). Python writes each frame as PNG; encode with `ffmpeg -framerate 30 -i f_%04d.png -c:v libx264 -pix_fmt yuv420p -crf 16`. White flash = one frame of #FFFFFF | cut_events.py and frame_strip.py (minidoc scripts) to check cut timing against the plan |
| 2 | Dot form with soft bloom | Yes (f30 to f89 default) | PIL mask, sample on a square grid (pitch 6 px at 640 wide, about 10 to 12 px at 1280 [J]), draw square dots, add a Gaussian glow stack (radii 4, 12, 32 px; weights 0.6, 0.45, 0.35), key the wide radius down over the shot. **Proof done, section 6** | motion-design native-looks.md section 3 halftone and section 4 glow; recipes/12-pixel_dither_background.md (AE, used as a reference only) |
| 3 | Vertical-line screen texture | Optional on footage | numpy: darken every 3rd column by 7%: `f[:, ::3] *= 0.93`. ffmpeg: `geq=lum='lum(X,Y)*(1-0.07*eq(mod(X,3),0))'` | None needed |
| 4 | Corner code labels blur in | No (WHP) | PIL text in Inter Italic; frames 1 to 3 at GaussianBlur 6, 3, 0 px; glow = blurred copy at 40% added | titles-captions-type.md section 2 |
| 5 | Two-frame big word | No (WHP) | One PIL text layer on 2 frames | None needed |
| 6 | White blowout into 1-bit threshold | No (WHP) | numpy: gain 1, 2, 4 over 3 f, clip; then `(luma > t) * 255` for 5 f. ffmpeg alt: `lutyuv` or `curves` | transitions.md light blow-out |
| 7 | Product UI tilted in 3D, focus pull | Partly, inside #18 | PIL `Image.transform(size, Image.PERSPECTIVE, coeffs)`, coeffs solved from 4 corner points with numpy lstsq; blur 8, 3, 0 px over the first 2 to 3 f; drift with two keys and an ease. ffmpeg alt: `perspective` filter | effect-library/blocks/screen-photo-push (screen_push.py) for the filmed-screen look, partly |
| 8 | Scan-line tear plus log list | No (WHP); #17 is the ATN glitch | numpy: per band of rows (4 to 40 px tall) `np.roll` by 10 to 120 px; white bars; a DejaVu Sans Mono log list for a few frames. 18 f | recipes/13-one_frame_glitch_burst.md, 14-shake_chroma_impact.md (AE references); ffmpeg `rgbashift`. STUDY.md says check the box-glitch verdict |
| 9 | Fade from white into dot form, drifting labels | No (WHP) | Per-frame lerp white to grey to dark over 3 f; two labels move 25 px over 60 f in opposite directions, two keys each | Partly (proof dot form) |
| 10 | Flash, particles converge into a logo | No (WHP) | numpy: N particles from random starts to the dot positions of the mask, cubic in-out over 46 f; 2-frame bloom by raising glow gain | effect-library/blocks/particle-mind (particle_mind.py), partly |
| 11 | Photo-tile logo bursts into a collage | No (WHP) | PIL: tiles at the mask grid filled with photo crops; camera scale with two keys | effect-library/blocks/video-wall (video_wall.py), partly |
| 12 | Slow-shutter footage | Optional f246 to f278 | ffmpeg `tmix=frames=8` on the clip, or numpy mean of the last 8 frames | recipes/09-slow_shutter_echo_trail.md (AE reference) |
| 13 | Rotating dot globe | No (WHP) | numpy orthographic sphere: lat/lon points, rotate by angle per frame, keep z > 0, dot size and level by z, faint red tint, fade over about 60 f | native-looks.md section 8 (AE reference) |
| 14 | Wordmark right-to-left wipe then fade | No (sign-off has no fade in, per ATN) | PIL mask with an x edge moving right to left over 3 f, then alpha ramp over 7 f | None needed |
| 15 | Profile card montage, words add on | Yes, f0 to f29 | HTML card template (fictional logo tile, name, badge, bio, banner) rendered by headless Chrome to PNG, 4 f each; words drawn in PIL on top, one more word every 4 to 6 f. PIL-only cards as a fallback | production-automation card pipeline (HTML templates plus headless Chrome plus ffmpeg) |
| 16 | Montage reflected in an eye | Option only | Hand-made iris mask (PIL ellipse, 8 px feather) on licensed eye footage; screen-blend the montage at 50 to 70%; slow push via scale keys; red and cyan character grid in DejaVu Sans Mono at the left | native-looks.md section 9 character grid (AE reference) |
| 17 | Rectangle glitch insert | Yes, f45 to f53 | numpy: paste 4 to 8 rectangles copied from other frames at offsets, one zoomed copy of the text line, 2 or 3 flat colour blocks; new layout every 1 to 2 f | Box-glitch family; STUDY.md says it is banned in music edits only |
| 18 | Curved 3D wall of screens | Yes, f90 to f149 | Each screen PNG warped with PIL PERSPECTIVE; placed on a cylinder (angle to x, depth to scale and darkness); fly-in and stack with two keys per card; hero card lands about two thirds in; global darken to black over the last 15 f | None direct; video_wall.py tilt logic, partly |
| 19 | Right-to-left text reveal | Yes, problem line | PIL alpha mask; visible x edge moves right to left over 6 f | None needed |
| 20 | Held cut-out over swapping backgrounds | Substitute, f180 to f215 | Held subject = our text block or dot form (alpha known, no matte needed) over 7 backgrounds at 3 f each. With a green-screen clip: ffmpeg `chromakey` then overlay | person_mask.js is Mac only; no Linux matte |
| 21 | Cylinder-wrapped repeated word | Pilot only (STUDY.md item 18) | numpy per-column warp: for output column x, theta = asin((x - cx) / R), source u = R * theta + scroll; shade by cos(theta); inverted window = 255 minus the region | None in the repo |
| 22 | Word in a selection box | Yes, f216 to f245 | PIL: 1 px #FFFFFF rectangle 12 px outside the ink box, 8 handles of 6x6 px at the corners and mid-edges | None needed |
| 23 | Hard cut to black, then sign-off | Yes, f279 to f449 | 31 f black; "[STUDIO]" with no fade at f310; 56 f hold; alpha 1 to 0 over 24 f; black to the end | None needed |

Finish (not a section 5 effect, needed for the gates):
- Grain and vignette (ATN): ffmpeg `noise=alls=6:allf=t` and `vignette=PI/5` [J values].
- Loudness, two pass: pass 1 `ffmpeg -i mix.wav -af loudnorm=I=-9.5:TP=-1.0:LRA=7:print_format=json -f null -`; pass 2 with measured_I, measured_TP, measured_LRA, measured_thresh and offset fed back. At -9.5 LUFS loudnorm may fall back to dynamic mode; put `alimiter=limit=0.85` before it [J]. Verify with `ebur128=peak=true`.
- Mux: `ffmpeg -i video.mp4 -i mix.wav -c:v copy -c:a aac -b:a 320k -shortest out.mp4`.

## 4. Steps in order, with gates and time [J]
Gate 1 is already passed (BRIEF.md). Times are machine plus agent time for one person-agent, judged, not measured.
| Step | What | Output | Gate | Time |
|---|---|---|---|---|
| 1 | Script: write 12 to 20 words in the claim, problem, turn, thesis shape; word count and per-card counts checked | script.json | **G2: user approves the copy** | 20 min |
| 2 | Frame plan: lock section 1 table to the copy; cut list JSON with frame numbers | cutlist.json | | 15 min |
| 3 | Asset pull: Commons search and download (or own shoot), licence log in SOURCES.txt; reject NC and ND | assets/, SOURCES.txt | **G3: rights check, every file has a licence line** | 30 to 60 min (own shoot: 1 day) |
| 4 | Music and SFX: port synth.py filters to numpy (or ffmpeg filters), write the bed with the drop at 5.0 s and hits on picture changes | mix_v1.wav | | 45 min |
| 5 | Animatic: grey boxes and real text at 640x360 with the music, to check timing | animatic.mp4 (small) | **G4: user approves timing and order** | 30 min |
| 6 | Effect pilots at 640x360, 1 to 2 s each: #15 cards, #17 glitch (3 or 4 strengths), #18 wall, #20 substitute, #22 box, #2 dot form (done) | pilots/ | **G5: user picks per effect** | 90 min |
| 7 | Build script: one Python file writes all 450 frames from cutlist.json; encode with ffmpeg | rough_v1.mp4 | | 60 min write, about 5 to 15 min render [J] |
| 8 | Measure: colour_stats.py (mean brightness 0.14 to 0.25, near-black 63 to 78%), frame_strip.py contact sheet, ebur128 loudness | qa/ | **G6: numbers in range** | 15 min |
| 9 | Fix pass, then final encode and two-pass loudness, mux | final.mp4 | **G7: user final approval** | 30 min |
Total: about 5.5 to 6.5 hours of work with no own shoot [J].

## 5. Gaps: what we cannot match, and why
- G1. **No person matte on Linux.** person_mask.js is Mac only [S]. The held skier cut-out (#20) needs a green-screen or pre-keyed clip. Default: hold our own text or dot form instead.
- G2. **No After Effects or Premiere.** Recipes in motion-design/effects-library/recipes are AE notes; here they are references only. Every effect is rebuilt in PIL and numpy, frame by frame. Real 3D (camera, depth of field, motion blur) is faked with 2D perspective warps and blur [J]: expect less natural parallax on #18.
- G3. **Fonts.** Inter is installed (checked with fc-list), so the type law is met. SF Pro, which ATN reads closest to [S], is not installed and is Apple-licensed. Matches are judged, not fitted [S].
- G4. **scipy missing.** synth.py will not run. Port its four filter calls to numpy (FFT-domain filters, numpy convolve for the reverb) or use ffmpeg audio filters. No installs allowed.
- G5. **Footage.** No stock footage is in the job yet. Commons reach was not tested. Monochrome stock-like clips of hands, eyes and crowds may be thin on Commons [J]; own shoot is the fallback.
- G6. **No real brand logos** (Gate 1). ATN's hook relies on famous marks [S]; fictional marks will hit less hard [J]. That is a deliberate rights trade-off.
- G7. **No voice sample by default.** ATN opens on a voice sample [S]. We cannot use one without a licence; tts.py needs a key (unset here [M]) and network (not checked).
- G8. **Loudness.** We target -9.5 LUFS, not ATN's -5.4 LUFS [S]; ours will sound quieter next to it, by design.
- G9. **Claude cannot watch or hear.** All timing and look checks are by numbers (frame stats, ebur128, contact sheets). The user must watch the pilots and the rough cut.
- G10. **Headless Chrome** works [M], but at about 7 s per cold screenshot. Render each card once to PNG and reuse it, never per frame. PIL cards are the fallback.

## 6. Proof: dot-matrix form (effect #2) [M]
- Script: jobs/dhruvxr-01/sprint/proof/dot_matrix_proof.py. Output: proof/dot_00.png to dot_11.png and proof/dot_matrix_proof.mp4.
- 640x360, 12 frames at 30 fps (0.4 s). Mask = "[STUDIO]" in Inter Medium 120 px. 6 px grid, 4 px square dots, ink up to #DF, three-radius Gaussian glow whose wide radius shrinks over the 12 frames.
- Result: runtime 0.42 s; frame 0 mean brightness 0.055; near-black (below 0.1) 88.2%.
- Reading: the method works and is fast. On its own the frame is darker than the style range (0.14 to 0.25 mean, 63 to 78% near-black [S]); a full shot needs a larger form or footage behind it. Not viewed by eye (Claude cannot watch); the user should open the PNGs.

## 7. Not checked
- Network reach to Wikimedia Commons, Pexels, Pixabay, ElevenLabs.
- Whether Inter loaded inside Chrome (the test asked for it by name; the glyph shape was not checked).
- Render time for 450 frames at 1280x720 (the proof suggests a few seconds per effect pass at 640x360; the full number is a guess).
- The internals of each effect-library block beyond the first lines of BLOCK.md.
