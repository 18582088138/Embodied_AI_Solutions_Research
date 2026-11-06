import pathlib,json,sys,hashlib
sys.stdout.reconfigure(encoding='utf-8')
ROOT=pathlib.Path(__file__).resolve().parents[1]
P=ROOT/'01_Compute_Chips/06_Huawei_HiSilicon'
R=json.loads((P/'reference_metrial/_registry/materials.json').read_text('utf-8'))
def manifest(name,rows):
 f=ROOT/'toolkit/manifests'/name
 f.write_text(json.dumps([dict(name=n,url=u,expected=e,used_by=['02_Software_Stack']) for n,u,e in rows],ensure_ascii=False,indent=2),encoding='utf-8');print(f)
if sys.argv[1]=='initial':
 manifest('Huawei_HiSilicon_02_discovery.json',[
 ('Huawei_CANN_Current','https://www.hiascend.com/cann','html'),
 ('Huawei_CANN921_Release','https://www.hiascend.com/productbulletins/detail/833','html'),
 ('Ascend_Samples_RepoAPI','https://api.github.com/repos/Ascend/samples','json'),
 ('Ascend_Pytorch_RepoAPI','https://api.github.com/repos/Ascend/pytorch','json'),
 ('MindSpore_RepoAPI','https://api.github.com/repos/mindspore-ai/mindspore','json'),
 ('VLLM_Ascend_RepoAPI','https://api.github.com/repos/vllm-project/vllm-ascend','json'),
 ('Ultralytics_RepoAPI','https://api.github.com/repos/ultralytics/ultralytics','json')])
elif sys.argv[1]=='read':
 for name in sys.argv[2:]:
  x=R[name];print('\nSOURCE',name,x.get('archive_status'),x.get('error'),x.get('file'))
  if x.get('file'):
   f=pathlib.Path(x['file']);t=(f.parent/'text.txt').read_text('utf-8') if f.suffix=='.html' else f.read_text('utf-8',errors='replace')
   print(t[:25000])
elif sys.argv[1]=='repos':
 for n in sys.argv[2:]:
  x=R[n]
  if x.get('file'):
   a=json.loads(pathlib.Path(x['file']).read_text('utf-8'));print(n,{k:a.get(k) for k in ['full_name','default_branch','pushed_at','archived','license']})
elif sys.argv[1]=='trees':
 rows=[]
 for n in sys.argv[2:]:
  a=json.loads(pathlib.Path(R[n]['file']).read_text('utf-8'));rows.append((n.replace('RepoAPI','TreeAPI'),'https://api.github.com/repos/'+a['full_name']+'/git/trees/'+a['default_branch']+'?recursive=1','json'))
 manifest('Huawei_HiSilicon_02_trees.json',rows)
elif sys.argv[1]=='paths':
 for n in sys.argv[2:]:
  a=json.loads(pathlib.Path(R[n]['file']).read_text('utf-8'));print(n,'SHA',a.get('sha'),'truncated',a.get('truncated'))
  for x in a.get('tree',[]):
   path=x['path']
   if any(k in path.lower() for k in ['resnet50','acl.json','robot','ascend.md','faqs.md','infer.py','model_process.cpp','sample_process.cpp','dvpp_process.cpp','svp','mpp','license','readme','mindspore_lite']) and x['type']=='blob': print(path)
elif sys.argv[1]=='core':
 rows=[]
 def add(tree,name,path):
  a=json.loads(pathlib.Path(R[tree]['file']).read_text('utf-8'))
  assert path in [x['path'] for x in a['tree']],path
  repo={'Ascend_Samples_TreeAPI':'Ascend/samples','Ascend_Pytorch_TreeAPI':'Ascend/pytorch','MindSpore_TreeAPI':'mindspore-ai/mindspore','VLLM_Ascend_TreeAPI':'vllm-project/vllm-ascend','Ultralytics_TreeAPI':'ultralytics/ultralytics'}[tree]
  rows.append((name,'https://raw.githubusercontent.com/'+repo+'/'+a['sha']+'/'+path,'any'))
 for tree,name,path in [
 ('Ascend_Samples_TreeAPI','Ascend_Samples_README','README_CN.md'),
 ('Ascend_Samples_TreeAPI','Ascend_Samples_License','LICENSE'),
 ('Ascend_Pytorch_TreeAPI','Ascend_Pytorch_README','README.zh.md'),
 ('Ascend_Pytorch_TreeAPI','Ascend_Pytorch_License','LICENSE'),
 ('MindSpore_TreeAPI','MindSpore_README','README_CN.md'),
 ('MindSpore_TreeAPI','MindSpore_License','LICENSE'),
 ('VLLM_Ascend_TreeAPI','VLLM_Ascend_FAQ','docs/source/faqs.md'),
 ('VLLM_Ascend_TreeAPI','VLLM_Ascend_License','LICENSE'),
 ('Ultralytics_TreeAPI','Ultralytics_Ascend_Doc','docs/en/integrations/ascend.md'),
 ('Ultralytics_TreeAPI','Ultralytics_License','LICENSE')]:add(tree,name,path)
 manifest('Huawei_HiSilicon_02_core.json',rows)
elif sys.argv[1]=='extra':
 manifest('Huawei_HiSilicon_02_extra.json',[
 ('HiSilicon_MaterialsCenter','https://www.hisilicon.com/cn/chip-academy/materiallist','html'),
 ('HiView_RepoAPI','https://api.github.com/repos/openhisilicon/HIVIEW','json'),
 ('OH_HiSilicon_RepoAPI','https://api.github.com/repos/openharmony/device_soc_hisilicon','json'),
 ('LiteOS_RepoAPI','https://api.github.com/repos/LiteOS/LiteOS','json')])
elif sys.argv[1]=='implementation':
 rows=[]
 groups={
 'Ascend_Samples_TreeAPI':('Ascend/samples',[
 ('ACL_ResNet_README','cplusplus/level2_simple_inference/1_classification/resnet50_imagenet_classification/README_CN.md'),
 ('ACL_ModelProcess','cplusplus/level2_simple_inference/1_classification/resnet50_imagenet_classification/src/model_process.cpp'),
 ('ACL_SampleProcess','cplusplus/level2_simple_inference/1_classification/resnet50_imagenet_classification/src/sample_process.cpp'),
 ('ACL_Dynamic_README','cplusplus/level2_simple_inference/1_classification/resnet50_imagenet_dynamic_dims/README_CN.md'),
 ('ACL_Async_ModelProcess','cplusplus/level2_simple_inference/1_classification/resnet50_async_imagenet_classification/src/model_process.cpp'),
 ('ACL_FirstApp_Figure','cplusplus/level2_simple_inference/1_classification/resnet50_firstapp/README_fig.png'),
 ('Ascend_Robot_Arm_README','python/level3_multi_model/Robotic_Arm_Object_Following/README_CN.md'),
 ('Ascend_Robot_Chess_README','python/level3_multi_model/Robot_Play_Chess/README_CN.md'),
 ('Ascend_Robot_Car_README','cplusplus/contrib/robots_car/README_CN.md')]),
 'Ascend_Pytorch_TreeAPI':('Ascend/pytorch',[
 ('TorchNPU_Compatibility','COMPATIBILITY.md'),('TorchNPU_Support','SUPPORT.md'),('TorchNPU_ArchitectureSVG','docs/zh/figures/architecture.svg'),('TorchNPU_Docs_License','docs/LICENSE')]),
 'Ultralytics_TreeAPI':('ultralytics/ultralytics',[
 ('Ultralytics_Ascend_Exporter','ultralytics/utils/export/ascend.py'),('Ultralytics_Ascend_Backend','ultralytics/nn/backends/ascend.py')]),
 'MindSpore_TreeAPI':('mindspore-ai/mindspore',[
 ('MindSpore_Lite_README','mindspore/lite/README_CN.md'),('MindSpore_Lite_Context','mindspore/lite/python/api/context.py'),('MindSpore_Lite_Model','mindspore/lite/python/api/model.py'),('MindSpore_Lite_Converter','mindspore/lite/python/api/converter.py')])}
 for tree,(repo,files) in groups.items():
  a=json.loads(pathlib.Path(R[tree]['file']).read_text('utf-8'));paths={x['path'] for x in a['tree']}
  for n,path in files:
   assert path in paths,path
   rows.append((n,'https://raw.githubusercontent.com/'+repo+'/'+a['sha']+'/'+path,'any'))
 manifest('Huawei_HiSilicon_02_implementation.json',rows)
