"""Core conversion services."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Final

from csv2json.exceptions import ConversionRuntimeError, InputValidationError
from csv2json.models import ConversionOptions, ConversionRequest

DEFAULT_NEWLINE: Final[str] = ""


class CsvToJsonConverter:
    """Convert CSV content into JSON representations."""

    def convert_text(
        self,
        csv_text: str,
        options: ConversionOptions | None = None,
    ) -> str:
        """Convert CSV text content into a JSON string."""
        selected_options = options or ConversionOptions()
        self._validate_options(selected_options)

        try:
            reader = csv.DictReader(
                csv_text.splitlines(),
                delimiter=selected_options.delimiter,
            )
            rows = list(reader)
        except csv.Error as error:
            msg = "Unable to parse CSV text."
            raise ConversionRuntimeError(msg) from error

        return self._serialize_rows(rows, selected_options)

    def convert_file(self, request: ConversionRequest) -> Path:
        """Convert a CSV file into a JSON file and return the destination path."""
        self._validate_options(request.options)

        try:
            with request.source.open(
                "r",
                encoding=request.options.input_encoding,
                newline=DEFAULT_NEWLINE,
            ) as source_file:
                reader = csv.DictReader(
                    source_file,
                    delimiter=request.options.delimiter,
                )
                rows = list(reader)
        except FileNotFoundError as error:
            msg = f"Source file not found: {request.source}"
            raise ConversionRuntimeError(msg) from error
        except OSError as error:
            msg = f"Unable to read source file: {request.source}"
            raise ConversionRuntimeError(msg) from error
        except csv.Error as error:
            msg = f"Unable to parse source CSV file: {request.source}"
            raise ConversionRuntimeError(msg) from error

        payload = self._serialize_rows(rows, request.options)

        try:
            request.destination.parent.mkdir(parents=True, exist_ok=True)
            request.destination.write_text(
                payload,
                encoding=request.options.output_encoding,
            )
        except OSError as error:
            msg = f"Unable to write destination file: {request.destination}"
            raise ConversionRuntimeError(msg) from error

        return request.destination

    def _serialize_rows(
        self,
        rows: list[dict[str, str | None]],
        options: ConversionOptions,
    ) -> str:
        """Serialize parsed CSV rows according to the selected JSON mode."""
        if options.json_lines:
            return "\n".join(
                json.dumps(
                    row,
                    ensure_ascii=options.ensure_ascii,
                    sort_keys=options.sort_keys,
                )
                for row in rows
            )

        return json.dumps(
            rows,
            indent=options.indent,
            ensure_ascii=options.ensure_ascii,
            sort_keys=options.sort_keys,
        )

    def _validate_options(self, options: ConversionOptions) -> None:
        """Validate user-selected options and map errors to domain exceptions."""
        try:
            options.validate()
        except ValueError as error:
            raise InputValidationError(str(error)) from error
