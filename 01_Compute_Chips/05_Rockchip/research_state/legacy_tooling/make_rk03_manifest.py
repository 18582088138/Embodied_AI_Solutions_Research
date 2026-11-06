from rk02_report import *
from urllib.parse import urlsplit
r=json.loads((a/'_registry/materials.json').read_text(encoding='utf-8'));v=r['RK02_RKNN3_ToolkitRepo']
items=[dict(name='RK02_RKNN3_Readme',url='https://raw.githubusercontent.com/airockchip/rknn3-toolkit/main/README.md',expected='any'),dict(name='RK02_RKNN3_License',url='https://raw.githubusercontent.com/airockchip/rknn3-toolkit/main/LICENSE',expected='any')]
for u in dict.fromkeys(v['links']):
 if '/blob/main/doc/EN/' in u and u.endswith('.pdf'):
  path=u.split('/blob/main/')[1];stem=pathlib.PurePosixPath(path).stem
  items.append(dict(name='RK02_'+stem,url='https://raw.githubusercontent.com/airockchip/rknn3-toolkit/main/'+path,expected='pdf'))
(root/'toolkit/manifests/Rockchip_02D_Docs.json').write_text(json.dumps(items,indent=2),encoding='utf-8')
print(len(items),'confirmed sources')
