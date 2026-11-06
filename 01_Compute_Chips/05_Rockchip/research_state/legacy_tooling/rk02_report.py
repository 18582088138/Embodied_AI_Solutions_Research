import pathlib,json,hashlib,re,sys
from rockchip_02_work import baseline
root=pathlib.Path(__file__).resolve().parent.parent;p=root/'01_Compute_Chips/05_Rockchip';a=p/'reference_metrial';s=p/'research_state'
def sha(f):return hashlib.sha256(pathlib.Path(f).read_bytes()).hexdigest()
def write(stem,body,ids,claims,figures=None,coverage='',licenses=''):
 r=json.loads((a/'_registry/materials.json').read_text(encoding='utf-8'));figures=figures or []
 for n in ids:
  assert r[n]['status']==200 and r[n]['archive_status'] in ['complete_static','partial_static'],n
 def cite(m):
  n=m[1];assert n in ids,n
  return f"[{n}]({r[n]['url']})（[本地原件](<{pathlib.Path(r[n]['file']).as_posix()}>))"
 body=re.sub(r'\[\[([\w.]+)\]\]',cite,body)
 for i,fig in enumerate(figures):body=body.replace(f'FIGURE{i}',f"![{fig['caption']}](<{pathlib.Path(fig['file']).as_posix()}>)")
 body+='\n\n## 参考资料与本地原文\n\n采集时间逐项列出；移动分支及无版本网页仅代表此次快照。HTML 保留正文与可取得静态依赖，动态交互、视频及缺失依赖不保证完整。未进行目标板安装或实机性能验证。\n\n| 来源 | 原 URL | 本地原件 | 采集 UTC | 归档状态 |\n| --- | --- | --- | --- | --- |\n'
 for n in ids:
  v=r[n];body+=f"| {n} | [原文]({v['url']}) | [归档](<{pathlib.Path(v['file']).as_posix()}>) | {v['archived_at_utc']} | {v['archive_status']}；缺失依赖 {len(v.get('unavailable_assets',{}))} |\n"
 body+=f"\n[证据记录](<{(s/'evidence'/f'{stem}.json').as_posix()}>)；[本章开始前哈希基线](<{(s/'baselines'/f'{stem}_before.json').as_posix()}>)。检查和去重记录由专题索引汇总。\n"
 trace=dict(source_ids=ids,figures=[{k:v for k,v in f.items() if k!='caption'} for f in figures],claim_review=claims,manual_review=dict(coverage=coverage,versions_and_measurements='核对原文版本、对象、参数和测量边界；源码仅静态阅读，未安装或实测。移动分支commit未取得时明确限制。',maturity_and_licenses=licenses,figures_opened='图像逐张实际打开并核对说明；无图专题在正文解释来源检索及取得缺口。'))
 (s/'evidence'/f'{stem}.json').write_text(json.dumps(trace,ensure_ascii=False,indent=2),encoding='utf-8')
 (p/f'{stem}.md').write_text(body,encoding='utf-8')
 (root/'toolkit/manifests'/f'Rockchip_{stem}_Cited.json').write_text(json.dumps([dict(name=n,url=r[n]['url'],expected='any') for n in ids],ensure_ascii=False,indent=2),encoding='utf-8')
def claim(source,loc,text,conditions,finding,kind='事实/分析'):
 return dict(source_id=source,location=loc,claim=text,conditions=conditions,finding=finding,evidence_type=kind)
def figure(n,file,operation,caption):
 r=json.loads((a/'_registry/materials.json').read_text(encoding='utf-8'))[n]
 return dict(file=str(pathlib.Path(file).resolve()),sha256=sha(file),source_id=n,source_url=r['url'],original_file=r['file'],original_sha256=sha(r['file']),operation=operation,caption=caption)
