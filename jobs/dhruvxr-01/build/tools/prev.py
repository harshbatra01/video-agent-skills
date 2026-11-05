import subprocess,sys,os,json
from PIL import Image,ImageDraw
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130 Safari/537.36'
C=json.loads(sys.argv[1])  # {slot:[ids]}
for slot,ids in C.items():
  rows=[]
  for i in ids:
    p=f'prev/{i}.mp4'
    if not os.path.exists(p):
      subprocess.run(['curl','-sL','-A',UA,'-o',p,f'https://assets.mixkit.co/videos/{i}/{i}-360.mp4'])
    d=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout.strip()
    try: d=float(d)
    except: print('bad',i); continue
    fr=[]
    for k,t in enumerate([d*0.1,d*0.5,d*0.85]):
      o=f'prev/{i}_{k}.jpg'
      subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',p,'-frames:v','1','-vf','scale=320:-2',o])
      if os.path.exists(o): fr.append(Image.open(o))
    rows.append((i,d,fr))
  W=320*3; H=sum((f[0].height if f else 180)+22 for _,_,f in rows)
  S=Image.new('RGB',(W,H),'black'); y=0; dr=ImageDraw.Draw(S)
  for i,d,fr in rows:
    dr.text((4,y+4),f'{slot}  {i}  {d:.1f}s',fill='yellow'); y+=22
    for k,f in enumerate(fr): S.paste(f,(k*320,y))
    y+=fr[0].height if fr else 180
  S.save(f'sheets/{slot}.jpg',quality=80); print(slot,len(rows))
