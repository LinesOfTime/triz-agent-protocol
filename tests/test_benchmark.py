import json
import tempfile
import unittest
from pathlib import Path

from triz_protocol.benchmark import score_context_funnel
from triz_protocol.cli import main


ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "benchmarks" / "context-funnel-v1"


class BenchmarkTests(unittest.TestCase):
    def test_frozen_example_passes(self):
        score = score_context_funnel(CASE / "gold.json", CASE / "result.example.json")
        self.assertTrue(score["pass"])
        self.assertEqual(score["critical_file_recall"], 1.0)
        self.assertEqual(score["missing_critical_files"], [])

    def test_missing_dependency_fails(self):
        result = json.loads((CASE / "result.example.json").read_text(encoding="utf-8"))
        result["discovered_files"].remove("src/writer.py")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "result.json"
            path.write_text(json.dumps(result), encoding="utf-8")
            score = score_context_funnel(CASE / "gold.json", path)
        self.assertFalse(score["pass"])
        self.assertEqual(score["missing_critical_files"], ["src/writer.py"])

    def test_cli_returns_failure_for_unsupported_claim(self):
        result = json.loads((CASE / "result.example.json").read_text(encoding="utf-8"))
        result["unsupported_claims"] = ["The old format is unused"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "result.json"
            path.write_text(json.dumps(result), encoding="utf-8")
            self.assertEqual(main(["benchmark", str(CASE / "gold.json"), str(path)]), 1)


if __name__ == "__main__":
    unittest.main()
