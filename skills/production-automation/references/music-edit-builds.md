# Music edit builds (`edits-kit/`)

The free in-house kit for beat-synced "cracked" sports music edits: one command prepares a song and its footage, a
plan script of about 100 lines describes the edit, a preview checks the framing without rendering, and one layered
After Effects comp is built and rendered. Built 13 to 14 Oct 2026; the pilot went v1 to v8 and wave 1 (three edits,
three bases) took about 1.5 hours. The effect vocabulary, flash recipes, type rules and the taste verdicts (what was
loved, what was banned) are in motion-design and editing-playbook; this file is the machine and its numbers.
Since 15 Oct 2026 the one-comp build described here is the old route: music edits are assembled in Premiere and After
Effects only makes the effect elements (section 10).

## 1. The chain
| Step | Tool | Gives |
|---|---|---|
| 1 Setup | `setup_edit.py EDIT_DIR SUBJECT --song <file or YT id> --footage <id,id> [--max 1080]` | `song/` (song.wav 48 kHz, song_22k.wav, beats.json, words.json), `footage/` (fNN_*.mp4), `catalog/` (catalog.json, embeddings, thumbs, sheets), folders for mattes, ae, renders, qa; every step cached, re-running skips what exists |
| 2 Song read | `tools/yt.py` with `search`, `meta` or `heat` (YouTube metadata and the most-replayed curve, no downloads), words, loudness | where the drop, the hook and the strong hits are; the most replayed stretch |
| 3 Base | `STRUCTURES.md` (12 bases), `RESEARCH_V2.md` | the story shape for this song, subject and footage |
| 4 Shots | `catalog.py strips / sheet / search`, `cutcheck.py` | the exact second inside each shot; hidden cuts found |
| 5 Plan | `edits/NN_name/plan_NN.py` using `tools/plankit.py` | the edit as JSON; `save()` prints the sync report |
| 6 Preview | `planview.py plan.json out.png` | crops, mattes and type boxes at start, middle and end of every clip, with safe lines; no render |
| 7 Test new effects | a test-reel plan (one real cut per technique, 1.2 s each) + `compare.py --stats` | proof the effect matches the reference frame by frame before it goes in an edit |
| 8 Build | `build_edit.py plan.json [--only-test S] [--range A-B] [--final]`, then the skill's `ae_run.py <jsx>` | a layered .aep (every clip, word, hit and transition live) + an H.264 preview, or ProRes 422 with `--final` |
| 9 QA | `anatomy.py`, `moments.py`, `qasheet.py`, audio subtraction | sync on strong hits vs chance, effect density vs references, labelled frame windows |
- Run setup and the GPU tools without `python -I` on Windows (torch, open_clip, faster-whisper and yt-dlp sat in the
  user site-packages). On the Mac use one venv.
- Caches: footage catalog, CLIP embeddings, re-ID galleries, reframe paths, mattes keyed by file + range + prompt.

## 2. Beat maps
- **Hits:** the skill's `beats.py` gives kicks, snares, tempo and per-frame loudness. `cuts.hits()` merges a kick and a
  snare within 0.03 s into one hit (keeps the stronger) and scales strength 0 to 1 relative to the loudest hit in the
  edit window.
- **Snap:** `cuts.on(t)` takes the strongest hit within +-0.2 s of a planned cut, scored `s x (1 - 0.5 x distance /
  0.2)`, and floors it to a frame, so cuts land 0 to 1 frame BEFORE the hit, like top edits: the picture may lead the
  sound, never trail it (sound arriving early is noticed at about 45 ms, sound arriving late only at about 125 ms,
  ITU-R BT.1359). Why: a fixed beat grid drifts off a real performance (snares swung up to 0.15 s) and strong hits
  are not evenly spaced. Sync went from 31% of cuts on strong hits (chance 27%) to 54 to 62%.
- **Report before rendering:** `python3 cuts.py PLAN.json BEATS.json SONG_IN` lists every cut with its nearest hit,
  offset in frames and strength; a cut counts when the hit's strength is 0.5 or more and the offset is -1.5 to +0.5
  frames.
- **Known flaw (fix not built):** strength is scaled to the loudest hit, so a song with a big level jump (a
  beat-switch drop) fails the report in its quiet part: one edit read "5/19 cuts on a strong hit" although most cuts
  sat within 1 frame of hits of strength 0.13 to 0.35. Normalise strength per loudness section (or per 4 bars) before
  snapping and reporting.
- **Words:** titles and lyric words use Whisper word times floored to a frame (`F()`); cuts use the strongest hit
  (`C()`). Lyric moments beat drum hits when the words matter (one edit: 13 of 24 cuts on strong drum hits by design,
  the rest on lyric words).
- **Frame arithmetic:** frames per beat = 60 / BPM x fps; 150 BPM at 30 fps = 12 frames (a 16th note = 3 frames); a
  slowed 70 BPM = 25.7 frames. Trust the kick/snare list over the BPM: detectors read half or double time (one song
  measured 138, 94 and 70 BPM in different runs).
- **Snap every event to its frame** (`snap_plan`: round(t x fps) / fps minus 0.1 ms). 4-decimal plan times had put a
  third of all cuts and hits of v1 to v3 one frame late.
- **Pick the song window from data:** start one beat before the drop, include the song's most replayed stretch (the
  YouTube heatmap), end on a section's last downbeat plus one bar.
- **Sync the transition's peak, not only the cut frame** (the white frame, the streak peak or the fullest flash panel
  on the beat): motion-design.

## 3. Footage catalog and hygiene
- `catalog.py build | tag | strips | idscore | search | sheet`: splits packs into shots (scan at 64x36, thumbs 224x126
  at 5 per second, shots under 0.4 s dropped), scores motion and sharpness, tags scale, action and kit with CLIP
  ViT-L-14 (`laion2b_s32b_b82k`), scores how clearly the subject is in each shot (re-ID), and searches by text. Sheet
  selectors are explicit (`ids:a,b`, `q:text`, `from:K`): an id list was once read as a text search.
- **Pick the moment inside a shot from strips** (8 frames per shot labelled with source seconds): one shot showed shins
  instead of the foot on the ball; another had the player chasing, not on the ball.
- **Hygiene before cataloguing:** rename files to ASCII (`fNN_name.mp4`; emoji names tripped the tools); detect the
  real picture area inside pillar or letter bars from the median frame (`active_area`); crop burned-in captions with
  `keep_above(k, y, zoom)` (zoom 1.35, or 1.6 for a score bug); frame a watermarked pack low at zoom 1.2 so the band
  starts below the watermark; check every chosen range for hidden cuts (`cutcheck.py`: correlation under 0.45, or a
  luma jump over 16 and 3x the local median; found in 4 shots).
- About a third of fan-pack "action" shots hide the subject (pilot 110 of 167 clear, a boxing pack 35 of 67, a
  basketball pack 49 of 103): score before planning.
- **Limits:** the re-ID gallery and the CLIP tag prompts were football-specific (one club's kit): they picked the wrong
  player in other kits and were reused for boxing and basketball. Give a box at a named time, and write per-sport
  prompts. 1080p broadcast wide shots go soft past about 1.8x zoom; source quality is part of the look, so ask for 4K
  packs when downloads are blocked.

## 4. Mattes and framing
- `roto.py CLIP OUT.mp4 [--box | --point]`: SAM 2.1 large tracks the subject both ways from the prompt frame;
  guided-filter edge refine (r = W/240, eps 2e-3), core firm-up `(a - 0.15) / 0.7`, temporal blend 0.75/0.25; writes
  a grey H.264 matte; about 8.5 fps at 1080p on a 12 GB RTX laptop GPU; keeps hair curls.
- `automatte.py`: a matte for every clip range (prompt = box, point, the re-ID person or the largest person), cached
  with the prompt in the key; framing from the matte (head and shoulders = centre of the top 45% of the shape,
  smoothed, speed capped); `auto_zoom` (subject to about 55% of the frame height, capped at 1.5 to 1.8); `comp_point`
  (the head in comp pixels, so a number can sit right behind it).
- `reframe.py`: Faster R-CNN v2 person detector about every 1/15 s on 960-wide frames (boxes over 8% of the height), a
  CLIP re-ID gallery of 40 crops from close shots (top 60% by mutual similarity), switching target only when sure
  (score above 0.62 and 0.03 over the rest), 0.4 s smoothing, a speed cap of 0.6 widths per second. Now mainly gives
  the re-ID person for the matte prompt.
- Wrong-person mattes (defenders, a keeper, a team-mate's arm) are fixed with a hand box at a named time; `planview`
  shows them before any render.
- One GPU job at a time: mattes for two edits at once competed for the 12 GB card.

## 5. The plan
- `plankit.Edit`: `add`, `hit`, `tr`, `number`, `title`, `lyric_line`, `strike_name`, `caption`, `keep_above`,
  `keep_left_of`, `side_x`, `subj_src`, `strong`, `save`; helpers `ramp_rk` (speed ramps anchored on a hit),
  `stutter_rk`, `active_area`, `fit_caption`. A new edit plan is about 100 lines.
- Plan keys (times in edit seconds; the full list is in `build_edit.py`'s docstring): `name, w, h, fps, dur, audio
  {file, in}`; `clips` [{file, t0, t1, src or rk (time remap pairs), speed, focus, zoom, smooth, matte, fit}]; `look`
  (Lumetri values, vignette, grain); `overlays`; `words` [{text, t0, t1, style, font, size, color, x, y (the baseline),
  tracking, behind CLIP or the bar layer, sub}]; `hits` [{t, punch, shake, flash, expo, sil}]; `band` [y0, h] (the
  letterbox picture band, for example [560, 800]); `popouts`; `zoomcuts`; `fade`; `bloom`; `transitions` (named types
  and per-frame recipes); `breaths`. Rejected devices stay in the code for the record and are not used: whips and
  swipes, spins, closing shutters, box or checkered glitches ("PowerPoint" as plain devices), auras, reticles and the
  lock-on ring, the charging battery. Geometry is fine only as the flash panels he described, done well and mixed with
  flashes (the verdicts and their nuance: motion-design effect-vocabulary-and-taste.md).
- `typeset.py measure | line | fit`: real font widths and cap heights by PostScript name, so type boxes are exact (a
  guessed width put a caption off both edges).
- `planview.py PLAN.json OUT.png`: every clip's crop at start, middle and end with its matte tinted red, type boxes
  yellow and the 10% / 76% safe lines cyan. It caught 4 framing problems in one round with no render.
- Test reel for any new technique: one real cut per technique (1.2 s each, about 45 s render), compared with the
  reference frames by `compare.py --stats` (per-frame mean luma, luma spread, colourfulness) and tuned until the rows
  follow the reference. Only then use it in an edit.

## 6. Build and render
- `build_edit.py` writes `<plan dir>/ae/<name>.jsx`, builds and saves the layered .aep, and renders
  `<plan dir>/renders/<name>.mp4` (H.264 with audio) or a ProRes 422 .mov with `--final`. `--range A-B` sets the comp's
  work area and renders one moment; `--only-test S` renders a short test first.
- Cost of a 30 s 1080x1920 layered edit on the Windows laptop: v2 about 2 min, v3 82 s, v4 104 to 111 s, slower once
  every clip carried Motion Tile.
- Libraries: `tools/ae/edits_lib.jsx` (footage with remap, focus, zoom, band, mirror extension, audio off; punch, shake,
  flash, exposure pop, overlays, looks, slam words, captions, mattes, cut-outs, silhouette strobes, outlines, colour
  pop, zoom cut, flickers, colour flash, RGB split, posterize) and `tools/ae/fx_lib.jsx` (per-frame recipes, optical
  transitions, flash panels, type flash, freeze clone, ghost trail, pop freeze, photo print, outline text, strike
  word). ES3; they load after the skill's `ae_lib.jsx`.
- `overlays.py OUT --palette warm|cool|...` and `sfx.py OUT` regenerate the overlay pack (light leaks, light-bar
  sweeps, film burns, flare streaks, rendered at quarter size then upscaled) and procedural SFX (whooshes, impact,
  riser, glitch, 48 kHz stereo): ship the scripts, not the media.
- **Toolkit defaults that fixed systematic misses** (fix the kit, not the plan): `snap_plan`; footage audio off in
  `clip()` (clip audio mixed into the song in v1 to v4, "A MAJOR BUG is audio"); no mirrored band extension on pop-outs
  (a mirrored head showed over the title); `side_x` (a narrow numeral behind a centred player vanished); `active_area`;
  `keep_above`; `fit_caption`; front words emitted after cut-outs (they hid behind the player); Motion Tile on each
  footage layer, never on an adjustment layer (a 9000% stretch ran the GPU out of memory).

## 7. QA before showing (every version)
- `anatomy.py` on the render: sync on strong hits against chance.
- `moments.py VIDEO OUT [--n 8 --win 12]`: the 8 most intense 12-frame windows (change, invert = correlation below
  -0.25, hue, blur, white) at least 1 s apart, every frame laid out, plus per-10 s density counts. Density targets
  measured on the picture band (crop letterbox bars first or every white frame is hidden): 20 to 35% of frames in a
  transition or effect state, a transition on every cut, about 5 white frames per 10 s, 25 or more colour bursts per
  10 s. v5 had about 1% and read "basic"; the top three references had 108 to 116 blur or transition frames and 6.3 to
  10.8 white frames per 10 s.
- `qasheet.py VIDEO PREFIX "a-b,c-d" [step] [w] [cols] [--crop] [--grid N]`: labelled windows at every changed moment
  at full size; `--crop` for ball contact or a face in a wide shot, `--grid` to read coordinates for prompts.
- One pass over the whole render every third of a second.
- Audio subtraction: cross-correlate the render's audio with the song (to find the AAC delay), subtract, and check the
  remainder: v5 was 27 dB under the song at 0.99 correlation, so no clip audio was leaking.
- On-screen facts listed for the human to double-check before posting (dates, records, ages, draft picks).

## 8. Measuring references (study tools)
- `anatomy.py VIDEO OUT --name N`: shots, cuts (correlation under 0.35, or under 0.6 with histogram under 0.55, with
  blank-aware logic), flashes, breaths, the drop (the biggest 1 s rise), recurring motifs (shot pairs with correlation
  over 0.9 and histogram over 0.75 at least 1.5 s apart), letterbox crop from the median frame, kicks and snares (strong
  = 0.5, 0.005 s phase grid), sync vs chance for strong hits and the 8th-note grid. Calibrated on the editor's own edit
  (26 shots, median 0.62 s, matched the hand count) and it found a progress motif automatically.
- `study.py REFS OUT [--words]` runs anatomy (plus Whisper words) over a folder of references and skips done ones.
- `compare.py OUT "ours@t|ref@t|label" ... --stats` and `cmp_fxtest.py TAG` compare our moments with the reference
  frame by frame.
- Every-frame contact sheets and version diffs (`fsheet.py` in premiere-ae-editing) when effects last 1 to 3 frames.

## 9. The research bank page (`edits-kit/bank-page/`)
- `build_page.py` parses the research lane files (a shared brief fixes the entry format) into one filterable page and
  prints a parse report per file, so format drift is visible (H1 headings and marker variants once dropped entries);
  `page_assets.py` (filmstrip, key frames, loudness, hits for "our edit"), `framestats.py` (per-frame stats and version
  diffs), `timeline.py` (frame stats + audio events), `picks.py` (big crops of chosen frames).
- The page was a private Artifact with database collections "marks" (item -> want / note) and "finds" (user-added
  links). Read them at the start of the next phase, but do not wait for marks: none were made.
- Edits found by 2 to 4 research lanes independently are the real standouts: sort "top picks first".

## 10. Open items
- Sync-report normalisation per section; per-sport prompts and per-kit re-ID; a better shot-cut detector (dissolves,
  replays).
- Premiere assembly (decided 15 Oct 2026): music edits are assembled in Premiere and After Effects only makes the
  effect elements. The one-comp build in section 1 is the old route.
- Not built: glass shatter, depth-map strobe (needs a free depth model and an OK to install), material strobe, a 3D
  extruded word (Blender), world swap, rays shake; RIFE slow motion and Real-ESRGAN upscaling (planned, not installed);
  a 13 s loop cut of every edit.
- Long-term aim: automate these edits like the news posts (spec in, render out), once the taste is stable.

## 10b. Extending the kit
- **A new technique:** build it as one function in `fx_lib.jsx` or `edits_lib.jsx`, expose it as a plan key or a
  `transitions` type in `build_edit.py`, render a test reel of it on real cuts, compare frame by frame with the
  reference, and only then use it in an edit. Record the user's verdict next to it (kept, short only, banned).
- **A new base (story shape):** add it to `STRUCTURES.md` with its measured numbers and a "when to choose" line; add a
  plankit helper if it needs a repeated device.
- **A new sport or subject:** write per-sport CLIP tag prompts and give re-ID boxes at named times; check the subject
  score per shot before planning.
- **A new edit:** copy the newest `edits/NN_*/plan_NN.py` as the template (about 100 lines), never edit an old
  version's plan in place; every render gets a new version name.

## 11. On the Mac
- **CUDA is hard-coded** in `roto.py`, `reframe.py` and `automatte.py` (`.cuda()`, `device="cuda"`,
  `torch.autocast("cuda", dtype=torch.bfloat16)`, `torch.cuda.empty_cache()`). Use a device variable: "mps" if
  available, else "cpu"; autocast with float16 on MPS or none. SAM 2 runs on MPS with a "preliminary support" warning
  and is slower: test on a 2 s clip first. `catalog.py` already falls back to CPU.
- **NVENC is hard-coded** in `roto.py` for the matte encode with no fallback: use `h264_videotoolbox` or libx264
  (CRF 12 to 14 for mattes). `overlays.py` already falls back to libx264. Untested on his Mac.
- **Paths:** the original tools loaded a Windows Arial Bold for sheet labels, searched only Windows font folders in
  `typeset.py`, and pointed `build_edit.py`, `setup_edit.py` and `study.py` at the skill's scripts on the old machine.
  In the kit copy (packaged 14 Oct) these are already fixed: Mac Arial Bold
  (`/System/Library/Fonts/Supplemental/Arial Bold.ttf`), the Mac font folders, and `PAE_SCRIPTS` (default
  `~/.claude/skills/premiere-ae-editing/scripts`). CUDA and NVENC above were NOT changed. Adobe Fonts activated through
  Creative Cloud are not in any font folder: install the font files. The worked plan scripts find the kit folder
  relative to themselves, so they run from wherever the kit was copied (their media paths still need the job's files).
- **Running AE:** the skill's `ae_run.py` switches to its Mac route by itself (it sends the .jsx into a running AE
  with AppleScript `DoScript`, refuses to replace a project the user has open, and quits only an AE it launched;
  premiere-ae-editing mac-notes.md); the scripting preference must be ticked by the user. Or render the saved .aep with
  `aerender`. `build_edit.py` through that route is untested. The
  libraries are plain ES3 with built-in effects (CC Radial Fast Blur, Motion Tile, Threshold, Find Edges, Minimax,
  Shift Channels, Posterize Time, Exposure, Lumetri, Glow): they should port; re-run the effects probe
  (`tools/ae/probe/`) on his AE to confirm match names and render template names first.
- **Python:** a venv with PyAV, numpy, Pillow, torch + torchvision (Mac wheels), SAM 2 from Meta's repo, open_clip_torch
  (downloads ViT-L-14 weights on first run), faster-whisper (CPU int8 is fine) or mlx-whisper, yt-dlp + Deno, ffmpeg.
  Install SAM 2 after its dependencies: `setuptools wheel hydra-core iopath` first, then `pip install
  --no-build-isolation --no-deps` with `SAM2_BUILD_CUDA=0` (pip's build isolation otherwise re-downloads torch, 2.7 GB);
  SAM 2 then skips its fill-holes post-processing with a harmless warning. Model weights (SAM 2.1 large is 898 MB) are
  downloaded on his machine, with his OK.
- **Fonts used:** Coolvetica Heavy Comp (titles, lyric words, type flash), Galano Grotesque Black (numbers, outline
  numerals), Proxima Nova Semibold / Extrabold (captions, labels): he needs his own licensed files.
