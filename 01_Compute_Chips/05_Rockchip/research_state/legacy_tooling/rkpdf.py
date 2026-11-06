import pathlib,re,sys
sys.stdout.reconfigure(encoding='utf-8')
p=pathlib.Path(__file__).resolve().parent.parent/'01_Compute_Chips/05_Rockchip/reference_metrial/derived/extracted'
t=(p/(sys.argv[1]+'.txt')).read_text(encoding='utf-8')
if sys.argv[2]=='find':
 for m in re.finditer(sys.argv[3],t,re.I):
  page=list(re.finditer(r'===== PAGE (\d+) =====',t[:m.start()]))[-1][1]
  print('page',page,t[m.start():m.start()+220].replace('\n',' '))
else:
 nums=[]
 for v in sys.argv[2].split(','):
  if '-' in v:x,y=map(int,v.split('-'));nums.extend(range(x,y+1))
  else:nums.append(int(v))
 for m in re.finditer(r'===== PAGE (\d+) =====([\s\S]*?)(?=\n===== PAGE|\Z)',t):
  if int(m[1]) in nums:print(m[0])
