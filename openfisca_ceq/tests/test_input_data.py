import pandas as pd
import pytest

from openfisca_ceq.tools.data import get_data_file_paths
from openfisca_ceq.tools.data import year_by_country


@pytest.mark.parametrize("country, year", list(year_by_country.items()))
def test_household_id_coherence(country, year):
    expenditures_data_path, income_data_path = get_data_file_paths(country, year)
    expenditures = pd.read_stata(expenditures_data_path).astype({"prod_id": str})
    income = pd.read_stata(income_data_path)
    print(
        len(
            set(expenditures.hh_id).difference(set(income.hh_id))
            )
        )
    print(
        len(
            set(income.hh_id).difference(set(expenditures.hh_id))
            )
        )
    # BIM
    # Sénégal: keep only household from income
    # Mali: manque 165 ménages


if __name__ == "__main__":
    country = "cote_d_ivoire"
    test_household_id_coherence(country, 2014)
