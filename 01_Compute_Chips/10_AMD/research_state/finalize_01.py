"""Freeze successful chapter QA, record actual review status. No network."""
import hashlib,json,pathlib,shutil
P=pathlib.Path(__file__).resolve().parents[1]
Q=P/'reference_metrial/derived/qa'
quality=json.loads((Q/'01_Hardware_Platform_quality.json').read_text(encoding='utf-8'))
run=P/'reference_metrial/_registry/last_run.json'
dedup=json.loads(run.read_text(encoding='utf-8'))
evidence=json.loads((P/'research_state/evidence/01_Hardware_Platform.json').read_text(encoding='utf-8'))
assert quality['outcome']=='pass' and not quality['errors']
assert dedup['network_requests_including_robots']==0 and not dedup['summary'].get('failed',0)
assert set(dedup['names'])==set(evidence['source_ids'])
shutil.copyfile(run,Q/'01_Hardware_Platform_dedup_last_run.json')
registry=json.loads((P/'reference_metrial/_registry/materials.json').read_text(encoding='utf-8'))
excluded=['AMD_K26_DS987','AMD_K26_Thermal_UG1090','OpenNav_Full_Report','AMD_Kria_Selection','AMD_Versal_DS950']
log=dict(data_cutoff='2026-11-04 Asia/Shanghai',excluded_candidates=[dict(source_id=s,url=registry[s]['url'],
    registry_archive_status=registry[s]['archive_status'],reason=registry[s].get('error') or '导航门户shell，未取得可引用完整文档正文') for s in excluded],
    partial_static=[dict(source_id=s,metadata_file=str(pathlib.Path(registry[s]['file']).parent/'metadata.json')) for s in evidence['source_ids'] if registry[s]['archive_status']=='partial_static'],
    visual_review='7幅已逐张打开。P100汽车频率PDF可视表为3.65，不能采用有误摘要。PSG元数据/门户日期不作为本地PDF正式发布日期。',
    check_execution='首次检查已写出pass QA，但控制台cp1252无法打印中文；使用Python -X utf8重跑，返回0。未改toolkit脚本。',
    semantic_review='人工核对39项关键主张，保留版本、精度、代理、投影、温度、功耗、成熟度与许可边界；没有硬件实机测试。')
(Q/'01_Hardware_Platform_research_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf-8')
progress=dict(platform='AMD',scope='具身智能软硬件平台，01—09逐章；当前只完成01硬件平台',
    data_cutoff='2026-11-04 Asia/Shanghai',authorization='用户明确：先完成01供审阅，通过后继续；不授权并行章节或研究子代理',
    review_status='awaiting_user_review',approved_dimensions=[],completed_dimensions=['01_Hardware_Platform'],
    current_dimension='01_Hardware_Platform',next_dimension='02_Software_Stack',
    pending_evidence=[
        'K26 DS987/UG1090附件受robots限制，未取得可归档完整手册；未作为有效引用',
        'OpenNav完整technical PDF被重定向目标访问规则拒绝；公开文章已归档，完整数据/commit与低功率结果未复核',
        'X100官网公开brief保留Confidential/无正式revision/PID；X188i L3与部分接口需正式版消歧',
        'K26网页与PSG频率、K24典型/最大功率、1066Mb/s单位、Embedded总览与专门brief及VEK命名冲突',
        'Kria AI开发平台仍Notify Me；未取得准确P/N、价格、确定交期、FPGA确切SKU/BOM/尺寸/环境与整机功率',
        'P100逐SKU量产交付、部分裸SoC制程/封装/容量/热与价格、目标模型完整时延/成功率需进一步证据',
        '代码/runtime/权重/数据/资产/本体SDK许可及实际软件支持矩阵留待获批02—06核验'
    ],
    next_step='等待用户审阅01；只有明确通过后才开展02_Software_Stack，继续遵循逐章深度与统一资料归档标准。',
    chapter_summary=dict(body_han_chars=quality['body_han_chars'],tables=quality['tables'],sources=quality['sources'],
        figures=quality['figures'],claim_reviews=len(evidence['claim_review']),archive_status=quality['archive_status'],
        quality_errors=0,dedup_network_requests=0,
        report_sha256=hashlib.sha256((P/'01_Hardware_Platform.md').read_bytes()).hexdigest()),
    qa_files=[str(Q/x) for x in ['01_Hardware_Platform_quality.json','01_Hardware_Platform_dedup_last_run.json','01_Hardware_Platform_research_log.json']])
(P/'research_state/progress.json').write_text(json.dumps(progress,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(progress['chapter_summary'],ensure_ascii=False))
