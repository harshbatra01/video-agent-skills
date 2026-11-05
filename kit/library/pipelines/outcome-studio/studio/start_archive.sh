#!/bin/sh
# Mac version of start_archive.bat (added in the boss kit): runs the price archive and keeps the Mac awake
# while it runs (caffeinate -i). Leave the Terminal window open. Stop with Ctrl+C.
cd "$(dirname "$0")" || exit 1
exec caffeinate -i python3 -u archive.py "$@"
