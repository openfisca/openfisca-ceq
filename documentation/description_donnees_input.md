
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
* `cov_i_lien_cm`: liens par rapport au chef du ménage
* `cov_m_taille`: nombre de personnes dans le ménage

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

Si l'on prend la différence formel/informel dans un sens plus large que la seule dichotomie taxé/non-taxé, mais au sens où le secteur formel est celui de la contractualisation, de la loi etc ... alors parmis les 5 catégories de revenus énumérées plus haut seul rev_i_salaires_taxe appartient au formel, le reste c'est de l'informel.

* `rev_i_autoconsommation`
* `rev_i_loyers_imputes`
* `rev_i_locatifs`
* `rev_i_autres_transferts`
* `rev_i_autres_revenus_capital`
* `rev_i_pensions`
* `rev_i_transferts_publics`

#### Revenus indisponibles par pays

* Mali
  - `rev_i_independants_taxe`
  - `rev_i_independants_Ntaxe`
  - `rev_i_locatifs`
  - `rev_i_autres_revenus_capital`
  - `rev_i_pensions`
  - `rev_i_transferts_publics`

#### Entité auxquelles sont attribués les revenus

Quand elles sont disponibles les variables suivantes sont mesurées au niveau du ménage:
 - autoconsommation
 - loyer imputé
 - transferts publics
 - autres transferts dans le cas du Mali

Les autres variables sont mesurées au niveau des individus.

### Autre covariables d'intérêt

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
* `tva`: taux tva appliqué pour ce type de bien (ex : `taux_normal`, `taux_reduit`)
* `douanes`: taux appliqué aux importations de ce type de bien
* `taux_taxe_speciale_1`: taux appliqué aux bien de ce type, au titre d'une autre tax sur la conso
* `taux_taxe_speciale_2`:..
* ...
* subvention ?

# Construction des variables - SENEGAL - par ordre alphabéthique

## Variables de revenu

| Nom de la variable 	| Définition 	| Question dans l'enquete 	|
|--------------------------	|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|-----------------------------------------------------------------	|
| rev_i_agricoles 	| Revenu agricole déclaré par ceux qui travaillent dans le sector agricole. On pose la question à chaque individu dans le mébage. 	| e11a; e20==1 ; e20==2 ; e20==5; 	|
| rev_i_autoconsommation 	| Autoconsommation des produits agricoles, d'élevage et de la pêche. La variable est mesurée au niveau ménage. Mais on a divisé par la taille du ménage. 	| I8_1; I8_2; I8_3 	|
| rev_i_autres 	| C'est la somme des revenus hors emplois et transferts associé à des prestations de service (commissions/honoraires, location véhicule, autres revenus hors emploi/transfers), des revenus des activités sécondaires ainsi que des revenus d'assurance 	| fr2a; fr1; e14b 	|
| rev_i_autres_transferts 	| Il s'agit de l'ensemble des transferts privés incluant transferts d'individus (migrants), entreprises, ONG, etc. 	| ftr2; ftr8; ftr7 	|
| rev_i_independants_Ntaxe 	| Revenu des indépendants non agricoles éligibles à l'impôt type CGU n'ayant pas versé d'impôt.  A combiner avec la variable secteur d'activité pour savoir à quel type de CGU le revenu est eligible 	| e11a; e20; e19; e12; e10; e24i_annuel==0 	|
| rev_i_independants_taxe 	| Revenu des indépendants non agricoles éligibles à l'impôt type CGU ayant versé un impôt.  A combiner avec la variable secteur d'activité pour savoir à quel type de CGU le revenu est eligible 	| e11a; e20; e19; e12; e10; e24i_annuel>0 & e24i_annuel!=. 	|
| rev_i_locatifs 	| Revenu tiré de la location de maison, terrain et champ 	| fr2a;fr1==4 	|
| rev_i_loyers_imputes 	| Loyer imputé calculé par l'ANSD. Celui-ci étant mesuré au niveau ménage, la variable est divisée par la taille du ménage 	|  	|
| rev_i_pension 	| Pension de retraite 	| fr2a;fr1==2 	|
| rev_i_salaires_formels 	| Salaires du secteur formel incluant administration, entreprise publique, Banques/assurances, organisations internationales/ ambassades, associations/ONG 	| e11a; e18a==1 ; e18a==2 ; e18a==3 ; e18a==5 ; e18a==6 ; e18a==7 	|
| rev_i_salaires_informels 	| Tous les salaires du secteur non formel 	|  	|
| rev_i_transferts_publics 	| Bourse scolaire, pension d'invalidité, programme/projet d'assistance sociale. La variable est mesurée au niveau ménage. Mais on a divisé par la taille du ménage. 	| p2_*; fr2a 	|

## Variables de consommation

La variable cov_m_conso est la somme des postes de consommation ci-dessous. Elle a été divisée par la taille du ménage afin de rester cohérent avec les variables revenus mesurés niveau ménage rapportées à la taille du ménage.

| Libellé postes TES 	| Période de reférence dans l'enquête 	| Méthode d'annualisation 	|
|-----------------------------------------	|-------------------------------------	|--------------------------------------------------------	|
| Education et formation 	| Année scolaire 2009-2010 	| Pas besoin 	|
| Produits édités et imprimés 	| Année scolaire 2009-2010 	| Pas besoin 	|
| Services de santé humaine 	| 12 derniers mois 	| Pas besoin 	|
| Produits pharmaceutiques 	| 12 derniers mois 	| Pas besoin 	|
| Mil-sorgho 	| 7 derniers jours 	| ANSD 	|
| Maïs 	| 7 derniers jours 	| ANSD 	|
| Fonio 	| 7 derniers jours 	| ANSD 	|
| Farine de mil et Sorgho 	| 7 derniers jours 	| ANSD 	|
| Riz décortiqué 	| 7 derniers jours 	| ANSD 	|
| Riz paddy 	| 7 derniers jours 	| ANSD 	|
| Arachide-coques 	| 7 derniers jours 	| ANSD 	|
| Huile de palme 	| 7 derniers jours 	| ANSD 	|
| Huile raffinée végétale (arachide, coto 	| 7 derniers jours 	| ANSD 	|
| Autres corps gras alimentaires , autres 	| 7 derniers jours 	| ANSD 	|
| Conserves de tomate 	| 7 derniers jours 	| ANSD 	|
| Tomates 	| 7 derniers jours 	| ANSD 	|
| Manioc 	| 7 derniers jours 	| ANSD 	|
| Légumes 	| 7 derniers jours 	| ANSD 	|
| Condiments et assaisonnement 	| 7 derniers jours 	| ANSD 	|
| Fruits 	| 7 derniers jours 	| ANSD 	|
| Bars et restaurants 	| 7 derniers jours 	| ANSD 	|
| Poisson frais 	| 7 derniers jours 	| ANSD 	|
| Poisson séché,salé et fûmé 	| 7 derniers jours 	| ANSD 	|
| Viandes 	| 7 derniers jours 	| ANSD 	|
| Ovins sur pied 	| 7 derniers jours 	| ANSD 	|
| Bovins sur pied 	| 7 derniers jours 	| ANSD 	|
| Volailles traditionnelles 	| 7 derniers jours 	| ANSD 	|
| Sucre 	| 7 derniers jours 	| ANSD 	|
| café et thé transformé 	| 7 derniers jours 	| ANSD 	|
| Plantes et fleurs 	| 7 derniers jours 	| ANSD 	|
| Eaux de table 	| 7 derniers jours 	| ANSD 	|
| Bière, autres boissons alcoolisées et m 	| 7 derniers jours 	| ANSD 	|
| Pain 	| 7 derniers jours 	| ANSD 	|
| Pâtisserie de conservation, biscuits 	| 7 derniers jours 	| ANSD 	|
| Produits laitiers 	| 7 derniers jours 	| ANSD 	|
| Produits d'entretien et glycérine 	| 30 derniers jours 	| ANSD 	|
| gaz 	| 30 derniers jours 	| ANSD 	|
| Charbon de bois 	| 30 derniers jours 	| ANSD 	|
| Bois en agrumes 	| 30 derniers jours 	| ANSD 	|
| Services immobiliers du logement 	| 30 derniers jours 	| ANSD 	|
| Bougies 	| 30 derniers jours 	| ANSD 	|
| Pétrole 	| 30 derniers jours 	| ANSD 	|
| Cigarettes 	| 30 derniers jours 	| ANSD 	|
| Autres services associatifs, récréatifs 	| 30 derniers jours 	| ANSD 	|
| Services domestiques 	| 30 derniers jours 	| ANSD 	|
| uniforme scolaire 	| 30 derniers jours 	| ANSD 	|
| Articles d'habillement 	| 30 derniers jours 	| ANSD 	|
| Tissus imprimés et teints 	| 30 derniers jours 	| ANSD 	|
| Chaussures 	| 30 derniers jours 	| ANSD 	|
| gasoil, essence ordinaire, super carbur 	| 30 derniers jours 	| ANSD 	|
| Services de transports de passagers 	| 30 derniers jours 	| ANSD 	|
| Réparation, entretien, modification de 	| 30 derniers jours 	| ANSD 	|
| Autres farines, céréales transformées, 	| 30 derniers jours 	| ANSD 	|
| Eau courante 	| 2 derniers mois 	| ANSD 	|
| Electricité, production et distribution 	| 2 derniers mois 	| ANSD 	|
| Assainissement voirie et gestion des dé 	| 12 derniers mois 	| Pas besoin 	|
| Services des réseaux de télécommunicati 	| 30 derniers jours 	| ANSD 	|
| Services d'accès aux réseaux de télécom 	| 30 derniers jours 	| ANSD 	|
| Sommiers et matelas 	| 12 derniers mois 	| Nombre d'acquisition (g3-g2) X prix d'acquisition (g5) 	|
| Equipements appareils radios, télévisio 	| 12 derniers mois 	| Nombre d'acquisition (g3-g2) X prix d'acquisition (g5) 	|
| Machines, appareils et matériels nca 	| 12 derniers mois 	| Nombre d'acquisition (g3-g2) X prix d'acquisition (g5) 	|
| Produits de métallurgie et de fonderie 	| 12 derniers mois 	| Nombre d'acquisition (g3-g2) X prix d'acquisition (g5) 	|
| Autres machines et appareils électrique 	| 12 derniers mois 	| Nombre d'acquisition (g3-g2) X prix d'acquisition (g5) 	|
| Autres mobiliers 	| 12 derniers mois 	| Nombre d'acquisition (g3-g2) X prix d'acquisition (g5) 	|
| Vélos et motocycles 	| 12 derniers mois 	| Nombre d'acquisition (g3-g2) X prix d'acquisition (g5) 	|
| Véhicules automobiles et remorques 	| 12 derniers mois 	| Nombre d'acquisition (g3-g2) X prix d'acquisition (g5) 	|
| parfums, produits de toilette 	| 30 derniers jours 	| ANSD 	|
| Boissons de fabrication traditionnelle 	| 30 derniers jours 	| ANSD 	|
| Entretien et réparation de machines, au 	| 30 derniers jours 	| ANSD 	|
| Auto conso agric 	| 12 derniers mois 	| ANSD 	|
| Auto conso élév 	| 12 derniers mois 	| ANSD 	|
| Auto conso peche 	| 12 derniers mois 	| ANSD 	|
| Achats et modification de parrures (bij 	| 12 derniers mois 	| ANSD 	|
| Loyer imputé 	| Pas d'info 	| Pas d'info 	|
| Transport éducation 	| année scolaire 2009-2010 	| Pas besoin 	|
| Transport santé 	| année scolaire 2009-2010 	| Pas besoin 	|
| Dépenses de construction de logement/Ac 	| 12 derniers mois 	| Pas besoin 	|
| Impôts. amendes. taxes contravention 	| 12 derniers mois 	| Pas besoin 	|
| Grosses réparations 	| 12 derniers mois 	| Pas besoin 	|
| Emballages métalliques 	| 12 derniers mois 	| Nombre d'acquisition (g3-g2) X prix d'acquisition (g5) 	|
| Epices et autres produits de l'agricult 	| 30 derniers jours 	| ANSD 	|
| Fauteuil, canapé 	| 12 derniers mois 	| Pas besoin 	|
| Articles de bonneterie et autres articl 	| 12 derniers mois 	| Pas besoin 	|
| Services de coiffure et autres soins de 	| 30 derniers jours 	| ANSD 	|
| Cérémonies, fetes 	| 12 derniers mois 	| Pas besoin 	|


## Covariables d'intérêt et variables structurelles

| Nom_variable 	| Définition 	| Question_dans_enquete 	|
|-------------------------------	|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|-----------------------------------------------------------------------------------------------------------------------------	|
| cov_i_age 	| Age de l'individu 	|  	|
| cov_i_cadre 	| Dummy prenant la valeur 1 pour les individus ayant comme catégorie socio-professionnelle est cadre supérieur, ingénieur, cadre moyen ou agent de maitrise et 2 pour les autres catégories	|  e12==1 ; e12==2	|
| cov_i_categorie_CGU| Cette variable est définie uniquement sur les indépendants. Elle permet de faire la distinction entre les indépendants entre les commerçants et revendeurs de ciments et de denrées alimentaires (CGU prod A) des autres commerçants ou revendeurs (CGU prod B) ou des prestataires de service (CGU service). Elle est particulièrement pertinente dans le cas du système socio-fiscal sénégalais. En lien avec les données de l'enquête, les indépendants CGU prod A incluent ceux dont la branche d'activité est les produits des industries alimentaires (Qe20). Ceux dont l'entreprise se trouvent dans la branche des services (hotelerie, transport, immobilier, informatique, education, etc) sont considérés comme indépendants CGU services (Qe20). Tous les autres indépendants qui ne sont pas dans les deux précédentes catégories sont dans CGU prod B (Qe20).| |
| cov_i_classe_frequente 	| Classe fréquentée au moment de l'enquête. | c9 	|
| cov_i_enfant_charge 	| Nombre d'enfants à charge des individus vivant dans le ménage. Il s'agit des enfants biologiques de moins de 21 ans ou de ceux entre 21 et 25 ans mais qui sont étudiants 	| age; e7; b11; b12; b11; b9 	|
| cov_i_lien_cm 	| Lien de l'individu avec le chef de ménage 	| b2 	|
| cov_i_no_mere| Numero d'ordre du pere au sein du ménage | b9 |
| cov_i_no_pere| Numero d'ordre du pere au sein du ménage | b10 |
| cov_i_secteur_activite 	| Secteur d'activité des individus âgés de plus de 15 ans. Cette variable permet de distinguer les actifs agricoles, les salariés du formel et de l'informel ainsi que les indépendants. Les actifs agricoles comprennent ceux dont l'entreprise est dans la branche des produits agricoles, sylvicoles, pêche et piscicultures (Qe20). Les salaries regroupent les cadres, employés, ouvriers, aides-familiaux, apprentis (Qe12) ou ceux qui déclarent percevoir un salaire (Qe10). Les indépendants sont les employeurs ou les travailleurs sous compte propre (Qe12).	| e20; e12; e10; e9; e18a 	|
| cov_i_secteur_calage | Secteur d'activité des individus, utilisé pour le calage. Il regroupe les secteurs agricoles, industriels et service. le secteur agricole comprend les individus dont l'entreprise est dans la branche des produits agricoles, sylvicoles, pêche et piscicultures. Le secteur industriel comprend les branches: charbonm hydrocarbure, minerais, textiles, raffinage, travaux de construction, machines, produits chimiques, etc. Celui des services inclus toutes les activités de ventes et de services.| e20; e19|
| cov_i_secteur_activite 	| Secteur d'activité des individus âgés de plus de 15 ans. Cette variable permet de distinguer les actifs agricoles, les salariés du formel et de l'informel ainsi que les indépendants. Les actifs agricoles comprennent ceux dont l'entreprise est dans la branche des produits agricoles, sylvicoles, pêche et piscicultures (Qe20). Les salaries regroupent les cadres, employés, ouvriers, aides-familiaux, apprentis (Qe12) ou ceux qui déclarent percevoir un salaire (Qe10). Les indépendants sont les employeurs ou les travailleurs sous compte propre (Qe12).	| e20; e12; e10; e9; e18a 	| 
| cov_i_secteur_activite 	| Secteur d'activité des individus âgés de plus de 15 ans. Cette variable permet de distinguer les actifs agricoles, les salariés du formel et de l'informel ainsi que les indépendants. Les actifs agricoles comprennent ceux dont l'entreprise est dans la branche des produits agricoles, sylvicoles, pêche et piscicultures (Qe20). Les salaries regroupent les cadres, employés, ouvriers, aides-familiaux, apprentis (Qe12) ou ceux qui déclarent percevoir un salaire (Qe10). Les indépendants sont les employeurs ou les travailleurs sous compte propre (Qe12).	| e20; e12; e10; e9; e18a 	|
| cov_i_secteur_publique_prive 	| Variable dichotomique égale à 1 lorsque l'individu est un salarié de l'administration publique, l'armée ou les forces de l'ordre. Elle prend la valeur 2 pour les salariés du privé affiliés à un système de sécurité sociale (IPRES, CSS, FNR, mutuelle de santé, ou autres). 	| e18a==1 ; e12<=5 ; e12==8 ; e12==9 ; e10==1; e13_1==1 ; e13_2==1 ; e13_3==1  ; e13_4==1 | e13_5==1	|
| cov_i_secteur_formel_informel 	| Il regroupe tous les salariés du secteur publique et les salariés du secteur privé formel. Ces derniers étant définis comme tous les salariés hors secteur publique affiliés à un système de sécurité sociale | 
| cov_i_sexe 	| Sexe de l'individu 	|  	|
| cov_i_statut_matrimonial 	| Statut matrimonial de l'individu 	| b4 	|
|cov_i_taxe_Ntaxe| Dummy indiquant si l'indépendant a versé un impôt| e24i_annuel>0 & e24i_annuel!=.|
| cov_i_type_ecole 	| Dummy indiquant si l'individu fréquente l'école publique. 	| c10==1 	|
| cov_i_urbain_rural 	| Milieu de résidence (urbain/rural) 	|  	|
| cov_m_region 	| Région de résidence 	|  	|
| cov_m_taille 	| La taille du ménage 	|  	|
| hh_id 	| Identifiant du ménage 	| a07b;a08 	|
| pers_id 	| identifiant de l'individu 	| a07b;a08;numpers 	|
| pond_i 	| Poids de l'individu dans la population 	| poids3_a 	|


## Label code des covariables d'intérêt et variables structurels
| cov_i_cadre 	|  	|
|-------------------------------	|------	|
| Libelle 	| Code 	|
| non-cadre 	| 1	|
| cadre	| 2 	|

| cov_i_categorie_CGU 	|  	|
|-------------------------------	|------	|
| Libelle 	| Code 	|
| CGU comm/prod A (agro-alimentaire et ciment) 	| 1	|
| CGU comm/prod B (autres produits) 	| 2 	|
| CGU service 	| 3 	|

| cov_i_classe_frequente 	|  	|
|-------------------------------	|------	|
| Libelle 	| Code 	|
| Maternelle 	| 1 	|
| Primaire 	| 2 	|
| Secondaire 	| 3 	|
| Superieur 	| 4 	|


| cov_i_secteur_activite 	|  	|
|-------------------------------	|------	|
| Libelle 	| Code 	|
| Actif agricole 	| 0 	|
| Salarie/dependant formel 	| 1 	|
| Salarie/dependant informel 	| 2 	|
| Independant	| 3 	|

| cov_i_secteur_formel_informel 	|  	|
|-------------------------------	|------	|
| Libelle 	| Code 	|
| Formel 	| 1 	|
| Informel 	| 0 	|

| cov_i_secteur_calage 	|  	|
|-------------------------------	|------	|
| Libelle 	| Code 	|
| agriculture 	| 1 	|
| industrie 	| 2 	|
| service 	| 3 	|

| cov_i_secteur_publique_prive 	|  	|
|-------------------------------	|------	|
| Libelle 	| Code 	|
| public 	| 1 	|
| prive 	| 2 	|


| cov_i_sexe 	|  	|
|-------------------------------	|------	|
| Libelle 	| Code 	|
| femme 	| 1 	|
| homme 	| 2 	|

| cov_i_statut_matrimonial 	|  	|
|-------------------------------	|------	|
| Libelle 	| Code 	|
| Marie 	| 1 	|
| Celibataire 	| 2 	|
| Veuf, Divorcé 	| 3 	|
| Non concerné 	| 4 	|


| cov_i_type_ecole 	|  	|
|-------------------------------	|------	|
| Libelle 	| Code 	|
| public 	| 1 	|
| prive 	| 2 	|

| cov_i_lien_cm 	|  	|
|-----------------------------------	|------	|
| Libelle 	| Code 	|
| Chef du menage 	| 1 	|
| Conjoint du CM 	| 2 	|
| Enfant du chef/conjoint du CM 	| 3 	|
| Pere/mere du CM/conjoint du CM 	| 4 	|
| Autre parent du CM/conjoint du CM 	| 5 	|
| Autres personnes non apparentees 	| 6 	|
| Domestique 	| 7 	|

| cov_i_urbain_rural 	|  	|
|-------------------------------	|------	|
| Libelle 	| Code 	|
| urbain 	| 1	|
| rural	| 2 	|

# Construction des variables - COTE D IVOIRE - par ordre alphabéthique

## Variables de revenu 

Les revenus dits individualises sont mesurés dans l'enquêtes au niveau du ménage, mais on ici été individualisés, i.e divisés par le nombre de personnes dans le ménage. 

| nom variable (format wide)   | numero de la question         | Description - methode                                                                                                                                                                                                                 |
|------------------------------|-------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| rev_i_agricoles              | i1; i2; g15 ; g18 ; g21 ; g24 | partiellement individualise - revenu de l'activite principale si l'individu est agriculteur independant + des revenus résiduels, individualises, provenant de la vente de produits agricoles et d elevage                                                           |
| rev_i_autoconsommation       | section M                     | individualises - le menage valorise lui-meme la quantite consommee                                                                                                                                                                    |
| rev_i_autres_revenus_capital | i6                            | revenus sous forme d'interets ou de dividendes                                                                                                                                                                                        |
| rev_i_autres_transferts      | i8; i9; i10                   | revenus, monetaires ou non, recus d autres menages                                                                                                                                                                                       |
| rev_i_independants_Ntaxe     | i1;i2                         | revenus de l'activitee principale si l'individu est independant, non agricole, et NE paie PAS des impots                                                                                                                               |
| rev_i_independants_taxe      | i1;i2                         | revenus de l'activitee principale si l'individu est independant, non agricole, et paie des impots                                                                                                                                      |
| rev_i_locatifs                 | i5                            | revenus locatifs                                                                                                                                                                                                                      |
| rev_i_loyers_imputes         | NA                            | individualises - loyers imputes a partir de variables decrivant le type de l'habitation (connexion a l'electricite, eau courante, toilettes interieures, utilisation de charbon pour la cuisine, appartement), le milieu et la region |
| rev_i_pensions               | i4                            | revenu des pensions de retraite                                                                                                                                                                                                       |
| rev_i_salaires_formels       | i1; i2                        | revenu de l'activitee principale si l'individu travaille dans le secteur formel = cotise a la secu et/ou contrat ecrit                                                                                                                |
| rev_i_salaires_informels     | i1; i2;               | revenu de l'activitee principale si l'individu ne tombe dans aucune des autres categories                                                                        |
| rev_i_transferts_publics     | i7                            | revenus tires de programme d'aide du gouvernment, ambassades ou institutions                                                                                                                                                          |
| rev_i_autres     | i3 ; i11                           |  revenus de l activite secondaire + autres revenus non encore cites                                                                                                                                                          |

## Variables de consommation

la variable consommation est la somme de toutes ces variables :

| nom variable (format wide)     | identifiant du produit (format long) | numero de la question | Description                                                                                          |
|--------------------------------|--------------------------------------|-----------------------|------------------------------------------------------------------------------------------------------|
| exp_activite_peri_scolaires    | 1                                    | la8                   | Contribution activite peri-scolaire ou activite culturelle                                           |
| exp_administrations_scolaires  | 2                                    | la10                  | Depenses liees a l'etablissement des pieces administratives pour la scolarisation des enfants        |
| exp_allumette                  | 3                                    | lg8                   | Allumette                                                                                            |
| exp_ampoule                    | 4                                    | lg4                   | Ampoule ordinaire et neon                                                                            |
| exp_assurance_vignette         | 5                                    | lf6                   | Assurance vignette et visite technique                                                               |
| exp_autre_scolaires            | 6                                    | la11                  | Depenses scolaires autres non encore citees                                                          |
| exp_bus_taxi                   | 7                                    | lf1                   | Depenses de bus, gbaka, woro-woro, taxi et autres transports en commun                               |
| exp_carburant                  | 8                                    | lf2                   | Carburant                                                                                            |
| exp_cloth_autre                | 9                                    | lc9                   | Autres depenses d'habillement non encore citees                                                      |
| exp_cloth_chaussures           | 10                                   | lc6                   | Chaussures hommes, dammes et enfants                                                                 |
| exp_cloth_coiffure             | 11                                   | lc8                   | Coiffure, tresse, coupe de cheveux, foulars                                                          |
| exp_cloth_coutures             | 12                                   | lc5                   | Frais de couture hommes, dames et enfants                                                            |
| exp_cloth_enfants              | 13                                   | lc2                   | Habits des enfants (vetements, tenues de fete)                                                       |
| exp_cloth_femmes               | 14                                   | lc3                   | Habits des femmes (vetements, tenues de fetes, pagnes)                                               |
| exp_cloth_hommes               | 15                                   | lc4                   | Habits des hommes (chemises, pantalons, tissus)                                                      |
| exp_cloth_montre               | 16                                   | lc7                   | Montres et bijoux                                                                                    |
| exp_comb_autre                 | 17                                   | o18                   | depense pour le chauffage - autre                                                                    |
| exp_comb_bois                  | 18                                   | o18                   | bois pour le chauffage                                                                               |
| exp_comb_charbon               | 19                                   | o18                   | charbon pour le chauffage                                                                            |
| exp_comb_electricite           | 20                                   | o18                   | electricite pour le chauffage                                                                        |
| exp_comb_gaz                   | 21                                   | o18                   | gaz pour le chauffage                                                                                |
| exp_comb_petrole               | 22                                   | o18                   | petrole pour le chauffage                                                                            |
| exp_comm_cabine                | 23                                   | le1                   | Cabines telephoniques (fixe ou mobile)                                                               |
| exp_comm_carte_abonnements_tel | 24                                   | le2_le3               | Cartes prepayees ou abonnement telephone fixe ou mobile                                              |
| exp_comm_chaines_tele          | 25                                   | le6                   | Abonnement aux chaines de television etrangeres                                                      |
| exp_comm_internet              | 26                                   | le4                   | Cybercafe ou connexion domestiques a Internet                                                        |
| exp_comm_tel_autre             | 27                                   | le5                   | Autres depenses de telephonie (citelcarte, Kibaro)                                                   |
| exp_communication_autre        | 28                                   | le9                   | Depenses de communication non encore citees ou exceptionnelles                                       |
| exp_contributions_scolaires    | 29                                   | la9                   | Contribution COGES, APE                                                                              |
| exp_courriers                  | 30                                   | le8                   | Depenses de timbres et courriers divers                                                              |
| exp_droit_inscription          | 31                                   | la1_la2               | Droits et autres frais d'inscription et scolarite                                                    |
| exp_entretient_reparation      | 32                                   | lf3                   | Entretien et reparation de vehicule                                                                  |
| exp_fournitures_scolaires      | 33                                   | la3                   | Livres scolaires, cahiers et autres fournitures scolaires                                            |
| exp_health_accompagnant        | 34                                   | lb7                   | Frais de sejour et de transport des personnes accompagnant le malade                                 |
| exp_health_assurance_mal       | 35                                   | lb13                  | Depense d'assurance maladie                                                                          |
| exp_health_autre               | 36                                   | lb9                   | Depenses de sante non encore citees                                                                  |
| exp_health_consult             | 37                                   | lb5                   | Consultation d'un personnel de sante moderne et de vaccination                                       |
| exp_health_hopital             | 38                                   | lb6                   | Frais d'hospitalisation                                                                              |
| exp_health_medic_trad          | 39                                   | lb4                   | Medicaments traditionnels                                                                            |
| exp_health_produits_pharma     | 40                                   | lb3                   | Produits pharmaceutiques                                                                             |
| exp_health_trad_practicien     | 41                                   | lb8                   | Frais de consultation d'un guerisseur ou d'un tradi-praticien et depenses ordonnees par ces derniers |
| exp_hygn                       | 42                                   | lg1                   | Savons et papier hygienique                                                                          |
| exp_journaux                   | 43                                   | le7                   | Achats de journaux ou autre presse                                                                   |
| exp_light_electricite          | 44                                   | o16                   | electricite pour l'eclairage                                                                         |
| exp_light_huile                | 45                                   | o16                   | huile pour l'eclairage                                                                               |
| exp_light_petrole              | 46                                   | o16                   | petrole pour l'eclairage                                                                             |
| exp_loisirs                    | 47                                   | lg2a                  | Loisir (jeux, excursion, sport)                                                                      |
| exp_machette                   | 48                                   | lg7                   | Machette                                                                                             |
| exp_maid                       | 49                                   | lg3                   | Domestique                                                                                           |
| exp_nourritures_scolaires      | 50                                   | la6                   | Nourriture, cantine, internat, pensionat et tuteur                                                   |
| exp_parapluie                  | 51                                   | lg9                   | Parapluie                                                                                            |
| exp_piles                      | 52                                   | lg5                   | Pile                                                                                                 |
| exp_rasoire                    | 53                                   | lg10                  | Rasoir                                                                                               |
| exp_soutients_scolaires        | 54                                   | la7                   | Repetiteur, maitre de maison, cours de renforcement, cours de vacances                               |
| exp_tabac                      | 55                                   | lg2b                  | Tabac                                                                                                |
| exp_torche                     | 56                                   | lg6                   | Torche                                                                                               |
| exp_transf_alim_parents        | 57                                   | ld3                   | Valeur des envois de produits alimentaires aux parents et autres persoones                           |
| exp_transf_association         | 58                                   | ld8                   | Cotisations dans diverses associations                                                               |
| exp_transf_autre_aide          | 59                                   | ld5                   | Aides et soutiens non encore citees                                                                  |
| exp_transf_epouses             | 60                                   | ld2                   | Envois d'argent aux epouses                                                                          |
| exp_transf_funerails           | 61                                   | ld7                   | Depenses aux funerailles ou autres ceremonies                                                        |
| exp_transf_marriage            | 62                                   | ld6                   | Depenses pour les mariages et les baptemes                                                           |
| exp_transf_parents             | 63                                   | ld1                   | Envois d'argent aux parents et autres                                                                |
| exp_transf_parents_autre       | 64                                   | ld4c                  | Valeur des envois d'autres produits aux parents et autres personnes                                  |
| exp_transf_parents_education   | 65                                   | ld4b                  | Valeur des envois de produits d education aux parents et autres personnes                            |
| exp_transf_parents_sante       | 66                                   | ld4                   | Valeur des envois de produits de sante aux parents et autres personnes                               |
| exp_transport_exceptionnel     | 67                                   | lf5                   | Transport exceptionnel                                                                               |
| exp_transports_scolaires       | 68                                   | la5                   | Frais de transport des personnes qui vont a l'ecole                                                  |
| exp_uniformes_scolaires        | 69                                   | la4                   | Frais d'uniforme, de tenue de sport et autres habillements                                           |
| exp_voyage                     | 70                                   | lf4                   | Voyages                                                                                              |
| exp_waste                      | 71                                   | o22                   | Enlevement des ordures                                                                               |
| exp_water_autre                | 72                                   | o14                   | eau provenant d'autres sources                                                                       |
| exp_water_publique             | 73                                   | o14                   | eau via le reseau publique                                                                           |
| exp_rent                       | 74                                   | o3                    | loyers résidence principale                                                                          |
| exp_equipement                 | de 75 a 119                          | K                     | Achats d'equipement - voir liste                                                                     |
| exp_nourriture                 | de 120 a 246                         | M                     | depenses d'aliment                                                                                   |
| exp_light_autre                | 247                                  | o15                   | Eclairage de source diverse                                                                          |
| exp_nourriture_dons            | de 248 a 374                         | M                     | Consommation d'aliment produit donnes au menage                                                      |
| exp_autoconsommation           | de 375 a 401                         | M                     | Consommation d'aliment produit par le menage                                                         |

### liste des équipements 

| nom variable (format wide) | identifiant du produit (format long) | numero de la question | Description               |
|----------------------------|--------------------------------------|-----------------------|---------------------------|
| exp_equipement             | 75                                   | K1                    | Telephone portable        |
| exp_equipement             | 76                                   | K2                    | Telephone fixe            |
| exp_equipement             | 77                                   | K3                    | Television                |
| exp_equipement             | 78                                   | K4                    | Radio                     |
| exp_equipement             | 79                                   | K5                    | Lecteur VCD/DVD           |
| exp_equipement             | 80                                   | K6                    | Refrigerateur             |
| exp_equipement             | 81                                   | K7                    | Congelateur               |
| exp_equipement             | 82                                   | K8                    | Ventilateur               |
| exp_equipement             | 83                                   | K9                    | Climatiseur               |
| exp_equipement             | 84                                   | K10                   | Ordinateur                |
| exp_equipement             | 85                                   | K11                   | Cuisinière               |
| exp_equipement             | 86                                   | K12                   | Antenne parabolique       |
| exp_equipement             | 87                                   | K13                   | Voiture                   |
| exp_equipement             | 88                                   | K14                   | Camionnette               |
| exp_equipement             | 89                                   | K15                   | Bicyclette                |
| exp_equipement             | 90                                   | K16                   | Velomoteur                |
| exp_equipement             | 91                                   | K17                   | Tracteur                  |
| exp_equipement             | 92                                   | K18                   | Pirogue                   |
| exp_equipement             | 93                                   | K19                   | Charette                  |
| exp_equipement             | 94                                   | K20                   | Brouette                  |
| exp_equipement             | 95                                   | K21                   | Charrue                   |
| exp_equipement             | 96                                   | K22                   | Vaporisateur              |
| exp_equipement             | 97                                   | K23                   | Bateau de plaisance       |
| exp_equipement             | 98                                   | K24                   | Bateau de peche           |
| exp_equipement             | 99                                   | K25                   | Fer a repasser            |
| exp_equipement             | 100                                  | K26                   | Tablette                  |
| exp_equipement             | 101                                  | K27                   | Tondeuse a gazon          |
| exp_equipement             | 102                                  | K28                   | Machine a coudre          |
| exp_equipement             | 103                                  | K29                   | Velo pour enfant          |
| exp_equipement             | 104                                  | K30                   | Appareil photo numerique  |
| exp_equipement             | 105                                  | K31                   | Camera                    |
| exp_equipement             | 106                                  | K32                   | Chaine HIFI               |
| exp_equipement             | 107                                  | K33                   | Scie non electrique       |
| exp_equipement             | 108                                  | K34                   | Tondeuse electrique       |
| exp_equipement             | 109                                  | K35                   | Salle a manger            |
| exp_equipement             | 110                                  | K36                   | Salon ordinaire           |
| exp_equipement             | 111                                  | K37                   | Fautteuil a mousse (salon |
| exp_equipement             | 112                                  | K38                   | Table                     |
| exp_equipement             | 113                                  | K39                   | Chaise                    |
| exp_equipement             | 114                                  | K40                   | Lit                       |
| exp_equipement             | 115                                  | K41                   | Matelas                   |
| exp_equipement             | 116                                  | K42                   | Drap et couverture        |
| exp_equipement             | 117                                  | K43                   | Natte                     |
| exp_equipement             | 118                                  | K44                   | Sceau en plastique        |
| exp_equipement             | 119                                  | K45                   | Pilon et mortier          |

### liste des aliments 

| nom variable (format wide) | identifiant du produit (format long) | numero de la question | Description                |
|----------------------------|--------------------------------------|-----------------------|----------------------------|
| exp_nourriture             | 120                                  | M1                    | Riz local                  |
| exp_nourriture             | 121                                  | M2                    | Mais en epis               |
| exp_nourriture             | 122                                  | M3                    | Mais e, grain              |
| exp_nourriture             | 123                                  | M4                    | Farine de mais             |
| exp_nourriture             | 124                                  | M5                    | Mil en grain               |
| exp_nourriture             | 125                                  | M6                    | Farine de mil              |
| exp_nourriture             | 126                                  | M7                    | Sorgho en grain            |
| exp_nourriture             | 127                                  | M8                    | Farine de sorgho           |
| exp_nourriture             | 128                                  | M9                    | Fonio en grain             |
| exp_nourriture             | 129                                  | M10                   | Haricot vert               |
| exp_nourriture             | 130                                  | M11                   | Haricot sec                |
| exp_nourriture             | 131                                  | M12                   | Igname                     |
| exp_nourriture             | 132                                  | M13                   | Farine d'ignale            |
| exp_nourriture             | 133                                  | M14                   | Manioc fraix               |
| exp_nourriture             | 134                                  | M15                   | Attieke                    |
| exp_nourriture             | 135                                  | M16                   | Farine de manioc           |
| exp_nourriture             | 136                                  | M17                   | Pâte de manioc             |
| exp_nourriture             | 137                                  | M18                   | Gari                       |
| exp_nourriture             | 138                                  | M19                   | Taro                       |
| exp_nourriture             | 139                                  | M20                   | Patate douce               |
| exp_nourriture             | 140                                  | M21                   | Banane plantain            |
| exp_nourriture             | 141                                  | M22                   | Farine de banane           |
| exp_nourriture             | 142                                  | M23                   | Arachide decortiquee       |
| exp_nourriture             | 143                                  | M24                   | Pâte d'arachide            |
| exp_nourriture             | 144                                  | M25                   | Pistache                   |
| exp_nourriture             | 145                                  | M26                   | Persil                     |
| exp_nourriture             | 146                                  | M27                   | Pâte de pistache           |
| exp_nourriture             | 147                                  | M28                   | Nois de palme              |
| exp_nourriture             | 148                                  | M29                   | Huile de palm trad.        |
| exp_nourriture             | 149                                  | M30                   | Beurre de karite           |
| exp_nourriture             | 150                                  | M31                   | Tomate fraiche             |
| exp_nourriture             | 151                                  | M32                   | Aubergine locale           |
| exp_nourriture             | 152                                  | M33                   | Aubergine violet           |
| exp_nourriture             | 153                                  | M34                   | Gombo frais                |
| exp_nourriture             | 154                                  | M35                   | Gombo sec                  |
| exp_nourriture             | 155                                  | M36                   | Oignon                     |
| exp_nourriture             | 156                                  | M37                   | Piment                     |
| exp_nourriture             | 157                                  | M38                   | Carotte                    |
| exp_nourriture             | 158                                  | M39                   | Chou                       |
| exp_nourriture             | 159                                  | M40                   | Citrouille                 |
| exp_nourriture             | 160                                  | M41                   | Concombre                  |
| exp_nourriture             | 161                                  | M42                   | Courgette                  |
| exp_nourriture             | 162                                  | M43                   | Poivron                    |
| exp_nourriture             | 163                                  | M44                   | Salades divers             |
| exp_nourriture             | 164                                  | M45                   | feuille de manios          |
| exp_nourriture             | 165                                  | M46                   | Noix de cajou              |
| exp_nourriture             | 166                                  | M47                   | Epinard                    |
| exp_nourriture             | 167                                  | M48                   | Feuille de palme           |
| exp_nourriture             | 168                                  | M49                   | Kloila                     |
| exp_nourriture             | 169                                  | M50                   | Dah                        |
| exp_nourriture             | 170                                  | M51                   | Autres feuilles            |
| exp_nourriture             | 171                                  | M52                   | Ananas                     |
| exp_nourriture             | 172                                  | M53                   | Banane douce               |
| exp_nourriture             | 173                                  | M54                   | Orange                     |
| exp_nourriture             | 174                                  | M55                   | Mandarine                  |
| exp_nourriture             | 175                                  | M56                   | Pamplemousse               |
| exp_nourriture             | 176                                  | M57                   | Citron                     |
| exp_nourriture             | 177                                  | M58                   | Avocat                     |
| exp_nourriture             | 178                                  | M59                   | Mangue                     |
| exp_nourriture             | 179                                  | M60                   | Papaye                     |
| exp_nourriture             | 180                                  | M61                   | Gombo sec en poudre        |
| exp_nourriture             | 181                                  | M62                   | Viande de bœuf             |
| exp_nourriture             | 182                                  | M63                   | Viande de mouton           |
| exp_nourriture             | 183                                  | M64                   | Viande de porc             |
| exp_nourriture             | 184                                  | M65                   | Viande de volaille         |
| exp_nourriture             | 185                                  | M66                   | Abats                      |
| exp_nourriture             | 186                                  | M67                   | poisson frais Appolo       |
| exp_nourriture             | 187                                  | M68                   | Poisson fume Hareng        |
| exp_nourriture             | 188                                  | M69                   | Escargot                   |
| exp_nourriture             | 189                                  | M70                   | Viande de brousse          |
| exp_nourriture             | 190                                  | M71                   | Œuf                        |
| exp_nourriture             | 191                                  | M72                   | Lait frais                 |
| exp_nourriture             | 192                                  | M73                   | Miel                       |
| exp_nourriture             | 193                                  | M74                   | Boisson alc. Tradition     |
| exp_nourriture             | 194                                  | M75                   | Boisson non alc. Tradition |
| exp_nourriture             | 195                                  | M76                   | Fruit de la passion        |
| exp_nourriture             | 196                                  | M77                   | Gingembre                  |
| exp_nourriture             | 197                                  | M78                   | Amandes de karite          |
| exp_nourriture             | 198                                  | M79                   | Soja                       |
| exp_nourriture             | 199                                  | M80                   | Coprah                     |
| exp_nourriture             | 200                                  | M81                   | Tabac brut                 |
| exp_nourriture             | 201                                  | M82                   | Poisson frais capitaine    |
| exp_nourriture             | 202                                  | M83                   | Poisson frais sosso        |
| exp_nourriture             | 203                                  | M84                   | Poisson frais carpe rouge  |
| exp_nourriture             | 204                                  | M85                   | Machoiron fume             |
| exp_nourriture             | 205                                  | M86                   | Maquereau fume             |
| exp_nourriture             | 206                                  | M87                   | Crabes                     |
| exp_nourriture             | 207                                  | M88                   | Riz importe denicachia     |
| exp_nourriture             | 208                                  | M89                   | Riz importe de luxe        |
| exp_nourriture             | 209                                  | M90                   | Pain                       |
| exp_nourriture             | 210                                  | M91                   | Pate alimentaire           |
| exp_nourriture             | 211                                  | M92                   | farine de ble              |
| exp_nourriture             | 212                                  | M93                   | Ble                        |
| exp_nourriture             | 213                                  | M94                   | Biscuit et patisserie      |
| exp_nourriture             | 214                                  | M95                   | Lait en poudre             |
| exp_nourriture             | 215                                  | M96                   | Lait conc. Sucre           |
| exp_nourriture             | 216                                  | M97                   | Lait conc. Non sucre       |
| exp_nourriture             | 217                                  | M98                   | Yogourt                    |
| exp_nourriture             | 218                                  | M99                   | Beurre de karite           |
| exp_nourriture             | 219                                  | M100                  | Fromage                    |
| exp_nourriture             | 220                                  | M101                  | Crevettes                  |
| exp_nourriture             | 221                                  | M102                  | Bouillon cube              |
| exp_nourriture             | 222                                  | M103                  | Pate de tomate             |
| exp_nourriture             | 223                                  | M104                  | Sel                        |
| exp_nourriture             | 224                                  | M105                  | Huile raffinee             |
| exp_nourriture             | 225                                  | M106                  | Sucre                      |
| exp_nourriture             | 226                                  | M107                  | Cafe                       |
| exp_nourriture             | 227                                  | M108                  | Margarine                  |
| exp_nourriture             | 228                                  | M109                  | Chocolat a croquer         |
| exp_nourriture             | 229                                  | M110                  | The (sachet)               |
| exp_nourriture             | 230                                  | M111                  | Autres boisson alcoolisee  |
| exp_nourriture             | 231                                  | M112                  | Boisson non alcolisee      |
| exp_nourriture             | 232                                  | M113                  | Pomme de terre             |
| exp_nourriture             | 233                                  | M114                  | Boite de sardine           |
| exp_nourriture             | 234                                  | M115                  | Conserve de viande         |
| exp_nourriture             | 235                                  | M116                  | Conserve de fruit          |
| exp_nourriture             | 236                                  | M117                  | Mangue importee            |
| exp_nourriture             | 237                                  | M118                  | Plats emportes             |
| exp_nourriture             | 238                                  | M119                  | Plats exterieurs           |
| exp_nourriture             | 239                                  | M120                  | Champignon                 |
| exp_nourriture             | 240                                  | M121                  | Eau minerale               |
| exp_nourriture             | 241                                  | M122                  | Saucission                 |
| exp_nourriture             | 242                                  | M123                  | Cacao en poudre sucree     |
| exp_nourriture             | 243                                  | M124                  | Cafe soluble ou moulu      |
| exp_nourriture             | 244                                  | M125                  | Lait infantile             |
| exp_nourriture             | 245                                  | M126                  | Aliment pour bebe          |
| exp_nourriture             | 246                                  | M127                  | Biere                      |  


## Covariables et variables structurelles

| Nom de la variable            | Valeurs possibles                                   | Explications - Sources                                                                                                                                                            |
|-------------------------------|-----------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| cov_i_secteur_formel_informel | 1 / 0                                               | Sont considérés comme formels ceux qui déclarent côtiser à la caisse nationale de prévoyance sociale (eb12c) - informels tous les autres individus ayant une acctivité principale |

| cov_i_public_prive            | 1 / 0                                               | Variable définie à partir de l'activité principale (eb3b) - seulement pour le secteur formel                                                                                      |

| cov_i_secteur_activite        | formel / agricoles / independant / autres informels | Variable définie à partir de l'activité principale (eb3b)                                                                                                                         |

| cov_i_secteur_calage        | 1/2/3 - agriculture / industrie / service | Variable définie à partir de l'activité principale (eb3b), le lieu de travail (eb4) et la branche d'activité (eb2a_nombranchactiv)                                                                                                                        |

| cov_i_classe_frequente        | 1/2/3/4 - Maternelle/Primaire/Secondaire/Supérieur  | Classe frequentée lors de l'enquête (dq14)                                                                                                                                        |
| cov_i_type_ecole              | 1/0 - publique/privée                               | Qualité de l'établissement fréquenté lors de l'enquête  (dq15)                                                                                                                    |
| cov_i_sexe                    | 1/2 - Masculin/Féminin                              | a1                                                                                                                                                                                |
| cov_i_lien_cm                 | 1 à 7                                               | Lien de parent avec le chef de ménage (a2)                                                                                                                                        |
| cov_i_age                     | âge de l'individu                                   | a4aimput                                                                                                                                                                          |
| cov_m_enfant                  | nombre d'enfant <=15 ans dans le ménage             | a4aimput                                                                                                                                                                          |
| cov_i_no_mere| Numero d'ordre du pere au sein du ménage | a16 |
| cov_i_no_pere| Numero d'ordre du pere au sein du ménage | a19 |


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
| rev_i_locatifs 	| Pas d'informations dans l'enquête 	|  	|
| rev_i_loyers_imputes	| Loyer imputé prédit à partir d'un modèle OLS exploitant les informations relatives aux caractéristiques du logement. On a divisé par la taille du ménage.  	| conso_hl; nbr_piece_log; nature_toit; nature_mure; nature_sol; evac_eaux; aisance; approv_eau; conso_hl_tet; Milieu; region 	|
| rev_i_pension 	| Pas d'informations dans l'enquête 	|  	|
| rev_i_salaires_formels 	| Salaires du secteur formel incluant administration, entreprise publique, entre prive/ ONG enregistrés à l'institut nationa de prevoyance sociale (INPS) 	| w27; ((w17==1 ; w17==2 ; w17==3 ; w17==4) & w18b==1) ; w26==1 & ( w16>=1 & w16<=5) ; w16==9 ; w16==8 ; w24==1 	|

## Variables de consommation

La variable cov_m_conso est la somme des postes de consommation ci-dessous. Elle a été divisée par la taille du ménage afin de rester cohérent avec les variables revenus mesurés niveau ménage rapportées à la taille du ménage.

| Libellé poste 	| Période de reférence dans l'enquête 	| Méthode d'annualisation 	|
|--------------------------------------------------------------------------------------------------------------	|-------------------------------------	|---------------------------------------------------------------------------------------------------------------	|
| Boissons alcoolisees et tabac 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Habillement 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Chaussures  et  reparation 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Loyer 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Entretien de la maison  (excl. renovation, incl. services/materiels) 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Approvisionnement en  eau 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Ramassage d'ordure et evacuation des eaux usees 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Autres services et  couts domestiques (excl. interet/assurance) 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| electricite 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Gaz 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Combustibles liquides (carburant, etc.) 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Combustibles solides (charbon, bois, etc.) 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Services domestiques et autres services menagers 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Medicament  et produits et equipement therapeutiques 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Soins medicaux 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Soins dentaires 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Maintenance et reparation des vehicules 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Essence, autres combustibles  (pour le 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Bus et taxi (tous les membres du menages) 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Autre couts lies au transport (sans les voyages internationaux) 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Poste 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Services d'appel telephonique (portable) 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Autres services telephoniques /fax 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Jeux  et  hobby 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Equipment de sport, camping et recreation plein aire 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Jardins, plantes et fleurs (pas pour l agriculture) 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Animaux domestiques et les couts  (incl. nourriture des animaux) 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Frais pour le sport, cinema, muse, etc 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Frais pour la TV, radio, etc (incl. L'eaupement loue) 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| CD, Video et DVD (louer ou acheter) 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Jeux  de chance 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Autres  services de loisirs 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Journaux 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Livres, papiers et d'autre fournitures 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Hotel et services de logement 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Vacances organises 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Frais de scolarite et de prise en char 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Salon de coiffure 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Bijoux, horloges et montres 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Voyage et autres articles personnels 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Services de protection sociale, garderie 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Assurance maison 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Assurance maladie 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Assurance voyage et incendie 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Autres  assurances sans l'assurance vi 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Frais bancaires  et autres services financiers 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Funerailles et  autres  services nca 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Autres articles menagers non durables 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Frais funerailles et autres services n 	| 3 derniers mois 	| Aggrégation des 4 passages de l'enquêtes 	|
| Meubles et revetement de sol 	| 12 derniers mois 	| Pas besoin 	|
| Textiles domestiques (rideaux, torchons, serviettes) 	| 12 derniers mois 	| Pas besoin 	|
| Refrigerateurs et congelateurs 	| 12 derniers mois 	| Pas besoin 	|
| Gazinieres, cuisinieres electriques 	| 12 derniers mois 	| Pas besoin 	|
| Lave vaisselles 	| 12 derniers mois 	| Pas besoin 	|
| Machines a laver et a secher 	| 12 derniers mois 	| Pas besoin 	|
| Gros appareils menagers (appareils de chauffage, climatiseurs, humidifcateur, chauffe-eau) 	| 12 derniers mois 	| Pas besoin 	|
| Fer a repasser 	| 12 derniers mois 	| Pas besoin 	|
| Mixeurs de tout genre 	| 12 derniers mois 	| Pas besoin 	|
| Fours micro-ondes 	| 12 derniers mois 	| Pas besoin 	|
| Aspirateurs et autre equipement de menage 	| 12 derniers mois 	| Pas besoin 	|
| Machines a coudre et a tricoter 	| 12 derniers mois 	| Pas besoin 	|
| Autres petits appareils electromenagers 	| 12 derniers mois 	| Pas besoin 	|
| Verrerie, vaisselle et ustensiles de me 	| 12 derniers mois 	| Pas besoin 	|
| Gros outillages et materiel pour la maison 	| 12 derniers mois 	| Pas besoin 	|
| Petits outillages et accessoires divers 	| 12 derniers mois 	| Pas besoin 	|
| Nouvelle voiture, moto te minibus 	| 12 derniers mois 	| Pas besoin 	|
| Nouvelles voitures de seconde main 	| 12 derniers mois 	| Pas besoin 	|
| Cycles et motocycles 	| 12 derniers mois 	| Pas besoin 	|
| Autre equipement de transport (pas pour le bussiness ou l'agriculture) 	| 12 derniers mois 	| Pas besoin 	|
| Biens durables comme voyages internationaux 	| 12 derniers mois 	| Pas besoin 	|
| Telephones portables (y compris les reparations) 	| 12 derniers mois 	| Pas besoin 	|
| Autres equipements de telephones et fax 	| 12 derniers mois 	| Pas besoin 	|
| Radio ou autre equipement audio 	| 12 derniers mois 	| Pas besoin 	|
| Tele, y compris l'antenne, video 	| 12 derniers mois 	| Pas besoin 	|
| Autre materiel du son et de l'image (haut parleur, magnetophone, lecteur cassette/CD/DVD, casques, baladeur) 	| 12 derniers mois 	| Pas besoin 	|
| Appareils photos, cameras et equipement 	| 12 derniers mois 	| Pas besoin 	|
| Instruments optiques 	| 12 derniers mois 	| Pas besoin 	|
| Ordinateurs personnels et autre equipement 	| 12 derniers mois 	| Pas besoin 	|
| Reparation de materiel audiovisuel, photographique, trantement de l'information 	| 12 derniers mois 	| Pas besoin 	|
| Instruments de musique 	| 12 derniers mois 	| Pas besoin 	|
| Loisir et  la culture 	| 12 derniers mois 	| Pas besoin 	|
| Riz 	| 7 derniers jours 	| Multiplication par 12 pour obtenir la conso trimestrielle ensuite aggrégation sur les 4 passages de l'enquête 	|
| Mil 	| 7 derniers jours 	| Multiplication par 12 pour obtenir la conso trimestrielle ensuite aggrégation sur les 4 passages de l'enquête 	|
| Sucre 	| 7 derniers jours 	| Multiplication par 12 pour obtenir la conso trimestrielle ensuite aggrégation sur les 4 passages de l'enquête 	|
| Sorgho 	| 7 derniers jours 	| Multiplication par 12 pour obtenir la conso trimestrielle ensuite aggrégation sur les 4 passages de l'enquête 	|
| Viande de boeuf fraiche 	| 7 derniers jours 	| Multiplication par 12 pour obtenir la conso trimestrielle ensuite aggrégation sur les 4 passages de l'enquête 	|
| The 	| 7 derniers jours 	| Multiplication par 12 pour obtenir la conso trimestrielle ensuite aggrégation sur les 4 passages de l'enquête 	|
| Mais en grain crus 	| 7 derniers jours 	| Multiplication par 12 pour obtenir la conso trimestrielle ensuite aggrégation sur les 4 passages de l'enquête 	|
| Beurre de karite 	| 7 derniers jours 	| Multiplication par 12 pour obtenir la conso trimestrielle ensuite aggrégation sur les 4 passages de l'enquête 	|
| Poisson fume, seche, sale 	| 7 derniers jours 	| Multiplication par 12 pour obtenir la conso trimestrielle ensuite aggrégation sur les 4 passages de l'enquête 	|
| Poisson frais 	| 7 derniers jours 	| Multiplication par 12 pour obtenir la conso trimestrielle ensuite aggrégation sur les 4 passages de l'enquête 	|
| Huile d'arachide 	| 7 derniers jours 	| Multiplication par 12 pour obtenir la conso trimestrielle ensuite aggrégation sur les 4 passages de l'enquête 	|
| Pain 	| 7 derniers jours 	| Multiplication par 12 pour obtenir la conso trimestrielle ensuite aggrégation sur les 4 passages de l'enquête 	|
| Arachide decortiquee 	| 7 derniers jours 	| Multiplication par 12 pour obtenir la conso trimestrielle ensuite aggrégation sur les 4 passages de l'enquête 	|
| Viande de mouton ou de chevre fraeche 	| 7 derniers jours 	| Multiplication par 12 pour obtenir la conso trimestrielle ensuite aggrégation sur les 4 passages de l'enquête 	|
| Lait frais local 	| 7 derniers jours 	| Multiplication par 12 pour obtenir la conso trimestrielle ensuite aggrégation sur les 4 passages de l'enquête 	|
| Tubercules et plantain 	| 7 derniers jours 	| Multiplication par 12 pour obtenir la conso trimestrielle ensuite aggrégation sur les 4 passages de l'enquête 	|
| Oignon frais 	| 7 derniers jours 	| Multiplication par 12 pour obtenir la conso trimestrielle ensuite aggrégation sur les 4 passages de l'enquête 	|
| Cube( Maggi, Jumbo, etc) 	| 7 derniers jours 	| Multiplication par 12 pour obtenir la conso trimestrielle ensuite aggrégation sur les 4 passages de l'enquête 	|
| Lait en poudre 	| 7 derniers jours 	| Multiplication par 12 pour obtenir la conso trimestrielle ensuite aggrégation sur les 4 passages de l'enquête 	|
| Haricots secs 	| 7 derniers jours 	| Multiplication par 12 pour obtenir la conso trimestrielle ensuite aggrégation sur les 4 passages de l'enquête 	|

## Covariables et variables structurelles


| Nom_variable 	| Définition 	| Question_dans_enquete 	|
|------------------------------	|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|-----------------------------------------------------------------------------------------------------------------------------	|
| cov_i_age 	| Age de l'individu 	|  m4 	|
| cov_i_cadre 	| Dummy prenant la valeur 1 pour les individus ayant comme catégorie socio-professionnelle est cadre supérieur, ingénieur, cadre moyen ou agent de maitrise 	| w16==1 ; w16==2 	|
| cov_i_categorie_CGU | Cette variable est définie uniquement sur les indépendants. Elle permet de faire la distinction entre les indépendants entre les commerçants et revendeurs de ciments et de denrées alimentaires (CGU prod A) des autres commerçants ou revendeurs (CGU prod B) ou des prestataires de service (CGU service). Elle est particulièrement pertinente dans le cas du système socio-fiscal sénégalais. Les indépendants CGU prod A incluent ceux dont la branche d'activité est les produits des industries alimentaires tels que l'abattage, la conservation et la transformation de produits alimentaires et de boissons. Ceux dont l'entreprise se trouvent dans la branche des services sont considérés comme indépendants CGU services. Tous les autres indépendants qui ne sont pas dans les deux précédentes catégories sont dans CGU prod B.|   | 
| cov_i_classe_frequente 	| Classe fréquentée au moment de l'enquête 	| E6 	|
| cov_i_enfant_charge 	| Nombre d'enfants à charge du chef de ménage ou du conjoint. Il s'agit des enfants biologiques de moins de 21 ans ou de ceux entre 21 et 25 ans mais qui sont étudiants 	| m4<=21 & m5==3; w11==7 & m4>21 & m4<=25 & m5==3 	|
| cov_i_lien_cm 	| Lien de l'individu avec le chef de ménage 	| m5 	|
| cov_i_ponderation 	| Poids de l'individu dans la population 	| weight_pc 	|
| cov_i_secteur_activite 	| Secteur d'activité des individus âgés de plus de 15 ans. Cette variable permet de distinguer les actifs agricoles, les salariés du formel et de l'informel ainsi que les indépendants. Les actifs agricoles comprennent ceux dont l'entreprise est dans la branche des produits agricoles, sylvicoles, pêche et piscicultures (w15). Les salaries regroupent les cadres, employés, ouvriers, aides-familiaux, apprentis (w16) ou ceux qui déclarent percevoir un salaire (w24). Les indépendants sont les employeurs ou les travailleurs sous compte propre (w16). |  w17; w18a;w18b;w18c;w18d;w18e;w16;w24;w14;w15;w15_bis |
| cov_i_secteur_calage | Secteur d'activité des individus, utilisé pour le calage. Il regroupe les secteurs agricoles, industriels et service. Le secteur agricole comprend les individus dont l'entreprise est dans la branche des produits agricoles, sylvicoles, pêche et piscicultures (w15). Le secteur industriel comprend les branches: extraction (petrole, minerrais, etc), abattage, charbon hydrocarbure, minerais, textiles, raffinage, travaux de construction, machines, produits chimiques, etc. Celui des services inclus toutes les activités de transports (routier, maritimes, etc), ventes et de services (educations, conseil, intermédiation, etc.).| e20; e19|
| cov_i_secteur_publique_prive 	| Variable dichotomique prenant la valeur 1 pour tous les salariés qui travaillent dans l'administration publique, l'armée ou les forces de l'ordre. Elle prend la valeur 2 pour tous les salariés du privé ayant un bulletin de paie.	| w15==751 ; w15==752 ; w14==340 ; w14==22; ; w14>=546 ; w14<=550 	|
| cov_i_secteur_formel_informel 	| Tous les salariés du publique plus ceux du privé formels. 	| w26==1 & agri==0 & w16<=5	|
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

| cov_i_cadre 	|  	|
|-------------------------------	|------	|
| Libelle 	| Code 	|
| non-cadre 	| 1	|
| cadre	| 2 	|

| cov_i_categorie_CGU 	|  	|
|-------------------------------	|------	|
| Libelle 	| Code 	|
| CGU comm/prod A (agro-alimentaire et ciment) 	| 1	|
| CGU comm/prod B (autres produits) 	| 2 	|
| CGU service 	| 3 	|

| cov_i_classe_frequente 	|  	|
|-------------------------------	|------	|
| Libelle 	| Code 	|
| Maternelle 	| 1 	|
| Primaire 	| 2 	|
| Secondaire 	| 3 	|
| Superieur 	| 4 	|


| cov_i_secteur_activite 	|  	|
|-------------------------------	|------	|
| Libelle 	| Code 	|
| Actif agricole 	| 0 	|
| Salarie/dependant formel 	| 1 	|
| Salarie/dependant informel 	| 2 	|
| Independant	| 3 	|

| cov_i_secteur_formel_informel 	|  	|
|-------------------------------	|------	|
| Libelle 	| Code 	|
| Formel 	| 1 	|
| Informel 	| 0 	|

| cov_i_secteur_calage 	|  	|
|-------------------------------	|------	|
| Libelle 	| Code 	|
| agriculture 	| 1 	|
| industrie 	| 2 	|
| service 	| 3 	|

| cov_i_secteur_publique_prive 	|  	|
|-------------------------------	|------	|
| Libelle 	| Code 	|
| public 	| 1 	|
| prive 	| 2 	|


| cov_i_sexe 	|  	|
|-------------------------------	|------	|
| Libelle 	| Code 	|
| femme 	| 1 	|
| homme 	| 2 	|

| cov_i_statut_matrimonial 	|  	|
|-------------------------------	|------	|
| Libelle 	| Code 	|
| Marie 	| 1 	|
| Celibataire 	| 2 	|
| Veuf, Divorcé 	| 3 	|
| Non concerné 	| 4 	|

| cov_i_lien_cm 	|  	|
|-----------------------------------	|------	|
| Libelle 	| Code 	|
| Chef du menage 	| 1 	|
| Conjoint du CM 	| 2 	|
| Enfant du chef/conjoint du CM 	| 3 	|
| Pere/mere du CM/conjoint du CM 	| 4 	|
| Autre parent du CM/conjoint du CM 	| 5 	|
| Autres personnes non apparentees 	| 6 	|
| Domestique 	| 7 	|

| cov_i_urbain_rural 	|  	|
|-------------------------------	|------	|
| Libelle 	| Code 	|
| urbain 	| 1	|
| rural	| 2 	|
