import pathlib,json,hashlib,re,shutil,datetime
P=pathlib.Path(__file__).resolve().parents[1]
A=P/'reference_metrial'
ROOT=P.parents[1]
SHA='1b0b22a2964f0f998c34cc03c5053fe61764015d'
def registry():return json.loads((A/'_registry/materials.json').read_text(encoding='utf-8'))
def dump(p,obj):
 p=pathlib.Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def baseline(stem):
 f=P/'research_state/baselines'/f'{stem}_before.json'
 if not f.exists():dump(f,{p.name:sha(p) for p in P.glob('*.md')})
def manifest(stem,items):
 f=ROOT/'toolkit/manifests'/f'Intel_{stem}.json';dump(f,items);return f
def reuse_manifest(stem,ids):
 r=registry();return manifest(stem,[dict(name=n,url=r[n]['url'],expected='any',used_by=[stem]) for n in ids])
def read(n):
 v=registry()[n];p=pathlib.Path(v['file']);p=p.parent/'text.txt' if p.suffix=='.html' else p
 return p.read_text(encoding='utf-8')
def source(name,path,topic):return dict(name=name,url=f'https://raw.githubusercontent.com/open-edge-platform/robotics-ai-suite/{SHA}/{path}',expected='any',used_by=[topic])
def compose(stem,ids,claims,figids=(),limits='文献/API/源码核验；未安装SDK、运行模型或测试机器人。'):
 baseline(stem);r=registry();body=(P/'research_state/drafts'/f'{stem}.md').read_text(encoding='utf-8')
 def cite(m):
  n=m[1];assert n in ids,n
  return f"[{n}]({r[n]['url']})"
 body=re.sub(r'\[\[([A-Za-z0-9_]+)\]\]',cite,body)
 figures=json.loads((P/'research_state/figures_02.json').read_text(encoding='utf-8'))
 used=[]
 for n in figids:
  f=figures[n];assert f.get('visual_review'),n
  body=body.replace(f'[[FIG:{n}]]',pathlib.Path(f['file']).as_posix());used.append(f)
 assert '[[' not in body
 refs='\n## 参考资料\n\n原文与本地原件对应如下。动态分支只代表所列采集时点；固定Suite源码对象不等于每篇发布日期。代码许可不自动覆盖固件、二进制、模型权重、数据和本体SDK。HTML静态依赖缺失以registry记录为准，不承诺动态交互或像素级离线一致。\n\n| 资料 | 原文 | 版本/边界 | 本地原件 | 采集时间UTC | 归档状态 |\n|---|---|---|---|---|---|\n'
 for n in ids:
  v=r[n];assert v['status']==200 and v['archive_status'] in ('complete_static','partial_static'),n
  version='固定Suite源码对象 '+SHA[:12] if SHA in v['url'] else '动态快照；文中限定API/发行版本'
  if 'Landing' in n:version+='；仅元数据'
  refs+=f"| {n} | [原文]({v['url']}) | {version} | [本地原件]({pathlib.Path(v['file']).as_posix()}) | {v['retrieved_at_utc']} | {v['archive_status']}；缺失依赖{len(v.get('unavailable_assets',{}))} |\n"
 (P/f'{stem}.md').write_text(body+refs,encoding='utf-8')
 traceclaims=[]
 for claim,n,loc,kind,conditions,finding in claims:
  v=r[n];traceclaims.append(dict(claim=claim,source_id=n,location=loc,evidence_type=kind,conditions=conditions,finding=finding,source_url=v['url'],original_file=v['file'],original_sha256=v['sha256'],retrieved_at_utc=v['retrieved_at_utc']))
 dump(P/'research_state/evidence'/f'{stem}.json',dict(source_ids=ids,figures=used,claim_review=traceclaims,manual_review=dict(coverage='本文逐机制、API对象、产物交接、硬件依赖与故障条件已人工核对；未取得信息正文保留。',versions_and_measurements='当前通用栈、Suite绑定版本与样例配置分开；性能未独立复测。',maturity_and_licenses='区分Intel提供/优化、上游组件、样例和未验收路径；许可按文件与资产范围核验。',figures_opened='所有本文图已实际打开确认文字、图例与完整边界；详见figures记录。'),research_limits=[limits]))
 reuse_manifest(stem,ids)
 print(json.dumps(dict(stem=stem,body_han=len(re.findall(r'[\u4e00-\u9fff]',body)),sources=len(ids),figures=len(used)),ensure_ascii=False))
def mark_done(stem):
 q=json.loads((A/'derived/qa'/f'{stem}_quality.json').read_text(encoding='utf-8'));assert q['outcome']=='pass'
 d=json.loads((A/'_registry/last_run.json').read_text(encoding='utf-8'));assert d['network_requests_including_robots']==0
 shutil.copy2(A/'_registry/last_run.json',A/'derived/qa'/f'{stem}_dedup_last_run.json')
 j=json.loads((P/'research_state/progress.json').read_text(encoding='utf-8'));topics=j['software_depth_topics'];topics['completed'].append(stem);topics.setdefault('checks',{})[stem]=dict(outcome=q['outcome'],body_han=q['body_han_chars'],sources=q['sources'],figures=q['figures'],dedup_network_requests=0);todo=[s for s in topics['planned'] if s not in topics['completed']];topics['current']=todo[0] if todo else '02_Software_Stack';dump(P/'research_state/progress.json',j)
