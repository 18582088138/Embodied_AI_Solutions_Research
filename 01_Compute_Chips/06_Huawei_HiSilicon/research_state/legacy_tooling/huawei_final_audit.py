import pathlib,json,hashlib,subprocess,shutil,re,datetime
ROOT=pathlib.Path(__file__).resolve().parents[1];P=ROOT/'01_Compute_Chips/06_Huawei_HiSilicon';A=P/'reference_metrial';S=P/'research_state'
chapters=['01_Hardware_Platform','02_Software_Stack','03_Sensor_Integration','04_AI_Capabilities','05_Simulation_Environment','06_Robot_Integration','07_Ecosystem','08_Core_Technology_Moat','09_SWOT_Analysis']
software=['02A_Ascend_CANN_Runtime','02B_Framework_Model_Deployment','02C_HiSilicon_BSP_MPP_NPU','02D_Robot_Integration_Operations','02E_CloudRobo_Development_Platform']
core=['08A_Ascend_Execution_Compilation','08B_HiSilicon_Media_Memory','08C_CloudRobo_Action_Learning']
reports=chapters+software+core
def dump(p,v): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
dedup=json.loads((A/'_registry/last_run.json').read_text('utf8'))
assert dedup['network_requests_including_robots']==0 and len(dedup['names'])==104
shutil.copy2(A/'_registry/last_run.json',A/'derived/qa/final_union_dedup.json')
audit={}
for stem in reports:
 p=subprocess.run(['python',str(ROOT/'toolkit/check_report.py'),'--project',str(P),'--report',stem+'.md','--baseline',str(S/'baselines/final_package_frozen.json')],stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
 result=json.loads((A/'derived/qa'/(stem+'_quality.json')).read_text('utf8'))
 assert result['outcome']=='pass' and all(result['other_reports_unchanged'].values())
 audit[stem]={k:result[k] for k in ['outcome','body_han_chars','sources','figures','errors','warnings']}
 print(stem,result['outcome'],result['body_han_chars'],flush=True)
broken=[]
for name in ['Research_Index.md','02_Topics_Index.md']:
 for path in re.findall(r'\]\(<([^>]+)>\)',(P/name).read_text('utf8')):
  if pathlib.Path(path)==A/'derived/qa/final_package_audit.json': continue
  if not pathlib.Path(path).exists(): broken.append(path)
assert not broken,broken
one_hash=hashlib.sha256((P/'01_Hardware_Platform.md').read_bytes()).hexdigest()
assert one_hash=='b13be8dbee593fb8b4314e5688ecb2a76f2e104524ddc6fb4b71e55b5ae1744e'
final={'platform':'Huawei_HiSilicon','data_cutoff':'2026-11-05','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'outcome':'pass','reports':audit,'report_count':len(reports),'total_effective_body_han_chars':sum(x['body_han_chars'] for x in audit.values()),'union_effective_sources':104,'dedup_network_requests':0,'indexes_local_links':'all exist','01_unchanged_sha256':one_hash,'baseline':(S/'baselines/final_package_frozen.json').as_posix(),'limits':'结构、归档和人工核验记录；未开展模型/设备/仿真/机器人实测，未证明商业收益；静态依赖缺口已披露'}
dump(A/'derived/qa/final_package_audit.json',final)
assert all(pathlib.Path(path).exists() for name in ['Research_Index.md','02_Topics_Index.md'] for path in re.findall(r'\]\(<([^>]+)>\)',(P/name).read_text('utf8')))
old=json.loads((S/'progress.json').read_text('utf8'))
soft_union=json.loads((S/'evidence/02_Software_Stack.json').read_text('utf8'))['source_ids']
pending=json.loads((S/'evidence/final_rejected_and_pending.json').read_text('utf8'))['remaining']
state={'platform':'Huawei_HiSilicon','scope':'01—09及02A—02E/08A—08C全部公开资料调研完成','data_cutoff':'2026-11-05','authorization':'用户先审阅01，后要求继续02，最终明确“继续后面全部内容的调研”；剩余章节连续授权，无逐章停审门槛','review_status':'01用户已批准；02—09及专题完成自检，待用户审阅；completed不等于用户approved','user_approved_dimensions':['01_Hardware_Platform'],'completed_dimensions':chapters,'completed_topics':software+core,'current_dimension':None,'next_step':'交付总索引与报告；未取得项保留，工程/商业放行依实际SDK、合同和测试','pending_evidence':pending,'software_depth_topics':{'planned_topics':software,'completed_topics':software,'current_topic':None,'review_status':'五篇及总览完成自检，未记录用户批准','checks':{n:audit[n] for n in software+['02_Software_Stack']},'union_sources':soft_union,'union_source_count':61,'collection':(A/'02_software_depth/index.html').as_posix(),'dedup_network_requests':0},'core_depth_topics':{'completed_topics':core,'checks':{n:audit[n] for n in core+['08_Core_Technology_Moat']},'union_source_count':38,'collection':(A/'08_core/index.html').as_posix()},'dimension_checks':{n:audit[n] for n in chapters},'final_manifest':(ROOT/'toolkit/manifests/Huawei_01_09_Final_Union.json').as_posix(),'final_union_sources':104,'final_collection':(A/'final_01_09/index.html').as_posix(),'quality_result':'pass','dedup_network_requests':0,'report_index':(P/'Research_Index.md').as_posix(),'final_audit':(A/'derived/qa/final_package_audit.json').as_posix(),'01_preserved_sha256':one_hash,'preserved_history':['01原文未改','08_Proprietary_Technologies.md历史浅版保留，不作为本轮正式08'],'revisions':['02总览新增CloudRobo独立专题与联合资料','04补R2C分钟/或逻辑及RLinf910B模型路线','05补O3DE时钟与RLinf/OSMesa/Wan路线','引用版本main/master与SHA/tag边界校正'],'finalized_at_utc':final['at_utc']}
dump(S/'progress.json',state)
print('FINAL',json.dumps({k:final[k] for k in ['outcome','report_count','total_effective_body_han_chars','union_effective_sources','dedup_network_requests']},ensure_ascii=False))
