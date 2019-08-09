
# DESCRIPTION GENERALE PAR BASE / TABLE

## Base dépenses - échelle : ménage x produit

* hh_id = identifiant du ménage
* prod_id = identifiant du type de produit acheté
* depense
* prix (missing si pas dispo)
* quantite (missing is pas dispo) 

autre ? 

## Base revenus - échelle : par ménage x individus

* hh_id
* pers_id 
* pond_m = pondération du ménage
* lien_cm = liens par rapport au chef du ménage 
* taille_m = nombre de personnes dans le ménage
* rev_b_i_*nom_du_revenu* = tous les revenus brut individualisés. Par brut il faut vraiment entendre "avant toutes taxes et tout transfers" 
* rev_n_i_*nom_du_revenu* = tous les revenus net individualisés. Ici par net il faut entendre que au moins un impôts simulé par openfisca a été prélevé. 
* cov_i_*nom_de_la_covariable* = toutes les covariables individuelles
* cov_m_*nom_de_la_covariable* = toutes les covariables niveaux ménage 

autre ? 

## Table taux taxes indirectes - échelle : produits

* prod_id = identifiant du type de produit acheté
* cat = categorie du bien 
* taux_tva = taux tva appliqué pour ce type de bien (ex : 0.18)
* taux_importation = taux appliqué aux importations de ce type de bien
* taux_taxe_speciale_1 = taux appliqué aux bien de ce type, au titre d'une autre tax sur la conso
* taux_taxe_speciale_2 ...
* ...
* subvention ?

autre ?

# Liste variable - SENEGAL - par ordre alphabéthique 

# Liste variable - COTE D IVOIRE - par ordre alphabéthique

* rev_n_i_act1 = revenus de l'activité principale nette de l'impôt sur le revenu. (sera vide pour le secteur identifié comme informel)
* rev_b_i_act1 = revenus de l'activité principale brute de l'impôt sur le revenu. (sera vide pour le secteur identifié comme formel)
* rev_b_act2 = revenus des activités secondaire (non taxé) 

etc 

# Liste variable - MALI - par ordre alphabéthique




