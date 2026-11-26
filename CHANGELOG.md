# Changelog

## 2.0.0 - Scission cœur / études (BREAKING)

Séparation du cœur réutilisable et des études pays Afrique de l'Ouest. Les études
(Sénégal, Mali, Côte d'Ivoire) migrent vers le paquet `openfisca-ceq-afrique-ouest`.
`openfisca-ceq` ne contient plus que le cœur réutilisable.

* **Breaking** : `add_ceq_framework` est désormais **agnostique du pays**. Signature
  keyword-only : `add_ceq_framework(tbs, *, harmonized_income_mapping=None,
  custom_variables=None, extra_variables=None, education_unit_cost=None)`. Les données
  propres à une étude (mapping harmonisé, variables custom, variables d'enquête, coûts
  unitaires) sont **injectées** par l'appelant, plus importées au chargement du module.
* **Breaking** : `add_ceq_education_unit_cost(tbs, unit_cost_by_category)` prend un dict
  `{catégorie: coût}` au lieu d'un `legislation_country`.
* **Breaking** : suppression du cœur de la réforme `ceq`, des variables d'enquête
  concrètes (`cadre`, `categorie_cgu`, `labor_type`, `secteur_*`, `survey_income`,
  `hh_id`, …), de `labor_type_by_index`, et des modules études `tools/survey_scenario.py`,
  `tools/data/`, `tools/data_ceq_correspondence.py`, `tools/results/`, des notebooks,
  des tests dépendants des données pays, et des assets `unit_cost_*`. Tout cela vit
  désormais dans `openfisca-ceq-afrique-ouest`.
* **Breaking** : le générateur de taxes indirectes n'a plus de table pays codée en dur.
  La correspondance pays -> code est lue depuis l'option `country_codes` de la section
  `[ceq]` de `raw_data.ini` (format `senegal:SEN,mali:MLI,cote_d_ivoire:CIV`) ; un code
  manquant lève une erreur explicite.
* **Conservé** : entités, les 72 variables de concepts CEQ (`variables/`), le framework
  de complétion générique, le générateur de taxes indirectes, `tests/formulas`.
* **Bugfix** (porté de 819eae5) : `add_ceq_education_unit_cost` liait mal les variables
  lues à l'expression numexpr (KeyError) ; corrigé via un `local_dict` explicite.
* **Dépendances élaguées** : retrait de `matplotlib`, `scipy`, `xlrd` (runtime) et
  `papermill` (dev), devenus inutiles après le départ des études (graphiques, calibration,
  lecture `.xls`, exécution de notebooks). Conservés : `OpenFisca-Survey-Manager`,
  `OpenFisca-Core`, `python-slugify`, `xlsxwriter`, `xlwt` (écriture `merged.xls`).
* **Bugfix (signe)** : `health_net_transfers` retranchait à tort `health_in_patient` et
  `health_out_patient`. Le manuel CEQ (Lustig, Handbook 2022) définit le revenu final comme
  ajoutant la valeur monétisée des transferts en nature de santé (au coût moyen de l'État) et
  ne retranchant que les co-paiements / frais d'usager : les prestations hospitalières et
  ambulatoires s'**additionnent** désormais ; seul `health_copay_fees` se retranche. Impact :
  `final_income` plus élevé quand il y a des soins in/out-patient.
* **Tests** : nouveaux tests YAML du cœur, sans données pays — échelle complète des concepts
  de revenu (identités yc/yf), agrégateurs de composantes, signe de `health_net_transfers`,
  agrégation personne→ménage, cas nul.
* **Non impacté** : `ceq-tunisie`, qui ne consomme que `CountryTaxBenefitSystem`.

## 1.0.4 - [#81](https://github.com/openfisca/openfisca-ceq/pull/81) - Finalize packaging migration to pyproject.toml

* **Technical improvement**: Complete the packaging migration started in 1.0.0 (follow-up to [#79](https://github.com/openfisca/openfisca-ceq/pull/79))
  - Remove `MANIFEST.in` (catch-all `recursive-include * *`); package data is now declared explicitly in `pyproject.toml` via `[tool.setuptools.package-data]` (`assets/`, `variables/`, `tests/formulas/`)
  - Restrict package discovery to `openfisca_ceq*` (`[tool.setuptools.packages.find]`), aligning with OpenFisca-Tunisia conventions
  - Add `Issues` and `Changelog` project URLs
* **Bugfix**: Fix the PyPI deploy job failure that prevented 1.0.3 from being published
  - Add `twine >=6.0.0` to the `dev` extra and lock it in `uv.lock`, so the deploy job's `uv pip install twine` no longer upgrades `packaging` on the fly in the synced environment (which broke `twine upload` with `ImportError: cannot import name 'errors' from 'packaging'`)

## 1.0.3 - [#79](https://github.com/openfisca/openfisca-ceq/pull/79) - Python 3.12 compatibility

* **Bugfix**: Fix `AttributeError: module 'pkgutil' has no attribute 'ImpImporter'` at import time on Python >= 3.12 (fixes [#78](https://github.com/openfisca/openfisca-ceq/issues/78))
  - Replace `pkg_resources` with `importlib.resources` in `openfisca_ceq/tools/tax_benefit_system_ceq_completion.py` and `openfisca_ceq/tools/indirect_taxation/consumption_items_nomenclature.py`
  - Remove the `setuptools<66` runtime dependency (no longer needed)
  - Relax the `yamllint` dev dependency pin (`<1.27` -> `<2`) so dev environments no longer pull `setuptools 65.7.0`, whose `pkg_resources` breaks on Python 3.12
  - Regenerate `uv.lock` (`setuptools` is no longer locked)

## 1.0.2 - [#76](https://github.com/openfisca/openfisca-ceq/pull/76) - Bugfix release

* **Bugfix**: Documentation and deployment improvements
  - Add PyPI deployment configuration guide
  - Add verbose flag to twine upload for better error diagnostics
  - Improve troubleshooting documentation

## 1.0.1 - Bugfix release

* **Bugfix**: Fix deploy job in GitHub Actions workflow
  - Create virtual environment before installing twine in deploy job
  - Fixes error: "No virtual environment found" during PyPI deployment

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
