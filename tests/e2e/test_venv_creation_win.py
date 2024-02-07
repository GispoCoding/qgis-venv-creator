# SPDX-FileCopyrightText: 2024 Gispo Ltd. <info@gispo.fi>
#
# SPDX-License-Identifier: MIT

import subprocess
from pathlib import Path

import pytest

# Mark the whole module to run only on Windows
pytestmark = [pytest.mark.windows, pytest.mark.e2e]


class TestVenvCreation:
    @pytest.fixture(scope="class")
    def venv_parent(self, tmp_path_factory: pytest.TempPathFactory) -> Path:
        venv_parent_directory = tmp_path_factory.mktemp("venv_parent")

        try:
            subprocess.run(
                ["create-qgis-venv", "--venv-name", ".venv"],
                input="1\n",
                cwd=venv_parent_directory,
                text=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Venv creation failed.: {e.stdout}. {e.stderr}")

        return venv_parent_directory

    def test_qgis_is_importable(self, venv_parent: Path):
        try:
            p = subprocess.run(
                '.venv\\Scripts\\activate && python -c "from qgis.core import Qgis;print(Qgis.version())"',
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
            pytest.fail(f"Venv has no qgis module available.: {e.stderr}")

    def test_sqlite_is_importable(self, venv_parent: Path):
        """Test if the sqlite3 module is available in the venv.

        Sqlite has its dll in osgeo4w/bin directory which is problematic if the bin path is not added
        right in sitecustomize.py
        """
        try:
            p = subprocess.run(
                '.venv\\Scripts\\activate && python -c "import sqlite3"',
                cwd=venv_parent,
                capture_output=True,
                shell=True,
                text=True,
                check=True,
            )
            print(p.stdout)  # noqa: T201
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Venv has no sqlite3 module available.: {e.stderr}")

    def test_pip_works(self, venv_parent: Path):
        """Test if new packages can be installed using pip

        Pip uses a ssl library that is located in osgeo4w/bin directory which is not discovered without the right
        kind of sitecustomize.py.
        """
        try:
            p = subprocess.run(
                ".venv\\Scripts\\activate && python -m pip install -U pip",
                cwd=venv_parent,
                capture_output=True,
                shell=True,
                text=True,
                check=True,
            )
            print(p.stdout)  # noqa: T201
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Pip does not work on the venv created.: {e.stderr}")
