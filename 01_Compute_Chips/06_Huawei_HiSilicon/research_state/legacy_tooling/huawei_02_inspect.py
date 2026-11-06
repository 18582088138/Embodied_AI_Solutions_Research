import pathlib,json,sys,re
sys.stdout.reconfigure(encoding='utf-8');root=pathlib.Path(__file__).resolve().parents[1];p=root/'01_Compute_Chips/06_Huawei_HiSilicon';r=json.loads((p/'reference_metrial/_registry/materials.json').read_text('utf-8'))
if sys.argv[1]=='pin':
 groups=[('Ascend_Pytorch_TreeAPI','Ascend/pytorch',[('TorchNPU_Version','version.txt')]),('OH_HiSilicon_TreeAPI','openharmony/device_soc_hisilicon',[('OH_HiSilicon_README','README.md'),('OH_DV300_README','hi3516dv300/README_zh.md'),('OH_Driver_License','hi3516dv300/sdk_linux/drv/LICENSE')])]
 rows=[]
 for tree,repo,files in groups:
  a=json.loads(pathlib.Path(r[tree]['file']).read_text('utf-8'));paths={x['path'] for x in a['tree']}
  for n,f in files:
   assert f in paths;rows.append(dict(name=n,url='https://raw.githubusercontent.com/'+repo+'/'+a['sha']+'/'+f,expected='any',used_by=['02_Software_Stack']))
 a=json.loads(pathlib.Path(r['HiView_TreeAPI']['file']).read_text('utf-8'))
 candidates=[x['path'] for x in a['tree'] if x['type']=='blob' and re.search('svp.*(cv610|3403|dv500|v3).*\\.(c|cpp)$',x['path'],re.I)]
 print('SVP candidates',candidates[:25]);print('License files',[x['path'] for x in a['tree'] if 'license' in x['path'].lower()])
 (root/'toolkit/manifests/Huawei_HiSilicon_02_pin.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
elif sys.argv[1]=='pdf':
 from pypdf import PdfReader
 out=p/'reference_metrial/derived/extracted';out.mkdir(exist_ok=True)
 for n in sys.argv[2:]:
  a=PdfReader(r[n]['file']);t='\n'.join('PAGE '+str(i+1)+'\n'+(pg.extract_text() or '') for i,pg in enumerate(a.pages));(out/(n+'.txt')).write_text(t,encoding='utf-8');print(n,len(a.pages),'pages\n',t[:18000])
elif sys.argv[1]=='brief':
 for n in sys.argv[2:]:
  t=pathlib.Path(r[n]['file']).read_text('utf-8',errors='replace');print('\nSOURCE',n,'\n',t[:9000])
else:
 pat=sys.argv[2]
 for n in sys.argv[3:]:
  f=pathlib.Path(r[n]['file']);f=f.parent/'text.txt' if f.suffix=='.html' else f
  lines=f.read_text('utf-8',errors='replace').splitlines();found=set()
  for i,l in enumerate(lines):
   if re.search(pat,l,re.I):found.update(range(max(0,i-2),min(len(lines),i+5)))
  print('\nSOURCE',n);print('\n'.join(str(i+1)+': '+lines[i] for i in sorted(found))[:14000])
