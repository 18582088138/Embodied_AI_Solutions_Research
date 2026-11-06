import pathlib,json,hashlib,shutil
D=pathlib.Path(__file__).resolve().parent;A=D.parents[1]/'reference_metrial';R=json.loads((A/'_registry/materials.json').read_text(encoding='utf8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
figs=[]
for slug,tail in [('02E_realtime','realtime.png'),('02E_mixedcriticality','mixedcriticality.png')]:
 q=next(x for x in R['KRS_Realtime']['assets'] if x['url'].endswith('/'+tail));o=A/q.get('local_file',q.get('file'));f=A/'derived/figures'/(slug+'.png');shutil.copyfile(o,f)
 figs.append(dict(slug=slug,source_id='KRS_Realtime',source_url=q['url'],original_file=o.as_posix(),original_sha256=sha(o),file=f.as_posix(),sha256=sha(f),operation='官方PNG完整无修改复制，无裁剪'))
(D/'figures_E.json').write_text(json.dumps(figs,ensure_ascii=False,indent=2),encoding='utf8')
