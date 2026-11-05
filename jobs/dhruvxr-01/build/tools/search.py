import re,subprocess,sys,json
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130 Safari/537.36'
Q={
'notification_stack':['phone notifications','smartphone screen','phone scrolling'],
'sticky_notes':['sticky notes','post it'],
'tangled_cables':['cables','wires'],
'alarm_clock':['alarm clock'],
'whiteboard':['whiteboard'],
'typing_fast':['typing keyboard','typing'],
'office_lowangle':['busy office','office people walking','office'],
'office_crowd':['crowd cheering','crowd','audience'],
'crowd_threshold':['crowd','people walking'],
'crowd_above':['crowd from above','people from above','aerial people walking'],
'slowshutter_crowd':['train station','station people','motion blur people','time lapse people'],
'stairwell':['spiral staircase','staircase','stairs'],
'fisheye':['fisheye','climbing','low angle'],
}
out={}
for k,qs in Q.items():
  seen={}
  for q in qs:
    slug=q.replace(' ','-')
    h=subprocess.run(['curl','-sL','-A',UA,f'https://mixkit.co/free-stock-video/{slug}/'],capture_output=True,text=True).stdout
    for m in re.finditer(r'href="/free-stock-video/([a-z0-9-]+)-(\d+)/"',h):
      seen.setdefault(m.group(2),m.group(1))
  out[k]=seen
  print('##',k,len(seen))
  for i,t in list(seen.items())[:40]: print('  ',i,t)
json.dump(out,open('search.json','w'),indent=1)
