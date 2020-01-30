from openfisca_ceq.tools.survey_scenario import build_ceq_survey_scenario


def test():
    country = "senegal"
    year = 2011
    survey_scenario = build_ceq_survey_scenario(legislation_country = country, year = year)
    assert survey_scenario is not None
