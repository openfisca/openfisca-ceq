import numpy as np
import pandas as pd


from openfisca_survey_manager.statshelpers import gini, bottom_share, top_share


BOTTOM_SHARE = .4
TOP_SHARE = .1


def inequality_table(
        survey_scenario,
        bottom_share_value = BOTTOM_SHARE,
        per_capita = True,
        period = None,
        top_share_value = TOP_SHARE,
        variables = None,
        digits = 2
        ):

    if period is None:
        period = survey_scenario.year
    if variables is None:
        variables = [
            "market_income",
            "market_income_plus_pensions",
            "gross_income",
            "disposable_income",
            "consumable_income",
            "final_income",
            ]

    nb_persons = survey_scenario.calculate_variable("number_of_people_per_household", period = period) if per_capita else 1
    weights = survey_scenario.calculate_variable("household_weight", period = period) * nb_persons
    return pd.DataFrame.from_dict(
        dict([
            (
                variable,
                {
                    "Gini": gini(survey_scenario.calculate_variable(
                        variable, period = period) / nb_persons, weights),
                    "Bottom 40 %": bottom_share(survey_scenario.calculate_variable(
                        variable, period = period) / nb_persons, bottom_share_value, weights = weights),
                    "Top 10 %": top_share(survey_scenario.calculate_variable(
                        variable, period = period) / nb_persons, top_share_value, weights = weights),
                    }
                )
            for variable in variables
            ])
        ).round(digits)


def incidence_table(
        survey_scenario,
        income_variable = None,
        tax_variables = None,
        by_variable = None,
        period = None,
        digits = 2,
        ):

    if not isinstance(tax_variables, str) and len(tax_variables) >= 2:
        df = pd.concat(
            [
                incidence_table(survey_scenario, income_variable, [tax_variable], by_variable)
                for tax_variable in tax_variables
                ],
            axis = 1,
            )
        df.name = "incidence"
        return df

    if period is None:
        period = survey_scenario.year
    assert period is not None

    tax_variable = tax_variables[0]
    variables = [tax_variable, income_variable]
    series = (
        survey_scenario.compute_pivot_table(
            aggfunc = "sum",
            values = variables,
            index = by_variable,
            period = survey_scenario.year,
            concat_axis = 1)
        .eval("{tax_variable}_incidence = {tax_variable} / {income_variable}".format(
            tax_variable = tax_variable,
            income_variable= income_variable
            ))
        .round(digits)
        ["{}_incidence".format(tax_variable)]
        )
    series.name = tax_variable
    return series


def concentration_share(
        survey_scenario,
        tax_variables = None,
        by_variable = None,
        period = None,
        digits = 2,
        ):

    if not isinstance(tax_variables, str) and len(tax_variables) >= 2:
        df = pd.concat(
            [
                concentration_share(survey_scenario, [tax_variable], by_variable)
                for tax_variable in tax_variables
                ],
            axis = 1,
            )
        df.name = "concenctration_share"
        return df

    tax_variable = tax_variables[0]
    if period is None:
        period = survey_scenario.year
    assert period is not None

    masses = (
        survey_scenario.compute_pivot_table(
            aggfunc = "sum",
            values = [tax_variable],
            index = by_variable,
            period = survey_scenario.year,
            )
        .round(digits)
        )
    return (masses / masses.sum()).round(digits)


def income_shares(
        survey_scenario,
        income_variables = None,
        by_variable = None,
        period = None,
        digits = 2,
        ):

    if not isinstance(income_variables, str) and len(income_variables) >= 2:
        df = pd.concat(
            [
                concentration_share(survey_scenario, [income_variable], by_variable)
                for income_variable in income_variables
                ],
            axis = 1,
            )
        df.name = "income_shares"
        return df

    income_variable = income_variables[0]
    if period is None:
        period = survey_scenario.year
    assert period is not None

    masses = (
        survey_scenario.compute_pivot_table(
            aggfunc = "sum",
            values = [income_variable],
            index = by_variable,
            period = survey_scenario.year,
            )
        .round(digits)
        )
    return (masses / masses.sum()).round(digits)



def taxpayers_share(
        survey_scenario,
        tax_variables = None,
        by_variable = None,
        period = None,
        digits = 2,
        ):
    if not isinstance(tax_variables, str) and len(tax_variables) >= 2:
        df = pd.concat(
            [
                taxpayers_share(survey_scenario, [tax_variable], by_variable)
                for tax_variable in tax_variables
                ],
            axis = 1,
            )
        df.name = "pct_of_taxpayers"
        return df

    tax_variable = tax_variables[0]
    if period is None:
        period = survey_scenario.year
    assert period is not None


    entity_key = survey_scenario.tax_benefit_system.variables[tax_variable].entity.key
    weight_variable = survey_scenario.weight_variable_by_entity[entity_key]
    series = (
        (
            survey_scenario.create_data_frame_by_entity(
                variables = [tax_variable, by_variable, weight_variable],
                period = survey_scenario.year,
                )
            )[entity_key]
        .eval("taxpayers = ({} > 0)".format(tax_variable))
        .groupby(by_variable)
        .apply(
            lambda x: np.average(x.taxpayers, weights = x[weight_variable])
            )
        ).round(digits)

    series.name = tax_variable
    return series