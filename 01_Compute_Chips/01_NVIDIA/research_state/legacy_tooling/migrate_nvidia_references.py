"""Move report references to the project archive after unified downloads finish.

No network requests; leaves historical shared evidence intact for older reports.
"""
import hashlib,json,pathlib,shutil
from collections import Counter
from download_materials import presentation_status
ROOT=pathlib.Path(__file__).resolve().parents[2]
BASE=ROOT/'Embodied_AI_Solutions_Research'
OLD=BASE/'_Evidence'
NEW=BASE/'01_Compute_Chips/01_NVIDIA/reference_metrial'
if (NEW/'_registry/materials.json').exists():
    raise SystemExit('Legacy migration disabled for current archive layout. Use download_materials.py; do not copy old source files back.')
items=json.loads((BASE/'toolkit/manifests/NVIDIA_materials.json').read_text(encoding='utf-8'))
extracted=NEW/'_extracted';extracted.mkdir(exist_ok=True)
for item in items:
    record=json.loads((NEW/(item['name']+'.meta.json')).read_text(encoding='utf-8'))
    presentation_status(record)
    (NEW/(item['name']+'.meta.json')).write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
    assert record['archive_status']!='failed',item['name']
    assert pathlib.Path(record['file']).is_file(),item['name']
    assert hashlib.sha256(pathlib.Path(record['original_file']).read_bytes()).hexdigest()==record['original_sha256']
    for path in OLD.glob(item['name']+'_*'):
        if path.suffix=='.txt':shutil.copy2(path,extracted/path.name)
for name in ['NVIDIA_Official_Figure_Thor_SoC.png','NVIDIA_Official_Table_Thor_Compute.png','NVIDIA_Official_Table_Orin_NX.png','NVIDIA_Hardware_Baseline_Hashes.json']:
    shutil.copy2(OLD/name,NEW/name)
for filename in ['build_nvidia_hardware_report.py','check_nvidia_hardware_report.py']:
    path=ROOT/'scripts'/filename;text=path.read_text(encoding='utf-8')
    text=text.replace("E=BASE/'_Evidence'","E=BASE/'01_Compute_Chips'/'01_NVIDIA'/'reference_metrial'")
    path.write_text(text,encoding='utf-8')
path=ROOT/'scripts/inspect_nvidia_pdfs.py'
text=path.read_text(encoding='utf-8').replace("/'Embodied_AI_Solutions_Research'/'_Evidence'","/'Embodied_AI_Solutions_Research'/'01_Compute_Chips'/'01_NVIDIA'/'reference_metrial'")
text=text.replace("for path in root.glob('NVIDIA_*.pdf'):","out=root/'_extracted'\nout.mkdir(exist_ok=True)\nfor path in root.glob('NVIDIA_*.pdf'):")
text=text.replace("(root/(path.stem+","(out/(path.stem+")
path.write_text(text,encoding='utf-8')
body=ROOT/'research/nvidia_hardware_report_body.txt'
text=body.read_text(encoding='utf-8').replace('以下官方资料均保留原始响应，采集时间、最终URL、HTTP结果及SHA256保存在同名`.meta.json`。HTML另有正文抽取文件，PDF另有逐页文本；抽取文本用于检索，原PDF为版式/脚注核对依据。','以下资料统一保存到本项目的`reference_metrial`，由`toolkit/download_materials.py`下载/迁移。网页保留本地HTML及样式、图片等依赖，原始响应保存在`_original`；本地化前后静态可见文本一致性已校验。采集时间、最终URL、原始/本地SHA256、资源缺失与归档状态保存在同名`.meta.json`。`partial_static`表示部分依赖未取得，不代表完整离线呈现；动态API、交互和嵌入媒体也不保证离线可用。HTML另有正文抽取文件，PDF另有逐页文本；抽取文本用于检索，原PDF为版式/脚注核对依据。')
body.write_text(text,encoding='utf-8')
manifest={p.stem.removesuffix('.meta'):json.loads(p.read_text(encoding='utf-8')) for p in NEW.glob('*.meta.json')}
(NEW/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
run_path=NEW/'last_run.json'
run=json.loads(run_path.read_text(encoding='utf-8'))
run['summary_before_script_classification']=run['summary']
run['summary']=dict(Counter(record['archive_status'] for record in manifest.values()))
run['presentation_classification_tool']='toolkit/download_materials.py:presentation_status'
run_path.write_text(json.dumps(run,ensure_ascii=False,indent=2),encoding='utf-8')
print('Migrated reference paths and derivative files for',len(items),'NVIDIA sources')
