"""Behavioral checks in isolated local fixtures, without public network access."""
import contextlib,hashlib,io,json,pathlib,tempfile,unittest
import check_report as cr
from test_download_materials import Tests as DownloadTests

class ReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):DownloadTests.setUpClass()
    @classmethod
    def tearDownClass(cls):DownloadTests.tearDownClass()
    def setUp(self):
        import download_materials as dm
        import urllib.request
        self.temp=tempfile.TemporaryDirectory(prefix='report-check-',dir=dm.ROOT)
        self.project=pathlib.Path(self.temp.name)
        network=dm.Network(delay=0,timeout=2)
        network.opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),dm.CheckedRedirect(network))
        self.archive=dm.Archive(self.project,network)
        with contextlib.redirect_stdout(io.StringIO()):
            self.record=self.archive.collect('official',DownloadTests.url+'/index.html')
            # A failed research candidate must not invalidate an otherwise valid cited report.
            self.archive.collect('failed_candidate',DownloadTests.url+'/blocked')
        self.report=self.project/'01_Hardware_Platform.md'
        text='# 合成测试报告\n\n'+('条件与机制分析，测试占位材料不作行业事实。'*110)+'\n\n'
        text+='| 方案 | 条件 |\n|---|---|\n| 合成 | 本地测试 |\n\n'
        text+='## 参考资料与本地原文\n\n[原文]('+self.record['url']+')\n\n[归档]('+pathlib.Path(self.record['file']).as_posix()+')\n'
        self.report.write_text(text,encoding='utf-8')
        other=self.project/'02_Existing.md';other.write_text('existing report',encoding='utf-8')
        self.baseline=self.project/'before.json';self.baseline.write_text(json.dumps({other.name:hashlib.sha256(other.read_bytes()).hexdigest()}),encoding='utf-8')
        self.trace=self.project/'trace.json';self.data=dict(source_ids=['official'],figures=[],claim_review=[dict(claim='fixture',finding='local test only')],manual_review={x:'fixture check only' for x in ('coverage','versions_and_measurements','maturity_and_licenses','figures_opened')})
        self.save_trace()
    def save_trace(self):self.trace.write_text(json.dumps(self.data),encoding='utf-8')
    def verify(self):return cr.verify(self.project,self.report,self.trace,self.baseline)
    def tearDown(self):self.archive.network.close();self.temp.cleanup()
    def test_cited_scope_and_html_dependencies(self):
        result=self.verify();self.assertEqual(result['outcome'],'pass',result['errors'])
        self.assertEqual(result['html_visible_text_equal'],1)
        self.assertGreater(result['page_local_dependencies_checked'],0)
        self.assertEqual(result['sources'],1)
        count=self.archive.network.requests
        with contextlib.redirect_stdout(io.StringIO()):self.archive.collect('alias',self.record['url'])
        self.assertEqual(self.archive.network.requests,count)
    def test_tampered_asset_is_rejected(self):
        asset=self.record['assets'][0];path=self.project/'reference_metrial'/asset['local_file'];path.write_bytes(b'tampered')
        result=self.verify();self.assertEqual(result['outcome'],'fail')
        self.assertTrue(any('哈希' in e for e in result['errors']))
    def test_unknown_links_and_unrelated_changes(self):
        with self.report.open('a',encoding='utf-8') as out:out.write('\n[unknown](https://example.org/uncited)\n[missing](absent.md)\n')
        (self.project/'02_Existing.md').write_text('changed',encoding='utf-8')
        errors=self.verify()['errors']
        self.assertTrue(any('归档证据' in e for e in errors))
        self.assertTrue(any('本地报告链接' in e for e in errors))
        self.assertTrue(any('基线' in e for e in errors))
    def test_failed_source_and_table_are_rejected(self):
        self.data['source_ids'].append('failed_candidate');self.save_trace()
        self.report.write_text(self.report.read_text(encoding='utf-8').replace('|---|---|','|---|'),encoding='utf-8')
        errors=self.verify()['errors']
        self.assertTrue(any('正文未成功取得' in e for e in errors))
        self.assertTrue(any('表格' in e for e in errors))
    def test_false_figure_provenance_is_rejected(self):
        file=pathlib.Path(self.record['file'])
        self.data['figures']=[dict(file=file.as_posix(),sha256=self.record['sha256'],source_id='official',source_url='https://example.org/false-origin',original_file=file.as_posix(),original_sha256=self.record['sha256'],operation='false provenance fixture')]
        self.save_trace();self.assertTrue(any('未匹配' in e for e in self.verify()['errors']))

if __name__=='__main__':unittest.main()
