"""Read existing archive only, preserving article/table boundaries."""
import argparse, json, pathlib, re
from html.parser import HTMLParser
from urllib.parse import urldefrag
P=pathlib.Path(__file__).resolve().parents[1]
R=json.loads((P/'reference_metrial/_registry/materials.json').read_text(encoding='utf-8'))
ap=argparse.ArgumentParser(); ap.add_argument('names',nargs='+'); ap.add_argument('--links'); ap.add_argument('--pattern'); ap.add_argument('--tables',action='store_true'); ap.add_argument('--limit',type=int,default=10000); args=ap.parse_args()
class Reader(HTMLParser):
 def __init__(self): super().__init__(); self.capture=0; self.skip=0; self.out=[]; self.tables=[]; self.row=None; self.cell=None
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='main' or (t=='article' and not self.capture): self.capture+=1
  if t in ('script','style'): self.skip+=1
  if t=='tr': self.row=[]
  if t in ('th','td'): self.cell=[]
  if self.capture and t in ('p','li','h1','h2','h3','h4','div','pre','tr','br'): self.out.append('\n')
 def handle_endtag(self,t):
  if t in ('script','style'): self.skip=max(0,self.skip-1)
  if t in ('th','td') and self.cell is not None:
   if self.row is not None: self.row.append(' '.join(''.join(self.cell).split()))
   self.cell=None
  if t=='tr' and self.row is not None: self.tables.append(self.row); self.row=None
  if t in ('main','article'): self.capture=max(0,self.capture-1)
 def handle_data(self,s):
  if self.skip: return
  if self.capture: self.out.append(s)
  if self.cell is not None: self.cell.append(s)
for n in args.names:
 r=R.get(n,{}); print('\nSOURCE',n,r.get('archive_status'),r.get('error',''))
 if args.links:
  print('\n'.join(dict.fromkeys(urldefrag(x)[0] for x in r.get('links',[]) if re.search(args.links,x,re.I)))); continue
 if not r.get('file'): continue
 f=pathlib.Path(r['file'])
 if f.suffix=='.pdf':
  from pypdf import PdfReader
  content='\n'.join(f'PAGE {i+1}\n'+p.extract_text() for i,p in enumerate(PdfReader(f).pages))
 else:
  h=Reader(); h.feed(f.read_text(encoding='utf-8'))
  content='\n'.join(' | '.join(row) for row in h.tables) if args.tables else ''.join(h.out)
  if not content.strip(): content=(f.parent/'text.txt').read_text(encoding='utf-8')
 content='\n'.join(line.strip() for line in content.splitlines() if line.strip())
 if args.pattern:
  intervals=[]
  for m in re.finditer(args.pattern,content,re.I):
   l,rr=max(0,m.start()-100),min(len(content),m.end()+900)
   if intervals and l<=intervals[-1][1]: intervals[-1]=(intervals[-1][0],max(rr,intervals[-1][1]))
   else: intervals.append((l,rr))
  content='\n[... ]\n'.join(content[l:rr] for l,rr in intervals)
 print(content[:args.limit])
 if len(content)>args.limit: print('[read limit reached; archive retained]')
