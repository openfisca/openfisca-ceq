# -*- coding: utf-8 -*-


from openfisca_core.model_api import Variable, YEAR
from openfisca_ceq.entities import Household


ceq_input_by_person_variable = {
    "rev_i_autoconsommation": "autoconsumption",
    "rev_i_autres_transferts": "other_income",
    "rev_i_loyers_imputes": "imputed_rent",
    }

ceq_intermediate_by_person_variable = {
    "rev_i_transferts_publics": "direct_transfers"
    }

non_ceq_input_by_person_variable = {
    "rev_i_autres_revenus_capital": "autres_revenus_du_capital",
    "rev_i_independants_formels": "revenu_non_salarie",
    "rev_i_informels_agricoles": "revenu_informel_agricole",
    "rev_i_informels_autres": "autres_revenus_informels",
    "rev_i_loyers": "revenu_locatif",
    "rev_i_pensions": "pension_retraite",
    "rev_i_salaires_formels": "salaire",
    }


class all_income_excluding_transfers(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Earned and Unearned Incomes of All Possible Sources and Excluding Government Transfers"

    def formula(household, period):
        income_variables = [
            "autres_revenus_du_capital",
            "revenu_non_salarie",
            "revenu_informel_agricole",
            "autres_revenus_informels",
            "revenu_locatif",
            "pension_retraite",
            "salaire",
            ]
        return household.sum(
            sum(
                household.members(variable, period)
                for variable in income_variables
                )
            )


class nontaxable_income(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "All nontaxable source of income"

    def formula(household, period):
        income_variables = [
            "revenu_informel_agricole",
            "autres_revenus_informels",
            ]
        return household.sum(
            sum(
                household.members(variable, period)
                for variable in income_variables
                )
            )


multi_country_custom_ceq_variables = [all_income_excluding_transfers, nontaxable_income]
