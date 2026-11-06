"""Offline structural/archive checks for one platform report; not semantic certification."""
import argparse,hashlib,json,pathlib,re
from archive_paths import load_json, portable
from collections import Counter
from html.parser import HTMLParser
from urllib.parse import unquote,urlsplit
from download_materials import VisibleText,charset,decode_body,normalized

def verify(project,report,trace_path,baseline=None):
    archive=project/'reference_metrial';errors=[];warnings=[];hashes=0;page_links=0
    text=report.read_text(encoding='utf-8')
    body=re.split(r'^##\s+(?:参考资料.*|资料与核验.*|本地原文.*|References.*)$',text,maxsplit=1,flags=re.M)[0]
    han=len(re.findall(r'[\u4e00-\u9fff]',body))
    if han<1500:errors.append('正文有效汉字不足1500（不含参考表）')
    if re.search(r'\{\{|<a\s+id=|\]\(#|\bTODO\b|待填写|此处填写',text):errors.append('存在模板占位或不允许的锚点')
    tables=[];rows=[]
    for line in body.splitlines()+['']:
        if line.startswith('|'):rows.append(line)
        elif rows:tables.append(rows);rows=[]
    if not tables:errors.append('缺少比较表')
    for i,table in enumerate(tables,1):
        counts=[len(re.split(r'(?<!\\)\|',x))-2 for x in table]
        if len(table)<3 or len(set(counts))!=1 or not 1<=counts[0]<=8:errors.append(f'表格{i}行列不一致、无数据或超过8列')
        elif not all(re.fullmatch(r'\s*:?-{3,}:?\s*',x) for x in re.split(r'(?<!\\)\|',table[1])[1:-1]):
            errors.append(f'表格{i}缺少有效分隔行')
    headings=list(re.finditer(r'^#{1,6} .+$',body,re.M))
    for left,right in zip(headings,headings[1:]):
        if not body[left.end():right.start()].strip() and right[0].count('#')<=left[0].count('#'):
            errors.append('空壳章节: '+left[0])
    trace=load_json(trace_path)
    registry=json.loads((archive/'_registry/materials.json').read_text(encoding='utf-8'))
    ids=trace.get('source_ids',[])
    if not isinstance(ids,list) or not ids:errors.append('trace缺少有效source_ids');ids=[]
    if len(set(ids))!=len(ids):warnings.append('source_ids重复')
    selected={};allowed_urls=set();html_equal=0;assets={};checked=set()

    def check_hash(path,expected,label):
        nonlocal hashes
        path=pathlib.Path(path)
        if not expected:errors.append('缺少哈希: '+label);return False
        key=(path.as_posix(),expected)
        if key in checked:return True
        if not path.is_file():errors.append('缺少文件: '+label+' '+str(path));return False
        hashes+=1
        if hashlib.sha256(path.read_bytes()).hexdigest()!=expected:errors.append('哈希不匹配: '+label);return False
        checked.add(key);return True

    def page_local(value,base,page_dir):
        nonlocal page_links
        if not value or value.startswith(('#','data:','blob:','javascript:')) or urlsplit(value).scheme:return
        target=(base/unquote(urlsplit(value).path)).resolve();page_links+=1
        if not target.is_relative_to(page_dir.resolve()) or not target.is_file():errors.append('无效页内依赖: '+str(target))

    def css_links(content,base,page_dir):
        # Resolve relative CSS references without fetching remote dependencies.
        values=[next(x for x in m.groups() if x is not None).strip() for m in re.finditer(r'url\(\s*(?:"([^"]*)"|\'([^\']*)\'|([^)]*?))\s*\)',content,re.I)]
        values += [m[1] for m in re.finditer(r'@import\s+["\']([^"\']+)["\']',content,re.I)]
        for value in values:page_local(value,base,page_dir)

    class PageLinks(HTMLParser):
        def __init__(self,folder):super().__init__();self.folder=folder;self.style=False
        def handle_starttag(self,tag,attrs):
            values=dict(attrs)
            for key,value in attrs:
                if not value:continue
                resource=(key=='src' and tag in ('img','script','source','video','audio','input')) or (key=='poster' and tag=='video') or (tag=='link' and key=='href' and bool(set(values.get('rel','').lower().split()) & {'stylesheet','icon','preload','modulepreload','apple-touch-icon'}))
                if resource:page_local(value,self.folder,self.folder)
                if key in ('srcset','data-srcset') and 'data:' not in value:
                    for part in value.split(','):
                        if part.strip():page_local(part.strip().split()[0],self.folder,self.folder)
                if key=='style':css_links(value,self.folder,self.folder)
            if tag=='style':self.style=True
        def handle_endtag(self,tag):
            if tag=='style':self.style=False
        def handle_data(self,data):
            if self.style:css_links(data,self.folder,self.folder)

    for name in dict.fromkeys(ids):
        record=registry.get(name)
        if not record:errors.append('未知来源: '+name);continue
        if record.get('status')!=200 or record.get('archive_status') not in ('complete_static','partial_static'):
            errors.append('引用正文未成功取得: '+name);continue
        selected[name]=record;allowed_urls.add(normalized(record['url']))
        path=pathlib.Path(record['file'])
        if not path.resolve().is_relative_to(archive.resolve()):errors.append('原文不在项目归档: '+name)
        file_ok=check_hash(path,record.get('sha256'),name)
        raw_ok=check_hash(record['original_file'],record.get('original_sha256'),name+' original')
        for asset in record.get('assets',[]):
            local=archive/asset.get('local_file',asset['file']);assets[asset['url']]=asset
            allowed_urls.add(normalized(asset['url']));check_hash(local,asset.get('sha256'),name+' asset')
            if local.suffix=='.css' and local.is_file():css_links(local.read_text(encoding='utf-8'),local.parent,path.parent)
        if path.suffix=='.html' and file_ok and raw_ok:
            try:
                raw=decode_body(pathlib.Path(record['original_file']).read_bytes(),record['headers'])
                before=VisibleText();before.feed(raw.decode(charset(raw,record['content_type'])))
                local=path.read_text(encoding='utf-8');after=VisibleText();after.feed(local)
                if before.value()!=after.value():errors.append('HTML可见文本不同: '+name)
                else:html_equal+=1
                PageLinks(path.parent).feed(local)
            except Exception as exc:errors.append('HTML检查失败: '+name+' '+str(exc))
        if record.get('archive_status')=='partial_static':warnings.append('静态依赖部分缺失: '+name+'（报告应披露）')
    # Rspress pages may carry their body in officially archived JS chunks.
    # Accept the document route only with a selected original and hashed local derivatives.
    for dynamic in trace.get('dynamic_provenance',[]):
        name=dynamic.get('source_id');record=selected.get(name)
        if not record or dynamic.get('content_js_sha256')!=record.get('original_sha256'):
            errors.append('动态正文未匹配已归档JS原件: '+str(name));continue
        if pathlib.Path(dynamic.get('content_js_original','')).resolve()!=pathlib.Path(record['original_file']).resolve():
            errors.append('动态正文原件路径不匹配: '+str(name));continue
        for pathkey,hashkey in [('extracted_text','text_sha256'),('rendered_html','html_sha256')]:
            dp=pathlib.Path(dynamic.get(pathkey,''))
            if not dp.resolve().is_relative_to(archive.resolve()):errors.append('动态衍生正文路径越界: '+str(name))
            check_hash(dp,dynamic.get(hashkey),str(name)+' '+pathkey)
        if not dynamic.get('method') or not dynamic.get('url'):errors.append('动态正文缺少来源/方法: '+str(name))
        else:allowed_urls.add(normalized(dynamic['url']))
    figures=trace.get('figures',[])
    for i,fig in enumerate(figures,1):
        required=('file','sha256','source_id','source_url','original_file','original_sha256','operation')
        if any(not fig.get(x) for x in required):errors.append(f'图{i}缺少来源/操作/哈希字段');continue
        record=selected.get(fig['source_id'])
        if not record:errors.append(f'图{i}来源不在本章引用清单');continue
        check_hash(fig['file'],fig['sha256'],f'图{i}衍生')
        check_hash(fig['original_file'],fig['original_sha256'],f'图{i}原件')
        original=pathlib.Path(fig['original_file']).resolve()
        candidates=[(pathlib.Path(record['file']).resolve(),record['sha256'],record['url'])]
        candidates += [( (archive/a.get('local_file',a['file'])).resolve(),a['sha256'],a['url']) for a in record.get('assets',[])]
        if not any(original==p and fig['original_sha256']==sha and normalized(fig['source_url'])==normalized(url) for p,sha,url in candidates):
            errors.append(f'图{i}原件/URL未匹配所引registry资料')
        allowed_urls.add(normalized(fig['source_url']))
    if not figures:warnings.append('未记录官方图片，需人工说明检索范围和原因')
    local_links=0;remote_links=set();image_files=set()
    for m in re.finditer(r'(!?)\[[^\]]*\]\((<[^>]+>|[^)\n]+)\)',text):
        value=m[2].strip().strip('<>');path=pathlib.Path(unquote(value))
        if value.startswith(('http://','https://')):
            remote_links.add(normalized(value))
            if m[1]:errors.append('报告官方图应使用已归档本地图: '+value)
        elif value.startswith(('mailto:','tel:')):continue
        elif value.startswith('#'):errors.append('不允许使用锚点链接: '+value)
        else:
            target=path if path.is_absolute() else report.parent/path;local_links+=1
            if not target.is_file():errors.append('不存在的本地报告链接: '+str(target))
            if m[1]:image_files.add(target.resolve())
    for url in remote_links-allowed_urls:errors.append('原文链接未列入本章归档证据: '+url)
    tracked_images={pathlib.Path(f['file']).resolve() for f in figures if f.get('file')}
    # Report figure mirrors are published separately from intentionally local archives.
    mirrors_path=project/'research_state/organization_figures.json'
    if mirrors_path.is_file():
        for mirror in load_json(mirrors_path):
            original=pathlib.Path(mirror['local_original']).resolve()
            for figure in figures:
                if original==pathlib.Path(figure.get('file','')).resolve() and mirror['sha256']==figure.get('sha256'):
                    published=project/mirror['figure']
                    check_hash(published,mirror['sha256'],'published figure mirror')
                    tracked_images.add(published.resolve())
    for path in image_files-tracked_images:errors.append('正文图片未记录图源trace: '+str(path))
    for path in tracked_images-image_files:warnings.append('trace图未出现在正文: '+str(path))
    if not trace.get('claim_review'):errors.append('缺少关键主张的人工核验记录')
    review=trace.get('manual_review',{})
    for field in ('coverage','versions_and_measurements','maturity_and_licenses','figures_opened'):
        if not review.get(field):errors.append('缺少人工审阅记录: '+field)
    unchanged={}
    if baseline:
        for rel,sha in load_json(baseline).items():
            path=(project/rel).resolve()
            if not path.is_relative_to(project):errors.append('基线路径越界: '+rel);continue
            if path==report.resolve():continue
            unchanged[rel]=path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==sha
        if not all(unchanged.values()):errors.append('其他报告与本章基线不一致')
    else:warnings.append('未提供本章开始基线；不能证明其他报告未变')
    result=dict(report=report.as_posix(),body_han_chars=han,tables=len(tables),sources=len(selected),
        archive_status=dict(Counter(x['archive_status'] for x in selected.values())),figures=len(figures),
        file_hash_checks=hashes,html_visible_text_equal=html_equal,page_local_dependencies_checked=page_links,
        report_local_links=local_links,other_reports_unchanged=unchanged,errors=errors,warnings=warnings,
        outcome='pass' if not errors else 'fail',limits='结构、归档与审阅记录检查；未自动证明事实正确或开展实机测试')
    out=archive/'derived/qa';out.mkdir(parents=True,exist_ok=True)
    (out/(report.stem+'_quality.json')).write_text(json.dumps(portable(result),ensure_ascii=False,indent=2),encoding='utf-8')
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project',required=True,type=pathlib.Path)
    parser.add_argument('--report',required=True,type=pathlib.Path)
    parser.add_argument('--trace',type=pathlib.Path)
    parser.add_argument('--baseline',type=pathlib.Path)
    args=parser.parse_args();project=args.project.resolve()
    report=args.report if args.report.is_absolute() else project/args.report
    if not report.resolve().is_relative_to(project):parser.error('report must be within project')
    trace=args.trace or project/'research_state/evidence'/(report.stem+'.json')
    result=verify(project,report,trace,args.baseline)
    print(json.dumps(portable(result),ensure_ascii=False,indent=2));return bool(result['errors'])

if __name__=='__main__':raise SystemExit(main())
