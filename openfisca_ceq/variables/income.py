# -*- coding: utf-8 -*-

# This file defines variables for the modelled legislation.
# A variable is a property of an Entity such as a Person, a Household…
# See https://openfisca.org/doc/variables.html

# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_ceq.entities import *


# This variable is a pure input: it doesn't have a formula


class alimony(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Alimony"


class all_income_excluding_transfers(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Earned and Unearned Incomes of All Possible Sources and Excluding Government Transfers"


class autoconsumption(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Autoconsumption"


class gifts_sales_durables(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Gifts, proceeds from sale of durables"


class imputed_rent(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Imputed rent for owner occupied housing"


class market_income(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Market income"

    def formula(household, period):
        all_income_excluding_transfers = household('all_income_excluding_transfers', period)
        gifts_sales_durables = household('gifts_sales_durables', period)
        alimony = household('alimony', period)
        autoconsumption = household('autoconsumption', period)
        imputed_rent = household('imputed_rent', period)
        other_income = household('other_income', period)

        market_income = (
            all_income_excluding_transfers
            + gifts_sales_durables
            + alimony
            + autoconsumption
            + imputed_rent
            + other_income
            )
        return market_income


class market_income_plus_pensions(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Market income plus net pensions"

    def formula(houshold, period):
        market_income = houshold('market_income', period)
        pensions = houshold('pensions', period)
        contributions_pensions = houshold('contributions_pensions', period)
        market_income_plus_pensions = (
            market_income
            + pensions
            - contributions_pensions
            )
        return market_income_plus_pensions


class other_income(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Other sources of income"


class pensions(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Old-age contributory pensions"
