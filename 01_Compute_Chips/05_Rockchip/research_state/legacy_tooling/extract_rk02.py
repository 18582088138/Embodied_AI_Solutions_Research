import pathlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
from pypdf import PdfReader
root=pathlib.Path(__file__).resolve().parent.parent;p=root/'01_Compute_Chips/05_Rockchip/reference_metrial';r=json.loads((p/'_registry/materials.json').read_text(encoding='utf-8'));out=p/'derived/extracted';out.mkdir(exist_ok=True)
for n,v in r.items():
 if not n.startswith('RK02') or not v.get('file','').endswith('.pdf'):continue
 pages=PdfReader(v['file']).pages
 (out/(n+'.txt')).write_text('\n'.join(f'\n===== PAGE {i+1} =====\n'+(pg.extract_text() or '') for i,pg in enumerate(pages)),encoding='utf-8')
 print(n,len(pages),'pages')
