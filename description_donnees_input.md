
# DESCRIPTION GENERALE PAR BASE / TABLE

Toutes les noms de variables, de toutes les bases doivent être les mêmes pour chaque pays. 
La construction des variaables par contre peut être spéficique à chaque pays, et doit être exlicitée dans les sections suivantes. 

## Base dépenses - échelle : ménage x produit

### variables structurelles 

* hh_id = identifiant du ménage
* prod_id = identifiant du type de produit acheté

### informations sur les dépenses

* prix (missing si pas dispo)
* quantite (missing si pas dispo) 
* depense = valeur dépensée (= prix X quantité - en théorie) - c'est la variable que l'on aura tout le temps, les deux autres, prix et quantité, ne sont malheureusement que rarement disponibles.

## Base revenus - échelle : par ménage x individus

### variables structurelles 

* hh_id
* pers_id 
* pond_m = pondération du ménage
* lien_cm = liens par rapport au chef du ménage 
* taille_m = nombre de personnes dans le ménage

### variables de revenus  

* rev_i_salaires_taxe = les revenus salariés taxés (ou bien on l'appelle rev_i_salaires_formel ?)
* rev_i_independants_taxe = les revenus des indépendants taxés
* rev_i_agricoles = tous les revenus de l'agriculture sauf ceux déjà comptés dans rev_i_salaires_taxe et rev_i_independants_taxe
* rev_i_independants_Ntaxe = tous ceux qui travaillent dans le secteur informel non agricole en tant qu'indépendant et ne sont pas taxés 
* rev_i_salarie_Ntaxe = tous ceux qui travaillent dans le secteur informel non agricole en tant que salarié et ne sont pas taxés 

Si l'on prend la différent formel/informel dans un sens plus large que juste la dichotomie taxé/non-taxé, mais au sens où le secteur formel est celui de la contractualisation, de la loi etc ... alors parmis les 5 catégorie de revenus énumérées plus haut seul rev_i_salaires_taxe appartient au formel, le reste c'est de l'informel. 

* rev_i_autoconsommation
* rev_i_loyers_imputes
* rev_i_loyers
* rev_i_autres_transferts
* rev_i_autres_revenus_capital
* rev_i_pensions
* rev_i_transferts_publics

### covariables d'intérêt

* cov_i_*nom_de_la_covariable* = toutes les covariables individuelles
* cov_m_*nom_de_la_covariable* = toutes les covariables niveaux ménage 

## Table taux taxes indirectes - échelle : produits

* prod_id = identifiant du type de produit acheté
* nom_variable_format_wide = nom de la variable dans la de données stata initiale, en général le format est wide (une colonne par type de dépense) alors qu'ici tout est transposé en long. 
* nom_question = indice de ou des questions dans le questionnaire ayant permi de calculer la dépense
* label = Label du type de dépense tel qu'indiqué dans le questionnaire 
* categorie_coicop = label de la catégorie coicop
* code_coicop = code de la catégorie coicop
* taux_tva = taux tva appliqué pour ce type de bien (ex : 0.18)
* taux_importation = taux appliqué aux importations de ce type de bien
* taux_taxe_speciale_1 = taux appliqué aux bien de ce type, au titre d'une autre tax sur la conso
* taux_taxe_speciale_2 ...
* ...
* subvention ?

autre ?

# Construction des variables - SENEGAL - par ordre alphabéthique 

## Variables de revenu


| Nom de la variable 	| Définition 	| Question dans enquete 	|
|--------------------------	|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|-----------------------------------------------------------------	|
| rev_i_agricoles 	| Revenu agricole déclaré par ceux qui travaillent dans le sector agricole 	| e11a; e20==1 | e20==2 | e20==5; 	|
| rev_i_assurance_sante 	| Prestations d'assurance maladie dont l'individu a bénéficié 	| d5 	|
| rev_i_autoconsommation 	| Autoconsommation des produits agricoles, d'élevage et de la pêche. La variable est mesurée au niveau ménage 	| I8_1; I8_2; I8_3 	|
| rev_i_autres 	| C'est la somme des revenus hors emplois et transferts associé à des prestations de service (commissions/honoraires, location véhicule, autres revenus hors emploi/transfers) et des revenus des activités sécondaires 	| fr2a; fr1; e14b 	|
| rev_i_autres_transferts 	| Il s'agit de l'ensemble des transferts privés incluant transferts d'individus (migrants), entreprises, ONG 	| ftr2; ftr8; ftr7 	|
| rev_i_independants_Ntaxe 	| Revenu des indépendants non agricoles éligibles à l'impôt type CGU n'ayant pas versé d'impôt.  A combiner avec la variable secteur d'activité pour savoir à quel type de CGU le revenu est eligible 	| e11a; e20; e19; e12; e10; e24i_annuel==0 	|
| rev_i_independants_taxe 	| Revenu des indépendants non agricoles éligibles à l'impôt type CGU ayant versé un impôt.  A combiner avec la variable secteur d'activité pour savoir à quel type de CGU le revenu est eligible 	| e11a; e20; e19; e12; e10; e24i_annuel>0 & e24i_annuel!=. 	|
| rev_i_loyers 	| Revenu tiré de la location de maison, terrain et champ 	| fr2a;fr1==4 	|
| rev_i_loyers_imputes 	| Loyer imputé calculé par l'ANSD. Celui-ci étant mesuré au niveau ménage, la variable est dividsée par la taille du ménage 	|  	|
| rev_i_pension 	| Pension de retraite 	| fr2a;fr1==2 	|
| rev_i_salaires_formels 	| Salaires du secteur formel incluant administration, entreprise publique, Banques/assurances, organisations internationales/ ambassades, associations/ONG 	| e11a; e18a==1 | e18a==2 | e18a==3 | e18a==5 | e18a==6 | e18a==7 	|
| rev_i_salaires_informels 	| Tous les salaires du secteur non formel 	|  	|
| rev_i_transferts_publics 	| Bourse scolaire, pension d'invalidité, programme/projet d'assistance sociale 	| p2_*; fr2a 	|


## Covariables d'intérêt

| Nom_variable 	| Définition 	| Question_dans_enquete 	|
|-------------------------------	|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|-----------------------------------------------------------------------------------------------------------------------------	|
| cov_i_age 	| Age de l'individu 	|  	|
| cov_i_classe_frequente 	| Classe fréquentée au moment de l'enquête 	| c9 	|
| cov_i_enfant_charge 	| Nombre d'enfants à charge des individus vivant dans le ménage. Il s'agit des enfants biologiques de moins de 21 ans ou de ceux entre 21 et 25 ans mais qui sont étudiants 	| age; e7; b11; b12; b11; b9 	|
| cov_i_lien_cm 	| Lien de l'individu avec le chef de ménage 	| b2 	|
| cov_i_ponderation 	| Poids de l'individu dans la population 	| poids3_a 	|
| cov_i_region 	| Région de résidence 	|  	|
| cov_i_secteur_activite 	| Secteur d'activité de l'individu 	| e20; e12; e10; e9; e18a 	|
| cov_i_secteur_formel_informel 	| Le secteur formel regroupe les individus travaillant dans l'administration, grande entreprise, institution financière, association ou ceux affiliés au système de sécurité sociale (IPRES, CSS, FNR) ou lorsque l'indépendant déclare avoir versé un impôt. 	| e18a==1 | e18a==2 | e18a==3 | e18a==5 | e18a==6 | e18a==7 | e13_1==1 | e13_2==1 | e13_3==1 | e24i_annuel>0 & e24i_annuel!=. 	|
| cov_i_secteur_publique_prive 	| Dummy indiquant si l'individu travaille dans le publique. Publique est défini ici comme tous ceux qui travaillent dans l'administration. 	| e18a==1 	|
| cov_i_sexe 	| Sexe de l'individu 	|  	|
| cov_i_statut_emploi 	| Statut d'emploi de l'individu 	| cov_i_secteur_activite; e1; e3; e7 	|
| cov_i_statut_matrimonial 	| Statut matrimonial de l'individu 	| b4 	|
| cov_i_taille_menage 	| La taille du ménage 	|  	|
| cov_i_type_ecole 	| Dummy indiquant si l'individu fréquente l'école publique. 	| c10==1 	|
| cov_i_urbain_rural 	| Milieu de résidence (urbain/rural) 	|  	|
| hh_id 	| Identifiant du ménage 	| a07b;a08 	|
| pers_id 	| identifiant de l'individu 	| a07b;a08;numpers 	|


# Construction des variables - COTE D IVOIRE - par ordre alphabéthique



# Construction des variables - MALI - par ordre alphabéthique




