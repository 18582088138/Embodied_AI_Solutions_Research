import pathlib,json,sys,shutil,collections
P=pathlib.Path(__file__).resolve().parents[2];A=P/'reference_metrial';T=P.parents[1]/'toolkit/manifests'
stems=['08_Core_Technology_Moat','08A_GPU_Memory_and_Execution','08B_XDNA_Numerics_and_Dataflow','08C_Versal_Dataflow_RealTime_and_Lifecycle']
rows={}
for s in stems:
 for r in json.loads((T/('AMD_'+s+'_final.json')).read_text(encoding='utf8')):
  v=rows.setdefault(r['name'],r.copy());v['used_by']=list(dict.fromkeys(v['used_by']+r['used_by']))
mf=T/'AMD_08_all_final.json'
if len(sys.argv)==1:
 mf.write_text(json.dumps(list(rows.values()),ensure_ascii=False,indent=2),encoding='utf8');print(len(rows))
else:
 r=json.loads((A/'_registry/last_run.json').read_text(encoding='utf8'))
 assert r['network_requests_including_robots']==0 and not r['summary'].get('failed',0) and set(r['names'])==set(rows)
 shutil.copyfile(A/'_registry/last_run.json',A/'derived/qa/08_all_dedup_last_run.json')
 f=P/'research_state/progress.json';p=json.loads(f.read_text(encoding='utf8'))
 p['core_technology_topics']={'completed':stems,'unique_sources':len(rows),'union_manifest':mf.as_posix(),'collection':(A/'08_core').as_posix(),'archive_status':r['summary'],'dedup_network_requests':0,'summaries':{s:p['chapter_summaries'][s] for s in stems}}
 f.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(p['core_technology_topics'],ensure_ascii=False))
