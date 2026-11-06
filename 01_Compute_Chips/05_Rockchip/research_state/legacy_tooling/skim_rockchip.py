import pathlib,json,sys
from html.parser import HTMLParser
from urllib.parse import urljoin
class Links(HTMLParser):
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='a' and d.get('href'):self.links.append(urljoin(self.origin,d['href']))
p=pathlib.Path(__file__).resolve().parent.parent/'01_Compute_Chips/05_Rockchip/reference_metrial'
r=json.loads((p/'_registry/materials.json').read_text(encoding='utf-8'))
for n in sys.argv[1:]:
 v=r.get(n,{})
 print('\n',n,v.get('archive_status'))
 if not v.get('file'):continue
 f=pathlib.Path(v['file']);t=f.with_name('text.txt')
 if t.exists():
  text=t.read_text(encoding='utf-8')
  for key in ['Spec:','Specification','Product Description','Specifications','详细参数','RK182X Development Kit Overview','RK182X 3D RAM Stacking Development Kit RK3588S','Price','Power Supply','Product Introduction','ROCK 5T/5T-IndustrialOn this page']:
   pos=text.find(key)
   if pos>=0:print(text[pos:pos+6500]);break
  else:print(text[:8000])
 if f.suffix=='.html':
  a=Links();a.links=[];a.origin=v['url'];a.feed(f.read_text(encoding='utf-8'))
  print('TARGET LINKS',[x for x in dict.fromkeys(a.links) if '.pdf' in x or '/getting-started/' in x or 'download.t-firefly' in x])
