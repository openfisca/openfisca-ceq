# -*- coding: utf-8 -*-


import logging
import os
import pkg_resources


from openfisca_core.model_api import Variable, YEAR


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


ceq_variables = CEQTaxBenefitSystem().variables
ceq_input_variables = {
    name
    for name, variable in ceq_variables.items()
    if len(variable.formulas) == 0
    }

ceq_computed_variables = {
    name
    for name, variable in ceq_variables.items()
    if len(variable.formulas) > 0
    }


def add_ceq_framework(country_tax_benefit_system):
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

    country_tax_benefit_system.add_variables_from_directory(ceq_variables_directory,
        ignored_variables = ignored_variables)

    from openfisca_ceq.tools.data_ceq_correspondence import non_ceq_input_by_person_variable
    missing_income_variables = set(non_ceq_input_by_person_variable.values()).difference(
        set(country_tax_benefit_system.variables.keys())
        )
    for missing_income_variable in missing_income_variables:
        definitions_by_name = dict(
            definition_period = YEAR,
            entity = entities_by_name['person'],
            label = missing_income_variable,
            value_type = float,
            )
        country_tax_benefit_system.add_variable(
            type(missing_income_variable, (Variable,), definitions_by_name)
            )

    from openfisca_ceq.tools.data_ceq_correspondence import multi_country_custom_ceq_variables
    for variable in multi_country_custom_ceq_variables:
        country_tax_benefit_system.replace_variable(variable)

    return country_tax_benefit_system


def get_all_neutralized_variables(survey_scenario, period, variables = None):
    assert variables is not None
    df_by_entity = survey_scenario.create_data_frame_by_entity(
        variables = variables,
        )
    by_design_neutralized_variables = list()
    de_facto_neutralized_variables = list()

    for entity, df in df_by_entity.items():
        for column in df:
            variable = survey_scenario.tax_benefit_system.variables.get(column)
            if variable is None:
                continue
            if variable.is_neutralized:
                by_design_neutralized_variables.append(column)
            elif (df[column] == variable.default_value).all():
                de_facto_neutralized_variables.append(column)

    return by_design_neutralized_variables, de_facto_neutralized_variables