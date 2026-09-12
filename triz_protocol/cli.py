from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from .benchmark import compare_runs, score_context_funnel, score_suite
from .core import load_json, render_markdown, template, validate
from .experiment import prepare_experiment, verify_experiment
from .io import atomic_write_text


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="triz", description="TRIZ Agent Protocol tools")
    commands = root.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="create an empty analysis artifact")
    init.add_argument("path")
    init.add_argument("--mode", choices=("lite", "analysis", "ariz-guided"), default="lite")
    check = commands.add_parser("validate", help="validate an analysis artifact")
    check.add_argument("path")
    render = commands.add_parser("render", help="render an analysis artifact as Markdown")
    render.add_argument("path")
    render.add_argument("--output", "-o")
    render.add_argument("--language", "-l", choices=("en", "ru"), default="en")
    analyze = commands.add_parser("analyze", help="create a prefilled analysis draft")
    analyze.add_argument("path")
    analyze.add_argument("--problem", required=True)
    analyze.add_argument("--goal", default="")
    analyze.add_argument("--mode", choices=("lite", "analysis", "ariz-guided"), default="lite")
    benchmark = commands.add_parser("benchmark", help="score a context-funnel result against a frozen gold set")
    benchmark.add_argument("gold")
    benchmark.add_argument("result")
    benchmark.add_argument("--output", "-o")
    suite = commands.add_parser("benchmark-suite", help="score all results in a frozen benchmark suite")
    suite.add_argument("suite")
    suite.add_argument("results")
    suite.add_argument("--output", "-o")
    compare = commands.add_parser("compare", help="compare baseline and protocol suite scores")
    compare.add_argument("baseline")
    compare.add_argument("protocol")
    compare.add_argument("--output", "-o")
    prepare = commands.add_parser("prepare-experiment", help="create isolated baseline and protocol packets")
    prepare.add_argument("suite")
    prepare.add_argument("output")
    prepare.add_argument("--protocol-path", required=True)
    prepare.add_argument("--pair-id", required=True)
    prepare.add_argument("--model", required=True)
    prepare.add_argument("--model-version", required=True)
    prepare.add_argument("--decoding", required=True)
    verify = commands.add_parser("verify-experiment", help="verify experiment packet isolation and hashes")
    verify.add_argument("packet")
    return root


def _main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.command in {"init", "analyze"}:
        path = Path(args.path)
        if path.exists():
            print(f"refusing to overwrite existing file: {path}")
            return 2
        data = template(args.mode)
        if args.command == "analyze":
            data["problem"] = args.problem
            data["goal"] = args.goal
        atomic_write_text(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        print(path)
        return 0
    if args.command == "prepare-experiment":
        prepared = prepare_experiment(
            args.suite, args.output, args.protocol_path, pair_id=args.pair_id,
            model=args.model, model_version=args.model_version, decoding=args.decoding,
        )
        print(json.dumps(prepared, ensure_ascii=False))
        return 0
    if args.command == "verify-experiment":
        report = verify_experiment(args.packet)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["pass"] else 1
    if args.command in {"benchmark", "benchmark-suite", "compare"}:
        if args.command == "benchmark":
            score = score_context_funnel(args.gold, args.result)
        elif args.command == "benchmark-suite":
            score = score_suite(args.suite, args.results)
        else:
            score = compare_runs(args.baseline, args.protocol)
        output = json.dumps(score, indent=2, ensure_ascii=False) + "\n"
        if args.output:
            atomic_write_text(args.output, output)
            print(args.output)
        else:
            print(output, end="")
        if args.command == "benchmark":
            return 0 if score["pass"] else 1
        return 0
    data = load_json(args.path)
    errors = validate(data)
    if args.command == "validate":
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        print("VALID")
        return 0
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    output = render_markdown(data, language=args.language)
    if args.output:
        atomic_write_text(args.output, output)
        print(args.output)
    else:
        print(output)
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    try:
        return _main(argv)
    except (FileExistsError, FileNotFoundError, json.JSONDecodeError, KeyError, OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
