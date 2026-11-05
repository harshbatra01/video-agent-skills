#!/usr/bin/env bash
# Copies this pack's skills to ~/.claude/skills. Never overwrites a skill that already exists.
#   ./install.sh           show what would happen
#   ./install.sh --apply   do it
set -eu
HERE="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/.claude/skills"
APPLY=0
[ "${1:-}" = "--apply" ] && APPLY=1
[ "$APPLY" = 1 ] && mkdir -p "$DEST"
new=0; kept=0
for dir in "$HERE"/skills/*/; do
  name="$(basename "$dir")"
  if [ -e "$DEST/$name" ]; then
    echo "keep     $name (already installed)"
    kept=$((kept + 1))
  else
    echo "install  $name"
    [ "$APPLY" = 1 ] && cp -R "$dir" "$DEST/$name"
    new=$((new + 1))
  fi
done
echo "$new to install, $kept kept."
if [ "$APPLY" = 0 ]; then
  echo "Nothing changed. Run with --apply to install."
else
  echo "Done. Start a new Claude Code session so the skills load."
fi
for tool in python3 ffmpeg ffprobe yt-dlp; do
  command -v "$tool" >/dev/null 2>&1 || echo "missing: $tool (some tools need it)"
done
