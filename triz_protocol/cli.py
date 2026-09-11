from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .benchmark import score_context_funnel
from .core import load_json, render_markdown, template, validate


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
    return root


def main(argv: Sequence[str] | None = None) -> int:
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
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(path)
        return 0
    if args.command == "benchmark":
        score = score_context_funnel(args.gold, args.result)
        output = json.dumps(score, indent=2, ensure_ascii=False) + "\n"
        if args.output:
            Path(args.output).write_text(output, encoding="utf-8")
            print(args.output)
        else:
            print(output, end="")
        return 0 if score["pass"] else 1
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
        Path(args.output).write_text(output, encoding="utf-8")
        print(args.output)
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
