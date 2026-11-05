"""Intro name title (all 8 ads) and TRYIMMUFIX code card (ads that say "use this code").
Title: name baseline y in px (1080x1920 frame), left edge x = 62 px, shown 0.40 s -> 4.90 s.
Code: starts on the word ("use" / "this code"), holds to the end of the ad."""
TITLE_X = 62
TITLE = {
    '348e0ba6': dict(sub='World Marathon Champion', y=252),   # I'm 52 (sofa, hedge behind)
    '404c5cb2': dict(sub='Four-time Olympian', y=252),        # I held the record (park)
    '664b35b2': dict(sub='World Marathon Champion', y=252),   # People are always surprised (sofa)
    '0991faf2': dict(sub='Four-time Olympian', y=412),        # ran professionally (riverside: sit over the trees, not the bright sky)
    'cd03e189': dict(sub='World Marathon Champion', y=252),   # 1 star reviews (sofa)
    '974102f7': dict(sub='Four-time Olympian', y=412),        # 3 questions (riverside)
    'f233433f': dict(sub='World Marathon Champion', y=190),   # 3 things to check (above the whiteboard)
    '593f11c4': dict(sub='Four-time Olympian', y=412),        # Secret weapon (riverside)
}
TITLE_IN, TITLE_OUT = 0.40, 4.90
CODE = {   # start (s): the word she says it on
    '348e0ba6': 26.80,    # "Use this code for a discount"
    '0991faf2': 26.10,    # "use this code here for 20% off"
    '974102f7': 42.70,    # "so use this code here"
    'f233433f': 48.25,    # "They use this code"
    '593f11c4': 22.28,    # "give you this code"
}
