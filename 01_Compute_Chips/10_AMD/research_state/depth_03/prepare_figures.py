import json,pathlib,hashlib,shutil
D=pathlib.Path(__file__).resolve().parent;P=D.parents[1];A=P/'reference_metrial';O=A/'derived/figures';O.mkdir(exist_ok=True)
R=json.loads((A/'_registry/materials.json').read_text(encoding='utf8'))
items=[('MV_Top','AMD_MV_HW','Top_level_hardware_architecture.png'),('MV_Capture','AMD_MV_HW','hw_arch_capture_pipeline.png'),('MV_ISP','AMD_MV_HW','hw_arch_isp_pipeline.png'),('MV_10G','AMD_MV_HW','hw_arch_10g_pipeline.png'),('MV_Wiring','AMD_MV_Deploy','KR260_SFP+_Host.jpg'),('PTP_HW','AMD_PTP_HW','hw_arch_gps.png'),('PTP_SW','AMD_PTP_SW','sw_arch_intro.png'),('TSN_HW','AMD_TSN_HW','hw_arch_tsn.png'),('TSN_Measure','AMD_TSN_HW','test_pmod.png')]
F=[]
for slug,s,end in items:
 a=next(x for x in R[s]['assets'] if x['url'].endswith('/'+end));src=A/a.get('local_file',a['file']);dst=O/('03_'+slug+src.suffix);shutil.copyfile(src,dst)
 h=hashlib.sha256(src.read_bytes()).hexdigest();assert h==a['sha256']
 F.append(dict(slug=slug,file=dst.as_posix(),sha256=h,source_id=s,source_url=a['url'],original_file=src.as_posix(),original_sha256=h,operation='从官方HTML归档asset逐字节复制PNG/JPG原图，无渲染、裁剪、重画或修改'))
(D/'figures.json').write_text(json.dumps(F,ensure_ascii=False,indent=2),encoding='utf8')
print('\n'.join(f['file'] for f in F))
