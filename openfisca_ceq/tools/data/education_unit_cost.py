import logging
import pandas as pd
import os
from slugify import slugify


from openfisca_ceq.tools.indirect_taxation.consumption_items_nomenclature import assets_directory


log = logging.getLogger(__name__)


def build_unit_cost(country):
    df = pd.read_csv(
        os.path.join(assets_directory, "unit_cost_of_education_public_service_by_country.csv"
        ))
    print(df)
    return df

country = "senegal"
df = build_unit_cost(country)
