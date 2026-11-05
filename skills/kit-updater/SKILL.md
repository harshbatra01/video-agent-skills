---
name: kit-updater
description: Install, update, check or roll back the Vision kit (Kanishk's editing skills, house rules and client files) that arrives as a weekly VisionKit_vYYYY.MM.DD.zip. Use whenever the user mentions the Vision kit, VisionKit, a kit update or kit zip from Kanishk, "apply the update", "what changed in the kit", kit status, a .kit-new conflict file, or wants to undo an update.
---

# Kit updater

The Vision kit is a set of skills plus `~/VisionKit/kit/` (house rules, client files, library, tools). Kanishk sends a
new full zip about once a week. `~/VisionKit/kit/tools/kit_install.py` does the file work; your job is to run it
safely and explain the result in plain words.

## Apply an update
1. Find the zip: `~/VisionKit/inbox/`, then `~/Downloads/`, or a path the user gives. Several waiting? Apply the
   newest one only (each zip is complete, not a patch).
2. Preview: `python3 ~/VisionKit/kit/tools/kit_install.py update <zip> --dry-run`. Tell the user the counts and any
   conflicts in two or three lines.
3. Apply: same command with `--yes` instead of `--dry-run` (the script cannot read a keyboard answer when you run it).
4. Read the new entries in `~/VisionKit/kit/CHANGELOG.md` (everything above the old version) and tell the user what
   changed: the big picture first, then anything marked "Action for you" (things to install or set up). Ask before
   installing any software.
5. Say that a new Claude Code session is needed for updated skills to load.
6. Leave the zip in the inbox (old zips are a useful history; the user can clear them).

## Conflicts (`.kit-new` files)
A conflict means the user edited a kit file and the update also changed it. The script kept the user's file and put
the kit's new version beside it as `<file>.kit-new`. To resolve one: show the user the differences in plain words,
merge the kit's improvements into their file without losing their edits (or move their edits into
`~/VisionKit/mine/overrides.md` and take the kit file as is, which avoids future conflicts), then delete the
`.kit-new` file. Recommend the overrides route: kit files stay untouched and updates stay clean.

## Skills that collided
"skill folder X already exists and is not from the kit" means the user had their own skill with that name before.
Leave it. If the user wants the kit's version, rerun with `--adopt X` (their old copy goes to `~/VisionKit/backups/`).

## Other commands
- `status`: installed version, days since the last update, open conflicts, newer zips waiting. Run it when the user
  asks about the kit, and if the last update is more than 9 days old, mention that Kanishk's weekly update may be due.
- `rollback`: undoes the last update from backups. Preview what it will do, ask, then run with `--yes`.
- First install from an unzipped folder: `python3 <folder>/kit/tools/kit_install.py install <folder>` (dry run first).

## Rules
- Never edit files in `~/VisionKit/kit/` or the kit's skill folders by hand to "fix" something. Put the fix in
  `~/VisionKit/mine/overrides.md`, and note it in `~/VisionKit/mine/feedback-for-kanishk.md` so Kanishk fixes it upstream.
- Never touch `~/VisionKit/mine/`; it belongs to the user.
- The received log `~/VisionKit/RECEIVED-LOG.md` is written by the script; do not rewrite its history.
