import numpy as np


from openfisca_survey_manager.statshelpers import mark_weighted_percentiles
from openfisca_core.model_api import *
from openfisca_ceq.entities import *

# Market income
# Disposable income
# Consumable income
# Final income


class decile_disposable_income_per_capita(Variable):
    value_type = int
    entity = Household
    definition_period = YEAR
    label = "Decile of disposable income per capita"

    def formula(household, period):
        disposable_income = household('disposable_income', period)
        number_of_people_per_household = household('number_of_people_per_household', period)
        weights = (
            household("household_weight", period)
            * household("number_of_people_per_household", period)
            )
        labels = np.arange(1, 11)
        decile, _ = mark_weighted_percentiles(
            disposable_income / number_of_people_per_household,
            labels,
            weights,
            method = 2,
            return_quantiles = True,
            )
        return decile


class decile_market_income_per_capita(Variable):
    value_type = int
    entity = Household
    definition_period = YEAR
    label = "Decile of market income per capita"

    def formula(household, period):
        market_income = household('market_income', period)
        number_of_people_per_household = household('number_of_people_per_household', period)
        weights = (
            household("household_weight", period)
            * household("number_of_people_per_household", period)
            )
        labels = np.arange(1, 11)
        decile, _ = mark_weighted_percentiles(
            market_income / number_of_people_per_household,
            labels,
            weights,
            method = 2,
            return_quantiles = True,
            )
        return decile


class decile_market_income_plus_pensions_per_capita(Variable):
    value_type = int
    entity = Household
    definition_period = YEAR
    label = "Decile of market income plus pensions per capita"

    def formula(household, period):
        market_income = household('market_income_plus_pensions', period)
        number_of_people_per_household = household('number_of_people_per_household', period)
        weights = (
            household("household_weight", period)
            * household("number_of_people_per_household", period)
            )
        labels = np.arange(1, 11)
        decile, _ = mark_weighted_percentiles(
            market_income / number_of_people_per_household,
            labels,
            weights,
            method = 2,
            return_quantiles = True,
            )
        return decile


class decile_consumable_income_per_capita(Variable):
    value_type = int
    entity = Household
    definition_period = YEAR
    label = "Decile of consumable income per capita"

    def formula(household, period):
        consumable_income = household('consumable_income', period)
        number_of_people_per_household = household('number_of_people_per_household', period)
        weights = (
            household("household_weight", period)
            * household("number_of_people_per_household", period)
            )
        labels = np.arange(1, 11)
        decile, _ = mark_weighted_percentiles(
            consumable_income / number_of_people_per_household,
            labels,
            weights,
            method = 2,
            return_quantiles = True,
            )
        return decile


class decile_final_income_per_capita(Variable):
    value_type = int
    entity = Household
    definition_period = YEAR
    label = "Decile of final income per capita"

    def formula(household, period):
        final_income = household('final_income', period)
        number_of_people_per_household = household('number_of_people_per_household', period)
        weights = (
            household("household_weight", period)
            * household("number_of_people_per_household", period)
            )
        labels = np.arange(1, 11)
        decile, _ = mark_weighted_percentiles(
            final_income / number_of_people_per_household,
            labels,
            weights,
            method = 2,
            return_quantiles = True,
            )
        return decile
