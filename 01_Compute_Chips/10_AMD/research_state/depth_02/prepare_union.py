import json,pathlib,hashlib
D=pathlib.Path(__file__).resolve().parent;P=D.parents[1];T=json.loads((D/'topics.json').read_text(encoding='utf8'));R=P.parents[1];rows={}
baseline={x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in P.glob('*.md')}
bp=P/'research_state/baselines/02_Topics_Index_before.json'
if not bp.exists():bp.write_text(json.dumps(baseline,ensure_ascii=False,indent=2),encoding='utf8')
for stem,title in T:
 for item in json.loads((R/'toolkit/manifests'/('AMD_'+stem+'_final.json')).read_text(encoding='utf8')):
  name=item['name']
  if name not in rows:rows[name]=item
  else:
   assert rows[name]['url']==item['url'] and rows[name]['expected']==item['expected']
   rows[name]['used_by']=list(dict.fromkeys(rows[name]['used_by']+item['used_by']))
mf=R/'toolkit/manifests/AMD_02_software_depth_all.json';mf.write_text(json.dumps(list(rows.values()),ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(dict(unique_sources=len(rows),source_memberships=sum(len(x['used_by']) for x in rows.values()),manifest=mf.as_posix()),ensure_ascii=False))
