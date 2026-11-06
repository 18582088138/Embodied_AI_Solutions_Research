from rk02_report import *
import shutil
stem=sys.argv[1];q=json.loads((a/'derived/qa'/f'{stem}_quality.json').read_text(encoding='utf-8'));assert q['outcome']=='pass',q['errors']
run=json.loads((a/'_registry/last_run.json').read_text(encoding='utf-8'));assert run['network_requests_including_robots']==0,run
shutil.copy2(a/'_registry/last_run.json',a/'derived/qa'/f'{stem}_dedup_last_run.json')
v=json.loads((s/'progress.json').read_text(encoding='utf-8'));t=v['software_depth_topics']
if stem not in t['completed']:t['completed'].append(stem)
t['checks'][stem]=dict(outcome='pass',body_han_chars=q['body_han_chars'],sources=len(json.loads((s/'evidence'/f'{stem}.json').read_text(encoding='utf-8'))['source_ids']),network_requests=0,quality=f'reference_metrial/derived/qa/{stem}_quality.json',dedup=f'reference_metrial/derived/qa/{stem}_dedup_last_run.json')
remaining=[x for x in t['planned'] if x not in t['completed']];t['current_topic']=remaining[0] if remaining else 'overview/index'
if remaining:baseline(remaining[0])
(s/'progress.json').write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
print(stem,'complete',q['body_han_chars'],'Han; next',t['current_topic'])
