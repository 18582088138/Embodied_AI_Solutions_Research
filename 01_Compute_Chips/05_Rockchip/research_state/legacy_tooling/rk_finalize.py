from rk_work import *
def union(prefix,collection):
 traces=sorted((s/'evidence').glob(prefix+'*.json'));ids=[]
 for t in traces:ids+=json.loads(t.read_text(encoding='utf-8'))['source_ids']
 ids=list(dict.fromkeys(ids));r=json.loads((a/'_registry/materials.json').read_text(encoding='utf-8'))
 f=manifest(prefix+'_Union',[(n,r[n]['url']) for n in ids])
 cmd=[sys.executable,str(root/'toolkit/download_materials.py'),'--project','01_Compute_Chips/05_Rockchip','--manifest',str(f),'--dimension',prefix+'_Union','--collection',collection,'--proxy','http://child-prc.intel.com:913']
 ret=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');assert ret.returncode==0,ret.stdout+ret.stderr
 run=json.loads((a/'_registry/last_run.json').read_text(encoding='utf-8'));assert run['network_requests_including_robots']==0
 shutil.copy2(a/'_registry/last_run.json',a/'derived/qa'/f'{prefix}_Union_dedup_last_run.json')
 print(prefix,'union',len(ids),'sources; network=0')
 return ids
def chapter_done(num,stem,nextstem=None):
 v=json.loads((s/'progress.json').read_text(encoding='utf-8'))
 if num not in v['completed_dimensions']:v['completed_dimensions'].append(num)
 v['current_dimension']=str(int(num)+1).zfill(2) if nextstem else 'complete'
 v['next_step']='按用户完整授权继续'+nextstem if nextstem else '01—09报告与资料归档完成；供用户审阅'
 v.setdefault('chapter_checks',{})[num]={'report':stem+'.md','quality':'reference_metrial/derived/qa/'+stem+'_quality.json','dedup':'reference_metrial/derived/qa/'+stem+'_dedup_last_run.json','review':'研究完成，非用户批准/实机验收'}
 if num=='02':v['software_depth_topics'].update(current_topic='complete',review_status='complete; user authorized all remaining chapters')
 if nextstem:baseline(nextstem)
 (s/'progress.json').write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
def index02():
 stems=['02_Software_Stack']+json.loads((s/'progress.json').read_text(encoding='utf-8'))['software_depth_topics']['planned']
 body='# 02 软件栈专题索引\n\n截至2026-11-05。总览与5篇专题完成公开文献/API研究及逐篇检查；未执行SDK安装、板端测试或机器人验收。01已审阅，其余由用户明确授权连续研究。\n\n'
 roles=['能力/接口与版本总图；模型到传感器/动作的缺口','kernel/DTS→MPP/RGA/GPU→buffer；stride、DMA与所有权','源图→校准→.rknn→张量；量化、输出布局与版本','视觉/音频embedding→语言会话；缓存、callback与分段计时','主机代理→协处理器；GRQ、多卡、分页、队列与语法','ROS消息→实时域→EtherCAT；资源划分、OTA/签名']
 body+='| 报告 | 研究对象/交接 | 正文汉字 | 原件数 | 图 | 验证 |\n| --- | --- | --- | --- | --- | --- |\n'
 for stem,role in zip(stems,roles):
  q=json.loads((a/'derived/qa'/f'{stem}_quality.json').read_text(encoding='utf-8'))
  body+=f"| [{stem}](<{(p/(stem+'.md')).as_posix()}>) | {role} | {q['body_han_chars']} | {q['sources']} | {q['figures']} | [检查](<{(a/'derived/qa'/f'{stem}_quality.json').as_posix()}>)；[证据](<{(s/'evidence'/f'{stem}.json').as_posix()}>)；[基线](<{(s/'baselines'/f'{stem}_before.json').as_posix()}>)；[去重](<{(a/'derived/qa'/f'{stem}_dedup_last_run.json').as_posix()}>) |\n"
 body+='\n实际交接包括固件/DTS、dma-buf与布局、模型/词表/embedding、context/session、frame/time与动作单位；最终本体契约未取得。版本重点：RKNN2 2.5.0、RKLLM1.3.1、RKNN3手册1.2.0与Firefly1.1.0部署样例独立。完整BSP、模型commit/权重授权、并发热稳定/P99/WCET、动作成功率和量产维护仍需补齐。\n\n'
 body+=f"[联合归档目录](<{(a/'02_software_depth/index.html').as_posix()}>)；[联合清单](<{(root/'toolkit/manifests/Rockchip_02_Union.json').as_posix()}>)；[联合零网络去重记录](<{(a/'derived/qa/02_Union_dedup_last_run.json').as_posix()}>)。HTML静态依赖缺损逐原件记录，动态/视频不保证完整。\n"
 (p/'02_Topics_Index.md').write_text(body,encoding='utf-8')
 # Index exempt body threshold; audit every local target.
 targets=re.findall(r'\]\(<([^>]+)>\)',body)
 assert all(pathlib.Path(x).exists() for x in targets)
 (a/'derived/qa/02_Index_quality.json').write_text(json.dumps(dict(outcome='pass',links=len(targets),limit='索引链接检查；正文门槛不适用于索引'),ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':
 if sys.argv[1]=='02':
  done('02_Software_Stack',collection='02_software_depth');union('02','02_software_depth');index02();chapter_done('02','02_Software_Stack','03_Sensor_Integration')
 elif sys.argv[1]=='chapter':chapter_done(*sys.argv[2:])
 elif sys.argv[1]=='union':union(sys.argv[2],sys.argv[3])
