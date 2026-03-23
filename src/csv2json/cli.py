"""Command line interface for csv2json."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from csv2json.core import CsvToJsonConverter
from csv2json.exceptions import Csv2JsonError
from csv2json.models import ConversionOptions, ConversionRequest
from csv2json.version import VERSION


def build_parser() -> argparse.ArgumentParser:
    """Build and return the CLI argument parser."""
    parser = argparse.ArgumentParser(description="Convert CSV files to JSON.")
    parser.add_argument("source", type=Path, help="Path to the source CSV file.")
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Path to the destination JSON file.",
    )
    parser.add_argument(
        "--delimiter",
        default=",",
        help="Single-character CSV delimiter.",
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="JSON indent level. Use 0 or more.",
    )
    parser.add_argument(
        "--ensure-ascii",
        action="store_true",
        help="Escape non-ASCII characters in the JSON output.",
    )
    parser.add_argument(
        "--sort-keys",
        action="store_true",
        help="Sort JSON object keys alphabetically.",
    )
    parser.add_argument(
        "--json-lines",
        action="store_true",
        help="Emit one JSON object per line instead of a JSON array.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return a process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    options = ConversionOptions(
        delimiter=args.delimiter,
        indent=args.indent,
        ensure_ascii=args.ensure_ascii,
        sort_keys=args.sort_keys,
        json_lines=args.json_lines,
    )

    try:
        request = ConversionRequest(
            source=args.source,
            destination=args.output,
            options=options,
        )
        converter = CsvToJsonConverter()
        output_path = converter.convert_file(request)
    except Csv2JsonError as error:
        sys.stderr.write(f"csv2json: error: {error}\n")
        return 1

    sys.stdout.write(f"Generated {output_path}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
