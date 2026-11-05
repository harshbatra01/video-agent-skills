# The page

The outline gets published as a self-contained HTML page so the client can open a link instead of a markdown file.
Load the artifact-design skill first (our environment expects it before any page), write the HTML to a real file in
the job folder, then publish it with the Artifact tool. Pages start private; the user decides who gets the link.

**Write to a stable path and reuse it.** Republishing the same file path keeps the same URL, so the client's link
survives every revision. A new path mints a new URL and orphans the one they already have.

**Confirm before revising a published page.** The client may have the link open or may already have forwarded it. Say
what you are about to change, then wait.

## Design system

The page is a production document, not a pitch deck. It should look like something made by someone who takes the
episode seriously.

Two palettes, picked by the episode's register:

**Somber** (grief, loss, memorial): warm dark, candle-lit:
```css
--bg:#14161C; --surface:#1B1E26; --ink:#ECEAE3; --ink-soft:#A8A69E;
--accent:#CDA255;        /* candle amber */
--cool:#7C8798;          /* slate, for the host and structural chrome */
--line:#2A2E38;
```

**Warm** (music, celebration, comeback stories): parchment and brass:
```css
--bg:#F0EBE1; --surface:#FBF8F1; --ink:#241D14; --ink-soft:#5C5142;
--brass:#9A6F1E; --brick:#B24A3C; --line:#E0D6C4;
```

Support both light and dark through `prefers-color-scheme` plus `:root[data-theme="dark"]` / `[data-theme="light"]`
overrides, because the viewer's theme toggle stamps `data-theme` on the root and it has to win.

Type (Mac faces first, Windows fallbacks after them):
```css
--f-display:'Hoefler Text','Iowan Old Style',Palatino,'Palatino Linotype',Georgia,serif;
--f-body:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;
--f-mono:'SF Mono',ui-monospace,Menlo,Consolas,'Roboto Mono',monospace;   /* timecodes */
```

A soft radial glow behind the title carries the candle metaphor on somber episodes. Keep it subtle enough to read as
lighting rather than decoration.

## Speaker styling

This is the detail that makes the page scannable. The three voices look different, so the eye can tell who is speaking
without reading the label:

```css
.line       { font-family:var(--f-display); font-size:1.24rem; }   /* guest: hero serif */
.line.host  { font-family:var(--f-body); font-size:1rem; color:var(--ink-soft);
              padding-left:.9rem; border-left:2px solid var(--line); }  /* host: quiet aside */
.line.quoted{ font-style:italic; }        /* a third party quoted by the guest */
```

The guest gets the largest, most typographically serious treatment because those are the lines the trailer is built
on. The host recedes. Anyone the guest is quoting is italic, so a daughter's remembered words read as hers and not as
narration.

## Section order

Match the markdown outline so the two documents can be read side by side. Lean format (client feedback, July 2026): the
beats ARE the cut list, so there is no separate table, no legend section, no emotional-shape chart and no editing-note
section.

1. Header: title, framework line, meta chips (runtime, scene count, episode length)
2. The episode summary + tone, glossed for a reader outside the show's world
3. **The episode map**: the whole conversation in big chunks, one line each: timecode, plain-English chunk name, the
   host question that opens it
4. The arc
5. **The cut**: the scene script. Scene blocks (speaker header + timecode range in mono, quotes as stacked lines,
   search phrases as chips) with VO blocks between them (visually distinct: a narration treatment, not a speaker card)
   and full-line production directions in small caps. The title-card VO block also shows the card text that carries the
   names.
6. **VO, tagged for ElevenLabs**: one code block per segment, in script order
7. **Music and pacing**
8. **Swaps and alternates**
9. **What we would need**: the asks
10. Footer: verbatim confirmation, name spellings, anything deliberately left out and why, "trailer only"

## Constraints

- Fully self-contained, so the client can save it and it still works: inline the CSS, embed any image as a `data:`
  URI, no external fonts or scripts.
- Any wide content scrolls inside its own `overflow-x:auto` container. The page body must never scroll sideways.
- No em dashes in any visible copy, including headings and cue notes.
- Set a stable `<title>` and keep the same icon across redeploys. A changed icon reads as a different page to someone
  hunting through browser tabs.
