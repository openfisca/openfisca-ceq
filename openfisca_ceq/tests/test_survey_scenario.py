from openfisca_ceq.tools.survey_scenario import build_ceq_survey_scenario


def test():
    country = "senegal"
    survey_scenario = build_ceq_survey_scenario(legislation_country = country)
    assert survey_scenario is not None



