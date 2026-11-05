---
name: edit-loop-guard
description: Stops the iteration loops from the Elon video (18 versions in 5 days). Holds what the user actually meant by each important note, and the rule that stops each loop. Use it on any narrated video edit: before planning or storyboarding, before building, whenever the user gives edit notes or timecodes, whenever an effect, sound, graphic or B-roll is added or changed, and before showing any version. Pair with editing-playbook and the job's DADDY.md.
---

# Edit loop guard

Written 4 Nov 2026 from the full prompt history of one 18-version mini-doc job. Numbers like (#30) are prompt numbers in that history.

The intents below are Claude's reading of the user's words. The user can overrule any of them. The guard warns and proposes. It never refuses a note. The user's taste decides, then the decision is logged.

## The one intent
The user asked for a video with "an equal opportunity for going viral" (#1) and loved the reference for its "impact and psychology of retention" (#15). Copying the reference was the method, not the goal.

The Elon job drifted. Each round asked "does it match the reference and the last note?" and no round asked "will a stranger stay?" It ended at 18 versions. The user's main reason: too many effects and sounds in the first seconds, hard to grasp.

**Test for every decision: does a first-time viewer understand this and want the next second?** If matching the reference hurts that, say so.

**First priorities from the user (4 Nov):** the Altman video's colour, pacing and overall vibe, and video B-roll like Altman's instead of photos (loops 4 and 13).

**Ask when needed:** the user said on 4 Nov: if you need my approval, feedback or input at any point, just say so. Say it plainly in one line. Do not guess, and do not stall.

## The 13 loops

### Before anything is built

**1. Reference study that never reached the edit (#13, #22)**
- Said: "you didn't go through the reference", then "if you were able to detect them why didn't you apply them, what stopped you".
- Meant: if you saw it, use it or tell me why not.
- Rule: a reference study ends in a numbered list. Each item is marked use, change or drop, with where it goes. The user sees the list before the first build.
- Rule: measure every frame of key moments. Contact sheets hid the Altman grid build, and a median alone hid the slow pace.

**2. Sound settled after the picture (#15, #22, #52 to #58, #66, #67)**
- Said: "the main mistake you made was not syncing music first". Yet the synth stand-in stayed until v13 and the voice changed at v14, so the timing moved late.
- Meant: settle the sound once and early, because everything sits on it.
- Rule: no picture build on a stand-in voice or stand-in music.
- Rule: the voice pick includes energy and expression tests. On Elon those came after the voice was chosen, and the user kept the old read anyway.
- Rule: try music against the real voice. Propose start point and levels on that first try. Elon's final answers: music in 0.5 s late, voice +2 dB, music -4 dB.
- Rule: if a late swap is asked for, say what it will move before doing it.

**3. Length decided last (#44, #55, #72)**
- Said: "4 seconds is nothing", "keep the better parts in and remove the bad parts", "very boring, not relatable stuff".
- Meant: short from the start, with only the parts that earn their place. The length went 81, 84, 80, 50, 43, 40 s, and the full picture was rebuilt along the way.
- Rule: lock the target length before the storyboard, using the real read and not a word-count estimate.
- Rule: mark any line that is boring or not relatable before it gets pictures.
- Rule: keep every longer script. The user asked for the 1:20 one back (#72).

**4. Footage gap hidden by stills (#22, #30, #40)**
- Said: "as much videos as there were in reference". The gap never closed: about 17% moving clips in v18 against about 67% in the reference.
- Meant: real moving footage, and tell me plainly if we cannot get it.
- Repeated 4 Nov: "most of the time, we used photos as B-rolls", and of Altman's videos, "I want the same". So the target is Altman's share, about 67% moving footage, unless the user changes it.
- Altman's look includes real interviews, hearings and news hosts. Open-licence sources could not supply these on Elon (7% news footage against 29%). Settle clip rights with the user before the footage map.
- Rule: make a footage map before the storyboard. If the share cannot be reached, say so before building and give options. Never fill with stills quietly.
- Rule: every status report states the moving share until it meets the target or the user waives it.
- Rule: B-roll must match the word being said. The subject fills at least 50% of the frame, is never cut by the edge (#16, #30), and is never a stand-in face.
- Rule: the user's taste beats the B-roll score (#47).

**13. Colour and design never planned (user's verdict, 4 Nov)**
- Said: "the overall colour theme and design choices were boring and non-engaging". Altman has "very good colours, good pacing, and a good colour theme and overall vibe. We want that, first of all."
- Meant: the video should look alive and varied, not only well made.
- Measured with `word-matched-broll/scripts/colour_stats.py`, 2 frames a second:

| | Altman | Elon v18 |
|---|---|---|
| Mean brightness | 0.36 | 0.24 |
| Near-black pixels | 36% | 44% |
| Mean saturation | 0.31 | 0.30 |
| Vivid pixels that are red, orange or yellow | 56% | 86% |
| Vivid pixels that are cyan or blue | 34% | 11% |

- Reading: Elon was not less saturated. It was darker and nearly all one warm range, brown and gold. Altman mixes warm and cool.
- From one frame sheet of each: much of Altman's colour seems to come from the footage itself, such as blue news sets, screens and red clothes. Claude's reading, not measured. So moving footage and colour are one problem, and a stronger grade alone will not fix it.
- Rule: plan colour in the storyboard, scene by scene, before building. Show one frame sheet beside Altman's for the user's verdict.
- Rule: run the colour numbers on the storyboard frames and every version. They are a warning light. The user's eye decides.

### While building

**5. Each note right, the total wrong (#30, #55, #77 to #79)**
- Said on 19 Oct: sound effects "at very less places, not a lot". Then notes added clicks, montage sounds and a gavel, each reasonable alone. Result: 28 of 51 sound cues in the first 5 s, which the user now blames for the flop.
- Meant: a sound should feel caused by what is on screen. Sync was the point, not more sound.
- Rule: keep a budget for the first 5 s: sound cues, effect types, ideas the viewer must take in. Set it before the build by measuring the references. The user picks the number.
- Rule: any note that adds to the opening gets a reply with the new count. If it goes over budget, say so before building and propose what comes out.
- Rule: sounds match frame changes exactly, flashes stop when the sound stops (#66), and never repeat one sound back to back or on a timer (#24).

**6. Starting weak and climbing (#22, #24, #30, #40, #60, #63, #64, #65, #72, #73, #74)**
- Said, in 11 prompts over 4 days: "looks like a border glow", "still not done right", "still looks weak", "much more than what we have".
- Meant: an effect the viewer can see at normal size, like the reference, at the edges only. Each round Claude tried a safe level, and the 12.5% preview never reached the final cut.
- Rule, for any look: first show 3 or 4 strengths on real frames of this video beside the reference, including one that looks too strong. The user points at one. Never climb one step per version.
- Rule: say plainly what it does: whole frame or edges, all frames or some (#72).
- Rule: look for an existing tool or look before making one by hand (#24).

**7. Fixing the wrong thing (#42, #51, #53, #55)**
- Said: "you replaced the wrong nine shares line". The phrase appeared twice. The note said 7th second, the real spot was near the 5th. The user approved a sheet of the look, not the place.
- Meant: fix that exact moment, and my timestamps are approximate.
- Rule: before acting on a note, read it back: the words spoken, the time, a frame before, a frame after.
- Rule: if the note could mean two places or two elements, ask one question with frames. Give each element a name and ID in `DADDY.md`.

**8. Approved things coming back wrong (#42, #66)**
- Said: "how did you come back to 9 squares, we had 4, this is a blunder", "how are you losing so much of the context we just discussed".
- Meant: what I approved stays approved.
- Rule: keep a locked list in `DADDY.md` of each approved item with its time and values.
- Rule: before showing any version, compare the new plan against the list. Anything missing or changed stops the show, unless the user asked for it.
- Rule: use one build script per job, edited forward. Elon left 76 entries in `tools/`, many one per version.
- A rejection applies to its context. The 9-box grid was rejected because it was portrait (#30), so landscape reopens it as a question.

**9. Elements that say nothing new (#22, #26, #46, #70)**
- Said: "so pointless, we have been naming him for 15 seconds". Also: no empty frames with a little text unless it is a deliberate rule break, and a map covered a caption.
- Meant: nothing on screen unless it adds something the viewer does not have yet.
- Rule: run the Daddy gate before building, and also ask "does the viewer already know this?"
- Rule: a user request goes through the gate too. Flag doubts once, then do what the user says. The logo outro was asked for (#30) and removed later (#70).
- Rule: overlays never cover captions.

### Working together

**10. The user having to chase (#23, #38, #39, #68, #73)**
- Said: "What do you want me to choose, say now?", "is the video rendering?", "did you do the chromatic aberration frames task?"
- Meant: I should not have to ask what is happening or what you need.
- Rule: keep a note ledger. Each note gets a number, a status and proof (a frame, a measurement). A note with many points gets a table answering every point.
- Rule: each reply ends with one state: building, rendering with a time estimate, or waiting on you. Say exactly what is being waited on, in one sentence, with a recommendation.

**11. Render cost not stated (#65, #68, #69, #71, #77)**
- Said: "don't render yet, I'll order more edits", "tell me first if you can do these fixes without starting a render", "will this require a separate render".
- Meant: let me see before we spend time and limit, and collect my notes first.
- Rule: every reply to a note says, unasked, whether it needs a render and about how long.
- Rule: preview with frames. Use sound-only and cut-only changes where possible. Collect notes until the user says go.

**12. A go-ahead for every step (16 of 79 prompts)**
- Said: "continue working", "proceed", "whichever one you recommend".
- Meant: when the direction is agreed, keep moving.
- Rule: set the gates up front: plan, first 3 s pilot, 10 s test, full cut. Show before building at each gate. Between gates, keep working without asking.
- Rule: put open questions in one batch, each with a default.

## Every note, in this order
1. Add it to the ledger with a number.
2. Read it back with the words, time and frames (loop 7). For a small, clear fix, one line is enough.
3. Check it against the locked list (loop 8) and the opening budget (loop 5).
4. Run the Daddy gate (loop 9). Flag doubts once.
5. Say whether it needs a render (loop 11).
6. Do it. Close it with proof.
7. If it teaches something reusable, write it into a skill or tool (#22: "converted into reusable skills").

## Before showing any version
- [ ] Nothing on the locked list changed by accident.
- [ ] First 5 s are within budget, with the counts stated.
- [ ] Stranger test on the opening frames: in plain words, what does a first-time viewer understand by 3 s?
- [ ] Every note in the ledger is closed or named as open.
- [ ] Moving footage share stated against the target (about 67%).
- [ ] Colour numbers and a frame sheet beside Altman's.
- [ ] Sound sync measured against frame changes.
- [ ] No empty frames unless deliberate, no covered captions, no cut-off subjects.
- [ ] Said what was not checked. Claude cannot watch the playback or hear.

## Limits of this file
- Left out as noise: key setup, storage, limits, transfers, page name, other work.
- The under-500 cause is the user's read. No skip rate or watch time is on file. Reach or topic could also explain it, so the budget in loop 5 is a sensible guard, not proven.
- This is instructions for Claude. `guard_check.py` next to this file tests what a script can, but only when run. Nothing forces it yet.
