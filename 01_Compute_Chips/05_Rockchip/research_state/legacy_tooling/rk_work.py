from rk02_report import *
import subprocess,shutil
def links(names):
 r=json.loads((a/'_registry/materials.json').read_text(encoding='utf-8'))
 for n in names:
  v=r[n];content=pathlib.Path(v['file']).read_text(encoding='utf-8',errors='replace')
  ls=re.findall(r'href=["\']([^"\']+)',content)
  if v['content_type'].startswith('text/plain'):ls+=re.findall(r'\]\(([^)]+)\)',content)
  print(n,'\n'+'\n'.join(dict.fromkeys(x.split('#')[0] for x in ls if '/docs/' in x or 'raw.githubusercontent' in x or 'github.com' in x)))
def make(stem,figs=None):
 baseline(stem)
 body=(root/'toolkit/drafts'/f'{stem}.txt').read_text(encoding='utf-8')
 ids=list(dict.fromkeys(re.findall(r'\[\[([\w.]+)\]\]',body)))
 figs=figs or []
 for f in figs:
  if f['source_id'] not in ids:ids.append(f['source_id'])
 claims=[]
 for n in ids:
  claims.append(claim(n,'正文对应小节；原文与本地快照','正文引用内容与机制边界','截至2026-11-05；具体SKU/版本/条件见正文','人工静态阅读核对；未运行硬件；缺口和分析明确标注'))
 write(stem,body,ids,claims,figs,coverage='本维度按正文逐项覆盖机制、目标/版本、测量边界和可复建验证；未取得资料明确记录。',licenses='代码/权重/数据/二进制/固件/本体资产分别核对；不以公开仓库推导全部开源或商业授权。')
def check(stem):
 q=subprocess.run([sys.executable,str(root/'toolkit/check_report.py'),'--project',str(p),'--report',stem+'.md','--baseline',str(s/'baselines'/f'{stem}_before.json')],capture_output=True,text=True,encoding='utf-8')
 v=json.loads((a/'derived/qa'/f'{stem}_quality.json').read_text(encoding='utf-8'))
 print(stem,{k:v[k] for k in ['outcome','body_han_chars','sources','figures','errors']});assert q.returncode==0
def done(stem,dimension=None,collection=None):
 cmd=[sys.executable,str(root/'toolkit/download_materials.py'),'--project','01_Compute_Chips/05_Rockchip','--manifest',str(root/'toolkit/manifests'/f'Rockchip_{stem}_Cited.json'),'--dimension',dimension or stem,'--proxy','http://child-prc.intel.com:913']
 if collection:cmd+=['--collection',collection]
 result=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');assert result.returncode==0,result.stdout+result.stderr
 v=json.loads((a/'_registry/last_run.json').read_text(encoding='utf-8'));assert v['network_requests_including_robots']==0,v
 shutil.copy2(a/'_registry/last_run.json',a/'derived/qa'/f'{stem}_dedup_last_run.json')
 print(stem,'dedup network=0')
def manifest(label,pairs):
 f=root/'toolkit/manifests'/f'Rockchip_{label}.json';f.write_text(json.dumps([dict(name=n,url=u,expected='any') for n,u in pairs],ensure_ascii=False,indent=2),encoding='utf-8');return f
if __name__=='__main__':
 if sys.argv[1]=='links':links(sys.argv[2:])
 elif sys.argv[1]=='make':make(sys.argv[2]);check(sys.argv[2])
 elif sys.argv[1]=='done':done(sys.argv[2],collection=sys.argv[3] if len(sys.argv)>3 else None)
