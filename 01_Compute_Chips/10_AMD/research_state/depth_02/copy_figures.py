import json,pathlib,hashlib,shutil,sys
D=pathlib.Path(__file__).resolve().parent;P=D.parents[1];A=P/'reference_metrial'
R=json.loads((A/'_registry/materials.json').read_text(encoding='utf-8'))
groups={'B':[('02B_xint8','AMD_Quark_XINT8','xint8_quantize.png'),('02B_search','AMD_Quark_Search','auto_search_diagram.png')],
 'C':[('02C_nchw','AMD_VAI_Tensor_Formats','tensor_float32_nchw.png'),('02C_hcwnc4','AMD_VAI_Tensor_Formats','tensor_float32_hcwnc4.png'),('02C_partitions','AMD_VAI_Partition_Analyzer','AIAnalyzer_PartitioningSummary.png')]}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
out=[]
for slug,sid,tail in groups[sys.argv[1]]:
 a=next(a for a in R[sid]['assets'] if a['url'].endswith('/'+tail));original=A/a.get('local_file',a.get('file'));dest=A/'derived/figures'/(slug+original.suffix)
 shutil.copyfile(original,dest)
 out.append(dict(slug=slug,source_id=sid,source_url=a['url'],original_file=original.as_posix(),original_sha256=sha(original),file=dest.as_posix(),sha256=sha(dest),operation='官方原PNG无修改复制，完整图无裁剪'))
(D/('figures_'+sys.argv[1]+'.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))
