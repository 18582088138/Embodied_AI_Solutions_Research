"""Select the already cited NVIDIA sources; does not download or alter reports."""
import json,pathlib,re
ROOT=pathlib.Path(__file__).resolve().parents[1]
report=ROOT/'01_Compute_Chips/01_NVIDIA/01_Hardware_Platform.md'
urls=set(re.findall(r'\]\((https://[^)]+)\)',report.read_text(encoding='utf-8')))
entries=[]
for path in sorted((ROOT/'_Evidence').glob('NVIDIA_*.meta.json')):
    meta=json.loads(path.read_text(encoding='utf-8'))
    if meta.get('url') in urls:
        entries.append({'name':meta['id'],'url':meta['url'],'expected':pathlib.Path(meta['file']).suffix.lstrip('.') if pathlib.Path(meta['file']).suffix in ('.pdf','.html','.json') else 'any'})
assert len(entries)==len(urls),(len(entries),len(urls))
entries.sort(key=lambda item:(item['expected']=='html',not ('Documentation' in item['name'] or 'Developer_Page' in item['name']),item['name']))
target=ROOT/'toolkit/manifests/NVIDIA_materials.json';target.parent.mkdir(exist_ok=True)
target.write_text(json.dumps(entries,ensure_ascii=False,indent=2),encoding='utf-8')
print(target,len(entries))
