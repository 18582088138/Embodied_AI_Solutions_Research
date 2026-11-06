"""Verify portable deployment, idempotency, conflict handling and path bounds."""
import pathlib,subprocess,sys,tempfile,unittest

class BootstrapTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='embodied-skill-deploy-')
        self.base=pathlib.Path(self.temp.name);self.root=self.base/'research'
        self.script=pathlib.Path(__file__).with_name('bootstrap_research.py')
    def tearDown(self):self.temp.cleanup()
    def run_bootstrap(self,project='01_Compute_Chips/02_Fixture'):
        return subprocess.run([sys.executable,str(self.script),'--root',str(self.root),'--project',project],capture_output=True,text=True,encoding='utf-8')
    def test_deploy_and_repeat_preserve_tools(self):
        first=self.run_bootstrap();self.assertEqual(first.returncode,0,first.stderr)
        target=self.root/'toolkit/download_materials.py';original=target.read_bytes()
        second=self.run_bootstrap();self.assertEqual(second.returncode,0,second.stderr)
        self.assertEqual(target.read_bytes(),original)
        self.assertTrue((self.root/'01_Compute_Chips/02_Fixture/research_state/evidence').is_dir())
        self.assertFalse(list((self.root/'01_Compute_Chips/02_Fixture').glob('*.md')))
    def test_conflict_does_not_overwrite(self):
        folder=self.root/'toolkit';folder.mkdir(parents=True)
        target=folder/'download_materials.py';target.write_bytes(b'existing version')
        result=self.run_bootstrap();self.assertNotEqual(result.returncode,0)
        self.assertEqual(target.read_bytes(),b'existing version')
        self.assertFalse((folder/'check_report.py').exists())
    def test_path_escape_does_not_create_project(self):
        result=self.run_bootstrap('../outside')
        self.assertNotEqual(result.returncode,0)
        self.assertFalse((self.base/'outside').exists())

if __name__=='__main__':unittest.main()
