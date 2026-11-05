# Captions and subtitles: making, styling, burning in, disabling, reading

Caption style and judgement (words per caption, placement, when captions step aside for graphics): editing-playbook
`references/captions-and-on-screen-text.md`. Animated caption recipes (kicker + big word, stacked list words, partial-word
rolls): motion-design `references/titles-captions-type.md`. This file is the mechanics.

## 1. Where the timed words come from
- Premiere's own transcripts and caption tracks (`prtranscript.py`, timing.md). When the transcripts are older than the
  current cut, the caption track is the timed script.
- Whisper word timings (`hear.py`) for new audio; edges snapped to the real audio (`speech_cuts.py`, timing.md).
- Type brand names correctly on screen even when a transcript mishears them (Premiere heard a brand as "fix").

## 2. Phrases from word timings (SRT or burned-in subtitles)
- Break a phrase at a pause over 0.3 s, at . ! or ?, or at a Whisper segment start; split each phrase evenly into
  chunks of up to 4 words; end each line at the next line's start or 0.4 s after its last word. Why: grouping on pauses
  alone ran two phrases together, and word-count chunks alone cut thoughts in half ("TOO MUCH MAN PEACE").
- Speech only, never lyrics: stop the subtitles before a song comes in (the song is the audio; lyrics on screen add
  nothing and risk misquotes), and star out swears in on-screen text.

## 3. Burning subtitles in with ffmpeg (code-built posts)
- Write an ASS file from the phrases: uppercase, Proxima Nova Extrabold 70 px, white, black outline 6, bottom centre,
  `MarginV` 560 on 1080x1920 (a per-post margin when the layout needs it), and render it with ffmpeg's `subtitles` /
  `ass` filter. That needs an ffmpeg built with libass: check `ffmpeg -hide_banner -filters` on a new machine (the Mac's
  Homebrew build lacked drawtext, so do not assume).
- Proxima Nova is a licensed font: the boss needs his own files (Adobe Fonts activation gives no file path).

## 4. Premiere caption tracks
- Create: import the SRT under a NEW file name each time (Premiere keeps an old item's captions), then build the track
  by UI or by the bridge (`seq.createCaptionTrack(srtItem, 0, Sequence.CAPTION_FORMAT_SUBTITLE)`, premiere-ui.md).
- Style: `scripts/captions/style_captions.py` on the saved, CLOSED project (captions-style-patch.md, prproj-recipes
  R17). At Lora Italic 58 on 1080x1920 the width limit is about 780 px: split longer lines first.
- Caption tracks draw above every video track: grades and zooms never touch them, graphics on video tracks sit under
  them (prproj-format.md section 10).
- Under a graphic that shows the same words: DISABLE the captions whose midpoint falls inside the graphic
  (`disable_item`, R5), never delete them. One build deleted them, and the next version had to be rebuilt from an older
  save to bring every subtitle back.
- Deleting captions you made yourself (reference-counted clean-up): prproj-format.md section 10.
- Premiere may upgrade captions to graphics on save (items with no SubClip or Components): scripts must tolerate it
  (prproj-format.md section 16).
- Burn in at export: "Burn Captions Into Video" on the subtitle track (window), or an .epr copy with
  `ADBECaptionExportOption` 2 (bridge; 0 none, 1 sidecar .srt). Leave it off when the subtitles are graphics.

## 5. Captions built in After Effects
- Dynamic captions render as alpha elements over B-roll with the subtitles under them disabled; text mechanics:
  after-effects.md section 6; generated from one spec list together with their SFX: after-effects.md section 1.
- In a designed film, keep all captions in ONE separate comp for the whole film, never inside scene comps, so wording
  changes never touch the scenes (motion-design `scene-building.md`).

## 6. Reading burned-in captions in source footage
Frame-exact subtitle spans, the white-only mask, the 1.3% pixel guard, by-eye strips for coloured speaker boxes and
two-line subtitles: timing.md "Long raw footage". Treat every caption span as speech that a cut must not split.

## 7. Checks before delivery
- Captions match the spoken words; none sits over a face or the platform's buttons (safe zones: social-video-formats).
- No subtitle flashes for 1-5 frames at a cut edge (timing.md); look at both sides of every white transition.
- Report stray placeholders in the user's own caption track (a "New Caption" left at 2.3-2.5 s once) instead of
  fixing their layer.
