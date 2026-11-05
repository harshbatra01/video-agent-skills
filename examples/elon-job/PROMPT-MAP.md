# Prompt map of the Elon chat (written 4 Nov 2026)

Companion to `../minidoc-02-anthropic-ipo/LAST-VIDEO-RECAP.md`, which holds the effects, rules and verdicts. This file adds only the prompts themselves.
Source: every typed message in the transcript `af7c48e3-...jsonl`, read in full, plus the 9 messages of the side chat `cc5439a4-...jsonl`. Tags and the "led to" column are my reading, matched against the job notes.

## 1. Counts
**79 typed prompts in 5 days.** An earlier handoff note said 102; that count included automatic messages.

| Type | Prompts | Share |
|---|---|---|
| Edit notes and feedback | 22 | 28% |
| Go-aheads and picks | 16 | 20% |
| Asking for a new tool, asset or option (music, voice, effect) | 11 | 14% |
| Limits, storage, transfers | 9 | 11% |
| API key setup | 8 | 10% |
| Questions to Claude | 6 | 8% |
| Other work (page name, Vishvam) | 3 | 4% |
| Deliverables (no-music file, caption) | 2 | 3% |
| Setup and script | 1 | 1% |
| Empty (sent early) | 1 | 1% |

Prompts that touched each topic (one prompt can count for several):

| Topic | Prompts | Which |
|---|---|---|
| Chromatic aberration | 11 | 22, 24, 30, 40, 60, 63, 64, 65, 72, 73, 74 |
| Sound effects | 9 | 22, 24, 30, 52, 53, 55, 77, 78, 79 |
| Voice | 9 | 3, 11, 52, 53, 54, 56, 57, 66, 67 |
| Music | 9 | 15, 16, 17, 18, 19, 20, 22, 56, 58 (plus level and start time in 66, 71) |
| Nine shares and the grid | 7 | 22, 30, 42, 51, 53, 55, 66 |
| Pace | 4 | 13, 15, 22, 44 |
| B-roll | 5 | 15, 22, 30, 38, 40 |
| Script | 1 direct review | 22 (log only). Otherwise only cuts: 44, 55, 71 |

## 2. Every prompt
| # | When | What you said, in short | Type | Led to |
|---|---|---|---|---|
| 1 | 18 Oct | Analyse the reference, find a similar idea, storyboard, script, edit plan. Finish in an hour before the limit ends | Setup | Topic, script, v1 |
| 2 | 18 Oct | Go with all the defaults | Go | v1 |
| 3 | 18 Oct | Key is set, make the real voice, build v2 | Key | |
| 4 | 18 Oct | Pasted the key in chat | Key | Key had to be replaced |
| 5-10 | 18 Oct | How to open zshenv, screenshots, make a new key, permissions | Key | New key set |
| 11 | 18 Oct | Use Brian, build v2 | Pick | v2 |
| 12 | 18 Oct | Fine with the rights, fetch 8 clips, build v3 | Go | v3 |
| 13 | 18 Oct | You did not go through the reference, it is very fast. Analyse all frames | Note | Frame analysis |
| 14 | 18 Oct | Build v4 to the pacing template, open-licence montage material | Go | v4 |
| 15 | 18 Oct | Long brief: exact style replica, music first, pilot the first 2 s, tighten script, B-roll meaningless | Note | Music plan, pilot |
| 16 | 18 Oct | Creepier opening image, head must fit polaroid, here is Looperman | Note | Pilot v4 |
| 17-19 | 18 Oct | Music options from the library, show samples, mix tracks | Request | `MUSIC-OPTIONS.md` |
| 20 | 18 Oct | Scrap that, use the earlier music, proceed | Pick | v5, v6 |
| 21 | 19 Oct | "Notes on v6 with timecodes:" (sent early) | Empty | |
| 22 | 19 Oct | 12-point review of v6, 3 images | Note | v7, `REVIEW-v6-ANSWERS.md`, skill |
| 23 | 19 Oct | Continue working | Go | |
| 24 | 19 Oct | SFX repeating, no sound on the interview, border looks like glow, fix VOIDED | Note | v8 |
| 25 | 19 Oct | Installed HyperFrames, add it, show a one-to-one comparison | Request | v9 |
| 26 | 19 Oct | Elon card is pointless. Create the Daddy file and gate | Note | v9b, v9c, `DADDY.md` |
| 27-29 | 19 Oct | Tokens used, weekly reset | Limits | |
| 30 | 19 Oct | Big note: CA repo, 2x2 grid with a still, label and score all B-roll, camera clicks, Singularity outro | Note | `PLAN-v10.md`, `BROLL-REPORT.md` |
| 31 | 19 Oct | Stay local, continue with the 5 requests | Go | |
| 32-36 | 19 Oct | Free disk, explain tiers, why so much storage | Storage | 4.1 GB to Trash |
| 37 | 19 Oct | Proceed | Go | |
| 38-39 | 19 Oct | Summarise the B-roll findings before I choose. What do you want me to choose? | Question | |
| 40 | 19 Oct | Build it all, replace B-roll, make it a skill | Go | v10, skill `broll-scoring` |
| 41 | 19 Oct | What is this new session option? | Question | Offer to find more video, not run |
| 42 | 19 Oct | "9 shares" repeats at 5 s, use the old animation | Note | v10b |
| 43 | 19 Oct | Whichever you recommend | Pick | v11 |
| 44 | 20 Oct | 4 s is nothing, make it about 50 s. Zoom on pictures looks bad, use separate images | Note | Script v4 |
| 45 | 20 Oct | Build v12 as proposed | Go | v12 |
| 46-47 | 20 Oct | Map covers the caption. Bring rocket shots back | Note | v12b |
| 48 | 20 Oct | Linked GitHub, transfer now | Transfer | |
| 49 | 20 Oct | Continue Vishvam stuff | Other | Pointed to the other session |
| 50 | 21 Oct | Latest version without music | Deliverable | No-music export |
| 51 | 21 Oct | Bring back the 9 shares animation at 7 s | Note | Misread, see 55 |
| 52 | 21 Oct | 4 back-to-back camera clicks. Better voice, HeyGen? | Request | |
| 53 | 21 Oct | Your click file, how to start HeyGen | Request | v12c |
| 54 | 21 Oct | Can VoiceStudio help, public opinion? | Question | Tested nothing, kept for later |
| 55 | 21 Oct | Wrong nine shares replaced. Flash sync, montage SFX, VOIDED sound, cut the boring part, "he owns" gap | Note | v13 (render stopped) |
| 56-57 | 21 Oct | 2-brian-heygen looks best, any more? Succession music. Go with 2 | Pick | v14 |
| 58 | 21 Oct | Your Succession file from about 35 s | Request | v14b |
| 59 | 21 Oct | Delete safe old versions | Storage | |
| 60 | 21 Oct | Try a CA repo on a random image (link missing from the message) | Request | Baseline sheet |
| 61-62 | 21 Oct | Name the new page, more options | Other | Names listed, none chosen |
| 63 | 21 Oct | Use this EachLabs CA skill | Request | Whole-frame shift, not borders only |
| 64 | 21 Oct | Add it to this level, colours and blur near the border | Note | Options sheet |
| 65 | 21 Oct | Choose strong, hold the render. Would Adobe save credits? | Pick | `build_v15.py` |
| 66 | 21 Oct | Music 0.5 s later, 4 squares not 9, flashes stop with the sound, graphic missing, more energy | Note | v15 staged, energy tests |
| 67 | 21 Oct | Keep the current voice | Pick | |
| 68-69 | 22 Oct | Is it rendering? Do all the edits and render | Go | v15 |
| 70-71 | 22 Oct | Remove logo, remove "deal voided", music down, voice up, no render if possible | Note | v16 ("deal voided" kept in the end) |
| 72 | 22 Oct | CA still weak, show much stronger. Give back the 1:20 script | Note | Preview sheet, `SCRIPT-v11-80s-full.txt` |
| 73 | 22 Oct | Did you do the CA frames task? | Question | |
| 74 | 22 Oct | Show 12.5%, strongest at the edges | Note | Preview, not applied |
| 75 | 22 Oct | Latest is good to go, upload now? | Question | Posting checklist |
| 76 | 22 Oct | Caption from this reference | Deliverable | Caption written |
| 77-78 | 22 Oct | Clicks only on the first few images. Do all 9 and the earlier montage | Note | v17 |
| 79 | 22 Oct | Hammer SFX on the gavel at 12 s | Note | v18 |

## 3. Side chat (19 Oct, 9 messages)
- Pasted a list of skills and repos to inspect, read only.
- "The editable timeline isn't exactly the best benefit for me", but tell me if Adobe would give better output.
- Asked why the Roadster clip was a gap.
- HyperFrames test approved.
- End goal stated: Claude should know all available effects and say at the start of a video which one goes where. This became `effects-catalog.md`.
- Asked for a breakdown of the kit's effects and a verdict on Vibe Motion, then parked it: "Not now. Keep the plan in the files for later."

## 4. Limits
- My tags are one reading. A prompt with several notes has one main tag.
- The 8 prompts with your screenshots were read as text only. I did not open the images.
- One gap: the notes say you felt the second half was "stretched", which led to v11. No typed prompt with that note is in this transcript. It may have been said elsewhere.
- Nothing here was checked by watching or listening.
