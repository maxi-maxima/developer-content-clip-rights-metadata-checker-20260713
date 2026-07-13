import importlib.util, pathlib, unittest, subprocess, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'developer_content_clip_rights_metadata_checker.py'

class SmokeTest(unittest.TestCase):
    def test_help(self):
        r=subprocess.run([sys.executable,str(SCRIPT),'--help'],text=True,capture_output=True)
        self.assertEqual(r.returncode,0)
        self.assertIn('usage:',r.stdout)
    def test_example_runs(self):
        examples=list((ROOT/'examples').iterdir())
        r=subprocess.run([sys.executable,str(SCRIPT),*(str(x) for x in examples)],text=True,capture_output=True)
        self.assertIn(r.returncode,(0,1))
        self.assertTrue(r.stdout.strip())

if __name__=='__main__': unittest.main()
