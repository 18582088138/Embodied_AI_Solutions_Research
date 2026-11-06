import json,pathlib,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8');root=pathlib.Path(__file__).resolve().parents[1];p=root/'01_Compute_Chips/06_Huawei_HiSilicon';a=p/'reference_metrial';stem=sys.argv[2]
s=json.loads((p/'research_state/progress.json').read_text('utf-8'))
if sys.argv[1]=='start':
 f=p/'research_state/baselines'/(stem+'_before.json')
 if not f.exists():f.write_text(json.dumps({x.relative_to(p).as_posix():hashlib.sha256(x.read_bytes()).hexdigest() for x in p.glob('*.md')},ensure_ascii=False,indent=2),encoding='utf-8')
 s['current_dimension']=stem;s['next_step']='完成当前章节资料、正文、图像复核及检查，再按顺序继续'
elif sys.argv[1]=='complete':
 q=json.loads((a/'derived/qa'/(stem+'_quality.json')).read_text('utf-8'));assert q['outcome']=='pass'
 run=(a/'_registry/last_run.json').read_text('utf-8');(a/'derived/qa'/(stem+'_dedup.json')).write_text(run,encoding='utf-8')
 s['completed_dimensions']=list(dict.fromkeys(s.get('completed_dimensions',[])+[stem]));s.setdefault('dimension_checks',{})[stem]={k:q[k] for k in ['outcome','body_han_chars','sources','figures','errors','warnings']};s['current_dimension']=None;s['next_step']='当前章节完成，继续下一获授权章节'
(p/'research_state/progress.json').write_text(json.dumps(s,ensure_ascii=False,indent=2),encoding='utf-8');print(sys.argv[1],stem)
