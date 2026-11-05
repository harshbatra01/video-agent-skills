# Debugging: every failure we hit, and the rule it left

Grouped by where it broke. Each row: what broke, the cause, the fix, the rule that prevents it. App-specific traps
(Premiere project internals, After Effects scripting quirks) are listed in full in premiere-ae-editing; the ones here
are the ones that broke a pipeline run.

## 1. Writing and patching code
| What broke | Cause | Fix | Rule |
|---|---|---|---|
| Patches mangled 5+ times; a JS regex `\b` became a backspace in a template | Git Bash heredocs collapse `\\`, turn `\n` into line breaks and evaluate `$[...]`, even with `<<'EOF'` | rewrote the files with the Write tool | write code with the Write/Edit tools; parse-check (`py_compile`, esprima) before running |
| Two fixes silently lost | a failed text match inside a chained shell command | redone with Edit | one edit per call, confirm each landed |
| A runner patch did not apply, so a render was heading for the same wall | the file was edited without reading it first | stopped the render, patched again | grep that a patch landed before relaunching |
| A literal em dash and curly quotes appeared in a checker that tests for them | the Write tool decodes `\uXXXX` escapes into real characters | constants built with `chr(0x2014)` | build non-ASCII constants with `chr()`; grep written files for non-ASCII bytes |
| A template stopped rendering | a template literal nested inside another one, inside a JS ternary, is invalid there | parentheses or plain string concatenation | parse-check templates (Python `esprima.parseScript` when Node is missing) |
| AE never started a build | a stray `%` in Python %-formatting of the JS | fixed the formatter | build JS strings with `json.dumps`; watch the log for START instead of waiting blind |
| "ReferenceError: W is undefined" in two renders | a new .jsx composed from pieces of older generators without their constants header | header copied | copy the constants header with the pieces |
| A build crashed; shell appends broke | a Python name clash in a patch; apostrophes in shell strings | renamed; patches as script files | never patch through shell strings; unique names |
| Old shots came back after a "fix" | a quoting error in an edit script meant nothing changed | Edit tool, then re-render | after editing a generator, grep the new value in the written .jsx |
| Watermark patterns silently stopped matching | regex escapes inside raw strings (`\\.`) | fixed the escapes | test every regex on a known positive |
| A script built `python3 -c "...open('$f')..."` | file names pasted into code | names passed as arguments | never paste file names into code strings (a crafted name in a downloaded folder could run code) |
| Three scripts ran slices of another script's text | `exec()` | imports with `__main__` guards | never `exec()` another file |
| `cp1252` print crashes on emoji and accented names | Windows console encoding; `python -I` ignores PYTHONIOENCODING | `PYTHONIOENCODING=utf-8`, `encoding='utf-8'` in subprocess, `python -X utf8` | run tools as `python3 -X utf8` |
| `/markets/sports/...` arrived as a Windows path | Git Bash rewrites arguments that look like POSIX paths | full URLs, or `MSYS_NO_PATHCONV=1` | Windows only; not a Mac issue |
| GPU tools and yt-dlp "not installed" | `python -I` skips the user site-packages on Windows; pip gave no yt-dlp exe | run without `-I`; `python -m yt_dlp` | on the Mac use one venv per pipeline |
| A shebang script failed on a Mac | files written on Windows had CRLF line endings | converted to LF | save shipped scripts with LF |
| A batch file overwritten | no check before writing | rebuilt from the transcript (the original Write plus each Edit) | `ls` first; unique batch names |
| A process check sent Ctrl+C on Windows | `os.kill(pid, 0)` is not a test on Windows (signal 0 is CTRL_C_EVENT) | ask the OS properly | `os.kill(pid, 0)` only on the Mac or Linux |
| AE showed "Unable to execute script at line 17" on the user's screen | a syntax error in a generated script | fixed the formatter | esprima-check every .jsx and every spec string before an AE launch |
| Scripts read files that no longer existed or had other names | stale names and docstrings after renames (a docstring named a script that did not exist) | names fixed | after a rename, grep every script and README for the old name |
| Generator bugs (a generator plus a list, a missing `+`, 3-value clips where 2 were expected, an indent mismatch in a text patch) | quick edits under time pressure | fixed one by one | write scripts as files and `py_compile` them before every run |

## 2. Headless Chrome and HTML templates
| What broke | Cause | Fix | Rule |
|---|---|---|---|
| The second Chrome failed in a batch | two instances shared one profile | one profile per port | free port + own profile per instance |
| An Italic font got picked | the fallback search took the first file | recursive search that skips Italic; variable fonts at weights 100 to 900 | list fonts explicitly per family |
| Removing a pop-up crashed someone else's web app | deleting DOM nodes under React | close + Escape + a CSS hide rule | never delete nodes on a site you do not own |
| A timed film was unusable | a sign-in modal and a separate blur layer came back | wider selector, re-applied every 15 frames | a 4 s test film before any timed window |
| Cameras died during an outage | the hide rule threw on a null page head and killed the threads | null-safe hider, 15 s retries, a restart loop | every long job needs retries and a restart path |
| Headless Edge wrote nothing; Chrome crashed on a tall shop page | Edge hands off to a running Edge; renderer crash | normal window height, a fallback (screenshot, quote card) | use Chrome; keep a fallback |
| An old contact sheet showed up inside the new one | the glob caught `_sheet.png` | skip `_` files | prefix helper outputs with `_` |
| Template content bugs (quiz answer always in the middle, "a 18%", colour clashes, markup asterisks showing, a chart covered, an empty first frame) | layout code assumed too much | randomise, an a/an helper, a colour pair picker, a markup state machine, a phone frame, start 0.5 s in | build one item per type and look at it before the batch |

## 3. ffmpeg, frames and timing
| What broke | Cause | Fix | Rule |
|---|---|---|---|
| Black bars inside music videos | bars baked into the file | `cropdetect` auto-crop | detect bars before framing |
| Wide photos cropped badly behind a portrait card | the photo sat behind the card | screenshot-style tweet with the photo inside | choose the layout by photo shape |
| A title card clipped at the edges | text wider than a portrait frame | full width on a blurred backdrop | never crop title cards |
| Renders dropped first frames; joined parts off the grid; QC grabs one frame off; drift of 3 frames in 13 min | seek rounding; MKV's 1 ms clock; B-frames on GPU encodes; a container average rate of 29.974 for 29.970 | trim from `pre - 0.5/fps` + `-frames:v`, quarter-frame seeks, MPEG-TS parts, sequential decode at the nominal rate | frame-exact rules in references/render-pipeline.md section 4 |
| An insert one frame short | a 25 fps file in a 29.97 slot | `tpad=stop_mode=clone`, then `-frames:v` | pad inserts at another frame rate |
| QC tools assumed 60 fps on 29.97 sources | a hard-coded rate | probe every video | never assume a frame rate |
| A third of music-edit events one frame late | 4-decimal plan times | snap to `round(t x fps) / fps - 0.1 ms` | snap every event |
| Stale crop previews | the cache key missed crop centre, scale and y | key on every parameter | caches key on every input |

## 4. Audio
| What broke | Cause | Fix | Rule |
|---|---|---|---|
| True peak over the ceiling | louder beds; an AAC noise-substitution burst | limiter 0.70, `-aac_pns 0`, a true-peak fix pass | measure true peak on every render; a 192 kHz oversampled limiter made it worse |
| A bed played under an insert | it started 0.4 ms after the insert's first frame | `if ga - 1e-3 <= cur < gb: cur = gb` | render and XML share one layout, so the XML check tests the render |
| Renders failed silently | a bed cue inside a removed stretch; a flash one clip early after an insert | 0.5 s tolerance, a story-position map, a dry layout check | dry-run the audio layout before rendering |
| Clip audio mixed into the song (v1 to v4 of a music edit) | every AE footage layer and duplicate has audio on | `audioEnabled = false` in the clip helper | subtract the song from each render after cross-correlating for the AAC delay |
| A +8 dB bed clipped | the gain was baked into the WAV | plain bed + level keyframes | never bake boosts |
| Two previews silent after 2:14 | the temp track was 133.8 s | a looped bed | assert music length covers the cut |
| Hits silently missing (including the biggest landing) | a strict SFX lane guard dropped them | 3 lanes + a bed lane + tail trimming + a report | never drop a cue without reporting it |
| Most booms inaudible on phones; one click file silent | 89 to 99% of their energy under 150 Hz; a 96 kHz file with 97% above 6 kHz vanished at 48 kHz | layered pops (bright top + driven low layer), booms only as weight | measure energy bands after resampling |

## 5. Premiere projects and XML
| What broke | Cause | Fix | Rule |
|---|---|---|---|
| "File Import Failure" on every cutdown XML | sound clips pointed at a `<file>` that declared only video; beds ran past their MP3's end | a proven layout + `fcpxml.py --check`; beds looped as back-to-back clips 0.05 s clear | check every XML; the tell was a `.ims` named after the XML with a blank format |
| No way to test the importer from code | Claude cannot run Premiere's importer | copied a file that already imports on that machine; listed every element ours used that it did not | a known-good file + a checker that passes it and fails the bad ones |
| "could not be loaded, may be damaged" on a valid file | a mask template id taken from an older save had been renumbered | find templates by MatchName and content; a semantic validator | references/review-pages-and-qa.md section 3 |
| Mac paths broken in generated XML | `'file://localhost/' + path` doubles the slash for `/Users/...`; the checker stripped the wrong prefix | write `file://localhost` + path for absolute paths; strip only `file://localhost` (done 14 Oct 2026 in the kit's `fcpxml.py` and both `vcn.py` copies) | test one XML import on the Mac before relying on it |
| Cloned clips drew at the wrong time | clones kept transition refs and node ids | fresh identity, no inherited transitions | open every built project and check the changed times |
| A build destroyed captions | the build deleted captions under graphics | next version rebuilt from the save before it; captions disabled, not deleted | disable, never delete |
| Premiere stalled during a scripted import | about 170 files in one import call (Premiere 2025, reference set) | about 20 files per call, saving after each | batch imports; by the UI, about 12 names per typed batch |
| A render was paired with the wrong sequence | the render was named differently from its sequence | names mapped from the render folder | read names from disk, never guess |

## 6. After Effects runs
| What broke | Cause | Fix | Rule |
|---|---|---|---|
| Scripts silently did nothing; a good render was called a crash | the scripting preference reset by an update; AE 26.5's Home screen ignored `AfterFX.exe -r`; the console launcher shows as AfterFX.com | the user ticked the preference; `AfterFX.com -r`; the runner checks both names | a file-writing ping first; scripts log START; the runner stops after 150 s with no START (Windows) |
| Render "done" but no file (status 3015) | the script went to an AE that was still quitting | wait until no AE process, kill a stuck one, then launch | one AE at a time through the runner |
| Crash Repair and "Save As Untitled" dialogs | force kills; an unsaved scratch project | Continue; cancel | `close(DO_NOT_SAVE_CHANGES)` before quitting; never kill while a file grows |
| AE crashed | 20 items queued at once | one item at a time | one render-queue item at a time |
| Three 1 MB stub renders | AE killed at the DONE flag | wait for file sizes to settle | check sizes, not just flags |
| Wrong or ignored effect values | script scales differ from the UI (Lumetri saturation 0 to 300, Threshold 0 to 1, menu items 1 to 10; Exposure works in gamma space) | probed values | probe doubtful params with a Ramp solid and `saveFrameToPng`; keep a parameter dump per install |
| GPU out of memory; squashed picture | a 9000% Transform stretch; Motion Tile on an adjustment layer | Motion Tile per footage layer | toolkit default |
| Out of RAM | Photoshop left running beside AE | quit helper apps after each job | one heavy app at a time |
| Stale shots after a library edit | the filter and specs are baked into the .jsx at generation | regenerate every block | regenerate after library edits |
| 107 auto-save copies left behind | scripted builds | clean up with the user's OK | save build projects to scratch |
| One un-keyable property aborted a whole block | a parameter that cannot take keyframes (Levels Output White) | the key helper logs it and sets the last value | log and continue; never abort a block on one parameter |
| A cleanup step could close a user's unsaved project (an earlier harness) | it closed any untitled project holding a folder named like its own root | a distinctive root folder name | cleanup steps match a distinctive name and touch only what the script created |

## 7. Data and matching
| What broke | Cause | Fix | Rule |
|---|---|---|---|
| Fact and result matching failed twice | an accented club name in one source, plain in the other | NFKD + drop combining marks | strip accents in every matcher |
| UK stories buried; one artist missed | US pages post far more; one page misspelled the name in 14 of 15 posts | aliases, UK weights, a UK top section | rank home-market stories separately; alias every spelling seen |
| Wrong market names; wrong P&L; HTTP 400 on profiles | the wrong JSON path; read-back started too late; anonymous rows | `data.markets.<id>.outcome`; start from `firstTrade`; skip anonymous rows | sanity-check data against the app |
| Replays showed impossible in-match prices | thin markets flicker and go stale | goal-cam prices, filtered trades and snapshots, resolved 100/0 | never chart a thin market raw |
| A caption said 52% while the app showed 70% | polled mid vs the app's own label | quote the on-screen label | captions match what viewers see |
| Empty results looked like "nothing trending" | geo-blocks return empty data with no error | a fewer-than-N-rows alarm | an empty result is an error |
| A query service rate-limited to 1 request a minute | an outage limit | 14-day cache, 65 s spacing; later dropped from the daily path | cache slow sources and keep them off the daily path |
| A store search matched the wrong release | gaps in the search API | other sources; story swapped when no clean art | check cover art against the release |
| An unverified count sat in an example post | typed by hand | placeholder until read live | no unchecked number in any draft |

## 8. Downloads and sources
| What broke | Cause | Fix | Rule |
|---|---|---|---|
| A 15 minute "not a bot" block | about 15 parallel yt-dlp calls | a throttled function with a lock and a 6 s gap | one YouTube call at a time across sessions |
| 403, "format not available", 0-byte files | two downloads at once | one at a time behind a lock with a PID check | same |
| A 360p file accepted silently | a single-file fallback | a 720p floor, no fallback | check resolution after every download |
| YouTube blocked every route for a day (PO token, embed error 153, a headless player) | the machine's address was flagged | sourcing moved to other routes and own recordings | ask early for a throwaway account's cookies or for the user's own clips |
| A bot check after about 40 downloads; 4K re-downloads blocked | volume | waited; asked for 4K packs | pace downloads; ask for packs |
| Five vertical references failed | a size filter assumed landscape | an orientation-neutral limit | never assume orientation |
| Tools tripped on file names | emoji and special characters | ASCII rename on download | rename on download |
| Goal clips gone the next day | posts deleted (404) | fetch the same day | download borrowed clips the day you find them |
| A social site rate-limited after about 20 quick lookups | profile lookups too fast | stopped at once | read slowly, from a monitoring account only |
| Stock sites returned 403 or 429; some clips licence-restricted | no API keys; "restricted" licence tiers | free sources with tag pages; asked for free keys | ask for the free keys; frame-check every clip for faces and logos |
| Monitoring logins found logged out | session expiry | the user logged back in | check login state before browser reads |
| A doc behind another workspace's sign-in | Claude never signs in | the user pasted text and screenshots | ask for an export, a paste or a share |
| Browser pane screenshots cropped to about 799 px; capture timeouts | a small pane | `resize_window`, a small JS thumbnail overlay of the post grid, one `zoom` capture, then reset the viewport | enlarge first, capture once |

## 8b. Cutdown prep, transcripts and seams
| What broke | Cause | Fix | Rule |
|---|---|---|---|
| Sentence endings clipped ("nearby", numbers, comma endings, a bleeped swear, a two-line subtitle) | subtitle edges are not speech edges; ASR up to 7 s off; digits not aligned; same-voice repeats taken for echoes; a censor mute read as a pause; guards moved cuts into speech; OCR read one line of two | subtitle-guided word alignment, the censor-mute FAIL, a shot guard that never cuts speech, SPARSE / COMMA / DIGITS flags | run the edge-word checks on every cut list, against the raw ASR words too |
| Subtitles flashed for 1 to 5 frames at seams | half-frame rounding; OCR span ends early in motion; narrator cross-fades; in-points just before a switch | frame-exact spans, a pixel guard, narrator outs at the fade start, ins at or after the switch | QC seam sheets plus an eye check of the white seams |
| 9 frames of another camera at a clip edge; 1-frame wrong angles | the shot guard reached only 5 frames | reach of 0.5 s; edge-shot check before rendering | check every edge for stray shots before rendering |
| 60 s of action silently dropped (blind test) | the snapper dragged no-speech points to the nearest word | points more than 0.35 s from any word stay put | snapping must never move no-speech edges |
| Transcripts drifted 5 to 14 s on crackly audio, lost most words in pairing, looped "." tokens, smeared shouting over 2 to 8 s, misheard a key line | batched ASR on noisy audio; an alignment that overwrote its own file | the full WhisperX pipeline, backups, numerals filled from neighbours, words over 1.2 s ignored, subtitles win | keep backups of every transcript; let burned-in subtitles win over ASR |
| OCR returned nothing, or blobs | relative paths (Windows OCR needs absolute ones); bold outlined fonts; coloured boxes | absolute paths, a white-only mask (48% to 91% read), a by-eye strip for coloured lines | measure the read rate; read the rest by eye in one strip |
| Notes pages showed the wrong reasons | a 0.1 s head sliver shifted every reason; partial overlaps quoted whole notes | a 0.3 s sliver rule, list only the dropped lines, clean display copies | derive notes from the same timeline as the render |
| Another video's footage stayed in a cut | the narrator's cross-promo and 4 s of a different person | both cut whole | watch for cross-promo clips while reading the source |
| An on-screen counter skipped 05 to 07 in a long cut | a clip with an increment was cut | item 06 added back | stateful counters stay in order in long cuts (shorts may skip, still open) |

## 9. Long jobs and processes
| What broke | Cause | Fix | Rule |
|---|---|---|---|
| A render started on top of a prep | an empty process query under load read as "not busy" | empty or failed = busy | the heavy-job gate |
| Slow renders | on battery the CPU was capped at 2.4 GHz (about 4x slower); one part at a time; NVENC needed driver 610+ | a wait-for-mains watcher, parallel parts, the cache, a driver update | check power before long renders; name the upgrade |
| The archive and a goal-cam relaunch stopped together | unverified, possibly the chat session closing | not fixed | run always-on jobs outside the chat; check before match nights |
| Background jobs stopped four times | the user closed windows | checked DONE flags and logs, re-armed watchers | resume by checking outputs, never blindly |
| Research agents died; one report lost | a monthly spend limit; a shared search budget | a resume file; reports pulled from transcripts | resume file first; cap calls per agent; agents write their own files |
| One agent overwrote another's helper | shared scratch folder | own subfolders | one folder per agent |
| Disk nearly full | own temp frames (8.3 GB) | deleted only own scratch | check free space before heavy steps |

## 10. Wrong output that passed every check
| What happened | Lesson |
|---|---|
| 18 clean data cards: "these are all SAME types of posts" | vary the kind of post, not the card |
| 40 clean motion videos: "the UI is bad", "I can't watch them" | measure text density and cuts against native references and show a plan page before building |
| A researched text style: "TOOO off beat" | one mock frame first; the user's taste wins on look |
| An auto-crop rule cropped 74 of 171 items | automatic edits default to no change and need a measured trigger |
| A re-cut replaced a delivered post (before the versioning rule) | delivered means `_v2`; a backup was kept in `_temp/superseded` |
| The versioning helper made `_v2` of undelivered drafts | move drafts to `_superseded` before a rebuild; never delete |
| A report said a video "had been posted twice" (it was two videos) | correct wrong claims in the next report |
| Reused older presenter stills although newer ones sat in the shared folder (17 re-renders) | diff overlapping asset folders at intake and ask which set is current |
