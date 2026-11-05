# 03 Platform rules, disclosure law and legal risk for faceless Outcome pages

Researched on 13 Oct 2026 for the Vision Clipping team.
Client: Outcome (https://outcome.xyz), a prediction market front end on Hyperliquid (Yes/No contracts, USDC).
Pages in scope: faceless TikTok, Instagram/Facebook, YouTube Shorts and X pages run by a UK clipping agency.
This is research, not legal advice. Anything with real money or a regulator attached should go past a lawyer before launch.

## How to read this file

- Every claim carries a source tag like [T1]. The tags are listed with URL and date at the end of each section.
- UNCLEAR means I could not confirm it from a primary source, or the sources disagree. I did not guess.
- "Read via proxy" means my machine cannot open that site directly (tiktok.com refuses the connection from here, and X blocks automated readers). I read the page through a public reader service (r.jina.ai) so the text is the real page, but I could not click around it.
- "Secondary" means news, a law firm blog or a trade site describing the rule. Useful, but not the rule itself.
- If a page shows no date, I say "no date on page". All pages were read on 13 Oct 2026.
- Quotes are kept to a few words. Everything else is my paraphrase.

## 0. Read this first (the 10 things that matter most)

1. Outcome's own Terms rule out the audiences people usually aim at. Section 3B lists the United States, the United Kingdom, the UAE, Ontario, Singapore, Hong Kong, South Korea, China, Belgium and other EU states where not permitted, and sanctioned places as Prohibited Jurisdictions. Section 3E bans using a VPN to get round it. Section 3N bans encouraging others to break the Terms. India is not on the list. No date on the Terms page. [L0]
2. India is not a safe fallback. The Online Gaming Act 2025 bans making or causing any advertisement that promotes an online money game, with up to 2 years in prison and/or a fine up to Rs 50 lakh. India blocked Polymarket in May 2026 and treats prediction markets as online money games, according to press reports. [IN1][IN2]
3. No platform has a rule that names prediction markets for organic posts. Platforms file them under "gambling" or under "financial services". Plan for both.
4. TikTok is the biggest platform risk. The new Branded Content Policy (in force 31 Aug 2026) puts "Gambling, lotteries and real money games" and investment-type "Financial services" in the restricted list. A brand needs TikTok's explicit permission, a Registered Business Account, and must work with creators only through TikTok One. If TikTok counts Outcome in one of those industries (UNCLEAR), clippers paid per view outside TikTok One do not fit that. Crypto, trading and prediction markets are not named in that policy. [T1]
5. TikTok has a separate ad policy for prediction markets (updated Aug 2026). Approved advertisers can run ads in 17 markets, but only if they use trading or event contract language. Platforms that talk about users "placing bets", and odds-style or sportsbook-style products, are excluded. [T8]
6. Meta (Instagram and Facebook): branded content for real money gambling and for cryptocurrency products needs Meta's written pre-authorization. Binary options and CFD trading are banned from branded content. On 30 Apr 2026 Instagram extended its rule against recommending accounts that repost too much of other people's content to photos and carousels (Reels were already covered). [M3][M10]
7. YouTube: since 19 Mar 2025, any link, URL, logo or spoken mention that sends viewers to a gambling site not certified by Google is not allowed. Promising guaranteed returns can get a video removed even for certified sites. Casino-type content is age-restricted. No YouTube policy names prediction markets. [Y1][Y3]
8. X: since Feb 2026, gambling is banned from paid partnerships (affiliate codes, gifts and flat fees all count). Kalshi pulled every X affiliate badge on or about 23 Feb 2026. I could not read X's own policy pages. [X1][X3]
9. Anything paid is an ad, including pay per view. UK: the ASA wants a prominent "Ad" label upfront and says the platform label alone may not be enough. The CMA can fine up to 10% of global turnover. US: the FTC wants the disclosure in the video itself and says a platform tool is no guarantee. Ad agencies and networks can be liable. [D1][D3][D5][D9]
10. The 2026 warning shots are about the marketing, not the product: Polymarket (staged wins, hidden payments, "warm-up" accounts, sued 26 Jun 2026), Kalshi (NAD referral 8 Jun 2026, "money hack" TikTok ads), the FCA's April 2026 sweep, and the UK Gambling Commission's February 2026 statement. Do not copy what they did. [C2][C3][C4][T12][UK4][UK5]

Also remember: the "no bet/betting" rule helps with platform wording tests (TikTok's ad policy uses one), but it does not decide the legal category. The UK Gambling Commission says a prediction market cannot call itself non-gambling, the FCA says the financial ones are binary options, and the US Ninth Circuit called sports event contracts sports bets. [UK1][UK5][US3]

## 0.1 Quick table

| Platform | Organic gambling-type posts | Organic finance or crypto posts | Paid post label | Brand permission before paid posts | Link in bio | Main risk for Outcome clips |
|---|---|---|---|---|---|---|
| TikTok | Trading, marketing or giving access is not allowed. Posting links or sending people off-platform counts as marketing. In some regions shown or promoted gambling is 18+ and kept off For You. | "High-risk financial services" not allowed. Financial education allowed. Fake investment offers and get-rich-quick not allowed. Crypto not named. | Content disclosure toggle on every paid post | Yes for gambling and investment-type finance: TikTok's explicit permission, Registered Business Account, TikTok One only | Needs 1,000 followers or a Verified Business Account | Per-view clips in a restricted industry, paid outside TikTok One |
| Instagram / Facebook | Allowed but shown to adults 18+ only. Guaranteed-win offers removed. | No organic crypto rule found. Guaranteed or risk-free returns, get-rich-quick removed. | Branded content tool ("Paid partnership") plus clear ad text | Yes: written pre-authorization for real money gambling and crypto. Binary options and CFD trading banned | Up to 5 links, must follow the guidelines | Not being recommended (reposts, regulated products), hidden paid posts |
| YouTube Shorts | Links, URLs, logos and spoken mentions of uncertified gambling sites not allowed. Casino content age-restricted. | No crypto rule for organic found. Get-rich-quick schemes banned. | Tick "paid promotion" in video details | Paid promotions cannot push gambling sites that Google or YouTube have not reviewed | Links in Shorts comments and descriptions not clickable since 31 Aug 2023; channel links stay | A spoken or visual mention counts like a link |
| X | No organic gambling ban found. Banned in paid partnerships since Feb 2026. | No organic crypto ban found. Auto-lock for first-time crypto posters being rolled out. | Paid Partnership label (launched 1 to 2 Mar 2026) | Gambling not allowed in paid partnerships. Financial products reported as restricted | UNCLEAR (policy page blocked) | Paid posts about gambling-type content |

Sources for this table are in sections 1 to 4.

[L0] Outcome Terms of Service (Terms of Use), TytanTech Corporation (Panama). No date on page. https://outcome.xyz/terms . Read via proxy.
All other tags in this table and in section 0 ([T1], [T8], [M3], [M10], [Y1], [Y3], [X1], [X3], [D1], [D3], [D5], [D9], [C2], [C3], [C4], [T12], [UK1], [UK4], [UK5], [US3], [IN1], [IN2]) are listed with URL and date in the section that uses them.

## 1. TikTok

### 1.0 What I could and could not read

- tiktok.com and ads.tiktok.com refuse connections from this machine. I read TikTok pages through a public reader proxy.
- TikTok's Community Guidelines pages are script-built and came back empty through the proxy. For the full text I used a version-controlled archive copy of the 2025H2 guidelines (released 14 Aug 2025, in force 13 Sep 2025) [T3] and TikTok's Creator Academy article on regulated goods [T2]. The Creator Academy article has no date, but its disclosure wording matches the newer text that press reports describe [T11], so I treat it as the current text. UNCLEAR on the exact version date.
- A newer set of guidelines ("2026H2") was reported as released 25 Aug 2026 and in force 24 Sep 2026. I could only see it through secondary reports [T11]. UNCLEAR on its gambling lines.

### 1.1 Gambling in organic posts

- In Sep 2025 TikTok merged gambling, alcohol, tobacco, drugs, firearms and weapons into one "regulated goods and services" policy [T4].
- Not allowed: trading, marketing or giving access to gambling, gambling-like activities (social casinos, mystery boxes) and mystery-value products [T2][T3].
- "Trade" is defined widely. It includes posting links, sharing contact or location details and directing people off-platform [T2].
- Not allowed: showing or promoting young people gambling [T3].
- Region split in the 2025H2 text: in some regions even showing or promoting gambling is not allowed. In other regions it is allowed but age-restricted and kept out of the For You feed (FYF). The text I read does not say which regions. UNCLEAR [T3].
- Some regions let verified business accounts or TikTok Shop sellers market gambling [T2][T3].
- TikTok's definition of gambling is betting money or something of value on uncertain outcomes for financial gain [T3]. An older 2024H1 version, seen only in a search snippet, added digital currencies such as bitcoin and said gambling content is 18+ and kept off FYF if it shows or glamorises gambling [T10].
- Does this cover prediction markets? No TikTok text says so. TikTok's own ad rules file prediction markets under "Other products and services", not under "Gambling and Games" [T8]. UNCLEAR for organic posts. A Yes/No contract on a match result looks like a bet to a reviewer, so treat sports content as gambling content.

### 1.2 Finance and crypto in organic posts

- The Creator Academy article lists "high-risk financial services" as something you cannot trade, market or give access to. It defines them as money or asset management products or activities that are predatory, carry extreme risk or lack transparency [T2].
- Allowed: financial education and information about financial products and services [T2].
- Not allowed: fake investment offers and get-rich-quick schemes (scams), celebrity impersonation to sell something, multi-level marketing and money muling [T2][T3].
- Cryptocurrency, trading and investing are not named in either text [T2][T3].
- The 2025H2 archive copy has the scams ban but no "high-risk financial services" line [T3]. So that line looks new in the 2026 text. UNCLEAR, because the Creator Academy page is undated.
- My reading: explaining how a market works is education. Telling people to deposit and make money is promotion and could hit the scams rule or the high-risk rule. UNCLEAR where TikTok draws the line for Outcome.

### 1.3 Branded content policy (paid posts)

The global Branded Content Policy was published 4 Aug 2026 and is in force from 31 Aug 2026 [T1].

Banned from branded content (cannot be promoted at all), selected items [T1]:
- Financial services of the pyramid scheme, multi-level marketing, too-good-to-be-true offer, payday loan and get-rich-quick kind.
- Products and services that enable dishonest behaviour (fraud, falsification, stealing personal data).
- Professional services (accounting, legal, immigration).
- Also banned: adult products, animals, tobacco and nicotine, dating and live video apps, drug-related products, pharmaceuticals and medicine, political advertising, sensitive religious content, weapons, weight loss products, counterfeit goods and other highly controversial or dangerous items. Full list at the URL.

Restricted (allowed only with TikTok permission, 18+, and only in some markets) [T1]:
- "Financial services", described as loans, credit cards, insurance, investment services, and lending and management of money assets.
- "Gambling, lotteries and real money games".
- Also alcohol, energy drinks, film and game trailers, over-the-counter and prescription medicines, vitamin supplements, underwear and government advertising.

The rules for the restricted list [T1]:
- All brand partners must get explicit permission from TikTok before promoting these industries.
- The brand must hold a Registered Business Account and pass any extra qualification steps.
- Brands may only work with creators through the TikTok One platform.
- The content is limited to viewers aged 18+ and to the market where it was originally posted.

Where it is allowed for the countries that matter here [T1]:

| Country | Financial services | Gambling |
|---|---|---|
| United Kingdom | Allowed, 18+, original market only | Allowed, 18+, original market only |
| United States | Allowed, 18+, original market only | Allowed, 18+, original market only |
| UAE | Allowed, 18+, original market only | Allowed, 18+, original market only |
| Ireland | Not allowed | Not allowed |
| India | Not listed | Not listed |

- TikTok saying "allowed" is not the client's permission. The UK, US and UAE are on TikTok's allowed list but are Prohibited Jurisdictions in Outcome's Terms [L0].
- "Original market" matters. My reading is that the account's market decides who can see restricted branded posts, so a UK-registered account would reach UK viewers only. That is the audience Outcome excludes. UNCLEAR how TikTok decides the market.
- Crypto, trading platforms, betting and prediction markets are not named anywhere in the policy [T1]. UNCLEAR whether TikTok would put Outcome under financial services, gambling, both or neither.
- TikTok's country-specific branded content page says its Branded Content and Ads policies differ, and that something banned in branded content may still be allowed in ads. Seen in a search snippet only [T14].

Does the "content disclosure" toggle apply? Yes. Anyone posting branded content must switch on the commercial content disclosure toggle. The post is then labelled as Branded Content, may be kept in TikTok's Commercial Content Library where the law requires, and the product must be clear without opening the profile or any link [T1]. The toggle does not make a restricted product allowed. It only discloses the deal.

### 1.4 What happens if you skip the disclosure toggle

- Required when you promote your own business, product or service, or post branded content (reviews and endorsements) for any incentive [T2][T3][T5]. A per-view payment is an incentive.
- 2025H2 text: undisclosed commercial content is ineligible for FYF [T3]. Newer Creator Academy text: it may have reduced visibility, or TikTok may switch the setting on for you. Repeated failure can mean temporary posting restrictions or a ban [T2].
- TikTok sends a notice when a post may be undisclosed branded content. You have 24 hours to respond before it becomes ineligible for FYF. Only the original poster can appeal [T5].
- TikTok says exact legal requirements vary by country and points to the US FTC Endorsement Guides [T5].

### 1.5 For You feed (FYF) eligibility rules that hit gambling and finance posts

- Gambling shown or promoted: age-restricted and FYF-ineligible where allowed at all, not allowed elsewhere [T3].
- Undisclosed commercial content: see 1.4.
- Reused or unoriginal content posted without creative edits: FYF-ineligible. This hits plain clip reposts [T3].
- Realistic AI scenes or people must be labelled. Unlabelled realistic AI content is FYF-ineligible [T3].
- Services that boost engagement are not allowed, and "like-for-like" promises are FYF-ineligible [T3].
- Since Sep 2025 the FYF rules are spread across many sections instead of one list, so they are harder to check [T15].
- TikTok says restrictions show up in the TikTok analytics tool, and low views alone do not prove a restriction [T6].
- Reported 2026 change (secondary): action against associated accounts for serious violations or evasion, and a ladder of warning, restriction, then ban [T11]. Relevant to a network of pages. UNCLEAR how TikTok decides two accounts are associated.

### 1.6 Links in bio

- You need 1,000 followers or a Verified Business Account to add a website link. Many blogs say a plain Business Account is enough, but TikTok's own page does not say that. UNCLEAR [T7].
- Links must follow the Community Guidelines and users can report a link [T7]. TikTok limits link chains in its in-app browser [T7].
- For gambling-type products, TikTok counts posting links, sharing contact details and sending people off-platform as marketing or giving access [T2]. So a bio link or a link in a comment to Outcome could itself be treated as promotion. UNCLEAR whether TikTok sees Outcome that way.
- Gambling affiliate guides (secondary, not TikTok text) suggest a neutral explainer page instead of a direct operator link. A neutral page does not change the legal position [T16].

### 1.7 TikTok's ad rules for prediction markets (ads only, but it shows how TikTok thinks)

- Page "Other products and services", last updated Aug 2026. The ad policy change log lists "Update to Prediction Markets and Event Contracts Policy (July 2026)" [T8].
- Ads may be allowed, with restrictions, in 17 markets: Canada, United States, Philippines, Bolivia, Ecuador, Guatemala, Dominican Republic, Paraguay, Colombia, Panama, Peru, United Kingdom, Ireland, Denmark, Finland, Sweden and Israel. Other markets are not eligible [T8].
- The advertiser must work with a TikTok Sales Representative and apply for permission. Ads must be age-targeted and must meet disclosure and disclaimer rules [T8].
- Examples that may be allowed: platforms using financial trading or event contract terms, regulated event outcome trading platforms, and platforms where users trade contracts with other participants [T8].
- Examples not allowed: platforms that describe users as placing bets or use gambling terms, odds-based or sportsbook-style betting products, and products not licensed or permitted where the ad runs [T8].
- The page does not cover profit claims, guaranteed returns, testimonials or specific event types such as elections [T8].
- A law firm comment (Troutman Pepper Locke, 21 Sep 2026) says "trade" versus "bet" wording carries legal weight. Calling the product trading to regulators and betting in marketing invites deception claims [T13].
- TikTok's gambling ad policy needs certification and licence proof, bans ads to minors and bans unlicensed services [T9].

### 1.8 Known enforcement against Polymarket or Kalshi style content, 2025 to 2026

- I found no public report that TikTok removed, restricted or shadowbanned prediction-market videos or creators in 2025 or 2026. That is absence of evidence, not proof. UNCLEAR.
- What is documented: Kalshi ran TikTok ads that promised a "money hack", showed "$761 last night" style claims and a "side hustle" framing, and said it was "legal in all 50 states". Kalshi told Media Matters it no longer works with those influencers (30 Mar 2026) [T12].
- The Wall Street Journal (20 to 21 Jun 2026) found Polymarket's paid clips drew more than 140 million views across TikTok, YouTube and Instagram. I found no report that the platforms took them down [C2].
- On 8 Jun 2026 the National Advertising Division said it would refer Kalshi to regulators including state attorneys general, and to the platforms where the ads appeared [C4]. Platform action could follow. UNCLEAR.

### 1.9 What this means for Outcome clips on TikTok

- Treat every per-view or paid clip as branded content and switch the toggle on.
- Ask Outcome for written proof that TikTok has given it permission for the restricted industry and that it works through TikTok One. If it has not, paid posts risk removal and the account risks restriction. UNCLEAR how often TikTok enforces this.
- Keep gambling cues out: no odds boards, no sports score plus Yes/No price combos that look like a bet slip, no winnings.
- Do not present Outcome as a way to earn money.

### Sources for section 1

- [T1] TikTok Branded Content Policy (global). Published 4 Aug 2026, in force 31 Aug 2026. https://www.tiktok.com/legal/bc-policy?lang=en . Read via proxy.
- [T2] TikTok Creator Academy, "Regulated Goods on TikTok". No date on page. https://www.tiktok.com/creator-academy/en/article/regulated-goods-on-tiktok?lang=en . Read via proxy.
- [T3] TikTok Community Guidelines, 2025H2 version, released 14 Aug 2025, in force 13 Sep 2025. Archive copy by OpenTermsArchive. https://github.com/OpenTermsArchive/contrib-versions/blob/main/TikTok/Community%20Guidelines.md (raw text read from https://raw.githubusercontent.com/OpenTermsArchive/contrib-versions/main/TikTok/Community%20Guidelines.md ). Capture date not shown.
- [T4] TikTok Newsroom, 14 Aug 2025. https://newsroom.tiktok.com/create-discover-and-connect-on-tiktok-with-simpler-and-stronger-community-guidelines?lang=en . Read via proxy.
- [T5] TikTok Business Help, "About the Commercial Content Disclosure setting for creators". No date on page (tagged 2025H2update). https://ads.tiktok.com/resources/help/article/about-the-content-disclosure-setting-for-creators . Read via proxy.
- [T6] TikTok Creator Academy, why a video may not be recommended. No date on page. https://www.tiktok.com/creator-academy/article/video-not-recommended . Read via proxy.
- [T7] TikTok Support, "Adding a website link to your profile". No date on page. https://www.tiktok.com/support/faq_detail?id=7581821550328896012 . Read via proxy.
- [T8] TikTok Ads policy, "Other products and services" (prediction markets), last updated Aug 2026. https://ads.tiktok.com/resources/help/article/tiktok-ads-policy-other-products-and-services . Change log, page updated Oct 2026: https://ads.tiktok.com/resources/help/article/tiktok-ad-policy-change-log-2026 . Read via proxy.
- [T9] TikTok Ads policy, "Gambling and Games". No date on page. https://ads.tiktok.com/resources/help/article/tiktok-ads-policy-gambling-and-games . Read via proxy.
- [T10] Older TikTok Community Guidelines page (2024H1 version), seen only as a search-result snippet, not opened. https://www.tiktok.com/community-guidelines/en/regulated-commercial-activities?cgversion=2024H1update
- [T11] Secondary reports on the 2026H2 guidelines (released 25 Aug 2026, in force 24 Sep 2026): SocialDay, 29 Sep 2026, https://socialday.live/features/tiktoks-september-community-guidelines-formalise-off-platform-account-bans ; NoobClaw, no date, https://noobclaw.com/blog/tiktok-community-guidelines-update-september-2026/ .
- [T12] Media Matters, 30 Mar 2026. https://www.mediamatters.org/tiktok/kalshi-aggressively-advertising-tiktok-seemingly-targeting-young-people-while-promising
- [T13] Gambling Insider piece reposted by Troutman Pepper Locke, 21 Sep 2026. https://www.troutman.com/insights/tiktoks-prediction-market-ad-rules-make-trading-vs-betting-more-than-branding/ (commentary only; it quotes no TikTok text).
- [T14] TikTok Business Help, branded content policy country-specific requirements. No date. https://ads.tiktok.com/help/article/branded-content-policy-country-specific-requirements . The "ads versus branded content differ" line was seen in a search snippet only.
- [T15] TechCrunch, 15 Aug 2025. https://techcrunch.com/2025/08/15/tiktoks-new-guidelines-add-subtle-changes-for-live-creators-ai-content-and-more/
- [T16] Affnook, iGaming affiliate guide to TikTok (secondary, not TikTok text). Page shows 08/12/2025 as the published date (day and month order unclear). https://affnook.com/tiktok-gambling/
- [C2], [C4], [L0]: see sections 7 and 6.

## 2. Instagram and Facebook (Meta)

### 2.0 What I could and could not read

- Meta's Transparency Center pages were readable (some directly, some via the reader proxy). The Instagram Help Center pages were read via proxy. Facebook's own Branded Content Policies page hides behind a login wall, so I used the Instagram version of the same policy.
- None of the Meta pages I read show a date unless I say so.

### 2.1 Gambling in organic posts

- Meta's Community Standard on restricted goods and services covers online gaming and gambling where you pay something of value to play and can win a money prize. Examples listed: betting, sports betting, casino games, lotteries, sweepstakes. Content that attempts to sell, trade, depict or promote these is not removed. Its visibility is limited to adults aged 18 and over [M1].
- Social casino games and free-to-play games that copy gambling get the same 18+ limit [M1].
- Meta counts digital currencies such as bitcoin as something of value you can pay with [M1].
- Prediction markets are not named. UNCLEAR [M1].
- Effect for you: a post that promotes a gambling-type service stays up but is shown to adults only, which usually means less reach. The reach drop is my inference, not a Meta statement.

### 2.2 Scams, "guaranteed" claims and deceptive gambling promotion (these are removed)

From Meta's Fraud, Scams and Deceptive Practices standard [M2]:
- Investment offers with guaranteed or risk-free returns are not allowed.
- Citing past returns to suggest similar future results is not allowed.
- Offers of quick returns (such as under 24 hours) and "cash flip" or "money flip" offers are not allowed.
- Get-rich-quick offers (a big reward for little or unclear effort) are not allowed.
- Real money gambling offers that guarantee a win are not allowed.
- Promoting gambling in deceptive or hidden ways, and promoting known deceptive gambling vendors, are not allowed.
- Implying or admitting that a game or match was rigged is not allowed.
- Pretending to speak for a brand ("brand bait") or using a public figure's name or face ("celebrity bait") is not allowed.
- Enforcement can mean removing content, reducing distribution, restricting ad accounts or disabling accounts [M2].
- There is no crypto-specific organic rule on that page [M2].

### 2.3 Crypto and gambling in Meta's ad rules (not organic, but it shows where Meta draws the line)

- Ads promoting crypto exchanges and trading platforms (spot, margin, futures), crypto lending, wallets that buy, sell, swap or stake, and soliciting investment in them need Meta's prior written permission. Crypto education and news with no product offer do not [M5].
- Licences Meta accepts include FCA authorisation for the UK and FinCEN registration or a New York BitLicense for the US [M5].
- Ads for online gambling need Meta authorisation, cannot target under-18s, and India is on the list of unsupported markets [M4].
- If an affiliate wants to publish gambling ads itself, it must apply in Business Suite as an "Affiliate" and upload the operator's licence. If the operator publishes and the affiliate is only tagged, the affiliate does not need to apply [M6].

### 2.4 Branded content tool and rules (paid posts)

From Instagram's Branded Content Policies [M3]:
- Branded content may only be posted with the branded content tool. Creators need the partner's prior permission to tag it.
- Banned from branded content: payday loans, multi-level marketing, initial coin offerings, binary options and CFD trading (plus tobacco, drugs, weapons, adult products, state lotteries and other items).
- The business partner needs Meta's written pre-authorization before branded content in these areas, including real money gambling and cryptocurrency products and services.
- Financial and insurance products are a restricted category with limits on who can see the post.
- Creators must give the disclosures needed to show the content is commercial and must follow all laws.

Two UNCLEAR points that matter for Outcome:
- The FCA's view is that financial yes/no prediction products are binary options [UK1]. Meta bans binary options in branded content [M3]. No Meta text says Outcome counts as binary options, but a reviewer could read it that way.
- If a clipper labels a post "Ad" in text but does not tag it through the tool, Meta's rule says branded content may only go through the tool. What Meta does in that case is UNCLEAR.

### 2.5 What keeps a Reel out of recommendations

Instagram's Recommendations Guidelines set a higher bar than the Community Standards because recommended content comes from accounts people did not choose to follow [M7].

Content that is allowed but may not be recommended includes [M7]:
- Self-harm related content, violence, and sexually explicit or suggestive content.
- Promotion of regulated products: tobacco, vaping, alcohol, firearms, pharmaceutical drugs, psychedelics, cannabis.
- Promotion of weight loss products or cosmetic surgery.
- Low-quality content, including unoriginal content that is mostly repurposed from another source with only minor edits, and coordinated comment networks.
- Content rated false or altered by fact-checkers (in countries with that programme).

What is not named on that page: gambling, betting, casino, crypto, investment, finance, scams, get-rich-quick, clickbait, engagement bait and links [M7]. "Regulated products" is named, so a reviewer could place gambling there. UNCLEAR.

An account can be made ineligible for recommendations if it [M7]:
- Recently broke the Community Guidelines.
- Repeatedly shared ineligible content, including in its name, username, profile photo or bio.
- Used misleading follower-building such as buying likes.
- Has been banned from running ads.
- Repeatedly posted content rated false or altered.
- Repeatedly shared photorealistic AI-generated people without the AI-generated profile label.

Creator advice from Instagram [M8]: avoid reuploading Reels that are already on Instagram; Reels with watermarks or blur are less likely to be recommended; Settings > Account > Account Status shows whether you are eligible and lets you ask for a review.

On the Facebook side, content that Meta's systems predict is likely to break the rules but is not confirmed (the list includes scams, and buying, selling, trading or promoting restricted goods and services) gets its distribution reduced. Clickbait links and engagement bait are also demoted [M9].

New in 2026: on 30 Apr 2026 Instagram extended its originality rule from Reels to photos and carousels. Accounts that repost too much become ineligible for recommendations, and reuploads do not show in the Discover feed unless they are significantly changed. Followers of the account still see the posts. Memes with real added humour, commentary or a distinct take count as original. Speed changes or a credit to the original poster do not [M10]. This lands directly on clipping pages. (Secondary report quoting Instagram's blog.)

### 2.6 Link in bio

- Since Apr 2023, Instagram allows up to 5 links in a bio. Meta said any URL that follows its Community Guidelines and Terms is fine, and links are scanned [M11].
- I found no Instagram rule that bans a gambling or crypto bio link by itself. The gambling (18+ limit) and scam rules above apply to the account's content. UNCLEAR [M1][M2][M11].
- Bio, name and username count when Instagram decides whether an account is eligible for recommendations [M7]. Do not put "bet" style or "guaranteed" style text there.

### 2.7 Enforcement signals

- The FCA's April 2026 sweep: its figures on 1,267 illegal financial adverts and 120 takedown requests to platforms relate to Meta platforms only. The FCA said platforms are not doing enough to enforce their own rules [UK4].
- On 8 Jun 2026 NAD flagged Instagram and X posts for Kalshi that potentially lacked disclosures [C4].
- Garbage Day (29 Jun 2026) says Instagram is the main target of Kalshi clipping campaigns, with about 50 meme pages reaching US and UK Gen Z audiences, and that very few posts were disclosed as ads [C1].
- I found no report of Meta banning prediction-market meme pages or clipper accounts in 2026. UNCLEAR.

### Sources for section 2

- [M1] Meta Community Standards, Restricted Goods and Services. No date on page. https://transparency.meta.com/policies/community-standards/restricted-goods-services/ . Read via proxy.
- [M2] Meta Community Standards, Fraud, Scams and Deceptive Practices (same wording appears in Prohibited Commercial Practices). Change log shows "Today", no date. https://transparency.meta.com/policies/community-standards/fraud-and-scams/
- [M3] Instagram Help, Branded Content Policies. No date on page. https://help.instagram.com/1695974997209192 . Read via proxy.
- [M4] Meta Advertising Standards, Online Gambling and Games. No date on page. https://transparency.meta.com/policies/ad-standards/restricted-goods-services/gambling-games/ . Read via proxy.
- [M5] Meta Advertising Standards, Cryptocurrency Products and Services. Latest dated change log entry 15 Apr 2026. https://transparency.meta.com/policies/ad-standards/restricted-goods-services/cryptocurrency-products-and-services/
- [M6] Meta Business Help, how to apply for permission to promote online games or gambling. No date on page. https://en-gb.facebook.com/business/help/4740325989340856 . Read via proxy.
- [M7] Instagram Help, Recommendations on Instagram (Recommendations Guidelines). No date on page. https://help.instagram.com/313829416281232 . Read via proxy.
- [M8] Instagram Creators blog, recommendations eligibility tips. No date on page. https://creators.instagram.com/blog/instagram-recommendations-eligibility-tips-creators
- [M9] Meta Transparency Center, content likely violating our Community Standards, and Types of content we demote (updated 2 Jul 2025). https://transparency.meta.com/features/approach-to-ranking/content-distribution-guidelines/content-likely-violating-our-community-standards/ and https://transparency.meta.com/features/approach-to-ranking/types-of-content-we-demote/
- [M10] Tubefilter, 30 Apr 2026. https://www.tubefilter.com/2026/04/30/instagram-removes-algorithm-recommendations-repost-content-aggregator/ (secondary; Instagram's own post was not opened).
- [M11] TechCrunch, 18 Apr 2023. https://techcrunch.com/2023/04/18/instagram-takes-on-linktree-and-others-with-support-for-up-to-5-links-in-bio/
- [UK1], [UK4], [C1], [C4]: see sections 6 and 7.

## 3. YouTube Shorts

### 3.0 What I could and could not read

YouTube's help pages (support.google.com) opened normally. The original TeamYouTube announcement thread would not show its body, so for the March 2025 announcement I used a trade-press mirror of the post [Y3].

### 3.1 Gambling content (including the 2025 updates)

- YouTube lists "uncertified online gambling sites" as regulated goods. Not allowed: facilitating access to an online gambling or sports betting site that is not certified, and promising guaranteed returns through online gambling whether or not the site is certified [Y1].
- "Facilitating access" covers clickable URLs and also verbally pointing people to other sites in videos [Y1].
- Only domains certified by Google Ads can be linked or promoted, and certification changes over time. YouTube allows links only to gambling sites that meet local legal requirements [Y2].
- The TeamYouTube announcement (post dated 8 Mar 2025, in force 19 Mar 2025) said [Y3]:
  - No way of sending viewers to gambling sites or apps not certified by Google: URLs, embedded links, logos, spoken mentions and visual displays all count.
  - Content promising guaranteed returns can be removed even when the site is certified.
  - Content that does not break the rules but shows or promotes online casino sites or apps can be age-restricted, so signed-out users and under-18s cannot view it. Online sports betting and depictions of in-person gambling are outside that age restriction.
- The policy page lists the same age-restriction idea: content that facilitates access to, promotes or depicts online gambling and social or sweepstakes casinos. Exceptions: sports betting from Google-certified providers, and promotion of certified sites during a live sporting event [Y1].
- Prediction markets are not named in any YouTube text I found. UNCLEAR [Y1][Y2][Y3].
- UNCLEAR and important: Google does not publish its list of certified gambling sites. If YouTube treats Outcome as a gambling site, any link, URL, logo or spoken name of Outcome in a Short could break the rule. Ask the client whether YouTube or Google has ever classified Outcome.
- Google Ads opened to prediction-market ads on 21 Jan 2026, but only for CFTC-regulated platforms in the US, and binary options ads stay banned, including from offshore platforms (secondary report) [Y10].

### 3.2 Crypto and finance

- The Spam, deceptive practices and scams policy bans "get rich quick" investment schemes, fake offers, misleading titles and thumbnails, and content made only to push viewers off YouTube. Crypto is not named there [Y4].
- The Harmful or dangerous content policy mentions crypto only for phishing for wallet details [Y5].
- I found no organic crypto promotion policy on YouTube. UNCLEAR.
- Monetisation rules: the monetisation page treats AI personas that present as experts on finance as a problem (its example is an AI-generated host giving investment tips). It also limits or removes ad earnings for templated, mass-produced or repetitive content, and for reused content with no real changes, even when you have permission [Y9]. This matters for faceless AI-voice pages and for clip pages. It affects earnings and channel standing, not only single videos.

### 3.3 Paid promotion disclosure

- Tick the paid promotion box in video details. The rule covers videos, descriptions, comments, live streams and Shorts [Y6].
- YouTube then shows viewers a disclosure message for 10 seconds at the start of the video [Y6].
- Creators and brands are responsible for local legal disclosure rules, which can be stricter about when, how and to whom you disclose [Y6].
- The page lists things that cannot be promoted in paid promotions, including online gambling sites not yet reviewed by Google or YouTube [Y6]. It does not mention financial or crypto products specifically [Y6].
- UK standard on top of the tickbox: the ASA says the title or thumbnail of a YouTube video should carry an identifier such as "Ad" before the click, and that autoplay video needs the disclosure as soon as people engage [D1]. How the ASA applies this to Shorts is UNCLEAR.

### 3.4 Links in Shorts

- Since 31 Aug 2023, links in Shorts comments, Shorts descriptions and the vertical live feed are not clickable. YouTube added clickable links on channel profiles instead (secondary report of YouTube's help page) [Y8].
- Under the External links policy, a violating URL in a video or its metadata can get the video removed. A first violation usually gets a warning. Three strikes in 90 days can end the channel, and one severe case can too [Y7]. That page does not mention gambling. The gambling rules sit in the regulated goods policy [Y1][Y7].

### 3.5 Enforcement signals

- I found no report that YouTube removed, age-restricted or demonetised prediction-market Shorts or channels in 2025 or 2026. Absence of evidence, not proof. UNCLEAR.
- The Polymarket clips that the WSJ reviewed reportedly drew views on YouTube as well as TikTok and Instagram, and I found no report that they were taken down [C2].
- The only enforcement-style change that touches this topic is the March 2025 gambling-link rule in 3.1 [Y3].

### Sources for section 3

- [Y1] YouTube Help, Illegal or regulated goods or services policies. Shows only "2026 Google", no update date. https://support.google.com/youtube/answer/9229611
- [Y2] YouTube Help, links to online gambling sites. No date on page. https://support.google.com/youtube/answer/9910779
- [Y3] TeamYouTube announcement "An update to YouTube's policies on online gambling content", thread https://support.google.com/youtube/thread/328728041 (body not readable). Mirror: Public Gaming Research Institute, 8 Mar 2025, https://publicgaming.com/news-categories-m/company-news/14040-youtube-to-remove-or-age-restrict-online-gambling-content-starting-march-19
- [Y4] YouTube Help, Spam, deceptive practices and scams policies. No date on page. https://support.google.com/youtube/answer/2801973
- [Y5] YouTube Help, Harmful or dangerous content policies. No date on page. https://support.google.com/youtube/answer/2801964
- [Y6] YouTube Help, Add paid product placements, sponsorships and endorsements. No date on page. https://support.google.com/youtube/answer/154235
- [Y7] YouTube Help, External links policy. No date on page. https://support.google.com/youtube/answer/9054257
- [Y8] Tubefilter, 10 Aug 2023 (secondary, not opened; seen in search results). https://tubefilter.com/2023/08/10/youtube-shorts-comments-spam/
- [Y9] YouTube Help, channel monetization policies (heading still reads "Generic or repetitive content"; policy renamed "inauthentic content" on 15 Jul 2025). https://support.google.com/youtube/answer/1311392
- [Y10] PPC Land on Google's prediction-markets ad policy (announced 5 Jan 2026, effective 21 Jan 2026), secondary, not opened. https://ppc.land/google-opens-prediction-markets-to-advertising-but-only-for-cftc-regulated-platforms/
- [D1]: see section 5.

## 4. X (Twitter)

### 4.0 What I could and could not read

help.x.com and business.x.com return a bot-check block even through the reader proxy. I could not read X's own policy pages. Everything below comes from press reports and crypto and gambling news sites, so treat X rule details as UNCLEAR until someone opens X's page in a normal browser: https://help.x.com/en/rules-and-policies/paid-partnerships-policy

### 4.1 Gambling and paid partnerships

- In Feb 2026 X added gambling to the industries banned from paid partnerships: lotteries, social casinos, sports betting and other gambling-related content. The exact effective date is UNCLEAR: CasinoBeats reported it on 18 Feb 2026 and Yahoo Tech on 20 Feb 2026 [X1][X2].
- "Paid partnership" is defined widely: any post made in return for compensation or incentives from a third party. That includes direct payments, affiliate commissions, revenue sharing, referral and discount codes, and gifts [X1][X2].
- Penalties reported: removal of the post, read-only mode for an undetermined time, and suspension for repeat breaches [X1][X2].
- X ads are governed separately, so gambling banned in paid partnerships can still be allowed in X ads in some countries (reports) [X2].
- Financial products are also named among the affected sectors [X1].
- Prediction markets are not mentioned in the reports. UNCLEAR [X1][X2].
- Kalshi removed all its X affiliate badges on or about 23 Feb 2026 (The Block reported it on 24 Feb 2026). Its spokesperson said it became too difficult to police and people confused badged accounts with Kalshi-endorsed messages. Polymarket affiliates kept their badges, and Polymarket is an official X partner [X3].

### 4.2 Paid Partnership label

- Launched 1 to 2 Mar 2026. Creators switch on a content disclose setting and a Paid Partnership label shows under the post. It can be added after posting. Before this, creators used #ad and similar hashtags [X4].
- X's head of product Nikita Bier said undisclosed promotions hurt the integrity of the product [X4]. The TechCrunch report does not say the label is mandatory or describe penalties [X4].

### 4.3 Crypto

- Bier said on 31 Mar to 2 Apr 2026 that X was implementing auto-locking and verification when an account posts about crypto for the first time, and would require ownership verification for accounts over 10,000 followers that launch a memecoin with no crypto history. Spam that mass-tags accounts to push crypto was reported blocked from 1 Apr [X5].
- Status was "in progress". UNCLEAR whether it is live for everyone [X5].
- Practical meaning: a brand-new faceless page whose first posts are about crypto may get locked and asked to verify.

### 4.4 Organic gambling and crypto posts

I found no ban on organic gambling or crypto posts on X. UNCLEAR. X's platform manipulation and spam rules (duplicate content, multiple accounts, coordinated activity) are the ones that usually catch clipping networks, but I could not read them.

### Sources for section 4

- [X1] Yahoo Tech, 20 Feb 2026 (quotes X's updated paid partnerships policy). https://tech.yahoo.com/social-media/articles/x-policy-change-paid-partnerships-152000378.html
- [X2] CasinoBeats, 18 Feb 2026. https://casinobeats.com/2026/02/18/x-updates-paid-partnerships-policy-ban-gambling-promotions/
- [X3] The Block, 24 Feb 2026. https://www.theblock.co/post/390983/kalshi-removes-x-affiliate-badges-after-policy-shift-tightens-promotion-rules
- [X4] TechCrunch, 2 Mar 2026. https://techcrunch.com/2026/03/02/x-ads-paid-partnership-labels-for-creators-so-they-can-ditch-the-hashtags/
- [X5] TradingView (NewsBTC), early Apr 2026 (reports Bier's posts of 1 and 2 Apr 2026). https://www.tradingview.com/news/newsbtc:a76055662094b:0-crypto-users-beware-x-s-new-rules-could-get-you-banned/

## 5. Disclosure law for paid promotion

### 5.1 When is a post an ad?

- UK, ASA: a post is an ad when a brand pays or otherwise incentivises the poster, or there is a personal or commercial tie, and the brand has editorial control. Affiliate links and codes count. Requested or unsolicited incentives both count [D1].
- UK, CMA: any incentive counts: money, commission, discounts, free products. It applies no matter how many followers you have [D3].
- US, FTC: disclose any financial, employment, personal or family relationship, and anything of value given for mentioning a product [D8][D9].
- My reading: a fee per view, per signup or a flat fee from a brand or from a clipping platform is an incentive, so the post is an ad. Being faceless changes nothing, because the page is the publisher.

### 5.2 UK: ASA, CAP Code and CMA

- CAP Code rule 2.1: marketing communications must be obviously identifiable as such. Rule 2.3: they must not falsely claim or imply the marketer is acting as a consumer and must make clear their commercial intent if the context does not. Rule 2.4: advertorials must be made clear. Rules 2.3 and 2.4 reflect banned practices in Schedule 20 of the DMCC Act [D2].
- ASA expects a prominent "Ad" label upfront, visible before people click anything. A "#" is not needed. Burying it after "See more" or in a hashtag list is not enough [D1].
- Video: commercial intent should be clear before the click, or immediately clear from the outset. For autoplay, as soon as people engage. For YouTube-style video the title or thumbnail should carry an identifier such as "Ad" [D1].
- Platform tools help but, per the ASA's 2026 research, the Paid partnership label "may not be enough on its own". Add your own "Ad" label [D1].
- ASA advises against "Sponsored". Vague or short labels such as "Supported by", "Gifted", "In association with", "#BrandAmbassador", "aff", "sp", "spon" and "affiliate" are likely insufficient. @mentions, discount codes, the bio and earlier posts do not count. Each post must be recognisable as an ad on its own [D1].
- Responsibility: brands and influencers are both responsible. For affiliate content the ASA typically treats the brand as at least jointly responsible. Rulings name both [D1].
- CMA says it must be immediately clear that content is an ad. Acceptable labels include "ad", "advert", "advertising" and "advertisement". Platform tools such as "paid partnership" are fine if clearly visible, otherwise use #Ad upfront. Avoid #gift, #spon, #collab and "thank you". Put video and audio disclosures at the start. Each item in a carousel needs its own label [D3].
- CMA says hidden ads are illegal. Enforcement can come from the CMA, Trading Standards or the Northern Ireland Department for the Economy [D3]. Hidden advertising is a banned practice under Schedule 20 of the DMCC Act [D4]. Since the new regime started in April 2025 (CMA release of 7 Apr 2025) the CMA can decide breaches itself and fine up to 10% of global turnover [D5].
- Finance overlay: the FCA expects social media promotions to disclose paid relationships, and refers influencers to the ASA expectation to label ads upfront, including affiliate links [D6][D7].
- Real-world check: Adclear (24 Sep 2026) scored 57 high-traffic Instagram and TikTok crypto trading posts. 89% breached FCA promotion rules, 56% lacked risk warnings, 54% did not disclose paid advertising and 11% suggested guaranteed returns. Some creators were outside the UK [D12].

### 5.3 US: FTC

- Disclosure must be hard to miss and placed with the endorsement itself. For video, put it in the video, early; repeats are better. A description alone is not enough. A hyperlinked "Disclosure" button is not clear and conspicuous [D9].
- A platform disclosure tool is not automatically enough. The ultimate responsibility rests with the influencer and the brand [D9].
- Advertisers need reasonable programmes to train and monitor their network of endorsers. Outsourcing does not remove responsibility. The FTC's focus is usually on advertisers or their ad agencies and PR firms, and intermediaries can be liable [D9].
- Use plain terms such as "ad", "advertisement" or "sponsored". Avoid "sp", "spon" and "collab" [D8]. The ASA advises against "Sponsored" [D1], so use "Ad" and you are fine in both countries.
- The Endorsement Guides were revised in 2023 [D9].
- The FTC's Consumer Reviews and Testimonials Rule (final 14 Aug 2024, in force 21 Oct 2024) bans selling or buying fake indicators of social media influence, such as bot followers or views, when the buyer knew or should have known they were fake and used them for a commercial purpose. Civil penalties can follow for knowing violators [D10]. Do not buy views.
- Enforcement mood in 2026: no FTC action against prediction-market influencers has been announced. Law firm Kelley Drye (28 Jun 2026) says the FTC "may have temporarily stepped away" while private plaintiffs and consumer groups step up [C3]. NPR (7 Jun 2026) reports the FTC rules have not been rolled back and no enforcement actions announced [C5]. Class actions in California, Florida and Illinois cite state consumer protection law and the FTC guidelines (Ifrah Law, 11 Jun 2026) [C3].

### 5.4 India (short)

- The Department of Consumer Affairs issued "Endorsement Know-hows" in Jan 2023. Endorsers must disclose material interests such as gifts, discounts or equity, clearly and prominently. Penalties come from the Consumer Protection Act: up to Rs 10 lakh, up to Rs 50 lakh for repeat offences, and endorsement bans (secondary reports) [D11].
- ASCI's guidance on virtual digital asset ads (in force 1 Apr 2022) requires a prominent risk disclaimer saying crypto products are unregulated and highly risky, in the caption and in the picture or video (secondary reports) [D11].
- None of this fixes the problem in 6.3. A disclosed ad for an online money game is still an ad for an online money game.

### 5.5 How faceless pages normally disclose, and what the rules say about it

| What pages do | Where it shows up | Verdict |
|---|---|---|
| Nothing | Garbage Day found very few Kalshi clipping posts disclosed (29 Jun 2026) [C1]. Adclear: 54% of crypto trading posts undisclosed [D12]. NAD flagged Instagram and X posts [C4]. | Breaks ASA, CMA and FTC expectations. This is the pattern regulators and plaintiffs are now attacking. |
| A partner tag or bio line only | Some Polymarket creators added "@polymarket partner" to their bios only after the WSJ asked questions [C2]. An X account that NAD flagged for Kalshi describes itself as a "Kalshi Partner" in its profile [C4]. | ASA: bio and tags do not count, each post must stand alone [D1]. |
| Platform label only (TikTok toggle, Instagram Paid partnership, YouTube tickbox, X label) | Standard practice | Helps, but ASA says it may not be enough alone and the FTC says no guarantee [D1][D9]. Use it plus text. |
| A tiny label | Sponsored posts on X carried a "paid partnership" tag in small print (NPR, 7 Jun 2026) [C5] | Weak. The test is clear and prominent. |
| "Ad" in the first line or first frame plus the platform label | Best practice | Meets the ASA, CMA and FTC tests if upfront and prominent [D1][D3][D9]. |

### 5.6 Who carries the risk when an agency runs a network of pages

- FTC: advertisers and their ad agencies and PR firms are the usual target, and they must monitor their network [D9].
- ASA: brand and publisher are both named in rulings [D1].
- The NACA lawsuit against Polymarket (filed 26 Jun 2026, DC) names the company, its CEO and its CMO. It alleges they controlled scripts and told clippers not to make videos feel like ads. These are allegations, not findings [C3].
- So the agency should keep its own paper trail: the brief it was given, the label rules it applied, and proof of each post's label.

### Sources for section 5

- [D1] ASA, "Recognising ads: Social media and influencer marketing". Page dated 6 Aug 2026. https://www.asa.org.uk/advice-online/recognising-ads-social-media.html
- [D2] CAP Code, section 2 (recognition of marketing communications). No date on page. https://www.asa.org.uk/type/non_broadcast/code_section/02.html
- [D3] CMA, "Social media endorsements: being transparent with your followers". Updated 3 Sep 2025. https://www.gov.uk/government/publications/social-media-endorsements-guide-for-influencers/social-media-endorsements-being-transparent-with-your-followers
- [D4] CMA, hidden ads principles for social media platforms. Updated 28 Aug 2025. https://www.gov.uk/government/publications/compliance-principles-for-social-media-platforms/hidden-ads-principles-for-social-media-platforms
- [D5] CMA press release, 7 Apr 2025. https://www.gov.uk/government/news/cma-to-boost-consumer-and-business-confidence-as-new-consumer-protection-regime-comes-into-force
- [D6] FCA FG24/1, "Finalised guidance on financial promotions on social media", Mar 2024. https://www.fca.org.uk/publication/finalised-guidance/fg24-1.pdf (paragraphs 1.6 to 1.9, 4.5, 4.7, 4.16 to 4.23)
- [D7] FCA FG23/3, cryptoasset financial promotions guidance. First published 2 Nov 2023. https://www.fca.org.uk/publication/finalised-guidance/fg23-3.pdf (paragraphs 2.70 and 2.71)
- [D8] FTC, "Disclosures 101 for Social Media Influencers". Nov 2019. https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
- [D9] FTC, "FTC's Endorsement Guides: What People Are Asking" (guides revised 2023; no page date). https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking
- [D10] FTC press release, 14 Aug 2024. https://www.ftc.gov/news-events/news/press-releases/2024/08/federal-trade-commission-announces-final-rule-banning-fake-reviews-testimonials . In force 21 Oct 2024 per the FTC Q&A (seen in search results, not opened): https://www.ftc.gov/business-guidance/resources/consumer-reviews-testimonials-rule-questions-answers
- [D11] India, secondary reports: Business Today, 21 Jan 2023, https://www.businesstoday.in/technology/news/story/influencers-take-note-centre-issues-new-social-media-regulations-with-fines-up-to-rs-50-lakh-366984-2023-01-21 ; The Quint on ASCI crypto disclaimer (Feb 2022), https://www.thequint.com/amp/story/tech-and-auto/tech-news/risky-disclaimer-asci-finally-issues-guidelines-for-advertising-crypto-nfts . Both seen in search results, not opened. Check the CCPA and ASCI documents before relying on exact figures.
- [D12] Fintech Times on the Adclear study, 24 Sep 2026. https://thefintechtimes.com/nine-in-10-crypto-influencer-posts-breach-fca-promotion-rules/
- [C1] to [C5]: see section 7.

## 6. Legal promotion rules where the audience might be

### 6.0 Start with Outcome's own list

Outcome's Terms (Section 3B) say these people are strictly prohibited from using the interface: users in the United States and its territories, Ontario, the United Kingdom, the UAE, Belgium and other EU states where the activity is not permitted, Singapore, Hong Kong, South Korea and China, plus sanctioned places and the citizens of those places wherever they are. India is not listed [L0].

- A post aimed at UK or US viewers promotes a service to people the service itself bans. Section 3N bans encouraging others to break the Terms, and Section 3E bans VPN workarounds [L0].
- The Terms describe the markets as prediction markets on price outcomes. Your brief mentions sports and esports as well. UNCLEAR whether sports or esports markets are live. If they are, the gambling analysis below gets stronger [L0].
- No date appears on the Terms page, so confirm with the client that this is the current version.
- I found no public licence or registration for Outcome. UNCLEAR; ask the client.

### 6.1 United Kingdom

Bottom line: both UK regulators say this kind of product is theirs (the FCA for crypto and stock price contracts, the Gambling Commission for sports contracts). Outcome has no UK licence that I can find, and its own Terms ban UK users. A UK-based agency promoting it to anyone who can see the posts takes on real criminal and civil risk.

Crypto and stock price contracts sit with the FCA. Its Perimeter Report (first published 26 Mar 2026, updated 16 Jul 2026) says the financial prediction-market products it has seen are binary options. Those stay under the permanent ban on selling, marketing and distributing binary options to retail consumers, in force since 2 Apr 2019 [UK1][UK2]. Anyone who communicates an invitation to invest "in the course of business" without FCA authorisation or approval may commit a criminal offence. The FCA says this can reach influencers even with no deal with the firm, and that being paid by a platform for views, or growing a following to win future deals, would likely count [D6]. Law firm summaries put the maximum at two years in prison under section 21 of the Financial Services and Markets Act (secondary) [UK9]. In April 2026 the FCA made 120 takedown requests to platforms and got a guilty plea from a TV personality for illegal promotions [UK4]. Sports and esports contracts sit with the Gambling Commission. On 4 Feb 2026 it said a prediction market launching in Great Britain would not be able to call itself non-gambling and would likely need a betting intermediary licence, that unlicensed operators should not target or transact with GB consumers, and that there are criminal offences for operating without a licence [UK5]. Under section 330 of the Gambling Act 2005 it is an offence to advertise unlawful gambling, with up to 51 weeks in prison and/or a level 5 fine on summary conviction [UK6]. Section 333 catches online advertising that is intended to come to the attention of people in Great Britain, or is made available where it is likely to be accessed by them [UK7]. A public page run from the UK is reachable by UK viewers, so "we are not targeting the UK" is a weak defence. The hidden-ad rules in section 5 apply on top. UNCLEAR: I found no reported prosecution of a clipper or affiliate for promoting a prediction market in the UK, and how the Commission would treat a page aimed only at non-UK viewers is untested. The FCA confirmed talks with Polymarket and Kalshi on 6 Oct 2026, but no rule has changed [UK8].

### 6.1a The FCA cryptoasset promotions regime in short

- In force since 8 Oct 2023. It covers promotions of "qualifying cryptoassets" to UK consumers, including by overseas firms, and applies on social media such as YouTube, Reddit, X, Discord and Telegram [D7][UK10].
- Promotions must come from, or be approved by, an FCA-authorised firm, or come from an FCA-registered cryptoasset business using an exemption. Unauthorised influencers who promote without approval may commit an offence [D6][D7].
- Required: promotions that are fair, clear and not misleading, a clear risk warning and risk summary, and no incentives to invest such as refer-a-friend or new-joiner bonuses. Paid relationships should be disclosed [UK10][D7].
- The prescribed risk warning starts "Don't invest unless you're prepared to lose all the money you invest" (FCA Handbook COBS 4.12A, seen in search results, so check the current wording) [UK11].
- The FCA published final rules for the wider UK crypto regime on 30 Jun 2026, with the new regime starting in October 2027 (search-result summary, UNCLEAR) [UK12].
- Does this regime apply to Outcome? UNCLEAR. Outcome's contracts are Yes/No contracts on prices, and the FCA's current view is that financial ones are binary options [UK1]. The social media rules in FG24/1 apply either way [D6].

### 6.2 United States

Bottom line: nobody can yet say whether sports and other event contracts are federal derivatives or state sports betting. States are suing and charging platforms. The live risk for promoters is deceptive-marketing and disclosure law. Outcome is offshore, bans US users in its Terms, and I found no CFTC registration for it.

On 9 Oct 2026 the CFTC proposed to put event contracts on sports, politics, culture and weather into the swap definition, and issued an interim rule saying casino-style gambling is not a swap [US1][US2]. Neither is final. Courts are split: the Third Circuit sided with Kalshi against New Jersey in April 2026, while the Ninth Circuit (28 Aug 2026, Nevada) and the Sixth Circuit (25 Sep 2026, Ohio and Tennessee) held that states can regulate Kalshi's sports contracts, and the Supreme Court may be asked to step in [US3][US4]. States are acting. Kentucky's attorney general sued Kalshi and Polymarket on 17 Jun 2026, including a claim that Polymarket's ads gave a false impression it could offer sports wagering there [US6]. Missouri's attorney general sent cease-and-desist letters to Polymarket, Kalshi and others on 18 Sep 2026 [US5]. New York's attorney general sued Coinbase and Gemini on 21 Apr 2026, and New York's gaming commission had sent Kalshi a cease-and-desist letter in Oct 2025 [US7]. Minnesota passed a law in May 2026 that reports say also criminalises advertising prediction markets (statute text not read, UNCLEAR). A federal judge blocked it on 27 Jul 2026, but the order protects only exchanges registered with the CFTC [US8][US9]. The New York City Council opened a probe of prediction-market marketing on 12 Aug 2026 [US10]. These cases mostly involve platforms that are CFTC-registered or partner with registered exchanges. Outcome is an offshore front end on Hyperliquid, its Terms exclude US users, and I found no CFTC registration for it (UNCLEAR, ask the client). So the preemption arguments registered platforms use may not help it. A US-aimed promoter would face state gambling law, state consumer protection law, FTC endorsement rules and private suits such as NACA v. Polymarket (filed 26 Jun 2026 in DC) [C3]. UNCLEAR: I found no state action naming an individual influencer or clipper so far. The live risk to promoters is deceptive-marketing and disclosure law, enforced by attorneys general, city governments and private plaintiffs more than by the FTC.

### 6.3 India

Bottom line: India bans advertising online money games, and the law covers the people who make the ad, not only the platform. Authorities have already blocked Polymarket. Whether Outcome counts is untested, but the definition is broad.

The Promotion and Regulation of Online Gaming Act 2025 (Act 32 of 2025, assent 22 Aug 2025) defines an "online money game" as an online game, whether based on skill, chance or both, where a user pays fees or deposits money or other stakes in expectation of winning money or other enrichment. E-sports are excluded (section 2(1)(g)) [IN1]. Section 6 says no person shall make, cause to be made, aid, abet, induce or otherwise be involved in making any advertisement, in any media including electronic, that directly or indirectly promotes or induces anyone to play an online money game. Section 9(2) sets the penalty for advertising at up to two years in prison and/or a fine up to Rs 50 lakh, with higher minimums for repeat offences. Offering the games is a cognisable, non-bailable offence (sections 5 and 10), and the Act applies to services operated from outside India (section 1(2)) [IN1]. A MeitY letter dated 25 Apr 2026 warned VPN providers about blocked prediction-market platforms, and a MeitY blocking order against Polymarket had been issued by 21 May 2026 [IN2][IN3]. A MeitY official told ThePrint that online money games are prohibited including offering, advertising and the related financial transactions [IN2]. Search-result summaries (not confirmed in a primary source, so UNCLEAR) say the Online Gaming Rules took effect on 1 May 2026 and that Kalshi barred Indian users on 17 Jun 2026 [IN4]. Whether Outcome's markets count as an "online money game" is UNCLEAR: the definition is broad and Indian authorities have treated prediction markets that way, but no Indian source I found discusses Outcome or crypto price contracts specifically. Anyone who makes the ads in India, for example an editor working from India, may be personally exposed even if the audience is elsewhere. UNCLEAR, and a question for Indian counsel. TikTok has been blocked in India since 2020 and TikTok said in Aug 2025 that the ban still stands, so TikTok is not an India route anyway [IN5]. Meta lists India as an unsupported market for gambling ads [M4]. Outcome's Terms do not exclude India [L0], but that does not make promotion there lawful.

### 6.4 Other places

Outcome's Terms also exclude the UAE, Singapore, Hong Kong, South Korea, China, Ontario and Belgium and other EU states where the activity is not permitted [L0]. Ireland is "not allowed" for gambling and financial branded content on TikTok [T1]. I did not research other countries' law. UNCLEAR.

### Sources for section 6

- [L0] Outcome Terms of Service. No date on page. https://outcome.xyz/terms . Read via proxy. Outcome docs (HIP-4 deployer, uses "trade" not "bet"): https://docs.outcome.xyz
- [UK1] FCA Perimeter Report, section on prediction markets. First published 26 Mar 2026, last updated 16 Jul 2026. https://www.fca.org.uk/publications/corporate-documents/fca-perimeter-report
- [UK2] FCA PS19/11, ban on sale, marketing and distribution of binary options to retail consumers, rules in force 2 Apr 2019. https://www.fca.org.uk/publications/policy-statements/ps19-11-product-intervention-measures-retail-binary-options
- [UK3] is the same document as [D6] (FCA FG24/1), listed under section 5.
- [UK4] FCA press release, 24 Apr 2026. https://www.fca.org.uk/news/press-releases/fca-spearheads-global-action-stop-illegal-finfluencers
- [UK5] UK Gambling Commission blog "Prediction markets: here's what you need to know", 4 Feb 2026. https://www.gamblingcommission.gov.uk/blog/post/prediction-markets-heres-what-you-need-to-know
- [UK6] Gambling Act 2005 section 330. https://www.legislation.gov.uk/ukpga/2005/19/section/330 (read via proxy)
- [UK7] Gambling Act 2005 section 333, as amended in force 1 Nov 2014. https://www.legislation.gov.uk/ukpga/2005/19/section/333 (read via proxy)
- [UK8] Yahoo Finance, 7 Oct 2026 (FCA talks confirmed 6 Oct 2026). https://finance.yahoo.com/markets/options/articles/polymarket-kalshi-coming-uk-fca-112215545.html
- [UK9] Freeths, 29 Jun 2023, on the FCA crypto promotion rules and the section 21 offence (secondary, seen in search results, not opened). https://www.freeths.co.uk/2023/06/29/financial-conduct-authority-introduces-new-financial-promotions-rules-for-cryptocurrencies/
- [UK10] ASA, "Financial products and services: Cryptoassets", page dated 25 Mar 2026 (FCA took over technical regulation of qualifying cryptoasset ads from 8 Oct 2023; risk warnings, risk summaries, ban on refer-a-friend and new-joiner incentives). https://www.asa.org.uk/advice-online/financial-products-and-services-cryptoassets.html . Also FCA FG23/3 page, first published 2 Nov 2023, regime supervised since 8 Oct 2023: https://www.fca.org.uk/publications/fg23-3-finalised-non-handbook-guidance-cryptoasset-financial-promotions (see [D7] for the PDF, paragraphs 2.70 and 2.71).
- [UK11] FCA Handbook, COBS 4.12A (promotion of restricted mass market investments), seen in search results, not opened. https://handbook.fca.org.uk/handbook/cobs4/cobs4s17
- [UK12] FCA, overview of its cryptoassets regime policy statements (final rules reported as published 30 Jun 2026, start October 2027), seen in search results, not opened. https://www.fca.org.uk/publications/policy-statements/cryptoasset-regime
- [US1] CFTC press release 9310-26, 9 Oct 2026 (proposed rule on event contracts and the swap definition). https://www.cftc.gov/PressRoom/PressReleases/9310-26
- [US2] CFTC press release 9309-26, 9 Oct 2026 (interim final rule excluding casino-style gambling). https://www.cftc.gov/PressRoom/PressReleases/9309-26
- [US3] US Court of Appeals for the Ninth Circuit, KalshiEX LLC v. Assad, No. 25-7516, filed 28 Aug 2026. https://cdn.ca9.uscourts.gov/datastore/opinions/2026/08/28/25-7516.pdf
- [US4] Al Jazeera, 25 Sep 2026 (Sixth Circuit; Third Circuit and Ninth Circuit context). https://www.aljazeera.com/news/2026/9/25/us-court-rules-against-kalshi-says-states-can-regulate-prediction-markets
- [US5] KCTV5, 18 Sep 2026 (Missouri attorney general). https://www.kctv5.com/2026/09/18/missouri-ag-sends-cease-desist-letters-prediction-market-operators/
- [US6] LEX18 on Kentucky attorney general suits (image file name refers to 17 Jun 2026; page shows no date). https://www.lex18.com/news/covering-kentucky/kentucky-attorney-general-sues-kalshi-polymarket-and-vgw-over-illegal-gambling-claims . The Attorney General's filed complaint is named with the date 2026.06.17 but returned a 403 when I tried to open it: https://www.ag.ky.gov/Press%20Release%20Attachments/2026.06.17%20As%20Filed%20KYOAG%20v.%20Kalshi%20et%20al%20-%20Final.pdf
- [US7] Insurance Journal, 22 Apr 2026 (New York attorney general suits against Coinbase and Gemini filed 21 Apr 2026; seen in search results, not opened). https://amp.insurancejournal.com/news/east/2026/04/22/866783.htm
- [US8] NBC News, 27 Jul 2026 (Minnesota law blocked). https://www.nbcnews.com/tech/tech-news/minnesota-prediction-market-ban-blocked-federal-judge-rcna589494
- [US9] Keil Defense summary of Minnesota law, and ESPN (both seen in search results, not opened; they say the law covers advertising). https://keildefense.com/blog/minnesota-prediction-market-felony-law-2026.html ; https://www.espn.com/espn/betting/story/_/id/48818821/trump-sues-minnesota-block-law-banning-prediction-markets
- [US10] CBS News, 12 Aug 2026 (NYC Council probe). https://www.cbsnews.com/news/nyc-investigates-polymarket-kalshi-prediction-markets/
- [IN1] Promotion and Regulation of Online Gaming Act, 2025 (Act 32 of 2025), text on the MeitY site. https://www.meity.gov.in/static/uploads/2025/10/8a7f103cefc68ed8aaa2ebc9a2ed7c13.pdf . Read via proxy. (The cover page gives 22.08.2025; a footnote gives a different Gazette date, so the exact notification date is UNCLEAR.)
- [IN2] ThePrint, 21 May 2026. https://theprint.in/india/governance/polymarket-kalshi-india-prediction-markets/2937547/
- [IN3] Yogonet, 22 May 2026. https://www.yogonet.com/international/news/2026/05/22/121400-india-blocks-access-to-polymarket-amid-prediction-markets-crackdown
- [IN4] CoinDesk, 22 May 2026, and Complete iGaming on Kalshi restricting India (both seen in search results, not opened). https://www.coindesk.com/markets/2026/05/22/india-cracks-down-on-prediction-markets-polymarket-goes-dark-kalshi-could-be-next ; https://completeigaming.com/kalshi-restricted-in-india-after-warnings-followed-by-country-wide-block/
- [IN5] TechCrunch, 22 Aug 2025, TikTok denies India comeback (seen in search results, not opened; no 2026 source found). https://techcrunch.com/2025/08/22/tiktok-denies-india-comeback-after-reports-of-website-going-live
- [M4], [T1], [D6], [C3]: see their own sections.

## 7. How the big prediction markets and their campaigns word posts, disclose, and what styles they use

### 7.1 How the companies word things on their own sites

- Kalshi's homepage calls itself a prediction market "for trading the future". Buttons and menus use "Predict", "Trade" and "Markets". The word "bet" does not appear on the page. The footer says trading involves risk and may not suit everyone, members can lose their entry cost including fees, past results are not necessarily indicative of future results, and Kalshi is subject to US oversight by the CFTC [C6].
- Polymarket's homepage calls itself the world's largest prediction market and tells US visitors to "trade" on polymarket.us. It does not use "bet". Its footer says trading involves substantial risk of loss and that the international platform is not regulated by the CFTC [C6].
- Other brands: a search-result summary of a Gambling Insider article (21 Sep 2026; the page returned a 403 when I tried to open it) says DraftKings, Novig and Polymarket campaigns already use "trade" in place of "bet". UNCLEAR. https://www.gamblinginsider.com/news/195651/tiktoks-prediction-market-ad-rules-make-trading-vs-betting-more-than-branding
- Outcome's homepage says "Trade to earn" for a rewards programme and "Predict the outcome". Its docs use "trade" and call contracts fully collateralised binary instruments with no leverage, and show no formal risk warning on that page. Its Terms warn that a position can fall to zero and that you can lose a substantial portion or all of your funds (3H, 3I) [L0].
- My view, not a source: do not lift "Trade to earn" into paid clips without legal review, because "earn" reads as a profit claim.
- Do not copy regulatory claims such as "regulated by the CFTC" or "legal in all 50 states" [C6][T12]. Those claims come from registered US exchanges. I found nothing showing Outcome is registered anywhere. UNCLEAR.

### 7.2 How the campaigns were actually run (and what went wrong)

Kalshi clipping through FindClout (Garbage Day investigation, 29 Jun 2026) [C1]:
- Clippers add a Kalshi-style live odds chart banner to sports and meme clips. The tutorial says to make the chart move with the clip, keep the banner above the bottom 30% of the frame, use two-option markets only, and keep captions off the banner. Pay is listed as $130 per million views. Payouts go through PayPal, and screenshots show up to $2,000.
- The tutorial names TikTok and Reels as targets. Garbage Day says Instagram is the main target, with about 50 meme pages reaching US and UK Gen Z audiences.
- FindClout's terms put the duty to mark posts as ads on the clipper, but the reporters found very few posts disclosed as ads. The tutorial itself lists no disclosure rule.
- Clippers were told the banner does not have to match the actual market. For a protein brand they were told to feature it naturally without tagging it.
- After the reporters made contact, public campaign pages started redirecting to the homepage, and the Discord moved to moderator approval.

Polymarket (WSJ investigation reported by The Block on 21 Jun 2026; NACA lawsuit described by Kelley Drye on 28 Jun 2026 and KTS Law on 8 Jul 2026) [C2][C3]:
- The WSJ reviewed 1,105 videos from 10 creators posted between Dec 2025 and mid-May 2026. Creators filmed fake bets and fake wins on near-identical copies of the Polymarket site. In 118 videos creators celebrated nearly $900,000 in invented winnings. The same bets would have lost more than $166,000. None of the roughly $1.9 million in wagers shown were real.
- Creators were paid about $2,000 to $3,000 a month, were told not to disclose the arrangement, and worked from bullet-point scripts that Polymarket reviewed before posting.
- Clippers were paid only if at least 60% of their audience was in the US. Polymarket paid for at least 19 videos about trading on inside information. The clips drew more than 140 million views across TikTok, YouTube and Instagram (Tubular figures).
- The NACA complaint (filed 26 Jun 2026 in DC under the Consumer Protection Procedures Act, against the company, its CEO and its CMO) alleges clippers earned $1 per 1,000 views, were told not to make videos feel like ads, were barred from putting "Polymarket" or "poly" in account names, and were told to spend about three days "warming up" new accounts. These are allegations, not findings.
- Polymarket said it is auditing its promotional content.

Kalshi and Polymarket creator rules (NPR via KPBS, 7 Jun 2026) [C5]:
- Both offered creators up to $500 per post, according to former employees.
- Kalshi told paid influencers to delete posts questioning a Los Angeles election result and confirmed that affiliates may not question election integrity. Polymarket told creators about its content guidelines.
- Paid posts on X carried a "paid partnership" tag in tiny font.

Kalshi's TikTok creator ads (Media Matters, 30 Mar 2026) [T12]:
- Ads promised a "money hack", showed claims such as "$761 last night", framed weather markets as a "side hustle", and said it was "legal in all 50 states". Kalshi said it no longer works with those influencers.

Regulator reaction [C4]:
- NAD (8 Jun 2026) examined whether Kalshi's links with influencers and affiliates were clearly and conspicuously disclosed and whether Kalshi ensures compliance with the FTC Endorsement Guides. Kalshi declined to take part. NAD said it would refer the matter to regulators including state attorneys general, and to the platforms where the ads appeared. MediaPost says the FTC was included; Kelley Drye notes the NAD release did not name the FTC. UNCLEAR.
- MediaPost says NAD found Instagram and X posts that potentially lacked disclosures. Kalshi's spokesperson said it complies with all applicable advertising laws and has strengthened its communication with influencers.
- Direction of travel (opinion piece, City Journal, 23 Jul 2026): the authors want the CFTC to require paid-partnership disclosure in every ad, ban guaranteed-winnings promises and fabricated or simulated winnings, and extend broker registration to anyone paid to drive traffic to a prediction market. This is a proposal, not law [C7].

### 7.3 Which styles "avoid takedowns"?

- I found no source showing that any content style avoids takedowns by design, and no public count of prediction-market clips removed by TikTok, Instagram, YouTube or X. UNCLEAR.
- What the record does show: the big styles (odds-banner sports clips, meme pages, creator testimonials) have been challenged by journalists, regulators, courts and brands themselves. Brands pulled content for election-denial posts and changed practice when X changed its rules [C5][X3]. So "has not been taken down" does not mean "safe".

### 7.4 Content styles, with a risk read

| Style | Seen in | Risk | Reason |
|---|---|---|---|
| Live odds-chart banner on sports or meme clips | Kalshi clipping via FindClout [C1] | High | The banner can be simulated and not match a real market. Odds-style display is what TikTok's ad rules exclude [T8]. Disclosure is often missing. |
| "I made $X" testimonial or screen recording of a win | Kalshi TikTok ads [T12]; Polymarket creators [C2] | Very high | Fake or cherry-picked wins sit at the centre of the Polymarket lawsuit. Meta removes guaranteed and get-rich claims [M2]. FTC testimonial rules apply [D9][D10]. |
| Mock-up or replica trading screen | Polymarket (alleged) [C2][C3] | Never do | Alleged fabrication drove the lawsuit and press storm. |
| Meme page that hides the commercial tie | Garbage Day [C1]; NACA complaint [C3] | High | Hidden ads breach ASA, CMA and FTC rules [D1][D3][D9]. |
| Brand-new accounts "warmed up" to look organic | NACA complaint [C3] | High | Alleged sockpuppet tactic. Buying or faking influence is also covered by the FTC rule on fake indicators [D10]. |
| Creator or celebrity post with a clear label and permissions in place | Not measured. Label tools exist on every platform [T5][M3][Y6][X4]. Paid creator posts for both brands were reported on X [C5]. | Medium | Fine in principle if labelled upfront and the brand has the platform permissions. The reported X posts used a tiny tag, which is the weak version. |
| Explainer: what a market price says about an event, with real data, a date stamp, a risk line and no call to trade | No source measures this style. My suggestion. | Lower | TikTok allows financial education [T2]. It is still an ad if paid, and still has the audience and licensing problems in section 6. |

### Sources for section 7

- [C1] Garbage Day, "We spent a month hiding in a Kalshi clipping Discord", 29 Jun 2026. https://www.garbageday.email/p/we-spent-a-month-hiding-in-a-kalshi-clipping-discord . FindClout Kalshi tutorial (no date): https://app.findclout.com/kalshi/tutorial
- [C2] The Block, 21 Jun 2026, reporting the Wall Street Journal investigation. https://www.theblock.co/news/ecosystems/2026-06-21-polymarket-paid-creators-to-stage-fake-winning-bets-on-dummy-sites-wsj-405471 (the WSJ article itself was not opened)
- [C3] Kelley Drye, 28 Jun 2026, https://www.kelleydrye.com/viewpoints/blogs/ad-law-access/all-bets-are-off-as-polymarket-faces-lawsuit-over-influencer-campaigns ; KTS Law, 8 Jul 2026, https://ktslaw.com/en/Blog/Kilpatrick-Ad-Vantage/2026/7/Betting-on-Deception-Polymarkets-Influencer-Campaign-Draws-Lawsuit ; Ifrah Law, 11 Jun 2026, https://www.ifrahlaw.com/ftc-beat/11228/ . The $1 per 1,000 views, "Do NOT make the videos feel like ads" and "poly" account-name details are from Kelley Drye and from a Deseret News report of the complaint (seen in search results, not opened).
- [C4] BBB National Programs, NAD Case 7573, 8 Jun 2026, https://bbbprograms.org/media/newsroom/decisions/kalshi ; MediaPost, 8 Jun 2026, https://www.mediapost.com/publications/article/415623/nad-refers-kalshi-to-ftc-over-influencer-ads.html ; Kelley Drye, 9 Jun 2026, https://www.kelleydrye.com/viewpoints/blogs/ad-law-access/nad-investigates-kalshis-influencer-practices
- [C5] NPR, 7 Jun 2026, read as the KPBS copy: https://www.kpbs.org/news/politics/2026/06/07/kalshi-and-polymarket-crack-down-on-paid-influencers-claiming-election-fraud
- [C6] Kalshi homepage https://kalshi.com and Polymarket homepage https://polymarket.com , both read via proxy on 13 Oct 2026 (live pages, no publication date).
- [C7] City Journal, 23 Jul 2026 (opinion). https://www.city-journal.org/article/prediction-market-ads-polymarket-kalshi
- [T12], [X3], [M2], [T2], [T8], [D1], [D3], [D9], [D10], [L0]: see their own sections.

## 8. Final checklist for faceless Outcome posts (15 lines)

1. DO get the client's written list of allowed countries before any post. Outcome's Terms ban the US, UK, UAE and others [L0]. DON'T aim at, write for or hashtag those audiences, and never hint at a VPN.
2. DON'T aim at India without Indian legal advice. Section 6 of the Online Gaming Act covers anyone who makes or causes ads for online money games [IN1].
3. DO label every paid or per-view post with a plain "Ad" in the first line or first frame AND the platform tool: TikTok content disclosure toggle, Instagram Paid partnership, YouTube paid promotion box, X Paid Partnership label [D1][D3][D9][T5][M3][Y6][X4]. DON'T rely on a bio line, a partner tag or a pile of hashtags.
4. DO ask Outcome in writing about platform permissions. TikTok: explicit permission, Registered Business Account, TikTok One [T1]. Meta: written pre-authorization for real money gambling and crypto branded content [M3]. YouTube: whether Google counts Outcome as a certified or uncertified gambling site [Y1]. DON'T post paid content where nobody has checked. UNCLEAR how each platform will classify Outcome.
5. DON'T fake or show results: no "I made $X", no winnings screenshots, no mock-up trading screens, no odds banners that do not match a real live market [C1][C2][C3][M2].
6. DON'T promise or imply profit, safety or legality. Skip "guaranteed", "risk-free", "can't lose", "free money", "passive income", "side hustle" and "make $X a day". Skip "regulated", "licensed" and "legal in [place]" unless the client proves it in writing [M2][Y1][T2][T12].
7. DO keep the client word rule: trade, market, contract, Yes/No price, chance in percent. DON'T use bet, betting, wager, gamble, casino, sportsbook or parlay, or odds formats such as +150 [T8]. The words do not protect you in law [UK5][US3].
8. DO put a short risk line in the caption and on the last frame, for example "Trading involves risk. You can lose all the money you put in. 18+. Not financial advice. Not available in [list]." Wording is for legal review [C6][L0]. DON'T treat the line as a cure for a misleading post.
9. DO keep visuals plain: a real screen with date and time, no cash piles, chips, dice, slot imagery, celebration effects or countdown pressure. DON'T show or suggest anyone under 18 [T3][M1].
10. DO make links boring. One link in bio where the platform allows it (TikTok needs 1,000 followers or a Verified Business Account [T7]; Instagram allows up to 5 [M11]). DON'T put links in comments or captions, don't use cloaked or shortened links, and on YouTube don't show, say or link Outcome's URL or logo until the client confirms how YouTube treats it [Y1][T2].
11. DO run each page as one honest identity. If it is a paid page, say so in the bio. DON'T pose as an official Outcome account [M2]. DON'T buy views, likes or followers [D10][M7]. DON'T build "warmed-up" sockpuppet networks [C3].
12. DO add real edits to clips: new voiceover or commentary, new captions, an original angle. DON'T repost raw clips or clips with another app's watermark [M7][M10][T3][Y9].
13. DO label realistic AI visuals. DON'T use an AI "analyst" or "expert" persona to give finance tips [T3][M7][Y9].
14. DON'T go near election-result or election-fraud claims, insider-trading or "leaked info" angles, or anything aimed at minors [C5][C2][T3].
15. DO keep a paper trail and watch for warnings: save the brief, the label rules and a screenshot of each post's label; check TikTok analytics and Instagram Account Status weekly [T6][M8]. If a platform, regulator or lawyer contacts you, stop posting and tell the client the same day [D9].

## 9. Open questions and limits

Questions for the client or a lawyer:
1. Which countries does Outcome actually want, is the Terms page current, and does Outcome geo-block the Prohibited Jurisdictions? [L0]
2. Is Outcome licensed or registered anywhere (CFTC, FCA, UK Gambling Commission, elsewhere)? Are sports and esports markets live, or only price markets? [L0][UK5]
3. Has Outcome applied for or received TikTok, Meta or YouTube permission, and how did each platform classify it (gambling, financial services, binary options, or neither)? [T1][M3][Y1]
4. India: does section 6 of the Online Gaming Act reach editors working from India, and is Outcome an "online money game"? Needs Indian counsel [IN1].
5. UK: is a public page not aimed at the UK still "advertising" under Gambling Act sections 330 and 333, and does per-view pay make a clipper someone acting "in the course of business" for FCA purposes? [UK6][UK7][D6]
6. TikTok: how does the "market where it was originally posted" rule pick the market (account region or location)? [T1]

What I could not read, so treat as UNCLEAR:
- TikTok's live Community Guidelines pages (script-built) and the full 2026H2 version (only secondary reports).
- X's help center and ad policy pages (bot-check block).
- Facebook's own Branded Content Policies page (login wall; used the Instagram copy).
- The TeamYouTube thread body (used a trade-press mirror).
- Original WSJ and Politico articles, the Kentucky complaint PDF, a US Senate letter to Polymarket dated 26 Aug 2026 (Padilla), Rolling Stone and several law-firm pages (blocked or paywalled; I did not use a paywall bypass).
- Whether any platform removed prediction-market clips in 2025 to 2026. No public data found.

This area moves fast. Re-check before launch: the CFTC rules (comment periods running from Oct 2026), any Supreme Court step on the circuit split, Minnesota and Kentucky cases, TikTok's 2026H2 guidelines, Meta's reposts rule, X's paid partnership policy, the FCA talks with prediction-market operators, and India's blocking orders.
