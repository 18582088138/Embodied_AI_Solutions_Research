from rk_work import *
from urllib.parse import urljoin
def nav(names,pat):
 r=json.loads((a/'_registry/materials.json').read_text(encoding='utf-8'))
 for n in names:
  print(n)
  text=pathlib.Path(r[n]['file']).read_text(encoding='utf-8',errors='replace')
  links=re.findall(r'href=["\']([^"\']+)',text)
  print('\n'.join(dict.fromkeys(urljoin(r[n]['url'],x) for x in links if re.search(pat,x,re.I))))
def fetch(label,pairs,dimension):
 f=manifest(label,pairs)
 cmd=[sys.executable,str(root/'toolkit/download_materials.py'),'--project','01_Compute_Chips/05_Rockchip','--manifest',str(f),'--dimension',dimension,'--proxy','http://child-prc.intel.com:913']
 result=subprocess.run(cmd);print('download exit',result.returncode)
def render(n,page,name):
 r=json.loads((a/'_registry/materials.json').read_text(encoding='utf-8'))
 target=a/'derived/figures'/name
 pop='C:/Users/kundaxu/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe'
 subprocess.run([pop,'-f',str(page),'-l',str(page),'-scale-to','1600','-png','-singlefile',r[n]['file'],str(target.with_suffix(''))],check=True)
 return str(target)
def index08():
 stems=['08_Core_Technology_Moat','08A_Quantization_Compiler','08B_Memory_Coprocessor_Multicard','08C_Perception_RealTime_Trust']
 roles=['跨机制价值、证据层次和条件选型','数值格式、GRQ block误差、混合映射、CPU插件、精度','DRAM、tensor同步、KV页、分段/队列与链路分析','ISP/IQ、时间、RT锁/AMP、EtherCAT、模型/启动保护']
 body='# 08 核心技术专题索引\n\n截至2026-11-05。总览与三篇独立专题逐篇完成文献/API/源码静态核验、官方图复核、报告检查和零网络去重；未进行板端或机器人实机测试。\n\n| 报告 | 研究对象 | 有效汉字 | 原件 | 图 | 检查与归档 |\n| --- | --- | --- | --- | --- | --- |\n'
 for stem,role in zip(stems,roles):
  q=json.loads((a/'derived/qa'/f'{stem}_quality.json').read_text(encoding='utf-8'))
  body+=f"| [{stem}](<{(p/(stem+'.md')).as_posix()}>) | {role} | {q['body_han_chars']} | {q['sources']} | {q['figures']} | [检查](<{(a/'derived/qa'/f'{stem}_quality.json').as_posix()}>)；[证据](<{(s/'evidence'/f'{stem}.json').as_posix()}>)；[基线](<{(s/'baselines'/f'{stem}_before.json').as_posix()}>)；[去重](<{(a/'derived/qa'/f'{stem}_dedup_last_run.json').as_posix()}>) |\n"
 body+=f"\n[08联合资料目录](<{(a/'08_core/index.html').as_posix()}>)；[联合引用清单](<{(root/'toolkit/manifests/Rockchip_08_Union.json').as_posix()}>)；[联合去重记录](<{(a/'derived/qa/08_Union_dedup_last_run.json').as_posix()}>)。\n\n关键版本为RKNN3 V1.2.0；RKNN2、RKLLM与板商BSP独立，不能统一称为同一版本。尚未取得物理DRAM带宽、完整kernel/tactic/格式、VLA同条件精度与闭环数据、功能安全和长期维护合同。旧08_Proprietary_Technologies.md只保留历史占位，当前研究入口为08_Core_Technology_Moat.md。\n"
 (p/'08_Topics_Index.md').write_text(body,encoding='utf-8')
 targets=re.findall(r'\]\(<([^>]+)>\)',body);assert all(pathlib.Path(x).exists() for x in targets)
 (a/'derived/qa/08_Index_quality.json').write_text(json.dumps(dict(outcome='pass',links=len(targets),scope='专题及联合归档索引'),ensure_ascii=False,indent=2),encoding='utf-8')
 v=json.loads((s/'progress.json').read_text(encoding='utf-8'))
 v['core_technology_topics']=dict(planned=stems[1:],completed=stems[1:],current_topic='complete',review_status='研究完成；用户授权连续调研，未代用户批准',checks={stem:json.loads((a/'derived/qa'/f'{stem}_quality.json').read_text(encoding='utf-8'))['outcome'] for stem in stems},union_manifest='toolkit/manifests/Rockchip_08_Union.json',collection='reference_metrial/08_core/index.html')
 (s/'progress.json').write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':
 if sys.argv[1]=='nav':nav(sys.argv[2].split(','),sys.argv[3])
 elif sys.argv[1]=='rawlinks':
  r=json.loads((a/'_registry/materials.json').read_text(encoding='utf-8'))
  for n in sys.argv[2].split(','):
   f=pathlib.Path(r[n]['file']).with_name('original.response');t=f.read_text(encoding='utf-8',errors='replace');print(n)
   for line in t.splitlines():
    if re.search(sys.argv[3],line,re.I):print(line[:1800])
 elif sys.argv[1]=='inspect':
  import gzip
  r=json.loads((a/'_registry/materials.json').read_text(encoding='utf-8'))
  for n in sys.argv[2].split(','):
   f=pathlib.Path(r[n]['file']).with_name('original.response');b=f.read_bytes();b=gzip.decompress(b) if b.startswith(b'\x1f\x8b') else b
   print(n,r[n]['content_type']);print(b[:1400].decode('utf-8',errors='replace'))
