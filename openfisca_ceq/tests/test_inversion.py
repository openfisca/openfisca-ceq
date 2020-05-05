import logging
import numpy as np


from openfisca_ceq.tools.data import year_by_country
from openfisca_ceq.tools.survey_scenario import build_ceq_survey_scenario
from openfisca_ceq.tools.survey_scenario import tax_benefit_system_class_by_country

from openfisca_senegal.scenarios import init_single_entity


log = logging.getLogger(__name__)


def test_variable_inversion(country, test):
    CountryTaxBenefitSystem = tax_benefit_system_class_by_country[country]

    tax_benefit_system = CountryTaxBenefitSystem()
    period = year_by_country[country]

    scenario = tax_benefit_system.new_scenario()

    count = test["count"]
    value_min = test["value_min"]
    value_max = test["value_max"]
    input_variable = test["input_variable"]
    target_variable = test["target_variable"]

    init_single_entity(
        scenario,
        parent1 = dict(),
        axes = [[{
            'count': count,
            'min': value_min,
            'max': value_max,
            'name': input_variable,
            }]],
        period = period,
        )

    simulation = scenario.new_simulation()
    target = np.linspace(value_min, value_max, count)

    np.testing.assert_allclose(
        simulation.calculate(target_variable, period = period),
        target,
        rtol = 1e-6,
        atol = 1e-2,
        )


def test_survey_scenarios_variable_inversion(country, test):
    input_variable = test["input_variable"]
    target_variable = test["target_variable"]
    period = year_by_country[country]
    additionnal_variables = test.get("additionnal_variables", list())
    survey_scenario = build_ceq_survey_scenario(legislation_country = country, year = period)

    df = survey_scenario.create_data_frame_by_entity(
        variables = [target_variable, input_variable] + additionnal_variables,
        index = True, merge = True,
        )

    results = (df
        .eval("absolute_difference = abs({} - {})".format(
            input_variable, target_variable),
            )
        .sort_values("absolute_difference", ascending = False)
        .head(30)[[target_variable, input_variable, "absolute_difference"] + additionnal_variables]
        )

    np.testing.assert_allclose(
        survey_scenario.calculate_variable(target_variable, period = period),
        survey_scenario.calculate_variable(input_variable, period = period),
        rtol = 1e-6,
        atol = 1,
        err_msg = results
        )
    return results


if __name__ == '__main__':
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    tests_by_country = {
        "cote_d_ivoire": [
            {
                "count": 1000,
                "value_min": 0,
                "value_max": 5e6,
                "input_variable": "salaire",
                "target_variable": "salaire_net_a_payer",
                "additionnal_variables": ["nombre_enfants_a_charge"],
                }
            ],
        "mali": [
            {
                "count": 1000,
                "value_min": 0,
                "value_max": 5e6,
                "input_variable": "salaire",
                "target_variable": "salaire_net_a_payer",
                "additionnal_variables": ["nombre_enfants_a_charge"],
                }
            ],
        "senegal": [
            # {
            #     "count": 1000,
            #     "value_min": 0,
            #     "value_max": 5e6,
            #     "input_variable": "salaire",
            #     "target_variable": "salaire_net_a_payer",
            #     "additionnal_variables": ["revenu_foncier_brut", "pension_retraite", "nombre_de_parts"],
            #     },
            {
                "count": 1000,
                "value_min": 0,
                "value_max": 5e6,
                "input_variable": "pension_retraite",
                "target_variable": "pension_net_a_payer",
                "additionnal_variables": ["revenu_foncier_brut", "salaire", "nombre_de_parts"],
                },
            ],
        }

    country = "cote_d_ivoire"
    for test in tests_by_country[country]:
        # test_variable_inversion(country, test)
        results = test_survey_scenarios_variable_inversion(country, test)