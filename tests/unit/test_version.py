# SPDX-FileCopyrightText: 2026 Gispo Ltd. <info@gispo.fi>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

from importlib.metadata import version

from qgis_venv_creator import create_qgis_venv


def test_version_matches_package_metadata():
    # pyproject.toml [project].version is the source of truth; the script's
    # __version__ is a synced copy. Guard against the two drifting apart.
    assert create_qgis_venv.__version__ == version("qgis-venv-creator")
