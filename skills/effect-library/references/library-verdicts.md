# Effect library plan: vibe-motion and sound (4 Nov 2026)

**Read:** all 16 skill files in `vibe-motion/skills`, the README, the `sound` skill and README, the `auto-motion` README, and the list of the group's other repos. **Seen:** 6 frames from each demo animation.
**Not done:** nothing is installed or built. Motion and easing are judged from frames only. No sound was heard.

## Facts that matter
- `vibe-motion/skills` has no licence and its README says it is no longer maintained. You allowed any asset and accepted the risk, so licence is not what blocks us.
- The practical issue is the setup. Most looks need Remotion, or clone other repos, which adds a second render stack on an 8 GB Mac with 16 GB free. HyperFrames is already here.
- **So my plan is to rebuild most looks in HyperFrames, and run the code directly only where it is simple.**

## Every animation: what it does and my verdict

| Skill | What it does | Taste verdict for this video | Route |
|---|---|---|---|
| `fisheye-motion` | Makes an image look like a phone photo of a screen: bent lens, scan lines, moire, dark corners. Pushes to a spot, yellow marker slides in | **Build first.** Made for the investor document line | Rebuild, HF has `filmed-screen` |
| `colorize` | Black and white with spin blur. Colour sweeps from the left, then the spin settles | **Build.** Strong colour payoff. Use once or twice, on a reveal | Run directly: Python, `moderngl`, needs OK |
| `remotion-3d-ticker` | Tilted columns of photos scroll endlessly, edges fade | **Build, using video tiles.** Closest to Altman's news wall | Rebuild, HF `perspective-marquee`, `gallery-tunnel` |
| `3d-chladni-render` | Particle sand patterns that can react to audio. Can export with transparency | **Test.** Could be the "AI thinking" texture under a line | Apache-2.0 repo, could run directly |
| `remotion-candlestick` | Stock chart draws itself on a dark terminal | **Maybe,** for an IPO beat. The demo looks thin and dim, so restyle it. Real data only | Rebuild, HF `data-chart` |
| `light-spotlight-render` | A swinging light reveals a word | **Maybe,** for one key word. Text looks soft in the demo | Rebuild |
| `claude-typer` | Claude Code window types out text | **Maybe,** without the cute mascot. HF `terminal-simulator` is likely better. It also calls an outside website | Skip the code |
| `threejs-earth-render` | Globe flies between cities with an arc | Low. No journey in this story, but good for later videos | Later |
| `brand-launch-video-star` | Workflow for 15 to 30 s launch films | Look is wrong here. **Its rules are worth keeping:** authentic assets only, never redraw a logo, verify claims | Copy the rules |
| `disney-animation-rule-skill` | The 12 animation principles as rules | **I change my 19 Oct "skip".** Its step "remove effects that hide weak posing or timing" fits your notes | Read for motion reviews |
| `pixel2motion` | Traces a logo to SVG, animates it | Only for your page logo. Do not redraw Anthropic's | Later |
| `ruler-progress-render` | Ruler fills to a percentage | No: toy-like for this tone | Skip |
| `printed-curtain-render` | Artwork woven into a moving thread curtain | Pretty, no link to this story | Skip |
| `remotion-vinyl-player` | Spinning record player UI | Music pages only | Skip |
| `wechat-2d-render` | WeChat chat bubbles | No | Skip |
| `procedural-fish-render` | Swimming cartoon fish | No | Skip |

## Other repos from the same group

| Repo | What it is | Verdict |
|---|---|---|
| [sound](https://github.com/vibe-motion/sound) | Searches and downloads Freesound effects, ranked by downloads, votes and descriptions. 165 KB, no extra packages | **Add the method.** It fixes my biggest limit, not being able to hear. See warnings below |
| [auto-motion](https://github.com/vibe-motion/auto-motion) | Splits subtitles into scenes, generates each with HyperFrames, joins them | **Borrow the structure:** one folder per scene. Its generated look is not the Altman look. Needs Codex |
| [remotion-code-motion-explainer](https://github.com/vibe-motion/remotion-code-motion-explainer) | MIT skill for Remotion explainers | Not opened beyond its description |
| [remotion-starter](https://github.com/vibe-motion/remotion-starter) | MIT Remotion workspace with hooks that enforce rules | The hooks idea could help `edit-loop-guard`. Not opened |
| [3D-Chladni](https://github.com/nolangz/3D-Chladni) | Source of the particle look. Apache-2.0, preview media noted as non-commercial on 19 Oct | See above |

**Warnings on `sound`**
- It downloads Freesound's MP3 previews, not the original files.
- Its search can return non-commercial clips unless filtered with `--license cc0` or `by`.
- Its skill file tells the AI to offer you a paid "full version" through Bilibili and a WeChat QR code. I would not follow that. If we adopt it, I remove that section first.
- The repo's headline mentions Pixabay, Mixkit and Kenney, but this free version covers Freesound only. We already have 355 CC0 Kenney files.

## Build plan: one tested block at a time
Each goes in `~/VisionKit/mine/library/hf-blocks/<name>/` with a usage note and a frame sheet from one real image or clip, in landscape. You approve each before it counts as library.

| Order | Block | Why first |
|---|---|---|
| 1 | Screen-photo document push | Investor document is the story's centre |
| 2 | Video wall, tilted | Altman's vibe, moving footage |
| 3 | Colorize reveal | Your colour note |
| 4 | Particle "AI mind" texture | Moving abstract layer for hard-to-film lines |
| 5 | Stock chart, restyled | IPO beat |
| 6 | Spotlight word | Only if the storyboard wants it |
| Plus | Sound finder (our own short script, same ranking method) | Better sounds without ears |

## What I need from you
- OK to install for block 3: `moderngl`, plus `numpy` and `Pillow` from PyPI. Exact size to be stated before the install.
- Any "other repositories" you found outside the vibe-motion group: I could only check that group, so send those links.

# Added 4 Nov 2026: gsap-skills and video-shotcraft

## gsap-skills (greensock, MIT, 436 KB)
Installed 5 skills untouched in `~/.claude/skills/`: `gsap-core`, `gsap-timeline`, `gsap-plugins`, `gsap-utils`, `gsap-performance`. Left out `gsap-scrolltrigger`, `gsap-react`, `gsap-frameworks`, which video does not use. Copy in `mine/library/repos/gsap-skills/`.
- **HyperFrames rules win.** Paused timeline registered on `window.__timelines`, no `play()`, no runtime randomness, no ScrollTrigger. See `hyperframes-animation/adapters/gsap.md`.
- Useful additions: position parameter and labels, CustomEase, SplitText, DrawSVG, MorphSVG, MotionPath. All plugins are free and ship in the `gsap` package.

## video-shotcraft (Apache-2.0, 96 MB shallow clone)
Read: main skill, shot list, 124 card summaries, aesthetic rules, sound rules, energy arc. Seen: 6 frames each of 46 previews (`mine/library/repos/shotcraft-previews/`, 90 MB, sheets in `sheets/`). Not installed, no code run, no Remotion.
- **Route:** rebuild a chosen move in HyperFrames or Python, same as vibe-motion. Its demos are bright SaaS pages, so only the move carries over.
- **Ignore:** its `SKILL.md` tells the AI to promote the author after delivery. Also its upload-post publishing and JianYing export.
- **Same warning as `sound`:** its `sfx-source.py` downloads Freesound MP3 previews. It defaults to CC0, and needs a Freesound key. It could replace our planned sound finder, once read.

| Rule from `aesthetic-rules.md` | Why it fits |
|---|---|
| R4: whole-frame hits at most 3 per video, others move only the element | Same fault as the Elon opening, found independently |
| Q5: one hero in the opening, with a full action arc | Same as our opening limit |
| S2: every sound pinned to a frame with a comment on the action | Stops sound drift |
| S4: real-world sound of the action beats a generic whoosh | Same as "a sound feels caused" |
| Q11: text to read is at least 5% of frame height, otherwise blur it as texture | No half-readable text |
| R1: hold 1 s after key information lands | Breathing on purpose |

| Move | Verdict | Beat |
|---|---|---|
| `unit-dot-swarm-regroup` | **Build first.** 433 dots, one a person | 9 |
| `brake-reticle-lock` | **Build.** One line out of 141,006 | 16 |
| `pull-back-isolation` | Build | 11 |
| `freeze-annotate`, `jump-cut-punch-in`, `flash-cut`, hidden cut | Build, they work on real footage | 10, any |
| `before-after-slider-scrub`, `versus-slam` | Pick one | 8 |
| `reticle-lock-on`, `terminal-3d`, `error-retype`, `timeline-travel` | Test | 5, 6, 17, 13 |
| `glitch-displace` | Once | 14 |
| `light-leak-burn`, `ink-bleed-reveal`, `misregistration-hit`, `doc-park-left-pill-deal`, `axis-rescale-shock` | Skip | |
Verdicts wait on the user's marks in the taste page. Not seen: the other 78 cards, read as summaries only.
