from pathlib import Path

import pytest

from validate_report import load_report, main, validate

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures"


def test_valid_json_has_no_errors():
    data = load_report(FIXTURES / "valid.json")
    assert validate(data) == []


def test_valid_yaml_has_no_errors():
    data = load_report(FIXTURES / "valid.yaml")
    assert validate(data) == []


def test_invalid_json_collects_errors():
    data = load_report(FIXTURES / "invalid.json")
    errors = validate(data)
    joined = "\n".join(errors)
    assert "week must look like" in joined
    assert "author must be a non-empty string" in joined
    assert "title must be a non-empty string" in joined
    assert "status must be one of" in joined
    assert "must be an object" in joined


def test_missing_top_level_fields():
    errors = validate({"items": [{"title": "x", "status": "done"}]})
    assert "missing field: week" in errors
    assert "missing field: author" in errors


def test_cli_ok_on_valid(capsys):
    assert main([str(FIXTURES / "valid.json")]) == 0
    assert "ok:" in capsys.readouterr().out


def test_cli_nonzero_on_invalid():
    assert main([str(FIXTURES / "invalid.json")]) == 1


def test_cli_usage_without_args():
    assert main([]) == 2
