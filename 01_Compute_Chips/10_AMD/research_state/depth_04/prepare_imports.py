import json,pathlib,re,hashlib,sys
D=pathlib.Path(__file__).resolve().parent;P=D.parents[1];R=json.loads((P.parent/'01_NVIDIA/reference_metrial/_registry/materials.json').read_text(encoding='utf8'))
if len(sys.argv)==1:
 for s,r in R.items():
  if re.search('OPENVLA|OPENPI|SMOL|DIFFUSION|ACT_|DINO|SAM|WAN|WORLD|LEROBOT',s,re.I):print(s,r.get('archive_status'),r['url'])
else:
 I=D/'imports';I.mkdir(exist_ok=True);items=[]
 for s in sys.argv[1:]:
  r=R[s];name='Model04_'+s;f=pathlib.Path(r['original_file']);assert r['archive_status'] in ('complete_static','partial_static') and hashlib.sha256(f.read_bytes()).hexdigest()==r['original_sha256']
  (I/(name+'.meta.json')).write_text(json.dumps(dict(url=r['url'],status=200,file=f.as_posix(),sha256=r['original_sha256'],headers={'Content-Type':r['content_type']},final_url=r['final_url'],retrieved_at_utc=r['retrieved_at_utc'])),encoding='utf8');items.append(dict(name=name,url=r['url'],expected='pdf' if pathlib.Path(r['file']).suffix=='.pdf' else 'any',used_by=['04_AI_Capabilities']))
 (P.parents[1]/'toolkit/manifests/AMD_04_imports.json').write_text(json.dumps(items,indent=2),encoding='utf8');print(len(items))
