# -*- coding: utf-8 -*-


import logging
import os
import pkg_resources


from openfisca_ceq import (
    CountryTaxBenefitSystem as CEQTaxBenefitSystem,
    entities,
    )

log = logging.getLogger(__name__)


ceq_variables_directory = os.path.join(
    pkg_resources.get_distribution('openfisca-ceq').location,
    'openfisca_ceq',
    'variables'
    )
assert os.path.exists(ceq_variables_directory)

ceq_input_variables = {
    name
    for name, variable in CEQTaxBenefitSystem().variables.items()
    if len(variable.formulas) == 0
    }

ceq_computed_variables = {
    name
    for name, variable in CEQTaxBenefitSystem().variables.items()
    if len(variable.formulas) > 0
    }


def add_ceq(country_tax_benefit_system):
    country_entities = country_tax_benefit_system.entities
    entities_by_name = dict((entity.key, entity) for entity in country_entities)
    entities.Person = entities_by_name['person']
    entities.Household = entities_by_name['household']
    country_variables = set(country_tax_benefit_system.variables.keys())

    input_intersection_country = ceq_input_variables.intersection(country_variables)
    if input_intersection_country:
        log.info("Country variables replacing CEQ input variables:\n{}".format(
            " - " + ('\n - ').join(
                list(sorted(input_intersection_country))
                )
            ))
    input_difference_country = ceq_input_variables.difference(country_variables)
    if input_difference_country:
        log.info("Missing CEQ input variables:\n{}".format(
            " - " + ('\n - ').join(
                list(sorted(input_difference_country))
                )
            ))
    computed_intersection_country = ceq_computed_variables.intersection(country_variables)
    if computed_intersection_country:
        log.info("Country variables replacing CEQ computed variables:\n{}".format(
            " - " + ('\n - ').join(
                list(sorted(computed_intersection_country))
                )
            ))

    ignored_variables = country_variables
    assert not country_variables.intersection(ceq_computed_variables), \
        "Some country variables matches computed CEQ variables: {}".format(
            country_variables.intersection(ceq_computed_variables))

    # TODO load only variables that do not already exist
    country_tax_benefit_system.add_variables_from_directory(ceq_variables_directory,
        ignored_variables = ignored_variables)

    return country_tax_benefit_system


if __name__ == '__main__':
    import sys
    from openfisca_cote_d_ivoire import CountryTaxBenefitSystem
    from openfisca_cote_d_ivoire.survey_scenarios import CoteDIvoireSurveyScenario
    logging.basicConfig(level = logging.DEBUG, stream = sys.stdout)

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
