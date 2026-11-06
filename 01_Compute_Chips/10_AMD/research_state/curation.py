"""Offline curated evidence and figure records; no network or registry edits."""
import pathlib,json,hashlib,shutil
P=pathlib.Path(__file__).resolve().parent.parent
def records():return json.loads((P/'reference_metrial/_registry/materials.json').read_text(encoding='utf8'))
def inputs(stem,collection,reviews,manual):
 d=P/'research_state'/('depth_'+stem[:2]);d.mkdir(exist_ok=True)
 (d/'config.json').write_text(json.dumps({'collection':collection}),encoding='utf8')
 (d/(stem+'_reviews.json')).write_text(json.dumps([dict(source_id=s,needle=n,claim=c,location=l,evidence_type=t,conditions=k,finding=f) for s,n,c,l,t,k,f in reviews],ensure_ascii=False,indent=2),encoding='utf8')
 (d/(stem+'_manual.json')).write_text(json.dumps(manual,ensure_ascii=False,indent=2),encoding='utf8')
def figure(ch,slug,source,match,opened,operation='官方原始图，复制归档asset；未裁剪，已实际打开逐字复核'):
 assert opened is True
 r=records()[source];a=next(a for a in r.get('assets',[]) if match in a['url']);o=P/'reference_metrial'/a.get('local_file',a['file'])
 return figure_file(ch,slug,source,o,a['url'],operation)
def figure_file(ch,slug,source,original,url,operation):
 o=pathlib.Path(original);out=P/'reference_metrial/derived/figures'/ch;out.mkdir(exist_ok=True)
 f=out/(slug+o.suffix);shutil.copyfile(o,f)
 item=dict(slug=slug,opened=True,source_id=source,source_url=url,file=f.as_posix(),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),original_file=o.as_posix(),original_sha256=hashlib.sha256(o.read_bytes()).hexdigest(),operation=operation)
 d=P/'research_state'/('depth_'+ch);fp=d/'figures.json';v=json.loads(fp.read_text(encoding='utf8')) if fp.exists() else [];v=[a for a in v if a['slug']!=slug]+[item];fp.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8');return item
