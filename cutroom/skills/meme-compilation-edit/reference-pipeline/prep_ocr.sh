#!/bin/bash
# Stage 2 of the pipeline: OCR every meme and the recording's title bar. Run from the job's _pipeline folder.
# macOS as written (ocr_batch is the Swift Vision tool: swiftc -O ocr_batch.swift -o ocr_batch). On Windows the rest runs
# in Git Bash with PY=python, but the OCR step needs a replacement (see README).
set -e
PY="${PY:-python3}"
C="/CHANGE/ME/client folder"
REC="CHANGE_ME recording.mp4"            # the narrator's raw screen recording, inside the client folder
RAW="$C/$REC"
mkdir -p imgconv vframes title
# webp -> png copies for OCR and pixel work (the file name is passed as an argument, never pasted into Python code)
for f in "$C"/*.webp "$C"/*.WEBP; do
  [ -e "$f" ] || continue
  b=$(basename "$f")
  "$PY" -c 'import sys; from PIL import Image; Image.open(sys.argv[1]).convert("RGB").save(sys.argv[2])' "$f" "imgconv/$b.png"
done
# a frame from the middle of each video meme
for f in "$C"/*.mp4; do
  b=$(basename "$f"); [ "$b" = "$REC" ] && continue
  d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
  mid=$("$PY" -c 'import sys; print(float(sys.argv[1]) / 2)' "$d")
  ffmpeg -v error -y -ss "$mid" -i "$f" -frames:v 1 "vframes/$b.png"
done
# meme OCR
ls "$C" | grep -v -F -x "$REC" > imglist.txt
: > img_ocr.jsonl
while IFS= read -r b; do
  case "$b" in *.webp|*.WEBP) p="imgconv/$b.png";; *.mp4) p="vframes/$b.png";; *) p="$C/$b";; esac
  ./ocr_batch "$p" >> img_ocr.jsonl
done < imglist.txt
echo "img ocr: $(wc -l < img_ocr.jsonl)"
# title bar at 2 fps (the crop is where the file name sits in THIS recording's preview window: measure it per job)
ffmpeg -v error -y -i "$RAW" -vf "fps=2,crop=1000:30:110:33" title/t_%05d.png
ls title | wc -l
: > title_ocr.jsonl
ls title | sed 's#^#title/#' | xargs -n 200 ./ocr_batch >> title_ocr.jsonl
echo "title ocr: $(wc -l < title_ocr.jsonl)"
echo DONE
