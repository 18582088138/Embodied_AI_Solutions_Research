"""Deterministic local-server tests; no external website access."""
import gzip,json,pathlib,tempfile,threading,unittest,urllib.request
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import download_materials as dm

HTML='''<!doctype html><html><head><meta charset="utf-8"><base href="/nested/">
<link rel="stylesheet" href="style.css" integrity="old"><style>.x{background:url('../image.png')}</style>
<script src="../app.js"></script></head><body><h1>中文标题 &amp; 参数</h1>
<p class="x">内容、格式应保留。</p><img src="../image.png" srcset="../image.png 1x, ../second.png 2x">
<a href="detail.html">原站链接</a></body></html>'''.encode()
class Handler(BaseHTTPRequestHandler):
    hits=[]
    resources_alias=False
    repair_missing=False
    def log_message(self,*args):pass
    def do_GET(self):
        self.hits.append(self.path)
        resources={
          '/robots.txt':('text/plain',b'User-agent: *\nDisallow: /blocked\n'),
          '/index.html':('text/html; charset=utf-8',gzip.compress(HTML)),
          '/nested/style.css':('text/css',b'@import "more.css"; h1{color:rgb(20,40,60)} @font-face{font-family:x;src:url("../font.woff2")}'),
          '/nested/more.css':('text/css',b'@import "style.css"; p{background:url(../second.png)}'),
          '/image.png':('image/png',b'\x89PNG\r\nmock-image'),
          '/second.png':('image/png',b'\x89PNG\r\nother-image'),
          '/font.woff2':('font/woff2',b'wOF2mock-font'),
          '/app.js':('application/javascript',b'window.example=true;'),
          '/manual':('application/pdf',b'%PDF-1.7\nmock-manual'),
          '/broken.html':('text/html',b'<html><body>Test<img src="/missing.png"></body></html>'),
          '/localref.html':('text/html',b'<html><body>Public text<img src="file:///author/temp/image.png"></body></html>'),
        }
        if self.resources_alias:resources['/other.html']=resources['/index.html']
        if self.repair_missing:resources['/missing.png']=resources['/image.png']
        if self.path=='/redirect':
            self.send_response(302);self.send_header('Location','/blocked');self.end_headers();return
        if self.path not in resources:self.send_response(404);self.end_headers();return
        kind,data=resources[self.path];self.send_response(200);self.send_header('Content-Type',kind)
        if self.path in ('/index.html','/other.html'):self.send_header('Content-Encoding','gzip')
        self.end_headers();self.wfile.write(data)

class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original_root=dm.ROOT
        cls.fixture_root=tempfile.TemporaryDirectory(prefix='embodied-fixtures-')
        dm.ROOT=pathlib.Path(cls.fixture_root.name)
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
        cls.url=f'http://127.0.0.1:{cls.server.server_port}'
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close();cls.thread.join()
        dm.ROOT=cls.original_root;cls.fixture_root.cleanup()
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='archive-test-',dir=dm.ROOT)
        self.project=pathlib.Path(self.temp.name)
        network=dm.Network(delay=0,timeout=2)
        network.opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),dm.CheckedRedirect(network))
        self.archive=dm.Archive(self.project,network)
    def tearDown(self):self.archive.network.close();self.temp.cleanup()
    def test_author_local_asset_is_preserved_unavailable(self):
        result=self.archive.collect('localref',self.url+'/localref.html')
        self.assertEqual(result['archive_status'],'partial_static')
        self.assertTrue(result['visible_text_unchanged'])
        self.assertIn('file:///author/temp/image.png',result['unavailable_assets'])
        self.assertIn('Public text',pathlib.Path(result['file']).read_text(encoding='utf-8'))
    def test_html_resources_text_gzip_and_cache(self):
        result=self.archive.collect('page',self.url+'/index.html')
        self.assertEqual(result['archive_status'],'complete_static')
        self.assertTrue(result['visible_text_unchanged'])
        page=pathlib.Path(result['file']).read_text(encoding='utf-8')
        self.assertIn('中文标题 &amp; 参数',page);self.assertNotIn('<base',page)
        self.assertIn('application/x-archived-script',page);self.assertNotIn('integrity=',page)
        self.assertIn(self.url+'/nested/detail.html',page)
        self.assertEqual(len(result['assets']),6)
        self.assertTrue(all((self.archive.out/a['file']).exists() for a in result['assets']))
        self.assertTrue(pathlib.Path(result['original_file']).read_bytes().startswith(b'\x1f\x8b'))
        hits=len(Handler.hits);self.archive.collect('page',self.url+'/index.html');self.assertEqual(len(Handler.hits),hits)
    def test_pdf_content_type_and_expected(self):
        result=self.archive.collect('manual',self.url+'/manual',expected='pdf')
        self.assertEqual(pathlib.Path(result['file']).suffix,'.pdf')
        self.assertEqual(self.archive.collect('wrong',self.url+'/index.html',expected='pdf')['archive_status'],'failed')
    def test_robots_and_redirect(self):
        self.assertEqual(self.archive.collect('blocked',self.url+'/blocked')['archive_status'],'failed')
        self.assertEqual(self.archive.collect('redirect',self.url+'/redirect')['archive_status'],'failed')
        self.assertNotIn('/blocked',Handler.hits)
    def test_missing_dependency_is_explicit(self):
        result=self.archive.collect('partial',self.url+'/broken.html')
        self.assertEqual(result['archive_status'],'partial_static')
        self.assertIn(self.url+'/missing.png',result['unavailable_assets'])
    def test_missing_frozen_script_does_not_hide_presentation_gaps(self):
        result=self.archive.collect('partial',self.url+'/broken.html')
        result['unavailable_assets'][self.url+'/missing.js']='404'
        original=pathlib.Path(result['original_file'])
        original.write_bytes(b'<html><body>Test<img src="/missing.png"><script src="/missing.js"></script></body></html>')
        dm.presentation_status(result)
        self.assertIn(self.url+'/missing.js',result['unavailable_assets'])
        self.assertNotIn(self.url+'/missing.js',result['unavailable_presentation_assets'])
        self.assertIn(self.url+'/missing.png',result['unavailable_presentation_assets'])
    def test_saved_original_repairs_deleted_local_assets(self):
        result=self.archive.collect('page',self.url+'/index.html')
        original=pathlib.Path(result['original_file']).read_bytes()
        source=self.project/'legacy';source.mkdir()
        (source/'page.html').write_bytes(original)
        dm.save_json(source/'page.meta.json',{'id':'page','url':self.url+'/index.html','status':200,'file':str(source/'page.html'),'sha256':dm.digest(original),'headers':{'Content-Type':'text/html; charset=utf-8','Content-Encoding':'gzip'}})
        (self.archive.out/result['assets'][0]['local_file']).unlink()
        hits=len(Handler.hits)
        result=self.archive.collect('page',self.url+'/index.html',import_dir=source)
        self.assertEqual(result['archive_status'],'complete_static')
        self.assertEqual(pathlib.Path(result['original_file']).read_bytes(),original)
        self.assertEqual(len(Handler.hits),hits)
        self.assertTrue((self.archive.out/result['assets'][0]['local_file']).exists())
    def test_url_alias_dimensions_partial_and_cross_run_reuse(self):
        result=self.archive.collect('one',self.url+'/broken.html',dimensions=['hardware'])
        hits=len(Handler.hits)
        other=self.archive.collect('two',self.url+'/broken.html#section',dimensions=['software'])
        self.assertEqual(other['file'],result['file'])
        self.assertEqual(other['used_by'],['hardware','software'])
        self.assertEqual(len(Handler.hits),hits)
        next_archive=dm.Archive(self.project,self.archive.network)
        next_archive.collect('three',self.url+'/broken.html')
        self.assertEqual(len(Handler.hits),hits)
    def test_cross_page_dependencies_local_paths_and_no_duplicate_requests(self):
        first=self.archive.collect('first',self.url+'/index.html')
        hits=len(Handler.hits)
        second=self.archive.collect('second',self.url+'/index.html?version=2')
        # This distinct query is not merged; fixture does not serve it.
        self.assertEqual(second['archive_status'],'failed')
        Handler.resources_alias=True
        second=self.archive.collect('third',self.url+'/other.html')
        Handler.resources_alias=False
        self.assertEqual(second['archive_status'],'complete_static')
        self.assertEqual(len(second['assets']),6)
        self.assertEqual(len(Handler.hits),hits+2)
        for record in [first,second]:
            folder=pathlib.Path(record['file']).parent
            page=pathlib.Path(record['file']).read_text(encoding='utf-8')
            self.assertIn('assets/styles/',page)
            for asset in record['assets']:
                local=self.archive.out/asset['local_file']
                self.assertTrue(local.is_relative_to(folder));self.assertTrue(local.exists())
                if local.suffix=='.css':
                    import re
                    for value in re.findall(r'url\("([^"]+)"\)|@import "([^"]+)"',local.read_text()):
                        ref=next(v for v in value if v)
                        self.assertTrue((local.parent/ref).is_file(),ref)
    def test_normalization_preserves_version_queries(self):
        self.assertEqual(dm.normalized('https://EXAMPLE.com:443/a#x'),'https://example.com/a')
        self.assertNotEqual(dm.normalized('https://example.com/a?v=1'),dm.normalized('https://example.com/a?v=2'))
    def test_windows_path_budget(self):
        path=dm.material_directory(self.archive.out,'webpages','NVIDIA_'+'LongTitle'*16,self.url+'/page')
        self.assertLessEqual(len(str(path)),200)
        self.assertLess(len(str(path/'assets/scripts'/('a'*24+'.woff2'))),260)
        other=dm.material_directory(self.archive.out,'webpages','NVIDIA_'+'LongTitle'*16,self.url+'/other')
        self.assertNotEqual(path,other)
    def test_explicit_repair_and_refresh(self):
        self.archive.collect('partial',self.url+'/broken.html')
        count=Handler.hits.count('/broken.html')
        Handler.repair_missing=True
        try:
            repaired=self.archive.collect('partial',self.url+'/broken.html',repair_assets=True)
            self.assertEqual(repaired['archive_status'],'complete_static')
            self.assertEqual(Handler.hits.count('/broken.html'),count)
            self.archive.collect('partial',self.url+'/broken.html',refresh=True)
            self.assertEqual(Handler.hits.count('/broken.html'),count+1)
        finally:Handler.repair_missing=False
    def test_name_and_scope_validation(self):
        for name in ['../escape','CON','a/b','..']:
            with self.assertRaises(ValueError):dm.safe_name(name)
        with self.assertRaises(ValueError):dm.Archive(dm.ROOT)
        self.archive.collect('same',self.url+'/manual')
        with self.assertRaises(ValueError):self.archive.collect('same',self.url+'/index.html')
    def test_collection_offline_dependencies_dedup_and_scope(self):
        rec=self.archive.collect('topic',self.url+'/index.html',dimensions=['08_Core_Technology_Moat'])
        requests=len(Handler.hits)
        folder=dm.export_collection(self.archive,'08_core',[rec,rec])
        view=json.loads((folder/'collection.json').read_text(encoding='utf-8'))
        self.assertEqual(len(view['materials']),1)
        page=pathlib.Path(view['materials'][0]['file'])
        self.assertEqual(page.read_bytes(),pathlib.Path(rec['file']).read_bytes())
        for asset in rec['assets']:
            relative=(self.archive.out/asset['local_file']).relative_to(pathlib.Path(rec['file']).parent)
            self.assertTrue((page.parent/relative).is_file())
        dm.export_collection(self.archive,'08_core',[rec])
        self.assertEqual(len(Handler.hits),requests)
        repeated=json.loads((folder/'collection.json').read_text(encoding='utf-8'))
        self.assertEqual(repeated['new_hardlinks']+repeated['new_local_copies'],0)
        for bad in ['../escape','_registry','documents']:
            with self.assertRaises(ValueError):dm.export_collection(self.archive,bad,[rec])
    def test_robots_wildcards_and_specific_agents(self):
        rules=dm.RobotRules('User-agent: *\nDisallow: /*?private=*\nDisallow: /docs/\nAllow: /docs/open/\nUser-agent: OtherBot\nDisallow: /')
        self.assertFalse(rules.can_fetch(dm.AGENT,self.url+'/index?private=yes'))
        self.assertFalse(rules.can_fetch(dm.AGENT,self.url+'/docs/private'))
        self.assertTrue(rules.can_fetch(dm.AGENT,self.url+'/docs/open/file'))
        self.assertFalse(rules.can_fetch('OtherBot',self.url+'/index'))
    def test_challenge_after_large_inline_prefix(self):
        page='<html><head><script>'+('x'*25000)+"</script></head><body>Making sure you're not a bot! Protected by Anubis</body></html>"
        self.assertTrue(dm.challenge_page(page))
        self.assertTrue(dm.challenge_page("<html>Making sure you&#39;re <b>not</b> a bot!</html>"))
        self.assertTrue(dm.challenge_page("<html>Protected by <a href='/'>Anubis</a></html>"))
        self.assertFalse(dm.challenge_page(HTML.decode()))

    def test_script_only_cookie_challenge(self):
        self.assertTrue(dm.challenge_page('<html><script>var arg1="'+'A'*40+'"; var encoded="YWN3X3NjX192Mj0=";</script></html>'))
        self.assertFalse(dm.challenge_page('<html><body>Valid article</body><script>var arg1="'+'A'*40+'";</script></html>'))

if __name__=='__main__':unittest.main()
