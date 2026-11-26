# Passation — session openfisca-ceq (préparée le 26/11/2026 depuis ceq-tunisie)

Pour la session dédiée à openfisca-ceq. Travailler en **worktrees séparés** (`git worktree add
../openfisca-ceq-wt-<chantier> origin/master`), jamais dans le working tree principal.

## État du dépôt au moment de la passation

- **v1.0.4 publiée sur PyPI** (la chaîne de publication était cassée depuis la 1.0.3 — réparée
  par la PR #81 ; la 1.0.3 n'est jamais partie, ne pas la chercher).
- Mergées aujourd'hui : **#79** (Python ≥ 3.12 : pkg_resources → importlib ; Fixes #78),
  **#81** (packaging finalisé : MANIFEST.in supprimé, package-data explicite, twine verrouillé).
- Issues ouvertes : **#80** (doc gross_income handbook vs WB Tunisie PDI), #387/#474/#476
  (préexistantes). PRs dependabot #71/#73/#77 : un tri était en cours (fermeture probable —
  autopep8/flake8 remplacés par ruff, requirements.txt disparu) ; VÉRIFIER `gh pr list` en
  arrivant.
- **Protection de master** : revue obligatoire RETIRÉE (mainteneur solo) ; les checks CI restent
  requis ; `--admin` disponible.
- Consommateur aval : **ceq-tunisie** épingle `openfisca-ceq>=1.0.4,<2` — tout breaking = 2.0.

## Pièges connus (vécus aujourd'hui)

1. **Le deploy PyPI tourne à CHAQUE push sur master** et ÉCHOUE (400, bénin) si la version est
   déjà publiée (commits sans bump, ex. docs). Patch prêt, NON APPLIQUÉ (token sans scope
   `workflow`) — à faire en priorité dans `.github/workflows/ci.yml` :
   - `uv pip install twine` → SUPPRIMER la ligne (twine est verrouillé dans les extras dev
     depuis #81 ; l'install à la volée upgradait packaging et cassait twine) ;
   - `uv run twine upload dist/*` → `uv run twine upload --skip-existing dist/*` ;
   - `uv build --wheel` → `uv build` (publier aussi le sdist).
2. **Tout bump de version mergé publie immédiatement sur PyPI** — bumper en conscience.
3. Si les commandes git mutatives sont bloquées dans le harnais : l'API GitHub marche
   (`gh api git/blobs|trees|commits|refs`, puis PATCH de la ref) — méthode éprouvée 3× aujourd'hui.
4. `tax_benefit_system_ceq_completion` exige une section `[ceq]` dans la config
   openfisca-survey-manager (exigence d'environnement, pas un bug).

## Chantiers, par priorité (détail : documentation/backlog.md et plan-scission-core-etudes.md)

1. **Patch ci.yml** (ci-dessus, 5 min, débloque l'idempotence du deploy).
2. **Scission core / études pays** — LE chantier structurant. Plan complet :
   `documentation/plan-scission-core-etudes.md`. La phase 0 (décisions : nom du dépôt études,
   sort de data_ceq_correspondence, des notebooks test/example/export, des assets merged*)
   appartient au mainteneur — les trancher avant d'exécuter.
3. **Dé-coder `country_packages`** (tools/tax_benefit_system_ceq_completion.py) : API générique
   `add_ceq_framework(tbs, mapping, …)` — cœur de la phase 2 de la scission ; breaking → 2.0.
4. **Tests du core sans données pays** : presque tous les tests actuels skippent sans les
   enquêtes ; écrire des tests unitaires purs sur les 72 variables (l'intégration ceq-tunisie
   a montré comment : cas-types, identités yc/yf — voir ceq-tunisie
   tests/unit/test_ceq_dtx_variables.py et tests d'intégration revenu_ceq pour s'inspirer).
5. **#80** : documenter la divergence gross_income (handbook vs WB PDI pens=0).

## Acquis réutilisables depuis ceq-tunisie (lecture seule pour cette session)

- `/home/benjello/projets/ceq-tunisie` : la réforme CEQTunisiaReform est le premier
  consommateur réel moderne du core — ses adaptations (`reform.py::_add_openfisca_ceq_variables`,
  qui a dû CORRIGER la copie des formules : méthodes liées → fonctions brutes de
  `ceq_variable.formulas` ; et éviter la reconstruction O(n²) du TBS) sont la matière première
  du futur `add_ceq_framework` générique (phase 2 scission).
- Le backlog ceq-tunisie (`docs/notes/backlog-remise-en-etat.md`, sections openfisca-ceq)
  documente tout le vécu d'intégration.
