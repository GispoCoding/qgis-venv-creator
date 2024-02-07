# SPDX-FileCopyrightText: 2024 Gispo Ltd. <info@gispo.fi>
#
# SPDX-License-Identifier: MIT

import subprocess
from pathlib import Path

import pytest

# Mark the whole module to run only on Windows
pytestmark = [pytest.mark.linux, pytest.mark.e2e]


@pytest.fixture(scope="session")
def venv_parent(tmp_path_factory: pytest.TempPathFactory) -> Path:
    venv_parent_directory = tmp_path_factory.mktemp("venv_parent")

    try:
        subprocess.run(
            ["create-qgis-venv", "--venv-name", ".venv"],
            cwd=venv_parent_directory,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Venv creation failed.: {e.stdout}. {e.stderr}")

    return venv_parent_directory


def test_venv_creation(venv_parent: Path):
    try:
        p = subprocess.run(
            '. .venv/bin/activate && python -c "from qgis.core import Qgis;print(Qgis.version())"',
            cwd=venv_parent,
            capture_output=True,
            shell=True,
            text=True,
            check=True,
        )
        qgis_version = p.stdout.strip()
        print(qgis_version)  # noqa: T201
        assert qgis_version.startswith("3.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Venv creation failed or the venv has no qgis module available.: {e.stderr}")
