from rk_work import *
from html.parser import HTMLParser
class Parser(HTMLParser):
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if v and k in ('src','href','poster','srcset') and ':' in v and not v.startswith(('http','https')):print(tag,k,v)
n=sys.argv[1];r=json.loads((a/'_registry/materials.json').read_text(encoding='utf-8'));v=r[n];data=pathlib.Path(v['original_file']).read_bytes().decode('utf-8',errors='replace');Parser().feed(data)
