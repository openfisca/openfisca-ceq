# Brancher le cœur sur un pays

Le cœur est **agnostique du pays**. Pour l'utiliser, on greffe les variables de
concepts CEQ sur le système socio-fiscal d'un pays (p. ex. `openfisca-senegal`) via
`add_ceq_framework`, en injectant les données propres à l'étude.

## L'API `add_ceq_framework`

```python
from openfisca_senegal import CountryTaxBenefitSystem
from openfisca_ceq.tools.tax_benefit_system_ceq_completion import add_ceq_framework

tbs = CountryTaxBenefitSystem()
add_ceq_framework(
    tbs,
    harmonized_income_mapping=...,   # {nom_harmonisé: variable_pays}
    custom_variables=...,            # itérable de Variable (update_variable)
    extra_variables=...,             # variables d'enquête de l'étude (add/replace)
    education_unit_cost=...,         # {catégorie: coût} -> variables de coût unitaire
)
```

Tous les paramètres propres à une étude sont **keyword-only** et optionnels :

- `harmonized_income_mapping` : les valeurs absentes du TBS sont créées comme variables
  d'entrée `float` au niveau de la personne.
- `custom_variables` : appliquées via `update_variable` (variables harmonisées multi-pays).
- `extra_variables` : ajoutées, ou remplacées si déjà présentes (variables d'enquête).
- `education_unit_cost` : déclenche la génération des variables de coût unitaire
  d'éducation (`add_ceq_education_unit_cost`).

!!! note "Le cœur ne peut pas se greffer sur lui-même"
    `add_ceq_framework` refuse un TBS qui contient déjà les variables CEQ *calculées*.
    Il s'applique au système d'un **package pays**, pas au paquet CEQ lui-même.

## Exemples réels

- **[ceq-tunisie](https://github.com/openfisca/ceq-tunisie)** : premier consommateur
  moderne du cœur ; n'utilise que `CountryTaxBenefitSystem` + le framework.
- **[openfisca-ceq-afrique-ouest](https://github.com/openfisca/openfisca-ceq-afrique-ouest)** :
  câble les études Sénégal / Mali / Côte d'Ivoire via un module `ceq_framework` qui
  délègue à `add_ceq_framework` (mapping harmonisé, variables d'enquête, coûts d'éducation).
