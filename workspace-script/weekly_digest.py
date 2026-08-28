"""Build a weekly digest from a CSV that stands in for a Google Sheet.

Columns: date, owner, task, status, due
Open statuses: open, wip, blocked. Grouped by owner.
No Google API calls.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

OPEN_STATUSES = {"open", "wip", "blocked"}
COLUMNS = ("date", "owner", "task", "status", "due")


@dataclass(frozen=True)
class Task:
    date: str
    owner: str
    task: str
    status: str
    due: str

    @property
    def is_open(self) -> bool:
        return self.status.strip().lower() in OPEN_STATUSES


def load_tasks(path: Path) -> list[Task]:
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise ValueError("CSV has no header row")
        missing = [c for c in COLUMNS if c not in reader.fieldnames]
        if missing:
            raise ValueError(f"CSV missing columns: {', '.join(missing)}")
        tasks: list[Task] = []
        for row in reader:
            tasks.append(
                Task(
                    date=row["date"].strip(),
                    owner=row["owner"].strip(),
                    task=row["task"].strip(),
                    status=row["status"].strip().lower(),
                    due=row["due"].strip(),
                )
            )
        return tasks


def group_open_by_owner(tasks: list[Task]) -> dict[str, list[Task]]:
    grouped: dict[str, list[Task]] = defaultdict(list)
    for t in tasks:
        if t.is_open:
            grouped[t.owner].append(t)
    return dict(sorted(grouped.items(), key=lambda kv: kv[0]))


def render_markdown(grouped: dict[str, list[Task]], title: str = "本周未完成") -> str:
    if not grouped:
        return f"# {title}\n\n（没有未完成任务）\n"
    lines = [f"# {title}", ""]
    for owner, items in grouped.items():
        lines.append(f"## {owner}")
        lines.append("")
        for t in items:
            due = f"，截止 {t.due}" if t.due else ""
            lines.append(f"- [{t.status}] {t.task}{due}")
        lines.append("")
    return "\n".join(lines)


def render_text(grouped: dict[str, list[Task]], title: str = "本周未完成") -> str:
    if not grouped:
        return f"{title}\n\n（没有未完成任务）\n"
    blocks = [title, ""]
    for owner, items in grouped.items():
        blocks.append(f"{owner}:")
        for t in items:
            due = f", due {t.due}" if t.due else ""
            blocks.append(f"  - [{t.status}] {t.task}{due}")
        blocks.append("")
    return "\n".join(blocks)


def digest(path: Path, fmt: str = "markdown") -> str:
    grouped = group_open_by_owner(load_tasks(path))
    if fmt == "text":
        return render_text(grouped)
    if fmt == "markdown":
        return render_markdown(grouped)
    raise ValueError(f"unknown format: {fmt}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Sheets-like CSV to weekly digest")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--format", choices=("markdown", "text"), default="markdown")
    args = parser.parse_args(argv)
    print(digest(args.csv_path, fmt=args.format), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
