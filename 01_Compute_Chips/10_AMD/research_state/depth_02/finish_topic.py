"""Freeze successful topic checks and default reuse proof; no MD rewrites."""
import json,pathlib,sys,hashlib,shutil
D=pathlib.Path(__file__).resolve().parent;P=D.parents[1];s=sys.argv[1];Q=P/'reference_metrial/derived/qa'
q=json.loads((Q/(s+'_quality.json')).read_text(encoding='utf-8'));e=json.loads((P/'research_state/evidence'/(s+'.json')).read_text(encoding='utf-8'))
rpath=P/'reference_metrial/_registry/last_run.json';r=json.loads(rpath.read_text(encoding='utf-8'))
assert q['outcome']=='pass' and not q['errors'] and all(q['other_reports_unchanged'].values())
assert r['network_requests_including_robots']==0 and not r['summary']['failed'] and set(r['names'])==set(e['source_ids'])
shutil.copyfile(rpath,Q/(s+'_dedup_last_run.json'))
summary=dict(body_han_chars=q['body_han_chars'],tables=q['tables'],sources=q['sources'],figures=q['figures'],claim_reviews=len(e['claim_review']),
 quality_errors=0,dedup_network_requests=0,report_sha256=hashlib.sha256((P/(s+'.md')).read_bytes()).hexdigest())
f=P/'research_state/progress.json';p=json.loads(f.read_text(encoding='utf-8'))
t=p['software_depth_topics'];t.setdefault('summaries',{})[s]=summary
if s not in t['completed']:t['completed'].append(s)
order=[x[0] for x in json.loads((D/'topics.json').read_text(encoding='utf-8'))];pos=order.index(s)
if pos+1<len(order):
 nextstem=order[pos+1];baseline={x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in P.glob('*.md')}
 b=P/'research_state/baselines'/(nextstem+'_before.json')
 if not b.exists():b.write_text(json.dumps(baseline,ensure_ascii=False,indent=2),encoding='utf-8')
p['qa_files']=list(dict.fromkeys(p.get('qa_files',[])+[str(Q/(s+'_quality.json')),str(Q/(s+'_dedup_last_run.json'))]))
f.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(summary,ensure_ascii=False))
