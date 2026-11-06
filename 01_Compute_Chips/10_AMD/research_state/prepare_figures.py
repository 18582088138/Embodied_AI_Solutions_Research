"""Create traceable figures from already archived assets/PDFs, without network."""
import hashlib, json, pathlib, shutil, subprocess
PROJECT=pathlib.Path(__file__).resolve().parents[1]
ARCHIVE=PROJECT/'reference_metrial'
records=json.loads((ARCHIVE/'_registry/materials.json').read_text(encoding='utf-8'))
out=ARCHIVE/'derived/figures';out.mkdir(parents=True,exist_ok=True)
figures=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def asset(source,slug,suffix):
    record=records[source]
    a=next(a for a in record['assets'] if a['url'].endswith(suffix))
    original=ARCHIVE/a.get('local_file',a['file'])
    file=out/(slug+original.suffix)
    shutil.copy2(original,file)
    figures.append(dict(slug=slug,file=file.as_posix(),sha256=sha(file),source_id=source,
      source_url=a['url'],original_file=original.as_posix(),original_sha256=sha(original),operation='原始官方图片，本地副本，未裁剪或改图'))
def pdf(source,slug,page):
    record=records[source];original=pathlib.Path(record['file']);prefix=out/slug
    subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-scale-to','2200','-png',str(original),str(prefix)],check=True)
    file=prefix.with_suffix('.png')
    figures.append(dict(slug=slug,file=file.as_posix(),sha256=sha(file),source_id=source,
      source_url=record['url'],original_file=original.as_posix(),original_sha256=sha(original),operation=f'PDF第{page}页全页渲染，pdftoppm -scale-to 2200 -png；未裁剪'))
asset('AMD_Robotics','AMD_robotics_scope','4997850-robotics-image.png')
asset('AMD_Kria_AI','AMD_Kria_AI_ports','4997850-kria-ai-robotics-angled-ports.png')
asset('AMD_Versal_AI_Edge_Gen2','AMD_Versal_Gen2_block','2574740-versal-ai-edge-series-gen2-block-diagram.jpg')
pdf('AMD_P100_Brief','AMD_P100_table',3)
pdf('AMD_X100_Brief','AMD_X100_table',2)
pdf('AMD_Kria_Selection_PDF','AMD_Kria_SOM_table',3)
pdf('AMD_Kria_Selection_PDF','AMD_Kria_kit_table',4)
pdf('AMD_Embedded_8000_Brief','AMD_R8000_block',2)
(PROJECT/'research_state/figure_manifest.json').write_text(json.dumps(figures,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps([{'slug':f['slug'],'file':f['file']} for f in figures],indent=2))
