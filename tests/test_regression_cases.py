import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RegressionCaseTests(unittest.TestCase):
    def load_case(self, name):
        path = ROOT / "benchmarks" / "regressions" / name
        return json.loads(path.read_text(encoding="utf-8"))

    def test_intentional_working_copy_drift_is_not_corruption(self):
        expected = self.load_case("artifact-lifecycle.json")["expected"]
        self.assertEqual(expected["hash_mismatch_proves"], "byte_level_difference")
        self.assertFalse(expected["infer_corruption"])
        self.assertFalse(expected["recommend_restore_without_authorization"])

    def test_self_reconstructed_denominator_is_not_independent_recall(self):
        expected = self.load_case("recall-denominator.json")["expected"]
        self.assertIn("reconstructed known set", expected["allowed_claim"])
        self.assertFalse(expected["independent_recall_established"])
        self.assertFalse(expected["absolute_completeness_established"])


if __name__ == "__main__":
    unittest.main()
