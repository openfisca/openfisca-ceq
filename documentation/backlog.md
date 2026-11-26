# Backlog openfisca-ceq

Discipline : toute tâche reportée vit ici, pas dans les conversations ni les sessions.

> Branche de travail : `scission-core` (worktree `../openfisca-ceq-scission-core`), 2.0.0.
> La **phase 2** du plan (API générique + élagage du cœur) y est largement faite ; voir ci-dessous.

## Chantiers

- [ ] **Scission core / études pays** — phases 1 à 3 **faites en local** (dépôt études créé et
      adapté, cœur élagué). Reste, **gated** (actions irréversibles / réseau / scopes token) :
      - **merger `scission-core` → `master`** → publie 2.0.0 sur PyPI (le patch `ci.yml` est prêt) ;
      - **pousser** `scission-core` et ouvrir la PR ;
      - **créer le dépôt distant** `openfisca-ceq-afrique-ouest` (`gh repo create`) et le pousser ;
      - **relock ceq-tunisie** sur le cœur 2.0 (`>=1.0.4,<2` → `>=2,<3`) une fois 2.0 publié.
        **Analysé** : le code source de ceq-tunisie ne consomme que `CountryTaxBenefitSystem`
        (compat vérifiée : la réforme `CEQTunisiaReform` se construit sur le core 2.0 source).
        **Seul impact** : le test `tests/unit/test_openfisca_ceq_import.py::`
        `test_import_data_ceq_correspondence_natif` casse (le module `data_ceq_correspondence`
        a quitté le cœur → afrique-ouest) ; ce test (vestige de la migration Python 3.12) est
        à retirer/mettre à jour lors du relock. NB : `main` de ceq-tunisie a du WIP non commité
        — ne rien committer là-bas sans coordination ;
      - **transférer les issues** pays vers le dépôt études.
- [ ] **Dépôt études — finitions** (dans `../openfisca-ceq-afrique-ouest`) : imports des **notebooks**
      non réadaptés (data-gated) ; `survey_scenario.py:470` `CountryTaxBenefitSystem(coicop=False)`
      (argument `coicop` inexistant — legacy à corriger) ; pipeline complet non exécuté (enquêtes
      `.dta` + packages pays SN/ML/CI non disponibles).
- [ ] **Compléter les tests du cœur** : les deciles `decile_*_per_capita` (statistiques
      multi-ménages) et la valorisation des coûts unitaires d'éducation (`add_ceq_education_unit_cost`)
      ne sont pas encore couverts par des tests unitaires.
- [ ] **Doc `gross_income`** : divergence handbook CEQ vs implémentation Banque mondiale Tunisie
      (scénario PDI dégénéré, pens=0) — issue #80.

- [ ] **`.github/dependabot.yml` à dépoussiérer** (hors de portée du token agent → à faire à la main) :
      retirer le bloc `ignore: autopep8 1.5.5` (autopep8 abandonné au profit de ruff, PR #81) ;
      passer `package-ecosystem: pip` → `uv` (le dépôt n'a plus que `pyproject.toml` + `uv.lock`) ;
      envisager `interval: weekly` au lieu de `daily`.

## Fait récemment

- [x] **Scission phases 1–3 (local)** : dépôt `../openfisca-ceq-afrique-ouest` créé avec historique
      (`git filter-repo`, package renommé `openfisca_ceq_afrique_ouest`), scaffolding (pyproject,
      CI, README, AGPL), et code études **réadapté à l'API 2.0** (nouveau `tools/ceq_completion.py`
      délégant à `add_ceq_framework` ; imports intra-études renommés ; `country_code_by_country`
      local ; `education_unit_cost` découplé des assets du cœur). Import vérifié contre le vrai core 2.0.
- [x] **Cœur élagué (fin phase 2)** : retrait du générateur de comparaison multi-pays + assets
      `merged*` + doc `multi_country_comparison`, deps `xlwt`/`xlsxwriter` → `openpyxl`, README réécrit.
- [x] **Patch `ci.yml`** : deploy PyPI idempotent (`uv build`, retrait `uv pip install twine`,
      `twine upload --skip-existing`) — commité sur `scission-core`, **à pousser**.
- [x] **Scission phase 2 (branche `scission-core`)** : `add_ceq_framework` rendu agnostique du pays
      (données d'étude injectées en keyword-only) ; code études élagué (−21 972 lignes : notebooks,
      `tools/survey_scenario.py`, `tools/data/`, `tools/data_ceq_correspondence.py`, `tools/results/`,
      tests dépendants des données, assets `unit_cost_*`) ; table pays→code des taxes indirectes
      pilotée par la config `[ceq] country_codes` ; bump 2.0.0 + CHANGELOG de migration.
- [x] **Dépendances élaguées** (branche `scission-core`) : retrait de `matplotlib`, `scipy`, `xlrd`
      (runtime) et `papermill` (dev), inutiles après le départ des études ; `uv.lock` régénéré.
- [x] **Tests unitaires purs du cœur** (branche `scission-core`) : 5 fichiers YAML sans données —
      échelle complète des concepts de revenu (identités yc/yf), agrégateurs de composantes,
      agrégation personne→ménage, cas nul. Au passage, **bug de signe corrigé** dans
      `health_net_transfers` (in/out-patient additionnés, non retranchés — conforme au manuel
      CEQ, Lustig 2022) ; test dédié qui le verrouille.

- [x] Python ≥ 3.12 : pkg_resources → importlib (#78, PR #79, v1.0.3).
- [x] Packaging finalisé : MANIFEST.in supprimé, package-data explicite, twine verrouillé
      (PR #81, v1.0.4) ; chaîne de publication PyPI réparée (1.0.4 en ligne — la 1.0.3
      n'était jamais partie, deploy cassé par twine/packaging).
- [x] Revue obligatoire retirée de master (mainteneur solo ; les checks CI restent requis).
- [x] PRs dependabot apurées : #71 (flake8) et #73 (autopep8) fermées (outils remplacés par ruff,
      setup.py disparu) ; #77 mergée (certifi 2026.11.20, retrait racine emSign).
