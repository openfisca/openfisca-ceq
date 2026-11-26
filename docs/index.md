# OpenFisca CEQ — le cœur réutilisable

[OpenFisca](https://openfisca.org/doc/) est un logiciel libre de micro-simulation.
Ce dépôt contient l'implémentation OpenFisca du cadre d'analyse
[Commitment to Equity (CEQ)](http://commitmentoequity.org).

Depuis la **version 2.0**, `openfisca-ceq` ne contient que le **cœur réutilisable** :

- les **entités** CEQ (ménage / personne) ;
- les **72 variables de concepts de revenu** CEQ (voir [Concepts de revenu](concepts.md)) ;
- un **framework agnostique du pays**, `add_ceq_framework`, pour greffer ces concepts
  sur le système socio-fiscal d'un pays (voir [Brancher le cœur sur un pays](usage.md)) ;
- un **générateur générique** de nomenclature de taxes indirectes
  (voir [Taxes indirectes](indirect-taxation.md)).

Il n'embarque plus aucune étude pays.

## L'écosystème CEQ

| Dépôt | Rôle |
|---|---|
| **[openfisca-ceq](https://github.com/openfisca/openfisca-ceq)** | Le cœur réutilisable (ce site). |
| [openfisca-ceq-afrique-ouest](https://github.com/openfisca/openfisca-ceq-afrique-ouest) | Études Côte d'Ivoire, Mali, Sénégal (consomme le cœur). |
| [ceq-tunisie](https://github.com/openfisca/ceq-tunisie) | Étude Tunisie (consomme le cœur). |
| [openfisca-senegal](https://github.com/openfisca/openfisca-senegal), [openfisca-mali](https://github.com/openfisca/openfisca-mali), [openfisca-cote-d-ivoire](https://github.com/openfisca/openfisca-cote-d-ivoire) | Systèmes socio-fiscaux pays. |

## Installation

Ce paquet requiert [Python ≥ 3.11](https://www.python.org/) et
[uv](https://github.com/astral-sh/uv).

```sh
uv sync --extra dev
```

Pour construire cette documentation localement :

```sh
uv sync --extra docs
uv run mkdocs serve
```
