
# Description générale des bases et tables d'entrées

Les variables doivent être homogénéïsées entre les pays
Tous les noms de variables de toutes les bases dépenses, revenus et taxes indiretcets doivent être les mêmes pour chaque pays.
En revanche, la construction des variables peut être spéficique à chaque pays, comme cela est explicité dans les sections suivantes.

## Dépenses

### Variables structurelles

Les observations se font au niveau du ménage x produit et sont indexées par les variables suivantes:
* `hh_id`: identifiant du ménage
* `prod_id`: identifiant du type de produit acheté

### Variables

* `prix`: prix du produit (potetiellement manquante)
* `quantite`: quantité achetée (potetiellement manquante)
* `depense`: valeur monétaire de ma dépensé (= prix x quantité - en théorie) - c'est la variable que l'on aura tout le temps, les deux autres, prix et quantité, ne sont malheureusement que rarement disponibles.

## Revenus

### Variables structurelles

Les observations se font au niveau du ménage x individu et sont indexées par les variables suivantes:
* `hh_id`: identifiant du ménage
* `pers_id`: identifiant de l'individu

Les variables suivantes précisent les interactions:
* `lien_cm`: liens par rapport au chef du ménage
* `taille_m`: nombre de personnes dans le ménage

Les ménages sont pondérés:
* `pond_m`: pondération du ménage

### Variables de revenus

#### Concepts retenus et variables associées

* `rev_i_agricoles`: tous les revenus de l'agriculture sauf ceux déjà comptés dans rev_i_salaires_formels et rev_i_independants_taxe
* `rev_i_salaires_formels`: les revenus salariés du secteur formel
* `rev_i_salaires_informels`: tous ceux qui travaillent dans le secteur informel non agricole
* `rev_i_independants`: Ensemble des revenus indépendants. Cette variable est particulièrement pertinente dans le cas du Mali parce que nous n'avons pas l'information sur le paiement effectif des taxes sur les revenus des indépendants.
* `rev_i_independants_taxe`: les revenus des indépendants non agricole qui sont effectivement taxés.
* `rev_i_independants_Ntaxe`: tous ceux qui travaillent dans le secteur informel non agricole en tant qu'indépendant et ne sont pas taxés.

Si l'on prend la différence formel/informel dans un sens plus large que la seule dichotomie taxé/non-taxé, mais au sens où le secteur formel est celui de la contractualisation, de la loi etc ... alors parmis les 5 catégorie de revenus énumérées plus haut seul rev_i_salaires_taxe appartient au formel, le reste c'est de l'informel.

* `rev_i_autoconsommation`
* `rev_i_locatif_impute`
* `rev_i_locatif`
* `rev_i_autres_transferts`
* `rev_i_autres_revenus_capital`
* `rev_i_pensions`
* `rev_i_transferts_publics`

#### Revenus indisponibles par pays

* Mali
  - `rev_i_independants_taxe`
  - `rev_i_independants_Ntaxe`
  - `rev_i_locatif`
  - `rev_i_autres_revenus_capital`
  - `rev_i_pensions`
  - `rev_i_transferts_publics`

#### Entité auxquelles sont attribués les revenus

Quand elles sont disponibles les variables suivantes sont mesurées au niveau du ménage:
 - autoconsommation
 - loyer imputé
 - transferts publics

Les autres variables sont mesurées au niveau des individus.

### Covariables d'intérêt

* cov_i_*nom_de_la_covariable* = toutes les covariables individuelles
* cov_m_*nom_de_la_covariable* = toutes les covariables niveaux ménage

## Taxes indirectes

Les observations se font au niveau du produits sont indexées par les variables suivantes:
* `prod_id`: identifiant du type de produit acheté
* `nom_variable_format_wide`: nom de la variable dans la de données stata initiale, en général le format est wide (une colonne par type de dépense) alors qu'ici tout est transposé en long.
* `nom_question`: indice de ou des questions dans le questionnaire ayant permi de calculer la dépense
* `label`: Label du type de dépense tel qu'indiqué dans le questionnaire
* `categorie_coicop`: label de la catégorie coicop
* `code_coicop`: code de la catégorie coicop
* `taux_tva`: taux tva appliqué pour ce type de bien (ex : 0.18)
* `taux_importation`: taux appliqué aux importations de ce type de bien
* `taux_taxe_speciale_1`: taux appliqué aux bien de ce type, au titre d'une autre tax sur la conso
* `taux_taxe_speciale_2`:..
* ...
* subvention ?

# Construction des variables - SENEGAL - par ordre alphabéthique

## Variables de revenu

| Nom de la variable 	| Définition 	| Question dans l'enquete 	|
|--------------------------	|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|-----------------------------------------------------------------	|
| rev_i_agricoles 	| Revenu agricole déclaré par ceux qui travaillent dans le sector agricole 	| e11a; e20==1 ; e20==2 ; e20==5; 	|
| rev_i_autoconsommation 	| Autoconsommation des produits agricoles, d'élevage et de la pêche. La variable est mesurée au niveau ménage. Mais on a divisé par la taille du ménage. 	| I8_1; I8_2; I8_3 	|
| rev_i_autres 	| C'est la somme des revenus hors emplois et transferts associé à des prestations de service (commissions/honoraires, location véhicule, autres revenus hors emploi/transfers), des revenus des activités sécondaires ainsi que des revenus d'assurance 	| fr2a; fr1; e14b 	|
| rev_i_autres_transferts 	| Il s'agit de l'ensemble des transferts privés incluant transferts d'individus (migrants), entreprises, ONG, etc. 	| ftr2; ftr8; ftr7 	|
| rev_i_independants_Ntaxe 	| Revenu des indépendants non agricoles éligibles à l'impôt type CGU n'ayant pas versé d'impôt.  A combiner avec la variable secteur d'activité pour savoir à quel type de CGU le revenu est eligible 	| e11a; e20; e19; e12; e10; e24i_annuel==0 	|
| rev_i_independants_taxe 	| Revenu des indépendants non agricoles éligibles à l'impôt type CGU ayant versé un impôt.  A combiner avec la variable secteur d'activité pour savoir à quel type de CGU le revenu est eligible 	| e11a; e20; e19; e12; e10; e24i_annuel>0 & e24i_annuel!=. 	|
| rev_i_locatif 	| Revenu tiré de la location de maison, terrain et champ 	| fr2a;fr1==4 	|
| rev_i_locatif_impute 	| Loyer imputé calculé par l'ANSD. Celui-ci étant mesuré au niveau ménage, la variable est divisée par la taille du ménage 	|  	|
| rev_i_pension 	| Pension de retraite 	| fr2a;fr1==2 	|
| rev_i_salaires_formels 	| Salaires du secteur formel incluant administration, entreprise publique, Banques/assurances, organisations internationales/ ambassades, associations/ONG 	| e11a; e18a==1 ; e18a==2 ; e18a==3 ; e18a==5 ; e18a==6 ; e18a==7 	|
| rev_i_salaires_informels 	| Tous les salaires du secteur non formel 	|  	|
| rev_i_transferts_publics 	| Bourse scolaire, pension d'invalidité, programme/projet d'assistance sociale. La variable est mesurée au niveau ménage. Mais on a divisé par la taille du ménage. 	| p2_*; fr2a 	|


## Covariables d'intérêt et variables structurels

| Nom_variable 	| Définition 	| Question_dans_enquete 	|
|-------------------------------	|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|-----------------------------------------------------------------------------------------------------------------------------	|
| cov_i_age 	| Age de l'individu 	|  	|
| cov_i_classe_frequente 	| Classe fréquentée au moment de l'enquête. | c9 	|
| cov_i_enfant_charge 	| Nombre d'enfants à charge des individus vivant dans le ménage. Il s'agit des enfants biologiques de moins de 21 ans ou de ceux entre 21 et 25 ans mais qui sont étudiants 	| age; e7; b11; b12; b11; b9 	|
| cov_i_region 	| Région de résidence 	|  	|
| cov_i_secteur_activite 	| Secteur d'activité de l'individu. Cette variable permet de distinguer les travailleurs agricoles, les salariés ainsi que les différents types d'indépendants (BIC, BNC) 	| e20; e12; e10; e9; e18a 	|
| cov_i_secteur_formel_informel 	| Le secteur formel regroupe les individus travaillant dans l'administration, grande entreprise, institution financière, association ou ceux affiliés au système de sécurité sociale (IPRES, CSS, FNR). 	| e18a==1 ; e18a==2 ; e18a==3 ; e18a==5 ; e18a==6 ; e18a==7 ; e13_1==1 ; e13_2==1 ; e13_3==1  	|
| cov_i_secteur_publique_prive 	| Dummy indiquant si l'individu travaille dans le publique. Publique est défini ici comme tous ceux qui travaillent dans l'administration. 	| e18a==1 	|
| cov_i_sexe 	| Sexe de l'individu 	|  	|
| cov_i_statut_matrimonial 	| Statut matrimonial de l'individu 	| b4 	|
|cov_i_taxe_Ntaxe| Dummy indiquant si l'indépendant a versé un impôt| e24i_annuel>0 & e24i_annuel!=.|
| cov_i_type_ecole 	| Dummy indiquant si l'individu fréquente l'école publique. 	| c10==1 	|
| cov_i_urbain_rural 	| Milieu de résidence (urbain/rural) 	|  	|
| cov_i_lien_cm 	| Lien de l'individu avec le chef de ménage 	| b2 	|
| cov_m_taille 	| La taille du ménage 	|  	|
| hh_id 	| Identifiant du ménage 	| a07b;a08 	|
| pers_id 	| identifiant de l'individu 	| a07b;a08;numpers 	|
| pond_i 	| Poids de l'individu dans la population 	| poids3_a 	|


## Label code des covariables d'intérêt et variables structurels

| cov_i_classe_frequente 	|  	|
|-------------------------------	|------	|
| Libelle 	| Code 	|
| Maternelle 	| 1 	|
| CI 	| 2 	|
| CP 	| 3 	|
| CE1 	| 4 	|
| CE2 	| 5 	|
| CM1 	| 6 	|
| CM2 	| 7 	|
| 6eme 	| 8 	|
| 5eme 	| 9 	|
| 4eme 	| 10 	|
| 3eme 	| 11 	|
| 2nde 	| 12 	|
| 1ere 	| 13 	|
| TERMINALE 	| 14 	|
| SUPERIEUR 1ere ANNEE 	| 15 	|
| SUPERIEUR 2eme ANNEE 	| 16 	|
| SUPERIEUR 3eme ANNEE 	| 17 	|
| SUPERIEUR 4eme ANNEE 	| 18 	|
| SUPERIEUR 5eme ANNEE 	| 19 	|
| SUPERIEUR 6 et + 	| 20 	|
| Ne sait pas 	| 99 	|


| cov_i_secteur_activite 	|  	|
|-------------------------------	|------	|
| Libelle 	| Code 	|
| actif agricole 	| 0 	|
| sal/dep formel 	| 1 	|
| sal/dep informel 	| 2 	|
| CGU comm/prod A 	| 3 	|
| CGU comm/prod B 	| 4 	|
| CGU services 	| 5 	|
| indep BNC (prof lib) 	| 6 	|


| cov_i_secteur_formel_informel 	|  	|
|-------------------------------	|------	|
| Libelle 	| Code 	|
| Formel 	| 1 	|
| Informel 	| 0 	|


| cov_i_secteur_publique_prive 	|  	|
|-------------------------------	|------	|
| Libelle 	| Code 	|
| Public 	| 1 	|
| Prive 	| 0 	|


| cov_i_sexe 	|  	|
|-------------------------------	|------	|
| Libelle 	| Code 	|
| Masculin 	| 1 	|
| Feminin 	| 2 	|

| cov_i_statut_matrimonial 	|  	|
|-------------------------------	|------	|
| Libelle 	| Code 	|
| Marié 	| 1 	|
| Célibataire 	| 2 	|
| Veuf/divorcé 	| 3 	|
| Non concerné 	| 4 	|


| cov_i_type_ecole 	|  	|
|-------------------------------	|------	|
| Libelle 	| Code 	|
| Public 	| 1 	|
| Prive 	| 0 	|

| lien_cm 	|  	|
|-----------------------------------	|------	|
| Libelle 	| Code 	|
| Chef du menage 	| 1 	|
| Conjoint du CM 	| 2 	|
| Enfant du chef/conjoint du CM 	| 3 	|
| Pere/mere du CM/conjoint du CM 	| 4 	|
| Autre parent du CM/conjoint du CM 	| 5 	|
| Autres personnes non apparentees 	| 6 	|
| Domestique 	| 7 	|

# Construction des variables - COTE D IVOIRE - par ordre alphabéthique

# Construction des variables - MALI - par ordre alphabéthique

## Variables de revenu 

| Nom de la variable 	| Définition 	| Question dans l'enquete 	|
|--------------------------	|---------------------------------------------------------------------------------------------------------------------------------------------------------	|-----------------------------------------------------------------------------------------------------------------------------	|
| rev_i_agricoles 	| Revenu agricole déclaré par ceux qui travaillent dans le sector agricole 	| w27; w15==11 ; w15==12 ; w15==13 ; w15==14 ; w15==15 ; w15==16 ; w15==21 ;  w15==22 ; w15==23 ; w15==50 	|
| rev_i_autoconsommation 	| Autoconsommation des produits agricoles, d'élevage et de la pêche. La variable est mesurée au niveau ménage. Mais on a divisé par la taille du ménage.  	| V10;V11 	|
| rev_i_autres 	| Cette catégorie de revenu inclut uniquement les revenus tirés des activités secondaires. 	| w35 	|
|rev_i_autres_revenus_capital| Pas d'informations dans l'enquête 	|  	|
| rev_i_autres_transferts 	| Il s'agit de l'ensemble des transferts des migrants. La variable est mesurée au niveau ménage. Elle a été divisée par la taille du ménage. 	| MT5	|
|rev_i_transferts_publics | Pas d'informations dans l'enquête 	|  	|
| rev_i_independants 	| Ensemble des revenu des indépendants non agricoles. 	| w27; cov_i_secteur_activite>=3 & cov_i_secteur_activite<=6 	|
| rev_i_independants_Ntaxe 	| Pas d'informations dans l'enquête sur le prelevement effectif des taxes 	|  	|
| rev_i_independants_taxe 	| Pas d'informations dans l'enquête sur le prelevement effectif des taxes 	|  	|
| rev_i_locatif 	| Pas d'informations dans l'enquête 	|  	|
| rev_i_locatif_impute	| Loyer imputé prédit à partir d'un modèle OLS exploitant les informations relatives aux caractéristiques du logement. On a divisé par la taille du ménage.  	| conso_hl; nbr_piece_log; nature_toit; nature_mure; nature_sol; evac_eaux; aisance; approv_eau; conso_hl_tet; Milieu; region 	|
| rev_i_pension 	| Pas d'informations dans l'enquête 	|  	|
| rev_i_salaires_formels 	| Salaires du secteur formel incluant administration, entreprise publique, entre prive/ ONG enregistrés à l'institut nationa de prevoyance sociale (INPS) 	| w27; ((w17==1 ; w17==2 ; w17==3 ; w17==4) & w18b==1) ; w26==1 & ( w16>=1 & w16<=5) ; w16==9 ; w16==8 ; w24==1 	|

## Covariables et variables structurelles

| Nom de la variable 	| Définition 	| Question dans l'enquete 	|
|-------------------------------	|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|-------------------------------------------------	|
| cov_i_age 	| Age de l'individu 	| m4 	|
| cov_i_classe_frequente 	| Classe fréquentée au moment de l'enquête 	| E6 	|
| cov_i_enfant_charge 	| Nombre d'enfants à charge du chef de ménage ou du conjoint. Il s'agit des enfants biologiques de moins de 21 ans ou de ceux entre 21 et 25 ans mais qui sont étudiants 	| m4<=21 & m5==3; w11==7 & m4>21 & m4<=25 & m5==3 	|
| cov_i_lien_cm 	| Lien de l'individu avec le chef de ménage 	| m5 	|
| cov_i_ponderation 	| Poids de l'individu dans la population 	| weight_pc 	|
| cov_i_secteur_activite 	| Secteur d'activité de l'individu 	|  	|
| cov_i_secteur_formel_informel 	| Le secteur formel regroupe les individus travaillant dans l'administration publique, entreprise publique ou parapublique,entreprise privée,entreprise associative et dont les entreprises sont enregistrées à l'INPS ou les individus ayant un bulletin de salaire 	| ((w17==1 ; w17==2 ; w17==3 ; w17==4) & w18b==1) ; w26==1 	|
| cov_i_secteur_publique_prive 	| Dummy indiquant si l'individu travaille dans le publique. Publique est défini ici comme tous ceux qui travaillent dans l'administration. 	| w17==1 	|
| cov_i_sexe 	| Sexe de l'individu 	| m3 	|
| cov_i_statut_matrimonial 	| Statut matrimonial de l'individu 	|  	|
| cov_i_taxe_Ntaxe 	| Pas d'informations dans l'enquête sur le prelevement effectif des taxes 	|  	|
| cov_i_type_ecole 	| Pas d'informations dans l'enquête 	|  	|
| cov_m_region 	| Région de résidence 	|  	|
| cov_m_taille 	| La taille du ménage 	|  	|
| cov_m_urbain_rural 	| Milieu de résidence (urbain/rural) 	|  	|
| hh_id 	| Identifiant du ménage 	|  	|
| pers_id 	| identifiant de l'individu 	|  	|

## Labels code des variables d'intérêt et variables structurelles


| cov_i_classe_frequente 	|  	|
|-----------------------------------	|------	|
| Libelle 	| Code 	|
| Maternelle 	| 0 	|
| 1ere annee 	| 1 	|
| 2eme annee 	| 2 	|
| 3eme annee 	| 3 	|
| 4eme annee 	| 4 	|
| 5eme annee 	| 5 	|
| 6eme annee 	| 6 	|
| 7eme annee 	| 7 	|
| 8eme annee 	| 8 	|
| 9eme annee 	| 9 	|
| Secondaire 	| 10 	|
| Superieur 	| 11 	|

| cov_i_secteur_activite 	|  	|
|-----------------------------------	|------	|
| Libelle 	| Code 	|
| actif agricole 	| 0 	|
| sal/dep formel 	| 1 	|
| sal/dep informel 	| 2 	|
| CGU comm/prod A 	| 3 	|
| CGU comm/prod B 	| 4 	|
| CGU services 	| 5 	|
| indep BNC (prof lib) 	| 6 	|

| cov_i_secteur_formel_informel 	|  	|
|-----------------------------------	|------	|
| Libelle 	| Code 	|
| Formel 	| 1 	|
| Informel 	| 0 	|

| cov_i_sexe 	|  	|
|-----------------------------------	|------	|
| Libelle 	| Code 	|
| Masculin 	| 1 	|
| Feminin 	| 2 	|

| cov_i_statut_matrimonial 	|  	|
|-----------------------------------	|------	|
| Libelle 	| Code 	|
| Marie monogame 	| 1 	|
| Marie polygame 	| 2 	|
| Union libre 	| 3 	|
| Celibataire (jamais marie) 	| 4 	|
| Divorce/separe 	| 5 	|
| Veuf(ve) 	| 6 	|
| Personnes de moins de 15 ans 	| 7 	|

| lien_cm 	|  	|
|-----------------------------------	|------	|
| Libelle 	| Code 	|
| Chef du menage 	| 1 	|
| Conjoint du CM 	| 2 	|
| Enfant du chef/conjoint du CM 	| 3 	|
| Pere/mere du CM/conjoint du CM 	| 4 	|
| Autre parent du CM/conjoint du CM 	| 5 	|
| Autres personnes non apparentees 	| 6 	|
| Domestique 	| 7 	|
