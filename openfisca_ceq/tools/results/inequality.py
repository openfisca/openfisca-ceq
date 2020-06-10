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

    weights = (
        (
            survey_scenario.calculate_variable("household_weight", period = period) 
            * survey_scenario.calculate_variable("number_of_people_per_household", period = period)
            )
        if per_capita
        else survey_scenario.calculate_variable("household_weight", period = period)
        )

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
        tax_variable = None,
        by_variable = None,
        period = None,
        digits = 2,
        ):
    if period is None:
        period = survey_scenario.year
    assert period is not None
    variables = [tax_variable, income_variable] 
    return (
        survey_scenario.compute_pivot_table(
            aggfunc = "sum", 
            values = variables, 
            index = by_variable, 
            period = survey_scenario.year, 
            concat_axis = 1)
        .eval("incidence = {} / {}".format(tax_variable, income_variable))
        .round(digits)
        )


def concentration_share(
        survey_scenario,
        tax_variable = None,
        by_variable = None,
        period = None,
        digits = 2,
        ):
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


def taxpayer_share(
        survey_scenario,
        tax_variable = None,
        by_variable = None,
        period = None,
        digits = 2,
        ):
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
        )
    series.name = "pct_of_taxpayers"
    return series