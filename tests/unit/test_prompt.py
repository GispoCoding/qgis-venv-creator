# SPDX-FileCopyrightText: 2024 Gispo Ltd. <info@gispo.fi>
#
# SPDX-License-Identifier: MIT

from pathlib import Path
from unittest import mock

import pytest

from qgis_venv_creator.create_qgis_venv import MultiQgisPlatform

pytestmark = [pytest.mark.windows]


def mock_input_factory(return_values):
    values = return_values

    def mock_input(prompt):
        print(prompt)  # noqa: T201
        return values.pop(0)

    return mock_input


def test_prompt_on_valid_selection(capfd):
    with mock.patch("builtins.input") as mock_input, mock.patch.object(
        MultiQgisPlatform, "_find_qgis_installations"
    ) as mock_find:
        mock_input.side_effect = mock_input_factory(return_values=["1"])
        qgis_installations = [
            "C:/OSGeo4W/apps/qgis",
            "C:/OSGeo4W/apps/qgis-ltr",
            "C:/OSGeo4W/apps/qgis-dev",
        ]
        mock_find.side_effect = [qgis_installations]

        selected_qgis_installation = MultiQgisPlatform.select_qgis_install()
        assert selected_qgis_installation == qgis_installations[0]

        expected_output = (
            "Found following QGIS installations from the system. Which one to use for development?\n"
            "  1 - C:/OSGeo4W/apps/qgis\n"
            "  2 - C:/OSGeo4W/apps/qgis-ltr\n"
            "  3 - C:/OSGeo4W/apps/qgis-dev\n"
            "  4 - Custom\n"
            "  Choose from [1/2/3/4]: \n"
        )
        out, err = capfd.readouterr()
        assert out == expected_output


def test_prompt_on_invalid_selection(capfd):
    with mock.patch("builtins.input") as mock_input, mock.patch.object(
        MultiQgisPlatform, "_find_qgis_installations"
    ) as mock_find:
        mock_input.side_effect = mock_input_factory(return_values=["5", "1"])
        qgis_installations = [
            "C:/OSGeo4W/apps/qgis",
            "C:/OSGeo4W/apps/qgis-ltr",
            "C:/OSGeo4W/apps/qgis-dev",
        ]
        mock_find.side_effect = [qgis_installations]

        selected_qgis_installation = MultiQgisPlatform.select_qgis_install()
        assert selected_qgis_installation == qgis_installations[0]

        expected_output = (
            "Found following QGIS installations from the system. Which one to use for development?\n"
            "  1 - C:/OSGeo4W/apps/qgis\n"
            "  2 - C:/OSGeo4W/apps/qgis-ltr\n"
            "  3 - C:/OSGeo4W/apps/qgis-dev\n"
            "  4 - Custom\n"
            "  Choose from [1/2/3/4]: \n"
            "Invalid selection\n"
            "  Choose from [1/2/3/4]: \n"
        )

        out, err = capfd.readouterr()
        assert out == expected_output


def test_prompt_on_custom_path(capfd):
    with mock.patch("builtins.input") as mock_input, mock.patch.object(
        MultiQgisPlatform, "_find_qgis_installations"
    ) as mock_find, mock.patch.object(MultiQgisPlatform, "_is_valid_qgis_path") as mock_is_valid:
        mock_input.side_effect = mock_input_factory(return_values=["2", "C:\\invalid", "C:\\valid"])
        mock_find.side_effect = [["C:/OSGeo4W/apps/qgis"]]
        mock_is_valid.side_effect = [False, True]
        selected_qgis_installation = MultiQgisPlatform.select_qgis_install()
        assert selected_qgis_installation == Path("C:/valid")

        expected_output = (
            "Found following QGIS installations from the system. Which one to use for development?\n"
            "  1 - C:/OSGeo4W/apps/qgis\n"
            "  2 - Custom\n"
            "  Choose from [1/2]: \n"
            "  Give path to QGIS installation: \n"
            "Invalid qgis installation path\n"
            "  Give path to QGIS installation: \n"
        )

        out, err = capfd.readouterr()
        assert out == expected_output
