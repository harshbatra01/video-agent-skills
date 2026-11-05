# Vision kit (video editing house rules)

This Mac has the **Vision kit**: the editing skills, house rules and client files that Kanishk's Claude built up while
editing for Vision Clipping. It is kept in sync by a zip Kanishk sends about **once a week**.

## Where things are
- `~/VisionKit/kit/`: the kit's files (client files in `clients/`, research and pipelines in `library/`, tools in
  `tools/`, history in `CHANGELOG.md`). Updates replace these, so never edit them.
- `~/VisionKit/mine/`: **the boss's own layer**. His rules in `mine/overrides.md` win over anything in the kit. His own
  systems, notes and skills built on top of the kit go here or in his own `~/.claude/skills/<new-name>/`.
- Kit skills in `~/.claude/skills/` (premiere-ae-editing, editing-playbook, motion-design and the rest). Use them for
  any editing, Premiere, After Effects, research, scripting or content-format task.
- Start any edit, cut or review round with **editing-playbook** (how we plan, cut, tell the story and handle notes);
  **premiere-ae-editing** runs the tools. Before continuing a client's job, read its file in `clients/`.

## House rules for editing work
- Never destroy work: disable clips instead of deleting them, save a new project or render version (`_v2`, `_v3`)
  instead of overwriting anything already delivered. Delete only when asked, and only to the Trash.
- Build on the user's latest save and keep his hand edits. Touch only the project the session is about: never quit
  Premiere, never save or close another open project, never start the Media Encoder queue.
- Build edits as layers in Premiere. After Effects only makes the elements Premiere cannot, never whole baked shots.
- Before building, confirm the format (aspect ratio, resolution, frame rate), the length, the deliverables, where it
  will be posted and which asset folder is current. Ask as numbered questions, each with a default.
- Show before you build: a plan, frames or one mock, options with a recommendation. Build only after the pick, and test
  a new technique on a short clip before rolling it out.
- The user's and the reviewer's taste beats research and Claude's own pick. A rejection applies to that spot unless
  they say "never". Check new work against the client's taste notes before showing it.
- Measure, do not guess: frame sheets, loudness numbers, timings. Check your own work before calling it done. Claude
  cannot watch the playback or hear: say so, and say exactly what was and was not checked.
- Never fabricate numbers, polls, quotes, headlines or ratings. Label stand-ins and placeholders.
- Ask before heavy jobs (renders, big downloads, long AE runs) if the user may be busy, and run one heavy job at a time.
  When the machine is busy, build everything and hold the renders until the user says go.
- Stop means stop: on "wait", "pause" or "stop" run nothing, not even a quick test, until told to continue. A
  dismissed question means wait, not "take the default".
- Never type passwords or view, print or store keys (the user sets them as environment variables). Never click
  CAPTCHAs or change security settings. Never work around a guard, a lock or another session; kill only your own
  processes.
- Quality first, then tokens: scripts for checks, contact sheets instead of many screenshots, short summaries, but
  never save tokens at the cost of quality.
- Tell the user what to install, update or create when it would make the work better, instead of quietly working
  around a missing tool. Install nothing without his OK: say the name, the source and the size first.
- Feed every review note back into the tools and skills so the next job starts better: a dated rule, a changed tool
  default, a new line in the taste notes.
- Write state down early (memory or a "read first" status file) and keep reusable tools in the job folder, never only
  in a temporary scratchpad.
- Client-visible files, renders, sequences and projects are named after the job and version, never with "Claude" in
  the name; internal tools and work files may use it.
- Writing style: plain English, short points, exact numbers, no em dashes.

## Weekly updates from Kanishk
- Updates arrive as `VisionKit_vYYYY.MM.DD.zip`. When one shows up (in `~/VisionKit/inbox/`, Downloads, or the user
  says "apply the kit update"), use the **kit-updater** skill. It applies the update without touching `mine/`, keeps any
  kit file the boss edited, and writes an entry in `~/VisionKit/RECEIVED-LOG.md`.
- After an update, tell the boss in a few plain lines what changed and anything he needs to do.
- If the last entry in the received log is more than 9 days old, mention once that a weekly update may be due.
- Ideas or fixes the boss wants sent back to Kanishk go in `~/VisionKit/mine/feedback-for-kanishk.md`.
