# Studying a reference creator or edit

When the user sends a reference, or asks to "match", "learn from" or "copy" a creator, the deliverable is numbers and
a rebuild spec, not adjectives. Measured looks already on file: reference-looks.md. Effect rebuilds (measure, rebuild,
compare frame by frame): motion-design. Measurement tools and installs: premiere-ae-editing (media-toolkit.md,
timing.md).

## Contents
1. What kind of reference is it?
2. Scope first
3. Study an edit at frame level
4. The measurement list
5. Study a page or a niche by frames
6. Measure your own output against the references
7. Read all the research, then filter it through the taste list
8. Keep a structure library
9. Prove the spec with a style test
10. Write it up

## 1. What kind of reference is it?
- **A quality reference** sets the bar, not the style: the editor's high-quality reel (a 0.8 s hook, about 14 s of
  cinematic B-roll under big 2 to 3 word type, then calm talking) came with "THAT IS NOT THE STYLE WE WANNA DO EXACTLY,
  its just to show you how high quality stuff looks". Ask which kind it is when it is not said.
- **The user's own edit** is a starting point, not the bar: "[it] was one that i did, im not that experienced. it nEEDS
  TO BE MUCH BETTER". The bar was the consensus top of a research bank (edits picked by 2 to 4 researchers
  independently).
- **A look to copy** (a client says "do it like this creator"): copy ONE measured look exactly. Mixing "inspired by" ideas
  with generic stock people and drawn props was "really really bad"; one measured look built from real footage of the
  subject passed (second reviewer).
- **A brand to fit** ("use his colours"): keep the reference's motion, swap in the client's own palette and type, pulled
  from the client's site and assets, never sampled from a film.

## 2. Scope first
- "Learn the effects from this page" means the headline effects: one or two per post. Count them, tell the user the
  count and the list, and ask before adding anything else. An analysis that logged every device ballooned to 108
  "effects" for a page of about 30 tutorials ("how is there so many effects").
- Agree which references (all of them, or the ones sent) and what the study is for (a client rebuild, a pitch, our own
  pages).

## 3. Study an edit at frame level
- Every-frame sheets (60 frames per sheet at small size), not one frame per second: edits hide 1-frame strobes, flash
  frames and inserts.
- Many versions of one render: diff small thumbnails against the first and list the frame ranges that differ (12 renders
  were identical except 2.4 to 4.6 s).
- Read the effect stack from the project dump too: nested sequences hide the strobes and transition presets.
- Measure in one pass: shots and median length, cuts within 1.5 frames of a kick, snare or onset (about 65% on a good
  hand-cut edit; report sync against chance), the drop, recurring motifs (a measured tool found a "start lights" motif by
  itself), the letterbox.
- Find the intense moments by numbers (luma change, inverted frames, blur, colour bursts over 12-frame windows) instead of
  watching, then lay every frame of each window out.
- Write a breakdown: a timeline table, an effect inventory, the numbers, the gaps (what the reference lacks: no ramps, no
  type, one grade, a weak first second, a static end card).

## 4. The measurement list
| What | How | Note |
|---|---|---|
| Cuts | ffmpeg scene detection first, then a shift-compensated frame difference to tell real cuts from fast scrolls and find cuts inside insets or one half of a split; merge flash frames that return to the same shot | report shots per minute, median shot, share of shots of 4 frames or less |
| Motion per shot | feature matching between the third and third-last frame of each shot | zoom % per second and pan |
| Captions | OCR at 10 fps in the caption band, fuzzy-matched to word timings within about 2.5 s, confirmed on native-rate strips | words per caption, position, size, timing to about 0.1 s |
| Fonts | render candidate free fonts next to enlarged crops of the sharpest frames | call it a closest match; a mask fit over ~170 fonts topped out at ~82% where a true match scores 93 to 95% |
| Colours | sample with a BT.709 decode | or hex values come out a few levels off |
| Content | label every shot from contact sheets (presenter, split, posts, articles, people, assets, stock, memes, graphics) | share of runtime per kind |
| Sound | split voice from music (Demucs), loudness per stem, beats on the music stem only, song IDs from 10 to 12 s windows, effects as clear level spikes | strip words Whisper invents over a closing music tail ("Thank you.") |
| Voice | words per minute, pauses over 0.3 s, pitch range | |
| Script | code every script by hand (topic, angle, hook type, lesson or not, ending, news peg, real clips, who it addresses) and compare median views per group, top 15 against the rest | count words, wpm, first sentence, questions, "But" sentences, numbers |
| Performance | views divided by the median of the 15 uploads either side (30 neighbours; 3x+ = outlier), by title word and length band; YouTube's Most-replayed heatmap | metadata only, nothing downloaded |
- Stem splitting, OpenCV and song identification are installs: ask the user first (name, source, size).

## 5. Study a page or a niche by frames
- Research by frames, not thumbnails or captions. Two rounds built from stats and thumbnails produced formats the user
  rejected ("I don't think you researched enough"); a third round that checked about 350 to 400 real posts as frames led
  to "based on research do the best formats cook them up".
- Method: download the real viral posts (media only, never run anything downloaded); timestamped contact sheets of 20
  frames, dense in the first 3 s; Whisper transcripts; rank by views divided by the page's followers; flag paid and
  co-authored posts.
- Discount bought reach: organic hits ran at 5 to 12 likes per 100 views, a boosted brand clip at 0.17; mark posts at
  about 0.1% likes per view or lower as "likely promoted" and rank on likes, shares, quotes and saves.
- The sample is picked for hits, so its ratios show what is possible, not what is typical.
- Read a page's last 12 posts slowly in the logged-in browser (a monitoring account, never the page itself), one small
  contact sheet per page; quick lookups got a 429 after about 20.
- Copy the mechanics of the benchmark accounts in a niche (the few with proven organic reach), not their skins.
- Where to read platforms without logins, and the agent brief for research lanes: research-and-sourcing.

## 6. Measure your own output against the references
Before redesigning, measure ours against the references with the same tools. It turns "looks designed" into a list of
fixes. On 22 of our native videos against 49 references: readable words on screen at once 10.5 vs 4; tiny words 27 vs
0; text centre at 26% of the height vs 50%; frames with any text 100% vs 88%; cuts 1.1 per 10 s vs either 0 or 3+.
Eight specific problems came out of it.

## 7. Read all the research, then filter it through the taste list
- Read every research file completely before planning: "go through the research once again properly. You didn't research
  all of them." Brief readers with the taste list (loves and bans) and ask for ranked techniques, new ideas, bases,
  openings, endings and likely hates.
- Filter through the user's verdicts. Research was overturned again and again: it said use the full vertical frame (he
  wanted the band), add a 0.3 to 0.6 s "dip or black" breath before big moments (he banned black frames), skip glitch and
  RGB split for a 40 to 65 audience (he loved RGB-split captions), use the white TikTok text box (he rejected it), give
  every format its own look (read as a template pack). Glows, auras and floods are everywhere in top edits: take their
  type and timing, skip the glow.
- Consensus across independent researchers is a quality signal: sort "top picks first".
- Do not wait for the user to mark favourites on a page; read the files yourself, marks are a bonus.
- Treat inherited research as leads: re-verify live and mark VERIFIED or UNVERIFIED with source and date ("dont take
  everything solid as the sources are a bit ass").

## 8. Keep a structure library
Measure 20+ references and keep a library of storytelling bases with a "how to choose" table; pick one base per piece
and say which. The editor asked to "REALLY try to understand structures of edits... mix and match andsee what fits best
ACCORDING to the edit". The current bases for music edits are in storytelling-and-structure.md; the measured mini-doc,
news-reel and launch-film beats are in reference-looks.md.

## 9. Prove the spec with a style test
Rebuild 10 to 15 s of one reference on the same cut times with your own footage and put it side by side with the
original (a reference mini-doc test landed its captions within 10% of the original's size and position by OCR). For
effects, compare frame by frame with luma, spread and colourfulness per frame until the rows follow the reference
(motion-design).

## 10. Write it up
- A study page with the short version in plain sentences; a numbers table per reference; timelines drawn to scale (the
  picture lane coloured by content, the music lane with drop-outs and hits); each look with frames and its measured spec
  (geometry, palette, fonts, captions, motion, devices); the sound; how the script drives the edit; a "rebuild in
  Premiere" spec; and a method section saying how each number was measured and how sure it is.
- Keep every raw file in a study folder with a README.
- Paraphrase reference scripts in anything published; quote transcripts only in local files.
- Add the measured look to reference-looks.md so the next job starts from it.
- When the user says "the focus is training you", the study IS the deliverable: a breakdown, a proof sheet, a test reel,
  a density table.
