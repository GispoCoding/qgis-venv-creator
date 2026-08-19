"""Sync __version__ in create_qgis_venv.py from the version in pyproject.toml.

create_qgis_venv.py is designed to also work as a standalone script copied
into another repo, so it must carry its version as a literal instead of
reading it from package metadata. Run this after `uv version --bump <part>`
to keep the two in sync (tests/unit/test_version.py guards against drift).

Requires Python 3.11+ (tomllib).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import tomllib

REPO_ROOT = Path(__file__).resolve().parent.parent
PYPROJECT = REPO_ROOT / "pyproject.toml"
SCRIPT = REPO_ROOT / "src" / "qgis_venv_creator" / "create_qgis_venv.py"


def main() -> None:
    version = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))["project"]["version"]
    source = SCRIPT.read_text(encoding="utf-8")
    updated, count = re.subn(
        r"^__version__ = .*$",
        f'__version__ = "{version}"',
        source,
        count=1,
        flags=re.MULTILINE,
    )
    if count != 1:
        sys.exit(f"error: no __version__ line found in {SCRIPT}")
    SCRIPT.write_text(updated, encoding="utf-8", newline="\n")
    print(f"Synced __version__ in {SCRIPT.relative_to(REPO_ROOT)} to {version}")


if __name__ == "__main__":
    main()
