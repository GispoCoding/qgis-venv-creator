# SPDX-FileCopyrightText: 2024 Gispo Ltd. <info@gispo.fi>
#
# SPDX-License-Identifier: MIT

from pathlib import Path

import pytest

from qgis_venv_creator.create_qgis_venv import Windows

pytestmark = [pytest.mark.windows]


def test_path_configuration_file_is_written_to_site_packages(tmp_path: Path):
    venv_directory = tmp_path / ".venv"
    site_packages = venv_directory / "Lib" / "site-packages"
    site_packages.mkdir(parents=True)

    Windows._create_path_configuration_file(venv_directory, Path("C:/OSGeo4W/apps/qgis"))  # noqa: SLF001

    assert (site_packages / "qgis.pth").read_text(encoding="utf-8") == "C:/OSGeo4W/apps/qgis/python\n"
    assert not (venv_directory / "qgis.pth").exists()
