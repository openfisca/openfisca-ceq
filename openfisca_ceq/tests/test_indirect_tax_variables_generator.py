import logging
import os
import pandas as pd


from openfisca_ceq import CountryTaxBenefitSystem as CEQTaxBenefitSystem
from openfisca_ceq.tools.variables_generator import generate_postes_variables


log = logging.getLogger(__name__)


def main():
    produits_file_path = os.path.join("/home/benjello/Dropbox/Projet_Micro_Sim/C_IO/Produits_CIV.xlsx")

    produits = pd.read_excel(produits_file_path)

    log.info(produits.columns)
    label_by_code_coicop = (produits
        .rename(
            columns = {
                'description_enquete': 'label',
                }
            )
        .filter(['label', 'code_coicop'])
        .dropna()
        .astype(str)
        )
    duplicated_coicop = label_by_code_coicop.loc[label_by_code_coicop.code_coicop.duplicated()]
    for code_coicop in duplicated_coicop.code_coicop.unique():
        n = sum(label_by_code_coicop.code_coicop == code_coicop)
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        enhanced_code_coicops = [code_coicop + '.' + alphabet[i] for i in range(n)]
        label_by_code_coicop.loc[label_by_code_coicop.code_coicop == code_coicop, 'code_coicop'] = enhanced_code_coicops

    assert not label_by_code_coicop.code_coicop.duplicated().any()
    label_by_code_coicop = (label_by_code_coicop
        .set_index('code_coicop')
        .to_dict()['label']
        )

    log.info(label_by_code_coicop)

    tax_benefit_system = CEQTaxBenefitSystem()
    log.info(tax_benefit_system.variables.keys())
    generate_postes_variables(tax_benefit_system, label_by_code_coicop)
    log.info(tax_benefit_system.variables.keys())


if __name__ == '__main__':
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)
    main()
