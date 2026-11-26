# Plan de scission : core openfisca-ceq vs études pays

> Établi le 26/11/2026 lors du branchement d'openfisca-ceq dans ceq-tunisie.
> Statut : PLAN — aucune exécution engagée. Suivi dans `documentation/backlog.md`.

## Constat

Le dépôt mélange deux natures :

- **Core réutilisable** (consommé p. ex. par ceq-tunisie) : `entities.py`, les 72 variables de
  concepts CEQ (`variables/`), le framework de branchement
  (`tools/tax_benefit_system_ceq_completion.py`), le générateur de taxes indirectes
  (`tools/indirect_taxation/`).
- **Études pays Afrique de l'Ouest** (couplées aux enquêtes harmonisées CEQ-Afrique) :
  `notebooks/` (senegal, mali, cote_d_ivoire + example/export/results/test),
  `tools/survey_scenario.py`, `tools/data/` (loaders revenus/dépenses/cibles),
  `tools/results/`, `tools/data_ceq_correspondence.py`, la quasi-totalité de `tests/`
  (dépendants des données pays), les assets pays (coûts unitaires éducation,
  `merged*.csv/xls` COICOP), `documentation/multi_country_comparison.md`.

Couplage structurel à corriger : `tax_benefit_system_ceq_completion` code en dur la table
`country_packages` (senegal/mali/côte-d'ivoire) — le core connaît les pays.

## Architecture cible : 2 dépôts

1. **`openfisca-ceq`** (core, PyPI, v2.0.0 — breaking) : entités, 72 variables, framework de
   complétion générique (le pays passe son TBS et son mapping en paramètres), générateur de
   taxes indirectes générique. Tests unitaires purs, sans données. Aucun notebook.
2. **`openfisca-ceq-afrique-ouest`** (nouveau, non publié) : les 3 études SN/ML/CI —
   notebooks, loaders, survey_scenario multi-pays, calibration, results, assets pays, doc
   comparative. Dépend du core via PyPI.

Pourquoi pas un dépôt par pays : les 3 études partagent loaders, nomenclatures harmonisées et
notebook de comparaison. (ceq-tunisie reste indépendant : il ne consomme que le core.)

## Phases

- **Phase 0 — décisions** : nom du dépôt études ; sort des notebooks `test/example/export` ;
  sort de `data_ceq_correspondence` (études, sauf nouveaux pays harmonisés prévus) ; sort des
  assets `merged*` COICOP (études ; le générateur core prend le chemin en paramètre).
- **Phase 1 — dépôt études avec historique** : `git filter-repo` (paths pays) → historique
  préservé ; pyproject (`openfisca-ceq>=2.0`) ; CI avec tests skippables sans données ; AGPL.
- **Phase 2 — élaguer le core** : retirer les éléments déménagés ; dé-coder les pays de
  `ceq_completion` (API `add_ceq_framework(tbs, mapping, …)`) ; release 2.0.0 + CHANGELOG de
  migration ; README croisés.
- **Phase 3 — adapter le dépôt études** : imports API 2.0 ; faire tourner au moins un notebook ;
  figer uv.lock.
- **Phase 4 — consommateurs & hygiène** : relock ceq-tunisie sur core 2.0 (impact attendu nul) ;
  purger build/, egg-info, MANIFEST résiduels ; transférer les issues pays.

## Risques

- Breaking 2.0 : utilisateurs inconnus des tools pays — CHANGELOG explicite, 1.0.4 reste sur PyPI.
- Les tests du core fondent (presque tous dépendent des données pays) : écrire des tests
  unitaires nouveaux sur les 72 variables (réinjecter l'expérience ceq-tunisie).
- Données d'enquêtes non versionnées : le dépôt études documentera leur provenance.
