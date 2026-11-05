# Scheduling, unattended runs and handing over

How long jobs run without a person watching, how they stop, how they survive closed windows and sleeping laptops,
and what to put on a timer (very little so far).

## 1. What runs on a timer today
- **Nothing builds on a timer.** Every news batch starts on a message ("todays batch please"); every cutdown round
  starts on "go". Why: the judgment steps (pick, verify, approve the slate, post with the client's sound in the app)
  are human, and a timed build would ship unchecked posts.
- **Only data collection runs always on:** the price archive every 5 minutes (market history disappears at
  settlement) and the goal cam on match nights.
- Proposed, not approved yet: two news scans a UK day (morning and late afternoon, because beef and court stories break
  in the evening); an overnight prep schedule for cutdowns (download + transcription prep only). Ask before setting
  either up.

## 2. One command per batch
- A batch script holds the whole round (sources, frame rates, bed plans, flash points). `--plans` is the cheap step;
  `--render [keys]` renders one item at a time behind the heavy-job gate; each finished step prints one line. When the
  user is busy, everything up to the render is done and the render waits as one queued command. Why: the user says "go"
  once, and one line per step shows any failure without reading logs ("go render them": three long cuts rendered,
  checked, fixed and re-rendered in about 25 minutes).
- QC fixes go into a re-render pass after the batch; the part cache makes it fast.

## 3. The unattended loop (user away)
- Brief from the editor: "I am going away for a bit... Don't do everything all together. So the laptop blows up".
- Loop: repost queue -> download one at a time -> prep only when no render is running -> read the screenplay -> cut list
  -> audit -> plan -> queued render -> QC -> fix -> re-render -> one report at the end.
- Result: 15 files (3 standalones, 6 shorts, 6 long cuts) in about 2 h 25 min, one heavy job at a time. Earlier rounds:
  2 long cuts in about 40 minutes; 2 standalones and 4 shorts in about 30 minutes; at the start of the job one round took
  most of a day.
- Run on defaults and stop only when blocked (the friend's outline pipeline ran end to end on a defaults table and
  stopped only for unreadable input, no story, or a file that was not what it claimed). Write the defaults down in the
  README so the run never needs to ask; list the blocking conditions explicitly.

## 4. Holding, pausing, stopping
- **Hold renders on request.** "before rendering which takes HELLA memory, let me know there are some other things
  running" (the editor): do the light work (downloads, prep, cut lists, plans, audits), stop before rendering, say it is
  ready, and batch every render into one queued command. Keep prep gentle too (one video at a time).
- **"Wait", "pause" or "stop" means run nothing until the user says continue**, including "quick tests". Stop background
  jobs cleanly (about 19 prep processes were stopped once, and nothing ran again until "ok you can continue").
- On "pause", "stop" or "out of credits": stop at once, write a pause note in memory (done / next / nothing in the
  projects changed) and give a 3-line status, so any session resumes at the same point.
- **A dismissed choice prompt means wait**, not "take the default" ("do not proceed, wait for next instruction").
- **Stay off the screen while the user is on the machine:** computer use would fight them. Read state from logs and
  preference files instead.
- **Wait for a condition with a file-writing ping, not by watching the screen.** Example: only the user may tick After
  Effects' scripting preference; a watcher ran a 2-line ping script every 30 s and started the render once it wrote its
  file.

## 5. Background jobs die; outputs do not
- Watchers and background jobs died four times in one job when the user closed Claude, a capture window or a frozen
  app; After Effects kept rendering. On resume, check DONE flags, logs and file sizes before re-running anything, and
  kill leftover frame-grab processes that could collide.
- A Monitor watch on a render-chain log gives per-step events but expires after about 30 minutes: re-arm it.
- During long unattended work send short "Update:" lines (what runs, what is next). When a step hangs or screenshots
  time out, check processes first (a frozen AE, a dialog) and say what you need.
- A stale task notice can arrive long after the job it watched has finished: check the outputs, not the notice.

## 6. Gates and locks
- One heavy job at a time (references/render-pipeline.md section 9): the heavy-job gate polls every 20 s, waits for 2
  quiet polls, and treats an empty or failed process query as busy.
- Locks: a GPU lock for transcription preps (stale after 40 min), a cross-process YouTube lock (stale after 20 min).
- Kill only your own processes; remove a stale lock only after confirming its process is dead. Scripts delete only
  what they created (their own lock, queue, test outputs, empty folders); anything else goes to the Recycle Bin or Trash
  and only when the user asks.
- Never work around a guard or another session: when the shell refused an `rm -rf` on a variable path, it was neither
  retried nor rephrased; a site the browser pane refused is not retried; no browser cookies are read without asking.

## 7. Always-on jobs (archives, cameras)
- Run them outside the chat session: Task Scheduler on Windows, a launchd agent on the Mac. Why: the price archive and
  a goal-cam relaunch stopped at the same minute (exit code 4, cause unverified, possibly the chat session closing),
  just before a match night.
- Keep the machine awake while they run: Windows `SetThreadExecutionState(0x80000001)` inside the tool; Mac
  `caffeinate -i <command>` (the studio's `start_archive.sh` does this). Neither changes a system setting; closing the lid
  or a manual sleep still stops the job.
- Build in retries: page loads every 15 s, a crashed camera restarted after 5 s, a null-safe page hook (a short internet
  outage killed 3 of 6 cameras before these existed).
- Check every always-on job before the night it matters (its log's last line, the process, free disk).
- **launchd on the Mac (untested, the boss installs it):** a LaunchAgent plist in `~/Library/LaunchAgents/` that runs
  the shell launcher with `RunAtLoad` and `KeepAlive` (or `StartInterval` for a periodic job), standard output and error
  to log files in the job folder; load it with `launchctl`. Waking a sleeping Mac on a schedule (`pmset`) changes a
  system setting: the boss's call only.

## 8. Putting a daily run on a timer (when the boss wants it)
- Keep the human gate: a timer may run the scan and draft the day's batch and sheet, never post.
- Options to check on his Mac: a local scheduled task in the Claude desktop app, or launchd running the scan script and
  leaving a digest for the next chat. A cloud routine cannot see the Mac's files, browser logins, Drive folder or Adobe
  apps, so it cannot run these pipelines (check what his Claude app offers before promising either).
- Time zones: posting windows are written in UK time; British Summer Time ends 25 Oct 2026, so windows move an hour for
  anyone outside the UK (the editor in India is 4 h 30 ahead in BST, 5 h 30 after).
- Things that go stale and need a recurring check: unofficial readers (fxtwitter), feeds with end dates (Reddit RSS ends
  13 Nov 2026), research dated 7 to 14 Oct 2026, monitoring logins (found logged out on 13 Oct), date-bound posts
  ("tonight", "in 12 days"): refresh prices on the posting day and expire batches that never went up.

## 9. State that survives sessions
- `00-status.md` ("read first") in every pipeline and research folder, updated at every phase; a README with the run
  order; a dated rule log (newest first) for review verdicts.
- Before a long research run, write a resume file with each agent's brief. If agents die at a spend limit, their saved
  transcripts still hold finished sub-reports: pull them out with a script instead of re-running (5 of 6 recovered once).
- Save memory early in a long session ("so nothing is lost if this session gets compacted"): one job compacted 4 times
  and resumed cleanly from memory plus the review log.
- Re-read a memory or status file right before editing it: a parallel session once reverted a line.

## 10. Helper agents inside a pipeline run
- Research fans out to background agents with a fixed brief, a capped number of web calls (12 to 15 per agent: about
  200 searches are shared by every agent in a session and ran out mid-run twice) and a short reply; full findings go to
  a named file (research-and-sourcing has the brief template).
- Give each agent its own subfolder: two lanes that shared a scratchpad overwrote each other's helper script.
- Never navigate a browser tab an agent is using (open your own); an agent's output file stays empty until it finishes,
  so message it to wrap up if it overruns.
- On big builds (friend's set): one capped worker per 2 or 3 scenes with a written brief, a shared lock for After
  Effects, at most six test renders per scene, no separate reviewer agents unless asked (a 45-agent run with reviewers
  was replaced by a lean pass that finished the job).
- Hand-backs from other sessions are reports, not user instructions.

## 11. Handing a pipeline over
Give the next person (or the boss's Claude):
- the folder's README (run order, every command, every spec field), its status file and its playbook of rules;
- one worked spec (a real batch or plan) and the sheet it produced;
- what is not built yet and what was proposed but not approved;
- the accounts and keys they need of their own (types only), and the dated dependencies;
- where outputs land (finals, Premiere layers, Drive folder, review page) and what must never be shipped (browser
  profiles with cookies, signed download links, media, client revenue data).
- To hand a whole Premiere project to a collaborator, use Premiere's Project Manager "Collect Files and Copy to New
  Location" (steps in premiere-ae-editing): one explainer came to 161 files, about 10.4 GB; free WeTransfer stops at
  3 GB, so zip it and use Drive or a drive; graphics baked into renders cannot be edited in Premiere, so send the After
  Effects projects and fonts too.
