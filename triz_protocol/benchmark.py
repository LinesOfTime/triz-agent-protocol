from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def score_context_funnel(gold_path: str | Path, result_path: str | Path) -> dict[str, Any]:
    gold = json.loads(Path(gold_path).read_text(encoding="utf-8"))
    result = json.loads(Path(result_path).read_text(encoding="utf-8"))
    expected = set(gold["critical_files"])
    discovered = set(result["discovered_files"])
    true_positive = expected & discovered
    missing = expected - discovered
    extra = discovered - expected
    recall = len(true_positive) / len(expected) if expected else 1.0
    precision = len(true_positive) / len(discovered) if discovered else (1.0 if not expected else 0.0)
    return {
        "case_id": gold["case_id"],
        "critical_file_recall": recall,
        "critical_file_precision": precision,
        "missing_critical_files": sorted(missing),
        "extra_files": sorted(extra),
        "unsupported_claim_count": len(result.get("unsupported_claims", [])),
        "pass": not missing and not result.get("unsupported_claims", []),
    }
