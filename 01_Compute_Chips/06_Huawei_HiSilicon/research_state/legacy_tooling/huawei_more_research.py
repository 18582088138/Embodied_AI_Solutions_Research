import json,pathlib,sys,re
from html.parser import HTMLParser
from urllib.parse import urljoin
sys.stdout.reconfigure(encoding='utf-8')
ROOT=pathlib.Path(__file__).resolve().parents[1];P=ROOT/'01_Compute_Chips/06_Huawei_HiSilicon';R=json.loads((P/'reference_metrial/_registry/materials.json').read_text('utf-8'))
class Links(HTMLParser):
 def __init__(self):super().__init__();self.rows=[];self.a=None
 def handle_starttag(self,t,attrs):
  d=dict(attrs)
  if t=='a':self.a=[d.get('href',''),'']
  if t=='img' and d.get('src'):self.rows.append((d['src'],d.get('alt','IMAGE')))
 def handle_data(self,d):
  if self.a:self.a[1]+=d
 def handle_endtag(self,t):
  if t=='a' and self.a:self.rows.append(tuple(self.a));self.a=None
if sys.argv[1]=='links':
 for n in sys.argv[2:]:
  x=R[n];h=Links();h.feed(pathlib.Path(x['file']).read_text('utf-8'));print('\n',n)
  for u,t in dict.fromkeys(h.rows):
   if 'cloudrobo_' in u or 'zh-cn_image_' in u or 'github.com' in u or 'huggingface.co' in u:print(t.strip(),urljoin(x['url'],u))
elif sys.argv[1]=='text':
 for n in sys.argv[2:]:
  x=R[n];f=pathlib.Path(x['file']);t=(f.parent/'text.txt').read_text('utf-8') if f.suffix=='.html' else f.read_text('utf-8',errors='replace')
  if 'GMT+08:00' in t:t=t.split('GMT+08:00',1)[1]
  t=t.split('相关文档 您对此',1)[0];print('\n',n,'\n',t[:45000])
elif sys.argv[1]=='manifest':
 rows=json.loads(pathlib.Path(sys.argv[2]).read_text('utf-8'));print(len(rows))
