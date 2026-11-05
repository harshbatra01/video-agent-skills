"""Write headlines.json from the research hand-back and add the headline notes to update_page.py."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
R = [  # moment (+ where it fits), outlet, date, headline, url, checked on the live page
    ('1998 illness: Secret weapon', 'BBC News', '4 Sep 1998', 'Virus wrecks Radcliffe medal bid', 'http://news.bbc.co.uk/2/hi/sport/164709.stm', True),
    ('2003 record: Ran professionally, held record', 'BBC Sport', '13 Apr 2003', 'Radcliffe smashes record', 'http://news.bbc.co.uk/sport2/hi/athletics/london_marathon_2003/2943913.stm', True),
    ('2003 record', 'The Guardian', '14 Apr 2003', 'Record breaker Radcliffe makes the men look soft', 'https://www.theguardian.com/sport/2003/apr/14/athletics.duncanmackay', True),
    ('Athens 2004', 'BBC Sport', '22 Aug 2004', 'Marathon agony for Radcliffe', 'http://news.bbc.co.uk/sport2/hi/olympics_2004/athletics/3589138.stm', True),
    ('Athens 2004', 'BBC Sport', '22 Aug 2004', 'Where did it go wrong for Paula?', 'http://news.bbc.co.uk/sport2/hi/olympics_2004/athletics/3589436.stm', True),
    ('Athens 2004', 'The Guardian', '23 Aug 2004', 'Tearful Radcliffe fails to finish marathon', 'https://www.theguardian.com/uk/2004/aug/23/athensolympics2004.athletics', True),
    ('Athens 2004', 'The Independent', '23 Aug 2004', 'Crying shame for Radcliffe as marathon dream dies in heat', 'https://www.independent.co.uk/sport/olympics/crying-shame-for-radcliffe-as-marathon-dream-dies-in-heat-557520.html', True),
    ('NYC 2004 comeback: I\'m 52 ("at 30")', 'BBC Sport', '7 Nov 2004', 'Radcliffe enjoys winning comeback', 'http://news.bbc.co.uk/sport2/hi/athletics/3990701.stm', True),
    ('NYC 2004 comeback', 'BBC Sport', '8 Nov 2004', 'Radcliffe win eases Athens agony', 'http://news.bbc.co.uk/sport2/hi/athletics/3990909.stm', True),
    ('2000 World Cross (not 1998)', 'The Independent', '19 Mar 2000', 'Radcliffe isrun ragged heat', 'https://www.independent.co.uk/sport/general/radcliffe-isrun-ragged-heat-283638.html', True),
    ('1998 World Cross (about the winner)', 'The Independent', '22 Mar 1998', "Athletics: O'Sullivan on top of the world", 'https://www.independent.co.uk/sport/athletics-o-sullivan-on-top-of-the-world-1151743.html', True),
    ('2003 record', 'The Guardian', '14 Apr 2003', "Radcliffe's million dollar marathon", 'https://www.theguardian.com/uk/2003/apr/14/athletics.sport', False),
    ('NYC 2004 comeback', 'The New York Times', '8 Nov 2004', 'Radcliffe Outruns the Field and the Memories of Athens', 'https://www.nytimes.com/2004/11/08/sports/radcliffe-outruns-the-field-and-the-memories-of-athens.html', False),
    ('NYC 2004 comeback', 'CNN', '7 Nov 2004', 'Radcliffe in New York marathon win', 'https://edition.cnn.com/2004/SPORT/11/07/marathon.newyork/', False),
    ('Helsinki 2005 world title', 'BBC Sport', 'Aug 2005', 'Radcliffe races to world victory', 'http://news.bbc.co.uk/sport2/hi/athletics/4150694.stm', False),
    ('NYC 2007, after her baby', 'BBC Sport', 'Nov 2007', 'Radcliffe storms to New York win', 'http://news.bbc.co.uk/sport2/hi/athletics/7077867.stm', False),
    ('NYC 2007, after her baby', 'ESPN', 'Nov 2007', 'Radcliffe outlasts Wami, Lel kicks to New York City Marathon win', 'https://www.espn.co.uk/olympics/trackandfield/news/story?id=3094342', False),
    ('NYC 2007, after her baby', 'NBC News', 'Nov 2007', "Marathon mom's win sparks exercise debate", 'https://www.nbcnews.com/health/health-news/marathon-moms-win-sparks-exercise-debate-flna1C9473178', False),
    ('2015 farewell: Ran professionally ("20 years")', 'The Guardian', '14 Jan 2015', 'Paula Radcliffe to end glorious marathon career at London race in April', 'https://www.theguardian.com/sport/2015/jan/14/paula-radcliffe-end-marathon-career-london-april', False),
    ('2015 farewell', 'The Guardian', '24 Apr 2015', "'Paula Radcliffe would rather have fallen off the treadmill than stop'", 'https://www.theguardian.com/sport/2015/apr/24/paula-radcliffe-london-marathon-ends-career', False),
    ('2019 record falls: Ran professionally ("16 years")', 'Sky Sports', 'Oct 2019', "Chicago Marathon: Kenya's Brigid Kosgei breaks Paula Radcliffe's 16-year-old women's world record", 'https://www.skysports.com/more-sports/athletics/news/29175/11834341/chicago-marathon-kenyas-brigid-kosgei-breaks-paula-radcliffes-16-year-old-womens-marathon-world-record', False),
    ('2019 record falls', 'Guinness World Records', 'Oct 2019', "Brigid Kosgei smashes Paula Radcliffe's 16-year marathon record", 'https://www.guinnessworldrecords.com/news/2019/10/brigid-kosgei-sets-new-record-for-womens-fastest-marathon-595061', False),
    ('Injury, 2004', 'BBC Sport', '2004', 'Radcliffe reveals trauma', 'http://news.bbc.co.uk/sport2/hi/athletics/3657890.stm', False),
    ('Longevity: the record', 'The Guardian', '20 Apr 2013', "Paula Radcliffe recalls her 'impossible' London marathon record run", 'https://www.theguardian.com/sport/2013/apr/20/paula-radcliffe-london-marathon-record', False),
    ('Longevity: the record', 'The Guardian', '10 Nov 2011', 'Paula Radcliffe keeps her marathon world record in IAAF about-turn', 'https://www.theguardian.com/sport/2011/nov/10/paula-radcliffe-world-marathon-record', False),
]
json.dump([dict(moment=m, outlet=o, date=d, headline=h, url=u, verified=v) for m, o, d, h, u, v in R],
          open(os.path.join(HERE, 'headlines.json'), 'w', encoding='utf-8'), indent=0)

p = os.path.join(HERE, 'update_page.py')
if not os.path.exists(p):
    # Kit copy (14 Oct 2026): update_page.py was damaged in transcript recovery and is not shipped, so only
    # headlines.json is written. The headline list above is the useful part (11 checked word for word on the live page).
    print('headlines', len(R), '-> headlines.json; update_page.py is not in this kit, page notes skipped')
    raise SystemExit(0)
s = open(p, encoding='utf-8').read()
old ='  <p class="note">Rule we keep: only headlines that really ran, word for word, with the outlet and date.</p>\n  %s\n</section>'
if old in s:
    new = ('  <p class="note">Rule we keep: only headlines that really ran, word for word, with the outlet and date. '
           'The first 11 were checked on the live page; the rest are search titles only, so check them on the page before using.</p>\n  %s\n'
           '  <p class="note">Strongest for us: "Virus wrecks Radcliffe medal bid" (Secret weapon, 1998), "Radcliffe smashes record" (2003, has a photo), '
           '"Marathon agony for Radcliffe" and "Radcliffe win eases Athens agony" (the fall and the comeback). Screenshot tips: old BBC pages show a small '
           'error line at the top, crop it; on the Guardian click "No, thank you" on the cookie banner first. One live headline really reads "isrun" (typo on the page).</p>\n</section>')
    s = s.replace(old, new)
s = s.replace("""a(E(h['url']), 'open') + ('' if h.get('verified', True) else ' <span class="d">(unverified)</span>')""",
              """a(E(h['url']), 'open') + (' <span class="d">checked</span>' if h.get('verified', True) else ' <span class="d">(not checked)</span>')""")
open(p, 'w', encoding='utf-8').write(s)
print('headlines', len(R), 'notes added' if 'Strongest for us' in s else 'NOTES NOT ADDED')
