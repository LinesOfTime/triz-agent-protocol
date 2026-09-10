from __future__ import annotations

import json
from pathlib import Path
from typing import Any

MODES = {"lite", "analysis", "ariz-guided"}
CLAIM_KINDS = {"evidence", "inference", "assumption", "simulation"}
CONTRADICTION_TYPES = {"administrative", "technical", "physical"}


def template(mode: str) -> dict[str, Any]:
    if mode not in MODES:
        raise ValueError(f"unknown mode: {mode}")
    return {
        "protocol_version": "0.1", "mode": mode, "problem": "", "goal": "", "ifr": "",
        "invariants": [], "claims": [], "functions": [], "causes": [],
        "contradictions": [], "resources": [], "solutions": [], "verification": [],
        "recommended_next_step": None, "open_questions": []
    }


def load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("analysis root must be a JSON object")
    return value


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("protocol_version") != "0.1":
        errors.append("protocol_version must equal '0.1'")
    mode = data.get("mode")
    if mode not in MODES:
        errors.append(f"mode must be one of {sorted(MODES)}")
    for field in ("problem", "goal", "ifr"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            errors.append(f"{field} must be a non-empty string")

    claims = data.get("claims")
    if not isinstance(claims, list) or not claims:
        errors.append("claims must contain at least one item")
    else:
        seen: set[str] = set()
        for index, claim in enumerate(claims):
            if not isinstance(claim, dict):
                errors.append(f"claims[{index}] must be an object")
                continue
            claim_id = claim.get("id")
            if not isinstance(claim_id, str) or not claim_id.strip():
                errors.append(f"claims[{index}].id must be non-empty")
            elif claim_id in seen:
                errors.append(f"duplicate claim id: {claim_id}")
            else:
                seen.add(claim_id)
            if claim.get("kind") not in CLAIM_KINDS:
                errors.append(f"claims[{index}].kind is invalid")
            if not isinstance(claim.get("statement"), str) or not claim["statement"].strip():
                errors.append(f"claims[{index}].statement must be non-empty")
            if claim.get("kind") == "evidence" and not claim.get("source"):
                errors.append(f"claims[{index}] is evidence but has no source")

    contradictions = data.get("contradictions")
    if not isinstance(contradictions, list) or not contradictions:
        errors.append("contradictions must contain at least one item")
    else:
        for index, item in enumerate(contradictions):
            if not isinstance(item, dict):
                errors.append(f"contradictions[{index}] must be an object")
                continue
            if item.get("type") not in CONTRADICTION_TYPES:
                errors.append(f"contradictions[{index}].type is invalid")
            for field in ("element", "requirement_a", "requirement_b"):
                if not isinstance(item.get(field), str) or not item[field].strip():
                    errors.append(f"contradictions[{index}].{field} must be non-empty")
            if item.get("type") == "physical" and mode == "ariz-guided":
                if not item.get("operational_zone") or not item.get("operational_time"):
                    errors.append(f"contradictions[{index}] physical contradiction requires operational zone and time in ariz-guided mode")

    for field in ("resources", "verification"):
        value = data.get(field)
        if not isinstance(value, list) or not any(isinstance(x, str) and x.strip() for x in value):
            errors.append(f"{field} must contain at least one non-empty string")

    solutions = data.get("solutions")
    if not isinstance(solutions, list) or len(solutions) < 2:
        errors.append("solutions must contain at least two distinct concepts")
    else:
        mechanisms: set[str] = set()
        for index, solution in enumerate(solutions):
            if not isinstance(solution, dict):
                errors.append(f"solutions[{index}] must be an object")
                continue
            for field in ("id", "concept", "mechanism"):
                if not isinstance(solution.get(field), str) or not solution[field].strip():
                    errors.append(f"solutions[{index}].{field} must be non-empty")
            mechanism = str(solution.get("mechanism", "")).strip().casefold()
            if mechanism and mechanism in mechanisms:
                errors.append(f"solutions[{index}] duplicates an earlier mechanism")
            mechanisms.add(mechanism)
            if not isinstance(solution.get("risks"), list):
                errors.append(f"solutions[{index}].risks must be a list")

    if mode in {"analysis", "ariz-guided"}:
        if not data.get("functions"):
            errors.append(f"functions are required in {mode} mode")
        if not data.get("causes"):
            errors.append(f"causes are required in {mode} mode")
    return errors


def render_markdown(data: dict[str, Any]) -> str:
    def bullets(values: list[Any]) -> str:
        return "\n".join(f"- {value}" for value in values) or "- None recorded"

    claims = [f"- **{c.get('id', '?')} — {c.get('kind', '?')}:** {c.get('statement', '')}" +
              (f" _(source: {c['source']})_" if c.get("source") else "")
              for c in data.get("claims", []) if isinstance(c, dict)]
    contradictions = [f"- **{c.get('type', '?')} — {c.get('element', '?')}:** "
                      f"{c.get('requirement_a', '')} ↔ {c.get('requirement_b', '')}"
                      for c in data.get("contradictions", []) if isinstance(c, dict)]
    solutions = [f"### {s.get('id', '?')}: {s.get('concept', '')}\n\n{s.get('mechanism', '')}"
                 f"\n\nRisks:\n{bullets(s.get('risks', []))}"
                 for s in data.get("solutions", []) if isinstance(s, dict)]
    return f"""# TRIZ analysis

**Protocol:** {data.get('protocol_version', '?')}
**Mode:** {data.get('mode', '?')}

## Problem

{data.get('problem', '')}

## Goal

{data.get('goal', '')}

## Ideal Final Result

{data.get('ifr', '')}

## Invariants

{bullets(data.get('invariants', []))}

## Claims

{chr(10).join(claims) or '- None recorded'}

## Contradictions

{chr(10).join(contradictions) or '- None recorded'}

## Resources

{bullets(data.get('resources', []))}

## Solution concepts

{chr(10).join(solutions) or 'None recorded'}

## Verification

{bullets(data.get('verification', []))}

## Recommended next step

{data.get('recommended_next_step') or 'Not selected'}

## Open questions

{bullets(data.get('open_questions', []))}
"""
