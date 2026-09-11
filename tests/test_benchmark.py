import json
import tempfile
import unittest
from pathlib import Path

from triz_protocol.benchmark import compare_runs, score_context_funnel, score_suite
from triz_protocol.cli import main


ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "benchmarks" / "context-funnel-v1"
SUITE = ROOT / "benchmarks" / "suite-v1"


class BenchmarkTests(unittest.TestCase):
    def test_frozen_example_passes(self):
        score = score_context_funnel(CASE / "gold.json", CASE / "result.example.json")
        self.assertTrue(score["pass"])
        self.assertEqual(score["critical_file_recall"], 1.0)
        self.assertEqual(score["missing_critical_files"], [])

    def test_missing_dependency_fails(self):
        result = json.loads((CASE / "result.example.json").read_text(encoding="utf-8"))
        result["discovered_items"].remove("src/writer.py")
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

    def test_suite_scores_all_frozen_cases(self):
        score = score_suite(SUITE / "suite.json", SUITE / "results/protocol-demo")
        self.assertEqual(score["case_count"], 4)
        self.assertEqual(score["pass_rate"], 1.0)
        self.assertEqual(score["unsupported_claim_count"], 0)

    def test_compare_reports_directional_deltas(self):
        baseline = score_suite(SUITE / "suite.json", SUITE / "results/baseline-demo")
        protocol = score_suite(SUITE / "suite.json", SUITE / "results/protocol-demo")
        with tempfile.TemporaryDirectory() as directory:
            base_path = Path(directory) / "baseline.json"
            protocol_path = Path(directory) / "protocol.json"
            base_path.write_text(json.dumps(baseline), encoding="utf-8")
            protocol_path.write_text(json.dumps(protocol), encoding="utf-8")
            comparison = compare_runs(base_path, protocol_path)
        self.assertGreater(comparison["critical_item_recall_delta"], 0)
        self.assertLess(comparison["unsupported_claim_count_delta"], 0)

    def test_compare_rejects_different_model_settings(self):
        baseline = score_suite(SUITE / "suite.json", SUITE / "results/baseline-demo")
        protocol = score_suite(SUITE / "suite.json", SUITE / "results/protocol-demo")
        protocol["run"]["decoding"] = "different-settings"
        with tempfile.TemporaryDirectory() as directory:
            base_path = Path(directory) / "baseline.json"
            protocol_path = Path(directory) / "protocol.json"
            base_path.write_text(json.dumps(baseline), encoding="utf-8")
            protocol_path.write_text(json.dumps(protocol), encoding="utf-8")
            with self.assertRaises(ValueError):
                compare_runs(base_path, protocol_path)

    def test_suite_rejects_mismatched_case_id(self):
        result = json.loads((SUITE / "results/protocol-demo/source-conflict-v1.json").read_text(encoding="utf-8"))
        result["case_id"] = "wrong-case"
        with tempfile.TemporaryDirectory() as directory:
            results = Path(directory)
            for source in (SUITE / "results/protocol-demo").glob("*.json"):
                target = results / source.name
                target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
            (results / "source-conflict-v1.json").write_text(json.dumps(result), encoding="utf-8")
            with self.assertRaises(ValueError):
                score_suite(SUITE / "suite.json", results)


if __name__ == "__main__":
    unittest.main()
