# Reviews, versions and delivery

How a review round runs, how far a note reaches, how versions are named and kept, and how to report. The mechanics of
building a round in Premiere (finding the latest save, diffing it, relinking, swapping a recurring asset, checking
changed times) live in premiere-ae-editing references/review-rounds.md.

## Contents
1. Taking the notes in
2. What a note means (scope)
3. Reviewer phrasebook
4. Options and picks
5. Plan pages and review pages
6. Building the round
7. Versions and names
8. Self-check before delivery
9. The report
10. Placeholders and build notes
11. Calibrate on every review

## 1. Taking the notes in
- Read every note with its timecode. The user's own explanation overrides the literal comment ("#3 note for self", "#13
  the info graphic is fine actually"). If they say "hold on, I'm sending explanations", wait.
- Ask once, up front: which piece, timestamp, who said it, any reference, deadline, must vs nice-to-have, which file
  version was reviewed, and to say "that's all" when done. Then map each screenshot to its piece and time yourself.
- Map times to shots in the CURRENT project: the user may have moved things since your delivery.
- Restate the notes as a fix list (in scratch, not in chat). Reviewer notes often arrive as phone screenshots: read them
  post by post, turn vague notes into concrete changes and say your reading back in one line each ("adjust font and a
  few bits" became a readable video font and a bigger clip box). Stating the reading catches a wrong guess before a
  rebuild.
- Check requested in and out times against the source length before rendering ("4:50 to 6:05" on a 6:02 video:
  "nonono not 6:05, 5:05").
- When the user reports a glitch, first check whether their own save caused it (a diff once showed their save had cut a
  1.35 s clip to 10 frames), then fix it and say so.

## 2. What a note means (scope)
- A rejection is about that placement unless the reviewer says "never" ("if u used it elsewhere and i didnt point it
  out there its fine there but here no"). Blanket bans are the ones said as bans: taste-verdicts.md section 8.
- "Don't fix these, apply next" is a common mode: log the rule, change the tool default, apply it from the next piece,
  and do not re-render the reviewed files ("small feedbacks dont change on these videos", "dont fix but keep in mind",
  "dont remake or anything just understand", "Don't fix the reviews on these"). When the user does want fixes now,
  deliver new versions.
- "Dont make the changes just keep this in mind": change the defaults and rules, not the delivered posts.
- Carry each note to every deliverable of the SAME round that shows the same thing (the animatic and the storyboard,
  second reviewer), without being asked twice. Do not reopen pieces from past rounds unless asked.
- Untouched parts of a reviewer's hand re-cut are approvals; whatever a reviewer did not mention is neither approved nor
  banned.
- The reviewer's taste beats research, beats Claude's recommendation, and beats a sibling skill's default.

## 3. Reviewer phrasebook (what they meant)
| They say | They mean | Do |
|---|---|---|
| "corporate", "slow" (ads) | not enough visual change, no stakes | more real footage of the talent, faster changes, music with stakes |
| "show not tell" | B-roll must show the literal line | swap to the exact action or object |
| "boring find ways to make it nice" | plain B-roll with nothing designed on it | add a caption device, a counter, a card |
| "cheap" (a graphic) | the treatment, not the idea | replace it (a green tint became a tracked spotlight) |
| "tooooo cluttered", "too much text man try to show" | too many elements, words instead of pictures | fewer items, show it instead of labelling it |
| "too poster ish, we wanted premium [calm]" | heavy display type on a calm brand | semibold humanist type, smaller, wider caps tracking |
| "PowerPoint" (music edits) | rigid geometry transitions | optical transitions (light, blur, streaks), flash panels |
| "looks ass", "this is ASSS" | rejected outright | remove, do not tweak |
| "TOO long" | abstract frames hiding the picture for 10+ frames | cut to a few frames or drop |
| "basic" / "good wont cut we need GREAT" | competent is not the bar on showcase work | study the top references, raise the device level |
| "these are all SAME types of posts" | variety of skin, not of kind | different formats, footage and moments |
| "the UI is bad", "I can't watch them" | designed data UI on a native page | start again from real moments and one line |
| "TOOO off beat" (a text style) | the look does not fit the house | back to the house look |
| "a bit shorter", "cut stuff shorter" | tighten, keep the shape | hooks 7 to 9 s, long cuts about 70 to 78% kept |
| "be a bit chill" | less of it | reduce, keep the best |
| "imbsr" | "I'm being so real" (emphasis) | |
| "looks really bad" (reference set) | the concept is wrong | three new treatments with the real audio; do not polish the rejected one |
| "make it more dynamic" (reference set) | speed contrast inside one move | kicks, whips, brakes, freezes inside one camera move; not more cuts (in music edits, no whip that shows mirrored frames) |
| "dont change angle like that" (reference set) | follow the action from a stable view | track the subject at a fixed screen point |
| "dont do pointers" (reference set) | no numbered points or callout tags | values inside or above the element, labels under it |
| "not cohesive" (reference set) | the images do not belong together | one subject, matched framing, one grade |
| "harsh" (reference set) | held too briefly behind a wipe and a pop | hold it longer or change it inside the frame with a short crossfade |
| "use his brand" (reference set) | the client's palette and type | pull them from the client's own site and assets |
| "make no mistakes" (reference set) | check everything yourself | frame sheets, validators, loudness, names, facts; say what was checked |

## 4. Options and picks
- For taste calls, offer 2 to 5 options mocked on real frames, each with a one-line reason and your recommendation; never
  build before the pick; expect the pick to differ (Claude recommended title E: "why would u even reccomend E bro it is
  so off putting"; option B won).
- Vague notes ("make it look better") get 2 to 3 concrete options with references and tutorials.
- On designed pieces every change request gets Option A and Option B side by side with a Pick button; where no pick
  comes, choose one and say which (reference method).
- "Looks really bad" gets three distinct treatments per beat as short previews WITH the real audio, next to the current
  cut, and a picks bar the reviewer can copy back ("A1, B1, C3, caption rule 1").
- A new text style: one mock frame before building anything around it (the white TikTok box would have been caught by
  one frame).
- After a rejection of a whole batch: research, then a plan page with proof frames and decisions, and "nothing new gets
  built until you've decided".

## 5. Plan pages and review pages
- **Plan page for a big review** (20 screenshots and 14 points became 50 tasks and 7 decisions): every note is a task with
  a code (D decisions, G all pieces, one letter per piece), an owner (you, me, both), a quick-win flag and a tick box saved
  in the browser; a timeline bar per piece showing its dead stretches; for vague notes, 2 to 3 options mocked on real
  frames; decisions listed at the bottom; republish the same link as answers arrive.
- **Review page per batch** (native and news posts): small web copies that keep their sound; each caption with a copy
  button and its posting window; a "why it works" line with the proof numbers and the data source behind every number;
  grouped by format, best evidence first, untested formats under "Tests"; republish to the same URL; always say the page
  is private and must be shared from its Share menu.
- **Frame review page for designed pieces** (reference method; build: production-automation): frame cards (image, id,
  time, voice line, motion note), comments with a timecode or range, a pin, sketch strokes, replies and a resolved flag,
  a note box on every card, A/B Pick buttons, an approval button, your reply stored next to each note.
- A published client page may already have been forwarded: say what you intend to change and wait before republishing.
- Client documents stay lean: about 600 words, big numbers, plain words, depth in a backup file; no annotation layers
  when the client asks them off.

## 6. Building the round
- Build on the user's latest save, never on your previous build (check the Auto-Save folder; if Premiere has it open,
  ask him to save). Diff it against your last delivery: his hand edits are the brief. Keep them and say what you kept (a
  subtitle he turned into a graphic, cross dissolves, a fade, his music swaps, pop levels, camera shutters).
- Re-check the save time right before building ("hold on. i saved it again. try now on the latest project").
- When your own last build did something destructive (it deleted captions under graphics), rebuild the next version
  from the save BEFORE it, after checking the newer save for hand edits worth carrying over.
- Flag defects in the user's own layers instead of silently fixing them (a duplicate caption, a stray "New Caption"
  placeholder): they own those layers.
- Deadline trade-off: when told "if it will take time do not do it, we are behind on the deadline", estimate the real
  cost first; if it is cheap (one helper switch plus seconds per shot), do it and say so.
- When the reviewer re-cuts your delivery by hand, do not ask for timecodes: diff their project against what you sent,
  clip by clip, and state each pattern with its evidence (mechanics: review-rounds.md section 6).
- When a recurring asset changes (a presenter's stills, a logo), find every use and re-render or relink only those
  (review-rounds.md section 3b). This is the cost of baking assets into renders: compile in Premiere next time.

## 7. Versions and names
- Never overwrite anything delivered: a change becomes `_v2`, `_v3` next to the old one ("do not replace this one make
  version 2. keep that in mind always"). Record the old settings in the job's history.
- Before delivery, fix under the same name: self-check found real misses every round (6 in one round: subtitles flashing
  1 to 5 frames at edges, a borrowed clip, clipped words), all fixed and re-rendered before the report.
- Claude may replace its own just-built file only if Premiere never opened or saved it; once the user has opened or saved
  a file, the next change is a new version.
- Undelivered drafts are moved aside (`_superseded`), old versions to `_old_versions`; never delete them to make room
  (deleting drafts once bent the house rule).
- Keep every version side by side (music edits v1 to v8 all kept); renders in versioned folders so an earlier delivery
  stays valid; a copy of exactly what you delivered (a delivered baseline) in your build folder.
- Project files built from one another share internal IDs: tell the user to close one before opening the other.
- Delete only when the user asks, and only to the Recycle Bin or Trash.
- Names: the job and the version, the way the user names their own. Never put "Claude" in a name a client sees (renders,
  sequences, delivered files, client-visible projects); internal tools and work files may use it.

## 8. Self-check before delivery
- A labelled sheet of every new shot (in, middle, out); both sides of every cut, join and white transition; every
  changed time checked in the real Premiere timeline (a valid project once drew a clip at the wrong time); text over
  faces, blank glyphs, clipped glows, text that leaves too early; loudness and true peak; edges for clipped words and
  stray frames; facts, numbers and name spellings last.
- Semantic checks beyond "the file opens": caption and audio track fingerprints unchanged where you did not touch them,
  B-roll matches the plan, grade pieces and B-roll tile the timeline with no gaps, zoom % per segment within plan,
  graphic texts as intended; one PASS or FAIL line each.
- Music edits before showing: sync on strong hits against chance, effect density against the references, full-size QA
  windows at every changed moment, one pass over the whole render every third of a second, the song subtracted to prove
  no clip audio leaks (motion-design and premiere-ae-editing have the tools).
- Watch it as a viewer would (the reviewer's scrub test): where would someone scrub or skip? "Trim the fat" there, and
  fill dead stretches.
- Say what you could not check ("I haven't heard any of the new audio"; "watch the stars on your first open").

## 9. The report
- Short plain pointers: which file to open; that the original is untouched; per note what changed (answer numbered notes
  one by one); which of the user's edits you kept; what is a placeholder; what is not cleared; mistakes your own check
  caught; what you could not check; at most 2 to 3 closed questions, each with your default; approvals needed; the next
  step in one line, not started. The user answers in one line ("for questions u asked answer is no for both, stuff is
  fine as is").
- Cutdowns: a table (cut, length, what the hook shows), the changes per note, the checks run, mistakes caught, at most 3
  "Your call" questions, then the approvals needed. Notes pages listing every removed stretch were dropped for speed once
  the XML markers carried the reasons.
- Daily news batch: a table per page (window, format, source), what was left out and why, which facts were checked
  where, what to watch next, with the contact sheet and videos. A schedule marks each built post POST, optional or skip
  with its posting window, expires batches that never went up and warns when a post has gone stale (a "drops tonight at
  7pm" video after the event is wrong). News posts expire fast.
- Client hand-offs (an outline, a review page, a document): lead with the page link and the file path, then the scenes or
  posts briefly, then what was assumed or not verified, then what still needs a human (photos, music clearance, the
  client's approval).
- "Which ones should I export?": one file, a per-piece table of what changed, the new lengths, and the in and out check
  ("None of the sequences has in/out marks, so exporting the entire sequence picks up the new CTA endings").
- Correct your own wrong claims in the next report ("I told you yesterday that [it] had been posted twice. That was
  wrong"). The user decides from these reports.
- When the user says "the edit is not the focus" ("The focus is training you"), deliver a training result: a study, a
  side-by-side proof sheet, a test reel, a density table.

## 10. Placeholders and build notes
- Every stand-in for a missing asset is tagged "PLACEHOLDER" on screen, and the build notes list each slot with exact
  timecodes for whoever delivers the real thing (a 3D artist got four slots and a clip-swap list). Why: a stand-in can
  never ship by accident.
- Values Claude had to invent (scores, prices to refresh) are marked as placeholders in the notes and in the report.
- Native posts ship placeholder identities ("@yourpage") until the client decides, and every review page lists what must
  change before posting (the real handle and avatar, fresh numbers on the day, approved usernames).
- Build notes per round: what changed per comment, a comment-status table (one line per comment with time and change,
  plus the comment numbers NOT received and the assumption made where one was missing), open questions, placeholders,
  fact-check flags, licence flags. Sound gets a listening note and a credits list (every sound and track with its source
  and licence); a README gives the rebuild order.

## 11. Calibrate on every review
- Do not just patch the one case: measure what really happened against what was predicted, feed it into the tool's
  defaults, and keep the calibration ("fine tuning these systems with each review, eventually we wanna get to a point
  where you're very accurate in doing everything").
- A systematic miss changes the generator or helper default, not only that shot (fix the toolkit, not the plan, or the
  same bug comes back on the next piece).
- Record every review as dated rules (a review log per client, newest first) plus a short memory gist ("whatever
  feedback i give get the gist of it and save it"), and add taste verdicts to taste-verdicts.md.
- Grade an automatic cut against the editor's real one (kept-time precision and recall per source second; a blind test
  scored 84% and 69%) and read the biggest disagreements with their words: the fastest way to learn his taste.
- Check every new piece against the client's taste list before showing it.
