# Review pages, QA gates and hand-over

How a batch is checked before anyone sees it, how it is shown, and how the user's answer comes back into the tools.
Reading review notes and running review rounds in general is in editing-playbook; this file is the pipeline side.

## 1. Review pages (private Artifacts)
- **One page per batch**, with everything the reviewer needs on one link: small web copies of every post (videos keep
  their sound), each caption with a copy button and its posting window, a "why it works" line with the proof numbers,
  the data source behind every number, posts grouped by format with the best evidence first, and untested formats
  under a "Tests" heading. Why: the boss reviews one link, and every number stays traceable.
- **Keep the URL:** republish from the same source file path; the page went through 6 versions on one link. Keep the
  page builder and its HTML source in the job folder, not a session scratchpad (three pages' sources once sat only in a
  temporary folder). When a page is big, publish only the changed files.
- **Say it is private.** The page is in the account that made it; the user shares it with the boss from its Share
  menu. Pages that hold client revenue data (a Facebook dashboard) stay private.
- **List the placeholders on the page** (page identity "@yourpage" / "Your Page", the CTA line, masked usernames,
  stand-in scores) and what must change before posting (the real handle and avatar, fresh prices on the day, the
  usernames OK). Why: nothing gets posted by accident with a wrong identity or a stale number.
- **Review videos under about 15 MB** so the page loads: 720p, two-pass, a light `hqdn3d` denoise (friend's set).
- **Pages with a database** (Artifact `db` capability) collect marks and comments. The research bank page had
  collections "marks" (item -> want / note) and "finds" (user-added links); read them at the start of the next phase,
  but never wait for marks (none were made). A fuller template (friend's set, an alternative): frame cards (image, id,
  time, voice line, motion note), comments with a timecode or range and an (x, y) pin, sketch strokes, replies and a
  resolved flag, A/B pairs with Pick buttons, an approval button, your reply stored next to each note; after
  publishing, check the database with one probe write, read and delete.
- **Plan pages for a big review** (20 screenshots and vague notes became 50 decidable tasks): every note a task with a
  code (D for decisions, G for all items, one letter per item), an owner (you, me, both), a quick-win flag and a tick
  box saved in the browser; a timeline bar per item showing dead stretches (4 s or more of talking head with no visual
  change); 2 to 3 concrete options mocked on real frames for each vague note, with references; open decisions at the
  bottom; the same link republished as answers arrive.
- **After a rejection, a plan page comes before any build:** proof frames from real winners, the look, the decisions;
  "Nothing new gets built until you've decided". Show one mock frame of any new text style first.
- Per-round notes pages (every removed stretch with timecode, words and reason) were dropped when speed mattered; the
  XML markers carry the reasons.

## 2. Contact sheets
- **One sheet per batch** answers "is everything right?" for a fraction of the tokens: every card plus 2 frames per
  video (at 1 s and at 60%), 216x384 cells, 6 columns, labels on top.
- Prefix every helper output with `_` and skip `_` files when globbing (an old sheet got pulled into the next one), and
  skip layer files (overlays, base clips).
- Split a sheet that is too tall to read (a 1400x3400 stack was "too tall to read in one go"): 2 images of the formats
  that matter.
- **Plan-overlay QC sheets before rendering:** every item exactly as it will appear with its overlays coloured by kind
  (blur boxes, safe zones, cards, type boxes). The music-edit `planview.py` is one (mattes red, type boxes yellow, safe
  lines cyan); the meme pipeline's crop and blur sheets are another.
- Frame-exact sheets for seams: both sides of every white transition and every flagged seam (that is where 4 of 4 real
  misses hid in one round).

## 3. QA gates (automatic, before anyone looks)
- **Structure:** `validate_struct.py` (project against its source) and `fcpxml.py --check` on every XML (premiere-ae-
  editing).
- **Semantic validator per build, one PASS/FAIL line each:** caption and audio track fingerprints unchanged, V1 and
  zoom tracks unchanged, B-roll matches the plan, grade pieces plus B-roll tile the timeline exactly, zoom percentages
  within the plan, graphic texts as intended. Why: a structurally valid file can still break the edit.
- **Reference integrity:** every SubComponent ref points at a VideoFilterComponent with MatchName `AE.ADBE AEMask2`,
  Component refs at `*Component`, Param refs at `*Param`, TrackItem refs at `*TrackItem`, SubClip refs at `SubClip`.
  Why: Premiere said "could not be loaded, may be damaged" on a structurally valid file because a mask template id taken
  from an older save had been renumbered. When Premiere gives no log, build variants that each leave one new feature
  out, open each, and diff a generated object against Premiere's own.
- **Gap and on-frame audit:** every used track continuous from 0 to the end and every clip on a frame boundary (it
  catches the "event one frame late" class).
- **Read back every scripted placement and retry:** scripted placement in Premiere silently fails now and then; stills
  can land a frame short and leave a hole.
- **Cuts by audio level:** flag any cut edge where the audio is louder than -55 dB on both sides; pair it with the
  ASR-based edge-word check.
- **Seams:** sequential-decode seam verify, a QC seam sheet, the edge-shot and edge-word checks before rendering.
- **Loudness and true peak of every render and preview** (references/render-pipeline.md section 6).
- **Facts and numbers:** every number matches its data source at build time (and the app's own on-screen label);
  on-screen facts listed for the human to double-check before posting.
- **Visual checks on the sheet:** frame 0 is a face or the hook, nobody misidentified, no foreign logos, safe zones,
  faces not cropped, no UI the client forbids covering.
- **A dead-frame test** that flags stretches where the picture barely changes (friend's set, content-adaptive).
- **Expect false alarms and judge flags on frame-exact sheets.** The flash detector fired on white dips, narrator fades,
  rain, flashing lights, the source's own subtitle blinks in fast motion, an insert's own animation and coloured
  subtitles; the stray-shot check fired on flashing lights changing colour. The seam check skips white-dip seams (both
  sides mean over 200) and soft seams (change under 8). Each long cut gave 5 to 12 flash flags, nearly all false.
- **Fix before delivery under the same name; after delivery, a new version.** QC found real misses every round
  (subtitles flashing 1 to 5 frames at hook edges and inserts, a borrowed clip, clipped words); one round had 6, all
  fixed and re-rendered before the report.
- From the boss's concept doc, the gates to automate next: loudness, black frames, safe zones, captions in sync, faces
  not cropped.

## 4. Measure your own output before redesigning
Why: it turns "looks designed" or "feels basic" into a list of fixes with numbers.
- **Text on screen:** OCR frames at 2 fps for the first 8 s, then 1 fps up to 40 s, at 720 px wide; count readable
  words and tiny words (under 1.8% of the frame height) at once, and where the text centre sits. Ours against native
  references: 10.5 readable words against 4; 27 tiny words against 0; text centre at 26% of the height against 50%;
  text on 100% of frames against 88%. Tools: `research-tools/textmetrics.py` + `ocr.ps1` (Windows OCR; on the Mac use
  Apple Vision OCR).
- **Cuts:** ffmpeg scene detection at 0.3 for cuts per 10 s (ours 1.1; native posts either held one shot or cut 3+ times
  per 10 s, "the worst of both").
- **Music edits:** sync on strong hits against chance, effect density per 10 s, white frames per 10 s, every-frame
  sheets, per-frame luma / spread / colourfulness against the reference (references/music-edit-builds.md).
- **Reference edits:** a light cut detector over 54x96 greyscale frames with timestamped sheets is enough to read a
  reference's pace; `anatomy.py` gives the full picture.
- **Text density rules that came out of it** belong to social-video-formats and motion-design; the method stays here.

## 5. Learn from the user's fixes (baseline diffs)
- Keep a `delivered_baseline` copy of every project you hand over (the reviewer edits in place). When they send their
  fixed save, diff it per item against the baseline: voice frames removed or added with words and per-frame levels; per
  item span, crop, scale, position and every mask with key times measured against what is said; on-screen rectangles;
  crop and blur sheets with yours in red and theirs in green (the meme pipeline's review tools). For cutdowns,
  `review_diff.py` does this against the timeline JSON.
- Untouched parts count as approvals. Each pattern becomes a dated rule and a code default.

## 6. Hand-over reports
- **Daily batch:** a table per page (window, format, source), what was left out and why, which facts were checked
  where, what to watch next; the sheet and the videos attached.
- **Cutdown round:** a table (cut, length, what the hook shows), the change made for each note, the checks run, the
  mistakes caught, at most 3 "your call" questions, then the approvals needed.
- **Music edit:** each numbered note answered one by one, the render path, facts to double-check, open asks; every
  version kept side by side under its own name.
- **Explainer build notes:** files, every placeholder slot with exact timecodes for the 3D artist, clips to swap,
  questions, fact-check flags, and a comment-status table (one line per comment: time, what changed) that also lists
  the comment numbers NOT received and the assumption made for each.
- **Placeholder discipline:** every stand-in for missing material is tagged "PLACEHOLDER" on screen and listed in the
  notes, so it can never ship by accident.
- **Every report:** say what you could not check ("I haven't heard any of the new audio"); end with 2 to 3 closed
  questions with your default (the user answers in one line); correct your own wrong claims from the last report in
  the next one ("I told you yesterday that ... had been posted twice. That was wrong").
- **Meme-style job reports** (friend's set): counts (items, cuts, masks by type, crops), unused files and why,
  policy-only calls to confirm, anything not checked.
- **Schedule file** for posting (`FINALS/SCHEDULE.md` in the newsdesk): POST / optional / skip per post with its
  window; expired batches marked; stale date-bound posts marked do-not-post.
