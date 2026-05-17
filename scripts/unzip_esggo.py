#!/usr/bin/env python3
"""Extract the ESGGO archive into a local folder."""

from __future__ import annotations

import argparse
from pathlib import Path
import zipfile


DEFAULT_ZIP = Path("ESGGO_Orignal-v25.25.249 (1).zip")
DEFAULT_OUTPUT = Path("extracted")


def _is_safe_path(base: Path, target: Path) -> bool:
    try:
        target.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False


def extract(zip_path: Path, output_dir: Path) -> None:
    if not zip_path.exists():
        raise FileNotFoundError(f"Archive not found: {zip_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as archive:
        for info in archive.infolist():
            destination = output_dir / info.filename
            if not _is_safe_path(output_dir, destination):
                raise ValueError(f"Unsafe path in archive: {info.filename}")
        archive.extractall(output_dir)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Unzip ESGGO_Orignal-v25.25.249 (1).zip into a target directory."
    )
    parser.add_argument("--zip", type=Path, default=DEFAULT_ZIP, help="Path to archive")
    parser.add_argument(
        "--out", type=Path, default=DEFAULT_OUTPUT, help="Output directory"
    )
    args = parser.parse_args()

    extract(args.zip, args.out)
    print(f"Extracted '{args.zip}' into '{args.out}'.")


if __name__ == "__main__":
    main()
