import pathlib,json,shutil,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8')
root=pathlib.Path(__file__).resolve().parent.parent;p=root/'01_Compute_Chips/05_Rockchip';a=p/'reference_metrial';s=p/'research_state'
quality=json.loads((a/'derived/qa/01_Hardware_Platform_quality.json').read_text(encoding='utf-8'))
assert quality['outcome']=='pass',quality['errors']
run=json.loads((a/'_registry/last_run.json').read_text(encoding='utf-8'))
assert run['network_requests_including_robots']==0,run
shutil.copy2(a/'_registry/last_run.json',a/'derived/qa/01_Hardware_Platform_dedup_last_run.json')
registry=json.loads((a/'_registry/materials.json').read_text(encoding='utf-8'))
trace=json.loads((s/'evidence/01_Hardware_Platform.json').read_text(encoding='utf-8'))
progress=dict(platform='Rockchip 瑞芯微',scope='01硬件平台；02—09按序在01审阅通过后继续',data_cutoff='2026-11-05 Asia/Shanghai；逐原件以archived_at_utc为准',source_collection_utc_range=[min(registry[n]['archived_at_utc'] for n in trace['source_ids']),max(registry[n]['archived_at_utc'] for n in trace['source_ids'])],authorization='用户：先完成01供我审阅，通过后继续。未批准02启动。',review_status='01 awaiting_user_review; not approved',completed_dimensions=['01'],current_dimension='01',pending_evidence=['完整SoC datasheet/TRM与热设计/结温阈值','逐SKU持续DDR带宽和准确NPU功率/稀疏口径','VLA模型commit/量化/输入/动作chunk/完整计时和真实成功率','ROCK5T工业温度测试及功能安全资料','板卡改版PCN/EOL、逐料号供货与SDK维护','各配置正式含税报价/库存/交期','网页部分静态依赖缺失、视频/动态交互未完整归档'],next_step='等待用户审阅01。仅在明确通过后开始02软件栈总览与独立专题；不改写其他现有章节。',figures_reviewed=7,source_count=len(trace['source_ids']),dedup=dict(network_requests=0,record='reference_metrial/derived/qa/01_Hardware_Platform_dedup_last_run.json'),completion_note='公开文献/原件研究完成，不代表实机、采购或功能安全验收。')
progress['validation']=dict(outcome=quality['outcome'],body_han_chars=quality['body_han_chars'],tables=quality['tables'],file_hash_checks=quality['file_hash_checks'],html_visible_text_equal=quality['html_visible_text_equal'],other_reports_unchanged=quality['other_reports_unchanged'],static_dependency_warning_count=len(quality['warnings']),semantic_review='人工核对关键规格/版本/测量条件及7张官方图；未进行实机验证')
(s/'progress.json').write_text(json.dumps(progress,ensure_ascii=False,indent=2),encoding='utf-8')
print('Dedup verified:',run['summary'],'network=0; state awaiting user review')
