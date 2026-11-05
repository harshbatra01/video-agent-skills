# HyperFrames motion-graphics layer (added 19 Oct 2026)

The user installed HyperFrames and wants its motion graphics on top of the reference-style edit, not replacing it.
Pattern that works: keep the Python/ffmpeg edit as the base, build ONE transparent HyperFrames overlay composition timed to
the edit plan, render it with alpha, composite with ffmpeg.

## Setup on this Mac
- HyperFrames needs Node 22 or newer. The shell defaults to nvm Node 20; prefix commands with
  `export PATH=~/.nvm/versions/node/v24.21.0/bin:$PATH`. Do not change the user's shell config.
- Route: `/hyperframes` -> `general-video` (an 81 s overlay layer for an existing edit; `motion-graphics` is for single
  units under 10 s). `npx hyperframes skills update general-video` installs the workflow skill (outside the Skill tool).
- `npx hyperframes usage --json` returned `unknown` (unsupported auth): say so, do not guess.
- `hyperframes add <block>` copies each snippet to the clipboard (side effect, mention it).

## Build
1. `npx hyperframes init <dir> --non-interactive --example=blank --skill=general-video`, then BRIEF.md (workflow,
   flow automation, storyboard no, message, aspect 1080x1920) with the palette and fonts in Notes.
2. Search before hand-building: `npx hyperframes catalog --query "<look>" --json` (results under `results`).
   Useful for mini-docs: `lower-third-bild` (news chyron, red and white, Barlow Condensed), `lt-kicker-name` (location
   tag), `news-ticker`, `us-map-flow` (city arcs; needs local topology), `hw-arrow` and `hw-callout-circle` (hand marks,
   Caveat), `marker-highlight`, `count-up`, `strikethrough-replace`, `caption-glitch-rgb`, `chromatic-radial-split`.
3. Registry blocks are 1920x1080: borrow their CSS and fonts into one portrait `index.html` (root 1080x1920,
   transparent background, `data-duration` = the edit's length). One paused GSAP timeline at absolute seconds taken from
   the edit plan JSON. Draw-on strokes with `strokeDashoffset`; wobble paths from a seeded hash (no `Math.random`).
4. Map data: save `us-atlas@3/states-10m.json` locally and load it as a script variable; the stock `us-map-flow`
   fetches it at render time.
5. `npx hyperframes check` (lint, layout, motion, contrast). Mark scrolling text `data-layout-allow-overflow`.
   Snapshots: `npx hyperframes snapshot --at t1,t2,...` render the overlay alone; composite them over frames of the base
   edit to judge placement.
6. Open `npx hyperframes preview --background` (Studio) before rendering; mention the HyperFrames desktop app (Framey).
7. Render alpha: `npx hyperframes render --format webm -o overlay.webm` (one heavy job at a time: wait for the base render).
8. Composite: `ffmpeg -i base.mp4 -c:v libvpx-vp9 -i overlay.webm -filter_complex "[0:v][1:v]overlay=format=auto" ...`
   (force the libvpx-vp9 decoder so the alpha channel is read), copy the base audio.

## What the layer adds (minidoc-01 v9)
- News chyrons naming people on screen (the reference does this with real broadcast chyrons): ELON MUSK, LARRY FINK.
- Location tags (COURT OF CHANCERY / WILMINGTON, DELAWARE; GIGAFACTORY TEXAS / AUSTIN).
- Hand-drawn circles, arrows and notes that point at the one shareholder, the nine shares, the 3%.
- A route map (Delaware to Texas arc with a travelling dot) where v8 had a static text card.
- An underline on $30B+, and a broadcast ticker on the news peg.
- Keep overlays out of the caption band (mid-frame); the map panel hides captions for 2 s, which reads as a planned break.
