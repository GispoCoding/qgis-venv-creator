"""Release and query version sections of CHANGELOG.md.

CHANGELOG.md follows the Keep a Changelog format (https://keepachangelog.com):
changes are collected under "## [Unreleased]" and moved under a version
heading when the version is released.

    python scripts/changelog.py release 1.2.0  # move [Unreleased] under [1.2.0], update the links
    python scripts/changelog.py notes 1.2.0    # print the entries of 1.2.0, e.g. for release notes

Works on Python 3.8+ so that the unit tests can run it on every supported version.
"""

from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CHANGELOG = REPO_ROOT / "CHANGELOG.md"

SECTION_HEADING = re.compile(r"^## \[(?P<name>[^\]]+)\]")
LINK_DEFINITION = re.compile(r"^\[[^\]]+\]: ")
UNRELEASED_LINK = re.compile(
    r"^(?P<label>\[unreleased\]): (?P<base>\S+)/compare/v(?P<previous>\S+)\.\.\.HEAD$",
    flags=re.IGNORECASE | re.MULTILINE,
)


def _find_heading(lines: list[str], name: str) -> int | None:
    for index, line in enumerate(lines):
        match = SECTION_HEADING.match(line)
        if match and match.group("name").lower() == name.lower():
            return index
    return None


def _section_end(lines: list[str], heading: int) -> int:
    """Return the index after the last line of the section starting at the heading.

    A section ends at the next section heading or at the link definitions at the end of the file.
    """
    end = heading + 1
    while end < len(lines) and not SECTION_HEADING.match(lines[end]) and not LINK_DEFINITION.match(lines[end]):
        end += 1
    return end


def _strip_blank_lines(lines: list[str]) -> list[str]:
    start, end = 0, len(lines)
    while start < end and not lines[start].strip():
        start += 1
    while end > start and not lines[end - 1].strip():
        end -= 1
    return lines[start:end]


def release(changelog: Path, version: str, date: str) -> None:
    lines = changelog.read_text(encoding="utf-8").splitlines()
    if _find_heading(lines, version) is not None:
        sys.exit(f"error: {changelog.name} already has a section for {version}")
    heading = _find_heading(lines, "Unreleased")
    if heading is None:
        sys.exit(f"error: no '## [Unreleased]' section in {changelog.name}")
    end = _section_end(lines, heading)
    entries = _strip_blank_lines(lines[heading + 1 : end])
    if not entries:
        sys.exit(f"error: add entries under '## [Unreleased]' in {changelog.name} before releasing")
    lines[heading:end] = [lines[heading], "", f"## [{version}] - {date}", "", *entries, ""]

    text = "\n".join(lines) + "\n"
    link = UNRELEASED_LINK.search(text)
    if link is None:
        sys.exit(f"error: no '[unreleased]: <repository>/compare/v<version>...HEAD' link in {changelog.name}")
    label, base, previous = link.group("label", "base", "previous")
    links = f"{label}: {base}/compare/v{version}...HEAD\n[{version}]: {base}/compare/v{previous}...v{version}"
    text = text[: link.start()] + links + text[link.end() :]

    # write_bytes keeps the LF line endings; write_text(newline=...) needs Python 3.10
    changelog.write_bytes(text.encode("utf-8"))
    print(f"Moved the unreleased entries of {changelog.name} under {version}")


def notes(changelog: Path, version: str) -> None:
    lines = changelog.read_text(encoding="utf-8").splitlines()
    heading = _find_heading(lines, version)
    if heading is None:
        sys.exit(f"error: no '## [{version}]' section in {changelog.name}")
    entries = _strip_blank_lines(lines[heading + 1 : _section_end(lines, heading)])
    if not entries:
        sys.exit(f"error: the '## [{version}]' section in {changelog.name} is empty")
    # Write UTF-8 with LF line endings regardless of the platform and console encoding
    sys.stdout.buffer.write(("\n".join(entries) + "\n").encode("utf-8"))


def _iso_date(value: str) -> str:
    return datetime.date.fromisoformat(value).isoformat()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--file", type=Path, default=CHANGELOG, help="changelog to use (default: %(default)s)")
    commands = parser.add_subparsers(dest="command", required=True)

    release_parser = commands.add_parser("release", help="move the unreleased entries under a new version")
    release_parser.add_argument("version")
    release_parser.add_argument(
        "--date",
        type=_iso_date,
        default=datetime.datetime.now(datetime.timezone.utc).date().isoformat(),
        help="release date as YYYY-MM-DD (default: today in UTC)",
    )

    notes_parser = commands.add_parser("notes", help="print the entries of a released version")
    notes_parser.add_argument("version")

    args = parser.parse_args()
    if args.command == "release":
        release(args.file, args.version, args.date)
    else:
        notes(args.file, args.version)


if __name__ == "__main__":
    main()
