# Backlog openfisca-ceq

Discipline : toute tâche reportée vit ici, pas dans les conversations ni les sessions.

## Chantiers

- [ ] **Scission core / études pays** — plan complet : `documentation/plan-scission-core-etudes.md`.
      Phase 0 (décisions de périmètre) à trancher par le mainteneur avant toute exécution.
- [ ] **Doc `gross_income`** : divergence handbook CEQ vs implémentation Banque mondiale Tunisie
      (scénario PDI dégénéré, pens=0) — issue #80.
- [ ] **Workflow deploy** (suites de la PR #81, token agent sans scope workflow) :
      passer `uv build --wheel` → `uv build` pour publier aussi le sdist ;
      supprimer l'étape `uv pip install twine` devenue redondante (twine est dans le lock).
- [ ] **Tests du core** : la plupart des tests actuels dépendent des données pays (skippés sans
      données) ; écrire des tests unitaires purs sur les 72 variables de concepts
      (cas-types, identités yc/yf) — prérequis de la phase 2 de la scission.
- [ ] **`country_packages` codé en dur** dans `tools/tax_benefit_system_ceq_completion.py` :
      à génériser (le pays passe TBS + mapping) — cœur de la phase 2.

## Fait récemment

- [x] Python ≥ 3.12 : pkg_resources → importlib (#78, PR #79, v1.0.3).
- [x] Packaging finalisé : MANIFEST.in supprimé, package-data explicite, twine verrouillé
      (PR #81, v1.0.4) ; chaîne de publication PyPI réparée (1.0.4 en ligne — la 1.0.3
      n'était jamais partie, deploy cassé par twine/packaging).
- [x] Revue obligatoire retirée de master (mainteneur solo ; les checks CI restent requis).
