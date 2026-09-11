from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _load(path: str | Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object: {path}")
    return value


def score_case(gold_path: str | Path, result_path: str | Path) -> dict[str, Any]:
    gold = _load(gold_path)
    result = _load(result_path)
    if result.get("case_id") != gold.get("case_id"):
        raise ValueError("result case_id does not match gold case_id")
    if not gold.get("established_before_run"):
        raise ValueError("gold set must be established before the evaluated run")

    expected = set(gold.get("critical_items", gold.get("critical_files", [])))
    discovered = set(result.get("discovered_items", result.get("discovered_files", [])))
    required_invariants = set(gold.get("required_invariants", []))
    preserved_invariants = set(result.get("preserved_invariants", []))
    missing_invariants = required_invariants - preserved_invariants
    unsupported = list(result.get("unsupported_claims", []))
    violated = list(result.get("violated_invariants", []))

    if not expected:
        raise ValueError("gold set must contain critical_items or critical_files")
    true_positive = expected & discovered
    missing = expected - discovered
    extra = discovered - expected
    recall = len(true_positive) / len(expected) if expected else 1.0
    precision = len(true_positive) / len(discovered) if discovered else (1.0 if not expected else 0.0)
    return {
        "case_id": gold["case_id"],
        "critical_item_recall": recall,
        "critical_item_precision": precision,
        "missing_critical_items": sorted(missing),
        "extra_items": sorted(extra),
        "missing_required_invariants": sorted(missing_invariants),
        "unsupported_claim_count": len(unsupported),
        "violated_invariant_count": len(violated),
        "pass": not missing and not missing_invariants and not unsupported and not violated,
    }


def score_context_funnel(gold_path: str | Path, result_path: str | Path) -> dict[str, Any]:
    """Backward-compatible v0.2 scorer with the original field names."""
    score = score_case(gold_path, result_path)
    return {
        **score,
        "critical_file_recall": score["critical_item_recall"],
        "critical_file_precision": score["critical_item_precision"],
        "missing_critical_files": score["missing_critical_items"],
        "extra_files": score["extra_items"],
    }


def score_suite(suite_path: str | Path, results_path: str | Path) -> dict[str, Any]:
    suite = _load(suite_path)
    suite_file = Path(suite_path)
    result_dir = Path(results_path)
    run = _load(result_dir / "run.json")
    if run.get("suite_id") != suite.get("suite_id"):
        raise ValueError("run suite_id does not match benchmark suite")
    if run.get("condition") not in {"baseline", "protocol"}:
        raise ValueError("run condition must be baseline or protocol")
    for field in ("run_id", "paired_run_id", "model", "model_version", "decoding"):
        if not run.get(field):
            raise ValueError(f"run manifest requires {field}")
    case_scores = []
    for case in suite.get("cases", []):
        gold_path = suite_file.parent / case["gold"]
        result_path = result_dir / f"{case['id']}.json"
        case_scores.append(score_case(gold_path, result_path))
    if not case_scores:
        raise ValueError("suite must contain at least one case")
    count = len(case_scores)
    return {
        "suite_id": suite["suite_id"],
        "run": run,
        "case_count": count,
        "mean_critical_item_recall": sum(x["critical_item_recall"] for x in case_scores) / count,
        "mean_critical_item_precision": sum(x["critical_item_precision"] for x in case_scores) / count,
        "unsupported_claim_count": sum(x["unsupported_claim_count"] for x in case_scores),
        "violated_invariant_count": sum(x["violated_invariant_count"] for x in case_scores),
        "pass_rate": sum(1 for x in case_scores if x["pass"]) / count,
        "cases": case_scores,
    }


def compare_runs(baseline_path: str | Path, protocol_path: str | Path) -> dict[str, Any]:
    baseline = _load(baseline_path)
    protocol = _load(protocol_path)
    if baseline.get("suite_id") != protocol.get("suite_id"):
        raise ValueError("suite_id values do not match")
    if baseline.get("case_count") != protocol.get("case_count"):
        raise ValueError("case counts do not match")
    baseline_run = baseline.get("run", {})
    protocol_run = protocol.get("run", {})
    if baseline_run.get("condition") != "baseline" or protocol_run.get("condition") != "protocol":
        raise ValueError("comparison requires baseline then protocol conditions")
    if baseline_run.get("paired_run_id") != protocol_run.get("run_id") or protocol_run.get("paired_run_id") != baseline_run.get("run_id"):
        raise ValueError("runs do not identify each other as a pair")
    for field in ("model", "model_version", "decoding"):
        if baseline_run.get(field) != protocol_run.get(field):
            raise ValueError(f"paired runs differ in {field}")
    return {
        "suite_id": baseline["suite_id"],
        "case_count": baseline["case_count"],
        "baseline_run_id": baseline_run["run_id"],
        "protocol_run_id": protocol_run["run_id"],
        "simulation": bool(baseline_run.get("simulation") or protocol_run.get("simulation")),
        "critical_item_recall_delta": protocol["mean_critical_item_recall"] - baseline["mean_critical_item_recall"],
        "critical_item_precision_delta": protocol["mean_critical_item_precision"] - baseline["mean_critical_item_precision"],
        "unsupported_claim_count_delta": protocol["unsupported_claim_count"] - baseline["unsupported_claim_count"],
        "violated_invariant_count_delta": protocol["violated_invariant_count"] - baseline["violated_invariant_count"],
        "pass_rate_delta": protocol["pass_rate"] - baseline["pass_rate"],
        "interpretation": "Negative claim/invariant deltas are improvements; positive recall, precision, and pass-rate deltas are improvements.",
    }
