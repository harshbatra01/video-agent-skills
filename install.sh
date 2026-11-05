#!/usr/bin/env bash
# Installs both packs' skills to ~/.claude/skills. Never overwrites a skill that already exists.
#   ./install.sh           show what would happen
#   ./install.sh --apply   do it
set -eu
HERE="$(cd "$(dirname "$0")" && pwd)"
for pack in attention-compound visionkit; do
  echo "== $pack"
  "$HERE/$pack/install.sh" "${1:-}"
done
