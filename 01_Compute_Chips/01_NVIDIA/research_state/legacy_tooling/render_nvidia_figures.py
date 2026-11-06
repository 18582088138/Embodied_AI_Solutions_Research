"""Render official PDF pages from the current archive; no downloads."""
import json,pathlib
import pypdfium2 as pdfium
from download_materials import digest,save_json
root=pathlib.Path(__file__).resolve().parents[1]/'01_Compute_Chips/01_NVIDIA/reference_metrial'
records=json.loads((root/'_registry/materials.json').read_text(encoding='utf-8'))
out=root/'derived/figures';out.mkdir(parents=True,exist_ok=True)
provenance=[]
for image,name,page in [
 ('NVIDIA_Official_Figure_Thor_SoC.png','NVIDIA_Technical_Brief_Robotics_Edge_AI',12),
 ('NVIDIA_Official_Table_Thor_Compute.png','NVIDIA_Datasheet_Thor_Full_v1_5',8),
 ('NVIDIA_Official_Table_Orin_NX.png','NVIDIA_Datasheet_Orin_NX_v1_7',7)]:
    record=records[name];document=pdfium.PdfDocument(record['file'])
    pdfpage=document[page-1];bitmap=pdfpage.render(scale=2)
    bitmap.to_pil().save(out/image)
    bitmap.close();pdfpage.close();document.close()
    provenance.append({'image':image,'source_url':record['url'],'source_file':record['file'],'source_sha256':record['sha256'],'pdf_page':page,'image_sha256':digest((out/image).read_bytes())})
    print('Rendered',image)
save_json(out/'provenance.json',provenance)
