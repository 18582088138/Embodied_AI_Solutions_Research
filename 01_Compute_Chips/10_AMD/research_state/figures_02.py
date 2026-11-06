"""Prepare official chapter 02 diagrams from existing archives. No network."""
import json,pathlib,subprocess,hashlib,shutil
P=pathlib.Path(__file__).resolve().parents[1]; A=P/'reference_metrial'
R=json.loads((A/'_registry/materials.json').read_text(encoding='utf-8'))
S=json.loads((A/'_registry/assets.json').read_text(encoding='utf-8'))
O=A/'derived/figures'; O.mkdir(parents=True,exist_ok=True); figures=[]
def record(slug,sid,url,original,out,op):
 figures.append(dict(slug=slug,source_id=sid,source_url=url,original_file=original.as_posix(),original_sha256=hashlib.sha256(original.read_bytes()).hexdigest(),file=out.as_posix(),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),operation=op))
for slug,sid,url in [
 ('02_ryzen_ai_stack','AMD_RyzenAI_Docs','https://ryzenai.docs.amd.com/en/latest/_images/rai-sw.png'),
 ('02_vitis_design_flow','AMD_Vitis_Product','https://www.amd.com/content/dam/amd/en/images/charts/2772134-vitis-design-flow-chart.png'),
 ('02_xrt_layers','AMD_XRT_Docs','https://xilinx.github.io/XRT/master/html/_images/XRT-Layers.svg'),
 ('02_vart_ml_architecture','AMD_VitisAI_Gen2_Architecture','https://vitisai.docs.amd.com/projects/gen2/en/latest/_images/vart_ml_architecture.png'),
 ('02_vart_async','AMD_VitisAI_Gen2_Async','https://vitisai.docs.amd.com/projects/gen2/en/latest/_images/sync_vs_async_overlap.svg'),
 ('02_vek385_system','AMD_VitisAI_Gen2_Reference','https://vitisai.docs.amd.com/projects/gen2/en/latest/_images/system-flow.png')]:
 asset=next(a for a in R[sid]['assets'] if a['url']==url)
 orig=A/asset.get('local_file',asset['file']); out=O/(slug+'.png')
 if orig.suffix=='.svg':
  assert b'foreignObject' not in orig.read_bytes(),'SVG foreignObject requires browser rendering'
  subprocess.run(['magick','-background','white',str(orig),str(out)],check=True)
 else: shutil.copyfile(orig,out)
 record(slug,sid,url,orig,out,'原PNG无修改复制' if orig.suffix!='.svg' else 'ImageMagick MSVG渲染完整SVG；未裁剪')
for page,slug in [(16,'02_edf_stack'),(20,'02_edf_artifacts'),(24,'02_shel_flow')]:
 sid='AMD_EDF_Overview_PDF'; orig=pathlib.Path(R[sid]['file']); prefix=O/slug
 subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-r','150','-png',str(orig),str(prefix)],check=True)
 record(slug,sid,R[sid]['url'],orig,prefix.with_suffix('.png'),f'Poppler 150dpi完整渲染PDF第{page}页；未裁剪')
(P/'research_state/figure_manifest_02.json').write_text(json.dumps(figures,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(figures,ensure_ascii=False,indent=2))
