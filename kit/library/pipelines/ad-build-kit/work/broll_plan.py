"""B-roll placement plan.  t0/t1 = timeline seconds, src = source in-point (s) in the B-roll clip,
cx = horizontal centre of the vertical crop as a fraction of source width, scale = Motion scale %,
py = optional Motion position Y (sequence fraction, default 0.5).  line = words spoken over the shot."""
C = lambda n: 'A003_0918' + n
PLAN = {
 # Sequence 04  I'm 52 now reframed Copy 01  (reference)
 '348e0ba6': [
  dict(t0=2.20,    t1=3.8333,  clip=C('1333_C125'), src=100.0, cx=0.55, scale=57, line='bounce back than it was at 30'),
  dict(t0=13.40,   t1=14.3167, clip=C('1405_C137'), src=51.85, cx=0.56, scale=57, line='Immufix'),
  dict(t0=14.3167, t1=17.05,   clip=C('1333_C124'), src=14.0,  cx=0.48, scale=57, line='as a part of my daily routine since I was 24'),
  dict(t0=17.05,   t1=18.96,   clip=C('1416_C141'), src=4.0,   cx=0.23, scale=57, line='Just one 25 gram scoop'),
  dict(t0=18.96,   t1=19.92,   clip=C('1332_C122'), src=4.0,   cx=0.45, scale=57, line='mixed with water'),
  dict(t0=21.28,   t1=23.00,   clip=C('1406_C138'), src=90.0,  cx=0.72, scale=57, line='vitamins, minerals and nutrients'),
  dict(t0=28.3167, t1=30.1667, clip=C('1350_C134'), src=20.0,  cx=0.30, scale=57, line="on your first order and see what I'm talking about"),
 ],
 # i held the record
 '404c5cb2': [
  dict(t0=2.67,  t1=4.72,  clip=C('1341_C129'), src=36.0, cx=0.50, scale=57, line='The marathon asks a lot of your body'),
  dict(t0=4.72,  t1=6.67,  clip=C('1333_C124'), src=6.0,  cx=0.48, scale=57, line='You spend months training and preparing'),
  dict(t0=11.32, t1=13.03, clip=C('1333_C125'), src=84.0, cx=0.56, scale=57, line='after completing a training session'),
  dict(t0=16.31, t1=18.05, clip=C('1332_C123'), src=4.0,  cx=0.45, scale=57, line="It's the best time to refuel"),
  dict(t0=21.68, t1=23.55, clip=C('1348_C132'), src=10.0, cx=0.45, scale=57, line='Immufix is a vital part of that'),
  dict(t0=26.77, t1=28.28, clip=C('1414_C140'), src=39.3, cx=0.52, scale=57, line='one scoop mixed with water'),
 ],
 # People are always surprised
 '664b35b2': [
  dict(t0=2.75,  t1=4.17,  clip=C('1333_C124'), src=12.0, cx=0.48, scale=57, line='rather than running gear which is'),
  dict(t0=4.17,  t1=5.93,  clip=C('1341_C129'), src=32.0, cx=0.50, scale=57, line='probably what I used to be in'),
  dict(t0=9.82,  t1=11.62, clip=C('1358_C136'), src=6.0,  cx=0.45, scale=70, py=0.39, line='different things, a lots of traveling'),
  dict(t0=15.48, t1=18.27, clip=C('1345_C131'), src=14.0, cx=0.36, scale=57, line='So for me a go to is always going to be'),
  dict(t0=24.08, t1=25.60, clip=C('1343_C130'), src=74.5, cx=0.54, scale=57, line='most out of every day'),
 ],
 # ran professionally
 '0991faf2': [
  dict(t0=13.25, t1=14.18, clip=C('1405_C137'), src=51.75, cx=0.56, scale=57, line='I had Immufix'),
  dict(t0=15.62, t1=17.48, clip=C('1406_C138'), src=96.0,  cx=0.70, scale=57, line='vitamins, minerals and nutrients'),
  dict(t0=19.75, t1=21.48, clip=C('1414_C140'), src=39.0,  cx=0.52, scale=57, line='one scoop mixed with water'),
  dict(t0=22.30, t1=24.78, clip=C('1335_C126'), src=8.0,   cx=0.44, scale=57, line='that same routine is keeping me healthy today'),
 ],
 # 1 star reviews
 'cd03e189': [
  dict(t0=6.45,  t1=8.07,  clip=C('1348_C132'), src=76.0, cx=0.50,  scale=57, line="Now there's just one pouch on it"),
  dict(t0=12.53, t1=13.87, clip=C('1406_C138'), src=6.0,  cx=0.625, scale=57, line='the best thing about Immufix'),
  dict(t0=17.07, t1=18.47, clip=C('1416_C141'), src=12.0, cx=0.385, scale=57, line='one scoop a day'),
  dict(t0=19.32, t1=20.23, clip=C('1332_C122'), src=6.0,  cx=0.45,  scale=57, line='mixed with water'),
 ],
 # 3 questions
 '974102f7': [
  dict(t0=13.50, t1=16.13, clip=C('1405_C137'), src=20.0,  cx=0.44, scale=57, line='So what Immufix does is sit alongside'),
  dict(t0=20.03, t1=23.03, clip=C('1419_C144'), src=10.0,  cx=0.50, scale=57, line='presented in a format that your body immediately recognizes'),
  dict(t0=24.20, t1=26.68, clip=C('1406_C138'), src=100.0, cx=0.72, scale=57, line='all of the vitamins, minerals and nutrients'),
  dict(t0=32.18, t1=33.67, clip=C('1341_C129'), src=90.0,  cx=0.50, scale=57, line='Consistency builds results'),
  dict(t0=33.67, t1=35.03, clip=C('1416_C141'), src=20.0,  cx=0.50, scale=57, line='by taking one scoop a day'),
  dict(t0=37.00, t1=38.78, clip=C('1343_C130'), src=74.45, cx=0.54, scale=57, line='to keep you performing at your best'),
  dict(t0=39.85, t1=41.58, clip=C('1330_C121'), src=8.0,   cx=0.50, scale=57, line='vital part of my daily routine'),
 ],
 # 3 things to check
 'f233433f': [
  dict(t0=19.05, t1=21.20, clip=C('1418_C143'), src=30.0,  cx=0.45, scale=57, line='We formulated it to ensure that your body'),
  dict(t0=22.78, t1=25.27, clip=C('1406_C138'), src=106.0, cx=0.55, scale=57, line='the vitamins, minerals and nutrients available'),
  dict(t0=38.03, t1=40.12, clip=C('1341_C129'), src=96.5,  cx=0.50, scale=57, line='start working and helping you work at 100%'),
  dict(t0=42.13, t1=44.77, clip=C('1332_C123'), src=10.0,  cx=0.45, scale=57, line="I've been taking it for almost 30 years"),
  dict(t0=45.97, t1=48.25, clip=C('1343_C130'), src=86.0,  cx=0.57, scale=57, line='helps me get the most out of my daily life'),
 ],
 # Secret weapon
 '593f11c4': [
  dict(t0=6.22,  t1=7.30,  clip=C('1405_C137'), src=85.2, cx=0.58, scale=57, line='and then I discovered Immufix'),
  dict(t0=9.03,  t1=10.72, clip=C('1414_C140'), src=39.1, cx=0.52, scale=57, line='a scoop in the morning mixed with water'),
  dict(t0=12.35, t1=14.30, clip=C('1341_C129'), src=94.0, cx=0.50, scale=57, line='Two weeks later I was able to resume training'),
  dict(t0=17.20, t1=18.88, clip=C('1330_C121'), src=14.0, cx=0.50, scale=57, line="it's a vital part of my daily routine"),
  dict(t0=18.88, t1=20.48, clip=C('1345_C131'), src=6.0,  cx=0.56, scale=57, line="the one thing I'm never without"),
 ],
}
