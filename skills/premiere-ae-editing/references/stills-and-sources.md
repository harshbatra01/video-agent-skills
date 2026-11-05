# Stills, cutouts, screenshots, stock and licensing

## Photoshop by script (PS 2026, v27)
- Windows, PowerShell: `$ps = New-Object -ComObject Photoshop.Application; $ps.DoJavaScriptFile("C:\x.jsx")` launches PS
  and runs synchronously (returns the last expression). It can also FAIL to launch (CO_E_SERVER_EXEC_FAILURE after
  120 s): have a numpy route ready.
- Mac: `osascript -e 'tell application "Adobe Photoshop 2026" to do javascript file (POSIX file "/abs/x.jsx")'` runs
  synchronously and launches PS if needed (ask the user before launching it). Not yet exercised on the Mac port: test
  on one image first, and keep the numpy route ready.
- Never name a variable `name` in PS JSX (global app.name; the assignment is silently ignored).
- Select Subject = `executeAction(sID("autoCutout"))` (sampleAllLayers false); Select and Mask = `sID("smartBrushWorkspace")`
  (smartBrushRadius, smartBrushUseSmartRadius, refineEdgeOutput = selectionOutputToSelection); layer mask from selection
  = Mk Chnl At Msk Usng RvlS; classic Content-Aware Fill = Fl with Usng FlCn = contentAware (not generative);
  polygon selection `doc.selection.select([[x, y], ...])`. Example: `scripts/stills/ps_cutout.jsx`.
- Cutout edges: `python scripts/stills/decon.py source.png cutout.png out.png` removes the studio background colour baked
  into hair edges. Select and Mask with a smart radius of 4 px gave clean product edges.
- Clean overlays (carousel arrows, sparkles) off a product photo BEFORE Select Subject: a greedy "erase the bright area"
  took 416 px including the product's cap; classic Content-Aware Fill on the overlay first, then cut out.
- Quit Photoshop once no documents are open: a COM-launched Photoshop left running beside After Effects ran the PC out
  of RAM.
- Presenter poses for swaps all come from ONE master image at the same size and framing: a softer, smaller pose with
  different arms and papers made swaps "jump a little". Pose alignment numbers: after-effects.md section 8.
- AI-generated stills: before removing a generator's visible mark (a sparkle) with Content-Aware Fill, check the
  generator's terms, and keep the platform's altered / synthetic content disclosure on (the content is still AI-made).

## Hiding brand names and private details
- Repaint, don't blur, on smooth surfaces: a gradient patch over a brand name on white plastic looked clean, while a
  blur box reads as hiding something. Sample the surface on both sides of the word and fill with a soft-edged
  interpolated gradient (numpy), or use classic Content-Aware Fill (not generative).
- On shop screenshots, blur seller names. Readable number plates, business signs and signage at the frame edge: crop
  them out by Scale / Position (prproj-recipes R7) or skip the take.

## Without Photoshop
- Read a PSD's flattened composite and layer list: `from psd_composite import read_psd` (scripts/stills).
- White-background product shots cut out well in numpy (threshold + flood from the corners + feathered alpha).
- Pillow 12: `ImageDraw.floodfill` silently does nothing on an image made with `Image.fromarray`: call `.copy()` first.

## Screenshots of web pages (sources)
- Headless Chrome: `chrome.exe --headless=new --user-data-dir=<scratch> --window-size=540,1400
  --force-device-scale-factor=2 --screenshot=out.png URL`, same flags on the Mac with this binary:
  `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"`. The separate user-data-dir keeps it away from the
  user's running Chrome and its sign-ins. The same binary prints PDFs (`--print-to-pdf=out.pdf`). Headless Edge hands off to a running Edge and
  writes nothing.
- Paywall dimming can be undone by dividing by the dimmed white level. Some shop pages crash headless Chrome (one did
  with a very tall window: keep a normal height and tile): use the user's screenshot or a typeset quote card of the
  exact text.
- One profile per Chrome instance (`--user-data-dir` per port): two Chromes sharing a profile made the second one fail.
- Pop-ups on React / Next.js sites: hide them with CSS, never by deleting nodes (deleting them crashed the site's app).
  Click the dialog's close button and press Escape, then inject a style rule that hides `[role=dialog],
  [role=presentation][data-open], [data-radix-portal], [data-overlay], [vaul-drawer], [data-vaul-overlay]` and restores
  scrolling. While filming a page, re-apply it every 15 frames, null-safe (`document.head || document.documentElement`),
  and run a 4 s test before any timed window (a sign-in modal and a 12 px blur layer came back once).
- Find quotes and studies online when the script cites them; quote them word for word; keep the source and date.

## Cards and overlays from HTML templates (headless Chrome)
- A transparent PNG overlay or card: `chrome --headless=new --disable-gpu --hide-scrollbars
  --force-device-scale-factor=1 --window-size=W,H --default-background-color=00000000 --virtual-time-budget=6000
  --user-data-dir=<own profile> --screenshot=out.png file:///page.html`. 12 test posts took 51 s, a day's 8 about a
  minute.
- Fonts: inject them as `@font-face` file URLs, call `document.fonts.load('40px Family')` for every family, and fit text
  only after `document.fonts.ready`; a fit loop that shrinks the size 2 px at a time until nothing overflows. Skip
  italic files when searching font folders by name (an italic fallback got picked once); variable fonts take weights
  100-900. On a Mac, Helvetica ships as a .ttc that Chrome may not load through @font-face (install .ttf files or swap
  the font), and Adobe Fonts give no file path at all.
- Build `file://` URLs with a tested helper: `'file:///' + '/Users/...'` doubles the slash on a Mac.
- Frame-by-frame video from HTML (Chrome driven over the DevTools protocol, screenshots piped into ffmpeg) and the
  template systems built on it: production-automation (`render-pipeline.md`, `faceless-studio.md`).

## Stock and archive
- Free stock: Pexels, Mixkit, Pixabay (no attribution needed). Pexels clip pages are behind a Cloudflare human check:
  never click it; older ids resolve at `videos.pexels.com/video-files/{id}/{id}-{hd|uhd}_{w}_{h}_{fps}fps.mp4`
  (HEAD-probe first). Searching Pexels through its search pages' JSON, the Mixkit 720p backup and which sites block
  curl: media-toolkit.md section 3. Keep a manifest (file, source URL, licence, where used).
- Brief rules seen: no strangers' faces in a celebrity ad (objects and hands fine); no free stock exists of people
  wearing niche gadgets (say so and offer a shoot or brand press B-roll).
- Archive of famous people (Getty, BBC Motion Gallery, event organisers) is EDITORIAL only: commercial use needs the
  rights holder (for an athlete, ask their team first). Download from YouTube only when the user asks
  (youtube-downloads.md; one moment of a long video: media-toolkit.md section 2), and say when footage is not cleared
  for the client's use; reading a video's info, captions and scrub storyboard is fine.
- Wikimedia Commons photos: check the licence, credit "Photo: Name, CC BY 4.0", mark edits "(edited)". The Commons API
  finds current photos of public figures; take the largest standard sizes (portraits 1920x2880, landscapes 3840x2560),
  because full-size originals were rate-limited. CC BY-SA 4.0 needs "Photo: Name, CC BY-SA 4.0, via Wikimedia Commons"
  and an edited version stays under the same licence; CC0 needs nothing. News-agency and broadcaster photos are
  placeholders only. Rights in full: research-and-sourcing `licensing-and-rights.md`.

## Platform policy flags worth raising (once, briefly)
- YouTube monetization: an AI persona presenting as a human health expert ("AI doctor") cannot monetize; tick the
  altered / synthetic content box for AI presenters.
- Ads: claims linking a product to a celebrity's results draw regulator attention (UK ASA). The user may park
  compliance: then do not keep raising it, but only use headlines that really ran, word for word.
- Showing a platform's UI (Instagram) in ads needs permission: design your own card instead.
