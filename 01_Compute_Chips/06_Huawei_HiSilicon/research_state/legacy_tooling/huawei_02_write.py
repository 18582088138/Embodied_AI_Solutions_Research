import pathlib,json,hashlib,sys,re
sys.stdout.reconfigure(encoding='utf-8')
ROOT=pathlib.Path(__file__).resolve().parents[1];P=ROOT/'01_Compute_Chips/06_Huawei_HiSilicon';A=P/'reference_metrial'
R=json.loads((A/'_registry/materials.json').read_text('utf-8'))
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def link(t,p):return '['+t+'](<'+pathlib.Path(p).as_posix()+'>)'
stem=sys.argv[1];cfg=json.loads((ROOT/'toolkit/manifests'/('Huawei_'+stem+'_config.json')).read_text('utf-8'))
baseline=P/'research_state/baselines'/(stem+'_before.json')
if not baseline.exists():baseline.write_text(json.dumps({f.relative_to(P).as_posix():sha(f) for f in P.glob('*.md')},ensure_ascii=False,indent=2),encoding='utf-8')
body=(ROOT/'toolkit/drafts'/(stem+'.md')).read_text('utf-8')
body=re.sub(r'\{\{REPORT:([^}]+)\}\}',lambda m:link(m[1],P/(m[1]+'.md')),body)
ids=cfg['source_ids']
for n in ids:
 x=R[n];assert x['archive_status'] in ('complete_static','partial_static')
 body=body.replace('{{'+n+'}}','['+n+']('+x['url']+')（'+link('本地原件',x['file'])+'）')
figures=[]
for item in cfg.get('figures',[]):
 n=item['source_id'];x=R[n];f=pathlib.Path(item.get('file',x['file']));body=body.replace('{{FIG:'+n+'}}','!['+item['caption']+'](<'+f.as_posix()+'>)')
 original=item.get('original_file',x['file'])
 figures.append(dict(file=f.as_posix(),sha256=sha(f),source_id=n,source_url=item.get('source_url',x['url']),original_file=original,original_sha256=sha(original),operation=item.get('operation','官方原图；逐图打开检查')))
body+='\n\n## 参考资料与原件\n\n下列资料按 2026-11-05 核验时点使用；抓取日期不是发布日期。URL带提交SHA或tag的源码限定对应版本；main/master及模型卡仅为采集快照，未锁不可变revision。未运行安装脚本、模型或设备。\n\n| 来源 | 原文 / 本地原件 | 版本与归档边界 |\n|---|---|---|\n'
for n in ids:
 x=R[n];default='固定提交源码/许可快照；确切 SHA 见原文 URL' if re.search(r'raw.githubusercontent.com/[^/]+/[^/]+/[0-9a-f]{40}/',x['url']) else ('main/master采集快照，未锁提交SHA' if re.search(r'/(?:raw/)?(?:main|master)/',x['url']) else '页面/tag版本见原文；按采集快照使用');v=cfg.get('versions',{}).get(n,default)
 body+='| '+n+' | ['+n+']('+x['url']+') / '+link('原件',x['file'])+' | '+v+'；采集 UTC '+str(x.get('retrieved_at_utc',x.get('archived_at_utc','见 metadata')))+'；'+x['archive_status']+' |\n'
body+='\n'+link('主张和图源核验',P/'research_state/evidence'/(stem+'.json'))+'。各引用保存原始响应、哈希及 metadata；静态归档不承诺动态交互或像素级复现。\n'
assert '{{' not in body
(P/(stem+'.md')).write_text(body,encoding='utf-8')
claims=[]
for c in cfg['claims']:
 n=c['source_id'];x=R[n];c.update(source_url=x['url'],local_original=x['original_file'],retrieved_at_utc=x.get('retrieved_at_utc',x.get('archived_at_utc')),material_version=cfg.get('versions',{}).get(n,'固定提交或采集快照，见正文参考表'));claims.append(c)
trace=dict(source_ids=ids,figures=figures,claim_review=claims,manual_review=cfg['manual_review'])
(P/'research_state/evidence'/(stem+'.json')).write_text(json.dumps(trace,ensure_ascii=False,indent=2),encoding='utf-8')
manifest=[dict(name=n,url=R[n]['url'],expected='any',used_by=[stem]) for n in ids]
(ROOT/'toolkit/manifests'/('Huawei_'+stem+'.json')).write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('written',stem,'sources',len(ids),'body Han',len(re.findall('[\u4e00-\u9fff]',body.split('## 参考资料')[0])))
