import json,pathlib,sys,hashlib
sys.stdout.reconfigure(encoding='utf-8');root=pathlib.Path(__file__).resolve().parents[1];p=root/'01_Compute_Chips/06_Huawei_HiSilicon';a=p/'reference_metrial';r=json.loads((a/'_registry/materials.json').read_text('utf-8'));topics=['02A_Ascend_CANN_Runtime','02B_Framework_Model_Deployment','02C_HiSilicon_BSP_MPP_NPU','02D_Robot_Integration_Operations']
def link(t,f):return '['+t+'](<'+f.as_posix()+'>)'
if sys.argv[1]=='config':
 traces=[json.loads((p/'research_state/evidence'/(t+'.json')).read_text('utf-8')) for t in topics]
 ids=list(dict.fromkeys(n for t in traces for n in t['source_ids']))
 cfg=dict(source_ids=ids,figures=[],claims=[c for t in traces for c in t['claim_review']],manual_review=dict(coverage='四个专题和总览逐篇完成；缺口显式保留',versions_and_measurements='固定提交、旧教材、当前产品分开；无实机测试',maturity_and_licenses='开发/量产、代码/文档/模型/二进制许可分开',figures_opened='总览复用专题解释；6张专题官方图及衍生图逐图实际打开，图源哈希在专题trace'))
 (root/'toolkit/manifests/Huawei_02_Software_Stack_config.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2),encoding='utf-8')
elif sys.argv[1]=='complete':
 union=json.loads((root/'toolkit/manifests/Huawei_02_Software_Stack.json').read_text('utf-8'));ids=[x['name'] for x in union]
 q={t:json.loads((a/'derived/qa'/(t+'_quality.json')).read_text('utf-8')) for t in topics+['02_Software_Stack']}
 assert all(x['outcome']=='pass' for x in q.values())
 run=json.loads((a/'_registry/last_run.json').read_text('utf-8'));(a/'derived/qa/02_Software_Stack_dedup.json').write_text(json.dumps(run,ensure_ascii=False,indent=2),encoding='utf-8')
 rejected=[]
 for n,reason in [('Huawei_CANN_Current','本地HTML主体只有导航，动态CANN正文未归档'),('Huawei_CANN921_Release','实际归档为产品公告正文占位，非发布内容'),('HiSilicon_MaterialsCenter','归档只有类别筛选；浏览器用于定位官方PDF，不引用列表正文')]:
  x=r[n];rejected.append(dict(source_id=n,url=x['url'],archive_status=x['archive_status'],reason=reason,original_file=x['original_file']))
 (p/'research_state/evidence/02_rejected_candidates.json').write_text(json.dumps(rejected,ensure_ascii=False,indent=2),encoding='utf-8')
 index='# 02 软件栈专题索引\n\n数据截止2026-11-05。总览与四篇专题均完成文献、原码、许可、图源与归档检查；完成不代表目标硬件已实测。用户追加授权继续剩余全部章节，下一步按03—09顺序推进。\n\n'+link('02软件栈总览',p/'02_Software_Stack.md')+'先给路径选择和版本/成熟度矩阵；下面按机制阅读。\n\n'
 descriptions=['ATC→OM、stub与真实runtime、context/stream、model descriptor/dataset及内存所有权；同步/异步完成、队列和动态档位。旧310官方样例作为API参考，当前310B目标不能直接套用。','TorchNPU设备/算子和图接入、构建/发行/维护版本分别判断；MindSpore Lite转换与CPU backup；YOLO静态FP16部署到InferSession；vLLM对200I A2的明确排除，AGPL/Apache/BSD/CCBY等许可分开。','BSP/OSDRV、VI/ISP/VPSS/VENC、SYS/VB/MMZ及cached buffer；旧NNIE Caffe/WK、CPU分段与RuyiStudio，当前3403第三方帧代码；OpenHarmony DV300端口与媒体EULA边界。','旧200DK+D435+Dobot和下棋/小车示例的真实分工；帧ID/曝光时刻、坐标反投影、动作期限、策略与伺服分层；容器主机依赖、并发观测、模型配置升级与OTA回退条件。']
 for t,d in zip(topics,descriptions):
  x=q[t];index+='\n## '+t+'\n\n'+link('专题正文',p/(t+'.md'))+'：'+d+'\n\n'+str(x['body_han_chars'])+'有效正文汉字；'+str(x['sources'])+'项来源；'+str(x['figures'])+'张官方图；检查'+x['outcome']+'。'+link('主张/图源',p/'research_state/evidence'/(t+'.json'))+'；'+link('结构归档检查',a/'derived/qa'/(t+'_quality.json'))+'；'+link('专题去重复用',a/'derived/qa'/(t+'_dedup.json'))+'。\n'
 index+='\n## 联合资料与使用方法\n\n'+link('本章有效资料集合',a/'02_software_depth/index.html')+'覆盖总览及所有专题联合'+str(len(ids))+'项引用，使用同一URL registry；collection仅建立复用视图。'+link('最终联合去重记录',a/'derived/qa/02_Software_Stack_dedup.json')+'保留实际请求统计，不用refresh模拟复用。'+link('排除候选日志',p/'research_state/evidence/02_rejected_candidates.json')+'保留空壳动态页，不将HTTP200等同有效正文。\n\n旧2021教材、2023样例仓和2026框架固定提交分别限定版本；代码、模型、资料及SDK的许可证不互相替代。官方图讲解可用来理解分层与流程，不能当同条件性能比较。所有专题声明未开展实机/本体测试；量产所需包、许可、并发性能和失效条件仍待实际验证。\n'
 (p/'02_Topics_Index.md').write_text(index,encoding='utf-8')
 state=json.loads((p/'research_state/progress.json').read_text('utf-8'));state.update(authorization='用户“继续02”，后追加“继续后面全部内容的调研”；剩余03—09连续授权，不再设置逐章批准门槛',current_dimension='03_Sensor_Integration',data_cutoff='2026-11-05',next_step='按03→09逐章研究、归档、图片和质量验收；当前03尚未开始正文')
 state['completed_dimensions']=list(dict.fromkeys(state.get('completed_dimensions',[])+['02_Software_Stack']))
 state['software_depth_topics']=dict(planned_topics=topics,completed_topics=topics,current_topic=None,review_status='完成待用户阅读；未记录用户对02逐项批准',checks={t:{k:v for k,v in q[t].items() if k in ['outcome','body_han_chars','sources','figures','errors','warnings']} for t in q},union_sources=ids,collection=(a/'02_software_depth/index.html').as_posix())
 (p/'research_state/progress.json').write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8');print('02 completed',len(ids),'union sources')
