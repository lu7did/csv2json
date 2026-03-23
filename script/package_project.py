"""Create a zip archive with the repository contents for GitHub upload."""

from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "dist" / "csv2json-github-upload.zip"
EXCLUDED_PREFIXES = {".git", ".venv", "dist", "__pycache__"}


def should_include(path: Path) -> bool:
    """Return True when the path should be packaged."""
    relative_parts = path.relative_to(ROOT).parts
    return not any(part in EXCLUDED_PREFIXES for part in relative_parts)


def create_archive() -> Path:
    """Create the project archive and return its path."""
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with ZipFile(OUTPUT, "w", compression=ZIP_DEFLATED) as archive:
        for path in sorted(ROOT.rglob("*")):
            if path.is_dir() or not should_include(path):
                continue
            archive.write(path, path.relative_to(ROOT))

    return OUTPUT


if __name__ == "__main__":
    print(create_archive())
