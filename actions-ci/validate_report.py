"""Validate a weekly-report JSON or YAML fixture. Exit 1 if invalid.

Usage:
    python validate_report.py path/to/report.json
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ALLOWED_STATUS = {"done", "wip", "blocked", "planned"}
WEEK_RE = re.compile(r"^\d{4}-W\d{2}$")
REQUIRED_TOP = ("week", "author", "items")
REQUIRED_ITEM = ("title", "status")


def load_report(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    suffix = path.suffix.lower()
    if suffix in {".yaml", ".yml"}:
        return yaml.safe_load(text)
    if suffix == ".json":
        return json.loads(text)
    raise ValueError(f"unsupported file type: {path.suffix} (use .json / .yaml / .yml)")


def validate(data: Any) -> list[str]:
    """Return a list of error strings. Empty means valid."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["report must be an object/mapping"]

    for key in REQUIRED_TOP:
        if key not in data:
            errors.append(f"missing field: {key}")

    week = data.get("week")
    if week is not None and not (isinstance(week, str) and WEEK_RE.match(week)):
        errors.append("week must look like YYYY-Www, e.g. 2026-W34")

    author = data.get("author")
    if author is not None and not (isinstance(author, str) and author.strip()):
        errors.append("author must be a non-empty string")

    items = data.get("items")
    if items is None:
        return errors
    if not isinstance(items, list):
        errors.append("items must be a list")
        return errors
    if not items:
        errors.append("items must not be empty")

    for i, item in enumerate(items):
        prefix = f"items[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for key in REQUIRED_ITEM:
            if key not in item:
                errors.append(f"{prefix} missing field: {key}")
        title = item.get("title")
        if title is not None and not (isinstance(title, str) and title.strip()):
            errors.append(f"{prefix}.title must be a non-empty string")
        status = item.get("status")
        if status is not None and status not in ALLOWED_STATUS:
            allowed = ", ".join(sorted(ALLOWED_STATUS))
            errors.append(f"{prefix}.status must be one of: {allowed}")
        hours = item.get("hours")
        if hours is not None and not isinstance(hours, (int, float)):
            errors.append(f"{prefix}.hours must be a number if present")
    return errors


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("usage: python validate_report.py <report.json|yaml>", file=sys.stderr)
        return 2
    path = Path(args[0])
    if not path.is_file():
        print(f"file not found: {path}", file=sys.stderr)
        return 2
    try:
        data = load_report(path)
    except (json.JSONDecodeError, yaml.YAMLError, ValueError) as exc:
        print(f"parse error: {exc}", file=sys.stderr)
        return 1
    errors = validate(data)
    if errors:
        print("invalid weekly report:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1
    print(f"ok: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
