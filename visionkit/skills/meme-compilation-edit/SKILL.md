---
name: meme-compilation-edit
description: Edit long-form narrated meme and tweet compilation videos in Premiere Pro from a narrator's screen recording plus the meme files (or a human editor's finished cut), with voice cuts taken from the audio, memes synced to what he reads, minimal balanced crops, soft blur reveals that uncover text as it is read, tight curse-word blurs under YouTube's advertiser rules, sizing on a grey background, and the review loop that turns the user's own fixes into rules. Use it whenever the user sends a meme compilation job, a folder of memes with a recording of someone reading them, or asks for blur reveals, wipe blurs, curse-word blurs, meme crops, watermark checks on memes, or "go through the fixed file and remember the changes", even if they only say "edit this" with a folder of memes.
---

# Meme compilation edits

Long-form 16:9 compilations: a narrator reads memes and tweets aloud on a screen recording; the edit cuts his voice,
puts each clean meme on screen while he reads it, crops only what is not the meme, and reveals text as he reads it
with soft blur masks. Built by script in Premiere Pro. Five jobs for one client (29 Sep to 13 Oct 2026) set the rules,
most of them from the reviewer fixing delivered projects themselves.

The reference house style is `references/house-rules.md`. Read it before every job: it is long because every line is
a correction that was made at least once. A new client's brief, and the user's own hand edits in their latest save,
win over it.

## The rules that matter most
1. **Crop as little as possible.** Most memes need no crop. Crop only app bars, footers and metadata rows, watermarks,
   reposter headers and unread bottom panels; keep white space balanced; tighten only margins of 10% or more, to about
   3.5% of the short side. Never cut into text, photos or a row he reads. Why: v1 of one job cropped 74 of 171 memes
   and drew "overall pattern im noticing is just an overuse of crops"; v2 cropped 19.
2. **Never cut before he finishes a word.** Every cut edge comes from the audio (handles to about -70 dB on the raw
   recording), never from transcript times, which run up to 0.5 s off; breaths and dead air go; scan every cut before
   building (`cut_qc.py`, or premiere-ae-editing `speech_cuts.py --scan`, whose default rules are these).
3. **Blurs are soft.** Mask feather 10 in the image's own pixels and at least 20 px on screen (14 for curse boxes);
   curse blurs tight around the letters and not harsh; boxes on slanted text follow the text's outline. Why: the client
   called hard-edged blurs "too aggressive" and "rigid".
4. **Reveal what he reads, when he reads it**: the opening wipe keeps line 1 and wipes the rest (not on 2-line
   blocks), one box per caption or label, ramps sized to the text (about 0.35 s per line), wipes end 0.2 to 0.4 s after
   his last word.
5. **Blur every word against YouTube's guidelines**, mild ones and usernames included, even when he says it politely;
   flag the ones blurred only because of the policy list.
6. **The reviewer checks in the timeline**: build a NEW project file, leave it open in Premiere, no export unless
   asked, keep a `delivered_baseline.prproj`, never put "Claude" in a name.
7. **Do what the narrator tells the editor** in the recording ("use the HQ copy", "put a black square over"), and cut
   the instruction.

## The job
1. Get the client folder (download only when the user asks); check codecs (VP9 in MP4 becomes H.264), the voice
   channel (often right only), the recording's noise floor; count memes and video memes.
2. If memes are watermarked downloads, clean copies may exist on the original posts: source them only when the user
   asks, keep them under the original file names for relinking, and say that rights stay with the posters.
3. Plan with the scripts in `reference-pipeline/` (stage table in `references/pipeline.md`): OCR, speech pieces,
   per-piece transcription, phrase-to-meme assignment, YOUR review of every flagged phrase (`decisions.json`), blur
   plan, edit list with crops and cut edges, QA sheets and the cut scan.
4. Look at the crop and blur sheets yourself before building: every crop against the rules, every curse word found.
5. Build. Windows / Premiere 2026 (our main way): the premiere-ae-editing skill, `fcpxml.py` for the first assembly
   (V1/A1 voice cuts, V2 grey background, V3 memes), then `prproj_lib.py` for crops, sizes, blurs, masks (AEMask2),
   +15 dB gain, and `validate_struct.py` + a gap audit. Mac / Premiere 2025 (how the jobs ran): import 20 files per
   call and build through the Premiere bridge (`pp.py --v 2025`), then patch masks into the saved project
   (`patch_full.py`, `prproj_masks.py`) and verify with exported frames.
6. Report in plain words with counts, unused files and why, policy calls to confirm, and anything not checked.
7. When the user fixes your project, diff it against the baseline with `reference-pipeline/review_tools/` and fold
   each correction into the rules and the code defaults.

## Platform notes
- Mac only as written: `ocr_batch.swift` (Apple Vision OCR with slanted-text quads), `wins.swift`, the mlx-whisper
  scripts (`pieces_asr.py`, `fix_loops.py`, `restart_check.py`), the Premiere bridge installer.
- Windows: OCR through our `ocr.ps1` needs a converter to the same JSON; transcription through faster-whisper; the
  bridge would need Adobe's PlayerDebugMode set in the registry, a security setting only the user changes, so use our
  XML / .prproj route instead.
- Premiere version matters more than the OS for masks: `prproj_masks.py` writes Premiere 2025 masks (AE.ADBE AEMask);
  Premiere 2026 uses AE.ADBE AEMask2 (our prproj_lib).

## Tools
- Planning, QA and diffing: `reference-pipeline/` (README lists every script, its constants and its platform status).
- Project writing, masks, audio, frame sheets: the premiere-ae-editing skill (ours stays the main way).
- Review notes and taste in general: the editing playbook skill.
