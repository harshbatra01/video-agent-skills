# Pull-list data. status: 'free' = free licence, I can download directly; 'manual' = free licence, download from the page;
# 'licence' = archive footage that needs commercial clearance before use; 'shoot' = best shot ourselves.
PX = 'https://www.pexels.com/video/%s/'
GT = 'https://www.gettyimages.co.uk/detail/video/news-footage/%s'
YT = 'https://www.youtube.com/watch?v=%s'

CLIPS = {  # pexels id: (short description, best file, size MB, orientation)
 '12893568': ('Woman typing at a laptop late at night, warm lamp light', '2160x3840', 21),
 '6032135': ('Woman at her desk rubbing her temples, tired', '2160x4096', 17),
 '10047234': ('Scoop of powder tipped into a shaker (landscape, crop to vertical)', '4096x2160', 46),
 '6297755': ('Two hands overflowing with capsules', '2160x3840', 18),
 '7930758': ('Green smoothie being blended, warm natural light', '2160x3840', 23),
 '9462888': ('Rain running down a window, trees and buildings behind', '2160x3840', 26),
 '6782216': ('Pink hourglass running on white', '2160x3840', 30),
 '8263997': ('Panel talk on stage, audience in foreground', '2160x3840', 29),
 '6396064': ('People laughing over drinks at an evening event', '1080x1920', 8),
 '8044794': ('Woman with a suitcase at an airport gate', '1080x1920', 5),
 '7615545': ('Hand sorting capsules into small white bowls, sage green', '1080x1920', 15),
 '7615546': ('Same set: capsules, bowls and supplement jars', '1080x1920', 15),
 '4661333': ('Fingers counting pills in a palm', '1080x2048', 20),
 '6801319': ('Pills poured from a bottle into a hand, soft white', '2160x3840', 16),
 '7672702': ('Family walking outdoors together', '2160x3840', 26),
 '7982709': ('Three generations walking a boardwalk', '1080x1920', 7),
 '8122968': ('Family breakfast in a bright kitchen', '1080x1920', 12),
 '9811588': ('Market stall stacked with fruit', '1080x2048', 14),
 '8802446': ('Hands holding a fresh salad bowl on warm wood', '2160x3840', 22),
 '8801823': ('Woman inspecting produce in a supermarket', '2160x3840', 23),
 '8801819': ('Supermarket produce shelf, carrots and greens', '2160x3840', 17),
 '8802444': ('Top-down kale salad with tomato and cucumber', '2160x3840', 20),
 '7889571': ('Tomatoes, basil and onion close-up, warm', '2160x4096', 9),
 '5723722': ('Woman buried in a sea of pills (bold, graphic)', '1080x2048', 34),
 '7033622': ('Yellow effervescent vitamin C tablet, macro', '1080x1920', 2),
 '8676954': ('Tablet fizzing in a glass of water', '2160x3840', 27),
 '6454262': ('Runners in a snowy park (winter brief idea)', '2160x3840', 25),
}
MANUAL = {  # newer Pexels uploads: free licence, but the file name is not predictable so download from the page
 '35675125': 'Vibrant market fruit stall (alternative to 9811588)',
 '39322844': 'Family walking a path at sunset',
 '29236674': 'Rain on a window, UK-style houses behind',
 '37925060': 'Raindrops on a window, brick house behind',
 '35460855': 'Blue-violet cell animation, vertical',
 '29851224': 'Blue cell animation',
 '35219401': 'Red blood cells moving through a vessel',
 '27441395': 'Mass-start marathon crowd (generic, no Paula)',
 '29639944': 'Hooded runner on a grey morning path (winter brief idea)',
}

ARCHIVE = [
 dict(event='London Marathon world record, 13 April 2003 (2:15:25)', why='The record in "I held the marathon world record for 17 years" and "in 2003 set a world record which stood for 16 years". Paula was 29, so it also fits "than it was at 30".',
      owner='London Marathon Events Ltd (event rights) and BBC (broadcast)',
      links=[('British Athletics #TBT clip (preview)', YT % 'bqBBPXaMREI'), ('London Marathon Facebook video (preview)', 'https://www.facebook.com/LondonMarathon/videos/paula-radcliffe-2003-london-marathon-world-record/640840380324898/'), ('London Marathon media terms (commercial use needs written approval)', 'https://www.londonmarathonevents.co.uk/london-marathon/tcs-london-marathon-media-terms')],
      priority='Top'),
 dict(event='London Marathon debut win, 14 April 2002 (BBC footage on Getty)', why='Strong racing shots: on the pacemaker\'s shoulder, pulling away, crowds, the Mall, sprint finish, saluting fans.',
      owner='BBC Motion Gallery via Getty Images (editorial)',
      links=[('Running steadily, tracking shot', GT % '1B23687_0008'), ('Pulls away from pacemaker', GT % '1B23687_0007'), ('Curved street lined with crowds', GT % '1B23687_0011'), ('Into the Mall near the finish', GT % '1B22539_0004'), ('Sprint to the finish line', GT % '1B22539_0005'), ('Salutes fans after winning', GT % '1B22539_0007')],
      priority='High'),
 dict(event='Chicago Marathon world record, 13 October 2002', why='Her first marathon world record. A 28-second clip.',
      owner='Getty Images (editorial)', links=[('Paula Radcliffe sets world record', GT % '141096625')], priority='High'),
 dict(event='Commonwealth Games 5000m gold, Manchester 2002', why='Home crowd, slow-motion last lap and finish. Good for "I ran professionally" and "90% of the time in running gear".',
      owner='Getty Images (editorial); event footage also involves the Commonwealth Games Federation',
      links=[('Start line', GT % '2042601759'), ('Last lap, slow motion', GT % '2042647458'), ('Approaches finish and wins, slow motion', GT % '2042664859'), ('Wins the 5000m', GT % '2042625285'), ('Medal presentation', GT % '2042916666')], priority='High'),
 dict(event='European Cross Country win, Ferrara, 13 December 1998', why='The race in "Three months later I won the European Cross country" (Secret weapon). Also when Paula was 24.',
      owner='European Athletics and the host broadcaster (not found online yet)',
      links=[('European Athletics flashback article', 'https://www.european-athletics.com/news/flashback-to-ferrara-1998-the-first-of-many-triumphs-for-radcliffe-and-lebid'), ('Stand-in for reference only: 2001 World Cross Country win (British Athletics)', YT % 'g9zsKEukhCg')],
      priority='Ask'),
 dict(event='European 10,000m gold, Munich 2002', why='Dominant track run, useful for the "professional career" lines.',
      owner='European Athletics', links=[('European Athletics "50 Golden Moments"', YT % 'GN0CB1BpYtA')], priority='Medium'),
 dict(event='2003 training feature, Paula aged 28 (30 parts)', why='Training, running sequences and close-ups from the world-record year. Good texture for "I ran professionally".',
      owner='Getty Images (editorial)', links=[('Feature part 17 of 30', GT % '1732319547'), ('All Paula Radcliffe clips on Getty', 'https://www.gettyimages.co.uk/videos/paula-radcliffe')], priority='Medium'),
 dict(event='Fifth Avenue Mile, New York, 1 September 1995', why='A 21-year-old Paula racing. Nice for a "for over 20 years" montage.',
      owner='Getty Images (editorial)', links=[('Paula Radcliffe and Sinead Delahunty, Fifth Avenue Mile', GT % '140828685')], priority='Low'),
 dict(event='New York City Marathon win', why='Another major win for a career montage.', owner='Getty Images (editorial)', links=[('Paula Radcliffe wins NYC Marathon', GT % '140867412')], priority='Low'),
 dict(event='World Championships marathon gold, Helsinki 2005', why='Her world title. No clip found yet.', owner='World Athletics', links=[('Ask World Athletics / Paula\'s team', 'https://worldathletics.org/athletes/great-britain-ni/paula-radcliffe-14276130')], priority='Ask'),
]

# per ad: list of (timecode, words, picks, note)   picks: list of (kind, id_or_text)
ADS = [
 ('I\'m 52 now', 'Sequence 04 (reference)', [
   ('02.20 to 03.83', 'than it was at 30', [('archive', 'London Marathon 2003, Paula aged 29')], 'Optional swap: our catching-breath shot is there now. Archive of her at 29 would land this line harder.'),
   ('03.84 to 05.12', 'A late night hits harder', [('px', '12893568')], ''),
   ('05.12 to 07.52', 'and a bad week takes a lot longer to shake off', [('px', '6032135')], ''),
   ('07.52 to 11.96', 'all the random protein powders, vitamin pills and green shakes', [('px', '10047234'), ('px', '6297755'), ('px', '7930758')], 'Three quick cuts, one per item.'),
   ('24.04 to 26.12', 'And if I\'m feeling slightly under the weather', [('px', '9462888'), ('manual', '29236674')], 'Keep it to weather, not illness. See compliance notes.'),
 ]),
 ('I held the record', 'i held the record', [
   ('00.00 to 02.67', 'I held the marathon world record for 17 years', [('archive', 'London Marathon 2003 finish, or Chicago 2002 world record (Getty 141096625)')], 'Best single use of archive in the whole campaign.'),
   ('06.67 to 11.32', 'make sure that your immune system is strong to support you all the way through', [('archive', 'London Marathon 2002 racing shots (Getty 1B23687_0008 / _0011)')], 'Avoid cell or virus imagery here.'),
   ('13.03 to 16.31', 'a little bit vulnerable for 20 minutes, half an hour', [('px', '6782216')], ''),
 ]),
 ('People are always surprised', 'Sequence 03', [
   ('05.93 to 07.52', '90% of the time', [('archive', 'Commonwealth Games 2002 last lap (Getty 2042647458)')], ''),
   ('11.62 to 13.57', 'lots of meeting some really interesting people', [('px', '8263997'), ('px', '6396064')], ''),
   ('13.57 to 15.48', 'lots of drains on my immune system', [('px', '8044794')], 'Busy travel, not illness.'),
 ]),
 ('Ran professionally', 'Sequence 06', [
   ('00.00 to 02.18', 'I ran professionally for over 20 years', [('archive', 'Career montage: 1995 Fifth Avenue Mile, 2002 London, 2002 Commonwealth')], 'Optional: hook stays on her face if archive is not cleared.'),
   ('02.18 to 05.77', 'and in 2003 set a world record which stood for 16 years', [('archive', 'London Marathon 2003 world record')], 'Top priority archive.'),
   ('05.77 to 11.80', 'countless athletes with a multitude of different pills and supplements filling up their shelves', [('px', '7615545'), ('px', '4661333'), ('px', '6297755')], 'A shelf of generic tubs is better shot ourselves (see shoot list).'),
   ('24.78 to 26.10', 'and my entire family too', [('px', '7672702'), ('px', '7982709')], 'Stock people must not look like Paula\'s own family or endorse the product. Her real family clips (with consent) would be better.'),
 ]),
 ('1 star reviews', 'A003_09181134_C109', [
   ('03.45 to 06.45', 'my shelf used to be completely full of containers', [('shoot', 'Kitchen shelf crammed with assorted supplement tubs')], 'Stock fallback: 7615546.'),
   ('08.07 to 09.83', 'It feels emptier in here than it used to', [('shoot', 'Same shelf, now holding just the Immufix pouch')], 'Before and after on the same shelf makes the joke land.'),
   ('13.87 to 17.07', 'You don\'t need to take a multitude of pills and supplements', [('px', '4661333'), ('px', '6801319')], 'Counting pills matches the brief\'s "stop counting supplements".'),
 ]),
 ('3 questions', 'Sequence 01', [
   ('03.62 to 08.22', 'Why can\'t we just eat a good balanced diet with lots of fruits and vegetables', [('px', '9811588'), ('px', '8802446')], ''),
   ('08.22 to 13.50', 'the quality of the vitamins and minerals available from the food is less than it used to be', [('px', '8801823'), ('px', '8801819')], 'Neutral shopping shots only. The brief says not to state food decline as fact.'),
   ('16.13 to 18.63', 'a good balanced diet and give you the perfect balance', [('px', '8802444'), ('px', '7889571')], ''),
 ]),
 ('3 things to check', 'Sequence 09', [
   ('04.94 to 09.38', 'a company might claim to have huge amounts of vitamins and minerals', [('px', '5723722'), ('px', '6297755')], 'No identifiable competitor products.'),
   ('09.38 to 14.42', '100 times the recommended daily amount of vitamin C', [('px', '7033622'), ('px', '8676954')], ''),
   ('31.74 to 36.82', 'immediately taken into the cells where they can start working', [('manual', '35460855'), ('manual', '35219401')], 'Compliance check needed on this absorption line before adding visuals.'),
 ]),
 ('Secret weapon', 'Sequence 08', [
   ('00.00 to 02.37', 'In 1998 my season was a write off', [('archive', '1998 archive of Paula (to be sourced)')], ''),
   ('14.30 to 16.48', 'Three months later I won the European Cross country', [('archive', 'European Cross Country, Ferrara 1998')], 'See compliance notes: this ad follows the illness to Immufix to recovery pattern.'),
 ]),
]
