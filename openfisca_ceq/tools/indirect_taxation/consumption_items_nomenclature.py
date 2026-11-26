import configparser
import logging
import os
import pandas as pd


from openfisca_survey_manager.coicop import build_raw_coicop_nomenclature
from pathlib import Path

# Get config directory using XDG Base Directory specification
# Fallback to ~/.config if XDG_CONFIG_HOME is not set
xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
if xdg_config_home:
    config_files_directory = os.path.join(xdg_config_home, "openfisca-survey-manager")
else:
    config_files_directory = os.path.join(
        Path.home(), ".config", "openfisca-survey-manager"
    )


log = logging.getLogger(__name__)


config_parser = configparser.ConfigParser()
config_parser.read(os.path.join(config_files_directory, "raw_data.ini"))
consumption_items_directory = config_parser.get("ceq", "consumption_items_directory")
assert os.path.exists(
    consumption_items_directory
), "Consumption items directory {} does not exists, please create it and add countries consumption items files".format(
    consumption_items_directory
)


def _load_country_code_by_country():
    """Table pays -> code pays, pilotée par la config (cœur agnostique du pays).

    Lue depuis l'option ``country_codes`` de la section ``[ceq]`` de ``raw_data.ini``,
    au format ``senegal:SEN,mali:MLI,cote_d_ivoire:CIV``. Absente, la table est vide :
    les codes sont alors exigés par l'appelant (cf. :func:`country_code`).
    """
    raw = config_parser.get("ceq", "country_codes", fallback=None)
    if not raw:
        return {}
    mapping = {}
    for pair in raw.split(","):
        country, _, code = pair.partition(":")
        if country.strip():
            mapping[country.strip()] = code.strip()
    return mapping


country_code_by_country = _load_country_code_by_country()


def country_code(country):
    """Code pays, avec message clair si la config ne le fournit pas."""
    try:
        return country_code_by_country[country]
    except KeyError:
        raise KeyError(
            "Code pays absent pour {!r}. Renseignez l'option 'country_codes' de la "
            "section [ceq] de raw_data.ini (ex. 'senegal:SEN,mali:MLI,"
            "cote_d_ivoire:CIV').".format(country)
        )


def build_label_by_code_coicop(
    country,
    additional_variables=None,
    new_code_coicop_variable="nouveau__code",
    fillna=dict(),
    filter_expression=None,
):
    consumption_items_file_path = os.path.join(
        consumption_items_directory,
        "Produits_{}.xlsx".format(country_code(country)),
    )
    if additional_variables is None:
        additional_variables = []
    consumption_items = pd.read_excel(consumption_items_file_path)
    if filter_expression is not None:
        consumption_items = consumption_items.query(filter_expression).copy()

    if new_code_coicop_variable is not None:
        consumption_items = consumption_items.drop(columns=["code_coicop"]).rename(
            columns={"nouveau_code_coicop": "code_coicop"}
        )
    label_by_code_coicop = (
        consumption_items.rename(
            columns={
                "label": "label_variable",
                "nom_variable_format_wide": "variable_name",
            }
        )
        .filter(
            ["label_variable", "code_coicop", "variable_name"] + additional_variables
        )
        .fillna(fillna)
        .dropna()
        .astype(str)
        .sort_values("code_coicop")
    )
    label_by_code_coicop["code_coicop"] = label_by_code_coicop.code_coicop.str.strip(
        "0"
    )
    duplicated_coicop = label_by_code_coicop.loc[
        label_by_code_coicop.code_coicop.duplicated()
    ]
    label_by_code_coicop["deduplicated_code_coicop"] = (
        label_by_code_coicop.code_coicop.copy()
    )
    for code_coicop in duplicated_coicop.code_coicop.unique():
        n = sum(label_by_code_coicop.code_coicop == code_coicop)
        enhanced_code_coicops = [code_coicop + "_item_" + str(i + 1) for i in range(n)]
        label_by_code_coicop.loc[
            label_by_code_coicop.code_coicop == code_coicop, "deduplicated_code_coicop"
        ] = enhanced_code_coicops

    assert not label_by_code_coicop.deduplicated_code_coicop.duplicated().any()
    label_by_code_coicop = label_by_code_coicop.set_index("deduplicated_code_coicop")
    return label_by_code_coicop.copy()


def build_complete_label_coicop_data_frame(country, file_path=None, deduplicate=True):
    label_by_code_coicop = build_label_by_code_coicop(country)
    raw_coicop_nomenclature = build_raw_coicop_nomenclature()
    completed_label_coicop = (
        label_by_code_coicop.reset_index()
        .merge(raw_coicop_nomenclature, on="code_coicop", how="left")
        .filter(
            items=[
                "label_division",
                "label_groupe",
                "label_classe",
                "label_sous_classe",
                "label_poste",
                "label_variable",
                "code_coicop",
                "deduplicated_code_coicop",
            ]
        )
    )

    if deduplicate:
        completed_label_coicop = completed_label_coicop.drop(
            "code_coicop", axis=1
        ).rename(columns={"deduplicated_code_coicop": "code_coicop"})

    if file_path:
        completed_label_coicop.to_csv(file_path)
    return completed_label_coicop


def build_tax_rate_by_code_coicop(
    country, tax_variables=None, fillna=dict(), filter_expression=None
):
    assert tax_variables is not None
    label_by_code_coicop = (
        build_label_by_code_coicop(
            country,
            additional_variables=tax_variables,
            fillna=fillna,
            filter_expression=filter_expression,
        )
        .drop(columns="code_coicop")
        .reset_index()
        .rename(columns={"deduplicated_code_coicop": "code_coicop"})
    )
    assert "code_coicop" in label_by_code_coicop.columns
    return label_by_code_coicop.copy()
