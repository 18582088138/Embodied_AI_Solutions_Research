import pathlib,json,sys
from pypdf import PdfReader
P=pathlib.Path(__file__).resolve().parent.parent;R=json.loads((P/'reference_metrial/_registry/materials.json').read_text(encoding='utf8'))
for s in sys.argv[1:]:
 f=pathlib.Path(R[s]['file']);pages=PdfReader(f).pages
 print('\nSOURCE',s,'PAGES',len(pages))
 txt='\n'.join('PAGE '+str(i+1)+'\n'+p.extract_text() for i,p in enumerate(pages))
 out=P/'reference_metrial/derived/extracted'/(s+'.txt');out.parent.mkdir(exist_ok=True);out.write_text(txt,encoding='utf8');print(txt)
