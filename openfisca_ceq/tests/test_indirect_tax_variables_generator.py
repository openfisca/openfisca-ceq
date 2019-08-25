import logging
import os
import pandas as pd


from openfisca_ceq import CountryTaxBenefitSystem as CEQTaxBenefitSystem
from openfisca_ceq.tools.variables_generator import generate_postes_variables
from openfisca_survey_manager.coicop import build_raw_coicop_nomenclature

log = logging.getLogger(__name__)


def build_label_by_code_coicop(consumption_items_file_path):
    consumption_items = pd.read_excel(consumption_items_file_path)
    label_by_code_coicop = (consumption_items
        .rename(
            columns = {
                'label': 'label_variable',
                'nom_variable_format_wide': 'variable_name'
                }
            )
        .filter(['label_variable', 'code_coicop', 'variable_name'])
        .dropna()
        .astype(str)
        .sort_values('code_coicop')
        )
    label_by_code_coicop['code_coicop'] = label_by_code_coicop.code_coicop.str.strip("0")
    duplicated_coicop = label_by_code_coicop.loc[label_by_code_coicop.code_coicop.duplicated()]
    label_by_code_coicop['deduplicated_code_coicop'] = label_by_code_coicop.code_coicop.copy()
    for code_coicop in duplicated_coicop.code_coicop.unique():
        n = sum(label_by_code_coicop.code_coicop == code_coicop)
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        enhanced_code_coicops = [code_coicop + '.' + alphabet[i] for i in range(n)]
        label_by_code_coicop.loc[label_by_code_coicop.code_coicop == code_coicop, 'deduplicated_code_coicop'] = enhanced_code_coicops

    assert not label_by_code_coicop.deduplicated_code_coicop.duplicated().any()
    label_by_code_coicop = (label_by_code_coicop
        .set_index('deduplicated_code_coicop')
        )
    return label_by_code_coicop


def build_complete_label_coicop_data_frame(consumption_items_file_path, file_path = None, deduplicate = True):
    label_by_code_coicop = build_label_by_code_coicop(consumption_items_file_path)
    raw_coicop_nomenclature = build_raw_coicop_nomenclature()
    raw_coicop_nomenclature.to_csv('raw.csv')
    completed_label_coicop = (label_by_code_coicop
        .reset_index()
        .merge(raw_coicop_nomenclature, on = 'code_coicop', how = 'left')
        .filter(items = [
            'label_division',
            'label_groupe',
            'label_classe',
            'label_sous_classe',
            'label_poste',
            'label_variable',
            'code_coicop',
            'deduplicated_code_coicop',
            ])
        )

    if deduplicate:
        completed_label_coicop = (completed_label_coicop
            .drop('code_coicop', axis = 1)
            .rename(columns = {'deduplicated_code_coicop': "code_coicop"})
            )

    if file_path:
        completed_label_coicop.to_csv(file_path)
    return completed_label_coicop


def add_coicop_item_to_tax_benefit_system(tax_benefit_system, consumption_items_file_path):
    label_by_code_coicop = (build_label_by_code_coicop(consumption_items_file_path)
        .filter(['label_variable'])
        .reset_index()
        .rename(columns = {'deduplicated_code_coicop': "code_coicop"})
        .set_index("code_coicop")
        .to_dict()['label_variable']
        )
    log.info(label_by_code_coicop)
    log.info(tax_benefit_system.variables.keys())
    generate_postes_variables(tax_benefit_system, label_by_code_coicop)


def build_comparison_table(country_codes):
    dfs = [
        build_complete_label_coicop_data_frame(
            os.path.join(
                "/home/benjello/Dropbox/Projet_Micro_Sim/C_IO/Produits_{}.xlsx".format(country_code)),
            deduplicate = False
            )
        for country_code in country_codes
        ]

    index = [
        'label_division',
        'label_groupe',
        'label_classe',
        'label_sous_classe',
        'label_poste',
        'code_coicop'
        ]

    dfs = [
        df.groupby(index)['label_variable'].unique()
        for df in dfs
        ]

    merged = pd.concat(dfs, axis = 1, keys = country_codes, join = 'outer', copy = False)

    merged.to_csv('merged.csv')
    merged.to_excel('merged.xls')
    return merged.reset_index()


def main():
    consumption_items_file_path = os.path.join("/home/benjello/Dropbox/Projet_Micro_Sim/C_IO/Produits_CIV.xlsx")
    build_complete_label_coicop_data_frame(consumption_items_file_path)

    tax_benefit_system = CEQTaxBenefitSystem()
    add_coicop_item_to_tax_benefit_system(tax_benefit_system, consumption_items_file_path)
    log.info(sorted(tax_benefit_system.variables.keys()))



if __name__ == '__main__':
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)
    # consumption_items_file_path = os.path.join("/home/benjello/Dropbox/Projet_Micro_Sim/C_IO/Produits_SEN.xlsx")

    # label_by_code_coicop = build_label_by_code_coicop(consumption_items_file_path)

    country_codes = ['CIV', 'SEN']
    merged = build_comparison_table(country_codes)

    # main()
