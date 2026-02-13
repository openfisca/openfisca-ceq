all: test

uninstall:
	uv pip freeze | grep -v "^-e" | xargs uv pip uninstall -y

clean:
	rm -rf build dist
	find . -name '*.pyc' -exec rm \{\} \;

deps:
	@# Ensure uv is installed
	@command -v uv >/dev/null 2>&1 || { echo "Error: uv is not installed. Install it with: curl -LsSf https://astral.sh/uv/install.sh | sh"; exit 1; }
	uv pip install --upgrade twine

install:
	@# Install OpenFisca-CEQ for development.
	@# `make install` installs the editable version of OpenFisca-CEQ.
	@# This allows contributors to test as they code.
	@# uv sync automatically creates a virtual environment and installs dependencies from pyproject.toml
	@# --extra dev installs the optional dev dependencies
	uv sync --extra dev
	uv pip install openfisca-core

build: clean
	@# Install OpenFisca-CEQ for deployment and publishing.
	@# `make build` allows us to be be sure tests are run against the packaged version
	@# of OpenFisca-CEQ, the same we put in the hands of users and reusers.
	uv build --wheel
	find dist -name "*.whl" -exec uv pip install --upgrade {}[dev] \;
	uv pip install openfisca-core[web-api]

check-syntax-errors:
	uv run python -m compileall -q .

format-style:
	@# Do not analyse .gitignored files.
	@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
	uv run ruff format `git ls-files | grep "\.py$$"`
	uv run ruff check --fix `git ls-files | grep "\.py$$"`

check-style:
	@# Do not analyse .gitignored files.
	@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
	uv run ruff check `git ls-files | grep "\.py$$"`

notebook-all: notebook-cote_d_ivoire notebook-mali notebook-senegal

notebook-cote_d_ivoire:
	rm -f notebooks/cote_d_ivoire.ipynb
	uv run papermill -p country cote_d_ivoire notebooks/test.ipynb notebooks/cote_d_ivoire.ipynb

notebook-mali:
	rm -f notebooks/mali.ipynb
	uv run papermill -p country mali notebooks/test.ipynb notebooks/mali.ipynb

notebook-senegal:
	rm -f notebooks/senegal.ipynb
	uv run papermill -p country senegal notebooks/test.ipynb notebooks/senegal.ipynb

notebook-results:
	uv run jupyter nbconvert --execute --to notebook --inplace notebooks/results.ipynb

test: check-syntax-errors check-style
	@# Launch tests from openfisca_ceq/tests directory (and not .) because TaxBenefitSystem must be initialized
	@# before parsing source files containing formulas.
	@# Tests requiring local Stata .dta files are ignored (CI mode)
	uv run openfisca test --country-package openfisca_ceq openfisca_ceq/tests

test-all: check-syntax-errors check-style
	@# Run all tests including those requiring local Stata .dta files
	@# This requires raw_data.ini configuration and local data files
	@# Override pytest addopts to remove --ignore options from pyproject.toml
	uv run pytest openfisca_ceq/tests -o "addopts=--showlocals --exitfirst --doctest-modules --disable-pytest-warnings"
