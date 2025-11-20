# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2025-11-20

### Added

- Initial public release of `toonlite` for Python.
- `loads()` to decode TOON Lite text into Python dictionaries.
- `dumps()` to encode Python dictionaries into TOON Lite text.
- Support for:
  - key–value pairs (`key: value`)
  - nested objects via 4-space indentation
  - lists using `key: []` and `- item` syntax
  - scalar values: integers, floats, booleans, null, and strings
- Basic test suite using `pytest`.
- Packaging configuration via `pyproject.toml`.
