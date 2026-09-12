from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

from .io import atomic_write_text


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _files(path: Path):
    return sorted((item for item in path.rglob("*") if item.is_file()), key=lambda item: item.as_posix())


def _copy_material(source: Path, destination: Path) -> None:
    if source.name == "gold.json" or "results" in source.parts:
        raise ValueError(f"forbidden evaluation material: {source}")
    if source.is_dir():
        shutil.copytree(source, destination)
    elif source.is_file():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    else:
        raise FileNotFoundError(source)


def prepare_experiment(
    suite_path: str | Path,
    output_path: str | Path,
    protocol_path: str | Path,
    *,
    pair_id: str,
    model: str,
    model_version: str,
    decoding: str,
) -> dict[str, Any]:
    suite_file = Path(suite_path).resolve()
    output = Path(output_path).resolve()
    protocol = Path(protocol_path).resolve()
    if output.exists():
        raise FileExistsError(f"refusing to overwrite existing directory: {output}")
    suite = json.loads(suite_file.read_text(encoding="utf-8"))
    if not pair_id.strip():
        raise ValueError("pair_id must be non-empty")
    if not protocol.is_dir():
        raise FileNotFoundError(protocol)
    if output == protocol or output.is_relative_to(protocol):
        raise ValueError("output directory must not be inside the protocol directory")

    staging = output.with_name(f".{output.name}.staging")
    if staging.exists():
        raise FileExistsError(f"staging directory already exists: {staging}")
    try:
        for condition in ("baseline", "protocol"):
            condition_dir = staging / condition
            material_hashes: dict[str, str] = {}
            for case in suite.get("cases", []):
                if not case.get("materials"):
                    raise ValueError(f"suite case requires materials: {case.get('id', '<missing id>')}")
                case_dir = condition_dir / "cases" / case["id"]
                for material in case.get("materials", []):
                    source = (suite_file.parent / material).resolve()
                    destination = case_dir / Path(material).name
                    if destination.exists():
                        raise ValueError(f"duplicate material destination: {destination.name}")
                    _copy_material(source, destination)
                for item in _files(case_dir):
                    relative = item.relative_to(condition_dir).as_posix()
                    material_hashes[relative] = _sha256(item)

            protocol_hashes: dict[str, str] = {}
            if condition == "protocol":
                target = condition_dir / "protocol"
                shutil.copytree(protocol, target)
                for item in _files(target):
                    protocol_hashes[item.relative_to(condition_dir).as_posix()] = _sha256(item)

            run = {
                "run_id": f"{pair_id}-{condition}",
                "paired_run_id": f"{pair_id}-{'protocol' if condition == 'baseline' else 'baseline'}",
                "suite_id": suite["suite_id"],
                "condition": condition,
                "model": model,
                "model_version": model_version,
                "decoding": decoding,
                "context_policy": "case materials only" if condition == "baseline" else "case materials plus frozen protocol",
                "simulation": False,
                "suite_sha256": _sha256(suite_file),
                "material_sha256": material_hashes,
                "protocol_sha256": protocol_hashes,
            }
            atomic_write_text(condition_dir / "run.json", json.dumps(run, ensure_ascii=False, indent=2) + "\n")
        shutil.move(staging, output)
    except BaseException:
        if staging.exists():
            shutil.rmtree(staging)
        raise
    return {"output": str(output), "pair_id": pair_id, "conditions": ["baseline", "protocol"]}
