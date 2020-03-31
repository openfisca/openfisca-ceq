import logging
import pandas as pd


from openfisca_ceq.tools.data import config_parser
from openfisca_ceq.tools.indirect_taxation.consumption_items_nomenclature import country_code_by_country


log = logging.getLogger(__name__)


def read_income_target(country):
    code_country = country_code_by_country[country]
    targets_file = config_parser.get("ceq", "income_targets_file")
    target = (
        pd.read_excel(targets_file)
        .query("Pays == @code_country")
        .query("Agrégat == 'VA brute'")
        ["Montants Cible"]
        .copy()
        )
    assert len(target) == 1
    target = target.values[0]
    log.info("Income target for {} is {} Billion CFA".format(country, target))
    del code_country
    return target * 1e9

