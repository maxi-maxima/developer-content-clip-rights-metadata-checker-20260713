import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "developer_content_clip_rights_metadata_checker.py"


class SmokeTest(unittest.TestCase):
    def test_help(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--help"], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("usage:", result.stdout)

    def test_example_runs(self):
        examples = list((ROOT / "examples").iterdir())
        result = subprocess.run([sys.executable, str(SCRIPT), *(str(path) for path in examples)], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertTrue(result.stdout.strip())

    def test_directory_summary_json(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(ROOT / "examples"), "--json", "--summary"],
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["summary"]["checked"], 1)
        self.assertEqual(payload["summary"]["failed"], 0)

    def test_csv_and_warning_exit(self):
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = pathlib.Path(tmp) / "clip.csv"
            csv_path.write_text(
                "source_url,license,creator,consent,ai_generated_disclosure\n"
                "ftp://example.invalid/demo,unknown,DevRel,no,none\n",
                encoding="utf-8",
            )
            result = subprocess.run([sys.executable, str(SCRIPT), str(csv_path), "--json"], text=True, capture_output=True)
        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertEqual(payload[0]["status"], "FAIL")
        self.assertIn("source_url is not http(s)", payload[0]["warnings"])
        self.assertIn("license is not in known allow-list", payload[0]["warnings"])


if __name__ == "__main__":
    unittest.main()
