from pathlib import Path

from weekly_digest import (
    Task,
    digest,
    group_open_by_owner,
    load_tasks,
    render_markdown,
    render_text,
)

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "fixtures" / "tasks.csv"


def test_load_fixture_columns():
    tasks = load_tasks(CSV)
    assert len(tasks) == 6
    assert {t.owner for t in tasks} == {"李明", "王芳", "陈涛"}


def test_open_tasks_grouped_by_owner():
    grouped = group_open_by_owner(load_tasks(CSV))
    assert set(grouped) == {"李明", "王芳", "陈涛"}
    assert [t.task for t in grouped["李明"]] == ["补一周报 YAML 样例"]
    assert {t.status for t in grouped["王芳"]} == {"wip", "blocked"}
    assert all(t.status != "done" for items in grouped.values() for t in items)


def test_markdown_digest_lists_owners():
    md = digest(CSV, fmt="markdown")
    assert md.startswith("# 本周未完成")
    assert "## 李明" in md
    assert "## 王芳" in md
    assert "## 陈涛" in md
    assert "已关闭的旧 ticket" not in md


def test_text_digest():
    text = digest(CSV, fmt="text")
    assert "李明:" in text
    assert "[open] 补一周报 YAML 样例, due 2026-08-29" in text


def test_empty_open_list():
    grouped = group_open_by_owner(
        [Task("2026-08-01", "zc", "shipped", "done", "2026-08-01")]
    )
    assert grouped == {}
    assert "没有未完成任务" in render_markdown(grouped)
    assert "没有未完成任务" in render_text(grouped)
