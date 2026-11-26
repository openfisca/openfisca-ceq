# Backlog openfisca-ceq

Discipline : toute tâche reportée vit ici, pas dans les conversations ni les sessions.

> Branche de travail : `scission-core` (worktree `../openfisca-ceq-scission-core`), 2.0.0.
> La **phase 2** du plan (API générique + élagage du cœur) y est largement faite ; voir ci-dessous.

## Chantiers

- [ ] **Scission core / études pays** — plan complet : `documentation/plan-scission-core-etudes.md`.
      Phase 0 (décisions de périmètre) à trancher par le mainteneur. Restent les phases 1 (dépôt
      `openfisca-ceq-afrique-ouest` extrait avec historique via `git filter-repo`), 3 (adapter les
      études aux imports 2.0) et 4 (relock ceq-tunisie sur le cœur 2.0, hygiène).
- [ ] **Tests unitaires purs du cœur** (PRIORITÉ) : il ne reste que 4 tests YAML (`tests/formulas/`).
      Écrire des cas-types et identités yc/yf sur les 72 variables de concepts — le risque
      « les tests fondent » du plan s'est matérialisé ; sécurise le 2.0.
- [ ] **Doc `gross_income`** : divergence handbook CEQ vs implémentation Banque mondiale Tunisie
      (scénario PDI dégénéré, pens=0) — issue #80.
- [ ] **Workflow deploy** (suites de la PR #81, token agent sans scope workflow) :
      passer `uv build --wheel` → `uv build` pour publier aussi le sdist ;
      supprimer l'étape `uv pip install twine` devenue redondante (twine est dans le lock).

- [ ] **`.github/dependabot.yml` à dépoussiérer** (hors de portée du token agent → à faire à la main) :
      retirer le bloc `ignore: autopep8 1.5.5` (autopep8 abandonné au profit de ruff, PR #81) ;
      passer `package-ecosystem: pip` → `uv` (le dépôt n'a plus que `pyproject.toml` + `uv.lock`) ;
      envisager `interval: weekly` au lieu de `daily`.

## Fait récemment

- [x] **Scission phase 2 (branche `scission-core`)** : `add_ceq_framework` rendu agnostique du pays
      (données d'étude injectées en keyword-only) ; code études élagué (−21 972 lignes : notebooks,
      `tools/survey_scenario.py`, `tools/data/`, `tools/data_ceq_correspondence.py`, `tools/results/`,
      tests dépendants des données, assets `unit_cost_*`) ; table pays→code des taxes indirectes
      pilotée par la config `[ceq] country_codes` ; bump 2.0.0 + CHANGELOG de migration.
- [x] **Dépendances élaguées** (branche `scission-core`) : retrait de `matplotlib`, `scipy`, `xlrd`
      (runtime) et `papermill` (dev), inutiles après le départ des études ; `uv.lock` régénéré.

- [x] Python ≥ 3.12 : pkg_resources → importlib (#78, PR #79, v1.0.3).
- [x] Packaging finalisé : MANIFEST.in supprimé, package-data explicite, twine verrouillé
      (PR #81, v1.0.4) ; chaîne de publication PyPI réparée (1.0.4 en ligne — la 1.0.3
      n'était jamais partie, deploy cassé par twine/packaging).
- [x] Revue obligatoire retirée de master (mainteneur solo ; les checks CI restent requis).
- [x] PRs dependabot apurées : #71 (flake8) et #73 (autopep8) fermées (outils remplacés par ruff,
      setup.py disparu) ; #77 mergée (certifi 2026.11.20, retrait racine emSign).
