# Cracked Edits Bank (13 Oct 2026)

Page (private, filterable, with "Want this" marks and "Your finds"): https://claude.ai/artifact/SumRpyqLV6Fr5rNxEgVyj6
Local copy of the page: `cracked-edits-bank.html`.

## What is here
| File | What it holds |
|---|---|
| `00-our-mbappe-breakdown.md` | Our GASS x Mbappe edit read frame by frame: second-by-second table, effect inventory from the .prproj, version history, numbers, gaps; plus our other 4 edits |
| `our-edits\sheets\` | every-frame sheets of v1, the changed window of v4 / v5 / FINAL_1 / final, key-frame crops, other edits overview |
| `research\_brief.md` | the brief every research agent followed, including the technique tag list |
| `research\01-football.md` | 41 football edits, creators, tutorials, patterns |
| `research\02-basketball-us-sports.md` | 40 NBA / NFL / US sports edits |
| `research\03-combat-f1-other.md` | 55 fight, F1, cricket and other edits, tiered A to D |
| `research\04-amv-edit-community.md` | 55 anime / After Effects / CapCut edit-scene pieces, contests, collabs, the artist-commissions-edits model |
| `research\05-captions-typography.md` | 47 type-led pieces, the 10 most-used font styles |
| `research\06-effects-catalogue.md` | 73 techniques with looks, examples (44 frame-checked), trend status and music-sync rule |
| `research\07-roto-compositing.md` | 37 roto / text-behind / compositing pieces, roto tools |
| `research\08-sync-structure-virality.md` | replay maps of 69 YouTube edits, lengths, sync tolerance, song trends, how labels use edits |
| `research\09-tools-packs-sources.md` | 59 plugins, packs, scenepack sources and AI tools, with prices and free alternatives |
| `research\10-past-artifacts.md` | notes from the earlier Drill Edit Handbook and Hoops and Hurt pages |
| `page-src\` | page template, data and the builder (`build_page.py`) to rebuild the page after adding research |

## The short version
- Our 1-frame strobes are already as dense as anything the researchers could verify. What beats us: one clear concept per
  edit, designed typography (giant name or number behind the player, one lyric word per beat), compositing (cutouts,
  3D words, card scenes), a hook in the first second and a payoff 55-70% in, speed ramps, and a loop or live song-card ending.
- 273 edits in the bank; 29 were found independently by two or more researchers (top of the default sort).
- Most used technique across the bank: kinetic type (98 edits), then colour grade, glow, beat cuts, lyric text. We
  have no kinetic or lyric type yet.
- Limits: TikTok does not open from India, so TikTok entries are leads from search results; Instagram was only partly
  readable; the shared web-search budget ran out mid-run. Each card on the page says whether frames were seen.

## Rebuild the page after adding research
`python page-src\build_page.py research page-src\template.html page-src\ouredit.json page-src\our_summary.json page-src\aims.json cracked-edits-bank.html`
then publish it to the same artifact URL.
