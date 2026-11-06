import pathlib,json,sys,hashlib
P=pathlib.Path(__file__).resolve().parent.parent;ch=sys.argv[1];R=json.loads((P.parent/'01_NVIDIA/reference_metrial/_registry/materials.json').read_text(encoding='utf8'));d=P/'research_state'/('depth_'+ch)/'imports';d.mkdir(exist_ok=True);items=[]
for source in sys.argv[2:]:
 r=R[source];assert r['archive_status'] in ('partial_static','complete_static');f=pathlib.Path(r['original_file']);assert hashlib.sha256(f.read_bytes()).hexdigest()==r['original_sha256'];n='Model'+ch+'_'+source
 (d/(n+'.meta.json')).write_text(json.dumps(dict(url=r['url'],status=200,file=f.as_posix(),sha256=r['original_sha256'],headers={'Content-Type':r['content_type']},final_url=r['final_url'],retrieved_at_utc=r['retrieved_at_utc'])),encoding='utf8');items.append(dict(name=n,url=r['url'],expected='pdf' if pathlib.Path(r['file']).suffix=='.pdf' else 'any'))
(P.parents[1]/'toolkit/manifests'/('AMD_'+ch+'_imports.json')).write_text(json.dumps(items,indent=2),encoding='utf8');print(len(items))
