import pathlib,json,hashlib,datetime,subprocess,re,shutil
ROOT=pathlib.Path(__file__).resolve().parents[1];P=ROOT/'01_Compute_Chips/06_Huawei_HiSilicon';A=P/'reference_metrial';S=P/'research_state'
chapters=['01_Hardware_Platform','02_Software_Stack','03_Sensor_Integration','04_AI_Capabilities','05_Simulation_Environment','06_Robot_Integration','07_Ecosystem','08_Core_Technology_Moat','09_SWOT_Analysis']
topics=['02A_Ascend_CANN_Runtime','02B_Framework_Model_Deployment','02C_HiSilicon_BSP_MPP_NPU','02D_Robot_Integration_Operations','02E_CloudRobo_Development_Platform','08A_Ascend_Execution_Compilation','08B_HiSilicon_Media_Memory','08C_CloudRobo_Action_Learning']
reports=chapters+topics
def dump(path,value): path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf8')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def link(label,path): return '['+label+'](<'+path.as_posix()+'>)'
qa={n:json.loads((A/'derived/qa'/(n+'_quality.json')).read_text('utf8')) for n in reports}
assert all(q['outcome']=='pass' for q in qa.values())
assert sha(P/'01_Hardware_Platform.md')=='b13be8dbee593fb8b4314e5688ecb2a76f2e104524ddc6fb4b71e55b5ae1744e'
index=P/'02_Topics_Index.md'
if not (S/'revisions/02_Topics_Index_before.json').exists():
 dump(S/'revisions/02_Topics_Index_before.json',{f.name:sha(f) for f in P.glob('*.md')})
 shutil.copy2(index,S/'revisions/02_Topics_Index_before.md')
text=index.read_text('utf8').replace('总览与四篇专题均完成文献、原码、许可、图源与归档检查；完成不代表目标硬件已实测。用户追加授权继续剩余全部章节，下一步按03—09顺序推进。','总览与五篇专题均完成文献、源码、许可、图源与归档检查；完成不代表目标硬件已实测。后续发现的CloudRobo云开发已独立补为02E；01—09现均完成公开资料调研，只有01获用户审阅批准。').replace('联合46项引用','联合61项引用')
n='02E_CloudRobo_Development_Platform';q=qa[n]
block='## '+n+'\n\n'+link('专题正文',P/(n+'.md'))+'：工作空间与资源/权限、OBS/SWR/CCE/ModelArts分工、模型源—训练—注册—部署、R2C JSON/YAML生效与ROS2队列/同步、证书与成组回退。云训练/部署、本体端侧和A2/海思支持分别核验。\n\n'+str(q['body_han_chars'])+'有效正文汉字；'+str(q['sources'])+'项来源；'+str(q['figures'])+'张官方图；检查pass。'+link('主张/图源',S/'evidence'/(n+'.json'))+'；'+link('结构归档检查',A/'derived/qa'/(n+'_quality.json'))+'；'+link('专题去重复用',A/'derived/qa'/(n+'_dedup.json'))+'。\n\n'
if '## '+n not in text: text=text.replace('## 联合资料与使用方法',block+'## 联合资料与使用方法')
text=text.replace('旧2021教材、2023样例仓和2026框架固定提交分别限定版本；','旧2021教材、旧机器人示例、2026框架固定提交及CloudRobo网页采集快照分别限定版本；')
index.write_text(text,encoding='utf8')
dump(S/'revisions/02_Topics_Index_revision.json',{'reason':'补入已完成02E、联合61项及真实完成/审阅状态','sha256':sha(index)})
registry=json.loads((A/'_registry/materials.json').read_text('utf8'))
union={}
for n in reports:
 for sid in json.loads((S/'evidence'/(n+'.json')).read_text('utf8'))['source_ids']:
  assert registry[sid]['archive_status'] in ['complete_static','partial_static']
  union.setdefault(sid,[]).append(n)
dump(ROOT/'toolkit/manifests/Huawei_01_09_Final_Union.json',[{'name':sid,'url':registry[sid]['url'],'expected':'any','used_by':users} for sid,users in union.items()])
software=list(dict.fromkeys(sid for n in ['02_Software_Stack']+topics[:5] for sid in json.loads((S/'evidence'/(n+'.json')).read_text('utf8'))['source_ids']))
assert set(software)==set(json.loads((S/'evidence/02_Software_Stack.json').read_text('utf8'))['source_ids'])
dump(S/'evidence/final_rejected_and_pending.json',{
 'data_cutoff':'2026-11-05','not_effective_sources':{n:{'url':r['url'],'status':r.get('archive_status'),'error':r.get('error')} for n,r in registry.items() if r.get('archive_status')=='failed'},
 'navigation_or_dynamic_only_excluded':['CloudRobo_ResidualRL','CloudRobo_ResidualRobot','CloudRobo_ResidualData','CloudRobo_ResidualOnline','CloudRobo_RobotManagement','CloudRobo_SimAssets','CloudRobo_DataProduction','HiSilicon_DevCenter'],
 'browser_observation_only':{'source_id':'Huawei_NationalCenter_Case','url':registry['Huawei_NationalCenter_Case']['url'],'observed':'官方2026-07-20国地中心实训场公告；灵龙进入延锋完成实景采集/自主作业验证','status':'浏览器曾可见，归档robots不可检查/拒绝；未纳入有效引用','limits':'未取得台数、SKU、成功率、合同或ROI；观察记录不是归档原件'},
 'best_practice_pdf_limit':'CloudRobo_BestPracticePDF超过下载器大小限制，未保存截断件；使用已读具体网页子章节',
 'remaining':['A2准确料号/板号及正式电气热/生命周期文档','当前海思SDK、算子/量化支持、二进制商业许可及工业/安全等级','R2C/本体SDK完整发行包与许可、模型权重/数据/资产revision','目标SKU多sensor/视频/模型并发热稳定、观测年龄与闭环P99/失效实测','正式报价、MOQ/交期、PCN/EOL/备件及云合同包含量','客户合同/交付/在岗规模、全部尝试/人工干预/暴露小时与可归因收益','带地区时期分母的市场份额及逐SKU/最终用途/目的地现行出口分类']})
title=['硬件平台','软件栈总览','传感器接入','AI能力与模型地图','仿真环境','机器人本体适配','生态建设','核心技术护城河','SWOT与条件选型']
out='# Huawei / HiSilicon 具身智能平台调研总索引\n\n数据截止2026-11-05。01—09及02A—02E、08A—08C共17篇研究正文已完成公开资料、源码/模型卡、许可、图源和归档检查。仅01已获用户审阅批准；其余完成表示调研与自检完成，不代替用户批准、设备测试或商业放行。01原文SHA256核对未变，历史08_Proprietary_Technologies.md保留，正式08以本索引链接为准。\n\n'
out+='## 按01—09阅读\n\n|章节|正文|有效正文汉字|引用项|官方图|检查/证据|\n|---|---|---|---|---|---|\n'
for n,t in zip(chapters,title):
 q=qa[n];out+='|'+n[:2]+'|'+link(t,P/(n+'.md'))+'|'+str(q['body_han_chars'])+'|'+str(q['sources'])+'|'+str(q['figures'])+'|'+link('检查',A/'derived/qa'/(n+'_quality.json'))+' / '+link('证据',S/'evidence'/(n+'.json'))+'|\n'
out+='\n## 独立深度专题\n\n'+link('02专题索引',P/'02_Topics_Index.md')+'提供五篇软件专题的机制与交接说明。\n\n|专题|内容|字数/来源/图|核查入口|\n|---|---|---|---|\n'
descriptions=['ATC/OM、AscendCL内存与异步/动态档位','TorchNPU、MindSpore Lite、YOLO和vLLM支持边界','BSP/MPP、旧NNIE与多执行域/媒体许可','旧本体示例、消息/坐标/动作时效与运维','CloudRobo资源/权限、R2C生命周期、ROS2部署链','昇腾执行/编译、模型内存和机制对标','海思媒体帧/缓存、专用引擎及当前源码路径','CloudRobo动作/资产血缘、RLinf/Wan学习对照']
for n,d in zip(topics,descriptions):
 q=qa[n];out+='|'+link(n,P/(n+'.md'))+'|'+d+'|'+str(q['body_han_chars'])+' / '+str(q['sources'])+' / '+str(q['figures'])+'|'+link('检查',A/'derived/qa'/(n+'_quality.json'))+' / '+link('证据',S/'evidence'/(n+'.json'))+' / '+link('去重',A/'derived/qa'/(n+'_dedup.json'))+'|\n'
out+='\n## 主要发现与使用边界\n\nHuawei/HiSilicon能力分布于昇腾模型执行、海思视觉前端和CloudRobo云开发三层，三者不同设备与交付对象必须分别验收。服务器Atlas A2/910B不等于200I A2/310B；海思专用HNR/DPU不能视为任意模型可用通算力。\n\nCloudRobo已有SO101/PI05、UR5e残差强化及Q25路径的具体开发实践，并公开R2C JSON/YAML生效与ROS2队列规则。RLinf增加第三方910B/CANN9.1.1、CPU OSMesa及Wan世界模型学习路线，仍无310B或海思端侧同条件支持证明。\n\n09的TCO区分平台、模型、仿真、训练、存储/网络、本体及维护；50000/10000元仅为官方计费示例，不是正式现行报价。未获得市场份额、连续在岗规模和可归因ROI，不从合作/演示补数。数据出境按已归档监管原文及项目数据流判断，安全云功能不能代替机器人功能安全。\n\n## 资料、复核与版本修订\n\n'
out+=link('整套有效资料集合',A/'final_01_09/index.html')+'覆盖'+str(len(union))+'项联合有效来源；'+link('02联合61项',A/'02_software_depth/index.html')+'、'+link('08联合38项',A/'08_core/index.html')+'、'+link('09资料',A/'09_swot/index.html')+'复用唯一URL registry。HTML/PDF/源码/模型卡原件保留metadata和哈希，静态依赖缺失按实际状态披露，未保证动态登录、交互或像素级离线完整。\n\n'
out+=link('最终联合去重运行',A/'derived/qa/final_union_dedup.json')+'与'+link('最终整套审计',A/'derived/qa/final_package_audit.json')+'记录实际检查与请求统计。'+link('排除/失败/待取件清单',S/'evidence/final_rejected_and_pending.json')+'区别原文未披露、未取得、访问限制与版本不适用。\n\n'
out+='后续新证据已小范围补入02、04、05，原报告、前后哈希和修订基线存于'+link('修订记录',S/'revisions')+'。main/master快照与提交SHA/tag表述已统一核对。各篇最初基线和逐章检查保留；最终审计使用整套完成后的冻结基线，验证当前文件及资料一致性，不能替代最初保护基线。\n\n'
out+='仍需取得当前目标SKU正式手册/SDK/商业许可、准确模型与资产版本、同条件并发/热/闭环失效测试、正式价格/交期/生命周期、客户任务与运营收益及逐案区域政策分类。公开调研至此完成，工程和商业放行仍以项目实测与合同为准。\n'
(P/'Research_Index.md').write_text(out,encoding='utf8')
dump(S/'baselines/final_package_frozen.json',{f.name:sha(f) for f in P.glob('*.md')})
print('reports',len(reports),'union',len(union),'software union',len(software),'01 preserved')
