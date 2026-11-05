# Format catalog (7 Oct 2026)

Seen directly on the best pages' latest 12 Instagram posts (RapTV @rap, Say Cheese, GRM Daily, Mixtape Madness, Link Up TV) plus X text patterns from 01 and the UK raw reports. Feed posts are 1080x1350 (4:5); videos 1080x1920.

## Photo / card formats
| ID | Format | Who | Layout | Best for |
|---|---|---|---|---|
| F1 | **UK headline card** | GRM, Mixtape Madness, Link Up | Full-bleed cinematic photo, dark gradient at the bottom, bold condensed UPPERCASE white headline (2 to 4 lines) in the bottom third, song titles in quotes, small page logo bottom centre. Options: 1 to 3 key words in an accent colour (Link Up: yellow/green), series label (Originals, THROWBACK, HAPPY BIRTHDAY), circle cut-out of a second person top-left, flag sticker | Almost every story: releases, news, quotes, anniversaries, birthdays. UK house style |
| F2 | **RapTV card** | @rap | Photo top ~65%, big condensed headline block below (white, key words orange), logo bottom-left, date or series badge top-left ("AUG/26", "POWER RANKINGS") | Same stories, louder; series posts |
| F3 | **Meme header** | Say Cheese | White band on top with a bold black Impact-style headline plus emoji, media below; circular face cut-outs with red outlines for court/beef; mugshot photos | Beef, court, drama, viral moments |
| F4 | **Own tweet card** | Daily Loud, Say Cheese, @rap X, Link Up | The page's own tweet-style card (avatar, name, tick, text) over a photo or above a clip. Use our own brand only: Instagram demotes screenshots of other accounts with usernames (30 Apr 2026 rule) | Statements, quotes, fast news |
| F5 | **Data card** | Chart Data, Official Charts | Cover art + fill-in line: position, movement, weeks, streams/units | Chart days (Fri chart, Sun/Mon/Tue midweeks), streaming milestones |
| F6 | **Calendar card** | DailyRapFacts, GRM, MM, Kurrco, Pop Crave | "N YEARS AGO TODAY X DROPPED 'Y'", "HAPPY BIRTHDAY X", "NEW MUSIC TONIGHT" list | Built a day ahead from a calendar |
| F7 | Carousel explainer | RapTV, XXL | Multi-slide (flowers, power rankings) | Later |

## Video formats (9:16)
| ID | Format | Who | Layout |
|---|---|---|---|
| V1 | **Split news (our current)** | @rap TikTok, RAP.prproj | Two artist photos top, white rounded caption box with black uppercase headline + emoji, music video clip in the lower two thirds, 20 to 30 s, song as audio |
| V2 | **Header over clip** | Say Cheese, Daily Loud reels | White band with black headline on top, clip below, caption ends with a question |
| V3 | **Headline over clip** | GRM, MM, Link Up reels | Full-bleed clip, bold condensed caption in the lower third, logo, series label |
| V4 | **Tweet card over clip** | Link Up, Daily Loud | Own tweet card mid-screen over the clip |
| V5 | **Clip + quote** | HotNewHipHop TikTok | Clip led by its best line as on-screen text |
| V6 | Performance clip with sticker captions | Mixtape Madness | "WAIT FOR THE FLOW SWITCH" style stickers on freestyle clips |

## Headline grammar (captions and on-image text)
- Kurrco: "ARTIST & ARTIST - Title", "TITLE OUT NOW 🚨", "N years ago today, X released 'Y' 💿 Favourite track?", "via TikTok 🤳".
- RapTV: lines end "‼️"; caption sign-off "Y'all rockin' with ...⁉️".
- GBMC: one sentence, one CAPS keyword, one emoji, "EXCLUSIVE:", asterisk censoring.
- MM: "🚨Out Now🚨", "🗓️: X dropped N years ago 🔥".
- Daily Loud: always end with a question. Pop Crave: neutral and sourced for stats.

## Build route (proposal)
- Cards F1 to F6: HTML/CSS templates rendered to PNG by headless Chrome (exact fonts, auto text fitting, fully unattended), or Photoshop templates when hand polish is wanted.
- Videos V1 to V5: Premiere template project per format, filled by script (prproj_lib; needs a text setter), or After Effects templates rendered unattended. Client song as the audio; TikTok and IG photo posts can carry the sound too.

## Suggested build order
1. F1 UK headline card (covers most stories). 2. V1 split news + V3 headline over clip. 3. F6 calendar cards (made a day ahead). 4. F3 / V2 meme header for beef and court. 5. F5 data cards for chart slots.

## Pipeline notes from this pass
- Instagram rate-limits fast (HTTP 429 after ~20 quick profile lookups): read IG slowly, never in bursts, to protect the monitoring account.
- UK IG news accounts found by search, not yet sized (check slowly): uk_rap_news_, uk.rap.news, uk_rap_official, drillonlytv, uk.drill.news, _ukdrillnews, ukrapnumbers, ukrappers.quotes, realbarzuk, urbannmusicuk, uk_musicnews.
- Tools installed 7 Oct: ffmpeg 9.0.2, Deno 2.9.7, gallery-dl 1.32.15, yt-dlp 2026.08.19 (run as "python -m yt_dlp").
