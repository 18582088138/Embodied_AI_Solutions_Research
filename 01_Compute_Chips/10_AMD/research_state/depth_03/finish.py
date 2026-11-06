"""Freeze verified chapter 03 and stage audit, without altering reports."""
import pathlib,json,hashlib,shutil,collections,datetime
D=pathlib.Path(__file__).resolve().parent;P=D.parents[1];A=P/'reference_metrial';Q=A/'derived/qa';S='03_Sensor_Integration'
q=json.loads((Q/(S+'_quality.json')).read_text(encoding='utf8'));e=json.loads((P/'research_state/evidence'/(S+'.json')).read_text(encoding='utf8'))
last=A/'_registry/last_run.json';r=json.loads(last.read_text(encoding='utf8'))
assert q['outcome']=='pass' and not q['errors'] and all(q['other_reports_unchanged'].values())
assert r['network_requests_including_robots']==0 and not r['summary']['failed'] and set(r['names'])==set(e['source_ids'])
shutil.copyfile(last,Q/(S+'_dedup_last_run.json'))
R=json.loads((A/'_registry/materials.json').read_text(encoding='utf8'));candidates=[]
for path in sorted((P.parents[1]/'toolkit/manifests').glob('AMD_03_stage*.json')):
 for m in json.loads(path.read_text(encoding='utf8')):
  s=m['name'];v=R.get(s,{});mp=pathlib.Path(v['file']).parent/'metadata.json' if v.get('file') else None
  md=json.loads(mp.read_text(encoding='utf8')) if mp and mp.exists() else {}
  candidates.append(dict(source_id=s,stage_manifest=path.as_posix(),used=s in e['source_ids'],status=v.get('status'),archive_status=v.get('archive_status'),url=m['url'],notes=v.get('notes',[]),failure_reason=v.get('failure_reason',md.get('failure_reason')),unavailable_assets=v.get('unavailable_assets',{}),metadata_file=mp.as_posix() if mp else None))
excluded={
 'AMD_KV260_Interfaces':'取得JS loading壳，未作有效正文引用',
 'AMD_KR260_TSN':'redirect定位页，转至v0.3深层指南引用',
 'AMD_Wiki_Video':'目录导航仅定位', 'AMD_Wiki_Linux':'目录导航仅定位',
 'ROS_03_IMU':'原在线文档归档失败；未重试/未有效引用', 'ROS_03_PointCloud':'原在线文档归档失败；未重试/未有效引用', 'ROS_03_Image':'原在线文档归档失败；未重试/未有效引用','ROS_03_JointState':'原在线文档归档失败；未重试/未有效引用','ROS_03_Wrench':'原在线文档归档失败；未重试/未有效引用'}
summary=dict(body_han_chars=q['body_han_chars'],tables=q['tables'],sources=q['sources'],figures=q['figures'],claim_reviews=len(e['claim_review']),archive_status=q['archive_status'],quality_errors=0,dedup_network_requests=0,report_sha256=hashlib.sha256((P/(S+'.md')).read_bytes()).hexdigest())
log=dict(chapter=S,data_cutoff='2026-11-04',completed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='用户继续03；不开始04，不覆盖01/02',summary=summary,method='官方产品/教程→API/源码→图像实际复核→引用与精确短引→分析独立复算→结构归档检查→最终实际引用去重',candidates=candidates,excluded_candidates=excluded,limits=['28份partial_static保留已取得可读正文，CSS/字体/脚本等缺失见metadata，不保证像素/动态交互完整','linux-xlnx DMA页面可见源码不完整，master未绑定BSP','未下载/安装SDK或整container、未接受协议、未刷板或实测','ROS在线message页面失败未作有效引用；消息契约仅建议设计','多sensor目标SKU/driver qualification及同步误差缺口见正文'],corrections=['逐张打开MV Top/Capture发现IMX574误标，按其他器件证据研究IMX547并保留冲突','实际打开MV_SW media图：文件名含MIPI，图内imx547/subset/ISP/capture逻辑链，无CSI Rx；已纠正按文件名推PHY的初稿','精确短引避开目录导航，关键framecomplete、DMA、TSN、chrony与GPL证据对照实际正文'],other_reports_unchanged=q['other_reports_unchanged'],final_dedup=dict(names_count=len(r['names']),network_requests_including_robots=0,summary=r['summary']))
(Q/(S+'_research_log.json')).write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf8')
fp=P/'research_state/progress.json';p=json.loads(fp.read_text(encoding='utf8'))
p['current_dimension']=S;p['review_status']='03_awaiting_review';p['authorization']='用户明确“继续03”：完成03供审阅；本次不启动04，不代用户批准02或03。'
if S not in p['completed_dimensions']:p['completed_dimensions'].append(S)
p.setdefault('chapter_summaries',{})[S]=summary;p['chapter_summary']=summary
p['data_cutoff']='2026-11-04';p['next_step']='等待用户审阅03；明确授权继续后按顺序开始04，不提前创建04稿。'
p['sensor_integration_review']=dict(report=(P/(S+'.md')).as_posix(),status='awaiting_user_review',collection=(A/'03_sensors').as_posix(),source_catalog=(D/(S+'_sources.json')).as_posix(),evidence=(P/'research_state/evidence'/(S+'.json')).as_posix(),summary=summary)
p['pending_evidence']=list(dict.fromkeys(p.get('pending_evidence',[])+['03：X199平台FAKRA桥接芯片、BSP、相机型号/模式与统一buffer交付尚未取得','03：目标RGBD/ToF/LiDAR/Radar/IMU/力触觉关节设备SKU驱动、标定与故障契约需验证','03：camera/PTP/TSN联合设计、触发/曝光timestamp、并发P99/age与持续运行需实机验证','03：MV正式第三方IP许可、热插拔/second-load故障和版本冲突尚未消歧','03：源码浮动快照、DMA部分文件与实际BSP绑定commit、完整container/license/SBOM尚未核']))
new=[Q/(S+'_quality.json'),Q/(S+'_dedup_last_run.json'),Q/(S+'_research_log.json')]
p['qa_files']=list(dict.fromkeys(p.get('qa_files',[])+[x.as_posix() for x in new]));fp.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(dict(summary=summary,review_status=p['review_status'],completed=p['completed_dimensions'],approved=p.get('approved_dimensions',[]),network_requests=0),ensure_ascii=False))
