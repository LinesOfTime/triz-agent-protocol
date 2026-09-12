from __future__ import annotations

import re
import sys
from pathlib import Path


LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    failures: list[str] = []
    for document in sorted(root.rglob("*.md")):
        if any(part in {".git", ".venv"} for part in document.parts):
            continue
        for raw in LINK.findall(document.read_text(encoding="utf-8")):
            target = raw.split(maxsplit=1)[0].split("#", 1)[0]
            if not target or "://" in target or target.startswith(("mailto:", "#")):
                continue
            if not (document.parent / target).resolve().exists():
                failures.append(f"{document.relative_to(root)}: {raw}")
    if failures:
        print("Broken relative Markdown links:", file=sys.stderr)
        print("\n".join(failures), file=sys.stderr)
        return 1
    print("Markdown links: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
