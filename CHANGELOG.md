# Changelog

## 1.0.0 - Migration to modern Python tooling

* **Major change**: Complete migration to modern Python packaging and tooling.
* **Breaking changes**:
  - **Python 3.11 minimum required** (previously Python 3.7+)
  - Removed `setup.py` and `setup.cfg` in favor of `pyproject.toml`
  - Replaced `flake8` and `autopep8` with `ruff` for linting and formatting
  - Replaced `pip` with `uv` for all package management operations
  - Removed CircleCI in favor of GitHub Actions
* **Technical improvements**:
  - Modern Python packaging with `pyproject.toml` (PEP 517/518)
  - Faster dependency management with `uv`
  - Improved code quality checks with `ruff`
  - Streamlined CI/CD with GitHub Actions
  - Automatic PyPI deployment on master branch
  - Automatic git tag creation on releases
* **Documentation**:
  - Updated installation instructions to use `uv`
  - Updated README with new tooling information
* **Migration guide**:
  - **Python 3.11 or higher is now required** (upgrade from Python 3.7-3.10 if needed)
  - Users should install `uv` before installing this package
  - Developers should use `make install` which uses `uv sync`
  - All CI/CD now runs on GitHub Actions

## 0.4.1 - [#59](https://github.com/openfisca-ceq/pull/59)

* Technical improvement.
* Details:
  - Fix deps

## 0.4.0 - [#43](https://github.com/openfisca-ceq/pull/43)

* Technical improvement.
* Impacted periods: all.
* Details:
  - Add education unit cost by country

## 0.3.1 - [#41](https://github.com/openfisca-ceq/pull/41)

- Many changes

## 0.2.5 - [#30](https://github.com/openfisca-ceq/pull/30)

* Minor change.
  - Remove CEQ framework test with openfisca-cote-d-ivoire

## 0.2.4 - [#16](https://github.com/openfisca-ceq/pull/16)

* Minor change.
  - Remove CEQ framework test with openfisca-cote-d-ivoire

## 0.2.3 - [#12](https://github.com/openfisca-ceq/pull/12)

* Minor change.
  - Fix test

## 0.2.2 - [#11](https://github.com/openfisca-ceq/pull/11)

* Minor change.
  - Fix module discovery

## 0.2.1 - [#10](https://github.com/openfisca-ceq/pull/10)

* Minor change.
  - Fix dependency

## 0.2.0 - [#X](https://github.com/openfisca-ceq/pull/X)

* Minor change.
  - Clean obsolete boiler-plate
  - Create `add_ceq_framework`

## 0.1.2 - [#3](https://github.com/openfisca-ceq/pull/3)

* Minor change.
  - Clean unnecessary comments
  - Reoganize test folders

## 0.1.1 - [#2](https://github.com/openfisca-ceq/pull/2)

* Adapt test syntax to openfisca-core 25.2.2
* Improve Makefile

## 0.1.0 - [#](https://github.com/openfisca-ceq)

* Fisrt implementation of CEQ
