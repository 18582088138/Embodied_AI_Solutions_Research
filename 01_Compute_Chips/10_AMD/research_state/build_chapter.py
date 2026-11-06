"""Build one authorized 04–09 report from curated offline inputs; no registry writes."""
import pathlib,json,re,hashlib,sys,collections
P=pathlib.Path(__file__).resolve().parent.parent;stem=sys.argv[1];assert re.match(r'0[4-9][A-Z]?_',stem)
D=P/'research_state'/('depth_'+stem[:2]);A=P/'reference_metrial';R=json.loads((A/'_registry/materials.json').read_text(encoding='utf8'))
B=(D/(stem+'.txt')).read_text(encoding='utf8').replace('@@ROOT@@',P.as_posix())
ids=list(dict.fromkeys(re.findall(r'@@(?!FIG:)(\w+)@@',B)));num={s:f'S{i:02}' for i,s in enumerate(ids,1)}
M={}
for f in [P/'research_state/source_catalog_01.json',P/'research_state/source_catalog_02.json',D/'source_meta.json']:
 if f.exists():
  v=json.loads(f.read_text(encoding='utf8'));M.update(v if isinstance(v,dict) else {c['source_id']:c for c in v})
catalog=[]
for s in ids:
 r=R[s];assert r.get('status')==200 and r['archive_status'] in ('complete_static','partial_static'),s
 meta=M.get(s,{});title=meta.get('title',s);version=meta.get('version','官方公开快照；版本/适用条件见正文，采集日期不等发布日期')
 B=B.replace('@@'+s+'@@',f'[{num[s]} {title}]({r["url"]})')
 catalog.append(dict(source_id=s,number=num[s],title=title,version=version,url=r['url'],file=pathlib.Path(r['file']).as_posix(),sha256=r['sha256'],original_file=pathlib.Path(r['original_file']).as_posix(),original_sha256=r['original_sha256'],metadata_file=(pathlib.Path(r['file']).parent/'metadata.json').as_posix(),collected_at=r.get('retrieved_at_utc'),archive_status=r['archive_status'],unavailable_assets=r.get('unavailable_assets',{}),notes=r.get('notes',[])))
figids=list(dict.fromkeys(re.findall(r'@@FIG:(\w+)@@',B)));F={f['slug']:f for f in json.loads((D/'figures.json').read_text(encoding='utf8'))} if figids else {};figs=[]
for fid in figids:
 f=F[fid].copy();assert f.pop('opened',False),fid;f.pop('slug');assert f['source_id'] in ids
 for key,h in [('file','sha256'),('original_file','original_sha256')]:assert hashlib.sha256(pathlib.Path(f[key]).read_bytes()).hexdigest()==f[h]
 figs.append(f);B=B.replace('@@FIG:'+fid+'@@',f['file'])
assert '@@' not in B
reviews=json.loads((D/(stem+'_reviews.json')).read_text(encoding='utf8'));claims=[];missing=[]
for c0 in reviews:
 c=c0.copy();s=c['source_id'];assert s in ids
 sf=pathlib.Path(R[s]['file']);tf=sf.parent/'text.txt'
 if sf.suffix=='.pdf':tf=A/'derived/extracted'/(s+'.txt')
 t=re.sub(r'\s+',' ',(tf if tf.exists() else sf).read_text(encoding='utf8'));needle=re.sub(r'\s+',' ',c.pop('needle'));m=re.search(re.escape(needle),t,re.I)
 if not m:missing.append([s,needle]);continue
 c.update(exact_quote=t[m.start():m.end()],context_quote=t[max(0,m.start()-100):m.end()+700],source_url=R[s]['url'],material_version=M.get(s,{}).get('version','版本条件见正文'),collected_at=R[s].get('retrieved_at_utc'),quote_basis='已归档可见正文提取或原始Markdown规整空白的精确短引与上下文，人工核对章节/API/表；匹配不代替语义审阅');claims.append(c)
if missing:print(json.dumps(dict(missing_quotes=missing),ensure_ascii=False));raise SystemExit(2)
manual=json.loads((D/(stem+'_manual.json')).read_text(encoding='utf8'))
trace=dict(source_ids=ids,figures=figs,claim_review=claims,manual_review=manual)
E=P/'research_state/evidence'/(stem+'.json');E.write_text(json.dumps(trace,ensure_ascii=False,indent=2),encoding='utf8')
cp=D/(stem+'_sources.json');cp.write_text(json.dumps(catalog,ensure_ascii=False,indent=2),encoding='utf8')
col=json.loads((D/'config.json').read_text(encoding='utf8'))['collection']
app=['\n## 参考资料与本地原件\n','S编号对应正文原URL。每项有原响应、HTML/PDF及metadata和依赖。partial_static表示已取得可读正文但部分静态依赖缺失，不保证像素或动态交互完整。发布时间/版本与采集时间分开，导入既有原响应的来源保留原采集时间；没有将失败页/导航壳作为有效证据。\n','| 原始来源 | 版本/日期/条件 | 本地原件与metadata | 归档状态 |','|---|---|---|---|']
for c in catalog:app.append(f"| [{c['number']} {c['title']}]({c['url']}) | {c['version']} | [HTML/PDF/源码原件]({c['file']}) · [metadata]({c['metadata_file']}) | {c['archive_status']} |")
app.append(f'\n[主张、图源及人工核验]({E.as_posix()}) · [引用完整清单]({cp.as_posix()}) · [专题资料索引]({(A/col/"index.html").as_posix()})。本次未安装SDK/训练模型/刷板/接本体实测，测量与交付范围以正文为准。')
(P/(stem+'.md')).write_text(B+'\n'.join(app)+'\n',encoding='utf8')
mf=P.parents[1]/'toolkit/manifests'/('AMD_'+stem+'_final.json');mf.write_text(json.dumps([dict(name=s,url=R[s]['url'],expected='pdf' if pathlib.Path(R[s]['file']).suffix=='.pdf' else ('html' if pathlib.Path(R[s]['file']).suffix in ('.html','.htm') else 'any'),used_by=[stem]) for s in ids],ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(dict(stem=stem,han_chars=len(re.findall('[\u4e00-\u9fff]',B)),sources=len(ids),figures=len(figs),claims=len(claims)),ensure_ascii=False))
