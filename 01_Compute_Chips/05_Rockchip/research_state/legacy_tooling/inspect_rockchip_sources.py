import json,pathlib,re,sys
from html.parser import HTMLParser
from urllib.parse import urljoin
p=pathlib.Path(__file__).resolve().parent.parent/'01_Compute_Chips/05_Rockchip/reference_metrial'
r=json.loads((p/'_registry/materials.json').read_text(encoding='utf-8'))
class Links(HTMLParser):
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='a' and d.get('href'): self.links.append(urljoin(self.origin,d['href']))
for n,v in r.items():
 if len(sys.argv)>1 and not any(x.lower() in n.lower() for x in sys.argv[1:]):continue
 print('\nSOURCE',n,v.get('archive_status'),v.get('error',''))
 if not v.get('file'):continue
 f=pathlib.Path(v['file'])
 tf=f.with_name('text.txt')
 if tf.exists():print(tf.read_text(encoding='utf-8')[:24000])
 if f.suffix=='.html':
  a=Links();a.links=[];a.origin=v['url'];a.feed(f.read_text(encoding='utf-8'))
  print('\nLINKS',json.dumps([u for u in dict.fromkeys(a.links) if not any(x in u for x in ['#','github.com/radxa-docs','/en/rock2','/en/rock3','/en/x/','/en/orion','/en/cubie','/en/dragon','/en/zero','/en/e/'])],ensure_ascii=False))
