import json,pathlib,sys
sys.stdout.reconfigure(encoding='utf-8')
root=pathlib.Path(__file__).resolve().parents[1];p=root/'01_Compute_Chips/06_Huawei_HiSilicon'
r=json.loads((p/'reference_metrial/_registry/materials.json').read_text('utf-8'))
rows=[]
if sys.argv[1]=='pdf':
 for n,h in [('HiSilicon_Taurus_PDF','fc2eadf9366b49058f5c8a91edcf1b13'),('HiSilicon_LiteOS_PDF','5103be8a8500426e8b60325acbfc9359'),('HiSilicon_DV300_SDK_PDF','7c925d6a091b49b5b1d1b0dc28d6dc4b'),('HiSilicon_DV300_Media_PDF','2a1c6e800feb43f4a8a31f8bcdcdc84a'),('HiSilicon_DV300_SVP_PDF','4ef2e012655a4aae8c80619b8cfd093f')]:
  rows.append(dict(name=n,url='https://www.hisilicon.com/dam/asset/view/'+h+'.pdf/download',expected='pdf',used_by=['02C_HiSilicon_BSP_MPP_NPU']))
elif sys.argv[1]=='trees':
 for n in ['HiView','OH_HiSilicon']:
  a=json.loads(pathlib.Path(r[n+'_RepoAPI']['file']).read_text('utf-8'))
  rows.append(dict(name=n+'_TreeAPI',url='https://api.github.com/repos/'+a['full_name']+'/git/trees/'+a['default_branch']+'?recursive=1',expected='json',used_by=['02C_HiSilicon_BSP_MPP_NPU']))
elif sys.argv[1]=='files':
 for n,repo,files in [('HiView','openhisilicon/HIVIEW',[('HiView_README','README.md')]),('OH_HiSilicon','openharmony/device_soc_hisilicon',[('OH_HiSilicon_README','README_zh.md'),('OH_HiSilicon_License','LICENSE')])]:
  a=json.loads(pathlib.Path(r[n+'_TreeAPI']['file']).read_text('utf-8'));paths={x['path'] for x in a['tree']}
  for name,f in files:
   if f not in paths: print('NOT FOUND',f);continue
   rows.append(dict(name=name,url='https://raw.githubusercontent.com/'+repo+'/'+a['sha']+'/'+f,expected='any',used_by=['02C_HiSilicon_BSP_MPP_NPU']))
else:
 for n in sys.argv[2:]:
  a=json.loads(pathlib.Path(r[n]['file']).read_text('utf-8'));print(n,a['sha'])
  print('\n'.join(x['path'] for x in a['tree'] if any(t in x['path'].lower() for t in ['license','readme','svp','npu','mpp']) and x['type']=='blob')[:18000])
 exit()
f=root/'toolkit/manifests'/('Huawei_HiSilicon_02_'+sys.argv[1]+'.json');f.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8');print(f)
