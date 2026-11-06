import sys,json,pathlib
from pypdf import PdfReader
p=pathlib.Path(__file__).resolve().parent.parent/'01_Compute_Chips/05_Rockchip/reference_metrial'
r=json.loads((p/'_registry/materials.json').read_text(encoding='utf-8'))
for n in sys.argv[1:]:
 reader=PdfReader(r[n]['file'])
 t='\n'.join(f'===== PAGE {i+1} =====\n{page.extract_text()}' for i,page in enumerate(reader.pages))
 (p/'derived/extracted'/f'{n}.txt').write_text(t,encoding='utf-8');print(n,len(reader.pages))
