#!/bin/zsh
# Full v4: picture, sound, finish, mux. v3 is never touched.
set -e
cd ~/VisionKit/mine/jobs/minidoc-02-anthropic-ipo
python3 tools/edl_v4.py picture | tail -2
python3 tools/build_edit.py audio | tail -3
mkdir -p render/v4
python3 tools/edit_finish.py edit/picture_v4.mp4 edit/timeline_v4.json edit/finish_v4.mp4 | tail -1
ffmpeg -nostdin -v error -y -i edit/finish_v4.mp4 -i edit/audio/mix_music_v4.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest render/v4/Anthropic_IPO_v4.mp4
ffmpeg -nostdin -v error -y -i edit/finish_v4.mp4 -i edit/audio/mix_nomusic_v4.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest render/v4/Anthropic_IPO_v4_no-music.mp4
ffmpeg -nostdin -v error -y -i render/v4/Anthropic_IPO_v4.mp4 -vf scale=960:720 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k render/v4/Anthropic_IPO_v4_phone.mp4
echo RENDER_DONE
