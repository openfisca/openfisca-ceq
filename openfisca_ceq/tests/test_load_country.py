# -*- coding: utf-8 -*-


import os
import pkg_resources


from openfisca_ceq import entities



ceq_variables_directory = os.path.join(
    pkg_resources.get_distribution('openfisca-ceq').location,
    'openfisca_ceq',
    'variables'
    )
assert os.path.exists(ceq_variables_directory)


def add_ceq(country_tax_benefit_system):
    country_tax_benefit_system.add_variables_from_directory(ceq_variables_directory)
    return country_tax_benefit_system


if __name__ == '__main__':
    from openfisca_cote_d_ivoire import CountryTaxBenefitSystem
    country_tax_benefit_system = CountryTaxBenefitSystem()
    new_tbs = add_ceq(country_tax_benefit_system)

    print(sorted((new_tbs.variables.keys())))

    print(new_tbs.variables['age'].entity)
