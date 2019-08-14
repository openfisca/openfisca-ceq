import logging
import os
import pandas as pd


from openfisca_ceq import CountryTaxBenefitSystem as CEQTaxBenefitSystem
from openfisca_ceq.tools.variables_generator import generate_postes_variables


log = logging.getLogger(__name__)


def main():
    produits_file_path = os.path.join("/home/benjello/Dropbox/Projet_Micro_Sim/C_IO/Produits_CIV.xlsx")

    produits = pd.read_excel(produits_file_path)

    print(produits.columns)
    taxes = ['tva', 'tax_speciale_1',  'tax_speciale_2', 'tax_import']
    taxe = 'tva'

    # for taxe in taxes:
    #     print(produits.groupby(['id_produit', taxe])['id_hh'].count())

    label_by_code_coicop = (produits
        .rename(
            columns = {
                'description_enquete': 'label',
                }
            )
        .filter(['label', 'nom_question'])
        .rename(
            columns = {
                'nom_question': 'code_coicop',
                }
            )
        .astype(str)
        .set_index('code_coicop')
        .to_dict()['label']
        )

    print(label_by_code_coicop)


    tax_benefit_system = CEQTaxBenefitSystem()
    print(tax_benefit_system.variables.keys())
    generate_postes_variables(tax_benefit_system, label_by_code_coicop)
    print(tax_benefit_system.variables.keys())


if __name__ == '__main__':
    main()
