"""Project-scoped, auditable reference downloads and offline HTML archives.

Python 3.10+, standard library only. See README.md for CLI and fidelity limits.
"""
from __future__ import annotations
import argparse, concurrent.futures, gzip, hashlib, html, json, mimetypes, os, pathlib, re, shutil, sys, threading, time, zlib
import urllib.error, urllib.request, urllib.robotparser
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, urlunsplit, unquote

from archive_paths import load_json, portable
ROOT = pathlib.Path(__file__).resolve().parents[1]
AGENT = 'EmbodiedResearchArchive/1.0'

def utc(): return datetime.now(timezone.utc).isoformat()
def digest(data): return hashlib.sha256(data).hexdigest()
def save_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary=path.with_name(path.name+'.tmp')
    temporary.write_text(json.dumps(portable(obj), ensure_ascii=False, indent=2), encoding='utf-8')
    # Windows indexers/readers may briefly hold the destination without delete sharing.
    for attempt in range(6):
        try:
            temporary.replace(path)
            break
        except PermissionError:
            if attempt==5:raise
            time.sleep(0.1*(attempt+1))
def safe_name(name):
    if len(name)>180 or not re.fullmatch(r'[\w.-]+', name, re.UNICODE) or name in ('.','..'):
        raise ValueError('name must contain only letters, digits, underscore, hyphen or dot')
    if name.split('.')[0].upper() in {'CON','PRN','AUX','NUL',*(f'COM{i}' for i in range(1,10)),*(f'LPT{i}' for i in range(1,10))}:
        raise ValueError('reserved Windows file name')
    return name
def normalized(url):
    parts=urlsplit(url)
    if parts.scheme not in ('http','https') or not parts.netloc or parts.username or parts.password:
        raise ValueError('only anonymous public HTTP(S) URLs are supported')
    host=parts.hostname.lower()
    if ':' in host:host='['+host+']'
    port=parts.port
    if port and (parts.scheme,port) not in (('http',80),('https',443)):host+=':'+str(port)
    return urlunsplit((parts.scheme.lower(),host,parts.path or '/',parts.query,''))
def decode_body(data, headers):
    coding=headers.get('Content-Encoding','').lower()
    if data.startswith(b'\x1f\x8b'): return gzip.decompress(data)
    if coding=='deflate':
        try: return zlib.decompress(data)
        except zlib.error: return zlib.decompress(data,-zlib.MAX_WBITS)
    if coding and coding not in ('identity','gzip'): raise ValueError(f'unsupported encoding: {coding}')
    return data
def charset(data, content_type):
    match=re.search(r'charset\s*=\s*["\']?([\w-]+)',content_type,re.I)
    if not match: match=re.search(r'charset\s*=\s*["\']?([\w-]+)',data[:20000].decode('ascii','ignore'),re.I)
    return match[1] if match else 'utf-8'
def extension(data, kind, url):
    kind=kind.lower().split(';')[0]
    if data.startswith(b'%PDF'): return '.pdf'
    if kind in ('text/html','application/xhtml+xml') or re.search(rb'<(?:!doctype html|html)[\s>]',data[:2000],re.I): return '.html'
    if 'json' in kind: return '.json'
    if kind=='text/css': return '.css'
    if 'javascript' in kind: return '.js'
    if data.startswith(b'\x89PNG'): return '.png'
    if data.startswith(b'\xff\xd8'): return '.jpg'
    if 'svg' in kind: return '.svg'
    suffix=pathlib.PurePosixPath(urlsplit(url).path).suffix.lower()
    return suffix if re.fullmatch(r'\.[a-z0-9]{1,8}',suffix) else (mimetypes.guess_extension(kind) or '.bin')

def challenge_page(decoded):
    # Challenge text can occur after >20KB of inline SVG/scripts.
    # Some cookie challenges have no visible text; do not execute their scripts.
    if re.search(r"\bvar\s+arg1\s*=\s*['\"][0-9a-f]{40}['\"]", decoded, re.I) and ('acw_sc__v2' in decoded or 'YWN3X3NjX192Mj0=' in decoded):
        return True
    visible=html.unescape(re.sub(r'<[^>]+>', ' ', decoded))
    visible=re.sub(r'\s+', ' ', visible)
    return bool(re.search(r"Making sure you.re not a bot|Just a moment\.\.\.|Checking your browser|Protected by Anubis",visible,re.I))

def material_directory(out,category,name,url):
    # Leave room for assets/categories/hash.ext on Windows with long-path support disabled.
    parent=out/category
    budget=min(32,200-len(str(parent.resolve()))-1-18)
    if budget<1:raise ValueError('project path too long; use a shorter research root')
    label=re.sub(r'^NVIDIA_','',name)
    return parent/(label[:budget]+'--'+digest(url.encode())[:16])

def export_collection(archive, name, records):
    """Publish a self-contained topic view without new network requests.

    Shared registry remains authoritative. Hard links share storage; callers
    must treat archived files as read-only. Cross-volume exports copy locally.
    """
    safe_name(name)
    if name in ('_registry','derived','webpages','documents','data'):
        raise ValueError('collection name conflicts with an archive directory')
    folder=(archive.out/name).resolve()
    if folder.parent != archive.out.resolve():raise ValueError('collection escapes archive root')
    folder.mkdir(exist_ok=True)
    rows=[];hardlinks=0;copies=0
    for rec in {r['url']:r for r in records}.values():
        if rec.get('status')!=200 or rec.get('archive_status')=='failed' or not rec.get('file'):continue
        source=pathlib.Path(rec['file']).resolve();original_dir=source.parent
        if not original_dir.is_relative_to(archive.out.resolve()):raise ValueError('source outside archive')
        target_dir=material_directory(archive.out,name,rec['id'],rec['url'])
        for src in original_dir.rglob('*'):
            if src.is_symlink():raise ValueError('unexpected symbolic link in material')
            if not src.is_file():continue
            dest=target_dir/src.relative_to(original_dir)
            if len(str(dest))>=260:raise ValueError('collection path exceeds Windows path budget')
            dest.parent.mkdir(parents=True,exist_ok=True)
            if dest.exists():
                if dest.is_symlink():raise ValueError('unexpected symbolic link in collection')
                if digest(dest.read_bytes())==digest(src.read_bytes()):continue
                dest.unlink()
            try:os.link(src,dest);hardlinks+=1
            except OSError:shutil.copy2(src,dest);copies+=1
        dest=target_dir/source.name
        rows.append(dict(id=rec['id'],aliases=rec.get('aliases',[]),url=rec['url'],canonical_file=source.as_posix(),
                         file=dest.resolve().as_posix(),sha256=rec['sha256'],archive_status=rec['archive_status'],
                         archived_at_utc=rec.get('archived_at_utc'),used_by=rec.get('used_by',[])))
    # This is a view of this manifest, not an independent download registry.
    save_json(folder/'collection.json',dict(collection=name,generated_at_utc=utc(),materials=rows,
              storage='Hard links when available; local copy fallback; no separate network downloads',new_hardlinks=hardlinks,new_local_copies=copies))
    items=''.join('<li><a href="'+html.escape(archive.relative(pathlib.Path(r['file']),folder))+'">'+html.escape(r['id'])+'</a> — '+html.escape(r['archive_status'])+' — <a href="'+html.escape(r['url'])+'">官方原文</a></li>' for r in rows)
    (folder/'index.html').write_text('<!doctype html><html lang="zh"><meta charset="utf-8"><title>'+html.escape(name)+'</title><h1>专题参考资料</h1><p>各资料含HTML/原件和本地依赖；与项目共享登记及存储，请勿原地编辑归档文件。</p><ul>'+items+'</ul></html>',encoding='utf-8')
    print('collection',folder,'materials='+str(len(rows)),'hardlinks='+str(hardlinks),'local_copies='+str(copies),flush=True)
    return folder

class RobotRules:
    """robots Allow/Disallow with longest-match precedence and RFC wildcards."""
    def __init__(self,text):
        self.groups=[];agents=[];rules=[]
        for line in text.splitlines():
            line=line.split('#',1)[0].strip()
            if ':' not in line:continue
            key,value=line.split(':',1);key=key.strip().lower();value=value.strip()
            if key=='user-agent':
                if rules:self.groups.append((agents,rules));agents=[];rules=[]
                agents.append(value.lower())
            elif key in ('allow','disallow') and agents and value:rules.append((key=='allow',value))
        if agents:self.groups.append((agents,rules))
    def can_fetch(self,agent,url):
        selected=[];best=-1
        for agents,rules in self.groups:
            specificity=max((0 if name=='*' else len(name) for name in agents if name=='*' or name in agent.lower()),default=-1)
            if specificity>best:best=specificity;selected=list(rules)
            elif specificity==best and specificity>=0:selected.extend(rules)
        parts=urlsplit(url);path=parts.path or '/'
        if parts.query:path+='?'+parts.query
        winner=(-1,True)
        for allow,pattern in selected:
            expression='^'+re.escape(pattern).replace(r'\*','.*')
            if pattern.endswith('$'):expression=expression[:-2]+'$'
            if re.search(expression,path):
                specificity=len(pattern.replace('*','').rstrip('$'))
                if specificity>winner[0] or (specificity==winner[0] and allow):winner=(specificity,allow)
        return winner[1]

class CheckedRedirect(urllib.request.HTTPRedirectHandler):
    def __init__(self,network):self.network=network
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        newurl=normalized(newurl)
        if getattr(req,'check_robots',False) and not self.network.allowed(newurl):
            raise PermissionError('redirect destination disallowed; not requested')
        redirected=super().redirect_request(req,fp,code,msg,headers,newurl)
        if redirected:redirected.check_robots=getattr(req,'check_robots',False)
        return redirected

class Network:
    def __init__(self, proxy=None, delay=.3, timeout=25, max_bytes=100*1024*1024, jobs=4):
        handlers=[urllib.request.ProxyHandler({'http':proxy,'https':proxy})] if proxy else []
        self.opener=urllib.request.build_opener(*handlers,CheckedRedirect(self))
        self.delay=delay;self.timeout=timeout;self.max_bytes=max_bytes
        self.last={};self.robots={};self.robot_notes={}
        self.rate_lock=threading.Lock();self.robot_lock=threading.RLock()
        self.pool=concurrent.futures.ThreadPoolExecutor(max_workers=jobs)
        self.prefetched={};self.request_errors={}
        self.requests=0
    def raw(self,url,check_robots=False):
        self.requests+=1
        host=urlsplit(url).netloc
        with self.rate_lock:
            scheduled=max(time.monotonic(),self.last.get(host,0)+self.delay)
            self.last[host]=scheduled
        time.sleep(max(0,scheduled-time.monotonic()))
        req=urllib.request.Request(url,headers={'User-Agent':AGENT,'Accept-Encoding':'identity'})
        req.check_robots=check_robots
        with self.opener.open(req,timeout=self.timeout) as response:
            data=response.read(self.max_bytes+1)
            if len(data)>self.max_bytes: raise ValueError('response exceeds --max-mb; no truncated file saved')
            return data,response.url,dict(response.headers),response.status
    def allowed(self,url):
        with self.robot_lock:return self._allowed(url)
    def _allowed(self,url):
        parts=urlsplit(url);origin=f'{parts.scheme}://{parts.netloc}'
        if origin not in self.robots:
            try:
                raw,_,headers,_=self.raw(origin+'/robots.txt')
                text=decode_body(raw,headers).decode('utf-8','replace')
                parser=RobotRules(text);note='retrieved'
            except urllib.error.HTTPError as exc:
                if exc.code in (404,410): parser=RobotRules('');note=f'absent HTTP{exc.code}'
                else: parser=RobotRules('User-agent: *\nDisallow: /');note=f'unavailable HTTP{exc.code}; fail closed'
            except Exception as exc:
                parser=RobotRules('User-agent: *\nDisallow: /');note=f'unavailable {type(exc).__name__}; fail closed'
            self.robots[origin]=parser;self.robot_notes[origin]=note
        return self.robots[origin].can_fetch(AGENT,url)
    def fetch(self,url):
        url=normalized(url)
        if url in self.prefetched:return self.prefetched[url].result()
        return self._fetch(url)
    def prefetch(self,urls):
        for url in dict.fromkeys(urls):
            if url not in self.prefetched:self.prefetched[url]=self.pool.submit(self._fetch,url)
    def close(self):self.pool.shutdown(wait=True)
    def _fetch(self,url):
        url=normalized(url)
        if url in self.request_errors:raise RuntimeError('Already unavailable in this run: '+self.request_errors[url])
        try:return self._fetch_checked(url)
        except Exception as exc:
            self.request_errors[url]=f'{type(exc).__name__}: {exc}'
            raise
    def _fetch_checked(self,url):
        url=normalized(url)
        if not self.allowed(url): raise PermissionError('robots.txt does not permit this URL or could not be checked')
        result=self.raw(url,check_robots=True)
        if normalized(result[1])!=url and not self.allowed(result[1]):
            raise PermissionError('redirect destination not allowed by robots.txt')
        if re.search(r'/(?:login|signin|sign-in|auth)(?:[/?.]|$)',urlsplit(result[1]).path,re.I):
            raise PermissionError('redirected to authentication; not archived as a reference')
        return result

class VisibleText(HTMLParser):
    def __init__(self): super().__init__(convert_charrefs=True);self.skip=0;self.text=[]
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style'):self.skip+=1
    def handle_endtag(self,tag):
        if tag in ('script','style'):self.skip=max(0,self.skip-1)
    def handle_data(self,data):
        if not self.skip:self.text.append(data)
    def value(self): return ' '.join(''.join(self.text).split())

class ScriptURLs(HTMLParser):
    def __init__(self,origin):super().__init__();self.origin=origin;self.urls=[]
    def handle_starttag(self,tag,attrs):
        values=dict(attrs)
        if tag=='base' and values.get('href'):self.origin=urljoin(self.origin,values['href'])
        if tag=='script' and values.get('src') and values.get('type','').lower() in ('','module','text/javascript','application/javascript'):
            try:self.urls.append(normalized(urljoin(self.origin,values['src'])))
            except ValueError:pass

def presentation_status(record):
    """Frozen scripts do not prevent static presentation; keep all failure evidence."""
    if record.get('archive_status')=='failed':return record
    failures=record.get('unavailable_assets',{})
    inactive=[]
    if record.get('script_policy')=='disable' and pathlib.Path(record.get('file','')).suffix=='.html':
        raw=pathlib.Path(record['original_file']).read_bytes();headers=record.get('headers',{})
        data=decode_body(raw,headers)
        parser=ScriptURLs(record.get('final_url',record['url']))
        parser.feed(data.decode(charset(data,headers.get('Content-Type','')),errors='strict'))
        inactive=parser.urls
    record['inactive_script_urls']=inactive
    record['unavailable_presentation_assets']={url:reason for url,reason in failures.items() if url not in inactive}
    record['archive_status']='partial_static' if record['unavailable_presentation_assets'] else 'complete_static'
    return record

class Archive:
    def __init__(self,project,network=None,max_assets=2500,scripts='disable'):
        self.project=pathlib.Path(project).resolve()
        if not self.project.is_dir(): raise ValueError('project must be an existing project directory')
        if self.project==ROOT or ROOT not in self.project.parents or any(p.name in ('_Evidence','toolkit','reference_metrial') for p in [self.project,*self.project.parents] if p!=ROOT):
            raise ValueError('project must be inside the research root, not the root, toolkit, or evidence directory')
        self.out=self.project/'reference_metrial';self.out.mkdir(exist_ok=True)
        self.registry_dir=self.out/'_registry';self.registry_dir.mkdir(exist_ok=True)
        self.assets=self.registry_dir/'assets';self.assets.mkdir(exist_ok=True)
        self.network=network or Network();self.max_assets=max_assets;self.scripts=scripts
        self.cache_path=self.registry_dir/'assets.json'
        self.cache=load_json(self.cache_path) if self.cache_path.exists() else {}
        self.manifest_path=self.registry_dir/'materials.json'
        self.records=load_json(self.manifest_path) if self.manifest_path.exists() else {}
        self.failure_path=self.registry_dir/'unavailable.json'
        self.failure_cache=load_json(self.failure_path) if self.failure_path.exists() else {}
        for record in self.records.values():self.failure_cache.update(record.get('unavailable_assets',{}))
        self.repair_started=False
        self.page_dir=self.out
        self.used={};self.failed={};self.notes=[];self.new_assets=0;self.asset_attempts=0
    def relative(self,path,base): return pathlib.Path(os.path.relpath(path,base)).as_posix()
    def mark_used(self,url,seen=None):
        seen=set() if seen is None else seen
        if url in seen:return
        seen.add(url)
        if url not in self.cache:raise ValueError('missing cached dependency: '+url)
        record=self.cache[url];path=self.out/record['file']
        if not path.is_file() or digest(path.read_bytes())!=record['sha256']:raise ValueError('corrupt cached dependency: '+url)
        self.used[url]=record
        self.failed.update(record.get('unavailable_dependencies',{}))
        for dependency in record.get('dependencies',[]):self.mark_used(dependency,seen)
    def local_asset(self,path):return self.page_dir/'assets'/path.relative_to(self.assets)
    def asset_relative(self,path,base):
        # Cached CSS and its imports use the same category hierarchy as each page.
        if self.assets==base or self.assets in pathlib.Path(base).parents:return self.relative(path,base)
        return self.relative(self.local_asset(path),base)
    def publish(self,name,record,dimensions):
        record['aliases']=sorted(set(record.get('aliases',[])+[name]))
        record['used_by']=sorted(set(record.get('used_by',[])+dimensions))
        for alias in record['aliases']:self.records[alias]=record
        save_json(self.manifest_path,self.records)
        if record.get('file'):save_json(pathlib.Path(record['file']).parent/'metadata.json',record)
        rows=[]
        for item in {r['url']:r for r in self.records.values()}.values():
            label=html.escape(' / '.join(item.get('aliases',[item['id']])))
            link=html.escape(self.relative(pathlib.Path(item['file']),self.out)) if item.get('file') else ''
            rows.append('<li><a href="'+link+'">'+label+'</a> — '+html.escape(item['archive_status'])+'</li>')
        (self.out/'index.html').write_text('<!doctype html><html lang="zh"><meta charset="utf-8"><title>参考资料索引</title><h1>参考资料</h1><p>每项资料独立目录；缺失依赖和采集时间见 metadata.json。</p><ul>'+''.join(rows)+'</ul></html>',encoding='utf-8')
        return record
    def asset(self,value,origin,base,depth=0):
        value=html.unescape(value.strip())
        if not value or value.startswith(('#','data:','blob:','javascript:','mailto:')): return value
        url=urljoin(origin,value);fragment=urlsplit(url).fragment
        try:url=normalized(url)
        except ValueError:
            # Published HTML sometimes contains author-local file references.
            # Preserve and disclose them; never read the host filesystem or abort the page.
            self.failed[url]='unsupported/non-public asset URL; preserved without access'
            return url
        if depth>12:
            self.failed[url]='dependency depth exceeds 12';return url
        cached=self.cache.get(url)
        if cached:
            path=self.out/cached['file']
            if path.is_file() and digest(path.read_bytes())==cached['sha256']:
                try:
                    self.mark_used(url)
                    return self.asset_relative(path,base)+('#'+fragment if fragment else '')
                except ValueError:self.used.pop(url,None)
        if url in self.failed:return url
        if url in self.failure_cache:
            self.failed[url]=self.failure_cache[url];return url
        if url in self.used:
            return self.asset_relative(self.out/self.used[url]['file'],base)+('#'+fragment if fragment else '')
        if self.asset_attempts>=self.max_assets:
            self.failed[url]='asset limit reached; increase --max-assets and rerun';return url
        self.asset_attempts+=1
        try:
            raw,final,headers,status=self.network.fetch(url)
            data=decode_body(raw,headers);kind=headers.get('Content-Type','')
            suffix=extension(data,kind,final)
            if suffix=='.html':raise ValueError('asset returned HTML rather than image/style/script/font')
            category=('styles' if suffix=='.css' else 'scripts' if suffix=='.js' else 'fonts' if suffix in ('.woff','.woff2','.ttf','.otf','.eot') else 'images' if suffix in ('.png','.jpg','.jpeg','.gif','.svg','.webp','.avif','.ico') else 'other')
            path=self.assets/category/(digest(url.encode())[:24]+suffix);path.parent.mkdir(exist_ok=True)
            record={'url':url,'final_url':final,'file':self.relative(path,self.out),'status':status,'retrieved_at_utc':utc(),'raw_sha256':digest(raw)}
            # Reserve before recursively visiting CSS imports to terminate cycles.
            self.used[url]=record
            if suffix=='.css':
                dependencies=PresentationCSSURLs(data.decode(charset(data,kind),errors='strict'),final)
                text=data.decode(charset(data,kind),errors='strict')
                data=self.css(text,final,path.parent,depth+1).encode('utf-8')
                record['localized_encoding']='utf-8'
                record['dependencies']=[u for u in dependencies if u in self.used and u!=url]
                record['unavailable_dependencies']={u:self.failed[u] for u in dependencies if u in self.failed}
            path.write_bytes(data);record['sha256']=digest(data);record['bytes']=len(data)
            self.cache[url]=record
            self.new_assets+=1
            save_json(self.cache_path,self.cache)
            if self.new_assets%25==0:print(f'  assets: {self.new_assets} downloaded, {len(self.failed)} unavailable',flush=True)
            return self.asset_relative(path,base)+('#'+fragment if fragment else '')
        except Exception as exc:
            self.used.pop(url,None);self.failed[url]=f'{type(exc).__name__}: {exc}'
            self.failure_cache[url]=self.failed[url];return url
    def css(self,text,origin,base,depth=0):
        pattern=r'url\(\s*(?:"([^"]*)"|\'([^\']*)\'|([^)]*?))\s*\)'
        candidates=[next(x for x in match.groups() if x is not None).strip() for match in re.finditer(pattern,text,re.I)]
        candidates += [match[1] for match in re.finditer(r'@import\s+["\']([^"\']+)["\']',text,re.I)]
        pending=[]
        for value in candidates:
            if not value or value.startswith(('#','data:','blob:')):continue
            try:url=normalized(urljoin(origin,value))
            except ValueError:continue
            if url not in self.used and url not in self.cache and url not in self.failed and url not in self.failure_cache:pending.append(url)
        self.network.prefetch(pending[:max(0,self.max_assets-self.new_assets)])
        text=re.sub(pattern,lambda m:'url("'+self.asset(next(x for x in m.groups() if x is not None),origin,base,depth).replace('"','%22')+'")',text,flags=re.I)
        # Quoted @import form not covered by url(...).
        return re.sub(r'(@import\s+)(["\'])([^"\']+)\2',lambda m:m[1]+m[2]+self.asset(m[3],origin,base,depth)+m[2],text,flags=re.I)
    def srcset(self,value,origin,base):
        if 'data:' in value:return value
        entries=[]
        for item in value.split(','):
            parts=item.strip().split()
            if parts:entries.append(' '.join([self.asset(parts[0],origin,base),*parts[1:]]))
        return ', '.join(entries)
    def collect(self,name,url,import_dir=None,refresh=False,expected=None,dimensions=None,repair_assets=False):
        name=safe_name(name);url=normalized(url)
        dimensions=dimensions or []
        if isinstance(dimensions,str):dimensions=[dimensions]
        old=self.records.get(name)
        if old and old.get('url')!=url:raise ValueError(f'{name} already belongs to another URL; choose a new name')
        old=old or next((r for r in self.records.values() if r['url']==url),None)
        if old and old.get('file') and expected not in (None,'any',pathlib.Path(old['file']).suffix.lstrip('.')):
            raise ValueError('existing URL archive does not match expected type')
        intact=False
        original_intact=False
        if old and old.get('file'):
            paths=[(pathlib.Path(old['file']),old.get('sha256')),(pathlib.Path(old.get('original_file','')),old.get('original_sha256'))]
            intact=all(p.is_file() and digest(p.read_bytes())==sha for p,sha in paths)
        if old and old.get('original_file'):
            original_path=pathlib.Path(old['original_file'])
            original_intact=original_path.is_file() and digest(original_path.read_bytes())==old.get('original_sha256')
        if intact and not refresh and not repair_assets and old.get('script_policy')==self.scripts:
            if pathlib.Path(old['file']).suffix=='.html' and challenge_page(pathlib.Path(old['file']).read_text(encoding='utf-8')):
                intact=False
            assets_intact=all((self.out/r.get('local_file',r['file'])).is_file() and digest((self.out/r.get('local_file',r['file'])).read_bytes())==r['sha256'] for r in old.get('assets',[]))
            if intact and assets_intact:
                print(name,'reused URL archive',flush=True)
                return self.publish(name,old,dimensions)
        self.used={};self.failed={};self.notes=[]
        self.network.prefetched={}
        if repair_assets:
            if not self.repair_started:
                self.network.request_errors.clear();self.failure_cache={};self.repair_started=True
            # Revisit CSS with missing imports/fonts; complete assets remain reusable.
            for key in list(self.cache):
                if self.cache[key].get('unavailable_dependencies'):self.cache.pop(key)
        record={'id':old['id'] if old else name,'url':url,'archived_at_utc':utc(),'tool':'toolkit/download_materials.py','script_policy':self.scripts,
                'aliases':old.get('aliases',[]) if old else [],'used_by':old.get('used_by',[]) if old else []}
        try:
            source=None
            if original_intact and not refresh:
                raw=pathlib.Path(old['original_file']).read_bytes();final=old['final_url'];headers=old['headers'];status=old['status'];source=old
            elif import_dir:
                source_meta=pathlib.Path(import_dir)/(name+'.meta.json')
                if source_meta.exists():
                    source=load_json(source_meta)
                    if source.get('url')!=url or source.get('status')!=200:raise ValueError('import record URL/status does not match')
                    source_path=pathlib.Path(source['file'])
                    if not source_path.is_absolute():source_path=pathlib.Path(import_dir)/source_path.name
                    raw=source_path.read_bytes()
                    if digest(raw)!=source['sha256']:raise ValueError('import original SHA256 mismatch')
                    final=source.get('final_url',url);headers=source.get('headers',{'Content-Type':source.get('content_type','')});status=200
                    record['imported_from']=str(source_meta.resolve())
            if source is None:raw,final,headers,status=self.network.fetch(url)
            data=decode_body(raw,headers);kind=headers.get('Content-Type','');suffix=extension(data,kind,final)
            if expected and expected not in ('any',suffix.lstrip('.')):raise ValueError(f'expected {expected}, received {suffix}')
            category='webpages' if suffix=='.html' else 'documents' if suffix=='.pdf' else 'data'
            self.page_dir=material_directory(self.out,category,record['id'],url);self.page_dir.mkdir(parents=True,exist_ok=True)
            record.update(status=status,final_url=final,headers=headers,content_type=kind,
                          retrieved_at_utc=source.get('retrieved_at_utc',utc()) if source else utc(),raw_sha256=digest(raw),bytes=len(raw))
            original=self.page_dir/'original.response';original.write_bytes(raw)
            path=self.page_dir/('index.html' if suffix=='.html' else 'document.pdf' if suffix=='.pdf' else 'content'+suffix)
            record['original_file']=str(original);record['original_sha256']=digest(raw)
            if suffix=='.html':
                decoded=data.decode(charset(data,kind),errors='strict')
                if challenge_page(decoded):
                    raise ValueError('challenge page; not accepted as reference content')
                candidates=PresentationURLs(decoded,final);candidates.feed(decoded)
                pending=[]
                for resource in dict.fromkeys(candidates.urls):
                    cached=self.cache.get(resource)
                    if resource not in self.failure_cache and (not cached or not (self.out/cached['file']).is_file()):pending.append(resource)
                self.network.prefetch(pending[:max(0,self.max_assets-self.new_assets)])
                parser=Localize(self,decoded,final);parser.feed(decoded);parser.close()
                localized=parser.result()
                before=VisibleText();before.feed(decoded);after=VisibleText();after.feed(localized)
                if before.value()!=after.value():raise ValueError('HTML visible text changed during localization')
                data=localized.encode('utf-8')
                record.update(localized_encoding='utf-8',visible_text_sha256=digest(before.value().encode()),visible_text_unchanged=True,
                              links=parser.links,images=parser.images)
                (self.page_dir/'text.txt').write_text(before.value(),encoding='utf-8')
                for asset in self.used.values():
                    source_path=self.out/asset['file'];target=self.local_asset(source_path);target.parent.mkdir(parents=True,exist_ok=True)
                    if target.exists():target.unlink()
                    try:os.link(source_path,target)
                    except OSError:shutil.copy2(source_path,target)
            path.write_bytes(data)
            record.update(file=str(path),sha256=digest(data),localized_bytes=len(data),
                          archive_status='partial_static' if self.failed else 'complete_static',
                          fidelity='Original bytes retained; static markup/text preserved. Dynamic content and pixel-perfect fidelity are not guaranteed.')
        except Exception as exc:record.update(archive_status='failed',error=f'{type(exc).__name__}: {exc}')
        record.update(assets=[dict(r,local_file=self.relative(self.local_asset(self.out/r['file']),self.out)) for r in self.used.values()],
                      unavailable_assets=dict(self.failed),notes=list(dict.fromkeys(self.notes)),robots=dict(self.network.robot_notes))
        presentation_status(record)
        save_json(self.cache_path,self.cache)
        save_json(self.failure_path,self.failure_cache)
        self.publish(name,record,dimensions)
        print(name,record['archive_status'],f'assets={len(self.used)} unavailable={len(self.failed)}',flush=True)
        return record


def PresentationCSSURLs(text,origin):
    values=[next(x for x in m.groups() if x is not None).strip() for m in re.finditer(r"url\(\s*(?:\"([^\"]*)\"|'([^']*)'|([^)]*?))\s*\)",text,re.I)]
    values += [m[1] for m in re.finditer(r"@import\s+[\"']([^\"']+)[\"']",text,re.I)]
    result=[]
    for value in values:
        if not value or value.startswith(('#','data:','blob:')):continue
        try:result.append(normalized(urljoin(origin,value)))
        except ValueError:pass
    return list(dict.fromkeys(result))

class PresentationURLs(HTMLParser):
    """Discover independent HTML assets for bounded parallel prefetch."""
    def __init__(self,text,origin):
        super().__init__();self.origin=origin;self.urls=[]
        base=re.search(r'<base\b[^>]*href\s*=\s*["\']([^"\']+)',text,re.I)
        if base:self.origin=urljoin(origin,html.unescape(base[1]))
    def add(self,value):
        if not value or value.startswith(('#','data:','blob:','javascript:')):return
        try:self.urls.append(normalized(urljoin(self.origin,value)))
        except ValueError:pass
    def handle_starttag(self,tag,attrs):
        values=dict(attrs)
        for key,value in attrs:
            if value is None:continue
            if (key=='src' and tag in ('img','script','source','video','audio','input')) or (key=='poster' and tag=='video') or (tag=='link' and key=='href' and bool(set(values.get('rel','').lower().split()) & {'stylesheet','icon','preload','modulepreload','apple-touch-icon'})) or (key in ('data-src','data-lazy-src') and tag in ('img','source')):self.add(value)
            if key in ('srcset','data-srcset') and 'data:' not in value:
                for part in value.split(','):
                    fields=part.strip().split()
                    if fields:self.add(fields[0])

def set_attr(tag,name,value):
    pattern=r'(\s'+re.escape(name)+r'\s*=\s*)(?:"[^"]*"|\'[^\']*\'|[^\s>]+)'
    replacement=lambda m:m[1]+'"'+html.escape(value,quote=True)+'"'
    if re.search(pattern,tag,re.I):return re.sub(pattern,replacement,tag,count=1,flags=re.I)
    return re.sub(r'\s*/?>$',lambda m:' '+name+'="'+html.escape(value,quote=True)+'"'+m[0],tag)

class Localize(HTMLParser):
    def __init__(self,archive,text,origin):
        super().__init__(convert_charrefs=False)
        self.archive=archive;self.text=text;self.origin=origin;self.edits=[];self.style=False;self.links=[];self.images=[]
        self.offsets=[0]
        for match in re.finditer('\n',text):self.offsets.append(match.end())
        # A document base changes all resource resolution, irrespective of tag order.
        base=re.search(r'<base\b[^>]*href\s*=\s*["\']([^"\']+)',text,re.I)
        if base:self.origin=urljoin(origin,html.unescape(base[1]))
    def pos(self):line,col=self.getpos();return self.offsets[line-1]+col
    def handle_startendtag(self,tag,attrs):self.handle_starttag(tag,attrs)
    def handle_starttag(self,tag,attrs):
        values=dict(attrs);raw=self.get_starttag_text();new=raw;a=self.archive
        if tag=='base':new=''
        elif tag=='meta' and values.get('http-equiv','').lower()=='content-security-policy':new=''
        else:
            for key,value in attrs:
                if value is None:continue
                resource=(key=='src' and tag in ('img','script','source','video','audio','input')) or (key=='poster' and tag=='video') or (tag=='link' and key=='href' and bool(set(values.get('rel','').lower().split()) & {'stylesheet','icon','preload','modulepreload','apple-touch-icon'}))
                if resource:
                    local=a.asset(value,self.origin,a.page_dir);new=set_attr(new,key,local)
                    if tag=='img':self.images.append(urljoin(self.origin,value))
                    # SRI hashes no longer match rewritten CSS; raw original is preserved separately.
                    new=re.sub(r'\s(?:integrity|crossorigin)\s*=\s*(?:"[^"]*"|\'[^\']*\')','',new,flags=re.I)
                elif key in ('srcset','data-srcset'):
                    new=set_attr(new,key,a.srcset(value,self.origin,a.page_dir))
                elif key in ('data-src','data-lazy-src') and tag in ('img','source'):
                    localized=a.asset(value,self.origin,a.page_dir);new=set_attr(new,key,localized)
                    if tag=='img':new=set_attr(new,'src',localized)
                elif key=='style':new=set_attr(new,key,a.css(value,self.origin,a.page_dir))
                elif key in ('href','action') and value and not value.startswith(('#','data:','javascript:','mailto:','tel:')):
                    new=set_attr(new,key,urljoin(self.origin,value))
            if tag=='meta' and ('charset' in values):new=set_attr(new,'charset','utf-8')
            if tag=='meta' and values.get('http-equiv','').lower()=='content-type':new=set_attr(new,'content','text/html; charset=utf-8')
            if tag=='script' and values.get('type','').lower() in ('','module','text/javascript','application/javascript'):
                a.notes.append('Executable scripts present: live interaction, API-fetched content, and media are not guaranteed offline.')
                if a.scripts=='disable':new=set_attr(new,'type','application/x-archived-script')
            if tag in ('iframe','object','embed'):
                a.notes.append('Embedded external frames/media are not recursively archived; review them separately.')
            if tag=='a' and values.get('href'):self.links.append(urljoin(self.origin,values['href']))
        if raw!=new:self.edits.append((self.pos(),len(raw),new))
        if tag=='style':self.style=True
    def handle_endtag(self,tag):
        if tag=='style':self.style=False
    def handle_data(self,data):
        if self.style:
            new=self.archive.css(data,self.origin,self.archive.page_dir)
            if new!=data:self.edits.append((self.pos(),len(data),new))
    def result(self):
        text=self.text
        for pos,length,new in sorted(self.edits,reverse=True):text=text[:pos]+new+text[pos+length:]
        if not re.search(r'<meta\b[^>]*charset',text[:20000],re.I):
            if re.search(r'<head\b',text,re.I):text=re.sub(r'(<head\b[^>]*>)',r'\1<meta charset="utf-8">',text,count=1,flags=re.I)
            elif re.search(r'<html\b',text,re.I):text=re.sub(r'(<html\b[^>]*>)',r'\1<head><meta charset="utf-8"></head>',text,count=1,flags=re.I)
            else:text='<meta charset="utf-8">'+text
        return text

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--project',required=True,help='Existing project path relative to research root, or its absolute path')
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--manifest',type=pathlib.Path,help='JSON object name->URL, or list of {name,url,expected}')
    group.add_argument('--url',help='One public URL')
    parser.add_argument('--name',help='File stem, required with --url')
    parser.add_argument('--expected',choices=('any','html','pdf','json'),default='any')
    parser.add_argument('--import-dir',type=pathlib.Path,help='Reuse verified existing raw snapshots and fetch their dependencies through this script')
    parser.add_argument('--refresh',action='store_true',help='Explicitly refetch main documents; verified dependencies remain cached')
    parser.add_argument('--repair-assets',action='store_true',help='Rebuild from saved original; retry unavailable dependencies without refetching the main document')
    parser.add_argument('--dimension',action='append',default=[],help='Report dimension that uses this material; may be repeated')
    parser.add_argument('--collection',help='Independent topic folder under reference_metrial; reuses shared URL registry and hard-linked files')
    parser.add_argument('--proxy',default=os.environ.get('REFERENCE_DOWNLOAD_PROXY'),help='Optional HTTP(S) proxy; otherwise normal environment proxy settings')
    parser.add_argument('--delay',type=float,default=.3)
    parser.add_argument('--timeout',type=float,default=25)
    parser.add_argument('--max-mb',type=int,default=100)
    parser.add_argument('--max-assets',type=int,default=2500)
    parser.add_argument('--jobs',type=int,default=4,help='Concurrent HTML dependency downloads; host request spacing still applies')
    parser.add_argument('--scripts',choices=('disable','preserve'),default='disable',help='Freeze executable scripts by default, preserving their source in HTML')
    parser.add_argument('--strict',action='store_true',help='Return nonzero also for incomplete presentation dependencies')
    args=parser.parse_args(argv)
    if args.delay<0 or args.timeout<=0 or args.max_mb<=0 or args.max_assets<0 or args.jobs<1 or args.jobs>8:parser.error('limits must be positive; jobs 1–8 (delay and max-assets may be zero)')
    project=pathlib.Path(args.project)
    if not project.is_absolute():project=ROOT/project
    archive=Archive(project,Network(args.proxy,args.delay,args.timeout,args.max_mb*1024*1024,args.jobs),args.max_assets,args.scripts)
    if args.manifest:
        items=json.loads(args.manifest.read_text(encoding='utf-8-sig'))
        entries=[{'name':name,'url':url} for name,url in items.items()] if isinstance(items,dict) else items
    else:
        if not args.name:parser.error('--name is required with --url')
        entries=[{'name':args.name,'url':args.url,'expected':args.expected}]
    # Validate the full batch before any main document is downloaded.
    names=set()
    for entry in entries:
        name=safe_name(entry['name']);normalized(entry['url'])
        if name.casefold() in names:raise ValueError(f'duplicate name: {name}')
        names.add(name.casefold())
    if args.collection:
        safe_name(args.collection)
        if args.collection in ('_registry','derived','webpages','documents','data'):parser.error('reserved collection name')
    lock=archive.project/'.reference_download.lock'
    try:
        lock_fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
    except FileExistsError:
        archive.network.close()
        raise RuntimeError('Another downloader holds '+str(lock)+'; verify it has exited before removing a stale lock')
    try:
        os.write(lock_fd,str(os.getpid()).encode());os.close(lock_fd)
        records=[archive.collect(entry['name'],entry['url'],args.import_dir,args.refresh,entry.get('expected',args.expected),entry.get('used_by',entry.get('dimensions',args.dimension)),args.repair_assets) for entry in entries]
        if args.collection:export_collection(archive,args.collection,records)
    finally:
        archive.network.close();lock.unlink()
    summary={status:sum(r['archive_status']==status for r in records) for status in ('complete_static','partial_static','failed')}
    save_json(archive.registry_dir/'last_run.json',{'time_utc':utc(),'summary':summary,'names':[r['id'] for r in records],'network_requests_including_robots':archive.network.requests,'new_assets':archive.new_assets,'asset_attempts':archive.asset_attempts,'tool':str(pathlib.Path(__file__).resolve())})
    print(json.dumps(summary),flush=True)
    return 1 if summary['failed'] or (args.strict and summary['partial_static']) else 0

if __name__=='__main__':sys.exit(main())
