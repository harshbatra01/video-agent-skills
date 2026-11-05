"""External B-roll placements (timeline seconds are word/cut times; the builder snaps them to V1 cuts or 60 fps frames).
media: key into MEDIA, src: source in-point (s), cx: horizontal centre of the vertical crop (fraction of source width),
scale: Motion scale %, grade: which light Lumetri preset to use (see GRADES)."""
EXT = r'C:\VISION\IMMUFIX\repair\ENCODED RUSHES\External B roll\Stock (Pexels, free)'
YT = r'C:\VISION\IMMUFIX\repair\ENCODED RUSHES\YT FOOTAGE'
MEDIA = {
    'chicago': YT + r'\Paula Radcliffe DESTROYS WORLD RECORD to win 2002 Chicago Marathon  #running_1080p.mp4',
    'london': YT + r'\#TBT Paula Radcliffe achieves world record at the London Marathon in 2003_720p.mp4',
    'powder': EXT + r'\hands_powder-scoop-into-shaker_pexels-10047234_4096x2160.mp4',
    'capsules_hands': EXT + r'\hands_hands-full-of-capsules_pexels-6297755_2160x3840.mp4',
    'green_shake': EXT + r'\hands_green-shake-blending_pexels-7930758_2160x3840.mp4',
    'spill': EXT + r'\hands_hand-sorting-capsules_pexels-7615545_1080x1920.mp4',
    'counting': EXT + r'\hands_counting-pills-in-palm_pexels-4661333_1080x2048.mp4',
    'poured': EXT + r'\hands_pills-poured-into-hand_pexels-6801319_2160x3840.mp4',
    'veg': EXT + r'\3questions_veg-closeup_pexels-7889571_1440x2732.mp4',
    # imported into the bin for later swaps, not placed
    'capsule_bowl': EXT + r'\1star_capsule-bowl_pexels-7615430_1080x1920.mp4',
    'pills_spill_static': EXT + r'\3things-ranpro_pills-spill_pexels-5697643_2160x3840.mp4',
    'vitc_fizz': EXT + r'\3things_vitaminC-fizz_pexels-8676954_2160x3840.mp4',
    'vitc_tablet': EXT + r'\3things_vitaminC-tablet_pexels-7033622_1080x1920.mp4',
    'bottles': EXT + r'\ranpro_supplement-bottles_pexels-7525915_1080x1920.mp4',
}

# existing B-roll shots to take out (ad key, start time).
# User (2026-09-30): never remove B-roll that is already in the project; they delete old shots themselves.
# Candidates they could cut to get back under ~40%: I'm 52 C124 lacing @14.317, I held the record C124 lacing @4.717,
# ran professionally C138 nutrition panel @15.617.
REMOVE = []

ADD = {
    # I'm 52 now (reference): list montage on "all the random protein powders, vitamin pills and green shakes"
    '348e0ba6': [
        dict(t0=9.0833, t1=10.3667, media='powder', src=7.80, cx=0.22, scale=1920 / 2160 * 100, grade='stock', line='all the random protein powders'),
        dict(t0=10.3667, t1=11.1167, media='capsules_hands', src=3.00, cx=0.5, scale=50, grade='stock', line='vitamin pills'),
        dict(t0=11.1167, t1=11.9667, media='green_shake', src=3.00, cx=0.5, scale=50, grade='stock', line='and green shakes'),
    ],
    # I held the record: Chicago 2002, breaking the tape
    '404c5cb2': [
        dict(t0=0.9833, t1=2.6667, media='chicago', src=46.00, cx=0.5, scale=100, grade='archive', line='world record for 17 years'),
    ],
    # ran professionally: London 2003 finish under the clock, then the capsule spill
    '0991faf2': [
        dict(t0=3.3833, t1=5.7667, media='london', src=101.97, cx=0.55, scale=1920 / 720 * 100, grade='archive_london', line='set a world record which stood for 16 years'),
        dict(t0=8.1833, t1=11.80, media='spill', src=8.70, cx=0.5, scale=100, grade='stock', line='with a multitude of different pills and supplements filling up their shelves'),
    ],
    # 1 star reviews
    'cd03e189': [
        dict(t0=14.9833, t1=17.0667, media='counting', src=0.50, cx=0.5, scale=100, grade='stock', line='a multitude of pills and supplements'),
    ],
    # 3 things to check
    'f233433f': [
        dict(t0=10.70, t1=13.1833, media='poured', src=1.50, cx=0.5, scale=50, grade='stock', line='100 times the recommended daily amount of vitamin C'),
    ],
    # 3 questions
    '974102f7': [
        dict(t0=4.6833, t1=6.9167, media='veg', src=0.30, cx=0.5, scale=75, grade='stock', line='a good balanced diet with lots of fruits and vegetables'),
    ],
}
