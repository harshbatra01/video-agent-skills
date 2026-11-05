#!/bin/bash
# Runs the repo's reference tools on each reel. Usage: tools/run_all.sh  (from research/metro-media-house)
set -e
R=../../reference-reels; S=../../skills
for id in DclpjyxhKF6 DdHKc5GBqT- Dee-mp9BJqG DfFsUfUx0dZ; do
  O=raw/$id; mkdir -p $O/evsheet $O/shotwords; v=$R/$id/reel.mp4; t=$R/$id/reel.transcript.json
  echo "=== $id"
  python3 -I $S/minidoc-reference-style/scripts/frame_scores.py $v $O/scores.json
  python3 -I $S/minidoc-reference-style/scripts/cut_events.py $O/scores.json $v $O/events.json
  python3 -I $S/minidoc-reference-style/scripts/event_sheets.py $O/events.json $v $O/evsheet/ev 25
  python3 -I $S/minidoc-reference-style/scripts/ref_stats.py $O $v $t > $O/ref_stats.txt; cat $O/ref_stats.txt
  python3 -I $S/minidoc-reference-style/scripts/motion_class.py $v $O/shots_ref.json $O/motion.json
  python3 -I $S/word-matched-broll/scripts/ac_shot_words.py $v $t $O/shotwords/sw
  python3 -I $S/word-matched-broll/scripts/colour_stats.py $id $v > $O/colour.json; cat $O/colour.json
done
