# dhruvxr study folder
Start with `STUDY.md`. Videos: `x-videos/` (WHP = _dhruvxr_2116246221421780992, ATN = _dhruvxr_2109649042661908480).

| Path | What |
|---|---|
| `strips/all_*.jpg` | Every frame of both videos, 2 s per sheet (frame_strip.py) |
| `text/*.jpg` | Every frame of each text box, frame numbers on each (tools/crop_strip.py) |
| `frames/*.jpg` | Full-resolution frames used to read and measure text |
| `raw/<code>/` | scores.json, events.json, evsheet/ (repo tools), beat_map.json, colour.json, inverted.txt, sync*.json, envelope_100ms.json |
| `raw/shots_by_hand.json`, `raw/hand_numbers.json` | Hand shot list from the strips and the numbers from it |
| `tools/` | crop_strip.py, text_box.py, box_presence.py (noisy, not used for results), sync_test.py, envelope.py |

Repo tools run unchanged: frame_scores.py, cut_events.py, event_sheets.py, frame_strip.py, beat_map.py, colour_stats.py, metro invert_frames.py.
Installs: none. OCR not installed, so text was read by eye on full-resolution frames and crops.
Rights: the videos belong to their owner; private study only.
