"""Finish only a chapter with passed QA and verified final dedup run."""
import pathlib,json,hashlib,shutil,datetime,sys
P=pathlib.Path(__file__).resolve().parent.parent;S=sys.argv[1];A=P/'reference_metrial';Q=A/'derived/qa'
q=json.loads((Q/(S+'_quality.json')).read_text(encoding='utf8'));e=json.loads((P/'research_state/evidence'/(S+'.json')).read_text(encoding='utf8'));r=json.loads((A/'_registry/last_run.json').read_text(encoding='utf8'))
assert q['outcome']=='pass' and not q['errors'] and all(q['other_reports_unchanged'].values())
assert r['network_requests_including_robots']==0 and r['summary'].get('failed',0)==0 and set(r['names'])==set(e['source_ids'])
shutil.copyfile(A/'_registry/last_run.json',Q/(S+'_dedup_last_run.json'))
summary=dict(body_han_chars=q['body_han_chars'],tables=q['tables'],sources=q['sources'],figures=q['figures'],claim_reviews=len(e['claim_review']),archive_status=q['archive_status'],quality_errors=0,dedup_network_requests=0,report_sha256=hashlib.sha256((P/(S+'.md')).read_bytes()).hexdigest())
(Q/(S+'_research_log.json')).write_text(json.dumps(dict(chapter=S,data_cutoff='2026-11-04',completed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),summary=summary,manual_review=e['manual_review'],other_reports_unchanged=q['other_reports_unchanged'],final_dedup=r,method='官方原文/模型卡/源码→原图实际打开→条件审阅→结构/归档检查→最终去重；未运行硬件/机器人实测'),ensure_ascii=False,indent=2),encoding='utf8')
fp=P/'research_state/progress.json';p=json.loads(fp.read_text(encoding='utf8'))
if S not in p['completed_dimensions']:p['completed_dimensions'].append(S)
p.setdefault('chapter_summaries',{})[S]=summary;p['current_dimension']=S;p['review_status']='completed_continuously_authorized';p['data_cutoff']='2026-11-04'
p['next_step']='按用户04—09连续授权进入下一章；完成09后整体交付供审阅。'
p['qa_files']=list(dict.fromkeys(p.get('qa_files',[])+[(Q/(S+suffix)).as_posix() for suffix in ('_quality.json','_dedup_last_run.json','_research_log.json')]))
fp.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(summary,ensure_ascii=False))
