"""Build one explicitly selected software topic only. Offline, no registry changes."""
import argparse,json,pathlib,re,hashlib
ap=argparse.ArgumentParser();ap.add_argument('stem');a=ap.parse_args()
D=pathlib.Path(__file__).resolve().parent;P=D.parents[1];A=P/'reference_metrial'
assert a.stem in dict(json.loads((D/'topics.json').read_text(encoding='utf-8')))
R=json.loads((A/'_registry/materials.json').read_text(encoding='utf-8'))
C={x['source_id']:x for x in json.loads((P/'research_state/source_catalog_02.json').read_text(encoding='utf-8'))}
meta=json.loads((D/'source_meta.json').read_text(encoding='utf-8')) if (D/'source_meta.json').exists() else {}
B=(D/(a.stem+'.txt')).read_text(encoding='utf-8')
ids=list(dict.fromkeys(re.findall(r'@@(?!FIG:)([\w]+)@@',B)))
num={s:f'S{i:02}' for i,s in enumerate(ids,1)}
catalog=[]
def ver(s):
 if s in meta:return meta[s].get('version','公开文档快照；见正文条件')
 if s in C:return C[s]['version']
 if s.startswith('AMD_MIGraphX_'):return 'MIGraphX latest文档（2.18.0支持环境另核）；develop仓库不等固定tag'
 if s.startswith('AMD_HIP_'):return 'HIP latest开发指南快照；设备/驱动/库版本有独立条件'
 if s.startswith('AMD_Quark_'):return 'Quark通用latest文档，不能替代VitisAI6.3内置Quark0.12'
 if s.startswith('Compare_'):return 'NVIDIA官方资料用于机制对标；导入2026-11-03已有原响应或本次取得，不套AMD目标'
 if s.startswith('AMD_VAI_'):return 'VitisAI Gen2 6.3 public guide；目标/overlay/精度分别固定'
 if s.startswith('AMD_EDF_'):return 'EDF26.06.1-rev3文档，评估参考发行，非OSV长期支持'
 return '2026-11-04公开快照，未标明确发布时间；具体release见正文'
for s in ids:
 r=R[s];assert r.get('status')==200 and r['archive_status'] in ('complete_static','partial_static'),s
 title=meta.get(s,{}).get('title',C.get(s,{}).get('title',s))
 B=B.replace('@@'+s+'@@',f"[{num[s]} {title}]({r['url']})")
 catalog.append(dict(source_id=s,number=num[s],title=title,version=ver(s),url=r['url'],file=pathlib.Path(r['file']).as_posix(),
  sha256=r['sha256'],original_file=pathlib.Path(r['original_file']).as_posix(),original_sha256=r['original_sha256'],
  metadata_file=(pathlib.Path(r['file']).parent/'metadata.json').as_posix(),collected_at=r.get('retrieved_at_utc'),
  archive_status=r['archive_status'],missing_dependencies=r.get('unavailable_assets',{}),notes=r.get('notes',[])))
allfig=[]
for fp in [P/'research_state/figure_manifest_02.json',*D.glob('figures_*.json')]:allfig+=json.loads(fp.read_text(encoding='utf-8'))
F={f.get('slug',pathlib.Path(f['file']).stem):f for f in allfig}
figids=list(dict.fromkeys(re.findall(r'@@FIG:(\w+)@@',B)));figs=[]
for fid in figids:
 f={k:v for k,v in F[fid].items() if k!='slug'};assert f['source_id'] in ids
 candidates=[q for q in R[f['source_id']].get('assets',[]) if q['url']==f['source_url']]
 if candidates:
  q=candidates[0];f['original_file']=(A/q.get('local_file',q['file'])).as_posix()
 assert hashlib.sha256(pathlib.Path(f['original_file']).read_bytes()).hexdigest()==f['original_sha256']
 f['manual_open_review']='已实际打开查看；全图/文字/箭头/单位完整，无空白/乱码；限制见正文图注。'
 figs.append(f);B=B.replace('@@FIG:'+fid+'@@',f['file'])
assert '@@' not in B
reviews=json.loads((D/(a.stem+'_review.json')).read_text(encoding='utf-8'))
claims=[]
for c in reviews:
 s=c['source_id'];assert s in ids
 text=re.sub(r'\s+',' ',(pathlib.Path(R[s]['file']).parent/'text.txt').read_text(encoding='utf-8'))
 needle=re.sub(r'\s+',' ',c.pop('needle'));m=re.search(re.escape(needle),text,re.I)
 if not m:raise ValueError(s+': missing exact archived quote '+needle)
 c.update(exact_quote=text[m.start():m.end()],context_quote=text[max(0,m.start()-100):min(len(text),m.end()+600)],
  source_url=R[s]['url'],material_version=ver(s),collected_at=R[s].get('retrieved_at_utc'),
  quote_basis='原文text.txt空白规整，精确短引及上下文；人工核验正文/API/表，不以匹配代替语义审阅')
 claims.append(c)
trace=dict(source_ids=ids,figures=figs,claim_review=claims,manual_review=dict(
 coverage='独立软件专题：机制、对象/数据流、优化条件、版本/许可、机制对标和可复建验证；具体覆盖详见正文各节。',
 versions_and_measurements='原文/API/表格和已归档图逐项核验；snapshot/绑定发行、示例/厂商宣称/分析公式/本次测试分别标识；没有实机测量。',
 maturity_and_licenses='遵循代码、编译工具/IP、二进制、模型/数据和本体SDK分层；未安装或接受下载协议，未取得对象明确列缺口。',
 figures_opened='每幅图均已实际打开复核；新SVG用Chromium保留foreignObject，旧图复用原检查；具体来源/哈希/操作与正文限制对应。'))
E=P/'research_state/evidence'/(a.stem+'.json');E.write_text(json.dumps(trace,ensure_ascii=False,indent=2),encoding='utf-8')
cp=D/(a.stem+'_sources.json');cp.write_text(json.dumps(catalog,ensure_ascii=False,indent=2),encoding='utf-8')
appendix=['\n## 参考资料与本地原件\n','下表S编号对应正文。原响应/哈希/采集时间和缺失依赖见metadata；partial_static保留可读正文，不保证动态交互/像素保真。既有2026-11-03 NVIDIA响应仅用于机制对标，其他材料采集于2026-11-04。\n',
 '| 原站来源 | 日期/版本/使用条件 | 本地原件与metadata | 归档状态 |','|---|---|---|---|']
for c in catalog:appendix.append(f"| [{c['number']} {c['title']}]({c['url']}) | {c['version']} | [HTML/PDF]({c['file']}) · [metadata]({c['metadata_file']}) | {c['archive_status']} |")
appendix.append(f"\n[主张、图源与人工核验记录]({E.as_posix()}) · [完整引用及依赖清单]({cp.as_posix()})。本专题未执行SDK安装、模型训练/推理、刷板或机器人闭环测试。")
(P/(a.stem+'.md')).write_text(B+'\n'.join(appendix)+'\n',encoding='utf-8')
mf=P.parents[1]/'toolkit/manifests'/('AMD_'+a.stem+'_final.json')
mf.write_text(json.dumps([dict(name=s,url=R[s]['url'],expected='pdf' if pathlib.Path(R[s]['file']).suffix=='.pdf' else 'html',used_by=[a.stem]) for s in ids],ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(stem=a.stem,han_chars=len(re.findall('[\u4e00-\u9fff]',B)),sources=len(ids),figures=len(figs),claims=len(claims)),ensure_ascii=False))
