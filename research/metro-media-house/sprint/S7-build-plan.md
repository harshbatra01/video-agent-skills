# S7 Build plan: one Metro Media House style video (Masayoshi Son, idea 1)

Status: done (13:24 IST). Built from STUDY.md sections 5, 6, 10, IDEAS.md idea 1 and tool checks with ls, grep and head.

Format: landscape 1920x1080, 25 fps, about 80 s, narrated, loud music bed. Organic post. Real interviews and news footage only, no feature-film clips. Voice picked by ear.

Sections below are filled in order: 1 assets, 2 effects, 3 steps, 4 gaps and risks.

## 1. Asset list

Topic: IDEAS.md idea 1, Masayoshi Son ("the man who lost $70 billion, and just bet his company again"). Peg: SoftBank Q2 FY2026 results on 10 Nov 2026 (per IDEAS.md).

| Asset | What we need | Likely sources | Rights note |
|---|---|---|---|
| Hook photo | Son with Jack Ma (handshake). Alternative: Jan 2025 Stargate announcement photo (Trump, Son, Altman, Ellison). | Wire photo agencies, SoftBank or Alibaba press rooms, Wikimedia Commons (search with `commons_search.py`). | Not found yet (IDEAS.md says "needs finding"). Commons first because `commons_get.py` logs licence and author. A wire photo needs a licence or a fair-use call by the user. Stargate photo is political: user call. |
| Footage: Son | Many different clips, not one repeated: SoftBank earnings briefings and AGMs, keynotes (SoftBank World), interviews, Son and Altman on stage, 2014 Alibaba IPO day. | SoftBank Group IR video archive, official YouTube channels, news channels (CNBC, Bloomberg) via `ytdl.py`. | Real interviews and news only (user default). News clips are third-party: credit on screen, short clips, user signs off. |
| Footage: soundbite | Son on record saying "We lost around $70 billion" (IDEAS.md, rating B). | Find the video; IDEAS.md has no URL. | Must be the real clip, captioned word for word. If not found, drop the soundbite rather than fake it. |
| Footage: context | 2000 dot-com crash news, Alibaba IPO bell, OpenAI and ChatGPT b-roll, S&P headline, Tokyo and SoftBank HQ exteriors. | News archives, Commons video (`commons_video_get.py`), company press kits. | No feature-film or pop-culture clips (user default). The comparison slot is open in IDEAS.md: fill it with real footage plus a printed comparison line. |
| Logos | SoftBank, Alibaba, OpenAI, Yahoo, ARM, WeWork, Vision Fund, S&P, for logo bursts (effect 11). | Company press kits, Commons. | Trademarks used to identify the company only, flat plates, no altered marks. |
| Built UI cards | Number cards and receipt-style or headline cards (effect 12, 13): "$70 billion", "$20 million", "$200 billion+", "$60 billion+", "Outlook: negative". | Built by us, from scratch. | Our own designs only. Never a real app's UI (effects-library row 17 rule). Figures from filings only (IDEAS.md: OpenAI dollar figure must come from SoftBank filings). |
| Fonts | Inter Medium for small captions, Inter Bold for big words. | Installed in this container under `/usr/share/fonts/opentype/inter/` (InterDisplay-Medium.otf seen by fc-list). On the Mac: check with `premiere-ae-editing/scripts/media/fontcheck.swift`. | Inter is OFL, free to use. |
| Music | One loud bed, voice-led. STUDY.md gives energy, not tempo: bed sits 0.8 to 3.7 dB under the voice in gaps; loudness peaks (risers or hits) on story turns. Tempo was not measured in STUDY.md, so pick by ear. Cuts follow words, not beats. | Licensed library track picked by the user. `minidoc-reference-style/scripts/synth.py` makes a stand-in score only. | Organic post: track must be cleared for Instagram. |
| SFX | 1-frame hits under inverted cuts, whooshes on zoom-blur pushes, a riser into the paradox beat, clicks for the logo burst, a soft paper sound for cards. | Licensed SFX library. | Licence per sound. |
| Voice | Narration at 170 to 185 words a minute, nearly non-stop (3.5 to 10.2 s of pause per reel). About 80 s means about 230 to 245 words. | `minidoc-reference-style/scripts/tts.py` (ElevenLabs; `tts.py voices` lists voices, `tts.py say <voice_id> <text_file> <out.mp3>`), needs `ELEVENLABS_API_KEY`. Voice picked by ear (user default). | Synthetic voice: check the provider's commercial terms. |

## 2. Effect by effect (STUDY.md section 6)

Engines: "Linux" = ffmpeg 7/PIL 12 in this container (both present; Inter-Medium.otf and Inter-Bold.otf installed). "AE" or "PS" = After Effects or Photoshop on the user's Mac. Dropped by the defaults: #10 film clips (no feature films), #16 typing cursor (EIN only, section 10 item 19), #19 M sting (Metro's mark), #20 ad tail (organic post). #4 and #6 are off by default (section 10 item 20), one big moment at most.

| # | Effect | Repo tool (verified path) | Engine | Status |
|---|---|---|---|---|
| 1 | 3x3 grid block reveal of the hook photo | `skills/motion-design/effects-library/ae/effects/pixel_reveal.jsx` (recipe `recipes/01-pixel_reveal.md`) as a base; or per-frame compose in the style of `skills/minidoc-reference-style/scripts/build_template_v8.py` | AE, or Linux PIL | Needs adapting. Warning: effects-library README row 1 marks pixel_reveal "breaks our taste, do not use unless asked". The Metro ask counts as asked, but pilot 3 s first (section 10 item 3). A 9-cell PIL build is small and runs here. |
| 2 | Subject cut-out, background dims, light rim | `skills/minidoc-reference-style/scripts/person_mask.js` (`osascript -l JavaScript person_mask.js <in.jpg> <out_mask.png>`) or `skills/premiere-ae-editing/scripts/stills/ps_cutout.jsx` (job list `ps_cutout_jobs.txt`, run in Photoshop) | Mac only (Vision or PS); dim and rim then in PIL or AE | Gap on Linux (no matte tool here). Ready on the Mac. One still, so one mask. |
| 3 | Background swap cell by cell to the place word | Same grid code as #1 over the #2 matte | AE or Linux PIL | Needs adapting (depends on #1 and #2). Place word for this script: "Tokyo" or "Silicon Valley" plate, our own sourced still. |
| 4 | Red neon outline tracing the subject | `effects-library/ae/effects/glowing_gradient_stroke.jsx` (README: "needs work", Deep Glow 2 or native swap) on the #2 matte edge | AE | Off by default. Needs adapting if used. |
| 5 | Inverted-frame cut (1 negative frame, optional 1 white/black frame) | `effects-library/ae/effects/one_frame_glitch_burst.jsx`, cut down to the invert step; or ffmpeg `negate` on one frame plus a 1-frame white card | Linux ffmpeg or AE | Ready (ffmpeg route is trivial). Budget about 1 every 3 to 5 s on sentence turns, so about 16 to 25 in 80 s; start near ACK/YC rate, user picks. |
| 6 | Thermal flash, 2 frames | No repo tool found (grep for thermal/colorama in effects-library not done in sprint time); ffmpeg `pseudocolor` or a PIL gradient map | Linux ffmpeg or AE | Off by default. Gap, small. |
| 7 | Zoom blur with RGB fringe into big type | `effects-library/ae/effects/shake_chroma_impact.jsx` (recipe 14) without shake, plus CC Radial Fast Blur | AE | Needs adapting. Use at 1 to 2 story turns. |
| 8 | Word-by-word small captions spread across the frame | Not found. `skills/premiere-ae-editing/scripts/captions/style_captions.py` only styles a saved Premiere project's captions. Word timings exist via `skills/minidoc-reference-style/scripts/asr_words.py <media> <out.json>`. | New script: Linux PIL overlay (Inter installed) or AE text layers | Gap. Biggest build item. Spec: Inter Medium, cap height about 38 px on 1080, centre y 44 to 52%, free x per word beside the face, each word on at its start, line clears at phrase end, black on white frames. |
| 9 | Big words split or stacked around the subject | Same new caption script, Inter Bold, 3 to 4x, tracking -20 | Same as #8 | Gap (part of #8). 8 to 15 per reel: "$70 billion", "richest", "six minutes", "$200 billion", "OpenAI", "twice". |
| 10 | Film and pop-culture clip | Dropped (user default). Replace with real news footage plus a printed comparison line. | n/a | Dropped. |
| 11 | Logo burst, 4 to 6 frames each | `skills/effect-library/blocks/video-wall/video_wall.py` is a tilted wall, not a burst; plain ffmpeg concat of logo plates does it | Linux ffmpeg | Ready (plain cuts). For SoftBank's portfolio list: Yahoo Japan, ARM, Alibaba, WeWork, Uber, OpenAI. |
| 12 | Portrait or photo burst into a counting number | `counterRow(c, t0, t1, target, word)` at line 206 of `skills/premiere-ae-editing/scripts/ae/motion_lib.jsx` | AE | Needs adapting (restyle Didot to Inter Bold, per STUDY.md). Use on "$70 billion" lost and "$20 million to $200 billion". |
| 13 | Built UI card with spinner, check and highlighter | Card: HTML or HyperFrames per `skills/minidoc-reference-style/references/hyperframes-overlays.md` (install not checked). Marker sweep: `skills/effect-library/blocks/screen-photo-push/screen_push.py <page.png> <page_marked.png> <out.mp4> --w 1920 --h 1080 --fps 25` (defaults are 1440x1080 at 30 fps). | Linux (numpy, scipy, Pillow, ffmpeg) | Needs adapting. Correction to STUDY.md: it cites `hail_mary_highlight_streak` for the marker, but README row 8 says that effect smears highlights into light streaks. The yellow marker lives in `screen_push.py`. Use for "S&P outlook: negative" or the filing line with the OpenAI figure. |
| 14 | Photo walk-through, B&W except the named person | `skills/effect-library/blocks/colorize-reveal/colorize_reveal.py <in> <out.mp4>` (whole frame only) plus a person matte from #2 | Linux plus Mac matte | Conditional: only if the hook is the Stargate group photo (section 10 item 16). The two-person handshake photo does not need it. |
| 15 | Polaroids and prints on off-white paper | `screen-photo-push` block; polaroid recipe in `minidoc-reference-style/references/effects-library.md` (word "polaroid" found there) | Linux PIL | Needs adapting. Paper #EDECEA to #F2F1EF with vignette. Breath beat every 10 to 20 s (11 to 14% bright frames). |
| 16 | Typing-cursor block | none | n/a | Dropped (EIN only). |
| 17 | Tilted 3D screen wall | `skills/effect-library/blocks/video-wall/video_wall.py <out.mp4> <clip1> <clip2> ... --tilt 28` | Linux (numpy, scipy, ffmpeg) | Ready to try. Use for "every time you use ChatGPT" zoom-out (ChatGPT screens, news screens). |
| 18 | Callback zoom-out reveal at the end | No tool. AE nested comps with scale keys. | AE | Gap: needs a designed or staged plate. Simpler fallback: zoom out to the hook photo printed on paper (#15). |
| 19 | M logo sting | none, not ours | n/a | Dropped. End on kicker plus callback shot. |
| 20 | Ad tail cards | none needed | n/a | Dropped (organic). |

## 3. Steps in order (video-agent stages and gates)

Stage numbers follow the table in `skills/video-agent/SKILL.md`. Times are rough working hours, not tested.

| # | Stage and gate | What happens | Where | Time |
|---|---|---|---|---|
| 1 | Idea (gate: pick topic) | IDEAS.md idea 1 by default. | done | 0 |
| 2 | Reference study (gate: use, change or drop list) | STUDY.md section 10 stands; defaults applied above. | done | 0 |
| 3 | Script in locked stages (`story-script-writer`, `goal-alignment-review`) | 230 to 245 words. Superlative photo hook, name held to 8 to 17 s, paradox line, Son's real "$70 billion" soundbite, ChatGPT zoom-out, mirrored kicker written first. Check every figure (OpenAI figure from SoftBank filings; the "borrowed it first" kicker claim is unchecked). | here | 2 to 3 h |
| 4 | Format intake | Set 1920x1080, 25 fps on purpose (our default is vertical). Organic. | here | 10 min |
| 5 | Voice, full read, word timings (gate: pick by ear) | `tts.py voices`, 3 or 4 candidate reads with `tts.py say`, user picks. Word timings with `asr_words.py`. | here (needs ELEVENLABS_API_KEY) plus user ears | 1 h |
| 6 | Music and sound plan (gate: pick by ear) | Loud bed, hits on story turns, SFX list. | user picks, plan here | 30 to 60 min |
| 7 | Footage map line by line (`word-matched-broll`; gate: hear the gaps) | About 90 to 120 shots at 1.1 to 1.5 cuts a second. `ytdl.py` for interviews and news, `commons_search.py`, `commons_get.py`, `commons_video_get.py` for licensed stills and clips. Hook photo and soundbite clip first. Rights list per clip. | here | 3 to 5 h |
| 8 | Word-anchored storyboard (gate: approve) | Effect per word from section 2; inverted cuts on sentence turns; cards every 10 to 20 s; 8 to 15 big words. | here | 2 h |
| 9 | 3-second pilot beside the reference (`edit-loop-guard`; gate: approve the look) | Grid reveal, cut-out with rim, place swap, first captions. Side-by-side crop against PAL and ACK at the same timecodes. Matte comes from the Mac. Also a caption crop test (section 10 item 8). | matte on Mac, rest here | 2 to 3 h |
| 10 | Full build and render (gate: say go) | Linux: cuts, inverted frames, logo bursts, cards, video wall, marker push, caption overlay (new script). Mac: person mattes, `counterRow`, zoom blur, any AE effects; JSX checked first with `check_jsx.py`, run with `ae_run.py`. Final assembly in one place (Linux ffmpeg or Premiere). | split | 4 to 6 h |
| 11 | Review notes (`edit-loop-guard`, `broll-scoring`) | Pace check with `skills/minidoc-reference-style/scripts/ref_stats.py` against STUDY.md section 2; mix check with `research/metro-media-house/tools/gap_level.py` (bed 1 to 4 dB under voice in gaps). | here | 1 to 2 h |
| 12 | Finish (gate: final approval) | Loudness, credits for licensed items, no M sting, kicker plus callback shot. Nothing posted by us. | here | 1 h |
| 13 | Feed back | Log what worked into the skills. | here | 30 min |

Total: about 17 to 24 working hours. The peg (SoftBank results, 10 Nov 2026) is 5 days away, so the script and footage stages decide whether we land on it.

## 4. Gaps and risks

1. **Per-word caption tool missing** (effects 8 and 9). `style_captions.py` only restyles a saved Premiere project and was measured on 1080x1920. A new script must place each word at a free x position on its word start. A PIL overlay is the fastest route here (Inter installed, word timings from `asr_words.py`). This is the largest build item and every frame depends on it.
2. **Person matte is Mac only.** `person_mask.js` needs macOS Vision via osascript; `ps_cutout.jsx` needs Photoshop. No Linux matte tool found in the repo. Effects 2, 3, 4 and 14 wait on the Mac.
3. **No OCR here.** Found `ocr.swift` (macOS) and `ocr.ps1` (Windows) in `premiere-ae-editing/scripts/media/`; no Linux OCR found in sprint time. Checking burned-in text in news clips and our caption positions against the reference is by eye.
4. **Footage rights.** News and interview clips are third-party; Commons items carry licences via `commons_get.py`, but wire photos and broadcaster clips do not. The hook photo (Son with Jack Ma) and the "$70 billion" soundbite video are both not found yet. If the soundbite is not found, drop it; never fake it.
5. **Landscape vs our vertical defaults.** Set 1920x1080, 25 fps in every tool call: `screen_push.py` defaults to 1440x1080 at 30 fps; `style_captions.py` numbers are from 1080x1920. Check every block's default size and fps before use.
6. **Taste conflict.** effects-library README marks `pixel_reveal` (base for effect 1) as "breaks our taste, do not use unless asked", and the inverted-frame cut is close to the glitch family. Settle both at the 3-second pilot gate.
7. **Wrong tool cited in STUDY.md.** Effect 13 points to `hail_mary_highlight_streak` for the marker; the marker is in `screen_push.py`. STUDY.md not edited here (rule).
8. **Facts.** OpenAI stake figure has conflicting sources (rated C in IDEAS.md); the kicker's borrowing claim is unchecked; no investment advice. Stargate photo is political if used.
9. **Unknowns not checked in sprint time:** HyperFrames install state, a thermal-flash tool (effect 6), music tempo (STUDY.md measured loudness, not tempo), ElevenLabs key presence, `ytdl.py` against YouTube bot checks through the proxy.
