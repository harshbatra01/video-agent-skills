# Review tools: diff the user's fixed project against what you delivered

Made for the reviewer's fixes on a delivered meme edit (Oct 2026). Every pattern found here became a house rule and a
code default.

1. Put both projects next to these scripts as gunzipped XML (gunzip works in Git Bash; or `python -c "import gzip,
   shutil, sys; shutil.copyfileobj(gzip.open(sys.argv[1]), open(sys.argv[2], 'wb'))" in.prproj out.xml`):
   - `../delivered_baseline.prproj` -> `delivered.xml`
   - his fixed `.prproj` -> `user.xml`
2. Set the sequence name once: `MEME_SEQ="<sequence name>"` (tl.py reads it).
3. Effect dumps (V3 = track index 2):
   `python ../extract_fx.py delivered.xml "<sequence name>" fx_delivered.json 2`
   `python ../extract_fx.py user.xml "<sequence name>" fx_user.json 2`
4. Then:
   - `python cut_diff.py`: voice frames he removed or added, with words and levels (needs `../data/db10ms.npy`,
     `../data/pieces_asr.json`)
   - `python cut_detail.py`: the same per change: head / tail / middle / whole clip, per-frame dB profile
   - `python meme_diff.py`: per meme: span vs speech, crop, scale/position, every blur with key times in RAW recording
     seconds (so retimes are measured against what he says, not clip in-points) -> meme_diff.txt (needs
     `../data/img_ocr.jsonl`, `../data/video_ocr.jsonl`, `../data/edl_full.json`)
   - `python rects.py`: the on-screen rectangle of every meme, yours vs his (-> rects.json)
   - `python crop_sheet.py`: crop sheets, red yours, green his -> crops_N.png
   - `python blur_sheet.py "name1,name2" tag`: mask overlays -> blurs_tag_N.png
5. Read the sheets once, write each pattern into `../../references/house-rules.md` with the date and his words, and
   change the default in the code.

Mac: any Python with numpy and Pillow (the jobs used Homebrew Python for the sheets). Windows: our Python 3.13 works.

Source: adapted from a friend's Mac skill set (Oct 2026)
