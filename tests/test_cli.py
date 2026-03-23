"""Tests for the command line interface."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from csv2json.cli import main


def test_main_generates_json_file(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The CLI converts the source file and reports success."""
    source = tmp_path / "input.csv"
    destination = tmp_path / "output.json"
    source.write_text("name,age\nAda,32\n", encoding="utf-8")

    result = main([str(source), "--output", str(destination)])

    assert result == 0
    assert json.loads(destination.read_text(encoding="utf-8")) == [
        {"name": "Ada", "age": "32"}
    ]
    assert "Generated" in capsys.readouterr().out


def test_main_returns_error_for_missing_source(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The CLI exits with a non-zero code for missing input files."""
    source = tmp_path / "missing.csv"
    destination = tmp_path / "output.json"

    result = main([str(source), "--output", str(destination)])

    assert result == 1
    assert "error" in capsys.readouterr().err.lower()
