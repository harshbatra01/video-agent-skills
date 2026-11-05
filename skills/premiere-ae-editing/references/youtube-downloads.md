# Downloading YouTube sources (set up and tested on the Windows PC, 11 Oct 2026)

Only download when the user asks for it (they do for their client channels' own videos).

## Read this first: rights and terms
- This route works around YouTube's bot check: it generates a "PO token" so YouTube serves HD streams to a script.
  That may break YouTube's terms of service, even for a client's own uploads. Use it only for footage the user or the
  client has the rights to use (their own videos, footage they licensed), only when the user asks, one download at a
  time. Whether the kit keeps this route is the boss's call. `ytdl.py` carries the same note at the top of the file
  ("READ FIRST").
- No sign-in and no cookies: private and paid videos stay out of reach, and no other workaround was added. Never add a
  login or browser cookies to get past a block.
- The plain yt-dlp fallback (a different player client plus format fallbacks, media-toolkit.md section 1) is the same
  kind of workaround and carries the same note.
- The cleaner route: ask the client for the masters, which are also better quality than YouTube's re-encodes.
- Looking before downloading needs no workaround and is the default: a video's page, captions, "most replayed" heatmap
  and scrub storyboard (timing.md for the heatmap; storyboard contact sheets: research-and-sourcing
  `references/footage-sourcing.md` section 4).

## On a Mac (not run there yet, 14 Oct 2026)
- Works as shipped: the folders resolve (the token server in `~/bgutil-ytdlp-pot-provider/server`, the lock file in
  the user's temp folder through `tempfile`, which is `$TMPDIR` on a Mac), the lock's "is that process still alive"
  check uses `os.kill(pid, 0)` off Windows, and `--help` or no video prints the note and usage without starting
  anything.
- Still Windows-only: `ensure_server()` starts the token server with Windows process flags, so when the server is not
  already running Python stops with "creationflags is only supported on Windows platforms". Until that is ported, start
  the server by hand first (the `deno run` line below, run from `server/node_modules`, and stop it afterwards); then
  `ytdl.py` only pings it. The port is one call (`start_new_session=True` instead of `creationflags` off Windows) and is
  step 16 of the boss's first-run task list (`MAC-TASKS.md`).
- Setup on a Mac (ask first, each install): `brew install deno`; yt-dlp and the provider plugin in the tools venv
  (`~/.venvs/premiere-ae/bin/pip install -U "yt-dlp[default]" bgutil-ytdlp-pot-provider`), because `ytdl.py` runs
  yt-dlp as `python -m yt_dlp` from its own Python; the server cloned to `~/bgutil-ytdlp-pot-provider` at the
  provider's version (below).
- Without the token server: plain yt-dlp with the format line and fallbacks in media-toolkit.md section 1 (the same
  kind of workaround, the same rights note). The one-download-at-a-time rule holds everywhere.

## One command
`python scripts/media/ytdl.py URL_OR_ID [...] --out DIR [--max 1080] [--meta-only]`
1080p H.264 + AAC merged to mp4 (Premiere-friendly), named `<title>_<height>p.mp4`, `download-archive.txt` in DIR
skips repeats. About 1 minute per 10-15 minute video. No video given, `--help` or `-h`: it prints the note and usage
and exits 1 before anything starts (an older copy started the token server even for `--help`).
- 720p is the floor and there is no single-file fallback: on 12 Oct a response without the adaptive formats quietly
  gave a 360p file through a `/b` fallback, so now a client that cannot give 720p or better fails and the next client
  is tried.
- The size filter is on HEIGHT: a vertical 1080x1920 video fails at `--max 1080` (five vertical references failed this
  way through a similar filter). Pass `--max 1920` for vertical sources. In your own yt-dlp lines, filter on the
  shorter side instead (yt-dlp's `-S res:1080` sorts by the smaller dimension; not tested here).

## Why it is needed
YouTube serves HD streams only to clients that present a "PO token" (proof of origin). Without it, on this PC:
`web` and `android_vr` say "Sign in to confirm you're not a bot" (worse after many quick requests), `mweb` gives
only 360p (format 18), `web_safari` only storyboards, `tv` "page needs to be reloaded".

## The setup (no Google account, no cookies)
- yt-dlp from pip with `yt-dlp[default]` (includes yt-dlp-ejs) + Deno on PATH (winget DenoLand.Deno; Homebrew `deno` on
  a Mac) for the JS challenges. Versions that worked together on 11-14 Oct 2026: yt-dlp 2026.08.19, Deno 2.9.7, provider 2.0.2. When pip
  leaves no `yt-dlp.exe` on PATH, run it as `python -m yt_dlp` (ytdl.py does).
- Plugin: `pip install bgutil-ytdlp-pot-provider==<ver>` (maintained by a yt-dlp maintainer, listed in the yt-dlp
  PO Token Guide).
- Token server, same version, in `%USERPROFILE%\bgutil-ytdlp-pot-provider` (`~/bgutil-ytdlp-pot-provider` on a Mac):
  `git clone --branch <ver> ...`, then in `server`: `deno install --allow-scripts=npm:canvas --frozen`; run from
  `server\node_modules` (`server/node_modules` on a Mac):
  `deno run --allow-env --allow-net --allow-ffi=. --allow-read=. ..\src\main.ts` (127.0.0.1:4416, check `/ping`).
  ytdl.py starts it detached when `/ping` fails (on Windows only, see "On a Mac").
- Client: `--extractor-args "youtube:player_client=mweb"` (mweb + GVS token is the guide's recommendation); 1080p60
  formats 299 (H.264), 303 (VP9), 399 (AV1) appear once the token works. ytdl.py falls back to `web_safari`, then `tv`.
- Other tools that call yt-dlp directly (a pipeline's own fetch helper) get none of this unless they start the token
  server and set the `mweb` client themselves: expect lower formats and earlier blocks from them.

## When it breaks
- Update both together: `pip install -U "yt-dlp[default]" bgutil-ytdlp-pot-provider`, then `git fetch --tags`,
  checkout the matching tag and re-run `deno install` in the server folder.
- `yt-dlp -v` must show "Generating a gvs PO Token ... via bgutil HTTP server"; if not, try another client.
- Be gentle: one video at a time, `--sleep-requests 1`. About 80 quick metadata lookups in a row triggered the
  bot check for the default client; about 15 parallel calls from another tool got a 15-minute block; about 40 study
  downloads in a row blocked 4K re-downloads until the next day.
- A whole machine can get flagged: on 13 Oct one PC was blocked on every route (PO token, the embed player with Error
  153, a headless player) for the day. Then stop; ask the user for the files, or ask early for a throwaway account's
  cookies (never a personal account, never the user's browser cookies).
- Plan B: the user downloads with their own tool into an inbox folder, or the client shares masters (better quality
  than YouTube anyway).
- yt-dlp lives in the user site-packages on this PC, so `python -I -m yt_dlp` fails with "No module named yt_dlp"; run it
  without `-I` (ytdl.py does) or add that site-packages path in a wrapper. Metadata only: `--skip-download -j`;
  YouTube's "most replayed" heatmap comes back in the same JSON (13 Oct 2026).

## One download at a time, across every session (13 Oct 2026)
Two YouTube downloads at once from this PC get blocked: 403 Forbidden, "Requested format is not available", or a
download that sits at 0 bytes forever. With several Claude sessions working at once this happens by accident, so
ytdl.py now takes turns through a lock file (`ytdl_one_at_a_time.lock` in `%TEMP%`, or the system temp folder such as
`$TMPDIR` on a Mac; stale after 20 min or when its process is gone) and gives up on a client after 20 min. Never start downloads in parallel; queue them, and start the next job's
prep while the next download waits.
