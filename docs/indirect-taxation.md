# Taxes indirectes — générateur de nomenclature

Le cœur fournit un générateur **générique** (mono-pays) de nomenclature de taxes
indirectes, dans
`openfisca_ceq.tools.indirect_taxation.consumption_items_nomenclature`.

!!! info "Configuration requise"
    Ce module lit sa configuration depuis la section `[ceq]` de `raw_data.ini`
    (openfisca-survey-manager) :

    - `consumption_items_directory` : dossier contenant les fichiers `Produits_<CODE>.xlsx` ;
    - `country_codes` : table pays → code ISO, p. ex.
      `senegal:SEN,mali:MLI,cote_d_ivoire:CIV`.

    La table pays n'est **plus codée en dur** : un code manquant lève une erreur explicite
    (`country_code(...)`).

## Fonctions principales

- `country_code(country)` — code ISO d'un pays, depuis la config.
- `build_label_by_code_coicop(country, …)` — table libellé ↔ code COICOP d'un pays,
  à partir de `Produits_<CODE>.xlsx`.
- `build_complete_label_coicop_data_frame(country, …)` — jointure avec la nomenclature
  COICOP complète.
- `build_tax_rate_by_code_coicop(country, tax_variables=…)` — taux de taxe par code COICOP.

!!! note "Comparaison multi-pays"
    Le générateur de **comparaison multi-pays** (assets `merged*`) a quitté le cœur en
    2.0 ; il vit désormais dans
    [openfisca-ceq-afrique-ouest](https://github.com/openfisca/openfisca-ceq-afrique-ouest).
