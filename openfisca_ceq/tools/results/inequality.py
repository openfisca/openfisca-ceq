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

    weights = survey_scenario.calculate_variable("household_weight", period = period)
    nb_persons = 1.0
    if per_capita:
        nb_persons = survey_scenario.calculate_variable("number_of_people_per_household", period = period)
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

