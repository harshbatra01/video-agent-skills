#!/usr/bin/env python3
"""Install or update the Vision editing kit (skills + house rules + client files) for Claude Code.

Works on macOS and Windows, Python 3.8+, standard library only.

  python3 kit_install.py install  <VisionKit_vX.zip | unzipped folder>   first install (asks before changing things)
  python3 kit_install.py update   <VisionKit_vX.zip | unzipped folder>   apply a weekly update
  python3 kit_install.py status                                         version, last update, open conflicts
  python3 kit_install.py inbox                                          list zips waiting in ~/VisionKit/inbox
  python3 kit_install.py rollback                                       undo the last update
  add --yes to skip the confirmation question, --dry-run to only print what would happen

Where things go:
  ~/VisionKit/kit/          the kit's own files (replaced by updates, do not edit)
  ~/VisionKit/mine/         YOUR layer: overrides, your own notes and systems (updates never touch it)
  ~/VisionKit/inbox/        drop new update zips here
  ~/VisionKit/backups/      files an update replaced, for rollback
  ~/VisionKit/RECEIVED-LOG.md   one entry per update applied
  ~/.claude/skills/<name>/  the kit's skills
  ~/.claude/CLAUDE.md       gets one small marked block that points Claude at the kit rules

Safety rules this script follows:
  - A kit file you edited by hand is never overwritten. The new version is saved beside it as <file>.kit-new and
    listed as a conflict, so you (or Claude) can merge the two.
  - A skill folder that already existed before the kit is never overwritten (pass --adopt NAME to hand it to the kit).
  - Older or equal versions are refused unless you pass --force.
  - Nothing is deleted outright: replaced or removed files go to ~/VisionKit/backups/.
Env overrides (for testing): VISIONKIT_HOME, VISIONKIT_CLAUDE_DIR.
"""
import datetime as _dt
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

HOME = Path(os.environ.get("VISIONKIT_HOME", Path.home() / "VisionKit"))
CLAUDE_DIR = Path(os.environ.get("VISIONKIT_CLAUDE_DIR", Path.home() / ".claude"))
SKILLS = CLAUDE_DIR / "skills"
CLAUDE_MD = CLAUDE_DIR / "CLAUDE.md"
STATE = HOME / ".installed.json"
LOG = HOME / "RECEIVED-LOG.md"
BEGIN = "<!-- VISIONKIT:BEGIN (managed by kit_install.py; edit ~/VisionKit/mine/overrides.md instead) -->"
END = "<!-- VISIONKIT:END -->"


# ---------- small helpers ----------
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def vtuple(v):
    return tuple(int(x) for x in str(v).lstrip("v").split(".") if x.isdigit())


def now():
    return _dt.datetime.now().strftime("%Y-%m-%d %H:%M")


def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"version": None, "files": {}, "skills": [], "history": []}


def save_state(st):
    HOME.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(st, indent=1), encoding="utf-8")


def open_package(src):
    """Return (root folder of the unzipped kit, temp dir to clean or None)."""
    src = Path(src).expanduser()
    if src.is_dir():
        root = src
        tmp = None
    elif zipfile.is_zipfile(src):
        tmp = Path(tempfile.mkdtemp(prefix="visionkit_"))
        with zipfile.ZipFile(src) as z:
            for m in z.namelist():  # refuse paths that escape the folder
                if m.startswith("/") or ".." in Path(m).parts:
                    sys.exit(f"refusing unsafe path inside zip: {m}")
            z.extractall(tmp)
        root = tmp
    else:
        sys.exit(f"not a zip or folder: {src}")
    # the zip holds one top folder (VisionKit_vX); find the MANIFEST.json
    hits = list(root.glob("MANIFEST.json")) or list(root.glob("*/MANIFEST.json"))
    if not hits:
        sys.exit("MANIFEST.json not found in the package")
    return hits[0].parent, tmp


def dest_for(rel):
    """Map a package path to where it is installed. Returns None for paths that are not installed."""
    parts = Path(rel).parts
    if parts[0] == "skills" and len(parts) > 2:
        return SKILLS.joinpath(*parts[1:])
    if parts[0] == "kit":
        return HOME.joinpath(*parts)
    if rel == "START-HERE.md":
        return HOME / "kit" / "START-HERE.md"
    return None  # MANIFEST.json and mine-template are handled separately


def key_for(dest):
    """Stable key for the state file (relative to HOME or CLAUDE_DIR)."""
    d = Path(dest)
    try:
        return "kit:" + d.relative_to(HOME).as_posix()
    except ValueError:
        return "claude:" + d.relative_to(CLAUDE_DIR).as_posix()


def path_for(key):
    kind, rel = key.split(":", 1)
    return (HOME if kind == "kit" else CLAUDE_DIR) / rel


def confirm(msg, yes):
    if yes:
        return True
    try:
        return input(msg + " [y/N] ").strip().lower().startswith("y")
    except EOFError:
        return False


# ---------- CLAUDE.md block ----------
def claude_block(pkg):
    body = (pkg / "kit" / "CLAUDE-kit.md").read_text(encoding="utf-8").strip()
    return f"{BEGIN}\n{body}\n\n@~/VisionKit/mine/overrides.md\n{END}"


def write_claude_md(pkg, dry):
    block = claude_block(pkg)
    old = CLAUDE_MD.read_text(encoding="utf-8") if CLAUDE_MD.exists() else ""
    if BEGIN in old and END in old:
        a = old.index(BEGIN)
        b = old.index(END) + len(END)
        new = old[:a] + block + old[b:]
    else:
        new = (old.rstrip() + "\n\n" if old.strip() else "") + block + "\n"
    if new != old and not dry:
        CLAUDE_DIR.mkdir(parents=True, exist_ok=True)
        if old:
            bk = HOME / "backups" / "CLAUDE.md.before-visionkit"
            if not bk.exists():
                bk.parent.mkdir(parents=True, exist_ok=True)
                bk.write_text(old, encoding="utf-8")
        CLAUDE_MD.write_text(new, encoding="utf-8")
    return new != old


# ---------- install / update ----------
def apply(src, yes=False, dry=False, force=False, adopt=()):
    pkg, tmp = open_package(src)
    try:
        man = json.loads((pkg / "MANIFEST.json").read_text(encoding="utf-8"))
        st = load_state()
        newv, oldv = man["version"], st.get("version")
        if oldv and vtuple(newv) <= vtuple(oldv) and not force:
            sys.exit(f"Installed v{oldv} is the same or newer than this package (v{newv}). Nothing to do. (--force to reinstall)")

        # what changes
        plan = {"add": [], "update": [], "same": [], "conflict": [], "remove": [], "skip_skill": []}
        new_keys = {}
        tracked_skills = set(st.get("skills", []))
        for rel, h in man["files"].items():
            d = dest_for(rel)
            if d is None:
                continue
            parts = Path(rel).parts
            if parts[0] == "skills":
                name = parts[1]
                sdir = SKILLS / name
                if sdir.exists() and name not in tracked_skills and name not in adopt:
                    if name not in plan["skip_skill"]:
                        plan["skip_skill"].append(name)
                    continue
            k = key_for(d)
            new_keys[k] = h  # baseline = the kit's version of this file
            adopting = parts[0] == "skills" and parts[1] in adopt
            if not d.exists():
                plan["add"].append((rel, d))
            else:
                cur = sha(d)
                if cur == h:
                    plan["same"].append((rel, d))
                elif adopting or (k in st["files"] and cur == st["files"][k]):
                    plan["update"].append((rel, d))  # untouched since the kit delivered it
                else:
                    plan["conflict"].append((rel, d))  # edited by the user, or a file that was there first
        for k, h in st["files"].items():
            if k not in new_keys:
                p = path_for(k)
                if p.exists():
                    plan["remove"].append((k, p, sha(p) != h))

        print(f"Vision kit: {'v' + oldv if oldv else 'not installed'} -> v{newv}")
        print(f"  new files {len(plan['add'])}, updated {len(plan['update'])}, unchanged {len(plan['same'])}, "
              f"your edits kept (conflicts) {len(plan['conflict'])}, retired {len(plan['remove'])}")
        for name in plan["skip_skill"]:
            print(f"  ! skill folder '{name}' already exists and is not from the kit: left alone (use --adopt {name} to hand it to the kit)")
        for rel, d in plan["conflict"]:
            print(f"  ! you changed {d}: kept yours, new kit version saved as {d.name}.kit-new")
        print(f"  ~/.claude/CLAUDE.md gets (or refreshes) one marked VisionKit block")
        if dry:
            print("dry run: nothing changed")
            return
        if not confirm("Apply these changes?", yes):
            print("Nothing changed.")
            return

        bdir = HOME / "backups" / f"{oldv or 'none'}_to_{newv}"
        replaced = []

        def backup(p):
            t = bdir / key_for(p).replace(":", "/")
            t.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, t)
            replaced.append(key_for(p))

        for rel, d in plan["add"] + plan["update"]:
            if d.exists():
                backup(d)
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(pkg / rel, d)
        conflicts, kitnew = [], []
        for rel, d in plan["conflict"]:
            kn = d.with_name(d.name + ".kit-new")
            shutil.copy2(pkg / rel, kn)
            conflicts.append(str(d))
            kitnew.append(str(kn))
        retired = []
        for k, p, edited in plan["remove"]:
            if edited:
                print(f"  kept {p}: the kit dropped it but you had changed it")
                continue
            backup(p)
            p.unlink()
            retired.append(str(p))

        # the user's own layer: created once, never overwritten
        mt = pkg / "mine-template"
        if mt.is_dir():
            for f in mt.rglob("*"):
                if f.is_file():
                    t = HOME / "mine" / f.relative_to(mt)
                    if not t.exists():
                        t.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(f, t)
        (HOME / "inbox").mkdir(parents=True, exist_ok=True)
        write_claude_md(pkg, dry=False)

        skills_now = sorted({Path(r).parts[1] for r in man["files"] if Path(r).parts[0] == "skills"} - set(plan["skip_skill"]))
        hist = st.get("history", [])
        hist.append({"from": oldv, "to": newv, "at": now(), "backup": str(bdir), "replaced": replaced,
                     "added": [key_for(d) for _, d in plan["add"]], "kitnew": kitnew,
                     "prev_files": st["files"], "prev_skills": st.get("skills", [])})
        save_state({"version": newv, "installed_at": now(), "files": new_keys, "skills": skills_now, "history": hist[-12:]})

        notes = changelog_since(pkg, oldv, newv)
        new_log = not LOG.exists() or LOG.stat().st_size == 0
        with open(LOG, "a", encoding="utf-8") as f:
            if new_log:
                f.write("# Vision kit: received updates\n\nOne entry per update applied, newest at the bottom.\n")
            f.write(f"\n## v{newv} received {now()} (was {'v' + oldv if oldv else 'not installed'})\n")
            f.write(f"- files: {len(plan['add'])} new, {len(plan['update'])} updated, {len(retired)} retired, "
                    f"{len(conflicts)} kept because you had edited them\n")
            for c in conflicts:
                f.write(f"- CONFLICT to merge: {c} (kit version beside it as .kit-new)\n")
            for name in plan["skip_skill"]:
                f.write(f"- skipped skill '{name}': a folder with that name already existed\n")
            if notes:
                f.write("- what changed (from the changelog):\n")
                for line in notes.splitlines():
                    f.write(f"  {line}\n")
        print(f"Done: v{newv} installed. Log: {LOG}")
        if conflicts:
            print("Conflicts to merge (yours kept, kit version beside each as .kit-new):")
            for c in conflicts:
                print("  " + c)
        print("Start a new Claude Code session so the updated skills load.")
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)


def changelog_since(pkg, oldv, newv):
    cl = pkg / "kit" / "CHANGELOG.md"
    if not cl.exists():
        return ""
    out, keep = [], False
    for line in cl.read_text(encoding="utf-8").splitlines():
        if line.startswith("## v"):
            v = line[4:].split()[0]
            keep = (oldv is None or vtuple(v) > vtuple(oldv)) and vtuple(v) <= vtuple(newv)
        if keep:
            out.append(line)
    return "\n".join(out).strip()


def status():
    st = load_state()
    if not st.get("version"):
        print("Vision kit is not installed yet.")
        return
    last = st.get("installed_at", "?")
    print(f"Vision kit v{st['version']}, last update applied {last}")
    try:
        days = (_dt.datetime.now() - _dt.datetime.strptime(last, "%Y-%m-%d %H:%M")).days
        print(f"  {days} day(s) since the last update" + ("  (weekly update may be overdue: ask Kanishk)" if days > 9 else ""))
    except ValueError:
        pass
    print(f"  skills: {', '.join(st.get('skills', []))}")
    pend = [p for p in list(HOME.rglob("*.kit-new")) + list(SKILLS.rglob("*.kit-new"))]
    print(f"  open conflicts: {len(pend)}")
    for p in pend:
        print("    " + str(p))
    inbox()


def inbox():
    st = load_state()
    cur = st.get("version")
    zips = sorted((HOME / "inbox").glob("VisionKit_v*.zip")) if (HOME / "inbox").exists() else []
    newer = [z for z in zips if not cur or vtuple(z.stem.split("_v", 1)[1]) > vtuple(cur)]
    if newer:
        print("  waiting in inbox (newer than installed):")
        for z in newer:
            print("    " + str(z))
    else:
        print("  inbox: nothing newer waiting")


def rollback(yes=False):
    st = load_state()
    hist = st.get("history", [])
    if not hist:
        sys.exit("nothing to roll back")
    h = hist[-1]
    print(f"Roll back v{h['to']} -> {('v' + h['from']) if h['from'] else 'not installed'}: restores {len(h['replaced'])} files, removes {len(h['added'])} new ones")
    if not confirm("Go ahead?", yes):
        return
    bdir = Path(h["backup"])
    for k in h["added"]:
        p = path_for(k)
        if p.exists():
            p.unlink()
    for kn in h.get("kitnew", []):
        if Path(kn).exists():
            Path(kn).unlink()
    for k in h["replaced"]:
        src = bdir / k.replace(":", "/")
        if src.exists():
            d = path_for(k)
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, d)
    st.update({"version": h["from"], "files": h["prev_files"], "skills": h["prev_skills"], "history": hist[:-1],
               "installed_at": now()})
    save_state(st)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"\n## ROLLBACK {now()}: v{h['to']} undone, back to {('v' + h['from']) if h['from'] else 'nothing'}\n")
    print("Rolled back. Note: the CLAUDE.md block keeps the newer wording until the next install.")


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return
    cmd, rest = argv[0], argv[1:]
    flags = {a for a in rest if a.startswith("--")}
    args = [a for a in rest if not a.startswith("--")]
    adopt = []
    if "--adopt" in rest:
        i = rest.index("--adopt")
        adopt = rest[i + 1].split(",") if i + 1 < len(rest) else []
        args = [a for a in args if a not in adopt]
    if cmd in ("install", "update"):
        if not args:
            sys.exit("give the path to the VisionKit zip or folder")
        apply(args[0], yes="--yes" in flags, dry="--dry-run" in flags, force="--force" in flags, adopt=adopt)
    elif cmd == "status":
        status()
    elif cmd == "inbox":
        inbox()
    elif cmd == "rollback":
        rollback(yes="--yes" in flags)
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
