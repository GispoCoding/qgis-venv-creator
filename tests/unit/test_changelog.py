# SPDX-FileCopyrightText: 2026 Gispo Ltd. <info@gispo.fi>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "changelog.py"
REPOSITORY = "https://github.com/example/project"

CHANGELOG = f"""\
# Changelog

## [Unreleased]

### Fixed

- Fix a bug.

## [1.1.0] - 2026-02-01

### Added

- Add a feature.

## [1.0.0] - 2026-01-01

### Added

- Initial release.

[unreleased]: {REPOSITORY}/compare/v1.1.0...HEAD
[1.1.0]: {REPOSITORY}/compare/v1.0.0...v1.1.0
[1.0.0]: {REPOSITORY}/releases/tag/v1.0.0
"""

# CHANGELOG after releasing 1.2.0
RELEASED_CHANGELOG = f"""\
# Changelog

## [Unreleased]

## [1.2.0] - 2026-03-01

### Fixed

- Fix a bug.

## [1.1.0] - 2026-02-01

### Added

- Add a feature.

## [1.0.0] - 2026-01-01

### Added

- Initial release.

[unreleased]: {REPOSITORY}/compare/v1.2.0...HEAD
[1.2.0]: {REPOSITORY}/compare/v1.1.0...v1.2.0
[1.1.0]: {REPOSITORY}/compare/v1.0.0...v1.1.0
[1.0.0]: {REPOSITORY}/releases/tag/v1.0.0
"""


def run_script(*args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, check=False)


@pytest.fixture
def changelog(tmp_path: Path) -> Path:
    path = tmp_path / "CHANGELOG.md"
    # write_bytes keeps the LF line endings on Windows too
    path.write_bytes(CHANGELOG.encode("utf-8"))
    return path


def test_release_moves_unreleased_entries_under_the_version(changelog: Path):
    result = run_script("--file", str(changelog), "release", "1.2.0", "--date", "2026-03-01")

    assert result.returncode == 0, result.stderr
    assert changelog.read_bytes().decode("utf-8") == RELEASED_CHANGELOG


def test_release_fails_without_unreleased_entries(changelog: Path):
    content = CHANGELOG.replace("### Fixed\n\n- Fix a bug.\n\n", "")
    changelog.write_bytes(content.encode("utf-8"))

    result = run_script("--file", str(changelog), "release", "1.2.0")

    assert result.returncode != 0
    assert b"add entries under '## [Unreleased]'" in result.stderr
    assert changelog.read_bytes().decode("utf-8") == content


def test_release_fails_for_an_already_released_version(changelog: Path):
    result = run_script("--file", str(changelog), "release", "1.1.0")

    assert result.returncode != 0
    assert b"already has a section for 1.1.0" in result.stderr
    assert changelog.read_bytes().decode("utf-8") == CHANGELOG


@pytest.mark.parametrize(
    ("version", "expected"),
    [
        ("1.1.0", "### Added\n\n- Add a feature.\n"),
        # The last section ends at the link definitions
        ("1.0.0", "### Added\n\n- Initial release.\n"),
    ],
)
def test_notes_prints_the_entries_of_the_version(changelog: Path, version: str, expected: str):
    result = run_script("--file", str(changelog), "notes", version)

    assert result.returncode == 0, result.stderr
    assert result.stdout.decode("utf-8") == expected


def test_notes_fails_for_an_unknown_version(changelog: Path):
    result = run_script("--file", str(changelog), "notes", "9.9.9")

    assert result.returncode != 0
    assert b"no '## [9.9.9]' section" in result.stderr


def test_notes_of_the_repository_changelog():
    # Guards against CHANGELOG.md drifting into a format the release workflows can't parse
    result = run_script("notes", "0.1.0")

    assert result.returncode == 0, result.stderr
    assert result.stdout.startswith(b"### Added")
