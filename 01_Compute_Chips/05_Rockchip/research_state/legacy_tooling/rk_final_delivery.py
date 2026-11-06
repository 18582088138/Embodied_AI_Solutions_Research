from rk_work import *
from rk_finalize import chapter_done
from datetime import datetime,timezone
stems=['01_Hardware_Platform','02_Software_Stack','02A_BSP_Multimedia','02B_RKNN2_Compiler_Runtime','02C_RKLLM','02D_RKNN3_RK182X','02E_ROS_Control_Operations','03_Sensor_Integration','04_AI_Capabilities','05_Simulation_Environment','06_Robot_Integration','07_Ecosystem','08_Core_Technology_Moat','08A_Quantization_Compiler','08B_Memory_Coprocessor_Multicard','08C_Perception_RealTime_Trust','09_SWOT_Analysis']
registry=json.loads((a/'_registry/materials.json').read_text(encoding='utf-8'))
ids=[];checks={};figure_count=0
for stem in stems:
 q=json.loads((a/'derived/qa'/f'{stem}_quality.json').read_text(encoding='utf-8'));assert q['outcome']=='pass' and q['body_han_chars']>=1500
 d=json.loads((a/'derived/qa'/f'{stem}_dedup_last_run.json').read_text(encoding='utf-8'));assert d['network_requests_including_robots']==0
 e=json.loads((s/'evidence'/f'{stem}.json').read_text(encoding='utf-8'));ids+=e['source_ids'];figure_count+=len(e['figures'])
 for fig in e['figures']:assert sha(fig['file'])==fig['sha256'] and sha(fig['original_file'])==fig['original_sha256']
 checks[stem]={'outcome':'pass','body_han_chars':q['body_han_chars'],'sources':q['sources'],'figures':q['figures'],'md_sha256':sha(p/(stem+'.md')),'network_requests':0}
ids=list(dict.fromkeys(ids))
for n in ids:assert registry[n]['archive_status'] in ('complete_static','partial_static') and registry[n]['status']==200
# The most recent chapter baseline protects every already completed chapter.
b=json.loads((s/'baselines/09_SWOT_Analysis_before.json').read_text(encoding='utf-8'))
protected={n:sha(p/n)==h for n,h in b.items() if n!='09_SWOT_Analysis.md'};assert all(protected.values())
approved=json.loads((s/'baselines/02_Software_Stack_before.json').read_text(encoding='utf-8'))['01_Hardware_Platform.md'];assert checks['01_Hardware_Platform']['md_sha256']==approved
f=manifest('01_09_Union',[(n,registry[n]['url']) for n in ids])
ret=subprocess.run([sys.executable,str(root/'toolkit/download_materials.py'),'--project','01_Compute_Chips/05_Rockchip','--manifest',str(f),'--dimension','01_09_Final','--proxy','http://child-prc.intel.com:913'],capture_output=True,text=True,encoding='utf-8');assert ret.returncode==0,ret.stdout+ret.stderr
run=json.loads((a/'_registry/last_run.json').read_text(encoding='utf-8'));assert run['network_requests_including_robots']==0
shutil.copy2(a/'_registry/last_run.json',a/'derived/qa/01_09_Union_dedup_last_run.json')
roles=['已审阅样章：芯片/板卡、规格与供应','软件总览与链路交接','BSP、多媒体、GPU与buffer','RKNN2编译/量化/runtime','RKLLM模型与多模态会话','RKNN3协处理器/Server','ROS/AMP/实时/OTA','采集、带宽、标定与时间','模型地图、VLA/视觉部署边界','仿真、训练与sim-to-real','产品绑定、演示与运营边界','伙伴分工、产线、保修与开放性','跨机制价值与条件判断','GRQ/格式/映射/插件/精度','DRAM/KV/多卡/队列/链路','ISP/时间/实时/可信与安全边界','商业分级、TCO、政策与条件选型']
body='# Rockchip 具身智能平台调研总索引\n\n截至2026-11-05，按01→09顺序完成公开文献、官方原件、API和源码静态研究。01为已审阅样章；02—09及必要专题依据用户“继续后面全部内容的调研”连续完成，研究完成不代用户批准或实机验收。\n\n'
body+=f'交付9章主报告、02的5篇专题、08的3篇专题，共17篇研究正文；实际引用联合清单含{len(ids)}个registry来源（按来源名称计，规范URL另由registry去重），有效正文汉字合计{sum(x["body_han_chars"] for x in checks.values())}。每篇正文达到1500有效汉字底线并通过结构/归档检查，图像逐张核查；全部引用联合复用运行为零网络请求。\n\n'
body+='| 报告 | 内容与读法 | 有效汉字 | 原件 | 图 | 检查/证据/去重 |\n| --- | --- | --- | --- | --- | --- |\n'
for stem,role in zip(stems,roles):
 q=checks[stem]
 body+=f"| [{stem}](<{(p/(stem+'.md')).as_posix()}>) | {role} | {q['body_han_chars']} | {q['sources']} | {q['figures']} | [检查](<{(a/'derived/qa'/f'{stem}_quality.json').as_posix()}>)；[证据](<{(s/'evidence'/f'{stem}.json').as_posix()}>)；[去重](<{(a/'derived/qa'/f'{stem}_dedup_last_run.json').as_posix()}>) |\n"
body+=f"\n[02专题索引](<{(p/'02_Topics_Index.md').as_posix()}>)；[08专题索引](<{(p/'08_Topics_Index.md').as_posix()}>)；[全部原件归档](<{(a/'index.html').as_posix()}>)；[最终引用联合清单](<{f.as_posix()}>)；[最终零网络去重](<{(a/'derived/qa/01_09_Union_dedup_last_run.json').as_posix()}>)；[最终审计](<{(a/'derived/qa/Final_Research_Audit.json').as_posix()}>)；[研究状态](<{(s/'progress.json').as_posix()}>)。\n\n"
body+='## 主要结论与限制\n\nRockchip形成SoC视觉/控制与RK182X语言/多模态协处理器的组合路线，RKNN工具、ISP/多媒体、伙伴板卡和工业文档提供可复用工程入口。其价值成立于模型受支持、精度与数据年龄合格、控制/保护独立验证、BSP与供应责任明确；当前证据不能给全面性能排名或机器人ROI。\n\n'
body+='软件重点版本为RKNN2/Zoo2.5.0、RKLLM1.3.1、RKNN3手册1.2.0。板商BSP、模型commit和运行库需单独锁定。RKNN3多卡为显式分段与主机队列转发，分页模型本版request_num只支持1；模型阶段benchmark与VLA演示FPS不是完整闭环/P99/WCET或任务成功率。\n\n'
body+='未进行SDK安装、模型运行、板端/机器人测试、下单或key烧写。完整BSP/TRM、实际DRAM带宽、并发热稳定与能耗、VLA完整配置和留出任务结果、功能安全、逐料号PCN/EOL/含税交期与现场合同仍需项目证据。HTML依赖缺损逐原件披露，动态交互/视频不保证完整。旧08_Proprietary_Technologies.md保持历史占位，当前08入口为08_Core_Technology_Moat.md。\n\n'
body+=f"财报官方目录/API已取得，但上交所三季报/半年报/年度摘要请求返回浏览器校验页，已拒收；个人信息保护法候选URL404。上述失败资料不计入有效引用，不引用收入/利润/市场份额数字。政策采用已取得的生成式AI办法原文，有限范围不代表完整当期法律/出海审查。[09未取得原件记录](<{(a/'derived/qa/09_unobtained_sources.json').as_posix()}>)。\n"
(p/'Research_Index.md').write_text(body,encoding='utf-8')
targets=re.findall(r'\]\(<([^>]+)>\)',body)
audit=dict(outcome='pass',checked_at_utc=datetime.now(timezone.utc).isoformat(),reports=checks,cited_source_names=len(ids),cited_unique_urls=len(set(registry[n]['url'] for n in ids)),figure_occurrences=figure_count,approved_01_unchanged=True,protected_hashes=protected,final_network_requests=0,index_links=len(targets),scope='结构/归档/图源哈希/完成基线检查，含人工静态核查记录；不代表实机或独立商业审计')
(a/'derived/qa/Final_Research_Audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
assert all(pathlib.Path(x).exists() for x in targets)
chapter_done('09','09_SWOT_Analysis')
v=json.loads((s/'progress.json').read_text(encoding='utf-8'));v['review_status']='01 approved; 02—09 research complete, awaiting user review; no hardware acceptance';v['next_step']='01—09及全部02/08专题研究交付；用户可通过Research_Index.md审阅；无自动实机/采购步骤'
times=[registry[n]['archived_at_utc'] for n in ids];v['source_collection_utc_range']=[min(times),max(times)];v['final_delivery']={'index':'Research_Index.md','audit':'reference_metrial/derived/qa/Final_Research_Audit.json','reports':len(stems),'cited_source_names':len(ids),'network_requests':0,'method':'public literature/API/source static research; no SDK/model/board/robot testing'}
v['pending_evidence']+=['上交所财报原件浏览器校验；本次无收入/利润/市场份额数字','模型权重/HF部分资料未取得及许可待核','完整目标BSP、关键芯片TRM和逐SKU软件/供货合同','完整当期政策与出海SKU/用途判定不在已取得有限证据内']
(s/'progress.json').write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
print('FINAL',len(stems),'reports',len(ids),'cited source names; approved01 unchanged; network=0; index links',len(targets))
