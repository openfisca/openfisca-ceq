# -*- coding: utf-8 -*-


from openfisca_core.model_api import Variable, YEAR
from openfisca_ceq.entities import Household


# Conversion depuis les variables listées dans openfisca-ceq/documentation/description_donnees_input.md

# 12 revenus
initial_revenues_source = set([
    "rev_i_agricoles",
    "rev_i_autoconsommation",
    "rev_i_autres_revenus_capital",
    "rev_i_autres_transferts",
    "rev_i_independants_Ntaxe",
    "rev_i_independants_taxe",
    "rev_i_loyers_imputes",
    "rev_i_loyers",
    "rev_i_pensions",
    "rev_i_salaires_formels",
    "rev_i_salaires_informels",
    "rev_i_transferts_publics",
    ])

ceq_input_by_person_variable = {
    "rev_i_autoconsommation": "autoconsumption",
    "rev_i_autres_transferts": "other_income",
    "rev_i_loyers_imputes": "imputed_rent",
    }

ceq_intermediate_by_person_variable = {
    "rev_i_transferts_publics": "direct_transfers"
    }

non_ceq_input_by_person_variable = {
    "rev_i_agricoles": "revenu_agricole",
    "rev_i_autres_revenus_capital": "autres_revenus_du_capital",
    "rev_i_independants_Ntaxe": "revenu_informel_non_salarie",
    "rev_i_independants_taxe": "revenu_non_salarie",
    "rev_i_loyers": "revenu_locatif",
    "rev_i_pensions": "pension_retraite",
    "rev_i_salaires_formels": "salaire",
    "rev_i_salaires_informels": "revenu_informel_salarie",
    }


assert initial_revenues_source == (set(ceq_input_by_person_variable.keys())
    .union(set(ceq_intermediate_by_person_variable.keys())
    ).union(set(non_ceq_input_by_person_variable.keys()))
    )


class all_income_excluding_transfers(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR
    label = "Earned and Unearned Incomes of All Possible Sources and Excluding Government Transfers"

    def formula(household, period):
        income_variables = [
            "autres_revenus_du_capital",
            "pension_retraite",
            "revenu_agricole",
            "revenu_informel_non_salarie",
            "revenu_informel_salarie"
            "revenu_locatif",
            "revenu_non_salarie",
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
            "revenu_informel_agricole",  # A construire
            "revenu_informel_non_salarie",
            "revenu_informel_salarie",
            # TODO
            ]
        return household.sum(
            sum(
                household.members(variable, period)
                for variable in income_variables
                )
            )

multi_country_custom_ceq_variables = [all_income_excluding_transfers, nontaxable_income]
