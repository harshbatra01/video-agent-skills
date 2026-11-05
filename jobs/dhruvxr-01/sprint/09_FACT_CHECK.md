# 09 Fact check (sprint files vs the measured study)

Status: FINAL, checked 07:51 to 07:54 UTC. Files were still being written; each finding is for the version read then.

## Method
- Source of truth: research/dhruvxr/STUDY.md sections 2, 4, 5, 7 (plus 9 where files cite it), raw/hand_numbers.json, raw/shots_by_hand.json.
- Checked: 01 to 08 in jobs/dhruvxr-01/sprint/. Not BRIEF.md, not this file.
- Per file: numbers that contradict the study (line quoted, study value given); judged or unverified claims stated as fact with no label; invented counts (views, likes, followers); real third-party logos or copied assets proposed; em dashes.
- Severity: 3 = wrong number or rights risk that would reach the build. 2 = wrong or mis-cited number, or unlabelled judgement, that could mislead a decision. 1 = rounding, wording, small mismatch.
- Em dash scan (U+2014) and en dash scan (U+2013) over all 8 files at 07:51 and 07:52 UTC: 0 in every file.
- How read: 02, 03 read in full. 05, 06, 07, 08 checked by targeted grep on numbers, logos, stock, LUFS, fps, gap and flash counts, not line by line. 01 read header and notes. 04 grep only.
- Not checked: audio, playback, web sources quoted in files (no re-fetch), proof/, sheets/, skill-draft/.

## Two errors inside the study itself (affect other files)
- S-1, severity 2. STUDY section 7: "There's a 2.4 s gap with no text (f67 to f121)". f67 to f121 is 55 frames = 1.83 s at 29.97 fps. 08_RED_TEAM.md line 18 caught this. 05_RULE_BOOK.md R38 copies the wrong value (see 05).
- S-2, severity 1. STUDY section 2: "White flash frames (1 to 3 f): 5 events (f10, f45, f78-80, f195-196, f243-244, f322)". That list has 6 entries. f78-80 is a blowout and f243-244 a logo bloom, so "5" vs "6" depends on what counts. Any file that quotes "5 white flashes" should give the frame list.

## Findings by file

### 01_SHOT_LABELS.md (final 07:50)
- Sev 1. Header: "30 fps, 494 frames, 16.47 s". STUDY section 2: 16.49 s (494 f). 16.47 is 494/30; 16.49 is ffprobe. Say which.
- Sev 1, good note. "ffmpeg decoded 493 WHP frames; the hand list says 494." Real 1-frame conflict with raw/shots_by_hand.json ("frames": 494). Labelled. Build should use 493 if decoding agrees.
- Shot counts 31 and 26 match hand_numbers.json. Shot type is labelled JUDGED. No logos proposed. No counts. Pass.

### 02_LOOK_COLOUR_TYPE.md (final 07:51)
- Sev 1. "near-black (Y < 0.10) WHP 76%, ATN 60%. This agrees with STUDY (0.14 to 0.25, 63 to 78%)." ATN 60% sits below the study's 63% (STUDY section 2: ATN 63%). Different method (mid frame per shot vs 2 fps). Say "close to", not "agrees".
- Sev 2, labelled conflict. "dhruv" fade: 02 says hold f310 to f347 (38 f), fade f348 to f390 (43 f). STUDY section 4 and effect 23: holds 56 f, fades over about 24 f (f366 to f390). The file flags this as a disagreement. The build needs one curve; 02's per-frame numbers are the measured ones.
- Sev 1. "Hard on, linear fade out" for "dhruv" matches STUDY ("no fade" in).
- Third-party brand colours (Whop #AB271C, Wise, Figma, Adobe, Meta) are listed with "do not copy". Pass on rights.
- New claims (horizontal lines on ATN backgrounds, graphics "on threes") are labelled JUDGED and "not confirmed by eye". Pass.

### 03_PAGE_STUDY.md (final 07:49)
- Sev 1, labelled. Line 54: self-claims "over 10 million views across platforms" and "10K+ leads". Marked "Not seen, not X numbers, not used." Keep that label on any reuse.
- Line 7: "No X view, like, repost, reply or follower counts appear below." Confirmed: no invented counts.
- Sev 1. Line 44: "brand cards every 4 frames". hand list: Apple 4 f, Meta 4, Whop 4, Wise 4, Figma 3, Adobe 4, asterisk 4, near black 1, ChatGPT 2. STUDY says "2 to 4 frames each".
- Sev 1. Line 44: voice sample "Yo," at 0.0 s. Not in STUDY section 7; from the transcript. Not checked by me.
- Line 45: "ATN bass drop plus 'Attention' at 5.1 s (34% in)": 5.1/14.95 = 34%. Pass.
- Post times are DERIVED from post IDs and labelled. Post IDs differ from the video file IDs (media IDs); not checked against x-videos/README.md by me.
- Line 39 "likely puts the post in front of the client's own followers" sits under "Judged (UNVERIFIED)". Pass.

### 04_WEB_RESEARCH.md (grep only)
- Sev 1, labelled. Line 64: "10M+ Views Across Platforms And 10K+ Leads" from fueler.io, marked SNIPPET. Self-claim, not measured.
- Line 108: "73% drop off before 15 s (Wyzowl 2026)" marked "UNVERIFIED, do not use". Pass.
- Line 107: vendor-blog rules ("hook in the first 3 to 5 s", "show real UI within 10 s") marked SNIPPET, "claim-to-URL match not confirmed". These are not study numbers; do not merge them into the rule book as measured.
- Line 70 lists Rotato (a third-party tool) for tilted device shots. Tool, not an asset. If used, its device frames may carry Apple hardware likeness; check before use. Sev 1.

### 05_RULE_BOOK.md (grep)
- Sev 2. R38: "One gap of about 2.4 s (about 72 f) with no copy ... Ex: ATN f67 to f121". Wrong: f67 to f121 = 55 f = 1.83 s (study error S-1). Fix to "about 1.8 s (55 f)".
- Sev 1. R9 and R68: "WHP wordmark f421 to f494". Last WHP frame is f493 (494 frames, f0 to f493), or f492 per 01's decode.
- Sev 1. R10: "ATN 9 shots, brand cards every 4 f". Cards run 2 to 4 f (Figma 3, ChatGPT 2).
- Sev 1, cross-file. R1 and checklist: "1920x1080 (plus 1280x720 copy)". 07 builds a 1280x720 master. STUDY 9.1 default is 1920x1080. Pick one.
- Sev 1, cross-file. R57: near-black "at least 60% (ref 63 to 78%)". 07 says "near-black 63 to 78%". STUDY 9.2 target is "at least 60%". Both cite the study; they disagree on the pass mark.
- Sev 1, cross-file. R64 says keep LRA 3.1 to 3.8 LU; 07 line 89 runs loudnorm with LRA=7. The loudnorm LRA is a ceiling, so not a contradiction, but the QA check should measure LRA against 3.1 to 3.8.
- Pass: R5 (31/26 shots, median 6 f/4 f, 35%/58%), R7 (bursts 0.7 to 0.8 s, 43 to 69% in), R8 (11% vs 16%, 0% vs 17%), R11 (15/11), R33 (20 words, 8 cards; WHP about 12), R34 (median 2.5, 0.9 to 1.2 s), R60 (12 of 22, 55% vs 27%), R63 (13 words, 0.0 to 5.2 s), R64 (-5.4 LUFS +2.1 dBFS; -14.1 LUFS +0.1 dBFS). All match STUDY section 2.
- Rights: R14 and R69 drop all real brand cards (Apple, Meta, Whop, Wise, Figma, Adobe, ChatGPT, asterisk). R68 drops "dhruv" and the Whop marks. Pass.
- R12 "famous products, all saying 'a great product'" is tagged [J]. Pass.

### 06_SCRIPTS.md (grep)
- Rights: line 224 bans real logos, names, UI "not even as parody or blurred". Line 206 uses fictional marks only. Pass.
- Sev 1. Line 208 eye macro and line 239 music, font, stock licences "UNCHECKED". Labelled; must be cleared before build.
- Sev 1. Line 145: WHP-style plan "Shot count 30 ... Shots of 4 f or less: 13 (43%)" vs WHP 31 and 35% (hand_numbers.json). It is a plan, compared openly. Pass.
- Line 10: "f0 to f29: 9 shots of 2 to 4 frames" matches the 8 to 9 shot range. Pass.
- Sev 2, copy risk. Script 1 "Taste" (cards table) reuses ATN's frames one for one (f2, f30, gap f67 to f121, f122, f153, f180, f216, f246, black f279, mark f310, tail f390) and ATN's sentence frame: "Attention" / "attention isn't earned" "by features." / "It's earned" "by perception." becomes "Taste" / "taste isn't" "a prompt." / "It's chosen" "frame by frame.". No ATN line is copied word for word, but layout, timing and grammar are. 08 item 20 flags the same COPY risk. Shift timings and change the sentence frame.
- Sev 1, unresolved conflict. Script 1 card 8: "hold f310 to f365 (56 f); fade out f366 to f389 (24 f)" uses STUDY's curve. 02 measured hold 38 f and fade f348 to f390 (43 f). Pick one.
- Script 1 gap row: "f67 to f121, 1.83 s". Correct (unlike 05 R38).
- Script 1 word count: 3+2+3+1+4+2+3+1 = 19. Checked. Inside 12 to 20.
- Scripts 2 and 3: grep only (16-word own voice-over, 495 f and 465 f plans). Not read line by line.

### 07_BUILD_PLAN.md (grep)
- Sev 2. Line 17: "1280x720 master (STUDY.md item 1 says 1920x1080 delivery is also possible; default here: build at 1280x720". Mis-cites the study. STUDY 9.1: "Default delivery 1920x1080 at 30 fps (the reference is 1280x720; we can deliver both)." The study's default is 1080p, not an option.
- Sev 1. Line 21 and line 103: near-black "63 to 78%" as the pass range. STUDY 9.2 target is "at least 60%". A dark piece at 85% near-black would fail 07's gate but pass the study's. Line 123 already shows the proof frame at 88.2%.
- Sev 1. Line 113: "ATN's hook relies on famous marks [S]". STUDY does not say "relies"; it says the burst is famous brands on one idea. That part is judged.
- Line 115: "-9.5 LUFS, not ATN's -5.4 LUFS" matches STUDY. Pass.
- Line 52 and G3: SF Pro is Apple-licensed and not used; Inter (OFL) used. Pass.
- Line 46: Pexels and Pixabay stock "Not checked". Labelled. Faces need releases (08 item 13).
- Proof result lines 121 to 123 are measured on our own render and say "Not viewed by eye". Pass.

### 08_RED_TEAM.md (grep)
- Line 18 correctly flags the study's 2.4 s gap as 1.83 s. Confirmed: 55 f / 29.97 = 1.835 s.
- Viewer quotes in the table are role-play. Header says "Every objection is judged" and phone sizes are "estimates, not measured". Labelled. Pass.
- 08 reviewed only script 1 of 06 (header says so). Scripts 2 and 3 have no red-team pass yet.
- Line 29: "lookalike marks are a trademark risk". Agrees with 06 line 206. Pass.

## Top fixes, in order
1. 05 R38: change the no-copy gap to about 1.8 s (55 f). Study section 7 says 2.4 s; its own frames give 1.83 s. (Sev 2)
2. 06 script 1: break the one-for-one ATN timing and sentence frame. (Sev 2, copy risk)
3. 07 line 17: STUDY 9.1 default is 1920x1080 delivery; 07 calls it an option. Settle the master size across 05, 06, 07. (Sev 2)
4. "dhruv" end-mark curve: 02 measured vs STUDY, used by 06. Pick one. (Sev 1 to 2)
5. Near-black pass mark: at least 60% (STUDY 9.2, 05) vs 63 to 78% (07). (Sev 1)
- No invented view, like or follower counts in any file. The only counts are the fueler.io self-claims, labelled in 03 and 04.
- No file proposes a real third-party logo or copied asset. 05, 06 and 07 all ban them.
- No em dashes in any file.

## Open items (not done by this check)
- 05, 06, 07, 08 read by grep, not line by line. 04 grep only.
- 06 scripts 2 and 3 not read line by line.
- 03 post URLs and IDs not checked against x-videos/README.md.
