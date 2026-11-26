# Plan de documentation MkDocs — écosystème CEQ / OpenFisca

> Établi lors de la scission cœur / études (openfisca-ceq 2.0). Chapeaute tous les
> dépôts de l'écosystème CEQ. Suivi dans les backlogs respectifs.

## Objectif

Une **convention de documentation unique**, versionnée avec le code, publiée en site
statique sur **GitHub Pages**, remplaçant les wikis (non versionnés, redondants).

## Convention commune (brique réutilisable dans chaque dépôt)

- **Outils** : `mkdocs`, `mkdocs-material`, `mkdocstrings[python]` (référence d'API
  auto-générée depuis les docstrings). Déclarés dans un extra `docs` de `pyproject.toml`.
- **Thème** : material, palette indigo, `navigation.tabs` + `navigation.sections`,
  `content.code.copy` ; extensions `admonition`, `pymdownx.details/superfences/tabbed`.
- **Arborescence `docs/`** : `index.md`, doc des concepts/variables, `usage.md`,
  `reference.md` (mkdocstrings), `changelog.md` (include du `CHANGELOG.md`).
- **CI** : un job `docs` identique — `mkdocs gh-deploy --force` sur push `master`
  (ou action Pages) → site `openfisca.github.io/<repo>`.
- **Docs internes** (backlog, passation, notes d'analyse) : **hors du `nav`** publié.
- **Hygiène** : `has_wiki=false`, `homepage` du repo → site Pages, liens croisés.

## Déclinaison par dépôt

1. **openfisca-ceq (cœur)** — site **hub** de l'écosystème :
   - `concepts.md` : échelle des concepts de revenu CEQ (yc/yf) — **source unique**,
     fusion de `documentation/ceq.md` et du wiki `Home.md` (doublons).
   - `usage.md` : brancher le cœur sur un pays via `add_ceq_framework(tbs, *, …)`,
     exemples ceq-tunisie et afrique-ouest.
   - `indirect-taxation.md` : générateur générique de nomenclature.
   - `reference.md` : API auto (mkdocstrings).
   - Liste et lie tous les dépôts consommateurs.

2. **ceq-tunisie** — *finir* l'existant (déjà sous MkDocs material) :
   déclarer les deps docs, ajouter le job CI + Pages, sortir les ~20 notes d'analyse
   du `nav` public (archive/interne), lien vers le hub.

3. **openfisca-ceq-afrique-ouest** — nouveau site :
   y **déplacer `description_donnees_input.md`** (depuis le cœur), description des
   données d'enquêtes, spécificités pays, notebooks (`mkdocs-jupyter`).

4. **openfisca-senegal / -mali / -cote-d-ivoire** — **README enrichi** (pas de site MkDocs ;
   ces packages sont minces) : barème, source légale, liste des variables/paramètres,
   « comment ce pays se branche sur CEQ » + lien vers le hub. Migrer d'abord le contenu
   utile du wiki. Démarrage : senegal (cloné localement) ; mali/CIV ensuite.

## Décisions actées

- Pays fins (SN/ML/CIV) : **README enrichi**, pas de site MkDocs dédié.
- Wikis : **migrer le contenu utile d'abord**, puis retirer (`has_wiki=false`) ;
  nettoyage/élagage autorisé du contenu obsolète.
- Le site du cœur sert de hub.
- Démarrage : cœur + tunisie + senegal + afrique-ouest ; mali/CIV ensuite.

## Ordre d'exécution

Branches dédiées `docs-mkdocs` par dépôt (indépendantes du chantier scission).
Le déploiement CI/Pages du cœur s'active après le merge de la 2.0.
