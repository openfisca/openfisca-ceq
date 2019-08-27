import logging
import os


from openfisca_ceq import CountryTaxBenefitSystem as CEQTaxBenefitSystem
from openfisca_ceq.tools.indirect_taxation.consumption_items_nomenclature import (
    build_complete_label_coicop_data_frame,
    build_label_by_code_coicop,
    consumption_items_directory,
    )
from openfisca_ceq.tools.indirect_taxation.variables_generator import generate_postes_variables


log = logging.getLogger(__name__)


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


def main():
    consumption_items_file_path = os.path.join(
        consumption_items_directory,
        "Produits_CIV.xlsx"
        )
    build_complete_label_coicop_data_frame(consumption_items_file_path)

    tax_benefit_system = CEQTaxBenefitSystem()
    add_coicop_item_to_tax_benefit_system(tax_benefit_system, consumption_items_file_path)
    log.info(sorted(tax_benefit_system.variables.keys()))


if __name__ == '__main__':
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)
    main()
