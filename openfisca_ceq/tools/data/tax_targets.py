import logging
import pandas as pd


from openfisca_ceq.tools.data import config_parser
# from openfisca_ceq.tools.indirect_taxation.consumption_items_nomenclature import country_code_by_country
from openfisca_ceq.tools.survey_scenario import build_ceq_survey_scenario
from openfisca_ceq.tools.data import year_by_country


log = logging.getLogger(__name__)


variable_by_index = {
    'Total tax revenue': '',
    'Direct taxes': 'direct_taxes',
    'Personal Income Taxes': 'personal_income_tax',
    'Payroll Tax and social contributions': 'payroll_tax_and_social_contributions',
    'Corporate Income Tax': 'corporate_income_tax',
    'Other Direct Taxes': 'other_direct_taxes',
    'Indirect taxes': 'indirect_taxes',
    'VAT': 'value_added_tax',
    'Import Taxes': 'customs_duties',
    'Excise taxes': 'excise_taxes',
    'on Oil Derivates': '',
    'on alcohol, tabac and other non-oil derivatives': '',
    'Other Indirect Taxes': '',
    }


def build_simulated_results(survey_scenario, index):
    simulated_amounts = pd.Series(
        index = index,
        )
    for index, variable in variable_by_index.items():
        if variable in survey_scenario.tax_benefit_system.variables:
            simulated_amounts[index] = (
                survey_scenario.compute_aggregate(variable, period = survey_scenario.year) / 1e9
                )
    return simulated_amounts


def read_tax_target():
    # code_country = country_code_by_country[country]
    # year = year_by_country[country]
    country_label_by_country = {
        "mali": "Mali",
        "senegal": "Senegal",
        "cote_d_ivoire": "Cote d'Ivoire",
        }
    targets_file = config_parser.get("ceq", "targets_file")
    target = pd.read_excel(
        targets_file,
        sheet_name = "tableau_16",
        header = [0, 1],
        index_col = 0,
        )
    extraction = target.xs('Millions FCFA', level=1, axis=1)
    results = None
    for country, year in year_by_country.items():
        country_label = country_label_by_country[country]
        result = pd.DataFrame(columns = pd.MultiIndex(
            levels = [[country_label], ["actual", "direct", "inflated"]],
            codes = [[0, 0, 0], [0, 1, 2]],
            ))
        result[country_label, "actual"] = extraction[country_label].copy()

        survey_scenario = build_ceq_survey_scenario(legislation_country = country, year = year)
        simulated_amounts = build_simulated_results(survey_scenario, result.index)
        result[country_label, "direct"] = simulated_amounts

        survey_scenario = build_ceq_survey_scenario(legislation_country = country, year = year, inflate = True)
        simulated_amounts = build_simulated_results(survey_scenario, result.index)
        result[country_label, "inflated"] = simulated_amounts

        results = result if results is None else pd.concat([results, result], axis = 1)

    return results.round(1)

if __name__ == '__main__':
    read_tax_target()
