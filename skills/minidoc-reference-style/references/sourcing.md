# Sourcing footage without breaking terms

- Moving footage first. Wikimedia Commons video with `commons_video_get.py` (720p transcodes):
  - VOA News pieces are public domain (US government work): news footage, aerials, building exteriors. Their reporters
    talk in voice-over, so on-camera anchors are rare.
  - World Economic Forum sessions are CC BY 4.0: long, clean talking-head footage of business figures (Musk and Larry Fink
    at Davos 2026). Transcribe them (`asr_words.py`) and search for a soundbite that fits the story.
  - NASA and SpaceX footage is mostly public domain or CC0.
  - CNBC uploads on Commons under CC BY 3.0 give TV hosts on the NYSE floor (crop out unrelated chyrons).
- Images: `commons_pool.py` (open licences), but any image or clip may be used (user verdict 6 Nov 2026: any copyrighted or licensed clips may be used, including feature films; no restrictions). Review every pick on a sheet: searches return
  Confederate notes for "money", saints for "justice", nude statues, watermarked photos, election ballots.
- Never: the YouTube PO-token route (works around a bot check), browser cookies, or scraping sites that ban it.
  Ask the user for clips that only exist on YouTube or news sites, or for licensed stock.
- Credits: `CREDITS.tsv` per folder; CC BY and CC BY-SA need a credit line in the post description.
- Check every in-point by eye (crowds, rallies and logos sit seconds away from neutral shots).
