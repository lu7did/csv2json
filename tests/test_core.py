"""Tests for the core conversion service."""

from __future__ import annotations

import csv
import io
import json
import string
from pathlib import Path

import pytest
from hypothesis import given
from hypothesis import strategies as st
from hypothesis.strategies import DrawFn

from csv2json.core import CsvToJsonConverter
from csv2json.exceptions import ConversionRuntimeError, InputValidationError
from csv2json.models import ConversionOptions, ConversionRequest

SAFE_TEXT = string.ascii_letters + string.digits


def test_convert_text_returns_json_array() -> None:
    """It converts CSV text into a JSON array."""
    converter = CsvToJsonConverter()

    result = converter.convert_text("name,age\nAda,32\nGrace,45\n")

    assert json.loads(result) == [
        {"name": "Ada", "age": "32"},
        {"name": "Grace", "age": "45"},
    ]


def test_convert_text_supports_json_lines() -> None:
    """It can produce JSON Lines output."""
    converter = CsvToJsonConverter()
    options = ConversionOptions(json_lines=True)

    result = converter.convert_text("name,age\nAda,32\nGrace,45\n", options)

    assert result.splitlines() == [
        '{"name": "Ada", "age": "32"}',
        '{"name": "Grace", "age": "45"}',
    ]


def test_convert_text_rejects_invalid_delimiter() -> None:
    """It maps invalid options to a domain exception."""
    converter = CsvToJsonConverter()

    with pytest.raises(InputValidationError):
        converter.convert_text("name,age\nAda,32\n", ConversionOptions(delimiter="::"))


def test_convert_file_writes_output(tmp_path: Path) -> None:
    """It writes the converted JSON to the destination file."""
    source = tmp_path / "input.csv"
    destination = tmp_path / "nested" / "output.json"
    source.write_text("name,age\nAda,32\n", encoding="utf-8")
    converter = CsvToJsonConverter()

    result = converter.convert_file(
        ConversionRequest(
            source=source,
            destination=destination,
            options=ConversionOptions(indent=None),
        )
    )

    assert result == destination
    assert json.loads(destination.read_text(encoding="utf-8")) == [
        {"name": "Ada", "age": "32"}
    ]


def test_convert_file_raises_when_source_is_missing(tmp_path: Path) -> None:
    """It raises a domain exception if the source file is missing."""
    converter = CsvToJsonConverter()

    with pytest.raises(ConversionRuntimeError):
        converter.convert_file(
            ConversionRequest(
                source=tmp_path / "missing.csv",
                destination=tmp_path / "output.json",
                options=ConversionOptions(),
            )
        )


@st.composite
def csv_rows(draw: DrawFn) -> tuple[list[str], list[dict[str, str]]]:
    """Generate CSV-compatible rows with shared headers."""
    headers = draw(
        st.lists(
            st.text(alphabet=SAFE_TEXT, min_size=1, max_size=5),
            min_size=1,
            max_size=4,
            unique=True,
        )
    )
    value_strategy = st.text(alphabet=SAFE_TEXT, min_size=0, max_size=8)
    rows = draw(
        st.lists(
            st.fixed_dictionaries({header: value_strategy for header in headers}),
            min_size=1,
            max_size=5,
        )
    )
    return headers, rows


@given(csv_rows())
def test_convert_text_matches_expected_rows(
    data: tuple[list[str], list[dict[str, str]]],
) -> None:
    """It preserves header/value mappings for CSV-compatible inputs."""
    headers, rows = data
    converter = CsvToJsonConverter()
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=headers, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    csv_payload = buffer.getvalue()

    result = converter.convert_text(csv_payload, ConversionOptions(indent=None))

    assert json.loads(result) == rows
