import logging
import pytest


from openfisca_ceq.tools.data import year_by_country
from openfisca_ceq.tools.survey_scenario import build_ceq_survey_scenario


log = logging.getLogger(__name__)


@pytest.mark.parametrize("country, year", list(year_by_country.items()))
def test(country, year):
    survey_scenario = build_ceq_survey_scenario(legislation_country = country, year = year)
    assert survey_scenario is not None


if __name__ == '__main__':
    country = "senegal"
    year = year_by_country[country]
    survey_scenario = build_ceq_survey_scenario(legislation_country = country, year = year)

    assert not survey_scenario.tax_benefit_system.variables['eleve_enseignement_niveau'].is_neutralized
    print(survey_scenario.compute_pivot_table(columns = 'eleve_enseignement_niveau', aggfunc = 'count', period = survey_scenario.year))
    print(survey_scenario.compute_aggregate('primary_education_person', period = survey_scenario.year))
    print(survey_scenario.compute_aggregate('primary_education', period = survey_scenario.year))
    print(survey_scenario.compute_aggregate('education_net_transfers', period = survey_scenario.year))
