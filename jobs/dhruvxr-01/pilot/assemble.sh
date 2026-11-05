#!/bin/bash
# Joins seg1..seg5.mp4 (90 frames each, 1280x720, 30 fps) into pilot_v1.mp4 with audio.wav.
# A missing segment is replaced by 90 black frames so the timing holds, and that is reported.
cd "$(dirname "$0")"; : > concat.txt; miss=""
for n in 1 2 3 4 5; do
  if [ -s seg$n.mp4 ]; then echo "file 'seg$n.mp4'" >> concat.txt
  else miss="$miss seg$n"; ffmpeg -v error -y -f lavfi -i color=c=black:s=1280x720:r=30 -frames:v 90 -c:v libx264 -pix_fmt yuv420p -crf 18 black$n.mp4; echo "file 'black$n.mp4'" >> concat.txt; fi
done
ffmpeg -v error -y -f concat -safe 0 -i concat.txt -c:v libx264 -pix_fmt yuv420p -crf 18 -r 30 video_only.mp4
if [ -s audio.wav ]; then ffmpeg -v error -y -i video_only.mp4 -i audio.wav -c:v copy -c:a aac -b:a 192k -t 15 pilot_v1.mp4; else cp video_only.mp4 pilot_v1.mp4; miss="$miss audio"; fi
echo "missing:${miss:- none}"
ffprobe -v error -count_frames -show_entries stream=codec_type,width,height,r_frame_rate,nb_read_frames:format=duration -of compact pilot_v1.mp4
ffmpeg -hide_banner -i pilot_v1.mp4 -af ebur128=peak=true -f null - 2>&1 | sed -n '/Summary/,$p' | grep -E "I:|Peak:" | tr -s ' ' | tr '\n' ' '; echo
ffmpeg -v error -y -i pilot_v1.mp4 -vf "fps=2,scale=320:-2,tile=6x5" -frames:v 1 pilot_v1_sheet.jpg && echo sheet ok
