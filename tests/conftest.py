# SPDX-FileCopyrightText: 2024 Gispo Ltd. <info@gispo.fi>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import platform

import pytest

platform_markers = {"windows", "linux", "macos"}
platform_to_marker = {"Windows": "windows", "Linux": "linux", "Darwin": "macos"}


def pytest_addoption(parser: pytest.Parser):
    parser.addoption("--run-e2e", action="store_true", default=False, help="Run e2e tests")


def pytest_configure(config: pytest.Config):
    config.addinivalue_line("markers", "windows: Mark a test to run only on Windows.")
    config.addinivalue_line("markers", "linux: Mark a test to run only on Linux.")
    config.addinivalue_line("markers", "macos: Mark a test to run only on MacOs.")
    config.addinivalue_line("markers", "e2e: Mark a test as an end-to-end test.")


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]):
    run_e2e = config.getoption("--run-e2e")
    platform_marker = platform_to_marker.get(platform.system())

    skip_e2e = pytest.mark.skip(reason="Need --run-e2e option to run this e2e-test.")
    for item in items:
        if run_e2e is False and "e2e" in item.keywords:
            item.add_marker(skip_e2e)

        run_on_markers = platform_markers.intersection(set(item.keywords))
        if run_on_markers and platform_marker not in run_on_markers:
            item.add_marker(
                pytest.mark.skip(reason=(f"Test is configured to run only on '{', '.join(run_on_markers)}'"))
            )
