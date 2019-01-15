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


from openfisca_ceq import CountryTaxBenefitSystem as CEQTaxBenefitSystem

ceq_variables = CEQTaxBenefitSystem().variables
print(ceq_variables.keys())

print(ceq_variables['disposable_income'].formulas)
print(ceq_variables['property_tax'].formulas)


ceq_input_variables = [
    name
    for name, variable in CEQTaxBenefitSystem().variables.items()
    if len(variable.formulas) == 0
    ]

ceq_computed_variables = [
    name
    for name, variable in CEQTaxBenefitSystem().variables.items()
    if len(variable.formulas) > 0
    ]

print(ceq_computed_variables)


def add_ceq(country_tax_benefit_system):
    country_entities = country_tax_benefit_system.entities
    entities_by_name = dict((entity.key, entity) for entity in country_entities)
    entities.Person = entities_by_name['person']
    entities.Household = entities_by_name['household']

    country_variables = country_tax_benefit_system.variables.keys()

    print("Missing CEQ input variables:\n{}".format(
        set(ceq_input_variables).difference(set(country_variables)))
        )
    country_tax_benefit_system.add_variables_from_directory(ceq_variables_directory)
    return country_tax_benefit_system


if __name__ == '__main__':
    from openfisca_cote_d_ivoire import CountryTaxBenefitSystem
    from openfisca_cote_d_ivoire.survey_scenarios import CoteDIvoireSurveyScenario
    country_tax_benefit_system = CountryTaxBenefitSystem()
    new_tbs = add_ceq(country_tax_benefit_system)


    from openfisca_cote_d_ivoire.tests.test_survey_scenario_from_stata_data import create_data_from_stata
    data = create_data_from_stata()
    survey_scenario = CoteDIvoireSurveyScenario(
        tax_benefit_system = new_tbs,
        data = data,
        year = 2017,
        )

    print(survey_scenario.calculate_variable('impots_directs', period = 2017)[0:10])
    print(survey_scenario.calculate_variable('impot_general_revenu', period = 2017)[0:10])
