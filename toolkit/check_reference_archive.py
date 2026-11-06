"""Verify a project's archive and report links without downloading anything."""
import argparse,hashlib,json,pathlib,re
from archive_paths import load_json
from collections import Counter
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from download_materials import VisibleText,decode_body,charset,PresentationCSSURLs
parser=argparse.ArgumentParser()
parser.add_argument('--project',required=True,type=pathlib.Path)
args=parser.parse_args();project=args.project.resolve();folder=project/'reference_metrial'
records=load_json(folder/'_registry/materials.json')
errors=[]
local_links_checked=0
def check_local(value,base,page_dir):
    global local_links_checked
    if not value or value.startswith(('#','data:','blob:','javascript:')) or urlsplit(value).scheme:return
    target=(base/unquote(urlsplit(value).path)).resolve()
    local_links_checked+=1
    if not target.is_relative_to(page_dir) or not target.is_file():errors.append('invalid page-local dependency: '+str(target))
def check_css(text,base,page_dir):
    values=[next(x for x in m.groups() if x is not None).strip() for m in re.finditer(r'url\(\s*(?:"([^"]*)"|\'([^\']*)\'|([^)]*?))\s*\)',text,re.I)]
    values += [m[1] for m in re.finditer(r'@import\s+["\']([^"\']+)["\']',text,re.I)]
    for value in values:check_local(value,base,page_dir)
class PageLinks(HTMLParser):
    def __init__(self,folder):super().__init__();self.folder=folder;self.style=False
    def handle_starttag(self,tag,attrs):
        values=dict(attrs)
        for key,value in attrs:
            if not value:continue
            if (key=='src' and tag in ('img','script','source','video','audio','input')) or (key=='poster' and tag=='video') or (tag=='link' and key=='href' and bool(set(values.get('rel','').lower().split()) & {'stylesheet','icon','preload','modulepreload','apple-touch-icon'})):
                check_local(value,self.folder,self.folder)
            if key in ('srcset','data-srcset') and 'data:' not in value:
                for part in value.split(','):
                    if part.strip():check_local(part.strip().split()[0],self.folder,self.folder)
            if key=='style':check_css(value,self.folder,self.folder)
        if tag=='style':self.style=True
    def handle_endtag(self,tag):
        if tag=='style':self.style=False
    def handle_data(self,data):
        if self.style:check_css(data,self.folder,self.folder)
for name,record in records.items():
    if record['archive_status']=='failed':errors.append(name+': body failed');continue
    for key,hashkey in [('file','sha256'),('original_file','original_sha256')]:
        path=pathlib.Path(record[key])
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=record[hashkey]:errors.append(name+': '+key)
    for asset in record.get('assets',[]):
        path=folder/asset.get('local_file',asset['file'])
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=asset['sha256']:errors.append(name+': asset '+asset['url'])
        if path.suffix=='.css' and path.exists():check_css(path.read_text(encoding='utf-8'),path.parent,pathlib.Path(record['file']).parent)
    if pathlib.Path(record['file']).suffix=='.html' and not record.get('visible_text_unchanged'):errors.append(name+': text equality missing')
    if pathlib.Path(record['file']).suffix=='.html':
        main_path=pathlib.Path(record['file']);localized=main_path.read_text(encoding='utf-8')
        original=decode_body(pathlib.Path(record['original_file']).read_bytes(),record['headers'])
        before=VisibleText();before.feed(original.decode(charset(original,record['content_type'])))
        after=VisibleText();after.feed(localized)
        if before.value()!=after.value():errors.append(name+': independent visible text mismatch')
        parser=PageLinks(main_path.parent);parser.feed(localized)
for report in project.glob('*.md'):
    # Only examine reports that have been migrated to this folder.
    text=report.read_text(encoding='utf-8')
    if 'reference_metrial/' not in text:continue
    for link in re.findall(r'\]\(([^)]+)\)',text):
        if re.match(r'^[A-Z]:/',link) and not pathlib.Path(link).is_file():errors.append('missing report link: '+link)
summary={'sources':len(records),'status_counts':dict(Counter(r['archive_status'] for r in records.values())),
 'html_sources':sum(pathlib.Path(r.get('file','')).suffix=='.html' for r in records.values()),
 'static_html_text_equal':all(r.get('visible_text_unchanged') for r in records.values() if pathlib.Path(r.get('file','')).suffix=='.html'),
 'assets':len(json.loads((folder/'_registry/assets.json').read_text(encoding='utf-8'))),
 'unavailable_asset_references':sum(len(r.get('unavailable_assets',{})) for r in records.values()),
 'unavailable_presentation_asset_references':sum(len(r.get('unavailable_presentation_assets',{})) for r in records.values()),'page_local_links_checked':local_links_checked,'errors':errors}
(folder/'derived/qa').mkdir(parents=True,exist_ok=True)
(folder/'derived/qa/archive_quality_check.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
