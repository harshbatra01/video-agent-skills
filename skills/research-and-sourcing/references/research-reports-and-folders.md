# Research reports and asset folders

How to keep research and sources so the next session, the boss's Claude or another editor can pick a job up cold.
Why it matters: sessions end and compact (one chat compacted 4 times and resumed cleanly only because memory and a
review log were current), scratch folders get wiped, and a source you cannot trace is a source you cannot clear.

## Contents
1. The research folder
2. Status and resume notes
3. Writing a research report
4. The hand-over per batch or job
5. Manifests: sources, stock, licences, credits
6. The asset folder layout and naming
7. Research pages and pull lists
8. What never ships
9. Worked examples in the kit

## 1. The research folder
```
research/
  00-status.md            read first: what is done, what is next, each agent's brief, open questions
  00-client-brief.md      the client's files digested: claims checked, links checked, rules, banned words
  01-<topic>.md ...       one report per question, numbered in the order they were made
  NN-catalogue.md         the merged, ranked catalogue (formats, references, devices)
  NN-calendar-and-facts.md  dated hooks, every entry with a source and a date
  raw/<NN>/               frames, videos, data and the small tools behind report NN
  raw/<NN>/brand/pages/   the client's brand guide, saved verbatim the day it was found
```
- Separate the distilled reports (start here) from the reference depth (read on demand). Example from one job: five
  short distilled reports (pages and sources, formats, engagement, growth from zero, retention and hooks, 5 to 9 KB
  each) sat in front of reference files of 35 to 74 KB each.
- Date every report. Research goes stale fast: platform facts dated 7 to 8 Oct were flagged as going stale within the
  week, and an older handoff's documents had several claims corrected by newer research.
- Save a client's public pages (brand guide, terms, fee page) the day you find them: one brand guide answered 403 to
  readers a day later.

## 2. Status and resume notes
- Write state down at every phase: `00-status.md`, the pipeline's README or playbook, and the project memory. Keep the
  brief of every agent in the status file before a long run (research-agents.md section 4).
- On "pause", "stop" or "out of credits": stop, and write done, next, and "nothing in the projects changed" so any session
  can resume at the same point.
- Re-read a memory or status file right before editing it: parallel sessions edit the same files.

## 3. Writing a research report
- The short version first, in plain sentences; then a numbers table; then the detail (cards per item); then the sources
  with the dates they were read.
- Every claim carries its source URL, the date read, VERIFIED or UNVERIFIED, and its evidence class (primary, vendor or
  synthesis). Mark disagreements between sources. Say how each number was measured and how sure you are.
- Label folklore as folklore (fact-and-claims-checks.md section 14).
- Say what you left out and why, and what you could not check (blocked sites, budget ran out, geo-blocked platforms).
- Correct your own earlier wrong claims at the top of the next report.
- For a client-facing document: about 600 words, big numbers, plain words; the depth goes in a backup file. Write for a
  reader who was not in the conversation.
- Reports by agents tag each claim primary, vendor or synthesis; two such reports (rules for cutting long videos, rules
  for dynamic music beds) were good enough to keep as references.

## 4. The hand-over per batch or job
- **Per batch of posts:** a table per page (posting window, format, source); what was left out on purpose and why; which
  facts were checked where; what to watch next; the contact sheet and the files attached. The batch file's `note`
  lists the sources checked. Why: the user decides fast when the skips and the checks are visible.
- **Per edit or ad:** build notes with the fact-check flags, each placeholder slot with its timecodes, the rights table
  (licensing-and-rights.md section 15), and the open questions with your default answer.
- **Placeholders until the client decides:** a placeholder page identity ("@yourpage", a plain avatar), the CTA in one
  config line, real users' names masked, and a list on the review page of what must change before posting (the real
  handle and avatar, fresh numbers on the day, names approved).
- **For the user's downloads:** the footage map plus numbered links with timestamps (footage-sourcing.md section 5).
- **Lead the hand-off** with the link and the file path, then the content in brief, then what was assumed or not
  verified, then what still needs a human (photos, music clearance, the client's approval).

## 5. Manifests: sources, stock, licences, credits
- **SOURCES.md** for borrowed footage, one row per file: URL, author, post date, views, content, where any burned-in
  text sits, duration, size, audio (real or laid-on music), licence.
- **A stock manifest** (JSON or table), one row per clip: the need it fills, file, creator, licence, size, fps, duration,
  best in and out points, what is visible (faces, logos).
- **LICENCES.md** next to every stock or sound folder, with the licence texts themselves kept in the kit folder.
- **CREDITS.md** at delivery: every sound and track with its source and licence. Credit lines for CC photos go on screen
  as the licence asks ("Photo: Name, CC BY 4.0").
- **In Premiere:** every external download, used or spare, sits in one "External B roll" bin with its own label colour,
  so the user can swap shots himself (premiere-ae-editing references/prproj-format.md).

## 6. The asset folder layout and naming
```
<job>/
  sources/
    client/                 the client's own footage, masters, brand files
    stock/                  + manifest, LICENCES.md
    archive (watermarked comps - licence before use)/
    borrowed/               clean cuts + the untouched <name>_src files + SOURCES.md
    photos/  screens/  papers/
  music/                    the plan, the analysis, WAV copies of every track (MP3 decoders differ in delay)
  sfx/                      raw downloads, the baked kit, LICENCES.md
  vo/                       voice files and word timings
  research/                 as section 1
  _build/                   generators, QA scripts and helper tools, with a README of the rebuild order
  final/                    projects, renders, README
```
- **Keep every tool you will need again inside the job folder or the kit,** never only in a session's scratch folder.
  Why: scratch folders get wiped. The YouTube search and storyboard helpers were lost that way once (copies were later
  recovered from a session transcript into the kit library), and a whole client's generators sat for days in a temp
  folder as their only copy.
- Downloads from untrusted places go in their own empty folder and are never run.
- ASCII file names (emoji and special characters broke tools); unique batch names; check a path with `ls` before writing
  a batch file (one was overwritten and had to be rebuilt from the session transcript).
- Delivered files are never overwritten: a change becomes `_v2`, `_v3`. Undelivered drafts move to `_superseded` and old
  versions to `_old_versions`; nothing is deleted.
- Fork an approved pipeline per client with its own brand file, batches and delivery folder; never write into another
  client's folder.
- Name unlicensed placeholders so nobody can mistake them (the comp folder name above, `COMP-WATERMARKED_` file names).

## 7. Research pages and pull lists
- A **pull list** page before anything is downloaded: stock picks per script line, archive with its licence route, what
  needs approval. A **plan page** after a big review or a rejection: proof frames, options, decisions, and nothing new
  built until the user decides.
- A **bank page** of references: filterable, consensus picks first (research-agents.md section 5).
- On review pages, every number shows the data source behind it, and every caption has its posting window.
- Pages are private artifacts: say so, and that the user must share them from the Share menu. Republish from the same
  file path to keep one URL. A page already shared with a client may have been forwarded: say what you will change and
  wait before republishing.

## 8. What never ships
In the kit, a hand-over or a shared folder: media, renders and footage; song files and lyric transcripts; scraped
usernames, wallet addresses and other people's avatars; browser profiles (they hold cookies); scripts that hold signed
download links; model weights; client analytics with money in them; private people's names from footage; cached
Apple emoji art; API keys and tokens of any kind (the boss gets "needs his own X" notes instead).

## 9. Worked examples in the kit
- Past research reports: `~/VisionKit/kit/library/research/`.
- Past hand-overs: `~/VisionKit/kit/library/handoffs/`.
- The pipelines that run research daily: `~/VisionKit/kit/library/pipelines/` (and production-automation).
