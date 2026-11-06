import json,pathlib
root=pathlib.Path(__file__).resolve().parents[1];p=root/'01_Compute_Chips/06_Huawei_HiSilicon';r=json.loads((p/'reference_metrial/_registry/materials.json').read_text('utf-8'));rows=[]
for n,repo,files in [('HiView_TreeAPI','openhisilicon/HIVIEW',[('HiView_3403_VPSS','mod/svp/3403/vpss_capture.cpp'),('HiView_3403_SVP','mod/svp/3403/svp.c'),('HiView_3403_YOLO','mod/svp/3403/yolov8.cpp')]),('OH_HiSilicon_TreeAPI','openharmony/device_soc_hisilicon',[('OH_Media_EULA','hi3516dv300/sdk_linux/out/lib/LICENSE')])]:
 a=json.loads(pathlib.Path(r[n]['file']).read_text('utf-8'));paths={x['path'] for x in a['tree']}
 for name,f in files:
  assert f in paths,f;rows.append(dict(name=name,url='https://raw.githubusercontent.com/'+repo+'/'+a['sha']+'/'+f,expected='any',used_by=['02C_HiSilicon_BSP_MPP_NPU']))
(root/'toolkit/manifests/Huawei_HiSilicon_02_currentcode.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
