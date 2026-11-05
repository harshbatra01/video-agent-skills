#!/usr/bin/env python3
"""Vision kit setup check: is the kit installed right, and what does this machine still need?
usage: python3 ~/VisionKit/kit/tools/selftest.py
Read only: it installs and changes nothing. Prints a checklist; lines starting with "NEED" are things to set up."""
import importlib
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

HOME = Path(os.environ.get("VISIONKIT_HOME", Path.home() / "VisionKit"))
CLAUDE_DIR = Path(os.environ.get("VISIONKIT_CLAUDE_DIR", Path.home() / ".claude"))
MAC = sys.platform == "darwin"
need = []


def line(ok, text, fix=""):
    print(("  ok    " if ok else "  NEED  ") + text + ("" if ok or not fix else f"  ->  {fix}"))
    if not ok:
        need.append(text)


print(f"== Machine: {platform.system()} {platform.release()} ({platform.machine()}), Python {sys.version.split()[0]}")
line(sys.version_info >= (3, 9), "Python 3.9 or newer", "install a current Python 3 (python.org or Homebrew)")

print("== Kit")
st = HOME / ".installed.json"
if st.exists():
    s = json.loads(st.read_text(encoding="utf-8"))
    line(True, f"installed v{s.get('version')} on {s.get('installed_at')}")
    for name in s.get("skills", []):
        line((CLAUDE_DIR / "skills" / name / "SKILL.md").exists(), f"skill {name}")
else:
    line(False, "kit installed", "run kit_install.py install <zip or folder>")
cm = CLAUDE_DIR / "CLAUDE.md"
line(cm.exists() and "VISIONKIT:BEGIN" in cm.read_text(encoding="utf-8", errors="replace"), "house rules block in ~/.claude/CLAUDE.md")
line((HOME / "mine" / "overrides.md").exists(), "your own layer ~/VisionKit/mine/")

print("== Apps")
if MAC:
    apps = sorted(Path("/Applications").glob("Adobe Premiere Pro*")), sorted(Path("/Applications").glob("Adobe After Effects*"))
else:
    pf = Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Adobe"
    apps = sorted(pf.glob("Adobe Premiere Pro*")), sorted(pf.glob("Adobe After Effects*"))
line(bool(apps[0]), "Premiere Pro: " + (apps[0][-1].name if apps[0] else "not found"), "needed for the Premiere tools")
line(bool(apps[1]), "After Effects: " + (apps[1][-1].name if apps[1] else "not found"), "needed for the After Effects tools")
if MAC and apps[1]:
    line(any(apps[1][-1].glob("aerender")), "aerender (After Effects command line renderer)")

print("== Command line tools")
hints = {"ffmpeg": "brew install ffmpeg", "ffprobe": "comes with ffmpeg", "yt-dlp": "brew install yt-dlp",
         "git": "xcode-select --install" if MAC else "git-scm.com", "node": "brew install node (only for the web pipelines)"}
for tool, fix in hints.items():
    line(shutil.which(tool) is not None, tool, fix)
if MAC:
    line(shutil.which("swiftc") is not None or subprocess.run(["xcrun", "--find", "swiftc"], capture_output=True).returncode == 0,
         "Swift compiler (for the small OCR and window tools)", "xcode-select --install")
    vlc = Path("/Applications/VLC.app")
    line(vlc.exists() or shutil.which("ffmpeg") is not None, "a frame grabber (ffmpeg or VLC)", "brew install ffmpeg")

print("== Python modules the scripts use")
mods = {"av": "pip install av", "numpy": "pip install numpy", "PIL": "pip install pillow", "esprima": "pip install esprima"}
mods["mlx_whisper" if MAC and platform.machine() == "arm64" else "faster_whisper"] = (
    "pip install mlx-whisper" if MAC and platform.machine() == "arm64" else "pip install faster-whisper")
for m, fix in mods.items():
    try:
        importlib.import_module(m)
        line(True, m)
    except Exception:
        line(False, m, fix + "  (best inside a venv, see premiere-ae-editing setup)")

env = CLAUDE_DIR / "skills" / "premiere-ae-editing" / "scripts" / "env_check.py"
if env.exists():
    print("== Detailed check from premiere-ae-editing (env_check.py)")
    r = subprocess.run([sys.executable, str(env)], capture_output=True, text=True, timeout=120)
    print("\n".join("  " + l for l in (r.stdout + r.stderr).strip().splitlines()))

print(f"\n{len(need)} thing(s) to set up." if need else "\nAll set.")
