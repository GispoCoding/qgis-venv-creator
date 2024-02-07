# QGIS Venv Creator

[![PyPI - Version](https://img.shields.io/pypi/v/qgis-venv-creator.svg)](https://pypi.org/project/qgis-venv-creator)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/qgis-venv-creator.svg)](https://pypi.org/project/qgis-venv-creator)
[![Tests and Style check](https://github.com/GispoCoding/qgis-venv-creator/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/GispoCoding/qgis-venv-creator/actions/workflows/test.yml)

---

Single file and zero dependency tool to create a Python virtual environment for QGIS plugin development.

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [Development](#development)
- [License](#license)

## Installation

The recommended way to install `qgis-venv-creator` (and other Python cli tools) is to install it with [pipx](https://pypa.github.io/pipx/). Pipx will install the application in an isolated environment and make it available as a command line utility. To install `pipx`, follow the instructions provided at https://github.com/pypa/pipx#install-pipx.

```console
$ pipx install qgis-venv-creator
```

Alternatively, to install in your current Python environment:

```console
$ pip install qgis-venv-creator
```

### Copy as a script

`qgis-venv-creator` is a single Python script that can be downloaded and copied to your project root, or any other location from which you wish to use it.

## Usage

### Quick start

On your plugin root directory, run:

```console
$ create-qgis-venv
```

> **Note:**  
> If you have copied the script file to your project root, you can run it with `python create-qgis-venv.py`.

On a system where there might be multiple QGIS installations (ie. Windows, MacOs), you are asked to select the one you want to use for development.

After the virtual environment is created, you can activate it and it will have access to the QGIS Python environment.

### Options

```
create-qgis-venv [-h] [--venv-parent VENV_PARENT] [--venv-name VENV_NAME]
                    [--qgis-installation QGIS_INSTALLATION]
                    [--qgis-installation-search-path-pattern QGIS_INSTALLATION_SEARCH_PATH_PATTERN]
                    [--python-executable PYTHON_EXECUTABLE] [--debug]
```

| Option                                  | Available on platform | Description                                                                                                                                                                                                                                                                             |
| --------------------------------------- | --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| -h, --help                              | ALL                   | Show this help message and exit                                                                                                                                                                                                                                                         |
| --venv-parent                           | ALL                   | Path to the parent directory of the virtual environment to be created. Most likely your project directory. Default current directory.                                                                                                                                                   |
| --venv-name                             | ALL                   | Name of the virtual environment                                                                                                                                                                                                                                                         |
| --qgis-installation                     | Windows               | Path to the QGIS installation to use for development. Installations made with official msi and Osgeo4W installers are supported. Give the path to the 'qgis' directory inside the 'apps' directory. If not given, the user is prompted to select one.                                   |
| --qgis-installation-search-path-pattern | Windows               | Custom glob pattern for QGIS installations to be selected. Can be set also with environment variable QGIS_INSTALLATION_SEARCH_PATH_PATTERN. For example "C:\\qgis\\\*\\apps\\qgis\*\\" to find installations from "C:\\qgis\\3.32\\apps\\qgis\\" and "C:\\qgis\\3.28\\apps\\qgis-ltr\\" |
| --python-executable                     | Windows               | Path to the Python executable used by the QGIS installation. If not given, the Python executable is searched from the QGIS installation.                                                                                                                                                |
| --debug                                 | ALL                   | Enable debug logging                                                                                                                                                                                                                                                                    |

## Development

This project uses [Hatch](https://hatch.pypa.io/) for development and packaging. Install instructions can be found at the project's website https://hatch.pypa.io/latest/install.

To facilitate development with VS Code, it is recommended to create hatch environments in the project folder. You can configure hatch to do so by running:

```console
hatch config set dirs.env.virtual ".hatch"
```

After Hatch has created the environment, you can set your Python interpreter to use the one located in `.hatch/qgis-venv-creator`.

### Pre-commit hook

This project uses [pre-commit](https://pre-commit.com/) to run code checks and tests before committing. You can install pre-commit with:

```console
pipx install pre-commit
```

Install pre-commit hooks to your repo with:

```console
pre-commit install
```

## License

`qgis-venv-creator` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
