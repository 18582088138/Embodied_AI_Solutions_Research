"""Freeze chapter 02 QA and actual user review status. Offline; no other MD writes."""
import hashlib,json,pathlib,shutil
P=pathlib.Path(__file__).resolve().parents[1];Q=P/'reference_metrial/derived/qa'
quality=json.loads((Q/'02_Software_Stack_quality.json').read_text(encoding='utf-8'))
run=P/'reference_metrial/_registry/last_run.json';dedup=json.loads(run.read_text(encoding='utf-8'))
trace=json.loads((P/'research_state/evidence/02_Software_Stack.json').read_text(encoding='utf-8'))
assert quality['outcome']=='pass' and not quality['errors']
assert all(quality['other_reports_unchanged'].values())
assert dedup['network_requests_including_robots']==0 and not dedup['summary'].get('failed',0)
assert set(dedup['names'])==set(trace['source_ids'])
shutil.copyfile(run,Q/'02_Software_Stack_dedup_last_run.json')
registry=json.loads((P/'reference_metrial/_registry/materials.json').read_text(encoding='utf-8'))
excluded={
 'KRS_Repository':'错误ros-acceleration候选HTTP404；正确Xilinx/KRS已引用',
 'KRS_Docs':'JavaScript redirect，没有实质正文；实际sphinx文档另引用',
 'Kria_Ubuntu':'redirect壳，无实质正文', 'Kria_BootFW':'redirect壳，无实质正文',
 'Kria_OpenAMP':'redirect壳，无实质正文', 'KR260_Perception_Overview':'目录导航，无实际部署正文',
 'AMD_VitisAI_Gen2_ML_API':'API链接跳转说明，不能当API实质正文',
 'Kria_Apps_Docs':'根目录redirect/导航，采用实际KR260部署页'
}
log=dict(data_cutoff='2026-11-04 Asia/Shanghai',excluded_candidates=[dict(source_id=s,url=registry[s]['url'],
 registry_archive_status=registry[s]['archive_status'],reason=why) for s,why in excluded.items() if s in registry],
 partial_static=[dict(source_id=s,metadata_file=str(pathlib.Path(registry[s]['file']).parent/'metadata.json'),
  missing_dependencies=registry[s].get('unavailable_assets',{}),notes=registry[s].get('notes',[]))
  for s in trace['source_ids'] if registry[s]['archive_status']=='partial_static'],
 structural_review='正文/≤8列表、本地链接、73HTML文本一致、原件/依赖/图哈希已检查；01和README基线一致。首次6幅图证据指向共享asset池，现改为相同哈希的页面自包含asset路径后重跑通过；未改原HTML/PDF/图片。',
 semantic_review='89项关键主张逐项按官方正文、表和API复核；版本/图示旧产物/SDKenv/driver/1.8算子表/1.9beta保留边界。EULA2.1是section编号；segmented无需shell.json、DFX另需。',
 visual_review=trace['manual_review']['figures_opened'],
 non_measurements='没有安装SDK、接受EULA、获取模型权重、构建/刷板/运行模型/机器人实机测试；样例sanity与厂商speedup不算本次实测。',
 dedup='对最终74个引用重新默认运行统一下载器，网络请求（含robots）为0；成功资料复用，无refresh/repair。')
(Q/'02_Software_Stack_research_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf-8')
# Make the working figure manifest carry the same registry-proven original path.
fpath=P/'research_state/figure_manifest_02.json';figs=json.loads(fpath.read_text(encoding='utf-8'))
for f in figs:
 t=next(x for x in trace['figures'] if x['file']==f['file']);f['original_file']=t['original_file']
fpath.write_text(json.dumps(figs,ensure_ascii=False,indent=2),encoding='utf-8')
progress_path=P/'research_state/progress.json';progress=json.loads(progress_path.read_text(encoding='utf-8'))
old=progress.get('chapter_summary',{})
summaries=progress.setdefault('chapter_summaries',{})
if '01_Hardware_Platform' not in summaries and old.get('report_sha256')=='9ef3c3adbe7bbc9c2cc7d1ed9a957ad3e694465f7de1744dcf910b4ea59d50f5':summaries['01_Hardware_Platform']=old
summary=dict(body_han_chars=quality['body_han_chars'],tables=quality['tables'],sources=quality['sources'],figures=quality['figures'],
 claim_reviews=len(trace['claim_review']),archive_status=quality['archive_status'],quality_errors=0,dedup_network_requests=0,
 report_sha256=hashlib.sha256((P/'02_Software_Stack.md').read_bytes()).hexdigest())
summaries['02_Software_Stack']=summary
progress.update(scope='AMD具身智能软硬件平台，01—09逐章；已完成01/02，03未开始',
 data_cutoff='2026-11-04 Asia/Shanghai',authorization='用户已审阅01并明确“继续02调研”；本次仅完成02，交用户审阅后继续。',
 review_status='awaiting_02_review',approved_dimensions=['01_Hardware_Platform'],completed_dimensions=['01_Hardware_Platform','02_Software_Stack'],
 current_dimension='02_Software_Stack',next_dimension='03_Sensor_Integration',
 next_step='等待用户审阅02；明确通过/授权后才按序开始03_Sensor_Integration。',chapter_summary=summary)
prior=[x for x in progress.get('pending_evidence',[]) if not x.startswith('代码/runtime/权重')]
progress['pending_evidence']=prior+[
 'RyzenAI1.9beta/driver最低行/EP option命名冲突，支持算子页仍标1.8；需实际包release与兼容验证',
 'EmbeddedX100/X199逐SKU ROCm/NPU兼容与新RoboticsSoftwareSuite唯一BSP/release/model manifest未取得',
 'Gen2SDK环境路径与图中ELF/cache残留；默认产物采用6.3.rai，仍需实板包/许可确认',
 '目标VLA动态图/算子/fallback/workspace、完整相机DMA路径、并发/热稳态/P99与机器人闭环未实测',
 'EDF生产维护需自维护/OSV责任；OTA/安全boot/回退/CVE与boot/PL/model兼容集成未验证',
 '模型代码/权重/数据/资产/本体SDK和实际下载二进制的具体license/SBOM仍需逐对象取得']
progress['qa_files']=list(dict.fromkeys(progress.get('qa_files',[])+[str(Q/x) for x in ['02_Software_Stack_quality.json','02_Software_Stack_dedup_last_run.json','02_Software_Stack_research_log.json']]))
progress_path.write_text(json.dumps(progress,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(review_status=progress['review_status'],summary=summary),ensure_ascii=False))
