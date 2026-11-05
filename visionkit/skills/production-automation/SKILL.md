---
name: production-automation
description: Design, run, extend and debug automated or batch video production. Daily news post runs (scan, verify, one batch JSON, build, contact sheet, Drive delivery, posting schedule), template builds of cards, carousels and short videos (HTML templates through headless Chrome plus ffmpeg), Premiere projects from generated FCP7 XML or .prproj edits, After Effects elements from scripts, beat maps and plan-to-After-Effects builds for music edits, bulk long cuts and shorts with an ffmpeg renderer, review pages, QA gates and contact sheets. Also render pipelines (parallel encodes, encoder picked by a VMAF test, part caches, two-pass loudness, NVENC or VideoToolbox), scheduling, unattended runs, handover and known failures. Use it when the user says today's batch, daily run, newsdesk, studio, automate, pipeline, template, batch render, spec, review page, schedule, overnight, launchd, faster renders, or wants posts, edits or cutdowns at volume.
---

# Production automation

How we build and run pipelines that make posts, edits and cutdowns at volume, and the rules that kept them good.
Everything here was learned on real jobs (Sept to Oct 2026). Tool mechanics (prproj_lib, fcpxml.py, ae_run.py,
frames.py, loudness tools, YouTube downloads) live in **premiere-ae-editing**; this skill is about the pipeline around
them: what decides, what gets built by which engine, how a batch runs, how it is checked and handed over.

## The pipelines
| Pipeline | Makes | Engine | Typical run | Read |
|---|---|---|---|---|
| Daily news desk | daily music and news posts: cards, carousels, 9:16 headline and tweet videos, Story stills, captions, a posting schedule | HTML templates in headless Chrome, ffmpeg compositing, Premiere layers + FCP7 XML per video | scan, write `batches/<date>.json`, build, contact sheet, deliver | references/daily-news-run.md |
| Edits kit (`library/pipelines/edits-kit/`, included) | beat-synced "cracked" sports music edits | song map + footage catalog + a ~100-line plan script; assembled in Premiere, After Effects for effect elements | `setup_edit.py`, `plan_NN.py`, `planview.py`, `build_edit.py` + `ae_run.py` | references/music-edit-builds.md |

The edits kit and `library/pipelines/youtube-research/` (search and storyboard sheets without downloading) ship with
this repo. The news desk is documented as a design in its reference: build it from those notes.

**Before the first run:** copy the pipeline into a working folder, check the platform lines at the top of each script,
and run one test item.

## The rules that matter most
1. **The content bar decides; the pipeline only builds.** A post earns its place on retention, CTR and watch time,
   "not because the system is cool or impressive" (the reviewer). Score stories before building (the interest test in
   social-video-formats, build at 7/10 or more). Why: our first faceless batches were technically clean and still
   "not worth posting"; speed only helps once the content is right.
2. **One spec file is the single source of truth.** Every decision (times, words, crops, sources, audio, versions)
   sits in one batch JSON, plan JSON, edit list or text cut list. Graphics, placement, SFX cues, captions, the
   Premiere XML and the review page are all derived from it. Why: re-runs, versions and reviews point at one file, and
   one timing change moves the graphic, its sound and its cut together (references/spec-driven-builds.md).
3. **Pick the engine per format, not one engine for everything.** Code (HTML to PNG + ffmpeg) for cards, carousels
   and headline videos; After Effects only for animated templates and elements; Premiere for edit-heavy work; an
   ffmpeg renderer plus XML for long cutdowns. Why: news posts are approved or rejected, not hand-finished, and code
   builds a day's 8 posts in about a minute on one machine with no Adobe seat (references/principles-and-build-engines.md).
4. **Code renders, Premiere stays editable.** Every code-built video also ships its layers (clip MP4, overlay PNG,
   WAV) and an FCP7 XML, plus a full-source XML so an editor can slip to any part of the source. Why: the editor asked
   "how can i access directly in premiere", and a 15 s cut layer had nothing to slip to.
5. **Compile in Premiere; After Effects makes elements.** Plates, stills, screenshots, text and simple moves are
   Premiere layers; After Effects renders alpha elements that a builder places. Why: a presenter baked into 17 renders
   meant 17 re-renders for one change to the presenter. Music edits follow it too (decided 15 Oct 2026): Premiere
   assembles them and After Effects only makes the effect elements; the single live AE comp is the old route.
6. **Measure before you redesign, and test small before you roll out.** Count words on screen, cuts per 10 s, sync
   on strong hits, loudness, against the references; then build one item per type before the batch. Why: numbers
   turned "looks designed" into 8 concrete fixes, and a 9 s test caught "not this many movements together" before a
   10 minute video was built that way.
7. **Cache everything slow, keyed on every input.** Render parts, mattes, catalogs, transcripts, embeddings. Why: a
   cached fix took 49 s against 2 min for a full render; a cache keyed on too few inputs once showed stale crops.
8. **Fix the generator, not the output.** A systematic miss becomes a toolkit default or a guard, and review notes
   marked "keep this in mind" or "don't fix these" change the defaults, not the delivered files. Why: the same bug
   comes back on the next item otherwise.
9. **Never overwrite what was delivered.** Undelivered drafts are fixed in place; delivered files get `_v2`, `_v3`
   automatically; superseded drafts move to `_superseded`, never deleted. Why: "do not replace this one make version
   2. keep that in mind always" (the editor), and stray versions blur what was actually sent.
10. **Keep a human gate where judgment lives.** A person approves the daily slate, checks one contact sheet, and posts
    in the app with the client's sound. Automatic changes default to "do nothing" until a measured trigger fires.
    Why: the sound must be attached in-app, and an auto-crop rule that fired on 74 of 171 items drew "overuse of crops".
11. **Every number is real, sourced and time-stamped.** Numbers come from data at build time, never typed by hand;
    placeholders (page identity, scores, prices) are labelled and listed on the review page. Why: one exposed fake stat
    ends a page's credibility, and date-bound posts ("tonight") go stale within hours.
12. **One heavy job at a time; hold renders when the machine is busy.** Renders, GPU jobs, preps, After Effects and
    downloads queue behind a gate. Build everything light, then wait for "go" if the user is working. Why: "Don't do
    everything all together. So the laptop blows up" (the editor); two heavy jobs once started on top of each other.
13. **State and tools live in the job folder.** A status file ("read first"), a README with the run order, the
    generators and page builders. Never keep the only copy in a session scratchpad. Why: scratchpads get cleaned;
    sessions compact and end; parallel sessions edit the same files.
14. **Fork an approved pipeline per client.** Copy it with its own brand file, batches, finals and delivery folder;
    never edit the original for another client. Why: one change for a new client must not break the pages already
    posting from the original.

## Order of work: a new automated format
1. **Prove the content first.** Research real winners frame by frame (research-and-sourcing), then a plan page with
   proof frames and one mock frame of any new look. Build nothing big until the decisions are answered. Why: research
   once favoured a text style the editor called "TOOO off beat"; one mock frame would have caught it.
2. **Write the spec format.** Decide the fields a person edits per item (references/spec-driven-builds.md) and what
   the generator derives. Keep the brand, CTA and accounts in one config file.
3. **Pick the engine** (rule 3) and build the template or builder library. Fonts load from files; text fits by measuring.
4. **Validate specs before building:** paths exist, in/out inside the source, sound names resolve, music covers the
   cut, events snapped to frames, no number typed by hand.
5. **Build one item per type**, then one contact sheet; fix; only then the full batch.
6. **Measure the output against the references** (references/review-pages-and-qa.md) and fix by numbers.
7. **Gate and deliver:** QA gates, a review page or a hand-over table, versioned finals in a clean folder.
8. **Feed every verdict back** into the defaults, the guards and the skill notes; keep a dated rule log.

## Order of work: a daily or batch run
1. Read the pipeline's status file and README. Check logins, disk space, power and whether the user is busy.
2. Scan or pick (data first: scans, heatmaps, outlier scores, archives), then shortlist against the content bar.
3. Verify facts at primary sources and choose the one added fact per post (research-and-sourcing).
4. Source assets one download at a time; log every borrowed file (URL, author, date, licence, burned-in text).
5. Write the spec (`ls` the path first; unique names). Validate it.
6. Build (one heavy job at a time). Rebuild only what failed (`--only`).
7. Look: one contact sheet per batch; frame 0 of every video; numbers against the data.
8. Deliver: finals folder plus Drive copy, captions file, schedule with posting windows, Premiere layers + XML.
9. Hand over: one table per page or per cut, what was left out and why, what was checked where, open questions.
10. Record verdicts as rules and defaults. Delivered items change only as new versions.

## Render rules on one screen (details: references/render-pipeline.md)
- Encode in parallel parts (3 to 4 at a time) and cache each part under a hash of its exact ffmpeg command plus the
  input's size and modification time, so a fix re-encodes only what changed.
- Pick the encoder and its quality setting by a VMAF test against the source (95 or more = visually lossless), timed
  as one job and as parallel jobs. Windows result: NVENC cq 21 (VMAF 99.85, about 6x real time). On a Mac test
  `h264_videotoolbox` / `hevc_videotoolbox` against libx264 the same way.
- Long mixes: two-pass loudnorm to -14 LUFS (TP -1, LRA 20, linear) then a limiter at 0.70, AAC with `-aac_pns 0`, and
  a true-peak re-check. Short posts: one-pass loudnorm I -14, TP -1.5, LRA 11 plus a 1 s fade-out.
- Frame exactness: parts as MPEG-TS, trim with `-frames:v`, seek a quarter frame in, pad inserts at another frame
  rate, use the stream's nominal rate, decode front to back for QC.
- After Effects: one AE, one render-queue item at a time, a 2 to 6 s test or a `--range` render first, ProRes for
  finals, never kill AE while a file still grows. Premiere: Export mode, one sequence at a time, never the AME queue.
- Measure every render (duration, frames, LUFS, true peak) before handing it over.

## Running on a Mac
- Use a Python venv (Homebrew Python is "externally managed") and `python3 -X utf8`.
- Chrome: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`. Fonts: `~/Library/Fonts`, `/Library/Fonts`,
  `/System/Library/Fonts/Supplemental`; licensed fonts need real font files (Adobe Fonts gives no file path).
- GPU: CUDA code needs a device switch (`mps` if available, else `cpu`); NVENC becomes VideoToolbox or libx264;
  Windows OCR becomes Apple Vision; faster-whisper on CUDA becomes mlx-whisper or CPU.
- Keep-awake: `caffeinate -i`; always-on jobs via launchd, not the chat.
- After Effects from scripts: premiere-ae-editing `ae_run.py` has a Mac route (AppleScript `DoScript`; see its
  mac-notes.md), or render a saved project with `aerender`.
- Check the ffmpeg build: `ffmpeg -filters` for `subtitles`, `vmaf`, `drawtext`; `ffmpeg -encoders` for videotoolbox.

## Accounts and keys you may need (set keys as environment variables, never in files)
- Adobe Premiere Pro and After Effects (Photoshop for the cutout scripts).
- Google Drive for desktop, if delivery goes to Drive. Posting stays manual in the app.
- Throwaway X and Instagram monitoring accounts (never the pages or a personal account); Claude never types passwords.
- A throwaway YouTube account's cookies file only if YouTube blocks downloads.
- A music licence that covers client work, with channels safelisted.
- Free API keys for stock (Pexels, Pixabay) and a Freesound login, if the stock steps are used.
- Optional: Hugging Face token (speaker labels), ElevenLabs key, font licences, model downloads (SAM 2, CLIP).

## Traps that bite first (all: references/debugging-and-failures.md)
- Never generate code through shell heredocs; write files with the Write/Edit tools, build JS strings with
  `json.dumps`, parse-check (`py_compile`, esprima) before running, and grep that a patch landed.
- The Write tool turns `\uXXXX` escapes into real characters: build non-ASCII constants with `chr()`.
- Empty results are errors: a geo-blocked source returns `[]` with no error. Alarm on "fewer than N rows".
- One YouTube call at a time across all processes (about 15 parallel calls got a 15 minute bot block).
- Never delete nodes on someone else's web app to hide a pop-up (it crashed the React page); hide with CSS.
- Strip accents in every name matcher (NFKD): "Atletico" vs its accented spelling broke matching twice.
- An FCP7 XML with one unresolvable clip is refused whole: run `fcpxml.py --check` on every XML you hand over.
- Background jobs and watchers die when the user closes things; After Effects keeps rendering. On resume, check DONE
  flags, logs and file sizes before re-running anything.
- `ls` before writing a spec file; one batch file was overwritten and had to be rebuilt from the transcript.

## Reference map
| File | Read it when |
|---|---|
| references/principles-and-build-engines.md | designing a pipeline; choosing code vs Premiere vs After Effects; layers + XML; versioning; forks; caches |
| references/spec-driven-builds.md | writing a spec format; deriving graphics, placement and SFX from one list; validating; patching changes |
| references/render-pipeline.md | stills and video from HTML, ffmpeg recipes, parallel parts, VMAF, loudness, AE and Premiere renders, gating |
| references/daily-news-run.md | running or extending the newsdesk: scan, ranking, fetch, batch fields, templates, Drive, schedule |
| references/music-edit-builds.md | the edits kit: beat maps, catalog, mattes, plans, planview, AE build, QA, Mac port |
| references/cutdown-batch-pipeline.md | bulk long cuts and shorts: prep, cut lists, snap and audit, round scripts, renderer, XML, review diff |
| references/review-pages-and-qa.md | review and plan pages, contact sheets, QA gates, measuring output, baseline diffs, hand-over reports |
| references/scheduling-and-unattended-runs.md | queues, unattended loops, holds and pauses, keep-awake, launchd, status files, agents |
| references/debugging-and-failures.md | something broke: every failure we hit with cause, fix and prevention |

## Sibling skills
- **premiere-ae-editing**: .prproj and XML mechanics (prproj_lib, fcpxml.py), After Effects runner and libraries,
  frames, loudness, transcription, OCR, downloads, Mac notes for the apps.
- **editing-playbook**: cutting, hooks, B-roll, sound taste, review rounds and the verdict library.
- **motion-design**: effect vocabulary, flash recipes, type, the effects library.
- **research-and-sourcing**: finding and verifying news, footage, music and SFX; licences; research agents.
- **social-video-formats**: the content bar, platform rules, posting windows, formats that perform.
- **meme-compilation-edit**: the narrated meme compilation pipeline (its own planning, QA and EDL tools).

Sources: real production jobs, Sept to Oct 2026.
