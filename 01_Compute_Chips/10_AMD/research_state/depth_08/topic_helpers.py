import sys,pathlib,json,hashlib
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from curation import inputs,figure,figure_file,records,P
D=P/'research_state/depth_08'
def prepare(stem,rows,manual,meta=None):
 inputs(stem,'08_core',rows,manual)
 fp=D/'source_meta.json';v=json.loads(fp.read_text(encoding='utf8')) if fp.exists() else {}
 v.update(meta or {});fp.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
def pdf_fig(slug,s,p):
 o=P/f'reference_metrial/derived/figures/source_{s}_p{p}.png';figure_file('08',slug,s,o,records()[s]['url'],f'官方PDF第{p}页，Poppler scale-to1800完整页PNG渲染，未裁剪，已实际打开')
 fp=D/'figures.json';v=json.loads(fp.read_text(encoding='utf8'));orig=pathlib.Path(records()[s]['file'])
 for x in v:
  if x['slug']==slug:x['original_file']=orig.as_posix();x['original_sha256']=hashlib.sha256(orig.read_bytes()).hexdigest()
 fp.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
def rowset():
 rows=[]
 def a(s,n,c,l='正文',t='事实',k='具体条件见正文',f='原件核对，不能推广未测SKU/模型/版本/任务'):rows.append((s,n,c,l,t,k,f))
 return rows,a
