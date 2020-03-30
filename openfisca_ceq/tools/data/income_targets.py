import pandas as pd

from openfisca_ceq.tools.data import config_parser, year_by_country
from openfisca_ceq.tools.indirect_taxation.consumption_items_nomenclature import country_code_by_country
from openfisca_ceq.tools.survey_scenario import build_ceq_survey_scenario


country = "mali"
code_country = country_code_by_country[country]


targets_file = config_parser.get("ceq", "income_targets_file")


target = (pd.read_excel(targets_file)
    .query("Pays == @code_country")
    .query("Agrégat == 'VA brute'")
    ["Montants Cible"]
    )
assert len(target) == 1
print(target.values[0])


target = target.values[0]

year = year_by_country[country]
survey_scenario = build_ceq_survey_scenario(legislation_country = country, year = year)
period = survey_scenario.year

incomes = [
    "salaire_super_brut",
    "revenu_informel_non_salarie",
    "revenu_agricole",
    ]

aggregate = sum(
    survey_scenario.compute_aggregate(income, period = period)
    for income in incomes
    )
print(aggregate / 1e9)


inflator = target / (aggregate / 1e9)
inflator_by_variable = dict(
    (income, inflator)
    for income in incomes
    )

survey_scenario.inflate(inflator_by_variable = inflator_by_variable, period = period)
