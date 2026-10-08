# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.1] - 2026-10-02

### Fixed

- On Windows, `qgis.pth` is written into `Lib/site-packages` instead of the venv root, so tools that resolve `.pth`
  files without running Python (such as ty) find the QGIS Python packages.

## [0.2.0] - 2026-08-20

### Added

- Support for QGIS 4 (Qt6) installations on Windows.

### Changed

- The package is built with `uv_build` instead of Hatch.

## [0.1.0] - 2024-02-14

### Added

- Create a Python virtual environment for QGIS plugin development on Windows and Linux.
- On Windows, discover QGIS installations under `C:\Program Files`, `C:\OSGeo4W` and `C:\OSGeo4W64`, and prompt
  for the one to use when there are several.

[unreleased]: https://github.com/GispoCoding/qgis-venv-creator/compare/v0.2.1...HEAD
[0.2.1]: https://github.com/GispoCoding/qgis-venv-creator/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/GispoCoding/qgis-venv-creator/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/GispoCoding/qgis-venv-creator/releases/tag/v0.1.0
