all: test

uninstall:
	pip freeze | grep -v "^-e" | xargs pip uninstall -y

clean:
	rm -rf build dist
	find . -name '*.pyc' -exec rm \{\} \;

deps:
	pip install --upgrade pip twine wheel build

install: deps
	@# Install OpenFisca-CEQ for development.
	@# `make install` installs the editable version of OpenFisca-CEQ.
	@# This allows contributors to test as they code.
	pip install --editable .[dev] --upgrade
	pip install openfisca-core

build: clean deps
	@# Install OpenFisca-CEQ for deployment and publishing.
	@# `make build` allows us to be be sure tests are run against the packaged version
	@# of OpenFisca-CEQ, the same we put in the hands of users and reusers.
	python -m build --wheel
	find dist -name "*.whl" -exec pip install --upgrade {}[dev] \;
	pip install openfisca-core[web-api]

check-syntax-errors:
	python -m compileall -q .

format-style:
	@# Do not analyse .gitignored files.
	@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
	ruff format `git ls-files | grep "\.py$$"`
	ruff check --fix `git ls-files | grep "\.py$$"`

check-style:
	@# Do not analyse .gitignored files.
	@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
	ruff check `git ls-files | grep "\.py$$"`

notebook-all: notebook-cote_d_ivoire notebook-mali notebook-senegal

notebook-cote_d_ivoire:
	rm -f notebooks/cote_d_ivoire.ipynb
	papermill -p country cote_d_ivoire notebooks/test.ipynb notebooks/cote_d_ivoire.ipynb

notebook-mali:
	rm -f notebooks/mali.ipynb
	papermill -p country mali notebooks/test.ipynb notebooks/mali.ipynb

notebook-senegal:
	rm -f notebooks/senegal.ipynb
	papermill -p country senegal notebooks/test.ipynb notebooks/senegal.ipynb

notebook-results:
	jupyter nbconvert --execute --to notebook --inplace notebooks/results.ipynb

test: clean check-syntax-errors check-style
	@# Launch tests from openfisca_ceq/tests directory (and not .) because TaxBenefitSystem must be initialized
	@# before parsing source files containing formulas.
	@# pytest
	openfisca test --country-package openfisca_ceq openfisca_ceq/tests
