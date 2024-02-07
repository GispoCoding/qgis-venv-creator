# SPDX-FileCopyrightText: 2024 Gispo Ltd. <info@gispo.fi>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import platform

import pytest

platform_markers = {"windows", "linux", "macos"}
platform_to_marker = {"Windows": "windows", "Linux": "linux", "Darwin": "macos"}


def pytest_configure(config: pytest.Config):
    config.addinivalue_line("markers", "windows: Mark a test to run only on Windows.")
    config.addinivalue_line("markers", "linux: Mark a test to run only on Linux.")
    config.addinivalue_line("markers", "macos: Mark a test to run only on MacOs.")


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]):
    platform_marker = platform_to_marker.get(platform.system())

    for item in items:
        run_on_markers = platform_markers.intersection(set(item.keywords))
        if run_on_markers and platform_marker not in run_on_markers:
            item.add_marker(
                pytest.mark.skip(reason=(f"Test is configured to run only on '{', '.join(run_on_markers)}'"))
            )
