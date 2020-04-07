# Comparaison des systèmes socio-fiscaux de la Côte d'Ivorie, du Mali et du Sénégal

## Objectif

L'objectif poursuivi est la comparaison des différents systèmes socio-fiscaux de la Côte d'Ivorie, du Mali et du Sénégal. Il s'agira d'appliquer chaque systèmes à chacun pays et d'en mesurer l'impact selon différentes dimensions.

Afin d'avoir des résultats comparables, l'analyse se fera dans la cadre des concepts du [CEQ](../documentation/ceq.md).

Afin de pouvoir réaliser des simulations s'appuyant sur les données d'enquête disponibles pour les différents pays avec tous les systèmes sociaux-fiscaux, il est nécessaire de disposer de données homogénéisées qui respectent autant que possible les traitements différenciés des revenus par l'ensemble des systèmes socio-fiscaux.

## Homogénéisation des variables d'enquête

Les données d'enquête brutes sont utilisées pour construire des variables de revenus communes, des variables de produits et construire la légisaltion pertinente pour chaque pays selon une [procédure similaire](./description_donnees_input.md).

## Injection dans les variables d'entrée des modèles pays

### Variables communes aux pays

Les variables d'entrée communes retenues pour les modèles des différents pays sont les suivantes:

| Harmonized_variable          | Model variable              |
|:-----------------------------|:----------------------------|
| cov_i_cadre                  | cadre                       |
| cov_i_classe_frequente       | eleve_enseignement_niveau   |
| cov_i_lien_cm                | household_role_index        |
| cov_i_secteur_publique_prive | secteur_public              |
| cov_i_type_ecole             | eleve_enseignement_public   |
| hh_id                        | household_id                |
| pers_id                      | person_id                   |
| rev_i_agricoles              | revenu_agricole             |
| rev_i_autoconsommation       | autoconsumption             |
| rev_i_autres                 | other_income                |
| rev_i_autres_revenus_capital | autres_revenus_du_capital   |
| rev_i_autres_transferts      | gifts_sales_durables        |
| rev_i_independants           | revenu_non_salarie_total    |
| rev_i_independants_Ntaxe     | revenu_informel_non_salarie |
| rev_i_independants_taxe      | revenu_non_salarie          |
| rev_i_locatifs               | revenu_locatif              |
| rev_i_loyers_imputes         | imputed_rent                |
| rev_i_pensions               | pension_retraite            |
| rev_i_salaires_formels       | salaire                     |
| rev_i_salaires_informels     | revenu_informel_salarie     |
| rev_i_transferts_publics     | direct_transfers            |


## Agrégats CEQ communs après homogénéisation

L'homogénéisation de certaines variables de revenus nous permets de définir d'emblée les régles de calculs de certains concepts de revenus CEQ communes à l'ensemble des pays considérés.

- all_income_excluding_transfers

- nontaxable_income
