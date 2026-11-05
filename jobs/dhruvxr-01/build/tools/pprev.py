import subprocess,os
from PIL import Image,ImageDraw
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130 Safari/537.36'
S={'notification_stack':['1190185/1190185-sd_640_360_30fps','853796/853796-sd_640_360_25fps','5321400/5321400-sd_640_360_25fps','6414244/6414244-sd_640_360_24fps'],
'sticky_notes':['853759/853759-sd_640_360_25fps','4832133/4832133-sd_640_360_24fps','6804115/6804115-sd_960_506_25fps'],
'tangled_cables':['6079428/6079428-sd_640_360_24fps','1085656/1085656-sd_640_360_25fps','5090782/5090782-sd_960_506_25fps'],
'whiteboard':['853977/853977-sd_640_360_25fps','5904584/5904584-sd_640_360_24fps','5569199/5569199-sd_640_360_25fps'],
'office_crowd':['3192023/3192023-sd_640_360_25fps','3192307/3192307-sd_640_360_25fps','12695740/12695740-sd_640_360_24fps','26744705/11999045_640_360_25fps'],
'crowd_above':['13852105/13852105-sd_640_360_30fps','2088290/2088290-sd_640_360_30fps','4687383/4687383-sd_640_360_24fps','853889/853889-sd_640_360_25fps'],
'stairwell':['5087355/5087355-sd_640_360_25fps','5986347/5986347-sd_640_360_24fps','4747497/4747497-sd_640_360_25fps','6279429/6279429-sd_640_360_24fps'],
'fisheye':['4481766/4481766-sd_640_360_25fps','4446278/4446278-sd_640_360_25fps'],
'alarm_clock':['7033779/7033779-sd_640_360_25fps','4420470/4420470-sd_640_360_25fps'],
'office_lowangle':['5981597/5981597-sd_960_506_25fps','3044678/3044678-sd_640_360_24fps']}
for slot,fs in S.items():
  rows=[]
  for f in fs:
    i=f.split('/')[0]; p=f'pprev/{i}.mp4'
    if not os.path.exists(p): subprocess.run(['curl','-sL','-A',UA,'-o',p,f'https://videos.pexels.com/video-files/{f}.mp4'])
    d=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout.strip()
    try:d=float(d)
    except: print('bad',slot,i,os.path.getsize(p)); continue
    fr=[]
    for k,t in enumerate([d*0.1,d*0.5,d*0.85]):
      o=f'pprev/{i}_{k}.jpg'; subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',p,'-frames:v','1','-vf','scale=320:180',o])
      fr.append(Image.open(o))
    rows.append((i,d,fr))
  S2=Image.new('RGB',(960,len(rows)*202),'black'); dr=ImageDraw.Draw(S2)
  for n,(i,d,fr) in enumerate(rows):
    y=n*202; dr.text((4,y+4),f'{slot} pexels {i} {d:.1f}s',fill='yellow')
    for k,f in enumerate(fr): S2.paste(f,(k*320,y+22))
  S2.save(f'sheets/px_{slot}.jpg',quality=75)
print('ok')
