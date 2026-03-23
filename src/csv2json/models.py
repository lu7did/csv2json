"""Data structures used by the converter."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True, frozen=True)
class ConversionOptions:
    """Immutable options for CSV-to-JSON conversion."""

    delimiter: str = ","
    indent: int | None = 2
    ensure_ascii: bool = False
    sort_keys: bool = False
    json_lines: bool = False
    input_encoding: str = "utf-8"
    output_encoding: str = "utf-8"

    def validate(self) -> None:
        """Validate the conversion options."""
        if len(self.delimiter) != 1:
            msg = "The delimiter must be a single character."
            raise ValueError(msg)

        if self.indent is not None and self.indent < 0:
            msg = "Indent must be None or greater than or equal to zero."
            raise ValueError(msg)


@dataclass(slots=True, frozen=True)
class ConversionRequest:
    """Represent a file-based conversion request."""

    source: Path
    destination: Path
    options: ConversionOptions
