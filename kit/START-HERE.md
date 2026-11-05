# Vision kit: start here

This zip moves everything Kanishk's Claude learned while editing for Vision Clipping onto your Claude: how we research
and source, tell stories, write hooks, cut and pace, use B-roll, grade, do sound and music, build motion graphics, edit
Premiere projects and After Effects comps by script, handle review notes, and run the automated production pipelines.
It also holds one file per client project so your Claude can pick any of them up.

## What you need
- **Claude Code** on this Mac (the Claude desktop app's Code tab, or the `claude` terminal app).
- Premiere Pro and After Effects (2025 or 2026) for the editing tools. The knowledge works without them.
- Python 3 (`python3 --version` in Terminal; if it is missing, macOS offers to install it, or use Homebrew).
- The kit's setup check will list anything else (ffmpeg, yt-dlp, a few small tools) and **asks before installing**.

## Install (about 5 minutes)
1. Unzip `VisionKit_v….zip` anywhere (Downloads is fine).
2. Open Claude Code in that unzipped folder and send this message:

   > Read START-HERE.md in this folder and install the Vision kit. Show me what will change before you do it.

3. When it is done, start a **new** Claude Code session so the skills load. Try: "What does the Vision kit give me?"

## Every week after that
Kanishk sends `VisionKit_vYYYY.MM.DD.zip`. Save it into `~/VisionKit/inbox/` (or leave it in Downloads) and tell
Claude: **"apply the kit update"**. Claude applies it, keeps anything you changed yourself, logs it in
`~/VisionKit/RECEIVED-LOG.md` and tells you what is new.

## Building your own systems on top
Your own rules go in `~/VisionKit/mine/overrides.md` (they win over the kit). Your own notes, systems and skills go in
`~/VisionKit/mine/` or new skill folders with new names. Updates never touch them. Anything you want Kanishk to change
goes in `~/VisionKit/mine/feedback-for-kanishk.md`; send him that file now and then.

---

## For Claude: how to install

Do these in order and keep the user informed in short plain lines.

1. Run a dry run from this unzipped folder:
   `python3 kit/tools/kit_install.py install . --dry-run`
   Tell the user what it will add (skills, `~/VisionKit/`, one marked block in `~/.claude/CLAUDE.md`) and any warnings,
   for example a skill name that already exists. Ask for a yes.
2. Apply: `python3 kit/tools/kit_install.py install . --yes`
3. Run the setup check: `python3 ~/VisionKit/kit/tools/selftest.py` and show the user the result as a short
   checklist. For anything missing, say what it is for and how to install it, and ask before installing anything
   (Homebrew packages, Python packages, Swift tools, the optional Premiere bridge). Never change macOS security or
   Adobe settings without the user's explicit yes; the Premiere bridge needs one such setting, so explain it first.
4. Read `~/VisionKit/kit/CHANGELOG.md` and `~/VisionKit/kit/clients/README.md`, then give the user a 6 to 10 line
   tour: the skills, the client files, the weekly updates, and their own `mine/` layer.
5. Tell the user to start a new Claude Code session so the skills load.
6. In that new session (or when the user says "do the Mac setup tasks"), work through `~/VisionKit/kit/MAC-TASKS.md`
   step by step. The tools were built on Windows and partly ported to Mac; that list tests each one on this Mac and
   fixes what needs fixing. Ask before installing anything, log results in `~/VisionKit/mine/mac-test-results.md`,
   and write anything Kanishk should fix upstream in `~/VisionKit/mine/feedback-for-kanishk.md`.
