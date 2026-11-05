# Review rounds: turning client / reviewer notes into a new version

The work comes in rounds: build, the user + reviewer comment (timecoded screenshots, a pasted review, Frame.io notes),
you fix, deliver a new version. This is the loop that kept the user happy.

## 1. Intake
- Read every comment with its timecode. The user's own explanations OVERRIDE the comment text ("#3 is a note for
  myself, ignore it", "#13 the infographic is fine actually"). If the user says "stop, I'm sending explanations", wait.
- Make one fix table first (in your scratch, not in chat): comment id, time, which shot / item is there, what to do,
  status. Map times to shots from your edit list or `prproj_dump.py` of the CURRENT project (the user may have moved
  things since your last delivery).
- Map review timecodes (HH:MM:SS:FF) to the shot and the voice line from your edit list with a small script, so each
  comment lands on the right item, then check it against the current project.
- When the user reports a glitch, first diff their latest save against your delivery: their own save may have caused it
  (a "clip cut to 10 frames" was the user's save trimming 1.35 s). Fix it either way and say which it was.
- Ask only about comments that are truly ambiguous; decide the rest with sensible defaults and say what you chose.
- "Don't fix these, apply next" is a common mode: then change the rules and tool defaults, not the delivered files
  (editing-playbook `reviews-and-versions.md`).
- Fast vs perfect: when the user says they are behind on the deadline, do the cheap fixes now and list the rest for next
  time (example: "premium type everywhere if quick, else next video").

## 2. Build on the user's latest save
- Find it (check the project folder AND Premiere's Auto-Save folder, `Adobe Premiere Pro Auto-Save` next to the
  project; file times). If Premiere has it open (title bar, or `pp.py --status` on the Mac), ask the user to save rather
  than reading a stale file. The user edits between rounds (their own layers, trims, blurs, swapped renders). Diff it
  against your last delivery (`prproj_dump.py` both, word diff).
- Their hand edits are the brief: keep them, adapt yours around them (a corner blur they added to hide something you
  later removed can go to 0, keep the effect).
- Never touch their original file. New file next to it: "<their name> v7.prproj". New renders in a new folder
  (renders/v7/) so earlier versions stay valid.
- You may replace your OWN just-built file only while Premiere has never opened or saved it (done once, ten minutes
  after a build, to fix a flag). Once the user has opened or saved it, every change is a new version.
- When your own last build did something destructive (one version deleted captions under graphics), build the next
  version from the save BEFORE it instead of patching on top, and carry over any hand edits from the newer save.
- A round, step by step: copy the user's latest save; import the new renders and audio in Premiere by UI and save that
  as its own version (an "imported" save); build vN by script on it (new objects appended, untouched objects
  byte-identical); validate (structure and semantic checks, prproj-format.md section 17); open it in Premiere; export
  30-60 check frames at the changed times into one sheet; fix; report.

## 3. Fix
- Re-render only the shots a comment touches (ae_build with only=[...] or a v7 generator importing the earlier block
  generators). Keep shot lengths unless the comment needs a new length; then extend the item and anything that depends
  on it (music to the new end, end screen).
- Relink / extend / disable in a copy of their project with prproj_lib (recipes R1-R5).
- Values you had to invent (scores, placeholders) are marked as placeholders in the notes and in the report.

## 3b. When a recurring asset changes (presenter, logo, product shot)
- Find EVERY use: scan the build scripts and the project dump for the asset's file paths (not only its name), and the
  timeline for which of those shots are really in the cut.
- Check whether the new asset lines up with the old one (same size, zero offset, mask overlap above 99 %): if it does,
  all positions, scales and timings still hold, so swap the asset folder and change nothing else.
- Map each old variant to its closest new one (expressions, poses); say which ones had no match and what you used.
- Re-render only the shots that use it, into a new version folder, and relink. Then check every one of them.
- This is the cost of baking assets into renders: next time keep such assets as Premiere clips (SKILL.md rule 10).

## 4. Verify (do not skip)
- `validate_struct.py` clean, `check_jsx.py` clean before rendering.
- Sheets of every new render (in / middle / out).
- Open the new project in Premiere and look at EVERY commented time (premiere-ui.md). Note what you could not check
  (for example "music keyframes not listened to").

## 5. Deliver and report
- Build notes file for the team (what changed per comment, open questions, placeholders, licensing flags), next to the
  renders: `<job>_build_notes_vN.txt`. Include a comment-status table: one line per comment number (time, what
  changed), the comment numbers NOT received, and the assumption made where one was missing.
- Placeholders: tag every 2D stand-in for a missing 3D shot "PLACEHOLDER" on screen and list each slot with exact
  timecodes (and any clips to swap) for the artist, so a stand-in can never ship by accident.
- Read render names from disk, never guess them: a render named differently from its ad was once paired with the wrong
  ad.
- Report in chat: short, plain English, no em dashes. Group by the client's points. Say which file to open, that their
  original is untouched, what you kept of their edits, what is a placeholder, what they still have to do (export,
  YouTube end-screen elements, official scores). Offer the next step in one line, do not start it.
- Keep a dated line in the project's memory file or the job's notes: version, what it contains, the client's rules
  learned this round.

## 6. Calibrate
When a note shows a systematic miss (labels too small everywhere, a wrong lens assumption, sync early by 0.3 s), fix the
generator or tool default, not only that shot, and record the rule (mechanics here; taste in editing-playbook or the
motion-design skill) so the next video starts right.

When the reviewer edits the delivered sequence by hand (import the XML, re-cut, save), do not ask for timecodes: diff
their project against what was sent, clip by clip (what each trim, inner cut or dropped clip removed: words, subtitle,
loudness, frames at the cut points), then state each pattern with its evidence. Their untouched parts are approvals.
