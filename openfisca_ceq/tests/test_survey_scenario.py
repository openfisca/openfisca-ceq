import logging
import pytest


from openfisca_ceq.tools.data import year_by_country
from openfisca_ceq.tools.survey_scenario import build_ceq_survey_scenario


log = logging.getLogger(__name__)


@pytest.mark.parametrize("country, year", list(year_by_country.items()))
def test(country, year):
    survey_scenario = build_ceq_survey_scenario(legislation_country = country, year = year)
    assert survey_scenario is not None
    assert not survey_scenario.tax_benefit_system.variables['eleve_enseignement_niveau'].is_neutralized


if __name__ == '__main__':
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)
    country = "senegal"

    year = year_by_country[country]
    survey_scenario = build_ceq_survey_scenario(legislation_country = country, year = year)
    assert not survey_scenario.tax_benefit_system.variables['eleve_enseignement_niveau'].is_neutralized

    variables = [
        'tva_taux_normal',
        'tva',
        'value_added_tax',
        'indirect_taxes'
        ]
    for variable in variables:
        log.info(
            "{variable}: {aggregate} billions FCFA".format(
                variable = variable,
                aggregate = int(round(survey_scenario.compute_aggregate(variable, period = survey_scenario.year) / 1e9))
                )
            )
