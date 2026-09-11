import json
import tempfile
import unittest
from pathlib import Path

from triz_protocol.cli import main
from triz_protocol.core import render_markdown, template, validate


def valid_artifact(mode="lite"):
    data = template(mode)
    data.update(
        problem="Observed problem", goal="Observable goal", ifr="Desired result without added harm",
        claims=[{"id": "E1", "kind": "evidence", "statement": "Observed", "source": "test.log"}],
        contradictions=[{"type": "technical", "element": "context", "requirement_a": "must be broad", "requirement_b": "must be narrow", "operational_zone": None, "operational_time": None}],
        resources=["existing index"],
        solutions=[
            {"id": "S1", "concept": "Route", "mechanism": "Use conditional routing", "risks": []},
            {"id": "S2", "concept": "Rerank", "mechanism": "Use a separate reranker", "risks": ["latency"]}
        ],
        verification=["Run frozen evaluation set"]
    )
    if mode in {"analysis", "ariz-guided"}:
        data["functions"] = [{"source": "a", "target": "b", "action": "changes", "class": "useful"}]
        data["causes"] = [{"id": "C1", "claim": "Cause", "kind": "inference"}]
    return data


class ValidationTests(unittest.TestCase):
    def test_valid_lite(self):
        self.assertEqual(validate(valid_artifact()), [])

    def test_evidence_requires_source(self):
        data = valid_artifact()
        data["claims"][0]["source"] = None
        self.assertIn("claims[0] is evidence but has no source", validate(data))

    def test_analysis_requires_functions_and_causes(self):
        data = valid_artifact("analysis")
        data["functions"] = []
        data["causes"] = []
        errors = validate(data)
        self.assertIn("functions are required in analysis mode", errors)
        self.assertIn("causes are required in analysis mode", errors)

    def test_duplicate_mechanisms_are_rejected(self):
        data = valid_artifact()
        data["solutions"][1]["mechanism"] = data["solutions"][0]["mechanism"].upper()
        self.assertTrue(any("duplicates" in error for error in validate(data)))

    def test_renderer_contains_key_sections(self):
        rendered = render_markdown(valid_artifact())
        self.assertIn("## Ideal Final Result", rendered)
        self.assertIn("Use conditional routing", rendered)

    def test_russian_renderer_contains_localized_sections(self):
        rendered = render_markdown(valid_artifact(), language="ru")
        self.assertIn("## Идеальный конечный результат", rendered)
        self.assertIn("## Механизмы решения", rendered)
        self.assertIn("источник: test.log", rendered)

    def test_cli_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "analysis.json"
            self.assertEqual(main(["init", str(path)]), 0)
            self.assertEqual(main(["init", str(path)]), 2)

    def test_analyze_prefills_problem_and_goal(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "analysis.json"
            self.assertEqual(main([
                "analyze", str(path), "--problem", "Context is noisy",
                "--goal", "Reduce noise", "--mode", "lite"
            ]), 0)
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(data["problem"], "Context is noisy")
            self.assertEqual(data["goal"], "Reduce noise")


if __name__ == "__main__":
    unittest.main()
