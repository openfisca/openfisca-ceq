"""Framework générique de complétion CEQ.

Greffe les variables de concepts CEQ (répertoire ``variables/``) sur le système
socio-fiscal d'un pays. Ce module est **agnostique du pays** : toute donnée propre à une
étude (mapping de revenus harmonisés, variables ``custom``, variables d'enquête
spécifiques, coûts unitaires d'éducation) est **injectée par l'appelant**.

Le câblage de l'étude CEQ-Afrique de l'Ouest (variables d'enquête concrètes, réforme
``ceq`` historique, coûts unitaires) vit désormais dans le paquet
``openfisca-ceq-afrique-ouest`` et n'est plus connu du cœur.
"""

import importlib.resources
import logging
import os

import numexpr as ne

from openfisca_core.model_api import Variable, YEAR

from openfisca_ceq import (
    CountryTaxBenefitSystem as CEQTaxBenefitSystem,
    entities,
)


log = logging.getLogger(__name__)


ceq_variables_directory = str(importlib.resources.files("openfisca_ceq") / "variables")

assert os.path.exists(ceq_variables_directory)


ceq_variables = CEQTaxBenefitSystem().variables
ceq_input_variables = {
    name for name, variable in ceq_variables.items() if len(variable.formulas) == 0
}

ceq_computed_variables = {
    name for name, variable in ceq_variables.items() if len(variable.formulas) > 0
}


def add_ceq_framework(
    country_tax_benefit_system,
    *,
    harmonized_income_mapping=None,
    custom_variables=None,
    extra_variables=None,
    education_unit_cost=None,
):
    """Greffe les variables de concepts CEQ sur le système socio-fiscal d'un pays.

    :param country_tax_benefit_system: le TBS du pays à compléter.
    :param harmonized_income_mapping: dict ``{nom_harmonisé: variable_pays}`` optionnel ;
        toute valeur absente du TBS est créée comme variable d'entrée ``float`` au niveau
        de la personne.
    :param custom_variables: itérable de classes ``Variable`` optionnel, appliqué via
        ``update_variable`` (p. ex. variables harmonisées multi-pays).
    :param extra_variables: itérable de classes ``Variable`` optionnel, ajouté (ou remplacé
        si déjà présent) — variables d'enquête propres à l'étude.
    :param education_unit_cost: dict ``{catégorie: coût}`` optionnel ; déclenche la
        génération des variables de coût unitaire d'éducation (cf.
        :func:`add_ceq_education_unit_cost`).
    :return: le TBS complété.
    """
    country_entities = country_tax_benefit_system.entities
    entities_by_name = dict((entity.key, entity) for entity in country_entities)
    entities.Person = entities_by_name["person"]
    entities.Household = entities_by_name["household"]
    country_variables = set(country_tax_benefit_system.variables.keys())

    input_intersection_country = ceq_input_variables.intersection(country_variables)
    if input_intersection_country:
        log.info(
            "Country variables replacing CEQ input variables:\n{}".format(
                " - " + ("\n - ").join(list(sorted(input_intersection_country)))
            )
        )
    input_difference_country = ceq_input_variables.difference(country_variables)
    if input_difference_country:
        log.info(
            "Missing CEQ input variables:\n{}".format(
                " - " + ("\n - ").join(list(sorted(input_difference_country)))
            )
        )
    computed_intersection_country = ceq_computed_variables.intersection(
        country_variables
    )
    if computed_intersection_country:
        log.info(
            "Country variables replacing CEQ computed variables:\n{}".format(
                " - " + ("\n - ").join(list(sorted(computed_intersection_country)))
            )
        )

    ignored_variables = country_variables
    assert not country_variables.intersection(
        ceq_computed_variables
    ), "Some country variables matches computed CEQ variables: {}".format(
        country_variables.intersection(ceq_computed_variables)
    )

    country_tax_benefit_system.add_variables_from_directory(
        ceq_variables_directory, ignored_variables=ignored_variables
    )

    if harmonized_income_mapping is not None:
        missing_income_variables = set(harmonized_income_mapping.values()).difference(
            set(country_tax_benefit_system.variables.keys())
        )
        for missing_income_variable in missing_income_variables:
            definitions_by_name = dict(
                definition_period=YEAR,
                entity=entities_by_name["person"],
                label=missing_income_variable,
                value_type=float,
            )
            country_tax_benefit_system.add_variable(
                type(missing_income_variable, (Variable,), definitions_by_name)
            )

    if custom_variables is not None:
        for variable in custom_variables:
            country_tax_benefit_system.update_variable(variable)

    if extra_variables is not None:
        for variable in extra_variables:
            if variable.__name__ in country_tax_benefit_system.variables:
                country_tax_benefit_system.replace_variable(variable)
            else:
                country_tax_benefit_system.add_variable(variable)

    if education_unit_cost is not None:
        add_ceq_education_unit_cost(country_tax_benefit_system, education_unit_cost)

    return country_tax_benefit_system


def add_ceq_education_unit_cost(country_tax_benefit_system, unit_cost_by_category):
    """Génère les variables de coût unitaire d'éducation à partir d'un mapping.

    :param country_tax_benefit_system: le TBS du pays.
    :param unit_cost_by_category: dict ``{catégorie: coût}`` où ``catégorie`` ∈
        {``pre_school``, ``primary_education``, ``secondary_education``,
        ``tertiary_education``} — agnostique du pays (l'étude fournit ses coûts).
    """
    entities_by_name = dict(
        (entity.key, entity) for entity in country_tax_benefit_system.entities
    )

    definitions_by_name = dict(
        definition_period=YEAR,
        entity=entities_by_name["person"],
        label="Niveau d'enseignement de l'élève ou de l'étudiant",
        value_type=float,
    )
    country_tax_benefit_system.add_variable(
        type("eleve_enseignement_niveau", (Variable,), definitions_by_name)
    )
    del definitions_by_name
    definitions_by_name = dict(
        definition_period=YEAR,
        entity=entities_by_name["person"],
        label="L'élève ou de l'étudiant fréquente l'enseignement public",
        value_type=float,
        default_value=1.0,
    )
    country_tax_benefit_system.add_variable(
        type("eleve_enseignement_public", (Variable,), definitions_by_name)
    )

    enseignement_niveau_by_variable_name = {
        "pre_school": 0,
        "primary_education": 1,
        "secondary_education": 2,
        "tertiary_education": 3,
    }

    for (
        variable_name,
        enseignement_niveau,
    ) in enseignement_niveau_by_variable_name.items():

        def unit_cost_function_creator(cost, enseignement_niveau):
            def func(entity, period_arg):
                # On passe un local_dict explicite à numexpr : les valeurs lues doivent
                # être liées aux noms de l'expression.
                niveau = entity("eleve_enseignement_niveau", period_arg)
                public = entity("eleve_enseignement_public", period_arg)
                expression = (
                    "(niveau == {enseignement_niveau}) * public * {cost}".format(
                        enseignement_niveau=enseignement_niveau,
                        cost=cost,
                    )
                )
                return ne.evaluate(
                    str(expression),
                    local_dict={"niveau": niveau, "public": public},
                )

            func.__name__ = "formula"
            return func

        cost = unit_cost_by_category
        definitions_by_name = dict(
            definition_period=YEAR,
            entity=entities_by_name["person"],
            formula=unit_cost_function_creator(
                cost[variable_name], enseignement_niveau
            ),
            label=variable_name,
            value_type=float,
        )
        country_tax_benefit_system.add_variable(
            type(variable_name + "_person", (Variable,), definitions_by_name)
        )

        def household_education_formula_creator(person_variable_name):
            def func(household, period_arg):
                return household.sum(
                    household.members(person_variable_name, period_arg)
                )

            func.__name__ = "formula"
            return func

        country_tax_benefit_system.update_variable(
            type(
                variable_name,
                (Variable,),
                dict(
                    formula=household_education_formula_creator(
                        variable_name + "_person"
                    )
                ),
            )
        )


def get_all_neutralized_variables(survey_scenario, period, variables):
    """List all neutralized and de-facto neutralized variables from scenario from a particular list

    :param survey_scenario: The survey scenario to extract the variables from
    :type survey_scenario: SurveyScenario
    :param period: period to compute to check the variables for
    :type period: Period
    :param variables: variables list to check
    :type variables: list
    :return: By design and de facto neutralized variables lists
    :rtype: list, list
    """
    assert variables is not None
    df_by_entity = survey_scenario.create_data_frame_by_entity(
        variables=variables,
        period=period,
    )
    by_design_neutralized_variables_by_entity = dict()
    de_facto_neutralized_variables_by_entity = dict()

    for entity, df in df_by_entity.items():
        by_design_neutralized_variables = list()
        de_facto_neutralized_variables = list()
        for column in df:
            variable = survey_scenario.tax_benefit_system.variables.get(column)
            if variable is None:
                continue
            if variable.is_neutralized:
                by_design_neutralized_variables.append(column)
            elif (df[column] == variable.default_value).all():
                de_facto_neutralized_variables.append(column)

        by_design_neutralized_variables_by_entity[entity] = (
            by_design_neutralized_variables
        )
        de_facto_neutralized_variables_by_entity[entity] = (
            de_facto_neutralized_variables
        )

    return (
        by_design_neutralized_variables_by_entity,
        de_facto_neutralized_variables_by_entity,
    )
