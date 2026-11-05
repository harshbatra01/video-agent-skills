# Researching what performs

How to find reference posts and edits, rank them fairly, and read a client's own numbers. This file owns the research
method. What the findings say about formats, hooks and posting lives in social-video-formats; how to study one
reference edit's craft (cuts, captions, motion, sound stems) lives in editing-playbook.

## Contents
1. Research by frames, not thumbnails or captions
2. Ranking reference posts fairly
3. Discounting bought reach
4. Building and reading benchmarks
5. Measuring our own output against the references
6. Coding posts by attribute and comparing medians
7. Auditing a person's or a brand's channels
8. A client's own page data
9. Choosing the time window
10. Scoping a study, and where verdicts come in

## 1. Research by frames, not thumbnails or captions
- Two rounds of research built from stats and thumbnails produced formats the user rejected ("I don't think you
  researched enough"); the third round looked at about 350 to 400 real posts as frames, and the user then said "based on
  research do the best formats cook them up".
- Method:
  - Download the real viral posts (media only, never executed; the user's OK first).
  - Make a timestamped contact sheet per post: 20 frames, dense in the first 3 s.
  - Make a Whisper transcript per post.
  - Rank by views divided by the page's followers.
  - Flag paid and co-authored posts.
- Remember the bias: a sample picked for hits shows what is possible, not what is typical.
- Cost: 58 to 83 minutes, 185 to 313 tool calls and 590K to 660K tokens per agent; about 3M tokens for a round of 5
  agents. Plan it as a real job.
- For one page's format study: read its last 12 posts in the logged-in browser, make one small contact sheet per page,
  zoom only for details, and read Instagram slowly (news-and-story-research.md section 4).

## 2. Ranking reference posts fairly
- **Reach potential:** views divided by followers. **A breakout on its own page:** views divided by the page's median
  views. **Engagement:** likes, shares, quotes and saves per view.
- Use medians, not averages: one viral outlier skews an average.
- Decide the metric from the goal before ranking: shares, saves, quotes and replies each come from different shapes of
  post (the findings: social-video-formats).
- Sources of exact counts without a login: news-and-story-research.md section 4.

## 3. Discounting bought reach
- Big brand numbers are often promoted or co-authored. One brand's 23.5M-view clip had 0.17 likes per 100 views;
  organic hits run at about 5 to 12 likes per 100 views, and boosted ones can fall under 0.2.
- Mark posts at about 0.1% likes per view or lower as "likely promoted", and rank them on likes, shares, quotes and saves
  instead of views.
- Co-authored (collab) posts borrow another account's reach, so their ratios mean little.

## 4. Building and reading benchmarks
- Say how the sample was picked. Example: 75 YouTube edits with 150K+ views had a median length of 39 s (middle half 27
  to 56 s), a median like rate of 2.8% (top 10% above 4.2%) and a median of 0.49 comments per 1,000 views.
- Niche benchmarks from public pages, read logged out: followers, median plays, posts a day, the best post and its
  length. In one niche's table of six pages, the client's page had the lowest median plays (about 30K), below two rivals
  with fewer followers, and the niche's biggest hits were single-incident cuts of 2:51 to 7:37.
- Platforms publish few benchmarks; build your own medians after about 20 posts, and judge a format after 30 to 50
  posts, not 5.
- What the benchmarks mean for formats and posting: social-video-formats.

## 5. Measuring our own output against the references
- Turn "it looks designed" or "it feels off" into a fix list with numbers before redesigning. One comparison of 22 of our
  videos against 71 references found 8 specific problems.
- Text on screen: OCR frames at 2 fps for the first 8 s, then 1 fps up to 40 s, at 720 px wide. Count readable words on
  screen at once (ours 10.5, native 4), tiny words under 1.8% of the frame height (ours 27, native 0), where the text
  centre sits (ours 26% from the top, native 50%), and the share of frames with any text (ours 100%, native 88%).
- Cuts: ffmpeg scene detection at 0.3 gives cuts per 10 s (ours 1.1, against references that either held one shot or
  cut 3+ times per 10 s, up to 19.3).
- The rules that came out of it (text density, placement, rhythm): social-video-formats and motion-design. OCR and
  scene-detection mechanics: premiere-ae-editing media-toolkit.md section 7.

## 6. Coding posts by attribute and comparing medians
- Code each post or title by hand (topic, angle, hook type, lesson or not, ending type, news peg, real clips or not, who
  it addresses; or the title's words), then compare the median views per group, and the top 15 against the rest.
- Example: on one mini-doc page, story-only reels did 170K median views against 6.9K with a lesson at the end.
- Always give the n (two title effects on one page rested on samples of 25 and 10 videos).
- **YouTube outliers:** views divided by the median of the 15 uploads either side of the video (on one channel, uploads
  of 25 to 45 min scored 2.8 to 3.8x). Use it to pick which videos to cut down (footage-sourcing.md section 2).
- **Hook candidates:** YouTube's "Most replayed" heatmap. The user's own hook clips sat at a median 95th percentile of
  replay; 46 of 66 were in the top 20%, and 16 of 20 hooks used a top-5 peak (editing-playbook).

## 7. Auditing a person's or a brand's channels
- Before pitching content for a person: followers, posting rate, who actually posts; rank their topics by engagement
  against their own median (one investor's robotaxi posts got 4.3x her median likes, her AI posts 1.1x, although AI was
  her most frequent topic). The pitch is the strong ideas that so far exist only as text.
- Mine the comments for demand, and borrow title grammar from the person's and their guests' best uploads.
- A brand's look: its public brand guide (try `brand.<domain>` on day 1), its site's CSS variables and its own art; a
  parked or default-theme domain is not brand evidence. Save the pages the day you find them (one guide answered 403 to
  readers a day later).

## 8. A client's own page data
- **Facebook:** the browser pane is refused on facebook.com (do not retry it). Use Meta Business Suite exports: the
  earnings export plus the detail export (246 columns, with a 41-point retention curve per video). Join them on the
  video ID in the permalink. Match posts to their YouTube originals by rare title words plus a plausible length; the
  exact length breaks ties.
- What the method found on one page (findings for that client's file, shown here as what the method yields): videos of
  10 min or more made 87% of earnings; only 7% of viewers reached the end while 24% were still watching at the
  midpoint (so the CTA moved to the middle); recommendations were 60% of watch time; reposts after 180+ days earned a
  median 39% of the first run.
- **Instagram:** per-post Insights at 24 h and 72 h (skip rate, average watch time, sends, follows, profile visits) and
  Story poll counts come from the user as screenshots or exports; ask for them, they decide what to make next.
- Client analytics are confidential: share ratios, not money (licensing-and-rights.md section 13). The boss needs his
  own Meta Business Suite access.

## 9. Choosing the time window
- Take trends from a short recent window and topics from a long one: the revenue-per-view trend from the last 4 weeks
  (the user: "rather than taking ALL the data"), topics from 15 months. A 4-week topic result was reversed by the
  longer window.

## 10. Scoping a study, and where verdicts come in
- Scope a study to the decision it serves. "Learn the effects from this page" means the headline effects (one or two
  per post): count them, tell the user the count and the list, and ask before adding more. One analysis logged every
  device and ballooned to 108 "effects" for about 30 tutorials ("how is there so many effects").
- Research findings are inputs; the user's and the boss's verdicts decide. The research favourite for one niche's
  caption style (a white rounded box with black lowercase text) was "TOOO off beat" for the user, and research that
  said "skip RGB split for a 40 to 65 audience" lost to the user loving RGB-split captions.
