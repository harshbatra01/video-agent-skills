# Spec-driven builds: one list drives graphics, placement and sound

Every pipeline we trust has one human-readable spec per batch or edit. A person (or Claude) edits the spec; scripts
derive everything else. Why: re-runs, versions and reviews all point at one file, nothing drifts apart, and a change
is one edit plus one rebuild.

## 1. The spec types we used
| Spec | Pipeline | What one entry holds |
|---|---|---|
| Batch JSON (`batches/<date>.json`) | daily news posts, faceless posts | per post: id, format, page, headline with colour markup, sub, label or logo, theme or accent, caption, posting window, photo(s) or clip {path, in, dur, focus, fill, crop, pre-filter}, audio {mode, song, song_in, bed_db}, subtitles, slides, Story still + poll, pinned comment, history; a batch `note` with the sources checked and the stories skipped and why |
| Overlay spec list (Python) | ads with many animated captions and cards | per overlay: kind, start and end in absolute sequence seconds, words with their spoken times, count windows, highlight rects |
| Edit list (Python) | a 10 minute explainer | per one-minute block: video shots, voice pieces with source in-points, music, SFX as (path, seq_in, seq_out, src_in, level_db, label); shared scene definitions so recurring shots match |
| Plan JSON (from a plan script) | music edits | name, size, fps, duration, audio {file, in}, clips with time remap, focus and zoom, look, overlays, words, hits, band, pop-outs, transitions, fade (full key list in references/music-edit-builds.md) |
| Text cut list (`cut_long_v1.txt`) | long cutdowns | header lines `key: value`, `[hook]` and `[story]` sections, one `IN > OUT \| note` line per clip with anchors, `!insert FILE gain=+4.5` |
| Plan files keyed by sequence id prefix | changes to an existing Premiere project | B-roll plan, external clip plan, zoom plan, graphics plan; one builder applies all of them |
- Times are written as anchors where the material allows (a word, a subtitle edge, an exact hold), not as bare
  seconds: times written against one transcript slipped onto neighbouring words when a better transcript replaced it.
- Write the spec to a new or checked path (`ls` first). Keep a `history` list inside an entry when a delivered item is
  rebuilt, so the old settings are not lost.
- A rule change mid-build is a one-line spec edit plus a rebuild: when the editor said "just dont remove previous b
  roll", the plan's `REMOVE` list became empty and the project was rebuilt in minutes.
- Some inputs no script makes (the meme pipeline's 10 ms level envelope, two audio extracts, OCR files, check-frame
  picks, the human decisions file). List every such hand-made input in the README with how to make it, and calibrate
  any threshold that depends on it (room noise should read -72 to -80 dB on a known pause before trusting -70 / -55 dB
  cut thresholds).

## 2. One spec, three outputs (the ads example)
Word timings -> one Python spec per overlay in absolute sequence seconds, then:
1. **The After Effects generator** converts to comp time, builds every overlay, renders each as an alpha element, and
   writes a meta JSON (start, end) plus a geometry JSON (rects, radii, reveal times).
2. **The Premiere builder** places each overlay from the meta file, disables (never deletes) captions whose midpoint
   falls inside an overlay, and builds the live blur under glass cards from the geometry.
3. **The SFX cue generator** reads the same specs and places the sounds (section 4).
- Why: one timing change updates picture, placement and sound together. Evidence: 39 overlays in one round, 11
  targeted re-renders in the next, SFX for 7 ads straight from the specs with only level notes coming back.
- **Shared geometry across engines.** A frosted-glass card = an AE alpha element plus a Premiere adjustment layer with
  Gaussian Blur 42 under a 4-vertex mask whose size is keyed every frame (60 fps) inside the reveal, grow and exit
  windows, read from the geometry file (`x0, y0, w, h1, h2, r, tIn, tOut, tG, dur`). Why: an alpha overlay cannot blur
  the footage below it, and baking the footage into AE breaks "compile in Premiere". Use the same ease function to make
  the AE keys and the exported geometry (per-frame linear keys), so the two engines match exactly.
- **One edit list feeds both the Premiere XML and the After Effects preview**, so they never disagree (the explainer).
  Recurring scenes come from one shared definition file.
- **One timeline file feeds the storyboard renderer, the AE generator and the sound cues** (friend's set): frames,
  cues and placements can then be checked against each other.
- **Review comments map back through the spec.** A small tool turned reviewer timecodes (HH:MM:SS:FF) into the shot
  and the voice line from the edit list, so 45 comments became one work list.
- **Assign assets to the voice automatically** (the meme pipeline): find which asset is on screen from OCR of the
  window title, and when the screen does not show it, match the spoken words against every asset's OCR text. The same
  idea fits narration to tweet cards and voice-over to screenshots; a human reviews the flagged matches.

## 3. Validate the spec before any build
- **In/out inside the source.** "4:50 to 6:05" on a 6:02 video was a typo ("nonono not 6:05, 5:05"): check requested
  times against the duration and ask when they overrun.
- **Every file exists; every sound name resolves.** Resolve SFX by base name through a cached index of the sound
  folders and fail before rendering if one does not ("All 74 sound cues resolved to real files").
- **The music covers the whole cut.** Two previews went silent after 2:14 because the temp track was 133.8 s long;
  nobody noticed until the full cut.
- **No picture gaps, no voice overlaps** in an edit list; every used track continuous and on frame boundaries.
- **No audio cue inside a removed stretch.** Renders failed silently with "src time ... is not inside a kept story
  clip", and a scene flash landed one clip early after an insert shifted the indices: dry-run the audio layout, map
  story positions explicitly, allow 0.5 s nearest-edge tolerance.
- **Events snapped to frames:** `round(t x fps) / fps` minus 0.1 ms. Plans stored 4-decimal times, which put a third of
  the cuts and hits of the first three versions one frame late.
- **Numbers come from data at build time and are time-stamped**, never typed by hand; a market price of exactly 0.5
  with no order book is a placeholder, not a number.

## 4. Sound from the spec
Mechanics only; sound taste and levels by role are in editing-playbook.
- **A house SFX kit, measured once.** Each file: resampled to 48 kHz, trimmed from 10 ms before the onset to the
  -50 dB tail + 30 ms, 2 ms fade-in, cosine fade-out, normalised to -1 dBFS, 24-bit. Stored per file: `peak_t` (first
  point at 90% of a 3 ms envelope), onset, duration, max momentary loudness `m_max`, "phone" loudness after a 250 Hz
  high-pass, and the share of energy under 150 Hz. Name files by role (`ROLE_Name_<8-char id>.wav`) so the kit
  builder globs by role. Why: placement and level become arithmetic.
- **A cue row** = (time the main peak must land, kit sound, level in LU relative to the dialogue, what it marks).
  Clip gain = dialogue integrated LUFS + relative level - the sound's `m_max`. Start = target - `peak_t`, plus a 10 ms
  sync bias (late is fine, early is noticed).
- **Generation rules from the specs** (example set that passed review): main-word pops rotate through 5 variants,
  never the same twice in a row; a tick on a kicker only if its main word lands 0.35 s or more later; drop any tick
  within 0.15 s of another accent; the same brand sting on every code card; rising stacked words pitched +0, +2, +4
  semitones.
- **Lanes:** up to 3 SFX lanes plus a separate bed lane. A sound takes the first lane free 10 ms after the previous
  clip; if none, trim the lane whose last sound peaked at least 0.12 s before (end it 5 ms before the new start); else
  drop it AND report it. The first strict guard silently dropped hits, including the biggest landing in one ad.
- **Mix offline before touching the app.** Rebuild the dialogue exactly as cut (source in-points + existing clip
  gains), add SFX and music in numpy, measure integrated LUFS and true peak, write a preview WAV. It found an existing
  +10 dB clip gain that clipped.
- **Timeline-emitted cues for HTML video.** The template exposes `window.getCues()` (time, name, gain); the mixer
  plays recorded files aligned on their hit points (`hit_offset_s` in `sfx.json`: the attack for hits, the loudest point
  for whooshes and risers, 0 for beds), with a synth fallback; ffmpeg muxes with a 0.15 s fade-in and a 0.8 s fade-out.
  Picture and sound cannot drift. Note: SFX-pack sound under designed graphics was rejected on native social pages;
  use this for explainers and data videos.
- **Scene beds from house sounds** when a borrowed clip carries someone else's song (references/faceless-studio.md).
- **Review-round changes as a patch layer.** Keep each block's original cue list and apply one global list of DROP
  (time +-0.03 s + a name fragment), MOVE (new time, optional new level) and ADD, plus a window where every old cue goes
  (a rebuilt section). Why: every change stays traceable and reversible (54 stale cues removed, 479 SFX in the cut).
- **Never ship download scripts that hold signed links.** Library download links (Epidemic) expire in about an hour,
  so batches of about 14 were written to a small script and fetched at once; those scripts contain signature tokens.
- Music fitting to an ad's length (preview-based shortlist, bar-grid edit planner, baked level shape) is an audio
  mechanic: premiere-ae-editing.

## 5. Changing a built thing through the spec
- **Rebuild only what failed or changed:** `--only id1,id2`, cached render parts, `ONLY=` filters in AE generators.
- **Asset swap by patching copies of generated scripts.** To replace a presenter still in 17 rendered shots: read
  `var BUILDERS = [...]` from each block's .jsx with `json.JSONDecoder().raw_decode`, replace the asset path inside
  each spec, rewrite the ONLY / log / DONE / output paths with regex, assert no unpatched render path remains, write a
  new .jsx + jobs file per block, render only the shots that use the asset into a new folder, relink. Old renders and
  scripts stay valid.
- **After editing a generator, grep the new value in the written .jsx before rendering.** A quoting error once meant
  nothing changed and a re-render repeated the old shots. Regenerate every block after a library edit, because filters
  and specs are baked in at generation time.
- **Swap an overlay's render in place in Premiere** (same in/out and times, delete only the old instance) with the
  prproj_lib helpers (premiere-ae-editing).

## 6. The per-round loop on an existing Premiere project
1. Copy the user's latest save (check Auto-Save too).
2. Import new renders and audio in Premiere by the UI (batches of about 12, folder path typed), save as `vNimp`.
3. Run `build_vN.py` on its XML: new objects appended, untouched objects byte-identical.
4. Structural and semantic validation (references/review-pages-and-qa.md section 3).
5. Install as the next version file next to the old ones; open it in Premiere.
6. Export 30 to 60 check frames at the changed times; one sheet; fix; report.
- Test-render one overlay per type (9 types) before the full batch.

## 7. Generator per block (the explainer pattern)
- A Python generator per ~1 minute of video decides everything (times from the word map, rects from OCR, crops,
  scores, asset paths) and writes short JS specs; builder libraries draw.
- Loop per block: generator -> runner writes one .jsx -> esprima syntax check -> launcher (clean AE, run, wait, grep
  the log) -> frame sheet at in / mid / out -> fix and re-render only what failed. While AE renders, write the next
  block's audio list or builders.
- Preview every 1 to 3 blocks with audio and apply notes before continuing.
- **Script to timed cues.** Tokenise the annotated script's words and `[bracket cues]`, align them to the recognised
  voice words with `difflib.SequenceMatcher(autojunk=False)`, give unmatched words the previous match's time, give each
  cue the start of the next voice beat, and print a beat sheet (file, start, end, text). Why: the script says WHAT, the
  recording says WHEN; ad-libs and pauses move everything.
- Throughput: the full 10:38 rough cut (91 shots, 533 SFX, voice, temp bed) took about 4.5 hours from intake; a
  45-comment review round with 9 new 3D renders about 2 h 20 min; later client rounds 30 to 60 minutes plus renders.
